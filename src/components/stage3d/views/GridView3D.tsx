"use client";

import type { GridView } from "@/lib/lesson";
import { TILE, TILE_GAP, type GridMetrics } from "../layout";
import { Block, Frame, Label, Slab, usePresence } from "../primitives";
import { INK, POINTER_COLORS, textWidth } from "../theme";

/** A matrix, board or 2-D DP table.  Cursors are coloured frames around a cell. */
export function GridView3D({ view, m }: { view?: GridView; m: GridMetrics }) {
  const flat = (view?.cells ?? []).flatMap((row, r) => row.map((cell, c) => ({ r, c, cell })));
  const present = usePresence(flat, (it) => `${it.r},${it.c}`);

  const stepX = m.cellW + TILE_GAP;
  const stepY = TILE + TILE_GAP;
  const contentW = m.rowLabelW + m.cols * stepX - TILE_GAP;
  const left = -contentW / 2;
  const top = m.h / 2;
  const cx = (c: number) => left + m.rowLabelW + c * stepX + m.cellW / 2;
  const cy = (r: number) => top - m.colLabelH - r * stepY - TILE / 2;
  const colorOf = (name: string) =>
    POINTER_COLORS[Math.max(0, m.ptrNames.indexOf(name)) % POINTER_COLORS.length];

  const legendY = -m.h / 2 + 0.17;
  const legendX: number[] = [];
  m.ptrNames.reduce((x, name) => {
    legendX.push(x);
    return x + 0.34 + textWidth(name, 0.22) + 0.5;
  }, left);

  return (
    <group>
      {view?.cols?.map((label, c) => (
        <Label key={`col-${c}`} text={label} size={0.3} color={INK.title} x={cx(c)} y={top - 0.24} z={-0.3} />
      ))}
      {view?.rows?.map((label, r) => (
        <Label
          key={`row-${r}`}
          text={label}
          size={0.3}
          color={INK.title}
          x={left + m.rowLabelW - 0.2}
          y={cy(r)}
          z={-0.3}
          anchorX="right"
        />
      ))}

      {present.map(({ key, item, exiting }) => (
        <Block
          key={key}
          x={cx(item.c)}
          y={cy(item.r)}
          w={m.cellW}
          h={TILE}
          d={0.3}
          radius={0.1}
          tone={item.cell.tone}
          text={item.cell.v === "" ? undefined : item.cell.v}
          textSize={0.4}
          exiting={exiting}
          spawn={[0, 0, 0.9]}
        />
      ))}

      {view?.ptrs?.map((p) => (
        <Frame key={p.name} x={cx(p.c)} y={cy(p.r)} w={m.cellW + 0.1} h={TILE + 0.1} color={colorOf(p.name)} />
      ))}

      {/* which frame is which */}
      {m.ptrNames.map((name, i) => {
        const x = legendX[i];
        return (
          <group key={`legend-${name}`}>
            <Slab x={x + 0.11} y={legendY} z={-0.4} w={0.22} h={0.22} d={0.06} color={colorOf(name)} glow={0.5} />
            <Label text={name} size={0.22} color={INK.title} x={x + 0.34} y={legendY} z={-0.4} anchorX="left" />
          </group>
        );
      })}
    </group>
  );
}
