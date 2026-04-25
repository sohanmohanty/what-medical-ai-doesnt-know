$python = if (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

& $python -m src.experiments.run_configured_experiment `
  --run-name graph_preview `
  --output-namespace sample `
  --datasets wdbc statlog_heart `
  --models logistic_regression `
  --imputers simple `
  --mechanisms mcar mar mnar `
  --rates 0.1 0.2 0.3 0.5 `
  --regimes clean_train_corrupt_test `
  --max-outer-splits 2 `
  --max-seeds 1 `
  --no-tuning `
  --no-save-masks `
  --no-save-predictions `
  --progress-every 8 `
  @args
