from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    input_path = "results/metrics/clean_baseline_combined.csv"
    output_path = "figures/clean_baseline_brier.png"

    df = pd.read_csv(input_path)

    datasets = df["dataset"].unique().tolist()
    models = ["logistic_regression", "random_forest", "gradient_boosting"]

    x = list(range(len(datasets)))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, model in enumerate(models):
        model_df = df[df["model"] == model].set_index("dataset").reindex(datasets)
        offsets = [val + (i - 1) * width for val in x]

        ax.bar(
            offsets,
            model_df["mean_brier"],
            width=width,
            label=model,
            yerr=model_df["std_brier"],
            capsize=4,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    ax.set_ylabel("Mean Brier Score")
    ax.set_title("Clean Baseline Comparison by Dataset")
    ax.legend()
    plt.tight_layout()

    Path("figures").mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print("Saved figure:")
    print(output_path)


if __name__ == "__main__":
    main()