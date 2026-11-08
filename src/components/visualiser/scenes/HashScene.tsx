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
  const shelf = Array.isArray(seen) && seen.length
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
          <AnimatePresence>
            {shelf.map((item, i) => (
              <motion.div
                key={`${item}-${i}`}
                initial={{ y: -12, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ opacity: 0 }}
                className="rounded-lg bg-remembered/15 px-3 py-2 text-sm font-semibold text-remembered"
              >
                {String(item)}
              </motion.div>
            ))}
          </AnimatePresence>
          {shelf.length === 0 && (
            <span className="text-sm text-muted">Empty for now</span>
          )}
        </div>
      </div>
    </div>
  );
}
