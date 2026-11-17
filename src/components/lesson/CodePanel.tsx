"use client";

import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import { tokenizeLine } from "./python";
import { Rich } from "./Rich";

/** What a code line does, in plain words: line number → text (from the lesson's `say`). */
export type Readings = Record<string, string> | undefined;

/**
 * The solution, with the line the current step is explaining lit up.  Under it, that line is
 * read out in plain words; pointing at (or tapping) another line reads that one instead.
 */
export function CodePanel({
  code,
  line,
  say,
  reduced = false,
}: {
  code: string;
  line: number;
  say?: Readings;
  /** the learner asked for less motion: jump to the line instead of gliding */
  reduced?: boolean;
}) {
  // a line the learner points at or taps; the next step goes back to the running line
  const [peek, setPeek] = useState<number | null>(null);
  useEffect(() => setPeek(null), [line]);
  const shown = peek !== null && say?.[peek] ? peek : line;
  const reading = say?.[shown];
  const lines = useMemo(
    () =>
      code.split("\n").map((raw) => {
        const rest = raw.trimStart();
        return { indent: raw.slice(0, raw.length - rest.length), tokens: tokenizeLine(rest) };
      }),
    [code],
  );
  const box = useRef<HTMLDivElement>(null);
  const rows = useRef<(HTMLDivElement | null)[]>([]);
  const liveLine = useRef(line);

  /** Scrolls the panel (never the page) so the live line sits comfortably in view. */
  const reveal = useCallback((behavior: ScrollBehavior) => {
    const container = box.current;
    const row = rows.current[liveLine.current - 1];
    if (!container || !row) return;
    // the row's position inside the panel's scrolled content.  (Not row.offsetTop: that is
    // measured from the nearest positioned ancestor, which lies outside the panel, so it
    // also counts everything above the panel and scrolled the live line out of sight.)
    const top = row.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop;
    const height = row.offsetHeight;
    const margin = height * 2.5;
    if (top - margin < container.scrollTop || top + height + margin > container.scrollTop + container.clientHeight) {
      container.scrollTo({ top: Math.max(0, top - container.clientHeight / 2 + height / 2), behavior });
    }
  }, []);

  useEffect(() => {
    liveLine.current = line;
    reveal(reduced ? "auto" : "smooth");
  }, [line, reduced, reveal]);

  // On wide screens the panel is as tall as the column beside it, so it shrinks or grows with
  // the caption.  Two steps can explain the same line with captions of different lengths; the
  // line does not change then, so re-check whenever the panel itself changes height.
  useEffect(() => {
    const container = box.current;
    if (!container) return;
    let height = container.clientHeight;
    const observer = new ResizeObserver(() => {
      if (container.clientHeight === height) return;
      height = container.clientHeight;
      reveal("auto");
    });
    observer.observe(container);
    return () => observer.disconnect();
  }, [reveal]);

  return (
    <>
      <div
        ref={box}
        className="code-panel"
        role="region"
        aria-label="Solution code"
        tabIndex={0}
        onPointerLeave={(e) => {
          if (e.pointerType === "mouse") setPeek(null);
        }}
      >
        {lines.map(({ indent, tokens }, i) => {
          const n = i + 1;
          const live = n === line;
          const readable = !!say?.[n];
          const classes = ["code-line"];
          if (live) classes.push("code-line-live");
          if (readable) classes.push("code-line-says");
          if (peek === n && !live) classes.push("code-line-peek");
          return (
            <div
              key={i}
              ref={(el) => {
                rows.current[i] = el;
              }}
              className={classes.join(" ")}
              aria-current={live ? "step" : undefined}
              onPointerEnter={(e) => {
                if (e.pointerType === "mouse" && readable) setPeek(n);
              }}
              onClick={() => {
                if (readable) setPeek((p) => (p === n ? null : n));
              }}
            >
              <span className="code-no">{i + 1}</span>
              {/* a long line wraps instead of running off the panel; the wrapped part hangs two
                  columns further in than the line itself, so it cannot be mistaken for a new line
                  (lesson.css narrows the indent on phones, and the indent itself never wraps) */}
              <span className="code-text" style={{ "--n": indent.length } as CSSProperties}>
                {indent && <span className="code-indent">{indent}</span>}
                {tokens.length === 0
                  ? indent
                    ? null
                    : " "
                  : tokens.map((t, j) => (
                      <span key={j} className={`tok-${t.kind}`}>
                        {t.text}
                      </span>
                    ))}
              </span>
            </div>
          );
        })}
      </div>
      {say && (
        <div className={reading ? "code-say" : "code-say code-say-none"}>
          {reading ? (
            <>
              <div className="code-say-head">
                Line {shown} in plain words
                {shown !== line && <span className="code-say-off"> (not the running line)</span>}
              </div>
              <p>
                <Rich text={reading} />
              </p>
            </>
          ) : (
            <p className="code-say-hint">Point at or tap a line of code to read it in plain words.</p>
          )}
        </div>
      )}
    </>
  );
}

/** One line of the solution, coloured like the code panel (used where the panel is out of sight). */
export function CodeLine({ code, line, say }: { code: string; line: number; say?: Readings }) {
  const tokens = useMemo(() => tokenizeLine((code.split("\n")[line - 1] ?? "").trim()), [code, line]);
  if (line < 1 || tokens.length === 0) return null;
  const reading = say?.[line];
  return (
    <div className="caption-code" aria-hidden>
      <div className="caption-code-row">
        <span className="caption-code-no">line {line}</span>
        <code>
          {tokens.map((t, j) => (
            <span key={j} className={`tok-${t.kind}`}>
              {t.text}
            </span>
          ))}
        </code>
      </div>
      {reading && (
        <p className="caption-say">
          <Rich text={reading} />
        </p>
      )}
    </div>
  );
}
