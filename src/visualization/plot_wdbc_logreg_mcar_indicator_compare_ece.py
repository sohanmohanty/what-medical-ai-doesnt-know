from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv"
    output_path = "figures/wdbc_logreg_mcar_indicator_compare_ece.png"

    df = pd.read_csv(input_path).sort_values(["variant", "rate"])

    plt.figure(figsize=(7, 5))

    for variant in ["simple", "simple_plus_indicators"]:
        sub = df[df["variant"] == variant].sort_values("rate")

        plt.errorbar(
            sub["rate"],
            sub["mean_ece"],
            yerr=sub["std_ece"],
            marker="o",
            capsize=4,
            label=variant,
        )

    plt.xlabel("MCAR rate")
    plt.ylabel("Mean ECE")
    plt.title("WDBC Logistic Regression: Missingness Indicators Comparison")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()
