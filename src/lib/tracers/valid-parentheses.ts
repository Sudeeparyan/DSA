import type { TraceStep } from "./types";

export function traceValidParentheses(input: unknown): TraceStep[] {
  const s = input as string;
  const steps: TraceStep[] = [];
  const stack: string[] = [];
  const map: Record<string, string> = { ")": "(", "}": "{", "]": "[" };
  const chars = s.split("");

  steps.push({
    line: 2,
    caption: "Start with an empty stack (a pile). Opening brackets go on the pile.",
    state: {
      chars,
      stack: [],
      currentIndex: null,
      result: null,
      highlights: {},
    },
  });

  for (let i = 0; i < chars.length; i++) {
    const char = chars[i];
    const opens = Object.values(map);

    steps.push({
      line: 5,
      caption: `Look at character '${char}' at index ${i}.`,
      state: {
        chars,
        stack: [...stack],
        currentIndex: i,
        currentValue: char,
        result: null,
        highlights: { [i]: "current" },
      },
    });

    if (opens.includes(char)) {
      stack.push(char);
      steps.push({
        line: 7,
        caption: `'${char}' is an opening bracket. Push it onto the stack.`,
        state: {
          chars,
          stack: [...stack],
          currentIndex: i,
          currentValue: char,
          result: null,
          highlights: { [i]: "remembered" },
        },
      });
    } else if (char in map) {
      const expected = map[char];
      if (!stack.length || stack[stack.length - 1] !== expected) {
        steps.push({
          line: 9,
          caption: `'${char}' wants to close '${expected}', but the top of the stack does not match (or the stack is empty). Invalid!`,
          state: {
            chars,
            stack: [...stack],
            currentIndex: i,
            currentValue: char,
            result: false,
            highlights: { [i]: "rejected" },
          },
        });
        steps.push({
          line: 10,
          caption: "Return False.",
          state: {
            chars,
            stack: [...stack],
            currentIndex: i,
            result: false,
            highlights: { [i]: "rejected" },
          },
        });
        return steps;
      }
      stack.pop();
      steps.push({
        line: 11,
        caption: `'${char}' matches the top '${expected}'. Pop it off — they hug and leave.`,
        state: {
          chars,
          stack: [...stack],
          currentIndex: i,
          currentValue: char,
          result: null,
          highlights: { [i]: "matched" },
        },
      });
    } else {
      steps.push({
        line: 13,
        caption: `'${char}' is not a bracket we know. Invalid.`,
        state: {
          chars,
          stack: [...stack],
          currentIndex: i,
          result: false,
          highlights: { [i]: "rejected" },
        },
      });
      return steps;
    }
  }

  const ok = stack.length === 0;
  steps.push({
    line: 15,
    caption: ok
      ? "Stack is empty — every opener found a closer. Return True."
      : "Stack still has openers waiting. Return False.",
    state: {
      chars,
      stack: [...stack],
      currentIndex: null,
      result: ok,
      highlights: Object.fromEntries(
        chars.map((_, i) => [i, ok ? "done" : "rejected"]),
      ),
    },
  });

  return steps;
}
