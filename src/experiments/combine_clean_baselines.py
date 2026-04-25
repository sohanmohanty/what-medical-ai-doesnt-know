from pathlib import Path

import pandas as pd


def main():
    wdbc_path = "results/metrics/wdbc_baseline_summary.csv"
    statlog_path = "results/metrics/statlog_baseline_summary.csv"
    output_path = "results/metrics/clean_baseline_combined.csv"

    wdbc_df = pd.read_csv(wdbc_path)
    statlog_df = pd.read_csv(statlog_path)

    combined_df = pd.concat([wdbc_df, statlog_df], ignore_index=True)
    combined_df = combined_df.sort_values(["dataset", "mean_brier", "mean_roc_auc"], ascending=[True, True, False])

    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(output_path, index=False)

    print("Combined clean baseline table saved.")
    print(f"Output: {output_path}")
    print("\nCombined table:")
    print(combined_df)


if __name__ == "__main__":
    main()