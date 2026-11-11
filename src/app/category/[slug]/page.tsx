import Link from "next/link";
import { notFound } from "next/navigation";
import { getCatalog, getProblemsByCategory } from "@/lib/problems";
import { DifficultyChip } from "@/components/ui/DifficultyChip";
import { accentFor } from "@/lib/categories";
import { CategoryProgress } from "./CategoryProgress";

export function generateStaticParams() {
  return getCatalog().categories.map((c) => ({ slug: c.slug }));
}

export default async function CategoryPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const cat = getCatalog().categories.find((c) => c.slug === slug);
  if (!cat) notFound();
  const problems = getProblemsByCategory(slug);
  const accent = accentFor(slug);

  return (
    <div className="mx-auto max-w-3xl space-y-8 px-4 py-10">
      <header className="space-y-3">
        <p className="section-kicker">Category</p>
        <h1
          className="brand-font text-5xl font-extrabold tracking-tight"
          style={{ color: accent }}
        >
          {cat.name}
        </h1>
        <p className="teach text-lg text-muted">{cat.whyItMatters}</p>
        <CategoryProgress slugs={problems.map((p) => p.slug)} />
      </header>
      <ul className="space-y-2">
        {problems.map((p, i) => (
          <li key={p.slug}>
            <Link
              href={`/problem/${p.slug}/`}
              className="group flex flex-wrap items-center gap-3 rounded-2xl border border-border bg-card/90 px-4 py-3.5 transition hover:border-transparent"
              style={{
                boxShadow: `inset 3px 0 0 0 ${accent}`,
              }}
            >
              <span className="font-mono text-xs text-muted">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="font-semibold group-hover:text-accent">
                {p.title}
              </span>
              <DifficultyChip difficulty={p.difficulty} />
              <span className="ml-auto hidden gap-1 text-[10px] font-bold uppercase tracking-wide text-muted sm:flex">
                {p.hasStory && <span className="rounded-md bg-accent-soft px-1.5 py-0.5">Story</span>}
                {p.hasAnimation && <span className="rounded-md bg-accent-soft px-1.5 py-0.5">Anim</span>}
                {p.hasCode && <span className="rounded-md bg-accent-soft px-1.5 py-0.5">Code</span>}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
