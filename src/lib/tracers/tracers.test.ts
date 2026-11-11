import { describe, expect, it } from "vitest";
import { runTracer } from "./index";
import fs from "fs";
import path from "path";
import { ProblemSchema } from "../schema";

describe("premium tracers", () => {
  it("contains-duplicate finds a duplicate", () => {
    const steps = runTracer("contains-duplicate", [1, 2, 3, 1]);
    expect(steps.at(-1)?.state.result).toBe(true);
  });

  it("contains-duplicate unique list", () => {
    const steps = runTracer("contains-duplicate", [1, 2, 3, 4]);
    expect(steps.at(-1)?.state.result).toBe(false);
  });

  it("two-sum returns indices", () => {
    const steps = runTracer("two-sum", { nums: [2, 7, 11, 15], target: 9 });
    expect(steps.at(-1)?.state.result).toEqual([0, 1]);
  });

  it("valid-parentheses accepts matching pairs", () => {
    const steps = runTracer("valid-parentheses", "()[]{}");
    expect(steps.at(-1)?.state.result).toBe(true);
  });

  it("valid-parentheses rejects mismatch", () => {
    const steps = runTracer("valid-parentheses", "(]");
    expect(steps.at(-1)?.state.result).toBe(false);
  });
});

describe("all problem JSON schemas", () => {
  const dir = path.join(process.cwd(), "content/problems");
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));

  it(`validates ${files.length} files`, () => {
    for (const file of files) {
      const raw = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"));
      const parsed = ProblemSchema.safeParse(raw);
      if (!parsed.success) {
        throw new Error(`${file}: ${parsed.error.message}`);
      }
    }
    expect(files.length).toBe(150);
  });
});
