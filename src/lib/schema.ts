import { z } from "zod";

export const DifficultySchema = z.enum(["Easy", "Medium", "Hard"]);

export const ExampleSchema = z.object({
  input: z.string(),
  output: z.string(),
  explanation: z.string().optional(),
});

export const ThinkingStepSchema = z.object({
  title: z.string(),
  body: z.string(),
});

export const ComplexitySchema = z.object({
  time: z.string(),
  timeReason: z.string(),
  space: z.string(),
  spaceReason: z.string(),
});

export const AnimationStepSchema = z.object({
  line: z.number().int().nonnegative(),
  caption: z.string(),
  state: z.record(z.string(), z.unknown()),
});

export const AnimationSchema = z.object({
  visualType: z.enum([
    "array",
    "hash",
    "stack",
    "queue",
    "linkedList",
    "tree",
    "trie",
    "graph",
    "grid",
    "heap",
    "backtracking",
    "dp",
    "intervals",
    "bits",
  ]),
  tracerId: z.string().min(1),
  defaultInput: z.unknown(),
  steps: z.array(AnimationStepSchema),
});

export const SolutionsSchema = z.object({
  python: z.string().min(1),
  cpp: z.string().nullable(),
  rust: z.string().nullable(),
});

export const ProblemSchema = z.object({
  id: z.number().int().positive(),
  leetcodeNumber: z.number().int().positive(),
  title: z.string().min(1),
  slug: z.string().min(1),
  category: z.string().min(1),
  difficulty: DifficultySchema,
  leetcodeUrl: z.string().url(),
  neetcodeVideoUrl: z.string().url().nullable(),
  kidExplanation: z.string().min(1),
  plainProblem: z.string().min(1),
  examples: z.array(ExampleSchema).min(1),
  thinkingSteps: z.array(ThinkingStepSchema).min(1),
  pattern: z.object({
    name: z.string(),
    whenToSpot: z.string(),
  }),
  solutions: SolutionsSchema,
  complexity: ComplexitySchema,
  edgeCases: z.array(z.string()),
  commonMistakes: z.array(z.string()),
  interviewTips: z.array(z.string()),
  animation: AnimationSchema,
  relatedProblems: z.array(z.string()),
  hasStory: z.boolean(),
  hasAnimation: z.boolean(),
  hasCode: z.boolean(),
  interviewApproachNotes: z.string().optional(),
});

export type Problem = z.infer<typeof ProblemSchema>;
export type AnimationStep = z.infer<typeof AnimationStepSchema>;
export type Difficulty = z.infer<typeof DifficultySchema>;
