from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/wdbc_logreg_iterative_calibration_summary.csv"
    output_path = "figures/wdbc_logreg_iterative_ece_compare.png"

    df = pd.read_csv(input_path).sort_values(["mechanism", "rate"])

    plt.figure(figsize=(7, 5))

    for mechanism in ["mcar", "mar", "mnar"]:
        sub = df[df["mechanism"] == mechanism].sort_values("rate")

        plt.errorbar(
            sub["rate"],
            sub["mean_ece"],
            yerr=sub["std_ece"],
            marker="o",
            capsize=4,
            label=mechanism.upper(),
        )

    plt.xlabel("Missingness rate")
    plt.ylabel("Mean ECE")
    plt.title("WDBC Logistic Regression + Iterative Imputation: ECE by Mechanism")
    plt.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()
