"""Views: each one photographs a live Python object for one lesson step.

A view is declared once per lesson, e.g. ``Arr("nums", ptrs=["l", "r"])``.
Whenever a step is recorded it evaluates its expressions against the running
solution and returns plain JSON for the 3D stage to draw.

Tones (colours with a fixed meaning in every lesson):
    cur   the thing being looked at right now
    alt   a second thing being compared with it
    good  matched / part of the answer
    bad   rejected / mismatch / removed
    seen  visited or remembered
    win   inside the current window / range / active path
    mark  waiting in a queue or flagged for later
    dim   no longer relevant
"""

from __future__ import annotations

import math
import re
from collections import deque

from . import fmt
from .core import MISSING, TONES, Ctx, LessonError
from .prelude import REG, GraphNode, ListNode, TreeNode

_CONTAINERS = (list, tuple, set, frozenset, deque, range, dict)


def _slug(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z]+", "_", text).strip("_") or "view"


def _check_tone(tone: str) -> str:
    if tone not in TONES and not tone.startswith("#"):
        raise LessonError(f"unknown tone {tone!r}")
    return tone


def _ptr_map(ptrs) -> dict:
    if not ptrs:
        return {}
    if isinstance(ptrs, dict):
        return dict(ptrs)
    if isinstance(ptrs, str):
        ptrs = [ptrs]
    return {name: name for name in ptrs}


def _ptr_value(ctx, spec):
    """Value of a pointer spec: an expression, or (expression, show-only-when)."""
    if isinstance(spec, tuple):
        expr, when = spec
        if not ctx.ev(when, False):
            return MISSING
        return ctx.ev(expr, MISSING)
    return ctx.ev(spec, MISSING)


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _indices(val, n: int) -> list[int]:
    if val is None or isinstance(val, (bool, str)):
        return []
    if _is_int(val):
        val = [val]
    out = []
    try:
        for i in val:
            if not _is_int(i):
                continue
            if i < 0:
                i += n
            if 0 <= i < n:
                out.append(i)
    except TypeError:
        return []
    return out


def _cells(val) -> list[tuple[int, int]]:
    if val is None or isinstance(val, (bool, str)):
        return []
    if isinstance(val, (tuple, list)) and len(val) == 2 and all(_is_int(x) for x in val):
        return [(val[0], val[1])]
    out = []
    try:
        for item in val:
            if isinstance(item, (tuple, list)) and len(item) == 2 and all(_is_int(x) for x in item):
                out.append((item[0], item[1]))
    except TypeError:
        return []
    return out


def _objects(val) -> list:
    if val is None or isinstance(val, (bool, str, int, float)):
        return []
    if isinstance(val, dict):
        return list(val.keys())
    if isinstance(val, _CONTAINERS):
        return [v for v in val if v is not None]
    return [val]


class View:
    kind = "?"

    def __init__(self, id: str, title: str | None = None, tones: dict | None = None):
        self.id = id
        self.title = title
        self.tones = dict(tones or {})
        for tone in self.tones:
            _check_tone(tone)

    def reset(self) -> None:
        pass

    def on_call(self, ctx: Ctx, call) -> None:
        pass

    def on_return(self, ctx: Ctx, call) -> None:
        pass

    def finalize(self, snapshots: list[dict]) -> None:
        pass

    def render(self, ctx: Ctx) -> dict | None:
        raise NotImplementedError

    # helpers -------------------------------------------------------------

    def _tone_values(self, ctx: Ctx, view_id: str | None = None) -> list[tuple[str, object]]:
        out = []
        for tone, expr in list(self.tones.items()) + ctx.extra(view_id or self.id):
            _check_tone(tone)
            val = ctx.ev(expr, MISSING)
            if val is MISSING or val is None or val is False:
                continue
            out.append((tone, val))
        return out

    def _base(self) -> dict:
        data = {"t": self.kind, "id": self.id}
        if self.title:
            data["title"] = self.title
        return data


# --------------------------------------------------------------------------
# Array (lists, strings, 1-D DP tables, bar charts)
# --------------------------------------------------------------------------


class Arr(View):
    """A row of cells.

    ptrs   names (or {label: expr}) of index variables drawn as arrows
    tones  {tone: expr} -> index or indexes to colour
    rng    (lo, hi[, label[, tone]]) inclusive bracket under the cells, or a list of them
    bars   draw numbers as bar heights (heights, prices, histograms)
    water  expr -> list of extra height drawn as water above each bar
    pool   (lo, hi, level) -> one sheet of water held between two bars
    box    (lo, hi, height) -> a rectangle covering bars lo..hi up to `height`
    """

    kind = "array"

    def __init__(self, expr, title=None, ptrs=None, tones=None, rng=None, bars=False,
                 water=None, pool=None, box=None, id=None, idx=True, text=None):
        super().__init__(id or _slug(expr if isinstance(expr, str) else "arr"),
                         title if title is not None else (expr if isinstance(expr, str) else None),
                         tones)
        self.expr = expr
        self.ptrs = _ptr_map(ptrs)
        if rng is None:
            self.rngs = []
        elif isinstance(rng, list):
            self.rngs = rng
        else:
            self.rngs = [rng]
        self.bars = bars
        self.water = water
        self.pool = pool
        self.box = box
        self.idx = idx
        self.text = text

    def render(self, ctx):
        seq = ctx.ev(self.expr, MISSING)
        if seq is MISSING or seq is None:
            return None
        try:
            seq = list(seq)
        except TypeError:
            return None
        n = len(seq)
        tones: dict[int, str] = {}
        for tone, val in self._tone_values(ctx):
            for i in _indices(val, n):
                tones[i] = tone
        cells = []
        for i, v in enumerate(seq):
            c = {"v": self.text(v) if self.text else fmt.cell(v)}
            if i in tones:
                c["tone"] = tones[i]
            if self.bars and isinstance(v, (int, float)) and not isinstance(v, bool):
                c["n"] = v
            cells.append(c)
        data = self._base()
        data["cells"] = cells
        ptrs = []
        for name, expr in self.ptrs.items():
            p = _ptr_value(ctx, expr)
            if _is_int(p) and -1 <= p <= n:
                ptrs.append({"name": name, "at": p})
        if ptrs:
            data["ptrs"] = ptrs
        ranges = []
        for spec in self.rngs:
            lo, hi = ctx.ev(spec[0], MISSING), ctx.ev(spec[1], MISSING)
            if _is_int(lo) and _is_int(hi) and n:
                lo, hi = max(lo, 0), min(hi, n - 1)
                if lo <= hi:
                    r = {"from": lo, "to": hi}
                    if len(spec) > 2 and spec[2]:
                        r["label"] = ctx.fmt(spec[2], spec[2])
                    if len(spec) > 3 and spec[3]:
                        r["tone"] = _check_tone(spec[3])
                    ranges.append(r)
        if ranges:
            data["ranges"] = ranges
        if self.bars:
            data["bars"] = True
            if self.water is not None:
                w = ctx.ev(self.water, None)
                if isinstance(w, (list, tuple)) and len(w) == n:
                    data["water"] = [max(0, x) if isinstance(x, (int, float)) else 0 for x in w]
            if self.pool is not None:
                lo, hi, level = (ctx.ev(e, MISSING) for e in self.pool)
                if (_is_int(lo) and _is_int(hi) and 0 <= lo < hi < n
                        and isinstance(level, (int, float)) and not isinstance(level, bool)):
                    data["pool"] = {"from": lo, "to": hi, "h": level}
            if self.box is not None:
                lo, hi, level = (ctx.ev(e, MISSING) for e in self.box)
                if (_is_int(lo) and _is_int(hi) and 0 <= lo <= hi < n
                        and isinstance(level, (int, float)) and not isinstance(level, bool)):
                    data["box"] = {"from": lo, "to": hi, "h": level}
        if not self.idx:
            data["idx"] = False
        return data

    def finalize(self, snapshots):
        if not self.bars:
            return
        top = 1
        for snap in snapshots:
            water = snap.get("water") or [0] * len(snap["cells"])
            for cell, w in zip(snap["cells"], water):
                top = max(top, cell.get("n", 0) + w)
        for snap in snapshots:
            snap["max"] = top


# --------------------------------------------------------------------------
# Hash map / set
# --------------------------------------------------------------------------


class HMap(View):
    """A dict, Counter, defaultdict or set drawn as key -> value tiles."""

    kind = "map"

    def __init__(self, expr, title=None, tones=None, id=None, key=None, val=None):
        super().__init__(id or _slug(expr if isinstance(expr, str) else "map"),
                         title if title is not None else (expr if isinstance(expr, str) else None),
                         tones)
        self.expr = expr
        self.key = key
        self.val = val
        self._order: list = []

    def reset(self):
        self._order = []

    def render(self, ctx):
        obj = ctx.ev(self.expr, MISSING)
        if obj is MISSING or obj is None:
            return None
        is_set = isinstance(obj, (set, frozenset))
        if is_set:
            # sets have no order: keep first-seen order so tiles do not jump
            present = set(obj)
            self._order = [k for k in self._order if k in present]
            known = set(self._order)
            fresh = [k for k in obj if k not in known]
            fresh.sort(key=lambda k: (str(type(k)), fmt.cell(k)) if not _is_int(k) else ("", f"{k:020d}"))
            self._order.extend(fresh)
            keys = list(self._order)
        elif isinstance(obj, dict):
            keys = list(obj.keys())
        else:
            return None
        tones: dict = {}
        for tone, val in self._tone_values(ctx):
            try:
                single = val in obj
            except TypeError:
                single = False
            if single:
                tones[val] = tone
            elif isinstance(val, _CONTAINERS):
                for k in val:
                    try:
                        if k in obj:
                            tones[k] = tone
                    except TypeError:
                        pass
        entries = []
        for k in keys:
            e = {"k": self.key(k) if self.key else fmt.cell(k)}
            if not is_set:
                e["v"] = self.val(obj[k]) if self.val else fmt.cell(obj[k])
            if k in tones:
                e["tone"] = tones[k]
            entries.append(e)
        data = self._base()
        data["kind"] = "set" if is_set else "map"
        data["entries"] = entries
        return data


# --------------------------------------------------------------------------
# Stack / queue / call stack
# --------------------------------------------------------------------------


def _carry_ids(prev_vals, prev_ids, vals, counter):
    """Keep ids for items that survived so pushes/pops animate properly."""
    best_k, best_cp = 0, -1
    for k in range(len(prev_vals) + 1):
        cp = 0
        while k + cp < len(prev_vals) and cp < len(vals) and prev_vals[k + cp] == vals[cp]:
            cp += 1
        if cp > best_cp:
            best_k, best_cp = k, cp
    ids = list(prev_ids[best_k : best_k + best_cp])
    while len(ids) < len(vals):
        counter[0] += 1
        ids.append(counter[0])
    return ids


class Stack(View):
    """A stack (drawn as a pile, top on top)."""

    kind = "stack"
    shape = "stack"

    def __init__(self, expr, title=None, tones=None, id=None, text=None):
        super().__init__(id or _slug(expr if isinstance(expr, str) else "stack"),
                         title if title is not None else (expr if isinstance(expr, str) else None),
                         tones)
        self.expr = expr
        self.text = text
        self.reset()

    def reset(self):
        self._vals: list = []
        self._ids: list = []
        self._counter = [0]

    def render(self, ctx):
        seq = ctx.ev(self.expr, MISSING)
        if seq is MISSING or seq is None:
            return None
        try:
            seq = list(seq)
        except TypeError:
            return None
        vals = [self.text(v) if self.text else fmt.cell(v) for v in seq]
        self._ids = _carry_ids(self._vals, self._ids, vals, self._counter)
        self._vals = vals
        tones: dict[int, str] = {}
        for tone, val in self._tone_values(ctx):
            for i in _indices(val, len(vals)):
                tones[i] = tone
        items = []
        for i, v in enumerate(vals):
            item = {"id": self._ids[i], "v": v}
            if i in tones:
                item["tone"] = tones[i]
            items.append(item)
        data = self._base()
        data["kind"] = self.shape
        data["items"] = items
        return data


class Queue(Stack):
    """A queue / deque (drawn left to right, front on the left)."""

    shape = "queue"


class Calls(View):
    """The recursion call stack: one slab per active call of `fn`."""

    kind = "stack"

    def __init__(self, fn, label, title="call stack", id="calls"):
        super().__init__(id, title)
        self.fns = {fn} if isinstance(fn, str) else set(fn)
        self.label = label

    def render(self, ctx):
        rec = ctx.rec
        items = []
        base_env = dict(ctx.env)
        for info in rec.frames:
            if info.name not in self.fns:
                continue
            env = dict(base_env)
            env.update(info.frame.f_locals)
            label = Ctx(rec, env, {}).fmt(self.label, info.name)
            items.append({"id": info.call.id + 1, "v": label})
        if items:
            items[-1]["tone"] = "cur"
        data = self._base()
        data["kind"] = "calls"
        data["items"] = items
        return data


# --------------------------------------------------------------------------
# Scalars and result lists
# --------------------------------------------------------------------------


class Vars(View):
    """Plain variables shown as name = value chips beside the code."""

    kind = "vars"

    def __init__(self, *names, id="vars"):
        super().__init__(id)
        self.items = [(n, n) if isinstance(n, str) else (n[0], n[1]) for n in names]

    def render(self, ctx):
        items = []
        for label, expr in self.items:
            val = ctx.ev(expr, MISSING)
            if val is MISSING:
                continue
            items.append({"k": label, "v": fmt.show(val, 48)})
        if not items:
            return None
        data = self._base()
        data["items"] = items
        return data

    def finalize(self, snapshots):
        prev: dict = {}
        for snap in snapshots:
            for item in snap["items"]:
                if item["k"] in prev and prev[item["k"]] != item["v"]:
                    item["changed"] = True
            prev = {item["k"]: item["v"] for item in snap["items"]}


class Items(View):
    """A list of finished pieces (results, groups, paths) drawn as slabs."""

    kind = "items"

    def __init__(self, expr, title=None, tones=None, id=None, text=None):
        super().__init__(id or _slug(expr if isinstance(expr, str) else "items"),
                         title if title is not None else (expr if isinstance(expr, str) else None),
                         tones)
        self.expr = expr
        self.text = text

    def render(self, ctx):
        val = ctx.ev(self.expr, MISSING)
        if val is MISSING or val is None:
            return None
        if isinstance(val, dict):
            seq = list(val.values())
        elif isinstance(val, (list, tuple, deque)):
            seq = list(val)
        elif isinstance(val, (set, frozenset)):
            seq = sorted(val, key=fmt.cell)
        else:
            seq = [val]
        tones: dict[int, str] = {}
        for tone, tv in self._tone_values(ctx):
            for i in _indices(tv, len(seq)):
                tones[i] = tone
        items = []
        for i, v in enumerate(seq):
            if self.text:
                text = self.text(v)
            elif isinstance(v, str):
                text = v if v != "" else '""'
            else:
                text = fmt.show(v, 40)
            item = {"v": text}
            if i in tones:
                item["tone"] = tones[i]
            items.append(item)
        data = self._base()
        data["items"] = items
        return data


# --------------------------------------------------------------------------
# Linked lists
# --------------------------------------------------------------------------


class LinkedList(View):
    """Every ListNode that exists, drawn where it was created.

    Arrows follow each node's real `.next`, so re-wiring is visible as the
    arrows move.  Input lists sit on their own rows; nodes created by the
    solution (dummy heads, copies...) appear on the row below.

    place  {expr: (row, col)} puts a particular node somewhere else (a dummy
           head to the left of the lists, for instance)
    names  {expr: label} shows a label instead of the node's value
    """

    kind = "list"

    def __init__(self, title=None, ptrs=None, tones=None, id="list", rows=None, text=None,
                 place=None, names=None):
        super().__init__(id, title, tones)
        self.ptrs = _ptr_map(ptrs)
        self.rows = rows
        self.text = text
        self.place = dict(place or {})
        self.names = dict(names or {})
        self._placed: dict[int, tuple] = {}
        self._named: dict[int, str] = {}

    def reset(self):
        self._placed = {}
        self._named = {}

    def finalize(self, snapshots):
        xs = [n["x"] for snap in snapshots for n in snap["nodes"]]
        ys = [n["y"] for snap in snapshots for n in snap["nodes"]]
        dx = -min(xs) if xs and min(xs) < 0 else 0
        dy = -min(ys) if ys and min(ys) < 0 else 0
        if dx or dy:
            for snap in snapshots:
                for n in snap["nodes"]:
                    n["x"] += dx
                    n["y"] += dy

    def render(self, ctx):
        nodes = REG.lists
        if not nodes:
            return None
        tones: dict[int, str] = {}
        for tone, val in self._tone_values(ctx):
            for obj in _objects(val):
                if isinstance(obj, ListNode):
                    tones[id(obj)] = tone
        for expr, where in self.place.items():
            node = ctx.ev(expr, None)
            if isinstance(node, ListNode):
                self._placed[id(node)] = where
        for expr, label in self.names.items():
            node = ctx.ev(expr, None)
            if isinstance(node, ListNode):
                self._named[id(node)] = label
        out = []
        for node in nodes:
            row, col = self._placed.get(id(node)) or REG.pos[id(node)]
            if id(node) in self._named:
                label = self._named[id(node)]
            else:
                label = self.text(node) if self.text else fmt.cell(node.val)
            item = {"id": REG.uid(node), "v": label, "x": col, "y": row}
            nxt = getattr(node, "next", None)
            if isinstance(nxt, ListNode):
                item["next"] = REG.uid(nxt)
            rnd = getattr(node, "random", None)
            if isinstance(rnd, ListNode):
                item["rand"] = REG.uid(rnd)
            if id(node) in tones:
                item["tone"] = tones[id(node)]
            out.append(item)
        data = self._base()
        data["nodes"] = out
        ptrs = []
        for name, expr in self.ptrs.items():
            val = _ptr_value(ctx, expr)
            if val is MISSING:
                continue
            if val is None:
                ptrs.append({"name": name, "at": None})
            elif isinstance(val, ListNode):
                ptrs.append({"name": name, "at": REG.uid(val)})
        if ptrs:
            data["ptrs"] = ptrs
        if self.rows:
            data["rows"] = list(self.rows)
        return data


class Chain(View):
    """A linked structure drawn in traversal order from `head` (for custom node
    classes such as the doubly linked list inside an LRU cache)."""

    kind = "list"

    def __init__(self, head, title=None, label="{n.val}", nxt="next", ptrs=None, tones=None,
                 id="chain", limit=24):
        super().__init__(id, title, tones)
        self.head = head
        self.label = label
        self.nxt = nxt
        self.ptrs = _ptr_map(ptrs)
        self.limit = limit

    def render(self, ctx):
        head = ctx.ev(self.head, MISSING)
        if head is MISSING:
            return None
        chain, seen = [], set()
        node = head
        while node is not None and id(node) not in seen and len(chain) < self.limit:
            seen.add(id(node))
            chain.append(node)
            node = getattr(node, self.nxt, None)
        tones: dict[int, str] = {}
        for tone, val in self._tone_values(ctx):
            for obj in _objects(val):
                tones[id(obj)] = tone
        out = []
        for i, n in enumerate(chain):
            env = dict(ctx.env)
            env["n"] = n
            item = {"id": REG.uid(n), "v": Ctx(ctx.rec, env, {}).fmt(self.label, "?"), "x": i, "y": 0}
            nxt = getattr(n, self.nxt, None)
            if nxt is not None and id(nxt) in seen:
                item["next"] = REG.uid(nxt)
            if id(n) in tones:
                item["tone"] = tones[id(n)]
            out.append(item)
        data = self._base()
        data["nodes"] = out
        ptrs = []
        for name, expr in self.ptrs.items():
            val = ctx.ev(expr, MISSING)
            if val is MISSING:
                continue
            if val is None:
                ptrs.append({"name": name, "at": None})
            elif id(val) in seen:
                ptrs.append({"name": name, "at": REG.uid(val)})
        if ptrs:
            data["ptrs"] = ptrs
        return data


# --------------------------------------------------------------------------
# Trees
# --------------------------------------------------------------------------


class Tree(View):
    """Binary tree(s).

    root        expression (or list of expressions) for the root(s); when
                omitted every TreeNode that exists is drawn, so trees that are
                being built or cloned show up piece by piece
    stack       name of the node argument of the recursive function: the
                node being visited is `cur`, its ancestors on the call stack `win`
    ret_badges  (function name, argument name): show each finished call's
                return value next to its node
    badges      expression -> {node: value} drawn next to nodes
    """

    kind = "tree"

    def __init__(self, root=None, title=None, ptrs=None, tones=None, id="tree", stack=None,
                 badges=None, ret_badges=None, text=None):
        super().__init__(id, title, tones)
        self.roots = [root] if isinstance(root, str) else (list(root) if root else None)
        self.ptrs = _ptr_map(ptrs)
        self.stack = stack
        self.badges = badges
        self.ret_badges = ret_badges
        self.text = text

    def _collect(self, ctx) -> list:
        if self.roots is None:
            return list(REG.trees)
        out, seen = [], set()
        for expr in self.roots:
            todo = [ctx.ev(expr, None)]
            while todo:
                node = todo.pop()
                if not isinstance(node, TreeNode) or id(node) in seen:
                    continue
                seen.add(id(node))
                out.append(node)
                todo.append(node.right)
                todo.append(node.left)
        return out

    def render(self, ctx):
        nodes = self._collect(ctx)
        if not nodes:
            return None
        present = {id(n) for n in nodes}
        tones: dict[int, str] = {}
        if self.stack:
            names = [self.stack] if isinstance(self.stack, str) else list(self.stack)
            chain = []
            for info in ctx.rec.frames:
                for name in names:
                    val = info.frame.f_locals.get(name)
                    if isinstance(val, TreeNode):
                        chain.append((info, val))
                        break
            for _, val in chain:
                tones[id(val)] = "win"
            if chain and chain[-1][0] is ctx.rec.frames[-1]:
                tones[id(chain[-1][1])] = "cur"
        for tone, val in self._tone_values(ctx):
            for obj in _objects(val):
                if isinstance(obj, TreeNode):
                    tones[id(obj)] = tone
        badges: dict[int, str] = {}
        if self.ret_badges:
            fn, arg = self.ret_badges
            for call in ctx.rec.calls:
                if call.fn == fn and call.done and isinstance(call.args.get(arg), TreeNode):
                    badges[id(call.args[arg])] = fmt.cell(call.ret)
        if self.badges is not None:
            table = ctx.ev(self.badges, None)
            if isinstance(table, dict):
                for node, value in table.items():
                    if isinstance(node, TreeNode):
                        badges[id(node)] = value if isinstance(value, str) else fmt.cell(value)
        children = set()
        out = []
        for node in nodes:
            item = {"id": REG.uid(node), "v": self.text(node) if self.text else fmt.cell(node.val)}
            if isinstance(node.left, TreeNode) and id(node.left) in present:
                item["l"] = REG.uid(node.left)
                children.add(id(node.left))
            if isinstance(node.right, TreeNode) and id(node.right) in present:
                item["r"] = REG.uid(node.right)
                children.add(id(node.right))
            if id(node) in tones:
                item["tone"] = tones[id(node)]
            if id(node) in badges:
                item["badge"] = badges[id(node)]
            out.append(item)
        data = self._base()
        data["nodes"] = out
        data["roots"] = [REG.uid(n) for n in nodes if id(n) not in children]
        ptrs = []
        for name, expr in self.ptrs.items():
            val = _ptr_value(ctx, expr)
            if isinstance(val, TreeNode) and id(val) in present:
                ptrs.append({"name": name, "at": REG.uid(val)})
        if ptrs:
            data["ptrs"] = ptrs
        return data


class Heap(View):
    """A heapq list drawn as the binary tree it represents."""

    kind = "tree"

    def __init__(self, expr, title=None, tones=None, id=None, text=None, neg=False):
        super().__init__(id or _slug(expr if isinstance(expr, str) else "heap"),
                         title if title is not None else (expr if isinstance(expr, str) else None),
                         tones)
        self.expr = expr
        self.text = text
        self.neg = neg

    def _label(self, v) -> str:
        if self.text:
            return self.text(v)
        if self.neg:
            if isinstance(v, (int, float)):
                v = -v
            elif isinstance(v, (tuple, list)) and v and isinstance(v[0], (int, float)):
                v = (-v[0], *v[1:])
        return fmt.cell(v)

    def render(self, ctx):
        heap = ctx.ev(self.expr, MISSING)
        if heap is MISSING or heap is None:
            return None
        heap = list(heap)
        n = len(heap)
        tones: dict[int, str] = {}
        for tone, val in self._tone_values(ctx):
            for i in _indices(val, n):
                tones[i] = tone
        nodes = []
        for i, v in enumerate(heap):
            item = {"id": i + 1, "v": self._label(v)}
            if 2 * i + 1 < n:
                item["l"] = 2 * i + 2
            if 2 * i + 2 < n:
                item["r"] = 2 * i + 3
            if i in tones:
                item["tone"] = tones[i]
            nodes.append(item)
        data = self._base()
        data["nodes"] = nodes
        data["roots"] = [1] if n else []
        data["shape"] = "box" if any(len(x["v"]) > 3 for x in nodes) else "circle"
        return data


class Trie(View):
    """A trie drawn from its root; each node shows the letter that leads to it."""

    kind = "tree"
    _END_NAMES = ("is_end", "end", "isEnd", "is_word", "isWord", "word", "is_end_of_word",
                  "end_of_word", "endOfWord", "is_end_word")

    def __init__(self, root, title=None, children="children", end=None, ptrs=None, tones=None,
                 id="trie"):
        super().__init__(id, title, tones)
        self.root = root
        self.children = children
        self.end = end
        self.ptrs = _ptr_map(ptrs)

    def _kids(self, node) -> list[tuple[str, object]]:
        kids = getattr(node, self.children, None)
        if isinstance(node, dict):
            kids = {k: v for k, v in node.items() if isinstance(v, dict)}
        if isinstance(kids, dict):
            return [(str(k), v) for k, v in kids.items()]
        if isinstance(kids, (list, tuple)):
            return [(chr(ord("a") + i), v) for i, v in enumerate(kids) if v is not None]
        return []

    def _is_end(self, node) -> bool:
        names = (self.end,) if self.end else self._END_NAMES
        for name in names:
            if isinstance(node, dict):
                if node.get(name):
                    return True
            elif getattr(node, name, None):
                return True
        return False

    def render(self, ctx):
        root = ctx.ev(self.root, MISSING)
        if root is MISSING or root is None:
            return None
        tones: dict[int, str] = {}
        for tone, val in self._tone_values(ctx):
            for obj in _objects(val) if not isinstance(val, dict) else [val]:
                tones[id(obj)] = tone
        nodes = []
        present = set()
        todo = deque([(root, "•")])
        while todo and len(nodes) < 120:
            node, ch = todo.popleft()
            if id(node) in present:
                continue
            present.add(id(node))
            kids = self._kids(node)
            item = {"id": REG.uid(node), "v": ch}
            if kids:
                item["kids"] = [REG.uid(k) for _, k in kids]
            if self._is_end(node):
                item["end"] = True
            if id(node) in tones:
                item["tone"] = tones[id(node)]
            nodes.append(item)
            for ch2, kid in kids:
                todo.append((kid, ch2))
        data = self._base()
        data["nodes"] = nodes
        data["roots"] = [REG.uid(root)]
        ptrs = []
        for name, expr in self.ptrs.items():
            val = ctx.ev(expr, MISSING)
            if val is not MISSING and val is not None and id(val) in present:
                ptrs.append({"name": name, "at": REG.uid(val)})
        if ptrs:
            data["ptrs"] = ptrs
        return data


class RecTree(View):
    """The recursion tree of `fn`, grown one call at a time.

    label      caption template evaluated when the call starts
    mark_call  {tone: expr} checked when a call starts (tone stays on the node)
    mark_ret   {tone: expr} checked when a call returns (`_ret` is its result)
    ret        show each call's return value as a badge
    """

    kind = "tree"

    def __init__(self, fn, label, title="recursion tree", id="rec", ret=False,
                 mark_call=None, mark_ret=None):
        super().__init__(id, title)
        self.fn = fn
        self.label = label
        self.ret = ret
        self.mark_call = dict(mark_call or {})
        self.mark_ret = dict(mark_ret or {})
        for tone in list(self.mark_call) + list(self.mark_ret):
            _check_tone(tone)
        self.reset()

    def reset(self):
        self._calls: list = []

    def on_call(self, ctx, call):
        if call.fn != self.fn:
            return
        info = {"label": ctx.fmt(self.label, self.fn), "tone": None, "badge": None}
        for tone, expr in self.mark_call.items():
            if ctx.ev(expr, False):
                info["tone"] = tone
        parent = call.parent
        while parent is not None and parent.fn != self.fn:
            parent = parent.parent
        info["parent"] = parent
        call.data[self.id] = info
        self._calls.append(call)

    def on_return(self, ctx, call):
        info = call.data.get(self.id)
        if info is None:
            return
        for tone, expr in self.mark_ret.items():
            if ctx.ev(expr, False):
                info["tone"] = tone
        if self.ret:
            info["badge"] = fmt.cell(call.ret)

    def render(self, ctx):
        if not self._calls:
            return None
        kids: dict[int, list[int]] = {}
        for call in self._calls:
            parent = call.data[self.id]["parent"]
            if parent is not None:
                kids.setdefault(parent.id, []).append(call.id + 1)
        active = [c for c in self._calls if not c.done]
        nodes = []
        for call in self._calls:
            info = call.data[self.id]
            item = {"id": call.id + 1, "v": info["label"]}
            if call.id in kids:
                item["kids"] = kids[call.id]
            tone = info["tone"]
            if not call.done:
                tone = "cur" if active and call is active[-1] else "win"
            if tone:
                item["tone"] = tone
            if info["badge"] is not None:
                item["badge"] = info["badge"]
            nodes.append(item)
        data = self._base()
        data["nodes"] = nodes
        data["roots"] = [c.id + 1 for c in self._calls if c.data[self.id]["parent"] is None]
        data["shape"] = "box"
        return data


# --------------------------------------------------------------------------
# Graphs
# --------------------------------------------------------------------------


class Graph(View):
    """Nodes and edges.

    nodes     expr -> iterable of node keys
    edges     expr -> iterable of (a, b) or (a, b, weight)
    adj       expr -> {node: [neighbours]} (alternative to edges)
    adj_item  how an adjacency entry is stored: "nb" | "nb_w" | "w_nb"
    pos       {key: (x, y)} to place nodes by hand (y grows upward); circle otherwise
    etones    {tone: expr} -> edge (a, b) or list of edges
    badges    expr -> {key: value} drawn beside nodes (distances, in-degrees...)
    """

    kind = "graph"

    def __init__(self, nodes, edges=None, adj=None, directed=False, pos=None, title=None,
                 tones=None, etones=None, badges=None, id="graph", adj_item="nb", labels=None):
        super().__init__(id, title, tones)
        self.nodes = nodes
        self.edges = edges
        self.adj = adj
        self.directed = directed
        self.pos = pos
        self.etones = dict(etones or {})
        for tone in self.etones:
            _check_tone(tone)
        self.badges = badges
        self.adj_item = adj_item
        self.labels = labels
        self.reset()

    def reset(self):
        self._layout: dict = {}
        self._order: list = []

    def _place(self, keys):
        for k in keys:
            if k not in self._layout and k not in self._order:
                self._order.append(k)
        if self.pos:
            for k in self._order:
                if k in self.pos:
                    self._layout[k] = tuple(self.pos[k])
        missing = [k for k in self._order if k not in self._layout]
        if not missing:
            return
        n = len(self._order)
        radius = max(1.5, n * 0.42)
        for i, k in enumerate(self._order):
            if k in self._layout:
                continue
            angle = math.pi / 2 - 2 * math.pi * i / n
            self._layout[k] = (round(radius * math.cos(angle), 3), round(radius * math.sin(angle), 3))

    def _edge_list(self, ctx, keyset):
        out = []
        if self.edges is not None:
            for e in ctx.ev(self.edges, None) or []:
                e = tuple(e)
                if len(e) >= 2 and e[0] in keyset and e[1] in keyset:
                    out.append((e[0], e[1], e[2] if len(e) > 2 else None))
        if self.adj is not None:
            adj = ctx.ev(self.adj, None) or {}
            items = adj.items() if isinstance(adj, dict) else enumerate(adj)
            for a, nbs in items:
                for item in nbs or []:
                    w = None
                    b = item
                    if self.adj_item == "nb_w":
                        b, w = item[0], item[1]
                    elif self.adj_item == "w_nb":
                        w, b = item[0], item[1]
                    if a in keyset and b in keyset:
                        out.append((a, b, w))
        if not self.directed:
            seen, uniq = set(), []
            for a, b, w in out:
                key = frozenset((a, b)) if a != b else (a, b)
                if key in seen:
                    continue
                seen.add(key)
                uniq.append((a, b, w))
            out = uniq
        return out

    def render(self, ctx):
        keys = ctx.ev(self.nodes, MISSING)
        if keys is MISSING or keys is None:
            return None
        keys = list(keys)
        if not keys:
            return None
        self._place(keys)
        keyset = set(keys)
        tones: dict = {}
        for tone, val in self._tone_values(ctx):
            try:
                single = val in keyset
            except TypeError:
                single = False
            if single:
                tones[val] = tone
            elif isinstance(val, _CONTAINERS):
                for k in val:
                    try:
                        if k in keyset:
                            tones[k] = tone
                    except TypeError:
                        pass
        badges = ctx.ev(self.badges, None) if self.badges is not None else None
        labels = ctx.ev(self.labels, None) if self.labels is not None else None
        nodes = []
        for k in keys:
            x, y = self._layout[k]
            item = {"id": fmt.cell(k), "v": fmt.cell(labels[k]) if labels and k in labels else fmt.cell(k),
                    "x": x, "y": y}
            if k in tones:
                item["tone"] = tones[k]
            if badges is not None:
                try:
                    b = badges[k]
                    item["badge"] = b if isinstance(b, str) else fmt.cell(b)
                except (KeyError, IndexError, TypeError):
                    pass
            nodes.append(item)
        etones: dict = {}
        for tone, expr in list(self.etones.items()) + ctx.extra(self.id + "_edges"):
            _check_tone(tone)
            val = ctx.ev(expr, None)
            if val is None:
                continue
            pairs = []
            if isinstance(val, (tuple, list)) and len(val) >= 2 and not isinstance(val[0], (tuple, list)):
                pairs = [val]
            else:
                try:
                    pairs = [p for p in val if isinstance(p, (tuple, list)) and len(p) >= 2]
                except TypeError:
                    pairs = []
            for p in pairs:
                etones[(p[0], p[1])] = tone
                if not self.directed:
                    etones[(p[1], p[0])] = tone
        edges = []
        for a, b, w in self._edge_list(ctx, keyset):
            e = {"a": fmt.cell(a), "b": fmt.cell(b)}
            if w is not None:
                e["w"] = fmt.cell(w)
            if (a, b) in etones:
                e["tone"] = etones[(a, b)]
            edges.append(e)
        data = self._base()
        data["nodes"] = nodes
        data["edges"] = edges
        if self.directed:
            data["directed"] = True
        return data


# --------------------------------------------------------------------------
# Grids (matrices, boards, 2-D DP tables)
# --------------------------------------------------------------------------


class Grid(View):
    """A 2-D grid.

    vals   {cell text: tone} fixed colouring by value (land / water / wall...)
    tones  {tone: expr} -> (r, c) or a collection of them
    ptrs   {label: expr} -> (r, c) marker
    rows / cols   expr -> header labels (e.g. the two strings of an LCS table)
    blank  cell texts that should be drawn empty
    changed  tone for every cell whose value differs from the first snapshot
    """

    kind = "grid"

    def __init__(self, expr, title=None, tones=None, vals=None, ptrs=None, rows=None, cols=None,
                 id=None, blank=(), text=None, changed=None):
        super().__init__(id or _slug(expr if isinstance(expr, str) else "grid"),
                         title if title is not None else (expr if isinstance(expr, str) else None),
                         tones)
        self.expr = expr
        self.vals = dict(vals or {})
        for tone in self.vals.values():
            _check_tone(tone)
        self.ptrs = dict(ptrs or {})
        self.rows = rows
        self.cols = cols
        self.blank = set(blank)
        self.text = text
        self.changed = _check_tone(changed) if changed else None
        self._first = None

    def reset(self):
        self._first = None

    def render(self, ctx):
        grid = ctx.ev(self.expr, MISSING)
        if grid is MISSING or grid is None:
            return None
        try:
            rows = [list(r) for r in grid]
        except TypeError:
            return None
        if not rows:
            return None
        tones: dict[tuple[int, int], str] = {}
        for tone, val in self._tone_values(ctx):
            for rc in _cells(val):
                tones[rc] = tone
        cells = []
        for r, row in enumerate(rows):
            line = []
            for c, v in enumerate(row):
                text = self.text(v) if self.text else fmt.cell(v)
                item = {"v": "" if text in self.blank else text}
                tone = tones.get((r, c))
                if tone is None and self.changed and self._first is not None:
                    try:
                        if self._first[r][c] != text:
                            tone = self.changed
                    except IndexError:
                        pass
                tone = tone or self.vals.get(text)
                if tone:
                    item["tone"] = tone
                line.append(item)
            cells.append(line)
        if self._first is None:
            self._first = [[self.text(v) if self.text else fmt.cell(v) for v in row] for row in rows]
        data = self._base()
        data["cells"] = cells
        for key, expr in (("rows", self.rows), ("cols", self.cols)):
            if expr is None:
                continue
            labels = ctx.ev(expr, None)
            if labels is not None:
                data[key] = [fmt.cell(x) for x in labels]
        ptrs = []
        for name, expr in self.ptrs.items():
            val = ctx.ev(expr, None)
            for r, c in _cells(val)[:1]:
                if 0 <= r < len(rows) and 0 <= c < len(rows[r]):
                    ptrs.append({"name": name, "r": r, "c": c})
        if ptrs:
            data["ptrs"] = ptrs
        return data


# --------------------------------------------------------------------------
# Intervals
# --------------------------------------------------------------------------


class Intervals(View):
    """Intervals on a number line.

    rows   list of (key, expr[, tones]) - each row is one list of [start, end]
    marks  {label: expr} -> a position on the axis (e.g. a query point)
    Note-level marks address a row by its key: {"merged.good": "-1"}.
    """

    kind = "intervals"

    def __init__(self, rows, title=None, id="intervals", marks=None):
        super().__init__(id, title)
        self.rows = []
        for row in rows:
            key, expr = row[0], row[1]
            tones = dict(row[2]) if len(row) > 2 and row[2] else {}
            for tone in tones:
                _check_tone(tone)
            self.rows.append((key, expr, tones))
        self.marks = dict(marks or {})

    def render(self, ctx):
        out_rows = []
        for key, expr, tones in self.rows:
            val = ctx.ev(expr, MISSING)
            if val is MISSING or val is None:
                continue
            seq = list(val)
            if len(seq) == 2 and all(isinstance(x, (int, float)) for x in seq):
                seq = [seq]
            toned: dict[int, str] = {}
            for tone, texpr in list(tones.items()) + ctx.extra(key):
                _check_tone(tone)
                tv = ctx.ev(texpr, None)
                for i in _indices(tv, len(seq)):
                    toned[i] = tone
            items = []
            for i, iv in enumerate(seq):
                try:
                    a, b = iv[0], iv[1]
                except (TypeError, IndexError):
                    continue
                item = {"a": a, "b": b}
                if i in toned:
                    item["tone"] = toned[i]
                items.append(item)
            out_rows.append({"label": key, "items": items})
        if not out_rows:
            return None
        data = self._base()
        data["rows"] = out_rows
        marks = []
        for label, expr in self.marks.items():
            val = ctx.ev(expr, None)
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                marks.append({"x": val, "label": ctx.fmt(label, label)})
        if marks:
            data["marks"] = marks
        return data

    def finalize(self, snapshots):
        lo, hi = math.inf, -math.inf
        for snap in snapshots:
            for row in snap["rows"]:
                for item in row["items"]:
                    lo, hi = min(lo, item["a"]), max(hi, item["b"])
            for mark in snap.get("marks", []):
                lo, hi = min(lo, mark["x"]), max(hi, mark["x"])
        if lo is math.inf:
            lo, hi = 0, 1
        for snap in snapshots:
            snap["min"], snap["max"] = lo, hi


# --------------------------------------------------------------------------
# Bits
# --------------------------------------------------------------------------


class Bits(View):
    """Numbers written in binary, one per row, columns aligned.

    rows  list of (label, expr[, tone])
    hi    expr -> bit position(s) counted from the right (0 = lowest bit)
    """

    kind = "bits"

    def __init__(self, rows, width=8, title=None, id="bits", hi=None):
        super().__init__(id, title)
        self.rows = [(r[0], r[1], r[2] if len(r) > 2 else None) for r in rows]
        self.width = width
        self.hi = hi

    def render(self, ctx):
        rows = []
        for label, expr, tone in self.rows:
            val = ctx.ev(expr, MISSING)
            if val is MISSING or not _is_int(val):
                continue
            row = {"label": ctx.fmt(label, label), "bits": fmt.bits(val, self.width), "v": str(val)}
            if tone:
                row["tone"] = _check_tone(tone)
            rows.append(row)
        if not rows:
            return None
        data = self._base()
        data["rows"] = rows
        if self.hi is not None:
            cols = sorted({self.width - 1 - p for p in _indices(ctx.ev(self.hi, None), self.width)})
            if cols:
                data["hi"] = cols
        return data
