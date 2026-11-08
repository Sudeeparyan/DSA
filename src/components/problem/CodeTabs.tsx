"use client";

import { useState } from "react";
import type { Problem } from "@/lib/schema";
import { clsx } from "clsx";

export function CodeTabs({ problem }: { problem: Problem }) {
  const tabs = [
    { id: "python", label: "Python", code: problem.solutions.python },
    {
      id: "cpp",
      label: "C++",
      code: problem.solutions.cpp,
    },
    {
      id: "rust",
      label: "Rust",
      code: problem.solutions.rust,
    },
  ] as const;
  const [active, setActive] = useState<(typeof tabs)[number]["id"]>("python");
  const current = tabs.find((t) => t.id === active)!;

  async function copy() {
    if (!current.code) return;
    await navigator.clipboard.writeText(current.code);
  }

  return (
    <div className="rounded-3xl border border-border bg-card p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setActive(t.id)}
            className={clsx(
              "min-h-10 rounded-xl px-3 py-1.5 text-sm font-semibold",
              active === t.id
                ? "bg-accent text-white"
                : "border border-border bg-background text-muted",
            )}
          >
            {t.label}
          </button>
        ))}
        <button
          type="button"
          onClick={copy}
          className="ml-auto min-h-10 rounded-xl border border-border px-3 text-sm font-medium"
          disabled={!current.code}
        >
          Copy
        </button>
      </div>
      {current.code ? (
        <pre className="overflow-x-auto rounded-2xl bg-[#0f172a] p-4 font-mono text-xs leading-6 text-slate-100 sm:text-sm">
          <code>{current.code}</code>
        </pre>
      ) : (
        <p className="rounded-2xl border border-dashed border-border bg-background/50 p-4 text-sm text-muted">
          No {current.label} solution in the source repo yet. Python is the
          primary language for this site.
        </p>
      )}
    </div>
  );
}
