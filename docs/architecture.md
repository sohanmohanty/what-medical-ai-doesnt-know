# Architecture

## Overview

The project has two connected systems:

- a Python benchmark that generates reproducible missing-data robustness results
- a Next.js web app that reads those saved results and presents them through an interactive explorer

The benchmark remains the source of truth. The web app does not train models in the browser, collect user data, or make clinical predictions. It reads precomputed artifacts and explains how model behavior changes under controlled missingness.

## Research Engine

The research layer is responsible for data loading, missingness simulation, model training, evaluation, and saved artifacts.

Key directories:

- `configs/`: YAML definitions for datasets, models, imputers, and experiment grids
- `src/`: Python package for data loading, preprocessing, missingness, modeling, evaluation, plotting, and experiments
- `scripts/`: reproducible entry points for common runs
- `results/`: metrics, predictions, masks, manifests, and sample outputs
- `figures/`: generated figures and reliability plots
- `tests/`: integrity checks for the benchmark core

The canonical paper-facing benchmark path is:

```text
scripts/run_paper_core.ps1
  -> src/experiments/run_configured_experiment.py
  -> results/metrics/paper_core_summary.csv
  -> results/predictions/paper_core_predictions.csv
  -> results/manifests/paper_core_run_manifest.json
```

## Artifact Bridge

The frontend should not parse arbitrary result folders directly. Instead, a small export script converts benchmark outputs into a stable JSON contract:

```text
scripts/export_frontend_artifacts.py
  -> artifacts/frontend/paper_core_explorer.json
```

The exported artifact includes:

- dataset, model, and missingness metadata
- available missingness rates
- per-scenario metrics
- clean-vs-missing deltas
- trust-score components
- model-comparison slices
- reliability data for calibration views

This keeps the app simple, auditable, and easy to deploy.

## Web App

The web layer lives in `web/` and uses Next.js, TypeScript, and Tailwind CSS.

Main pages:

- `/`: overview and confidence-vs-trust framing
- `/explorer`: interactive benchmark explorer
- `/methodology`: datasets, models, metrics, missingness mechanisms, and limitations
- `/about`: motivation and project framing

The app reads:

```text
artifacts/frontend/paper_core_explorer.json
```

through:

```text
web/lib/load-explorer-data.ts
```

The deterministic explanation layer is implemented in:

```text
web/lib/explainer.ts
```

## Data Flow

```text
Public benchmark datasets
  -> configured Python experiments
  -> saved metrics and predictions
  -> frontend JSON artifact
  -> interactive explorer and explanation layer
```

## Static Artifact Model

The current web app is intentionally static. Benchmark runs happen in Python, then a JSON artifact is exported for the interface. This keeps the public-facing experience reproducible, easy to deploy, and separate from any personal medical-data handling.

A server layer would only be useful for a later version that needs dynamic simulations or richer artifact browsing beyond precomputed results.
