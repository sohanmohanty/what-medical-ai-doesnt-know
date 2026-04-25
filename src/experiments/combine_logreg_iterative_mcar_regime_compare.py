from pathlib import Path
import pandas as pd


def main():
    files = [
        "results/metrics/wdbc_logreg_iterative_mcar_regime_compare_summary.csv",
        "results/metrics/statlog_logreg_iterative_mcar_regime_compare_summary.csv",
    ]

    dfs = [pd.read_csv(f) for f in files]
    combined = pd.concat(dfs, ignore_index=True).sort_values(["dataset", "regime", "rate"])

    out = "results/metrics/combined_logreg_iterative_mcar_regime_compare_summary.csv"
    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    combined.to_csv(out, index=False)

    print("Saved:")
    print(out)


if __name__ == "__main__":
    main()
