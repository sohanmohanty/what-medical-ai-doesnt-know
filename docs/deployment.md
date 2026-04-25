# Deployment

The public website should be accessed through a hosted URL. Admissions readers, teachers, and judges should not need to clone the repository or run a local development server.

The deployed website is not the main technical artifact. It is the public interpretation layer. The research paper and saved benchmark outputs remain the technical evidence for the project.

## Recommended Path

Use GitHub for the repository and Vercel for hosting the Next.js app.

1. Create a GitHub account.
2. Create a new repository on GitHub.
3. Push this local repository to GitHub.
4. Create a Vercel account.
5. Import the GitHub repository into Vercel.
6. Set the project root directory to `web`.
7. Keep the default Next.js build command: `npm run build`.
8. Deploy the project.
9. Share the generated `https://...vercel.app` link.

## Why This Works

The benchmark is precomputed. The public app does not need a Python backend, a database, or uploaded medical data. It only needs the exported frontend artifact:

```text
web/data/paper_core_explorer.json
```

That file is refreshed by:

```powershell
python scripts\export_frontend_artifacts.py
```

The canonical research artifact is still stored at:

```text
artifacts/frontend/paper_core_explorer.json
```

The copy under `web/data/` exists so the deployed web app is self-contained.

## What To Share

For a portfolio or application, share:

- the deployed website URL
- the repository URL
- the paper path: `report/paper.pdf`

The website gives a fast entry point. The paper should be used to show the statistical analysis, experimental design, calibration results, and reproducibility of the benchmark.

The deployed website also serves the paper at:

```text
/paper.pdf
```

## Pre-Deployment Checklist

Before deploying:

```powershell
python scripts\export_frontend_artifacts.py
cd web
npm run build
```

After deployment, check:

- the homepage explains the project quickly
- the Explorer loads without local files
- the Methodology page is readable
- the About page stays serious and not melodramatic
- the disclaimer is visible but not dominant

## Scope

The deployed site is educational and research-oriented. It is not a diagnostic tool, does not collect patient data, and does not provide treatment guidance.
