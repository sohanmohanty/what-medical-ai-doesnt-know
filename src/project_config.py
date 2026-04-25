"""Helpers for loading and validating project configuration files."""

from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"


def load_yaml(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_project_configs(config_dir: str | Path | None = None) -> dict:
    base_dir = Path(config_dir) if config_dir is not None else CONFIG_DIR

    def resolve_config_path(filename: str) -> Path:
        candidate = base_dir / filename
        if candidate.exists():
            return candidate
        return CONFIG_DIR / filename

    return {
        "datasets": load_yaml(resolve_config_path("datasets.yaml")).get("datasets", {}),
        "models": load_yaml(resolve_config_path("models.yaml")).get("models", {}),
        "imputers": load_yaml(resolve_config_path("imputers.yaml")).get("imputers", {}),
        "experiment": load_yaml(resolve_config_path("experiments.yaml")).get("experiment", {}),
    }


def select_named_entries(mapping: dict, requested_names: list[str] | None, label: str) -> dict:
    if not requested_names:
        return mapping

    missing = [name for name in requested_names if name not in mapping]
    if missing:
        raise ValueError(f"Unknown {label}: {', '.join(missing)}")

    return {name: mapping[name] for name in requested_names}


def merge_schema_with_feature_types(schema: dict, feature_types: dict | None, all_columns=None) -> dict:
    merged = deepcopy(schema or {})
    feature_types = feature_types or {}

    numeric_columns = list(
        feature_types.get("numeric_columns", merged.get("numeric_columns", merged.get("numeric_features", [])))
    )
    binary_columns = list(
        feature_types.get("binary_columns", merged.get("binary_columns", merged.get("binary_features", [])))
    )
    categorical_columns = list(
        feature_types.get(
            "categorical_columns",
            merged.get("categorical_columns", merged.get("categorical_features", [])),
        )
    )

    assigned = set(numeric_columns) | set(binary_columns) | set(categorical_columns)
    if all_columns is not None:
        for column in all_columns:
            if column not in assigned:
                numeric_columns.append(column)

    merged.update(
        {
            "numeric_columns": numeric_columns,
            "binary_columns": binary_columns,
            "categorical_columns": categorical_columns,
            "numeric_features": numeric_columns,
            "binary_features": binary_columns,
            "categorical_features": categorical_columns,
        }
    )
    return merged


def override_output_paths(
    experiment_config: dict,
    run_name: str | None = None,
    output_namespace: str | None = None,
) -> dict:
    outputs = deepcopy(experiment_config.get("outputs", {}))
    base_name = experiment_config.get("name", "experiment")

    if output_namespace is None:
        output_namespace = "official" if not run_name or run_name == base_name else "user"

    if output_namespace == "official" and (not run_name or run_name == base_name):
        return outputs

    if output_namespace in {"sample", "user"}:
        folder = "samples" if output_namespace == "sample" else "user_runs"
        run_name = run_name or base_name
        return {
            "metrics_path": str(Path("results") / folder / run_name / "metrics.csv"),
            "summary_path": str(Path("results") / folder / run_name / "summary.csv"),
            "predictions_path": str(Path("results") / folder / run_name / "predictions.csv"),
            "manifest_path": str(Path("results") / folder / run_name / "run_manifest.json"),
            "masks_dir": str(Path("results") / folder / run_name / "masks"),
            "figures_dir": str(Path("figures") / folder / run_name),
        }

    adjusted = {}
    for key, raw_path in outputs.items():
        path = Path(raw_path)
        if key.endswith("_dir"):
            new_name = path.name.replace(base_name, run_name, 1) if base_name in path.name else run_name
            adjusted[key] = str(path.parent / new_name)
            continue

        new_stem = path.stem.replace(base_name, run_name, 1) if base_name in path.stem else f"{run_name}_{path.stem}"
        adjusted[key] = str(path.with_name(f"{new_stem}{path.suffix}"))

    return adjusted
