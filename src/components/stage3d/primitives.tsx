"use client";

import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useReducer,
  useRef,
  type ReactNode,
} from "react";
import { useFrame } from "@react-three/fiber";
import { Text } from "@react-three/drei";
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/examples/jsm/geometries/RoundedBoxGeometry.js";
import { TITLE_H, TITLE_SIZE } from "./layout";
import { FONT, INK, fitSize, glyphs, isHot, textWidth, toneStyle } from "./theme";

/**
 * Building blocks of the 3D stage.
 *
 * Every piece eases toward its target (position, colour, size) on each frame,
 * so a change between two lesson steps is always shown as motion, never a jump.
 */

/** Time constant of the easing in seconds; 0 switches all motion off. */
export const motion = { tau: 0.085 };

/** Fraction of the remaining distance to cover this frame. */
function ease(dt: number, scale = 1): number {
  const tau = motion.tau * scale;
  if (tau <= 0) return 1;
  return 1 - Math.exp(-Math.min(dt, 0.1) / tau);
}

// ---- shared geometry ------------------------------------------------------

const boxCache = new Map<string, THREE.BufferGeometry>();

export function roundedBox(w: number, h: number, d: number, r = 0.13): THREE.BufferGeometry {
  const key = `${w.toFixed(3)}|${h.toFixed(3)}|${d.toFixed(3)}|${r.toFixed(3)}`;
  let geo = boxCache.get(key);
  if (!geo) {
    const radius = Math.max(0.01, Math.min(r, w / 2, h / 2, d / 2) * 0.98);
    geo = new RoundedBoxGeometry(w, h, d, 3, radius);
    boxCache.set(key, geo);
  }
  return geo;
}

const ballCache = new Map<string, THREE.BufferGeometry>();

function ball(radius: number): THREE.BufferGeometry {
  const key = radius.toFixed(3);
  let geo = ballCache.get(key);
  if (!geo) {
    geo = new THREE.SphereGeometry(radius, 40, 28);
    ballCache.set(key, geo);
  }
  return geo;
}

let unitBox: THREE.BufferGeometry | null = null;
let unitCylinder: THREE.BufferGeometry | null = null;
let unitCone: THREE.BufferGeometry | null = null;
let unitPlane: THREE.BufferGeometry | null = null;
let glowTexture: THREE.Texture | null = null;

function box(): THREE.BufferGeometry {
  unitBox ??= new THREE.BoxGeometry(1, 1, 1);
  return unitBox;
}

function cylinder(): THREE.BufferGeometry {
  unitCylinder ??= new THREE.CylinderGeometry(1, 1, 1, 12);
  return unitCylinder;
}

function cone(): THREE.BufferGeometry {
  unitCone ??= new THREE.ConeGeometry(1, 1, 18);
  return unitCone;
}

function plane(): THREE.BufferGeometry {
  unitPlane ??= new THREE.PlaneGeometry(1, 1);
  return unitPlane;
}

function glowMap(): THREE.Texture {
  if (!glowTexture) {
    const canvas = document.createElement("canvas");
    canvas.width = canvas.height = 128;
    const g = canvas.getContext("2d")!;
    const grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0, "rgba(255,255,255,0.9)");
    grad.addColorStop(0.45, "rgba(255,255,255,0.3)");
    grad.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = grad;
    g.fillRect(0, 0, 128, 128);
    glowTexture = new THREE.CanvasTexture(canvas);
  }
  return glowTexture;
}

/** Round nodes are slightly flattened spheres, so their label sits on the surface. */
const BALL_FLAT = 0.62;

const noRaycast = () => null;
const UP = new THREE.Vector3(0, 1, 0);
const tmpDir = new THREE.Vector3();
const tmpA = new THREE.Vector3();
const tmpB = new THREE.Vector3();
const tmpC = new THREE.Vector3();

// ---- text -----------------------------------------------------------------

export function Label({
  text,
  size = 0.3,
  color = "#f1f5fb",
  x = 0,
  y = 0,
  z = 0,
  anchorX = "center",
  anchorY = "middle",
}: {
  text: string;
  size?: number;
  color?: string;
  x?: number;
  y?: number;
  z?: number;
  anchorX?: "left" | "center" | "right";
  anchorY?: "top" | "middle" | "bottom";
}) {
  return (
    <Text
      font={FONT}
      fontSize={size}
      color={color}
      position={[x, y, z]}
      anchorX={anchorX}
      anchorY={anchorY}
      raycast={noRaycast}
    >
      {glyphs(text)}
    </Text>
  );
}

/** Children glide to (x, y, z) instead of jumping there. */
export function Glide({
  x,
  y,
  z = 0,
  children,
}: {
  x: number;
  y: number;
  z?: number;
  children: ReactNode;
}) {
  const group = useRef<THREE.Group>(null);
  useLayoutEffect(() => {
    group.current!.position.set(x, y, z);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useFrame((_, dt) => {
    group.current?.position.lerp(tmpC.set(x, y, z), ease(dt));
  });
  return <group ref={group}>{children}</group>;
}

// ---- block: the basic solid piece (array cell, node, slab, tile) ----------

export interface BlockProps {
  x: number;
  y: number;
  z?: number;
  w: number;
  h: number;
  d?: number;
  tone?: string;
  text?: string;
  /** largest font size; shrinks automatically for long text */
  textSize?: number;
  shape?: "box" | "ball";
  radius?: number;
  /** highlighted pieces pop toward the viewer unless this is false */
  lift?: boolean;
  exiting?: boolean;
  /** where a new piece flies in from, relative to its place */
  spawn?: [number, number, number];
  /** receives the live position so edges can follow this piece */
  register?: (pos: THREE.Vector3 | null) => void;
  children?: ReactNode;
}

export function Block({
  x,
  y,
  z = 0,
  w,
  h,
  d = 0.5,
  tone,
  text,
  textSize = 0.42,
  shape = "box",
  radius = 0.13,
  lift = true,
  exiting = false,
  spawn,
  register,
  children,
}: BlockProps) {
  const style = toneStyle(tone);
  const group = useRef<THREE.Group>(null);
  const pulse = useRef(0);
  const mounted = useRef(false);
  const hot = lift && isHot(tone);

  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: style.fill,
        emissive: style.emissive,
        emissiveIntensity: style.glow * 0.5,
        roughness: 0.48,
        metalness: 0.04,
      }),
    // created once: colours are eased toward their targets every frame
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );
  const halo = useMemo(
    () =>
      new THREE.MeshBasicMaterial({
        map: glowMap(),
        color: style.emissive,
        transparent: true,
        opacity: 0,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
        toneMapped: false,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );
  const target = useMemo(
    () => ({ fill: new THREE.Color(style.fill), emissive: new THREE.Color(style.emissive) }),
    [style.fill, style.emissive],
  );

  useLayoutEffect(() => {
    const g = group.current!;
    const s = spawn ?? [0, 0.25, 1.2];
    if (motion.tau > 0) {
      g.position.set(x + s[0], y + s[1], z + s[2]);
      g.scale.setScalar(0.001);
    } else {
      g.position.set(x, y, z);
    }
    register?.(g.position);
    return () => {
      register?.(null);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(
    () => () => {
      material.dispose();
      halo.dispose();
    },
    [material, halo],
  );

  useEffect(() => {
    if (!mounted.current) {
      mounted.current = true;
      return;
    }
    pulse.current = 1; // a little "pop" whenever the value or colour changes
  }, [tone, text]);

  useFrame((_, dt) => {
    const g = group.current;
    if (!g) return;
    const a = ease(dt);
    g.position.lerp(tmpC.set(x, y, z + (hot ? 0.3 : 0)), a);
    pulse.current = Math.max(0, pulse.current - dt * 2.8);
    const s = exiting ? 0.001 : 1 + Math.sin(pulse.current * Math.PI) * 0.16;
    g.scale.lerp(tmpC.set(s, s, s), ease(dt, exiting ? 0.6 : 0.8));
    material.color.lerp(target.fill, a);
    material.emissive.lerp(target.emissive, a);
    material.emissiveIntensity += (style.glow * 0.5 - material.emissiveIntensity) * a;
    halo.opacity += ((exiting ? 0 : style.glow * 0.85) - halo.opacity) * a;
    halo.color.lerp(target.emissive, a);
  });

  const isBall = shape === "ball";
  const depth = isBall ? w * BALL_FLAT : d;
  // the glow reaches the same distance on every side, set by the shorter side, so a long
  // slab (a call-stack frame, a wide label) does not throw light far outside its panel
  const haloPad = Math.min(w, h) * 1.2 + 0.5;
  const label = text === undefined ? "" : glyphs(text);
  const size = label ? fitSize(label, (isBall ? w * 0.8 : w) - 0.16, textSize) : textSize;

  return (
    <group ref={group}>
      <mesh
        geometry={isBall ? ball(w / 2) : roundedBox(w, h, d, radius)}
        material={material}
        scale={isBall ? [1, 1, BALL_FLAT] : undefined}
        castShadow
        receiveShadow
        raycast={noRaycast}
      />
      <mesh
        geometry={plane()}
        material={halo}
        position={[0, 0, -depth / 2 - 0.06]}
        scale={[w + haloPad, h + haloPad, 1]}
        raycast={noRaycast}
      />
      {label !== "" && (
        <Text
          font={FONT}
          fontSize={size}
          color={style.text}
          position={[0, 0, depth / 2 + 0.015]}
          anchorX="center"
          anchorY="middle"
          raycast={noRaycast}
        >
          {label}
        </Text>
      )}
      {children}
    </group>
  );
}

/** A small note attached to a piece (a return value, a distance, a count). */
export function Badge({ text, x, y, z = 0.3 }: { text: string; x: number; y: number; z?: number }) {
  const label = glyphs(text);
  const w = Math.max(0.42, textWidth(label, 0.23) + 0.22);
  return (
    <group position={[x + w / 2, y, z]}>
      <mesh geometry={roundedBox(w, 0.4, 0.12, 0.1)} raycast={noRaycast}>
        <meshStandardMaterial color="#f1f5fb" roughness={0.6} />
      </mesh>
      <Label text={label} size={0.23} color="#101622" z={0.07} />
    </group>
  );
}

/** A ring around a piece (marks the end of a word in a trie). */
export function Ring({ radius, color }: { radius: number; color: string }) {
  return (
    <mesh raycast={noRaycast}>
      <torusGeometry args={[radius, 0.04, 10, 44]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.4} roughness={0.4} />
    </mesh>
  );
}

// ---- slab: a plain plate whose position and size ease (trays, water) ------

export function Slab({
  x,
  y,
  z = 0,
  w,
  h,
  d = 0.1,
  color,
  opacity = 1,
  glow = 0,
  visible = true,
}: {
  x: number;
  y: number;
  z?: number;
  w: number;
  h: number;
  d?: number;
  color: string;
  opacity?: number;
  glow?: number;
  visible?: boolean;
}) {
  const ref = useRef<THREE.Mesh>(null);
  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: glow,
        roughness: 0.5,
        transparent: true,
        opacity: 0,
        depthWrite: opacity >= 1,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );
  const target = useMemo(() => new THREE.Color(color), [color]);
  useEffect(() => () => material.dispose(), [material]);
  useLayoutEffect(() => {
    const m = ref.current!;
    m.position.set(x, y, z);
    m.scale.set(Math.max(w, 0.001), Math.max(h, 0.001), d);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useFrame((_, dt) => {
    const m = ref.current;
    if (!m) return;
    const a = ease(dt);
    m.position.lerp(tmpC.set(x, y, z), a);
    m.scale.lerp(tmpC.set(Math.max(w, 0.001), Math.max(h, 0.001), d), a);
    material.opacity += ((visible ? opacity : 0) - material.opacity) * a;
    material.color.lerp(target, a);
    material.emissive.lerp(target, a);
    m.visible = material.opacity > 0.012;
  });
  return <mesh ref={ref} geometry={box()} material={material} raycast={noRaycast} />;
}

/** A rectangular outline that glides from cell to cell (grid cursor). */
export function Frame({
  x,
  y,
  z = 0.5,
  w,
  h,
  color,
  thickness = 0.075,
}: {
  x: number;
  y: number;
  z?: number;
  w: number;
  h: number;
  color: string;
  thickness?: number;
}) {
  const t = thickness;
  return (
    <Glide x={x} y={y} z={z}>
      {(
        [
          [0, h / 2, w + t, t],
          [0, -h / 2, w + t, t],
          [-w / 2, 0, t, h + t],
          [w / 2, 0, t, h + t],
        ] as const
      ).map(([px, py, sx, sy], i) => (
        <mesh key={i} geometry={box()} position={[px, py, 0]} scale={[sx, sy, t]} raycast={noRaycast}>
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.55} roughness={0.4} />
        </mesh>
      ))}
    </Glide>
  );
}

// ---- pointer tag: a named arrow that glides between cells / nodes ---------

export function Tag({
  x,
  y,
  z = 0.36,
  name,
  color,
  level = 0,
  step = 0.56,
}: {
  x: number;
  /** y of the surface the arrow touches */
  y: number;
  z?: number;
  name: string;
  color: string;
  /** 0 = touching the target; higher levels stack above it */
  level?: number;
  step?: number;
}) {
  const group = useRef<THREE.Group>(null);
  const ty = y + 0.53 + level * step;
  useLayoutEffect(() => {
    const g = group.current!;
    g.position.set(x, ty + (motion.tau > 0 ? 0.6 : 0), z);
    if (motion.tau > 0) g.scale.setScalar(0.001);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useFrame((_, dt) => {
    const g = group.current;
    if (!g) return;
    g.position.lerp(tmpC.set(x, ty, z), ease(dt, 0.9));
    g.scale.lerp(tmpC.set(1, 1, 1), ease(dt, 0.8));
  });
  const label = glyphs(name);
  const w = Math.max(0.62, textWidth(label, 0.25) + 0.3);
  return (
    <group ref={group}>
      <mesh geometry={roundedBox(w, 0.42, 0.16, 0.1)} castShadow raycast={noRaycast}>
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} roughness={0.4} />
      </mesh>
      <Label text={label} size={0.25} color="#171200" z={0.09} />
      {level === 0 && (
        <mesh
          geometry={cone()}
          position={[0, -0.34, 0]}
          rotation={[0, 0, Math.PI]}
          scale={[0.13, 0.26, 0.13]}
          castShadow
          raycast={noRaycast}
        >
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} roughness={0.4} />
        </mesh>
      )}
    </group>
  );
}

// ---- edges ----------------------------------------------------------------

export type PosGetter = () => THREE.Vector3 | undefined;
/** How far an edge stops short of a piece: a radius, or [halfWidth, halfHeight] of a box. */
export type Trim = number | readonly [number, number];

function trimDistance(trim: Trim, dir: THREE.Vector3): number {
  if (typeof trim === "number") return trim;
  const ax = Math.abs(dir.x);
  const ay = Math.abs(dir.y);
  const tx = ax > 1e-6 ? trim[0] / ax : Infinity;
  const ty = ay > 1e-6 ? trim[1] / ay : Infinity;
  return Math.min(tx, ty);
}

/**
 * A straight tube (optionally an arrow) between two pieces.  It follows them
 * as they move, and when it is re-pointed at another piece it swings over.
 */
export function Edge({
  from,
  to,
  trimA = 0,
  trimB = 0,
  color = INK.edge,
  arrow = false,
  width = 0.05,
  shift = 0,
  exiting = false,
}: {
  from: PosGetter;
  to: PosGetter;
  trimA?: Trim;
  trimB?: Trim;
  color?: string;
  arrow?: boolean;
  width?: number;
  /** sideways offset, used to separate a pair of opposite arrows */
  shift?: number;
  exiting?: boolean;
}) {
  const group = useRef<THREE.Group>(null);
  const shaft = useRef<THREE.Mesh>(null);
  const head = useRef<THREE.Mesh>(null);
  const ends = useRef<{ a: THREE.Vector3; b: THREE.Vector3; ready: boolean }>({
    a: new THREE.Vector3(),
    b: new THREE.Vector3(),
    ready: false,
  });
  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 0.2,
        roughness: 0.5,
        transparent: true,
        opacity: 0,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );
  const target = useMemo(() => new THREE.Color(color), [color]);
  useEffect(() => () => material.dispose(), [material]);

  useFrame((_, dt) => {
    const g = group.current;
    const a = from();
    const b = to();
    if (!g || !shaft.current) return;
    if (!a || !b) {
      g.visible = false;
      return;
    }
    const e = ends.current;
    if (!e.ready) {
      e.a.copy(a);
      e.b.copy(b);
      e.ready = true;
    } else {
      const k = ease(dt, 0.9);
      e.a.lerp(a, k);
      e.b.lerp(b, k);
    }
    tmpDir.subVectors(e.b, e.a);
    tmpDir.z = 0;
    const dist = tmpDir.length();
    if (dist < 1e-4) {
      g.visible = false;
      return;
    }
    tmpDir.divideScalar(dist);
    const ta = trimDistance(trimA, tmpDir);
    const tb = trimDistance(trimB, tmpDir);
    const headLen = arrow ? 0.3 : 0;
    const len = dist - ta - tb - headLen;
    if (len < 0.03) {
      g.visible = false;
      return;
    }
    g.visible = true;
    tmpA.set(e.a.x, e.a.y, 0).addScaledVector(tmpDir, ta);
    if (shift) {
      tmpA.x += -tmpDir.y * shift;
      tmpA.y += tmpDir.x * shift;
    }
    shaft.current.position.copy(tmpA).addScaledVector(tmpDir, len / 2);
    shaft.current.quaternion.setFromUnitVectors(UP, tmpDir);
    shaft.current.scale.set(width, len, width);
    if (head.current) {
      head.current.position.copy(tmpA).addScaledVector(tmpDir, len + headLen / 2);
      head.current.quaternion.copy(shaft.current.quaternion);
      head.current.scale.set(0.14, headLen, 0.14);
    }
    const k = ease(dt);
    material.color.lerp(target, k);
    material.emissive.lerp(target, k);
    material.opacity += ((exiting ? 0 : 1) - material.opacity) * ease(dt, 1.2);
  });

  return (
    <group ref={group} visible={false}>
      <mesh ref={shaft} geometry={cylinder()} material={material} castShadow raycast={noRaycast} />
      {arrow && <mesh ref={head} geometry={cone()} material={material} castShadow raycast={noRaycast} />}
    </group>
  );
}

/** A curved arrow between two fixed points (links that skip or go backwards). */
export function Arc({
  a,
  b,
  bend,
  color = INK.edge,
  width = 0.045,
  arrow = true,
}: {
  a: [number, number, number];
  b: [number, number, number];
  /** offset of the curve's control point from the straight line (sign picks the side) */
  bend: number;
  color?: string;
  width?: number;
  arrow?: boolean;
}) {
  const [ax, ay, az] = a;
  const [bx, by, bz] = b;
  const built = useMemo(() => {
    const start = new THREE.Vector3(ax, ay, az);
    const end = new THREE.Vector3(bx, by, bz);
    const mid = start.clone().add(end).multiplyScalar(0.5);
    mid.y += bend;
    const tangent = end.clone().sub(mid).normalize();
    const headLen = arrow ? 0.3 : 0;
    const tip = end.clone().addScaledVector(tangent, -headLen);
    const curve = new THREE.QuadraticBezierCurve3(start, mid, tip);
    const geometry = new THREE.TubeGeometry(curve, 28, width, 8, false);
    const headPos = tip.clone().addScaledVector(tangent, headLen / 2);
    const headQuat = new THREE.Quaternion().setFromUnitVectors(UP, tangent);
    return { geometry, headPos, headQuat, headLen };
  }, [ax, ay, az, bx, by, bz, bend, width, arrow]);
  useEffect(() => () => built.geometry.dispose(), [built]);

  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 0.2,
        roughness: 0.5,
        transparent: true,
        opacity: 0,
      }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );
  const target = useMemo(() => new THREE.Color(color), [color]);
  useEffect(() => () => material.dispose(), [material]);
  useFrame((_, dt) => {
    material.opacity += (1 - material.opacity) * ease(dt, 1.4);
    material.color.lerp(target, ease(dt));
    material.emissive.lerp(target, ease(dt));
  });

  return (
    <group>
      <mesh geometry={built.geometry} material={material} castShadow raycast={noRaycast} />
      {arrow && (
        <mesh
          geometry={cone()}
          material={material}
          position={built.headPos}
          quaternion={built.headQuat}
          scale={[0.14, built.headLen, 0.14]}
          castShadow
          raycast={noRaycast}
        />
      )}
    </group>
  );
}

/** A straight bar between two fixed points (axes, ticks, base plates). */
export function Bar({
  from,
  to,
  color = INK.edge,
  width = 0.04,
}: {
  from: [number, number, number];
  to: [number, number, number];
  color?: string;
  width?: number;
}) {
  const ref = useRef<THREE.Mesh>(null);
  const [ax, ay, az] = from;
  const [bx, by, bz] = to;
  useLayoutEffect(() => {
    const m = ref.current;
    if (!m) return;
    tmpA.set(ax, ay, az);
    tmpB.set(bx, by, bz);
    tmpDir.subVectors(tmpB, tmpA);
    const len = tmpDir.length() || 0.001;
    tmpDir.divideScalar(len);
    m.position.copy(tmpA).addScaledVector(tmpDir, len / 2);
    m.quaternion.setFromUnitVectors(UP, tmpDir);
    m.scale.set(width, len, width);
  }, [ax, ay, az, bx, by, bz, width]);
  return (
    <mesh ref={ref} geometry={cylinder()} raycast={noRaycast}>
      <meshStandardMaterial color={color} roughness={0.6} />
    </mesh>
  );
}

// ---- panel: the plate a structure sits on, with its name -------------------

export function Panel({ w, h, title }: { w: number; h: number; title?: string }) {
  const titleH = title ? TITLE_H : 0;
  return (
    <group>
      <mesh
        geometry={roundedBox(w + 1, h + titleH + 0.8, 0.16, 0.26)}
        position={[0, titleH / 2, -0.66]}
        receiveShadow
        raycast={noRaycast}
      >
        <meshLambertMaterial color={INK.panel} />
      </mesh>
      {title && (
        <Label
          text={title}
          size={TITLE_SIZE}
          color={INK.title}
          x={-w / 2 - 0.16}
          y={h / 2 + 0.42}
          z={-0.56}
          anchorX="left"
        />
      )}
    </group>
  );
}

/** Faint note shown in place of an empty structure. */
export function Empty({ text = "empty", y = 0 }: { text?: string; y?: number }) {
  return <Label text={text} size={0.26} color={INK.faint} y={y} z={-0.5} />;
}

// ---- presence: keep removed pieces around long enough to animate out -------

export interface Present<T> {
  key: string | number;
  item: T;
  /** position of the item in the live list (its last position while leaving) */
  index: number;
  exiting: boolean;
}

export function usePresence<T>(
  items: readonly T[],
  keyOf: (item: T, index: number) => string | number,
  ms = 240,
): Present<T>[] {
  const store = useRef({
    live: new Map<string | number, { item: T; index: number }>(),
    ghosts: new Map<string | number, { item: T; index: number; at: number }>(),
  });
  const [, tick] = useReducer((n: number) => n + 1, 0);
  const now = typeof performance !== "undefined" ? performance.now() : 0;
  const s = store.current;

  const current = new Map<string | number, { item: T; index: number }>();
  items.forEach((item, index) => current.set(keyOf(item, index), { item, index }));
  if (motion.tau > 0) {
    for (const [key, value] of s.live) {
      if (!current.has(key) && !s.ghosts.has(key)) s.ghosts.set(key, { ...value, at: now });
    }
  }
  for (const key of current.keys()) s.ghosts.delete(key);
  for (const [key, ghost] of s.ghosts) if (now - ghost.at > ms) s.ghosts.delete(key);
  s.live = current;

  const pending = s.ghosts.size;
  useEffect(() => {
    if (!pending) return;
    const id = setTimeout(tick, ms + 40);
    return () => clearTimeout(id);
  });

  const out: Present<T>[] = [];
  for (const [key, value] of current) out.push({ key, item: value.item, index: value.index, exiting: false });
  for (const [key, ghost] of s.ghosts) out.push({ key, item: ghost.item, index: ghost.index, exiting: true });
  return out;
}

// ---- live positions, so edges can follow moving pieces ---------------------

export function useRegistry<K>() {
  const map = useRef(new Map<K, THREE.Vector3>());
  const register = useCallback(
    (key: K) => (pos: THREE.Vector3 | null) => {
      if (pos) map.current.set(key, pos);
      else map.current.delete(key);
    },
    [],
  );
  const getter = useCallback((key: K): PosGetter => () => map.current.get(key), []);
  return { register, getter };
}

/** Stack several pointers that land on the same target: returns name -> level. */
export function pointerLevels<P extends { name: string }>(
  ptrs: readonly P[],
  targetOf: (p: P) => string | number,
): Map<string, number> {
  const count = new Map<string | number, number>();
  const levels = new Map<string, number>();
  for (const p of ptrs) {
    const key = targetOf(p);
    const level = count.get(key) ?? 0;
    levels.set(p.name, level);
    count.set(key, level + 1);
  }
  return levels;
}
