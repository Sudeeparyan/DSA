"use client";

import { motion, useReducedMotion } from "framer-motion";

const PARTS = [
  { id: "nose", d: "M120 28 L152 92 L88 92 Z", labelY: 48 },
  { id: "body", d: "M88 92 H152 V168 H88 Z", labelY: 128 },
  { id: "engine", d: "M96 168 H144 L156 198 H84 Z", labelY: 178 },
  { id: "finL", d: "M88 140 L60 188 L88 168 Z", labelY: 156 },
  { id: "finR", d: "M152 140 L180 188 L152 168 Z", labelY: 156 },
] as const;

export function RocketExplode({
  activeIndex,
  total,
  title,
  body,
}: {
  activeIndex: number;
  total: number;
  title: string;
  body: string;
}) {
  const reduce = useReducedMotion();
  const focus = Math.min(activeIndex, PARTS.length - 1);

  // Explode offsets per part when focused
  const explode = (i: number) => {
    if (reduce) return { x: 0, y: 0 };
    if (i !== focus) return { x: 0, y: 0, opacity: 0.35, scale: 0.96 };
    const map = [
      { x: 0, y: -36 },
      { x: 48, y: 0 },
      { x: 0, y: 42 },
      { x: -52, y: 18 },
      { x: 52, y: 18 },
    ];
    return { ...map[i], opacity: 1, scale: 1.05 };
  };

  return (
    <div className="relative mx-auto flex w-full max-w-3xl flex-col items-center gap-6 lg:flex-row lg:items-start lg:justify-center lg:gap-10">
      <div className="relative h-[280px] w-[240px] shrink-0 sm:h-[320px] sm:w-[260px]">
        <svg viewBox="0 0 240 220" className="h-full w-full overflow-visible">
          <defs>
            <linearGradient id="rocketSkin" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0%" stopColor="#2ec4a8" />
              <stop offset="100%" stopColor="#0b7a6f" />
            </linearGradient>
            <linearGradient id="rocketHot" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#ff8a3d" />
              <stop offset="100%" stopColor="#d4550a" />
            </linearGradient>
          </defs>
          {PARTS.map((part, i) => {
            const e = explode(i);
            const assembled = activeIndex >= i;
            return (
              <motion.g
                key={part.id}
                initial={false}
                animate={{
                  x: assembled ? (e.x as number) : 0,
                  y: assembled ? ((e.y as number) ?? 0) + (assembled && i > activeIndex ? 0 : 0) : 80,
                  opacity: assembled ? ((e.opacity as number) ?? 1) : 0.15,
                  scale: assembled ? ((e.scale as number) ?? 1) : 0.85,
                }}
                transition={{ type: "spring", stiffness: 140, damping: 16 }}
              >
                <path
                  d={part.d}
                  fill={i === focus ? "url(#rocketHot)" : "url(#rocketSkin)"}
                  stroke="rgba(255,255,255,0.35)"
                  strokeWidth="2"
                />
                {i === focus && (
                  <motion.circle
                    cx={120}
                    cy={part.labelY}
                    r={8}
                    fill="#ffd43b"
                    initial={{ scale: 0 }}
                    animate={{ scale: [1, 1.25, 1] }}
                    transition={{ duration: 1.2, repeat: Infinity }}
                  />
                )}
              </motion.g>
            );
          })}
          {/* callout line */}
          <motion.line
            x1="152"
            y1={PARTS[focus].labelY}
            x2="210"
            y2={PARTS[focus].labelY - 10}
            stroke="#ffd43b"
            strokeWidth="2"
            strokeDasharray="4 4"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            key={focus}
          />
        </svg>
        <div className="absolute bottom-2 left-0 right-0 text-center font-mono text-[11px] uppercase tracking-[0.2em] text-white/45">
          part {activeIndex + 1}/{total}
        </div>
      </div>

      <motion.div
        key={title}
        className="explode-card max-w-md"
        initial={reduce ? false : { opacity: 0, x: 24, scale: 0.96 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 160, damping: 18 }}
      >
        <div className="section-kicker text-[#ffd43b]">Exploded part</div>
        <h3 className="brand-font mt-2 text-2xl font-bold text-white">{title}</h3>
        <p className="teach mt-3 text-base text-white/80">{body}</p>
      </motion.div>
    </div>
  );
}
