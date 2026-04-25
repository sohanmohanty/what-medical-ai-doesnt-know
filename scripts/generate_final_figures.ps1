$python = if (Test-Path ".venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

& $python -m src.visualization.plot_clean_baseline
& $python -m src.visualization.plot_clean_baseline_auc
& $python -m src.visualization.plot_wdbc_logreg_mechanism_compare_brier
& $python -m src.visualization.plot_wdbc_logreg_mechanism_compare_auc
& $python -m src.visualization.plot_statlog_logreg_mechanism_compare_brier
& $python -m src.visualization.plot_statlog_logreg_mechanism_compare_auc
& $python -m src.visualization.plot_logreg_mcar_wdbc_vs_statlog_brier
& $python -m src.visualization.plot_logreg_mcar_wdbc_vs_statlog_auc
& $python -m src.visualization.plot_wdbc_mcar_model_compare_brier
& $python -m src.visualization.plot_wdbc_mcar_model_compare_auc
& $python -m src.visualization.plot_statlog_mcar_model_compare_brier
& $python -m src.visualization.plot_statlog_mcar_model_compare_auc
& $python -m src.visualization.plot_wdbc_logreg_iterative_ece_compare
& $python -m src.visualization.plot_statlog_logreg_iterative_ece_compare
& $python -m src.visualization.plot_logreg_iterative_wdbc_vs_statlog_ece
& $python -m src.visualization.plot_wdbc_logreg_mar_imputer_compare_brier
& $python -m src.visualization.plot_wdbc_logreg_mar_imputer_compare_auc
& $python scripts\organize_paper_figures.py
