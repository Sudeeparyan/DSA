"use client";

import { useState } from "react";
import { motion, useReducedMotion, AnimatePresence } from "framer-motion";
import type { Problem } from "@/lib/schema";
import { CodeTabs } from "@/components/problem/CodeTabs";

export function BlueprintStage({
  problem,
  onContinue,
  onBack,
}: {
  problem: Problem;
  onContinue: () => void;
  onBack: () => void;
}) {
  const reduce = useReducedMotion();
  const [reveal, setReveal] = useState(false);
  const lines = problem.solutions.python.split("\n").filter((l) => l.trim());

  return (
    <div className="space-y-8">
      <div className="hangar-panel relative overflow-hidden p-5 sm:p-8">
        <div className="blueprint-grid absolute inset-0 opacity-35" />
        <div className="relative">
          <p className="section-kicker">Blueprint bay</p>
          <h2 className="brand-font mt-2 text-2xl font-bold sm:text-3xl">
            Now read the construction drawing
          </h2>
          <p className="teach mt-3 max-w-2xl text-muted">
            You already built the idea and watched it run. The code is just the
            same story written for the computer.
          </p>

          {!reveal ? (
            <button
              type="button"
              onClick={() => setReveal(true)}
              className="blueprint-sealed mt-8 w-full"
            >
              <motion.div
                className="blueprint-sealed-glow"
                animate={
                  reduce
                    ? undefined
                    : { opacity: [0.3, 0.7, 0.3], scale: [1, 1.03, 1] }
                }
                transition={{ duration: 2.2, repeat: Infinity }}
              />
              <div className="brand-font text-xl font-bold">
                Unseal blueprint
              </div>
              <p className="mt-1 text-sm text-panel-fg/65">
                {lines.length} lines · Python first
              </p>
            </button>
          ) : (
            <motion.div
              initial={reduce ? false : { opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 space-y-4"
            >
              <AnimatePresence>
                <motion.div
                  className="flex flex-wrap gap-2"
                  initial="hidden"
                  animate="show"
                  variants={{
                    show: { transition: { staggerChildren: 0.04 } },
                  }}
                >
                  {lines.slice(0, 8).map((line, i) => (
                    <motion.span
                      key={`${i}-${line.slice(0, 12)}`}
                      variants={{
                        hidden: { opacity: 0, y: 8 },
                        show: { opacity: 1, y: 0 },
                      }}
                      className="rounded-lg border border-accent/30 bg-accent-soft px-2.5 py-1 font-mono text-[11px] text-foreground"
                    >
                      {line.trim().slice(0, 42)}
                      {line.trim().length > 42 ? "…" : ""}
                    </motion.span>
                  ))}
                </motion.div>
              </AnimatePresence>
              <CodeTabs problem={problem} />
            </motion.div>
          )}
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <div className="stat-tile">
          <div className="section-kicker">Time</div>
          <div className="brand-font mt-1 text-3xl font-bold">
            {problem.complexity.time}
          </div>
          <p className="teach mt-2 text-base text-muted">
            {problem.complexity.timeReason}
          </p>
        </div>
        <div className="stat-tile">
          <div className="section-kicker">Space</div>
          <div className="brand-font mt-1 text-3xl font-bold">
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

      <div className="flex flex-wrap justify-between gap-3">
        <button type="button" onClick={onBack} className="signal-btn signal-btn-secondary">
          ← Simulate
        </button>
        <button
          type="button"
          onClick={onContinue}
          disabled={!reveal}
          className="signal-btn signal-btn-primary disabled:opacity-40"
        >
          Flight check →
        </button>
      </div>
    </div>
  );
}
