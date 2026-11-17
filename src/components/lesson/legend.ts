import { TONE_LEGEND } from "@/components/stage3d/theme";
import type { Step } from "@/lib/lesson";

/** One entry of the colour legend under the stage. */
export interface LegendEntry {
  tone: string;
  label: string;
}

/** Every tone (named, or a #rrggbb colour) that a lesson's steps draw. */
export function tonesUsed(steps: Step[]): Set<string> {
  const used = new Set<string>();
  const visit = (node: unknown) => {
    if (Array.isArray(node)) node.forEach(visit);
    else if (node && typeof node === "object") {
      for (const [key, value] of Object.entries(node)) {
        if (key === "tone" && typeof value === "string") used.add(value);
        else visit(value);
      }
    }
  };
  for (const step of steps) visit(step.views);
  return used;
}

/**
 * The legend for a lesson: its own colours first (land, water, …), then the standard tones it
 * draws. A lesson may rename a standard tone where it means something more specific there.
 */
export function legendFor(steps: Step[], key: readonly LegendEntry[] = []): LegendEntry[] {
  const used = tonesUsed(steps);
  const renamed = new Map(key.map((entry) => [entry.tone, entry.label]));
  const own = key.filter((entry) => entry.tone.startsWith("#") && used.has(entry.tone));
  const standard = TONE_LEGEND.filter((entry) => used.has(entry.tone)).map((entry) => ({
    tone: entry.tone,
    label: renamed.get(entry.tone) ?? entry.label,
  }));
  return [...own, ...standard];
}
