import fs from "fs";
import path from "path";
import { describe, expect, it } from "vitest";
import { ProblemSchema } from "@/lib/schema";
import {
  animationQualityReport,
  resolveAnimationSteps,
} from "@/lib/animation";
import { buildLessonScript } from "@/lib/lessonScript";

const dir = path.join(process.cwd(), "content/problems");
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

describe("all 150 answer animations", () => {
  it("every problem has a playable non-stub cinema lesson", () => {
    const failures: string[] = [];
    for (const file of files) {
      const raw = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"));
      const parsed = ProblemSchema.safeParse(raw);
      if (!parsed.success) {
        failures.push(`${file}: schema`);
        continue;
      }
      const problem = parsed.data;
      const steps = resolveAnimationSteps(problem);
      const quality = animationQualityReport(steps);
      if (!quality.ok) {
        failures.push(`${problem.slug}: ${quality.reasons.join(",")}`);
      }
      const script = buildLessonScript(problem);
      if (!script.some((b) => b.kind === "answer3d")) {
        failures.push(`${problem.slug}: missing-answer3d`);
      }
    }
    expect(files.length).toBe(150);
    expect(failures).toEqual([]);
  });
});
