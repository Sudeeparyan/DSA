#!/usr/bin/env python3
"""Build the lesson JSON files that the web app plays.

    python lessons/build.py                 build every lesson that has a spec
    python lessons/build.py two-sum 3sum    build only these
    python lessons/build.py --strict        also fail if any of the 150 is missing

For each lesson this script:
  1. loads the real solution from ``solutions/`` (or the spec's own ``code=``),
  2. checks it returns the expected answer on the example and on extra tests,
  3. re-runs the example under the recorder to capture every teaching step,
  4. writes ``content/lessons/<slug>.json``.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import importlib
import json
import math
import pkgutil
import re
import struct
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lessons.engine import fmt, prelude  # noqa: E402
from lessons.engine.core import (  # noqa: E402
    HELPERS,
    SOLUTION_FILE,
    TONES,
    CodeInfo,
    LessonError,
    Recorder,
)
from lessons.engine.prelude import REG, normalize  # noqa: E402
from lessons.engine.spec import LESSONS, Lesson  # noqa: E402

OUT_DIR = ROOT / "content" / "lessons"
CATALOG = ROOT / "content" / "catalog.json"

PRELUDE_SRC = """
import collections, heapq, math, bisect, functools, itertools, string, random, operator, re
from typing import *
from collections import deque, defaultdict, Counter, OrderedDict
from heapq import heappush, heappop, heapify, heappushpop, heapreplace, nlargest, nsmallest
from functools import lru_cache, cache, reduce, cmp_to_key
from math import inf, gcd, ceil, floor, sqrt
from bisect import bisect_left, bisect_right, insort
"""


# --------------------------------------------------------------------------
# Solution source
# --------------------------------------------------------------------------


def clean_solution(src: str) -> str:
    """Strip the header docstring, alternative solutions kept in strings, and
    LeetCode boilerplate comments so only the real solution is shown."""
    src = src.replace("\r\n", "\n").replace("\t", "    ")
    tree = ast.parse(src)
    lines = src.split("\n")
    drop: set[int] = set()
    for node in tree.body:
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            drop.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    i = 0
    while i < len(lines):
        text = lines[i].strip()
        if text.startswith(("# Definition for", "# Your ", "# class ")):
            while i < len(lines) and lines[i].strip().startswith("#"):
                drop.add(i + 1)
                i += 1
        else:
            i += 1
    kept = [ln.rstrip() for n, ln in enumerate(lines, 1) if n not in drop]
    out: list[str] = []
    for ln in kept:
        if ln == "" and (not out or out[-1] == ""):
            continue
        out.append(ln)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def make_ns(lesson: Lesson, code_obj) -> dict:
    ns: dict = {"__name__": "solution", "__builtins__": builtins}
    exec(PRELUDE_SRC, ns)  # noqa: S102 - trusted
    for name in ("ListNode", "TreeNode", "RandomListNode", "GraphNode",
                 "L", "LR", "T", "G", "find", "list_vals", "tree_vals"):
        ns[name] = getattr(prelude, name)
    if lesson.pre:
        exec(lesson.pre, ns)  # noqa: S102 - trusted
    exec(code_obj, ns)  # noqa: S102 - trusted
    return ns


# --------------------------------------------------------------------------
# Comparing answers
# --------------------------------------------------------------------------


def _canon(value, depth: int):
    if depth <= 0 or not isinstance(value, list):
        return value
    items = [_canon(v, depth - 1) for v in value]
    return sorted(items, key=lambda v: json.dumps(v, sort_keys=True, default=str))


def _equal(a, b) -> bool:
    if isinstance(a, float) or isinstance(b, float):
        try:
            return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
        except TypeError:
            return False
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_equal(a[k], b[k]) for k in a)
    return a == b


def same(got, expected, unordered: int) -> bool:
    got, expected = normalize(got), normalize(expected)
    if got is None and expected == []:
        return True  # an empty linked list / tree is None
    if unordered:
        got, expected = _canon(got, unordered), _canon(expected, unordered)
    return _equal(got, expected)


# --------------------------------------------------------------------------
# Running a solution
# --------------------------------------------------------------------------


def entry_point(lesson: Lesson, info: CodeInfo) -> tuple[str, str]:
    cls = lesson.cls or ("Solution" if "Solution" in info.classes else info.classes[0])
    if lesson.method:
        return cls, lesson.method
    public = [m for m in info.methods[cls] if not m.startswith("_")]
    if not public:
        raise LessonError(f"class {cls} has no public method")
    return cls, public[0]


NEWLINE = chr(10)


def eval_args(args_src: str, ns: dict) -> dict:
    """Evaluate "a=..., b=..." left to right; later arguments may refer to earlier ones."""
    call = ast.parse(f"dict({args_src})", mode="eval").body
    args: dict = {}
    for kw in call.keywords:
        code = compile(ast.Expression(kw.value), "<args>", "eval")
        args[kw.arg] = eval(code, {**ns, **args})  # noqa: S307 - trusted lesson source
    return args


def input_text(args: dict) -> str:
    parts = [f"{k} = {fmt.pretty(v, len(k) + 3)}" for k, v in args.items()]
    if any(NEWLINE in part for part in parts):
        return NEWLINE.join(parts)
    return ", ".join(parts)


def run_function(lesson: Lesson, info: CodeInfo, code_obj, args_src: str, rec_factory=None):
    REG.reset()
    ns = make_ns(lesson, code_obj)
    cls, method = entry_point(lesson, info)
    args = eval_args(args_src, ns)
    shown = input_text(args)
    obj = ns[cls]()
    fn = getattr(obj, method)
    rec = None
    if rec_factory is not None:
        lesson.input_text = lesson.show_input or shown
        rec = rec_factory(ns)
        rec.start()
    try:
        ret = fn(**args)
    finally:
        Recorder.stop()
    final = ret
    if lesson.result:
        final = eval(lesson.result, {**ns, **HELPERS, **args, "_ret": ret})  # noqa: S307
    return shown, final, rec


_OUT_REF = re.compile(r"_out\[(\d+)\]")
_BUILDER = re.compile(r"\b(?:T|L)\((\[[^()]*\])\)")


def run_design(lesson: Lesson, code_obj, ops: list[str], rec_factory=None):
    REG.reset()
    ns = make_ns(lesson, code_obj)
    outputs: list = []
    raw: list = []
    labels = []
    rec = None
    if rec_factory is not None:
        rec = rec_factory(ns)
        rec.ops = [{"call": op, "state": "todo"} for op in ops]
        rec.start()
    obj = None
    try:
        for i, op in enumerate(ops):
            label = _OUT_REF.sub(lambda m: fmt.show(raw[int(m.group(1))], 30), op)
            label = _BUILDER.sub(r"\1", label)  # show T([1, 2]) as [1, 2]
            labels.append(label)
            if rec is not None:
                rec.ops[i]["call"] = label
                rec.begin_op(label, obj)
            env = {**ns, "_out": raw}
            if i == 0:
                obj = eval(op, env)  # noqa: S307 - trusted
                out = None
            else:
                env["_obj"] = obj
                out = eval("_obj." + op, env)  # noqa: S307 - trusted
            raw.append(out)
            outputs.append(normalize(out))
            if rec is not None:
                rec.end_op(obj, out)
        if rec is not None:
            rec.finish_design(obj, outputs)
    finally:
        Recorder.stop()
    lines = [
        label if out is None else f"{label}  →  {fmt.leet(out)}"
        for label, out in zip(labels, outputs)
    ]
    return NEWLINE.join(lines), outputs, rec


# --------------------------------------------------------------------------
# Text that is drawn inside the 3D stage
# --------------------------------------------------------------------------

FONT_FILE = ROOT / "public" / "fonts" / "IBMPlexMono-SemiBold.ttf"

# characters the stage font cannot draw -> a close replacement it can
GLYPH_FIX = {
    "∅": "ø",  # empty set -> o-slash
    "␣": "·",  # open box -> middle dot
    "“": '"', "”": '"', "‘": "'", "’": "'",
    "—": "-", "–": "-", "`": "",
}
STAGE_TEXT_KEYS = {"v", "k", "label", "title", "name", "badge"}


def font_codepoints(path: Path) -> set[int]:
    """Code points covered by a TrueType font (reads the cmap table)."""
    data = path.read_bytes()
    count = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(count):
        tag, _, offset, _ = struct.unpack(">4sIII", data[12 + 16 * i : 28 + 16 * i])
        tables[tag.decode()] = offset
    base = tables["cmap"]
    points: set[int] = set()
    for i in range(struct.unpack(">H", data[base + 2 : base + 4])[0]):
        _, _, sub = struct.unpack(">HHI", data[base + 4 + 8 * i : base + 12 + 8 * i])
        at = base + sub
        kind = struct.unpack(">H", data[at : at + 2])[0]
        if kind == 4:
            seg2 = struct.unpack(">H", data[at + 6 : at + 8])[0]
            seg = seg2 // 2
            ends = struct.unpack(f">{seg}H", data[at + 14 : at + 14 + seg2])
            starts = struct.unpack(f">{seg}H", data[at + 16 + seg2 : at + 16 + 2 * seg2])
            for a, b in zip(starts, ends):
                points.update(range(a, b + 1))
        elif kind == 12:
            groups = struct.unpack(">I", data[at + 12 : at + 16])[0]
            for g in range(groups):
                a, b, _ = struct.unpack(">III", data[at + 16 + 12 * g : at + 28 + 12 * g])
                points.update(range(a, b + 1))
    return points


_FONT: set[int] | None = None


def stage_text(text: str, slug: str) -> str:
    """Make a string safe for the stage font (it has no fallback glyphs)."""
    global _FONT
    if _FONT is None:
        _FONT = font_codepoints(FONT_FILE)
    out = "".join(GLYPH_FIX.get(ch, ch) for ch in text)
    bad = sorted({ch for ch in out if ord(ch) not in _FONT})
    if bad:
        raise LessonError(f"stage text {text!r} uses characters the 3D font lacks: {bad}")
    return out


def clean_stage_text(node, slug: str):
    """Walk one scene view and fix / verify every string that will be drawn in 3D."""
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str) and key in STAGE_TEXT_KEYS:
                node[key] = stage_text(value, slug)
            elif key in ("rows", "cols") and isinstance(value, list) and all(isinstance(x, str) for x in value):
                node[key] = [stage_text(x, slug) for x in value]
            else:
                clean_stage_text(value, slug)
    elif isinstance(node, list):
        for item in node:
            clean_stage_text(item, slug)


# --------------------------------------------------------------------------
# Building one lesson
# --------------------------------------------------------------------------


def _check_step(slug: str, index: int, step: dict) -> None:
    if not step["text"]:
        raise LessonError(f"{slug}: step {index} has no caption")
    for view in step["views"]:
        stack = [view]
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                tone = item.get("tone")
                if tone is not None and tone not in TONES and not str(tone).startswith("#"):
                    raise LessonError(f"{slug}: step {index} has unknown tone {tone!r}")
                stack.extend(item.values())
            elif isinstance(item, list):
                stack.extend(item)


def build_lesson(lesson: Lesson, entry: dict) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    if lesson.code:
        code = lesson.code
    else:
        code = clean_solution((ROOT / entry["pythonPath"]).read_text(encoding="utf8"))
    info = CodeInfo(code)
    code_obj = compile(code, SOLUTION_FILE, "exec")

    # 1. the solution must be right on the extra tests (no recording)
    more = []
    for test in lesson.tests:
        src, expected = test[0], test[1]
        if lesson.is_design:
            shown, got, _ = run_design(lesson, code_obj, src)
        else:
            shown, got, _ = run_function(lesson, info, code_obj, src)
        if not same(got, expected, lesson.unordered):
            raise LessonError(
                f"test {src!r}: expected {fmt.leet(normalize(expected))}, got {fmt.leet(normalize(got))}"
            )
        more.append({"input": shown, "output": "" if lesson.is_design else fmt.leet(normalize(expected))})

    # 2. record the worked example
    def factory(ns):
        return Recorder(lesson, info, ns, lesson.max_steps)

    if lesson.is_design:
        shown, got, rec = run_design(lesson, code_obj, lesson.ops, factory)
    else:
        shown, got, rec = run_function(lesson, info, code_obj, lesson.args, factory)
    if not same(got, lesson.expected, lesson.unordered):
        raise LessonError(
            f"example: expected {fmt.leet(normalize(lesson.expected))}, got {fmt.leet(normalize(got))}"
        )

    steps = rec.steps
    if len(steps) < 5:
        raise LessonError(f"only {len(steps)} steps - add notes")
    unused = rec.unused_notes()
    if unused and not lesson.allow_unused:
        raise LessonError(f"notes never fired on the example: {unused}")

    by_view: dict[str, list[dict]] = {}
    for step in steps:
        for view in step["views"]:
            by_view.setdefault(view["id"], []).append(view)
    for view in lesson.views:
        if view.id in by_view:
            view.finalize(by_view[view.id])
        else:
            warnings.append(f"view {view.id!r} never appeared")
    for i, step in enumerate(steps):
        _check_step(lesson.slug, i, step)
        for view in step["views"]:
            if view["t"] not in ("vars", "ops"):
                clean_stage_text(view, lesson.slug)
        if len(step["text"]) > 330:
            warnings.append(f"step {i} caption is long ({len(step['text'])} chars)")
        if step["line"] > len(info.lines):
            raise LessonError(f"step {i} points at line {step['line']} beyond the code")
    for a, b in zip(steps, steps[1:]):
        if a["text"] == b["text"] and a["views"] == b["views"]:
            warnings.append(f"duplicate consecutive step: {a['text'][:50]!r}")

    doc = {
        "id": entry["id"],
        "number": entry["leetcodeNumber"],
        "title": entry["title"],
        "slug": lesson.slug,
        "category": entry["category"],
        "difficulty": entry["difficulty"],
        "url": entry["leetcodeUrl"],
        "pattern": lesson.pattern or "",
        "statement": lesson.statement,
        "example": {
            "input": lesson.show_input or shown,
            # a design lesson lists its calls with their results, so it has no single output
            "output": "" if lesson.is_design else (lesson.show_output or fmt.leet(normalize(lesson.expected))),
            "why": lesson.why,
        },
        "more": more,
        "idea": lesson.idea,
        "code": code,
        "complexity": {
            "time": lesson.time[0],
            "timeWhy": lesson.time[1],
            "space": lesson.space[0],
            "spaceWhy": lesson.space[1],
        },
        "steps": steps,
    }
    return doc, warnings


def dump(doc: dict) -> str:
    head = {k: v for k, v in doc.items() if k != "steps"}
    text = json.dumps(head, ensure_ascii=False, indent=1)
    steps = ",\n".join(
        "  " + json.dumps(s, ensure_ascii=False, separators=(",", ":")) for s in doc["steps"]
    )
    return text[:-2] + ',\n "steps": [\n' + steps + "\n ]\n}\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def load_specs() -> None:
    import lessons.specs as specs

    for mod in sorted(pkgutil.iter_modules(specs.__path__), key=lambda m: m.name):
        importlib.import_module(f"lessons.specs.{mod.name}")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("slugs", nargs="*", help="only build these lessons")
    parser.add_argument("--strict", action="store_true", help="fail if any catalog problem has no lesson")
    parser.add_argument("--quiet", action="store_true")
    opts = parser.parse_args()

    catalog = json.loads(CATALOG.read_text(encoding="utf8"))
    entries = {p["slug"]: p for p in catalog["problems"]}
    load_specs()

    unknown = [s for s in LESSONS if s not in entries]
    if unknown:
        print(f"lessons for unknown slugs: {unknown}")
        return 1
    wanted = opts.slugs or [p["slug"] for p in catalog["problems"] if p["slug"] in LESSONS]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    failed = 0
    total_bytes = 0
    for slug in wanted:
        if slug not in LESSONS:
            print(f"FAIL {slug}: no lesson spec")
            failed += 1
            continue
        try:
            doc, warnings = build_lesson(LESSONS[slug], entries[slug])
        except LessonError as exc:
            print(f"FAIL {slug}: {exc}")
            failed += 1
            continue
        except Exception:  # a bug in a spec or in the solution itself
            print(f"FAIL {slug}: crashed\n{traceback.format_exc()}")
            failed += 1
            continue
        text = dump(doc)
        (OUT_DIR / f"{slug}.json").write_text(text, encoding="utf8", newline="\n")
        total_bytes += len(text.encode("utf8"))
        if not opts.quiet:
            print(f"ok   {slug:58s} {len(doc['steps']):3d} steps {len(text) // 1024:4d} KB")
        for w in warnings:
            print(f"     warning {slug}: {w}")

    missing = [p["slug"] for p in catalog["problems"] if p["slug"] not in LESSONS]
    built = len(wanted) - failed
    print(f"\nbuilt {built}/{len(wanted)} lessons, {total_bytes // 1024} KB total; "
          f"{len(LESSONS)}/{len(entries)} problems have a lesson")
    if missing and (opts.strict or not opts.quiet):
        print(f"missing ({len(missing)}): {', '.join(missing[:12])}{' ...' if len(missing) > 12 else ''}")
    if failed or (opts.strict and missing):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
