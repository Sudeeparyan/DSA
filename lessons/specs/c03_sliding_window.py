"""Sliding Window."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "best-time-to-buy-and-sell-stock",
    pattern="Track the lowest price so far",
    statement="""`prices[i]` is a stock's price on day `i`. You may buy on one day and sell on a
    **later** day. Return the largest profit possible, or 0 if no profit can be made.""",
    args="prices=[7, 1, 5, 3, 6, 4]",
    expected=5,
    why="Buy on day 1 at price 1 and sell on day 4 at price 6: 6 − 1 = 5.",
    idea=[
        "Trying every (buy day, sell day) pair is O(n²).",
        "If we sell today, the best day to have bought is simply the **cheapest day before today**.",
        "So walk through the days once, remembering the lowest price seen so far. Each day, check the profit of selling today and keep the best.",
    ],
    views=[
        Arr("prices", bars=True, ptrs={"price": "at('for price in prices')"},
            tones={"alt": "prices.index(min_price) if min_price in prices else None",
                   "cur": "at('for price in prices')"}),
        Vars("min_price", "max_profit"),
    ],
    notes=[
        ("min_price = float(",
         "`min_price` is the cheapest price seen so far — the best day to have **bought**. Nothing has been "
         "seen yet, so it starts at infinity."),
        ("max_profit = 0", "`max_profit` is the best profit found so far. Not trading at all earns 0."),
        ("min_price = min(min_price, price)", [
            ("price < was.min_price",
             "Day {at('for price in prices')}: the price is {price}, the **cheapest so far**. It becomes the new "
             "best day to buy: `min_price` = {min_price}."),
            (None,
             "Day {at('for price in prices')}: the price is {price}. The cheapest earlier price is still {min_price}."),
        ]),
        ("max_profit = max(max_profit, price - min_price)", [
            ("price - min_price > was.max_profit",
             "Selling today after buying at {min_price} earns {price} − {min_price} = **{price - min_price}** — "
             "a new best. `max_profit` = {max_profit}."),
            (None,
             "Selling today after buying at {min_price} would earn {price - min_price}, which does not beat {max_profit}."),
        ]),
        ("return max_profit", "The best profit over all selling days is **{_ret}**."),
    ],
    time=("O(n)", "One pass over the prices."),
    space=("O(1)", "Only the lowest price and the best profit are stored."),
    tests=[("prices=[7, 6, 4, 3, 1]", 0), ("prices=[2, 4, 1]", 2), ("prices=[]", 0)],
)

lesson(
    "longest-substring-without-repeating-characters",
    pattern="Sliding window + set of characters inside it",
    statement="""Given a string `s`, return the length of the longest **substring** (a run of
    neighbouring characters) in which no character appears twice.""",
    args="s='abcabcbb'",
    expected=3,
    why='The longest stretch without a repeat is "abc", of length 3.',
    idea=[
        "Checking every substring is O(n²) or worse. Instead, keep one **window** `[left … right]` that never contains a repeated character.",
        "Grow the window on the right while the next character is new. A set of the characters inside the window makes that check O(1).",
        "When the next character is already inside, shrink from the left — removing characters one by one — until it is gone. The largest window ever seen is the answer.",
    ],
    views=[
        Arr("s", ptrs=["left", "right"], rng=("left", "left + len(unique_chars) - 1", "window"),
            tones={"cur": "right"}),
        HMap("unique_chars", title="unique_chars  (letters inside the window)"),
        Vars("max_length"),
    ],
    notes=[
        ("unique_chars = set()",
         "The window is empty to begin with. The set mirrors which letters are inside it."),
        ("max_length = max(max_length, right - left + 1)",
         "`{s[right]}` is not in the window yet, so the window grows to take it in: `{s[left:right + 1]}`, "
         "length {right - left + 1}. Longest so far: **{max_length}**.",
         {"unique_chars.cur": "s[right]"}),
        ("left += 1",
         "`{s[right]}` is **already inside** the window, so the window has to shrink first: `{s[left - 1]}` "
         "leaves on the left.",
         {"s.bad": "left - 1"}),
        ("while right < len(s)", dict(no="`right` has passed the end of the string, so the scan is over.")),
        ("return max_length", "The longest window without a repeated letter had length **{_ret}**."),
    ],
    time=("O(n)", "`left` and `right` each move forward at most n times."),
    space=("O(k)", "The set holds the characters of the current window: at most the alphabet size k."),
    tests=[("s='bbbbb'", 1), ("s='pwwkew'", 3), ("s=''", 0), ("s='dvdf'", 3)],
)

lesson(
    "longest-repeating-character-replacement",
    pattern="Sliding window: length − most common letter ≤ k",
    statement="""Given a string `s` of uppercase letters and a number `k`, you may change at most
    `k` characters to any other letter. Return the length of the longest substring that can be
    made of **one single repeated letter**.""",
    args="s='AABABBA', k=1",
    expected=4,
    why='Change one B in "AABA" to A and the four letters are all the same.',
    idea=[
        "Inside any window, the cheapest plan is to keep the **most common** letter and replace all the others.",
        "So a window is valid exactly when `window length − count of its most common letter ≤ k`.",
        "Grow the window to the right; whenever it becomes invalid, drop one character on the left. The window never needs to get smaller than the best size found, so `max_freq` is never lowered.",
    ],
    views=[
        Arr("s", ptrs=["left", "right"], rng=("left", "right", "window"), tones={"cur": "right"}),
        HMap("char_freq", title="char_freq  (letter → count inside the window)"),
        Vars("k", "max_freq", "max_length"),
    ],
    notes=[
        ("max_freq = 0",
         "`char_freq` counts each letter inside the window, and `max_freq` is the count of the most common one."),
        ("max_freq = max(max_freq, char_freq[s[right]])",
         "`{s[right]}` enters the window → `{s[left:right + 1]}`. It appears {plural(char_freq[s[right]], 'time')} "
         "there; the most common letter appears **{max_freq}** times.",
         {"char_freq.cur": "s[right]"}),
        ("if (right - left + 1) - max_freq > k", dict(
            yes="Length {right - left + 1} − most common {max_freq} = {right - left + 1 - max_freq} letters would "
                "need replacing, but only k = {k} is allowed. The window is **too big**.",
            no="Length {right - left + 1} − most common {max_freq} = {right - left + 1 - max_freq} "
               "to replace, which is within k = {k}. The window is **valid**.")),
        ("left += 1",
         "Drop `{s[left - 1]}` from the left. The window is now `{s[left:right + 1]}`.",
         {"s.bad": "left - 1"}),
        ("max_length = max(max_length, right - left + 1)", [
            ("max_length > was.max_length",
             "This valid window has length {right - left + 1}: a new best, `max_length` = **{max_length}**."),
        ]),
        ("return max_length", "The longest window that can be turned into one repeated letter has length **{_ret}**."),
    ],
    time=("O(n)", "`right` visits each character once and `left` only ever moves forward."),
    space=("O(1)", "The count map has at most 26 entries."),
    tests=[("s='ABAB', k=2", 4), ("s='AAAA', k=0", 4), ("s='ABCDE', k=1", 2)],
)

lesson(
    "permutation-in-string",
    pattern="Fixed-size sliding window + letter counts",
    statement="""Given strings `s1` and `s2`, return `True` if some **substring of `s2`** is a
    permutation of `s1` — that is, it uses exactly the same letters, in any order.""",
    args="s1='ab', s2='eidbaooo'",
    expected=True,
    why='The substring "ba" of s2 is a rearrangement of "ab".',
    idea=[
        "A permutation of `s1` has the same length and exactly the same letter counts as `s1`.",
        "So slide a window of length `len(s1)` across `s2` and compare its letter counts with those of `s1`.",
        "Do not recount each window from scratch: when the window slides one step, one letter enters on the right and one leaves on the left — update just those two counts.",
    ],
    views=[
        Arr("s1"),
        Arr("s2", ptrs=["left", "right"], rng=("left", "right", "window"), tones={"cur": "right"}),
        HMap("char_freq_s1", title="char_freq_s1  (what we need)"),
        HMap("char_freq_temp", title="char_freq_temp  (what the window has)"),
    ],
    notes=[
        ("char_freq_s1[char] = char_freq_s1.get(char, 0) + 1",
         "Count the letters of `s1`: `{char}` → {char_freq_s1[char]}. Every permutation of `s1` has exactly these counts.",
         {"char_freq_s1.cur": "char"}),
        ("char_freq_temp = {}",
         "Now slide a window of length {len(s1)} across `s2`, keeping the letter counts of whatever is inside it."),
        ("char_freq_temp[s2[right]] = char_freq_temp.get(s2[right], 0) + 1",
         "`{s2[right]}` enters the window on the right.",
         {"char_freq_temp.cur": "s2[right]"}),
        ("if right - left + 1 == len(s1)", dict(
            no="The window holds only {plural(right - left + 1, 'letter')} so far — not yet the length of `s1`.")),
        ("if char_freq_temp == char_freq_s1", dict(
            yes="Window `{s2[left:right + 1]}` has **exactly the same letter counts** as `s1`, so it is a permutation of it.",
            no="Window `{s2[left:right + 1]}` has different letter counts from `s1`. No match here.",
            yes_marks={"s2.good": "range(left, right + 1)"})),
        ("return True", "A matching window exists → **True**.", {"s2.good": "range(left, right + 1)"}),
        ("left += 1", "Slide on: `{s2[left - 1]}` leaves the window on the left.", {"s2.bad": "left - 1"}),
    ],
    time=("O(n)", "Each character of `s2` enters and leaves the window once; comparing two maps of at most 26 letters is O(1)."),
    space=("O(1)", "Two count maps with at most 26 entries each."),
    tests=[("s1='ab', s2='eidboaoo'", False), ("s1='adc', s2='dcda'", True), ("s1='abc', s2='ab'", False)],
)

lesson(
    "minimum-window-substring",
    pattern="Grow until valid, then shrink while valid",
    statement="""Given strings `s` and `t`, return the **shortest substring of `s`** that contains
    every character of `t` (including repeats). Return an empty string if there is none.""",
    code="""
    class Solution:
        def minWindow(self, s: str, t: str) -> str:
            if not s or not t:
                return ""

            char_freq_t = {}
            for char in t:
                char_freq_t[char] = char_freq_t.get(char, 0) + 1

            left, right = 0, 0
            char_freq_temp = {}
            required_chars = len(char_freq_t)
            formed_chars = 0
            min_length = float("inf")
            min_start = 0  # where the best window begins

            while right < len(s):
                char_freq_temp[s[right]] = char_freq_temp.get(s[right], 0) + 1

                if (
                    s[right] in char_freq_t
                    and char_freq_temp[s[right]] == char_freq_t[s[right]]
                ):
                    formed_chars += 1

                while left <= right and formed_chars == required_chars:
                    if right - left + 1 < min_length:
                        min_length = right - left + 1
                        min_start = left  # remember where it is; copy it only once, at the end

                    char_freq_temp[s[left]] -= 1
                    if (
                        s[left] in char_freq_t
                        and char_freq_temp[s[left]] < char_freq_t[s[left]]
                    ):
                        formed_chars -= 1

                    left += 1

                right += 1

            if min_length == float("inf"):
                return ""
            return s[min_start : min_start + min_length]
    """,
    args="s='ABXCBA', t='ABC'",
    expected="CBA",
    why='"CBA" contains A, B and C, and no shorter substring of s does.',
    idea=[
        "Use a window `[left … right]`. Moving `right` adds characters until the window contains everything `t` needs.",
        "Once the window is valid, try to make it **shorter**: move `left` forward while it stays valid, recording the best size. As soon as it breaks, go back to growing.",
        "To test validity in O(1), count how many *distinct* required letters currently have enough copies in the window (`formed_chars`). The window is valid when that equals the number of distinct letters in `t`.",
    ],
    init={"told": "0"},
    views=[
        Arr("s", ptrs=["left", "right"], rng=("left", "right", "window"), tones={"cur": "right"}),
        HMap("char_freq_t", title="char_freq_t  (needed)"),
        HMap("char_freq_temp", title="char_freq_temp  (inside the window)"),
        Vars("formed_chars", "required_chars",
             ("best window", "s[min_start:min_start + min_length] if min_length != float('inf') else '(none yet)'")),
    ],
    notes=[
        ("left, right = 0, 0",
         "`t` needs these letters: {dict(char_freq_t)}. We slide a window over `s`, and `formed_chars` counts how "
         "many of those letters the window has **enough** of."),
        ("char_freq_temp[s[right]] = char_freq_temp.get(s[right], 0) + 1",
         "Grow: `{s[right]}` enters the window → `{s[left:right + 1]}`.",
         {"char_freq_temp.cur": "s[right]"}),
        ("formed_chars += 1",
         "The window now has enough `{s[right]}`. Requirements met: **{formed_chars} of {required_chars}**.",
         {"char_freq_temp.good": "s[right]", "char_freq_t.good": "s[right]"}),
        ("if right - left + 1 < min_length", dict(
            no="The window `{s[left:right + 1]}` is valid, but it is not shorter than the best one (length {min_length}).")),
        ("min_start = left", dict(
            post=[
                ("told == 1",
                 "All {required_chars} requirements are met, and `{s[min_start:min_start + min_length]}` is the "
                 "**shortest valid window so far** (length {min_length}). Only its start and length are "
                 "remembered — copying the letters every time would be wasteful."),
                (None,
                 "All {required_chars} requirements are met, and `{s[min_start:min_start + min_length]}` is the "
                 "**shortest valid window so far** (length {min_length})."),
            ],
            save={"told": "told + 1"},
            marks={"s.good": "range(left, right + 1)"})),
        ("formed_chars -= 1",
         "`{s[left]}` is about to leave, and without it the window has too few `{s[left]}`. It will be "
         "**invalid** again, so shrinking stops after this.",
         {"s.bad": "left", "char_freq_temp.bad": "s[left]"}),
        ("left += 1",
         "Shrink: `{s[left - 1]}` leaves on the left. The window is now `{s[left:right + 1]}`."),
        ("return s[min_start : min_start + min_length]",
         "Cut the best window out of `s` once: the shortest window that contains all of `t` is **`{_ret}`**.",
         {"s.good": "range(min_start, min_start + min_length)"}),
    ],
    time=("O(n + m)", "Each character of `s` enters and leaves the window at most once; counting `t` takes O(m). "
                      "The answer is cut out of `s` only once, at the very end."),
    space=("O(k)", "Two count maps, at most one entry per distinct character."),
    tests=[("s='ADOBECODEBANC', t='ABC'", "BANC"), ("s='a', t='a'", "a"), ("s='a', t='aa'", "")],
)

lesson(
    "sliding-window-maximum",
    pattern="Monotonic deque of indexes",
    statement="""A window of size `k` slides over `nums` from left to right, one step at a time.
    Return the **maximum** value of every window.""",
    args="nums=[1, 5, 3, 2, 1, 4], k=3",
    expected=[5, 5, 3, 4],
    why="The windows are [1,5,3], [5,3,2], [3,2,1] and [2,1,4], with maximums 5, 5, 3 and 4.",
    idea=[
        "Scanning each window for its maximum costs O(n · k). Most of that work is repeated.",
        "When a new number arrives, every **smaller number before it** can never be a maximum again — the new one is bigger *and* will stay in the window longer. Throw those away.",
        "What is left is a deque of indexes whose values decrease from front to back. The front is always the maximum; it only has to be removed when it slides out of the window.",
    ],
    views=[
        Arr("nums", ptrs=["i"], rng=("max(0, i - k + 1)", "i", "window"),
            tones={"seen": "list(window)", "cur": "i"}),
        Queue("[f'{j}:{nums[j]}' for j in window]", id="window",
              title="window  (index:value, largest at the front)"),
        Items("result", title="result"),
    ],
    notes=[
        ("window = deque()",
         "`window` is a deque of **indexes**. We keep it so that the values at those indexes always decrease "
         "from front to back — which makes the front the maximum."),
        ("window.pop()",
         "The new value {num} is bigger than {nums[was.window[-1]]} at the back. That smaller value can **never be a "
         "maximum again** while {num} is around, so remove it."),
        ("window.append(i)",
         "Add index {i} (value {num}) at the back. Values in the deque: {[nums[j] for j in window]}."),
        ("window.popleft()",
         "The front index {was.window[0]} is now k = {k} steps behind `i` = {i}: it has **slid out of the window**. "
         "Remove it from the front."),
        ("result.append(nums[window[0]])",
         "The window covers indexes {i - k + 1}–{i}. Its maximum sits at the front of the deque: "
         "`nums[{window[0]}]` = **{nums[window[0]]}**.",
         {"nums.good": "window[0]", "window.good": "0", "result.good": "-1"}),
        ("return result", "One maximum per window: **{_ret}**."),
    ],
    time=("O(n)", "Every index is added to the deque once and removed at most once."),
    space=("O(k)", "The deque never holds more than k indexes."),
    tests=[("nums=[1, 3, -1, -3, 5, 3, 6, 7], k=3", [3, 3, 5, 5, 6, 7]), ("nums=[1], k=1", [1]),
           ("nums=[9, 8, 7, 6], k=2", [9, 8, 7])],
)

# end of c03_sliding_window
