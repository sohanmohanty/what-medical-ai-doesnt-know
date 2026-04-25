$python = if (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }
& $python -m src.experiments.run_configured_experiment @args
