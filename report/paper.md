# Robustness and Calibration of Clinical Machine Learning Models Under Missing Data

## Abstract

Clinical prediction models are often evaluated on complete records, but real deployment settings may require predictions when some inputs are unavailable. This study evaluates the robustness of clinical machine learning models under controlled missing-data conditions. Using the Wisconsin Diagnostic Breast Cancer and Statlog Heart datasets, a canonical benchmark compared logistic regression, random forest, and gradient boosting under three missingness mechanisms: Missing Completely At Random (MCAR), Missing At Random (MAR), and Missing Not At Random (MNAR). Missingness rates of 10%, 20%, 30%, and 50% were examined with repeated stratified cross-validation and inner hyperparameter tuning. In addition to discrimination, the analysis evaluated probability reliability through Brier score, expected calibration error (ECE), and reliability diagrams. Results show that robustness depends strongly on dataset difficulty, model choice, missingness mechanism, and evaluation metric. WDBC remained stronger in absolute performance than Statlog Heart, MCAR was the most disruptive mechanism in the present constructions, and random forest was the most consistently robust core model for discrimination. However, robustness was metric-dependent: logistic regression often retained cleaner Brier/ECE behavior on WDBC, while gradient boosting became more brittle under severe MCAR. Focused follow-up analyses examined imputation strategy, training regime, and missingness indicators. Across both datasets, calibration could degrade even when ROC-AUC remained comparatively strong, highlighting the importance of evaluating probability reliability as well as classification performance. The repository also exports the benchmark outputs to a static JSON artifact for a companion interactive explorer; the experimental claims in this paper remain grounded in the saved benchmark results.

## 1. Introduction

Missing data are common in clinical machine learning. Laboratory values may be unavailable, tests may be skipped, and some features may be missing at prediction time. Because of this, model evaluation should consider not only performance on complete data, but also robustness when inputs are partially missing.

This study examines robustness under controlled missingness by comparing standard supervised models across multiple datasets and missingness mechanisms. The work focuses on four main questions:

1. How much does missingness degrade predictive performance?
2. Does robustness differ across model classes?
3. Do different missingness mechanisms produce different degradation patterns?
4. Does probability reliability degrade differently from discrimination?

By answering these questions in a structured experimental setting, the analysis aims to show how model failure depends not only on algorithm choice, but also on the interaction between the data, the imputation strategy, and the form of missingness.

## 2. Experimental Setup

### 2.1 Datasets

The experiments used two benchmark datasets:

- **Wisconsin Diagnostic Breast Cancer (WDBC):** 569 examples, 30 numeric features, and a binary tumor label.
- **Statlog Heart:** 270 examples, 13 clinical features, and a binary heart-disease label.

These datasets provide a useful contrast. WDBC is relatively clean and highly separable, while Statlog Heart is smaller, noisier, and more fragile. The goal is not to make disease-specific clinical claims from either benchmark dataset, but to study how prediction models behave under controlled missingness.

### 2.2 Models

The models evaluated were:

- Logistic regression
- Random forest
- Gradient boosting

Gradient boosting was fully expanded on WDBC and later mirrored on Statlog to improve model symmetry across the two datasets.

### 2.3 Missingness mechanisms

Three missingness mechanisms were implemented:

- **MCAR**: Missing Completely At Random
- **MAR**: Missing At Random
- **MNAR**: Missing Not At Random

Experiments were conducted at missingness rates of:

- 10%
- 20%
- 30%
- 50%

### 2.4 Imputation and feature handling

The analysis compared several ways of handling missing data:

- simple imputation
- KNN imputation
- iterative imputation
- simple imputation with explicit missingness indicators in selected experiments

The canonical cross-dataset `paper_core` benchmark used simple imputation so that the main model, dataset, and mechanism comparisons were made under a shared preprocessing baseline. KNN imputation, iterative imputation, and simple imputation with explicit missingness indicators were then examined in focused follow-up comparisons.

### 2.5 Evaluation metrics

Performance was evaluated using:

- Accuracy
- ROC-AUC
- Brier score
- Expected Calibration Error (ECE)

Reliability diagrams were also generated for selected conditions to visualize probability calibration directly.

### 2.6 Evaluation protocol

The canonical core benchmark used repeated stratified 5-fold cross-validation with 2 repeats and 3-fold inner hyperparameter tuning, optimizing ROC-AUC. This produced 10 outer evaluation runs for each dataset-model-mechanism-rate condition. All core benchmark comparisons used the `clean_train_corrupt_test` regime, while alternative training regimes were examined in focused follow-up experiments.

## 3. Results

### 3.1 Clean-data baselines

We first established clean-data baselines on WDBC and Statlog Heart before introducing missingness. On WDBC, all three models started from strong baselines, with logistic regression achieving the best clean discrimination and probability quality in the canonical core run. On Statlog Heart, clean performance was lower overall; logistic regression and random forest were close in ROC-AUC, while gradient boosting trailed them more clearly. These baselines reinforce that Statlog is a harder dataset even before missingness is introduced.

These baselines serve as the reference point for later degradation analyses and already suggest that WDBC is more forgiving than Statlog Heart.

### 3.2 Missingness mechanism validation

We implemented MCAR, MAR, and MNAR masking procedures and verified that achieved missingness rates tracked the requested rates of 10%, 20%, 30%, and 50% closely. This indicates that the masking procedures behaved as intended and that the downstream robustness results reflect controlled missingness rather than accidental corruption.

### 3.3 WDBC: logistic regression under MCAR, MAR, and MNAR

On WDBC, logistic regression under simple imputation showed measurable degradation under missingness, especially in Brier score and ECE. Among the three mechanisms, MCAR was clearly the harshest. As MCAR increased, Brier score and ECE worsened more clearly than ROC-AUC, suggesting that probability quality was more sensitive than ranking performance. MAR and MNAR were milder across most rates, although both still produced visible degradation at higher missingness rates.

Overall, logistic regression remained fairly strong on WDBC under moderate missingness, but its predicted probabilities became less reliable as missingness increased.

### 3.4 WDBC: model comparison across mechanisms

We then compared logistic regression, random forest, and gradient boosting on WDBC under MCAR, MAR, and MNAR.

The canonical core benchmark produced a metric-dependent model story. Random forest was the most consistently robust model for accuracy and ROC-AUC on WDBC. Logistic regression often retained the strongest Brier and ECE behavior, especially away from the harshest MCAR settings. Gradient boosting remained competitive at low corruption levels but became the most brittle model under 50% MCAR, where its drops were the largest across all four metrics.

These results suggest that, on WDBC, robustness is metric-dependent. Random forest best preserved discrimination, while logistic regression often preserved probability quality more cleanly.

### 3.5 Statlog Heart: logistic regression under MCAR, MAR, and MNAR

Statlog Heart showed a different pattern from WDBC. Under logistic regression with simple imputation, missingness had a larger effect overall, especially under MCAR.

In the canonical core run, MCAR was clearly the harshest mechanism on Statlog. Accuracy, ROC-AUC, and Brier score all degraded more noticeably than on WDBC. MAR stayed close to clean performance, and MNAR was often near baseline in the present construction. Compared with WDBC, the magnitude of the MCAR-driven loss in accuracy and ROC-AUC was substantially larger.

This indicates that Statlog is a more fragile dataset under missingness.

### 3.6 Statlog Heart: model comparison across mechanisms

We compared logistic regression, random forest, and gradient boosting on Statlog under MCAR, MAR, and MNAR.

The core benchmark again showed that model choice matters, but not all tree-based models behaved equally. Random forest was the most stable model overall on Statlog Heart, especially in accuracy and Brier score. Logistic regression remained competitive and sometimes edged out random forest in ROC-AUC under the milder MAR and MNAR settings. Gradient boosting was not uniformly robust in the canonical core run; instead, it tended to be the most brittle model under severe MCAR and produced the largest worst-case drops.

This shows that the dataset effect and model effect both matter. Harder datasets expose robustness weaknesses more clearly, even when the same mechanism construction is used, and the strongest model can depend on which metric is prioritized.

### 3.7 Cross-dataset comparison

Comparing the two datasets, WDBC remained much stronger in absolute performance and showed smaller losses in accuracy and ROC-AUC across the canonical core benchmark. The contrast was especially clear under MCAR, where Statlog showed much stronger discrimination loss and worse Brier deterioration.

The core benchmark also showed, however, that WDBC did not dominate every calibration-sensitive change. ECE drift under MCAR remained substantial on WDBC, especially for the tree-based models. The comparison therefore suggests that dataset characteristics matter greatly when evaluating robustness to missing data: WDBC is the easier and more resilient benchmark overall, but strong discrimination on WDBC does not guarantee calibration stability.

### 3.8 Imputer comparison

We compared simple imputation, KNN imputation, and iterative imputation for logistic regression on WDBC under MCAR, MAR, and MNAR. Iterative imputation performed best overall across these focused comparisons, while KNN imputation was less stable in some higher-missingness settings, especially under MCAR. Simple imputation remained competitive at lower corruption levels but degraded more steadily as missingness increased.

These results suggest that imputation strategy is not a trivial implementation detail. More flexible imputers can improve robustness, especially when missingness becomes stronger or more structured.

### 3.9 Calibration under missingness

In addition to discrimination metrics, we evaluated probability reliability using Brier score, expected calibration error (ECE), and reliability diagrams. This analysis focused on logistic regression with iterative imputation on both WDBC and Statlog Heart under MCAR, MAR, and MNAR.

On WDBC, calibration was relatively stable under missingness. Although ECE and Brier score worsened as missingness increased, the overall degradation was moderate, and the reliability diagrams suggested that predicted probabilities remained reasonably aligned with observed frequencies in many settings.

Statlog Heart showed a less stable calibration pattern. Under MCAR, ECE and Brier score deteriorated more clearly, especially at higher missingness rates. MAR and MNAR were milder than MCAR in the present constructions, but calibration drift was still more visible and more variable than on WDBC.

An important pattern across both datasets is that calibration can worsen even when ROC-AUC remains comparatively strong. In other words, the model may continue to rank cases reasonably well while producing probabilities that are less trustworthy. This is especially important in clinical machine learning, where predicted probabilities may be used directly for risk estimation, triage, or threshold-based decision support.

### 3.10 Training-regime comparison

We also examined whether matching the training environment to the deployment environment improves robustness. In focused comparisons under MCAR using logistic regression with iterative imputation, we compared two regimes:

- **clean_train_corrupt_test**
- **corrupt_train_corrupt_test**

This comparison is important because it separates deployment-time fragility from adaptation to corruption. If performance improves when training data are corrupted in the same way as test data, that suggests the model can partially adapt to the missingness pattern. If not, then exposure to corrupted training data may not compensate for the information loss caused by missing inputs.

Across the focused regime comparisons, the results showed that robustness is not only a test-time issue. It also depends on whether the model is trained in an environment that resembles deployment. This makes the experimental setup more realistic by moving beyond the question of whether missingness hurts performance and toward the question of whether corruption-aware training helps in practice.

### 3.11 Missingness indicators

Finally, we tested whether explicitly telling the model which values were missing could improve robustness. In focused comparisons on WDBC, we compared simple imputation alone against simple imputation plus missingness indicators.

This comparison addresses a subtle but important question: is the absence pattern itself informative? If so, then a model may benefit not only from filled-in values, but also from knowing which entries were originally missing.

These experiments strengthen the methodology because they connect the imputation problem to the broader idea that missingness can itself carry signal, especially in structured clinical settings.

### 3.12 Summary of findings

Taken together, the experiments support five main conclusions:

1. **Dataset difficulty matters:** Statlog Heart is more sensitive to missingness than WDBC.
2. **Model choice matters, but robustness is metric-dependent:** random forest was the most consistently robust core model for discrimination, logistic regression often retained the cleanest Brier/ECE behavior on WDBC, and gradient boosting was the most brittle model under severe MCAR.
3. **Imputation strategy matters:** iterative imputation was often the strongest of the focused imputer comparisons.
4. **Mechanism design matters:** in the present constructions, MCAR is typically the most disruptive mechanism, while MAR and MNAR are milder.
5. **Calibration matters:** degradation in probability reliability can appear even when ROC-AUC remains comparatively strong.

## 4. Discussion

This study shows that robustness to missing data is shaped by the interaction between the dataset, the model, the imputation strategy, and the missingness mechanism.

A first important result is that dataset characteristics matter substantially. WDBC remained the easier benchmark overall, with much stronger absolute accuracy and ROC-AUC than Statlog Heart even after corruption. In contrast, Statlog Heart showed larger drops in performance, particularly under MCAR. At the same time, the core benchmark showed that WDBC was not uniformly better on every calibration-sensitive change: ECE drift under MCAR could still be substantial, especially for the tree-based models. This suggests that datasets with stronger redundancy or more separable structure can better tolerate missing information in discrimination terms, but still show nontrivial probability drift.

A second major result is that model choice matters, but the benchmark supports a more metric-dependent story than a simple ranking. Random forest was the most consistently robust core model, especially for accuracy and ROC-AUC. Logistic regression often retained cleaner Brier and ECE behavior on WDBC. Gradient boosting remained strong in some easier settings, but it became the most brittle model under severe MCAR and produced the largest worst-case drops in the canonical core benchmark. The practical lesson is that the "best" model depends partly on whether the priority is discrimination or trustworthy probabilities.

A third result is that the apparent severity of a missingness mechanism depends strongly on how it is constructed. In this study, MCAR was clearly the harshest mechanism in the canonical core benchmark, especially on Statlog Heart. By contrast, MAR and MNAR were often much milder and sometimes stayed close to clean performance. This should not be interpreted as a universal claim that MCAR is always more harmful than MAR or MNAR. Rather, it reflects the specific masking procedures used here.

A fourth result is that calibration deserves its own attention. In many settings, ROC-AUC remained relatively stable while Brier score and ECE worsened. This means that a model may continue to rank cases reasonably well while producing probabilities that are less trustworthy. For clinical machine learning, this distinction matters because downstream decisions often depend on predicted probabilities, not just ranking performance.

A fifth result is that robustness is not just about the model itself. The imputer comparison showed that missing-value handling can materially affect performance, especially under stronger corruption. The regime comparison showed that training conditions can matter as well: robustness depends partly on whether the model is exposed during training to the type of corruption it encounters at test time. The missingness-indicator experiments further suggested that the absence pattern itself may carry useful information in some settings.

These findings have practical implications. Robustness to missingness should not be assumed to transfer across datasets. A model that appears stable on an easy benchmark may degrade more substantially on a harder clinical dataset. Similarly, evaluating only one missingness mechanism or one imputation strategy can give a misleadingly narrow picture of robustness.

This study also has limitations. The experiments were conducted on only two datasets, and the missingness generators were controlled constructions rather than mechanisms learned from real clinical observation patterns. The canonical cross-dataset model-mechanism grid used simple imputation to keep the core benchmark controlled, so alternative imputers were examined in focused rather than fully crossed settings. Some later extensions, such as regime comparison and missingness indicators, were also explored in focused rather than fully exhaustive settings. The study therefore provides a strong controlled comparative analysis, but not a complete account of all real-world clinical missingness behavior.

There are several natural directions for future work. One is to extend the two-regime and missingness-indicator comparisons more broadly across datasets and model classes. Another is to add an appendix dataset with native or semi-native missingness behavior. A third is to compare post-hoc calibration strategies after training under missingness. Finally, the framework could be extended to more realistic observational missingness processes or larger clinical databases.

Overall, these results show that robustness to missing clinical data is not determined by a single factor. Within the present setup, WDBC is comparatively forgiving in discrimination terms, Statlog Heart is more fragile, random forest is the most consistently robust core model for discrimination, and probability reliability can degrade before ranking performance fully collapses. These findings provide a strong base for a fuller study of missing-data robustness in clinical machine learning.

## 5. Conclusion

This study investigated how clinical machine learning models respond to missing data under controlled missingness mechanisms. Using the WDBC and Statlog Heart datasets, we evaluated logistic regression, random forest, and gradient boosting under MCAR, MAR, and MNAR settings across multiple missingness rates.

The results show that robustness depends on several interacting factors: the dataset, the model, the missingness mechanism, and the imputation strategy. WDBC remained stronger than Statlog Heart overall, especially in absolute accuracy and ROC-AUC, suggesting that dataset structure and redundancy strongly influence tolerance to missingness. Within the canonical core benchmark, random forest was the most consistently robust model for discrimination, while logistic regression often retained stronger Brier/ECE behavior on WDBC and gradient boosting was more brittle under severe MCAR. Iterative imputation still often outperformed simpler alternatives in the focused imputer comparisons.

An important practical finding is that degradation was often more visible in Brier score and ECE than in ROC-AUC. This suggests that missingness can weaken probability quality and calibration even when ranking performance remains relatively stable. For clinical prediction tasks, where probability estimates may guide decisions, this makes calibration-sensitive evaluation especially important.

The additional calibration, training-regime, and missingness-indicator analyses further show that robustness depends not only on predictive performance, but also on whether the model can maintain trustworthy probabilities and adapt to the corruption process it faces.

Overall, this work provides a structured experimental framework for studying robustness to missing data in clinical machine learning. The current results suggest that model robustness should not be assumed, that dataset difficulty matters substantially, and that probability reliability deserves explicit evaluation alongside standard discrimination metrics.

Future work should expand the analysis to additional datasets, stronger and more realistic MAR and MNAR mechanisms, and broader extensions of the regime and indicator comparisons. Even in its current form, however, this study demonstrates that controlled missingness experiments can reveal important differences in how models fail, and that these differences are highly relevant for reliable clinical ML deployment.

## 6. Reproducibility and Companion Explorer

The repository is organized so that the main benchmark can be rerun and inspected from saved artifacts. The canonical paper-facing path is `scripts/run_paper_core.ps1`, which writes summary metrics, fold-level metrics, predictions, masks, run manifests, and figures under `results/` and `figures/`.

A companion web explorer presents the same benchmark results through a static frontend artifact, `artifacts/frontend/paper_core_explorer.json`, generated by `scripts/export_frontend_artifacts.py`. This interface is intended for interpretation and communication. It does not collect user medical data, train models in the browser, or provide diagnosis. The scientific claims in this paper are based on the stored benchmark outputs rather than on user interaction with the web app.

## 7. Supplementary Figures

### Main Figures
- `figures/paper/clean_baseline_brier.png`
- `figures/paper/clean_baseline_auc.png`
- `figures/paper/wdbc_logreg_mechanism_compare_brier.png`
- `figures/paper/wdbc_logreg_mechanism_compare_auc.png`
- `figures/paper/statlog_logreg_mechanism_compare_brier.png`
- `figures/paper/statlog_logreg_mechanism_compare_auc.png`
- `figures/paper/logreg_mcar_wdbc_vs_statlog_brier.png`
- `figures/paper/logreg_mcar_wdbc_vs_statlog_auc.png`
- `figures/paper/wdbc_mcar_model_compare_brier.png`
- `figures/paper/wdbc_mcar_model_compare_auc.png`
- `figures/paper/statlog_mcar_model_compare_brier.png`
- `figures/paper/statlog_mcar_model_compare_auc.png`
- `figures/paper/wdbc_logreg_iterative_ece_compare.png`
- `figures/paper/statlog_logreg_iterative_ece_compare.png`
- `figures/paper/logreg_iterative_wdbc_vs_statlog_ece.png`

### Supporting Figures
- `figures/paper/wdbc_reliability_clean.png`
- `figures/paper/wdbc_reliability_mcar_0.3.png`
- `figures/paper/wdbc_reliability_mar_0.3.png`
- `figures/paper/wdbc_reliability_mnar_0.3.png`
- `figures/paper/statlog_reliability_clean.png`
- `figures/paper/statlog_reliability_mcar_0.3.png`
- `figures/paper/statlog_reliability_mar_0.3.png`
- `figures/paper/statlog_reliability_mnar_0.3.png`
- `figures/paper/wdbc_logreg_mcar_imputer_compare_brier.png`
- `figures/paper/wdbc_logreg_mcar_imputer_compare_auc.png`
- `figures/paper/wdbc_logreg_mar_imputer_compare_brier.png`
- `figures/paper/wdbc_logreg_mar_imputer_compare_auc.png`
- `figures/paper/wdbc_logreg_mnar_imputer_compare_brier.png`
- `figures/paper/wdbc_logreg_mnar_imputer_compare_auc.png`
- `figures/paper/wdbc_logreg_iterative_mcar_regime_compare_brier.png`
- `figures/paper/wdbc_logreg_iterative_mcar_regime_compare_ece.png`
- `figures/paper/statlog_logreg_iterative_mcar_regime_compare_brier.png`
- `figures/paper/statlog_logreg_iterative_mcar_regime_compare_ece.png`
- `figures/paper/logreg_iterative_mcar_regime_cross_dataset_ece.png`
- `figures/paper/wdbc_logreg_mcar_indicator_compare_brier.png`
- `figures/paper/wdbc_logreg_mcar_indicator_compare_ece.png`
- `figures/paper/wdbc_logreg_mar_indicator_compare_brier.png`
- `figures/paper/wdbc_logreg_mar_indicator_compare_ece.png`
- `figures/paper/wdbc_logreg_mnar_indicator_compare_brier.png`
- `figures/paper/wdbc_logreg_mnar_indicator_compare_ece.png`
- `figures/paper/wdbc_logreg_indicator_compare_combined_ece.png`
- `figures/paper/statlog_gb_mechanism_compare_brier.png`
- `figures/paper/statlog_gb_mechanism_compare_roc_auc.png`

## 8. Supplementary Tables

### Main Tables
- `results/metrics/paper_core_summary.csv`
- `results/metrics/clean_baseline_combined.csv`
- `results/metrics/combined_logreg_iterative_calibration_summary.csv`

### Supporting Tables
- `results/metrics/paper_core_metrics.csv`
- `results/metrics/wdbc_logreg_mcar_imputer_compare_summary.csv`
- `results/metrics/wdbc_logreg_mar_imputer_compare_summary.csv`
- `results/metrics/wdbc_logreg_mnar_imputer_compare_summary.csv`
- `results/metrics/wdbc_logreg_iterative_mcar_regime_compare_summary.csv`
- `results/metrics/statlog_logreg_iterative_mcar_regime_compare_summary.csv`
- `results/metrics/combined_logreg_iterative_mcar_regime_compare_summary.csv`
- `results/metrics/wdbc_logreg_mcar_indicator_compare_summary.csv`
- `results/metrics/wdbc_logreg_mar_indicator_compare_summary.csv`
- `results/metrics/wdbc_logreg_mnar_indicator_compare_summary.csv`
- `results/metrics/wdbc_logreg_indicator_compare_combined_summary.csv`
- `results/metrics/statlog_gb_combined_mechanism_summary.csv`

## 9. Additional Appendix Materials

### Fold-level metric files
Keep these as appendix material or supplementary artifacts rather than main-text tables.

- `results/metrics/paper_core_metrics.csv`

### Master summary table
- `results/metrics/master_core_summary_table.csv`

This is useful as a full study record, but it is too large and heterogeneous to serve as a clean main-report table.

## 10. References

- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1-3.
- Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of the 34th International Conference on Machine Learning*, 70, 1321-1330. https://proceedings.mlr.press/v70/guo17a.html
- Little, R. J. A., and Rubin, D. B. (2019). *Statistical Analysis with Missing Data* (3rd ed.). Wiley.
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830. https://www.jmlr.org/papers/v12/pedregosa11a.html
- UCI Machine Learning Repository. Breast Cancer Wisconsin (Diagnostic). https://doi.org/10.24432/C5DW2B
- UCI Machine Learning Repository. Statlog (Heart). https://doi.org/10.24432/C57303
