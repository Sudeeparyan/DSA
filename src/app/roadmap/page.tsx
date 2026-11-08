import Link from "next/link";
import { getCatalog } from "@/lib/problems";
import { accentFor } from "@/lib/categories";

export default function RoadmapPage() {
  const { categories } = getCatalog();
  return (
    <div className="mx-auto max-w-3xl space-y-8 px-4 py-8">
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold tracking-tight">Roadmap</h1>
        <p className="text-muted leading-relaxed">
          Eighteen patterns, in the NeetCode learning order. Finish one family
          before jumping ahead — Google interviews reward pattern recognition.
        </p>
      </header>
      <ol className="space-y-4">
        {categories.map((c, i) => (
          <li key={c.slug}>
            <Link
              href={`/category/${c.slug}/`}
              className="block rounded-3xl border border-border bg-card p-5 hover:border-accent"
            >
              <div className="flex items-baseline gap-3">
                <span className="font-mono text-sm text-muted">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <h2
                  className="text-xl font-semibold"
                  style={{ color: accentFor(c.slug) }}
                >
                  {c.name}
                </h2>
              </div>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                <strong className="text-foreground">Why this matters at Google: </strong>
                {c.whyItMatters}
              </p>
              <p className="mt-2 text-xs text-muted">
                {c.problemSlugs.length} problems
              </p>
            </Link>
          </li>
        ))}
      </ol>
    </div>
  );
}
