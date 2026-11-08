"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { ProgressRing } from "@/components/ui/ProgressRing";
import { HeroBoard } from "@/components/home/HeroBoard";
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
  const reduce = useReducedMotion();
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
    <div>
      <section className="relative overflow-hidden">
        <div className="mx-auto grid max-w-6xl items-end gap-8 px-4 pb-10 pt-8 lg:grid-cols-[1.05fr_0.95fr] lg:pb-14 lg:pt-12">
          <div>
            <motion.p
              className="section-kicker"
              initial={reduce ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
            >
              Google interview prep
            </motion.p>
            <motion.h1
              className="brand-font mt-4 max-w-xl text-5xl font-extrabold leading-[0.95] tracking-tight sm:text-6xl lg:text-7xl"
              initial={reduce ? false : { opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
            >
              NeetCode
              <span className="text-accent">150</span>
              <span className="block text-accent-2">Learn</span>
            </motion.h1>
            <motion.p
              className="teach mt-5 max-w-md text-lg text-muted"
              initial={reduce ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.12 }}
            >
              Stories, step-by-step animations, and interview-ready Python —
              simple enough for a curious beginner, sharp enough for Google.
            </motion.p>
            <motion.div
              className="mt-7 flex flex-wrap items-center gap-3"
              initial={reduce ? false : { opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.18 }}
            >
              {continueProblem ? (
                <Link
                  href={`/problem/${continueProblem.slug}/`}
                  className="signal-btn signal-btn-primary"
                >
                  Continue · {continueProblem.title}
                </Link>
              ) : (
                <Link
                  href="/problem/contains-duplicate/"
                  className="signal-btn signal-btn-primary"
                >
                  Start · Contains Duplicate
                </Link>
              )}
              <Link href="/roadmap/" className="signal-btn signal-btn-secondary">
                Open roadmap
              </Link>
              <div className="ml-auto hidden sm:block">
                <ProgressRing value={understood} total={150} size={96} />
              </div>
            </motion.div>
          </div>
          <HeroBoard />
        </div>
      </section>

      <div className="mx-auto max-w-6xl space-y-12 px-4 pb-16">
        <section className="space-y-3">
          <label htmlFor="home-search" className="section-kicker">
            Find a problem
          </label>
          <input
            id="home-search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Try “two sum”, “stack”, or “island”"
            className="w-full rounded-2xl border border-border bg-card px-5 py-4 text-base outline-none ring-accent focus:ring-2"
          />
          {filtered.length > 0 && (
            <ul className="glass overflow-hidden rounded-2xl">
              {filtered.map((p) => (
                <li key={p.slug} className="border-b border-border last:border-0">
                  <Link
                    href={`/problem/${p.slug}/`}
                    className="block px-4 py-3 hover:bg-accent-soft"
                  >
                    <span className="font-semibold">{p.title}</span>
                    <span className="ml-2 text-sm text-muted">{p.difficulty}</span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section>
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <p className="section-kicker">Eighteen patterns</p>
              <h2 className="brand-font mt-2 text-3xl font-bold">Categories</h2>
            </div>
            <div className="sm:hidden">
              <ProgressRing value={understood} total={150} size={72} />
            </div>
          </div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {categories.map((c, i) => {
              const done = catProgress[c.slug] ?? 0;
              const total = c.problemSlugs.length;
              const pct = total ? (done / total) * 100 : 0;
              const accent = accentFor(c.slug);
              return (
                <motion.div
                  key={c.slug}
                  initial={reduce ? false : { opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-40px" }}
                  transition={{ delay: Math.min(i * 0.03, 0.3) }}
                >
                  <Link
                    href={`/category/${c.slug}/`}
                    className="group block rounded-[1.4rem] border border-border bg-card/80 p-5 transition hover:-translate-y-0.5 hover:border-transparent"
                    style={{
                      boxShadow: "inset 0 0 0 0 transparent",
                    }}
                  >
                    <div
                      className="mb-3 h-1.5 w-12 rounded-full transition group-hover:w-20"
                      style={{ background: accent }}
                    />
                    <div
                      className="brand-font text-xl font-bold"
                      style={{ color: accent }}
                    >
                      {c.name}
                    </div>
                    <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-muted">
                      {c.whyItMatters}
                    </p>
                    <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-border">
                      <div
                        className="h-full rounded-full"
                        style={{ width: `${pct}%`, background: accent }}
                      />
                    </div>
                    <div className="mt-2 text-xs font-medium text-muted">
                      {done}/{total} understood
                    </div>
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}
