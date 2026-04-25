from pathlib import Path
import pandas as pd


def main():
    files = [
        "results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv",
        "results/metrics/wdbc_logreg_mar_indicator_compare_summary.csv",
        "results/metrics/wdbc_logreg_mnar_indicator_compare_summary.csv",
    ]

    dfs = [pd.read_csv(f) for f in files]
    combined = pd.concat(dfs, ignore_index=True).sort_values(["mechanism", "variant", "rate"])

    out = "results/metrics/wdbc_logreg_indicator_compare_combined_summary.csv"
    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    combined.to_csv(out, index=False)

    print("Saved:")
    print(out)


if __name__ == "__main__":
    main()
