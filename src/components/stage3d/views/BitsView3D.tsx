"use client";

import type { BitsView } from "@/lib/lesson";
import { BIT, BIT_GAP, type BitsMetrics } from "../layout";
import { Block, Label, Slab, usePresence } from "../primitives";
import { INK, toneFill } from "../theme";

const ROW_STEP = BIT + 0.24;

/** Numbers written in binary, one per row, with their columns lined up. */
export function BitsView3D({ view, m }: { view?: BitsView; m: BitsMetrics }) {
  const rows = view?.rows ?? [];
  const bitsLeft = -m.w / 2 + m.labelW;
  const stepX = BIT + BIT_GAP;
  const bx = (col: number) => bitsLeft + col * stepX + BIT / 2;
  const ry = (row: number) => m.h / 2 - 0.2 - row * ROW_STEP - BIT / 2;

  const flat = rows.flatMap((row, r) => {
    const pad = m.width - row.bits.length;
    return [...row.bits].map((bit, i) => ({ r, col: pad + i, bit, tone: row.tone }));
  });
  const present = usePresence(flat, (f) => `${f.r}:${f.col}`);

  return (
    <group>
      {/* light up the bit columns being discussed */}
      {view?.hi?.map((col) => (
        <Slab
          key={`hi-${col}`}
          x={bx(col)}
          y={(ry(0) + ry(Math.max(rows.length - 1, 0))) / 2}
          z={-0.3}
          w={BIT + 0.14}
          h={Math.max(rows.length, 1) * ROW_STEP}
          d={0.08}
          color={toneFill("cur")}
          glow={0.25}
          opacity={0.38}
        />
      ))}

      {rows.map((row, r) => (
        <group key={`row-${r}`}>
          <Label text={row.label} size={0.28} color={INK.title} x={bitsLeft - 0.22} y={ry(r)} z={-0.3} anchorX="right" />
          <Label
            text={`= ${row.v}`}
            size={0.3}
            color="#f1f5fb"
            x={bitsLeft + m.width * stepX + 0.14}
            y={ry(r)}
            z={-0.3}
            anchorX="left"
          />
        </group>
      ))}

      {present.map(({ key, item, exiting }) => (
        <Block
          key={key}
          x={bx(item.col)}
          y={ry(item.r)}
          w={BIT}
          h={BIT}
          d={0.26}
          radius={0.09}
          tone={item.bit === "1" ? (item.tone ?? "seen") : "dim"}
          text={item.bit}
          textSize={0.36}
          lift={false}
          exiting={exiting}
          spawn={[0, 0, 0.8]}
        />
      ))}
    </group>
  );
}
