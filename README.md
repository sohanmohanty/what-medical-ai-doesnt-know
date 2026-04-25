# What Medical AI Doesn't Know

This repository has two connected parts:

- a **config-driven research benchmark** for studying how clinical machine learning models behave when inputs are partially missing
- an **interactive web app** that turns those results into a readable explorer of calibration, uncertainty, and trust

The benchmark produces the evidence. The web app helps people understand what the evidence means.

## What This Repo Does

The project uses two public benchmark datasets:

- Breast Cancer Wisconsin (Diagnostic)
- Statlog Heart

For each dataset, the framework can:

- inject MCAR, MAR, and MNAR missingness
- train logistic regression, random forest, and gradient boosting models
- compare imputation strategies
- evaluate both discrimination and calibration
- save metrics, predictions, manifests, masks, figures, and the paper
- export frontend-friendly JSON artifacts for the public app layer

This repository can be used in two ways:

- **Research mode:** rerun benchmarks, inspect saved artifacts, and extend the experimental framework
- **Explorer mode:** open the `web/` app and inspect the saved benchmark results through an interactive interface

## Read This First

If you are new to the repo, start here:

- `docs/project-brief.md` for the product direction
- `docs/architecture.md` for the current repo audit and target structure
- `docs/migration-plan.md` for the phased transformation plan
- `report/paper.md` and `report/paper.pdf` for the write-up
- `scripts/run_paper_core.ps1` for the canonical paper-facing benchmark run
- `scripts/export_frontend_artifacts.py` for the benchmark-to-app bridge
- `web/` for the Next.js app
- `src/experiments/run_configured_experiment.py` for the main official runner
- `configs/` for the experiment definitions
- `results/` and `figures/` for the saved outputs

## Repo Map

- `configs/` holds the YAML configuration files that define datasets, models, imputers, CV settings, and output paths.
- `data/raw/` holds the benchmark datasets used by the project.
- `data/metadata/` holds saved schema files that describe the datasets.
- `src/` holds the Python code for loading data, injecting missingness, building pipelines, running experiments, and plotting results.
- `scripts/` holds easy entry-point commands so you do not need to remember long Python commands.
- `results/` holds numeric outputs such as metrics, predictions, manifests, and masks.
- `figures/` holds image outputs.
- `artifacts/frontend/` holds precomputed JSON files for the web app.
- `web/` holds the Next.js + TypeScript browser app.
- `docs/` holds the product brief, architecture notes, methodology, migration plan, and next-step docs.
- `report/` holds the paper and the paper artifact map.
- `tests/` holds the automated integrity checks.
- `notebooks/` holds supporting exploratory notebooks.

## Config Files

The official runner gets its instructions from the YAML files in `configs/`:

- `configs/datasets.yaml` defines dataset loaders, feature typing, and missingness profiles.
- `configs/models.yaml` defines model defaults and tuning grids.
- `configs/imputers.yaml` defines imputer defaults and tuning grids.
- `configs/experiments.yaml` defines the main benchmark grid and default output paths.
- `configs/paper_core/experiments.yaml` defines the smaller `paper_core` benchmark preset used for the paper-facing official run.

## Official Vs Legacy

### Official workflow

For new work, the canonical execution path is:

- configs in `configs/`
- runner: `src/experiments/run_configured_experiment.py`
- helper scripts include:
- `scripts/run_paper_core.ps1`
- `scripts/run_core_configured_experiment.ps1`
- `scripts/run_graph_preview.ps1`
- `scripts/run_smoke_experiment.ps1`

The official runner is the recommended path for:

- new experiments
- reproducibility checks
- regenerated manifests, metrics, predictions, masks, and run-summary figures

The canonical paper-facing preset is:

- config override: `configs/paper_core/experiments.yaml`
- command: `powershell -ExecutionPolicy Bypass -File scripts\run_paper_core.ps1`
- human-readable run spec: `results/manifests/paper_core_run_spec.md`

### Legacy provenance

The repo still keeps older focused scripts in:

- `src/experiments/`
- `src/visualization/`

These are useful for historical provenance and for understanding how some of the original project outputs were assembled, but they are not the recommended entry point for new runs.

## Environment Setup

Using pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Using Conda:

```powershell
conda env create -f environment.yml
conda activate robust-missing-clinical-ml
```

## Main Commands

### 1. Smoke test

Runs a tiny built-in sample check of the framework:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_smoke_experiment.ps1
```

Outputs go to:

- `results/samples/smoke_test/`
- `figures/samples/smoke_test/`

### 2. Graph preview

Runs a small built-in preview that is much faster than the full benchmark but still produces meaningful summary curves:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_graph_preview.ps1
```

Outputs go to:

- `results/samples/graph_preview/`
- `figures/samples/graph_preview/`

### 3. Canonical paper-core run

Runs the official paper-facing benchmark preset:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_paper_core.ps1
```

Outputs go to:

- `results/metrics/paper_core_metrics.csv`
- `results/metrics/paper_core_summary.csv`
- `results/predictions/paper_core_predictions.csv`
- `results/manifests/paper_core_run_manifest.json`
- `results/manifests/paper_core_run_spec.md`
- `results/masks/paper_core/`
- `figures/runs/paper_core/`

### 4. Full configured benchmark

Runs the main default benchmark grid:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_core_configured_experiment.ps1
```

This can be expensive. For a custom filtered run, you can use the runner directly:

```powershell
python -m src.experiments.run_configured_experiment `
  --run-name my_custom_run `
  --datasets wdbc `
  --models logistic_regression `
  --imputers simple iterative `
  --mechanisms mcar mar `
  --rates 0.1 0.3 `
  --regimes clean_train_corrupt_test corrupt_train_corrupt_test `
  --max-outer-splits 2 `
  --max-seeds 2
```

Because `my_custom_run` is a non-canonical custom run name, its outputs will default to:

- `results/user_runs/my_custom_run/`
- `figures/user_runs/my_custom_run/`

### 5. Refresh packaged assets

```powershell
powershell -ExecutionPolicy Bypass -File scripts\refresh_project_assets.ps1
```

This refreshes:

- dataset schemas in `data/metadata/`
- manifests in `results/manifests/`
- top-level exports in `results/metrics.csv` and `results/predictions.csv` when applicable
- `report/paper.pdf`

### 6. Regenerate paper-facing figures

```powershell
powershell -ExecutionPolicy Bypass -File scripts\generate_final_figures.ps1
```

This reads saved result tables and regenerates the curated figures in `figures/paper/`.

### 7. Run the automated checks

```powershell
pytest
```

The test suite checks:

- config parsing and output namespacing
- dataset schema handling
- preprocessing behavior
- split reproducibility
- missingness mechanism sanity
- metric edge cases

### 8. Export frontend artifacts

Generates the JSON contract used by the web app from the canonical benchmark outputs:

```powershell
python scripts\export_frontend_artifacts.py
```

This writes:

- `artifacts/frontend/paper_core_explorer.json`

It currently integrates:

- `results/metrics/paper_core_summary.csv`
- `results/predictions/paper_core_predictions.csv`
- `results/predictions/baseline_predictions.csv` when available

### 9. Run the web app

From the `web/` directory:

```powershell
npm install
npm run dev
```

The current web app includes:

- a landing page
- an explorer with general and technical modes
- a methodology page
- an about page

The browser app reads:

- `artifacts/frontend/paper_core_explorer.json`

## How Outputs Are Organized

### Results

- `results/metrics/` holds detailed metric tables and combined summaries.
- `results/predictions/` holds prediction artifacts and reliability tables.
- `results/manifests/` holds run manifests, fold definitions, and reproducibility metadata.
- `results/masks/` holds tracked official mask artifacts such as `paper_core`.
- `results/samples/` holds built-in smoke and preview runs.
- `results/user_runs/` holds custom non-canonical runs you launch yourself.
- `results/metrics.csv` and `results/predictions.csv` are top-level packaged exports.

### Figures

- `figures/paper/` holds the curated paper-facing figures referenced by `report/paper.md`.
- `figures/runs/` holds official run-summary figures such as `paper_core`.
- `figures/samples/` holds built-in sample and preview figures.
- `figures/user_runs/` holds custom user-run figures.
- `figures/old/` holds older development-era or non-paper-facing figures kept for provenance.

## Paper Status

The repo now has a clean official framework and a canonical `paper_core` run. The paper-facing figures and project artifacts in the repo are real project outputs, but some focused extensions still depend on older project-era scripts rather than a single fully unified path.

For the clearest mapping between the report and the artifacts, see:

- `report/paper_artifact_map.md`

## Why This Matters

Missing-data robustness is not only about whether ROC-AUC stays high. A model can continue to rank patients reasonably well while producing probabilities that are less trustworthy. The benchmark evaluates both discrimination and calibration, which makes it more informative than an accuracy-only check.
