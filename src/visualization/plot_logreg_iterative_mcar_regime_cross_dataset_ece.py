from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/combined_logreg_iterative_mcar_regime_compare_summary.csv"
    output_path = "figures/logreg_iterative_mcar_regime_cross_dataset_ece.png"

    df = pd.read_csv(input_path).sort_values(["dataset", "regime", "rate"])

    plt.figure(figsize=(8, 5))

    for dataset_name in ["wdbc", "statlog_heart"]:
        for regime in ["clean_train_corrupt_test", "corrupt_train_corrupt_test"]:
            sub = df[(df["dataset"] == dataset_name) & (df["regime"] == regime)].sort_values("rate")
            if sub.empty:
                continue

            plt.errorbar(
                sub["rate"],
                sub["mean_ece"],
                yerr=sub["std_ece"],
                marker="o",
                capsize=4,
                label=f"{dataset_name} - {regime}",
            )

    plt.xlabel("MCAR rate")
    plt.ylabel("Mean ECE")
    plt.title("Cross-Dataset Regime Comparison: Logistic Regression + Iterative Imputation")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()
