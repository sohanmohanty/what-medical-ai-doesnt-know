# Methodology

## Scope

The benchmark studies how clinical prediction models behave when parts of the input data are missing. The goal is not to build a diagnostic tool. The goal is to understand how robustness and trustworthiness change under controlled missing-data conditions.

## Datasets

The current benchmark uses two public datasets:

- **WDBC**
  - A relatively clean and separable breast tumor classification benchmark.
- **Statlog Heart**
  - A smaller and noisier heart disease classification benchmark.

They are intentionally paired because they differ in difficulty and robustness.

## Models

The benchmark currently evaluates:

- logistic regression
- random forest
- gradient boosting

These models give a useful contrast between interpretable linear behavior and more flexible tree-based behavior.

## Missingness Mechanisms

Three controlled mechanisms are injected:

- **MCAR**: values disappear independently of the observed data
- **MAR**: missingness depends on other observed variables
- **MNAR**: missingness depends on the value being hidden

The interface should explain these mechanisms plainly because they lead to different degradation patterns and different trust implications.

## Missingness Rates

The canonical benchmark studies missingness at:

- 10%
- 20%
- 30%
- 50%

These rates are high enough to make degradation patterns visible without making every scenario trivial.

## Evaluation Metrics

Calibration-sensitive metrics are treated as first-class outcomes.

### Discrimination

- ROC-AUC
- Accuracy

These show how well a model separates classes or gets labels right.

### Probability Quality

- Brier score
- Expected Calibration Error (ECE)

These show how trustworthy the predicted probabilities are.

This distinction matters because a model can still rank cases reasonably well while providing probabilities that are less reliable.

## Canonical Benchmark Path

The browser app should draw first from the canonical paper-facing benchmark path:

- runner: `src/experiments/run_configured_experiment.py`
- preset entry point: `scripts/run_paper_core.ps1`
- summary seed: `results/metrics/paper_core_summary.csv`

## Important Limitations

- The datasets are public benchmarks, not live clinical systems.
- The missingness mechanisms are controlled constructions, not learned from hospital workflows.
- The public app is educational and analytical, not diagnostic.
- The current app summarizes scenario-level trends and selected reliability views; future versions can expose richer fold-level calibration artifacts.

## How Results Should Be Described

- Avoid saying a model is "good" in general.
- Prefer saying a model appears more stable, more fragile, or less trustworthy under specific missing-data conditions.
- Emphasize that calibration and uncertainty matter, especially in high-stakes settings.
- Keep the distinction between benchmark findings and real medical deployment explicit.
