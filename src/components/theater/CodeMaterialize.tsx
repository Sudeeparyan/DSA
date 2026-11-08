"use client";

import { motion, useReducedMotion } from "framer-motion";

export function CodeMaterialize({
  code,
  time,
  space,
  timeReason,
  spaceReason,
}: {
  code: string;
  time: string;
  space: string;
  timeReason: string;
  spaceReason: string;
}) {
  const reduce = useReducedMotion();
  const lines = code.split("\n");

  return (
    <div className="mx-auto grid w-full max-w-5xl gap-4 lg:grid-cols-[1.3fr_0.7fr]">
      <div className="theater-panel overflow-hidden p-4">
        <div className="section-kicker text-[#ffd43b]">Blueprint materializing</div>
        <pre className="mt-3 max-h-80 overflow-auto font-mono text-[11px] leading-5 text-white/85 sm:text-sm sm:leading-6">
          {lines.map((line, i) => (
            <motion.div
              key={i}
              initial={reduce ? false : { opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: Math.min(i * 0.04, 1.2) }}
            >
              <span className="mr-3 inline-block w-5 text-white/30">{i + 1}</span>
              {line || " "}
            </motion.div>
          ))}
        </pre>
      </div>
      <div className="space-y-3">
        <motion.div
          className="theater-panel p-4"
          initial={reduce ? false : { y: 16, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="section-kicker">Time</div>
          <div className="brand-font mt-1 text-3xl font-bold text-white">{time}</div>
          <p className="mt-2 text-sm text-white/65">{timeReason}</p>
        </motion.div>
        <motion.div
          className="theater-panel p-4"
          initial={reduce ? false : { y: 16, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.35 }}
        >
          <div className="section-kicker">Space</div>
          <div className="brand-font mt-1 text-3xl font-bold text-white">{space}</div>
          <p className="mt-2 text-sm text-white/65">{spaceReason}</p>
        </motion.div>
      </div>
    </div>
  );
}
