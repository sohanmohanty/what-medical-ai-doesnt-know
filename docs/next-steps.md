# Next Development Steps

## What To Build Next

1. Add feature-level missingness summaries so the example inputs can become honest feature-impact controls.
2. Export clean-baseline reliability views for every dataset-model pair, not only the currently available baseline artifacts.
3. Create a "trust state" legend tied to exact metric thresholds and document those thresholds in the methodology page.
4. Add a scenario comparison view so visitors can compare two models side by side under the same missingness pattern.
5. Capture polished screenshots and deploy the first preview build.

## Immediate Engineering Priorities

- keep `paper_core` as the default frontend seed
- expand the export script instead of adding an API first
- preserve deterministic explanations
- test the app on narrow mobile widths before adding more controls

## Open Questions For The Next Pass

- Which fold-level artifacts should power calibration plots?
- What is the cleanest way to represent feature-dropout interactions using stored benchmark outputs?
- Should the first public deployment ship with one canonical dataset story or both datasets from day one?
