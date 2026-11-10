import type { Problem, AnimationStep } from "@/lib/schema";
import { getTracer, runTracer } from "@/lib/tracers";

function isStubSteps(steps: AnimationStep[]): boolean {
  if (steps.length < 5) return true;
  const blob = steps.map((s) => s.caption).join(" ");
  return /Start solving|see-leetcode|Green means done/i.test(blob);
}

/**
 * Single entry point for playable steps.
 * Specialty tracers win; rich authored cinema steps next; generic last.
 */
export function resolveAnimationSteps(
  problem: Problem,
  input: unknown = problem.animation.defaultInput,
): AnimationStep[] {
  const authored = problem.animation.steps;
  const id = problem.animation.tracerId;

  if (id && id !== "generic-array-scan" && id !== "authored" && getTracer(id)) {
    try {
      return runTracer(id, input) as AnimationStep[];
    } catch {
      /* fall through */
    }
  }

  if (!isStubSteps(authored)) {
    return authored;
  }

  if (id && getTracer(id)) {
    try {
      return runTracer(id, input) as AnimationStep[];
    } catch {
      /* ignore */
    }
  }

  return authored;
}

export function animationQualityReport(steps: AnimationStep[]): {
  ok: boolean;
  reasons: string[];
} {
  const reasons: string[] = [];
  if (steps.length < 5) reasons.push(`too-few-steps:${steps.length}`);
  if (isStubSteps(steps)) reasons.push("stub-captions");
  const caps = steps.map((s) => s.caption.trim()).filter(Boolean);
  if (caps.length !== steps.length) reasons.push("empty-caption");
  const hasVisual = steps.some((s) => {
    const st = s.state ?? {};
    return (
      Array.isArray(st.nums) ||
      Array.isArray(st.chars) ||
      Array.isArray(st.nodes) ||
      Array.isArray(st.grid) ||
      Array.isArray(st.table) ||
      Array.isArray(st.intervals) ||
      Array.isArray(st.bits) ||
      Array.isArray(st.heap) ||
      Array.isArray(st.path) ||
      (st.map && typeof st.map === "object") ||
      Array.isArray(st.seen) ||
      Array.isArray(st.stack)
    );
  });
  if (!hasVisual) reasons.push("no-visual-payload");
  const hl = steps.some(
    (s) =>
      s.state?.highlights &&
      typeof s.state.highlights === "object" &&
      Object.keys(s.state.highlights as object).length > 0,
  );
  if (!hl) reasons.push("no-highlights");
  return { ok: reasons.length === 0, reasons };
}
