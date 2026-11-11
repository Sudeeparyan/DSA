"use client";

import { motion, useReducedMotion } from "framer-motion";

const beats = [
  { label: "scan", value: "1", tone: "remembered" },
  { label: "scan", value: "2", tone: "remembered" },
  { label: "check", value: "3", tone: "current" },
  { label: "hit!", value: "1", tone: "matched" },
];

const toneColor: Record<string, string> = {
  remembered: "var(--remembered)",
  current: "var(--current)",
  matched: "var(--matched)",
};

export function HeroBoard() {
  const reduce = useReducedMotion();

  return (
    <div
      className="relative isolate min-h-[300px] w-full overflow-hidden rounded-[2rem] bg-panel text-panel-fg sm:min-h-[360px]"
      aria-hidden
    >
      <div className="blueprint-grid absolute inset-0 opacity-50" />
      <motion.div
        className="absolute -left-12 top-6 h-44 w-44 rounded-full bg-accent/25 blur-3xl"
        animate={reduce ? undefined : { x: [0, 28, 0], y: [0, 16, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute -right-10 bottom-0 h-52 w-52 rounded-full bg-accent-2/20 blur-3xl"
        animate={reduce ? undefined : { x: [0, -22, 0], y: [0, -14, 0] }}
        transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
      />

      <div className="relative flex h-full flex-col justify-between p-6 sm:p-8">
        <div className="flex items-center justify-between gap-3">
          <div className="text-xs font-semibold uppercase tracking-[0.22em] text-white/55">
            Live hangar · contains duplicate
          </div>
          <motion.span
            className="rounded-full bg-matched/20 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-matched"
            animate={reduce ? undefined : { opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.6, repeat: Infinity }}
          >
            simulating
          </motion.span>
        </div>

        <div className="my-6 flex flex-col items-center gap-4">
          <div className="flex flex-wrap items-end justify-center gap-3">
            {beats.map((b, i) => (
              <motion.div
                key={`${b.value}-${i}`}
                initial={reduce ? false : { y: 28, opacity: 0, rotate: -6 }}
                animate={{ y: 0, opacity: 1, rotate: 0 }}
                transition={{
                  delay: 0.1 * i,
                  type: "spring",
                  stiffness: 150,
                }}
                className="relative flex h-[4.25rem] w-[4.25rem] flex-col items-center justify-center rounded-2xl border-2 bg-white/5 text-2xl font-bold backdrop-blur"
                style={{ borderColor: toneColor[b.tone] }}
              >
                {b.value}
                <span className="absolute -bottom-5 text-[10px] font-medium uppercase tracking-wide text-white/45">
                  {b.label}
                </span>
              </motion.div>
            ))}
          </div>

          <motion.div
            className="mt-4 flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm"
            initial={reduce ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.55 }}
          >
            <span className="h-2 w-2 rounded-full bg-matched" />
            Memory shelf already held{" "}
            <strong style={{ color: "var(--matched)" }}>1</strong> → duplicate
          </motion.div>
        </div>

        <p className="mx-auto max-w-sm text-center text-sm leading-relaxed text-white/70">
          Missions teach by building: brief → assemble idea → simulate →
          blueprint → launch.
        </p>
      </div>
    </div>
  );
}
