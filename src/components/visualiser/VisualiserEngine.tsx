"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { Problem } from "@/lib/schema";
import { getTracer, runTracer } from "@/lib/tracers";
import { GenericScene } from "./scenes/GenericScene";
import { clsx } from "clsx";

function formatVars(state: Record<string, unknown>): Array<[string, string]> {
  const skip = new Set(["highlights", "nums", "chars", "input"]);
  return Object.entries(state)
    .filter(([k]) => !skip.has(k))
    .map(([k, v]) => [k, typeof v === "string" ? v : JSON.stringify(v)]);
}

function highlightLineIndex(stepLine: number, codeLines: string[]): number {
  // Tracers use 1-based conceptual lines inside the method body; map onto file lines.
  const idx = stepLine - 1;
  if (idx >= 0 && idx < codeLines.length) return idx;
  // Fallback: find first non-empty, non-comment code line near the mark
  for (let i = 0; i < codeLines.length; i++) {
    const t = codeLines[i].trim();
    if (t && !t.startsWith("#") && !t.startsWith('"""')) return Math.min(i + Math.max(0, stepLine - 1), codeLines.length - 1);
  }
  return Math.max(0, Math.min(codeLines.length - 1, stepLine));
}

export function VisualiserEngine({ problem }: { problem: Problem }) {
  const [customRaw, setCustomRaw] = useState(
    JSON.stringify(problem.animation.defaultInput),
  );
  const [input, setInput] = useState(problem.animation.defaultInput);
  const [error, setError] = useState<string | null>(null);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const lineRefs = useRef<Array<HTMLDivElement | null>>([]);

  useEffect(() => {
    setCustomRaw(JSON.stringify(problem.animation.defaultInput));
    setInput(problem.animation.defaultInput);
    setIndex(0);
    setPlaying(false);
    setError(null);
  }, [problem.slug, problem.animation.defaultInput]);

  const steps = useMemo(() => {
    const tracer = getTracer(problem.animation.tracerId);
    if (!tracer || problem.animation.tracerId === "generic-array-scan") {
      // Prefer authored steps for generic fallback unless input is a plain array
      if (
        problem.animation.tracerId === "generic-array-scan" &&
        !Array.isArray(input)
      ) {
        return problem.animation.steps;
      }
    }
    try {
      return runTracer(problem.animation.tracerId, input);
    } catch {
      return problem.animation.steps;
    }
  }, [problem, input]);

  const step = steps[Math.min(index, Math.max(0, steps.length - 1))];
  const codeLines = problem.solutions.python.split("\n");
  const activeLine =
    step != null ? highlightLineIndex(step.line, codeLines) : -1;

  const restart = useCallback(() => {
    setIndex(0);
    setPlaying(false);
  }, []);

  const next = useCallback(() => {
    setIndex((i) => Math.min(steps.length - 1, i + 1));
  }, [steps.length]);

  const prev = useCallback(() => {
    setIndex((i) => Math.max(0, i - 1));
  }, []);

  useEffect(() => {
    if (!playing) return;
    if (index >= steps.length - 1) {
      setPlaying(false);
      return;
    }
    const t = setTimeout(() => next(), 1100 / speed);
    return () => clearTimeout(t);
  }, [playing, index, next, speed, steps.length]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement | null)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      if (e.key === "ArrowRight") next();
      if (e.key === "ArrowLeft") prev();
      if (e.key === " ") {
        e.preventDefault();
        setPlaying((p) => !p);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [next, prev]);

  useEffect(() => {
    lineRefs.current[activeLine]?.scrollIntoView({
      block: "nearest",
      behavior: "smooth",
    });
  }, [activeLine]);

  function applyInput() {
    try {
      const parsed = JSON.parse(customRaw);
      setInput(parsed);
      setError(null);
      setIndex(0);
      setPlaying(false);
    } catch {
      setError(
        'Input must be valid JSON (e.g. [1,2,3] or {"nums":[2,7],"target":9}).',
      );
    }
  }

  const vars = formatVars(step?.state ?? {});

  return (
    <div className="space-y-4 rounded-[1.75rem] border border-border bg-card p-4 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-center gap-2">
        {[
          {
            label: playing ? "Pause" : "Play",
            onClick: () => setPlaying((p) => !p),
            primary: true,
          },
          { label: "Prev", onClick: prev },
          { label: "Next", onClick: next },
          { label: "Restart", onClick: restart },
        ].map((b) => (
          <button
            key={b.label}
            type="button"
            onClick={b.onClick}
            className={clsx(
              "min-h-11 rounded-full px-4 text-sm font-bold",
              b.primary
                ? "bg-ink text-panel-fg"
                : "border border-border bg-background",
            )}
            aria-label={b.label}
          >
            {b.label}
          </button>
        ))}
        <label className="ml-auto flex items-center gap-2 text-sm text-muted">
          Speed
          <input
            type="range"
            min={0.5}
            max={3}
            step={0.5}
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            aria-label="Animation speed"
          />
        </label>
      </div>

      <input
        type="range"
        min={0}
        max={Math.max(0, steps.length - 1)}
        value={index}
        onChange={(e) => {
          setPlaying(false);
          setIndex(Number(e.target.value));
        }}
        className="w-full accent-[var(--accent)]"
        aria-label="Step scrubber"
      />
      <div className="text-xs font-medium text-muted">
        Step {steps.length ? index + 1 : 0} / {steps.length} · arrows to step ·
        space to play
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <pre
          className="max-h-80 overflow-auto rounded-2xl bg-panel p-3 font-mono text-xs leading-6 text-panel-fg sm:text-sm"
          tabIndex={0}
          aria-label="Solution code with current line highlighted"
        >
          {codeLines.map((line, i) => (
            <div
              key={i}
              ref={(el) => {
                lineRefs.current[i] = el;
              }}
              className={clsx(
                "rounded-md px-2",
                i === activeLine ? "bg-[color:var(--current)]/30" : undefined,
              )}
            >
              <span className="mr-3 inline-block w-6 text-white/35">{i + 1}</span>
              {line || " "}
            </div>
          ))}
        </pre>

        <div className="space-y-4">
          <div className="min-h-44 rounded-2xl border border-border bg-background/70 p-4">
            <GenericScene
              visualType={problem.animation.visualType}
              state={step?.state ?? {}}
            />
          </div>
          <p className="teach rounded-2xl bg-accent-soft px-4 py-3 text-base">
            {step?.caption ?? "No steps yet."}
          </p>
          <div className="rounded-2xl border border-border p-3">
            <div className="mb-2 text-xs font-bold uppercase tracking-wide text-muted">
              Variables
            </div>
            <dl className="grid gap-1.5 text-sm">
              {vars.length === 0 && (
                <span className="text-muted">Waiting for the first step…</span>
              )}
              {vars.map(([k, v]) => (
                <div key={k} className="flex gap-2">
                  <dt className="shrink-0 font-mono font-semibold text-accent">
                    {k}
                  </dt>
                  <dd className="font-mono break-all text-foreground">{v}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>

      <div className="space-y-2 border-t border-border pt-4">
        <label className="block text-sm font-semibold" htmlFor="custom-input">
          Try your own input (JSON, keep it small)
        </label>
        <div className="flex flex-col gap-2 sm:flex-row">
          <input
            id="custom-input"
            value={customRaw}
            onChange={(e) => setCustomRaw(e.target.value.slice(0, 500))}
            className="w-full rounded-xl border border-border bg-background px-3 py-2.5 font-mono text-sm"
          />
          <button
            type="button"
            className="min-h-11 rounded-full bg-accent px-5 text-sm font-bold text-white"
            onClick={applyInput}
          >
            Re-run
          </button>
        </div>
        {error && <p className="text-sm text-rejected">{error}</p>}
      </div>
    </div>
  );
}
