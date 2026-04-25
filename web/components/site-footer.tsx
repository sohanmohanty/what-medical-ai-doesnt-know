export function SiteFooter() {
  return (
    <footer className="border-t border-line/70 py-8">
      <div className="page-shell flex flex-col gap-3 text-sm text-muted md:flex-row md:items-center md:justify-between">
        <p>
          Educational clinical ML project about missing data, calibration, and trust.
        </p>
        <p>Not medical advice. Not a diagnostic tool. No personal health data is collected.</p>
      </div>
    </footer>
  );
}
