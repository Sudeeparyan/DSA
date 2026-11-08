"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { DifficultyChip } from "@/components/ui/DifficultyChip";
import { getEntry, type ProblemStatus } from "@/lib/progress";
import type { Difficulty } from "@/lib/schema";

interface Item {
  slug: string;
  title: string;
  category: string;
  difficulty: Difficulty;
  pattern: string;
}

export function SearchClient({
  problems,
  categories,
}: {
  problems: Item[];
  categories: { slug: string; name: string }[];
}) {
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("all");
  const [difficulty, setDifficulty] = useState("all");
  const [status, setStatus] = useState("all");
  const [pattern, setPattern] = useState("all");
  const [statusMap, setStatusMap] = useState<Record<string, ProblemStatus>>({});

  useEffect(() => {
    const map: Record<string, ProblemStatus> = {};
    for (const p of problems) map[p.slug] = getEntry(p.slug).status;
    setStatusMap(map);
  }, [problems]);

  const patterns = useMemo(
    () => Array.from(new Set(problems.map((p) => p.pattern))).sort(),
    [problems],
  );

  const filtered = useMemo(() => {
    return problems.filter((p) => {
      if (category !== "all" && p.category !== category) return false;
      if (difficulty !== "all" && p.difficulty !== difficulty) return false;
      if (pattern !== "all" && p.pattern !== pattern) return false;
      if (status !== "all" && (statusMap[p.slug] ?? "not_started") !== status)
        return false;
      if (!q.trim()) return true;
      const needle = q.toLowerCase();
      return (
        p.title.toLowerCase().includes(needle) ||
        p.slug.includes(needle) ||
        p.pattern.toLowerCase().includes(needle)
      );
    });
  }, [problems, q, category, difficulty, status, pattern, statusMap]);

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-8">
      <h1 className="text-4xl font-semibold">Search</h1>
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search title, slug, or pattern"
        className="w-full rounded-2xl border border-border bg-card px-4 py-3"
        aria-label="Search problems"
      />
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <select
          className="rounded-xl border border-border bg-card px-3 py-2"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          aria-label="Filter by category"
        >
          <option value="all">All categories</option>
          {categories.map((c) => (
            <option key={c.slug} value={c.slug}>
              {c.name}
            </option>
          ))}
        </select>
        <select
          className="rounded-xl border border-border bg-card px-3 py-2"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          aria-label="Filter by difficulty"
        >
          <option value="all">All difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>
        <select
          className="rounded-xl border border-border bg-card px-3 py-2"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          aria-label="Filter by status"
        >
          <option value="all">All statuses</option>
          <option value="not_started">Not started</option>
          <option value="learning">Learning</option>
          <option value="understood">Understood</option>
          <option value="need_revision">Need revision</option>
        </select>
        <select
          className="rounded-xl border border-border bg-card px-3 py-2"
          value={pattern}
          onChange={(e) => setPattern(e.target.value)}
          aria-label="Filter by pattern"
        >
          <option value="all">All patterns</option>
          {patterns.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </div>
      <p className="text-sm text-muted">{filtered.length} results</p>
      <ul className="space-y-2">
        {filtered.map((p) => (
          <li key={p.slug}>
            <Link
              href={`/problem/${p.slug}/`}
              className="flex flex-wrap items-center gap-2 rounded-2xl border border-border bg-card px-4 py-3"
            >
              <span className="font-semibold">{p.title}</span>
              <DifficultyChip difficulty={p.difficulty} />
              <span className="text-xs text-muted">{p.pattern}</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
