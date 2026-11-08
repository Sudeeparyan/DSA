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
    <div className="mx-auto max-w-3xl space-y-6 px-4 py-8">
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold" style={{ color: accent }}>
          {cat.name}
        </h1>
        <p className="leading-relaxed text-muted">{cat.whyItMatters}</p>
        <CategoryProgress slugs={problems.map((p) => p.slug)} />
      </header>
      <ul className="space-y-2">
        {problems.map((p) => (
          <li key={p.slug}>
            <Link
              href={`/problem/${p.slug}/`}
              className="flex flex-wrap items-center gap-3 rounded-2xl border border-border bg-card px-4 py-3 hover:border-accent"
            >
              <span className="font-mono text-xs text-muted">
                #{p.leetcodeNumber}
              </span>
              <span className="font-semibold">{p.title}</span>
              <DifficultyChip difficulty={p.difficulty} />
              <span className="ml-auto flex gap-1 text-[10px] uppercase tracking-wide text-muted">
                {p.hasStory && (
                  <span className="rounded bg-accent-soft px-1.5 py-0.5">Story</span>
                )}
                {p.hasAnimation && (
                  <span className="rounded bg-accent-soft px-1.5 py-0.5">Anim</span>
                )}
                {p.hasCode && (
                  <span className="rounded bg-accent-soft px-1.5 py-0.5">Code</span>
                )}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
