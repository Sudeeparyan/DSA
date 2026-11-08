import { HomeClient } from "@/components/home/HomeClient";
import { getAllProblems, getCatalog } from "@/lib/problems";

export default function HomePage() {
  const catalog = getCatalog();
  const problems = getAllProblems().map((p) => ({
    slug: p.slug,
    title: p.title,
    difficulty: p.difficulty,
    category: p.category,
  }));

  return (
    <HomeClient
      categories={catalog.categories.map((c) => ({
        slug: c.slug,
        name: c.name,
        whyItMatters: c.whyItMatters,
        problemSlugs: c.problemSlugs,
      }))}
      problems={problems}
    />
  );
}
