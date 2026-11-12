"use client";

import type { ItemsView, StackView } from "@/lib/lesson";
import { SLAB_H, type ItemsMetrics, type StackMetrics } from "../layout";
import { Bar, Block, Empty, Glide, Label, usePresence } from "../primitives";
import { INK } from "../theme";

const PILE_GAP = 0.07;
const QUEUE_GAP = 0.12;

/** A stack (pile, top on top), a queue (front on the left) or the call stack. */
export function StackView3D({ view, m }: { view?: StackView; m: StackMetrics }) {
  const items = view?.items ?? [];
  const present = usePresence(items, (it) => it.id);
  const count = items.length;

  if (m.shape === "queue") {
    const stepX = m.slabW + QUEUE_GAP;
    const left = -m.w / 2;
    const y = m.h / 2 - SLAB_H / 2 - 0.04;
    const x = (i: number) => left + i * stepX + m.slabW / 2;
    return (
      <group>
        {present.map(({ key, item, index, exiting }) => (
          <Block
            key={key}
            x={x(index)}
            y={y}
            w={m.slabW}
            h={SLAB_H}
            d={0.44}
            tone={item.tone}
            text={item.v}
            textSize={0.36}
            exiting={exiting}
            spawn={[1.5, 0, 0]}
          />
        ))}
        {count > 0 && (
          <Glide x={x(0)} y={y - SLAB_H / 2 - 0.26} z={-0.3}>
            <Label text={count === 1 ? "front · back" : "front"} size={0.2} color={INK.faint} />
          </Glide>
        )}
        {count > 1 && (
          <Glide x={x(count - 1)} y={y - SLAB_H / 2 - 0.26} z={-0.3}>
            <Label text="back" size={0.2} color={INK.faint} />
          </Glide>
        )}
        {view && count === 0 && <Empty y={y} />}
      </group>
    );
  }

  const stepY = SLAB_H + PILE_GAP;
  const bottom = -m.h / 2 + 0.16;
  const cx = m.shape === "stack" ? -0.55 : 0;
  const y = (i: number) => bottom + i * stepY + SLAB_H / 2;
  return (
    <group>
      <Bar
        from={[cx - m.slabW / 2 - 0.2, bottom - 0.08, -0.1]}
        to={[cx + m.slabW / 2 + 0.2, bottom - 0.08, -0.1]}
        color={INK.edge}
        width={0.05}
      />
      {present.map(({ key, item, index, exiting }) => (
        <Block
          key={key}
          x={cx}
          y={y(index)}
          w={m.slabW}
          h={SLAB_H}
          d={0.5}
          tone={item.tone}
          text={item.v}
          textSize={0.36}
          exiting={exiting}
          spawn={[0, 1.7, 0]}
        />
      ))}
      {m.shape === "stack" && count > 0 && (
        <Glide x={cx + m.slabW / 2 + 0.2} y={y(count - 1)} z={0}>
          <Label text="← top" size={0.25} color={INK.title} anchorX="left" />
        </Glide>
      )}
      {view && count === 0 && <Empty y={bottom + 0.5} />}
    </group>
  );
}

/** Finished pieces (results, groups, paths) laid out as slabs. */
export function ItemsView3D({ view, m }: { view?: ItemsView; m: ItemsMetrics }) {
  const items = view?.items ?? [];
  const present = usePresence(items, (_, i) => i);
  const stepX = m.itemW + 0.2;
  const stepY = SLAB_H + 0.18;
  const left = -(m.perRow * stepX - 0.2) / 2;
  const top = m.h / 2;
  return (
    <group>
      {present.map(({ key, item, index, exiting }) => (
        <Block
          key={key}
          x={left + (index % m.perRow) * stepX + m.itemW / 2}
          y={top - Math.floor(index / m.perRow) * stepY - SLAB_H / 2}
          w={m.itemW}
          h={SLAB_H}
          d={0.4}
          tone={item.tone}
          text={item.v}
          textSize={0.34}
          exiting={exiting}
          spawn={[0, 0.8, 0.8]}
        />
      ))}
      {view && items.length === 0 && <Empty />}
    </group>
  );
}
