export interface TraceStep {
  line: number;
  caption: string;
  state: Record<string, unknown>;
}

export type TracerFn = (input: unknown) => TraceStep[];
