from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/wdbc_logreg_mnar_imputer_compare_summary.csv"
    output_path = "figures/wdbc_logreg_mnar_imputer_compare_auc.png"

    df = pd.read_csv(input_path).sort_values(["imputer", "rate"])

    plt.figure(figsize=(7, 5))

    for imputer_name in ["simple", "knn", "iterative"]:
        sub = df[df["imputer"] == imputer_name].sort_values("rate")

        plt.errorbar(
            sub["rate"],
            sub["mean_roc_auc"],
            yerr=sub["std_roc_auc"],
            marker="o",
            capsize=4,
            label=imputer_name,
        )

    plt.xlabel("MNAR rate")
    plt.ylabel("Mean ROC-AUC")
    plt.title("WDBC Logistic Regression: MNAR Imputer Comparison")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()
