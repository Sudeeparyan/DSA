"""Turning Python values into short display text."""

from __future__ import annotations

import math
from collections import deque

from .prelude import GraphNode, ListNode, TreeNode, list_vals, tree_vals


def cell(v) -> str:
    """Compact text for something drawn inside a block (array cell, node...)."""
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "T" if v else "F"
    if isinstance(v, float):
        if math.isinf(v):
            return "∞" if v > 0 else "-∞"
        if v == int(v):
            return str(int(v))
        return f"{v:.2f}".rstrip("0").rstrip(".")
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        if v == "":
            return '""'
        if v == " ":
            return "␣"
        return v
    if isinstance(v, (ListNode, TreeNode, GraphNode)):
        return cell(v.val)
    if isinstance(v, tuple):
        return "(" + ",".join(cell(x) for x in v) + ")"
    if isinstance(v, (list, deque)):
        return "[" + ",".join(cell(x) for x in v) + "]"
    if isinstance(v, (set, frozenset)):
        return "{" + ",".join(sorted((cell(x) for x in v), key=_sort_key)) + "}"
    if isinstance(v, dict):
        return "{" + ",".join(f"{cell(k)}:{cell(x)}" for k, x in v.items()) + "}"
    return str(v)


def _sort_key(text: str):
    try:
        return (0, float(text), text)
    except ValueError:
        return (1, 0.0, text)


def show(v, limit: int = 60) -> str:
    """Readable Python-style text for captions and the variables panel."""
    text = _show(v)
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text


def _show(v) -> str:
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        if math.isinf(v):
            return "∞" if v > 0 else "-∞"
        if v == int(v) and abs(v) < 1e15:
            return f"{v:.1f}"
        return f"{v:.5f}".rstrip("0").rstrip(".")
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return '"' + v + '"'
    if isinstance(v, ListNode):
        return "[" + " → ".join(_show(x) for x in list_vals(v, 12)) + "]"
    if isinstance(v, TreeNode):
        return "tree " + _show(tree_vals(v))
    if isinstance(v, GraphNode):
        return f"node {v.val}"
    if isinstance(v, tuple):
        inner = ", ".join(_show(x) for x in v)
        return "(" + inner + ("," if len(v) == 1 else "") + ")"
    if isinstance(v, (list, deque)):
        return "[" + ", ".join(_show(x) for x in v) + "]"
    if isinstance(v, (set, frozenset)):
        if not v:
            return "{}"
        return "{" + ", ".join(sorted((_show(x) for x in v), key=_sort_key)) + "}"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{_show(k)}: {_show(x)}" for k, x in v.items()) + "}"
    return str(v)


def leet(v) -> str:
    """LeetCode-style input/output text: [1,2,3], "abc", null-free Python words."""
    if isinstance(v, ListNode):
        return leet(list_vals(v))
    if isinstance(v, TreeNode):
        return leet(tree_vals(v))
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        return _show(v)
    if isinstance(v, str):
        return '"' + v + '"'
    if isinstance(v, (list, tuple, deque)):
        return "[" + ",".join(leet(x) for x in v) + "]"
    if isinstance(v, (set, frozenset)):
        return "[" + ",".join(sorted(leet(x) for x in v)) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{leet(k)}: {leet(x)}" for k, x in v.items()) + "}"
    return str(v)


def pretty(v, indent: int = 0) -> str:
    """Like `leet`, but a long matrix gets one row per line."""
    text = leet(v)
    rows = v if isinstance(v, (list, tuple)) else None
    if rows and len(text) > 44 and all(isinstance(r, (list, tuple)) for r in rows):
        pad = " " * (indent + 1)
        return "[" + ("," + chr(10) + pad).join(leet(r) for r in rows) + "]"
    return text


def bits(n: int, width: int = 8) -> str:
    return format(n & ((1 << width) - 1), f"0{width}b")


def plural(n: int, word: str, many: str | None = None) -> str:
    return f"{n} {word if n == 1 else (many or word + 's')}"


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
