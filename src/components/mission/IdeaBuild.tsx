"use client";

import { useMemo, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { Problem } from "@/lib/schema";
import { clsx } from "clsx";

/** Visual “rocket parts” that dock into a working idea. */
const PART_SHAPES = ["nose", "tank", "engine", "fin", "core"] as const;

export function IdeaBuild({
  problem,
  onContinue,
  onBack,
}: {
  problem: Problem;
  onContinue: () => void;
  onBack: () => void;
}) {
  const reduce = useReducedMotion();
  const steps = problem.thinkingSteps;
  const [docked, setDocked] = useState(0);
  const [exploded, setExploded] = useState<number | null>(null);
  const complete = docked >= steps.length;

  const parts = useMemo(
    () =>
      steps.map((step, i) => ({
        ...step,
        shape: PART_SHAPES[i % PART_SHAPES.length],
        hue: 160 + i * 28,
      })),
    [steps],
  );

  function dockNext() {
    if (docked < steps.length) {
      setExploded(null);
      setDocked((d) => d + 1);
    }
  }

  function undock() {
    setExploded(null);
    setDocked((d) => Math.max(0, d - 1));
  }

  return (
    <div className="space-y-8">
      <div className="hangar-panel relative overflow-hidden p-5 sm:p-8">
        <div className="blueprint-grid absolute inset-0 opacity-30" />
        <div className="relative">
          <p className="section-kicker">Idea hangar</p>
          <h2 className="brand-font mt-2 text-2xl font-bold sm:text-3xl">
            Build the answer like a rocket
          </h2>
          <p className="teach mt-3 max-w-2xl text-muted">
            Each thinking step is a part. Dock them in order. Tap a docked part
            to explode it open and read the detail — then snap it back.
          </p>

          <div className="mt-8 grid gap-8 lg:grid-cols-[1fr_280px]">
            <div className="rocket-bay">
              <AnimatePresence>
                {parts.slice(0, docked).map((part, i) => {
                  const open = exploded === i;
                  return (
                    <motion.button
                      key={part.title}
                      type="button"
                      layout
                      onClick={() => setExploded(open ? null : i)}
                      className={clsx(
                        "rocket-part",
                        `rocket-part-${part.shape}`,
                        open && "rocket-part-open",
                      )}
                      initial={
                        reduce
                          ? false
                          : { opacity: 0, y: 80, scale: 0.7, rotate: -8 }
                      }
                      animate={{
                        opacity: 1,
                        y: 0,
                        scale: open ? 1.02 : 1,
                        rotate: 0,
                      }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      transition={{ type: "spring", stiffness: 140, damping: 16 }}
                      style={{
                        borderColor: `oklch(0.72 0.14 ${part.hue})`,
                        boxShadow: open
                          ? `0 0 0 1px oklch(0.72 0.14 ${part.hue} / 0.5), 0 18px 40px -20px oklch(0.5 0.1 ${part.hue} / 0.55)`
                          : undefined,
                      }}
                    >
                      <div className="flex items-start gap-3">
                        <span
                          className="rocket-part-badge"
                          style={{
                            background: `oklch(0.72 0.14 ${part.hue})`,
                          }}
                        >
                          {i + 1}
                        </span>
                        <div className="min-w-0 text-left">
                          <div className="brand-font text-lg font-bold">
                            {part.title}
                          </div>
                          <AnimatePresence>
                            {open ? (
                              <motion.p
                                className="teach mt-2 text-base text-panel-fg/90"
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: "auto", opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                              >
                                {part.body}
                              </motion.p>
                            ) : (
                              <motion.p
                                className="mt-1 text-sm text-panel-fg/55"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                              >
                                Tap to explode open
                              </motion.p>
                            )}
                          </AnimatePresence>
                        </div>
                      </div>
                    </motion.button>
                  );
                })}
              </AnimatePresence>

              {!complete && (
                <motion.div
                  className="rocket-ghost"
                  animate={
                    reduce
                      ? undefined
                      : { opacity: [0.35, 0.7, 0.35], y: [0, -4, 0] }
                  }
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  Next part ready:{" "}
                  <strong>{parts[docked]?.title ?? "—"}</strong>
                </motion.div>
              )}

              {complete && (
                <motion.div
                  className="rocket-complete"
                  initial={reduce ? false : { scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                >
                  <div className="brand-font text-xl font-bold">
                    Idea assembled ✓
                  </div>
                  <p className="mt-1 text-sm text-panel-fg/70">
                    Pattern: {problem.pattern.name}. Now run it on real data.
                  </p>
                </motion.div>
              )}
            </div>

            <aside className="space-y-3">
              <div className="parts-tray">
                <div className="mb-3 text-xs font-bold uppercase tracking-wider text-muted">
                  Parts tray · {docked}/{steps.length}
                </div>
                {parts.map((part, i) => {
                  const used = i < docked;
                  return (
                    <div
                      key={part.title}
                      className={clsx(
                        "tray-item",
                        used && "tray-item-used",
                        i === docked && "tray-item-next",
                      )}
                    >
                      <span className="font-mono text-[10px]">{i + 1}</span>
                      <span className="truncate">{part.title}</span>
                    </div>
                  );
                })}
              </div>
              <div className="flex flex-col gap-2">
                <button
                  type="button"
                  onClick={dockNext}
                  disabled={complete}
                  className="signal-btn signal-btn-primary w-full disabled:opacity-40"
                >
                  {complete ? "All parts docked" : "Dock next part"}
                </button>
                <button
                  type="button"
                  onClick={undock}
                  disabled={docked === 0}
                  className="signal-btn signal-btn-secondary w-full disabled:opacity-40"
                >
                  Undock last
                </button>
                {docked > 0 && (
                  <button
                    type="button"
                    onClick={() =>
                      setDocked(steps.length)
                    }
                    className="text-sm font-semibold text-accent hover:underline"
                  >
                    Auto-assemble all
                  </button>
                )}
              </div>
            </aside>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap justify-between gap-3">
        <button type="button" onClick={onBack} className="signal-btn signal-btn-secondary">
          ← Brief
        </button>
        <button
          type="button"
          onClick={onContinue}
          disabled={!complete}
          className="signal-btn signal-btn-primary disabled:opacity-40"
        >
          Simulate the machine →
        </button>
      </div>
    </div>
  );
}
