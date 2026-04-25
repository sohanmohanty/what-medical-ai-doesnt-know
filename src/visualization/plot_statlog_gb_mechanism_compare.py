from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def make_plot(metric, ylabel):
    input_path = "results/metrics/statlog_gb_combined_mechanism_summary.csv"
    output_path = f"figures/statlog_gb_mechanism_compare_{metric}.png"

    df = pd.read_csv(input_path).sort_values(["mechanism", "rate"])

    plt.figure(figsize=(7, 5))

    for mechanism in ["mcar", "mar", "mnar"]:
        sub = df[df["mechanism"] == mechanism].sort_values("rate")
        plt.errorbar(
            sub["rate"],
            sub[f"mean_{metric}"],
            yerr=sub[f"std_{metric}"],
            marker="o",
            capsize=4,
            label=mechanism.upper(),
        )

    plt.xlabel("Missingness rate")
    plt.ylabel(ylabel)
    plt.title(f"Statlog Gradient Boosting: {ylabel} by Mechanism")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


def main():
    make_plot("brier", "Mean Brier score")
    make_plot("roc_auc", "Mean ROC-AUC")


if __name__ == "__main__":
    main()
