from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    mcar_path = "results/metrics/statlog_logreg_mcar_5fold_summary.csv"
    mar_path = "results/metrics/statlog_logreg_mar_5fold_summary.csv"
    mnar_path = "results/metrics/statlog_logreg_mnar_5fold_summary.csv"
    output_path = "figures/statlog_logreg_mechanism_compare_brier.png"

    mcar_df = pd.read_csv(mcar_path).sort_values("rate")
    mar_df = pd.read_csv(mar_path).sort_values("rate")
    mnar_df = pd.read_csv(mnar_path).sort_values("rate")

    plt.figure(figsize=(7, 5))

    plt.errorbar(
        mcar_df["rate"],
        mcar_df["mean_brier"],
        yerr=mcar_df["std_brier"],
        marker="o",
        capsize=4,
        label="MCAR",
    )

    plt.errorbar(
        mar_df["rate"],
        mar_df["mean_brier"],
        yerr=mar_df["std_brier"],
        marker="o",
        capsize=4,
        label="MAR",
    )

    plt.errorbar(
        mnar_df["rate"],
        mnar_df["mean_brier"],
        yerr=mnar_df["std_brier"],
        marker="o",
        capsize=4,
        label="MNAR",
    )

    plt.xlabel("Missingness rate")
    plt.ylabel("Mean Brier score")
    plt.title("Statlog Logistic Regression: Mean Brier by Mechanism")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()