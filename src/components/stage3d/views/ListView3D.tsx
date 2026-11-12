"use client";

import type { ListView } from "@/lib/lesson";
import { LIST_NODE_H, PTR_STEP, type ListMetrics } from "../layout";
import { Arc, Block, Edge, Label, Tag, pointerLevels, usePresence, useRegistry } from "../primitives";
import { INK, POINTER_COLORS, toneFill } from "../theme";

/**
 * A linked list.  Nodes stay where they were created; what changes is where
 * each node's arrow points, so re-wiring is visible as arrows swinging over.
 */
export function ListView3D({ view, m }: { view?: ListView; m: ListMetrics }) {
  const nodes = view?.nodes ?? [];
  const present = usePresence(nodes, (n) => n.id);
  const { register, getter } = useRegistry<number>();

  const slots = m.cols + (m.hasNull ? 1 : 0);
  const contentW = m.labelW + slots * m.pitchX - (m.pitchX - m.nodeW);
  const left = -contentW / 2 + m.labelW;
  const nx = (col: number) => left + col * m.pitchX + m.nodeW / 2;
  const ny = (row: number) => m.h / 2 - row * m.pitchY - m.ptrZone - LIST_NODE_H / 2;

  const byId = new Map(nodes.map((n) => [n.id, n]));
  const trim = [m.nodeW / 2 + 0.06, LIST_NODE_H / 2 + 0.06] as const;
  const ptrs = view?.ptrs ?? [];
  const levels = pointerLevels(ptrs, (p) => p.at ?? "none");

  return (
    <group>
      {view?.rows?.map((label, row) => (
        <Label
          key={`row-${row}`}
          text={label}
          size={0.24}
          color={INK.title}
          x={-contentW / 2}
          y={ny(row)}
          z={-0.3}
          anchorX="left"
        />
      ))}

      {present.map(({ key, item, exiting }) => (
        <Block
          key={key}
          x={nx(item.x)}
          y={ny(item.y)}
          w={m.nodeW}
          h={LIST_NODE_H}
          tone={item.tone}
          text={item.v}
          textSize={0.4}
          exiting={exiting}
          register={register(item.id)}
        />
      ))}

      {/* `next` links */}
      {nodes.map((n) => {
        const next = n.next !== undefined ? byId.get(n.next) : undefined;
        if (!next || next.id === n.id) return null;
        const adjacent = next.y === n.y && Math.abs(next.x - n.x) === 1;
        if (adjacent || next.y !== n.y) {
          return (
            <Edge
              key={`next-${n.id}`}
              from={getter(n.id)}
              to={getter(next.id)}
              trimA={trim}
              trimB={trim}
              arrow
              shift={adjacent ? 0.11 : 0}
              color={n.tone === "good" ? toneFill("good") : INK.edge}
            />
          );
        }
        const y = ny(n.y) - LIST_NODE_H / 2 - 0.05;
        const reach = Math.min(Math.abs(next.x - n.x), 4);
        return (
          <Arc
            key={`skip-${n.id}`}
            a={[nx(n.x), y, 0]}
            b={[nx(next.x), y, 0]}
            bend={-(1 + 0.2 * reach)}
            color={INK.edge}
          />
        );
      })}

      {/* `random` links (copy list with random pointer) */}
      {nodes.map((n) => {
        const other = n.rand !== undefined ? byId.get(n.rand) : undefined;
        if (!other) return null;
        const y = ny(n.y) - LIST_NODE_H / 2 - 0.05;
        const color = toneFill("alt");
        if (other.id === n.id) {
          return (
            <Arc
              key={`rand-${n.id}`}
              a={[nx(n.x) - 0.26, y, 0]}
              b={[nx(n.x) + 0.26, y, 0]}
              bend={-0.95}
              color={color}
              width={0.035}
            />
          );
        }
        if (other.y !== n.y) {
          return (
            <Edge
              key={`rand-${n.id}`}
              from={getter(n.id)}
              to={getter(other.id)}
              trimA={trim}
              trimB={trim}
              arrow
              color={color}
              width={0.035}
              shift={-0.16}
            />
          );
        }
        const reach = Math.min(Math.abs(other.x - n.x), 4);
        const side = other.x > n.x ? -0.14 : 0.14;
        return (
          <Arc
            key={`rand-${n.id}`}
            a={[nx(n.x) + side, y, 0]}
            b={[nx(other.x) - side, y, 0]}
            bend={-(1.25 + 0.22 * reach)}
            color={color}
            width={0.035}
          />
        );
      })}

      {m.hasNull && (
        <Block
          x={nx(m.cols)}
          y={ny(0)}
          w={m.nodeW}
          h={LIST_NODE_H * 0.74}
          d={0.3}
          tone="dim"
          text="None"
          textSize={0.26}
          lift={false}
        />
      )}

      {ptrs.map((p) => {
        const target = p.at !== null ? byId.get(p.at) : undefined;
        if (p.at !== null && !target) return null;
        return (
          <Tag
            key={p.name}
            name={p.name}
            x={target ? nx(target.x) : nx(m.cols)}
            y={(target ? ny(target.y) : ny(0)) + (target ? LIST_NODE_H / 2 : (LIST_NODE_H * 0.74) / 2)}
            level={levels.get(p.name) ?? 0}
            step={PTR_STEP}
            color={POINTER_COLORS[Math.max(0, m.ptrNames.indexOf(p.name)) % POINTER_COLORS.length]}
          />
        );
      })}
    </group>
  );
}
