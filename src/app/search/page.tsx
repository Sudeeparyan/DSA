import { getAllProblems, getCatalog } from "@/lib/problems";
import { SearchClient } from "./SearchClient";

export default function SearchPage() {
  const problems = getAllProblems().map((p) => ({
    slug: p.slug,
    title: p.title,
    category: p.category,
    difficulty: p.difficulty,
    pattern: p.pattern.name,
  }));
  const categories = getCatalog().categories.map((c) => ({
    slug: c.slug,
    name: c.name,
  }));
  return <SearchClient problems={problems} categories={categories} />;
}
