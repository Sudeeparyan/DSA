"use client";

import type { Problem } from "@/lib/schema";
import { LessonTheater } from "@/components/theater/LessonTheater";

export function ProblemView({ problem }: { problem: Problem }) {
  return <LessonTheater problem={problem} />;
}
