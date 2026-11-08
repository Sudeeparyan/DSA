"use client";

import { motion, useReducedMotion } from "framer-motion";
import type { Problem } from "@/lib/schema";
import { ProgressControls } from "@/components/problem/ProgressControls";
import Link from "next/link";

export function FlightCheck({
  problem,
  onBack,
}: {
  problem: Problem;
  onBack: () => void;
}) {
  const reduce = useReducedMotion();
  const panels = [
    { title: "Edge cases", items: problem.edgeCases, tone: "edge" },
    { title: "Common mistakes", items: problem.commonMistakes, tone: "warn" },
    { title: "Say this at Google", items: problem.interviewTips, tone: "tip" },
  ] as const;

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <p className="section-kicker">Pre-flight</p>
        <h2 className="brand-font text-2xl font-bold sm:text-3xl">
          Check the traps, then mark the mission
        </h2>
        <p className="teach max-w-2xl text-muted">
          Interviewers love edge cases. Read these out loud once, then lock in
          your status.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {panels.map((panel, i) => (
          <motion.div
            key={panel.title}
            className={`check-panel check-panel-${panel.tone}`}
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
          >
            <h3 className="brand-font text-lg font-bold">{panel.title}</h3>
            <ul className="mt-3 space-y-2.5">
              {panel.items.map((item, j) => (
                <motion.li
                  key={item}
                  className="flex gap-2 text-sm leading-relaxed"
                  initial={reduce ? false : { opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.12 + i * 0.08 + j * 0.04 }}
                >
                  <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-current opacity-60" />
                  <span>{item}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>

      <div className="hangar-panel p-5 sm:p-7">
        <p className="section-kicker">Mission status</p>
        <h3 className="brand-font mt-1 text-xl font-bold">How did it go?</h3>
        <div className="mt-4">
          <ProgressControls slug={problem.slug} />
        </div>
      </div>

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
        ) : null}
        <Link href="/roadmap/" className="signal-btn signal-btn-secondary">
          Back to roadmap
        </Link>
      </div>

      {problem.relatedProblems.length > 0 && (
        <div>
          <h3 className="brand-font mb-3 text-xl font-bold">Next missions</h3>
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
        </div>
      )}

      <div className="flex justify-start">
        <button type="button" onClick={onBack} className="signal-btn signal-btn-secondary">
          ← Blueprint
        </button>
      </div>
    </div>
  );
}
