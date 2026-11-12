"use client";

import type { IntervalsView } from "@/lib/lesson";
import { LANE_H, packLanes, type IntervalsMetrics } from "../layout";
import { Bar, Block, Glide, Label, usePresence } from "../primitives";
import { INK, fitSize, toneFill } from "../theme";

const LANE_STEP = LANE_H + 0.1;

function tickStep(span: number): number {
  for (const step of [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]) {
    if (span / step <= 16) return step;
  }
  return Math.ceil(span / 16);
}

/** Intervals drawn to scale on a shared number line, one labelled row per list. */
export function IntervalsView3D({ view, m }: { view?: IntervalsView; m: IntervalsMetrics }) {
  const left = -m.w / 2;
  const axisLeft = left + m.labelW + 0.2;
  const X = (v: number) => axisLeft + ((v - m.min) / (m.max - m.min)) * m.axisW;

  // top edge of every row, in the fixed order the rows first appeared
  const rowTop = new Map<string, number>();
  let y = m.h / 2;
  for (const key of m.order) {
    rowTop.set(key, y);
    y -= m.lanes[key] * LANE_STEP + 0.42;
  }
  const axisY = -m.h / 2 + 0.62;

  const flat = (view?.rows ?? []).flatMap((row) => {
    const lanes = packLanes(row.items);
    return row.items.map((it, i) => ({ row: row.label, i, it, lane: lanes[i] }));
  });
  const present = usePresence(flat, (f) => `${f.row}:${f.i}`);

  const span = m.max - m.min;
  const step = tickStep(span);
  const ticks: number[] = [];
  for (let v = Math.ceil(m.min / step) * step; v <= m.max + 1e-9; v += step) ticks.push(v);

  return (
    <group>
      {m.order.map((key) => (
        <Label
          key={`label-${key}`}
          text={key}
          size={0.26}
          color={INK.title}
          x={left + 0.05}
          y={rowTop.get(key)! - 0.21 - (m.lanes[key] * LANE_STEP - 0.1) / 2}
          z={-0.3}
          anchorX="left"
        />
      ))}

      {present.map(({ key, item, exiting }) => {
        const x0 = X(item.it.a);
        const x1 = X(item.it.b);
        const w = Math.max(x1 - x0, 0.24);
        const text = `[${item.it.a},${item.it.b}]`;
        const size = fitSize(text, w - 0.16, 0.3);
        return (
          <Block
            key={key}
            x={(x0 + x1) / 2}
            y={(rowTop.get(item.row) ?? 0) - 0.21 - item.lane * LANE_STEP - LANE_H / 2}
            w={w}
            h={LANE_H}
            d={0.4}
            radius={0.1}
            tone={item.it.tone ?? "seen"}
            text={size >= 0.17 ? text : undefined}
            textSize={0.3}
            lift={false}
            exiting={exiting}
            spawn={[0, 0.7, 0.6]}
          />
        );
      })}

      {/* the number line */}
      <Bar from={[X(m.min) - 0.2, axisY, -0.3]} to={[X(m.max) + 0.2, axisY, -0.3]} color={INK.edge} width={0.035} />
      {ticks.map((v) => (
        <group key={`tick-${v}`}>
          <Bar from={[X(v), axisY - 0.09, -0.3]} to={[X(v), axisY + 0.09, -0.3]} color={INK.edge} width={0.03} />
          <Label text={String(v)} size={0.2} color={INK.faint} x={X(v)} y={axisY - 0.3} z={-0.3} />
        </group>
      ))}

      {view?.marks?.map((mark) => (
        <Glide key={`mark-${mark.label}`} x={X(mark.x)} y={0} z={0.3}>
          <Bar from={[0, axisY, 0]} to={[0, m.h / 2 - 0.3, 0]} color={toneFill("cur")} width={0.04} />
          <Label text={mark.label} size={0.24} color={toneFill("cur")} y={m.h / 2 - 0.12} />
        </Glide>
      ))}
    </group>
  );
}
