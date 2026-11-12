#!/usr/bin/env node
/**
 * Runs a Python script with whichever Python 3.10+ this computer has.
 *
 *   node scripts/python.mjs lessons/build.py --strict
 *
 * Windows usually calls it `python` (or `py`), macOS and Linux `python3`.
 * The npm scripts go through this file so they work the same everywhere.
 */
import { spawnSync } from "node:child_process";

const MIN = [3, 10];
const CANDIDATES = process.platform === "win32" ? ["python", "py", "python3"] : ["python3", "python"];

function version(cmd) {
  const probe = spawnSync(cmd, ["-c", "import sys; print(sys.version_info[0], sys.version_info[1])"], {
    encoding: "utf8",
  });
  if (probe.status !== 0 || !probe.stdout) return null;
  const [major, minor] = probe.stdout.trim().split(" ").map(Number);
  return [major, minor];
}

const found = CANDIDATES.map((cmd) => ({ cmd, v: version(cmd) })).find(
  ({ v }) => v && (v[0] > MIN[0] || (v[0] === MIN[0] && v[1] >= MIN[1])),
);

if (!found) {
  console.error(
    `Python ${MIN.join(".")} or newer is needed for this command, but none was found ` +
      `(tried: ${CANDIDATES.join(", ")}). Install it from https://www.python.org and try again.`,
  );
  process.exit(1);
}

const run = spawnSync(found.cmd, process.argv.slice(2), { stdio: "inherit" });
process.exit(run.status ?? 1);
