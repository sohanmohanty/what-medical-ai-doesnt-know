# Architecture Overview

## Current Repo Audit

The current repository is already a strong research system. Its strongest qualities are:

- a **config-driven benchmark runner** in `src/experiments/run_configured_experiment.py`
- structured experiment definitions in `configs/`
- reproducible stored outputs in `results/`, `figures/`, and `report/`
- automated checks in `tests/`
- a canonical paper-facing path centered on `paper_core`

In other words, the repo already contains a real engine. The current architecture preserves that engine and adds a readable interface on top.

## What The Repo Currently Does

Today the project:

- loads public benchmark datasets
- injects MCAR, MAR, and MNAR missingness
- trains logistic regression, random forest, and gradient boosting models
- compares multiple imputers
- evaluates accuracy, ROC-AUC, Brier score, and ECE
- stores metrics, predictions, manifests, masks, and figures
- supports paper generation and reproducibility tracking

## Components To Preserve

These pieces should remain the analytical foundation:

- `configs/`
  - Keeps the benchmark configurable and reproducible.
- `src/`
  - Contains the actual experiment logic, missingness machinery, preprocessing, and evaluation code.
- `scripts/run_paper_core.ps1`
  - Remains the canonical paper-facing benchmark entry point.
- `results/metrics/paper_core_summary.csv`
  - Best seed artifact for the first frontend experience.
- `results/manifests/*.json`
  - Useful for provenance, display metadata, and future methodology pages.
- `tests/`
  - Important for keeping the research core reliable while the product layer evolves.

## What Feels Too Research-Only

These are valuable, but they are not enough on their own for a reader encountering the project for the first time:

- CSV-heavy outputs without a frontend contract
- figure and paper assets that require substantial context to understand
- many focused historical scripts that are good for provenance but not for product integration
- no stable explanation layer for nontechnical visitors
- no interaction model for nontechnical visitors
- no deterministic explanation system translating metrics into plain language

## What The Interface Adds

The interface layer is intentionally explanation-facing rather than model-facing:

- a web frontend
- a frontend-friendly artifact format
- a deterministic explanation layer
- a trust/stability mapping derived from stored benchmark metrics
- content architecture for general vs technical audiences
- navigation, disclaimers, and storytelling pages

## Target Architecture

The cleanest first version keeps the existing Python benchmark intact and adds a thin presentation layer on top.

### Layer 1: Research Engine

- `src/`
- `configs/`
- existing scripts and tests

This layer continues to generate canonical experiment outputs.

### Layer 2: Frontend Artifact Bridge

- `scripts/export_frontend_artifacts.py`
- `artifacts/frontend/`

This layer reads saved benchmark summaries and emits a stable JSON contract for the web app. It is intentionally lightweight and uses precomputed artifacts instead of a live backend.

### Layer 3: Web Explorer

- `web/`

This layer consumes the JSON artifact and focuses on:

- explanation
- interaction
- trust visualization
- methodology storytelling

## Recommended Directory Structure

```text
configs/                  Existing experiment definitions
src/                      Existing benchmark engine
scripts/                  Existing benchmark commands + artifact export
results/                  Existing saved research outputs
figures/                  Existing figures and run summaries
artifacts/frontend/       Precomputed JSON files for the web app
web/                      Next.js + TypeScript frontend
docs/                     Product, architecture, methodology, and migration docs
```

## Data Flow

```text
Canonical benchmark run
  -> results/metrics/paper_core_summary.csv
  -> scripts/export_frontend_artifacts.py
  -> artifacts/frontend/paper_core_explorer.json
  -> web/app/explorer/page.tsx
  -> interactive UI + deterministic explanation layer
```

## Frontend Contract

The JSON artifact exposes:

- dataset metadata and plain-English descriptions
- model metadata and positioning notes
- missingness mechanism descriptions
- available missingness rates
- per-scenario metric summaries
- clean-vs-corrupt deltas
- a derived stability/trust score

This supports:

- landing page context
- a functional explorer shell
- general and technical views
- stress-test comparisons by rate

## Why No Backend Yet

A backend is unnecessary for the first version because:

- the research outputs are already precomputed
- the product is educational and analytical, not transactional
- static artifacts are easier to audit and deploy
- it avoids introducing privacy or health-risk concerns

API routes can be added later only if needed for:

- dynamically filtered artifact loading
- future scenario simulation
- richer reliability-curve payloads

## Current Architectural Direction

The benchmark remains the engine.  
The artifact export becomes the bridge.  
The web app becomes the public identity.
