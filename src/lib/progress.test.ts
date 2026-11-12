import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { getLastSlug, loadUnderstood, setLastSlug, setUnderstood } from "./progress";

/** A tiny in-memory stand-in for the browser's window + localStorage. */
function fakeWindow(store: Map<string, string>, { blocked = false } = {}) {
  const localStorage = {
    getItem: (k: string) => store.get(k) ?? null,
    setItem: (k: string, v: string) => void store.set(k, v),
  };
  const win = {
    dispatchEvent: () => true,
    addEventListener: () => {},
    removeEventListener: () => {},
  };
  Object.defineProperty(win, "localStorage", {
    get() {
      if (blocked) throw new Error("SecurityError: storage is blocked");
      return localStorage;
    },
  });
  return win;
}

const g = globalThis as { window?: unknown };

describe("progress", () => {
  let store: Map<string, string>;

  beforeEach(() => {
    store = new Map();
    g.window = fakeWindow(store);
  });

  afterEach(() => {
    delete g.window;
  });

  it("remembers ticks and un-ticks", () => {
    setUnderstood("two-sum", true);
    setUnderstood("3sum", true);
    expect([...loadUnderstood()].sort()).toEqual(["3sum", "two-sum"]);
    setUnderstood("two-sum", false);
    expect([...loadUnderstood()]).toEqual(["3sum"]);
  });

  it("reads progress saved by earlier versions of the site", () => {
    store.set(
      "nc150-progress-v1",
      JSON.stringify({
        "two-sum": { status: "understood", notes: "my note", updatedAt: "2026-01-01T00:00:00.000Z" },
        "3sum": { status: "learning", notes: "", updatedAt: "2026-01-01T00:00:00.000Z" },
      }),
    );
    expect([...loadUnderstood()]).toEqual(["two-sum"]);
    setUnderstood("valid-anagram", true);
    // other entries, and their notes, are kept
    const saved = JSON.parse(store.get("nc150-progress-v1")!);
    expect(saved["two-sum"].notes).toBe("my note");
    expect(saved["3sum"].status).toBe("learning");
  });

  it("treats damaged data as no progress instead of crashing", () => {
    for (const bad of ["not json", "null", "[1,2]", '"text"']) {
      store.set("nc150-progress-v1", bad);
      expect(loadUnderstood().size).toBe(0);
    }
  });

  it("remembers the last lesson opened", () => {
    expect(getLastSlug()).toBeNull();
    setLastSlug("lru-cache");
    expect(getLastSlug()).toBe("lru-cache");
  });

  it("never throws when storage is blocked", () => {
    g.window = fakeWindow(store, { blocked: true });
    expect(() => setUnderstood("two-sum", true)).not.toThrow();
    expect(loadUnderstood().size).toBe(0);
    expect(() => setLastSlug("two-sum")).not.toThrow();
    expect(getLastSlug()).toBeNull();
  });

  it("does nothing on the server, where there is no window", () => {
    delete g.window;
    expect(loadUnderstood().size).toBe(0);
    expect(getLastSlug()).toBeNull();
  });
});
