# Paper Core Config

This config directory defines the canonical paper-facing benchmark run.

It is intentionally smaller than the largest exploratory grid, but still broad enough to support the main comparative story in the report.

The `paper_core` preset uses:

- both benchmark datasets
- all three model families
- simple imputation only
- all three missingness mechanisms
- all four missingness rates
- `clean_train_corrupt_test` only
- repeated outer cross-validation with inner tuning

Run it with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_paper_core.ps1
```

Its main outputs are:

- `results/metrics/paper_core_metrics.csv`
- `results/metrics/paper_core_summary.csv`
- `results/predictions/paper_core_predictions.csv`
- `results/manifests/paper_core_run_manifest.json`
- `results/manifests/paper_core_run_spec.md`
- `results/masks/paper_core/`
- `figures/runs/paper_core/`
