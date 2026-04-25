from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/wdbc_logreg_mcar_5fold_summary.csv"
    output_path = "figures/wdbc_logreg_mcar_5fold_brier.png"

    df = pd.read_csv(input_path)

    plt.figure(figsize=(7, 5))
    plt.errorbar(
        df["rate"],
        df["mean_brier"],
        yerr=df["std_brier"],
        marker="o",
        capsize=4,
    )
    plt.xlabel("MCAR rate")
    plt.ylabel("Mean Brier score")
    plt.title("WDBC Logistic Regression: 5-Fold Mean Brier vs MCAR Rate")
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()