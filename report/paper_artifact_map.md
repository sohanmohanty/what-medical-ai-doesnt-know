# Paper Artifact Map

This note explains which parts of the current paper are best represented by the canonical `paper_core` run and which parts still rely on focused historical scripts.

## Canonical paper-core path

Command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_paper_core.ps1
```

Primary outputs:

- `results/metrics/paper_core_metrics.csv`
- `results/metrics/paper_core_summary.csv`
- `results/predictions/paper_core_predictions.csv`
- `results/manifests/paper_core_run_manifest.json`
- `results/manifests/paper_core_run_spec.md`
- `figures/runs/paper_core/`
- tracked paper-facing figures in `figures/paper/`

This path is intended to support the paper's core benchmark story:

- clean vs corrupted benchmark evaluation
- WDBC vs Statlog robustness contrast
- logistic regression vs random forest vs gradient boosting
- MCAR vs MAR vs MNAR trends across rates

## Focused extension analyses

Some focused analyses in the current paper remain tied to older project-era scripts and outputs:

- calibration-specific reliability work
- focused imputer comparisons
- training-regime comparisons
- missingness-indicator comparisons

These remain valuable and are retained for provenance, but they are not yet fully migrated into the canonical `paper_core` path.

## Interpretation

The repo should currently be read as:

- one canonical official benchmark path for the main comparative study
- plus retained historical extension scripts for focused analyses that have not yet been fully unified
