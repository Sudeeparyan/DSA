import Link from "next/link";
import { getPatterns } from "@/lib/problems";

export default function PatternsPage() {
  const patterns = getPatterns();
  return (
    <div className="mx-auto max-w-3xl space-y-8 px-4 py-10">
      <header className="space-y-3">
        <p className="section-kicker">Cheat-sheet</p>
        <h1 className="brand-font text-5xl font-extrabold tracking-tight">
          Patterns
        </h1>
        <p className="teach text-lg text-muted">
          Name the pattern early in an interview. These templates are the
          phrases Google listeners expect.
        </p>
      </header>
      <div className="space-y-5">
        {patterns.map((p) => (
          <section
            key={p.id}
            className="rounded-[1.6rem] border border-border bg-card/90 p-5"
          >
            <h2 className="brand-font text-2xl font-bold">{p.name}</h2>
            <p className="teach mt-2 text-base text-muted">{p.summary}</p>
            <pre className="mt-4 overflow-x-auto rounded-2xl bg-panel p-4 font-mono text-xs leading-6 text-panel-fg">
              {p.templatePython}
            </pre>
            <div className="mt-4 flex flex-wrap gap-2">
              {p.problemSlugs.map((slug) => (
                <Link
                  key={slug}
                  href={`/problem/${slug}/`}
                  className="rounded-full border border-border px-3 py-1 text-xs font-medium hover:border-accent"
                >
                  {slug}
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
