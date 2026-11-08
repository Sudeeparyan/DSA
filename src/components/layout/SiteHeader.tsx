import Link from "next/link";
import { ThemeToggle } from "./ThemeToggle";

const links = [
  { href: "/", label: "Home" },
  { href: "/roadmap/", label: "Roadmap" },
  { href: "/patterns/", label: "Patterns" },
  { href: "/revise/", label: "Revise" },
  { href: "/search/", label: "Search" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/80 bg-background/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3">
        <Link href="/" className="mr-auto min-w-0">
          <div className="text-lg font-semibold tracking-tight text-foreground sm:text-xl">
            NeetCode<span className="text-accent">150</span> Learn
          </div>
          <div className="truncate text-xs text-muted">
            Google interview prep · kid-simple explanations
          </div>
        </Link>
        <nav
          aria-label="Main"
          className="hidden items-center gap-1 md:flex"
        >
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="rounded-lg px-3 py-2 text-sm font-medium text-muted hover:bg-accent-soft hover:text-foreground"
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <ThemeToggle />
      </div>
      <nav
        aria-label="Mobile"
        className="flex gap-1 overflow-x-auto border-t border-border px-2 py-2 md:hidden"
      >
        {links.map((l) => (
          <Link
            key={l.href}
            href={l.href}
            className="shrink-0 rounded-full bg-card px-3 py-1.5 text-sm text-muted ring-1 ring-border"
          >
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
