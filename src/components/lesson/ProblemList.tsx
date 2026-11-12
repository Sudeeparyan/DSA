"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import type { LessonMeta } from "@/lib/lesson";
import { getLastSlug, loadUnderstood, onProgressChange } from "@/lib/progress";

interface Group {
  slug: string;
  name: string;
  lessons: LessonMeta[];
}

/** Short forms people type, and the words they stand for in titles, topics and patterns. */
const ALIASES: Record<string, string[]> = {
  dp: ["dynamic programming", "dp"],
  bfs: ["bfs", "breadth-first"],
  dfs: ["dfs", "depth-first"],
  bst: ["bst", "binary search tree"],
  ll: ["linked list"],
  pq: ["priority queue", "heap"],
  "1d": ["1-d"],
  "2d": ["2-d", "2d"],
  "&": ["&", "and"],
  and: ["and", "&"],
};

function haystack(lesson: LessonMeta, group: string): string {
  return `${lesson.title} ${group} ${lesson.difficulty} ${lesson.pattern}`.toLowerCase().replace(/&/g, "& and");
}

/** Every word typed must appear somewhere (title, topic, difficulty or pattern); a bare number is a LeetCode number. */
function matches(lesson: LessonMeta, group: string, query: string): boolean {
  const q = query.trim().toLowerCase().replace(/^#/, "");
  if (!q) return true;
  if (/^\d+$/.test(q)) return String(lesson.number) === q;
  const text = haystack(lesson, group);
  return q.split(/\s+/).every((word) => (ALIASES[word] ?? [word]).some((form) => text.includes(form)));
}

/** The home page: every problem, grouped by topic, in the order to study them. */
export function ProblemList({ groups, total }: { groups: Group[]; total: number }) {
  const [query, setQuery] = useState("");
  const [done, setDone] = useState<Set<string>>(new Set());
  const [last, setLast] = useState<string | null>(null);

  useEffect(() => {
    const refresh = () => setDone(loadUnderstood());
    refresh();
    setLast(getLastSlug());
    return onProgressChange(refresh);
  }, []);

  const all = useMemo(() => groups.flatMap((g) => g.lessons), [groups]);
  const resume = all.find((l) => l.slug === last) ?? null;
  const understood = all.filter((l) => done.has(l.slug)).length;

  const shown = useMemo(
    () =>
      groups
        .map((g) => ({ ...g, lessons: g.lessons.filter((l) => matches(l, g.name, query)) }))
        .filter((g) => g.lessons.length > 0),
    [groups, query],
  );
  const found = shown.reduce((n, g) => n + g.lessons.length, 0);

  return (
    <div className="home">
      <header className="home-head">
        <h1>Understand the NeetCode 150</h1>
        <p>
          Pick a problem. You get the question in plain words, the idea that solves it, and a 3D
          walkthrough of the real solution running one line at a time.
        </p>
        <div className="home-actions">
          <Link
            href={`/problem/${(resume ?? all[0])?.slug ?? ""}/`}
            className="btn btn-primary"
            aria-disabled={all.length === 0}
          >
            {resume ? `Continue: ${resume.title}` : "Start with the first problem"}
          </Link>
          <div className="home-progress" aria-label={`${understood} of ${total} understood`}>
            <div className="home-progress-bar">
              <span style={{ width: `${total ? (understood / total) * 100 : 0}%` }} />
            </div>
            <span>
              {understood} of {total} understood
            </span>
          </div>
        </div>
        <input
          className="home-search"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Find a problem or pattern"
          aria-label="Find a problem by name, LeetCode number, topic, difficulty or pattern"
        />
        {query.trim() && found > 0 && (
          <p className="home-found" aria-live="polite">
            {found} {found === 1 ? "problem matches" : "problems match"}
          </p>
        )}
      </header>

      {shown.length === 0 && (
        <p className="home-none" aria-live="polite">
          No problem matches “{query}”. Try a name (two sum), a topic (graphs), a pattern (sliding window) or a
          difficulty (hard).
        </p>
      )}

      {shown.map((group) => (
        <section key={group.slug} className="home-group" aria-labelledby={`g-${group.slug}`}>
          <h2 id={`g-${group.slug}`}>
            {group.name}
            <span>
              {group.lessons.filter((l) => done.has(l.slug)).length}/{group.lessons.length}
            </span>
          </h2>
          <ul>
            {group.lessons.map((lesson) => (
              <li key={lesson.slug}>
                <Link href={`/problem/${lesson.slug}/`} className="home-item">
                  <span
                    className={done.has(lesson.slug) ? "home-tick home-tick-on" : "home-tick"}
                    aria-label={done.has(lesson.slug) ? "understood" : undefined}
                  >
                    {done.has(lesson.slug) ? "✓" : ""}
                  </span>
                  <span className="home-item-title">{lesson.title}</span>
                  <span className={`diff diff-${lesson.difficulty.toLowerCase()}`}>
                    {lesson.difficulty}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}
