"use client";

import { motion, useReducedMotion } from "framer-motion";

const cells = [1, 2, 3, 1, 4];
const highlights = ["remembered", "remembered", "current", "matched", "done"] as const;

const colors: Record<(typeof highlights)[number], string> = {
  remembered: "var(--remembered)",
  current: "var(--current)",
  matched: "var(--matched)",
  done: "var(--accent)",
};

export function HeroBoard() {
  const reduce = useReducedMotion();

  return (
    <div
      className="relative isolate min-h-[280px] w-full overflow-hidden rounded-[2rem] bg-panel text-panel-fg sm:min-h-[340px]"
      aria-hidden
    >
      <div
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)",
          backgroundSize: "28px 28px",
        }}
      />
      <motion.div
        className="absolute -left-10 top-8 h-40 w-40 rounded-full bg-accent/30 blur-3xl"
        animate={reduce ? undefined : { x: [0, 30, 0], y: [0, 18, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute -right-8 bottom-0 h-48 w-48 rounded-full bg-accent-2/25 blur-3xl"
        animate={reduce ? undefined : { x: [0, -24, 0], y: [0, -16, 0] }}
        transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
      />

      <div className="relative flex h-full flex-col justify-between p-6 sm:p-8">
        <div className="text-xs font-semibold uppercase tracking-[0.22em] text-white/55">
          Live pattern · hash set
        </div>

        <div className="my-8 flex flex-wrap items-end justify-center gap-3">
          {cells.map((n, i) => (
            <motion.div
              key={`${n}-${i}`}
              initial={reduce ? false : { y: 24, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.12 * i, type: "spring", stiffness: 160 }}
              className="relative flex h-16 w-16 flex-col items-center justify-center rounded-2xl border-2 bg-white/5 text-xl font-bold backdrop-blur"
              style={{ borderColor: colors[highlights[i]] }}
            >
              {n}
              <span className="absolute -bottom-6 text-[10px] font-medium text-white/45">
                {i}
              </span>
            </motion.div>
          ))}
        </div>

        <motion.p
          className="mx-auto max-w-sm text-center text-sm leading-relaxed text-white/75"
          initial={reduce ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          See <span style={{ color: "var(--current)" }}>3</span> — already in
          memory?{" "}
          <span style={{ color: "var(--matched)" }}>Yes → duplicate found</span>
        </motion.p>
      </div>
    </div>
  );
}
