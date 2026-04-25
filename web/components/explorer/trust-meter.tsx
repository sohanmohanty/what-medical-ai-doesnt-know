import { trustCopy } from "@/lib/explainer";
import { ScoreBreakdown, TrustBand } from "@/lib/types";

const bandClasses: Record<TrustBand, string> = {
  stable: "bg-accent/90 text-white",
  caution: "bg-caution text-ink",
  fragile: "bg-danger text-white",
};

export function TrustMeter({
  score,
  band,
  breakdown,
}: {
  score: number;
  band: TrustBand;
  breakdown: ScoreBreakdown;
}) {
  const copy = trustCopy(band);
  const rows = [
    { label: "Ranking retention", value: breakdown.ranking },
    { label: "Calibration trust", value: breakdown.calibration },
    { label: "Information completeness", value: breakdown.completeness },
  ];

  return (
    <div className="surface-panel p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="eyebrow">Trust signal</p>
          <h3 className="mt-4 text-2xl font-semibold text-ink">{copy.label}</h3>
          <p className="mt-2 max-w-sm text-sm leading-7 text-muted">{copy.summary}</p>
          <p className="mt-3 max-w-sm text-xs leading-6 text-muted">
            Confidence is the probability a model reports. Trust asks whether that confidence still
            holds up once calibration, stability, and missingness are taken into account.
          </p>
        </div>
        <div className="text-right">
          <p className="text-5xl font-semibold text-ink">{score}</p>
          <p className="text-xs uppercase tracking-[0.18em] text-muted">/ 100</p>
        </div>
      </div>

      <div className="mt-6 h-4 overflow-hidden rounded-full bg-panelAlt">
        <div
          className={`h-full rounded-full transition-all ${bandClasses[band]}`}
          style={{ width: `${score}%` }}
        />
      </div>

      <div className="mt-6 space-y-4">
        {rows.map((row) => (
          <div key={row.label}>
            <div className="flex items-center justify-between gap-4 text-sm">
              <span className="text-muted">{row.label}</span>
              <span className="font-semibold text-ink">{row.value}</span>
            </div>
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-panelAlt">
              <div className="h-full rounded-full bg-accent/75" style={{ width: `${row.value}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
