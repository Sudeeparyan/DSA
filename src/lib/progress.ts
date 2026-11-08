export type ProblemStatus =
  | "not_started"
  | "learning"
  | "understood"
  | "need_revision";

export interface ProgressEntry {
  status: ProblemStatus;
  notes: string;
  updatedAt: string;
}

const KEY = "nc150-progress-v1";
const LAST_KEY = "nc150-last-slug";

function canUseStorage(): boolean {
  return typeof window !== "undefined" && !!window.localStorage;
}

export function loadProgress(): Record<string, ProgressEntry> {
  if (!canUseStorage()) return {};
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Record<string, ProgressEntry>) : {};
  } catch {
    return {};
  }
}

export function saveProgress(all: Record<string, ProgressEntry>) {
  if (!canUseStorage()) return;
  localStorage.setItem(KEY, JSON.stringify(all));
}

export function getEntry(slug: string): ProgressEntry {
  return (
    loadProgress()[slug] ?? {
      status: "not_started",
      notes: "",
      updatedAt: new Date(0).toISOString(),
    }
  );
}

export function setStatus(slug: string, status: ProblemStatus) {
  const all = loadProgress();
  all[slug] = {
    ...(all[slug] ?? { notes: "" }),
    status,
    notes: all[slug]?.notes ?? "",
    updatedAt: new Date().toISOString(),
  };
  saveProgress(all);
  setLastSlug(slug);
}

export function setNotes(slug: string, notes: string) {
  const all = loadProgress();
  all[slug] = {
    status: all[slug]?.status ?? "not_started",
    notes,
    updatedAt: new Date().toISOString(),
  };
  saveProgress(all);
}

export function setLastSlug(slug: string) {
  if (!canUseStorage()) return;
  localStorage.setItem(LAST_KEY, slug);
}

export function getLastSlug(): string | null {
  if (!canUseStorage()) return null;
  return localStorage.getItem(LAST_KEY);
}

export function countByStatus(
  slugs: string[],
): Record<ProblemStatus, number> {
  const all = loadProgress();
  const counts: Record<ProblemStatus, number> = {
    not_started: 0,
    learning: 0,
    understood: 0,
    need_revision: 0,
  };
  for (const slug of slugs) {
    const s = all[slug]?.status ?? "not_started";
    counts[s] += 1;
  }
  return counts;
}
