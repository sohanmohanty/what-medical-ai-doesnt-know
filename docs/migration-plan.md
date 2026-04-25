# Migration Plan

## Goal

Transform the current repository from a research benchmark with saved artifacts into a flagship, user-facing project centered on trustworthy medical AI under uncertainty.

## Guiding Principle

Do not replace the benchmark. Wrap it.

The strongest technical move is to preserve the research core and add a presentation layer that makes the work accessible, memorable, and portfolio-ready.

## Phase 1: Audit And Product Definition

### Objectives

- inspect the existing repo
- identify what should remain canonical
- define the public-facing product identity
- document the architecture and migration path

### Status

- complete repo audit performed
- canonical runner identified
- reusable result tables identified
- initial product docs added

## Phase 2: Foundation

### Objectives

- create the initial `web/` application
- establish design language and navigation
- build landing, explorer shell, methodology, and about pages
- wire the app to a real frontend artifact instead of static prose only

### Status

- complete for the first working version

## Phase 3: Benchmark Integration

### Objectives

- formalize the benchmark-to-frontend export path
- use canonical outputs as the default data source
- add stability scoring and trust-state mapping
- expose real benchmark comparisons in the explorer

### Deliverables

- `scripts/export_frontend_artifacts.py`
- `artifacts/frontend/paper_core_explorer.json`
- frontend data loader and explorer state model

### Status

- complete for scenario-level benchmark integration
- reliability views and model comparison are powered by saved artifact data

## Phase 4: Technical Storytelling

### Objectives

- add richer technical visualizations
- integrate calibration and reliability artifacts
- sharpen the methodology narrative
- expand the explanation layer for general and technical audiences

### Next Artifacts To Export

- reliability bins for calibration plots
- selected fold-level predictions for example case walkthroughs
- feature-level missingness impact summaries
- clean-vs-corrupt comparison groups for model cards

## Phase 5: Polish

### Objectives

- tighten copy across the site
- improve accessibility and keyboard behavior
- verify responsive layout
- polish repo presentation and README
- prepare deployment workflow

## Recommended Sequencing

1. Treat `paper_core` as the canonical product seed.
2. Use summary metrics first, not raw predictions, for the first public explorer.
3. Add fold-level reliability data only after the summary-driven explorer feels coherent.
4. Add feature-toggle interactions only when exported artifacts support them honestly.

## Risks To Avoid

- turning the app into a fake medical tool
- overbuilding a backend too early
- creating decorative trust visuals that are not tied to actual metrics
- burying the core message under too much ML jargon
- letting the project feel like "just a paper with a nicer homepage"

## Immediate Next Build Steps

- add richer feature-level missingness summaries
- document trust-score thresholds in the methodology
- refine mobile layouts and capture portfolio screenshots
- introduce feature-dropout interaction only after artifact support exists
- deploy a preview build

## Definition Of "MVP Complete"

- the landing page clearly explains the project in under one minute
- the explorer uses real benchmark-derived data
- the technical mode exposes calibration-sensitive metrics
- the methodology page explains the setup and limitations responsibly
- the repo reads like a coherent flagship project, not only a benchmark archive
