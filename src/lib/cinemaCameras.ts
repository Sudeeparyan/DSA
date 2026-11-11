/**
 * Cinematic camera paths adapted from blender-skills:
 * turntable, crane-shot, slow-zoom, dolly-rotate, dynamic-full-loop.
 */

export type CinemaShot =
  | "crane"
  | "slowZoom"
  | "dollyRotate"
  | "turntable"
  | "whip"
  | "hero";

export interface CameraPose {
  position: [number, number, number];
  lookAt: [number, number, number];
  fov: number;
}

function lerp(a: number, b: number, t: number) {
  return a + (b - a) * t;
}

function easeInOut(t: number) {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

function easeOutCubic(t: number) {
  return 1 - Math.pow(1 - t, 3);
}

/** Local beat progress 0..1 inside a shot. */
export function poseForShot(
  shot: CinemaShot,
  tRaw: number,
  focus: [number, number, number] = [0, 0.4, 0],
): CameraPose {
  const t = Math.min(1, Math.max(0, tRaw));
  const [fx, fy, fz] = focus;

  switch (shot) {
    case "crane": {
      // Low → high reveal (crane-shot skill)
      const e = easeInOut(t);
      const height = lerp(-0.2, 3.2, e);
      const dist = lerp(3.2, 4.4, e);
      const fov = lerp(48, 38, e);
      return {
        position: [fx + 1.1, height, fz - dist],
        lookAt: [fx, fy, fz],
        fov,
      };
    }
    case "slowZoom": {
      // Push-in + lens tighten (slow-zoom skill)
      const e = easeInOut(t);
      const dist = lerp(4.2, 2.0, e);
      const height = lerp(2.6, 1.2, e);
      const fov = lerp(42, 58, e);
      return {
        position: [fx + 1.4, height, fz - dist],
        lookAt: [fx, fy + 0.15, fz],
        fov,
      };
    }
    case "dollyRotate": {
      // Forward + orbit (dolly-rotate skill)
      const e = easeInOut(t);
      const angle = lerp(0.35, -0.9, e); // ~90° sweep feel
      const dist = lerp(4.0, 2.6, e);
      const height = lerp(2.1, 1.5, e);
      return {
        position: [
          fx + Math.sin(angle) * dist,
          height,
          fz + Math.cos(angle) * dist,
        ],
        lookAt: [fx, fy, fz],
        fov: lerp(40, 48, e),
      };
    }
    case "turntable": {
      // Constant orbit (turntable / perfect-loop — LINEAR feel)
      const angle = t * Math.PI * 2;
      const dist = 4.2;
      const height = 2.0;
      return {
        position: [
          fx + Math.sin(angle) * dist,
          height,
          fz + Math.cos(angle) * dist,
        ],
        lookAt: [fx, fy, fz],
        fov: 45,
      };
    }
    case "whip": {
      // Speed-ramp whip toward a face (dynamic-full-loop)
      const e = easeOutCubic(t);
      const angle = lerp(0, Math.PI * 0.85, e);
      const dist = lerp(4.0, 2.3, e);
      return {
        position: [
          fx + Math.sin(angle) * dist,
          lerp(1.8, 1.3, e),
          fz + Math.cos(angle) * dist,
        ],
        lookAt: [fx, fy + 0.2, fz],
        fov: lerp(45, 55, e),
      };
    }
    case "hero":
    default: {
      return {
        position: [fx + 2.2, 2.4, fz + 3.6],
        lookAt: [fx, fy, fz],
        fov: 42,
      };
    }
  }
}

export function shotForAlgoMoment(opts: {
  index: number;
  total: number;
  matched?: boolean;
  starting?: boolean;
}): CinemaShot {
  if (opts.starting) return "crane";
  if (opts.matched) return "whip";
  if (opts.index === 0) return "slowZoom";
  if (opts.index >= opts.total - 1) return "turntable";
  return opts.index % 2 === 0 ? "dollyRotate" : "slowZoom";
}
