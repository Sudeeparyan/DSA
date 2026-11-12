import { ProblemList } from "@/components/lesson/ProblemList";
import { getCategories, getLessonList } from "@/lib/lessons";

export default function HomePage() {
  const lessons = getLessonList();
  const bySlug = new Map(lessons.map((l) => [l.slug, l]));
  const groups = getCategories()
    .map((category) => ({
      slug: category.slug,
      name: category.name,
      lessons: category.problemSlugs.flatMap((slug) => {
        const lesson = bySlug.get(slug);
        return lesson ? [lesson] : [];
      }),
    }))
    .filter((group) => group.lessons.length > 0);

  return <ProblemList groups={groups} total={lessons.length} />;
}
