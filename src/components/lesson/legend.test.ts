import { describe, expect, it } from "vitest";
import type { Step } from "@/lib/lesson";
import { legendFor, tonesUsed } from "./legend";

function step(cells: { v: string; tone?: string }[]): Step {
  return { line: 1, text: "x", views: [{ t: "array", id: "a", cells }] };
}

const LAND = "#3d9950";

describe("tonesUsed", () => {
  it("collects named tones and colours from every step", () => {
    const used = tonesUsed([step([{ v: "1", tone: "cur" }]), step([{ v: "1", tone: LAND }, { v: "2" }])]);
    expect([...used].sort()).toEqual([LAND, "cur"].sort());
  });
});

describe("legendFor", () => {
  it("lists only the standard tones a lesson draws, with their usual labels", () => {
    const legend = legendFor([step([{ v: "1", tone: "cur" }, { v: "2", tone: "good" }])]);
    expect(legend).toEqual([
      { tone: "cur", label: "looking at now" },
      { tone: "good", label: "match / answer" },
    ]);
  });

  it("puts a lesson's own colours first and renames standard tones it gives a meaning to", () => {
    const steps = [step([{ v: "1", tone: LAND }, { v: "0", tone: "good" }, { v: "7", tone: "cur" }])];
    const legend = legendFor(steps, [
      { tone: LAND, label: "land (1)" },
      { tone: "good", label: "gate (0)" },
    ]);
    expect(legend).toEqual([
      { tone: LAND, label: "land (1)" },
      { tone: "cur", label: "looking at now" },
      { tone: "good", label: "gate (0)" },
    ]);
  });

  it("leaves out key entries whose colour is never drawn", () => {
    const legend = legendFor([step([{ v: "1", tone: "cur" }])], [{ tone: LAND, label: "land" }]);
    expect(legend).toEqual([{ tone: "cur", label: "looking at now" }]);
  });
});
