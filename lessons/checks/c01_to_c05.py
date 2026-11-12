"""Checks: Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

from .kit import SKIP, Ok, args, calls, check, ints, same_sets, word

# -- Arrays & Hashing -----------------------------------------------------------


@check("contains-duplicate")
def contains_duplicate(rng):
    nums = ints(rng, 1, 9, -4, 6)
    return args(nums=nums), len(set(nums)) != len(nums)


@check("valid-anagram")
def valid_anagram(rng):
    s = word(rng, 1, 6)
    t = "".join(rng.sample(s, len(s))) if rng.random() < 0.5 else word(rng, 1, 6)
    return args(s=s, t=t), sorted(s) == sorted(t)


@check("two-sum")
def two_sum(rng):
    while True:  # LeetCode promises exactly one answer
        nums = ints(rng, 2, 8, -9, 9)
        i, j = sorted(rng.sample(range(len(nums)), 2))
        target = nums[i] + nums[j]
        if sum(nums[a] + nums[b] == target for a, b in combinations(range(len(nums)), 2)) == 1:
            break
    return args(nums=nums, target=target), Ok(lambda got: sorted(got) == [i, j], f"expected the indexes {i} and {j}")


@check("group-anagrams")
def group_anagrams(rng):
    strs = [word(rng, 0, 4) for _ in range(rng.randint(1, 8))]
    groups: dict[str, list[str]] = {}
    for s in strs:
        groups.setdefault("".join(sorted(s)), []).append(s)
    want = sorted(sorted(g) for g in groups.values())
    return args(strs=strs), Ok(lambda got: sorted(sorted(g) for g in got) == want, f"expected the groups {want}")


@check("top-k-frequent-elements")
def top_k_frequent(rng):
    m = rng.randint(1, 6)
    values = rng.sample(range(-9, 10), m)
    counts = rng.sample(range(1, m + 4), m)  # all different, so the answer is unique
    nums = [v for v, c in zip(values, counts) for _ in range(c)]
    rng.shuffle(nums)
    k = rng.randint(1, m)
    want = sorted(v for v, _ in sorted(zip(values, counts), key=lambda p: -p[1])[:k])
    return args(nums=nums, k=k), Ok(lambda got: sorted(got) == want, f"expected {want} in any order")


@check("product-of-array-except-self")
def product_except_self(rng):
    nums = ints(rng, 2, 8, -4, 5)
    want = []
    for i in range(len(nums)):
        p = 1
        for j, v in enumerate(nums):
            if j != i:
                p *= v
        want.append(p)
    return args(nums=nums), want


def _sudoku_ok(board) -> bool:
    units = []
    for i in range(9):
        units.append([board[i][c] for c in range(9)])
        units.append([board[r][i] for r in range(9)])
        units.append([board[3 * (i // 3) + r][3 * (i % 3) + c] for r in range(3) for c in range(3)])
    for unit in units:
        filled = [ch for ch in unit if ch != "."]
        if len(set(filled)) != len(filled):
            return False
    return True


@check("valid-sudoku", cases=120)
def valid_sudoku(rng):
    digits = list("123456789")
    rng.shuffle(digits)
    full = [[digits[(3 * (r % 3) + r // 3 + c) % 9] for c in range(9)] for r in range(9)]  # a solved grid
    board = [[ch if rng.random() < 0.45 else "." for ch in row] for row in full]
    for _ in range(rng.choice([0, 0, 1, 2])):  # sometimes spoil it
        board[rng.randrange(9)][rng.randrange(9)] = rng.choice("123456789")
    return args(board=board), _sudoku_ok(board)


@check("encode-and-decode-strings")
def encode_decode(rng):
    strs = [word(rng, 0, 6, "ab#1 0:,/") for _ in range(rng.randint(0, 5))]
    return (["Codec()", f"encode({strs!r})", "decode(_out[1])"],
            Ok(lambda got: got[2] == strs, f"decode(encode(x)) must give back {strs}"))


@check("longest-consecutive-sequence")
def longest_consecutive(rng):
    nums = ints(rng, 0, 12, -6, 8)
    best = run = 0
    prev = None
    for v in sorted(set(nums)):
        run = run + 1 if prev is not None and v == prev + 1 else 1
        best = max(best, run)
        prev = v
    return args(nums=nums), best


# -- Two Pointers ---------------------------------------------------------------


@check("valid-palindrome")
def valid_palindrome(rng):
    s = word(rng, 0, 9, "aAbB1 ,.:!")
    if rng.random() < 0.4:
        s = s + rng.choice(["", " ", "!"]) + s[::-1].swapcase()
    clean = [ch.lower() for ch in s if ch.isalnum()]
    return args(s=s), clean == clean[::-1]


@check("two-sum-ii-input-array-is-sorted")
def two_sum_sorted(rng):
    while True:
        numbers = sorted(ints(rng, 2, 8, -9, 9))
        i, j = sorted(rng.sample(range(len(numbers)), 2))
        target = numbers[i] + numbers[j]
        if sum(numbers[a] + numbers[b] == target for a, b in combinations(range(len(numbers)), 2)) == 1:
            break
    return args(numbers=numbers, target=target), [i + 1, j + 1]


@check("3sum")
def three_sum(rng):
    spread = rng.choice([4, 4, 2, 2, 1, 0])  # narrow ranges give many duplicates, 0 gives all zeros
    nums = ints(rng, 3, 9, -spread, spread)
    want = {tuple(sorted((nums[a], nums[b], nums[c])))
            for a, b, c in combinations(range(len(nums)), 3) if nums[a] + nums[b] + nums[c] == 0}
    return args(nums=nums), Ok(lambda got: same_sets(got, want))


@check("container-with-most-water")
def container(rng):
    height = ints(rng, 2, 9, 0, 9)
    want = max(min(height[i], height[j]) * (j - i) for i, j in combinations(range(len(height)), 2))
    return args(height=height), want


@check("trapping-rain-water")
def trapping_rain_water(rng):
    height = ints(rng, 1, 10, 0, 6)
    want = sum(min(max(height[: i + 1]), max(height[i:])) - h for i, h in enumerate(height))
    return args(height=height), want


# -- Sliding Window -------------------------------------------------------------


@check("best-time-to-buy-and-sell-stock")
def buy_sell(rng):
    prices = ints(rng, 1, 9, 0, 9)
    want = max([0] + [prices[j] - prices[i] for i, j in combinations(range(len(prices)), 2)])
    return args(prices=prices), want


@check("longest-substring-without-repeating-characters")
def longest_unique_substring(rng):
    s = word(rng, 0, 9, "abc ")
    want = max([0] + [j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if len(set(s[i:j])) == j - i])
    return args(s=s), want


@check("longest-repeating-character-replacement")
def character_replacement(rng):
    s = word(rng, 1, 9, "ABC")
    k = rng.randint(0, 3)
    want = max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1)
               if (j - i) - max(Counter(s[i:j]).values()) <= k)
    return args(s=s, k=k), want


@check("permutation-in-string")
def permutation_in_string(rng):
    s1 = word(rng, 1, 3)
    s2 = word(rng, 0, 8)
    want = any(sorted(s2[i : i + len(s1)]) == sorted(s1) for i in range(len(s2) - len(s1) + 1))
    return args(s1=s1, s2=s2), want


@check("minimum-window-substring")
def minimum_window(rng):
    s = word(rng, 1, 9, "abAB")
    t = word(rng, 1, 3, "abAB")
    need = Counter(t)

    def covers(window: str) -> bool:
        have = Counter(window)
        return all(have[ch] >= n for ch, n in need.items())

    sizes = [j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if covers(s[i:j])]
    best = min(sizes) if sizes else 0

    def judge(got):
        if best == 0:
            return got == "" or 'no window exists, expected ""'
        return (len(got) == best and got in s and covers(got)) or f"expected a covering window of length {best}"

    return args(s=s, t=t), Ok(judge)


@check("sliding-window-maximum")
def sliding_window_maximum(rng):
    nums = ints(rng, 1, 9, -5, 9)
    k = rng.randint(1, len(nums))
    return args(nums=nums, k=k), [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]


# -- Stack ----------------------------------------------------------------------


def _balanced(rng, pairs: int) -> str:
    if pairs == 0:
        return ""
    inside = rng.randint(0, pairs - 1)
    kind = rng.choice(["()", "[]", "{}"])
    return kind[0] + _balanced(rng, inside) + kind[1] + _balanced(rng, pairs - 1 - inside)


@check("valid-parentheses")
def valid_parentheses(rng):
    if rng.random() < 0.55:
        s = _balanced(rng, rng.randint(1, 4))
        if rng.random() < 0.3:  # damage one character
            i = rng.randrange(len(s))
            s = s[:i] + rng.choice("()[]{}") + s[i + 1 :]
    else:
        s = word(rng, 1, 8, "()[]{}")
    rest = s
    while True:  # delete matching neighbours until nothing changes
        smaller = rest.replace("()", "").replace("[]", "").replace("{}", "")
        if smaller == rest:
            break
        rest = smaller
    return args(s=s), rest == ""


@check("min-stack")
def min_stack(rng):
    ops, want, ref = ["MinStack()"], [SKIP], []
    for _ in range(rng.randint(1, 14)):
        kind = rng.choice(["push", "push", "pop", "top", "getMin"]) if ref else "push"
        if kind == "push":
            v = rng.randint(-9, 9)
            ref.append(v)
            ops.append(f"push({v})")
            want.append(SKIP)
        elif kind == "pop":
            ref.pop()
            ops.append("pop()")
            want.append(SKIP)
        elif kind == "top":
            ops.append("top()")
            want.append(ref[-1])
        else:
            ops.append("getMin()")
            want.append(min(ref))
    return ops, calls(want)


def _rpn(rng, depth: int):
    """A random expression as (tokens, value); division truncates toward zero."""
    if depth == 0 or rng.random() < 0.3:
        v = rng.randint(-9, 12)
        return [str(v)], v
    while True:
        left_tokens, a = _rpn(rng, depth - 1)
        right_tokens, b = _rpn(rng, depth - 1)
        op = rng.choice("+-*/")
        if op == "/" and b == 0:
            continue
        if op == "+":
            v = a + b
        elif op == "-":
            v = a - b
        elif op == "*":
            v = a * b
        else:
            q = abs(a) // abs(b)
            v = q if (a < 0) == (b < 0) else -q
        return left_tokens + right_tokens + [op], v


@check("evaluate-reverse-polish-notation")
def evaluate_rpn(rng):
    tokens, value = _rpn(rng, rng.randint(1, 3))
    return args(tokens=tokens), value


def _well_formed(chars) -> bool:
    depth = 0
    for ch in chars:
        depth += 1 if ch == "(" else -1
        if depth < 0:
            return False
    return depth == 0


@check("generate-parentheses", cases=12)
def generate_parentheses(rng):
    n = rng.randint(1, 6)
    want = sorted("".join(p) for p in product("()", repeat=2 * n) if _well_formed(p))
    return args(n=n), Ok(lambda got: sorted(got) == want, f"expected all {len(want)} well-formed strings exactly once")


@check("daily-temperatures")
def daily_temperatures(rng):
    t = ints(rng, 1, 10, 30, 40)
    want = [next((j - i for j in range(i + 1, len(t)) if t[j] > t[i]), 0) for i in range(len(t))]
    return args(temperatures=t), want


@check("car-fleet")
def car_fleet(rng):
    n = rng.randint(1, 7)
    target = rng.randint(n, 20)
    position = rng.sample(range(target), n)
    speed = [rng.randint(1, 6) for _ in range(n)]
    hours = {p: Fraction(target - p, s) for p, s in zip(position, speed)}
    # a car leads a fleet exactly when it needs strictly longer than every car ahead of it
    want = sum(1 for p in position if all(hours[p] > hours[q] for q in position if q > p))
    return args(target=target, position=position, speed=speed), want


@check("largest-rectangle-in-histogram")
def largest_rectangle(rng):
    heights = ints(rng, 1, 9, 0, 7)
    n = len(heights)
    want = max(min(heights[i : j + 1]) * (j - i + 1) for i in range(n) for j in range(i, n))
    return args(heights=heights), want


# -- Binary Search --------------------------------------------------------------


@check("binary-search")
def binary_search(rng):
    nums = sorted(rng.sample(range(-15, 16), rng.randint(1, 10)))
    target = rng.choice(nums) if rng.random() < 0.6 else rng.randint(-17, 17)
    return args(nums=nums, target=target), nums.index(target) if target in nums else -1


@check("search-a-2d-matrix")
def search_matrix(rng):
    rows, cols = rng.randint(1, 4), rng.randint(1, 4)
    flat = sorted(rng.sample(range(-20, 40), rows * cols))
    matrix = [flat[r * cols : (r + 1) * cols] for r in range(rows)]
    target = rng.choice(flat) if rng.random() < 0.5 else rng.randint(-22, 42)
    return args(matrix=matrix, target=target), any(target in row for row in matrix)


@check("koko-eating-bananas")
def koko(rng):
    piles = ints(rng, 1, 6, 1, 20)
    h = rng.randint(len(piles), len(piles) + 12)
    want = next(k for k in range(1, max(piles) + 1) if sum(-(-p // k) for p in piles) <= h)
    return args(piles=piles, h=h), want


@check("find-minimum-in-rotated-sorted-array")
def find_min_rotated(rng):
    base = sorted(rng.sample(range(-20, 21), rng.randint(1, 9)))
    r = rng.randrange(len(base))
    nums = base[r:] + base[:r]
    return args(nums=nums), min(nums)


@check("search-in-rotated-sorted-array")
def search_rotated(rng):
    base = sorted(rng.sample(range(-20, 21), rng.randint(1, 9)))
    r = rng.randrange(len(base))
    nums = base[r:] + base[:r]
    target = rng.choice(nums) if rng.random() < 0.6 else rng.randint(-22, 22)
    return args(nums=nums, target=target), nums.index(target) if target in nums else -1


@check("time-based-key-value-store")
def time_map(rng):
    ops, want = ["TimeMap()"], [SKIP]
    store: dict[str, list] = {}
    now = 0
    for _ in range(rng.randint(1, 14)):
        key = rng.choice("abc")
        if rng.random() < 0.5:
            now += rng.randint(1, 3)  # timestamps of set() are strictly increasing
            value = word(rng, 1, 3, "xyz")
            store.setdefault(key, []).append((now, value))
            ops.append(f"set({key!r}, {value!r}, {now})")
            want.append(SKIP)
        else:
            when = rng.randint(0, now + 2)
            older = [v for ts, v in store.get(key, []) if ts <= when]
            ops.append(f"get({key!r}, {when})")
            want.append(older[-1] if older else "")
    return ops, calls(want)


@check("median-of-two-sorted-arrays")
def median_two_arrays(rng):
    a = sorted(ints(rng, 0, 6, -9, 9))
    b = sorted(ints(rng, 0 if a else 1, 6, -9, 9))
    merged = sorted(a + b)
    n = len(merged)
    want = float(merged[n // 2]) if n % 2 else (merged[n // 2 - 1] + merged[n // 2]) / 2
    return args(nums1=a, nums2=b), want
