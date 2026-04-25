# Mask Artifacts

This folder stores tracked official missingness masks saved by the unified runner.

The main example in the current repo is:

- `paper_core/`

Each saved mask file records which cells were artificially hidden for a particular split and condition. A `True` value means that entry was masked out. A `False` value means it was left untouched.

Tracked official masks use a layout like:

- `<run_name>/<dataset>/<model>/<imputer>/<regime>/<mechanism>/rate_<rate>/seed_<seed>/repeat_<repeat>_fold_<fold>_<split>_mask.csv.gz`

Each file includes a leading `row_index` column so the mask can be matched back to the original dataset rows.

Built-in sample runs and custom user runs do not write here. Their masks, when enabled, are stored inside their own namespaced output folders under:

- `results/samples/<run_name>/masks/`
- `results/user_runs/<run_name>/masks/`
