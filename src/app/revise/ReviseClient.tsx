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
      <div className="mx-auto max-w-xl px-4 py-16 text-center">
        <h1 className="text-3xl font-semibold">Revision mode</h1>
        <p className="mt-3 text-muted">
          No cards due right now. Come back later — Leitner boxes are saved on
          this device.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-xl space-y-6 px-4 py-8">
      <h1 className="text-3xl font-semibold">Revision mode</h1>
      <p className="text-sm text-muted">{queue.length} cards in this session</p>
      <button
        type="button"
        onClick={() => setFlipped((f) => !f)}
        className="min-h-56 w-full rounded-3xl border border-border bg-card p-6 text-left shadow-sm"
        aria-label="Flip flashcard"
      >
        <div className="text-xs uppercase tracking-wide text-muted">
          {flipped ? "Answer" : "Question"}
        </div>
        <p className="mt-4 text-xl font-semibold leading-snug">
          {flipped ? answer : prompt}
        </p>
      </button>
      <div className="flex gap-3">
        <button
          type="button"
          className="min-h-12 flex-1 rounded-2xl border border-rejected/40 bg-rejected/10 font-semibold text-rejected"
          onClick={() => grade(false)}
        >
          Forgot
        </button>
        <button
          type="button"
          className="min-h-12 flex-1 rounded-2xl bg-matched/90 font-semibold text-white"
          onClick={() => grade(true)}
        >
          Got it
        </button>
      </div>
    </div>
  );
}
