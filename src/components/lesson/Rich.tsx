import { Fragment, type ReactNode } from "react";

/**
 * Lesson text uses three inline marks: **bold**, *emphasis* and `code`.
 * This turns such a string into React nodes (no HTML injection involved).
 */

const MARK = /(`[^`]+`|\*\*[^*]+(?:\*(?!\*)[^*]+)*\*\*|\*[^*\s](?:[^*]*[^*\s])?\*)/g;

function render(text: string, keyBase: string): ReactNode[] {
  const out: ReactNode[] = [];
  let last = 0;
  let n = 0;
  for (const match of text.matchAll(MARK)) {
    const at = match.index ?? 0;
    if (at > last) out.push(text.slice(last, at));
    const token = match[0];
    const key = `${keyBase}-${n++}`;
    if (token.startsWith("`")) {
      out.push(<code key={key}>{token.slice(1, -1)}</code>);
    } else if (token.startsWith("**")) {
      out.push(<strong key={key}>{render(token.slice(2, -2), key)}</strong>);
    } else {
      out.push(<em key={key}>{render(token.slice(1, -1), key)}</em>);
    }
    last = at + token.length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

export function Rich({ text }: { text: string }) {
  return <Fragment>{render(text, "r")}</Fragment>;
}
