# When Medical AI Doesn't Know

## Project Summary

**Working title:** When Medical AI Doesn't Know  
**Subtitle:** An interactive explorer of missing data, calibration, and trust in clinical prediction.

This project turns an existing clinical machine learning robustness benchmark into a polished, public-facing web experience. The research benchmark remains the analytical engine, but the flagship identity becomes a user-facing product about a harder and more human question:

**What should a medical model communicate when it has to make a prediction without all the information it needs?**

The app is not a diagnosis tool, symptom checker, or AI doctor. It is an educational and analytical product that shows how missing information changes model behavior, why calibration matters, and why confidence should not automatically be treated as trustworthiness.

## Why This Exists

The project is meant to express a clear intellectual identity at the intersection of:

- medicine
- computer science
- statistics
- uncertainty and decision-making

The benchmark already shows rigor. What it does not yet show is product thinking, explanation design, or a memorable public-facing narrative. This project fills that gap by making the benchmark understandable to both nontechnical and technical audiences.

## Core Message

High-stakes systems should be honest about uncertainty.

Missing data do not just reduce performance. They can change how trustworthy a prediction feels, especially when a model still ranks cases reasonably well while its probabilities become less reliable.

## Target Users

- General visitors who can understand a plain-English explanation in under a minute.
- Technical readers who want to inspect metrics, calibration, methodology, and limitations.
- Admissions readers, teachers, mentors, and judges who need to quickly understand both the rigor and the motivation behind the work.

## Product Goals

- Make the project feel like a serious, coherent flagship portfolio piece rather than a paper-only benchmark.
- Preserve the rigor of the original research engine.
- Communicate that trust in medical AI depends on calibration and uncertainty, not just ROC-AUC.
- Create a memorable project that ties together medicine, CS, statistics, and lived experience with uncertainty.

## Experience Principles

- **Plain-English first:** The default experience should explain what changed and why it matters without jargon.
- **Technical depth on demand:** Technical readers should be able to inspect metrics, methodology, and robustness details without cluttering the first impression.
- **Honest, not theatrical:** The project should feel thoughtful and serious, not melodramatic or hackathon-flashy.
- **No fake AI gloss:** Explanations should be deterministic, carefully written, and grounded in actual benchmark outputs.
- **Research-backed visuals:** Every trust or stability indicator should map back to real stored metrics, not decorative intuition.

## MVP Scope

### Included

- A polished landing page with a clear value proposition and disclaimer
- An interactive explorer with scenario, model, missingness mechanism, and missingness-rate controls
- A plain-English explanation panel
- Trust/stability communication that reflects calibration and degradation signals
- A technical mode with ROC-AUC, Brier score, ECE, and stress-test comparisons
- Methodology and About pages
- Precomputed frontend artifacts generated from the canonical benchmark outputs

### Explicitly Excluded

- medical advice
- diagnosis
- symptom checking
- seizure prediction
- personal health recommendations
- real patient data ingestion
- chat interfaces presented as clinicians

## Success Criteria

- A nontechnical visitor understands the point quickly.
- A technical visitor sees real modeling depth.
- The app feels portfolio-ready and visually intentional.
- The project clearly signals a CS + statistics identity with a medicine-facing mission.
- The benchmark is still visible, but no longer the only story.
