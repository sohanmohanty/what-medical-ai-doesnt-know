from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/wdbc_logreg_iterative_mcar_regime_compare_summary.csv"
    output_path = "figures/wdbc_logreg_iterative_mcar_regime_compare_brier.png"

    df = pd.read_csv(input_path).sort_values(["regime", "rate"])

    plt.figure(figsize=(7, 5))

    for regime in ["clean_train_corrupt_test", "corrupt_train_corrupt_test"]:
        sub = df[df["regime"] == regime].sort_values("rate")

        plt.errorbar(
            sub["rate"],
            sub["mean_brier"],
            yerr=sub["std_brier"],
            marker="o",
            capsize=4,
            label=regime,
        )

    plt.xlabel("MCAR rate")
    plt.ylabel("Mean Brier score")
    plt.title("WDBC Logistic Regression + Iterative Imputation: Regime Comparison")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()
