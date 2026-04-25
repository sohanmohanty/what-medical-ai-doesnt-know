type DisclaimerVariant = "banner" | "inline" | "compact";

const variantStyles: Record<DisclaimerVariant, string> = {
  banner: "surface-panel border-caution/40 bg-[rgba(255,250,233,0.92)] p-5",
  inline: "rounded-[1.5rem] border border-line/80 bg-[rgba(255,255,255,0.92)] p-5",
  compact: "rounded-[1.25rem] border border-line/80 bg-white/80 p-4",
};

const titleStyles: Record<DisclaimerVariant, string> = {
  banner: "text-base",
  inline: "text-lg",
  compact: "text-sm",
};

export function MedicalDisclaimer({
  variant = "inline",
}: {
  variant?: DisclaimerVariant;
}) {
  return (
    <section className={variantStyles[variant]}>
      <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div className="max-w-3xl">
          <p className="eyebrow">Disclaimer</p>
          <h2 className={`mt-3 font-semibold text-ink ${titleStyles[variant]}`}>
            Educational benchmark explorer only
          </h2>
          <p className="mt-2 text-sm leading-7 text-muted">
            This benchmark explorer shows how clinical prediction models behave when data are
            incomplete. It is not medical advice, not a diagnosis tool, and not designed for
            personal health decisions.
          </p>
        </div>

        <ul className="grid gap-2 text-sm leading-7 text-muted md:max-w-sm">
          <li>No chatbot or symptom-checking behavior</li>
          <li>No user medical-data upload or storage</li>
          <li>No fake clinical claims or treatment guidance</li>
        </ul>
      </div>
    </section>
  );
}
