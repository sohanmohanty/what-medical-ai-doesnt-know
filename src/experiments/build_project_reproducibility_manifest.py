from pathlib import Path
import json

def existing(paths):
    return [p for p in paths if Path(p).exists()]

def main():
    manifest = {
        "core_metrics": existing([
            "results/metrics/clean_baseline_combined.csv",
            "results/metrics/combined_logreg_mechanism_summary.csv",
            "results/metrics/wdbc_combined_model_mechanism_summary.csv",
            "results/metrics/statlog_combined_model_mechanism_summary.csv",
            "results/metrics/combined_logreg_iterative_calibration_summary.csv",
            "results/metrics/master_core_summary_table.csv",
        ]),
        "calibration_outputs": existing([
            "results/metrics/wdbc_logreg_iterative_calibration_summary.csv",
            "results/metrics/statlog_logreg_iterative_calibration_summary.csv",
            "figures/paper/wdbc_logreg_iterative_ece_compare.png",
            "figures/paper/statlog_logreg_iterative_ece_compare.png",
            "figures/paper/logreg_iterative_wdbc_vs_statlog_ece.png",
        ]),
        "imputer_outputs": existing([
            "results/metrics/wdbc_logreg_mcar_imputer_compare_summary.csv",
            "results/metrics/wdbc_logreg_mar_imputer_compare_summary.csv",
            "results/metrics/wdbc_logreg_mnar_imputer_compare_summary.csv",
        ]),
        "regime_outputs": existing([
            "results/metrics/wdbc_logreg_iterative_mcar_regime_compare_summary.csv",
            "results/metrics/statlog_logreg_iterative_mcar_regime_compare_summary.csv",
            "results/metrics/combined_logreg_iterative_mcar_regime_compare_summary.csv",
        ]),
        "indicator_outputs": existing([
            "results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv",
            "results/metrics/wdbc_logreg_mar_indicator_compare_summary.csv",
            "results/metrics/wdbc_logreg_mnar_indicator_compare_summary.csv",
            "results/metrics/wdbc_logreg_indicator_compare_combined_summary.csv",
        ]),
    }

    out = Path("results/manifests/project_reproducibility_manifest.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Saved:")
    print(out)

if __name__ == "__main__":
    main()
