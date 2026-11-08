"use client";

import { useEffect, useState } from "react";
import {
  getEntry,
  setNotes,
  setStatus,
  type ProblemStatus,
} from "@/lib/progress";
import { clsx } from "clsx";

const statuses: { id: ProblemStatus; label: string }[] = [
  { id: "not_started", label: "Not started" },
  { id: "learning", label: "Learning" },
  { id: "understood", label: "Understood" },
  { id: "need_revision", label: "Need revision" },
];

export function ProgressControls({ slug }: { slug: string }) {
  const [status, setLocalStatus] = useState<ProblemStatus>("not_started");
  const [notes, setLocalNotes] = useState("");

  useEffect(() => {
    const e = getEntry(slug);
    setLocalStatus(e.status);
    setLocalNotes(e.notes);
  }, [slug]);

  return (
    <div className="space-y-4 rounded-3xl border border-border bg-card p-4 sm:p-5">
      <div>
        <div className="mb-2 text-sm font-semibold">Mark your status</div>
        <div className="flex flex-wrap gap-2">
          {statuses.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => {
                setLocalStatus(s.id);
                setStatus(slug, s.id);
              }}
              className={clsx(
                "min-h-11 rounded-xl px-3 py-2 text-sm font-medium",
                status === s.id
                  ? "bg-accent text-white"
                  : "border border-border bg-background",
              )}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>
      <div>
        <label htmlFor="notes" className="mb-2 block text-sm font-semibold">
          Private notes (saved on this device)
        </label>
        <textarea
          id="notes"
          value={notes}
          onChange={(e) => {
            setLocalNotes(e.target.value);
            setNotes(slug, e.target.value);
          }}
          rows={4}
          className="w-full rounded-2xl border border-border bg-background px-3 py-2 text-sm"
          placeholder="Write reminders for your future self…"
        />
      </div>
    </div>
  );
}
