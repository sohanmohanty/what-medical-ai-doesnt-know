import { formatDecimal, formatPercent } from "@/lib/explainer";
import { ComparisonSliceModel, ModelMeta } from "@/lib/types";

const bandStyles = {
  stable: "bg-accent/15 text-accent",
  caution: "bg-caution/30 text-ink",
  fragile: "bg-danger/15 text-danger",
};

export function ModelComparisonStrip({
  selectedModel,
  models,
  modelMeta,
}: {
  selectedModel: string;
  models: ComparisonSliceModel[];
  modelMeta: Record<string, ModelMeta>;
}) {
  return (
    <section className="surface-panel p-6">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="eyebrow">Model comparison</p>
          <h3 className="mt-4 text-2xl font-semibold text-ink">
            Same dataset, same missingness, different model behavior
          </h3>
        </div>
        <p className="max-w-xl text-sm leading-7 text-muted">
          This comparison uses the same dataset, mechanism, and missingness severity so the main
          difference is model behavior, not a different test condition.
        </p>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        {models.map((entry) => {
          const selected = entry.model === selectedModel;
          return (
            <article
              key={entry.model}
              className={`flex h-full flex-col overflow-hidden rounded-[1.6rem] border p-5 transition ${
                selected
                  ? "border-accent/40 bg-[rgba(229,244,244,0.9)]"
                  : "border-line/80 bg-white/90"
              }`}
            >
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-xs uppercase tracking-[0.16em] text-muted">Rank #{entry.rank}</p>
                <span
                  className={`inline-flex max-w-full shrink-0 rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${bandStyles[entry.trustBand]}`}
                >
                  {entry.trustBand}
                </span>
              </div>

              <h4 className="mt-3 max-w-[12ch] text-2xl font-semibold leading-[1.04] text-ink">
                {modelMeta[entry.model].label}
              </h4>

              <p className="mt-3 text-sm leading-7 text-muted">{modelMeta[entry.model].audienceSummary}</p>

              <div className="mt-5 grid gap-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-muted">Trust score</span>
                  <span className="font-semibold text-ink">{entry.trustScore}/100</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted">ROC-AUC</span>
                  <span className="font-semibold text-ink">{formatPercent(entry.meanRocAuc)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted">Brier</span>
                  <span className="font-semibold text-ink">{formatDecimal(entry.meanBrier)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted">ECE</span>
                  <span className="font-semibold text-ink">{formatDecimal(entry.meanEce)}</span>
                </div>
              </div>

              {selected ? (
                <p className="mt-auto pt-5">
                  <span className="inline-flex rounded-[1rem] border border-accent/20 bg-white/70 px-3 py-2 text-xs uppercase tracking-[0.16em] text-accent">
                    Selected model
                  </span>
                </p>
              ) : null}
            </article>
          );
        })}
      </div>
    </section>
  );
}
