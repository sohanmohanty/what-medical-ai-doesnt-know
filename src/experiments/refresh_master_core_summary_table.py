from pathlib import Path
import pandas as pd


def safe_read(path):
    path = Path(path)
    if path.exists():
        df = pd.read_csv(path)
        df["source_file"] = path.name
        return df
    return None


def main():
    files = [
        "results/metrics/wdbc_combined_model_mechanism_summary.csv",
        "results/metrics/statlog_combined_model_mechanism_summary.csv",
        "results/metrics/combined_logreg_mechanism_summary.csv",
        "results/metrics/combined_logreg_iterative_calibration_summary.csv",
        "results/metrics/wdbc_logreg_mcar_imputer_compare_summary.csv",
        "results/metrics/wdbc_logreg_mar_imputer_compare_summary.csv",
        "results/metrics/wdbc_logreg_mnar_imputer_compare_summary.csv",
        "results/metrics/wdbc_logreg_iterative_mcar_regime_compare_summary.csv",
        "results/metrics/statlog_logreg_iterative_mcar_regime_compare_summary.csv",
        "results/metrics/combined_logreg_iterative_mcar_regime_compare_summary.csv",
        "results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv",
        "results/metrics/wdbc_logreg_mar_indicator_compare_summary.csv",
        "results/metrics/wdbc_logreg_mnar_indicator_compare_summary.csv",
        "results/metrics/wdbc_logreg_indicator_compare_combined_summary.csv",
    ]

    dfs = [safe_read(f) for f in files]
    dfs = [df for df in dfs if df is not None]

    combined = pd.concat(dfs, ignore_index=True, sort=False)

    out = Path("results/metrics/master_core_summary_table.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(out, index=False)

    print("Saved:")
    print(out)
    print("\nRows, cols:")
    print(combined.shape)


if __name__ == "__main__":
    main()
