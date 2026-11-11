/**
 * Shared animation-state contract used by 2D scenes and the 3D Answer Stage.
 * Keep payloads small and serializable (JSON-friendly) so content scripts and
 * specialty tracers can both emit them.
 */

export type HighlightKind =
  | "current"
  | "matched"
  | "rejected"
  | "remembered"
  | "done"
  | string;

export interface AnimationState {
  /** Primary linear stage values (array / nodes / chars / bits / heap). */
  nums?: unknown[];
  chars?: unknown[];
  nodes?: unknown[];
  bits?: number[];
  heap?: unknown[];
  path?: unknown[];
  visible?: unknown[];
  input?: unknown;
  /** Memory structures */
  seen?: unknown[];
  map?: Record<string, unknown>;
  stack?: unknown[];
  /** Spatial structures */
  grid?: unknown[][];
  table?: unknown[][];
  intervals?: number[][];
  edges?: unknown[];
  /** Pointers / focus */
  currentIndex?: number | null;
  currentValue?: unknown;
  target?: unknown;
  needed?: unknown;
  cell?: [number, number] | number[];
  pointers?: Record<string, number>;
  word?: string;
  /** Result + highlights */
  result?: unknown;
  highlights?: Record<string, HighlightKind>;
  [key: string]: unknown;
}

export function readPrimaryValues(state: AnimationState): unknown[] {
  if (Array.isArray(state.nums)) return state.nums;
  if (Array.isArray(state.chars)) return state.chars;
  if (Array.isArray(state.nodes)) return state.nodes;
  if (Array.isArray(state.bits)) return state.bits;
  if (Array.isArray(state.heap)) return state.heap;
  if (Array.isArray(state.path)) return state.path;
  if (Array.isArray(state.input)) return state.input as unknown[];
  return [];
}

export function readMemoryShelf(state: AnimationState): unknown[] {
  if (Array.isArray(state.seen)) return state.seen;
  if (state.map && typeof state.map === "object") {
    return Object.entries(state.map).map(([k, v]) => `${k}→${v}`);
  }
  if (Array.isArray(state.stack)) return state.stack;
  if (Array.isArray(state.path)) return state.path;
  if (Array.isArray(state.visible)) return state.visible;
  if (Array.isArray(state.heap)) return state.heap;
  return [];
}

export function readHighlights(
  state: AnimationState,
): Record<string, HighlightKind> {
  return (state.highlights ?? {}) as Record<string, HighlightKind>;
}

export function hasMatchHighlight(state: AnimationState): boolean {
  return Object.values(readHighlights(state)).includes("matched");
}
