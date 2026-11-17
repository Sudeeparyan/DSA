import fs from "fs";
import os from "os";
import path from "path";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

/**
 * The loader keeps parsed files in memory.  `npm run dev` must still show a lesson that
 * `npm run lessons` has just rebuilt, so a changed file has to be read again.
 */

const REPO = process.cwd();

describe("lesson loader cache", () => {
  let dir: string;

  beforeEach(() => {
    dir = fs.mkdtempSync(path.join(os.tmpdir(), "lessons-"));
    fs.mkdirSync(path.join(dir, "content", "lessons"), { recursive: true });
    fs.copyFileSync(path.join(REPO, "content", "catalog.json"), path.join(dir, "content", "catalog.json"));
    fs.copyFileSync(
      path.join(REPO, "content", "lessons", "two-sum.json"),
      path.join(dir, "content", "lessons", "two-sum.json"),
    );
    process.chdir(dir); // the loader finds content/ from the working directory when it loads
    vi.resetModules();
  });

  afterEach(() => {
    process.chdir(REPO);
    fs.rmSync(dir, { recursive: true, force: true });
  });

  it("reads a lesson again after its file changes", async () => {
    const { getLesson } = await import("./lessons");
    const file = path.join(dir, "content", "lessons", "two-sum.json");
    expect(getLesson("two-sum")?.pattern).toBe("Hash map lookup");

    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.pattern = "Changed pattern";
    fs.writeFileSync(file, JSON.stringify(doc));
    const later = new Date(Date.now() + 5000);
    fs.utimesSync(file, later, later);

    expect(getLesson("two-sum")?.pattern).toBe("Changed pattern");
  });

  it("returns the same parsed object while the file is unchanged", async () => {
    const { getLesson } = await import("./lessons");
    expect(getLesson("two-sum")).toBe(getLesson("two-sum"));
  });

  it("returns nothing for a lesson that has no file", async () => {
    const { getLesson, hasLesson } = await import("./lessons");
    expect(hasLesson("valid-anagram")).toBe(false);
    expect(getLesson("valid-anagram")).toBeUndefined();
  });
});
