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
  const theater =
    pathname === "/" || pathname?.startsWith("/problem/");

  return (
    <header
      className={clsx(
        "sticky top-0 z-40 border-b backdrop-blur-xl",
        theater
          ? "border-white/10 bg-[#070b09]/85"
          : "border-border/70 bg-background/75",
      )}
    >
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3">
        <Link href="/" className="mr-auto min-w-0">
          <div
            className={clsx(
              "brand-font text-xl font-extrabold tracking-tight sm:text-2xl",
              theater && "text-white",
            )}
          >
            NeetCode<span className="text-accent">150</span>
            <span className="ml-1 text-accent-2">Play</span>
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
                    ? theater
                      ? "bg-white text-[#070b09]"
                      : "bg-ink text-panel-fg"
                    : theater
                      ? "text-white/60 hover:bg-white/10 hover:text-white"
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
            className={clsx(
              "shrink-0 rounded-full border px-3.5 py-1.5 text-sm font-medium",
              theater
                ? "border-white/15 bg-white/5 text-white/70"
                : "border-border bg-card text-muted",
            )}
          >
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
