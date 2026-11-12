import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { LessonPage } from "@/components/lesson/LessonPage";
import { getCategories, getLesson, getLessonList } from "@/lib/lessons";

export const dynamicParams = false;

export function generateStaticParams() {
  return getLessonList().map((lesson) => ({ slug: lesson.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const lesson = getLesson(slug);
  if (!lesson) return {};
  return {
    title: lesson.title,
    description: lesson.statement.replace(/[`*]/g, ""),
  };
}

export default async function ProblemPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const lesson = getLesson(slug);
  if (!lesson) notFound();

  const list = getLessonList();
  const at = list.findIndex((l) => l.slug === slug);
  const category = getCategories().find((c) => c.slug === lesson.category);

  return (
    <LessonPage
      lesson={lesson}
      prev={at > 0 ? list[at - 1] : null}
      next={at >= 0 && at < list.length - 1 ? list[at + 1] : null}
      position={at + 1}
      total={list.length}
      categoryName={category?.name ?? lesson.category}
    />
  );
}
