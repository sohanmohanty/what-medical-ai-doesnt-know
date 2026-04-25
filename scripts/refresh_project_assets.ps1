$python = if (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

& $python -m src.experiments.export_metadata_and_manifests

if (Test-Path "results/metrics/core_missingness_grid_summary.csv") {
  Copy-Item -LiteralPath "results/metrics/core_missingness_grid_summary.csv" -Destination "results/metrics.csv" -Force
}

if (Test-Path "results/predictions/core_missingness_grid_predictions.csv") {
  Copy-Item -LiteralPath "results/predictions/core_missingness_grid_predictions.csv" -Destination "results/predictions.csv" -Force
}

& $python scripts/export_paper_pdf.py
