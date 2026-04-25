from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/combined_logreg_iterative_calibration_summary.csv"
    output_path = "figures/logreg_iterative_wdbc_vs_statlog_ece.png"

    df = pd.read_csv(input_path).sort_values(["dataset", "mechanism", "rate"])

    plt.figure(figsize=(8, 5))

    for dataset_name in ["wdbc", "statlog_heart"]:
        for mechanism in ["mcar", "mar", "mnar"]:
            sub = df[
                (df["dataset"] == dataset_name) &
                (df["mechanism"] == mechanism)
            ].sort_values("rate")

            label = f"{dataset_name} - {mechanism.upper()}"

            plt.errorbar(
                sub["rate"],
                sub["mean_ece"],
                yerr=sub["std_ece"],
                marker="o",
                capsize=4,
                label=label,
            )

    plt.xlabel("Missingness rate")
    plt.ylabel("Mean ECE")
    plt.title("Logistic Regression + Iterative Imputation: ECE Across Datasets")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()
