import fs from "fs";
import path from "path";
import { ProblemSchema } from "../src/lib/schema";
import { runTracer } from "../src/lib/tracers";

const dir = path.join(process.cwd(), "content/problems");
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));

let ok = 0;
const errors: string[] = [];

for (const file of files) {
  const raw = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"));
  const parsed = ProblemSchema.safeParse(raw);
  if (!parsed.success) {
    errors.push(`${file}: ${parsed.error.message}`);
    continue;
  }
  ok += 1;
}

const premium = [
  {
    slug: "contains-duplicate",
    input: [1, 2, 3, 1],
    expected: true,
  },
  {
    slug: "two-sum",
    input: { nums: [2, 7, 11, 15], target: 9 },
    expected: [0, 1],
  },
  {
    slug: "valid-parentheses",
    input: "()[]{}",
    expected: true,
  },
];

for (const p of premium) {
  const steps = runTracer(p.slug, p.input);
  const result = steps[steps.length - 1]?.state.result;
  const same = JSON.stringify(result) === JSON.stringify(p.expected);
  if (!same) {
    errors.push(
      `animation mismatch ${p.slug}: got ${JSON.stringify(result)} expected ${JSON.stringify(p.expected)}`,
    );
  }
}

console.log(`Validated ${ok}/${files.length} problem JSON files`);
if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log("Premium animation consistency checks passed");
