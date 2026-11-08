"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (!mounted) {
    return (
      <button
        type="button"
        className="min-h-10 rounded-full border border-border px-3 py-2 text-sm font-semibold"
        aria-label="Toggle theme"
      >
        Theme
      </button>
    );
  }

  const dark = resolvedTheme === "dark";
  return (
    <button
      type="button"
      onClick={() => setTheme(dark ? "light" : "dark")}
      className="min-h-10 rounded-full border border-border bg-card px-3.5 py-2 text-sm font-semibold hover:border-accent"
      aria-label={`Switch to ${dark ? "light" : "dark"} mode`}
    >
      {dark ? "Light" : "Dark"}
    </button>
  );
}
