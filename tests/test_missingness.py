import numpy as np
import pandas as pd

from src.missingness import apply_mar, apply_mcar, apply_mnar


def test_mcar_masks_requested_subset_at_approximately_requested_rate():
    X = pd.DataFrame(
        {
            "a": np.arange(1000, dtype=float),
            "b": np.arange(1000, dtype=float) * 2,
            "c": np.arange(1000, dtype=float) * 3,
        }
    )

    X_masked, mask, metadata = apply_mcar(X, rate=0.2, rng=np.random.default_rng(42), feature_subset=["a", "b"])

    assert metadata["feature_subset"] == ["a", "b"]
    assert abs(metadata["actual_rate"] - 0.2) < 0.03
    assert mask["c"].sum() == 0
    assert X_masked["c"].isna().sum() == 0


def test_mar_only_masks_target_features_and_tracks_target_rate():
    X = pd.DataFrame(
        {
            "anchor": np.linspace(-2, 2, 1000),
            "f1": np.linspace(0, 1, 1000),
            "f2": np.linspace(1, 2, 1000),
            "untouched": np.linspace(2, 3, 1000),
        }
    )

    X_masked, mask, metadata = apply_mar(
        X,
        rate=0.3,
        rng=np.random.default_rng(7),
        target_features=["f1", "f2"],
        anchor_feature="anchor",
        beta=2.0,
    )

    assert metadata["mechanism"] == "mar"
    assert abs(metadata["actual_rate"] - 0.3) < 0.04
    assert mask["untouched"].sum() == 0
    assert X_masked["untouched"].isna().sum() == 0


def test_mnar_missingness_is_more_likely_for_higher_feature_values():
    X = pd.DataFrame(
        {
            "signal": np.linspace(-3, 3, 2000),
            "other": np.linspace(0, 1, 2000),
        }
    )

    _, mask, metadata = apply_mnar(
        X,
        rate=0.25,
        rng=np.random.default_rng(9),
        target_features=["signal"],
        beta=2.5,
    )

    signal = X["signal"]
    masked = mask["signal"]
    low_group_rate = masked[signal <= signal.quantile(0.25)].mean()
    high_group_rate = masked[signal >= signal.quantile(0.75)].mean()

    assert metadata["mechanism"] == "mnar"
    assert abs(metadata["actual_rate"] - 0.25) < 0.04
    assert high_group_rate > low_group_rate
