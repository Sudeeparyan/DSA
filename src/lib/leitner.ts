const KEY = "nc150-leitner-v1";

export interface CardState {
  box: 1 | 2 | 3 | 4 | 5;
  dueAt: string;
}

function canUseStorage(): boolean {
  return typeof window !== "undefined" && !!window.localStorage;
}

export function loadLeitner(): Record<string, CardState> {
  if (!canUseStorage()) return {};
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Record<string, CardState>) : {};
  } catch {
    return {};
  }
}

function save(all: Record<string, CardState>) {
  if (!canUseStorage()) return;
  localStorage.setItem(KEY, JSON.stringify(all));
}

const INTERVALS_DAYS = [0, 1, 3, 7, 14, 30];

export function markCard(slug: string, remembered: boolean) {
  const all = loadLeitner();
  const current = all[slug]?.box ?? 1;
  const nextBox = remembered
    ? (Math.min(5, current + 1) as CardState["box"])
    : 1;
  const days = INTERVALS_DAYS[nextBox];
  const due = new Date();
  due.setDate(due.getDate() + days);
  all[slug] = { box: nextBox, dueAt: due.toISOString() };
  save(all);
}

export function dueCards(slugs: string[]): string[] {
  const all = loadLeitner();
  const now = Date.now();
  return slugs.filter((slug) => {
    const card = all[slug];
    if (!card) return true;
    return new Date(card.dueAt).getTime() <= now;
  });
}
