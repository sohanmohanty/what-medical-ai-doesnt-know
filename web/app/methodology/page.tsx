import { loadExplorerData } from "@/lib/load-explorer-data";

export default async function MethodologyPage() {
  const data = await loadExplorerData();

  return (
    <div className="space-y-10 pb-20">
      <section className="max-w-4xl">
        <p className="eyebrow">Methodology</p>
        <h1 className="mt-6 text-4xl font-semibold leading-[0.98] text-ink sm:text-6xl">
          The benchmark behind the experience
        </h1>
        <p className="mt-5 text-lg leading-9 text-muted">
          Here are the data, model families, missingness patterns, and evaluation choices behind
          the explorer. The goal is transparency: the interface shows what it is built on
          and where its limits are.
        </p>
      </section>
      <section className="grid gap-6 lg:grid-cols-2">
        <article className="surface-panel p-7">
          <p className="eyebrow">Datasets</p>
          <div className="mt-5 space-y-4">
            {data.datasets.map((dataset) => (
              <div key={dataset.id} className="rounded-[1.5rem] border border-line/70 bg-white/90 p-5">
                <h2 className="text-2xl font-semibold text-ink">{dataset.label}</h2>
                <p className="mt-3 text-sm leading-7 text-muted">{dataset.plainSummary}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Models</p>
          <div className="mt-5 space-y-4">
            {data.models.map((model) => (
              <div key={model.id} className="rounded-[1.5rem] border border-line/70 bg-white/90 p-5">
                <h2 className="text-2xl font-semibold text-ink">{model.label}</h2>
                <p className="mt-3 text-sm leading-7 text-muted">{model.plainSummary}</p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <article className="surface-panel p-7">
          <p className="eyebrow">Missingness mechanisms</p>
          <div className="mt-5 space-y-4">
            {data.mechanisms.map((mechanism) => (
              <div key={mechanism.id} className="rounded-[1.5rem] border border-line/70 bg-white/90 p-5">
                <h2 className="text-2xl font-semibold text-ink">{mechanism.longLabel}</h2>
                <p className="mt-3 text-sm leading-7 text-muted">{mechanism.plainSummary}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Key idea</p>
          <h2 className="mt-5 text-2xl font-semibold text-ink">
            Confidence is a claim. Trust is a check on that claim.
          </h2>
          <p className="mt-3 text-sm leading-7 text-muted">
            Here, confidence means the probability a model reports. Trust means checking whether
            that probability remains believable after looking at calibration, robustness, and the
            amount of missing information.
          </p>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Evaluation</p>
          <ul className="mt-5 space-y-4 text-sm leading-7 text-muted">
            <li>
              ROC-AUC and accuracy remain visible, but they are not treated as the whole story.
            </li>
            <li>
              Brier score and expected calibration error are emphasized because a model can still
              rank cases reasonably well while its probabilities become less trustworthy.
            </li>
            <li>
              Results are shown from a controlled benchmark setting in which models are evaluated as
              information is progressively removed from the test data.
            </li>
            <li>
              Reliability views are drawn from saved prediction probabilities, so the calibration
              curves reflect measured behavior rather than decorative examples.
            </li>
          </ul>
        </article>
      </section>

      <section className="surface-panel p-8">
        <p className="eyebrow">Limitations</p>
        <div className="mt-5 grid gap-5 md:grid-cols-2">
          <div className="rounded-[1.5rem] border border-line/70 bg-white/90 p-5">
            <h2 className="text-2xl font-semibold text-ink">Controlled, not clinical deployment</h2>
            <p className="mt-3 text-sm leading-7 text-muted">
              These are public benchmark datasets and controlled missingness constructions, not
              hospital production systems or patient-specific predictions.
            </p>
          </div>
          <div className="rounded-[1.5rem] border border-line/70 bg-white/90 p-5">
            <h2 className="text-2xl font-semibold text-ink">Educational, not diagnostic</h2>
            <p className="mt-3 text-sm leading-7 text-muted">
              The explorer shows how trustworthiness changes under incomplete information. It
              should never be used for personal medical decisions.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
