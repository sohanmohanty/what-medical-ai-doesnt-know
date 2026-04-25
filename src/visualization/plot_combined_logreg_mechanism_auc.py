from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/combined_logreg_mechanism_summary.csv"
    output_dir = Path("figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path).sort_values(["dataset", "mechanism", "rate"])

    for dataset_name in df["dataset"].unique():
        subset = df[df["dataset"] == dataset_name]

        plt.figure(figsize=(7, 5))

        for mechanism in ["mcar", "mar", "mnar"]:
            mech_df = subset[subset["mechanism"] == mechanism].sort_values("rate")

            plt.errorbar(
                mech_df["rate"],
                mech_df["mean_roc_auc"],
                yerr=mech_df["std_roc_auc"],
                marker="o",
                capsize=4,
                label=mechanism.upper(),
            )

        plt.xlabel("Missingness rate")
        plt.ylabel("Mean ROC-AUC")
        plt.title(f"{dataset_name}: Logistic Regression by Mechanism")
        plt.legend()
        plt.tight_layout()

        output_path = output_dir / f"{dataset_name}_logreg_mechanism_auc.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        print("Saved:")
        print(output_path)


if __name__ == "__main__":
    main()