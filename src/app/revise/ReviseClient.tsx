"use client";

import { useEffect, useMemo, useState } from "react";
import { dueCards, markCard } from "@/lib/leitner";

interface Card {
  slug: string;
  title: string;
  pattern: string;
  complexity: string;
  oneLiner: string;
}

type Face = "pattern" | "complexity" | "idea";

export function ReviseClient({ cards }: { cards: Card[] }) {
  const [queue, setQueue] = useState<Card[]>([]);
  const [face, setFace] = useState<Face>("pattern");
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    const due = new Set(dueCards(cards.map((c) => c.slug)));
    setQueue(cards.filter((c) => due.has(c.slug)));
  }, [cards]);

  const current = queue[0];

  const prompt = useMemo(() => {
    if (!current) return "";
    if (face === "pattern") return `What pattern does "${current.title}" use?`;
    if (face === "complexity")
      return `What is the time & space complexity of "${current.title}"?`;
    return `Explain the idea of "${current.title}" in one sentence.`;
  }, [current, face]);

  const answer = useMemo(() => {
    if (!current) return "";
    if (face === "pattern") return current.pattern;
    if (face === "complexity") return current.complexity;
    return current.oneLiner;
  }, [current, face]);

  function grade(ok: boolean) {
    if (!current) return;
    markCard(current.slug, ok);
    setFlipped(false);
    setFace((f) =>
      f === "pattern" ? "complexity" : f === "complexity" ? "idea" : "pattern",
    );
    setQueue((q) => q.slice(1));
  }

  if (!current) {
    return (
      <div className="mx-auto max-w-xl px-4 py-20 text-center">
        <p className="section-kicker">Leitner boxes</p>
        <h1 className="brand-font mt-3 text-4xl font-extrabold">All caught up</h1>
        <p className="teach mt-3 text-muted">
          No cards due right now. Come back later — progress stays on this
          device.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-xl space-y-6 px-4 py-10">
      <header>
        <p className="section-kicker">Spaced repetition</p>
        <h1 className="brand-font mt-2 text-4xl font-extrabold">Revision</h1>
        <p className="mt-2 text-sm text-muted">{queue.length} cards in this session</p>
      </header>
      <button
        type="button"
        onClick={() => setFlipped((f) => !f)}
        className="min-h-64 w-full rounded-[1.8rem] border border-border bg-panel p-7 text-left text-panel-fg shadow-sm"
        aria-label="Flip flashcard"
      >
        <div className="text-xs font-bold uppercase tracking-[0.18em] text-white/45">
          {flipped ? "Answer" : "Question"}
        </div>
        <p className="brand-font mt-5 text-2xl font-bold leading-snug">
          {flipped ? answer : prompt}
        </p>
        <p className="mt-8 text-sm text-white/40">Tap to flip</p>
      </button>
      <div className="flex gap-3">
        <button
          type="button"
          className="min-h-12 flex-1 rounded-full border border-rejected/40 bg-rejected/10 font-bold text-rejected"
          onClick={() => grade(false)}
        >
          Forgot
        </button>
        <button
          type="button"
          className="min-h-12 flex-1 rounded-full bg-matched font-bold text-white"
          onClick={() => grade(true)}
        >
          Got it
        </button>
      </div>
    </div>
  );
}
