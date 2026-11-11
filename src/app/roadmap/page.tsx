import Link from "next/link";
import { getCatalog } from "@/lib/problems";
import { accentFor } from "@/lib/categories";

export default function RoadmapPage() {
  const { categories } = getCatalog();
  return (
    <div className="mx-auto max-w-3xl space-y-8 px-4 py-10">
      <header className="space-y-3">
        <p className="section-kicker">Learning order</p>
        <h1 className="brand-font text-5xl font-extrabold tracking-tight">
          Roadmap
        </h1>
        <p className="teach text-lg text-muted">
          Eighteen patterns, in NeetCode order. Finish one family before jumping
          ahead — Google interviews reward pattern recognition.
        </p>
      </header>
      <ol className="relative space-y-4 before:absolute before:bottom-4 before:left-[1.15rem] before:top-4 before:w-px before:bg-border">
        {categories.map((c, i) => (
          <li key={c.slug} className="relative pl-12">
            <span
              className="absolute left-0 top-5 flex h-9 w-9 items-center justify-center rounded-full border border-border bg-card font-mono text-xs font-bold"
              style={{ color: accentFor(c.slug) }}
            >
              {String(i + 1).padStart(2, "0")}
            </span>
            <Link
              href={`/category/${c.slug}/`}
              className="block rounded-[1.5rem] border border-border bg-card/90 p-5 transition hover:-translate-y-0.5"
            >
              <h2
                className="brand-font text-2xl font-bold"
                style={{ color: accentFor(c.slug) }}
              >
                {c.name}
              </h2>
              <p className="teach mt-2 text-base text-muted">
                <strong className="text-foreground">Why Google cares: </strong>
                {c.whyItMatters}
              </p>
              <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-muted">
                {c.problemSlugs.length} problems
              </p>
            </Link>
          </li>
        ))}
      </ol>
    </div>
  );
}
