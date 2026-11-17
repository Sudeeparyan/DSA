import { describe, expect, it } from "vitest";
import { GROWTH, growthOf } from "./cost";

describe("growthOf", () => {
  it("finds the common costs as lessons write them", () => {
    expect(growthOf("O(n)")?.steps).toBe("1,000");
    expect(growthOf("O(1)")?.steps).toBe("1");
    expect(growthOf("O(log n)")?.o).toBe("O(log n)");
    expect(growthOf("O(n log n)")?.o).toBe("O(n log n)");
    expect(growthOf("O(n²)")?.o).toBe("O(n²)");
  });

  it("ignores spacing and ^2 spelled out", () => {
    expect(growthOf("O( n )")?.o).toBe("O(n)");
    expect(growthOf("O(n^2)")?.o).toBe("O(n²)");
    expect(growthOf("O(2^n)")?.o).toBe("O(2ⁿ)");
  });

  it("does not guess for costs that are not in the table", () => {
    expect(growthOf("O(m · n)")).toBeUndefined();
    expect(growthOf("O(n · 2ⁿ)")).toBeUndefined();
    expect(growthOf("O(V + E)")).toBeUndefined();
    expect(growthOf("O(log n) per add, O(1) per median")).toBeUndefined();
    expect(growthOf("O(n³)")).toBeUndefined();
  });

  it("lists each cost once, from cheapest to dearest", () => {
    expect(new Set(GROWTH.map((g) => g.o)).size).toBe(GROWTH.length);
    expect(GROWTH[0].o).toBe("O(1)");
  });
});
