"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import dynamic from "next/dynamic";
import type { Lesson, OpsView, Step, VarsView } from "@/lib/lesson";
import { TONE_LEGEND, toneFill } from "@/components/stage3d/theme";
import { CodeLine, CodePanel } from "./CodePanel";
import { Rich } from "./Rich";

const Stage = dynamic(() => import("@/components/stage3d/Stage").then((m) => m.Stage), {
  ssr: false,
  loading: () => <div className="stage-frame stage-loading">Loading the 3D stage…</div>,
});

const SPEEDS = [0.5, 1, 1.5, 2];

/** How long a step stays up during auto-play: longer captions get more time. */
function dwell(step: Step, speed: number): number {
  const ms = Math.min(7000, Math.max(2200, 1300 + step.text.length * 40));
  return ms / speed;
}

function tonesUsed(steps: Step[]): Set<string> {
  const used = new Set<string>();
  const visit = (node: unknown) => {
    if (Array.isArray(node)) node.forEach(visit);
    else if (node && typeof node === "object") {
      for (const [key, value] of Object.entries(node)) {
        if (key === "tone" && typeof value === "string") used.add(value);
        else visit(value);
      }
    }
  };
  for (const step of steps) visit(step.views);
  return used;
}

export function Walkthrough({ lesson }: { lesson: Lesson }) {
  const steps = lesson.steps;
  const last = steps.length - 1;
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [reduced, setReduced] = useState(false);
  const root = useRef<HTMLDivElement>(null);
  const main = useRef<HTMLDivElement>(null);
  // full screen gives the 3D stage the whole screen, which helps most in the busier lessons
  const [canFull, setCanFull] = useState(false);
  const [full, setFull] = useState(false);

  useEffect(() => {
    setCanFull(typeof document !== "undefined" && !!document.fullscreenEnabled);
    const update = () => setFull(!!main.current && document.fullscreenElement === main.current);
    document.addEventListener("fullscreenchange", update);
    return () => document.removeEventListener("fullscreenchange", update);
  }, []);

  const toggleFull = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    else main.current?.requestFullscreen().catch(() => {});
  }, []);

  // a link can open the lesson at a given step: /problem/two-sum/?step=7
  useEffect(() => {
    const wanted = Number(new URLSearchParams(window.location.search).get("step"));
    setIndex(Number.isFinite(wanted) && wanted >= 1 ? Math.min(last, Math.floor(wanted) - 1) : 0);
    setPlaying(false);
  }, [lesson.slug, last]);

  useEffect(() => {
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduced(query.matches);
    update();
    query.addEventListener("change", update);
    return () => query.removeEventListener("change", update);
  }, []);

  const go = useCallback(
    (to: number) => {
      setPlaying(false);
      setIndex(Math.min(last, Math.max(0, to)));
    },
    [last],
  );

  // the play button and the space bar do the same thing: play / pause, or replay from the start
  const togglePlay = useCallback(() => {
    if (index >= last) {
      setIndex(0);
      setPlaying(true);
    } else setPlaying((p) => !p);
  }, [index, last]);

  useEffect(() => {
    if (!playing) return;
    if (index >= last) {
      setPlaying(false);
      return;
    }
    const id = setTimeout(() => setIndex((i) => Math.min(last, i + 1)), dwell(steps[index], speed));
    return () => clearTimeout(id);
  }, [playing, index, last, speed, steps]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target instanceof HTMLElement ? e.target : null;
      // typing in a field, or using the speed menu / step slider, keeps its own keys
      if (el && (el.isContentEditable || el.closest("input, textarea, select"))) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "ArrowRight") {
        e.preventDefault();
        go(index + 1);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(index - 1);
      } else if (e.key === " ") {
        // space on a focused button, link or "More examples" toggle must still press that control
        if (el?.closest("button, a, summary, [role='button']")) return;
        e.preventDefault();
        togglePlay();
      } else if ((e.key === "f" || e.key === "F") && canFull) {
        e.preventDefault();
        toggleFull();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go, index, canFull, toggleFull, togglePlay]);

  const step = steps[Math.min(index, last)];
  const vars = step.views.find((v): v is VarsView => v.t === "vars");
  const ops = step.views.find((v): v is OpsView => v.t === "ops");
  const legend = useMemo(() => {
    const used = tonesUsed(steps);
    return TONE_LEGEND.filter((entry) => used.has(entry.tone));
  }, [steps]);
  // many lessons keep everything on the stage and track no plain variables at all
  const tracksVars = useMemo(
    () => steps.some((s) => s.views.some((v) => v.t === "vars" && v.items.length > 0)),
    [steps],
  );

  return (
    <div ref={root} className="walk">
      <div ref={main} className="walk-main">
        <Stage steps={steps} index={index} reduced={reduced} />

        {legend.length > 0 && (
          <ul className="legend" aria-label="What the colours mean">
            {legend.map((entry) => (
              <li key={entry.tone}>
                <span className="legend-dot" style={{ background: toneFill(entry.tone) }} />
                {entry.label}
              </li>
            ))}
          </ul>
        )}

        <div className="caption" aria-live="polite">
          <div className="caption-step">
            Step {index + 1} of {steps.length}
          </div>
          <p key={index} className="caption-text">
            <Rich text={step.text} />
          </p>
          {/* on narrow screens the code panel sits below the controls, so repeat the running line here */}
          <CodeLine code={lesson.code} line={step.line} />
        </div>

        <div className="controls">
          <button type="button" className="btn" onClick={() => go(index - 1)} disabled={index === 0}>
            ← Back
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => go(index + 1)}
            disabled={index >= last}
          >
            Next step →
          </button>
          <button type="button" className="btn" onClick={togglePlay} aria-pressed={playing}>
            {playing ? "❚❚ Pause" : index >= last ? "↺ Replay" : "▶ Auto-play"}
          </button>
          <label className="speed">
            Speed
            <select value={speed} onChange={(e) => setSpeed(Number(e.target.value))}>
              {SPEEDS.map((s) => (
                <option key={s} value={s}>
                  {s}×
                </option>
              ))}
            </select>
          </label>
          <input
            className="scrub"
            type="range"
            min={0}
            max={last}
            value={index}
            onChange={(e) => go(Number(e.target.value))}
            aria-label="Jump to step"
          />
          {canFull && (
            <button type="button" className="btn" onClick={toggleFull} aria-pressed={full}>
              {full ? "Exit full screen" : "Full screen"}
            </button>
          )}
        </div>
        <p className="keys">
          Keyboard: ← → to step, space to play or pause{canFull ? ", F for full screen" : ""}.
        </p>
      </div>

      <aside className="walk-side">
        {ops && (
          <div className="side-card">
            <h3 className="side-title">Operations</h3>
            <ol className="ops">
              {ops.items.map((op, i) => (
                <li key={i} className={`op op-${op.state}`}>
                  <code>{op.call}</code>
                  {op.ret !== undefined && <span className="op-ret">→ {op.ret}</span>}
                </li>
              ))}
            </ol>
          </div>
        )}

        <div className="side-card side-code">
          <h3 className="side-title">Code</h3>
          <CodePanel code={lesson.code} line={step.line} reduced={reduced} />
        </div>

        {tracksVars && (
          <div className="side-card">
            <h3 className="side-title">Variables</h3>
            {vars && vars.items.length > 0 ? (
              <dl className="vars">
                {vars.items.map((item) => (
                  <div key={item.k} className={item.changed ? "var var-changed" : "var"}>
                    <dt>{item.k}</dt>
                    <dd>{item.v}</dd>
                  </div>
                ))}
              </dl>
            ) : (
              <p className="vars-empty">Nothing to show yet.</p>
            )}
          </div>
        )}
      </aside>
    </div>
  );
}
