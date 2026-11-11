"use client";

import { useState } from "react";
import { motion, useReducedMotion } from "framer-motion";

interface OrbitItem {
  label: string;
  text: string;
}

export function OrbitTips({ items }: { items: OrbitItem[] }) {
  const reduce = useReducedMotion();
  const [open, setOpen] = useState(0);

  return (
    <div className="relative mx-auto w-full max-w-3xl pb-36 pt-8">
      <div className="relative mx-auto h-[260px] w-[260px] sm:h-[300px] sm:w-[300px]">
        <div className="orbit-core absolute left-1/2 top-1/2 flex h-24 w-24 -translate-x-1/2 -translate-y-1/2 items-center justify-center text-center text-[11px] font-bold uppercase tracking-[0.18em] text-white/70">
          Tap
          <br />a chip
        </div>
        {items.map((item, i) => {
          const angle = (i / Math.max(items.length, 1)) * Math.PI * 2 - Math.PI / 2;
          const radius = 112;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;
          const active = open === i;
          return (
            <motion.button
              key={`${item.label}-${i}`}
              type="button"
              className="orbit-chip absolute left-1/2 top-1/2"
              style={{
                marginLeft: x - 44,
                marginTop: y - 22,
                borderColor: active ? "var(--current)" : "rgba(255,255,255,0.2)",
                zIndex: active ? 5 : 1,
              }}
              onClick={() => setOpen(i)}
              animate={
                reduce
                  ? undefined
                  : { y: [0, -5, 0] }
              }
              transition={{
                duration: 2.8 + i * 0.15,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <span className="text-[10px] font-bold uppercase tracking-wider text-[#ffd43b]">
                {item.label}
              </span>
            </motion.button>
          );
        })}
      </div>

      <motion.div
        key={open}
        className="explode-card mx-auto mt-6 max-w-md"
        initial={reduce ? false : { opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="section-kicker text-[#ffd43b]">
          {items[open]?.label}
        </div>
        <p className="teach mt-2 text-base text-white/85">{items[open]?.text}</p>
      </motion.div>
    </div>
  );
}
