"""
WDBC gradient boosting under 5-fold MCAR.
Saves:
- results/metrics/wdbc_gb_mcar_5fold_metrics.csv
- results/metrics/wdbc_gb_mcar_5fold_summary.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, brier_score_loss

from src.data_loading import load_wdbc
from src.data.splits import make_outer_cv_splits
from src.preprocessing import build_preprocessor
from src.missingness import apply_mcar


def evaluate_pipeline(X_train, X_test, y_train, y_test, schema):
    preprocessor = build_preprocessor(schema, scale_numeric=False)

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    model = HistGradientBoostingClassifier(random_state=42)
    model.fit(X_train_processed, y_train)

    y_pred = model.predict(X_test_processed)
    y_prob = model.predict_proba(X_test_processed)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    brier = brier_score_loss(y_test, y_prob)

    return {
        "accuracy": accuracy,
        "roc_auc": auc,
        "brier": brier,
    }


def main():
    X, y, schema = load_wdbc()

    print("WDBC loaded")
    print("Original X shape:", X.shape)

    splits = make_outer_cv_splits(X, y, n_splits=5)
    rates = [0.1, 0.2, 0.3, 0.5]

    all_results = []

    for fold_idx, (train_idx, test_idx) in enumerate(splits):
        print(f"\n===== Fold {fold_idx} =====")

        X_train = X.iloc[train_idx].copy()
        X_test = X.iloc[test_idx].copy()
        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        clean_results = evaluate_pipeline(X_train, X_test, y_train, y_test, schema)

        print(
            f"Clean: Accuracy={clean_results['accuracy']:.4f}, "
            f"AUC={clean_results['roc_auc']:.4f}, "
            f"Brier={clean_results['brier']:.4f}"
        )

        for rate in rates:
            rng_train = np.random.default_rng(42 + fold_idx)
            rng_test = np.random.default_rng(123 + fold_idx)

            X_train_masked, _, train_meta = apply_mcar(X_train, rate=rate, rng=rng_train)
            X_test_masked, _, test_meta = apply_mcar(X_test, rate=rate, rng=rng_test)

            corrupted_results = evaluate_pipeline(X_train_masked, X_test_masked, y_train, y_test, schema)

            row = {
                "dataset": "wdbc",
                "model": "gradient_boosting",
                "mechanism": "mcar",
                "fold": fold_idx,
                "rate": rate,
                "train_actual_rate": train_meta["actual_rate"],
                "test_actual_rate": test_meta["actual_rate"],
                "clean_accuracy": clean_results["accuracy"],
                "clean_roc_auc": clean_results["roc_auc"],
                "clean_brier": clean_results["brier"],
                "accuracy": corrupted_results["accuracy"],
                "roc_auc": corrupted_results["roc_auc"],
                "brier": corrupted_results["brier"],
                "accuracy_change": corrupted_results["accuracy"] - clean_results["accuracy"],
                "roc_auc_change": corrupted_results["roc_auc"] - clean_results["roc_auc"],
                "brier_change": corrupted_results["brier"] - clean_results["brier"],
            }
            all_results.append(row)

            print(
                f"  Rate={rate}: "
                f"Accuracy={row['accuracy']:.4f}, "
                f"AUC={row['roc_auc']:.4f}, "
                f"Brier={row['brier']:.4f}, "
                f"dAUC={row['roc_auc_change']:.4f}, "
                f"dBrier={row['brier_change']:.4f}"
            )

    results_df = pd.DataFrame(all_results)

    summary_df = (
        results_df.groupby(["dataset", "model", "mechanism", "rate"], as_index=False)
        .agg(
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
    )

    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    results_df.to_csv("results/metrics/wdbc_gb_mcar_5fold_metrics.csv", index=False)
    summary_df.to_csv("results/metrics/wdbc_gb_mcar_5fold_summary.csv", index=False)

    print("\nSaved:")
    print("- results/metrics/wdbc_gb_mcar_5fold_metrics.csv")
    print("- results/metrics/wdbc_gb_mcar_5fold_summary.csv")

    print("\nAverage results across 5 folds:")
    print(summary_df)


if __name__ == "__main__":
    main()
