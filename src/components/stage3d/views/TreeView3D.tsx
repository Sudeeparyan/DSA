"use client";

import { useMemo, useRef } from "react";
import type { TreeView } from "@/lib/lesson";
import { NODE_D, PTR_STEP, layoutTree, stableTreeLayout, treeNodeWidth, type TreeMetrics } from "../layout";
import { Badge, Block, Edge, Empty, Ring, Tag, pointerLevels, usePresence, useRegistry } from "../primitives";
import { INK, POINTER_COLORS, toneFill } from "../theme";

const BOX_H = 0.62;

function childrenOf(node: TreeView["nodes"][number]): number[] {
  if (node.kids) return node.kids;
  const out: number[] = [];
  if (node.l !== undefined) out.push(node.l);
  if (node.r !== undefined) out.push(node.r);
  return out;
}

function onPath(tone?: string): boolean {
  return tone === "cur" || tone === "win";
}

/**
 * Binary trees, heaps, tries and recursion trees.  When the shape changes the
 * nodes glide to their new places and the links follow them.
 */
export function TreeView3D({ view, m, last }: { view?: TreeView; m: TreeMetrics; last?: TreeView }) {
  const lastLayout = useMemo(() => (last ? layoutTree(last) : undefined), [last]);
  const layout = useMemo(
    () => (view ? stableTreeLayout(view, last, lastLayout) : undefined),
    [view, last, lastLayout],
  );
  const nodes = view?.nodes ?? [];
  const presentNodes = usePresence(nodes, (n) => n.id);
  const { register, getter } = useRegistry<number>();
  const shapeOf = view ?? last;
  const isBox = shapeOf?.shape === "box";
  const widthOf = (label: string) => (shapeOf ? treeNodeWidth(shapeOf, label) : NODE_D);

  const byId = new Map(nodes.map((n) => [n.id, n]));
  const links: { key: string; a: number; b: number; hot: boolean }[] = [];
  for (const n of nodes) {
    for (const child of childrenOf(n)) {
      const c = byId.get(child);
      if (c) links.push({ key: `${n.id}-${child}`, a: n.id, b: child, hot: onPath(n.tone) && onPath(c.tone) });
    }
  }
  const presentLinks = usePresence(links, (l) => l.key);

  // remember where each node was, so a removed node can shrink away in place
  const where = useRef(new Map<number, { x: number; y: number }>());
  const topY = m.h / 2 - m.topH - NODE_D / 2;
  if (layout) {
    for (const [id, p] of layout.pos) where.current.set(id, { x: p.x, y: topY + p.y });
  }
  const at = (id: number) => where.current.get(id) ?? { x: 0, y: topY };

  const half = isBox ? BOX_H / 2 : NODE_D / 2;
  const ptrs = view?.ptrs ?? [];
  const levels = pointerLevels(ptrs, (p) => p.at);

  return (
    <group>
      {presentLinks.map(({ key, item, exiting }) => {
        const wa = widthOf(byId.get(item.a)?.v ?? "");
        const wb = widthOf(byId.get(item.b)?.v ?? "");
        return (
          <Edge
            key={key}
            from={getter(item.a)}
            to={getter(item.b)}
            trimA={isBox ? ([wa / 2 + 0.03, half + 0.03] as const) : half + 0.03}
            trimB={isBox ? ([wb / 2 + 0.03, half + 0.03] as const) : half + 0.03}
            color={item.hot ? toneFill("win") : INK.edge}
            width={item.hot ? 0.07 : 0.05}
            exiting={exiting}
          />
        );
      })}

      {presentNodes.map(({ key, item, exiting }) => {
        const p = at(item.id);
        const w = widthOf(item.v);
        return (
          <Block
            key={key}
            x={p.x}
            y={p.y}
            w={w}
            h={isBox ? BOX_H : NODE_D}
            d={0.4}
            shape={isBox ? "box" : "ball"}
            tone={item.tone}
            text={item.v}
            textSize={isBox ? 0.32 : 0.4}
            exiting={exiting}
            spawn={[0, 0.5, 0.9]}
            register={register(item.id)}
          >
            {item.badge !== undefined && !exiting && <Badge text={item.badge} x={w / 2 - 0.06} y={half * 0.72} />}
            {item.end && <Ring radius={NODE_D / 2 + 0.1} color={toneFill("good")} />}
          </Block>
        );
      })}

      {ptrs.map((p) => {
        if (!byId.has(p.at)) return null;
        const pos = at(p.at);
        return (
          <Tag
            key={p.name}
            name={p.name}
            x={pos.x}
            y={pos.y + half}
            level={levels.get(p.name) ?? 0}
            step={PTR_STEP}
            color={POINTER_COLORS[Math.max(0, m.ptrNames.indexOf(p.name)) % POINTER_COLORS.length]}
          />
        );
      })}
      {/* a heap or tree that exists but holds nothing yet */}
      {view && nodes.length === 0 && <Empty />}
    </group>
  );
}
