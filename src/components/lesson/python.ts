/** A very small Python tokenizer — just enough to colour the solution code. */

/** `op` is a run of operator characters (`->`, `+=`, `==`, `(`...); lesson.css keeps each one on one line. */
export type TokenKind = "kw" | "builtin" | "str" | "num" | "com" | "fn" | "self" | "op" | "plain";

export interface Token {
  kind: TokenKind;
  text: string;
}

const KEYWORDS = new Set([
  "def", "class", "return", "if", "elif", "else", "for", "while", "in", "not", "and", "or", "is",
  "None", "True", "False", "break", "continue", "pass", "import", "from", "as", "lambda", "with",
  "yield", "try", "except", "finally", "raise", "global", "nonlocal", "del", "assert",
]);

const BUILTINS = new Set([
  "len", "range", "enumerate", "max", "min", "sum", "sorted", "list", "dict", "set", "tuple", "int",
  "str", "float", "bool", "abs", "zip", "map", "filter", "any", "all", "reversed", "ord", "chr",
  "divmod", "isinstance", "print", "pow", "round", "iter", "next",
]);

const PIECE =
  /(#.*$)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+)|([^\sA-Za-z_0-9"'#]+|.)/g;

export function tokenizeLine(line: string): Token[] {
  const tokens: Token[] = [];
  let naming = false; // the identifier right after `def` / `class`
  for (const m of line.matchAll(PIECE)) {
    const text = m[0];
    let kind: TokenKind = "plain";
    if (m[1]) kind = "com";
    else if (m[2]) kind = "str";
    else if (m[3]) kind = "num";
    else if (m[6]) kind = "op";
    else if (m[4]) {
      if (naming) {
        kind = "fn";
        naming = false;
      } else if (KEYWORDS.has(text)) {
        kind = "kw";
        naming = text === "def" || text === "class";
      } else if (text === "self") kind = "self";
      else if (BUILTINS.has(text)) kind = "builtin";
    }
    const prev = tokens[tokens.length - 1];
    if (prev && prev.kind === kind && kind === "plain") prev.text += text;
    else tokens.push({ kind, text });
  }
  return tokens;
}
