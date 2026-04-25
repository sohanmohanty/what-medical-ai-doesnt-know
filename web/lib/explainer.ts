import {
  ComparisonSliceModel,
  DatasetMeta,
  ExplorerScenario,
  MechanismMeta,
  MetricCard,
  ModelMeta,
  TrustBand,
} from "@/lib/types";

export function formatRate(rate: number): string {
  return `${Math.round(rate * 100)}%`;
}

export function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

export function formatDecimal(value: number): string {
  return value.toFixed(3);
}

export function formatSignedDelta(value: number, digits = 3): string {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(digits)}`;
}

export function trustCopy(band: TrustBand) {
  if (band === "stable") {
    return {
      label: "Relatively stable",
      summary:
        "This setting still behaves comparatively well, but it should be framed as robustness under stress, not certainty.",
    };
  }

  if (band === "caution") {
    return {
      label: "Use caution",
      summary:
        "The model still produces usable structure here, but the trust signal is meaningfully weaker than the headline score alone suggests.",
    };
  }

  return {
    label: "Fragile under missingness",
    summary:
      "In this setting, uncertainty should be shown plainly instead of letting the output sound cleanly confident.",
  };
}

export function severityTone(label: ExplorerScenario["severity"]["label"]) {
  if (label === "mild") {
    return {
      badge: "Mild information loss",
      summary: "The model is missing some information, but not enough to ignore subtle trust shifts.",
    };
  }

  if (label === "moderate") {
    return {
      badge: "Moderate information loss",
      summary: "A meaningful share of the input is missing, so drift should be taken seriously.",
    };
  }

  if (label === "heavy") {
    return {
      badge: "Heavy information loss",
      summary: "The model is operating with a substantial gap in what it would normally use.",
    };
  }

  return {
    badge: "Severe information loss",
    summary: "This is close to a half-blind prediction setting, which makes overconfidence especially risky.",
  };
}

export function metricStatusCopy(metric: MetricCard, metricName: "roc_auc" | "brier" | "ece" | "accuracy") {
  if (metric.status === "holding") {
    if (metricName === "roc_auc") {
      return "Ranking is holding fairly close to the clean baseline.";
    }
    if (metricName === "accuracy") {
      return "Label-level performance is staying fairly steady.";
    }
    if (metricName === "brier") {
      return "Probability quality is not drifting much from the clean reference.";
    }
    return "Calibration is staying comparatively controlled.";
  }

  if (metric.status === "drifting") {
    if (metricName === "roc_auc") {
      return "Ranking is starting to slip, even if the model still looks functional.";
    }
    if (metricName === "accuracy") {
      return "The label-level result is softening enough to notice.";
    }
    if (metricName === "brier") {
      return "Probability quality is moving in the wrong direction.";
    }
    return "Calibration drift is visible and deserves caution.";
  }

  if (metricName === "roc_auc") {
    return "Ranking performance drops hard enough that this is more than a subtle trust issue.";
  }
  if (metricName === "accuracy") {
    return "The label-level degradation is now part of the main story.";
  }
  if (metricName === "brier") {
    return "Probability quality is deteriorating sharply.";
  }
  return "Calibration drift is large enough that confidence can become misleading.";
}

function comparisonNarrative(selected: ExplorerScenario, peers: ComparisonSliceModel[], modelLabelLookup: Record<string, string>) {
  const ordered = [...peers].sort((left, right) => left.rank - right.rank);
  const position = ordered.findIndex((entry) => entry.model === selected.model) + 1;
  const best = ordered[0];

  if (!position) {
    return "This scenario can still be interpreted on its own, but the same-slice model comparison is unavailable.";
  }

  if (position === 1) {
    return `Among the three benchmarked models under this exact missingness setting, ${modelLabelLookup[selected.model]} currently looks the most trustworthy overall.`;
  }

  if (position === ordered.length) {
    return `${modelLabelLookup[best.model]} looks steadier than ${modelLabelLookup[selected.model]} under the same dataset, mechanism, and severity level.`;
  }

  return `${modelLabelLookup[selected.model]} sits in the middle of the three-model comparison here, while ${modelLabelLookup[best.model]} currently looks strongest overall.`;
}

function rankingNarrative(delta: number) {
  if (delta <= -0.05) {
    return "Ranking performance drops sharply, so the missing information is undermining more than just calibration polish.";
  }

  if (delta <= -0.02) {
    return "Ranking performance slips noticeably, which means discrimination is being affected alongside trust.";
  }

  if (delta < 0) {
    return "Ranking only softens slightly, so the bigger issue may be how trustworthy the probabilities still are.";
  }

  return "Ranking stays close to the clean baseline, which is exactly why calibration deserves its own attention.";
}

function probabilityNarrative(eceDelta: number, brierDelta: number) {
  if (eceDelta > 0.03 || brierDelta > 0.03) {
    return "The probability estimate deserves strong caution because calibration-sensitive metrics deteriorate much faster than a casual visitor might expect.";
  }

  if (eceDelta > 0.012 || brierDelta > 0.012) {
    return "The probability estimate deserves caution because calibration and probability quality are clearly drifting.";
  }

  if (eceDelta > 0 || brierDelta > 0) {
    return "Probability quality only drifts modestly, but even small calibration losses matter in high-stakes settings.";
  }

  return "Probability quality does not worsen much here, which helps explain why this setting feels comparatively stable.";
}

export function buildScenarioExplanation(
  scenario: ExplorerScenario,
  dataset: DatasetMeta,
  model: ModelMeta,
  mechanism: MechanismMeta,
  peers: ComparisonSliceModel[],
  modelLabelLookup: Record<string, string>,
) {
  const trust = trustCopy(scenario.trustBand);
  const severity = severityTone(scenario.severity.label);

  return {
    headline: trust.label,
    overview: `${mechanism.longLabel} at ${formatRate(scenario.rate)} missingness removes a meaningful share of the information available to ${model.label} on ${dataset.label}.`,
    severityRead: `${severity.badge}: about ${formatPercent(scenario.severity.actualRate)} of the test-time information is missing in this scenario. ${scenario.severity.summary}`,
    whyItMoves: `${mechanism.audienceSummary} ${dataset.audienceSummary}`,
    stabilityRead: rankingNarrative(scenario.meanRocAucChange),
    probabilityRead: probabilityNarrative(scenario.meanEceChange, scenario.meanBrierChange),
    comparisonRead: comparisonNarrative(scenario, peers, modelLabelLookup),
    closing: trust.summary,
  };
}
