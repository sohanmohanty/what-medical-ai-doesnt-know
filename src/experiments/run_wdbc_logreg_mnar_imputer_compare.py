from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data_loading import load_wdbc
from src.data.splits import make_outer_cv_splits
from src.missingness import apply_mnar


def build_pipeline(imputer_name):
    if imputer_name == "simple":
        imputer = SimpleImputer(strategy="median")
    elif imputer_name == "knn":
        imputer = KNNImputer(n_neighbors=5)
    elif imputer_name == "iterative":
        imputer = IterativeImputer(random_state=42, max_iter=20)
    else:
        raise ValueError(f"Unknown imputer: {imputer_name}")

    return Pipeline(
        steps=[
            ("imputer", imputer),
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
    }


def main():
    print("STARTING MNAR IMPUTER COMPARISON")

    X, y, _ = load_wdbc()

    print("WDBC loaded")
    print("Original X shape:", X.shape)

    splits = make_outer_cv_splits(X, y, n_splits=5)
    rates = [0.1, 0.2, 0.3, 0.5]
    imputers = ["simple", "knn", "iterative"]
    all_results = []

    target_features = [
        "mean texture",
        "mean perimeter",
        "mean area",
        "worst texture",
        "worst perimeter",
    ]

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
            f"Brier={clean_results['brier']:.4f}"
        )

        for rate in rates:
            rng_train = np.random.default_rng(42 + fold_idx)
            rng_test = np.random.default_rng(123 + fold_idx)

            X_train_mnar, _, train_meta = apply_mnar(
                X_df=X_train,
                rate=rate,
                rng=rng_train,
                target_features=target_features,
                beta=2.0,
            )

            X_test_mnar, _, test_meta = apply_mnar(
                X_df=X_test,
                rate=rate,
                rng=rng_test,
                target_features=target_features,
                beta=2.0,
            )

            for imputer_name in imputers:
                pipeline = build_pipeline(imputer_name)
                results = evaluate_pipeline(pipeline, X_train_mnar, X_test_mnar, y_train, y_test)

                row = {
                    "dataset": "wdbc",
                    "model": "logistic_regression",
                    "mechanism": "mnar",
                    "imputer": imputer_name,
                    "fold": fold_idx,
                    "rate": rate,
                    "train_actual_rate": train_meta["actual_rate"],
                    "test_actual_rate": test_meta["actual_rate"],
                    "accuracy": results["accuracy"],
                    "roc_auc": results["roc_auc"],
                    "brier": results["brier"],
                    "accuracy_change_vs_clean": results["accuracy"] - clean_results["accuracy"],
                    "roc_auc_change_vs_clean": results["roc_auc"] - clean_results["roc_auc"],
                    "brier_change_vs_clean": results["brier"] - clean_results["brier"],
                }
                all_results.append(row)

                print(
                    f"  Rate={rate}, imputer={imputer_name}: "
                    f"Accuracy={row['accuracy']:.4f}, "
                    f"AUC={row['roc_auc']:.4f}, "
                    f"Brier={row['brier']:.4f}"
                )

    results_df = pd.DataFrame(all_results)

    summary_df = (
        results_df.groupby(["dataset", "model", "mechanism", "imputer", "rate"], as_index=False)
        .agg(
            mean_accuracy=("accuracy", "mean"),
            std_accuracy=("accuracy", "std"),
            mean_roc_auc=("roc_auc", "mean"),
            std_roc_auc=("roc_auc", "std"),
            mean_brier=("brier", "mean"),
            std_brier=("brier", "std"),
            mean_accuracy_change_vs_clean=("accuracy_change_vs_clean", "mean"),
            mean_roc_auc_change_vs_clean=("roc_auc_change_vs_clean", "mean"),
            mean_brier_change_vs_clean=("brier_change_vs_clean", "mean"),
        )
    )

    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    results_df.to_csv("results/metrics/wdbc_logreg_mnar_imputer_compare_metrics.csv", index=False)
    summary_df.to_csv("results/metrics/wdbc_logreg_mnar_imputer_compare_summary.csv", index=False)

    print("\nSaved:")
    print("- results/metrics/wdbc_logreg_mnar_imputer_compare_metrics.csv")
    print("- results/metrics/wdbc_logreg_mnar_imputer_compare_summary.csv")

    print("\nDONE")


if __name__ == "__main__":
    main()

