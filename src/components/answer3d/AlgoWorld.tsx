"use client";

import { useMemo, useRef } from "react";
import { Text } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import type { Group, Mesh } from "three";

type Highlight = string;

const HIGHLIGHT: Record<string, string> = {
  current: "#ffd43b",
  matched: "#51cf66",
  rejected: "#ff6b6b",
  remembered: "#74c0fc",
  done: "#2ec4a8",
};

function Cell({
  value,
  index,
  highlight,
  x,
  z = 0,
  size = 0.72,
}: {
  value: unknown;
  index: number;
  highlight?: Highlight;
  x: number;
  z?: number;
  size?: number;
}) {
  const mesh = useRef<Mesh>(null);
  const color = highlight ? HIGHLIGHT[highlight] ?? "#2ec4a8" : "#1a2a24";
  const emissive = highlight ? color : "#000000";

  useFrame((_, dt) => {
    if (!mesh.current) return;
    const targetY =
      highlight === "current" || highlight === "matched" ? 0.55 : 0.35;
    mesh.current.position.y +=
      (targetY - mesh.current.position.y) * Math.min(1, dt * 8);
    const targetScale = highlight === "matched" ? 1.12 : 1;
    mesh.current.scale.x +=
      (targetScale - mesh.current.scale.x) * Math.min(1, dt * 6);
    mesh.current.scale.y = mesh.current.scale.x;
    mesh.current.scale.z = mesh.current.scale.x;
  });

  return (
    <group position={[x, 0, z]}>
      <mesh ref={mesh} position={[0, 0.35, 0]} castShadow>
        <boxGeometry args={[size, size, size]} />
        <meshStandardMaterial
          color={color}
          emissive={emissive}
          emissiveIntensity={highlight ? 0.45 : 0.05}
          metalness={0.35}
          roughness={0.35}
        />
      </mesh>
      <Text
        position={[0, 0.35, size / 2 + 0.02]}
        fontSize={Math.min(0.28, size * 0.4)}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
      >
        {String(value)}
      </Text>
      <Text
        position={[0, -0.12, size / 2 + 0.02]}
        fontSize={0.12}
        color="#9aa89a"
        anchorX="center"
        anchorY="middle"
      >
        {String(index)}
      </Text>
    </group>
  );
}

function ShelfItem({
  value,
  index,
  total,
}: {
  value: unknown;
  index: number;
  total: number;
}) {
  const ref = useRef<Group>(null);
  const spacing = 0.7;
  const start = -((total - 1) * spacing) / 2;

  useFrame((_, dt) => {
    if (!ref.current) return;
    ref.current.rotation.y += dt * 0.6;
  });

  return (
    <group ref={ref} position={[start + index * spacing, 1.35, -1.6]}>
      <mesh castShadow>
        <boxGeometry args={[0.5, 0.5, 0.5]} />
        <meshStandardMaterial
          color="#74c0fc"
          emissive="#1c7ed6"
          emissiveIntensity={0.35}
          metalness={0.4}
          roughness={0.3}
        />
      </mesh>
      <Text
        position={[0, 0, 0.28]}
        fontSize={0.18}
        color="#041018"
        anchorX="center"
        anchorY="middle"
      >
        {String(value)}
      </Text>
    </group>
  );
}

export function AlgoWorld({
  nums,
  seen,
  highlights,
  grid,
  intervals,
  bits,
}: {
  nums: unknown[];
  seen: unknown[];
  highlights: Record<string, string>;
  grid?: unknown[][];
  intervals?: number[][];
  bits?: number[];
}) {
  const values = bits?.length ? bits : nums;
  const spacing = values.length > 8 ? 0.7 : 0.95;
  const start = useMemo(
    () => -((Math.max(values.length, 1) - 1) * spacing) / 2,
    [values.length, spacing],
  );

  return (
    <group>
      <mesh position={[0, -0.35, 0]} receiveShadow>
        <cylinderGeometry args={[2.8, 3.1, 0.35, 48]} />
        <meshStandardMaterial color="#121a16" metalness={0.5} roughness={0.45} />
      </mesh>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.17, 0]}
        receiveShadow
      >
        <circleGeometry args={[2.7, 48]} />
        <meshStandardMaterial color="#0b7a6f" metalness={0.2} roughness={0.7} />
      </mesh>

      {/* Primary row */}
      {values.map((v, i) => (
        <Cell
          key={`n-${i}`}
          value={v}
          index={i}
          x={start + i * spacing}
          highlight={highlights[String(i)]}
          size={values.length > 8 ? 0.55 : 0.72}
        />
      ))}

      {/* Optional grid plane behind */}
      {grid && grid.length > 0 && (
        <group position={[0, 1.6, -1.9]}>
          {grid.map((row, r) =>
            row.map((cell, c) => (
              <mesh
                key={`g-${r}-${c}`}
                position={[
                  (c - (row.length - 1) / 2) * 0.45,
                  -(r - (grid.length - 1) / 2) * 0.45,
                  0,
                ]}
              >
                <boxGeometry args={[0.38, 0.38, 0.12]} />
                <meshStandardMaterial
                  color={
                    String(cell) === "0" || cell === 0 ? "#24302a" : "#2ec4a8"
                  }
                  emissive="#0b7a6f"
                  emissiveIntensity={0.15}
                />
              </mesh>
            )),
          )}
          <Text position={[0, grid.length * 0.28, 0]} fontSize={0.16} color="#9aa89a">
            grid
          </Text>
        </group>
      )}

      {/* Intervals as bars */}
      {intervals && intervals.length > 0 && (
        <group position={[0, 1.5, -1.7]}>
          {intervals.map((iv, i) => {
            const a = Number(iv[0]);
            const b = Number(iv[1]);
            const width = Math.max(0.3, (b - a) * 0.15);
            return (
              <mesh key={`iv-${i}`} position={[((a + b) / 2 - 5) * 0.15, -i * 0.28, 0]}>
                <boxGeometry args={[width, 0.18, 0.18]} />
                <meshStandardMaterial
                  color={highlights[String(i)] ? "#ffd43b" : "#ff8a3d"}
                  emissive="#d4550a"
                  emissiveIntensity={0.2}
                />
              </mesh>
            );
          })}
          <Text position={[0, 0.55, 0]} fontSize={0.16} color="#9aa89a">
            intervals
          </Text>
        </group>
      )}

      {/* Memory shelf */}
      <mesh position={[0, 1.1, -1.6]} receiveShadow>
        <boxGeometry
          args={[Math.max(2.4, seen.length * 0.75 + 1.2), 0.12, 0.7]}
        />
        <meshStandardMaterial color="#1a2430" metalness={0.3} roughness={0.5} />
      </mesh>
      <Text position={[0, 1.85, -1.6]} fontSize={0.18} color="#9aa89a" anchorX="center">
        memory shelf
      </Text>
      {seen.map((v, i) => (
        <ShelfItem
          key={`s-${i}-${String(v)}`}
          value={v}
          index={i}
          total={seen.length}
        />
      ))}
    </group>
  );
}
