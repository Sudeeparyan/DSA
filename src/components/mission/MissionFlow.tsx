"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { Problem } from "@/lib/schema";
import { setLastSlug } from "@/lib/progress";
import { accentFor } from "@/lib/categories";
import { DifficultyChip } from "@/components/ui/DifficultyChip";
import Link from "next/link";
import { MissionBrief } from "./MissionBrief";
import { IdeaBuild } from "./IdeaBuild";
import { SimulateArena } from "./SimulateArena";
import { BlueprintStage } from "./BlueprintStage";
import { FlightCheck } from "./FlightCheck";
import { clsx } from "clsx";

const STAGES = [
  { id: "brief", label: "Brief", verb: "Understand the ask" },
  { id: "build", label: "Build", verb: "Assemble the idea" },
  { id: "simulate", label: "Simulate", verb: "Watch it run" },
  { id: "blueprint", label: "Blueprint", verb: "Read the code" },
  { id: "check", label: "Launch", verb: "Flight check" },
] as const;

export type MissionStageId = (typeof STAGES)[number]["id"];

export function MissionFlow({ problem }: { problem: Problem }) {
  const [stage, setStage] = useState<MissionStageId>("brief");
  const reduce = useReducedMotion();
  const accent = accentFor(problem.category);
  const stageIndex = STAGES.findIndex((s) => s.id === stage);

  useEffect(() => {
    setLastSlug(problem.slug);
    setStage("brief");
  }, [problem.slug]);

  function go(next: MissionStageId) {
    setStage(next);
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  }

  function next() {
    if (stageIndex < STAGES.length - 1) go(STAGES[stageIndex + 1].id);
  }

  function prev() {
    if (stageIndex > 0) go(STAGES[stageIndex - 1].id);
  }

  return (
    <div className="mission-shell pb-28">
      <header className="mission-topbar">
        <div className="mx-auto flex max-w-5xl flex-col gap-4 px-4 py-5">
          <div className="flex flex-wrap items-center gap-2 text-sm text-muted">
            <Link
              href={`/category/${problem.category}/`}
              className="font-semibold hover:text-foreground"
            >
              {problem.category.replace(/-/g, " ")}
            </Link>
            <span aria-hidden>·</span>
            <span className="font-mono">#{problem.leetcodeNumber}</span>
            <DifficultyChip difficulty={problem.difficulty} />
            <span
              className="ml-auto rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider text-white"
              style={{ background: accent }}
            >
              Mission {problem.id}/150
            </span>
          </div>
          <h1 className="brand-font text-3xl font-extrabold tracking-tight sm:text-4xl">
            {problem.title}
          </h1>
          <p className="max-w-2xl text-sm text-muted sm:text-base">
            Pattern gear: <strong className="text-foreground">{problem.pattern.name}</strong>
            {" — "}
            {problem.pattern.whenToSpot}
          </p>

          <nav aria-label="Mission stages" className="stage-rail">
            {STAGES.map((s, i) => {
              const done = i < stageIndex;
              const active = i === stageIndex;
              return (
                <button
                  key={s.id}
                  type="button"
                  onClick={() => go(s.id)}
                  className={clsx(
                    "stage-pill",
                    done && "stage-pill-done",
                    active && "stage-pill-active",
                  )}
                >
                  <span className="stage-index">{i + 1}</span>
                  <span className="min-w-0">
                    <span className="block text-xs font-bold uppercase tracking-wide">
                      {s.label}
                    </span>
                    <span className="hidden truncate text-[11px] opacity-70 sm:block">
                      {s.verb}
                    </span>
                  </span>
                </button>
              );
            })}
          </nav>
          <div className="h-1.5 overflow-hidden rounded-full bg-border">
            <motion.div
              className="h-full rounded-full bg-accent"
              animate={{ width: `${((stageIndex + 1) / STAGES.length) * 100}%` }}
              transition={{ type: "spring", stiffness: 120, damping: 20 }}
            />
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-5xl px-4 pt-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={stage}
            initial={reduce ? false : { opacity: 0, y: 18, scale: 0.985 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={reduce ? undefined : { opacity: 0, y: -12, scale: 0.985 }}
            transition={{ duration: 0.28 }}
          >
            {stage === "brief" && (
              <MissionBrief problem={problem} onContinue={next} />
            )}
            {stage === "build" && (
              <IdeaBuild problem={problem} onContinue={next} onBack={prev} />
            )}
            {stage === "simulate" && (
              <SimulateArena problem={problem} onContinue={next} onBack={prev} />
            )}
            {stage === "blueprint" && (
              <BlueprintStage problem={problem} onContinue={next} onBack={prev} />
            )}
            {stage === "check" && (
              <FlightCheck problem={problem} onBack={prev} />
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
