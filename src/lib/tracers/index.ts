import type { TracerFn } from "./types";
import { traceContainsDuplicate } from "./contains-duplicate";
import { traceTwoSum } from "./two-sum";
import { traceValidParentheses } from "./valid-parentheses";
import { traceGenericArrayScan } from "./generic";

const registry: Record<string, TracerFn> = {
  "contains-duplicate": traceContainsDuplicate,
  "two-sum": traceTwoSum,
  "valid-parentheses": traceValidParentheses,
  "generic-array-scan": traceGenericArrayScan,
};

export function getTracer(id: string): TracerFn | undefined {
  return registry[id];
}

export function runTracer(id: string, input: unknown) {
  const tracer = getTracer(id);
  if (!tracer) {
    throw new Error(`Unknown tracer: ${id}`);
  }
  return tracer(input);
}

export * from "./types";
