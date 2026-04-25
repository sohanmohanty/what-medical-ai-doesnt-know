import { ReliabilityProfile } from "@/lib/types";

function pointsFromProfile(profile: ReliabilityProfile | null, width: number, height: number) {
  if (!profile) {
    return [];
  }

  return profile.bins
    .filter((bin) => bin.count > 0 && bin.meanPred !== null && bin.fracPositive !== null)
    .map((bin) => {
      const x = 28 + bin.meanPred! * (width - 56);
      const y = height - 28 - bin.fracPositive! * (height - 56);
      return { ...bin, x, y };
    });
}

function linePath(points: { x: number; y: number }[]) {
  if (!points.length) {
    return "";
  }

  return points
    .map((point, index) => `${index === 0 ? "M" : "L"} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`)
    .join(" ");
}

export function ReliabilityChart({
  profile,
  baselineProfile,
  title,
  subtitle,
}: {
  profile: ReliabilityProfile | null;
  baselineProfile?: ReliabilityProfile | null;
  title: string;
  subtitle: string;
}) {
  const width = 360;
  const height = 232;
  const points = pointsFromProfile(profile, width, height);
  const baselinePoints = pointsFromProfile(baselineProfile ?? null, width, height);

  return (
    <article className="surface-panel p-6">
      <p className="eyebrow">Reliability view</p>
      <h3 className="mt-4 text-[1.65rem] font-semibold leading-[1.15] text-ink">{title}</h3>
      <p className="mt-3 max-w-2xl text-sm leading-7 text-muted">{subtitle}</p>

      <div className="mt-6 mx-auto max-w-[42rem] overflow-hidden rounded-[1.6rem] border border-line/80 bg-[linear-gradient(180deg,rgba(241,248,248,0.78),rgba(255,255,255,0.94))] p-3">
        <svg aria-label={title} className="h-auto w-full" viewBox={`0 0 ${width} ${height}`}>
          <defs>
            <linearGradient id="current-line" x1="0%" x2="100%" y1="0%" y2="100%">
              <stop offset="0%" stopColor="rgba(23, 120, 128, 0.95)" />
              <stop offset="100%" stopColor="rgba(204, 90, 59, 0.95)" />
            </linearGradient>
          </defs>

          <rect fill="rgba(255,255,255,0.28)" height={height} rx="24" width={width} />

          {[0, 0.25, 0.5, 0.75, 1].map((tick) => {
            const x = 28 + tick * (width - 56);
            const y = height - 28 - tick * (height - 56);
            return (
              <g key={tick}>
                <line stroke="rgba(124, 151, 156, 0.24)" strokeWidth="1" x1={x} x2={x} y1={24} y2={height - 28} />
                <line stroke="rgba(124, 151, 156, 0.24)" strokeWidth="1" x1={28} x2={width - 24} y1={y} y2={y} />
              </g>
            );
          })}

          <line
            stroke="rgba(115, 128, 132, 0.7)"
            strokeDasharray="7 7"
            strokeWidth="2"
            x1={28}
            x2={width - 28}
            y1={height - 28}
            y2={28}
          />

          {baselinePoints.length ? (
            <path
              d={linePath(baselinePoints)}
              fill="none"
              stroke="rgba(64, 86, 89, 0.55)"
              strokeDasharray="5 5"
              strokeWidth="2.5"
            />
          ) : null}

          {points.length ? (
            <path d={linePath(points)} fill="none" stroke="url(#current-line)" strokeWidth="3.5" />
          ) : null}

          {points.map((point) => (
            <circle
              key={`${point.left}-${point.right}`}
              cx={point.x}
              cy={point.y}
              fill="rgba(23, 120, 128, 0.95)"
              r={Math.max(3, Math.min(8, Math.sqrt(point.count)))}
            />
          ))}
        </svg>
      </div>

      <div className="mt-5 flex flex-wrap gap-4 text-[0.7rem] uppercase tracking-[0.16em] text-muted">
        <span>Dashed diagonal = perfectly calibrated</span>
        <span>Solid line = selected missing-data scenario</span>
        {baselineProfile ? <span>Dashed dark line = available clean reference</span> : null}
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <div className="rounded-[1.25rem] border border-line/80 bg-white/90 p-4">
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Pooled predictions</p>
          <p className="mt-2 text-2xl font-semibold text-ink">{profile?.pooledCount ?? 0}</p>
        </div>
        <div className="rounded-[1.25rem] border border-line/80 bg-white/90 p-4">
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Mean abs gap</p>
          <p className="mt-2 text-2xl font-semibold text-ink">
            {profile ? profile.meanAbsGap.toFixed(3) : "n/a"}
          </p>
        </div>
        <div className="rounded-[1.25rem] border border-line/80 bg-white/90 p-4">
          <p className="text-xs uppercase tracking-[0.16em] text-muted">Max bin gap</p>
          <p className="mt-2 text-2xl font-semibold text-ink">
            {profile ? profile.maxAbsGap.toFixed(3) : "n/a"}
          </p>
        </div>
      </div>
    </article>
  );
}
