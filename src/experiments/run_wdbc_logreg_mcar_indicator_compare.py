from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin

from src.data_loading import load_wdbc
from src.data.splits import make_outer_cv_splits
from src.missingness import apply_mcar


def expected_calibration_error(y_true, y_prob, n_bins=10):
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        left = bin_edges[i]
        right = bin_edges[i + 1]

        if i == n_bins - 1:
            mask = (y_prob >= left) & (y_prob <= right)
        else:
            mask = (y_prob >= left) & (y_prob < right)

        if np.sum(mask) == 0:
            continue

        bin_acc = np.mean(y_true[mask])
        bin_conf = np.mean(y_prob[mask])
        bin_weight = np.mean(mask)

        ece += bin_weight * abs(bin_acc - bin_conf)

    return ece


class MissingIndicatorAppender(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.feature_names_in_ = list(X.columns)
        return self

    def transform(self, X):
        missing_flags = X.isna().astype(int)
        missing_flags.columns = [f"{c}_missing" for c in X.columns]
        return pd.concat([X.reset_index(drop=True), missing_flags.reset_index(drop=True)], axis=1)


def build_pipeline(variant):
    if variant == "simple":
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(C=1.0, solver="liblinear", max_iter=1000)),
            ]
        )

    if variant == "simple_plus_indicators":
        return Pipeline(
            steps=[
                ("append_indicators", MissingIndicatorAppender()),
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(C=1.0, solver="liblinear", max_iter=1000)),
            ]
        )

    raise ValueError(f"Unknown variant: {variant}")


def evaluate_pipeline(pipeline, X_train, X_test, y_train, y_test):
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "brier": brier_score_loss(y_test, y_prob),
        "ece": expected_calibration_error(y_test, y_prob, n_bins=10),
    }


def main():
    X, y, _ = load_wdbc()

    print("WDBC loaded")
    print("Original X shape:", X.shape)

    splits = make_outer_cv_splits(X, y, n_splits=5)
    rates = [0.1, 0.2, 0.3, 0.5]
    variants = ["simple", "simple_plus_indicators"]
    all_results = []

    for fold_idx, (train_idx, test_idx) in enumerate(splits):
        print(f"\n===== Fold {fold_idx} =====")

        X_train = X.iloc[train_idx].copy()
        X_test = X.iloc[test_idx].copy()
        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        clean_pipeline = build_pipeline("simple")
        clean_results = evaluate_pipeline(clean_pipeline, X_train, X_test, y_train, y_test)

        print(
            f"Clean baseline: Accuracy={clean_results['accuracy']:.4f}, "
            f"AUC={clean_results['roc_auc']:.4f}, "
            f"Brier={clean_results['brier']:.4f}, "
            f"ECE={clean_results['ece']:.4f}"
        )

        for rate in rates:
            rng_train = np.random.default_rng(42 + fold_idx)
            rng_test = np.random.default_rng(123 + fold_idx)

            X_train_mcar, _, train_meta = apply_mcar(X_train, rate=rate, rng=rng_train)
            X_test_mcar, _, test_meta = apply_mcar(X_test, rate=rate, rng=rng_test)

            for variant in variants:
                pipeline = build_pipeline(variant)
                results = evaluate_pipeline(pipeline, X_train_mcar, X_test_mcar, y_train, y_test)

                row = {
                    "dataset": "wdbc",
                    "model": "logistic_regression",
                    "mechanism": "mcar",
                    "variant": variant,
                    "fold": fold_idx,
                    "rate": rate,
                    "train_actual_rate": train_meta["actual_rate"],
                    "test_actual_rate": test_meta["actual_rate"],
                    "accuracy": results["accuracy"],
                    "roc_auc": results["roc_auc"],
                    "brier": results["brier"],
                    "ece": results["ece"],
                    "accuracy_change_vs_clean": results["accuracy"] - clean_results["accuracy"],
                    "roc_auc_change_vs_clean": results["roc_auc"] - clean_results["roc_auc"],
                    "brier_change_vs_clean": results["brier"] - clean_results["brier"],
                    "ece_change_vs_clean": results["ece"] - clean_results["ece"],
                }
                all_results.append(row)

                print(
                    f"  Rate={rate}, variant={variant}: "
                    f"AUC={row['roc_auc']:.4f}, "
                    f"Brier={row['brier']:.4f}, "
                    f"ECE={row['ece']:.4f}"
                )

    results_df = pd.DataFrame(all_results)

    summary_df = (
        results_df.groupby(["dataset", "model", "mechanism", "variant", "rate"], as_index=False)
        .agg(
            mean_accuracy=("accuracy", "mean"),
            std_accuracy=("accuracy", "std"),
            mean_roc_auc=("roc_auc", "mean"),
            std_roc_auc=("roc_auc", "std"),
            mean_brier=("brier", "mean"),
            std_brier=("brier", "std"),
            mean_ece=("ece", "mean"),
            std_ece=("ece", "std"),
            mean_accuracy_change_vs_clean=("accuracy_change_vs_clean", "mean"),
            mean_roc_auc_change_vs_clean=("roc_auc_change_vs_clean", "mean"),
            mean_brier_change_vs_clean=("brier_change_vs_clean", "mean"),
            mean_ece_change_vs_clean=("ece_change_vs_clean", "mean"),
        )
    )

    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    results_df.to_csv("results/metrics/wdbc_logreg_mcar_indicator_compare_metrics.csv", index=False)
    summary_df.to_csv("results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv", index=False)

    print("\nSaved:")
    print("- results/metrics/wdbc_logreg_mcar_indicator_compare_metrics.csv")
    print("- results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv")


if __name__ == "__main__":
    main()

