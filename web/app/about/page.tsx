export default function AboutPage() {
  return (
    <div className="space-y-10 pb-20">
      <section className="max-w-4xl">
        <p className="eyebrow">About</p>
        <h1 className="mt-6 text-5xl font-semibold leading-[0.98] text-ink sm:text-6xl">
          A project about uncertainty, not just prediction.
        </h1>
        <p className="mt-5 text-lg leading-9 text-muted">
          This project grew out of a more personal shift in how I think about medicine. After
          experiencing seizures in high school, I became much more aware that medical decisions are
          often made with incomplete information, imperfect signals, and real stakes. That pushed my
          interest in medicine away from a vague "health + tech" idea and toward statistics,
          modeling, and trustworthy decision-making.
        </p>
      </section>
      <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <article className="surface-panel p-7">
          <p className="eyebrow">Project mission</p>
          <h2 className="mt-5 text-4xl font-semibold text-ink">
            High-stakes systems should be honest about uncertainty.
          </h2>
          <p className="mt-5 text-base leading-8 text-muted">
            At its core, this project studies how clinical prediction models behave when data go
            missing. The site turns that work into something more legible: a way to show that
            confidence is not the same thing as trustworthiness, especially when a model is missing
            some of the information it would normally rely on.
          </p>
          <p className="mt-5 text-base leading-8 text-muted">
            The aim is not to imitate a medical product or dramatize medicine. It is to ask a
            serious question in public: if uncertainty is unavoidable, how should a model express
            it responsibly?
          </p>
        </article>

        <article className="surface-panel p-7">
          <p className="eyebrow">Core idea</p>
          <h2 className="mt-5 text-4xl font-semibold text-ink">
            Missing information should change how much certainty we allow.
          </h2>
          <p className="mt-5 text-base leading-8 text-muted">
            In clinical data, absence is rarely just an empty cell. It can change how a model ranks
            cases, how well its probabilities line up with reality, and how much confidence a
            person should place in its output.
          </p>
          <p className="mt-5 text-base leading-8 text-muted">
            This site uses controlled benchmark experiments to make that hidden shift visible, so
            visitors can see why a responsible prediction system should communicate uncertainty
            instead of simply sounding sure.
          </p>
        </article>
      </section>
    </div>
  );
}
