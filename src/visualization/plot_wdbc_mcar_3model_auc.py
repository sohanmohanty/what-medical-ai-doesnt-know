from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    logreg_path = "results/metrics/wdbc_logreg_mcar_5fold_summary.csv"
    rf_path = "results/metrics/wdbc_rf_mcar_5fold_summary.csv"
    gb_path = "results/metrics/wdbc_gb_mcar_5fold_summary.csv"
    output_path = "figures/wdbc_mcar_3model_auc.png"

    logreg_df = pd.read_csv(logreg_path)
    rf_df = pd.read_csv(rf_path)
    gb_df = pd.read_csv(gb_path)

    plt.figure(figsize=(7, 5))

    plt.errorbar(
        logreg_df["rate"],
        logreg_df["mean_roc_auc"],
        yerr=logreg_df["std_roc_auc"],
        marker="o",
        capsize=4,
        label="logistic_regression",
    )

    plt.errorbar(
        rf_df["rate"],
        rf_df["mean_roc_auc"],
        yerr=rf_df["std_roc_auc"],
        marker="o",
        capsize=4,
        label="random_forest",
    )

    plt.errorbar(
        gb_df["rate"],
        gb_df["mean_roc_auc"],
        yerr=gb_df["std_roc_auc"],
        marker="o",
        capsize=4,
        label="gradient_boosting",
    )

    plt.xlabel("MCAR rate")
    plt.ylabel("Mean ROC-AUC")
    plt.title("WDBC MCAR: Mean ROC-AUC by Model")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()