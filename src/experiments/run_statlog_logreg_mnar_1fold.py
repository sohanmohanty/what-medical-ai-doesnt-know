"""
Statlog Heart logistic regression under 1-fold MNAR.
First working MNAR run on the second dataset.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, brier_score_loss

from src.data_loading import load_statlog_heart
from src.data.splits import make_outer_cv_splits
from src.preprocessing import build_preprocessor
from src.missingness import apply_mnar


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
    X, y, schema = load_statlog_heart()

    print("Statlog Heart loaded")
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

    rng_train = np.random.default_rng(42)
    rng_test = np.random.default_rng(123)

    X_train_mnar, _, train_meta = apply_mnar(
        X_df=X_train,
        rate=0.2,
        rng=rng_train,
        target_features=["rest-bp", "serum-chol", "max-heart-rate"],
        beta=2.0,
    )

    X_test_mnar, _, test_meta = apply_mnar(
        X_df=X_test,
        rate=0.2,
        rng=rng_test,
        target_features=["rest-bp", "serum-chol", "max-heart-rate"],
        beta=2.0,
    )

    mnar_results = evaluate_pipeline(X_train_mnar, X_test_mnar, y_train, y_test, schema)

    print("\nClean results:")
    print("Accuracy:", round(clean_results["accuracy"], 4))
    print("ROC-AUC:", round(clean_results["roc_auc"], 4))
    print("Brier score:", round(clean_results["brier"], 4))

    print("\nMNAR results (20%):")
    print("Train actual missing rate:", round(train_meta["actual_rate"], 4))
    print("Test actual missing rate:", round(test_meta["actual_rate"], 4))
    print("Accuracy:", round(mnar_results["accuracy"], 4))
    print("ROC-AUC:", round(mnar_results["roc_auc"], 4))
    print("Brier score:", round(mnar_results["brier"], 4))

    print("\nDegradation (MNAR - clean):")
    print("Accuracy change:", round(mnar_results["accuracy"] - clean_results["accuracy"], 4))
    print("ROC-AUC change:", round(mnar_results["roc_auc"] - clean_results["roc_auc"], 4))
    print("Brier change:", round(mnar_results["brier"] - clean_results["brier"], 4))


if __name__ == "__main__":
    main()
