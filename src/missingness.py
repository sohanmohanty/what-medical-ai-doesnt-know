import numpy as np
import pandas as pd


def apply_mcar(X_df: pd.DataFrame, rate: float, rng: np.random.Generator, feature_subset=None):
    X_masked = X_df.copy()

    columns = feature_subset if feature_subset is not None else list(X_df.columns)
    mask = pd.DataFrame(False, index=X_df.index, columns=X_df.columns)

    for col in columns:
        col_mask = rng.random(len(X_df)) < rate
        X_masked.loc[col_mask, col] = np.nan
        mask.loc[col_mask, col] = True

    actual_missing_rate = mask[columns].to_numpy().mean()

    metadata = {
        "mechanism": "mcar",
        "requested_rate": rate,
        "actual_rate": float(actual_missing_rate),
        "feature_subset": columns,
    }

    return X_masked, mask, metadata


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def _find_intercept_for_rate(z, rate, beta, max_iter=100):
    lo, hi = -20.0, 20.0

    for _ in range(max_iter):
        mid = (lo + hi) / 2
        probs = _sigmoid(mid + beta * z)
        mean_prob = probs.mean()

        if mean_prob < rate:
            lo = mid
        else:
            hi = mid

    return (lo + hi) / 2


def apply_mar(
    X_df: pd.DataFrame,
    rate: float,
    rng: np.random.Generator,
    target_features,
    anchor_feature,
    beta=1.0,
):
    X_masked = X_df.copy()
    mask = pd.DataFrame(False, index=X_df.index, columns=X_df.columns)

    z = X_df[anchor_feature].to_numpy(dtype=float)
    z = (z - z.mean()) / z.std()

    alpha = _find_intercept_for_rate(z, rate, beta)
    probs = _sigmoid(alpha + beta * z)

    for feature in target_features:
        draws = rng.random(len(X_df)) < probs
        X_masked.loc[draws, feature] = np.nan
        mask.loc[draws, feature] = True

    actual_missing_rate = mask[target_features].to_numpy().mean()

    metadata = {
        "mechanism": "mar",
        "requested_rate": rate,
        "actual_rate": float(actual_missing_rate),
        "target_features": target_features,
        "anchor_feature": anchor_feature,
        "beta": beta,
    }

    return X_masked, mask, metadata


def apply_mnar(
    X_df: pd.DataFrame,
    rate: float,
    rng: np.random.Generator,
    target_features,
    beta=1.0,
):
    X_masked = X_df.copy()
    mask = pd.DataFrame(False, index=X_df.index, columns=X_df.columns)

    for feature in target_features:
        z = X_df[feature].to_numpy(dtype=float)
        z = (z - z.mean()) / z.std()

        alpha = _find_intercept_for_rate(z, rate, beta)
        probs = _sigmoid(alpha + beta * z)

        draws = rng.random(len(X_df)) < probs
        X_masked.loc[draws, feature] = np.nan
        mask.loc[draws, feature] = True

    actual_missing_rate = mask[target_features].to_numpy().mean()

    metadata = {
        "mechanism": "mnar",
        "requested_rate": rate,
        "actual_rate": float(actual_missing_rate),
        "target_features": target_features,
        "beta": beta,
    }

    return X_masked, mask, metadata
