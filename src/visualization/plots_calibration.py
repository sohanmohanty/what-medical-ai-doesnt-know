from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_reliability_diagram(input_csv_path: str, output_png_path: str):
    df = pd.read_csv(input_csv_path)

    Path(output_png_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(6, 6))
    plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect calibration")
    plt.plot(df["mean_pred"], df["frac_positive"], marker="o", label="Model")

    plt.xlabel("Mean predicted probability")
    plt.ylabel("Observed fraction positive")
    plt.title("Reliability Diagram: WDBC Logistic Regression")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_png_path, dpi=300)
    plt.close()