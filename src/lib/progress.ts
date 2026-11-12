/**
 * Progress kept in the browser (localStorage): which problems the learner has
 * ticked "I understand this one", and the last lesson they opened.
 *
 * Nothing here ever throws: storage can be switched off, full, or blocked
 * (private windows, strict cookie settings).  Progress then just is not saved.
 *
 * Stored format, kept as it is so existing progress survives updates:
 *   "nc150-progress-v1" → { [slug]: { status, notes, updatedAt } }
 *     (`status` is "understood" when ticked; `notes` is no longer shown but kept)
 *   "nc150-last-slug"   → slug of the last lesson opened
 */

interface ProgressEntry {
  status: string;
  notes: string;
  updatedAt: string;
}

const KEY = "nc150-progress-v1";
const LAST_KEY = "nc150-last-slug";
/** fired on this tab when a tick changes ("storage" covers the other tabs) */
const EVENT = "nc150-progress";

function storage(): Storage | null {
  try {
    // reading window.localStorage itself throws in some browsers when storage is blocked
    return typeof window !== "undefined" ? window.localStorage : null;
  } catch {
    return null;
  }
}

function loadAll(): Record<string, ProgressEntry> {
  try {
    const raw = storage()?.getItem(KEY);
    const parsed: unknown = raw ? JSON.parse(raw) : null;
    return parsed && typeof parsed === "object" && !Array.isArray(parsed)
      ? (parsed as Record<string, ProgressEntry>)
      : {};
  } catch {
    return {};
  }
}

function saveAll(all: Record<string, ProgressEntry>): void {
  try {
    storage()?.setItem(KEY, JSON.stringify(all));
    window.dispatchEvent(new Event(EVENT));
  } catch {
    /* storage is full or blocked; the change just will not persist */
  }
}

/** Slugs of every problem ticked "I understand this one". */
export function loadUnderstood(): Set<string> {
  const all = loadAll();
  return new Set(Object.keys(all).filter((slug) => all[slug]?.status === "understood"));
}

export function setUnderstood(slug: string, understood: boolean): void {
  const all = loadAll();
  all[slug] = {
    notes: all[slug]?.notes ?? "",
    status: understood ? "understood" : "not_started",
    updatedAt: new Date().toISOString(),
  };
  saveAll(all);
}

/** Calls `listener` whenever a tick changes (in this tab or another one). Returns the unsubscribe. */
export function onProgressChange(listener: () => void): () => void {
  window.addEventListener(EVENT, listener);
  window.addEventListener("storage", listener);
  return () => {
    window.removeEventListener(EVENT, listener);
    window.removeEventListener("storage", listener);
  };
}

export function setLastSlug(slug: string): void {
  try {
    storage()?.setItem(LAST_KEY, slug);
  } catch {
    /* ignore */
  }
}

export function getLastSlug(): string | null {
  try {
    return storage()?.getItem(LAST_KEY) ?? null;
  } catch {
    return null;
  }
}
