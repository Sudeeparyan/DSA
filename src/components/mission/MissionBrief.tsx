"use client";

import { useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { Problem } from "@/lib/schema";

export function MissionBrief({
  problem,
  onContinue,
}: {
  problem: Problem;
  onContinue: () => void;
}) {
  const reduce = useReducedMotion();
  const [split, setSplit] = useState(false);
  const [exampleIdx, setExampleIdx] = useState(0);
  const ex = problem.examples[exampleIdx] ?? problem.examples[0];

  return (
    <div className="space-y-8">
      <div className="hangar-panel relative overflow-hidden">
        <div className="blueprint-grid absolute inset-0 opacity-40" />
        <div className="relative p-5 sm:p-8">
          <p className="section-kicker">Mission brief</p>
          <h2 className="brand-font mt-2 text-2xl font-bold sm:text-3xl">
            First: feel the puzzle
          </h2>
          <p className="teach mt-3 max-w-2xl text-muted">
            Tap the capsule. It splits into the kid story and the real ask —
            same idea, two zoom levels.
          </p>

          <button
            type="button"
            onClick={() => setSplit((s) => !s)}
            className="relative mx-auto mt-8 block w-full max-w-xl focus:outline-none"
            aria-expanded={split}
            aria-label={split ? "Collapse puzzle capsule" : "Split puzzle capsule"}
          >
            <AnimatePresence mode="wait">
              {!split ? (
                <motion.div
                  key="closed"
                  layoutId="brief-capsule"
                  className="capsule-closed"
                  initial={reduce ? false : { scale: 0.96, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.9, opacity: 0 }}
                >
                  <motion.div
                    className="capsule-pulse"
                    animate={
                      reduce
                        ? undefined
                        : { scale: [1, 1.04, 1], opacity: [0.45, 0.8, 0.45] }
                    }
                    transition={{ duration: 2.4, repeat: Infinity }}
                  />
                  <div className="brand-font text-xl font-bold sm:text-2xl">
                    {problem.title}
                  </div>
                  <div className="mt-2 text-sm text-panel-fg/70">
                    Tap to split open →
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="open"
                  className="grid gap-3 sm:grid-cols-2"
                  initial={reduce ? false : { opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <motion.div
                    layoutId="brief-story"
                    className="capsule-half"
                    initial={reduce ? false : { x: 40, rotate: -2 }}
                    animate={{ x: 0, rotate: 0 }}
                    transition={{ type: "spring", stiffness: 160, damping: 18 }}
                  >
                    <div className="section-kicker mb-2">Kid story</div>
                    <p className="teach text-base text-panel-fg">
                      {problem.kidExplanation}
                    </p>
                  </motion.div>
                  <motion.div
                    layoutId="brief-real"
                    className="capsule-half capsule-half-accent"
                    initial={reduce ? false : { x: -40, rotate: 2 }}
                    animate={{ x: 0, rotate: 0 }}
                    transition={{ type: "spring", stiffness: 160, damping: 18 }}
                  >
                    <div className="section-kicker mb-2">Real ask</div>
                    <p className="teach text-base text-panel-fg">
                      {problem.plainProblem}
                    </p>
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>
          </button>
        </div>
      </div>

      <div className="hangar-panel p-5 sm:p-7">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="section-kicker">Worked example</p>
            <h3 className="brand-font mt-1 text-xl font-bold">
              Trace one input by hand
            </h3>
          </div>
          <div className="flex gap-2">
            {problem.examples.map((_, i) => (
              <button
                key={i}
                type="button"
                onClick={() => setExampleIdx(i)}
                className={
                  i === exampleIdx
                    ? "signal-btn signal-btn-primary !min-h-10 !px-3 !text-sm"
                    : "signal-btn signal-btn-secondary !min-h-10 !px-3 !text-sm"
                }
              >
                Ex {i + 1}
              </button>
            ))}
          </div>
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={exampleIdx}
            initial={reduce ? false : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="mt-5 grid gap-3 sm:grid-cols-[1.2fr_0.8fr]"
          >
            <div className="example-block">
              <div className="text-xs font-bold uppercase tracking-wider text-accent">
                Input
              </div>
              <code className="mt-2 block font-mono text-sm sm:text-base">
                {ex.input}
              </code>
            </div>
            <div className="example-block example-out">
              <div className="text-xs font-bold uppercase tracking-wider text-accent-2">
                Output
              </div>
              <code className="mt-2 block font-mono text-lg font-bold sm:text-xl">
                {ex.output}
              </code>
            </div>
            {ex.explanation && (
              <p className="teach sm:col-span-2 text-muted">{ex.explanation}</p>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      <div className="flex justify-end">
        <button
          type="button"
          onClick={onContinue}
          className="signal-btn signal-btn-primary"
        >
          Build the idea →
        </button>
      </div>
    </div>
  );
}
