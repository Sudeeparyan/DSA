import type { TraceStep } from "./types";

export function traceTwoSum(input: unknown): TraceStep[] {
  const { nums, target } = input as { nums: number[]; target: number };
  const steps: TraceStep[] = [];
  const prevMap = new Map<number, number>();

  steps.push({
    line: 2,
    caption: `We want two numbers that add up to ${target}. Start with an empty memory map (hash map).`,
    state: {
      nums,
      target,
      map: {},
      currentIndex: null,
      result: null,
      highlights: {},
    },
  });

  for (let i = 0; i < nums.length; i++) {
    const n = nums[i];
    const diff = target - n;

    steps.push({
      line: 4,
      caption: `Look at ${n} at index ${i}. We need a partner that is ${target} − ${n} = ${diff}.`,
      state: {
        nums,
        target,
        map: Object.fromEntries(prevMap),
        currentIndex: i,
        currentValue: n,
        needed: diff,
        result: null,
        highlights: { [i]: "current" },
      },
    });

    if (prevMap.has(diff)) {
      const j = prevMap.get(diff)!;
      steps.push({
        line: 6,
        caption: `Is ${diff} already in our memory? Yes — at index ${j}. Pair found!`,
        state: {
          nums,
          target,
          map: Object.fromEntries(prevMap),
          currentIndex: i,
          currentValue: n,
          needed: diff,
          result: [j, i],
          highlights: { [j]: "matched", [i]: "matched" },
        },
      });
      steps.push({
        line: 7,
        caption: `Return the indices [${j}, ${i}].`,
        state: {
          nums,
          target,
          map: Object.fromEntries(prevMap),
          currentIndex: i,
          result: [j, i],
          highlights: { [j]: "matched", [i]: "matched" },
        },
      });
      return steps;
    }

    steps.push({
      line: 6,
      caption: `Is ${diff} in our memory? No. Save ${n} → index ${i} for later.`,
      state: {
        nums,
        target,
        map: Object.fromEntries(prevMap),
        currentIndex: i,
        currentValue: n,
        needed: diff,
        result: null,
        highlights: { [i]: "current" },
      },
    });

    prevMap.set(n, i);
    steps.push({
      line: 8,
      caption: `Remember: value ${n} lives at index ${i}.`,
      state: {
        nums,
        target,
        map: Object.fromEntries(prevMap),
        currentIndex: i,
        currentValue: n,
        result: null,
        highlights: { [i]: "remembered" },
      },
    });
  }

  steps.push({
    line: 8,
    caption: "No pair adds up to the target.",
    state: {
      nums,
      target,
      map: Object.fromEntries(prevMap),
      currentIndex: null,
      result: null,
      highlights: {},
    },
  });

  return steps;
}
