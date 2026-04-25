"""Shared plotting helpers for figures and report assets."""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import pandas as pd


def save_metric_line_plot(df: pd.DataFrame, x_col: str, y_col: str, output_path: str, title: str, ylabel: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 5))
    plt.plot(df[x_col], df[y_col], marker="o")
    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_grouped_bar_plot(
    df: pd.DataFrame,
    category_col: str,
    group_col: str,
    value_col: str,
    output_path: str,
    title: str,
    ylabel: str,
):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pivoted = df.pivot(index=category_col, columns=group_col, values=value_col)
    pivoted.plot(kind="bar", figsize=(8, 5))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_reliability_diagram(table: pd.DataFrame, output_path: str, title: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 6))
    plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect calibration")
    plt.plot(table["mean_pred"], table["frac_positive"], marker="o", label="Model")
    plt.xlabel("Mean predicted probability")
    plt.ylabel("Observed fraction positive")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_run_summary_figure(
    summary_df: pd.DataFrame,
    output_path: str,
    title: str,
):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    metrics = [
        ("roc_auc", "ROC-AUC", True),
        ("accuracy", "Accuracy", True),
        ("brier", "Brier", False),
        ("ece", "ECE", False),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)
    axes = axes.ravel()

    mechanisms = list(dict.fromkeys(summary_df["mechanism"].tolist()))
    color_cycle = plt.rcParams["axes.prop_cycle"].by_key().get("color", ["#1f77b4", "#ff7f0e", "#2ca02c"])
    color_map = {mechanism: color_cycle[idx % len(color_cycle)] for idx, mechanism in enumerate(mechanisms)}

    sorted_df = summary_df.sort_values(["mechanism", "rate"]).copy()

    for axis, (metric_name, label, higher_is_better) in zip(axes, metrics):
        clean_col = f"mean_clean_{metric_name}"
        corrupt_col = f"mean_{metric_name}"

        if clean_col in sorted_df.columns:
            clean_baseline = sorted_df[clean_col].dropna()
            if not clean_baseline.empty:
                axis.axhline(
                    clean_baseline.iloc[0],
                    linestyle="--",
                    linewidth=1.5,
                    color="#4d4d4d",
                    label="clean baseline",
                )

        for mechanism in mechanisms:
            subset = sorted_df[sorted_df["mechanism"] == mechanism]
            axis.plot(
                subset["rate"],
                subset[corrupt_col],
                marker="o",
                linewidth=2,
                color=color_map[mechanism],
                label=mechanism.upper(),
            )

        direction_text = "Higher is better" if higher_is_better else "Lower is better"
        axis.set_title(f"{label}\n{direction_text}", fontsize=15, pad=12)
        axis.set_xlabel("Missingness Rate")
        axis.set_ylabel(label)
        axis.grid(alpha=0.25)

    handles, labels = axes[0].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    wrapped_title = "\n".join(textwrap.wrap(title, width=72))
    fig.suptitle(wrapped_title, fontsize=16, y=0.985)
    fig.legend(
        unique.values(),
        unique.keys(),
        loc="upper center",
        bbox_to_anchor=(0.5, 0.93),
        ncol=min(4, len(unique)),
        frameon=True,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.84))
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
