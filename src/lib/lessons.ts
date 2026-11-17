import fs from "fs";
import path from "path";
import { LessonSchema, type Lesson, type LessonMeta } from "./lesson";

/** Server-side loaders (used at build time by the statically exported pages). */

const CONTENT_DIR = path.join(process.cwd(), "content");
const LESSON_DIR = path.join(CONTENT_DIR, "lessons");

export interface CatalogCategory {
  id: number;
  slug: string;
  name: string;
  whyItMatters: string;
  problemSlugs: string[];
}

interface CatalogProblem {
  id: number;
  leetcodeNumber: number;
  title: string;
  slug: string;
  category: string;
  difficulty: "Easy" | "Medium" | "Hard";
}

interface Catalog {
  categories: CatalogCategory[];
  problems: CatalogProblem[];
}

/**
 * Parsed files are kept in memory, keyed by the file's modification time: a build reads each file
 * once, and `npm run dev` picks up a lesson rebuilt by `npm run lessons` on the next page load
 * (without the time check it kept serving the old copy until restarted).
 */
const cache = new Map<string, { mtime: number; value: unknown }>();

function readCached<T>(file: string, parse: (raw: string) => T): T | undefined {
  let mtime: number;
  try {
    mtime = fs.statSync(file).mtimeMs;
  } catch {
    return undefined;
  }
  const hit = cache.get(file);
  if (hit && hit.mtime === mtime) return hit.value as T;
  const value = parse(fs.readFileSync(file, "utf8"));
  cache.set(file, { mtime, value });
  return value;
}

export function getCatalog(): Catalog {
  const catalog = readCached(path.join(CONTENT_DIR, "catalog.json"), (raw) => JSON.parse(raw) as Catalog);
  if (!catalog) throw new Error("content/catalog.json is missing");
  return catalog;
}

export function hasLesson(slug: string): boolean {
  return fs.existsSync(path.join(LESSON_DIR, `${slug}.json`));
}

export function getLesson(slug: string): Lesson | undefined {
  return readCached(path.join(LESSON_DIR, `${slug}.json`), (raw) => {
    const parsed = LessonSchema.safeParse(JSON.parse(raw));
    if (!parsed.success) {
      throw new Error(`Invalid lesson file ${slug}.json: ${parsed.error.message}`);
    }
    return parsed.data;
  });
}

/** Every problem that has a lesson, in NeetCode roadmap order. */
export function getLessonList(): LessonMeta[] {
  return getCatalog()
    .problems.filter((p) => hasLesson(p.slug))
    .map((p) => ({
      id: p.id,
      number: p.leetcodeNumber,
      title: p.title,
      slug: p.slug,
      category: p.category,
      difficulty: p.difficulty,
      pattern: getLesson(p.slug)?.pattern ?? "",
    }));
}

export function getCategories(): CatalogCategory[] {
  return getCatalog().categories;
}
