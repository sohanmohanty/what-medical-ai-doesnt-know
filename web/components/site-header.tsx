import Link from "next/link";

const nav = [
  { href: "/", label: "Home" },
  { href: "/explorer", label: "Explorer" },
  { href: "/methodology", label: "Methodology" },
  { href: "/about", label: "About" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-line/70 bg-[rgba(250,248,243,0.85)] backdrop-blur-xl">
      <div className="page-shell flex items-center justify-between gap-6 py-4">
        <Link className="flex items-center gap-3 text-sm font-semibold tracking-[0.18em] text-ink" href="/">
          <span className="flex h-11 w-11 items-center justify-center rounded-2xl border border-accent/20 bg-accentSoft text-base text-accent">
            WM
          </span>
          <span className="hidden sm:block">What Medical AI Doesn&apos;t Know</span>
        </Link>

        <nav className="flex items-center gap-2 text-sm text-muted">
          {nav.map((item) => (
            <Link
              key={item.href}
              className="rounded-full px-4 py-2 transition hover:bg-white hover:text-ink"
              href={item.href}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
