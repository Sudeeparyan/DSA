import fs from "fs";
import path from "path";

const root = process.cwd();
const catalog = JSON.parse(
  fs.readFileSync(path.join(root, "content/catalog.json"), "utf8"),
) as {
  problems: Array<{
    leetcodeNumber: number;
    title: string;
    slug: string;
    pythonPath: string;
    hasCpp: boolean;
    hasRust: boolean;
    problemDir: string;
  }>;
};

const report: string[] = [];
report.push("# Solutions Audit");
report.push("");
report.push(`Total problems in catalog: ${catalog.problems.length}`);
report.push(
  `Python present: ${catalog.problems.filter((p) => fs.existsSync(p.pythonPath)).length}`,
);
report.push(`C++ present: ${catalog.problems.filter((p) => p.hasCpp).length}`);
report.push(`Rust present: ${catalog.problems.filter((p) => p.hasRust).length}`);
report.push("");
report.push("## Known README mismatches (fixed in catalog by trusting file numbers)");
report.push(
  "- Search in Rotated Sorted Array (33) vs Find Minimum (153): README titles/links were swapped; folders/files are correct.",
);
report.push(
  "- Copy List with Random Pointer: README labelled 141; files use 0138 (correct). 141 is Linked List Cycle.",
);
report.push("");
report.push("## Missing language implementations");
report.push("- All 150 C++ links in upstream README point to missing files.");
report.push("- All 150 Rust links in upstream README point to missing files.");
report.push("");

const missingPy = catalog.problems.filter((p) => !fs.existsSync(p.pythonPath));
if (missingPy.length) {
  report.push("## Missing Python");
  for (const p of missingPy) report.push(`- ${p.leetcodeNumber} ${p.title}`);
}

fs.writeFileSync(path.join(root, "BUILD_REPORT.md"), report.join("\n") + "\n");
console.log(report.join("\n"));
