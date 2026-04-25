from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    logreg_path = "results/metrics/statlog_logreg_mcar_5fold_summary.csv"
    rf_path = "results/metrics/statlog_rf_mcar_5fold_summary.csv"
    output_path = "figures/statlog_mcar_model_compare_auc.png"

    logreg_df = pd.read_csv(logreg_path).sort_values("rate")
    rf_df = pd.read_csv(rf_path).sort_values("rate")

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

    plt.xlabel("MCAR rate")
    plt.ylabel("Mean ROC-AUC")
    plt.title("Statlog MCAR: Mean ROC-AUC by Model")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()