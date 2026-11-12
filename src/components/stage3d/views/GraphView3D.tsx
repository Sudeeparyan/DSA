"use client";

import type { GraphView } from "@/lib/lesson";
import { NODE_D, type GraphMetrics } from "../layout";
import { Badge, Block, Edge, Label, usePresence, useRegistry } from "../primitives";
import { INK, toneFill } from "../theme";

/** Nodes and edges, with optional weights on edges and notes beside nodes. */
export function GraphView3D({ view, m }: { view?: GraphView; m: GraphMetrics }) {
  const nodes = view?.nodes ?? [];
  const edges = view?.edges ?? [];
  const presentNodes = usePresence(nodes, (n) => n.id);
  const presentEdges = usePresence(edges, (e) => `${e.a}>${e.b}`);
  const { register, getter } = useRegistry<string>();

  const byId = new Map(nodes.map((n) => [n.id, n]));
  const pairs = new Set(edges.map((e) => `${e.a}>${e.b}`));
  const px = (x: number) => x - m.cx;
  const py = (y: number) => y - m.cy;
  const trim = NODE_D / 2 + 0.05;

  return (
    <group>
      {presentEdges.map(({ key, item, exiting }) => {
        const twoWay = !!view?.directed && pairs.has(`${item.b}>${item.a}`);
        return (
          <Edge
            key={key}
            from={getter(item.a)}
            to={getter(item.b)}
            trimA={trim}
            trimB={trim}
            arrow={!!view?.directed}
            color={item.tone ? toneFill(item.tone) : INK.edge}
            width={item.tone ? 0.075 : 0.05}
            shift={twoWay ? 0.13 : 0}
            exiting={exiting}
          />
        );
      })}

      {/* edge weights sit beside the middle of their edge */}
      {edges.map((e) => {
        const a = byId.get(e.a);
        const b = byId.get(e.b);
        if (e.w === undefined || !a || !b) return null;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const len = Math.hypot(dx, dy) || 1;
        const twoWay = !!view?.directed && pairs.has(`${e.b}>${e.a}`);
        const off = twoWay ? 0.42 : 0.3;
        return (
          <Label
            key={`w-${e.a}>${e.b}`}
            text={e.w}
            size={0.27}
            color={e.tone ? toneFill(e.tone) : INK.title}
            x={px((a.x + b.x) / 2) + (-dy / len) * off}
            y={py((a.y + b.y) / 2) + (dx / len) * off}
            z={0.05}
          />
        );
      })}

      {presentNodes.map(({ key, item, exiting }) => (
        <Block
          key={key}
          x={px(item.x)}
          y={py(item.y)}
          w={NODE_D}
          h={NODE_D}
          shape="ball"
          tone={item.tone}
          text={item.v}
          textSize={0.4}
          exiting={exiting}
          spawn={[0, 0.4, 1]}
          register={register(item.id)}
        >
          {item.badge !== undefined && !exiting && <Badge text={item.badge} x={NODE_D / 2 - 0.08} y={NODE_D * 0.36} />}
        </Block>
      ))}
    </group>
  );
}
