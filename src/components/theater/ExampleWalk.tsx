"use client";

import { motion, useReducedMotion } from "framer-motion";
import { GenericScene } from "@/components/visualiser/scenes/GenericScene";

export function ExampleWalk({
  input,
  output,
  explanation,
  visualInput,
  visualType,
}: {
  input: string;
  output: string;
  explanation: string;
  visualInput: unknown;
  visualType: string;
}) {
  const reduce = useReducedMotion();
  const nums = Array.isArray(visualInput)
    ? visualInput
    : visualInput &&
        typeof visualInput === "object" &&
        Array.isArray((visualInput as { nums?: unknown[] }).nums)
      ? (visualInput as { nums: unknown[] }).nums
      : [];

  return (
    <div className="mx-auto grid w-full max-w-4xl gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <div className="theater-panel space-y-4 p-5">
        <div className="section-kicker text-[#ffd43b]">Live walkthrough</div>
        <GenericScene
          visualType={visualType}
          state={{
            nums,
            seen: nums.slice(0, Math.max(0, nums.length - 1)),
            highlights: nums.length
              ? { [String(nums.length - 1)]: "matched" }
              : {},
          }}
        />
        <motion.p
          className="teach text-white/75"
          initial={reduce ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {explanation || "Follow the highlights — the answer pops when the pattern hits."}
        </motion.p>
      </div>
      <div className="flex flex-col gap-3">
        <motion.div
          className="theater-panel p-4"
          initial={reduce ? false : { x: 30, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
        >
          <div className="text-xs font-bold uppercase tracking-wider text-accent">
            Input
          </div>
          <code className="mt-2 block font-mono text-sm text-white sm:text-base">
            {input}
          </code>
        </motion.div>
        <motion.div
          className="theater-panel border-[color:var(--accent-2)] p-4"
          initial={reduce ? false : { x: 30, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.15 }}
        >
          <div className="text-xs font-bold uppercase tracking-wider text-accent-2">
            Output
          </div>
          <div className="brand-font mt-2 text-3xl font-bold text-white">
            {output}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
