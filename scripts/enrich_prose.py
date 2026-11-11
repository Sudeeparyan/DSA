#!/usr/bin/env python3
"""Replace stub plainProblem / thinkingSteps with teachable prose from existing fields."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "content" / "problems"

PLAIN_STUB = re.compile(r"Restate the official prompt", re.I)
THINK_STUB = re.compile(
    r"slow but correct approach \(often nested loops or rescanning\)", re.I
)
BETTER_STUB = re.compile(r"Write the optimal plan in 3 bullets", re.I)


def first_sentence(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return parts[0].strip()


def build_plain(problem: dict) -> str:
    title = problem["title"]
    kid = first_sentence(problem.get("kidExplanation", ""))
    ex = problem["examples"][0]
    pattern = problem.get("pattern", {}).get("name", "a known pattern")
    bits = [
        f"{title}: {kid}" if kid else f"Solve “{title}”.",
        f"Worked example — input: {ex['input']}; expected output: {ex['output']}.",
    ]
    if ex.get("explanation"):
        bits.append(f"Why: {ex['explanation']}")
    bits.append(f"Interview pattern to name out loud: {pattern}.")
    return " ".join(bits)


def build_thinking(problem: dict) -> list[dict]:
    title = problem["title"]
    pattern = problem.get("pattern", {}).get("name", "the right pattern")
    when = problem.get("pattern", {}).get("whenToSpot", "")
    aha = ""
    for step in problem.get("thinkingSteps", []):
        if step.get("title", "").lower().startswith("aha") and not THINK_STUB.search(
            step.get("body", "")
        ):
            aha = step["body"].strip()
            break
    if not aha:
        aha = first_sentence(problem.get("kidExplanation", "")) or (
            f"Spot {pattern}. {when}".strip()
        )

    ex = problem["examples"][0]
    complexity = problem.get("complexity", {})
    return [
        {
            "title": "Brute force idea",
            "body": (
                f"For “{title}”, first say a correct slow approach: scan or retry every "
                f"candidate until the example works by hand. Input {ex['input']} should "
                f"still produce {ex['output']}."
            ),
        },
        {
            "title": "Why it is slow",
            "body": (
                f"Count the nested work. If each choice restarts a full scan, time blows up. "
                f"Name the cost before optimizing — interviewers want that honesty. "
                f"Target after the insight: {complexity.get('time', 'better than brute force')}."
            ),
        },
        {
            "title": "Aha insight",
            "body": aha,
        },
        {
            "title": "Better idea",
            "body": (
                f"Commit to {pattern}. {when} "
                f"Walk example `{ex['input']}` → `{ex['output']}` while naming each variable, "
                f"then code. Close with {complexity.get('time', '?')} time and "
                f"{complexity.get('space', '?')} space."
            ).strip(),
        },
    ]


EDGE_STUB = re.compile(r"Empty or minimal input", re.I)
MISTAKE_STUB = re.compile(r"Coding before stating the pattern", re.I)
TIME_STUB = re.compile(r"We follow the loops in the solution", re.I)
SPACE_STUB = re.compile(r"Extra memory comes from sets", re.I)


def build_edges(problem: dict) -> list[str]:
    title = problem["title"]
    ex0 = problem["examples"][0]["input"]
    ex1 = problem["examples"][1]["input"] if len(problem["examples"]) > 1 else None
    edges = [
        f"Smallest legal input for “{title}” — confirm the base answer before the main loop.",
        f"Replay example `{ex0}` and check boundary indices / empty containers.",
    ]
    if ex1:
        edges.append(f"Second example `{ex1}` often hides duplicates, ties, or already-sorted cases.")
    else:
        edges.append("Duplicates, already-sorted input, and max/min constraint values.")
    return edges


def build_mistakes(problem: dict) -> list[str]:
    pattern = problem.get("pattern", {}).get("name", "the pattern")
    return [
        f"Jumping into code before naming {pattern} and the complexity target.",
        "Off-by-one errors on indices, windows, or inclusive/exclusive bounds.",
        "Mutating a set/map/list while iterating it, or forgetting the undo step in backtracking.",
    ]


def enrich_complexity(problem: dict) -> bool:
    changed = False
    c = problem.get("complexity") or {}
    if TIME_STUB.search(c.get("timeReason", "")):
        c["timeReason"] = (
            f"From the coded loops for “{problem['title']}”: {c.get('time', '?')} matches how many "
            f"elements / states each pass touches (say this out loud in the interview)."
        )
        changed = True
    if SPACE_STUB.search(c.get("spaceReason", "")):
        c["spaceReason"] = (
            f"Extra memory is {c.get('space', '?')} from the structures this solution allocates "
            f"(hash maps, stacks, DP rows, recursion depth) — not counting the input itself."
        )
        changed = True
    if changed:
        problem["complexity"] = c
    return changed


def enrich(problem: dict) -> bool:
    changed = False
    if PLAIN_STUB.search(problem.get("plainProblem", "")):
        problem["plainProblem"] = build_plain(problem)
        changed = True

    bodies = " ".join(t.get("body", "") for t in problem.get("thinkingSteps", []))
    if THINK_STUB.search(bodies) or BETTER_STUB.search(bodies):
        # Preserve a strong existing Aha if present; rebuild the stub scaffolding.
        problem["thinkingSteps"] = build_thinking(problem)
        changed = True

    if any(EDGE_STUB.search(e or "") for e in problem.get("edgeCases", [])):
        problem["edgeCases"] = build_edges(problem)
        changed = True
    if any(MISTAKE_STUB.search(e or "") for e in problem.get("commonMistakes", [])):
        problem["commonMistakes"] = build_mistakes(problem)
        changed = True
    if enrich_complexity(problem):
        changed = True
    return changed


def main():
    files = sorted(PROBLEMS.glob("*.json"))
    changed = 0
    for path in files:
        problem = json.loads(path.read_text())
        if enrich(problem):
            path.write_text(json.dumps(problem, indent=2) + "\n")
            changed += 1
            print("prose", problem["slug"])
    print(f"DONE prose_changed={changed}/{len(files)}")


if __name__ == "__main__":
    main()
