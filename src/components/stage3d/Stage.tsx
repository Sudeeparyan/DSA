"use client";

import { useEffect, useMemo, useRef, useState, type ComponentRef } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import type {
  ArrayView,
  BitsView,
  GraphView,
  GridView,
  IntervalsView,
  ItemsView,
  ListView,
  MapView,
  SceneView,
  StackView,
  Step,
  TreeView,
} from "@/lib/lesson";
import { isSceneView } from "@/lib/lesson";
import { STAGE_PAD_H, STAGE_PAD_W, planStage, type Slot, type StagePlan } from "./layout";
import { Empty, Panel, motion } from "./primitives";
import { INK } from "./theme";
import { ArrayView3D } from "./views/ArrayView3D";
import { BitsView3D } from "./views/BitsView3D";
import { GraphView3D } from "./views/GraphView3D";
import { GridView3D } from "./views/GridView3D";
import { IntervalsView3D } from "./views/IntervalsView3D";
import { ListView3D } from "./views/ListView3D";
import { MapView3D } from "./views/MapView3D";
import { ItemsView3D, StackView3D } from "./views/StackView3D";
import { TreeView3D } from "./views/TreeView3D";

const FOV = 30;
/** Resting camera angle: a little above and to the side, so depth is visible. */
const PITCH = 0.17;
const YAW = -0.07;
/** the camera's angle down from straight above when it is at rest */
const REST_POLAR = Math.PI / 2 - PITCH;

function SlotView({
  slot,
  view,
  last,
  idle,
}: {
  slot: Slot;
  view?: SceneView;
  last?: SceneView;
  /** why the panel is blank at this step, when it is */
  idle?: string;
}) {
  const m = slot.m;
  return (
    <group position={[slot.x, slot.y, 0]}>
      <Panel w={slot.w} h={slot.h} title={slot.title} />
      {!view && idle && <Empty text={idle} />}
      {m.kind === "array" && <ArrayView3D view={view as ArrayView | undefined} m={m} />}
      {m.kind === "map" && <MapView3D view={view as MapView | undefined} m={m} />}
      {m.kind === "stack" && <StackView3D view={view as StackView | undefined} m={m} />}
      {m.kind === "items" && <ItemsView3D view={view as ItemsView | undefined} m={m} />}
      {m.kind === "list" && <ListView3D view={view as ListView | undefined} m={m} />}
      {m.kind === "tree" && (
        <TreeView3D view={view as TreeView | undefined} m={m} last={last as TreeView | undefined} />
      )}
      {m.kind === "graph" && <GraphView3D view={view as GraphView | undefined} m={m} />}
      {m.kind === "grid" && <GridView3D view={view as GridView | undefined} m={m} />}
      {m.kind === "intervals" && <IntervalsView3D view={view as IntervalsView | undefined} m={m} />}
      {m.kind === "bits" && <BitsView3D view={view as BitsView | undefined} m={m} />}
    </group>
  );
}

/** Frames the whole stage and lets the learner look around it. */
function CameraRig({
  plan,
  resetKey,
  zoom,
  touch,
  onMoved,
}: {
  plan: StagePlan;
  resetKey: number;
  zoom: boolean;
  /** a touch screen: up/down finger moves scroll the page, so the camera only turns sideways */
  touch: boolean;
  onMoved: () => void;
}) {
  const camera = useThree((s) => s.camera);
  const width = useThree((s) => s.size.width);
  const height = useThree((s) => s.size.height);
  const controls = useRef<ComponentRef<typeof OrbitControls>>(null);
  // a touch that turns into a page scroll starts the controls but never moves the camera,
  // so "moved" is only reported once the view really changes during a drag or pinch
  const dragging = useRef(false);

  const dist = useMemo(() => {
    const w = plan.w + STAGE_PAD_W;
    const h = plan.h + STAGE_PAD_H;
    const t = Math.tan(THREE.MathUtils.degToRad(FOV) / 2);
    const aspect = width / Math.max(height, 1);
    return Math.max(h / (2 * t), w / (2 * t * aspect)) * 1.02 + 0.9;
  }, [plan, width, height]);

  useEffect(() => {
    camera.position.set(
      Math.sin(YAW) * Math.cos(PITCH) * dist,
      Math.sin(PITCH) * dist,
      Math.cos(YAW) * Math.cos(PITCH) * dist,
    );
    camera.lookAt(0, 0, 0);
    const c = controls.current;
    if (c) {
      c.target.set(0, 0, 0);
      c.update();
    }
  }, [camera, dist, resetKey]);

  return (
    <OrbitControls
      ref={controls}
      enablePan={false}
      enableZoom={zoom}
      enableDamping
      dampingFactor={0.12}
      rotateSpeed={0.7}
      minDistance={dist * 0.35}
      maxDistance={dist * 1.5}
      minPolarAngle={touch ? REST_POLAR : Math.PI / 2 - 1.0}
      maxPolarAngle={touch ? REST_POLAR : Math.PI / 2 + 0.35}
      minAzimuthAngle={-1.0}
      maxAzimuthAngle={1.0}
      onStart={() => {
        dragging.current = true;
      }}
      onEnd={() => {
        dragging.current = false;
      }}
      onChange={() => {
        const c = controls.current;
        if (!c || !dragging.current) return;
        // only a real change of view counts, not the jitter of a finger that starts a page scroll
        const off =
          Math.abs(c.getAzimuthalAngle() - YAW) +
          Math.abs(c.getPolarAngle() - REST_POLAR) +
          Math.abs(c.getDistance() / dist - 1);
        if (off > 0.04) onMoved();
      }}
    />
  );
}

function Lights({ plan }: { plan: StagePlan }) {
  const w = plan.w + 4;
  const h = plan.h + 4;
  const s = Math.max(w, h) * 0.9 + 6;
  return (
    <>
      <ambientLight intensity={1.85} />
      <directionalLight
        castShadow
        position={[-s * 0.3, s * 0.48, s]}
        intensity={2.1}
        shadow-mapSize={[2048, 2048]}
        shadow-bias={-0.0004}
        shadow-normalBias={0.02}
      >
        <orthographicCamera attach="shadow-camera" args={[-w / 2, w / 2, h / 2, -h / 2, 0.1, s * 3]} />
      </directionalLight>
      <directionalLight position={[s * 0.6, -s * 0.1, s * 0.7]} intensity={0.5} color="#bcd3ff" />
    </>
  );
}

function webglAvailable(): boolean {
  try {
    const canvas = document.createElement("canvas");
    return !!(canvas.getContext("webgl2") || canvas.getContext("webgl"));
  } catch {
    return false;
  }
}

/**
 * The 3D stage.  It is given every step up front so it can reserve a fixed
 * place for each data structure, then shows the structures as they are at
 * step `index`; moving to another step animates the difference.
 */
export function Stage({ steps, index, reduced = false }: { steps: Step[]; index: number; reduced?: boolean }) {
  const frame = useRef<HTMLDivElement>(null);
  const [aspect, setAspect] = useState(1.6);
  const plan = useMemo(() => planStage(steps, aspect), [steps, aspect]);
  const lasts = useMemo(() => {
    const map = new Map<string, SceneView>();
    for (const step of steps) for (const view of step.views) if (isSceneView(view)) map.set(view.id, view);
    return map;
  }, [steps]);
  const current = useMemo(() => {
    const map = new Map<string, SceneView>();
    for (const view of steps[index]?.views ?? []) if (isSceneView(view)) map.set(view.id, view);
    return map;
  }, [steps, index]);
  // the first step each structure shows up in, to tell "not created yet" from "not in use right now"
  const firsts = useMemo(() => {
    const map = new Map<string, number>();
    steps.forEach((step, i) => {
      for (const view of step.views) if (isSceneView(view) && !map.has(view.id)) map.set(view.id, i);
    });
    return map;
  }, [steps]);

  const [supported, setSupported] = useState<boolean | null>(null);
  const [resetKey, setResetKey] = useState(0);
  const [moved, setMoved] = useState(false);
  const [engaged, setEngaged] = useState(false);

  useEffect(() => setSupported(webglAvailable()), []);
  const [touch, setTouch] = useState(false);
  useEffect(() => {
    const query = window.matchMedia("(pointer: coarse)");
    const update = () => setTouch(query.matches);
    update();
    query.addEventListener("change", update);
    return () => query.removeEventListener("change", update);
  }, []);
  // re-plan the stage when the canvas changes shape (window resize, phone rotation)
  useEffect(() => {
    const el = frame.current;
    if (!el) return;
    const update = () => {
      const box = el.getBoundingClientRect();
      if (box.height < 1) return;
      const next = box.width / box.height;
      setAspect((a) => (Math.abs(next - a) > 0.06 ? next : a));
    };
    update();
    const observer = new ResizeObserver(update);
    observer.observe(el);
    return () => observer.disconnect();
  }, [supported]);
  useEffect(() => {
    motion.tau = reduced ? 0 : 0.085;
  }, [reduced]);

  if (supported === false) {
    return (
      <div className="stage-fallback">
        The 3D stage needs WebGL, which this browser has switched off. The explanation, code and variables
        below still work.
      </div>
    );
  }

  return (
    <div
      ref={frame}
      className="stage-frame"
      onPointerDown={() => setEngaged(true)}
      onPointerLeave={() => setEngaged(false)}
    >
      {supported && (
        <Canvas
          flat
          shadows="percentage"
          dpr={[1, 2]}
          camera={{ fov: FOV, near: 0.1, far: 400, position: [0, 0, 40] }}
          gl={{ antialias: true, powerPreference: "high-performance" }}
          role="img"
          aria-label="3D picture of the data at this step. The caption under it says what is happening."
        >
          <color attach="background" args={[INK.wall]} />
          <Lights plan={plan} />
          <mesh position={[0, 0, -0.9]} receiveShadow>
            <planeGeometry args={[plan.w + 120, plan.h + 120]} />
            <meshLambertMaterial color={INK.wall} />
          </mesh>
          {plan.slots.map((slot) => (
            <SlotView
              key={slot.id}
              slot={slot}
              view={current.get(slot.id)}
              last={lasts.get(slot.id)}
              idle={index < (firsts.get(slot.id) ?? 0) ? "not created yet" : "not in use right now"}
            />
          ))}
          <CameraRig
            plan={plan}
            resetKey={resetKey}
            zoom={engaged}
            touch={touch}
            onMoved={() => setMoved(true)}
          />
        </Canvas>
      )}
      <div className="stage-hint">
        {moved ? (
          <button
            type="button"
            onClick={() => {
              setResetKey((k) => k + 1);
              setMoved(false);
            }}
          >
            Reset view
          </button>
        ) : (
          <>
            <span className="hint-mouse">drag to rotate · click, then scroll to zoom</span>
            <span className="hint-touch">swipe sideways to rotate · pinch to zoom</span>
          </>
        )}
      </div>
    </div>
  );
}
