# Content Strategy

## Voice

The site should sound:

- thoughtful
- precise
- calm
- trustworthy
- intellectually curious

It should not sound:

- alarmist
- melodramatic
- overconfident
- startup-salesy
- faux-clinical

## Audience Split

The product should intentionally support two reading modes.

### General Mode

Purpose:

- explain the concept in plain English
- help a visitor understand why missing data change trust
- highlight caution without jargon overload

Primary questions this mode answers:

- What changed?
- Why did the prediction become less trustworthy?
- Does the model still seem stable?
- Should the probability be treated cautiously?

### Technical Mode

Purpose:

- show real rigor
- expose calibration-sensitive metrics
- make the benchmark legible to technical readers

Primary questions this mode answers:

- How much did ROC-AUC move?
- How much did Brier score and ECE drift?
- Which model is more stable under which mechanism?
- Which results are benchmark-specific versus broadly suggestive?

## Page Messaging

## Landing Page

Primary job:

- communicate the central question immediately

Best framing:

- "What happens when a model has to make a medical prediction without all the information it needs?"
- "Not every confident prediction deserves trust."

## Explorer

Primary job:

- show how missingness changes both performance and trust indicators

Copy principle:

- every selection state should produce a short deterministic explanation

## Methodology

Primary job:

- reassure technical readers that the project is grounded in real benchmark design

Copy principle:

- use plain language first, then exact terms

## About

Primary job:

- connect motivation to uncertainty and trustworthy systems

Copy principle:

- personal, restrained, and reflective

## Explanation Template Rules

- Start with what changed.
- Follow with why the model likely shifted.
- Distinguish ranking stability from probability trust.
- End with a human-readable caution level.

## Copy Guardrails

- Never imply medical advice.
- Never imply the app can evaluate a user's personal health.
- Never anthropomorphize the model as if it "understands" the patient.
- Prefer "the model appears more fragile under this setting" over dramatic claims.

## Portfolio Positioning

Short description:

> I built an interactive platform that shows how clinical prediction models change when patient data are incomplete, focusing on calibration, uncertainty, and when a model should admit it does not know enough.

Longer positioning:

This project combines a reproducible clinical ML robustness benchmark with a public-facing interface that explains how missing data affect both performance and trustworthiness in high-stakes prediction systems.
