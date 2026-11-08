import Link from "next/link";
import { getPatterns } from "@/lib/problems";

export default function PatternsPage() {
  const patterns = getPatterns();
  return (
    <div className="mx-auto max-w-3xl space-y-8 px-4 py-8">
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold">Patterns cheat-sheet</h1>
        <p className="text-muted leading-relaxed">
          One page of reusable templates. Interviewers listen for these names.
        </p>
      </header>
      <div className="space-y-6">
        {patterns.map((p) => (
          <section
            key={p.id}
            className="rounded-3xl border border-border bg-card p-5"
          >
            <h2 className="text-2xl font-semibold">{p.name}</h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">{p.summary}</p>
            <pre className="mt-4 overflow-x-auto rounded-2xl bg-[#0f172a] p-4 font-mono text-xs text-slate-100">
              {p.templatePython}
            </pre>
            <div className="mt-4 flex flex-wrap gap-2">
              {p.problemSlugs.map((slug) => (
                <Link
                  key={slug}
                  href={`/problem/${slug}/`}
                  className="rounded-full border border-border px-3 py-1 text-xs"
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
