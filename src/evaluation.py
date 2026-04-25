"""Evaluation helpers for binary classification experiments."""

import warnings

import pandas as pd
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.exceptions import UndefinedMetricWarning

from src.calibration import expected_calibration_error


def safe_roc_auc_score(y_true, y_prob):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
        try:
            return float(roc_auc_score(y_true, y_prob))
        except ValueError:
            return float("nan")


def compute_binary_classification_metrics(y_true, y_pred, y_prob, n_bins=10):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "roc_auc": safe_roc_auc_score(y_true, y_prob),
        "brier": brier_score_loss(y_true, y_prob),
        "ece": expected_calibration_error(y_true, y_prob, n_bins=n_bins),
    }


def summarize_metrics(df: pd.DataFrame, group_cols):
    metric_specs = {
        "accuracy": ("mean_accuracy", "std_accuracy"),
        "roc_auc": ("mean_roc_auc", "std_roc_auc"),
        "brier": ("mean_brier", "std_brier"),
        "ece": ("mean_ece", "std_ece"),
    }

    available = {metric: names for metric, names in metric_specs.items() if metric in df.columns}
    agg_map = {}

    for metric, (mean_name, std_name) in available.items():
        agg_map[mean_name] = (metric, "mean")
        agg_map[std_name] = (metric, "std")

    return df.groupby(group_cols, as_index=False).agg(**agg_map)
