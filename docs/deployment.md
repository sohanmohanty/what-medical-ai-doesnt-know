# Deployment

The web interface is designed to be deployed as a static Next.js site. The current deployment is available at:

```text
https://what-medical-ai-doesnt-know.vercel.app/
```

The deployed website is an interpretation layer over saved benchmark outputs. The research paper, metrics, predictions, masks, figures, and manifests remain the technical evidence for the project.

The deployed paper is available at:

```text
https://what-medical-ai-doesnt-know.vercel.app/paper.pdf
```

## Deployment Configuration

The Vercel project uses:

- Framework preset: Next.js
- Root directory: `web`
- Install command: `npm install`
- Build command: `npm run build`
- Output directory: Next.js default

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

## Research Artifact Links

The main project links are:

- the deployed website URL: `https://what-medical-ai-doesnt-know.vercel.app/`
- the repository URL: `https://github.com/sohanmohanty/what-medical-ai-doesnt-know`
- the deployed paper URL: `https://what-medical-ai-doesnt-know.vercel.app/paper.pdf`
- the repository paper path: `report/paper.pdf`

The website provides an interactive view of the saved benchmark results. The paper describes the statistical analysis, experimental design, calibration results, limitations, and reproducibility details.

## Redeploy Checklist

Before redeploying:

```powershell
python scripts\export_frontend_artifacts.py
cd web
npm run build
```

After deployment, check:

- the homepage explains the project quickly
- the Explorer loads without local files
- the Methodology page is readable
- the About page preserves the research framing
- the disclaimer is visible but not dominant

## Scope

The deployed site is educational and research-oriented. It is not a diagnostic tool, does not collect patient data, and does not provide treatment guidance.
