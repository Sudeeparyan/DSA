"""Checks: Backtracking, Graphs, Advanced Graphs."""

from __future__ import annotations

from itertools import combinations, permutations, product

from .kit import Ok, Raw, args, check, grid, ints, neighbours, reachable, regions, same_sets, traceable, word

INF = 2147483647

# -- Backtracking ---------------------------------------------------------------


@check("subsets")
def subsets(rng):
    nums = rng.sample(range(-9, 10), rng.randint(1, 6))
    want = [c for r in range(len(nums) + 1) for c in combinations(nums, r)]
    return args(nums=nums), Ok(lambda got: same_sets(got, want))


@check("combination-sum")
def combination_sum(rng):
    candidates = rng.sample(range(2, 9), rng.randint(1, 4))
    target = rng.randint(1, 12)
    want = set()
    for counts in product(*[range(target // c + 1) for c in candidates]):  # how often each candidate is used
        if sum(n * c for n, c in zip(counts, candidates)) == target:
            want.add(tuple(sorted(c for n, c in zip(counts, candidates) for _ in range(n))))
    return args(candidates=candidates, target=target), Ok(lambda got: same_sets(got, want))


@check("permutations")
def permutations_check(rng):
    nums = rng.sample(range(-9, 10), rng.randint(1, 5))
    want = sorted(permutations(nums))
    return args(nums=nums), Ok(lambda got: sorted(tuple(p) for p in got) == want,
                               f"expected each of the {len(want)} orderings exactly once")


@check("subsets-ii")
def subsets_with_dup(rng):
    nums = ints(rng, 1, 6, 0, 3)
    n = len(nums)
    want = {tuple(sorted(nums[i] for i in idx)) for r in range(n + 1) for idx in combinations(range(n), r)}
    return args(nums=nums), Ok(lambda got: same_sets(got, want))


@check("combination-sum-ii")
def combination_sum_ii(rng):
    candidates = ints(rng, 1, 7, 1, 6)
    target = rng.randint(1, 12)
    n = len(candidates)
    want = {tuple(sorted(candidates[i] for i in idx))
            for r in range(1, n + 1) for idx in combinations(range(n), r)
            if sum(candidates[i] for i in idx) == target}
    return args(candidates=candidates, target=target), Ok(lambda got: same_sets(got, want))


@check("word-search")
def word_search(rng):
    board = grid(rng, 1, 3, 1, 4, lambda: rng.choice("ab"))
    text = word(rng, 1, 6, "ab")
    return args(board=board, word=text), traceable(board, text)


@check("palindrome-partitioning")
def palindrome_partitioning(rng):
    s = word(rng, 1, 7, "ab")
    n = len(s)
    want = []
    for mask in range(1 << (n - 1)):  # every way to place cuts between the letters
        parts, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(s[start : i + 1])
                start = i + 1
        parts.append(s[start:])
        if all(p == p[::-1] for p in parts):
            want.append(tuple(parts))
    return args(s=s), Ok(lambda got: sorted(tuple(p) for p in got) == sorted(want),
                         f"expected the {len(want)} palindrome partitions")


KEYS = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


@check("letter-combinations-of-a-phone-number", cases=80)
def letter_combinations(rng):
    digits = word(rng, 0, 3, "23456789")
    want = sorted("".join(p) for p in product(*[KEYS[d] for d in digits])) if digits else []
    return args(digits=digits), Ok(lambda got: sorted(got) == want, f"expected {len(want)} combinations")


@check("n-queens", cases=12)
def n_queens(rng):
    n = rng.randint(1, 6)
    want = []
    for cols in permutations(range(n)):  # one queen per row and per column
        if all(abs(cols[a] - cols[b]) != b - a for a, b in combinations(range(n), 2)):
            want.append(tuple("." * c + "Q" + "." * (n - 1 - c) for c in cols))
    return args(n=n), Ok(lambda got: sorted(tuple(b) for b in got) == sorted(want),
                         f"expected the {len(want)} solutions")


# -- Graphs ---------------------------------------------------------------------


@check("number-of-islands")
def number_of_islands(rng):
    g = grid(rng, 1, 4, 1, 5, lambda: rng.choice("01"))
    land = {(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == "1"}
    return args(grid=g), len(regions(land))


@check("clone-graph")
def clone_graph(rng):
    n = rng.randint(0, 6)
    edges = set()
    for node in range(2, n + 1):  # a random connected graph: a tree plus a few extra edges
        edges.add((rng.randint(1, node - 1), node))
    for a, b in combinations(range(1, n + 1), 2):
        if rng.random() < 0.25:
            edges.add((a, b))
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b)
        adj[b - 1].append(a)
    for row in adj:
        rng.shuffle(row)
    return args(node=Raw(f"G({adj!r})")), adj


@check("max-area-of-island")
def max_area_of_island(rng):
    g = grid(rng, 1, 4, 1, 5, lambda: rng.randint(0, 1))
    land = {(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 1}
    return args(grid=g), max([0] + [len(group) for group in regions(land)])


@check("pacific-atlantic-water-flow")
def pacific_atlantic(rng):
    h = grid(rng, 1, 4, 1, 4, lambda: rng.randint(0, 5))
    rows, cols = len(h), len(h[0])

    def flows_to(start):  # every cell the water from `start` can run to
        seen, todo = {start}, [start]
        while todo:
            r, c = todo.pop()
            for nr, nc in neighbours(r, c, rows, cols):
                if (nr, nc) not in seen and h[nr][nc] <= h[r][c]:
                    seen.add((nr, nc))
                    todo.append((nr, nc))
        return seen

    want = []
    for r in range(rows):
        for c in range(cols):
            wet = flows_to((r, c))
            pacific = any(x == 0 or y == 0 for x, y in wet)
            atlantic = any(x == rows - 1 or y == cols - 1 for x, y in wet)
            if pacific and atlantic:
                want.append([r, c])
    return args(heights=h), want


@check("surrounded-regions")
def surrounded_regions(rng):
    board = grid(rng, 1, 5, 1, 5, lambda: rng.choice("XO"))
    rows, cols = len(board), len(board[0])
    want = [row[:] for row in board]
    for group in regions({(r, c) for r in range(rows) for c in range(cols) if board[r][c] == "O"}):
        if not any(r in (0, rows - 1) or c in (0, cols - 1) for r, c in group):
            for r, c in group:
                want[r][c] = "X"
    return args(board=board), want


@check("rotting-oranges")
def rotting_oranges(rng):
    g = grid(rng, 1, 4, 1, 4, lambda: rng.choice([0, 1, 1, 2]))
    rows, cols = len(g), len(g[0])
    now = [row[:] for row in g]
    minutes = 0
    while True:  # simulate minute by minute
        rot = [(r, c) for r in range(rows) for c in range(cols)
               if now[r][c] == 1 and any(now[nr][nc] == 2 for nr, nc in neighbours(r, c, rows, cols))]
        if not rot:
            break
        for r, c in rot:
            now[r][c] = 2
        minutes += 1
    return args(grid=g), -1 if any(1 in row for row in now) else minutes


@check("walls-and-gates")
def walls_and_gates(rng):
    rooms = grid(rng, 1, 4, 1, 4, lambda: rng.choice([INF, INF, INF, -1, 0]))
    rows, cols = len(rooms), len(rooms[0])
    want = [row[:] for row in rooms]
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] != INF:
                continue
            dist, todo = {(r, c): 0}, [(r, c)]  # a separate search from every room
            for cur in todo:
                if rooms[cur[0]][cur[1]] == 0:
                    want[r][c] = dist[cur]
                    break
                for nxt in neighbours(cur[0], cur[1], rows, cols):
                    if nxt not in dist and rooms[nxt[0]][nxt[1]] != -1:
                        dist[nxt] = dist[cur] + 1
                        todo.append(nxt)
    return args(rooms=rooms), want


def _course_order_exists(n: int, pairs) -> bool:
    for order in permutations(range(n)):
        pos = {course: i for i, course in enumerate(order)}
        if all(pos[b] < pos[a] for a, b in pairs):
            return True
    return False


def _prerequisites(rng, n: int, loops: bool) -> list[list[int]]:
    every = [(a, b) for a in range(n) for b in range(n) if a != b or loops]
    return [list(p) for p in rng.sample(every, min(len(every), rng.randint(0, 7)))]


@check("course-schedule", cases=100)
def course_schedule(rng):
    n = rng.randint(1, 6)
    pairs = _prerequisites(rng, n, loops=rng.random() < 0.1)
    return args(numCourses=n, prerequisites=pairs), _course_order_exists(n, pairs)


@check("course-schedule-ii", cases=100)
def course_schedule_ii(rng):
    n = rng.randint(1, 6)
    pairs = _prerequisites(rng, n, loops=False)
    possible = _course_order_exists(n, pairs)

    def judge(got):
        if not possible:
            return got == [] or "the courses contain a cycle, expected []"
        if sorted(got) != list(range(n)):
            return "the answer must list every course exactly once"
        pos = {course: i for i, course in enumerate(got)}
        return all(pos[b] < pos[a] for a, b in pairs) or "a course is listed before one of its prerequisites"

    return args(numCourses=n, prerequisites=pairs), Ok(judge)


@check("redundant-connection")
def redundant_connection(rng):
    n = rng.randint(3, 7)
    edges = [[rng.randint(1, node - 1), node] for node in range(2, n + 1)]  # a tree
    spare = [[a, b] for a, b in combinations(range(1, n + 1), 2) if [a, b] not in edges]
    edges.append(rng.choice(spare))  # plus one extra edge
    rng.shuffle(edges)
    want = None
    for i in range(len(edges) - 1, -1, -1):  # the last edge whose removal keeps everything connected
        rest = edges[:i] + edges[i + 1 :]
        if len(reachable(1, rest)) == n:
            want = edges[i]
            break
    return args(edges=edges), want


@check("number-of-connected-components-in-an-undirected-graph")
def count_components(rng):
    n = rng.randint(1, 7)
    edges = [[a, b] for a, b in combinations(range(n), 2) if rng.random() < 0.25]
    rng.shuffle(edges)
    groups = {frozenset(reachable(node, edges)) for node in range(n)}
    return args(n=n, edges=edges), len(groups)


@check("graph-valid-tree")
def valid_tree(rng):
    n = rng.randint(1, 6)
    if rng.random() < 0.5:
        edges = [[rng.randint(0, node - 1), node] for node in range(1, n)]  # a tree ...
        spare = [[a, b] for a, b in combinations(range(n), 2) if [a, b] not in edges]
        roll = rng.random()
        if roll < 0.25 and edges:
            edges.pop(rng.randrange(len(edges)))  # ... with an edge missing
        elif roll < 0.5 and spare:
            edges.append(rng.choice(spare))  # ... or with one too many
    else:
        edges = [[a, b] for a, b in combinations(range(n), 2) if rng.random() < 0.3]
    rng.shuffle(edges)
    return args(n=n, edges=edges), len(edges) == n - 1 and len(reachable(0, edges)) == n


@check("word-ladder")
def word_ladder(rng):
    every = ["".join(p) for p in product("abc", repeat=3)]
    begin = rng.choice(every)
    words = rng.sample(every, rng.randint(1, 12))
    end = rng.choice(words) if rng.random() < 0.85 else rng.choice(every)
    if end == begin:
        end = next(w for w in every if w != begin)
    want = 0
    if end in words:
        dist, todo = {begin: 1}, [begin]
        for cur in todo:
            for nxt in words:
                if nxt not in dist and sum(a != b for a, b in zip(cur, nxt)) == 1:
                    dist[nxt] = dist[cur] + 1
                    todo.append(nxt)
        want = dist.get(end, 0)
    return args(beginWord=begin, endWord=end, wordList=words), want


# -- Advanced Graphs ------------------------------------------------------------


@check("reconstruct-itinerary", cases=120)
def reconstruct_itinerary(rng):
    airports = ["JFK", "AAA", "BBB", "CCC"]
    here, tickets = "JFK", []
    for _ in range(rng.randint(1, 7)):  # a random trip guarantees that an itinerary exists
        there = rng.choice([a for a in airports if a != here])
        tickets.append([here, there])
        here = there
    rng.shuffle(tickets)

    def search(path, left):  # smallest destination first, so the first full trip found is the smallest
        if not left:
            return path
        for there in sorted({b for a, b in left if a == path[-1]}):
            i = left.index([path[-1], there])
            found = search(path + [there], left[:i] + left[i + 1 :])
            if found:
                return found
        return None

    return args(tickets=tickets), search(["JFK"], tickets)


@check("min-cost-to-connect-all-points", cases=100)
def min_cost_connect(rng):
    cells = [(x, y) for x in range(-5, 6) for y in range(-5, 6)]
    points = [list(p) for p in rng.sample(cells, rng.randint(1, 6))]
    n = len(points)
    links = [(abs(points[a][0] - points[b][0]) + abs(points[a][1] - points[b][1]), a, b)
             for a, b in combinations(range(n), 2)]
    best = 0 if n == 1 else None
    for chosen in combinations(links, n - 1):  # every set of n - 1 links that connects everything
        if n > 1 and len(reachable(0, [(a, b) for _, a, b in chosen])) == n:
            cost = sum(d for d, _, _ in chosen)
            best = cost if best is None else min(best, cost)
    return args(points=points), best


@check("network-delay-time")
def network_delay(rng):
    n = rng.randint(1, 6)
    pairs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a != b]
    times = [[a, b, rng.randint(1, 9)] for a, b in rng.sample(pairs, min(len(pairs), rng.randint(0, 9)))]
    k = rng.randint(1, n)
    far = float("inf")
    dist = {(a, b): 0 if a == b else far for a in range(1, n + 1) for b in range(1, n + 1)}
    for a, b, w in times:
        dist[a, b] = w
    for mid in range(1, n + 1):  # Floyd-Warshall
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                dist[a, b] = min(dist[a, b], dist[a, mid] + dist[mid, b])
    slowest = max(dist[k, node] for node in range(1, n + 1))
    return args(times=times, n=n, k=k), -1 if slowest == far else slowest


@check("swim-in-rising-water")
def swim_in_water(rng):
    n = rng.randint(1, 4)
    values = list(range(n * n))
    rng.shuffle(values)
    g = [values[r * n : (r + 1) * n] for r in range(n)]
    for level in range(n * n):  # raise the water until the far corner can be reached
        if g[0][0] > level:
            continue
        seen, todo = {(0, 0)}, [(0, 0)]
        while todo:
            r, c = todo.pop()
            for nr, nc in neighbours(r, c, n, n):
                if (nr, nc) not in seen and g[nr][nc] <= level:
                    seen.add((nr, nc))
                    todo.append((nr, nc))
        if (n - 1, n - 1) in seen:
            return args(grid=g), level
    raise AssertionError("unreachable")


@check("alien-dictionary")
def alien_dictionary(rng):
    letters = "abcd"
    words = [word(rng, 1, 3, letters) for _ in range(rng.randint(1, 5))]
    if rng.random() < 0.65:  # usually a list that really is sorted by some hidden alphabet
        hidden = rng.sample(letters, len(letters))
        words.sort(key=lambda w: [hidden.index(ch) for ch in w])
    used = sorted(set("".join(words)))
    rules, broken = set(), False
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                rules.add((x, y))
                break
        else:
            broken = broken or len(a) > len(b)  # a word listed before its own prefix

    def fits(order) -> bool:
        pos = {ch: i for i, ch in enumerate(order)}
        return all(pos[x] < pos[y] for x, y in rules)

    possible = not broken and any(fits(order) for order in permutations(used))

    def judge(got):
        if not possible:
            return got == "" or 'the list is contradictory, expected ""'
        if sorted(got) != used:
            return f"the answer must contain exactly the letters {used}"
        return fits(got) or "the order breaks one of the rules given by neighbouring words"

    return args(words=words), Ok(judge)


@check("cheapest-flights-within-k-stops")
def cheapest_flights(rng):
    n = rng.randint(2, 6)
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    flights = [[a, b, rng.randint(1, 20)] for a, b in rng.sample(pairs, min(len(pairs), rng.randint(0, 10)))]
    src, dst = rng.sample(range(n), 2)
    k = rng.randint(0, 4)
    best = [float("inf")]

    def fly(city, cost, flights_left):  # every route with at most k + 1 flights
        if city == dst:
            best[0] = min(best[0], cost)
            return
        if flights_left == 0:
            return
        for a, b, price in flights:
            if a == city:
                fly(b, cost + price, flights_left - 1)

    fly(src, 0, k + 1)
    return args(n=n, flights=flights, src=src, dst=dst, k=k), -1 if best[0] == float("inf") else best[0]
