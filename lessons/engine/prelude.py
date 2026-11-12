"""LeetCode-style building blocks that every traced solution can use.

The node classes register every instance they create.  That lets the lesson
views draw *all* linked-list / tree nodes that exist at a given moment, even
ones the solution has detached or is still assembling.
"""

from __future__ import annotations

from collections import deque


class Registry:
    """Tracks node objects and hands out small, stable ids for them."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.lists: list = []  # every ListNode, in creation order
        self.trees: list = []  # every TreeNode, in creation order
        self.pos: dict[int, tuple[int, int]] = {}  # id(node) -> (row, col)
        self.row_len: dict[int, int] = {}
        self.input_rows = 0  # rows used by input lists; run-time nodes go below
        self.cur_row: int | None = None
        self._uid: dict[int, int] = {}
        self._keep: list = []  # keep objects alive so id() is never reused
        self._n = 0

    def uid(self, obj) -> int:
        key = id(obj)
        if key not in self._uid:
            self._n += 1
            self._uid[key] = self._n
            self._keep.append(obj)
        return self._uid[key]

    def add_list(self, node) -> None:
        row = self.cur_row if self.cur_row is not None else self.input_rows
        col = self.row_len.get(row, 0)
        self.row_len[row] = col + 1
        self.pos[id(node)] = (row, col)
        self.lists.append(node)
        self.uid(node)

    def add_tree(self, node) -> None:
        self.trees.append(node)
        self.uid(node)


REG = Registry()


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        REG.add_list(self)

    def __repr__(self) -> str:
        return f"Node({self.val})"


class RandomListNode(ListNode):
    """Linked-list node with an extra `random` pointer (LeetCode 138)."""

    def __init__(self, x=0, next=None, random=None):
        super().__init__(x, next)
        self.random = random


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        REG.add_tree(self)

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class GraphNode:
    """Undirected graph node (LeetCode 133)."""

    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self) -> str:
        return f"Node({self.val})"


# --------------------------------------------------------------------------
# Builders used in lesson arguments
# --------------------------------------------------------------------------


def L(values, pos: int = -1):
    """Build a linked list from a Python list.  `pos` makes a cycle (tail -> index)."""
    values = list(values)
    if not values:
        return None
    REG.cur_row = REG.input_rows
    nodes = [ListNode(v) for v in values]
    REG.cur_row = None
    REG.input_rows += 1
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def LR(pairs):
    """Build a list with random pointers from [[val, random_index_or_None], ...]."""
    if not pairs:
        return None
    REG.cur_row = REG.input_rows
    nodes = [RandomListNode(v) for v, _ in pairs]
    REG.cur_row = None
    REG.input_rows += 1
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    for node, (_, r) in zip(nodes, pairs):
        node.random = nodes[r] if r is not None else None
    return nodes[0]


def T(values):
    """Build a binary tree from a LeetCode level-order list (None = no child)."""
    values = list(values)
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def G(adj):
    """Build an undirected graph from a 1-indexed adjacency list; returns node 1."""
    if not adj:
        return None
    nodes = [GraphNode(i + 1) for i in range(len(adj))]
    for node, neighbors in zip(nodes, adj):
        node.neighbors = [nodes[j - 1] for j in neighbors]
    return nodes[0]


def find(root, val):
    """Return the first tree node with the given value (pre-order)."""
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val == val:
            return node
        stack.append(node.right)
        stack.append(node.left)
    return None


# --------------------------------------------------------------------------
# Converters used to compare / display results
# --------------------------------------------------------------------------


def list_vals(head, limit: int = 200):
    out, seen = [], set()
    while head is not None and id(head) not in seen and len(out) < limit:
        seen.add(id(head))
        out.append(head.val)
        head = head.next
    return out


def tree_vals(root):
    """LeetCode level-order serialisation with trailing Nones trimmed."""
    if root is None:
        return []
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def graph_adj(node):
    """Adjacency list (1-indexed values) of the graph reachable from `node`."""
    if node is None:
        return []
    seen, order, queue = {id(node): node}, [], deque([node])
    while queue:
        cur = queue.popleft()
        order.append(cur)
        for nb in cur.neighbors:
            if id(nb) not in seen:
                seen[id(nb)] = nb
                queue.append(nb)
    order.sort(key=lambda n: n.val)
    return [[nb.val for nb in n.neighbors] for n in order]


def normalize(value):
    """Turn a solution result into plain JSON-like data for comparison."""
    if isinstance(value, ListNode):
        return list_vals(value)
    if isinstance(value, TreeNode):
        return tree_vals(value)
    if isinstance(value, GraphNode):
        return graph_adj(value)
    if isinstance(value, (list, tuple, deque)):
        return [normalize(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(normalize(v) for v in value)
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    return value
