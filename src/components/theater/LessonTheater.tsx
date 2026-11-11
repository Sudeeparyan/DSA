"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import Link from "next/link";
import type { Problem } from "@/lib/schema";
import { buildLessonScript, type TeachBeat } from "@/lib/lessonScript";
import { setLastSlug } from "@/lib/progress";
import { DifficultyChip } from "@/components/ui/DifficultyChip";
import { ProgressControls } from "@/components/problem/ProgressControls";
import { PuzzleBlocks } from "./PuzzleBlocks";
import { ExampleWalk } from "./ExampleWalk";
import { RocketExplode } from "./RocketExplode";
import { AlgoBeat } from "./AlgoBeat";
import { CodeMaterialize } from "./CodeMaterialize";
import { OrbitTips } from "./OrbitTips";
import { VisualiserEngine } from "@/components/visualiser/VisualiserEngine";
import type { AnimationStep } from "@/lib/schema";
import { clsx } from "clsx";

const AnswerStage = dynamic(
  () =>
    import("@/components/answer3d/AnswerStage").then((m) => m.AnswerStage),
  {
    ssr: false,
    loading: () => (
      <div className="answer-stage grid min-h-[360px] place-items-center text-white/55">
        Loading 3D answer stage…
      </div>
    ),
  },
);

function StageBody({
  beat,
  problem,
}: {
  beat: TeachBeat;
  problem: Problem;
}) {
  const d = beat.data ?? {};
  switch (beat.kind) {
    case "hook":
      return (
        <div className="mx-auto max-w-2xl text-center">
          <motion.div
            className="brand-font text-5xl font-extrabold text-white sm:text-6xl"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            {String(d.title ?? "")}
          </motion.div>
          <p className="mt-4 text-white/55">Sit tight — teacher mode is on.</p>
        </div>
      );
    case "puzzle":
      return (
        <PuzzleBlocks
          mode={(d.mode as "kid" | "real") ?? "kid"}
          text={String(d.text ?? "")}
        />
      );
    case "example":
      return (
        <ExampleWalk
          input={String(d.input ?? "")}
          output={String(d.output ?? "")}
          explanation={String(d.explanation ?? "")}
          visualInput={d.visualInput}
          visualType={String(d.visualType ?? "array")}
        />
      );
    case "answer3d":
      return <AnswerStage problem={problem} />;
    case "rocket":
      return (
        <RocketExplode
          activeIndex={Number(d.index ?? 0)}
          total={Number(d.total ?? 1)}
          title={String(d.title ?? "")}
          body={String(d.body ?? "")}
        />
      );
    case "algo":
      return (
        <AlgoBeat
          step={d.step as AnimationStep}
          code={String(d.code ?? "")}
          visualType={String(d.visualType ?? "array")}
          stepIndex={Number(d.stepIndex ?? 0)}
          stepTotal={Number(d.stepTotal ?? 1)}
        />
      );
    case "code":
      return (
        <CodeMaterialize
          code={String(d.code ?? "")}
          time={String(d.time ?? "")}
          space={String(d.space ?? "")}
          timeReason={String(d.timeReason ?? "")}
          spaceReason={String(d.spaceReason ?? "")}
        />
      );
    case "orbit":
      return (
        <OrbitTips
          items={(d.items as { label: string; text: string }[]) ?? []}
        />
      );
    case "done":
      return (
        <div className="mx-auto max-w-xl space-y-4 text-center">
          <div className="brand-font text-4xl font-bold text-white">Mission clear</div>
          <p className="text-white/65">
            Pattern locked: <strong className="text-white">{String(d.pattern ?? "")}</strong>
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            <a
              href={String(d.leetcodeUrl ?? "#")}
              target="_blank"
              rel="noreferrer"
              className="signal-btn signal-btn-primary"
            >
              Practise on LeetCode
            </a>
            <Link href="/roadmap/" className="signal-btn signal-btn-secondary !text-white !border-white/25">
              Next missions
            </Link>
          </div>
        </div>
      );
    default:
      return null;
  }
}

export function LessonTheater({ problem }: { problem: Problem }) {
  const reduce = useReducedMotion();
  const script = useMemo(() => buildLessonScript(problem), [problem]);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [showLab, setShowLab] = useState(false);

  useEffect(() => {
    setLastSlug(problem.slug);
    setIndex(0);
    setPlaying(true);
    setShowLab(false);
  }, [problem.slug]);

  const beat = script[Math.min(index, script.length - 1)];
  const progress = script.length ? ((index + 1) / script.length) * 100 : 0;

  const next = useCallback(() => {
    setIndex((i) => Math.min(script.length - 1, i + 1));
  }, [script.length]);

  const prev = useCallback(() => {
    setIndex((i) => Math.max(0, i - 1));
  }, []);

  // Hold on interactive 3D answer stage — student drives Play there.
  useEffect(() => {
    if (beat?.kind === "answer3d") setPlaying(false);
  }, [beat?.kind, beat?.id]);

  useEffect(() => {
    if (!playing || reduce) return;
    if (beat?.kind === "answer3d") return;
    if (index >= script.length - 1) {
      setPlaying(false);
      return;
    }
    const t = setTimeout(() => next(), beat?.durationMs ?? 4000);
    return () => clearTimeout(t);
  }, [playing, index, next, beat?.durationMs, beat?.kind, script.length, reduce]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement | null)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      if (e.key === "ArrowRight") {
        setPlaying(false);
        next();
      }
      if (e.key === "ArrowLeft") {
        setPlaying(false);
        prev();
      }
      if (e.key === " ") {
        e.preventDefault();
        setPlaying((p) => !p);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [next, prev]);

  const chapters = useMemo(() => {
    const seen = new Map<string, number>();
    script.forEach((b, i) => {
      if (!seen.has(b.chapter)) seen.set(b.chapter, i);
    });
    return [...seen.entries()];
  }, [script]);

  return (
    <div className="theater-root">
      <div className="theater-sky" aria-hidden />

      <header className="relative z-10 mx-auto flex max-w-6xl flex-wrap items-center gap-3 px-4 pt-4">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2 text-sm text-white/55">
            <Link href={`/category/${problem.category}/`} className="hover:text-white">
              {problem.category.replace(/-/g, " ")}
            </Link>
            <span>·</span>
            <span className="font-mono">#{problem.leetcodeNumber}</span>
            <DifficultyChip difficulty={problem.difficulty} />
          </div>
          <h1 className="brand-font truncate text-2xl font-extrabold text-white sm:text-3xl">
            {problem.title}
          </h1>
        </div>
        <div className="ml-auto flex flex-wrap gap-2">
          <button
            type="button"
            className="signal-btn signal-btn-secondary !min-h-10 !border-white/20 !px-3 !text-sm !text-white"
            onClick={() => setShowLab((s) => !s)}
          >
            {showLab ? "Back to lesson" : "Open lab desk"}
          </button>
        </div>
      </header>

      {!showLab ? (
        <>
          <div className="relative z-10 mx-auto mt-3 flex max-w-6xl gap-2 overflow-x-auto px-4 pb-2">
            {chapters.map(([name, start]) => (
              <button
                key={name}
                type="button"
                onClick={() => {
                  setPlaying(false);
                  setIndex(start);
                }}
                className={clsx(
                  "shrink-0 rounded-full px-3 py-1.5 text-xs font-bold uppercase tracking-wide",
                  beat?.chapter === name
                    ? "bg-accent text-white"
                    : "bg-white/10 text-white/65 hover:bg-white/15",
                )}
              >
                {name}
              </button>
            ))}
          </div>

          <div className="relative z-10 mx-auto flex min-h-[52vh] max-w-6xl items-center px-4 py-6">
            <AnimatePresence mode="wait">
              <motion.div
                key={beat?.id}
                className="w-full"
                initial={reduce ? false : { opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                transition={{ duration: 0.28 }}
              >
                {beat && <StageBody beat={beat} problem={problem} />}
              </motion.div>
            </AnimatePresence>
          </div>

          <div className="teacher-bar relative z-20">
            <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-4">
              <div className="flex items-start gap-3">
                <div className="teacher-avatar" aria-hidden>
                  T
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-[11px] font-bold uppercase tracking-[0.18em] text-[#ffd43b]">
                    Teacher · {beat?.chapter}
                  </div>
                  <AnimatePresence mode="wait">
                    <motion.p
                      key={beat?.id + "-say"}
                      className="teach mt-1 text-base text-white sm:text-lg"
                      initial={reduce ? false : { opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                    >
                      {beat?.teacher}
                    </motion.p>
                  </AnimatePresence>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <button
                  type="button"
                  className="play-fab"
                  onClick={() => setPlaying((p) => !p)}
                  aria-label={playing ? "Pause lesson" : "Play lesson"}
                >
                  {playing ? "Pause" : "Play"}
                </button>
                <button type="button" className="play-chip" onClick={() => { setPlaying(false); prev(); }}>
                  Prev
                </button>
                <button type="button" className="play-chip" onClick={() => { setPlaying(false); next(); }}>
                  Next
                </button>
                <button
                  type="button"
                  className="play-chip"
                  onClick={() => {
                    setIndex(0);
                    setPlaying(true);
                  }}
                >
                  Restart
                </button>
                <div className="ml-auto text-xs text-white/45">
                  Beat {index + 1}/{script.length} · space play · arrows step
                </div>
              </div>
              <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                <motion.div
                  className="h-full rounded-full bg-accent"
                  animate={{ width: `${progress}%` }}
                />
              </div>
              <input
                type="range"
                min={0}
                max={Math.max(0, script.length - 1)}
                value={index}
                onChange={(e) => {
                  setPlaying(false);
                  setIndex(Number(e.target.value));
                }}
                className="w-full accent-[var(--accent)]"
                aria-label="Lesson scrubber"
              />
            </div>
          </div>
        </>
      ) : (
        <div className="relative z-10 mx-auto max-w-3xl space-y-6 px-4 py-8">
          <div className="theater-panel p-5">
            <h2 className="brand-font text-2xl font-bold text-white">Lab desk</h2>
            <p className="mt-2 text-white/65">
              Free-play the machine, then mark your status.
            </p>
            <div className="mt-4 rounded-2xl bg-background/95 p-2 text-foreground">
              <VisualiserEngine problem={problem} immersive />
            </div>
            <div className="mt-4">
              <ProgressControls slug={problem.slug} />
            </div>
          </div>
          {problem.relatedProblems.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {problem.relatedProblems.map((slug) => (
                <Link
                  key={slug}
                  href={`/problem/${slug}/`}
                  className="rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-sm text-white/80 hover:border-accent"
                >
                  {slug}
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
