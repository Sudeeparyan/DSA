"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ProgressRing } from "@/components/ui/ProgressRing";
import { accentFor } from "@/lib/categories";
import {
  countByStatus,
  getLastSlug,
  loadProgress,
} from "@/lib/progress";

interface CatCard {
  slug: string;
  name: string;
  whyItMatters: string;
  problemSlugs: string[];
}

interface ProblemLite {
  slug: string;
  title: string;
  difficulty: string;
  category: string;
}

export function HomeClient({
  categories,
  problems,
}: {
  categories: CatCard[];
  problems: ProblemLite[];
}) {
  const [understood, setUnderstood] = useState(0);
  const [last, setLast] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [catProgress, setCatProgress] = useState<Record<string, number>>({});

  useEffect(() => {
    const slugs = problems.map((p) => p.slug);
    const counts = countByStatus(slugs);
    setUnderstood(counts.understood);
    setLast(getLastSlug());
    const prog = loadProgress();
    const map: Record<string, number> = {};
    for (const c of categories) {
      map[c.slug] = c.problemSlugs.filter(
        (s) => prog[s]?.status === "understood",
      ).length;
    }
    setCatProgress(map);
  }, [categories, problems]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    return problems
      .filter(
        (p) =>
          p.title.toLowerCase().includes(q) ||
          p.slug.includes(q) ||
          p.category.includes(q),
      )
      .slice(0, 8);
  }, [query, problems]);

  const continueProblem = problems.find((p) => p.slug === last);

  return (
    <div className="mx-auto max-w-6xl space-y-10 px-4 py-8">
      <section className="relative overflow-hidden rounded-[2rem] border border-border bg-card px-6 py-10 sm:px-10">
        <div
          className="pointer-events-none absolute inset-0 opacity-70"
          style={{
            background:
              "radial-gradient(600px 280px at 80% 20%, rgba(15,118,110,0.18), transparent), linear-gradient(135deg, rgba(234,179,8,0.08), transparent 40%)",
          }}
        />
        <div className="relative grid items-center gap-8 md:grid-cols-[1.2fr_auto]">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-accent">
              NeetCode 150 Learn
            </p>
            <h1 className="mt-3 max-w-xl text-4xl font-semibold tracking-tight sm:text-5xl">
              DSA stories, animations, and interview-ready Python.
            </h1>
            <p className="mt-4 max-w-lg text-base leading-relaxed text-muted sm:text-lg">
              Built for beginners aiming at Google. Understand the idea before
              the code — then practise on LeetCode.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              {continueProblem ? (
                <Link
                  href={`/problem/${continueProblem.slug}/`}
                  className="inline-flex min-h-12 items-center rounded-2xl bg-accent px-5 font-semibold text-white"
                >
                  Continue: {continueProblem.title}
                </Link>
              ) : (
                <Link
                  href="/problem/contains-duplicate/"
                  className="inline-flex min-h-12 items-center rounded-2xl bg-accent px-5 font-semibold text-white"
                >
                  Start with Contains Duplicate
                </Link>
              )}
              <Link
                href="/roadmap/"
                className="inline-flex min-h-12 items-center rounded-2xl border border-border px-5 font-semibold"
              >
                View roadmap
              </Link>
            </div>
          </div>
          <ProgressRing value={understood} total={150} size={140} />
        </div>
      </section>

      <section className="space-y-3">
        <label htmlFor="home-search" className="text-sm font-semibold">
          Search problems
        </label>
        <input
          id="home-search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Try “two sum” or “stack”"
          className="w-full rounded-2xl border border-border bg-card px-4 py-3 text-base"
        />
        {filtered.length > 0 && (
          <ul className="rounded-2xl border border-border bg-card p-2">
            {filtered.map((p) => (
              <li key={p.slug}>
                <Link
                  href={`/problem/${p.slug}/`}
                  className="block rounded-xl px-3 py-2 hover:bg-accent-soft"
                >
                  {p.title}{" "}
                  <span className="text-sm text-muted">({p.difficulty})</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2 className="mb-4 text-2xl font-semibold">Categories</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((c) => {
            const done = catProgress[c.slug] ?? 0;
            const total = c.problemSlugs.length;
            const pct = total ? (done / total) * 100 : 0;
            const accent = accentFor(c.slug);
            return (
              <Link
                key={c.slug}
                href={`/category/${c.slug}/`}
                className="rounded-3xl border border-border bg-card p-5 transition hover:-translate-y-0.5 hover:shadow-md"
              >
                <div className="text-lg font-semibold" style={{ color: accent }}>
                  {c.name}
                </div>
                <p className="mt-2 line-clamp-3 text-sm leading-relaxed text-muted">
                  {c.whyItMatters}
                </p>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-border">
                  <div
                    className="h-full rounded-full"
                    style={{ width: `${pct}%`, background: accent }}
                  />
                </div>
                <div className="mt-2 text-xs text-muted">
                  {done}/{total} understood
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </div>
  );
}
