# Paper Core Run Spec

This document describes the canonical paper-facing benchmark run for the current repo.

## Command

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_paper_core.ps1
```

## Config source

- `configs/paper_core/experiments.yaml`
- base datasets/models/imputers fall back to `configs/`

## Scope

- datasets: `wdbc`, `statlog_heart`
- models: `logistic_regression`, `random_forest`, `gradient_boosting`
- imputers: `simple`
- mechanisms: `mcar`, `mar`, `mnar`
- rates: `0.1`, `0.2`, `0.3`, `0.5`
- regime: `clean_train_corrupt_test`
- CV: repeated stratified 5-fold outer CV with 2 repeats
- tuning: 3-fold inner CV using ROC-AUC
- random seeds: `0`

## Intended purpose

`paper_core` is meant to regenerate the main benchmark comparison layer of the project in one practical, official path.

It is the best current fit for claims about:

- dataset-level robustness differences between WDBC and Statlog Heart
- model-level robustness differences across logistic regression, random forest, and gradient boosting
- mechanism and rate trends under controlled missingness
- the difference between clean baselines and corrupted evaluation performance

## Outputs

- `results/metrics/paper_core_metrics.csv`
- `results/metrics/paper_core_summary.csv`
- `results/predictions/paper_core_predictions.csv`
- `results/manifests/paper_core_run_manifest.json`
- `results/masks/paper_core/`
- `figures/runs/paper_core/`

## Boundary

This run is intended to be the canonical paper-facing benchmark path.

Focused extension analyses such as calibration-specific reliability work, imputer comparisons, regime comparisons, and missingness-indicator experiments may still rely on separate historical scripts until they are fully migrated into the official framework.
