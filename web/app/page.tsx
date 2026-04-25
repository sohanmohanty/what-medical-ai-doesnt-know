import Link from "next/link";

import { MedicalDisclaimer } from "@/components/medical-disclaimer";
import { loadExplorerData } from "@/lib/load-explorer-data";

function labelForId(items: { id: string; label: string }[], id: string) {
  return items.find((item) => item.id === id)?.label ?? id;
}

export default async function HomePage() {
  const data = await loadExplorerData();
  const rankingDrop = data.highlights.largestRankingDrop;

  return (
    <div className="space-y-24 pb-20">
      <section className="grid gap-12 lg:grid-cols-[1.1fr_0.9fr] lg:items-start">
        <div>
          <p className="eyebrow">Interactive uncertainty explorer</p>
          <h1 className="mt-6 max-w-4xl text-5xl font-semibold leading-[0.96] text-ink sm:text-6xl">
            How much should we trust a medical model when part of the patient record is missing?
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-9 text-muted">
            This site lets you remove information, compare models, and see how a medical
            prediction can change as the record becomes more incomplete. The goal is to show that
            confidence and trust are not the same thing.
          </p>

          <div className="mt-6 grid max-w-2xl gap-3 text-sm sm:grid-cols-3">
            <div className="border-l border-line pl-3">
              <p className="text-xs uppercase tracking-[0.16em] text-muted">Step 1</p>
              <p className="mt-1 font-medium text-ink">Pick a prediction setting</p>
            </div>
            <div className="border-l border-line pl-3">
              <p className="text-xs uppercase tracking-[0.16em] text-muted">Step 2</p>
              <p className="mt-1 font-medium text-ink">Remove information</p>
            </div>
            <div className="border-l border-line pl-3">
              <p className="text-xs uppercase tracking-[0.16em] text-muted">Step 3</p>
              <p className="mt-1 font-medium text-ink">Watch trust change</p>
            </div>
          </div>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link className="button-primary" href="#confidence-vs-trust">
              Start with the idea
            </Link>
            <Link className="button-secondary" href="#how-to-read-it">
              See how it works
            </Link>
          </div>

          <p className="mt-6 max-w-2xl text-sm leading-7 text-muted">
            Educational and research-oriented only. This is not medical advice, diagnosis, or a
            personal health tool.
          </p>

        </div>

        <div className="surface-panel relative overflow-hidden p-8">
          <div className="absolute right-0 top-0 h-40 w-40 rounded-full bg-accent/10 blur-3xl" />
          <p className="eyebrow">Simple example</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink">
            The probability can look similar while trust changes.
          </h2>
          <p className="mt-4 text-base leading-8 text-muted">
            Imagine a model reports almost the same probability before and after part of the record
            disappears. The number may still look confident, but the evidence behind it has changed.
          </p>

          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            <div className="rounded-[1.5rem] border border-line/80 bg-white/85 p-5">
              <p className="text-xs uppercase tracking-[0.18em] text-muted">More complete record</p>
              <p className="mt-4 text-4xl font-semibold text-ink">80%</p>
              <p className="mt-1 text-sm text-muted">reported probability</p>
              <div className="mt-5">
                <div className="flex items-center justify-between text-xs uppercase tracking-[0.16em] text-muted">
                  <span>Trust</span>
                  <span>Stable</span>
                </div>
                <div className="mt-2 h-3 rounded-full bg-accent/12">
                  <div className="h-full w-[86%] rounded-full bg-accent" />
                </div>
              </div>
            </div>

            <div className="rounded-[1.5rem] border border-line/80 bg-white/85 p-5">
              <p className="text-xs uppercase tracking-[0.18em] text-muted">Partly missing record</p>
              <p className="mt-4 text-4xl font-semibold text-ink">78%</p>
              <p className="mt-1 text-sm text-muted">reported probability</p>
              <div className="mt-5">
                <div className="flex items-center justify-between text-xs uppercase tracking-[0.16em] text-muted">
                  <span>Trust</span>
                  <span>Caution</span>
                </div>
                <div className="mt-2 h-3 rounded-full bg-amber-100">
                  <div className="h-full w-[48%] rounded-full bg-amber-300" />
                </div>
              </div>
            </div>
          </div>

          <p className="mt-5 rounded-[1.5rem] border border-line/70 bg-white/75 p-4 text-sm leading-7 text-muted">
            The exact probability is not the whole story. The harder question is whether that
            probability still deserves trust after missingness, calibration, and model stability are
            taken into account.
          </p>

          <div className="mt-5 grid gap-3 text-sm sm:grid-cols-3">
            <div className="border-l border-line pl-3">
              <p className="text-xs uppercase tracking-[0.16em] text-muted">1</p>
              <p className="mt-1 font-medium text-ink">Choose a model</p>
            </div>
            <div className="border-l border-line pl-3">
              <p className="text-xs uppercase tracking-[0.16em] text-muted">2</p>
              <p className="mt-1 font-medium text-ink">Remove information</p>
            </div>
            <div className="border-l border-line pl-3">
              <p className="text-xs uppercase tracking-[0.16em] text-muted">3</p>
              <p className="mt-1 font-medium text-ink">Compare trust</p>
            </div>
          </div>
        </div>
      </section>

      <section id="confidence-vs-trust" className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <article className="surface-panel p-7">
          <p className="eyebrow">Confidence vs. Trust</p>
          <h2 className="mt-5 text-4xl font-semibold text-ink">
            They sound similar, but they are not the same.
          </h2>
          <p className="mt-4 max-w-2xl text-base leading-8 text-muted">
            A model can sound very sure of itself and still be wrong about how trustworthy that
            confidence really is. The explorer makes that gap visible.
          </p>
        </article>

        <div className="grid gap-5 md:grid-cols-2">
          <article className="surface-panel p-6">
            <p className="eyebrow">Confidence</p>
            <h3 className="mt-4 text-2xl font-semibold text-ink">
              The probability the model reports
            </h3>
            <p className="mt-3 text-sm leading-7 text-muted">
              If a model says there is an 80% chance of an outcome, that number is its confidence.
              It tells you what the model is claiming.
            </p>
          </article>

          <article className="surface-panel p-6">
            <p className="eyebrow">Trust</p>
            <h3 className="mt-4 text-2xl font-semibold text-ink">
              Whether that confidence still holds up
            </h3>
            <p className="mt-3 text-sm leading-7 text-muted">
              Trust asks whether the probability still lines up with reality once we check
              calibration, stability, and how much information is missing.
            </p>
          </article>
        </div>
      </section>

      <section className="surface-panel p-7 sm:p-8">
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div className="max-w-2xl">
            <p className="eyebrow">Next Step</p>
            <h2 className="mt-4 text-3xl font-semibold text-ink">
              Once the distinction is clear, try the interactive explorer.
            </h2>
            <p className="mt-3 text-base leading-8 text-muted">
              Start with one prediction setting, remove information, and watch how the reported
              probability and the trust signal move together.
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            <Link className="button-primary" href="/explorer">
              Open the explorer
            </Link>
            <Link className="button-secondary" href="/methodology">
              Read the methodology
            </Link>
          </div>
        </div>
      </section>

      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <article className="surface-panel p-6">
          <p className="text-sm uppercase tracking-[0.18em] text-muted">Datasets</p>
          <p className="mt-4 text-4xl font-semibold text-ink">{data.datasets.length}</p>
          <p className="mt-3 text-sm leading-7 text-muted">
            Contrasting benchmark settings to show that robustness depends on context.
          </p>
        </article>
        <article className="surface-panel p-6">
          <p className="text-sm uppercase tracking-[0.18em] text-muted">Models</p>
          <p className="mt-4 text-4xl font-semibold text-ink">{data.models.length}</p>
          <p className="mt-3 text-sm leading-7 text-muted">
            Logistic regression, random forest, and gradient boosting under shared conditions.
          </p>
        </article>
        <article className="surface-panel p-6">
          <p className="text-sm uppercase tracking-[0.18em] text-muted">Missingness patterns</p>
          <p className="mt-4 text-4xl font-semibold text-ink">{data.mechanisms.length}</p>
          <p className="mt-3 text-sm leading-7 text-muted">
            MCAR, MAR, and MNAR are presented in plain language and compared directly.
          </p>
        </article>
        <article className="surface-panel p-6">
          <p className="text-sm uppercase tracking-[0.18em] text-muted">Stress levels</p>
          <p className="mt-4 text-4xl font-semibold text-ink">{data.rates.length}</p>
          <p className="mt-3 text-sm leading-7 text-muted">
            From 10% to 50% missingness so visitors can see fragility emerge instead of guessing.
          </p>
        </article>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <article className="surface-panel p-7">
          <p className="eyebrow">General mode</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink">Plain English first</h2>
          <p className="mt-4 text-base leading-8 text-muted">
            Start with a plain-language reading of what changed, why it changed, and whether a
            reported probability should still be trusted.
          </p>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Technical mode</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink">Metrics that respect uncertainty</h2>
          <p className="mt-4 text-base leading-8 text-muted">
            ROC-AUC stays visible, but Brier score, ECE, missingness severity, reliability curves,
            and same-slice model comparison all help tell the trust story.
          </p>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Why it feels different</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink">
            Built for clarity, grounded in evidence
          </h2>
          <p className="mt-4 text-base leading-8 text-muted">
            The charts are backed by saved benchmark outputs, not decorative placeholder values.
            The goal is to make missing-data behavior understandable without flattening the
            statistical story.
          </p>
        </article>
      </section>
      <section id="how-to-read-it" className="surface-panel p-8 sm:p-10">
        <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-center">
          <div>
            <p className="eyebrow">How to read it</p>
            <h2 className="mt-5 text-4xl font-semibold text-ink">
              From benchmark results to a clearer trust question
            </h2>
            <p className="mt-4 max-w-xl text-base leading-8 text-muted">
              The experience begins with public clinical benchmark data, stresses each model under
              incomplete information, and then translates the results into a simpler question:
              when should a prediction still be trusted, and when should it be treated with more
              caution?
            </p>
          </div>

          <div className="rounded-[1.75rem] border border-line/80 bg-[rgba(255,255,255,0.92)] p-6 shadow-[0_30px_70px_-42px_rgba(18,54,63,0.7)]">
            <div className="space-y-4">
              <div className="rounded-[1.25rem] border border-line/70 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-muted">Step 1</p>
                <p className="mt-2 text-base font-semibold text-ink">Public clinical benchmark data</p>
              </div>
              <div className="rounded-[1.25rem] border border-line/70 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-muted">Step 2</p>
                <p className="mt-2 text-base font-semibold text-ink">
                  Missing information introduced under MCAR, MAR, and MNAR
                </p>
              </div>
              <div className="rounded-[1.25rem] border border-line/70 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-muted">Step 3</p>
                <p className="mt-2 text-base font-semibold text-ink">
                  Multiple model families evaluated side by side
                </p>
              </div>
              <div className="rounded-[1.25rem] border border-line/70 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-muted">Step 4</p>
                <p className="mt-2 text-base font-semibold text-ink">
                  Ranking, calibration, and probability quality read together
                </p>
              </div>
              <div className="rounded-[1.25rem] border border-line/70 bg-white/80 p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-muted">Step 5</p>
                <p className="mt-2 text-base font-semibold text-ink">
                  Results translated into an interactive view of trust under uncertainty
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-2">
        <article className="surface-panel p-7">
          <p className="eyebrow">Sharpest ranking drop</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink">
            Accuracy and trust do not always break in the same way.
          </h2>
          <p className="mt-4 text-base leading-8 text-muted">
            {labelForId(data.models, rankingDrop.model)} on {labelForId(data.datasets, rankingDrop.dataset)} under{" "}
            {labelForId(data.mechanisms, rankingDrop.mechanism)} at {Math.round(rankingDrop.rate * 100)}%
            missingness records the largest ROC-AUC drop in this benchmark:{" "}
            {rankingDrop.meanRocAucChange.toFixed(3)}. In other words, this is where ranking
            performance itself starts to give way most visibly.
          </p>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Why that matters</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink">
            A model can still look accurate while becoming less reliable.
          </h2>
          <p className="mt-4 text-base leading-8 text-muted">
            Ranking and calibration do not always fail together. A confident-looking model can still
            drift away from trustworthy probability estimates, and that difference is what the
            explorer is built to show.
          </p>
        </article>
      </section>

      <MedicalDisclaimer variant="compact" />
    </div>
  );
}
