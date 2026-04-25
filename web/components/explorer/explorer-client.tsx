"use client";

import { useMemo, useState } from "react";

import {
  buildScenarioExplanation,
  formatDecimal,
  formatPercent,
  formatRate,
  formatSignedDelta,
  metricStatusCopy,
  severityTone,
} from "@/lib/explainer";
import { ExplorerArtifact } from "@/lib/types";
import { ModelComparisonStrip } from "@/components/explorer/model-comparison-strip";
import { ReliabilityChart } from "@/components/explorer/reliability-chart";
import { TrustMeter } from "@/components/explorer/trust-meter";

type ViewMode = "general" | "technical";

const statusStyles = {
  holding: "bg-accent/15 text-accent",
  drifting: "bg-caution/30 text-ink",
  warning: "bg-danger/15 text-danger",
};

function metricTone(value: number, inverse = false) {
  const worsening = inverse ? value < 0 : value > 0;
  return worsening ? "text-danger" : "text-accent";
}

function ScenarioSnapshotCard({
  datasetLabel,
  modelLabel,
  mechanismLabel,
  observedMissingness,
  selectedRank,
  cleanBaselineRocAuc,
  reliabilityBins,
}: {
  datasetLabel: string;
  modelLabel: string;
  mechanismLabel: string;
  observedMissingness: string;
  selectedRank: string;
  cleanBaselineRocAuc: string;
  reliabilityBins: number;
}) {
  return (
    <section className="surface-panel p-6">
      <p className="eyebrow">Scenario snapshot</p>
      <dl className="mt-6 space-y-4 text-sm">
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Dataset</dt>
          <dd className="max-w-[14rem] text-right text-ink">{datasetLabel}</dd>
        </div>
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Model</dt>
          <dd className="max-w-[14rem] text-right text-ink">{modelLabel}</dd>
        </div>
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Mechanism</dt>
          <dd className="max-w-[14rem] text-right text-ink">{mechanismLabel}</dd>
        </div>
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Observed missingness</dt>
          <dd className="text-ink">{observedMissingness}</dd>
        </div>
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Comparison rank</dt>
          <dd className="text-ink">{selectedRank}</dd>
        </div>
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Clean baseline ROC-AUC</dt>
          <dd className="text-ink">{cleanBaselineRocAuc}</dd>
        </div>
        <div className="flex items-start justify-between gap-4">
          <dt className="text-muted">Reliability bins</dt>
          <dd className="text-ink">{reliabilityBins}</dd>
        </div>
      </dl>
    </section>
  );
}

function ExampleInputsCard({ features }: { features: string[] }) {
  return (
    <section className="surface-panel p-6">
      <p className="eyebrow">Example inputs</p>
      <h3 className="mt-4 text-2xl font-semibold text-ink">
        What incomplete information can look like
      </h3>
      <p className="mt-3 text-sm leading-7 text-muted">
        These variables come from the selected dataset and illustrate the kinds of signals a model
        may lose when a record is only partially observed.
      </p>

      <div className="mt-6 space-y-3">
        {features.map((feature) => (
          <div
            key={feature}
            className="flex flex-col items-start gap-2 rounded-2xl border border-line/80 bg-white/90 px-4 py-3 sm:flex-row sm:items-center sm:justify-between"
          >
            <span className="text-sm text-ink">{feature}</span>
            <span className="shrink-0 rounded-full bg-accent/10 px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em] text-accent">
              Example signal
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}

export function ExplorerClient({ data }: { data: ExplorerArtifact }) {
  const [dataset, setDataset] = useState(data.defaultSelection.dataset);
  const [model, setModel] = useState(data.defaultSelection.model);
  const [mechanism, setMechanism] = useState(data.defaultSelection.mechanism);
  const [rate, setRate] = useState(data.defaultSelection.rate);
  const [view, setView] = useState<ViewMode>("general");

  const datasetMetaById = useMemo(
    () => Object.fromEntries(data.datasets.map((entry) => [entry.id, entry])),
    [data.datasets],
  );
  const modelMetaById = useMemo(
    () => Object.fromEntries(data.models.map((entry) => [entry.id, entry])),
    [data.models],
  );
  const mechanismMetaById = useMemo(
    () => Object.fromEntries(data.mechanisms.map((entry) => [entry.id, entry])),
    [data.mechanisms],
  );

  const selected =
    data.scenarios.find(
      (scenario) =>
        scenario.dataset === dataset &&
        scenario.model === model &&
        scenario.mechanism === mechanism &&
        scenario.rate === rate,
    ) ?? data.scenarios[0];

  const datasetMeta = datasetMetaById[selected.dataset];
  const modelMeta = modelMetaById[selected.model];
  const mechanismMeta = mechanismMetaById[selected.mechanism];
  const comparisonSlice =
    data.comparisonSlices.find(
      (slice) =>
        slice.dataset === selected.dataset &&
        slice.mechanism === selected.mechanism &&
        slice.rate === selected.rate,
    ) ?? data.comparisonSlices[0];

  const explanation = buildScenarioExplanation(
    selected,
    datasetMeta,
    modelMeta,
    mechanismMeta,
    comparisonSlice?.models ?? [],
    Object.fromEntries(data.models.map((entry) => [entry.id, entry.label])),
  );

  const stressSeries = data.scenarios
    .filter(
      (scenario) =>
        scenario.dataset === selected.dataset &&
        scenario.model === selected.model &&
        scenario.mechanism === selected.mechanism,
    )
    .sort((left, right) => left.rate - right.rate);

  const severity = severityTone(selected.severity.label);
  const selectedRank =
    comparisonSlice?.models.find((entry) => entry.model === selected.model)?.rank ?? null;

  return (
    <div className="space-y-8">
      <div className="grid gap-8 lg:grid-cols-[minmax(0,1.08fr)_minmax(0,0.92fr)]">
        <div className="min-w-0">
          <section className="surface-panel p-6 sm:p-8">
            <div className="flex flex-col gap-6">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
                <div>
                  <p className="eyebrow">Interactive explorer</p>
                  <h2 className="mt-4 text-3xl font-semibold leading-tight text-ink sm:text-4xl">
                    What changes when the model has to predict with missing information?
                  </h2>
                  <p className="mt-3 max-w-2xl text-base leading-8 text-muted">
                    Choose a prediction setting and watch how trust moves alongside ranking,
                    calibration, and missingness severity. The goal is not to produce a diagnosis,
                    but to make uncertainty visible.
                  </p>
                </div>

                <div className="inline-flex rounded-full border border-line bg-white p-1">
                  {(["general", "technical"] as ViewMode[]).map((mode) => (
                    <button
                      key={mode}
                      className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                        view === mode ? "bg-accent text-white" : "text-muted hover:text-ink"
                      }`}
                      onClick={() => setView(mode)}
                      type="button"
                    >
                      {mode === "general" ? "General view" : "Technical view"}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                <label className="flex flex-col gap-2 text-sm font-medium text-ink">
                  Scenario
                  <select
                    className="rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
                    onChange={(event) => setDataset(event.target.value)}
                    value={dataset}
                  >
                    {data.datasets.map((entry) => (
                      <option key={entry.id} value={entry.id}>
                        {entry.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="flex flex-col gap-2 text-sm font-medium text-ink">
                  Model
                  <select
                    className="rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
                    onChange={(event) => setModel(event.target.value)}
                    value={model}
                  >
                    {data.models.map((entry) => (
                      <option key={entry.id} value={entry.id}>
                        {entry.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="flex flex-col gap-2 text-sm font-medium text-ink">
                  Missingness
                  <select
                    className="rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
                    onChange={(event) => setMechanism(event.target.value)}
                    value={mechanism}
                  >
                    {data.mechanisms.map((entry) => (
                      <option key={entry.id} value={entry.id}>
                        {entry.longLabel}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="flex flex-col gap-2 text-sm font-medium text-ink">
                  Missing rate
                  <select
                    className="rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
                    onChange={(event) => setRate(Number(event.target.value))}
                    value={rate}
                  >
                    {data.rates.map((entry) => (
                      <option key={entry} value={entry}>
                        {formatRate(entry)}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            </div>
          </section>
        </div>

        <aside className="min-w-0 space-y-6">
          <TrustMeter
            band={selected.trustBand}
            breakdown={selected.scoreBreakdown}
            score={selected.trustScore}
          />
        </aside>
      </div>

      {view === "general" ? (
        <section className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1.02fr)_minmax(0,0.98fr)] lg:items-start">
            <article className="surface-panel p-6 sm:p-8">
              <p className="eyebrow">Plain-language reading</p>
              <h3 className="mt-4 text-2xl font-semibold text-ink">{explanation.headline}</h3>
              <div className="mt-6 space-y-5 text-base leading-8 text-muted">
                <p>{explanation.overview}</p>
                <p>{explanation.severityRead}</p>
                <p>{explanation.whyItMoves}</p>
                <p>{explanation.stabilityRead}</p>
                <p>{explanation.probabilityRead}</p>
                <p>{explanation.comparisonRead}</p>
                <p className="font-medium text-ink">{explanation.closing}</p>
              </div>
            </article>

            <div className="space-y-6">
              <ExampleInputsCard features={datasetMeta.exampleFeatures} />

              <ScenarioSnapshotCard
                cleanBaselineRocAuc={formatPercent(selected.baseline.meanRocAuc)}
                datasetLabel={datasetMeta.label}
                mechanismLabel={mechanismMeta.longLabel}
                modelLabel={modelMeta.label}
                observedMissingness={formatPercent(selected.meanTestActualRate)}
                reliabilityBins={data.source.calibrationBins}
                selectedRank={selectedRank ? `#${selectedRank} of 3` : "n/a"}
              />
            </div>
          </div>

          <div className="grid gap-5 md:grid-cols-3">
            <article className="surface-panel p-6">
              <p className="eyebrow">Missingness severity</p>
              <h3 className="mt-4 text-2xl font-semibold text-ink">{severity.badge}</h3>
              <p className="mt-3 text-sm leading-7 text-muted">
                {selected.severity.summary}
              </p>
            </article>

            <article className="surface-panel p-6">
              <p className="eyebrow">Ranking signal</p>
              <h3 className="mt-4 text-2xl font-semibold text-ink">
                {selected.metricCards.rocAuc.status === "holding"
                  ? "Holding fairly well"
                  : selected.metricCards.rocAuc.status === "drifting"
                    ? "Starting to slip"
                    : "Dropping hard"}
              </h3>
              <p className="mt-3 text-sm leading-7 text-muted">
                {metricStatusCopy(selected.metricCards.rocAuc, "roc_auc")}
              </p>
            </article>

            <article className="surface-panel p-6">
              <p className="eyebrow">Probability trust</p>
              <h3 className="mt-4 text-2xl font-semibold text-ink">
                {selected.metricCards.ece.status === "holding"
                  ? "Still fairly aligned"
                  : selected.metricCards.ece.status === "drifting"
                    ? "Calibration drift is visible"
                    : "Confidence is getting risky"}
              </h3>
              <p className="mt-3 text-sm leading-7 text-muted">
                {metricStatusCopy(selected.metricCards.ece, "ece")}
              </p>
            </article>
          </div>

          <ReliabilityChart
            baselineProfile={selected.baselineReliability}
            profile={selected.reliability}
            subtitle="The solid line shows the selected condition, while the diagonal marks perfect calibration. When a clean reference is available, the darker dashed line shows how much the probability behavior has shifted."
            title="How the predicted probabilities line up with observed outcomes"
          />

          <ModelComparisonStrip
            modelMeta={modelMetaById}
            models={comparisonSlice?.models ?? []}
            selectedModel={selected.model}
          />
        </section>
      ) : (
        <section className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <ScenarioSnapshotCard
              cleanBaselineRocAuc={formatPercent(selected.baseline.meanRocAuc)}
              datasetLabel={datasetMeta.label}
              mechanismLabel={mechanismMeta.longLabel}
              modelLabel={modelMeta.label}
              observedMissingness={formatPercent(selected.meanTestActualRate)}
              reliabilityBins={data.source.calibrationBins}
              selectedRank={selectedRank ? `#${selectedRank} of 3` : "n/a"}
            />

            <ExampleInputsCard features={datasetMeta.exampleFeatures} />
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <article className="surface-panel p-5">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm uppercase tracking-[0.18em] text-muted">ROC-AUC</p>
                <span className={`inline-flex max-w-full rounded-full px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em] ${statusStyles[selected.metricCards.rocAuc.status]}`}>
                  {selected.metricCards.rocAuc.status}
                </span>
              </div>
              <p className="mt-3 text-3xl font-semibold text-ink">
                {formatPercent(selected.meanRocAuc)}
              </p>
              <p className={`mt-2 text-sm ${metricTone(selected.meanRocAucChange, true)}`}>
                {formatSignedDelta(selected.meanRocAucChange)} vs clean
              </p>
              <p className="mt-3 text-sm leading-7 text-muted">
                {metricStatusCopy(selected.metricCards.rocAuc, "roc_auc")}
              </p>
            </article>

            <article className="surface-panel p-5">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm uppercase tracking-[0.18em] text-muted">Accuracy</p>
                <span className={`inline-flex max-w-full rounded-full px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em] ${statusStyles[selected.metricCards.accuracy.status]}`}>
                  {selected.metricCards.accuracy.status}
                </span>
              </div>
              <p className="mt-3 text-3xl font-semibold text-ink">
                {formatPercent(selected.meanAccuracy)}
              </p>
              <p className={`mt-2 text-sm ${metricTone(selected.meanAccuracyChange, true)}`}>
                {formatSignedDelta(selected.meanAccuracyChange)} vs clean
              </p>
              <p className="mt-3 text-sm leading-7 text-muted">
                {metricStatusCopy(selected.metricCards.accuracy, "accuracy")}
              </p>
            </article>

            <article className="surface-panel p-5">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm uppercase tracking-[0.18em] text-muted">Brier score</p>
                <span className={`inline-flex max-w-full rounded-full px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em] ${statusStyles[selected.metricCards.brier.status]}`}>
                  {selected.metricCards.brier.status}
                </span>
              </div>
              <p className="mt-3 text-3xl font-semibold text-ink">{formatDecimal(selected.meanBrier)}</p>
              <p className={`mt-2 text-sm ${metricTone(selected.meanBrierChange)}`}>
                {formatSignedDelta(selected.meanBrierChange)} vs clean
              </p>
              <p className="mt-3 text-sm leading-7 text-muted">
                {metricStatusCopy(selected.metricCards.brier, "brier")}
              </p>
            </article>

            <article className="surface-panel p-5">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm uppercase tracking-[0.18em] text-muted">ECE</p>
                <span className={`inline-flex max-w-full rounded-full px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em] ${statusStyles[selected.metricCards.ece.status]}`}>
                  {selected.metricCards.ece.status}
                </span>
              </div>
              <p className="mt-3 text-3xl font-semibold text-ink">{formatDecimal(selected.meanEce)}</p>
              <p className={`mt-2 text-sm ${metricTone(selected.meanEceChange)}`}>
                {formatSignedDelta(selected.meanEceChange)} vs clean
              </p>
              <p className="mt-3 text-sm leading-7 text-muted">
                {metricStatusCopy(selected.metricCards.ece, "ece")}
              </p>
            </article>
          </div>

          <ReliabilityChart
            baselineProfile={selected.baselineReliability}
            profile={selected.reliability}
            subtitle="This curve compares predicted risk with observed outcomes in the selected condition. Larger departures from the diagonal mean the model's confidence is becoming less well aligned with reality."
            title="Calibration shape for the selected condition"
          />

          <ModelComparisonStrip
            modelMeta={modelMetaById}
            models={comparisonSlice?.models ?? []}
            selectedModel={selected.model}
          />

          <div className="grid gap-6 lg:grid-cols-[minmax(0,1.08fr)_minmax(0,0.92fr)]">
            <article className="surface-panel overflow-hidden">
              <div className="border-b border-line px-6 py-5">
                <p className="eyebrow">Stress test by missingness rate</p>
                <h3 className="mt-4 text-2xl font-semibold text-ink">
                  Same model, same mechanism, increasing information loss
                </h3>
              </div>

              <div className="overflow-x-auto px-2 pb-2 md:overflow-visible">
                <table className="w-full table-fixed border-separate border-spacing-y-3 text-left text-sm">
                  <thead className="text-[0.68rem] uppercase tracking-[0.16em] text-muted">
                    <tr>
                      <th className="w-[12%] px-3 pt-4">Rate</th>
                      <th className="w-[22%] px-3 pt-4">Trust</th>
                      <th className="w-[22%] px-3 pt-4">Severity</th>
                      <th className="w-[15%] px-3 pt-4">ROC-AUC</th>
                      <th className="w-[14%] px-3 pt-4">Brier</th>
                      <th className="w-[15%] px-3 pt-4">ECE</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stressSeries.map((scenario) => (
                      <tr
                        key={scenario.id}
                        className="rounded-2xl bg-[rgba(255,255,255,0.92)] text-ink shadow-[0_18px_40px_-30px_rgba(14,49,57,0.6)]"
                        >
                          <td className="rounded-l-2xl px-3 py-4 font-semibold">{formatRate(scenario.rate)}</td>
                          <td className="px-3 py-4">
                            <span className="inline-flex whitespace-nowrap rounded-full bg-panelAlt px-2.5 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.14em] text-ink">
                              {scenario.trustBand} / {scenario.trustScore}
                            </span>
                          </td>
                          <td className="px-3 py-4 capitalize">{scenario.severity.label}</td>
                          <td className="px-3 py-4">{formatPercent(scenario.meanRocAuc)}</td>
                          <td className="px-3 py-4">{formatDecimal(scenario.meanBrier)}</td>
                          <td className="rounded-r-2xl px-3 py-4">{formatDecimal(scenario.meanEce)}</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </article>

            <article className="surface-panel p-6">
              <p className="eyebrow">Reading guide</p>
              <p className="mt-4 text-sm leading-7 text-muted">
                Read these views together rather than one at a time. A model can remain strong on
                headline metrics while its probability estimates drift away from trustworthy
                calibration, especially as more information goes missing.
              </p>
            </article>
          </div>
        </section>
      )}
    </div>
  );
}
