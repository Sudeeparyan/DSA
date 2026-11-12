"use client";

import type { ArrayView } from "@/lib/lesson";
import { BAR_MAX, CELL, CELL_GAP, PTR_STEP, type ArrayMetrics } from "../layout";
import { Block, Empty, Label, Slab, Tag, pointerLevels, usePresence } from "../primitives";
import { INK, POINTER_COLORS, toneFill } from "../theme";

/**
 * A row of cells with index labels, named pointers and optional range trays.
 * In `bars` mode the numbers are drawn as bar heights (and can hold water).
 */
export function ArrayView3D({ view, m }: { view?: ArrayView; m: ArrayMetrics }) {
  const cells = view?.cells ?? [];
  const present = usePresence(cells, (_, i) => i);

  const slots = m.n + (m.ghostL ? 1 : 0) + (m.ghostR ? 1 : 0);
  const contentW = slots * m.pitch - CELL_GAP;
  const left = -contentW / 2 + (m.ghostL ? m.pitch : 0);
  const cx = (i: number) => left + i * m.pitch + m.cellW / 2;

  const bodyTop = m.h / 2 - m.topH;
  const baseY = bodyTop - m.bodyH;
  const barH = (i: number) => {
    const n = cells[i]?.n ?? 0;
    return Math.max(0.08, (Math.max(n, 0) / m.barMax) * BAR_MAX);
  };
  /** y of the top surface of cell i (where a pointer arrow lands) */
  const topOf = (i: number) => {
    if (!m.bars) return bodyTop;
    return i >= 0 && i < cells.length ? baseY + barH(i) : baseY + 0.08;
  };

  const ptrs = view?.ptrs ?? [];
  const levels = pointerLevels(ptrs, (p) => p.at);
  const ranges = view?.ranges ?? [];
  const water = view?.water;
  const pool = view?.pool;
  const rect = view?.box;
  const scale = BAR_MAX / m.barMax;

  const valueY = baseY - 0.32;
  const indexY = m.bars ? baseY - 0.78 : baseY - 0.28;
  const rangeLabelY = -m.h / 2 + 0.24;

  return (
    <group>
      {/* trays under the cells of each range (sliding windows, search ranges) */}
      {ranges.map((r, i) => {
        const x = (cx(r.from) + cx(r.to)) / 2;
        const w = cx(r.to) - cx(r.from) + m.cellW + 0.22;
        const color = toneFill(r.tone ?? "win");
        return (
          <group key={`range-${i}`}>
            {m.bars ? (
              <Slab x={x} y={baseY - 0.07} z={0.1} w={w} h={0.12} d={0.7} color={color} glow={0.5} />
            ) : (
              <Slab x={x} y={bodyTop - CELL / 2} z={-0.34} w={w} h={CELL + 0.24} d={0.12} color={color} glow={0.55} />
            )}
            {r.label && (
              <Slab x={x} y={rangeLabelY + 0.26} z={-0.4} w={w} h={0.05} d={0.05} color={color} glow={0.4} />
            )}
            {r.label && <Label text={r.label} size={0.24} color={color} x={x} y={rangeLabelY} z={-0.3} />}
          </group>
        );
      })}

      {present.map(({ key, item, index, exiting }) =>
        m.bars ? (
          <Block
            key={key}
            x={cx(index)}
            y={baseY + barH(index) / 2}
            w={m.cellW}
            h={exiting ? 0.08 : barH(index)}
            d={0.5}
            tone={item.tone}
            radius={0.08}
            lift={false}
            exiting={exiting}
          />
        ) : (
          <Block
            key={key}
            x={cx(index)}
            y={bodyTop - CELL / 2}
            w={m.cellW}
            h={CELL}
            tone={item.tone}
            text={item.v}
            exiting={exiting}
          />
        ),
      )}

      {/* value and index under each cell */}
      {cells.map((cell, i) => (
        <group key={`label-${i}`}>
          {m.bars && <Label text={cell.v} size={0.34} x={cx(i)} y={valueY} z={0.2} />}
          {m.idx && <Label text={String(i)} size={0.21} color={INK.faint} x={cx(i)} y={indexY} z={0.2} />}
        </group>
      ))}

      {/* water standing on top of single bars */}
      {m.bars &&
        water?.map((amount, i) => (
          <Slab
            key={`water-${i}`}
            x={cx(i)}
            y={baseY + barH(i) + (amount * scale) / 2}
            w={m.cellW}
            h={amount * scale}
            d={0.5}
            color={INK.water}
            opacity={0.62}
            glow={0.25}
            visible={amount > 0}
          />
        ))}

      {/* one sheet of water held between two walls */}
      {m.bars && (
        <Slab
          x={pool ? (cx(pool.from) + cx(pool.to)) / 2 : 0}
          y={baseY + ((pool?.h ?? 0) * scale) / 2}
          w={pool ? cx(pool.to) - cx(pool.from) : 0.001}
          h={(pool?.h ?? 0) * scale}
          d={0.64}
          color={INK.water}
          opacity={0.42}
          glow={0.2}
          visible={!!pool && pool.h > 0}
        />
      )}

      {/* a rectangle laid over a run of bars (largest rectangle in a histogram) */}
      {m.bars && (
        <Slab
          x={rect ? (cx(rect.from) + cx(rect.to)) / 2 : 0}
          y={baseY + ((rect?.h ?? 0) * scale) / 2}
          z={0.06}
          w={rect ? cx(rect.to) - cx(rect.from) + m.cellW + 0.06 : 0.001}
          h={(rect?.h ?? 0) * scale}
          d={0.62}
          color={toneFill("good")}
          opacity={0.6}
          glow={0.35}
          visible={!!rect && rect.h > 0}
        />
      )}

      {ptrs.map((p) => (
        <Tag
          key={p.name}
          name={p.name}
          x={cx(p.at)}
          y={topOf(p.at)}
          level={levels.get(p.name) ?? 0}
          step={PTR_STEP}
          color={POINTER_COLORS[Math.max(0, m.ptrNames.indexOf(p.name)) % POINTER_COLORS.length]}
        />
      ))}

      {view && cells.length === 0 && <Empty y={bodyTop - m.bodyH / 2} />}
    </group>
  );
}
