# Frontend Artifacts

This directory stores precomputed JSON files intended for the web app.

The primary explorer artifact is:

- `paper_core_explorer.json`

It is generated from:

- `results/metrics/paper_core_summary.csv`
- `results/predictions/paper_core_predictions.csv`
- `results/predictions/baseline_predictions.csv` when available

Refresh it with:

```powershell
python scripts\export_frontend_artifacts.py
```

These artifacts are intentionally static so the app can be deployed without a custom backend.
