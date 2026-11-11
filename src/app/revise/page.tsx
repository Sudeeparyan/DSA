import { getAllProblems } from "@/lib/problems";
import { ReviseClient } from "./ReviseClient";

export default function RevisePage() {
  const cards = getAllProblems().map((p) => ({
    slug: p.slug,
    title: p.title,
    pattern: p.pattern.name,
    complexity: `${p.complexity.time} time, ${p.complexity.space} space`,
    oneLiner: p.thinkingSteps[p.thinkingSteps.length - 1]?.body ?? p.plainProblem,
  }));
  return <ReviseClient cards={cards} />;
}
