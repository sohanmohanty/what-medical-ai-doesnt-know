from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/wdbc_logreg_mcar_degradation.csv"
    output_path = "figures/wdbc_logreg_mcar_auc.png"

    df = pd.read_csv(input_path)

    plt.figure(figsize=(7, 5))
    plt.plot(df["rate"], df["roc_auc"], marker="o")
    plt.xlabel("MCAR rate")
    plt.ylabel("ROC-AUC")
    plt.title("WDBC Logistic Regression: ROC-AUC vs MCAR Rate")
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()