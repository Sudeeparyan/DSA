import type { TraceStep } from "./types";

/** Mirrors the taught Python hash-set solution. */
export function traceContainsDuplicate(input: unknown): TraceStep[] {
  const nums = input as number[];
  const steps: TraceStep[] = [];
  const hashset = new Set<number>();

  steps.push({
    line: 2,
    caption: "We start with an empty notebook of numbers we have already seen (a hash set).",
    state: {
      nums,
      seen: [],
      currentIndex: null,
      result: null,
      highlights: {},
    },
  });

  for (let i = 0; i < nums.length; i++) {
    const n = nums[i];
    steps.push({
      line: 4,
      caption: `Look at the number ${n} at index ${i}.`,
      state: {
        nums,
        seen: [...hashset],
        currentIndex: i,
        currentValue: n,
        result: null,
        highlights: { [i]: "current" },
      },
    });

    if (hashset.has(n)) {
      steps.push({
        line: 5,
        caption: `Have we seen ${n} before? Yes! So there is a duplicate.`,
        state: {
          nums,
          seen: [...hashset],
          currentIndex: i,
          currentValue: n,
          result: true,
          highlights: { [i]: "matched" },
        },
      });
      steps.push({
        line: 6,
        caption: "Return True — we found a twin.",
        state: {
          nums,
          seen: [...hashset],
          currentIndex: i,
          currentValue: n,
          result: true,
          highlights: { [i]: "matched" },
        },
      });
      return steps;
    }

    steps.push({
      line: 5,
      caption: `Have we seen ${n} before? No.`,
      state: {
        nums,
        seen: [...hashset],
        currentIndex: i,
        currentValue: n,
        result: null,
        highlights: { [i]: "current" },
      },
    });

    hashset.add(n);
    steps.push({
      line: 7,
      caption: `Remember ${n} in our notebook (hash set).`,
      state: {
        nums,
        seen: [...hashset],
        currentIndex: i,
        currentValue: n,
        result: null,
        highlights: { [i]: "remembered" },
      },
    });
  }

  steps.push({
    line: 8,
    caption: "We checked every number. No twins. Return False.",
    state: {
      nums,
      seen: [...hashset],
      currentIndex: null,
      result: false,
      highlights: Object.fromEntries(nums.map((_, i) => [i, "done"])),
    },
  });

  return steps;
}
