"""Calibration utilities for reliability analysis."""

import numpy as np
import pandas as pd


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

    return float(ece)


def reliability_table(y_true, y_prob, n_bins=10):
    df = pd.DataFrame(
        {
            "y_true": y_true,
            "y_prob": y_prob,
        }
    )

    df["bin"] = pd.qcut(df["y_prob"], q=n_bins, duplicates="drop")

    table = (
        df.groupby("bin", observed=False)
        .agg(
            mean_pred=("y_prob", "mean"),
            frac_positive=("y_true", "mean"),
            count=("y_true", "size"),
        )
        .reset_index()
    )

    return table
