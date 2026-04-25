from pathlib import Path

import pandas as pd


def main():
    input_files = [
        "results/metrics/wdbc_logreg_mcar_5fold_summary.csv",
        "results/metrics/wdbc_logreg_mar_5fold_summary.csv",
        "results/metrics/wdbc_logreg_mnar_5fold_summary.csv",
        "results/metrics/statlog_logreg_mcar_5fold_summary.csv",
        "results/metrics/statlog_logreg_mar_5fold_summary.csv",
        "results/metrics/statlog_logreg_mnar_5fold_summary.csv",
    ]

    dfs = [pd.read_csv(path) for path in input_files]
    combined_df = pd.concat(dfs, ignore_index=True)

    combined_df = combined_df.sort_values(
        ["dataset", "mechanism", "rate"],
        ascending=[True, True, True],
    )

    output_path = "results/metrics/combined_logreg_mechanism_summary.csv"
    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(output_path, index=False)

    print("Saved:")
    print(output_path)

    print("\nCombined mechanism summary:")
    print(combined_df)


if __name__ == "__main__":
    main()