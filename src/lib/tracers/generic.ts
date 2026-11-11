import type { TraceStep } from "./types";

/** Fallback tracer for array-style walkthroughs when a dedicated tracer is not ready. */
export function traceGenericArrayScan(input: unknown): TraceStep[] {
  const nums = Array.isArray(input)
    ? (input as unknown[])
    : ((input as { nums?: unknown[] })?.nums ?? []);
  const steps: TraceStep[] = [
    {
      line: 1,
      caption: "Start scanning the list from left to right.",
      state: {
        nums,
        currentIndex: null,
        result: null,
        highlights: {},
      },
    },
  ];

  for (let i = 0; i < nums.length; i++) {
    steps.push({
      line: 2,
      caption: `Visit index ${i} with value ${String(nums[i])}.`,
      state: {
        nums,
        currentIndex: i,
        currentValue: nums[i],
        result: null,
        highlights: { [i]: "current" },
      },
    });
  }

  steps.push({
    line: 3,
    caption: "Finished scanning every item.",
    state: {
      nums,
      currentIndex: null,
      result: "done",
      highlights: Object.fromEntries(nums.map((_, i) => [i, "done"])),
    },
  });

  return steps;
}
