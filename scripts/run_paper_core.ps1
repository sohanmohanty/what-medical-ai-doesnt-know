$python = if (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

& $python -m src.experiments.run_configured_experiment `
  --config-dir configs\paper_core `
  --progress-every 12 `
  @args
