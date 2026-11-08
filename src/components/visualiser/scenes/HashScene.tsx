"use client";

import { motion, AnimatePresence } from "framer-motion";
import { ArrayScene } from "./ArrayScene";

export function HashScene({
  nums = [],
  seen = [],
  map = {},
  highlights = {},
}: {
  nums?: unknown[];
  seen?: unknown[];
  map?: Record<string, unknown>;
  highlights?: Record<string, string>;
}) {
  const shelf =
    Array.isArray(seen) && seen.length
      ? seen
      : Object.entries(map).map(([k, v]) => `${k}→${v}`);

  return (
    <div className="space-y-6">
      <ArrayScene values={nums} highlights={highlights} />
      <div>
        <div className="mb-2 text-center text-sm font-medium text-muted">
          Memory shelf (hash set / map)
        </div>
        <div className="mx-auto flex min-h-16 max-w-lg flex-wrap justify-center gap-2 rounded-2xl border border-dashed border-remembered/50 bg-remembered/5 p-3">
          <AnimatePresence mode="popLayout">
            {shelf.map((item, i) => (
              <motion.div
                key={`${item}-${i}`}
                layout
                initial={{ y: -18, opacity: 0, scale: 0.7, rotate: -8 }}
                animate={{ y: 0, opacity: 1, scale: 1, rotate: 0 }}
                exit={{ opacity: 0, scale: 0.6 }}
                transition={{ type: "spring", stiffness: 260, damping: 18 }}
                className="rounded-lg bg-remembered/15 px-3 py-2 text-sm font-semibold text-remembered shadow-[0_8px_18px_-12px_var(--remembered)]"
              >
                {String(item)}
              </motion.div>
            ))}
          </AnimatePresence>
          {shelf.length === 0 && (
            <span className="text-sm text-muted">Empty shelf — dock values here</span>
          )}
        </div>
      </div>
    </div>
  );
}
