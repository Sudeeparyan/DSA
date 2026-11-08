"use client";

import { motion, useReducedMotion } from "framer-motion";

export function PuzzleBlocks({
  mode,
  text,
}: {
  mode: "kid" | "real";
  text: string;
}) {
  const reduce = useReducedMotion();
  const kid = mode === "kid";

  return (
    <div className="relative mx-auto flex w-full max-w-3xl flex-col items-center gap-6">
      <div className="flex items-end justify-center gap-3 sm:gap-4">
        {(kid ? ["🧸", "🧩", "🎲", "🧸"] : ["1", "2", "3", "1"]).map((v, i) => (
          <motion.div
            key={`${mode}-${i}`}
            className="puzzle-block"
            initial={reduce ? false : { y: -80, opacity: 0, rotate: -12 }}
            animate={{ y: 0, opacity: 1, rotate: 0 }}
            transition={{ delay: i * 0.12, type: "spring", stiffness: 180 }}
            style={{
              borderColor: i === 3 ? "var(--matched)" : "var(--current)",
              boxShadow:
                i === 3
                  ? "0 0 28px -6px var(--matched)"
                  : "0 0 28px -8px var(--current)",
            }}
          >
            <span className="text-2xl sm:text-3xl">{v}</span>
            <span className="mt-1 text-[10px] uppercase tracking-wider text-white/50">
              {i === 3 ? (kid ? "seen!" : "dup") : "new"}
            </span>
          </motion.div>
        ))}
      </div>

      <motion.div
        className="split-panel"
        initial={reduce ? false : { scaleY: 0.6, opacity: 0 }}
        animate={{ scaleY: 1, opacity: 1 }}
        style={{ originY: 0 }}
      >
        <div className="section-kicker">
          {kid ? "Teacher story mode" : "Interview wording"}
        </div>
        <p className="teach mt-3 text-lg text-white/90 sm:text-xl">{text}</p>
      </motion.div>
    </div>
  );
}
