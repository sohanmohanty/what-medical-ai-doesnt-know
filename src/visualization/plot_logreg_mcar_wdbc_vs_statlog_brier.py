from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    wdbc_path = "results/metrics/wdbc_logreg_mcar_5fold_summary.csv"
    statlog_path = "results/metrics/statlog_logreg_mcar_5fold_summary.csv"
    output_path = "figures/logreg_mcar_wdbc_vs_statlog_brier.png"

    wdbc_df = pd.read_csv(wdbc_path)
    statlog_df = pd.read_csv(statlog_path)

    plt.figure(figsize=(7, 5))

    plt.errorbar(
        wdbc_df["rate"],
        wdbc_df["mean_brier"],
        yerr=wdbc_df["std_brier"],
        marker="o",
        capsize=4,
        label="WDBC",
    )

    plt.errorbar(
        statlog_df["rate"],
        statlog_df["mean_brier"],
        yerr=statlog_df["std_brier"],
        marker="o",
        capsize=4,
        label="Statlog Heart",
    )

    plt.xlabel("MCAR rate")
    plt.ylabel("Mean Brier score")
    plt.title("Logistic Regression under MCAR: WDBC vs Statlog")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()