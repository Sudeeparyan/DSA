"use client";

import { motion, AnimatePresence } from "framer-motion";
import { ArrayScene } from "./ArrayScene";

export function StackScene({
  chars = [],
  stack = [],
  highlights = {},
}: {
  chars?: unknown[];
  stack?: unknown[];
  highlights?: Record<string, string>;
}) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div>
        <div className="mb-2 text-center text-sm text-muted">Input</div>
        <ArrayScene values={chars} highlights={highlights} />
      </div>
      <div>
        <div className="mb-2 text-center text-sm text-muted">Stack (top is right)</div>
        <div className="flex min-h-24 flex-wrap items-end justify-center gap-2 rounded-2xl border border-border bg-card p-4">
          <AnimatePresence>
            {stack.map((item, i) => (
              <motion.div
                key={`${item}-${i}`}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: -10, opacity: 0 }}
                className="flex h-12 w-12 items-center justify-center rounded-xl bg-accent-soft text-lg font-bold text-accent"
              >
                {String(item)}
              </motion.div>
            ))}
          </AnimatePresence>
          {stack.length === 0 && (
            <span className="text-sm text-muted">Empty pile</span>
          )}
        </div>
      </div>
    </div>
  );
}
