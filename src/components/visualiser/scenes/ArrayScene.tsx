"use client";

import { motion } from "framer-motion";

type Highlight = "current" | "matched" | "rejected" | "remembered" | "done";

const color: Record<Highlight, string> = {
  current: "var(--current)",
  matched: "var(--matched)",
  rejected: "var(--rejected)",
  remembered: "var(--remembered)",
  done: "var(--matched)",
};

export function ArrayScene({
  values,
  highlights = {},
  pointers = {},
  window,
}: {
  values: unknown[];
  highlights?: Record<string, Highlight | string>;
  pointers?: Record<string, number>;
  window?: { left: number; right: number } | null;
}) {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap justify-center gap-2">
        {values.map((v, i) => {
          const h = highlights[String(i)] as Highlight | undefined;
          const inWindow = window && i >= window.left && i <= window.right;
          return (
            <motion.div
              key={i}
              layout
              initial={{ scale: 0.92, opacity: 0.7 }}
              animate={{
                scale: h === "current" || h === "matched" ? 1.08 : 1,
                opacity: 1,
                y: h === "current" ? -6 : 0,
              }}
              transition={{ type: "spring", stiffness: 320, damping: 22 }}
              className="relative flex h-14 w-14 flex-col items-center justify-center rounded-xl border-2 bg-card text-sm font-semibold"
              style={{
                borderColor: h
                  ? color[h]
                  : inWindow
                    ? "var(--accent)"
                    : "var(--border)",
                background: h
                  ? `color-mix(in oklab, ${color[h]} 28%, transparent)`
                  : undefined,
                boxShadow: h
                  ? `0 10px 24px -14px ${color[h]}`
                  : undefined,
              }}
            >
              <span>{String(v)}</span>
              <span className="absolute -bottom-5 text-[10px] text-muted">
                {i}
              </span>
            </motion.div>
          );
        })}
      </div>
      {Object.keys(pointers).length > 0 && (
        <div className="flex flex-wrap justify-center gap-3 text-xs text-muted">
          {Object.entries(pointers).map(([name, idx]) => (
            <span key={name}>
              <strong className="text-foreground">{name}</strong> → {idx}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
