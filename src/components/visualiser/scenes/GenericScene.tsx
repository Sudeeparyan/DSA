"use client";

import { ArrayScene } from "./ArrayScene";
import { HashScene } from "./HashScene";
import { StackScene } from "./StackScene";

export function GenericScene({
  visualType,
  state,
}: {
  visualType: string;
  state: Record<string, unknown>;
}) {
  const highlights = (state.highlights ?? {}) as Record<string, string>;

  if (visualType === "hash") {
    return (
      <HashScene
        nums={(state.nums as unknown[]) ?? []}
        seen={(state.seen as unknown[]) ?? []}
        map={(state.map as Record<string, unknown>) ?? {}}
        highlights={highlights}
      />
    );
  }

  if (visualType === "stack" || visualType === "queue") {
    return (
      <StackScene
        chars={(state.chars as unknown[]) ?? (state.nums as unknown[]) ?? []}
        stack={(state.stack as unknown[]) ?? []}
        highlights={highlights}
      />
    );
  }

  if (visualType === "dp" && Array.isArray(state.table)) {
    const table = state.table as unknown[][];
    return (
      <div className="overflow-x-auto">
        <div className="inline-grid gap-1" style={{ gridTemplateColumns: `repeat(${table[0]?.length ?? 1}, minmax(2.5rem, 1fr))` }}>
          {table.flatMap((row, r) =>
            row.map((cell, c) => (
              <div
                key={`${r}-${c}`}
                className="flex h-10 w-10 items-center justify-center rounded-md border border-border bg-card text-xs font-semibold"
              >
                {String(cell)}
              </div>
            )),
          )}
        </div>
      </div>
    );
  }

  if (visualType === "bits" && Array.isArray(state.bits)) {
    return (
      <div className="flex flex-wrap justify-center gap-1">
        {(state.bits as number[]).map((b, i) => (
          <div
            key={i}
            className="flex h-10 w-10 items-center justify-center rounded-md border-2 font-mono text-sm font-bold"
            style={{
              borderColor: highlights[String(i)] ? "var(--current)" : "var(--border)",
              background: b ? "var(--accent-soft)" : "var(--card)",
            }}
          >
            {b}
          </div>
        ))}
      </div>
    );
  }

  if (visualType === "intervals" && Array.isArray(state.intervals)) {
    const intervals = state.intervals as number[][];
    return (
      <div className="space-y-2">
        {intervals.map((iv, i) => (
          <div key={i} className="relative h-8 rounded-full bg-border/40">
            <div
              className="absolute top-1 h-6 rounded-full bg-accent/70"
              style={{
                left: `${(iv[0] / 20) * 100}%`,
                width: `${(Math.max(1, iv[1] - iv[0]) / 20) * 100}%`,
              }}
            />
          </div>
        ))}
      </div>
    );
  }

  const values =
    (state.nums as unknown[]) ??
    (state.chars as unknown[]) ??
    (Array.isArray(state.input) ? (state.input as unknown[]) : []);

  return (
    <ArrayScene
      values={values}
      highlights={highlights}
      pointers={
        state.currentIndex != null
          ? { i: state.currentIndex as number }
          : undefined
      }
      window={state.window as { left: number; right: number } | undefined}
    />
  );
}
