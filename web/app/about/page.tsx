export default function AboutPage() {
  return (
    <div className="space-y-10 pb-20">
      <section className="max-w-4xl">
        <p className="eyebrow">About</p>
        <h1 className="mt-6 text-4xl font-semibold leading-[0.98] text-ink sm:text-6xl">
          A project about uncertainty, not just prediction.
        </h1>
        <p className="mt-5 text-lg leading-9 text-muted">
          I started thinking differently about medicine after experiencing seizures in high school.
          What stayed with me was not only the medical side, but the uncertainty around it: decisions
          made from incomplete signals, imperfect measurements, and real stakes. That pulled my
          interest away from a vague "health + tech" idea and toward statistics, modeling, and
          trustworthy decision-making.
        </p>
      </section>
      <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <article className="surface-panel p-7">
          <p className="eyebrow">Why this matters</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink sm:text-4xl">
            High-stakes systems should be honest about uncertainty.
          </h2>
          <p className="mt-5 text-base leading-8 text-muted">
            The benchmark asks how clinical prediction models behave when data go missing. The
            interface makes that behavior easier to see: confidence is not the same thing as
            trustworthiness, especially when a model is missing information it would normally rely
            on.
          </p>
          <p className="mt-5 text-base leading-8 text-muted">
            The aim is not to imitate a medical product or dramatize medicine. It is to ask a
            serious question in public: if uncertainty is unavoidable, how should a model express
            it responsibly?
          </p>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Core idea</p>
          <h2 className="mt-5 text-3xl font-semibold text-ink sm:text-4xl">
            Missing information should change how much certainty we allow.
          </h2>
          <p className="mt-5 text-base leading-8 text-muted">
            In clinical data, absence is rarely just an empty cell. It can change how a model ranks
            cases, how well its probabilities line up with reality, and how much confidence a
            person should place in its output.
          </p>
          <p className="mt-5 text-base leading-8 text-muted">
            Controlled benchmark experiments make that hidden shift visible. The central point is
            that a prediction system should show uncertainty when the evidence behind its output
            gets thinner.
          </p>
        </article>
      </section>
    </div>
  );
}
