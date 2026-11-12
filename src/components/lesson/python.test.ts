import { describe, expect, it } from "vitest";
import { tokenizeLine, type TokenKind } from "./python";

const kinds = (line: string) => tokenizeLine(line).map((t) => [t.kind, t.text] as [TokenKind, string]);

describe("tokenizeLine", () => {
  it("keeps the text exactly as written", () => {
    const line = 'def twoSum(self, nums: List[int], target: int) -> List[int]:  # "hi" -> there';
    expect(tokenizeLine(line).map((t) => t.text).join("")).toBe(line);
  });

  it("keeps `->` as one operator token, so it cannot wrap in the middle", () => {
    const arrow = tokenizeLine("def f(x) -> int:").find((t) => t.text.includes(">"));
    expect(arrow).toEqual({ kind: "op", text: "->" });
  });

  it("colours keywords, names, builtins, self, numbers and strings", () => {
    expect(kinds("def helper(self):")).toEqual([
      ["kw", "def"],
      ["plain", " "],
      ["fn", "helper"],
      ["op", "("],
      ["self", "self"],
      ["op", "):"],
    ]);
    expect(kinds("x = len('a#b') + 10")).toEqual([
      ["plain", "x "],
      ["op", "="],
      ["plain", " "],
      ["builtin", "len"],
      ["op", "("],
      ["str", "'a#b'"],
      ["op", ")"],
      ["plain", " "],
      ["op", "+"],
      ["plain", " "],
      ["num", "10"],
    ]);
  });

  it("treats everything after # as a comment, but not a # inside a string", () => {
    expect(kinds('s = "#" # note').at(-1)).toEqual(["com", "# note"]);
  });
});
