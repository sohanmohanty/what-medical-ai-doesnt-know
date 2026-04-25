from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/statlog_combined_model_mechanism_summary.csv"
    output_dir = Path("figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path).sort_values(["mechanism", "model", "rate"])

    for mechanism in df["mechanism"].unique():
        subset = df[df["mechanism"] == mechanism]

        plt.figure(figsize=(7, 5))

        for model_name in ["logistic_regression", "random_forest"]:
            model_df = subset[subset["model"] == model_name].sort_values("rate")

            plt.errorbar(
                model_df["rate"],
                model_df["mean_roc_auc"],
                yerr=model_df["std_roc_auc"],
                marker="o",
                capsize=4,
                label=model_name,
            )

        plt.xlabel("Missingness rate")
        plt.ylabel("Mean ROC-AUC")
        plt.title(f"Statlog: Mean ROC-AUC by Model under {mechanism.upper()}")
        plt.legend()
        plt.tight_layout()

        output_path = output_dir / f"statlog_{mechanism}_model_compare_auc.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        print("Saved:")
        print(output_path)


if __name__ == "__main__":
    main()