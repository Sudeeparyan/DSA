"use client";

import type { MapView } from "@/lib/lesson";
import { ENTRY_H, MAP_ARROW, type MapMetrics } from "../layout";
import { Block, Empty, Glide, Label, usePresence } from "../primitives";
import { INK } from "../theme";

/**
 * A hash map (key → value tiles) or a hash set (key tiles only).  Each key → value pair sits on
 * its own card, so a row of pairs cannot be misread as "0 11" belonging together.
 */
export function MapView3D({ view, m }: { view?: MapView; m: MapMetrics }) {
  const entries = view?.entries ?? [];
  const present = usePresence(entries, (e) => e.k);

  const stepX = m.entryW + m.gap;
  const stepY = ENTRY_H + m.rowGap;
  const left = -(m.perRow * stepX - m.gap) / 2;
  const top = m.h / 2;

  return (
    <group>
      {present.map(({ key, item, index, exiting }) => {
        const x0 = left + (index % m.perRow) * stepX;
        const y = top - Math.floor(index / m.perRow) * stepY - ENTRY_H / 2;
        return (
          <group key={key}>
            {item.v !== undefined && (
              <Block
                x={x0 + m.entryW / 2}
                y={y}
                z={-0.3}
                w={m.entryW + 0.24}
                h={ENTRY_H + 0.2}
                d={0.1}
                radius={0.12}
                tone={INK.card}
                lift={false}
                exiting={exiting}
                spawn={[0, 0.9, 0.6]}
              />
            )}
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
                  <Glide x={x0 + m.keyW + MAP_ARROW / 2} y={y} z={0.05}>
                    <Label text="→" size={0.32} color={INK.title} />
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
