/**
 * Visual language of the 3D stage.
 *
 * Colours carry meaning and mean the same thing in every lesson, so a learner
 * only has to learn them once.
 */

export const FONT = "/fonts/IBMPlexMono-SemiBold.ttf";

/** Advance width of the bundled monospace font, as a fraction of font size. */
export const CHAR = 0.6;

export interface ToneStyle {
  fill: string;
  emissive: string;
  /** strength of the halo behind the block (0 = none) */
  glow: number;
  text: string;
}

export const BASE_TONE: ToneStyle = {
  fill: "#36435a",
  emissive: "#000000",
  glow: 0,
  text: "#f1f5fb",
};

const TONES: Record<string, ToneStyle> = {
  cur: { fill: "#f7b731", emissive: "#f59f00", glow: 0.6, text: "#241800" },
  alt: { fill: "#b69cff", emissive: "#7950f2", glow: 0.45, text: "#170a38" },
  good: { fill: "#3fcf8e", emissive: "#0ca678", glow: 0.45, text: "#032318" },
  bad: { fill: "#ff7a70", emissive: "#f03e3e", glow: 0.45, text: "#350706" },
  seen: { fill: "#5eabf8", emissive: "#1c7ed6", glow: 0.18, text: "#04162d" },
  win: { fill: "#3bd6c6", emissive: "#0c8599", glow: 0.22, text: "#03231f" },
  mark: { fill: "#ff9f45", emissive: "#f76707", glow: 0.28, text: "#2c1300" },
  dim: { fill: "#222b3b", emissive: "#000000", glow: 0, text: "#8290a8" },
};

/** Legend shown under the stage (only the tones a lesson really uses). */
export const TONE_LEGEND: { tone: string; label: string }[] = [
  { tone: "cur", label: "looking at now" },
  { tone: "alt", label: "compared with" },
  { tone: "good", label: "match / answer" },
  { tone: "bad", label: "rejected" },
  { tone: "seen", label: "visited / remembered" },
  { tone: "win", label: "current range / path" },
  { tone: "mark", label: "queued / flagged" },
  { tone: "dim", label: "no longer needed" },
];

function luminance(hex: string): number {
  const n = parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
}

export function toneStyle(tone?: string): ToneStyle {
  if (!tone) return BASE_TONE;
  if (tone.startsWith("#")) {
    return {
      fill: tone,
      emissive: "#000000",
      glow: 0,
      text: luminance(tone) > 0.55 ? "#101622" : "#f1f5fb",
    };
  }
  return TONES[tone] ?? BASE_TONE;
}

export function toneFill(tone: string): string {
  return toneStyle(tone).fill;
}

/** Tones that should pop toward the viewer. */
export function isHot(tone?: string): boolean {
  return tone === "cur" || tone === "alt" || tone === "good" || tone === "bad";
}

/** Colours for pointer arrows, by order of first appearance in a view. */
export const POINTER_COLORS = [
  "#f7b731",
  "#b69cff",
  "#3bd6c6",
  "#ff9f45",
  "#f783ac",
  "#74c0fc",
];

export const INK = {
  title: "#9fb0c9",
  faint: "#66758f",
  edge: "#8799b8",
  edgeHot: "#3bd6c6",
  panel: "#172135",
  wall: "#0b1019",
  water: "#3aa0ff",
};

/** The glyphs the bundled font can draw; anything else is swapped out. */
const GLYPH_FIX: Record<string, string> = {
  "∅": "ø",
  "␣": "·",
  "▶": ">",
  "✗": "x",
  "“": '"',
  "”": '"',
  "‘": "'",
  "’": "'",
  "—": "-",
  "–": "-",
};

export function glyphs(text: string): string {
  let out = "";
  for (const ch of text) out += GLYPH_FIX[ch] ?? ch;
  return out;
}

export function textWidth(text: string, size: number): number {
  return [...text].length * CHAR * size;
}

/** Largest font size (up to `base`) at which `text` fits in `width`. */
export function fitSize(text: string, width: number, base: number): number {
  const n = Math.max(1, [...text].length);
  return Math.min(base, width / (n * CHAR));
}
