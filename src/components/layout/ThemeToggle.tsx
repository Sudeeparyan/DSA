"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) {
    return (
      <button
        type="button"
        className="rounded-xl border border-border px-3 py-2 text-sm"
        aria-label="Toggle theme"
      >
        Theme
      </button>
    );
  }
  const next = theme === "dark" ? "light" : "dark";
  return (
    <button
      type="button"
      onClick={() => setTheme(next)}
      className="rounded-xl border border-border bg-card px-3 py-2 text-sm font-medium hover:border-accent"
      aria-label={`Switch to ${next} mode`}
    >
      {theme === "dark" ? "Light" : "Dark"}
    </button>
  );
}
