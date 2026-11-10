"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { ContactShadows, Environment, OrbitControls } from "@react-three/drei";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import type { Problem } from "@/lib/schema";
import { shotForAlgoMoment, type CinemaShot } from "@/lib/cinemaCameras";
import {
  type AnimationState,
  hasMatchHighlight,
  readHighlights,
  readMemoryShelf,
  readPrimaryValues,
  resolveAnimationSteps,
} from "@/lib/animation";
import { AlgoWorld } from "./AlgoWorld";
import { CinematicCamera } from "./CinematicCamera";
import { clsx } from "clsx";

export function AnswerStage({ problem }: { problem: Problem }) {
  const reduce = useReducedMotion();
  const steps = useMemo(() => resolveAnimationSteps(problem), [problem]);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [shotProgress, setShotProgress] = useState(0);
  const [freeCam, setFreeCam] = useState(false);

  useEffect(() => {
    setIndex(0);
    setPlaying(true);
    setShotProgress(0);
    setFreeCam(false);
  }, [problem.slug]);

  const step = steps[Math.min(index, Math.max(0, steps.length - 1))];
  const state = useMemo(
    () => (step?.state ?? {}) as AnimationState,
    [step],
  );
  const highlights = useMemo(() => readHighlights(state), [state]);
  const matched = hasMatchHighlight(state);
  const shot: CinemaShot = shotForAlgoMoment({
    index,
    total: steps.length,
    matched,
    starting: index === 0,
  });

  const focusX = useMemo(() => {
    const nums = readPrimaryValues(state);
    const spacing = nums.length > 8 ? 0.7 : 0.95;
    const start = -((Math.max(nums.length, 1) - 1) * spacing) / 2;
    const ci =
      typeof state.currentIndex === "number"
        ? (state.currentIndex as number)
        : Object.keys(highlights)
            .map(Number)
            .find((n) => !Number.isNaN(n));
    if (ci == null || nums.length === 0) return 0;
    return start + Math.min(ci, nums.length - 1) * spacing;
  }, [state, highlights]);

  useEffect(() => {
    if (!playing || reduce) return;
    if (index >= steps.length - 1) {
      setPlaying(false);
      return;
    }
    const duration = matched ? 1400 : 1700;
    const start = performance.now();
    let raf = 0;
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      setShotProgress(t);
      if (t < 1) raf = requestAnimationFrame(tick);
      else setIndex((i) => Math.min(steps.length - 1, i + 1));
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [playing, index, steps.length, matched, reduce]);

  useEffect(() => {
    setShotProgress(0);
  }, [index]);

  const nums = readPrimaryValues(state);
  const seen = readMemoryShelf(state);
  const grid = Array.isArray(state.grid) ? (state.grid as unknown[][]) : undefined;
  const intervals = Array.isArray(state.intervals)
    ? (state.intervals as number[][])
    : undefined;
  const bits = Array.isArray(state.bits) ? (state.bits as number[]) : undefined;

  return (
    <div className="answer-stage">
      <div className="answer-stage-canvas">
        <Canvas
          shadows
          dpr={[1, 1.75]}
          camera={{ position: [2.4, 2.6, 4.2], fov: 42, near: 0.1, far: 60 }}
          gl={{ antialias: true, alpha: true }}
        >
          <color attach="background" args={["#070b09"]} />
          <ambientLight intensity={0.35} />
          {/* Golden key / warm fill inspired by blender turntable lighting */}
          <directionalLight
            castShadow
            position={[3.2, 4.5, -2]}
            intensity={1.35}
            color="#ffd6a0"
            shadow-mapSize={[1024, 1024]}
          />
          <directionalLight position={[-3, 2.5, 2]} intensity={0.55} color="#9ad7ff" />
          <directionalLight position={[0, 1.5, 4]} intensity={0.35} color="#ffffff" />
          <Suspense fallback={null}>
            <AlgoWorld
              nums={nums}
              seen={seen}
              highlights={highlights}
              grid={grid}
              intervals={intervals}
              bits={bits}
            />
            <ContactShadows
              position={[0, -0.16, 0]}
              opacity={0.45}
              scale={10}
              blur={2.2}
              far={4}
            />
            <Environment preset="city" />
          </Suspense>
          <CinematicCamera
            shot={freeCam ? "hero" : shot}
            progress={freeCam ? 0 : shotProgress}
            focus={[focusX, 0.45, 0]}
            interactive={freeCam}
          />
          {freeCam && (
            <OrbitControls
              enablePan={false}
              minDistance={2}
              maxDistance={8}
              maxPolarAngle={Math.PI * 0.49}
            />
          )}
        </Canvas>
      </div>

      <div className="answer-stage-hud">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-accent/20 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.16em] text-accent">
            Shot · {shot}
          </span>
          <span className="text-[11px] text-white/45">
            Beat {steps.length ? index + 1 : 0}/{steps.length}
          </span>
          <button
            type="button"
            className={clsx(
              "ml-auto rounded-full border px-3 py-1 text-xs font-bold",
              freeCam
                ? "border-accent bg-accent text-white"
                : "border-white/20 text-white/70",
            )}
            onClick={() => {
              setFreeCam((f) => !f);
              setPlaying(false);
            }}
          >
            {freeCam ? "Cinema cam" : "Orbit freely"}
          </button>
        </div>

        <AnimatePresence mode="wait">
          <motion.p
            key={step?.caption ?? "empty"}
            className="teach mt-3 text-base text-white sm:text-lg"
            initial={reduce ? false : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            {step?.caption ?? "Loading the answer stage…"}
          </motion.p>
        </AnimatePresence>

        <div className="mt-4 flex flex-wrap gap-2">
          <button
            type="button"
            className="play-fab"
            onClick={() => setPlaying((p) => !p)}
          >
            {playing ? "Pause" : "Play answer"}
          </button>
          <button
            type="button"
            className="play-chip"
            onClick={() => {
              setPlaying(false);
              setIndex((i) => Math.max(0, i - 1));
            }}
          >
            Prev
          </button>
          <button
            type="button"
            className="play-chip"
            onClick={() => {
              setPlaying(false);
              setIndex((i) => Math.min(steps.length - 1, i + 1));
            }}
          >
            Next
          </button>
          <button
            type="button"
            className="play-chip"
            onClick={() => {
              setIndex(0);
              setPlaying(true);
              setFreeCam(false);
            }}
          >
            Restart
          </button>
        </div>
        <input
          type="range"
          className="mt-3 w-full accent-[var(--accent)]"
          min={0}
          max={Math.max(0, steps.length - 1)}
          value={index}
          onChange={(e) => {
            setPlaying(false);
            setIndex(Number(e.target.value));
          }}
          aria-label="Answer beat scrubber"
        />
      </div>
    </div>
  );
}
