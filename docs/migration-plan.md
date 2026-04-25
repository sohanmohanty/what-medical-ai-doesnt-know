# Development Roadmap

This file records how the project moved from a research benchmark into an interactive benchmark explorer, and what remains to improve. It is not an external audit; it is a project roadmap.

## Completed

### Research Benchmark

- Config-driven experiment runner in `src/experiments/run_configured_experiment.py`
- Public benchmark datasets for WDBC and Statlog Heart
- MCAR, MAR, and MNAR missingness simulations
- Logistic regression, random forest, and gradient boosting models
- ROC-AUC, accuracy, Brier score, ECE, and reliability outputs
- Canonical `paper_core` run artifacts
- Automated tests for configuration, data handling, splitting, missingness, and evaluation

### Artifact Bridge

- `scripts/export_frontend_artifacts.py`
- `artifacts/frontend/paper_core_explorer.json`
- Scenario-level metrics for the frontend
- Trust-score components derived from ranking retention, calibration, and missingness severity
- Reliability data for the calibration view

### Web App

- Landing page with confidence-vs-trust framing
- Explorer with dataset, model, mechanism, and missingness-rate controls
- General and technical views
- Plain-English deterministic explanations
- Trust meter and model comparison cards
- Methodology and About pages
- Educational disclaimer and non-diagnostic framing

## Current Limitations

- Example input controls are illustrative; they do not yet represent feature-level counterfactual experiments.
- Trust thresholds are implemented in code but should be documented more explicitly in the methodology.
- The explorer uses scenario-level summaries rather than exposing every fold-level artifact.
- The current deployment path has not yet been finalized.

## Next Work

1. Add feature-level missingness summaries so example inputs can become honest feature-impact controls.
2. Document the trust-score formula and thresholds in the methodology.
3. Add a scenario comparison view for side-by-side model or mechanism comparisons.
4. Test mobile layouts more thoroughly.
5. Capture screenshots and prepare the first public deployment.

## Design Constraints

- Do not turn the project into a diagnostic tool.
- Do not collect personal health data.
- Do not add a chatbot or symptom checker.
- Do not make clinical claims beyond the benchmark setting.
- Keep the benchmark as the source of truth.
