"""Checks: Linked List, Trees, Tries, Heap / Priority Queue."""

from __future__ import annotations

from collections import Counter, OrderedDict
from functools import lru_cache

from .kit import (
    LL,
    SKIP,
    TT,
    Ok,
    Raw,
    args,
    calls,
    check,
    clone,
    grid,
    height,
    inorder,
    ints,
    level,
    preorder,
    rand_bst,
    rand_tree,
    traceable,
    walk,
    word,
)

# -- Linked List ----------------------------------------------------------------


@check("reverse-linked-list")
def reverse_list(rng):
    vals = ints(rng, 0, 8, -9, 9)
    return args(head=LL(vals)), vals[::-1]


@check("merge-two-sorted-lists")
def merge_two_lists(rng):
    a, b = sorted(ints(rng, 0, 6, -9, 9)), sorted(ints(rng, 0, 6, -9, 9))
    return args(l1=LL(a), l2=LL(b)), sorted(a + b)


@check("reorder-list")
def reorder_list(rng):
    vals = ints(rng, 1, 9, 0, 20)
    want, i, j = [], 0, len(vals) - 1
    while i <= j:  # first, last, second, second-to-last, ...
        want.append(vals[i])
        if i != j:
            want.append(vals[j])
        i, j = i + 1, j - 1
    return args(head=LL(vals)), want


@check("remove-nth-node-from-end-of-list")
def remove_nth_from_end(rng):
    vals = ints(rng, 1, 8, 0, 20)
    n = rng.randint(1, len(vals))
    return args(head=LL(vals), n=n), vals[: len(vals) - n] + vals[len(vals) - n + 1 :]


@check("copy-list-with-random-pointer")
def copy_random_list(rng):
    n = rng.randint(0, 7)
    vals = rng.sample(range(1, 40), n)  # distinct, so a value identifies its node
    links = [rng.choice([None] + list(range(n))) for _ in range(n)]
    pairs = [[v, r] for v, r in zip(vals, links)]
    want = [[v, vals[r] if r is not None else None] for v, r in zip(vals, links)]
    return args(head=Raw(f"LR({pairs!r})")), want


@check("add-two-numbers")
def add_two_numbers(rng):
    a = rng.randint(0, 10 ** rng.randint(1, 6))
    b = rng.randint(0, 10 ** rng.randint(1, 6))
    digits = lambda x: [int(d) for d in str(x)[::-1]]  # noqa: E731 - lowest digit first
    return args(l1=LL(digits(a)), l2=LL(digits(b))), digits(a + b)


@check("linked-list-cycle")
def linked_list_cycle(rng):
    vals = ints(rng, 0, 7, -9, 9)
    pos = rng.randrange(len(vals)) if vals and rng.random() < 0.5 else None
    return args(head=LL(vals, pos)), pos is not None


@check("find-the-duplicate-number")
def find_duplicate(rng):
    n = rng.randint(1, 7)  # n + 1 numbers from 1..n, exactly one value repeated
    dup = rng.randint(1, n)
    extra = rng.randint(1, n)  # how many extra copies of the repeated value
    others = [v for v in range(1, n + 1) if v != dup]
    nums = [dup] * (extra + 1) + rng.sample(others, n - extra)
    rng.shuffle(nums)
    return args(nums=nums), dup


@check("lru-cache")
def lru_cache_design(rng):
    capacity = rng.randint(1, 3)
    ops, want = [f"LRUCache({capacity})"], [SKIP]
    ref: OrderedDict = OrderedDict()  # least recently used first
    for _ in range(rng.randint(1, 18)):
        key = rng.randint(1, 4)
        if rng.random() < 0.5:
            value = rng.randint(0, 99)
            if key in ref:
                ref.move_to_end(key)
            elif len(ref) >= capacity:
                ref.popitem(last=False)
            ref[key] = value
            ops.append(f"put({key}, {value})")
            want.append(SKIP)
        else:
            if key in ref:
                ref.move_to_end(key)
                want.append(ref[key])
            else:
                want.append(-1)
            ops.append(f"get({key})")
    return ops, calls(want)


@check("merge-k-sorted-lists")
def merge_k_lists(rng):
    lists = [sorted(ints(rng, 0, 4, -9, 9)) for _ in range(rng.randint(0, 4))]
    source = Raw("[" + ", ".join(f"L({vals!r})" for vals in lists) + "]")
    return args(lists=source), sorted(v for vals in lists for v in vals)


@check("reverse-nodes-in-k-group")
def reverse_k_group(rng):
    vals = ints(rng, 1, 9, 0, 20)
    k = rng.randint(1, len(vals))
    want = []
    for i in range(0, len(vals), k):
        chunk = vals[i : i + k]
        want += chunk[::-1] if len(chunk) == k else chunk
    return args(head=LL(vals), k=k), want


# -- Trees ----------------------------------------------------------------------


def _tree(rng, lo: int, hi: int, v_lo: int = -9, v_hi: int = 9):
    return rand_tree(rng, rng.randint(lo, hi), lambda: rng.randint(v_lo, v_hi))


def _graph(root):
    """The tree as an undirected graph: (nodes, adjacency lists by index)."""
    nodes = list(walk(root))
    index = {id(n): i for i, n in enumerate(nodes)}
    adj: list[list[int]] = [[] for _ in nodes]
    for node in nodes:
        for kid in (node[1], node[2]):
            if kid is not None:
                adj[index[id(node)]].append(index[id(kid)])
                adj[index[id(kid)]].append(index[id(node)])
    return nodes, adj


def _levels(root) -> list[list]:
    out, row = [], [root] if root else []
    while row:
        out.append([n[0] for n in row])
        row = [kid for n in row for kid in (n[1], n[2]) if kid is not None]
    return out


@check("invert-binary-tree")
def invert_tree(rng):
    t = _tree(rng, 0, 8)

    def mirror(node):
        return None if node is None else [node[0], mirror(node[2]), mirror(node[1])]

    return args(root=TT(level(t))), level(mirror(t))


@check("maximum-depth-of-binary-tree")
def max_depth(rng):
    t = _tree(rng, 0, 9)
    return args(root=TT(level(t))), height(t)


@check("diameter-of-binary-tree")
def diameter(rng):
    t = _tree(rng, 1, 9)
    nodes, adj = _graph(t)
    best = 0
    for start in range(len(nodes)):  # farthest node from every node
        dist = {start: 0}
        todo = [start]
        for cur in todo:
            for nxt in adj[cur]:
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    todo.append(nxt)
        best = max(best, max(dist.values()))
    return args(root=TT(level(t))), best


@check("balanced-binary-tree")
def balanced(rng):
    t = _tree(rng, 0, 9)
    return args(root=TT(level(t))), all(abs(height(n[1]) - height(n[2])) <= 1 for n in walk(t))


def _spoil(rng, t):
    """Change one random thing in a copy of the tree (a value, or drop a subtree)."""
    t = clone(t)
    nodes = list(walk(t))
    if not nodes:
        return [rng.randint(0, 3), None, None]
    node = rng.choice(nodes)
    if rng.random() < 0.5:
        node[0] += rng.choice([-1, 1])
    else:
        side = rng.choice([1, 2])
        node[side] = None if node[side] is not None else [rng.randint(0, 3), None, None]
    return t


@check("same-tree")
def same_tree(rng):
    p = _tree(rng, 0, 6, 0, 3)
    roll = rng.random()
    q = clone(p) if roll < 0.45 else _spoil(rng, p) if roll < 0.75 else _tree(rng, 0, 6, 0, 3)
    return args(p=TT(level(p)), q=TT(level(q))), p == q


@check("subtree-of-another-tree")
def subtree(rng):
    s = _tree(rng, 1, 8, 0, 2)
    roll = rng.random()
    if roll < 0.45:
        t = clone(rng.choice(list(walk(s))))
    elif roll < 0.7:
        t = _spoil(rng, rng.choice(list(walk(s))))
    else:
        t = _tree(rng, 1, 3, 0, 2)
    return args(s=TT(level(s)), t=TT(level(t))), any(node == t for node in walk(s))


@check("lowest-common-ancestor-of-a-binary-search-tree")
def lca_bst(rng):
    values = rng.sample(range(0, 40), rng.randint(2, 9))
    root = rand_bst(rng, values)
    a, b = rng.sample(values, 2)

    def path(v):
        out, node = [], root
        while node[0] != v:
            out.append(node[0])
            node = node[1] if v < node[0] else node[2]
        return out + [v]

    shared = [x for x, y in zip(path(a), path(b)) if x == y]
    call = args(root=TT(level(root)), p=Raw(f"find(root, {a})"), q=Raw(f"find(root, {b})"))
    return call, shared[-1]


@check("binary-tree-level-order-traversal")
def level_order(rng):
    t = _tree(rng, 0, 9)
    return args(root=TT(level(t))), _levels(t)


@check("binary-tree-right-side-view")
def right_side_view(rng):
    t = _tree(rng, 0, 9)
    return args(root=TT(level(t))), [row[-1] for row in _levels(t)]


@check("count-good-nodes-in-binary-tree")
def good_nodes(rng):
    t = _tree(rng, 1, 9, -3, 5)

    def count(node, above):
        if node is None:
            return 0
        good = all(a <= node[0] for a in above)
        return int(good) + count(node[1], above + [node[0]]) + count(node[2], above + [node[0]])

    return args(root=TT(level(t))), count(t, [])


@check("validate-binary-search-tree")
def validate_bst(rng):
    roll = rng.random()
    if roll < 0.4:
        t = rand_bst(rng, rng.sample(range(-20, 21), rng.randint(1, 8)))
    elif roll < 0.7:
        t = rand_bst(rng, rng.sample(range(-20, 21), rng.randint(1, 8)))
        rng.choice(list(walk(t)))[0] = rng.randint(-20, 20)  # one value changed: may break the order
    else:
        t = _tree(rng, 1, 7, 0, 9)
    flat = inorder(t)
    return args(root=TT(level(t))), all(a < b for a, b in zip(flat, flat[1:]))


@check("kth-smallest-element-in-a-bst")
def kth_smallest(rng):
    values = rng.sample(range(-20, 21), rng.randint(1, 9))
    k = rng.randint(1, len(values))
    return args(root=TT(level(rand_bst(rng, values))), k=k), sorted(values)[k - 1]


@check("construct-binary-tree-from-preorder-and-inorder-traversal")
def build_tree(rng):
    n = rng.randint(1, 8)
    pool = rng.sample(range(-20, 21), n)
    t = rand_tree(rng, n, pool.pop)
    return args(preorder=preorder(t), inorder=inorder(t)), level(t)


@check("binary-tree-maximum-path-sum")
def max_path_sum(rng):
    t = _tree(rng, 1, 8)
    nodes, adj = _graph(t)
    best = max(n[0] for n in nodes)

    def extend(cur, seen, total):  # every simple path, by brute force
        nonlocal best
        best = max(best, total)
        for nxt in adj[cur]:
            if nxt not in seen:
                extend(nxt, seen | {nxt}, total + nodes[nxt][0])

    for start in range(len(nodes)):
        extend(start, {start}, nodes[start][0])
    return args(root=TT(level(t))), best


@check("serialize-and-deserialize-binary-tree")
def serialize_tree(rng):
    t = _tree(rng, 0, 8, -9, 20)
    want = level(t)
    return ([f"Codec()", f"serialize(T({want!r}))", "deserialize(_out[1])"],
            Ok(lambda got: (got[2] or []) == want, f"deserialize(serialize(tree)) must rebuild {want}"))


# -- Tries ----------------------------------------------------------------------


@check("implement-trie-prefix-tree")
def trie(rng):
    ops, want, words = ["Trie()"], [SKIP], set()
    for _ in range(rng.randint(1, 16)):
        w = word(rng, 1, 4, "ab")
        kind = rng.choice(["insert", "search", "startsWith"])
        if kind == "insert":
            words.add(w)
            want.append(SKIP)
        elif kind == "search":
            want.append(w in words)
        else:
            want.append(any(x.startswith(w) for x in words))
        ops.append(f"{kind}({w!r})")
    return ops, calls(want)


@check("design-add-and-search-words-data-structure")
def word_dictionary(rng):
    ops, want, words = ["WordDictionary()"], [SKIP], set()
    for _ in range(rng.randint(1, 16)):
        if rng.random() < 0.45:
            w = word(rng, 1, 4, "ab")
            words.add(w)
            ops.append(f"addWord({w!r})")
            want.append(SKIP)
        else:
            pattern = word(rng, 1, 4, "ab.")
            hit = any(len(w) == len(pattern) and all(p in (".", ch) for p, ch in zip(pattern, w)) for w in words)
            ops.append(f"search({pattern!r})")
            want.append(hit)
    return ops, calls(want)


@check("word-search-ii", cases=120)
def word_search_ii(rng):
    board = grid(rng, 1, 3, 1, 3, lambda: rng.choice("abc"))
    words = sorted({word(rng, 1, 4, "abc") for _ in range(rng.randint(1, 6))})
    want = sorted(w for w in words if traceable(board, w))
    return args(board=board, words=words), Ok(lambda got: sorted(got) == want, f"expected {want} in any order")


# -- Heap / Priority Queue ------------------------------------------------------


@check("kth-largest-element-in-a-stream")
def kth_largest_stream(rng):
    k = rng.randint(1, 4)
    nums = ints(rng, k - 1, k + 4, -9, 9)  # at least k - 1 numbers, as LeetCode promises
    ops, want, seen = [f"KthLargest({k}, {nums!r})"], [SKIP], list(nums)
    for _ in range(rng.randint(1, 8)):
        v = rng.randint(-9, 9)
        seen.append(v)
        ops.append(f"add({v})")
        want.append(sorted(seen)[-k])
    return ops, calls(want)


@check("last-stone-weight")
def last_stone_weight(rng):
    stones = ints(rng, 1, 8, 1, 12)
    left = list(stones)
    while len(left) > 1:
        left.sort()
        heavy, light = left.pop(), left.pop()
        if heavy != light:
            left.append(heavy - light)
    return args(stones=stones), left[0] if left else 0


@check("k-closest-points-to-origin")
def k_closest(rng):
    points = [[rng.randint(-5, 5), rng.randint(-5, 5)] for _ in range(rng.randint(1, 8))]
    k = rng.randint(1, len(points))
    far = lambda p: p[0] ** 2 + p[1] ** 2  # noqa: E731
    best = sorted(far(p) for p in points)[:k]

    def judge(got):
        if len(got) != k:
            return f"expected {k} points"
        pool = Counter(tuple(p) for p in points)
        for p in got:
            if pool[tuple(p)] <= 0:
                return f"{p} is not one of the points (or is used too often)"
            pool[tuple(p)] -= 1
        return sorted(far(p) for p in got) == best or "these are not the k closest points"

    return args(points=points, k=k), Ok(judge)


@check("kth-largest-element-in-an-array")
def kth_largest_array(rng):
    nums = ints(rng, 1, 10, -9, 9)
    k = rng.randint(1, len(nums))
    return args(nums=nums, k=k), sorted(nums)[-k]


def _fewest_slots(counts: tuple, gap: int) -> int:
    """Exhaustive search: at every slot run any task that is allowed, or idle."""

    @lru_cache(maxsize=None)
    def best(left: tuple, wait: tuple) -> int:
        if not any(left):
            return 0
        cooled = tuple(max(0, w - 1) for w in wait)
        options = []
        for i, n in enumerate(left):
            if n and wait[i] == 0:
                after = tuple(x - 1 if j == i else x for j, x in enumerate(left))
                options.append(1 + best(after, tuple(gap if j == i else w for j, w in enumerate(cooled))))
        if any(wait):  # idling changes the state only while something is cooling down
            options.append(1 + best(left, cooled))
        return min(options)

    return best(counts, (0,) * len(counts))


@check("task-scheduler", cases=120)
def task_scheduler(rng):
    tasks = [rng.choice("ABC") for _ in range(rng.randint(1, 7))]
    n = rng.randint(0, 3)
    counts = tuple(tasks.count(ch) for ch in "ABC")
    return args(tasks=tasks, n=n), _fewest_slots(counts, n)


@check("design-twitter")
def twitter(rng):
    ops, want = ["Twitter()"], [SKIP]
    tweets: list[tuple[int, int]] = []  # (author, tweet id), oldest first
    follows: set[tuple[int, int]] = set()
    tweet_id = 100
    for _ in range(rng.randint(1, 30)):
        kind = rng.choice(["post", "post", "post", "feed", "feed", "follow", "unfollow"])
        user = rng.randint(1, 3)
        if kind == "post":
            tweet_id += 1
            tweets.append((user, tweet_id))
            ops.append(f"postTweet({user}, {tweet_id})")
            want.append(SKIP)
        elif kind == "feed":
            visible = [t for author, t in tweets if author == user or (user, author) in follows]
            ops.append(f"getNewsFeed({user})")
            want.append(visible[::-1][:10])
        else:
            other = rng.choice([u for u in (1, 2, 3) if u != user])
            if kind == "follow":
                follows.add((user, other))
            else:
                follows.discard((user, other))
            ops.append(f"{kind}({user}, {other})")
            want.append(SKIP)
    return ops, calls(want)


@check("find-median-from-data-stream")
def median_finder(rng):
    ops, want, data = ["MedianFinder()"], [SKIP], []
    for _ in range(rng.randint(1, 16)):
        if not data or rng.random() < 0.6:
            v = rng.randint(-20, 20)
            data.append(v)
            ops.append(f"addNum({v})")
            want.append(SKIP)
        else:
            s = sorted(data)
            n = len(s)
            ops.append("findMedian()")
            want.append(float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)
    return ops, calls(want)
