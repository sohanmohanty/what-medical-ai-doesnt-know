from pathlib import Path
import pandas as pd


def main():
    files = [
        "results/metrics/statlog_logreg_mcar_5fold_summary.csv",
        "results/metrics/statlog_logreg_mar_5fold_summary.csv",
        "results/metrics/statlog_logreg_mnar_5fold_summary.csv",
        "results/metrics/statlog_rf_mcar_5fold_summary.csv",
        "results/metrics/statlog_rf_mar_5fold_summary.csv",
        "results/metrics/statlog_rf_mnar_5fold_summary.csv",
        "results/metrics/statlog_gb_mcar_5fold_summary.csv",
        "results/metrics/statlog_gb_mar_5fold_summary.csv",
        "results/metrics/statlog_gb_mnar_5fold_summary.csv",
    ]

    dfs = [pd.read_csv(f) for f in files]
    combined = pd.concat(dfs, ignore_index=True).sort_values(["model", "mechanism", "rate"])

    out = "results/metrics/statlog_combined_model_mechanism_summary.csv"
    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    combined.to_csv(out, index=False)

    print("Saved:")
    print(out)


if __name__ == "__main__":
    main()
