# Results Directory

This directory stores the numeric outputs of the project.

If `src/` is the machinery, `results/` is where the machinery drops its tables and run receipts.

## Top-Level Exports

- `metrics.csv` is the current top-level summary export.
- `predictions.csv` is the current top-level prediction export.

These are refreshed by `scripts/refresh_project_assets.ps1` when relevant config-driven outputs are available.

## Main Subfolders

- `metrics/` holds detailed experiment-level and summary-level CSV files.
- `predictions/` holds saved prediction artifacts and reliability-table outputs.
- `manifests/` holds run manifests, fold definitions, and reproducibility metadata.
- `masks/` holds tracked official missingness-mask artifacts.
- `samples/` holds outputs from built-in sample commands such as the smoke test and graph preview.
- `user_runs/` holds outputs from custom non-canonical runs launched by the user.

## Official Tracked Outputs

The canonical paper-facing benchmark preset writes:

- `metrics/paper_core_metrics.csv`
- `metrics/paper_core_summary.csv`
- `predictions/paper_core_predictions.csv`
- `manifests/paper_core_run_manifest.json`
- `manifests/paper_core_run_spec.md`
- `masks/paper_core/`
- figures under `../figures/runs/paper_core/`

The broader default benchmark config writes:

- `metrics/core_missingness_grid_metrics.csv`
- `metrics/core_missingness_grid_summary.csv`
- `predictions/core_missingness_grid_predictions.csv`
- `manifests/core_missingness_grid_run_manifest.json`
- `masks/core_missingness_grid/`
- figures under `../figures/runs/core_missingness_grid/`

## Sample Outputs

Built-in sample and preview scripts write their outputs into namespaced folders such as:

- `samples/smoke_test/`
- `samples/graph_preview/`

Each sample run folder can contain:

- `metrics.csv`
- `summary.csv`
- `predictions.csv` when enabled
- `run_manifest.json`
- `masks/` when enabled

## Custom User Runs

Non-canonical custom runs you launch yourself are kept separate from built-in samples and official tracked outputs.

They are written under:

- `user_runs/<run_name>/`

A custom run folder can contain:

- `metrics.csv`
- `summary.csv`
- `predictions.csv` when enabled
- `run_manifest.json`
- `masks/` when enabled
