/**
 * End-to-end verification loop for all 150 problem answer animations.
 * Exit 1 if anything is stubby, unloadable, or unusable by the cinema stage.
 */
import fs from "fs";
import path from "path";
import { ProblemSchema } from "../src/lib/schema";
import {
  animationQualityReport,
  resolveAnimationSteps,
} from "../src/lib/animation";
import { buildLessonScript } from "../src/lib/lessonScript";

const dir = path.join(process.cwd(), "content/problems");
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort();

type Row = {
  slug: string;
  ok: boolean;
  steps: number;
  reasons: string[];
  visual: string;
  tracer: string;
};

const rows: Row[] = [];

for (const file of files) {
  const raw = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"));
  const parsed = ProblemSchema.safeParse(raw);
  const reasons: string[] = [];
  if (!parsed.success) {
    reasons.push(`schema:${parsed.error.issues[0]?.message ?? "invalid"}`);
    rows.push({
      slug: file,
      ok: false,
      steps: 0,
      reasons,
      visual: "?",
      tracer: "?",
    });
    continue;
  }
  const problem = parsed.data;
  if (
    problem.animation.defaultInput &&
    typeof problem.animation.defaultInput === "object" &&
    !Array.isArray(problem.animation.defaultInput) &&
    (problem.animation.defaultInput as { demo?: boolean }).demo === true
  ) {
    reasons.push("demo-input");
  }

  let steps;
  try {
    steps = resolveAnimationSteps(problem);
  } catch (e) {
    reasons.push(`resolve:${(e as Error).message}`);
    steps = problem.animation.steps;
  }

  const quality = animationQualityReport(steps);
  reasons.push(...quality.reasons);

  try {
    const script = buildLessonScript(problem);
    if (script.length < 8) reasons.push(`lesson-too-short:${script.length}`);
    if (!script.some((b) => b.kind === "answer3d")) {
      reasons.push("missing-answer3d-beat");
    }
  } catch (e) {
    reasons.push(`lesson:${(e as Error).message}`);
  }

  const uniq = [...new Set(reasons)];
  rows.push({
    slug: problem.slug,
    ok: uniq.length === 0,
    steps: steps.length,
    reasons: uniq,
    visual: problem.animation.visualType,
    tracer: problem.animation.tracerId,
  });
}

const failed = rows.filter((r) => !r.ok);
const passed = rows.filter((r) => r.ok);

console.log(`Animation verify: ${passed.length}/${rows.length} passed`);
if (failed.length) {
  console.log("\nFailures:");
  for (const f of failed) {
    console.log(`- ${f.slug} [${f.visual}/${f.tracer}] steps=${f.steps} :: ${f.reasons.join(", ")}`);
  }
  process.exit(1);
}

const byVisual: Record<string, number> = {};
for (const r of rows) byVisual[r.visual] = (byVisual[r.visual] ?? 0) + 1;
console.log("Visual coverage:", byVisual);
console.log("ALL 150 answer animations verified.");
