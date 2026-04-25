# Communication Guide

This document explains how the project describes benchmark results. It is meant to keep the website, README, and methodology pages consistent.

## Voice

The writing should be clear, restrained, and technically honest. It should help nontechnical readers understand the main idea without weakening the research framing.

Use language that is:

- precise
- calm
- evidence-based
- understandable without advanced ML background

Avoid language that is:

- alarmist
- theatrical
- startup-like
- overly casual
- falsely clinical

## Main Distinction

The project repeatedly separates two ideas:

- **Confidence:** the probability a model reports
- **Trust:** whether that probability still holds up after checking calibration, robustness, and missingness

This distinction should stay central across the site.

## General View

The general view should answer:

- What changed?
- Why might missing information matter here?
- Is the model still relatively stable?
- Should the probability be treated with caution?

The explanation should use plain English, but it should not oversimplify the result into "good" or "bad."

## Technical View

The technical view should make the benchmark legible to readers who care about the metrics.

It should emphasize:

- ROC-AUC for ranking behavior
- accuracy for label-level behavior
- Brier score for probability quality
- ECE for calibration error
- reliability curves for probability alignment
- model comparisons under the same dataset, mechanism, and rate

## Guardrails

- Never imply medical advice.
- Never imply the app can evaluate a visitor's personal health.
- Never ask users to upload medical records.
- Never present benchmark outputs as clinical recommendations.
- Avoid saying a model is "good" in general. Prefer "more stable under this setting" or "less trustworthy under this missingness pattern."

## Short Project Description

I built an interactive benchmark explorer that shows how clinical prediction models change when patient data are incomplete, with emphasis on calibration, uncertainty, and when a model should communicate caution.
