import math

import numpy as np
import pandas as pd

from src.data.splits import make_repeated_outer_cv_splits
from src.evaluation import compute_binary_classification_metrics, safe_roc_auc_score


def test_repeated_outer_cv_splits_are_reproducible():
    X = pd.DataFrame({"x": np.arange(30)})
    y = pd.Series([0, 1] * 15)

    splits_a = make_repeated_outer_cv_splits(X, y, n_splits=5, n_repeats=2, random_state=42)
    splits_b = make_repeated_outer_cv_splits(X, y, n_splits=5, n_repeats=2, random_state=42)

    assert len(splits_a) == 10
    assert [(split["repeat"], split["fold"]) for split in splits_a] == [(split["repeat"], split["fold"]) for split in splits_b]
    for split_a, split_b in zip(splits_a, splits_b):
        assert np.array_equal(split_a["train_idx"], split_b["train_idx"])
        assert np.array_equal(split_a["test_idx"], split_b["test_idx"])


def test_safe_roc_auc_score_returns_nan_for_single_class_targets():
    y_true = np.array([1, 1, 1, 1])
    y_prob = np.array([0.2, 0.4, 0.7, 0.9])

    score = safe_roc_auc_score(y_true, y_prob)

    assert math.isnan(score)


def test_compute_binary_classification_metrics_returns_valid_ranges():
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])

    metrics = compute_binary_classification_metrics(y_true, y_pred, y_prob, n_bins=4)

    assert metrics["accuracy"] == 1.0
    assert metrics["roc_auc"] == 1.0
    assert 0.0 <= metrics["brier"] <= 1.0
    assert 0.0 <= metrics["ece"] <= 1.0
