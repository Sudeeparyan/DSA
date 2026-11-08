"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import {
  countByStatus,
  getLastSlug,
  loadProgress,
} from "@/lib/progress";
import { accentFor } from "@/lib/categories";

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

const DEMO_BEATS = [
  {
    say: "You get a list of numbers. Is any value repeated?",
    cells: [
      { v: "1", t: "scan" },
      { v: "2", t: "scan" },
      { v: "3", t: "check" },
      { v: "1", t: "hit" },
    ],
  },
  {
    say: "Keep a memory shelf. If you already saw it — true.",
    cells: [
      { v: "1", t: "mem" },
      { v: "2", t: "mem" },
      { v: "3", t: "mem" },
      { v: "1", t: "hit" },
    ],
  },
  {
    say: "That's a hash set. One pass. Interview-ready.",
    cells: [
      { v: "✓", t: "done" },
      { v: "O(n)", t: "time" },
      { v: "set", t: "gear" },
      { v: "go", t: "play" },
    ],
  },
];

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
  const [beat, setBeat] = useState(0);
  const [query, setQuery] = useState("");
  const [catProgress, setCatProgress] = useState<Record<string, number>>({});

  useEffect(() => {
    const slugs = problems.map((p) => p.slug);
    setUnderstood(countByStatus(slugs).understood);
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

  useEffect(() => {
    if (reduce) return;
    const t = setInterval(() => setBeat((b) => (b + 1) % DEMO_BEATS.length), 3200);
    return () => clearInterval(t);
  }, [reduce]);

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
  const demo = DEMO_BEATS[beat];

  return (
    <div className="theater-root !min-h-0">
      <div className="theater-sky" aria-hidden />

      <section className="relative z-10 mx-auto grid max-w-6xl gap-10 px-4 pb-10 pt-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:pt-14">
        <div>
          <motion.p
            className="section-kicker text-[#ffd43b]"
            initial={reduce ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
          >
            Teacher theater · Google prep
          </motion.p>
          <motion.h1
            className="brand-font mt-4 text-5xl font-extrabold leading-[0.95] tracking-tight text-white sm:text-6xl lg:text-7xl"
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
          >
            Learn by
            <span className="block text-accent">playing</span>
            <span className="block text-accent-2">the lesson</span>
          </motion.h1>
          <motion.p
            className="teach mt-5 max-w-md text-lg text-white/70"
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            Every NeetCode 150 problem is a continuous animated class: the
            puzzle appears, a rocket idea explodes into parts, the algorithm
            runs like a game, then the blueprint unseals.
          </motion.p>
          <motion.div
            className="mt-8 flex flex-wrap gap-3"
            initial={reduce ? false : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.16 }}
          >
            <Link
              href={
                continueProblem
                  ? `/problem/${continueProblem.slug}/`
                  : "/problem/contains-duplicate/"
              }
              className="signal-btn signal-btn-primary"
            >
              {continueProblem
                ? `Play · ${continueProblem.title}`
                : "Play lesson 1 · Contains Duplicate"}
            </Link>
            <Link
              href="/roadmap/"
              className="signal-btn signal-btn-secondary !border-white/25 !text-white"
            >
              All 150 map
            </Link>
            <div className="flex items-center gap-2 text-sm text-white/50">
              <span className="font-mono text-white">{understood}</span>/150 cleared
            </div>
          </motion.div>
        </div>

        <div className="home-demo-stage">
          <div className="mb-4 flex items-center justify-between text-[11px] font-bold uppercase tracking-[0.2em] text-white/45">
            <span>Live demo · contains duplicate</span>
            <span className="text-matched">auto-play</span>
          </div>
          <AnimatePresence mode="wait">
            <motion.div
              key={beat}
              initial={reduce ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="space-y-6"
            >
              <div className="flex flex-wrap justify-center gap-3">
                {demo.cells.map((c, i) => (
                  <motion.div
                    key={`${beat}-${i}`}
                    className="puzzle-block !h-16 !w-16 sm:!h-20 sm:!w-20"
                    initial={reduce ? false : { y: 24, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: i * 0.08 }}
                    style={{
                      borderColor:
                        c.t === "hit" || c.t === "done"
                          ? "var(--matched)"
                          : c.t === "check"
                            ? "var(--current)"
                            : "var(--accent)",
                    }}
                  >
                    <span className="text-xl font-bold sm:text-2xl">{c.v}</span>
                    <span className="text-[10px] uppercase tracking-wide text-white/45">
                      {c.t}
                    </span>
                  </motion.div>
                ))}
              </div>
              <p className="teach text-center text-base text-white/80 sm:text-lg">
                {demo.say}
              </p>
            </motion.div>
          </AnimatePresence>
          <div className="mt-6 flex justify-center gap-1.5">
            {DEMO_BEATS.map((_, i) => (
              <button
                key={i}
                type="button"
                aria-label={`Demo beat ${i + 1}`}
                onClick={() => setBeat(i)}
                className={clsxDot(i === beat)}
              />
            ))}
          </div>
        </div>
      </section>

      <div className="relative z-10 border-t border-white/10 bg-[#070b09]/70">
        <div className="mx-auto max-w-6xl space-y-10 px-4 py-12">
          <section className="space-y-3">
            <label htmlFor="home-search" className="section-kicker text-[#ffd43b]">
              Jump to a lesson
            </label>
            <input
              id="home-search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Try “two sum”, “stack”, or “island”"
              className="w-full rounded-2xl border border-white/15 bg-white/5 px-5 py-4 text-base text-white outline-none ring-accent placeholder:text-white/35 focus:ring-2"
            />
            {filtered.length > 0 && (
              <ul className="overflow-hidden rounded-2xl border border-white/10 bg-[#0d1512]">
                {filtered.map((p) => (
                  <li key={p.slug} className="border-b border-white/10 last:border-0">
                    <Link
                      href={`/problem/${p.slug}/`}
                      className="block px-4 py-3 text-white/85 hover:bg-white/5"
                    >
                      <span className="font-semibold">{p.title}</span>
                      <span className="ml-2 text-sm text-white/45">
                        {p.difficulty}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section>
            <p className="section-kicker text-[#ffd43b]">Pattern sectors</p>
            <h2 className="brand-font mt-2 text-3xl font-bold text-white">
              Pick a hangar
            </h2>
            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {categories.map((c) => {
                const done = catProgress[c.slug] ?? 0;
                const total = c.problemSlugs.length;
                const pct = total ? (done / total) * 100 : 0;
                const accent = accentFor(c.slug);
                return (
                  <Link
                    key={c.slug}
                    href={`/category/${c.slug}/`}
                    className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 transition hover:border-white/25 hover:bg-white/[0.06]"
                  >
                    <div
                      className="mb-3 h-1.5 w-10 rounded-full"
                      style={{ background: accent }}
                    />
                    <div className="brand-font text-xl font-bold" style={{ color: accent }}>
                      {c.name}
                    </div>
                    <p className="mt-2 line-clamp-2 text-sm text-white/55">
                      {c.whyItMatters}
                    </p>
                    <div className="mt-4 h-1 overflow-hidden rounded-full bg-white/10">
                      <div
                        className="h-full rounded-full"
                        style={{ width: `${pct}%`, background: accent }}
                      />
                    </div>
                  </Link>
                );
              })}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

function clsxDot(on: boolean) {
  return `h-2 w-2 rounded-full ${on ? "bg-accent" : "bg-white/25"}`;
}
