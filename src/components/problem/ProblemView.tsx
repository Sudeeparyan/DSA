"use client";

import type { Problem } from "@/lib/schema";
import { DifficultyChip } from "@/components/ui/DifficultyChip";
import { VisualiserEngine } from "@/components/visualiser/VisualiserEngine";
import { CodeTabs } from "./CodeTabs";
import { ProgressControls } from "./ProgressControls";
import { accentFor } from "@/lib/categories";
import Link from "next/link";
import { useEffect } from "react";
import { setLastSlug } from "@/lib/progress";

const TOC = [
  { id: "story", label: "Story" },
  { id: "think", label: "Think" },
  { id: "animation", label: "Animation" },
  { id: "code", label: "Code" },
  { id: "complexity", label: "Complexity" },
  { id: "tips", label: "Tips" },
  { id: "practice", label: "Practise" },
  { id: "status", label: "Status" },
];

export function ProblemView({ problem }: { problem: Problem }) {
  const accent = accentFor(problem.category);

  useEffect(() => {
    setLastSlug(problem.slug);
  }, [problem.slug]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <div
        className="mb-8 overflow-hidden rounded-[2rem] border border-border"
        style={{
          background: `linear-gradient(135deg, color-mix(in oklab, ${accent} 18%, transparent), transparent 55%), var(--card)`,
        }}
      >
        <div className="px-6 py-8 sm:px-10">
          <div className="flex flex-wrap items-center gap-2 text-sm text-muted">
            <Link
              href={`/category/${problem.category}/`}
              className="font-semibold hover:text-foreground"
            >
              {problem.category.replace(/-/g, " ")}
            </Link>
            <span aria-hidden>·</span>
            <span className="font-mono">#{problem.leetcodeNumber}</span>
            <DifficultyChip difficulty={problem.difficulty} />
          </div>
          <h1 className="brand-font mt-3 max-w-3xl text-4xl font-extrabold tracking-tight sm:text-5xl">
            {problem.title}
          </h1>
          <p className="mt-3 max-w-2xl text-muted">
            Pattern:{" "}
            <strong className="text-foreground">{problem.pattern.name}</strong>
            <span className="mx-2 text-border">|</span>
            Spot it when {problem.pattern.whenToSpot.toLowerCase()}
          </p>
        </div>
      </div>

      <div className="grid gap-8 lg:grid-cols-[200px_minmax(0,1fr)]">
        <nav
          aria-label="On this page"
          className="sticky top-24 hidden self-start lg:block"
        >
          <p className="section-kicker mb-3">On this page</p>
          <ul className="space-y-1">
            {TOC.map((item, i) => (
              <li key={item.id}>
                <a
                  href={`#${item.id}`}
                  className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm text-muted hover:bg-accent-soft hover:text-foreground"
                >
                  <span className="font-mono text-[10px] text-accent">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <article className="min-w-0 space-y-12">
          <section id="story" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Story</h2>
            <p className="teach glass rounded-[1.5rem] p-6">{problem.kidExplanation}</p>
            <div className="glass rounded-[1.5rem] p-6">
              <h3 className="mb-2 text-lg font-bold">The real problem</h3>
              <p className="teach text-foreground/90">{problem.plainProblem}</p>
              <div className="mt-5 grid gap-3">
                {problem.examples.map((ex, i) => (
                  <div
                    key={i}
                    className="rounded-2xl border border-border bg-background/50 p-4 text-sm"
                  >
                    <div className="section-kicker mb-2">Example {i + 1}</div>
                    <div>
                      <span className="font-semibold">Input:</span>{" "}
                      <code className="font-mono text-[13px]">{ex.input}</code>
                    </div>
                    <div className="mt-1">
                      <span className="font-semibold">Output:</span>{" "}
                      <code className="font-mono text-[13px]">{ex.output}</code>
                    </div>
                    {ex.explanation && (
                      <p className="mt-2 text-muted">{ex.explanation}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section id="think" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Think it through</h2>
            <ol className="space-y-3">
              {problem.thinkingSteps.map((step, i) => (
                <li key={i} className="glass rounded-[1.5rem] p-5">
                  <div className="mb-1 flex items-center gap-2 text-sm font-bold text-accent">
                    <span className="font-mono">{String(i + 1).padStart(2, "0")}</span>
                    {step.title}
                  </div>
                  <p className="teach">{step.body}</p>
                </li>
              ))}
            </ol>
          </section>

          <section id="animation" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Animation</h2>
            <VisualiserEngine problem={problem} />
          </section>

          <section id="code" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Code</h2>
            <CodeTabs problem={problem} />
          </section>

          <section id="complexity" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Complexity</h2>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="glass rounded-[1.5rem] p-5">
                <div className="section-kicker">Time</div>
                <div className="brand-font mt-1 text-2xl font-bold">
                  {problem.complexity.time}
                </div>
                <p className="teach mt-2 text-base text-muted">
                  {problem.complexity.timeReason}
                </p>
              </div>
              <div className="glass rounded-[1.5rem] p-5">
                <div className="section-kicker">Space</div>
                <div className="brand-font mt-1 text-2xl font-bold">
                  {problem.complexity.space}
                </div>
                <p className="teach mt-2 text-base text-muted">
                  {problem.complexity.spaceReason}
                </p>
              </div>
            </div>
            {problem.interviewApproachNotes && (
              <p className="rounded-[1.25rem] border border-accent/30 bg-accent-soft/70 p-4 text-sm leading-relaxed">
                <strong>Interview note:</strong> {problem.interviewApproachNotes}
              </p>
            )}
          </section>

          <section id="tips" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">
              Edge cases · mistakes · tips
            </h2>
            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["Edge cases", problem.edgeCases],
                ["Common mistakes", problem.commonMistakes],
                ["Say this at Google", problem.interviewTips],
              ].map(([title, items]) => (
                <div key={title as string} className="glass rounded-[1.5rem] p-5">
                  <h3 className="mb-3 font-bold">{title as string}</h3>
                  <ul className="list-disc space-y-2 pl-4 text-sm leading-relaxed">
                    {(items as string[]).map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          <section id="practice" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Video + practise</h2>
            <div className="flex flex-col gap-3 sm:flex-row">
              <a
                href={problem.leetcodeUrl}
                target="_blank"
                rel="noreferrer"
                className="signal-btn signal-btn-primary"
              >
                Practise on LeetCode
              </a>
              {problem.neetcodeVideoUrl ? (
                <a
                  href={problem.neetcodeVideoUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="signal-btn signal-btn-secondary"
                >
                  Watch NeetCode video
                </a>
              ) : (
                <div className="inline-flex min-h-12 items-center rounded-full border border-dashed border-border px-5 text-sm text-muted">
                  Video slot empty — URL not verified yet
                </div>
              )}
            </div>
          </section>

          <section id="status" className="scroll-mt-28 space-y-4">
            <h2 className="brand-font text-3xl font-bold">Your progress</h2>
            <ProgressControls slug={problem.slug} />
          </section>

          {problem.relatedProblems.length > 0 && (
            <section>
              <h2 className="brand-font mb-3 text-2xl font-bold">Related</h2>
              <div className="flex flex-wrap gap-2">
                {problem.relatedProblems.map((slug) => (
                  <Link
                    key={slug}
                    href={`/problem/${slug}/`}
                    className="rounded-full border border-border bg-card px-3 py-1.5 text-sm font-medium hover:border-accent"
                  >
                    {slug}
                  </Link>
                ))}
              </div>
            </section>
          )}
        </article>
      </div>
    </div>
  );
}
