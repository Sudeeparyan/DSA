"""Checks: 1-D DP, 2-D DP, Greedy, Intervals, Math & Geometry, Bit Manipulation."""

from __future__ import annotations

import re
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb

from .kit import SKIP, Ok, args, calls, check, grid, ints, neighbours, word

# -- 1-D Dynamic Programming ------------------------------------------------------


@check("climbing-stairs", cases=40)
def climbing_stairs(rng):
    n = rng.randint(1, 30)
    # choose how many double steps (k); the n - k moves can then be arranged in C(n - k, k) ways
    return args(n=n), sum(comb(n - k, k) for k in range(n // 2 + 1))


@check("min-cost-climbing-stairs")
def min_cost_climbing_stairs(rng):
    cost = ints(rng, 2, 10, 0, 20)
    n = len(cost)
    # a route is a choice of stairs to step on that never skips two stairs in a row
    want = min(sum(c for c, on in zip(cost, pick) if on)
               for pick in product([0, 1], repeat=n)
               if all(pick[i] or pick[i + 1] for i in range(n - 1)))
    return args(cost=cost), want


@check("house-robber")
def house_robber(rng):
    nums = ints(rng, 1, 10, 0, 20)
    n = len(nums)
    want = max(sum(v for v, on in zip(nums, pick) if on)
               for pick in product([0, 1], repeat=n)
               if not any(pick[i] and pick[i + 1] for i in range(n - 1)))
    return args(nums=nums), want


@check("house-robber-ii")
def house_robber_ii(rng):
    nums = ints(rng, 1, 10, 0, 20)
    n = len(nums)
    want = max(sum(v for v, on in zip(nums, pick) if on)
               for pick in product([0, 1], repeat=n)
               if not any(pick[i] and pick[(i + 1) % n] for i in range(n) if n > 1))
    return args(nums=nums), want


@check("longest-palindromic-substring")
def longest_palindrome(rng):
    s = word(rng, 1, 9, "abc")
    best = max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return args(s=s), Ok(lambda got: (len(got) == best and got in s and got == got[::-1])
                         or f"expected a palindromic substring of length {best}")


@check("palindromic-substrings")
def palindromic_substrings(rng):
    s = word(rng, 0, 9, "ab")
    want = sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return args(s=s), want


@check("decode-ways")
def decode_ways(rng):
    s = word(rng, 1, 8, "01122367890")

    def count(rest: str) -> int:
        if rest == "":
            return 1
        total = 0
        if rest[0] != "0":
            total += count(rest[1:])
            if len(rest) >= 2 and int(rest[:2]) <= 26:
                total += count(rest[2:])
        return total

    return args(s=s), count(s)


@check("coin-change")
def coin_change(rng):
    coins = rng.sample(range(1, 9), rng.randint(1, 3))
    amount = rng.randint(0, 20)
    frontier, seen, used, want = {0}, {0}, 0, -1
    while frontier:  # breadth-first over the amounts reachable with `used` coins
        if amount in frontier:
            want = used
            break
        frontier = {a + c for a in frontier for c in coins if a + c <= amount} - seen
        seen |= frontier
        used += 1
    return args(coins=coins, amount=amount), want


@check("maximum-product-subarray")
def max_product(rng):
    nums = ints(rng, 1, 8, -4, 4)
    best = None
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = p if best is None else max(best, p)
    return args(nums=nums), best


@check("word-break")
def word_break(rng):
    s = word(rng, 1, 8, "ab")
    words = sorted({word(rng, 1, 3, "ab") for _ in range(rng.randint(1, 4))})

    @lru_cache(maxsize=None)
    def can(i: int) -> bool:
        return i == len(s) or any(s.startswith(w, i) and can(i + len(w)) for w in words)

    return args(s=s, wordDict=words), can(0)


@check("longest-increasing-subsequence")
def lis(rng):
    nums = ints(rng, 0, 9, -5, 9)
    want = 0
    for size in range(len(nums), 0, -1):
        if any(all(a < b for a, b in zip(c, c[1:])) for c in combinations(nums, size)):
            want = size
            break
    return args(nums=nums), want


@check("partition-equal-subset-sum")
def partition_equal(rng):
    nums = ints(rng, 1, 9, 1, 9)
    total = sum(nums)
    want = total % 2 == 0 and any(sum(c) * 2 == total for r in range(len(nums) + 1) for c in combinations(nums, r))
    return args(nums=nums), want


# -- 2-D Dynamic Programming ------------------------------------------------------


@check("unique-paths", cases=60)
def unique_paths(rng):
    m, n = rng.randint(1, 9), rng.randint(1, 9)
    return args(m=m, n=n), comb(m + n - 2, m - 1)


def _is_subsequence(small, big) -> bool:
    it = iter(big)
    return all(ch in it for ch in small)


@check("longest-common-subsequence")
def lcs(rng):
    a, b = word(rng, 1, 7), word(rng, 1, 7)
    want = 0
    for size in range(len(a), 0, -1):
        if any(_is_subsequence(c, b) for c in combinations(a, size)):
            want = size
            break
    return args(text1=a, text2=b), want


@check("best-time-to-buy-and-sell-stock-with-cooldown", cases=80)
def cooldown(rng):
    prices = ints(rng, 1, 8, 0, 9)
    best = 0
    for plan in product("-BS", repeat=len(prices)):  # every day: rest, buy or sell
        holding, cooling, profit, legal = False, False, 0, True
        for action, price in zip(plan, prices):
            if action == "B":
                if holding or cooling:
                    legal = False
                    break
                holding, profit = True, profit - price
                cooling = False
            elif action == "S":
                if not holding:
                    legal = False
                    break
                holding, profit, cooling = False, profit + price, True
            else:
                cooling = False
        if legal and not holding:
            best = max(best, profit)
    return args(prices=prices), best


@check("coin-change-ii")
def coin_change_ii(rng):
    coins = rng.sample(range(1, 8), rng.randint(1, 4))
    amount = rng.randint(0, 12)
    want = sum(1 for counts in product(*[range(amount // c + 1) for c in coins])
               if sum(n * c for n, c in zip(counts, coins)) == amount)
    return args(amount=amount, coins=coins), want


@check("target-sum")
def target_sum(rng):
    nums = ints(rng, 1, 8, 0, 5)
    target = rng.randint(-12, 12)
    want = sum(1 for signs in product([1, -1], repeat=len(nums)) if sum(s * v for s, v in zip(signs, nums)) == target)
    return args(nums=nums, S=target), want


@check("interleaving-string")
def interleave(rng):
    s1, s2 = word(rng, 0, 4, "ab"), word(rng, 0, 4, "ab")
    roll = rng.random()
    if roll < 0.55:  # a genuine interleaving ...
        a, b, mixed = list(s1), list(s2), []
        while a or b:
            source = a if (a and (not b or rng.random() < 0.5)) else b
            mixed.append(source.pop(0))
        s3 = "".join(mixed)
        if roll < 0.15 and s3:  # ... sometimes with one letter changed
            i = rng.randrange(len(s3))
            s3 = s3[:i] + ("a" if s3[i] == "b" else "b") + s3[i + 1 :]
    else:
        s3 = word(rng, max(0, len(s1) + len(s2) - 1), len(s1) + len(s2) + 1, "ab")

    @lru_cache(maxsize=None)
    def can(i: int, j: int) -> bool:
        k = i + j
        if k == len(s3):
            return True
        return (i < len(s1) and s1[i] == s3[k] and can(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and can(i, j + 1))

    return args(s1=s1, s2=s2, s3=s3), len(s1) + len(s2) == len(s3) and can(0, 0)


@check("longest-increasing-path-in-a-matrix")
def longest_increasing_path(rng):
    m = grid(rng, 1, 3, 1, 4, lambda: rng.randint(0, 6))
    rows, cols = len(m), len(m[0])

    def longest(r, c) -> int:  # no memo: plain exhaustive search
        return 1 + max([longest(nr, nc) for nr, nc in neighbours(r, c, rows, cols) if m[nr][nc] > m[r][c]] or [0])

    return args(matrix=m), max(longest(r, c) for r in range(rows) for c in range(cols))


@check("distinct-subsequences")
def distinct_subsequences(rng):
    s, t = word(rng, 0, 8, "ab"), word(rng, 0, 4, "ab")
    want = sum(1 for idx in combinations(range(len(s)), len(t)) if all(s[i] == ch for i, ch in zip(idx, t)))
    return args(s=s, t=t), want


@check("edit-distance", cases=100)
def edit_distance(rng):
    a, b = word(rng, 0, 5), word(rng, 0, 5)
    longest = max(len(a), len(b))
    dist, todo = {a: 0}, [a]
    for cur in todo:  # shortest path through "one edit apart" strings
        if cur == b:
            break
        nearby = set()
        for i in range(len(cur) + 1):
            if i < len(cur):
                nearby.add(cur[:i] + cur[i + 1 :])  # delete
                nearby.update(cur[:i] + ch + cur[i + 1 :] for ch in "abc")  # replace
            if len(cur) < longest:
                nearby.update(cur[:i] + ch + cur[i:] for ch in "abc")  # insert
        for nxt in nearby:
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                todo.append(nxt)
    return args(word1=a, word2=b), dist[b]


@check("burst-balloons", cases=60)
def burst_balloons(rng):
    nums = ints(rng, 1, 6, 0, 7)
    best = 0
    for order in permutations(range(len(nums))):  # every order of bursting
        left, coins = list(range(len(nums))), 0
        for i in order:
            at = left.index(i)
            before = nums[left[at - 1]] if at > 0 else 1
            after = nums[left[at + 1]] if at + 1 < len(left) else 1
            coins += before * nums[i] * after
            left.pop(at)
        best = max(best, coins)
    return args(nums=nums), best


@check("regular-expression-matching", cases=300)
def regex_matching(rng):
    s = word(rng, 1, 5, "ab")
    p = "".join(rng.choice("ab.") + ("*" if rng.random() < 0.4 else "") for _ in range(rng.randint(1, 4)))
    return args(s=s, p=p), re.fullmatch(p, s) is not None


# -- Greedy ---------------------------------------------------------------------


@check("maximum-subarray")
def max_subarray(rng):
    nums = ints(rng, 1, 9, -6, 6)
    want = max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))
    return args(nums=nums), want


def _jumps(nums) -> dict[int, int]:
    """Fewest jumps to every index that can be reached (breadth-first)."""
    dist, todo = {0: 0}, [0]
    for i in todo:
        for j in range(i + 1, min(len(nums), i + nums[i] + 1)):
            if j not in dist:
                dist[j] = dist[i] + 1
                todo.append(j)
    return dist


@check("jump-game")
def jump_game(rng):
    nums = ints(rng, 1, 9, 0, 3)
    return args(nums=nums), len(nums) - 1 in _jumps(nums)


@check("jump-game-ii")
def jump_game_ii(rng):
    while True:  # the last index is promised to be reachable
        nums = ints(rng, 1, 9, 0, 4)
        dist = _jumps(nums)
        if len(nums) - 1 in dist:
            return args(nums=nums), dist[len(nums) - 1]


@check("gas-station")
def gas_station(rng):
    n = rng.randint(1, 6)
    gas, cost = [rng.randint(0, 6) for _ in range(n)], [rng.randint(0, 6) for _ in range(n)]

    def works(start: int) -> bool:
        tank = 0
        for i in range(n):
            j = (start + i) % n
            tank += gas[j] - cost[j]
            if tank < 0:
                return False
        return True

    starts = [s for s in range(n) if works(s)]

    def judge(got):
        if not starts:
            return got == -1 or "no start works, expected -1"
        return got in starts or f"expected one of the working starts {starts}"

    return args(gas=gas, cost=cost), Ok(judge)


@check("hand-of-straights")
def hand_of_straights(rng):
    size = rng.randint(1, 4)
    if rng.random() < 0.55:  # usually a hand that really consists of runs
        hand = [start + i for start in ints(rng, 1, 3, 0, 6) for i in range(size)]
        if rng.random() < 0.25:
            hand[rng.randrange(len(hand))] += 1
    else:
        hand = ints(rng, 1, 9, 0, 6)
    rng.shuffle(hand)
    cards = sorted(hand)
    ok = len(cards) % size == 0
    while ok and cards:  # the smallest card left must start a run
        first = cards[0]
        for v in range(first, first + size):
            if v in cards:
                cards.remove(v)
            else:
                ok = False
                break
    return args(hand=hand, W=size), ok


@check("merge-triplets-to-form-target-triplet")
def merge_triplets(rng):
    triplets = [[rng.randint(1, 5) for _ in range(3)] for _ in range(rng.randint(1, 6))]
    if rng.random() < 0.5:
        chosen = rng.sample(triplets, rng.randint(1, len(triplets)))
        target = [max(t[i] for t in chosen) for i in range(3)]
    else:
        target = [rng.randint(1, 5) for _ in range(3)]
    want = any([max(t[i] for t in chosen) for i in range(3)] == target
               for r in range(1, len(triplets) + 1) for chosen in combinations(triplets, r))
    return args(triplets=triplets, target=target), want


@check("partition-labels")
def partition_labels(rng):
    s = word(rng, 1, 10, "abcde")
    cuts = [i for i in range(1, len(s) + 1) if set(s[:i]).isdisjoint(s[i:])]  # nothing occurs on both sides
    return args(s=s), [b - a for a, b in zip([0] + cuts, cuts)]


@check("valid-parenthesis-string")
def valid_parenthesis_string(rng):
    s = word(rng, 1, 8, "()*")

    def balanced(text) -> bool:
        depth = 0
        for ch in text:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                return False
        return depth == 0

    stars = s.count("*")
    want = False
    for choice in product(["(", ")", ""], repeat=stars):  # every way to read the stars
        fill = iter(choice)
        if balanced("".join(next(fill) if ch == "*" else ch for ch in s)):
            want = True
            break
    return args(s=s), want


# -- Intervals --------------------------------------------------------------------


def _union(intervals) -> list[list[int]]:
    """Merge intervals by painting them on a line.  Two cells per unit, so that
    [1, 2] and [2, 3] join while [1, 2] and [3, 4] stay apart."""
    if not intervals:
        return []
    lo = min(a for a, _ in intervals)
    hi = max(b for _, b in intervals)
    cells = [False] * (2 * (hi - lo) + 1)
    for a, b in intervals:
        for x in range(2 * (a - lo), 2 * (b - lo) + 1):
            cells[x] = True
    out, start = [], None
    for x, on in enumerate(cells + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            out.append([lo + start // 2, lo + (x - 1) // 2])
            start = None
    return out


@check("insert-interval")
def insert_interval(rng):
    points = sorted(rng.sample(range(0, 30), 2 * rng.randint(0, 5)))
    intervals = [[points[i], points[i + 1]] for i in range(0, len(points), 2)]  # sorted, not touching
    for interval in intervals:
        if rng.random() < 0.15:
            interval[1] = interval[0]  # a single point
    a = rng.randint(0, 30)
    new = [a, rng.randint(a, min(32, a + 12))]
    return args(intervals=intervals, newInterval=new), _union(intervals + [new])


@check("merge-intervals")
def merge_intervals(rng):
    intervals = []
    for _ in range(rng.randint(1, 7)):
        a = rng.randint(0, 15)
        intervals.append([a, rng.randint(a, min(18, a + 6))])
    want = _union(intervals)
    return args(intervals=intervals), Ok(lambda got: sorted(got) == want, f"expected {want}")


def _spans(rng, lo: int, hi: int) -> list[list[int]]:
    out = []
    for _ in range(rng.randint(lo, hi)):
        a = rng.randint(0, 10)
        out.append([a, rng.randint(a + 1, a + 5)])
    return out


@check("non-overlapping-intervals")
def non_overlapping(rng):
    intervals = _spans(rng, 1, 8)
    n = len(intervals)
    keep = 0
    for size in range(n, 0, -1):  # the largest set of intervals that fit together
        if any(all(x[1] <= y[0] or y[1] <= x[0] for x, y in combinations(chosen, 2))
               for chosen in combinations(intervals, size)):
            keep = size
            break
    return args(intervals=intervals), n - keep


@check("meeting-rooms")
def meeting_rooms(rng):
    intervals = _spans(rng, 0, 6)
    clash = any(x[0] < y[1] and y[0] < x[1] for x, y in combinations(intervals, 2))
    return args(intervals=intervals), not clash


@check("meeting-rooms-ii")
def meeting_rooms_ii(rng):
    intervals = _spans(rng, 0, 7)
    # the busiest moment is always the start of some meeting
    want = max([0] + [sum(1 for a, b in intervals if a <= start < b) for start, _ in intervals])
    return args(intervals=intervals), want


@check("minimum-interval-to-include-each-query")
def min_interval_query(rng):
    intervals = []
    for _ in range(rng.randint(1, 6)):
        a = rng.randint(1, 12)
        intervals.append([a, rng.randint(a, a + 5)])
    queries = ints(rng, 1, 6, 0, 16)
    want = [min([b - a + 1 for a, b in intervals if a <= q <= b] or [-1]) for q in queries]
    return args(intervals=intervals, queries=queries), want


# -- Math & Geometry ----------------------------------------------------------------


@check("rotate-image")
def rotate_image(rng):
    n = rng.randint(1, 5)
    m = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    return args(matrix=m), [list(row) for row in zip(*m[::-1])]


@check("spiral-matrix")
def spiral_matrix(rng):
    m = grid(rng, 1, 4, 1, 5, lambda: rng.randint(-9, 20))
    rest, want = [row[:] for row in m], []
    while rest:  # take the top row, then turn what is left a quarter turn to the left
        want += rest.pop(0)
        rest = [list(row) for row in zip(*rest)][::-1]
    return args(matrix=m), want


@check("set-matrix-zeroes")
def set_matrix_zeroes(rng):
    m = grid(rng, 1, 4, 1, 4, lambda: rng.choice([0, 1, 2, 3, 4]))
    rows, cols = len(m), len(m[0])
    want = [[0 if (0 in m[r] or any(m[x][c] == 0 for x in range(rows))) else m[r][c] for c in range(cols)]
            for r in range(rows)]
    return args(matrix=m), want


@check("happy-number")
def happy_number(rng):
    n = rng.randint(1, 9999)
    seen, x = set(), n
    while x != 1 and x not in seen:
        seen.add(x)
        x = sum(int(d) ** 2 for d in str(x))
    return args(n=n), x == 1


@check("plus-one")
def plus_one(rng):
    size = rng.randint(1, 12)
    number = 10**size - 1 if rng.random() < 0.2 else rng.randint(0, 10**size)
    return args(digits=[int(d) for d in str(number)]), [int(d) for d in str(number + 1)]


@check("powx-n")
def pow_x_n(rng):
    x = 0.0
    while x == 0.0:
        x = round(rng.uniform(-3, 3), 2)
    n = rng.randint(-9, 9)
    return args(x=x, n=n), x**n


@check("multiply-strings")
def multiply_strings(rng):
    a = rng.randint(0, 10 ** rng.randint(1, 9))
    b = rng.randint(0, 10 ** rng.randint(1, 9))
    return args(num1=str(a), num2=str(b)), str(a * b)


@check("detect-squares")
def detect_squares(rng):
    ops, want = ["DetectSquares()"], [SKIP]
    count: Counter = Counter()
    for _ in range(rng.randint(1, 24)):
        x, y = rng.randint(0, 4), rng.randint(0, 4)
        if rng.random() < 0.65:
            count[x, y] += 1
            ops.append(f"add([{x}, {y}])")
            want.append(SKIP)
        else:
            # pick the corner diagonally opposite the query; the other two corners are then fixed
            total = sum(n * count[x, y2] * count[x2, y]
                        for (x2, y2), n in list(count.items())
                        if x2 != x and abs(x2 - x) == abs(y2 - y))
            ops.append(f"count([{x}, {y}])")
            want.append(total)
    return ops, calls(want)


# -- Bit Manipulation ---------------------------------------------------------------


@check("single-number")
def single_number(rng):
    values = rng.sample(range(-20, 21), rng.randint(1, 6))
    nums = values[:-1] * 2 + values[-1:]
    rng.shuffle(nums)
    return args(nums=nums), values[-1]


@check("number-of-1-bits")
def number_of_1_bits(rng):
    n = rng.randint(1, 2**31 - 1) if rng.random() < 0.7 else rng.randint(1, 64)
    return args(n=n), bin(n).count("1")


@check("counting-bits", cases=40)
def counting_bits(rng):
    num = rng.randint(0, 70)
    return args(num=num), [bin(i).count("1") for i in range(num + 1)]


@check("reverse-bits")
def reverse_bits(rng):
    n = rng.randint(0, 2**32 - 1)
    return args(n=n), int(format(n, "032b")[::-1], 2)


@check("missing-number")
def missing_number(rng):
    n = rng.randint(1, 9)
    nums = list(range(n + 1))
    gone = nums.pop(rng.randrange(n + 1))
    rng.shuffle(nums)
    return args(nums=nums), gone


@check("sum-of-two-integers")
def sum_of_two_integers(rng):
    a, b = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
    return args(a=a, b=b), a + b


@check("reverse-integer")
def reverse_integer(rng):
    roll = rng.random()
    if roll < 0.55:
        x = rng.randint(-(10 ** rng.randint(1, 9)), 10 ** rng.randint(1, 9))
    elif roll < 0.8:
        x = rng.randint(-(2**31), 2**31 - 1)
    else:  # numbers whose mirror image lands right next to the 32-bit limit
        x = 0
        while not 0 < x <= 2**31 - 1:
            x = int(str(2**31 + rng.randint(-40, 40))[::-1])
        x *= rng.choice([1, -1])
    flipped = int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)
    return args(x=x), flipped if -(2**31) <= flipped <= 2**31 - 1 else 0
