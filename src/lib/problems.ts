import fs from "fs";
import path from "path";
import { ProblemSchema, type Problem } from "./schema";

const CONTENT_DIR = path.join(process.cwd(), "content");
const PROBLEMS_DIR = path.join(CONTENT_DIR, "problems");

export interface CatalogProblem {
  id: number;
  leetcodeNumber: number;
  title: string;
  slug: string;
  category: string;
  categoryDir: string;
  problemDir: string;
  difficulty: "Easy" | "Medium" | "Hard";
  leetcodeUrl: string;
  pythonPath: string;
  hasCpp: boolean;
  hasRust: boolean;
  cppPath?: string | null;
  rustPath?: string | null;
}

export interface CatalogCategory {
  id: number;
  slug: string;
  name: string;
  dir: string;
  whyItMatters: string;
  problemSlugs: string[];
}

export interface Catalog {
  categories: CatalogCategory[];
  problems: CatalogProblem[];
}

let catalogCache: Catalog | null = null;
let problemsCache: Problem[] | null = null;

export function getCatalog(): Catalog {
  if (catalogCache) return catalogCache;
  const raw = fs.readFileSync(path.join(CONTENT_DIR, "catalog.json"), "utf8");
  catalogCache = JSON.parse(raw) as Catalog;
  return catalogCache;
}

export function getAllProblems(): Problem[] {
  if (problemsCache) return problemsCache;
  if (!fs.existsSync(PROBLEMS_DIR)) {
    problemsCache = [];
    return problemsCache;
  }
  const files = fs
    .readdirSync(PROBLEMS_DIR)
    .filter((f) => f.endsWith(".json"))
    .sort();
  problemsCache = files.map((file) => {
    const raw = JSON.parse(
      fs.readFileSync(path.join(PROBLEMS_DIR, file), "utf8"),
    );
    return ProblemSchema.parse(raw);
  });
  return problemsCache;
}

export function getProblem(slug: string): Problem | undefined {
  return getAllProblems().find((p) => p.slug === slug);
}

export function getProblemsByCategory(categorySlug: string): Problem[] {
  return getAllProblems().filter((p) => p.category === categorySlug);
}

export function getCategory(slug: string): CatalogCategory | undefined {
  return getCatalog().categories.find((c) => c.slug === slug);
}

export function getPatterns() {
  const file = path.join(CONTENT_DIR, "patterns.json");
  if (!fs.existsSync(file)) return [];
  return JSON.parse(fs.readFileSync(file, "utf8")) as Array<{
    id: string;
    name: string;
    summary: string;
    templatePython: string;
    problemSlugs: string[];
  }>;
}
