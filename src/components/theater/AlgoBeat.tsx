"use client";

import { motion, useReducedMotion } from "framer-motion";
import { GenericScene } from "@/components/visualiser/scenes/GenericScene";
import type { AnimationStep } from "@/lib/schema";
import { clsx } from "clsx";

export function AlgoBeat({
  step,
  code,
  visualType,
  stepIndex,
  stepTotal,
}: {
  step: AnimationStep;
  code: string;
  visualType: string;
  stepIndex: number;
  stepTotal: number;
}) {
  const reduce = useReducedMotion();
  const lines = code.split("\n");
  const active = Math.max(0, Math.min(lines.length - 1, step.line - 1));

  return (
    <div className="mx-auto grid w-full max-w-5xl gap-4 lg:grid-cols-2">
      <div className="theater-panel overflow-hidden p-3">
        <div className="mb-2 flex items-center justify-between px-1 text-[11px] font-bold uppercase tracking-wider text-white/45">
          <span>Code radar</span>
          <span>
            beat {stepIndex + 1}/{stepTotal}
          </span>
        </div>
        <pre className="max-h-72 overflow-auto font-mono text-[11px] leading-5 text-white/80 sm:text-xs sm:leading-6">
          {lines.map((line, i) => (
            <div
              key={i}
              className={clsx(
                "rounded px-2",
                i === active && "bg-[color:var(--current)]/35 text-white",
              )}
            >
              <span className="mr-2 inline-block w-5 text-white/30">{i + 1}</span>
              {line || " "}
            </div>
          ))}
        </pre>
      </div>
      <motion.div
        className="theater-panel flex min-h-56 flex-col justify-center p-4"
        key={stepIndex}
        initial={reduce ? false : { scale: 0.97, opacity: 0.6 }}
        animate={{ scale: 1, opacity: 1 }}
      >
        <GenericScene visualType={visualType} state={step.state} />
      </motion.div>
    </div>
  );
}
