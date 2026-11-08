"use client";

import type { Problem } from "@/lib/schema";
import { MissionFlow } from "@/components/mission/MissionFlow";

export function ProblemView({ problem }: { problem: Problem }) {
  return <MissionFlow problem={problem} />;
}
