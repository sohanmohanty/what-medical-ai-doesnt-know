from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/statlog_logreg_iterative_mcar_regime_compare_summary.csv"

    for metric, ylabel in [
        ("brier", "Mean Brier score"),
        ("ece", "Mean ECE"),
    ]:
        output_path = f"figures/statlog_logreg_iterative_mcar_regime_compare_{metric}.png"
        df = pd.read_csv(input_path).sort_values(["regime", "rate"])

        plt.figure(figsize=(7, 5))
        for regime in ["clean_train_corrupt_test", "corrupt_train_corrupt_test"]:
            sub = df[df["regime"] == regime].sort_values("rate")
            plt.errorbar(
                sub["rate"],
                sub[f"mean_{metric}"],
                yerr=sub[f"std_{metric}"],
                marker="o",
                capsize=4,
                label=regime,
            )

        plt.xlabel("MCAR rate")
        plt.ylabel(ylabel)
        plt.title(f"Statlog Logistic Regression + Iterative Imputation: Regime Comparison ({metric.upper()})")
        plt.legend()
        plt.tight_layout()

        Path("figures").mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
        plt.close()

        print("Saved figure:")
        print(output_path)


if __name__ == "__main__":
    main()
