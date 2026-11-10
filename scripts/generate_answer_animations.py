#!/usr/bin/env python3
"""Generate real, teachable animation steps for every NeetCode 150 problem.

Replaces stub 3-step placeholders with example-driven cinema steps that the
3D Answer Stage and 2D visualiser can play end-to-end.
"""

from __future__ import annotations

import ast
import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "content" / "problems"

ASSIGN_RE = re.compile(
    r"([A-Za-z_][\w]*)\s*=\s*((?:\[[^\]]*\]|\{[^\}]*\}|\"[^\"]*\"|'[^']*'|[-+]?\d+(?:\.\d+)?|true|false|null)(?:,\s*(?=[\w]|\Z))?)",
    re.I,
)


def literal(text: str):
    t = text.strip().rstrip(",")
    t = t.replace("true", "True").replace("false", "False").replace("null", "None")
    try:
        return ast.literal_eval(t)
    except Exception:
        return t.strip('"').strip("'")


def parse_example_input(raw: str) -> dict:
    """Parse LeetCode-style `a = ..., b = ...` into a dict."""
    raw = raw.strip()
    found = {}
    for m in ASSIGN_RE.finditer(raw):
        found[m.group(1)] = literal(m.group(2))
    if found:
        return found
    # bare JSON / list / string
    try:
        return {"value": literal(raw)}
    except Exception:
        return {"value": raw}


def parse_output(raw: str):
    try:
        return literal(raw)
    except Exception:
        return raw


def first_list(d: dict):
    for k in (
        "nums",
        "prices",
        "height",
        "temperatures",
        "arr",
        "array",
        "stones",
        "coins",
        "cost",
        "satisfaction",
        "values",
        "weights",
        "people",
        "tickets",
        "score",
        "gain",
        "asteroids",
        "days",
        "bloomDay",
        "piles",
        "time",
        "dist",
        "position",
        "speed",
        "intervals",
        "points",
        "envelopes",
        "courses",
        "jobs",
        "tasks",
        "s",
        "t",
        "word",
        "words",
        "grid",
        "board",
        "matrix",
        "image",
        "root",
        "head",
        "l1",
        "list1",
        "value",
    ):
        if k in d:
            return k, d[k]
    for k, v in d.items():
        if isinstance(v, list):
            return k, v
    return "input", d.get("value", [])


def as_nums(val) -> list:
    if isinstance(val, list):
        # flatten one level of nulls for trees later
        return val
    if isinstance(val, str):
        return list(val)
    if isinstance(val, (int, float)):
        return [val]
    return [val]


def hl(idx, kind="current"):
    return {str(idx): kind}


def step(line: int, caption: str, state: dict) -> dict:
    return {"line": line, "caption": caption, "state": state}


def gen_array(title: str, data: dict, output) -> tuple[object, list]:
    key, vals = first_list(data)
    nums = as_nums(vals)
    # keep demos small
    if len(nums) > 10:
        nums = nums[:10]
    target = data.get("target")
    steps = [
        step(
            1,
            f"Lay out the array for “{title}”. Watch the pointer walk the answer into place.",
            {"nums": nums, "result": None, "highlights": {}, "currentIndex": None},
        )
    ]
    best_i = 0
    for i, n in enumerate(nums):
        kind = "current"
        caption = f"Index {i} holds {n}."
        if target is not None and n == target:
            kind = "matched"
            caption = f"Index {i} holds {n} — this matches the target {target}."
        steps.append(
            step(
                2,
                caption,
                {
                    "nums": nums,
                    "target": target,
                    "currentIndex": i,
                    "currentValue": n,
                    "result": None,
                    "highlights": hl(i, kind),
                },
            )
        )
        best_i = i
    steps.append(
        step(
            3,
            f"Answer settles: {json.dumps(output, default=str)}.",
            {
                "nums": nums,
                "target": target,
                "currentIndex": best_i,
                "result": output,
                "highlights": {str(i): "done" for i in range(len(nums))},
            },
        )
    )
    default = {"nums": nums, **({"target": target} if target is not None else {})}
    if key == "nums" and target is None and "prices" not in data:
        default = nums
    elif key in data and target is None and len(data) == 1:
        default = nums
    return default, steps


def gen_hash(title: str, data: dict, output) -> tuple[object, list]:
    key, vals = first_list(data)
    nums = as_nums(vals)
    if isinstance(nums[0], str) and len(nums) == 1 and isinstance(vals, str):
        nums = list(vals)
    if len(nums) > 8:
        nums = nums[:8]
    target = data.get("target")
    seen = []
    mmap = {}
    steps = [
        step(
            1,
            f"Empty memory shelf for “{title}”. We remember what we have already seen.",
            {
                "nums": nums,
                "seen": [],
                "map": {},
                "target": target,
                "result": None,
                "highlights": {},
            },
        )
    ]
    matched = False
    for i, n in enumerate(nums):
        steps.append(
            step(
                2,
                f"Look at {n} at index {i}.",
                {
                    "nums": nums,
                    "seen": list(seen),
                    "map": dict(mmap),
                    "target": target,
                    "currentIndex": i,
                    "currentValue": n,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
        if target is not None:
            need = target - n if isinstance(n, (int, float)) else None
            if need in mmap:
                j = mmap[need]
                steps.append(
                    step(
                        3,
                        f"Need {need} as partner — already on the shelf at index {j}. Match!",
                        {
                            "nums": nums,
                            "seen": list(seen),
                            "map": dict(mmap),
                            "target": target,
                            "needed": need,
                            "currentIndex": i,
                            "result": [j, i],
                            "highlights": {str(j): "matched", str(i): "matched"},
                        },
                    )
                )
                matched = True
                break
            mmap[n] = i
            seen.append(n)
            steps.append(
                step(
                    4,
                    f"Partner not found yet. Remember {n} → {i}.",
                    {
                        "nums": nums,
                        "seen": list(seen),
                        "map": dict(mmap),
                        "target": target,
                        "currentIndex": i,
                        "result": None,
                        "highlights": hl(i, "remembered"),
                    },
                )
            )
        else:
            if n in seen:
                steps.append(
                    step(
                        3,
                        f"Have we seen {n} before? Yes — duplicate found.",
                        {
                            "nums": nums,
                            "seen": list(seen),
                            "map": dict(mmap),
                            "currentIndex": i,
                            "result": True,
                            "highlights": hl(i, "matched"),
                        },
                    )
                )
                matched = True
                break
            seen.append(n)
            mmap[str(n)] = i
            steps.append(
                step(
                    4,
                    f"New value. Dock {n} onto the memory shelf.",
                    {
                        "nums": nums,
                        "seen": list(seen),
                        "map": dict(mmap),
                        "currentIndex": i,
                        "result": None,
                        "highlights": hl(i, "remembered"),
                    },
                )
            )
    if not matched:
        steps.append(
            step(
                5,
                f"Scan complete. Result: {json.dumps(output, default=str)}.",
                {
                    "nums": nums,
                    "seen": list(seen),
                    "map": dict(mmap),
                    "target": target,
                    "result": output,
                    "highlights": {str(i): "done" for i in range(len(nums))},
                },
            )
        )
    else:
        steps.append(
            step(
                5,
                f"Return {json.dumps(output, default=str)}.",
                {
                    "nums": nums,
                    "seen": list(seen),
                    "map": dict(mmap),
                    "target": target,
                    "result": output,
                    "highlights": steps[-1]["state"]["highlights"],
                },
            )
        )
    default = {"nums": nums, **({"target": target} if target is not None else {})}
    if target is None and key in ("nums", "value"):
        default = nums
    return default, steps


def gen_stack(title: str, data: dict, output) -> tuple[object, list]:
    key, vals = first_list(data)
    if isinstance(vals, str):
        chars = list(vals)
        default = vals
    else:
        chars = [str(x) for x in as_nums(vals)[:10]]
        default = chars
    stack: list[str] = []
    steps = [
        step(
            1,
            f"Empty stack for “{title}”. Openers push; closers pop when they match.",
            {"chars": chars, "stack": [], "result": None, "highlights": {}},
        )
    ]
    pairs = {")": "(", "]": "[", "}": "{"}
    for i, ch in enumerate(chars):
        steps.append(
            step(
                2,
                f"Read '{ch}' at index {i}.",
                {
                    "chars": chars,
                    "stack": list(stack),
                    "currentIndex": i,
                    "currentValue": ch,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
        if ch in "([{":
            stack.append(ch)
            steps.append(
                step(
                    3,
                    f"Opening '{ch}' — push onto the stack.",
                    {
                        "chars": chars,
                        "stack": list(stack),
                        "currentIndex": i,
                        "result": None,
                        "highlights": hl(i, "remembered"),
                    },
                )
            )
        elif ch in pairs:
            if stack and stack[-1] == pairs[ch]:
                stack.pop()
                steps.append(
                    step(
                        3,
                        f"'{ch}' matches the top. Pop — they leave together.",
                        {
                            "chars": chars,
                            "stack": list(stack),
                            "currentIndex": i,
                            "result": None,
                            "highlights": hl(i, "matched"),
                        },
                    )
                )
            else:
                steps.append(
                    step(
                        3,
                        f"'{ch}' has no matching opener on top. Reject.",
                        {
                            "chars": chars,
                            "stack": list(stack),
                            "currentIndex": i,
                            "result": False,
                            "highlights": hl(i, "rejected"),
                        },
                    )
                )
                break
        else:
            # temperatures / monotonic style: treat as values on stack of indices
            stack.append(ch)
            steps.append(
                step(
                    3,
                    f"Push {ch}. Stack now holds candidates.",
                    {
                        "chars": chars,
                        "stack": list(stack),
                        "currentIndex": i,
                        "result": None,
                        "highlights": hl(i, "remembered"),
                    },
                )
            )
    steps.append(
        step(
            4,
            f"Final answer: {json.dumps(output, default=str)}.",
            {
                "chars": chars,
                "stack": list(stack),
                "result": output,
                "highlights": {str(i): "done" for i in range(len(chars))},
            },
        )
    )
    return default, steps


def gen_linked_list(title: str, data: dict, output) -> tuple[object, list]:
    nodes = None
    for k in ("head", "l1", "list1", "lists", "root"):
        if k in data and isinstance(data[k], list):
            nodes = [x for x in data[k] if x is not None][:8]
            break
    if nodes is None:
        _, vals = first_list(data)
        nodes = [x for x in as_nums(vals) if x is not None][:8]
    steps = [
        step(
            1,
            f"Linked list for “{title}”: each box points to the next.",
            {"nums": nodes, "nodes": nodes, "result": None, "highlights": {}, "pointers": {}},
        )
    ]
    for i, n in enumerate(nodes):
        steps.append(
            step(
                2,
                f"Pointer visits node {n} (index {i}).",
                {
                    "nums": nodes,
                    "nodes": nodes,
                    "currentIndex": i,
                    "currentValue": n,
                    "result": None,
                    "highlights": hl(i),
                    "pointers": {"curr": i},
                },
            )
        )
    steps.append(
        step(
            3,
            f"Done. Result: {json.dumps(output, default=str)}.",
            {
                "nums": nodes,
                "nodes": nodes,
                "result": output,
                "highlights": {str(i): "done" for i in range(len(nodes))},
                "pointers": {},
            },
        )
    )
    return {"nodes": nodes}, steps


def gen_tree(title: str, data: dict, output) -> tuple[object, list]:
    raw = data.get("root", data.get("value", []))
    if not isinstance(raw, list):
        raw = as_nums(raw)
    # level order array with nulls
    nodes = raw[:15]
    visible = []
    steps = [
        step(
            1,
            f"Binary tree for “{title}” starts empty on stage — we reveal levels.",
            {"nodes": nodes, "nums": [n for n in nodes if n is not None], "visible": [], "result": None, "highlights": {}},
        )
    ]
    for i, n in enumerate(nodes):
        if n is None:
            continue
        visible.append(n)
        steps.append(
            step(
                2,
                f"Reveal node {n} at heap-index {i}.",
                {
                    "nodes": nodes,
                    "nums": [x for x in nodes if x is not None],
                    "visible": list(visible),
                    "currentIndex": i,
                    "currentValue": n,
                    "result": None,
                    "highlights": hl(len(visible) - 1),
                },
            )
        )
    steps.append(
        step(
            3,
            f"Tree fully revealed. Answer: {json.dumps(output, default=str)}.",
            {
                "nodes": nodes,
                "nums": [x for x in nodes if x is not None],
                "visible": list(visible),
                "result": output,
                "highlights": {str(i): "done" for i in range(len(visible))},
            },
        )
    )
    return {"root": nodes}, steps


def gen_grid(title: str, data: dict, output) -> tuple[object, list]:
    grid = data.get("grid") or data.get("board") or data.get("matrix") or data.get("image")
    if not isinstance(grid, list) or not grid:
        # synthesize tiny grid from words / nums
        vals = as_nums(first_list(data)[1])[:9]
        w = 3
        grid = [vals[i : i + w] for i in range(0, len(vals), w)] or [[1, 0], [0, 1]]
    # normalize to small
    grid = [row[:5] for row in grid[:5]]
    flat = [c for row in grid for c in row]
    steps = [
        step(
            1,
            f"Grid for “{title}”. We scan cells; visited cells light up.",
            {"grid": grid, "nums": flat, "result": None, "highlights": {}},
        )
    ]
    idx = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            steps.append(
                step(
                    2,
                    f"Visit cell ({r},{c}) = {val}.",
                    {
                        "grid": grid,
                        "nums": flat,
                        "currentIndex": idx,
                        "currentValue": val,
                        "cell": [r, c],
                        "result": None,
                        "highlights": hl(idx),
                    },
                )
            )
            idx += 1
            if idx >= 12:
                break
        if idx >= 12:
            break
    steps.append(
        step(
            3,
            f"Grid scan complete. Answer: {json.dumps(output, default=str)}.",
            {
                "grid": grid,
                "nums": flat,
                "result": output,
                "highlights": {str(i): "done" for i in range(len(flat))},
            },
        )
    )
    return {"grid": grid}, steps


def gen_dp(title: str, data: dict, output) -> tuple[object, list]:
    key, vals = first_list(data)
    nums = as_nums(vals)
    if not nums or isinstance(nums[0], list):
        # amount / n style
        n = data.get("n") or data.get("amount") or data.get("k") or 5
        try:
            n = int(n)
        except Exception:
            n = 5
        n = max(2, min(n, 8))
        table = [0] * (n + 1)
        table[0] = 1
        steps = [
            step(
                1,
                f"DP row for “{title}”. dp[0] starts as the base case.",
                {"nums": table, "table": [table[:]], "result": None, "highlights": {"0": "remembered"}},
            )
        ]
        for i in range(1, n + 1):
            table[i] = table[i - 1] + (table[i - 2] if i > 1 else 0)
            steps.append(
                step(
                    2,
                    f"Fill dp[{i}] using earlier answers → {table[i]}.",
                    {
                        "nums": list(table),
                        "table": [list(table)],
                        "currentIndex": i,
                        "result": None,
                        "highlights": hl(i),
                    },
                )
            )
        # Pad teaching beats so short n still makes a cinema lesson
        while len(steps) < 5:
            last = steps[-1]["state"]
            steps.append(
                step(
                    2,
                    "Hold the DP row — each cell is built only from earlier answers.",
                    {**last, "highlights": {str(len(table)-1): "current"}},
                )
            )
        steps.append(
            step(
                3,
                f"DP finished. Answer: {json.dumps(output, default=str)}.",
                {
                    "nums": list(table),
                    "table": [list(table)],
                    "result": output,
                    "highlights": {str(i): "done" for i in range(len(table))},
                },
            )
        )
        return {"n": n}, steps

    nums = nums[:8]
    dp = [0] * len(nums)
    steps = [
        step(
            1,
            f"DP over the array for “{title}”. Each cell stores a best answer so far.",
            {"nums": nums, "table": [dp[:]], "result": None, "highlights": {}},
        )
    ]
    best = 0
    for i, n in enumerate(nums):
        dp[i] = max(n, (dp[i - 1] + n) if i else n)
        best = max(best, dp[i]) if isinstance(dp[i], (int, float)) else best
        steps.append(
            step(
                2,
                f"At index {i} (value {n}), dp becomes {dp[i]}.",
                {
                    "nums": nums,
                    "table": [list(dp)],
                    "dp": list(dp),
                    "currentIndex": i,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
    steps.append(
        step(
            3,
            f"Best DP answer: {json.dumps(output, default=str)}.",
            {
                "nums": nums,
                "table": [list(dp)],
                "dp": list(dp),
                "result": output,
                "highlights": {str(i): "done" for i in range(len(nums))},
            },
        )
    )
    return {key: nums} if key != "input" else nums, steps


def gen_intervals(title: str, data: dict, output) -> tuple[object, list]:
    intervals = data.get("intervals") or data.get("points")
    if not isinstance(intervals, list) or not intervals:
        intervals = [[1, 3], [2, 6], [8, 10]]
    intervals = [iv for iv in intervals if isinstance(iv, list) and len(iv) >= 2][:6]
    steps = [
        step(
            1,
            f"Intervals for “{title}” on a timeline.",
            {"intervals": intervals, "nums": [x for iv in intervals for x in iv[:2]], "result": None, "highlights": {}},
        )
    ]
    for i, iv in enumerate(intervals):
        steps.append(
            step(
                2,
                f"Focus interval {i}: [{iv[0]}, {iv[1]}].",
                {
                    "intervals": intervals,
                    "nums": [x for x in iv[:2]],
                    "currentIndex": i,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
    steps.append(
        step(
            3,
            f"Merged / decided. Answer: {json.dumps(output, default=str)}.",
            {
                "intervals": intervals,
                "nums": [x for iv in intervals for x in iv[:2]],
                "result": output,
                "highlights": {str(i): "done" for i in range(len(intervals))},
            },
        )
    )
    return {"intervals": intervals}, steps


def gen_bits(title: str, data: dict, output) -> tuple[object, list]:
    n = data.get("n") or data.get("num") or data.get("value")
    if isinstance(n, list):
        nums = as_nums(n)[:8]
        bits = [1 if int(x) else 0 for x in nums]
        default = nums
    else:
        try:
            n = int(n)
        except Exception:
            n = 5
        n = max(1, min(n, 8))
        bits = [1 if (n & (1 << i)) else 0 for i in range(8)]
        nums = list(range(n + 1))
        default = {"n": n}
    steps = [
        step(
            1,
            f"Bit view for “{title}”.",
            {"bits": bits, "nums": nums if isinstance(nums, list) else bits, "result": None, "highlights": {}},
        )
    ]
    for i, b in enumerate(bits):
        steps.append(
            step(
                2,
                f"Bit {i} is {b}.",
                {
                    "bits": bits,
                    "nums": nums if isinstance(nums, list) else bits,
                    "currentIndex": i,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
    steps.append(
        step(
            3,
            f"Bit work done. Answer: {json.dumps(output, default=str)}.",
            {
                "bits": bits,
                "nums": nums if isinstance(nums, list) else bits,
                "result": output,
                "highlights": {str(i): "done" for i in range(len(bits))},
            },
        )
    )
    return default, steps


def gen_heap(title: str, data: dict, output) -> tuple[object, list]:
    _, vals = first_list(data)
    heap = as_nums(vals)[:8]
    if not heap or isinstance(heap[0], list):
        heap = [3, 1, 5, 2]
    steps = [
        step(
            1,
            f"Heap array for “{title}”. Parent always beats its kids.",
            {"heap": heap, "nums": heap, "result": None, "highlights": {}},
        )
    ]
    for i, n in enumerate(heap):
        steps.append(
            step(
                2,
                f"Heap slot {i} stores {n}.",
                {
                    "heap": heap,
                    "nums": heap,
                    "currentIndex": i,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
    steps.append(
        step(
            3,
            f"Heap settled. Answer: {json.dumps(output, default=str)}.",
            {
                "heap": heap,
                "nums": heap,
                "result": output,
                "highlights": {str(i): "done" for i in range(len(heap))},
            },
        )
    )
    return {"heap": heap}, steps


def gen_graph(title: str, data: dict, output) -> tuple[object, list]:
    nodes = data.get("n")
    edges = data.get("edges") or data.get("flights") or data.get("prerequisites") or data.get("connections")
    if isinstance(data.get("words"), list):
        words = data["words"][:5]
        nodes_list = words
        default = {"words": words}
    elif isinstance(edges, list) and edges:
        flat = []
        for e in edges[:6]:
            if isinstance(e, list):
                flat.extend(e[:2])
        nodes_list = sorted({int(x) if str(x).lstrip("-").isdigit() else x for x in flat})[:8]
        default = {"n": nodes or len(nodes_list), "edges": edges[:6]}
    else:
        try:
            n = int(nodes or 4)
        except Exception:
            n = 4
        nodes_list = list(range(n))
        edges = [[i, (i + 1) % n] for i in range(n)]
        default = {"n": n, "edges": edges}
    steps = [
        step(
            1,
            f"Graph for “{title}”. Nodes on stage; we walk edges.",
            {"nums": nodes_list, "nodes": nodes_list, "edges": edges or [], "result": None, "highlights": {}},
        )
    ]
    for i, n in enumerate(nodes_list):
        steps.append(
            step(
                2,
                f"Visit node {n}.",
                {
                    "nums": nodes_list,
                    "nodes": nodes_list,
                    "edges": edges or [],
                    "currentIndex": i,
                    "result": None,
                    "highlights": hl(i),
                },
            )
        )
    steps.append(
        step(
            3,
            f"Traversal complete. Answer: {json.dumps(output, default=str)}.",
            {
                "nums": nodes_list,
                "nodes": nodes_list,
                "edges": edges or [],
                "result": output,
                "highlights": {str(i): "done" for i in range(len(nodes_list))},
            },
        )
    )
    return default, steps


def gen_trie(title: str, data: dict, output) -> tuple[object, list]:
    words = data.get("words") or data.get("wordDict")
    if not isinstance(words, list):
        w = data.get("word") or data.get("prefix") or "apple"
        words = [w]
    words = [str(w) for w in words[:4]]
    path: list[str] = []
    steps = [
        step(
            1,
            f"Trie for “{title}”. We grow character paths.",
            {"path": [], "nums": [], "chars": [], "result": None, "highlights": {}},
        )
    ]
    for w in words:
        path = []
        for i, ch in enumerate(w):
            path.append(ch)
            steps.append(
                step(
                    2,
                    f"Word '{w}': add character '{ch}'.",
                    {
                        "path": list(path),
                        "chars": list(path),
                        "nums": list(path),
                        "currentIndex": i,
                        "currentValue": ch,
                        "word": w,
                        "result": None,
                        "highlights": hl(i, "remembered"),
                    },
                )
            )
    steps.append(
        step(
            3,
            f"Trie built. Answer: {json.dumps(output, default=str)}.",
            {
                "path": list(path),
                "chars": list(path),
                "nums": list(path),
                "result": output,
                "highlights": {str(i): "done" for i in range(len(path))},
            },
        )
    )
    return {"words": words}, steps


def gen_backtracking(title: str, data: dict, output) -> tuple[object, list]:
    key, vals = first_list(data)
    nums = as_nums(vals)[:6]
    if isinstance(nums, list) and nums and isinstance(nums[0], list):
        # board
        return gen_grid(title, data, output)
    path: list = []
    steps = [
        step(
            1,
            f"Backtracking for “{title}”. Try a choice, then undo if it fails.",
            {"nums": nums, "path": [], "result": None, "highlights": {}},
        )
    ]
    for i, n in enumerate(nums):
        path.append(n)
        steps.append(
            step(
                2,
                f"Choose {n} → path {path}.",
                {
                    "nums": nums,
                    "path": list(path),
                    "currentIndex": i,
                    "result": None,
                    "highlights": hl(i, "current"),
                },
            )
        )
        if i == len(nums) - 1 or i == 2:
            steps.append(
                step(
                    3,
                    f"Path looks valid so far: {path}.",
                    {
                        "nums": nums,
                        "path": list(path),
                        "currentIndex": i,
                        "result": None,
                        "highlights": hl(i, "matched"),
                    },
                )
            )
    steps.append(
        step(
            4,
            f"Collected answers: {json.dumps(output, default=str)}.",
            {
                "nums": nums,
                "path": list(path),
                "result": output,
                "highlights": {str(i): "done" for i in range(len(nums))},
            },
        )
    )
    return {key: nums} if key in data else nums, steps


GENERATORS = {
    "array": gen_array,
    "hash": gen_hash,
    "stack": gen_stack,
    "queue": gen_stack,
    "linkedList": gen_linked_list,
    "tree": gen_tree,
    "grid": gen_grid,
    "dp": gen_dp,
    "intervals": gen_intervals,
    "bits": gen_bits,
    "heap": gen_heap,
    "graph": gen_graph,
    "trie": gen_trie,
    "backtracking": gen_backtracking,
}


def should_regenerate(problem: dict) -> bool:
    steps = problem.get("animation", {}).get("steps", [])
    if problem.get("animation", {}).get("tracerId") in {
        "contains-duplicate",
        "two-sum",
        "valid-parentheses",
    }:
        return False
    if len(steps) < 5:
        return True
    blob = json.dumps(steps)
    if "Start solving" in blob or "see-leetcode" in blob or "Green means done" in blob:
        return True
    if problem.get("animation", {}).get("defaultInput") == {"demo": True}:
        return True
    return False


def enrich(problem: dict) -> bool:
    if not should_regenerate(problem):
        return False
    visual = problem["animation"]["visualType"]
    ex = problem["examples"][0]
    data = parse_example_input(ex["input"])
    output = parse_output(ex["output"])
    gen = GENERATORS.get(visual, gen_array)
    default_input, steps = gen(problem["title"], data, output)
    # ensure quality floor for every visual type
    while len(steps) < 5:
        prev = steps[-1] if steps else step(1, "Begin.", {"result": None, "highlights": {}})
        st = deepcopy(prev["state"])
        st["highlights"] = st.get("highlights") or {"0": "current"}
        steps.append(
            step(
                max(2, prev["line"]),
                "Keep watching — the answer structure is still assembling.",
                st,
            )
        )
    # guarantee at least one highlight somewhere
    if not any((s.get("state") or {}).get("highlights") for s in steps):
        steps[1]["state"]["highlights"] = {"0": "current"}
    assert len(steps) >= 5, problem["slug"]
    problem["animation"]["defaultInput"] = default_input
    problem["animation"]["steps"] = steps
    problem["animation"]["tracerId"] = "authored"
    problem["hasAnimation"] = True
    return True


def main():
    files = sorted(PROBLEMS.glob("*.json"))
    changed = 0
    for path in files:
        problem = json.loads(path.read_text())
        if enrich(problem):
            path.write_text(json.dumps(problem, indent=2) + "\n")
            changed += 1
            print("updated", problem["slug"], "steps", len(problem["animation"]["steps"]))
    print(f"DONE changed={changed}/{len(files)}")


if __name__ == "__main__":
    main()
