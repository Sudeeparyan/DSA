"""Trees."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "invert-binary-tree",
    pattern="Tree recursion (DFS)",
    statement="""Given the `root` of a binary tree, invert it — swap the left and right child of
    **every** node — and return the root. The result is the mirror image of the original tree.""",
    args="root=T([4, 2, 7, 1, 3, 6, 9])",
    expected=[4, 7, 2, 9, 6, 3, 1],
    why="Every node's children are swapped, so each level reads right-to-left.",
    picture="""Picture holding a family tree up to a mirror. In the mirror every person's left and right
    children have swapped places, and so have their children's children, all the way down. The code
    does exactly that: at each node it swaps the two children, then asks the same function to mirror
    each child's own family below.""",
    idea=[
        "Mirroring a whole tree sounds big, but at one node it is tiny: just swap its left and right child.",
        "Do that swap at **every** node and the entire tree is mirrored. Recursion visits every node for us.",
        "Recipe for a node: swap its children → invert the left subtree → invert the right subtree. An empty node (None) needs nothing.",
    ],
    views=[
        Tree(stack="root", tones={"good": "_done('invertTree', 'root')"}),
    ],
    notes=[
        ("if not root", dict(
            yes="This child is empty (None). There is nothing to invert, so return straight away. "
                "This is the base case that stops the recursion.",
            first=1)),
        ("root.left, root.right = root.right, root.left", [
            ("root.left or root.right",
             "At node **{root.val}**: swap its two children. Now {nv(root.left)} is on the left and "
             "{nv(root.right)} on the right — their whole subtrees move with them."),
            (None,
             "Node **{root.val}** is a leaf: both children are empty, so swapping them changes nothing."),
        ]),
        ("self.invertTree(root.left)", dict(
            pre="Now mirror everything underneath node {root.val}'s left child ({nv(root.left)}).",
            when="root.left is not None")),
        ("self.invertTree(root.right)", dict(
            pre="Left side of node {root.val} is done. Now mirror its right child ({nv(root.right)}).",
            when="root.right is not None")),
        ("return root", dict(
            post="Everything under node {root.val} is mirrored. Return to its parent.",
            when="(root.left or root.right) and _depth > 1")),
    ],
    say={
        "def invertTree": (
            "The function we must write. It gets the top node (`root`) and returns it after "
            "mirroring the whole tree."
        ),
        "if not root": "Is there no node here (an empty spot below a leaf)?",
        "return None": "Then there is nothing to mirror: return nothing.",
        "root.left, root.right = root.right, root.left": (
            "Swap this node's two children in one move: the left becomes the right and the right "
            "becomes the left."
        ),
        "self.invertTree(root.left)": (
            "Now mirror everything below the new left child: the function calls itself on that "
            "smaller tree."
        ),
        "self.invertTree(root.right)": "And the same below the new right child.",
        "return root": "This node and everything below it are mirrored: hand it back.",
    },
    time=("O(n)", "Every node is visited once and does a constant amount of work."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h (log n if balanced, n if it is a chain)."),
    tests=[("root=T([2, 1, 3])", [2, 3, 1]), ("root=T([])", []), ("root=T([1, 2])", [1, None, 2])],
)

lesson(
    "maximum-depth-of-binary-tree",
    pattern="Tree recursion: combine the answers of both children",
    statement="""Given the `root` of a binary tree, return its **maximum depth**: the number of
    nodes on the longest path from the root down to a leaf.""",
    args="root=T([3, 9, 20, None, None, 15, 7])",
    expected=3,
    why="The longest path is 3 → 20 → 15 (or 3 → 20 → 7): three nodes.",
    picture="""Picture asking everyone in a family tree: *how many generations are there from you down to the
    youngest?* Someone with no children answers 1. Anyone else first asks both children, takes the
    bigger answer and adds 1 for themselves. The answer that reaches the top person is the depth of
    the whole tree.""",
    idea=[
        "The depth of a tree is 1 (for the root itself) plus the depth of its **deeper** subtree.",
        "The depth of each subtree is the same question on a smaller tree — so ask it recursively.",
        "The recursion stops at an empty spot, whose depth is 0. Each node then answers `max(left, right) + 1`.",
    ],
    views=[Tree(stack="root", ret_badges=("maxDepth", "root"))],
    notes=[
        ("if not root", dict(
            yes="An empty spot (None) has depth 0. That is the base case which stops the recursion.",
            first=1)),
        ("left_depth = self.maxDepth(root.left)", dict(
            pre="Node {root.val} asks its **left** child ({root.left.val}): how deep is your subtree?",
            when="root.left is not None")),
        ("right_depth = self.maxDepth(root.right)", dict(
            pre="The left side of node {root.val} answered {left_depth}. Now it asks its **right** child ({root.right.val}).",
            when="root.right is not None")),
        ("return max(left_depth, right_depth) + 1", [
            ("not root.left and not root.right",
             "Node {root.val} is a leaf: both sides are empty (depth 0), so its depth is 0 + 1 = **1**."),
            (None,
             "Node {root.val}: left depth {left_depth}, right depth {right_depth}. Take the deeper side and add "
             "this node: max({left_depth}, {right_depth}) + 1 = **{_ret}**."),
        ]),
    ],
    say={
        "def maxDepth": (
            "The function we must write. It gets a node and returns how many levels the tree "
            "below it has."
        ),
        "if not root": "Is this an empty spot, with no node?",
        "return 0": "Then it adds no levels: 0.",
        "left_depth = self.maxDepth(root.left)": (
            "Ask the same question of the left child: how deep is the tree below it? (The "
            "function calls itself.)"
        ),
        "right_depth = self.maxDepth(root.right)": "And of the right child.",
        "return max(left_depth, right_depth) + 1": (
            "This node's depth is its deeper side plus 1 for the node itself."
        ),
    },
    time=("O(n)", "Every node is visited once."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("root=T([1, None, 2])", 2), ("root=T([])", 0), ("root=T([1])", 1)],
)

lesson(
    "diameter-of-binary-tree",
    pattern="Tree recursion: return height, track best path",
    statement="""Return the **diameter** of a binary tree: the number of edges on the longest path
    between any two nodes. The path does not have to pass through the root.""",
    args="root=T([1, 2, 3, 4, 5])",
    expected=3,
    why="The path 4 → 2 → 1 → 3 has three edges (so does 5 → 2 → 1 → 3).",
    picture="""Picture the tree as rooms joined by corridors. The longest walk between two rooms climbs up to
    some highest room and then goes down again. At that top room, the walk is as long as the deepest
    way down its left side plus the deepest way down its right side. So every node measures how far
    down each side goes and adds the two; the biggest sum anywhere is the diameter.""",
    idea=[
        "Every path has one highest node where it *bends*: it comes up from the left subtree and goes down into the right subtree.",
        "The longest path bending at a node has `height(left) + height(right)` edges.",
        "So compute every node's height recursively, and at each node also check `left height + right height` against the best diameter seen so far.",
    ],
    views=[
        Tree(stack="node", ret_badges=("height", "node")),
        Vars(("self.diameter", "self.diameter")),
    ],
    notes=[
        ("self.diameter = 0",
         "`self.diameter` keeps the longest path found so far. The small labels that will appear beside "
         "nodes are their **heights**."),
        ("if not node", dict(yes="An empty spot has height 0.", first=1)),
        ("self.diameter = max(self.diameter, left_height + right_height)",
         "At node {node.val}: left height {left_height}, right height {right_height}. The longest path that bends "
         "here has {left_height} + {right_height} = **{left_height + right_height}** edges. Best so far: **{self.diameter}**."),
        ("return max(left_height, right_height) + 1",
         "Node {node.val} reports its own height to its parent: max({left_height}, {right_height}) + 1 = **{_ret}**."),
        ("return self.diameter", "The longest path found anywhere in the tree has **{_ret}** edges."),
    ],
    say={
        "def diameterOfBinaryTree": (
            "The function we must write. It gets the top node and returns the length of the "
            "longest path, counted in edges."
        ),
        "def height(node)": (
            "A helper: how many nodes lie on the longest way down from `node`? While it works, it"
            " also checks the path that turns at `node`."
        ),
        "if not node": "Is this an empty spot?",
        "return 0": "Then its height is 0.",
        "left_height = height(node.left)": (
            "The height of the left side (the helper calls itself)."
        ),
        "right_height = height(node.right)": "The height of the right side.",
        "self.diameter = max(self.diameter, left_height + right_height)": (
            "A path that turns at this node uses `left_height + right_height` edges. Keep it if "
            "it is the longest so far."
        ),
        "return max(left_height, right_height) + 1": (
            "This node's own height: its taller side, plus 1 for itself."
        ),
        "self.diameter = 0": (
            "The longest path found so far. (`self.` lets the helper change it.)"
        ),
        "height(root)": (
            "Measure the whole tree from the top; the helper records the longest path on the way."
        ),
        "return self.diameter": "Return the longest path found.",
    },
    time=("O(n)", "Each node's height is computed once."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("root=T([1, 2])", 1), ("root=T([1])", 0),
           ("root=T([1, 2, None, 3, 4, 5, None, None, 6])", 4)],
)

lesson(
    "balanced-binary-tree",
    pattern="Tree recursion: height with an early failure signal",
    statement="""A binary tree is **height-balanced** if, at every node, the heights of the left and
    right subtrees differ by at most 1. Return `True` if the given tree is balanced.""",
    args="root=T([1, 2, 2, 3, 3, None, None, 4, 4])",
    expected=False,
    why="At the root the left subtree has height 3 and the right subtree height 1 — a difference of 2.",
    picture="""Picture checking a hanging mobile, joint by joint, from the bottom up. At every joint the two
    sides may differ in height by at most one level. Each joint asks its two sides how tall they
    are. If they differ by more, it reports *broken* (here, infinity), and that report travels all
    the way up to the top.""",
    idea=[
        "Balance is a statement about heights, so compute heights bottom-up with recursion.",
        "At each node compare the two subtree heights. If they differ by more than 1, the tree is unbalanced.",
        "To report that upward without a second return value, this solution returns **infinity** as a failure signal. Infinity survives every `max(...) + 1`, so it reaches the root.",
    ],
    views=[Tree(stack="node", ret_badges=("height", "node"))],
    notes=[
        ("if not node", dict(yes="An empty spot has height 0.", first=1)),
        ("if abs(left_height - right_height) > 1", dict(
            yes="At node {node.val}: left height {left_height}, right height {right_height}. They differ by "
                "{abs(left_height - right_height)} — **more than 1**. The tree is unbalanced here.",
            no=[
                ("not node.left and not node.right",
                 "Node {node.val} is a leaf: both sides have height 0, so it is balanced and has height 1."),
                (None,
                 "At node {node.val}: left height {left_height}, right height {right_height}. They differ by "
                 "{abs(left_height - right_height)}, which is allowed."),
            ],
            yes_marks={"tree.bad": "node"})),
        ("return float(", "Report **infinity** upward: a signal that something below is unbalanced.",
         {"tree.bad": "node"}),
        ("return max(left_height, right_height) + 1", dict(
            post="Node {node.val} reports its height: max({left_height}, {right_height}) + 1 = **{_ret}**.",
            when="node.left or node.right")),
        ("return height(root) != float(",
         "The root came back with infinity, so somewhere two sides differed by more than 1 → **{_ret}**."),
    ],
    say={
        "def isBalanced": (
            "The function we must write. It gets the top node and answers `True` if, at every "
            "node, the two sides differ in height by at most 1."
        ),
        "def height(node)": (
            "A helper that returns a node's height, or infinity if anything below it is "
            "unbalanced."
        ),
        "if not node": "Is this an empty spot?",
        "return 0": "Then its height is 0.",
        "left_height = height(node.left)": (
            "The height of the left side (the helper calls itself)."
        ),
        "right_height = height(node.right)": "The height of the right side.",
        "if abs(left_height - right_height) > 1": (
            "Do the two sides differ by more than 1? (`abs` drops the minus sign.) This is also "
            "true when either side has already reported infinity."
        ),
        'return float("inf")': (
            "Then this part is unbalanced: report infinity, a warning sign that passes all the "
            "way up."
        ),
        "return max(left_height, right_height) + 1": (
            "Balanced here: report the taller side plus 1."
        ),
        'return height(root) != float("inf")': (
            "The tree is balanced exactly when the top did not report infinity."
        ),
    },
    time=("O(n)", "Each node is visited once; the balance check reuses the heights already computed."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("root=T([3, 9, 20, None, None, 15, 7])", True), ("root=T([])", True),
           ("root=T([1, 2, 2, 3, None, None, 3, 4, None, None, 4])", False)],
)

lesson(
    "same-tree",
    pattern="Walk two trees in step",
    statement="""Given the roots of two binary trees `p` and `q`, return `True` if they are the
    same: identical shape, and equal values in every position.""",
    args="p=T([1, 2, 3]), q=T([1, 2, 4])",
    expected=False,
    why="The right children differ: 3 in one tree, 4 in the other.",
    picture="""Picture two people walking through two buildings at the same time, room by room, comparing as
    they go. If one finds a room where the other finds none, or the two rooms have different numbers
    on the door, the buildings differ. If every pair of rooms matches all the way down, they are the
    same.""",
    idea=[
        "Two trees are the same when their roots match, their left subtrees are the same, **and** their right subtrees are the same.",
        "That definition is recursive, so the code is too: compare one pair of nodes, then recurse into both pairs of children.",
        "Two base cases stop it: both spots empty → equal; exactly one empty, or different values → not equal.",
    ],
    views=[Tree(ptrs=["p", "q"], tones={"cur": "[p, q]"})],
    notes=[
        ("if not p and not q", dict(
            yes="Both spots are empty, so they match: return True. (Every pair of empty spots ends this way.)",
            first=1)),
        ("if not p or not q or p.val != q.val", dict(
            yes=[
                ("not p or not q", "One tree has a node here and the other has nothing → **different**."),
                (None, "`p` holds {p.val} but `q` holds {q.val}. The values differ → **different**."),
            ],
            no="`p` holds {p.val} and `q` holds {q.val}: these match. Now their left subtrees must match **and** "
               "their right subtrees must match.",
            yes_marks={"tree.bad": "[p, q]"},
            no_marks={"tree.good": "[p, q]"})),
        ("return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)",
         "Below the pair of {p.val}s: {'both sides matched' if _ret else 'not everything matched'}, so return **{_ret}**."),
    ],
    say={
        "def isSameTree": (
            "The function we must write. It gets two nodes, `p` and `q`, and answers whether the "
            "trees below them are identical."
        ),
        "if not p and not q": "Are both spots empty?",
        "return True": "Two empty trees are the same.",
        "if not p or not q or p.val != q.val": (
            "Is only one of them empty, or do their values (`.val`) differ?"
        ),
        "return False": "Then the trees differ.",
        "return self.isSameTree(p.left, q.left) and": (
            "They match here, so check below: the left sides must match *and* the right sides "
            "must match. The function checks each by calling itself, and `and` stops early if the"
            " left sides already differ."
        ),
    },
    time=("O(n)", "Each pair of nodes is compared once (n = size of the smaller tree)."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("p=T([1, 2, 3]), q=T([1, 2, 3])", True), ("p=T([1, 2]), q=T([1, None, 2])", False),
           ("p=T([]), q=T([])", True)],
)

lesson(
    "subtree-of-another-tree",
    pattern="Try every node as the starting point",
    statement="""Given two binary trees `s` and `t`, return `True` if `t` appears inside `s` as a
    **subtree**: some node of `s`, together with *all* of its descendants, is identical to `t`.""",
    args="s=T([3, 4, 5, 1, 2]), t=T([4, 1, 2])",
    expected=True,
    why="The node 4 in s, with its children 1 and 2, is exactly the tree t.",
    picture="""Picture looking for a small pattern inside a big tree. Stand on each node of the big tree in
    turn and ask: if I start comparing here, does everything below match the small tree exactly? The
    first time the answer is yes, the small tree is a subtree.""",
    idea=[
        "If `t` is inside `s`, it must start at **some node** of `s`.",
        "So visit every node of `s` and ask: is the tree starting here identical to `t`? That check is the *Same Tree* problem.",
        "If it is not identical here, the answer may still be in the left or the right subtree — recurse into both.",
    ],
    views=[Tree(ptrs=["s", "t", "p", "q"], tones={"win": "s", "cur": "[p, q]"})],
    notes=[
        ("if self.isSameTree(s, t)", dict(
            pre="Could `t` start at node {s.val}? Compare the two trees node by node.",
            yes="Every node matched: the subtree at node {s.val} **is** `t`.",
            no="They are not identical, so `t` does not start at node {s.val}. Look inside its left subtree, then its right.",
            yes_marks={"tree.good": "subtree(s) + subtree(t)"})),
        ("if not p or not q or p.val != q.val", dict(
            yes="Comparing {nv(p)} with {nv(q)}: they differ.",
            no="Node {p.val} matches node {q.val}. Keep comparing the nodes below them.",
            yes_marks={"tree.bad": "[p, q]"},
            no_marks={"tree.good": "[p, q]"})),
        ("return True@1", "A matching subtree was found → **True**.",
         {"tree.good": "subtree(s) + subtree(t)"}),
    ],
    say={
        "def isSubtree": (
            "The function we must write. It gets the big tree `s` and the small tree `t`, and "
            "answers whether `t` appears inside `s`."
        ),
        "if not s": "Has the search gone past the bottom of the big tree?",
        "return False@1": "Then `t` was not found down this way.",
        "if self.isSameTree(s, t)": (
            "Starting from this node, is the tree below it identical to `t`?"
        ),
        "return True@1": "Yes: found it.",
        "return self.isSubtree(s.left, t) or": (
            "No: look for `t` in the left side, or else in the right side (the function calls "
            "itself on each)."
        ),
        "def isSameTree": "A helper: are the trees below `p` and `q` identical?",
        "if not p and not q": "Are both spots empty?",
        "return True@2": "Then they match.",
        "if not p or not q or p.val != q.val": (
            "Is only one of them empty, or are the values different?"
        ),
        "return False@2": "Then they differ.",
        "return self.isSameTree(p.left, q.left) and": (
            "Otherwise both sides below must match too."
        ),
    },
    time=("O(m · n)", "In the worst case, each of the m nodes of s starts a comparison that visits up to n nodes of t."),
    space=("O(h)", "The recursion stack is as deep as the height of s."),
    tests=[("s=T([3, 4, 5, 1, 2, None, None, None, None, 0]), t=T([4, 1, 2])", False),
           ("s=T([1]), t=T([1])", True), ("s=T([1, 1]), t=T([1])", True)],
)

lesson(
    "lowest-common-ancestor-of-a-binary-search-tree",
    pattern="Use the BST ordering to choose a side",
    statement="""Given a **binary search tree** and two of its nodes `p` and `q`, return their lowest
    common ancestor: the deepest node that has both `p` and `q` in its subtree (a node counts as
    its own descendant).""",
    args="root=T([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), p=find(root, 3), q=find(root, 5)",
    show_input="root = [6,2,8,0,4,7,9,None,None,3,5], p = node 3, q = node 5",
    result="_ret.val",
    expected=4,
    why="Nodes 3 and 5 are the two children of node 4, so 4 is the deepest node above both.",
    picture="""Picture a sorted family tree where everyone smaller lives to the left and everyone bigger to the
    right. Walk down from the top looking for two people. While both are smaller than where you
    stand, go left; while both are bigger, go right. The first place where they would go different
    ways, or where you meet one of them, is the lowest node above both.""",
    idea=[
        "In a BST everything in a node's left subtree is smaller than the node, and everything in its right subtree is larger.",
        "Start at the root. If **both** targets are smaller, their common ancestor must be in the left subtree; if both are larger, in the right subtree.",
        "The first node where they fall on **different sides** (or which is one of them) is where their paths split — that node is the answer.",
    ],
    views=[Tree(stack="root", ptrs=["p", "q"])],
    notes=[
        ("if root.val > p.val and root.val > q.val", dict(
            yes="At node {root.val}: both {p.val} and {q.val} are **smaller**. In a BST smaller values are in the "
                "left subtree, so their common ancestor is on the left.")),
        ("elif root.val < p.val and root.val < q.val", dict(
            yes="At node {root.val}: both {p.val} and {q.val} are **larger**, so both are in the right subtree. Go right.",
            no="At node {root.val}: {p.val} and {q.val} are **not on the same side** — one is ≤ {root.val} and the "
               "other ≥ {root.val}. Their paths split here, so this is the lowest common ancestor.",
            no_marks={"tree.good": "root"})),
        ("return root", "Return node **{root.val}**.", {"tree.good": "root"}),
    ],
    final={"tree.good": "_ret"},
    say={
        "def lowestCommonAncestor(": (
            "The function we must write. It gets the tree's top node and two nodes, `p` and `q`, "
            "and returns their lowest common ancestor."
        ),
        "if root.val > p.val and root.val > q.val": (
            "Are both values smaller than this node's? In a search tree, smaller values live on "
            "the left."
        ),
        "return self.lowestCommonAncestor(root.left, p, q)": (
            "Then both are on the left: carry on from the left child."
        ),
        "elif root.val < p.val and root.val < q.val": (
            "Are both bigger? Bigger values live on the right."
        ),
        "return self.lowestCommonAncestor(root.right, p, q)": (
            "Then carry on from the right child."
        ),
        "return root": (
            "Otherwise they split here, or this node is one of them: it is the lowest common "
            "ancestor."
        ),
    },
    time=("O(h)", "One step down the tree per comparison, so at most the height h."),
    space=("O(h)", "This recursive version uses one stack frame per level."),
    tests=[("root=T([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), p=find(root, 2), q=find(root, 8)", 6),
           ("root=T([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]), p=find(root, 2), q=find(root, 4)", 2)],
)

lesson(
    "binary-tree-level-order-traversal",
    pattern="Breadth-first search, one level at a time",
    statement="""Given the `root` of a binary tree, return its node values **level by level**: a list
    of lists, top level first, each level read from left to right.""",
    args="root=T([3, 9, 20, None, None, 15, 7])",
    expected=[[3], [9, 20], [15, 7]],
    why="Level 0 is the root 3, level 1 holds 9 and 20, and level 2 holds 15 and 7.",
    picture="""Picture a building whose floors are the levels of the tree. Visit it one floor at a time: write
    down everyone on the current floor from left to right, and meanwhile list who lives on the floor
    below. Then move down to that list and repeat, until there are no more floors.""",
    idea=[
        "Depth-first search dives down one branch. Here we need to finish a whole level before going deeper — that is **breadth-first search**.",
        "Keep a list of all nodes on the current level. Read their values, and while doing so collect their children: those are exactly the next level.",
        "Then swap: the collected children become the current level. Stop when a level has no nodes.",
    ],
    views=[
        Tree(tones={"win": "queue", "mark": "next_level", "cur": "node"}),
        Queue("[x.val for x in queue]", id="queue", title="queue  (the level being read)"),
        Queue("[x.val for x in next_level]", id="next_level", title="next_level  (children found so far)"),
        Items("result", title="result"),
    ],
    notes=[
        ("queue = [root]",
         "`queue` holds every node of the level we are about to read. The first level is just the root."),
        ("level.append(node.val)",
         "Read node {node.val} into the current level: {level}. Its children (if any) are noted for the next level."),
        ("result.append(level)", "The whole level has been read. Add {level} to the result.",
         {"result.good": "-1"}),
        ("queue = next_level", [
            ("next_level", "The children collected on the way — {[x.val for x in queue]} — are the next level. "
                           "They become the new queue."),
            (None, "No children were collected, so there is no next level."),
        ]),
        ("return result", "Every level has been read: **{_ret}**."),
    ],
    say={
        "def levelOrder": (
            "The function we must write. It gets the top node and returns the values level by "
            "level."
        ),
        "if not root": "Is the tree empty?",
        "return []": "Then there are no levels.",
        "result = []": "The answer: one list of values per level.",
        "queue = [root]": "The nodes of the current level. The first level is just the top node.",
        "while queue": "Repeat while the current level has nodes.",
        "level = []": "The values of this level.",
        "next_level = []": "The nodes of the level below, collected as we go.",
        "for node in queue": "Go through this level's nodes, from left to right.",
        "level.append(node.val)": "Write down this node's value.",
        "if node.left": "Does it have a left child?",
        "next_level.append(node.left)": "Then that child belongs to the next level.",
        "if node.right": "Does it have a right child?",
        "next_level.append(node.right)": "Then that child belongs to the next level too.",
        "result.append(level)": "This level is complete: add its values to the answer.",
        "queue = next_level": "Move down one level.",
        "return result": "Return all the levels.",
    },
    time=("O(n)", "Every node is read once."),
    space=("O(n)", "A level can hold up to about half of all nodes."),
    tests=[("root=T([1])", [[1]]), ("root=T([])", []), ("root=T([1, 2, None, 3])", [[1], [2], [3]])],
)

lesson(
    "binary-tree-right-side-view",
    pattern="Breadth-first search: last node of each level",
    statement="""Imagine standing to the **right** of a binary tree. Return the values of the nodes
    you can see, from top to bottom.""",
    code="""
    from collections import deque

    class Solution:
        def rightSideView(self, root: TreeNode) -> List[int]:
            if not root:
                return []

            result = []
            queue = deque([root])

            while queue:
                level_size = len(queue)

                for i in range(level_size):
                    node = queue.popleft()
                    if i == level_size - 1:
                        result.append(node.val)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)

            return result
    """,
    args="root=T([1, 2, 3, 4])",
    expected=[1, 3, 4],
    why="Node 3 hides node 2, but nothing stands to the right of node 4 on the bottom level.",
    picture="""Picture standing to the right of the tree and looking at it side-on: on every level you see only
    the node furthest to the right. So visit the tree level by level, from left to right, and from
    each level keep just its last node.""",
    idea=[
        "From the right you see exactly one node per level: the **rightmost** one.",
        "It is not enough to follow right children — a deeper node in the *left* subtree is visible when the right side is shorter.",
        "So walk the tree level by level with a queue, and for each level record the **last** node taken out.",
    ],
    views=[
        Tree(tones={"mark": "queue", "good": "[x for x in subtree(root) if x.val in result]", "cur": "node"}),
        Queue("[x.val for x in queue]", id="queue", title="queue"),
        Items("result", title="result  (what you see from the right)"),
    ],
    notes=[
        ("queue = deque([root])",
         "We walk the tree **level by level**. Seen from the right, the visible node of each level is the "
         "last one in it."),
        ("level_size = len(queue)",
         "The queue now holds exactly one level: {[x.val for x in queue]} — {plural(level_size, 'node')}."),
        ("node = queue.popleft()",
         "Take node {node.val} from the front: number {i + 1} of {level_size} on this level."),
        ("result.append(node.val)",
         "It is the **last** node of its level, so nothing hides it from the right. Add {node.val}.",
         {"result.good": "-1"}),
        ("queue.append(node.left)", "Queue its left child {node.left.val} for the next level."),
        ("queue.append(node.right)", "Queue its right child {node.right.val} for the next level."),
        ("return result", "One visible node per level: **{_ret}**."),
    ],
    say={
        "def rightSideView": (
            "The function we must write. It gets the top node and returns the values you can see "
            "from the right, from top to bottom."
        ),
        "if not root": "Is the tree empty?",
        "return []": "Then nothing is visible.",
        "result = []": "The visible values, from top to bottom.",
        "queue = deque([root])": (
            "A queue of nodes still to visit, starting with the top node. (A `deque` is quick to "
            "take from at the front.)"
        ),
        "while queue": "Repeat while there are nodes left to visit.",
        "level_size = len(queue)": (
            "Right now the queue holds exactly one whole level. Count its nodes."
        ),
        "for i in range(level_size)": (
            "Visit that many nodes: this level's nodes, from left to right."
        ),
        "node = queue.popleft()": "Take the next node from the front of the queue.",
        "if i == level_size - 1": "Is it the last node of this level, the rightmost one?",
        "result.append(node.val)": "Then it is the one seen from the right: keep its value.",
        "if node.left": "Does it have a left child?",
        "queue.append(node.left)": "Queue it for the next level.",
        "if node.right": "Does it have a right child?",
        "queue.append(node.right)": "Queue it too.",
        "return result": "Return the values seen from the right.",
    },
    time=("O(n)", "Every node passes through the queue once, and a deque removes its front item in O(1)."),
    space=("O(n)", "The queue holds up to one full level."),
    tests=[("root=T([1, 2, 3, None, 5, None, 4])", [1, 3, 4]), ("root=T([1, None, 3])", [1, 3]),
           ("root=T([])", [])],
)

lesson(
    "count-good-nodes-in-binary-tree",
    pattern="DFS carrying the maximum seen on the path",
    statement="""A node of a binary tree is **good** if no node on the path from the root down to it
    has a larger value. Return the number of good nodes.""",
    args="root=T([3, 1, 4, 3, None, 1, 5])",
    expected=4,
    why="Good nodes: the root 3, the node 4, the node 5, and the lower 3 (path 3 → 1 → 3 has nothing above 3).",
    picture="""Picture walking down from the top of the tree carrying a note of the biggest value seen on the
    way so far. A node is *good* if its value is at least as big as the note, so nothing above it
    beats it. A good node updates the note before you walk on to its children.""",
    idea=[
        "Whether a node is good depends only on the **largest value above it** on its own path from the root.",
        "So walk down with DFS and pass that maximum along as an argument.",
        "A node is good if its value is at least that maximum; in that case it also becomes the new maximum for everything below it.",
    ],
    init={"goods": "[]"},
    views=[
        Tree(stack="node", tones={"good": "goods"}, ret_badges=("dfs", "node")),
        Vars("max_val"),
    ],
    notes=[
        ("if not node", dict(yes="An empty spot contains no good nodes: return 0.", first=1)),
        ("if node.val >= max_val", dict(
            yes=[
                ("max_val == -inf", "The root has nothing above it, so it is always **good**."),
                (None, "Node {node.val}: the largest value above it on this path is {max_val}. Nothing above is "
                       "bigger than {node.val}, so it is **good**."),
            ],
            no="Node {node.val}: a bigger value, {max_val}, sits above it on this path. **Not good**.",
            save={"goods": "goods + [node] if node.val >= max_val else goods"},
            no_marks={"tree.bad": "node"})),
        ("return count", dict(
            post="The subtree of node {node.val} contains **{plural(_ret, 'good node')}**. (The small labels are these counts.)",
            when="node.left or node.right")),
    ],
    say={
        "def goodNodes": (
            "The function we must write. It gets the top node and returns how many good nodes "
            "there are."
        ),
        "def dfs(node, max_val)": (
            "A helper that counts the good nodes from `node` down. `max_val` is the biggest value"
            " on the path from the top to here."
        ),
        "if not node": "Is this an empty spot?",
        "return 0": "Then it has no good nodes.",
        "if node.val >= max_val": "Is this node at least as big as everything above it?",
        "max_val = node.val": "Yes: it is good, and it is now the biggest on the path.",
        "count = 1": "Count this node.",
        "count = 0": "No: something above is bigger, so it does not count.",
        "count += dfs(node.left, max_val)": (
            "Add the good nodes on the left side (the helper calls itself and passes the note "
            "down)."
        ),
        "count += dfs(node.right, max_val)": "And those on the right side.",
        "return count": "Report the total for this part of the tree.",
        'return dfs(root, float("-inf"))': (
            "Start at the top with minus infinity as the biggest value seen, so the top node "
            "always counts."
        ),
    },
    time=("O(n)", "Every node is visited once."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("root=T([3, 3, None, 4, 2])", 3), ("root=T([1])", 1), ("root=T([2, None, 1])", 1)],
)

lesson(
    "validate-binary-search-tree",
    pattern="In-order traversal must be increasing",
    statement="""Return `True` if a binary tree is a valid **binary search tree**: for every node,
    all values in its left subtree are smaller and all values in its right subtree are larger.""",
    args="root=T([5, 3, 8, 1, 6])",
    expected=False,
    why="6 sits in the left subtree of 5 but is larger than 5 — even though it is correctly to the right of 3.",
    picture="""Picture reading a sorted bookshelf from left to right: every book must come after the one before
    it. A binary search tree read in order (left side, then the node, then the right side) is
    exactly such a shelf. So read the tree in that order, remembering the last value read. If a
    value is ever not bigger than the one before it, the tree is not a valid search tree.""",
    idea=[
        "Checking each node only against its own children is **not enough**: a node deep in the left subtree must still be smaller than the root far above it.",
        "Key fact: reading a BST *in order* (left subtree, then the node, then right subtree) produces the values in strictly increasing order.",
        "So do an in-order walk and remember the previous value. The moment a value is not larger than the one before it, the tree is not a BST.",
    ],
    init={"seq": "[]"},
    views=[
        Tree(stack="node"),
        Items("seq", title="values read so far, in order"),
    ],
    notes=[
        ("prev = [None]",
         "Reading a BST **in order** (left subtree, node, right subtree) must give increasing values. `prev` "
         "remembers the last value read."),
        ("if not inorder_traversal(node.left, prev)", dict(
            pre="Before node {node.val} itself is read, everything in its **left** subtree comes first.",
            when="node.left is not None")),
        ("if prev[0] is not None and node.val <= prev[0]", dict(
            yes="Read node {node.val}. The value before it was {prev[0]}, and {node.val} is **not larger**. "
                "The order is broken, so this is not a BST.",
            no=[
                ("prev[0] is None", "Read node {node.val}: the very first value, so the smallest."),
                (None, "Read node {node.val}. The value before it was {prev[0]} and {node.val} is larger — still in order."),
            ],
            yes_marks={"tree.bad": "node"},
            no_marks={"tree.good": "node"})),
        ("prev[0] = node.val", dict(save={"seq": "seq + [node.val]"})),
        ("return inorder_traversal(node.right, prev)", dict(
            pre="Node {node.val} is read. Continue with its **right** subtree.",
            when="node.right is not None")),
        ("return False@2", "Return **False** — every caller above passes it straight on.", {"tree.bad": "node"}),
    ],
    say={
        "def isValidBST": (
            "The function we must write. It gets the top node and answers whether the tree is a "
            "valid binary search tree."
        ),
        "def inorder_traversal(node, prev)": (
            "A helper that reads the tree below `node` in order: left side, then the node, then "
            "the right side. `prev[0]` is the last value read."
        ),
        "if not node": "Is this an empty spot?",
        "return True": "There is nothing to read, so nothing is out of order.",
        "if not inorder_traversal(node.left, prev)": (
            "First read the left side. Was something out of order there?"
        ),
        "return False@1": "Then the whole tree is invalid.",
        "if prev[0] is not None and node.val <= prev[0]": (
            "Now this node. Is its value not bigger than the last value read? (`None` means "
            "nothing has been read yet.)"
        ),
        "return False@2": "Then the values are out of order: invalid.",
        "prev[0] = node.val": (
            "Remember this value as the last one read. (It is kept in a one-item list so that "
            "every call shares it.)"
        ),
        "return inorder_traversal(node.right, prev)": (
            "Finally read the right side; its answer is the answer for this part."
        ),
        "prev = [None]": "Nothing has been read yet.",
        "return inorder_traversal(root, prev)": "Read the whole tree, starting from the top.",
    },
    time=("O(n)", "Each node is read at most once."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("root=T([2, 1, 3])", True), ("root=T([5, 1, 4, None, None, 3, 6])", False),
           ("root=T([1, 1])", False), ("root=T([5, 3, 8, 1, 4])", True)],
)

lesson(
    "kth-smallest-element-in-a-bst",
    pattern="In-order walk with a stack, stopping at the k-th value",
    statement="""Given the root of a **binary search tree** and an integer `k`, return the `k`-th
    smallest value in the tree (k = 1 means the smallest).""",
    code="""
    class Solution:
        def kthSmallest(self, root: TreeNode, k: int) -> int:
            stack = []
            current = root

            while stack or current:
                # Go left as far as possible: smaller values come first
                while current:
                    stack.append(current)
                    current = current.left

                # The node on top of the stack is the next value in sorted order
                current = stack.pop()
                k -= 1
                if k == 0:
                    return current.val

                # Everything in its right subtree comes next
                current = current.right
    """,
    args="root=T([5, 3, 6, 2, 4, None, None, 1]), k=3",
    expected=3,
    why="In sorted order the values are 1, 2, 3, 4, 5, 6, and the third is 3.",
    picture="""Picture a binary search tree as a sorted shelf folded into the shape of a tree: reading it left
    side, node, right side gives the values from the smallest up. So read it in that order and
    count, and the `k`-th value read is the answer. A stack remembers the nodes passed on the way
    down, so you can come back up to them.""",
    idea=[
        "In a BST, everything left of a node is smaller and everything right of it is larger.",
        "So reading the tree **in order** — left subtree, the node, right subtree — lists the values from smallest to largest.",
        "The whole list is not needed. Walk the tree in order with a stack, count the values as they come out, and **stop at the k-th one**.",
    ],
    views=[
        Tree("root", ptrs=["current"], tones={"mark": "stack", "seen": "counted", "cur": "current"}),
        Stack("[x.val for x in stack]", id="stack", title="stack  (nodes waiting for their turn)"),
        Vars("k"),
    ],
    init={"counted": "[]"},
    final={"tree.good": "[x for x in subtree(root) if x.val == _ret]"},
    notes=[
        ("stack = []",
         "An in-order walk visits a BST from the smallest value to the largest. The stack remembers the nodes "
         "we passed on the way down and still have to come back to."),
        ("stack.append(current)", [
            ("current.left is not None",
             "Node {current.val} must wait: everything in its left subtree is smaller and comes first. "
             "Push it and keep going left."),
            (None,
             "Node {current.val} goes on the stack too, but it has nothing to its left — so it will be the "
             "next one to come off."),
        ]),
        ("current = stack.pop()",
         "There is nothing further to the left, so the node on top of the stack is the **next value in sorted "
         "order**: {current.val}. Take it off."),
        ("k -= 1", dict(
            post="Count it: {current.val} is the **{ordinal(len(counted))} smallest** value. "
                 "{'That is the one we want.' if k == 0 else 'Still ' + plural(k, 'value') + ' to go.'}",
            save={"counted": "counted + [current]"})),
        ("current = current.right", [
            ("current is not None",
             "The values that come after {was.current.val} are in its right subtree. Move to node {current.val} "
             "and again go left as far as possible."),
            (None,
             "Node {was.current.val} has no right subtree, so the next value in sorted order is the node "
             "waiting on top of the stack."),
        ]),
        ("return current.val", "k has reached 0, so the answer is **{_ret}**. The rest of the tree is never visited.",
         {"tree.good": "current"}),
    ],
    say={
        "def kthSmallest": (
            "The function we must write. It gets the top node and `k`, and returns the `k`-th "
            "smallest value."
        ),
        "stack = []": "The nodes we have passed on the way down and must come back to.",
        "current = root": "Start at the top.",
        "while stack or current": "Repeat while there is still somewhere to go.",
        "while current": "Keep going left for as long as there is a node.",
        "stack.append(current)": "Remember this node on the stack, to come back to it.",
        "current = current.left": "Step to the left child: smaller values come first.",
        "current = stack.pop()": (
            "No further left: the node on top of the stack holds the next smallest value."
        ),
        "k -= 1": "Count it: one fewer to go.",
        "if k == 0": "Was that the `k`-th one?",
        "return current.val": "Yes: return its value.",
        "current = current.right": (
            "No: the next values in order are in its right side, so go there."
        ),
    },
    time=("O(h + k)", "The walk first goes down the height h of the tree, then stops after k values instead of visiting all n nodes."),
    space=("O(h)", "The stack holds at most one node per level of the tree."),
    tests=[("root=T([3, 1, 4, None, 2]), k=1", 1), ("root=T([1]), k=1", 1),
           ("root=T([5, 3, 6, 2, 4, None, None, 1]), k=6", 6)],
)

lesson(
    "construct-binary-tree-from-preorder-and-inorder-traversal",
    pattern="Preorder gives the root, inorder splits left / right",
    statement="""`preorder` and `inorder` are the preorder and inorder traversals of the same binary
    tree (all values are different). Rebuild the tree and return its root.""",
    code="""
    class Solution:
        def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
            # Where does each value sit in inorder?  (so that no searching is needed)
            index_of = {value: i for i, value in enumerate(inorder)}
            next_root = 0  # position in preorder of the next root to use

            def build(left, right):
                # Builds the subtree whose values are inorder[left..right]
                nonlocal next_root
                if left > right:
                    return None

                root_val = preorder[next_root]
                next_root += 1
                root = TreeNode(root_val)
                root_index = index_of[root_val]

                root.left = build(left, root_index - 1)
                root.right = build(root_index + 1, right)

                return root

            return build(0, len(inorder) - 1)
    """,
    args="preorder=[3, 9, 20, 15, 7], inorder=[9, 3, 15, 20, 7]",
    expected=[3, 9, 20, None, None, 15, 7],
    why="3 is the root; 9 is everything to its left; 20 (with children 15 and 7) is its right subtree.",
    picture="""Picture two lists of the same family. One names every parent before their children (preorder);
    the other lists everyone from left to right (inorder). The next unused name in the preorder list
    is always the root of the part being built. Find that name in the inorder list: everyone to its
    left belongs to its left side, everyone to its right to its right side. Then build each side the
    same way.""",
    idea=[
        "**Preorder** visits a node *before* its subtrees, so its first value is always the root.",
        "**Inorder** visits the left subtree, then the node, then the right subtree. So once the root is located in `inorder`, everything left of it is the left subtree and everything right of it is the right subtree.",
        "Apply the same step to each side. Roots are taken from `preorder` one after another, which works because preorder lists the entire left subtree before the right one. A value → index map finds each root in `inorder` instantly, and a pair of indexes describes a part of `inorder` without copying it.",
    ],
    views=[
        Arr("preorder", title="preorder  (the arrow is on the next root)", ptrs={"next": "next_root"},
            tones={"seen": "range(next_root)"}),
        Arr("inorder", title="inorder  (the bracket is the part that belongs to this subtree)",
            rng=("left", "right", "this subtree")),
        Tree(title="tree being built", tones={"cur": "root"}),
    ],
    notes=[
        ("next_root = 0",
         "First note where every value sits in `inorder`: {index_of}. Finding a root there is then a single "
         "lookup instead of a search."),
        ("if left > right", dict(
            yes="This part of `inorder` is empty, so there is no subtree here: return None. "
                "(Every empty part ends this way.)",
            first=1)),
        ("root_val = preorder[next_root]",
         "Preorder lists a root before its subtrees, so the next unused preorder value is the root of this "
         "subtree: **{root_val}**."),
        ("root_index = index_of[root_val]", [
            ("left == right",
             "{root_val} sits at index {root_index} of `inorder` and is the only value in this subtree's part, "
             "so it has no children: it is a **leaf**."),
            (None,
             "{root_val} sits at index {root_index} of `inorder`. Within this subtree's part, everything to its left, "
             "{inorder[left:root_index] or 'nothing'}, is its **left subtree**; everything to its right, "
             "{inorder[root_index + 1:right + 1] or 'nothing'}, is its **right subtree**."),
         ],
         {"inorder.good": "root_index", "inorder.win": "range(left, root_index)",
          "inorder.mark": "range(root_index + 1, right + 1)"}),
        ("root.left = build(left, root_index - 1)", [
            ("root.left is not None", "The left part produced node {root.left.val}. Attach it as the left child of {root.val}."),
        ]),
        ("root.right = build(root_index + 1, right)", [
            ("root.right is not None", "The right part produced node {root.right.val}. Attach it as the right child of {root.val}."),
        ]),
    ],
    say={
        "def buildTree": (
            "The function we must write. It gets the two lists and returns the top node of the "
            "rebuilt tree."
        ),
        "index_of = {value: i for i, value in enumerate(inorder)}": (
            "A dictionary from each value to its position in `inorder`, so finding a value needs "
            "no searching."
        ),
        "next_root = 0": "The position in `preorder` of the next value to use as a root.",
        "def build(left, right)": (
            "A helper that builds the subtree made of `inorder[left]` to `inorder[right]` and "
            "returns its top node."
        ),
        "nonlocal next_root": (
            "Let the helper change `next_root`, which belongs to the outer function."
        ),
        "if left > right": "Is that range empty?",
        "return None": "Then there is no subtree here.",
        "root_val = preorder[next_root]": (
            "In preorder a parent comes before its children, so the next unused value is this "
            "subtree's root."
        ),
        "next_root += 1": "Mark it as used.",
        "root = TreeNode(root_val)": "Make the node.",
        "root_index = index_of[root_val]": (
            "Find where it sits in `inorder`. The values to its left form its left side; the "
            "values to its right, its right side."
        ),
        "root.left = build(left, root_index - 1)": (
            "Build the left side from the values to its left (the helper calls itself). This must"
            " come first, because in preorder the whole left side comes before the right."
        ),
        "root.right = build(root_index + 1, right)": (
            "Then build the right side from the values to its right."
        ),
        "return root": "This subtree is finished: return its top node.",
        "return build(0, len(inorder) - 1)": "Build the whole tree from all the values.",
    },
    time=("O(n)", "Every value becomes a node exactly once, and finding it in `inorder` is a single map lookup."),
    space=("O(n)", "The value → index map, plus a recursion as deep as the tree's height."),
    tests=[("preorder=[-1], inorder=[-1]", [-1]), ("preorder=[1, 2], inorder=[2, 1]", [1, 2]),
           ("preorder=[1, 2, 3], inorder=[1, 2, 3]", [1, None, 2, None, 3])],
)

lesson(
    "binary-tree-maximum-path-sum",
    pattern="Tree recursion: best single branch vs best bending path",
    statement="""A **path** is any chain of connected nodes in a binary tree (it need not pass through
    the root, and it may not visit a node twice). Return the largest possible sum of the values
    along a path.""",
    args="root=T([-10, 9, 20, None, None, 15, 7])",
    expected=42,
    why="The best path is 15 → 20 → 7, with sum 42. Going up through −10 would only lower it.",
    picture="""Picture each node as a town whose value you collect when you pass through; some values are
    negative. Any trip climbs up to a highest town and comes down again. Working from the bottom up,
    each town asks its two sides how much the best one-way trip down from them is worth, and ignores
    a side worth less than 0. A trip turning at this town collects its own value plus both sides.
    But a trip coming up from below can only use one side, because it cannot split in two.""",
    idea=[
        "Every path has one highest node where it *bends*: it may come up one branch, pass through the node, and go down the other branch.",
        "For each node compute the best sum of a **single branch** going downward from it. A branch with a negative sum is simply not taken (count it as 0).",
        "At each node, `left branch + node + right branch` is the best path bending there — compare it with the best so far. But to its parent a node can offer only **one** branch, because a path cannot fork.",
    ],
    views=[
        Tree(stack="node", ret_badges=("maxPathSumHelper", "node")),
        Vars(("self.max_sum", "self.max_sum"), "left_sum", "right_sum"),
    ],
    notes=[
        ("self.max_sum = float(",
         "`self.max_sum` keeps the best path found so far. The small labels that will appear beside nodes are "
         "the best **single branch** each node can offer its parent."),
        ("if not node", dict(yes="An empty spot adds nothing: 0.", first=1)),
        ("self.max_sum = max(self.max_sum, left_sum + right_sum + node.val)",
         "At node {node.val}: the best branch down-left is worth {left_sum} and down-right {right_sum} "
         "(a negative branch is dropped, counting as 0). The path bending here sums to "
         "{left_sum} + {node.val} + {right_sum} = **{left_sum + right_sum + node.val}**. Best so far: **{self.max_sum}**."),
        ("return max(left_sum, right_sum) + node.val",
         "A path cannot fork, so node {node.val} offers its parent only its better branch: "
         "max({left_sum}, {right_sum}) + {node.val} = **{_ret}**."),
        ("return self.max_sum", "The best path anywhere in the tree sums to **{_ret}**."),
    ],
    say={
        "def maxPathSum(self": (
            "The function we must write. It gets the top node and returns the biggest total of "
            "any path."
        ),
        "def maxPathSumHelper(node)": (
            "A helper that returns the best total of a path going *down* from `node` in one "
            "direction. On the way it also checks the path that turns at `node`."
        ),
        "if not node": "Is this an empty spot?",
        "return 0": "Then it adds nothing.",
        "left_sum = max(0, maxPathSumHelper(node.left))": (
            "The best one-way path down the left side, but never below 0: a side that would lower"
            " the total is simply not used."
        ),
        "right_sum = max(0, maxPathSumHelper(node.right))": "The same for the right side.",
        "self.max_sum = max(self.max_sum, left_sum + right_sum + node.val)": (
            "A path that turns here collects the left side, this node and the right side. Keep it"
            " if it is the best so far."
        ),
        "return max(left_sum, right_sum) + node.val": (
            "Going up to the parent, a path can use only one side: this node plus its better "
            "side."
        ),
        'self.max_sum = float("-inf")': (
            "The best total found so far. Minus infinity means none yet, since every real total "
            "is bigger."
        ),
        "maxPathSumHelper(root)": (
            "Visit the whole tree from the top; the helper records the best path."
        ),
        "return self.max_sum": "Return the best total found.",
    },
    time=("O(n)", "Every node is visited once."),
    space=("O(h)", "The recursion stack is as deep as the tree's height h."),
    tests=[("root=T([1, 2, 3])", 6), ("root=T([-3])", -3), ("root=T([2, -1])", 2)],
)

lesson(
    "serialize-and-deserialize-binary-tree",
    pattern="Preorder with markers for empty spots",
    statement="""Design `serialize`, which turns a binary tree into a string, and `deserialize`, which
    rebuilds exactly the same tree from that string.""",
    code="""
    class Codec:
        def serialize(self, root):
            parts = []

            def preorder(node):
                if not node:
                    parts.append("None")
                    return
                parts.append(str(node.val))
                preorder(node.left)
                preorder(node.right)

            preorder(root)
            return ",".join(parts)

        def deserialize(self, data):
            values = data.split(",")
            pos = 0  # index of the next token to read

            def build_tree():
                nonlocal pos
                value = values[pos]
                pos += 1
                if value == "None":
                    return None

                root = TreeNode(int(value))
                root.left = build_tree()
                root.right = build_tree()
                return root

            return build_tree()
    """,
    ops=["Codec()", "serialize(T([1, 2, 3, None, None, 4]))", "deserialize(_out[1])"],
    expected=[None, "1,2,None,None,3,4,None,None,None", [1, 2, 3, None, None, 4]],
    why="Writing None for every empty spot records the shape, so the string can be read back without guessing.",
    picture="""Picture writing a tree down as a list of instructions for rebuilding it, top first: each node's
    value, then its whole left side, then its whole right side, with *None* wherever a child is
    missing. Rebuilding just reads the list in the same order: each value makes a node, and a *None*
    says *nothing here, go back up*. Because the empty spots are written down too, the shape comes
    back exactly.""",
    idea=[
        "A plain list of values is not enough — many different trees contain the same values. The **shape** has to be stored too.",
        "Write the tree in preorder (node, then left subtree, then right subtree) and write `None` for every empty spot. With those markers the text describes exactly one tree.",
        "To rebuild, read the tokens in the same order: a value creates a node and is followed by its left subtree and then its right subtree; a `None` means *nothing here*.",
    ],
    views=[
        Tree(title="the original tree, and the rebuilt copy next to it",
             # while writing: the node being written; while reading: the node just created
             tones={"cur": lambda e: e._d.get("node") if "parts" in e else e._d.get("root") if "values" in e else None}),
        Arr(lambda e: e.values if "values" in e else e.parts, id="tokens",
            title="tokens  (written while serializing, read back while deserializing)",
            ptrs={"next": "pos"}, tones={"seen": "range(pos)", "cur": "len(parts) - 1"}),
    ],
    notes=[
        ('parts.append("None")', dict(
            post="An empty spot is written as `None` (every empty spot is). These markers are what make the "
                 "shape recoverable.",
            first=1)),
        ("parts.append(str(node.val))",
         "Node {node.val}: write its value first; everything from its left subtree follows, then its right subtree."),
        ('return ",".join(parts)', "Join the tokens with commas: the whole tree is now one string, `{_ret}`"),
        ('values = data.split(",")',
         "Split the text back into tokens. Reading them in the same order — node, left, right — rebuilds the same tree."),
        ("return None", dict(
            post="The next token is `None`: nothing goes in this spot.", first=3)),
        ("root = TreeNode(int(value))",
         "The next token is `{value}`: create that node. The tokens for its left subtree come next."),
        ("root.left = build_tree()", [
            ("root.left is not None", "Attach node {root.left.val} as the left child of {root.val}."),
        ]),
        ("root.right = build_tree()", [
            ("root.right is not None", "Attach node {root.right.val} as the right child of {root.val}."),
        ]),
    ],
    say={
        "class Codec": (
            "The problem asks for a class called `Codec` with two functions, `serialize` and "
            "`deserialize`."
        ),
        "def serialize": "The first function: turn the tree under `root` into one string.",
        "parts = []": "The pieces of the string, in order.",
        "def preorder(node)": (
            "A helper that writes a node, then its left side, then its right side."
        ),
        "if not node": "Is this an empty spot?",
        'parts.append("None")': "Write `None`, so the rebuild knows a child is missing here.",
        "return@1": "And go back up.",
        "parts.append(str(node.val))": "Write this node's value as text.",
        "preorder(node.left)": "Then write its whole left side (the helper calls itself).",
        "preorder(node.right)": "Then its whole right side.",
        "preorder(root)": "Write the whole tree, starting from the top.",
        'return ",".join(parts)': "Join the pieces with commas into one string.",
        "def deserialize": "The second function: turn such a string back into a tree.",
        'values = data.split(",")': "Cut the string at the commas, back into its pieces.",
        "pos = 0": "The position of the next piece to read.",
        "def build_tree()": (
            "A helper that reads the next pieces and builds the subtree they describe."
        ),
        "nonlocal pos": "Let the helper move `pos`, which belongs to the outer function.",
        "value = values[pos]": "Read the next piece.",
        "pos += 1": "Move past it.",
        'if value == "None"': "Is it `None`?",
        "return None": "Then there is no node here.",
        "root = TreeNode(int(value))": "Otherwise make a node holding that number.",
        "root.left = build_tree()": (
            "The pieces that follow describe its left side: build it (the helper calls itself)."
        ),
        "root.right = build_tree()": "Then the pieces after those describe its right side.",
        "return root": "This node and both its sides are rebuilt: return it.",
        "return build_tree()": "Rebuild the whole tree, starting from the first piece.",
    },
    time=("O(n)", "Each node (and each empty spot) is written once and read once; the tokens are joined in a single pass."),
    space=("O(n)", "The string and the token list are proportional to the size of the tree."),
    tests=[
        (["Codec()", "serialize(T([]))", "deserialize(_out[1])"], [None, "None", None]),
        (["Codec()", "serialize(T([1, None, 2]))", "deserialize(_out[1])"], [None, "1,None,2,None,None", [1, None, 2]]),
    ],
)

# end of c07_trees
