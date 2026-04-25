export default function PaperPage() {
  return (
    <div className="space-y-10 pb-20">
      <section className="max-w-4xl">
        <p className="eyebrow">Research paper</p>
        <h1 className="mt-6 text-4xl font-semibold leading-[0.98] text-ink sm:text-6xl">
          The full academic report behind the explorer.
        </h1>
        <p className="mt-5 max-w-3xl text-lg leading-9 text-muted">
          The website provides an interactive interpretation of the benchmark. The paper is the technical
          artifact: it describes the benchmark design, missing-data mechanisms, model comparisons,
          calibration metrics, figures, limitations, and references.
        </p>
      </section>

      <section className="surface-panel p-7 sm:p-8">
        <div className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
          <div>
            <p className="eyebrow">PDF report</p>
            <h2 className="mt-5 text-3xl font-semibold text-ink sm:text-4xl">
              Robustness and Calibration of Clinical Machine Learning Models Under Missing Data
            </h2>
            <p className="mt-5 text-base leading-8 text-muted">
              This report is written as a scholarly analysis of the benchmark. It is the best place
              to evaluate the statistical and experimental rigor of the project.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <a className="button-primary" href="/paper.pdf" rel="noopener noreferrer" target="_blank">
                Open the PDF
              </a>
              <a className="button-secondary" href="/paper.pdf" download>
                Download PDF
              </a>
            </div>
          </div>

          <div className="rounded-[1.6rem] border border-line/80 bg-white/90 p-6">
            <p className="text-sm uppercase tracking-[0.18em] text-muted">What it covers</p>
            <ul className="mt-5 space-y-4 text-sm leading-7 text-muted">
              <li>Controlled MCAR, MAR, and MNAR missingness experiments</li>
              <li>Logistic regression, random forest, and gradient boosting comparisons</li>
              <li>ROC-AUC, accuracy, Brier score, ECE, and reliability diagrams</li>
              <li>Limitations and artifact references for reproducibility</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        <article className="surface-panel p-6">
          <p className="eyebrow">Focus</p>
          <h2 className="mt-4 text-2xl font-semibold text-ink">Calibration under missing data</h2>
          <p className="mt-3 text-sm leading-7 text-muted">
            The paper distinguishes ranking performance from probability reliability.
          </p>
        </article>

        <article className="surface-panel p-6">
          <p className="eyebrow">Evidence</p>
          <h2 className="mt-4 text-2xl font-semibold text-ink">Saved benchmark outputs</h2>
          <p className="mt-3 text-sm leading-7 text-muted">
            Claims are grounded in reproducible artifacts, figures, and summary tables.
          </p>
        </article>

        <article className="surface-panel p-6">
          <p className="eyebrow">Scope</p>
          <h2 className="mt-4 text-2xl font-semibold text-ink">Research, not diagnosis</h2>
          <p className="mt-3 text-sm leading-7 text-muted">
            The work studies model behavior on public benchmarks and does not provide medical advice.
          </p>
        </article>
      </section>
    </div>
  );
}
