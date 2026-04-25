from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.data_loading import load_statlog_heart
from src.data.splits import make_outer_cv_splits
from src.missingness import apply_mcar


def build_pipeline():
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("model", HistGradientBoostingClassifier(learning_rate=0.05, max_iter=200, random_state=42)),
        ]
    )


def evaluate_pipeline(pipeline, X_train, X_test, y_train, y_test):
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "brier": brier_score_loss(y_test, y_prob),
    }


def main():
    X, y, _ = load_statlog_heart()
    splits = make_outer_cv_splits(X, y, n_splits=5)
    rates = [0.1, 0.2, 0.3, 0.5]
    all_results = []

    for fold_idx, (train_idx, test_idx) in enumerate(splits):
        X_train = X.iloc[train_idx].copy()
        X_test = X.iloc[test_idx].copy()
        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        clean_results = evaluate_pipeline(build_pipeline(), X_train, X_test, y_train, y_test)

        for rate in rates:
            rng_train = np.random.default_rng(42 + fold_idx)
            rng_test = np.random.default_rng(123 + fold_idx)

            X_train_masked, _, train_meta = apply_mcar(X_train, rate=rate, rng=rng_train)
            X_test_masked, _, test_meta = apply_mcar(X_test, rate=rate, rng=rng_test)

            results = evaluate_pipeline(build_pipeline(), X_train_masked, X_test_masked, y_train, y_test)

            all_results.append({
                "dataset": "statlog_heart",
                "model": "gradient_boosting",
                "mechanism": "mcar",
                "fold": fold_idx,
                "rate": rate,
                "train_actual_rate": train_meta["actual_rate"],
                "test_actual_rate": test_meta["actual_rate"],
                "accuracy": results["accuracy"],
                "roc_auc": results["roc_auc"],
                "brier": results["brier"],
                "accuracy_change": results["accuracy"] - clean_results["accuracy"],
                "roc_auc_change": results["roc_auc"] - clean_results["roc_auc"],
                "brier_change": results["brier"] - clean_results["brier"],
            })

    results_df = pd.DataFrame(all_results)
    summary_df = results_df.groupby(["dataset", "model", "mechanism", "rate"], as_index=False).agg(
        mean_accuracy=("accuracy", "mean"),
        std_accuracy=("accuracy", "std"),
        mean_roc_auc=("roc_auc", "mean"),
        std_roc_auc=("roc_auc", "std"),
        mean_brier=("brier", "mean"),
        std_brier=("brier", "std"),
        mean_accuracy_change=("accuracy_change", "mean"),
        mean_roc_auc_change=("roc_auc_change", "mean"),
        mean_brier_change=("brier_change", "mean"),
    )

    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    results_df.to_csv("results/metrics/statlog_gb_mcar_5fold_metrics.csv", index=False)
    summary_df.to_csv("results/metrics/statlog_gb_mcar_5fold_summary.csv", index=False)

    print("Saved:")
    print("- results/metrics/statlog_gb_mcar_5fold_metrics.csv")
    print("- results/metrics/statlog_gb_mcar_5fold_summary.csv")


if __name__ == "__main__":
    main()

