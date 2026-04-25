"""Unified config-driven experiment runner for the missingness study."""

from __future__ import annotations

import argparse
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.exceptions import ConvergenceWarning

from src.data.schemas import save_schema
from src.data.splits import make_inner_cv, make_repeated_outer_cv_splits
from src.data_loading import load_statlog_heart, load_wdbc
from src.evaluation import compute_binary_classification_metrics
from src.imputers import get_numeric_imputer_param_grid
from src.missingness import apply_mar, apply_mcar, apply_mnar
from src.models import build_model, get_model_param_grid, model_uses_scaling
from src.plotting import save_run_summary_figure
from src.preprocessing import build_preprocessor
from src.project_config import (
    load_project_configs,
    merge_schema_with_feature_types,
    override_output_paths,
    select_named_entries,
)


LOADER_REGISTRY = {
    "load_wdbc": load_wdbc,
    "load_statlog_heart": load_statlog_heart,
}


def _log(message: str):
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def _configure_warnings(show_convergence_warnings: bool):
    if show_convergence_warnings:
        return

    warnings.filterwarnings(
        "ignore",
        message=r"\[IterativeImputer\] Early stopping criterion not reached\.",
        category=ConvergenceWarning,
        module=r"sklearn\.impute\._iterative",
    )


def _rate_label(rate: float) -> str:
    return str(rate).replace(".", "p")


def _resolve_dataset(name: str, dataset_spec: dict):
    loader_name = dataset_spec["loader_name"]
    if loader_name not in LOADER_REGISTRY:
        raise ValueError(f"Unknown loader: {loader_name}")

    X, y, schema = LOADER_REGISTRY[loader_name]()
    schema = merge_schema_with_feature_types(schema, dataset_spec.get("feature_types"), all_columns=X.columns)
    return X, y, schema


def _build_masked_frame(X_df: pd.DataFrame, mechanism: str, rate: float, seed: int, profile: dict):
    rng = np.random.default_rng(seed)

    if mechanism == "mcar":
        feature_subset = profile.get("feature_subset")
        if feature_subset == "all":
            feature_subset = list(X_df.columns)
        return apply_mcar(X_df, rate=rate, rng=rng, feature_subset=feature_subset)

    if mechanism == "mar":
        return apply_mar(
            X_df,
            rate=rate,
            rng=rng,
            target_features=profile["target_features"],
            anchor_feature=profile["anchor_feature"],
            beta=profile.get("beta", 1.0),
        )

    if mechanism == "mnar":
        return apply_mnar(
            X_df,
            rate=rate,
            rng=rng,
            target_features=profile["target_features"],
            beta=profile.get("beta", 1.0),
        )

    raise ValueError(f"Unknown mechanism: {mechanism}")


def _build_pipeline(schema: dict, model_name: str, model_spec: dict, imputer_name: str, imputer_spec: dict):
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(
                    schema=schema,
                    scale_numeric=model_uses_scaling(model_name, model_spec),
                    imputer_name=imputer_name,
                    imputer_spec=imputer_spec,
                ),
            ),
            ("model", build_model(model_name, model_spec=model_spec)),
        ]
    )


def _fit_estimator(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    schema: dict,
    model_name: str,
    model_spec: dict,
    imputer_name: str,
    imputer_spec: dict,
    tuning_enabled: bool,
    inner_folds: int,
    tuning_metric: str,
    tuning_n_jobs: int,
    random_state: int,
):
    pipeline = _build_pipeline(schema, model_name, model_spec, imputer_name, imputer_spec)
    param_grid = {}
    param_grid.update(get_model_param_grid(model_name, model_spec))
    param_grid.update(get_numeric_imputer_param_grid(imputer_name, imputer_spec))

    if tuning_enabled and param_grid:
        search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring=tuning_metric,
            cv=make_inner_cv(n_splits=inner_folds, random_state=random_state),
            n_jobs=tuning_n_jobs,
            refit=True,
        )
        search.fit(X_train, y_train)
        return search.best_estimator_, search.best_params_

    pipeline.fit(X_train, y_train)
    return pipeline, {}


def _extract_selected_params(estimator: Pipeline) -> dict:
    payload = {
        "model": estimator.named_steps["model"].get_params(deep=False),
    }

    preprocessor = estimator.named_steps["preprocessor"]
    numeric_transformer = preprocessor.named_transformers_.get("num")
    binary_transformer = preprocessor.named_transformers_.get("bin")
    categorical_transformer = preprocessor.named_transformers_.get("cat")

    if hasattr(numeric_transformer, "named_steps"):
        payload["numeric_imputer"] = numeric_transformer.named_steps["imputer"].get_params(deep=False)
    if hasattr(binary_transformer, "named_steps"):
        payload["binary_imputer"] = binary_transformer.named_steps["imputer"].get_params(deep=False)
    if hasattr(categorical_transformer, "named_steps"):
        payload["categorical_imputer"] = categorical_transformer.named_steps["imputer"].get_params(deep=False)

    return payload


def _predict_binary(estimator: Pipeline, X_test: pd.DataFrame):
    y_prob = estimator.predict_proba(X_test)[:, 1]
    y_pred = estimator.predict(X_test)
    return y_pred, y_prob


def _evaluate_estimator(estimator: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, calibration_bins: int):
    y_pred, y_prob = _predict_binary(estimator, X_test)
    metrics = compute_binary_classification_metrics(
        y_true=y_test,
        y_pred=y_pred,
        y_prob=y_prob,
        n_bins=calibration_bins,
    )
    return metrics, y_pred, y_prob


def _build_predictions_table(index, y_true, y_pred, y_prob, metadata: dict) -> pd.DataFrame:
    payload = {
        "sample_index": list(index),
        "y_true": list(np.asarray(y_true)),
        "y_pred": list(np.asarray(y_pred)),
        "y_prob": list(np.asarray(y_prob)),
    }
    payload.update({key: [value] * len(index) for key, value in metadata.items()})
    return pd.DataFrame(payload)


def _save_mask(mask_df: pd.DataFrame, masks_root: Path, metadata: dict, split_label: str) -> str:
    subdir = (
        masks_root
        / metadata["dataset"]
        / metadata["model"]
        / metadata["imputer"]
        / metadata["regime"]
        / metadata["mechanism"]
        / f"rate_{_rate_label(metadata['rate'])}"
        / f"seed_{metadata['seed']}"
    )
    subdir.mkdir(parents=True, exist_ok=True)

    path = subdir / f"repeat_{metadata['repeat']:02d}_fold_{metadata['fold']:02d}_{split_label}_mask.csv.gz"
    mask_to_save = mask_df.copy()
    mask_to_save.insert(0, "row_index", mask_to_save.index)
    mask_to_save.to_csv(path, index=False, compression="gzip")
    return str(path)


def _summarize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["dataset", "model", "imputer", "regime", "mechanism", "rate"]

    return (
        df.groupby(group_cols, as_index=False)
        .agg(
            n_runs=("accuracy", "size"),
            mean_accuracy=("accuracy", "mean"),
            std_accuracy=("accuracy", "std"),
            mean_roc_auc=("roc_auc", "mean"),
            std_roc_auc=("roc_auc", "std"),
            mean_brier=("brier", "mean"),
            std_brier=("brier", "std"),
            mean_ece=("ece", "mean"),
            std_ece=("ece", "std"),
            mean_clean_accuracy=("clean_accuracy", "mean"),
            mean_clean_roc_auc=("clean_roc_auc", "mean"),
            mean_clean_brier=("clean_brier", "mean"),
            mean_clean_ece=("clean_ece", "mean"),
            mean_accuracy_change=("accuracy_change", "mean"),
            mean_roc_auc_change=("roc_auc_change", "mean"),
            mean_brier_change=("brier_change", "mean"),
            mean_ece_change=("ece_change", "mean"),
            mean_train_actual_rate=("train_actual_rate", "mean"),
            mean_test_actual_rate=("test_actual_rate", "mean"),
        )
    )


def _build_manifest(
    run_name: str,
    experiment_config: dict,
    outputs: dict,
    selected_datasets: dict,
    selected_models: dict,
    selected_imputers: dict,
    selected_mechanisms: list[str],
    selected_rates: list[float],
    selected_regimes: list[str],
    selected_seeds: list[int],
    executed_outer_splits: int,
    metrics_df: pd.DataFrame,
    predictions_df: pd.DataFrame,
    figure_paths: list[str],
) -> dict:
    return {
        "run_name": run_name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "experiment": experiment_config,
        "selected": {
            "datasets": list(selected_datasets.keys()),
            "models": list(selected_models.keys()),
            "imputers": list(selected_imputers.keys()),
            "mechanisms": selected_mechanisms,
            "rates": selected_rates,
            "train_test_regimes": selected_regimes,
            "random_seeds": selected_seeds,
            "executed_outer_splits": executed_outer_splits,
        },
        "outputs": outputs,
        "row_counts": {
            "metrics_rows": int(len(metrics_df)),
            "prediction_rows": int(len(predictions_df)),
        },
        "figure_paths": figure_paths,
    }


def _sanitize_slug(value: str) -> str:
    return value.replace("/", "_").replace("\\", "_").replace(" ", "_")


def _generate_run_figures(summary_df: pd.DataFrame, figures_dir: Path, run_name: str) -> list[str]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    figure_paths = []

    group_cols = ["dataset", "model", "imputer", "regime"]
    for keys, group_df in summary_df.groupby(group_cols, sort=True):
        dataset_name, model_name, imputer_name, regime_name = keys
        filename = "__".join(
            [
                _sanitize_slug(dataset_name),
                _sanitize_slug(model_name),
                _sanitize_slug(imputer_name),
                _sanitize_slug(regime_name),
                "summary.png",
            ]
        )
        output_path = figures_dir / filename
        title = (
            f"{run_name}: {dataset_name} | {model_name} | "
            f"{imputer_name} | {regime_name}"
        )
        save_run_summary_figure(group_df, str(output_path), title)
        figure_paths.append(str(output_path))

    return figure_paths


def _build_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", default="configs")
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--output-namespace", choices=["official", "sample", "user"], default=None)
    parser.add_argument("--datasets", nargs="*")
    parser.add_argument("--models", nargs="*")
    parser.add_argument("--imputers", nargs="*")
    parser.add_argument("--mechanisms", nargs="*")
    parser.add_argument("--rates", nargs="*", type=float)
    parser.add_argument("--regimes", nargs="*")
    parser.add_argument("--max-outer-splits", type=int, default=None)
    parser.add_argument("--max-seeds", type=int, default=None)
    parser.add_argument("--no-tuning", action="store_true")
    parser.add_argument("--no-save-masks", action="store_true")
    parser.add_argument("--no-save-predictions", action="store_true")
    parser.add_argument("--no-save-figures", action="store_true")
    parser.add_argument("--show-convergence-warnings", action="store_true")
    parser.add_argument("--progress-every", type=int, default=50)
    return parser


def main():
    run_started_at = perf_counter()
    args = _build_arg_parser().parse_args()
    _configure_warnings(args.show_convergence_warnings)
    configs = load_project_configs(args.config_dir)
    experiment_config = configs["experiment"]
    run_name = args.run_name or experiment_config.get("name", "configured_experiment")
    outputs = override_output_paths(
        experiment_config,
        run_name=run_name,
        output_namespace=args.output_namespace,
    )

    dataset_names = args.datasets or list(experiment_config.get("datasets", configs["datasets"].keys()))
    model_names = args.models or list(experiment_config.get("models", configs["models"].keys()))
    imputer_names = args.imputers or list(experiment_config.get("imputers", configs["imputers"].keys()))

    selected_datasets = select_named_entries(configs["datasets"], dataset_names, "datasets")
    selected_models = select_named_entries(configs["models"], model_names, "models")
    selected_imputers = select_named_entries(configs["imputers"], imputer_names, "imputers")

    mechanisms = args.mechanisms or list(experiment_config["missingness"]["mechanisms"])
    rates = args.rates or list(experiment_config["missingness"]["rates"])
    regimes = args.regimes or list(experiment_config["train_test_regimes"])
    seeds = list(experiment_config["missingness"]["random_seeds"])

    if args.max_seeds is not None:
        seeds = seeds[: args.max_seeds]

    tuning_enabled = bool(experiment_config["cv"].get("hyperparameter_tuning", False)) and not args.no_tuning
    save_predictions = bool(experiment_config["evaluation"].get("save_probabilities", True)) and not args.no_save_predictions
    save_masks = bool(experiment_config["evaluation"].get("save_masks", True)) and not args.no_save_masks
    save_figures = not args.no_save_figures
    calibration_bins = int(experiment_config["evaluation"].get("calibration_bins", 10))
    progress_every = max(1, int(args.progress_every))

    metrics_rows = []
    prediction_tables = []

    metrics_path = Path(outputs["metrics_path"])
    summary_path = Path(outputs["summary_path"])
    predictions_path = Path(outputs["predictions_path"])
    manifest_path = Path(outputs["manifest_path"])
    masks_dir = Path(outputs["masks_dir"])
    figures_dir = Path(outputs["figures_dir"])

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    if save_masks:
        masks_dir.mkdir(parents=True, exist_ok=True)
    if save_figures:
        figures_dir.mkdir(parents=True, exist_ok=True)

    outer_cv_config = experiment_config["cv"]
    executed_outer_splits = 0
    planned_splits_per_dataset = int(outer_cv_config.get("outer_folds", 5)) * int(outer_cv_config.get("repeats", 1))
    if args.max_outer_splits is not None:
        planned_splits_per_dataset = min(planned_splits_per_dataset, args.max_outer_splits)

    total_expected_rows = (
        len(selected_datasets)
        * planned_splits_per_dataset
        * len(selected_models)
        * len(selected_imputers)
        * len(mechanisms)
        * len(rates)
        * len(seeds)
        * len(regimes)
    )
    total_expected_clean_fits = (
        len(selected_datasets)
        * planned_splits_per_dataset
        * len(selected_models)
        * len(selected_imputers)
    )
    completed_rows = 0
    completed_clean_fits = 0

    _log(
        "Starting configured experiment "
        f"'{run_name}' with {len(selected_datasets)} dataset(s), "
        f"{len(selected_models)} model(s), {len(selected_imputers)} imputer(s), "
        f"{planned_splits_per_dataset} outer split(s) per dataset, "
        f"and approximately {total_expected_rows:,} result row(s)."
    )

    for dataset_name, dataset_spec in selected_datasets.items():
        _log(f"Loading dataset '{dataset_name}'")
        X, y, schema = _resolve_dataset(dataset_name, dataset_spec)

        schema_payload = {
            "dataset": dataset_name,
            "n_rows": int(X.shape[0]),
            "n_features": int(X.shape[1]),
            "feature_names": list(X.columns),
            "target_dtype": str(y.dtype),
            "task_type": dataset_spec.get("task_type", "binary_classification"),
            **schema,
        }
        save_schema(schema_payload, dataset_spec["schema_output"])

        splits = make_repeated_outer_cv_splits(
            X,
            y,
            n_splits=int(outer_cv_config.get("outer_folds", 5)),
            n_repeats=int(outer_cv_config.get("repeats", 1)),
            random_state=42,
        )
        if args.max_outer_splits is not None:
            splits = splits[: args.max_outer_splits]

        _log(
            f"Loaded dataset '{dataset_name}' with {X.shape[0]} rows, {X.shape[1]} features, "
            f"and {len(splits)} outer split(s) to execute."
        )

        for split_number, split in enumerate(splits, start=1):
            executed_outer_splits += 1
            repeat_idx = split["repeat"]
            fold_idx = split["fold"]
            train_idx = split["train_idx"]
            test_idx = split["test_idx"]

            _log(
                f"[{dataset_name}] Starting outer split {split_number}/{len(splits)} "
                f"(repeat {repeat_idx + 1}, fold {fold_idx + 1})"
            )

            X_train_clean = X.iloc[train_idx].copy()
            X_test_clean = X.iloc[test_idx].copy()
            y_train = y.iloc[train_idx].copy()
            y_test = y.iloc[test_idx].copy()

            clean_train_mask = pd.DataFrame(False, index=X_train_clean.index, columns=X_train_clean.columns)

            for model_name, model_spec in selected_models.items():
                for imputer_name, imputer_spec in selected_imputers.items():
                    completed_clean_fits += 1
                    clean_fit_started_at = perf_counter()
                    _log(
                        f"[{dataset_name}] Fitting clean estimator {completed_clean_fits}/"
                        f"{total_expected_clean_fits}: model={model_name}, imputer={imputer_name}, "
                        f"split {split_number}/{len(splits)}"
                    )
                    clean_estimator, clean_search_params = _fit_estimator(
                        X_train=X_train_clean,
                        y_train=y_train,
                        schema=schema,
                        model_name=model_name,
                        model_spec=model_spec,
                        imputer_name=imputer_name,
                        imputer_spec=imputer_spec,
                        tuning_enabled=tuning_enabled,
                        inner_folds=int(outer_cv_config.get("inner_folds", 3)),
                        tuning_metric=outer_cv_config.get("tuning_metric", "roc_auc"),
                        tuning_n_jobs=int(outer_cv_config.get("tuning_n_jobs", 1)),
                        random_state=42 + repeat_idx * 100 + fold_idx,
                    )
                    clean_metrics, _, _ = _evaluate_estimator(
                        estimator=clean_estimator,
                        X_test=X_test_clean,
                        y_test=y_test,
                        calibration_bins=calibration_bins,
                    )
                    clean_selected_params = _extract_selected_params(clean_estimator)
                    _log(
                        f"[{dataset_name}] Clean estimator ready for model={model_name}, "
                        f"imputer={imputer_name} in {perf_counter() - clean_fit_started_at:.1f}s "
                        f"(clean ROC-AUC={clean_metrics['roc_auc']:.4f}, "
                        f"clean Brier={clean_metrics['brier']:.4f})"
                    )

                    for mechanism in mechanisms:
                        mechanism_started_at = perf_counter()
                        if mechanism not in dataset_spec.get("missingness_profiles", {}):
                            raise ValueError(f"Dataset {dataset_name} is missing a {mechanism} profile.")

                        mechanism_profile = dataset_spec["missingness_profiles"][mechanism]

                        for rate in rates:
                            for seed in seeds:
                                test_seed = seed + repeat_idx * 1_000 + fold_idx * 100 + 17
                                train_seed = seed + repeat_idx * 1_000 + fold_idx * 100 + 53

                                X_test_masked, test_mask, test_meta = _build_masked_frame(
                                    X_df=X_test_clean,
                                    mechanism=mechanism,
                                    rate=rate,
                                    seed=test_seed,
                                    profile=mechanism_profile,
                                )

                                for regime in regimes:
                                    if regime == "clean_train_corrupt_test":
                                        X_train_fit = X_train_clean
                                        estimator = clean_estimator
                                        selected_params = clean_selected_params
                                        search_params = clean_search_params
                                        train_mask = clean_train_mask
                                        train_meta = {
                                            "actual_rate": 0.0,
                                        }
                                    elif regime == "corrupt_train_corrupt_test":
                                        X_train_masked, train_mask, train_meta = _build_masked_frame(
                                            X_df=X_train_clean,
                                            mechanism=mechanism,
                                            rate=rate,
                                            seed=train_seed,
                                            profile=mechanism_profile,
                                        )
                                        X_train_fit = X_train_masked
                                        estimator, search_params = _fit_estimator(
                                            X_train=X_train_fit,
                                            y_train=y_train,
                                            schema=schema,
                                            model_name=model_name,
                                            model_spec=model_spec,
                                            imputer_name=imputer_name,
                                            imputer_spec=imputer_spec,
                                            tuning_enabled=tuning_enabled,
                                            inner_folds=int(outer_cv_config.get("inner_folds", 3)),
                                            tuning_metric=outer_cv_config.get("tuning_metric", "roc_auc"),
                                            tuning_n_jobs=int(outer_cv_config.get("tuning_n_jobs", 1)),
                                            random_state=142 + repeat_idx * 100 + fold_idx + seed,
                                        )
                                        selected_params = _extract_selected_params(estimator)
                                    else:
                                        raise ValueError(f"Unknown regime: {regime}")

                                    metrics, y_pred, y_prob = _evaluate_estimator(
                                        estimator=estimator,
                                        X_test=X_test_masked,
                                        y_test=y_test,
                                        calibration_bins=calibration_bins,
                                    )

                                    mask_metadata = {
                                        "dataset": dataset_name,
                                        "model": model_name,
                                        "imputer": imputer_name,
                                        "regime": regime,
                                        "mechanism": mechanism,
                                        "rate": rate,
                                        "seed": seed,
                                        "repeat": repeat_idx,
                                        "fold": fold_idx,
                                    }
                                    train_mask_path = ""
                                    test_mask_path = ""
                                    if save_masks:
                                        train_mask_path = _save_mask(train_mask, masks_dir, mask_metadata, "train")
                                        test_mask_path = _save_mask(test_mask, masks_dir, mask_metadata, "test")

                                    row = {
                                        "run_name": run_name,
                                        "dataset": dataset_name,
                                        "model": model_name,
                                        "imputer": imputer_name,
                                        "regime": regime,
                                        "mechanism": mechanism,
                                        "rate": rate,
                                        "seed": seed,
                                        "repeat": repeat_idx,
                                        "fold": fold_idx,
                                        "train_size": int(len(train_idx)),
                                        "test_size": int(len(test_idx)),
                                        "train_actual_rate": float(train_meta.get("actual_rate", 0.0)),
                                        "test_actual_rate": float(test_meta.get("actual_rate", 0.0)),
                                        "accuracy": metrics["accuracy"],
                                        "roc_auc": metrics["roc_auc"],
                                        "brier": metrics["brier"],
                                        "ece": metrics["ece"],
                                        "clean_accuracy": clean_metrics["accuracy"],
                                        "clean_roc_auc": clean_metrics["roc_auc"],
                                        "clean_brier": clean_metrics["brier"],
                                        "clean_ece": clean_metrics["ece"],
                                        "accuracy_change": metrics["accuracy"] - clean_metrics["accuracy"],
                                        "roc_auc_change": metrics["roc_auc"] - clean_metrics["roc_auc"],
                                        "brier_change": metrics["brier"] - clean_metrics["brier"],
                                        "ece_change": metrics["ece"] - clean_metrics["ece"],
                                        "tuning_enabled": tuning_enabled,
                                        "inner_folds": int(outer_cv_config.get("inner_folds", 3)),
                                        "tuning_metric": outer_cv_config.get("tuning_metric", "roc_auc"),
                                        "search_best_params_json": json.dumps(search_params, sort_keys=True),
                                        "selected_params_json": json.dumps(selected_params, sort_keys=True, default=str),
                                        "train_mask_path": train_mask_path,
                                        "test_mask_path": test_mask_path,
                                    }
                                    metrics_rows.append(row)
                                    completed_rows += 1

                                    if (
                                        completed_rows == 1
                                        or completed_rows % progress_every == 0
                                        or completed_rows == total_expected_rows
                                    ):
                                        _log(
                                            f"Progress {completed_rows:,}/{total_expected_rows:,} "
                                            f"({completed_rows / total_expected_rows:.1%}) "
                                            f"- dataset={dataset_name}, model={model_name}, "
                                            f"imputer={imputer_name}, mechanism={mechanism.upper()}, "
                                            f"rate={rate}, seed={seed}, regime={regime}, "
                                            f"repeat={repeat_idx + 1}, fold={fold_idx + 1}"
                                        )

                                    if save_predictions:
                                        prediction_metadata = {
                                            "run_name": run_name,
                                            "dataset": dataset_name,
                                            "model": model_name,
                                            "imputer": imputer_name,
                                            "regime": regime,
                                            "mechanism": mechanism,
                                            "rate": rate,
                                            "seed": seed,
                                            "repeat": repeat_idx,
                                            "fold": fold_idx,
                                        }
                                        prediction_tables.append(
                                            _build_predictions_table(
                                                index=X_test_masked.index,
                                                y_true=y_test,
                                                y_pred=y_pred,
                                                y_prob=y_prob,
                                                metadata=prediction_metadata,
                                            )
                                        )

                        _log(
                            f"[{dataset_name}] Completed mechanism {mechanism.upper()} for "
                            f"model={model_name}, imputer={imputer_name}, split {split_number}/{len(splits)} "
                            f"in {perf_counter() - mechanism_started_at:.1f}s"
                        )

    if not metrics_rows:
        raise RuntimeError("No experiment rows were produced. Check the requested filters.")

    metrics_df = pd.DataFrame(metrics_rows)
    summary_df = _summarize_metrics(metrics_df)
    predictions_df = (
        pd.concat(prediction_tables, ignore_index=True)
        if prediction_tables
        else pd.DataFrame(columns=["sample_index", "y_true", "y_pred", "y_prob"])
    )

    metrics_df.to_csv(metrics_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    if save_predictions:
        predictions_df.to_csv(predictions_path, index=False)

    figure_paths = _generate_run_figures(summary_df, figures_dir, run_name) if save_figures else []

    manifest = _build_manifest(
        run_name=run_name,
        experiment_config=experiment_config,
        outputs=outputs,
        selected_datasets=selected_datasets,
        selected_models=selected_models,
        selected_imputers=selected_imputers,
        selected_mechanisms=mechanisms,
        selected_rates=rates,
        selected_regimes=regimes,
        selected_seeds=seeds,
        executed_outer_splits=executed_outer_splits,
        metrics_df=metrics_df,
        predictions_df=predictions_df,
        figure_paths=figure_paths,
    )
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    print(f"Saved metrics to {metrics_path}")
    print(f"Saved summary to {summary_path}")
    if save_predictions:
        print(f"Saved predictions to {predictions_path}")
    print(f"Saved manifest to {manifest_path}")
    if save_masks:
        print(f"Saved masks under {masks_dir}")
    if save_figures:
        print(f"Saved figures under {figures_dir}")
    _log(f"Configured experiment '{run_name}' finished in {perf_counter() - run_started_at:.1f}s")


if __name__ == "__main__":
    main()
