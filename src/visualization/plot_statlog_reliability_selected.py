from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data_loading import load_statlog_heart
from src.data.splits import make_outer_cv_splits
from src.missingness import apply_mcar, apply_mar, apply_mnar


def build_pipeline():
    return Pipeline(
        steps=[
            ("imputer", IterativeImputer(random_state=42, max_iter=20)),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(C=1.0, solver="liblinear", max_iter=1000)),
        ]
    )


def get_probabilities(X_train, X_test, y_train):
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    return pipeline.predict_proba(X_test)[:, 1]


def calibration_points(y_true, y_prob, n_bins=10):
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    xs = []
    ys = []

    for i in range(n_bins):
        left = bin_edges[i]
        right = bin_edges[i + 1]

        if i == n_bins - 1:
            mask = (y_prob >= left) & (y_prob <= right)
        else:
            mask = (y_prob >= left) & (y_prob < right)

        if np.sum(mask) == 0:
            continue

        xs.append(np.mean(y_prob[mask]))
        ys.append(np.mean(y_true[mask]))

    return xs, ys


def main():
    X, y, _ = load_statlog_heart()
    splits = make_outer_cv_splits(X, y, n_splits=5)

    conditions = {
        "clean": {"mechanism": "clean", "rate": 0.0},
        "mcar_0.3": {"mechanism": "mcar", "rate": 0.3},
        "mar_0.3": {"mechanism": "mar", "rate": 0.3},
        "mnar_0.3": {"mechanism": "mnar", "rate": 0.3},
    }

    target_features = [
        "resting_blood_pressure",
        "serum_cholestoral",
        "maximum_heart_rate_achieved",
    ]

    Path("figures").mkdir(parents=True, exist_ok=True)

    for condition_name, config in conditions.items():
        all_y_true = []
        all_y_prob = []

        for fold_idx, (train_idx, test_idx) in enumerate(splits):
            X_train = X.iloc[train_idx].copy()
            X_test = X.iloc[test_idx].copy()
            y_train = y.iloc[train_idx]
            y_test = y.iloc[test_idx]

            if config["mechanism"] == "clean":
                X_train_used = X_train
                X_test_used = X_test

            elif config["mechanism"] == "mcar":
                rng_train = np.random.default_rng(42 + fold_idx)
                rng_test = np.random.default_rng(123 + fold_idx)
                X_train_used, _, _ = apply_mcar(X_train, rate=config["rate"], rng=rng_train)
                X_test_used, _, _ = apply_mcar(X_test, rate=config["rate"], rng=rng_test)

            elif config["mechanism"] == "mar":
                rng_train = np.random.default_rng(42 + fold_idx)
                rng_test = np.random.default_rng(123 + fold_idx)
                X_train_used, _, _ = apply_mar(
                    X_df=X_train,
                    rate=config["rate"],
                    rng=rng_train,
                    target_features=target_features,
                    anchor_feature="age",
                    beta=2.0,
                )
                X_test_used, _, _ = apply_mar(
                    X_df=X_test,
                    rate=config["rate"],
                    rng=rng_test,
                    target_features=target_features,
                    anchor_feature="age",
                    beta=2.0,
                )

            elif config["mechanism"] == "mnar":
                rng_train = np.random.default_rng(42 + fold_idx)
                rng_test = np.random.default_rng(123 + fold_idx)
                X_train_used, _, _ = apply_mnar(
                    X_df=X_train,
                    rate=config["rate"],
                    rng=rng_train,
                    target_features=target_features,
                    beta=2.0,
                )
                X_test_used, _, _ = apply_mnar(
                    X_df=X_test,
                    rate=config["rate"],
                    rng=rng_test,
                    target_features=target_features,
                    beta=2.0,
                )

            else:
                raise ValueError(f"Unknown mechanism: {config['mechanism']}")

            y_prob = get_probabilities(X_train_used, X_test_used, y_train)

            all_y_true.extend(y_test.tolist())
            all_y_prob.extend(y_prob.tolist())

        xs, ys = calibration_points(all_y_true, all_y_prob, n_bins=10)

        plt.figure(figsize=(6, 6))
        plt.plot([0, 1], [0, 1], linestyle="--")
        plt.plot(xs, ys, marker="o")
        plt.xlabel("Mean predicted probability")
        plt.ylabel("Observed positive frequency")
        plt.title(f"Statlog Reliability Diagram: {condition_name}")
        plt.tight_layout()

        output_path = f"figures/statlog_reliability_{condition_name}.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        print("Saved figure:")
        print(output_path)


if __name__ == "__main__":
    main()

