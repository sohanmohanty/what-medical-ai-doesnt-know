import Link from "next/link";

const nav = [
  { href: "/", label: "Home" },
  { href: "/explorer", label: "Explorer" },
  { href: "/methodology", label: "Methodology" },
  { href: "/paper", label: "Paper" },
  { href: "/about", label: "About" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-line/70 bg-[rgba(250,248,243,0.85)] backdrop-blur-xl">
      <div className="page-shell flex flex-col items-start gap-3 py-4 sm:flex-row sm:items-center sm:justify-between sm:gap-6">
        <Link className="flex items-center gap-3 text-sm font-semibold tracking-[0.18em] text-ink" href="/">
          <span className="flex h-11 w-11 items-center justify-center rounded-2xl border border-accent/20 bg-accentSoft text-base text-accent">
            WM
          </span>
          <span className="max-w-[12rem] text-xs leading-5 sm:max-w-none sm:text-sm">
            What Medical AI Doesn&apos;t Know
          </span>
        </Link>

        <nav className="flex w-full flex-wrap items-center gap-1 text-xs text-muted sm:w-auto sm:gap-2 sm:text-sm">
          {nav.map((item) => (
            <Link
              key={item.href}
              className="rounded-full px-3 py-2 transition hover:bg-white hover:text-ink sm:px-4"
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
