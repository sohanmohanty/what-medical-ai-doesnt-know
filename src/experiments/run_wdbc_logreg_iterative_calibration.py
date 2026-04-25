from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data_loading import load_wdbc
from src.data.splits import make_outer_cv_splits
from src.missingness import apply_mcar, apply_mar, apply_mnar


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


def build_pipeline():
    return Pipeline(
        steps=[
            ("imputer", IterativeImputer(random_state=42, max_iter=20)),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(C=1.0, solver="liblinear", max_iter=1000)),
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
        "ece": expected_calibration_error(y_test, y_prob, n_bins=10),
    }


def main():
    X, y, _ = load_wdbc()

    print("WDBC loaded")
    print("Original X shape:", X.shape)

    splits = make_outer_cv_splits(X, y, n_splits=5)
    rates = [0.1, 0.2, 0.3, 0.5]
    mechanisms = ["mcar", "mar", "mnar"]
    all_results = []

    mar_target_features = [
        "mean texture",
        "mean perimeter",
        "mean area",
        "worst texture",
        "worst perimeter",
    ]
    mnar_target_features = mar_target_features.copy()

    for fold_idx, (train_idx, test_idx) in enumerate(splits):
        print(f"\n===== Fold {fold_idx} =====")

        X_train = X.iloc[train_idx].copy()
        X_test = X.iloc[test_idx].copy()
        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        clean_pipeline = build_pipeline()
        clean_results = evaluate_pipeline(clean_pipeline, X_train, X_test, y_train, y_test)

        print(
            f"Clean: Accuracy={clean_results['accuracy']:.4f}, "
            f"AUC={clean_results['roc_auc']:.4f}, "
            f"Brier={clean_results['brier']:.4f}, "
            f"ECE={clean_results['ece']:.4f}"
        )

        for mechanism in mechanisms:
            for rate in rates:
                rng_train = np.random.default_rng(42 + fold_idx)
                rng_test = np.random.default_rng(123 + fold_idx)

                if mechanism == "mcar":
                    X_train_masked, _, train_meta = apply_mcar(X_train, rate=rate, rng=rng_train)
                    X_test_masked, _, test_meta = apply_mcar(X_test, rate=rate, rng=rng_test)

                elif mechanism == "mar":
                    X_train_masked, _, train_meta = apply_mar(
                        X_df=X_train,
                        rate=rate,
                        rng=rng_train,
                        target_features=mar_target_features,
                        anchor_feature="mean radius",
                        beta=2.0,
                    )
                    X_test_masked, _, test_meta = apply_mar(
                        X_df=X_test,
                        rate=rate,
                        rng=rng_test,
                        target_features=mar_target_features,
                        anchor_feature="mean radius",
                        beta=2.0,
                    )

                elif mechanism == "mnar":
                    X_train_masked, _, train_meta = apply_mnar(
                        X_df=X_train,
                        rate=rate,
                        rng=rng_train,
                        target_features=mnar_target_features,
                        beta=2.0,
                    )
                    X_test_masked, _, test_meta = apply_mnar(
                        X_df=X_test,
                        rate=rate,
                        rng=rng_test,
                        target_features=mnar_target_features,
                        beta=2.0,
                    )
                else:
                    raise ValueError(f"Unknown mechanism: {mechanism}")

                pipeline = build_pipeline()
                results = evaluate_pipeline(pipeline, X_train_masked, X_test_masked, y_train, y_test)

                row = {
                    "dataset": "wdbc",
                    "model": "logistic_regression",
                    "imputer": "iterative",
                    "mechanism": mechanism,
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
                    f"  {mechanism.upper()} rate={rate}: "
                    f"AUC={row['roc_auc']:.4f}, "
                    f"Brier={row['brier']:.4f}, "
                    f"ECE={row['ece']:.4f}"
                )

    results_df = pd.DataFrame(all_results)

    summary_df = (
        results_df.groupby(["dataset", "model", "imputer", "mechanism", "rate"], as_index=False)
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
    results_df.to_csv("results/metrics/wdbc_logreg_iterative_calibration_metrics.csv", index=False)
    summary_df.to_csv("results/metrics/wdbc_logreg_iterative_calibration_summary.csv", index=False)

    print("\nSaved:")
    print("- results/metrics/wdbc_logreg_iterative_calibration_metrics.csv")
    print("- results/metrics/wdbc_logreg_iterative_calibration_summary.csv")

    print("\nSummary:")
    print(summary_df)


if __name__ == "__main__":
    main()

