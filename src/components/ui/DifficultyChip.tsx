import type { Difficulty } from "@/lib/schema";
import { clsx } from "clsx";

const styles: Record<Difficulty, string> = {
  Easy: "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300",
  Medium: "bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200",
  Hard: "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300",
};

export function DifficultyChip({ difficulty }: { difficulty: Difficulty }) {
  return (
    <span
      className={clsx(
        "inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold",
        styles[difficulty],
      )}
    >
      {difficulty}
    </span>
  );
}
