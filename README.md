# What Medical AI Doesn't Know

An interactive research project about clinical machine learning under missing data.

This repository combines a reproducible Python benchmark with a polished web explorer and a scholarly report. The central question is simple:

> How much should we trust a medical prediction model when part of the patient record is missing?

The project is educational and research-oriented. It is not medical advice, not a diagnosis tool, not a symptom checker, and it does not collect user medical data.

## Start Here

If you want the quick public overview:

1. Open the web app in `web/` to understand the project visually.
2. Read `report/paper.pdf` for the research write-up.
3. Read `docs/methodology.md` for the plain-English methodology.
4. Inspect `artifacts/frontend/paper_core_explorer.json` to see the benchmark-to-app artifact.
5. Use `scripts/run_paper_core.ps1` if you want to rerun the canonical benchmark.

If you are evaluating the technical work, start with `report/paper.pdf`. The paper is the primary academic artifact; the website is a companion interface that makes the benchmark easier to interpret.

The benchmark produces the evidence. The web app makes that evidence understandable.

## What The Project Shows

Clinical prediction models are often evaluated on complete records, but real deployment settings may involve unavailable labs, skipped tests, incomplete measurements, or partially observed features. This project studies how models behave when those inputs are missing.

The benchmark evaluates:

- missingness mechanisms: MCAR, MAR, and MNAR
- models: logistic regression, random forest, and gradient boosting
- datasets: Wisconsin Diagnostic Breast Cancer and Statlog Heart
- metrics: accuracy, ROC-AUC, Brier score, expected calibration error, and reliability diagrams
- robustness questions: whether ranking performance and probability trust degrade in the same way

The main lesson is that a model can still rank cases reasonably well while its reported probabilities become less trustworthy. That distinction matters in high-stakes settings.

## Project Artifacts

- `web/` contains the Next.js interactive explorer.
- `report/paper.pdf` is the formatted research paper.
- `report/paper.md` is the paper source.
- `report/paper_artifact_map.md` maps claims in the paper to saved artifacts.
- `artifacts/frontend/paper_core_explorer.json` is the static JSON consumed by the app.
- `results/metrics/paper_core_summary.csv` contains canonical benchmark summaries.
- `results/predictions/paper_core_predictions.csv` contains prediction-level outputs used for reliability views.
- `figures/paper/` contains curated figures used in the paper.
- `docs/` contains the project brief, architecture, methodology, migration plan, and content strategy.

## Run The Web App

The app uses precomputed benchmark artifacts, so you do not need to rerun the full benchmark just to view the site.

From the repository root:

```powershell
cd web
npm install
npm run dev
```

Then open:

```text
http://localhost:3000
```

On Windows, if `npm` is installed but not on your PowerShell path, use:

```powershell
cd C:\path\to\robust-missing-clinical-ml\web
& "C:\Program Files\nodejs\npm.cmd" install
& "C:\Program Files\nodejs\npm.cmd" run dev
```

## Publish A Clickable Website

For admissions readers or judges, the website should be deployed as a normal public link rather than requiring anyone to download the repo. The public link should introduce the idea quickly, while the repository and paper should demonstrate the technical depth.

The simplest path is:

1. Create a GitHub account.
2. Push this repository to GitHub.
3. Create a Vercel account and import the GitHub repository.
4. Set the Vercel project root directory to `web`.
5. Use the default Next.js build command, `npm run build`.
6. Deploy and share the generated `vercel.app` URL.

The web app is designed for this workflow. It reads a deployable artifact at `web/data/paper_core_explorer.json`, which is refreshed by:

```powershell
python scripts\export_frontend_artifacts.py
```

The research source of truth remains in `results/`, `figures/`, `artifacts/`, and `report/`. The website is the interpretation layer that makes those outputs easier to explore.

## Reproduce The Research Pipeline

Create a Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation scripts, run project scripts with `powershell -ExecutionPolicy Bypass` as shown below.

Run a quick smoke test:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_smoke_experiment.ps1
```

Run the canonical paper-facing benchmark:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_paper_core.ps1
```

Export the frontend artifact:

```powershell
python scripts\export_frontend_artifacts.py
```

Regenerate the paper PDF:

```powershell
python scripts\export_paper_pdf.py
```

Run automated checks:

```powershell
pytest
```

## Repository Map

- `configs/` defines datasets, models, imputers, and experiment grids.
- `data/` stores public benchmark datasets and metadata.
- `src/` contains the Python benchmark implementation.
- `scripts/` contains reproducible command-line entry points.
- `results/` stores metrics, predictions, masks, manifests, and run summaries.
- `figures/` stores generated figures.
- `artifacts/frontend/` stores static app-ready JSON artifacts.
- `web/` contains the browser interface.
- `docs/` contains planning, methodology, architecture, and content documentation.
- `report/` contains the paper and artifact map.
- `tests/` contains automated integrity checks.
- `notebooks/` contains supporting exploratory work.

## Research Design

The canonical benchmark compares model behavior under controlled missingness. The paper-facing run uses repeated stratified cross-validation with inner hyperparameter tuning, then evaluates both discrimination and calibration.

The study intentionally separates two ideas:

- **Performance:** whether the model still ranks or classifies cases well.
- **Trustworthiness:** whether the reported probabilities remain calibrated and reliable.

This distinction is the reason the project emphasizes Brier score, ECE, and reliability diagrams alongside ROC-AUC.

## Documentation

Useful documentation files:

- `docs/project-brief.md`: project purpose and audience.
- `docs/architecture.md`: how the benchmark, artifacts, and web app fit together.
- `docs/deployment.md`: how to publish the web app as a clickable public link.
- `docs/methodology.md`: explanation of datasets, missingness, models, and metrics.
- `docs/migration-plan.md`: completed migration work and future development path.
- `docs/content-strategy.md`: public-facing language and narrative guardrails.
- `docs/next-steps.md`: current development priorities.

## Scope And Limitations

This project uses public benchmark datasets and controlled missingness simulations. It does not make patient-specific claims, provide treatment guidance, or represent a deployed clinical system.

The current version is best understood as a reproducible robustness benchmark plus an interpretability layer: a way to study and communicate how model reliability changes when clinical information is incomplete.
