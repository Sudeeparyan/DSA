import type { TracerFn } from "./types";
import { traceContainsDuplicate } from "./contains-duplicate";
import { traceTwoSum } from "./two-sum";
import { traceValidParentheses } from "./valid-parentheses";
import { traceGenericArrayScan } from "./generic";

/**
 * Specialty algorithm tracers.
 * Add a new file + call `registerTracer(id, fn)` (or append below) to upgrade
 * a problem from authored cinema steps to a live deterministic tracer.
 */
const registry: Record<string, TracerFn> = {
  "contains-duplicate": traceContainsDuplicate,
  "two-sum": traceTwoSum,
  "valid-parentheses": traceValidParentheses,
  "generic-array-scan": traceGenericArrayScan,
};

/** Register or replace a tracer at runtime / module init. */
export function registerTracer(id: string, fn: TracerFn): void {
  registry[id] = fn;
}

export function listTracers(): string[] {
  return Object.keys(registry).sort();
}

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
