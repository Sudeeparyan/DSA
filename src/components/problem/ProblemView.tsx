"use client";

import type { Problem } from "@/lib/schema";
import { DifficultyChip } from "@/components/ui/DifficultyChip";
import { VisualiserEngine } from "@/components/visualiser/VisualiserEngine";
import { CodeTabs } from "./CodeTabs";
import { ProgressControls } from "./ProgressControls";
import { accentFor } from "@/lib/categories";
import Link from "next/link";

export function ProblemView({ problem }: { problem: Problem }) {
  const accent = accentFor(problem.category);

  return (
    <article className="mx-auto max-w-4xl space-y-10 px-4 py-8">
      <header className="space-y-3">
        <div className="flex flex-wrap items-center gap-2 text-sm text-muted">
          <Link href={`/category/${problem.category}/`} className="hover:text-accent">
            {problem.category}
          </Link>
          <span>·</span>
          <span>#{problem.leetcodeNumber}</span>
          <DifficultyChip difficulty={problem.difficulty} />
        </div>
        <h1
          className="text-3xl font-semibold tracking-tight sm:text-4xl"
          style={{ color: accent }}
        >
          {problem.title}
        </h1>
        <p className="text-muted">
          Pattern: <strong className="text-foreground">{problem.pattern.name}</strong>
        </p>
      </header>

      <section id="story" className="space-y-4">
        <h2 className="text-2xl font-semibold">1. Story</h2>
        <div className="prose-kid rounded-3xl border border-border bg-card p-5">
          <p>{problem.kidExplanation}</p>
        </div>
        <div className="rounded-3xl border border-border bg-card p-5">
          <h3 className="mb-2 text-lg font-semibold">The real problem (plain words)</h3>
          <p className="leading-relaxed text-foreground/90">{problem.plainProblem}</p>
          <div className="mt-4 space-y-3">
            {problem.examples.map((ex, i) => (
              <div key={i} className="rounded-2xl bg-background/70 p-3 text-sm">
                <div>
                  <span className="font-semibold">Example {i + 1} input:</span>{" "}
                  <code className="font-mono">{ex.input}</code>
                </div>
                <div>
                  <span className="font-semibold">Output:</span>{" "}
                  <code className="font-mono">{ex.output}</code>
                </div>
                {ex.explanation && (
                  <p className="mt-1 text-muted">{ex.explanation}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="think" className="space-y-4">
        <h2 className="text-2xl font-semibold">2. Think it through</h2>
        <ol className="space-y-3">
          {problem.thinkingSteps.map((step, i) => (
            <li key={i} className="rounded-3xl border border-border bg-card p-5">
              <div className="mb-1 text-sm font-semibold text-accent">
                Step {i + 1}: {step.title}
              </div>
              <p className="leading-relaxed">{step.body}</p>
            </li>
          ))}
        </ol>
        <p className="text-sm text-muted">
          Spot it when: {problem.pattern.whenToSpot}
        </p>
      </section>

      <section id="animation" className="space-y-4">
        <h2 className="text-2xl font-semibold">3. Animation</h2>
        <VisualiserEngine problem={problem} />
      </section>

      <section id="code" className="space-y-4">
        <h2 className="text-2xl font-semibold">4. Code</h2>
        <CodeTabs problem={problem} />
      </section>

      <section id="complexity" className="space-y-4">
        <h2 className="text-2xl font-semibold">5. Complexity (plain English)</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <div className="rounded-3xl border border-border bg-card p-5">
            <div className="text-sm text-muted">Time</div>
            <div className="text-xl font-semibold">{problem.complexity.time}</div>
            <p className="mt-2 text-sm leading-relaxed">{problem.complexity.timeReason}</p>
          </div>
          <div className="rounded-3xl border border-border bg-card p-5">
            <div className="text-sm text-muted">Space</div>
            <div className="text-xl font-semibold">{problem.complexity.space}</div>
            <p className="mt-2 text-sm leading-relaxed">{problem.complexity.spaceReason}</p>
          </div>
        </div>
        {problem.interviewApproachNotes && (
          <p className="rounded-2xl bg-accent-soft/50 p-4 text-sm leading-relaxed">
            <strong>Interview note:</strong> {problem.interviewApproachNotes}
          </p>
        )}
      </section>

      <section id="tips" className="space-y-4">
        <h2 className="text-2xl font-semibold">6. Edge cases, mistakes, tips</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {[
            ["Edge cases", problem.edgeCases],
            ["Common mistakes", problem.commonMistakes],
            ["Say this at Google", problem.interviewTips],
          ].map(([title, items]) => (
            <div key={title as string} className="rounded-3xl border border-border bg-card p-5">
              <h3 className="mb-2 font-semibold">{title as string}</h3>
              <ul className="list-disc space-y-2 pl-4 text-sm leading-relaxed">
                {(items as string[]).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <section id="practice" className="space-y-4">
        <h2 className="text-2xl font-semibold">7. Video + practise</h2>
        <div className="flex flex-col gap-3 sm:flex-row">
          <a
            href={problem.leetcodeUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex min-h-12 items-center justify-center rounded-2xl bg-accent px-5 font-semibold text-white"
          >
            Practise on LeetCode
          </a>
          {problem.neetcodeVideoUrl ? (
            <a
              href={problem.neetcodeVideoUrl}
              target="_blank"
              rel="noreferrer"
              className="inline-flex min-h-12 items-center justify-center rounded-2xl border border-border px-5 font-semibold"
            >
              Watch NeetCode video
            </a>
          ) : (
            <div className="inline-flex min-h-12 items-center rounded-2xl border border-dashed border-border px-5 text-sm text-muted">
              Video slot empty — URL not verified yet (we never invent links)
            </div>
          )}
        </div>
      </section>

      <section id="status" className="space-y-4">
        <h2 className="text-2xl font-semibold">8. Your progress</h2>
        <ProgressControls slug={problem.slug} />
      </section>

      {problem.relatedProblems.length > 0 && (
        <section>
          <h2 className="mb-3 text-xl font-semibold">Related</h2>
          <div className="flex flex-wrap gap-2">
            {problem.relatedProblems.map((slug) => (
              <Link
                key={slug}
                href={`/problem/${slug}/`}
                className="rounded-full border border-border bg-card px-3 py-1.5 text-sm"
              >
                {slug}
              </Link>
            ))}
          </div>
        </section>
      )}
    </article>
  );
}
