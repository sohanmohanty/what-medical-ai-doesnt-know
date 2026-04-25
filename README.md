# What Medical AI Doesn't Know

An interactive research project about clinical machine learning under missing data.

Created by Sohan Mohanty.

**Live site:** https://what-medical-ai-doesnt-know.vercel.app/

**Research paper:** https://what-medical-ai-doesnt-know.vercel.app/paper.pdf

This repository combines a reproducible Python benchmark with an interactive web explorer and a scholarly report. The study asks:

> How much should we trust a medical prediction model when part of the patient record is missing?

The project is educational and research-oriented. It is not medical advice, not a diagnosis tool, not a symptom checker, and it does not collect user medical data.

Copyright (c) 2026 Sohan Mohanty. All rights reserved.

## Start Here

Suggested reading order:

1. Open the live site: https://what-medical-ai-doesnt-know.vercel.app/
2. Read `report/paper.pdf` for the repository copy of the research write-up.
3. Read `docs/methodology.md` for the methodology overview.
4. Inspect `artifacts/frontend/paper_core_explorer.json` to see the benchmark-to-app artifact.
5. Use `scripts/run_paper_core.ps1` if you want to rerun the canonical benchmark.

The paper is the primary academic artifact. The website is a companion interface that makes the benchmark easier to inspect and interpret.

The benchmark produces the evidence. The web app makes that evidence understandable.

## What The Project Shows

Clinical prediction models are often evaluated on complete records, but real deployment settings may involve unavailable labs, skipped tests, incomplete measurements, or partially observed features. This project studies how models behave when those inputs are missing.

The benchmark evaluates:

- missingness mechanisms: MCAR, MAR, and MNAR
- models: logistic regression, random forest, and gradient boosting
- datasets: Wisconsin Diagnostic Breast Cancer and Statlog Heart
- metrics: accuracy, ROC-AUC, Brier score, expected calibration error, and reliability diagrams
- robustness questions: whether ranking performance and probability trust degrade in the same way

The central finding is that a model can still rank cases reasonably well while its reported probabilities become less trustworthy. That distinction matters in high-stakes settings.

## Project Artifacts

- `web/` contains the Next.js interactive explorer.
- `report/paper.pdf` is the formatted research paper.
- `web/public/paper.pdf` is the deployable website copy of the paper.
- `report/paper.md` is the paper source.
- `report/paper_artifact_map.md` maps claims in the paper to saved artifacts.
- `artifacts/frontend/paper_core_explorer.json` is the static JSON consumed by the app.
- `results/metrics/paper_core_summary.csv` contains canonical benchmark summaries.
- `results/predictions/paper_core_predictions.csv` contains prediction-level outputs used for reliability views.
- `figures/paper/` contains curated figures used in the paper.
- `docs/` contains methodology, architecture, and deployment notes.

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

## Deployment

The web app is designed for static deployment from the `web/` directory. The current deployment is available at:

```text
https://what-medical-ai-doesnt-know.vercel.app/
```

The deployed site also serves the formatted paper directly at:

```text
https://what-medical-ai-doesnt-know.vercel.app/paper.pdf
```

Current deployment settings:

- Hosting: Vercel
- Framework preset: Next.js
- Project root: `web`
- Install command: `npm install`
- Build command: `npm run build`
- Output directory: Next.js default

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
- `docs/` contains technical documentation for methodology, architecture, and deployment.
- `report/` contains the paper and artifact map.
- `tests/` contains automated integrity checks.
- `notebooks/` contains supporting exploratory work.

## Authorship And Use

This project was created by Sohan Mohanty as an independent research project. If you reference the work, please cite the repository using `CITATION.cff`.

This repository is currently shared without an open-source license. Unless a license is added later, no permission is granted for reuse, redistribution, or derivative works beyond normal viewing and citation.

## Research Design

The canonical benchmark compares model behavior under controlled missingness. The paper-facing run uses repeated stratified cross-validation with inner hyperparameter tuning, then evaluates both discrimination and calibration.

The study intentionally separates two ideas:

- **Performance:** whether the model still ranks or classifies cases well.
- **Trustworthiness:** whether the reported probabilities remain calibrated and reliable.

This distinction is the reason the project emphasizes Brier score, ECE, and reliability diagrams alongside ROC-AUC.

## Documentation

Useful documentation files:

- `docs/architecture.md`: how the benchmark, artifacts, and web app fit together.
- `docs/deployment.md`: deployment configuration for the web app.
- `docs/methodology.md`: explanation of datasets, missingness, models, and metrics.

## Scope And Limitations

This project uses public benchmark datasets and controlled missingness simulations. It does not make patient-specific claims, provide treatment guidance, or represent a deployed clinical system.

The current version is best understood as a reproducible robustness benchmark plus an interpretability layer: a way to study and communicate how model reliability changes when clinical information is incomplete.
