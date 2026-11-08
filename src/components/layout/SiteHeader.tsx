"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ThemeToggle } from "./ThemeToggle";
import { clsx } from "clsx";

const links = [
  { href: "/", label: "Home" },
  { href: "/roadmap/", label: "Roadmap" },
  { href: "/patterns/", label: "Patterns" },
  { href: "/revise/", label: "Revise" },
  { href: "/search/", label: "Search" },
];

export function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-border/70 bg-background/75 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3">
        <Link href="/" className="mr-auto min-w-0">
          <div className="brand-font text-xl font-extrabold tracking-tight sm:text-2xl">
            NeetCode<span className="text-accent">150</span>
            <span className="ml-1 text-accent-2">Learn</span>
          </div>
        </Link>
        <nav aria-label="Main" className="hidden items-center gap-1 md:flex">
          {links.map((l) => {
            const active =
              l.href === "/"
                ? pathname === "/"
                : pathname?.startsWith(l.href.replace(/\/$/, ""));
            return (
              <Link
                key={l.href}
                href={l.href}
                className={clsx(
                  "rounded-full px-3.5 py-2 text-sm font-semibold transition",
                  active
                    ? "bg-ink text-panel-fg"
                    : "text-muted hover:bg-accent-soft hover:text-foreground",
                )}
              >
                {l.label}
              </Link>
            );
          })}
        </nav>
        <ThemeToggle />
      </div>
      <nav
        aria-label="Mobile"
        className="flex gap-1.5 overflow-x-auto px-3 pb-3 md:hidden"
      >
        {links.map((l) => (
          <Link
            key={l.href}
            href={l.href}
            className="shrink-0 rounded-full border border-border bg-card px-3.5 py-1.5 text-sm font-medium text-muted"
          >
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
