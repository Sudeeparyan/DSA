import fs from "fs";
import path from "path";
import { describe, expect, it } from "vitest";
import { LessonSchema, type Lesson, type View } from "./lesson";

/**
 * Gate for the generated lesson files (`python lessons/build.py`).
 *
 * The Python builder already proves that every solution returns the right
 * answer.  This test proves that what it wrote is something the web app can
 * actually draw: valid against the schema, with no dangling references.
 */

const CONTENT = path.join(process.cwd(), "content");
const LESSON_DIR = path.join(CONTENT, "lessons");

interface CatalogProblem {
  slug: string;
  title: string;
  leetcodeNumber: number;
  difficulty: string;
  category: string;
}

const catalog = JSON.parse(fs.readFileSync(path.join(CONTENT, "catalog.json"), "utf8")) as {
  problems: CatalogProblem[];
};

const TONES = new Set(["cur", "alt", "good", "bad", "seen", "win", "mark", "dim"]);

function load(slug: string): Lesson {
  const raw = JSON.parse(fs.readFileSync(path.join(LESSON_DIR, `${slug}.json`), "utf8"));
  return LessonSchema.parse(raw);
}

function toneOk(tone: string | undefined): boolean {
  return tone === undefined || TONES.has(tone) || /^#[0-9a-fA-F]{6}$/.test(tone);
}

/** Every problem found in one view; an empty list means the view is drawable. */
function viewProblems(view: View): string[] {
  const out: string[] = [];
  const bad = (msg: string) => out.push(`${view.t}:${view.id} ${msg}`);

  switch (view.t) {
    case "array": {
      const n = view.cells.length;
      for (const cell of view.cells) if (!toneOk(cell.tone)) bad(`tone ${cell.tone}`);
      for (const p of view.ptrs ?? []) {
        if (!Number.isInteger(p.at) || p.at < -1 || p.at > n) bad(`pointer ${p.name} at ${p.at} of ${n}`);
      }
      for (const r of view.ranges ?? []) {
        if (r.from < 0 || r.to >= n || r.from > r.to) bad(`range ${r.from}..${r.to} of ${n}`);
        if (!toneOk(r.tone)) bad(`range tone ${r.tone}`);
      }
      if (view.water && view.water.length !== n) bad("water length");
      break;
    }
    case "map":
      for (const e of view.entries) if (!toneOk(e.tone)) bad(`tone ${e.tone}`);
      if (new Set(view.entries.map((e) => e.k)).size !== view.entries.length) bad("duplicate keys");
      break;
    case "stack":
      for (const item of view.items) if (!toneOk(item.tone)) bad(`tone ${item.tone}`);
      if (new Set(view.items.map((i) => i.id)).size !== view.items.length) bad("duplicate item ids");
      break;
    case "items":
      for (const item of view.items) if (!toneOk(item.tone)) bad(`tone ${item.tone}`);
      break;
    case "list": {
      const ids = new Set(view.nodes.map((n) => n.id));
      if (ids.size !== view.nodes.length) bad("duplicate node ids");
      for (const node of view.nodes) {
        if (node.next !== undefined && !ids.has(node.next)) bad(`next -> ${node.next}`);
        if (node.rand !== undefined && !ids.has(node.rand)) bad(`random -> ${node.rand}`);
        if (!toneOk(node.tone)) bad(`tone ${node.tone}`);
      }
      for (const p of view.ptrs ?? []) if (p.at !== null && !ids.has(p.at)) bad(`pointer ${p.name}`);
      break;
    }
    case "tree": {
      const ids = new Set(view.nodes.map((n) => n.id));
      if (ids.size !== view.nodes.length) bad("duplicate node ids");
      for (const node of view.nodes) {
        for (const kid of [node.l, node.r, ...(node.kids ?? [])]) {
          if (kid !== undefined && !ids.has(kid)) bad(`child -> ${kid}`);
        }
        if (!toneOk(node.tone)) bad(`tone ${node.tone}`);
      }
      for (const root of view.roots) if (!ids.has(root)) bad(`root ${root}`);
      for (const p of view.ptrs ?? []) if (!ids.has(p.at)) bad(`pointer ${p.name}`);
      break;
    }
    case "graph": {
      const ids = new Set(view.nodes.map((n) => n.id));
      if (ids.size !== view.nodes.length) bad("duplicate node ids");
      for (const node of view.nodes) if (!toneOk(node.tone)) bad(`tone ${node.tone}`);
      for (const e of view.edges) {
        if (!ids.has(e.a) || !ids.has(e.b)) bad(`edge ${e.a}-${e.b}`);
        if (!toneOk(e.tone)) bad(`edge tone ${e.tone}`);
      }
      break;
    }
    case "grid": {
      const width = view.cells[0]?.length ?? 0;
      if (view.cells.some((row) => row.length !== width)) bad("ragged rows");
      for (const row of view.cells) for (const cell of row) if (!toneOk(cell.tone)) bad(`tone ${cell.tone}`);
      if (view.rows && view.rows.length !== view.cells.length) bad("row headers");
      if (view.cols && view.cols.length !== width) bad("column headers");
      for (const p of view.ptrs ?? []) {
        if (p.r < 0 || p.r >= view.cells.length || p.c < 0 || p.c >= width) bad(`pointer ${p.name}`);
      }
      break;
    }
    case "intervals":
      for (const row of view.rows) {
        for (const item of row.items) {
          if (item.a > item.b) bad(`interval ${item.a}..${item.b}`);
          if (!toneOk(item.tone)) bad(`tone ${item.tone}`);
        }
      }
      break;
    case "bits": {
      const width = view.rows[0]?.bits.length ?? 0;
      for (const row of view.rows) {
        if (!/^[01]+$/.test(row.bits) || row.bits.length !== width) bad(`bits ${row.bits}`);
        if (!toneOk(row.tone)) bad(`tone ${row.tone}`);
      }
      for (const col of view.hi ?? []) if (col < 0 || col >= width) bad(`highlight ${col}`);
      break;
    }
    case "vars":
    case "ops":
      break;
  }
  return out;
}

describe("lesson files", () => {
  it("cover all 150 problems", () => {
    expect(catalog.problems).toHaveLength(150);
    const missing = catalog.problems
      .map((p) => p.slug)
      .filter((slug) => !fs.existsSync(path.join(LESSON_DIR, `${slug}.json`)));
    expect(missing).toEqual([]);
  });

  it("contain nothing but lessons for catalog problems", () => {
    const known = new Set(catalog.problems.map((p) => p.slug));
    const extra = fs
      .readdirSync(LESSON_DIR)
      .filter((f) => f.endsWith(".json"))
      .map((f) => f.replace(/\.json$/, ""))
      .filter((slug) => !known.has(slug));
    expect(extra).toEqual([]);
  });

  for (const problem of catalog.problems) {
    it(`${problem.slug} is complete and drawable`, () => {
      const lesson = load(problem.slug);

      // identity matches the catalog
      expect(lesson.slug).toBe(problem.slug);
      expect(lesson.title).toBe(problem.title);
      expect(lesson.number).toBe(problem.leetcodeNumber);
      expect(lesson.difficulty).toBe(problem.difficulty);
      expect(lesson.category).toBe(problem.category);

      // the teaching text is all there
      expect(lesson.statement.length).toBeGreaterThan(30);
      expect(lesson.idea.length).toBeGreaterThanOrEqual(2);
      expect(lesson.pattern.length).toBeGreaterThan(3);
      expect(lesson.example.input.length).toBeGreaterThan(0);
      expect(lesson.complexity.time).toMatch(/^O\(/);
      expect(lesson.complexity.space).toMatch(/^O\(/);
      expect(lesson.complexity.timeWhy.length).toBeGreaterThan(10);
      expect(lesson.complexity.spaceWhy.length).toBeGreaterThan(10);

      const codeLines = lesson.code.split("\n").length;
      const problems: string[] = [];
      const kinds = new Map<string, string>();

      lesson.steps.forEach((step, index) => {
        const where = `step ${index + 1}`;
        if (step.line > codeLines) problems.push(`${where}: line ${step.line} of ${codeLines}`);

        // captions must be finished sentences, not leaked Python objects
        if (/object at 0x|<function |<lessons\.|Traceback/.test(step.text)) {
          problems.push(`${where}: leaked object in caption`);
        }
        if ((step.text.match(/\*\*/g) ?? []).length % 2 !== 0) problems.push(`${where}: unbalanced **`);
        if ((step.text.match(/`/g) ?? []).length % 2 !== 0) problems.push(`${where}: unbalanced backtick`);

        const ids = step.views.map((v) => v.id);
        if (new Set(ids).size !== ids.length) problems.push(`${where}: duplicate view ids`);

        for (const view of step.views) {
          // a structure keeps its slot on the stage, so its kind may never change
          const kind = kinds.get(view.id);
          if (kind && kind !== view.t) problems.push(`${where}: view ${view.id} changes kind`);
          kinds.set(view.id, view.t);
          for (const issue of viewProblems(view)) problems.push(`${where}: ${issue}`);
        }
      });

      expect(problems).toEqual([]);

      // exactly one closing step, and it is the last one
      const finals = lesson.steps.filter((s) => s.final);
      expect(finals).toHaveLength(1);
      expect(lesson.steps[lesson.steps.length - 1].final).toBe(true);

      // every lesson shows something on the 3D stage
      const drawn = lesson.steps.some((s) => s.views.some((v) => v.t !== "vars" && v.t !== "ops"));
      expect(drawn).toBe(true);
    });
  }
});
