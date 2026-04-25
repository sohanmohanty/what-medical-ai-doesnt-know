"""
WDBC logistic regression 1-fold comparison:
- clean
- MCAR
- MAR
Intended as a quick comparison/debug script.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, brier_score_loss

from src.data_loading import load_wdbc
from src.data.splits import make_outer_cv_splits
from src.preprocessing import build_preprocessor
from src.missingness import apply_mcar, apply_mar


def evaluate_pipeline(X_train, X_test, y_train, y_test, schema):
    preprocessor = build_preprocessor(schema, scale_numeric=True)

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    model = LogisticRegression(C=1.0, solver="liblinear", max_iter=1000)
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
    train_idx, test_idx = splits[0]

    X_train = X.iloc[train_idx].copy()
    X_test = X.iloc[test_idx].copy()
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    print("\nTrain/Test split ready.")
    print("Train size:", len(X_train))
    print("Test size:", len(X_test))

    clean_results = evaluate_pipeline(X_train, X_test, y_train, y_test, schema)

    rng_train_mcar = np.random.default_rng(42)
    rng_test_mcar = np.random.default_rng(123)

    X_train_mcar, _, train_meta_mcar = apply_mcar(X_train, rate=0.2, rng=rng_train_mcar)
    X_test_mcar, _, test_meta_mcar = apply_mcar(X_test, rate=0.2, rng=rng_test_mcar)

    mcar_results = evaluate_pipeline(X_train_mcar, X_test_mcar, y_train, y_test, schema)

    rng_train_mar = np.random.default_rng(42)
    rng_test_mar = np.random.default_rng(123)

    X_train_mar, _, train_meta_mar = apply_mar(
        X_df=X_train,
        rate=0.2,
        rng=rng_train_mar,
        target_features=[
            "mean texture",
            "mean perimeter",
            "mean area",
            "worst texture",
            "worst perimeter",
        ],
        anchor_feature="mean radius",
        beta=2.0,
    )

    X_test_mar, _, test_meta_mar = apply_mar(
        X_df=X_test,
        rate=0.2,
        rng=rng_test_mar,
        target_features=[
            "mean texture",
            "mean perimeter",
            "mean area",
            "worst texture",
            "worst perimeter",
        ],
        anchor_feature="mean radius",
        beta=2.0,
    )

    mar_results = evaluate_pipeline(X_train_mar, X_test_mar, y_train, y_test, schema)

    print("\nClean results:")
    print("Accuracy:", round(clean_results["accuracy"], 4))
    print("ROC-AUC:", round(clean_results["roc_auc"], 4))
    print("Brier score:", round(clean_results["brier"], 4))

    print("\nMCAR results (20%):")
    print("Train actual missing rate:", round(train_meta_mcar["actual_rate"], 4))
    print("Test actual missing rate:", round(test_meta_mcar["actual_rate"], 4))
    print("Accuracy:", round(mcar_results["accuracy"], 4))
    print("ROC-AUC:", round(mcar_results["roc_auc"], 4))
    print("Brier score:", round(mcar_results["brier"], 4))

    print("\nMAR results (20%, multi-feature, anchored on mean radius):")
    print("Train actual missing rate:", round(train_meta_mar["actual_rate"], 4))
    print("Test actual missing rate:", round(test_meta_mar["actual_rate"], 4))
    print("Accuracy:", round(mar_results["accuracy"], 4))
    print("ROC-AUC:", round(mar_results["roc_auc"], 4))
    print("Brier score:", round(mar_results["brier"], 4))

    print("\nDegradation vs clean:")
    print("MCAR accuracy change:", round(mcar_results["accuracy"] - clean_results["accuracy"], 4))
    print("MCAR AUC change:", round(mcar_results["roc_auc"] - clean_results["roc_auc"], 4))
    print("MCAR Brier change:", round(mcar_results["brier"] - clean_results["brier"], 4))

    print("MAR accuracy change:", round(mar_results["accuracy"] - clean_results["accuracy"], 4))
    print("MAR AUC change:", round(mar_results["roc_auc"] - clean_results["roc_auc"], 4))
    print("MAR Brier change:", round(mar_results["brier"] - clean_results["brier"], 4))


if __name__ == "__main__":
    main()
