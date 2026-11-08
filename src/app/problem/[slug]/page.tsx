import { notFound } from "next/navigation";
import { getAllProblems, getProblem } from "@/lib/problems";
import { ProblemView } from "@/components/problem/ProblemView";

export function generateStaticParams() {
  return getAllProblems().map((p) => ({ slug: p.slug }));
}

export default async function ProblemPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const problem = getProblem(slug);
  if (!problem) notFound();
  return <ProblemView problem={problem} />;
}
