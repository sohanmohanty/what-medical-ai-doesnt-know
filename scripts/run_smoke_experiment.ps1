$python = if (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

& $python -m src.experiments.run_configured_experiment `
  --run-name smoke_test `
  --output-namespace sample `
  --datasets wdbc `
  --models logistic_regression `
  --imputers simple `
  --mechanisms mcar `
  --rates 0.1 `
  --regimes clean_train_corrupt_test `
  --max-outer-splits 1 `
  --max-seeds 1 `
  @args
