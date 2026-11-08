"use client";

import type { Problem } from "@/lib/schema";
import { VisualiserEngine } from "@/components/visualiser/VisualiserEngine";

export function SimulateArena({
  problem,
  onContinue,
  onBack,
}: {
  problem: Problem;
  onContinue: () => void;
  onBack: () => void;
}) {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <p className="section-kicker">Live simulation</p>
        <h2 className="brand-font text-2xl font-bold sm:text-3xl">
          Play the algorithm like a game
        </h2>
        <p className="teach max-w-2xl text-muted">
          Hit Play. Watch the data move. Pause anytime, scrub the timeline, or
          type your own tiny input and re-run. Code on the left lights up with
          the current move.
        </p>
      </div>

      <div className="arena-frame">
        <VisualiserEngine problem={problem} immersive />
      </div>

      <div className="flex flex-wrap justify-between gap-3">
        <button type="button" onClick={onBack} className="signal-btn signal-btn-secondary">
          ← Build
        </button>
        <button type="button" onClick={onContinue} className="signal-btn signal-btn-primary">
          Open the blueprint →
        </button>
      </div>
    </div>
  );
}
