export const CATEGORY_ACCENTS: Record<string, string> = {
  "arrays-hashing": "#0d9488",
  "two-pointers": "#2563eb",
  "sliding-window": "#ea580c",
  stack: "#ca8a04",
  "binary-search": "#4f46e5",
  "linked-list": "#db2777",
  trees: "#16a34a",
  tries: "#0891b2",
  "heap-priority-queue": "#c2410c",
  backtracking: "#7c3aed",
  graphs: "#0284c7",
  "advanced-graphs": "#1d4ed8",
  "1d-dp": "#b45309",
  "2d-dp": "#9a3412",
  greedy: "#059669",
  intervals: "#be123c",
  "math-geometry": "#4338ca",
  "bit-manipulation": "#475569",
};

export function accentFor(category: string): string {
  return CATEGORY_ACCENTS[category] ?? "#0f766e";
}
