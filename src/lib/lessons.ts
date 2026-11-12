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

let catalogCache: Catalog | null = null;
const lessonCache = new Map<string, Lesson>();

export function getCatalog(): Catalog {
  if (!catalogCache) {
    const raw = fs.readFileSync(path.join(CONTENT_DIR, "catalog.json"), "utf8");
    catalogCache = JSON.parse(raw) as Catalog;
  }
  return catalogCache;
}

export function hasLesson(slug: string): boolean {
  return fs.existsSync(path.join(LESSON_DIR, `${slug}.json`));
}

export function getLesson(slug: string): Lesson | undefined {
  const cached = lessonCache.get(slug);
  if (cached) return cached;
  const file = path.join(LESSON_DIR, `${slug}.json`);
  if (!fs.existsSync(file)) return undefined;
  const parsed = LessonSchema.safeParse(JSON.parse(fs.readFileSync(file, "utf8")));
  if (!parsed.success) {
    throw new Error(`Invalid lesson file ${slug}.json: ${parsed.error.message}`);
  }
  lessonCache.set(slug, parsed.data);
  return parsed.data;
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
