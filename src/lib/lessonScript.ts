import type { Problem } from "@/lib/schema";
import { getTracer, runTracer } from "@/lib/tracers";

export type BeatKind =
  | "hook"
  | "puzzle"
  | "example"
  | "rocket"
  | "algo"
  | "code"
  | "orbit"
  | "done";

export interface TeachBeat {
  id: string;
  kind: BeatKind;
  chapter: string;
  teacher: string;
  durationMs: number;
  /** Optional payload for the scene renderer */
  data?: Record<string, unknown>;
}

function firstExampleInput(problem: Problem): unknown {
  return problem.animation.defaultInput;
}

function algoSteps(problem: Problem) {
  const input = firstExampleInput(problem);
  try {
    const tracer = getTracer(problem.animation.tracerId);
    if (tracer) return runTracer(problem.animation.tracerId, input);
  } catch {
    /* fall through */
  }
  return problem.animation.steps;
}

/** Turn a problem into a continuous teacher-led playthrough. */
export function buildLessonScript(problem: Problem): TeachBeat[] {
  const beats: TeachBeat[] = [];
  const ex = problem.examples[0];
  const steps = algoSteps(problem);

  beats.push({
    id: "hook",
    kind: "hook",
    chapter: "The question",
    teacher: `Alright class — today's puzzle is “${problem.title}”. Don't touch code yet. First we feel the problem.`,
    durationMs: 4200,
    data: { title: problem.title, difficulty: problem.difficulty },
  });

  beats.push({
    id: "puzzle-kid",
    kind: "puzzle",
    chapter: "The question",
    teacher: problem.kidExplanation,
    durationMs: 6500,
    data: { mode: "kid", text: problem.kidExplanation },
  });

  beats.push({
    id: "puzzle-real",
    kind: "puzzle",
    chapter: "The question",
    teacher: `Now the interview wording: ${problem.plainProblem}`,
    durationMs: 5500,
    data: { mode: "real", text: problem.plainProblem },
  });

  beats.push({
    id: "example",
    kind: "example",
    chapter: "Walk an example",
    teacher: ex?.explanation
      ? `Watch this example. Input ${ex.input} → output ${ex.output}. ${ex.explanation}`
      : `Watch this example. Input ${ex?.input ?? ""} → output ${ex?.output ?? ""}.`,
    durationMs: 7000,
    data: {
      input: ex?.input ?? "",
      output: ex?.output ?? "",
      explanation: ex?.explanation ?? "",
      visualInput: problem.animation.defaultInput,
      visualType: problem.animation.visualType,
    },
  });

  problem.thinkingSteps.forEach((step, i) => {
    beats.push({
      id: `rocket-${i}`,
      kind: "rocket",
      chapter: "Build the idea",
      teacher: `${step.title}. ${step.body}`,
      durationMs: 6200,
      data: {
        index: i,
        total: problem.thinkingSteps.length,
        title: step.title,
        body: step.body,
        pattern: problem.pattern.name,
      },
    });
  });

  // Sample algo steps (cap for lesson length — keep it watchable)
  const sample = steps.length <= 10 ? steps : [
    ...steps.slice(0, 4),
    ...steps.slice(Math.floor(steps.length / 2), Math.floor(steps.length / 2) + 2),
    ...steps.slice(-3),
  ];

  sample.forEach((step, i) => {
    beats.push({
      id: `algo-${i}`,
      kind: "algo",
      chapter: "Watch it run",
      teacher: step.caption,
      durationMs: 1600,
      data: {
        step,
        line: step.line,
        code: problem.solutions.python,
        visualType: problem.animation.visualType,
        stepIndex: i,
        stepTotal: sample.length,
      },
    });
  });

  beats.push({
    id: "code",
    kind: "code",
    chapter: "The blueprint",
    teacher:
      "Same story, written for the computer. Read it out loud once — you already know every line from the animation.",
    durationMs: 8000,
    data: {
      code: problem.solutions.python,
      time: problem.complexity.time,
      space: problem.complexity.space,
      timeReason: problem.complexity.timeReason,
      spaceReason: problem.complexity.spaceReason,
    },
  });

  const orbitItems = [
    ...problem.edgeCases.slice(0, 3).map((t) => ({ label: "Edge", text: t })),
    ...problem.commonMistakes.slice(0, 2).map((t) => ({ label: "Trap", text: t })),
    ...problem.interviewTips.slice(0, 2).map((t) => ({ label: "Say this", text: t })),
  ];

  beats.push({
    id: "orbit",
    kind: "orbit",
    chapter: "Flight check",
    teacher:
      "Last stop — traps and what to say in the interview. Tap any floating chip to pin it open.",
    durationMs: 9000,
    data: { items: orbitItems },
  });

  beats.push({
    id: "done",
    kind: "done",
    chapter: "Mission clear",
    teacher: `You can now explain “${problem.title}” out loud. Mark your status, then practise on LeetCode.`,
    durationMs: 5000,
    data: {
      leetcodeUrl: problem.leetcodeUrl,
      related: problem.relatedProblems,
      pattern: problem.pattern.name,
    },
  });

  return beats;
}
