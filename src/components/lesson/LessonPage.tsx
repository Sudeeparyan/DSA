"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import type { Lesson, LessonMeta } from "@/lib/lesson";
import { loadUnderstood, setLastSlug, setUnderstood } from "@/lib/progress";
import { Rich } from "./Rich";
import { Walkthrough } from "./Walkthrough";

function Understood({ slug }: { slug: string }) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    setOn(loadUnderstood().has(slug));
  }, [slug]);
  return (
    <label className={on ? "understood understood-on" : "understood"}>
      <input
        type="checkbox"
        checked={on}
        onChange={(e) => {
          setOn(e.target.checked);
          setUnderstood(slug, e.target.checked);
        }}
      />
      I understand this one
    </label>
  );
}

export function LessonPage({
  lesson,
  prev,
  next,
  position,
  total,
  categoryName,
}: {
  lesson: Lesson;
  prev: LessonMeta | null;
  next: LessonMeta | null;
  position: number;
  total: number;
  categoryName: string;
}) {
  useEffect(() => {
    setLastSlug(lesson.slug);
  }, [lesson.slug]);

  return (
    <article className="lesson">
      <header className="lesson-head">
        <div className="lesson-crumbs">
          <Link href="/">All problems</Link>
          <span aria-hidden>›</span>
          <span>{categoryName}</span>
          <span aria-hidden>›</span>
          <span>
            {position} of {total}
          </span>
        </div>
        <div className="lesson-title-row">
          <h1>{lesson.title}</h1>
          <span className={`diff diff-${lesson.difficulty.toLowerCase()}`}>{lesson.difficulty}</span>
          {lesson.pattern && <span className="pattern">{lesson.pattern}</span>}
        </div>
      </header>

      <div className="lesson-intro">
        <section className="card" aria-labelledby="q-title">
          <h2 id="q-title" className="card-title">
            <span className="card-num">1</span> The question
          </h2>
          <p className="prose">
            <Rich text={lesson.statement} />
          </p>
          <div className="example">
            <div className="example-row">
              <span className="example-key">{lesson.example.output ? "Input" : "Calls"}</span>
              <pre>{lesson.example.input}</pre>
            </div>
            {lesson.example.output && (
              <div className="example-row">
                <span className="example-key">Output</span>
                <pre>{lesson.example.output}</pre>
              </div>
            )}
            {lesson.example.why && (
              <div className="example-row">
                <span className="example-key">Why</span>
                <p>
                  <Rich text={lesson.example.why} />
                </p>
              </div>
            )}
          </div>
          {lesson.more.length > 0 && (
            <details className="more">
              <summary>More examples</summary>
              <ul>
                {lesson.more.map((ex, i) => (
                  <li key={i}>
                    <pre>{ex.input}</pre>
                    {ex.output && <span aria-hidden>→</span>}
                    {ex.output && <pre>{ex.output}</pre>}
                  </li>
                ))}
              </ul>
            </details>
          )}
        </section>

        <section className="card" aria-labelledby="idea-title">
          <h2 id="idea-title" className="card-title">
            <span className="card-num">2</span> The idea
          </h2>
          <ol className="idea">
            {lesson.idea.map((point, i) => (
              <li key={i}>
                <Rich text={point} />
              </li>
            ))}
          </ol>
        </section>
      </div>

      <section className="card card-walk" aria-labelledby="walk-title">
        <h2 id="walk-title" className="card-title">
          <span className="card-num">3</span> Watch it solve the example
        </h2>
        <Walkthrough lesson={lesson} />
      </section>

      <section className="card" aria-labelledby="cost-title">
        <h2 id="cost-title" className="card-title">
          <span className="card-num">4</span> How fast is it?
        </h2>
        <div className="cost">
          <div>
            <div className="cost-label">Time</div>
            <div className="cost-value">{lesson.complexity.time}</div>
            <p>
              <Rich text={lesson.complexity.timeWhy} />
            </p>
          </div>
          <div>
            <div className="cost-label">Extra space</div>
            <div className="cost-value">{lesson.complexity.space}</div>
            <p>
              <Rich text={lesson.complexity.spaceWhy} />
            </p>
          </div>
        </div>
      </section>

      <footer className="lesson-foot">
        <Understood slug={lesson.slug} />
        <nav className="lesson-nav" aria-label="Other problems">
          {prev ? (
            <Link href={`/problem/${prev.slug}/`} className="btn">
              ← {prev.title}
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link href={`/problem/${next.slug}/`} className="btn btn-primary">
              Next: {next.title} →
            </Link>
          ) : (
            <Link href="/" className="btn btn-primary">
              Back to all problems
            </Link>
          )}
        </nav>
      </footer>
    </article>
  );
}
