"use client";

import type { MapView } from "@/lib/lesson";
import { ENTRY_H, MAP_ARROW, type MapMetrics } from "../layout";
import { Block, Empty, Glide, Label, usePresence } from "../primitives";
import { INK } from "../theme";

/** A hash map (key → value tiles) or a hash set (key tiles only). */
export function MapView3D({ view, m }: { view?: MapView; m: MapMetrics }) {
  const entries = view?.entries ?? [];
  const present = usePresence(entries, (e) => e.k);

  const stepX = m.entryW + 0.24;
  const stepY = ENTRY_H + 0.2;
  const left = -(m.perRow * stepX - 0.24) / 2;
  const top = m.h / 2;

  return (
    <group>
      {present.map(({ key, item, index, exiting }) => {
        const x0 = left + (index % m.perRow) * stepX;
        const y = top - Math.floor(index / m.perRow) * stepY - ENTRY_H / 2;
        return (
          <group key={key}>
            <Block
              x={x0 + m.keyW / 2}
              y={y}
              w={m.keyW}
              h={ENTRY_H}
              d={0.44}
              tone={item.tone}
              text={item.k}
              textSize={0.38}
              exiting={exiting}
              spawn={[0, 0.9, 0.6]}
            />
            {item.v !== undefined && (
              <>
                {!exiting && (
                  <Glide x={x0 + m.keyW + MAP_ARROW / 2} y={y} z={-0.2}>
                    <Label text="→" size={0.3} color={INK.title} />
                  </Glide>
                )}
                <Block
                  x={x0 + m.keyW + MAP_ARROW + m.valW / 2}
                  y={y}
                  w={m.valW}
                  h={ENTRY_H}
                  d={0.44}
                  tone={item.tone}
                  text={item.v}
                  textSize={0.38}
                  exiting={exiting}
                  spawn={[0, 0.9, 0.6]}
                />
              </>
            )}
          </group>
        );
      })}
      {view && entries.length === 0 && <Empty />}
    </group>
  );
}
