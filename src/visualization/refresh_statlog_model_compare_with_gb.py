from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def make_plot(metric, ylabel):
    input_path = "results/metrics/statlog_combined_model_mechanism_summary.csv"
    df = pd.read_csv(input_path).sort_values(["mechanism", "model", "rate"])

    for mechanism in ["mcar", "mar", "mnar"]:
        sub = df[df["mechanism"] == mechanism]
        output_path = f"figures/statlog_{mechanism}_model_compare_{metric}.png"

        plt.figure(figsize=(7, 5))

        for model_name in ["logistic_regression", "random_forest", "gradient_boosting"]:
            model_df = sub[sub["model"] == model_name].sort_values("rate")
            if model_df.empty:
                continue

            plt.errorbar(
                model_df["rate"],
                model_df[f"mean_{metric}"],
                yerr=model_df[f"std_{metric}"],
                marker="o",
                capsize=4,
                label=model_name,
            )

        plt.xlabel("Missingness rate")
        plt.ylabel(ylabel)
        plt.title(f"Statlog: {ylabel} by Model under {mechanism.upper()}")
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
