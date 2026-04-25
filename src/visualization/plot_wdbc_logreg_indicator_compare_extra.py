from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def make_plot(mechanism, metric, ylabel):
    input_path = f"results/metrics/wdbc_logreg_{mechanism}_indicator_compare_summary.csv"
    output_path = f"figures/wdbc_logreg_{mechanism}_indicator_compare_{metric}.png"

    df = pd.read_csv(input_path).sort_values(["variant", "rate"])

    plt.figure(figsize=(7, 5))
    for variant in ["simple", "simple_plus_indicators"]:
        sub = df[df["variant"] == variant].sort_values("rate")
        plt.errorbar(
            sub["rate"],
            sub[f"mean_{metric}"],
            yerr=sub[f"std_{metric}"],
            marker="o",
            capsize=4,
            label=variant,
        )

    plt.xlabel(f"{mechanism.upper()} rate")
    plt.ylabel(ylabel)
    plt.title(f"WDBC Logistic Regression: Missingness Indicators Comparison ({mechanism.upper()})")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


def main():
    for mechanism in ["mar", "mnar"]:
        make_plot(mechanism, "ece", "Mean ECE")
        make_plot(mechanism, "brier", "Mean Brier score")


if __name__ == "__main__":
    main()
