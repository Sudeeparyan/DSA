/**
 * Plain-words help for the "How fast is it?" card: what the common Big-O costs mean, and how
 * much work each one is for an input of 1,000 items.
 */

export interface Growth {
  /** the cost as lessons write it */
  o: string;
  /** roughly how many basic steps that is when n = 1,000 */
  steps: string;
  /** what kind of work grows like this */
  says: string;
}

export const GROWTH: readonly Growth[] = [
  { o: "O(1)", steps: "1", says: "the same however big the input is" },
  { o: "O(log n)", steps: "about 10", says: "the work is cut in half again and again" },
  { o: "O(n)", steps: "1,000", says: "each item is handled once, or a few times" },
  { o: "O(n log n)", steps: "about 10,000", says: "typical of sorting" },
  { o: "O(n²)", steps: "1,000,000", says: "every pair of items is looked at" },
  // 2^1000 ≈ 1.07 × 10^301
  { o: "O(2ⁿ)", steps: "a number 302 digits long", says: "every subset of the items is tried" },
];

/** Spelling differences that do not change the meaning ("O(n^2)", "O( n )"). */
function canonical(cost: string): string {
  return cost.replace(/\s+/g, "").replace(/\^2(?![0-9])/g, "²").replace(/\^n/g, "ⁿ").replace(/·/g, "");
}

/** The row of `GROWTH` that is exactly this cost, if there is one. */
export function growthOf(cost: string): Growth | undefined {
  const key = canonical(cost);
  return GROWTH.find((g) => canonical(g.o) === key);
}
