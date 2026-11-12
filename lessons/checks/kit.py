"""Shared pieces for the correctness checks: registry, input builders, tree helpers."""

from __future__ import annotations

from collections import deque

CHECKS: dict[str, tuple] = {}


def check(slug: str, cases: int = 150):
    """Register a check.  The function gets a ``random.Random`` and returns
    ``(call, expected)``:

    * ``call`` is the keyword-argument source for the solution (see ``args``),
      or a list of operation strings for a design problem;
    * ``expected`` is the reference answer, or an ``Ok(judge)`` when more than
      one answer is right.
    """

    def register(fn):
        if slug in CHECKS:
            raise ValueError(f"duplicate check for {slug}")
        CHECKS[slug] = (fn, cases)
        return fn

    return register


class Ok:
    """A judge for problems with several right answers.

    ``judge(answer)`` returns True when the answer is acceptable, or a short
    text saying what is wrong with it.
    """

    def __init__(self, judge, note: str = ""):
        self.judge = judge
        self.note = note


class Raw(str):
    """Source text that must be passed through as it is (not repr'd)."""


def args(**values) -> str:
    """Keyword-argument source: ``args(nums=[1, 2], k=3)`` -> ``"nums=[1, 2], k=3"``."""
    return ", ".join(f"{k}={v if isinstance(v, Raw) else repr(v)}" for k, v in values.items())


def LL(values, pos: int | None = None) -> Raw:
    """A linked list argument (``pos`` links the tail back to that index)."""
    return Raw(f"L({list(values)!r})" if pos is None else f"L({list(values)!r}, pos={pos})")


def TT(level_order) -> Raw:
    """A binary tree argument from a LeetCode level-order list."""
    return Raw(f"T({list(level_order)!r})")


SKIP = object()  # "this call returns nothing worth comparing" (design problems)


def calls(want: list) -> Ok:
    """Judge for a design problem: compare every call's result with the reference,
    ignoring the positions marked SKIP (constructors, void methods)."""

    def judge(got):
        from lessons import build  # late import: build pulls in the whole engine

        if len(got) != len(want):
            return f"{len(got)} results for {len(want)} calls"
        for i, (g, w) in enumerate(zip(got, want)):
            if w is SKIP:
                continue
            if not build.same(g, w, 0):
                return f"call number {i} returned {g!r}, expected {w!r}"
        return True

    return Ok(judge)


def same_sets(got, want) -> bool | str:
    """True when `got` lists exactly the groups in `want` (order inside a group and
    order of the groups do not matter, but nothing may be listed twice)."""
    canon = sorted(tuple(sorted(x)) for x in got)
    if len(set(canon)) != len(canon):
        return "the same item is listed twice"
    return canon == sorted(tuple(sorted(x)) for x in want) or "the groups differ from the reference"


# -- random data ---------------------------------------------------------------


def ints(rng, n_lo: int, n_hi: int, lo: int, hi: int) -> list[int]:
    return [rng.randint(lo, hi) for _ in range(rng.randint(n_lo, n_hi))]


def word(rng, n_lo: int, n_hi: int, alphabet: str = "abc") -> str:
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(n_lo, n_hi)))


def grid(rng, r_lo: int, r_hi: int, c_lo: int, c_hi: int, cell) -> list[list]:
    rows, cols = rng.randint(r_lo, r_hi), rng.randint(c_lo, c_hi)
    return [[cell() for _ in range(cols)] for _ in range(rows)]


def neighbours(r: int, c: int, rows: int, cols: int):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def regions(cells) -> list[set]:
    """Split a set of (row, col) cells into 4-connected groups."""
    left, out = set(cells), []
    while left:
        start = left.pop()
        group, todo = {start}, [start]
        while todo:
            r, c = todo.pop()
            for cell in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if cell in left:
                    left.discard(cell)
                    group.add(cell)
                    todo.append(cell)
        out.append(group)
    return out


def reachable(start, edges, directed: bool = False) -> set:
    """Every node that can be reached from `start` along `edges`."""
    seen, todo = {start}, [start]
    while todo:
        node = todo.pop()
        for a, b in edges:
            for x, y in ((a, b),) if directed else ((a, b), (b, a)):
                if x == node and y not in seen:
                    seen.add(y)
                    todo.append(y)
    return seen


def traceable(board, text: str) -> bool:
    """Can `text` be spelled on the board by moving between neighbouring cells,
    using no cell twice?  (Plain exhaustive search.)"""
    rows, cols = len(board), len(board[0])

    def go(r, c, i, used):
        if board[r][c] != text[i]:
            return False
        if i == len(text) - 1:
            return True
        used = used | {(r, c)}
        return any(go(nr, nc, i + 1, used) for nr, nc in neighbours(r, c, rows, cols) if (nr, nc) not in used)

    return any(go(r, c, 0, frozenset()) for r in range(rows) for c in range(cols))


# -- binary trees as nested [value, left, right] lists --------------------------


def rand_tree(rng, n: int, value):
    """A random binary tree with ``n`` nodes; ``value()`` supplies each value."""
    if n <= 0:
        return None
    left = rng.randint(0, n - 1)
    return [value(), rand_tree(rng, left, value), rand_tree(rng, n - 1 - left, value)]


def rand_bst(rng, values):
    """A binary search tree built by inserting ``values`` in a random order."""
    order = list(values)
    rng.shuffle(order)
    root = None
    for v in order:
        if root is None:
            root = [v, None, None]
            continue
        node = root
        while True:
            side = 1 if v < node[0] else 2
            if node[side] is None:
                node[side] = [v, None, None]
                break
            node = node[side]
    return root


def level(root) -> list:
    """LeetCode level-order list of a nested tree (trailing Nones trimmed)."""
    if root is None:
        return []
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node[0])
        queue.append(node[1])
        queue.append(node[2])
    while out and out[-1] is None:
        out.pop()
    return out


def walk(root):
    """Every node of a nested tree (pre-order)."""
    if root is not None:
        yield root
        yield from walk(root[1])
        yield from walk(root[2])


def height(root) -> int:
    return 0 if root is None else 1 + max(height(root[1]), height(root[2]))


def inorder(root) -> list:
    return [] if root is None else inorder(root[1]) + [root[0]] + inorder(root[2])


def preorder(root) -> list:
    return [] if root is None else [root[0]] + preorder(root[1]) + preorder(root[2])


def clone(root):
    return None if root is None else [root[0], clone(root[1]), clone(root[2])]
