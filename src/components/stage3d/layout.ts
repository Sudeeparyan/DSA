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
import { textWidth } from "./theme";

/**
 * Stage planning.
 *
 * Before a lesson plays we look at *every* step and work out how much room
 * each structure will ever need.  Each structure then gets a fixed slot, so
 * nothing jumps around and the camera never has to re-frame mid-lesson.
 *
 * Units: 1 = the width of a normal array cell.
 */

export const TITLE_H = 0.7;
export const TITLE_SIZE = 0.27;
const GAP_X = 1.3;
const GAP_Y = 1.25;
/** widest a single structure may get before its own contents wrap */
const ROW_BUDGET = 15;

// ---- shared sizes ---------------------------------------------------------

export const CELL = 1;
export const CELL_GAP = 0.13;
export const PTR_STEP = 0.56;
export const PTR_BASE = 0.62;
export const BAR_MAX = 3.3;
export const SLAB_H = 0.62;
export const ENTRY_H = 0.8;
/** room for the arrow between a key and its value */
export const MAP_ARROW = 0.44;
export const NODE_D = 0.96;
export const LEVEL_H = 1.6;
/** recursion trees use flat boxes, so their levels can sit closer together */
export const LEVEL_H_BOX = 1.18;
export const LIST_NODE_H = 0.86;
export const TILE = 0.92;
export const TILE_GAP = 0.09;
export const BIT = 0.66;
export const BIT_GAP = 0.07;
export const LANE_H = 0.62;

const VALUE_SIZE = 0.42;

function chars(text: string): number {
  return [...text].length;
}

function widthFor(maxChars: number, min: number, size = VALUE_SIZE, pad = 0.34): number {
  return Math.max(min, textWidth("x".repeat(maxChars), size) + pad);
}

// ---- per-view metrics -----------------------------------------------------

export interface ArrayMetrics {
  kind: "array";
  w: number;
  h: number;
  /** largest number of cells the array ever has */
  n: number;
  cellW: number;
  pitch: number;
  bars: boolean;
  barMax: number;
  ptrNames: string[];
  topH: number;
  bodyH: number;
  ghostL: boolean;
  ghostR: boolean;
  idx: boolean;
  hasRanges: boolean;
}

export interface MapMetrics {
  kind: "map";
  w: number;
  h: number;
  keyW: number;
  valW: number;
  entryW: number;
  perRow: number;
}

export interface StackMetrics {
  kind: "stack";
  w: number;
  h: number;
  slabW: number;
  shape: "stack" | "queue" | "calls";
}

export interface ItemsMetrics {
  kind: "items";
  w: number;
  h: number;
  itemW: number;
  perRow: number;
}

export interface ListMetrics {
  kind: "list";
  w: number;
  h: number;
  nodeW: number;
  pitchX: number;
  pitchY: number;
  ptrNames: string[];
  ptrZone: number;
  cols: number;
  rows: number;
  hasNull: boolean;
  labelW: number;
}

export interface TreeMetrics {
  kind: "tree";
  w: number;
  h: number;
  ptrNames: string[];
  topH: number;
}

export interface GraphMetrics {
  kind: "graph";
  w: number;
  h: number;
  cx: number;
  cy: number;
}

export interface GridMetrics {
  kind: "grid";
  w: number;
  h: number;
  rows: number;
  cols: number;
  /** room under the grid for the cursor legend */
  legendH: number;
  cellW: number;
  rowLabelW: number;
  colLabelH: number;
  ptrNames: string[];
}

export interface IntervalsMetrics {
  kind: "intervals";
  w: number;
  h: number;
  labelW: number;
  axisW: number;
  min: number;
  max: number;
  lanes: Record<string, number>;
  order: string[];
}

export interface BitsMetrics {
  kind: "bits";
  w: number;
  h: number;
  labelW: number;
  valueW: number;
  width: number;
  rows: number;
}

export type Metrics =
  | ArrayMetrics
  | MapMetrics
  | StackMetrics
  | ItemsMetrics
  | ListMetrics
  | TreeMetrics
  | GraphMetrics
  | GridMetrics
  | IntervalsMetrics
  | BitsMetrics;

export interface Slot {
  id: string;
  title?: string;
  /** centre of the content area (the title sits above it) */
  x: number;
  y: number;
  w: number;
  h: number;
  m: Metrics;
}

export interface StagePlan {
  slots: Slot[];
  byId: Map<string, Slot>;
  w: number;
  h: number;
}

function orderedNames(snaps: { ptrs?: { name: string }[] }[]): string[] {
  const names: string[] = [];
  for (const s of snaps) for (const p of s.ptrs ?? []) if (!names.includes(p.name)) names.push(p.name);
  return names;
}

function maxStack(snaps: { ptrs?: { name: string; at: number | null }[] }[]): number {
  let best = 0;
  for (const s of snaps) {
    const count = new Map<number | null, number>();
    for (const p of s.ptrs ?? []) count.set(p.at, (count.get(p.at) ?? 0) + 1);
    for (const c of count.values()) best = Math.max(best, c);
  }
  return best;
}

function ptrZone(levels: number): number {
  return levels > 0 ? PTR_BASE + levels * PTR_STEP : 0;
}

// ---- array ----------------------------------------------------------------

function measureArray(snaps: ArrayView[]): ArrayMetrics {
  let n = 0;
  let maxChars = 1;
  let barMax = 1;
  let ghostL = false;
  let ghostR = false;
  let hasRanges = false;
  let bars = false;
  let idx = true;
  for (const s of snaps) {
    n = Math.max(n, s.cells.length);
    for (const c of s.cells) maxChars = Math.max(maxChars, chars(c.v));
    for (const p of s.ptrs ?? []) {
      if (p.at < 0) ghostL = true;
      if (p.at >= s.cells.length) ghostR = true;
    }
    if (s.ranges?.length) hasRanges = true;
    if (s.bars) bars = true;
    if (s.max) barMax = Math.max(barMax, s.max);
    if (s.idx === false) idx = false;
  }
  const cellW = bars ? Math.max(0.9, widthFor(maxChars, 0.9, 0.34)) : widthFor(maxChars, CELL);
  const pitch = cellW + CELL_GAP;
  const slots = Math.max(n, 1) + (ghostL ? 1 : 0) + (ghostR ? 1 : 0);
  const topH = ptrZone(maxStack(snaps));
  const bodyH = bars ? BAR_MAX + 0.2 : CELL;
  const bottom = (bars ? 0.56 : 0) + (idx ? 0.44 : 0.1) + (hasRanges ? 0.74 : 0);
  return {
    kind: "array",
    w: Math.max(slots * pitch - CELL_GAP, 3),
    h: topH + bodyH + bottom,
    n: Math.max(n, 1),
    cellW,
    pitch,
    bars,
    barMax,
    ptrNames: orderedNames(snaps),
    topH,
    bodyH,
    ghostL,
    ghostR,
    idx,
    hasRanges,
  };
}

// ---- map / items ----------------------------------------------------------

function measureMap(snaps: MapView[]): MapMetrics {
  let keyChars = 1;
  let valChars = 0;
  let count = 0;
  for (const s of snaps) {
    count = Math.max(count, s.entries.length);
    for (const e of s.entries) {
      keyChars = Math.max(keyChars, chars(e.k));
      if (e.v !== undefined) valChars = Math.max(valChars, chars(e.v), 1);
    }
  }
  const keyW = widthFor(keyChars, 0.9, 0.38);
  const valW = valChars ? widthFor(valChars, 0.9, 0.38) : 0;
  const entryW = keyW + (valW ? valW + MAP_ARROW : 0);
  const perRow = Math.max(1, Math.min(Math.max(count, 1), Math.floor((ROW_BUDGET + 0.24) / (entryW + 0.24))));
  const rows = Math.max(1, Math.ceil(count / perRow));
  return {
    kind: "map",
    w: Math.max(perRow * (entryW + 0.24) - 0.24, 3.4),
    h: rows * (ENTRY_H + 0.2) - 0.2,
    keyW,
    valW,
    entryW,
    perRow,
  };
}

function measureItems(snaps: ItemsView[]): ItemsMetrics {
  let maxChars = 1;
  let count = 0;
  for (const s of snaps) {
    count = Math.max(count, s.items.length);
    for (const i of s.items) maxChars = Math.max(maxChars, chars(i.v));
  }
  const itemW = widthFor(maxChars, 1, 0.34, 0.4);
  const perRow = Math.max(1, Math.min(Math.max(count, 1), Math.floor((ROW_BUDGET + 0.2) / (itemW + 0.2))));
  const rows = Math.max(1, Math.ceil(count / perRow));
  return {
    kind: "items",
    w: Math.max(perRow * (itemW + 0.2) - 0.2, 3.4),
    h: rows * (SLAB_H + 0.18) - 0.18,
    itemW,
    perRow,
  };
}

// ---- stack / queue --------------------------------------------------------

function measureStack(snaps: StackView[]): StackMetrics {
  let maxChars = 1;
  let count = 0;
  for (const s of snaps) {
    count = Math.max(count, s.items.length);
    for (const i of s.items) maxChars = Math.max(maxChars, chars(i.v));
  }
  const shape = snaps[0].kind;
  const slabW = widthFor(maxChars, shape === "queue" ? 1 : 1.5, 0.36, 0.44);
  if (shape === "queue") {
    return {
      kind: "stack",
      w: Math.max(Math.max(count, 1) * (slabW + 0.12) - 0.12, 3.6),
      h: SLAB_H + 0.75,
      slabW,
      shape,
    };
  }
  return {
    kind: "stack",
    w: Math.max(slabW + (shape === "stack" ? 2.2 : 0.4), 3.6),
    h: Math.max(count, 2) * (SLAB_H + 0.07) + 0.3,
    slabW,
    shape,
  };
}

// ---- linked list ----------------------------------------------------------

function measureList(snaps: ListView[]): ListMetrics {
  let cols = 1;
  let rows = 1;
  let maxChars = 1;
  let hasNull = false;
  let hasArc = false;
  let labelChars = 0;
  for (const s of snaps) {
    const byId = new Map(s.nodes.map((n) => [n.id, n]));
    for (const n of s.nodes) {
      cols = Math.max(cols, n.x + 1);
      rows = Math.max(rows, n.y + 1);
      maxChars = Math.max(maxChars, chars(n.v));
      const next = n.next !== undefined ? byId.get(n.next) : undefined;
      if (next && next.y === n.y && Math.abs(next.x - n.x) !== 1) hasArc = true;
      if (n.rand !== undefined) hasArc = true;
    }
    for (const p of s.ptrs ?? []) if (p.at === null) hasNull = true;
    for (const label of s.rows ?? []) labelChars = Math.max(labelChars, chars(label));
  }
  const nodeW = widthFor(maxChars, 1.05, 0.4, 0.44);
  const pitchX = nodeW + 0.95;
  const zone = ptrZone(maxStack(snaps));
  const pitchY = zone + LIST_NODE_H + (hasArc ? 1.25 : 0.45);
  const labelW = labelChars ? textWidth("x".repeat(labelChars), 0.24) + 0.5 : 0;
  const slots = cols + (hasNull ? 1 : 0);
  return {
    kind: "list",
    w: Math.max(labelW + slots * pitchX - 0.5, 3.6),
    h: rows * pitchY,
    nodeW,
    pitchX,
    pitchY,
    ptrNames: orderedNames(snaps),
    ptrZone: zone,
    cols,
    rows,
    hasNull,
    labelW,
  };
}

// ---- trees ----------------------------------------------------------------

export interface TreeLayout {
  pos: Map<number, { x: number; y: number; w: number }>;
  w: number;
  h: number;
}

const PHANTOM = -1;

export function treeNodeWidth(view: TreeView, label: string): number {
  if (view.shape === "box") return Math.max(1, textWidth(label, 0.32) + 0.46);
  return NODE_D;
}

/** Tidy top-down layout: every subtree gets a span as wide as it needs. */
export function layoutTree(view: TreeView): TreeLayout {
  const byId = new Map(view.nodes.map((n) => [n.id, n]));
  const gap = view.shape === "box" ? 0.34 : 0.42;
  const levelH = view.shape === "box" ? LEVEL_H_BOX : LEVEL_H;
  const span = new Map<number, number>();
  const own = new Map<number, number>();
  const kidsOf = (id: number): number[] => {
    const n = byId.get(id);
    if (!n) return [];
    if (n.kids) return n.kids.filter((k) => byId.has(k));
    const l = n.l !== undefined && byId.has(n.l) ? n.l : undefined;
    const r = n.r !== undefined && byId.has(n.r) ? n.r : undefined;
    if (l !== undefined && r !== undefined) return [l, r];
    if (l !== undefined) return [l, PHANTOM];
    if (r !== undefined) return [PHANTOM, r];
    return [];
  };
  const seen = new Set<number>();
  const measure = (id: number): number => {
    if (id === PHANTOM) return NODE_D * 0.5;
    if (seen.has(id)) return 0;
    seen.add(id);
    const node = byId.get(id)!;
    const self = treeNodeWidth(view, node.v) + (node.badge ? 0.5 : 0);
    own.set(id, self);
    const kids = kidsOf(id);
    let total = 0;
    kids.forEach((k, i) => {
      total += measure(k) + (i ? gap : 0);
    });
    const s = Math.max(self, total);
    span.set(id, s);
    return s;
  };
  const pos = new Map<number, { x: number; y: number; w: number }>();
  let depthMax = 0;
  const placed = new Set<number>();
  const assign = (id: number, left: number, depth: number): void => {
    if (id === PHANTOM || placed.has(id)) return;
    placed.add(id);
    const s = span.get(id) ?? NODE_D;
    const node = byId.get(id)!;
    pos.set(id, { x: left + s / 2, y: -depth * levelH, w: treeNodeWidth(view, node.v) });
    depthMax = Math.max(depthMax, depth);
    const kids = kidsOf(id);
    let total = 0;
    kids.forEach((k, i) => {
      total += (k === PHANTOM ? NODE_D * 0.5 : (span.get(k) ?? NODE_D)) + (i ? gap : 0);
    });
    let cursor = left + (s - total) / 2;
    for (const k of kids) {
      const ks = k === PHANTOM ? NODE_D * 0.5 : (span.get(k) ?? NODE_D);
      assign(k, cursor, depth + 1);
      cursor += ks + gap;
    }
  };
  let cursor = 0;
  for (const root of view.roots) {
    if (!byId.has(root)) continue;
    const s = measure(root);
    assign(root, cursor, 0);
    cursor += s + 1.1;
  }
  const width = Math.max(cursor - 1.1, NODE_D);
  // centre horizontally on 0
  for (const p of pos.values()) p.x -= width / 2;
  return { pos, w: width, h: depthMax * levelH + NODE_D };
}

/** True when `view` only contains nodes and links that also exist in `last`. */
function isSubTree(view: TreeView, last: TreeView): boolean {
  const final = new Map(last.nodes.map((n) => [n.id, n]));
  for (const n of view.nodes) {
    const f = final.get(n.id);
    if (!f) return false;
    if (n.kids) {
      for (const k of n.kids) if (!f.kids?.includes(k)) return false;
    } else {
      if (n.l !== undefined && n.l !== f.l) return false;
      if (n.r !== undefined && n.r !== f.r) return false;
    }
  }
  return true;
}

/**
 * Layout for one step of a tree.  A tree that only grows (a recursion tree, a
 * trie, a tree under construction) is laid out as its finished self, so every
 * node appears in its final place instead of shuffling as siblings arrive.
 */
export function stableTreeLayout(view: TreeView, last?: TreeView, lastLayout?: TreeLayout): TreeLayout {
  if (last && lastLayout && last !== view && isSubTree(view, last)) return lastLayout;
  return layoutTree(view);
}

function measureTree(snaps: TreeView[]): TreeMetrics {
  let w = NODE_D;
  let h = NODE_D;
  for (const s of snaps) {
    const layout = layoutTree(s);
    w = Math.max(w, layout.w);
    h = Math.max(h, layout.h);
  }
  const topH = ptrZone(maxStack(snaps));
  return {
    kind: "tree",
    w: Math.max(w + 1.1, 3.6),
    h: h + topH + 0.25,
    ptrNames: orderedNames(snaps),
    topH,
  };
}

// ---- graph ----------------------------------------------------------------

function measureGraph(snaps: GraphView[]): GraphMetrics {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (const s of snaps) {
    for (const n of s.nodes) {
      minX = Math.min(minX, n.x);
      maxX = Math.max(maxX, n.x);
      minY = Math.min(minY, n.y);
      maxY = Math.max(maxY, n.y);
    }
  }
  if (!Number.isFinite(minX)) minX = maxX = minY = maxY = 0;
  return {
    kind: "graph",
    w: Math.max(maxX - minX + 2.6, 3.6),
    h: maxY - minY + 2.1,
    cx: (minX + maxX) / 2,
    cy: (minY + maxY) / 2,
  };
}

// ---- grid -----------------------------------------------------------------

function measureGrid(snaps: GridView[]): GridMetrics {
  let rows = 1;
  let cols = 1;
  let maxChars = 1;
  let rowLabelChars = 0;
  let hasCols = false;
  for (const s of snaps) {
    rows = Math.max(rows, s.cells.length);
    for (const row of s.cells) {
      cols = Math.max(cols, row.length);
      for (const c of row) maxChars = Math.max(maxChars, chars(c.v));
    }
    for (const label of s.rows ?? []) rowLabelChars = Math.max(rowLabelChars, chars(label));
    if (s.cols) hasCols = true;
  }
  const cellW = widthFor(maxChars, TILE, 0.4, 0.3);
  const rowLabelW = rowLabelChars ? textWidth("x".repeat(rowLabelChars), 0.3) + 0.45 : 0;
  const colLabelH = hasCols ? 0.62 : 0;
  const ptrNames = orderedNames(snaps);
  const legendH = ptrNames.length ? 0.56 : 0;
  return {
    kind: "grid",
    w: Math.max(rowLabelW + cols * (cellW + TILE_GAP) - TILE_GAP, 3),
    h: colLabelH + rows * (TILE + TILE_GAP) - TILE_GAP + legendH,
    rows,
    cols,
    legendH,
    cellW,
    rowLabelW,
    colLabelH,
    ptrNames,
  };
}

// ---- intervals ------------------------------------------------------------

/** Put overlapping intervals on separate lanes (first fit). */
export function packLanes(items: { a: number; b: number }[]): number[] {
  const ends: number[] = [];
  const lanes: number[] = [];
  const order = items.map((_, i) => i).sort((p, q) => items[p].a - items[q].a || p - q);
  for (const i of order) {
    let lane = ends.findIndex((end) => end < items[i].a);
    if (lane === -1) {
      lane = ends.length;
      ends.push(items[i].b);
    } else {
      ends[lane] = items[i].b;
    }
    lanes[i] = lane;
  }
  return lanes;
}

function measureIntervals(snaps: IntervalsView[]): IntervalsMetrics {
  const lanes: Record<string, number> = {};
  const order: string[] = [];
  let labelChars = 1;
  let min = Infinity;
  let max = -Infinity;
  for (const s of snaps) {
    if (s.min !== undefined) min = Math.min(min, s.min);
    if (s.max !== undefined) max = Math.max(max, s.max);
    for (const row of s.rows) {
      if (!order.includes(row.label)) order.push(row.label);
      labelChars = Math.max(labelChars, chars(row.label));
      const used = row.items.length ? Math.max(...packLanes(row.items)) + 1 : 1;
      lanes[row.label] = Math.max(lanes[row.label] ?? 1, used);
    }
  }
  if (!Number.isFinite(min)) {
    min = 0;
    max = 1;
  }
  if (max === min) max = min + 1;
  const labelW = textWidth("x".repeat(labelChars), 0.26) + 0.5;
  const axisW = Math.min(14, Math.max(9, (max - min) * 0.72));
  let h = 0.95;
  for (const key of order) h += lanes[key] * (LANE_H + 0.1) + 0.42;
  return { kind: "intervals", w: labelW + axisW + 0.6, h, labelW, axisW, min, max, lanes, order };
}

// ---- bits -----------------------------------------------------------------

function measureBits(snaps: BitsView[]): BitsMetrics {
  let rows = 1;
  let width = 1;
  let labelChars = 1;
  let valueChars = 1;
  for (const s of snaps) {
    rows = Math.max(rows, s.rows.length);
    for (const r of s.rows) {
      width = Math.max(width, r.bits.length);
      labelChars = Math.max(labelChars, chars(r.label));
      valueChars = Math.max(valueChars, chars(r.v));
    }
  }
  const labelW = textWidth("x".repeat(labelChars), 0.28) + 0.4;
  const valueW = textWidth("x".repeat(valueChars + 2), 0.3) + 0.3;
  return {
    kind: "bits",
    w: labelW + width * (BIT + BIT_GAP) + valueW,
    h: rows * (BIT + 0.24) + 0.45,
    labelW,
    valueW,
    width,
    rows,
  };
}

// ---- putting the stage together -------------------------------------------

function measure(snaps: SceneView[]): Metrics {
  const first = snaps[0];
  switch (first.t) {
    case "array":
      return measureArray(snaps as ArrayView[]);
    case "map":
      return measureMap(snaps as MapView[]);
    case "stack":
      return measureStack(snaps as StackView[]);
    case "items":
      return measureItems(snaps as ItemsView[]);
    case "list":
      return measureList(snaps as ListView[]);
    case "tree":
      return measureTree(snaps as TreeView[]);
    case "graph":
      return measureGraph(snaps as GraphView[]);
    case "grid":
      return measureGrid(snaps as GridView[]);
    case "intervals":
      return measureIntervals(snaps as IntervalsView[]);
    case "bits":
      return measureBits(snaps as BitsView[]);
  }
}

interface Item {
  id: string;
  title?: string;
  m: Metrics;
  w: number;
  h: number;
}

/** Fill rows left to right; a row is closed when the next structure would not fit. */
function packRows(items: Item[], budget: number): { rows: Item[][]; w: number; h: number } {
  const rows: Item[][] = [];
  let used = 0;
  for (const item of items) {
    const row = rows[rows.length - 1];
    if (row && used + GAP_X + item.w <= budget + 1e-6) {
      row.push(item);
      used += GAP_X + item.w;
    } else {
      rows.push([item]);
      used = item.w;
    }
  }
  let w = 0;
  let h = 0;
  for (const row of rows) {
    w = Math.max(w, row.reduce((sum, i) => sum + i.w, 0) + GAP_X * (row.length - 1));
    h += Math.max(...row.map((i) => i.h));
  }
  return { rows, w, h: h + GAP_Y * (rows.length - 1) };
}

/** Extra room the camera leaves around the stage (panel borders, pop-out). */
export const STAGE_PAD_W = 1.7;
export const STAGE_PAD_H = 1.7;

/**
 * Decide where every structure of a lesson goes.  `aspect` is the shape of the
 * canvas (width / height): rows are wrapped so the stage fills it as well as
 * possible, which keeps the pieces as large as they can be.
 */
export function planStage(steps: Step[], aspect = 1.6): StagePlan {
  const order: string[] = [];
  const snaps = new Map<string, SceneView[]>();
  for (const step of steps) {
    for (const view of step.views) {
      if (!isSceneView(view)) continue;
      if (!snaps.has(view.id)) {
        snaps.set(view.id, []);
        order.push(view.id);
      }
      snaps.get(view.id)!.push(view);
    }
  }

  const items: Item[] = order.map((id) => {
    const list = snaps.get(id)!;
    const m = measure(list);
    const title = list.find((v) => v.title)?.title;
    const w = Math.max(m.w, title ? textWidth(title, TITLE_SIZE) - 0.5 : 0);
    return { id, title, m, w, h: m.h + (title ? TITLE_H : 0) };
  });
  if (items.length === 0) return { slots: [], byId: new Map(), w: 1, h: 1 };

  // every width a run of neighbouring structures can have is a candidate row width
  const widest = Math.max(...items.map((i) => i.w));
  const budgets = new Set<number>([widest]);
  for (let i = 0; i < items.length; i++) {
    let w = 0;
    for (let j = i; j < items.length; j++) {
      w += items[j].w + (j > i ? GAP_X : 0);
      if (w >= widest) budgets.add(w);
    }
  }
  let best = packRows(items, widest);
  let bestScale = 0;
  for (const budget of [...budgets].sort((a, b) => a - b)) {
    const packed = packRows(items, budget);
    const scale = Math.min(aspect / (packed.w + STAGE_PAD_W), 1 / (packed.h + STAGE_PAD_H));
    if (scale > bestScale * 1.02) {
      best = packed;
      bestScale = scale;
    }
  }

  const slots: Slot[] = [];
  let y = 0;
  for (const row of best.rows) {
    const rowW = row.reduce((sum, i) => sum + i.w, 0) + GAP_X * (row.length - 1);
    const rowH = Math.max(...row.map((i) => i.h));
    let x = -rowW / 2;
    for (const item of row) {
      const titleH = item.title ? TITLE_H : 0;
      // structures in a row are top-aligned, each under its own title
      slots.push({
        id: item.id,
        title: item.title,
        x: x + item.w / 2,
        y: y - titleH - item.m.h / 2,
        w: item.w,
        h: item.m.h,
        m: item.m,
      });
      x += item.w + GAP_X;
    }
    y -= rowH + GAP_Y;
  }
  for (const slot of slots) slot.y += best.h / 2;

  return { slots, byId: new Map(slots.map((s) => [s.id, s])), w: Math.max(best.w, 1), h: Math.max(best.h, 1) };
}
