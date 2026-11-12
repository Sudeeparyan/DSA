"""Binary Search."""

from lessons.engine.api import *  # noqa: F401,F403

OUTSIDE = "list(range(left)) + list(range(right + 1, len(nums)))"

lesson(
    "binary-search",
    pattern="Halve the search range",
    statement="""Given a **sorted** array of distinct integers `nums` and a `target`, return the
    index of `target`, or −1 if it is not in the array. The algorithm must run in O(log n) time.""",
    args="nums=[1, 3, 5, 7, 9, 11, 13, 15, 17], target=11",
    expected=5,
    why="nums[5] is 11.",
    idea=[
        "Checking every element is O(n), but that ignores the fact that the array is sorted.",
        "Look at the **middle** element. If it is too small, the target cannot be in the left half at all; if it is too big, it cannot be in the right half.",
        "Either way, half of the remaining elements are discarded with one comparison. Repeating that leaves at most log₂ n steps.",
    ],
    views=[
        Arr("nums", ptrs=["left", "mid", "right"], tones={"dim": OUTSIDE, "cur": "mid"}),
        Vars("target"),
    ],
    notes=[
        ("left, right = 0, len(nums) - 1",
         "`left` and `right` mark the part of the array where the target could still be. At first that is everything."),
        ("mid = left + (right - left) // 2",
         "Look at the middle of that part: index {mid}, which holds **{nums[mid]}**."),
        ("return mid", "{nums[mid]} is the target. Found at index **{mid}**.", {"nums.good": "mid"}),
        ("left = mid + 1",
         "{nums[mid]} is **smaller** than {target}. The array is sorted, so the target cannot be at index {mid} or "
         "anywhere left of it. Discard that half: `left` = {left}."),
        ("right = mid - 1",
         "{nums[mid]} is **bigger** than {target}, so the target cannot be at index {mid} or anywhere right of it. "
         "Discard that half: `right` = {right}."),
    ],
    time=("O(log n)", "Every comparison halves the range that is left."),
    space=("O(1)", "Three index variables."),
    tests=[("nums=[-1, 0, 3, 5, 9, 12], target=9", 4), ("nums=[-1, 0, 3, 5, 9, 12], target=2", -1),
           ("nums=[5], target=5", 0)],
)

lesson(
    "search-a-2d-matrix",
    pattern="Binary search over a flattened matrix",
    statement="""Each row of `matrix` is sorted from left to right, and the first number of each row
    is larger than the last number of the row above. Return `True` if `target` is in the matrix.
    The solution must run in O(log(m · n)) time.""",
    args="matrix=[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target=16",
    expected=True,
    why="16 is in row 1, column 2.",
    idea=[
        "Read row after row and the whole matrix is **one long sorted list**: each row continues where the previous one ended.",
        "So do an ordinary binary search over positions 0 … rows·cols − 1 of that imaginary list.",
        "Position `p` of the list lives at row `p // cols` and column `p % cols`. No copying into a real list is needed.",
    ],
    views=[
        Grid("matrix", ptrs={"mid": "(mid // cols, mid % cols)"},
             tones={"dim": "[(p // cols, p % cols) for p in list(range(left)) + list(range(right + 1, rows * cols))]",
                    "cur": "(mid // cols, mid % cols)"}),
        Vars("target", "left", "right", "mid", "num"),
    ],
    notes=[
        ("left, right = 0, rows * cols - 1",
         "Read row by row, the matrix is one sorted list of {rows * cols} numbers. Binary-search positions 0 to "
         "{right} of that list."),
        ("num = matrix[mid // cols][mid % cols]",
         "Middle position {mid} → row {mid} // {cols} = {mid // cols}, column {mid} % {cols} = {mid % cols}. "
         "The number there is **{num}**."),
        ("return True", "{num} is the target → **True**.", {"matrix.good": "(mid // cols, mid % cols)"}),
        ("left = mid + 1",
         "{num} is smaller than {target}, so the target can only be **later** in the list. `left` = {left}."),
        ("right = mid - 1",
         "{num} is bigger than {target}, so the target can only be **earlier** in the list. `right` = {right}."),
    ],
    time=("O(log(m · n))", "A binary search over all m · n cells."),
    space=("O(1)", "A few index variables."),
    tests=[("matrix=[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target=13", False),
           ("matrix=[[1]], target=1", True), ("matrix=[[1, 3]], target=3", True)],
)

lesson(
    "koko-eating-bananas",
    pattern="Binary search on the answer",
    statement="""Koko has `piles` of bananas and `h` hours. Each hour she picks one pile and eats up
    to `k` bananas from it (if the pile has fewer, she finishes it and waits). Return the
    **smallest** eating speed `k` that lets her finish every pile within `h` hours.""",
    args="piles=[3, 6, 7, 11], h=8",
    expected=4,
    why="At speed 4 the piles take 1 + 2 + 2 + 3 = 8 hours. At speed 3 they would take 10.",
    idea=[
        "We are not searching the array — we are searching for a **number**: the speed `k`, somewhere between 1 and the largest pile.",
        "Speeds have a clear order: if speed `k` is fast enough, every faster speed is too; if it is too slow, every slower speed is too. That *no, no, no, yes, yes, yes* pattern is what binary search needs.",
        "Test the middle speed by adding up ⌈pile / k⌉ hours for every pile. Too slow → search the faster half. Fast enough → remember it and search the slower half.",
    ],
    views=[
        Arr("piles", bars=True),
        Arr("[(pile + mid - 1) // mid for pile in piles]", id="hours_each",
            title="hours each pile needs at speed mid"),
        Arr("list(range(1, max(piles) + 1))", id="speeds", title="candidate speeds k", idx=False,
            ptrs={"left": "left - 1", "mid": "mid - 1", "right": "right - 1"},
            tones={"dim": "list(range(left - 1)) + list(range(right, max(piles)))", "cur": "mid - 1"}),
        Vars("h", "hours"),
    ],
    notes=[
        ("left, right = 1, max(piles)",
         "The answer is a speed between 1 and {right} (the biggest pile — eating faster than that never helps). "
         "Slow speeds fail and fast speeds work, so we can **binary-search the speed**."),
        ("hours = sum((pile + mid - 1) // mid for pile in piles)",
         "Try speed {mid}. Each pile takes ⌈pile / {mid}⌉ hours: "
         "{[(pile + mid - 1) // mid for pile in piles]}, **{hours} hours** in total. Koko has {h}."),
        ("left = mid + 1",
         "{hours} hours is **too slow**. Speed {mid} fails, and so does every slower speed: `left` = {left}."),
        ("right = mid",
         "{hours} hours is in time, so speed {mid} works. A slower speed might work too, so keep {mid} as a "
         "candidate and look below it: `right` = {right}."),
        ("while left < right", dict(
            no="`left` and `right` have met at {left}: the slowest speed that still works.",
            no_marks={"speeds.good": "left - 1"})),
        ("return left", "The minimum eating speed is **{_ret}** bananas per hour.", {"speeds.good": "left - 1"}),
    ],
    time=("O(n · log m)", "log m speeds are tested (m = largest pile), and each test adds up all n piles."),
    space=("O(1)", "Only a few numbers are stored."),
    tests=[("piles=[30, 11, 23, 4, 20], h=5", 30), ("piles=[30, 11, 23, 4, 20], h=6", 23), ("piles=[1], h=1", 1)],
)

lesson(
    "find-minimum-in-rotated-sorted-array",
    pattern="Binary search against the right end",
    statement="""A sorted array of distinct numbers has been **rotated**: some front part was moved
    to the back, as in `[4,5,6,7,0,1,2]`. Return its smallest element in O(log n) time.""",
    args="nums=[4, 5, 6, 7, 0, 1, 2]",
    expected=0,
    why="The array rises 4, 5, 6, 7, then drops to 0 — the smallest value sits right after the drop.",
    idea=[
        "A rotated sorted array is two rising runs. Every value in the first run is bigger than every value in the second, and the minimum is the first element of the second run.",
        "Compare the middle with the **right end**. If the middle is bigger, the drop — and the minimum — lies to its right.",
        "Otherwise the middle already belongs to the second run, so the minimum is the middle itself or something to its left. Keep halving until one element is left.",
    ],
    views=[
        Arr("nums", bars=True, ptrs=["left", "mid", "right"], tones={"dim": OUTSIDE, "cur": "mid"}),
    ],
    notes=[
        ("left, right = 0, len(nums) - 1",
         "The array is two rising runs with one drop between them. The minimum sits right after the drop."),
        ("mid = left + (right - left) // 2",
         "The middle (index {mid}) holds {nums[mid]}; the right end holds {nums[right]}."),
        ("left = mid + 1",
         "{nums[mid]} is bigger than {nums[right]}, so the values **drop** somewhere to the right of `mid`. "
         "The minimum is in that part: `left` = {left}."),
        ("right = mid",
         "{nums[mid]} is not bigger than {nums[was.right]}, so everything from `mid` to the old right end only rises. "
         "The minimum is `mid` itself or further left: `right` = {right}."),
        ("while left < right", dict(
            no="`left` and `right` have met on index {left}.", no_marks={"nums.good": "left"})),
        ("return nums[left]", "The smallest element is `nums[{left}]` = **{_ret}**.", {"nums.good": "left"}),
    ],
    time=("O(log n)", "Half of the remaining range is discarded at every step."),
    space=("O(1)", "Three index variables."),
    tests=[("nums=[3, 4, 5, 1, 2]", 1), ("nums=[11, 13, 15, 17]", 11), ("nums=[2, 1]", 1)],
)

lesson(
    "search-in-rotated-sorted-array",
    pattern="Binary search: one half is always sorted",
    statement="""A sorted array of distinct numbers has been rotated (for example
    `[4,5,6,7,0,1,2]`). Return the index of `target`, or −1 if it is absent, in O(log n) time.""",
    args="nums=[6, 7, 8, 0, 1, 2, 4, 5], target=8",
    expected=2,
    why="nums[2] is 8.",
    idea=[
        "Cut a rotated array in the middle and **at least one of the two halves is perfectly sorted** — the drop can only be in one of them.",
        "Find the sorted half by comparing its two ends. A sorted half is easy to reason about: the target is inside it exactly when it lies between those two end values.",
        "If the target is in the sorted half, search there. If not, it can only be in the other half. Either way, half of the array is discarded.",
    ],
    views=[
        Arr("nums", bars=True, ptrs=["left", "mid", "right"], tones={"dim": OUTSIDE, "cur": "mid"}),
        Vars("target"),
    ],
    notes=[
        ("mid = left + (right - left) // 2", "The middle (index {mid}) holds **{nums[mid]}**."),
        ("return mid", "{nums[mid]} is the target. Found at index **{mid}**.", {"nums.good": "mid"}),
        ("if nums[left] <= nums[mid]", dict(
            yes="`nums[left]` = {nums[left]} is not bigger than `nums[mid]` = {nums[mid]}, so the **left half** "
                "(indexes {left}–{mid}) is in sorted order.",
            no="`nums[left]` = {nums[left]} is bigger than `nums[mid]` = {nums[mid]}: the drop is on the left, so "
               "the **right half** (indexes {mid}–{right}) is the sorted one.",
            yes_marks={"nums.win": "range(left, mid)"},
            no_marks={"nums.win": "range(mid + 1, right + 1)"})),
        ("left = mid + 1@1",
         "That sorted half runs from {nums[was.left]} to {nums[mid]}, and {target} is **not** in that range. "
         "So it must be in the other half: `left` = {left}."),
        ("right = mid - 1@2",
         "That sorted half runs from {nums[mid]} to {nums[was.right]}, and {target} is **not** in that range. "
         "So it must be in the other half: `right` = {right}."),
    ],
    time=("O(log n)", "Each step identifies the sorted half and discards one half."),
    space=("O(1)", "Three index variables."),
    tests=[("nums=[4, 5, 6, 7, 0, 1, 2], target=0", 4), ("nums=[4, 5, 6, 7, 0, 1, 2], target=3", -1),
           ("nums=[1], target=0", -1), ("nums=[5, 1, 3], target=3", 2)],
)

lesson(
    "time-based-key-value-store",
    pattern="Hash map of time-sorted lists + binary search",
    statement="""Design a store with `set(key, value, timestamp)` and `get(key, timestamp)`. `get`
    returns the value that was set for `key` at the **latest time ≤ timestamp**, or an empty
    string if nothing had been set by then. Timestamps passed to `set` always increase.""",
    ops=["TimeMap()", "set('price', 'low', 1)", "set('price', 'mid', 4)", "set('price', 'high', 8)",
         "get('price', 5)", "get('price', 8)", "get('price', 0)"],
    expected=[None, None, None, None, "mid", "high", ""],
    why="At time 5 the latest value is the one set at time 4. At time 0 nothing had been set yet.",
    idea=[
        "Keep, for every key, a list of (timestamp, value) pairs. Because timestamps only increase, each list is **already sorted** by time.",
        "`get` needs the last pair whose timestamp is ≤ the one asked for — a search in a sorted list, so use binary search.",
        "When the search ends without an exact hit, `right` has stopped on the last entry that is not too new. If `right` fell off the left edge, there is no such entry.",
    ],
    views=[
        HMap("self.data", id="data", title="data  (key → list of (timestamp, value))"),
        Arr("values", title="values for this key  (timestamp:value)", ptrs=["left", "mid", "right"],
            text=lambda v: f"{v[0]}:{v[1]}",
            tones={"dim": "list(range(left)) + list(range(right + 1, len(values)))", "cur": "mid"}),
        Vars("timestamp"),
    ],
    notes=[
        ("self.data = defaultdict(list)",
         "For every key we keep a list of (timestamp, value) pairs. Timestamps only go up, so each list stays "
         "**sorted by time** without any extra work."),
        ("self.data[key].append((timestamp, value))",
         "Append ({timestamp}, `{value}`) to the list for `{key}`.", {"data.cur": "key"}),
        ("left, right = 0, len(values) - 1",
         "We want the entry with the **latest timestamp that is ≤ {timestamp}**. The list is sorted by "
         "timestamp, so binary-search it."),
        ("mid = left + (right - left) // 2", "The middle entry (index {mid}) has timestamp {values[mid][0]}."),
        ("return values[mid][1]",
         "That is exactly the timestamp asked for. Return its value `{_ret}`.", {"values.good": "mid"}),
        ("left = mid + 1",
         "{values[mid][0]} ≤ {timestamp}: this entry is old enough to be the answer, but a later one might be "
         "too. Look right: `left` = {left}."),
        ("right = mid - 1",
         "{values[mid][0]} > {timestamp}: this entry was set too late. Look left: `right` = {right}."),
        ("return values[right][1]",
         "The search is over and `right` = {right} rests on the last entry that is not newer than {timestamp}. "
         "Return its value `{_ret}`.",
         {"values.good": "right"}),
        ('return ""',
         "`right` fell off the left edge: every entry is newer than {timestamp}, so nothing had been set yet. "
         "Return an empty string."),
    ],
    time=("O(log n) per get", "`set` appends in O(1); `get` binary-searches the n entries of one key."),
    space=("O(n)", "Every value ever set is stored."),
    tests=[
        (["TimeMap()", "set('foo', 'bar', 1)", "get('foo', 1)", "get('foo', 3)", "set('foo', 'bar2', 4)",
          "get('foo', 4)", "get('foo', 5)", "get('zzz', 5)"],
         [None, None, "bar", "bar", None, "bar2", "bar2", ""]),
    ],
)

lesson(
    "median-of-two-sorted-arrays",
    pattern="Binary search on the partition",
    statement="""Given two **sorted** arrays `nums1` and `nums2`, return the median of all their
    numbers together. The required running time is O(log(m + n)), so the arrays cannot simply be
    merged.""",
    args="nums1=[1, 3, 8], nums2=[2, 5, 9]",
    expected=4.0,
    why="Together the numbers are 1, 2, 3, 5, 8, 9. The two middle ones are 3 and 5, and their average is 4.",
    idea=[
        "The median splits all the numbers into a **left half** and a **right half** of equal size, with everything on the left ≤ everything on the right.",
        "Cut `nums1` at some point; the cut in `nums2` is then forced, because the left side must hold exactly half of all the numbers. So there is only one thing to search for: where to cut `nums1`.",
        "A cut is correct when the last left number of each array is ≤ the first right number of the *other* array. If `nums1`'s left part is too big, move its cut left; otherwise move it right. That is a binary search on the shorter array.",
    ],
    views=[
        Arr("nums1", tones={"win": "range(partition1)"}, rng=("0", "partition1 - 1", "left part")),
        Arr("nums2", tones={"win": "range(partition2)"}, rng=("0", "partition2 - 1", "left part")),
        Vars("partition1", "partition2", "maxLeft1", "minRight1", "maxLeft2", "minRight2"),
    ],
    notes=[
        ("m, n = len(nums1), len(nums2)",
         "We cut **both** arrays so that the two left parts together hold half of all {m + n} numbers. If every "
         "left number is ≤ every right number, the median sits exactly at the cut."),
        ("partition2 = (m + n + 1) // 2 - partition1",
         "Try cutting `nums1` after {plural(partition1, 'number')}. The left side needs {(m + n + 1) // 2} numbers "
         "in total, so `nums2` must be cut after {partition2}."),
        ("minRight2 = float(",
         "Next to the cuts: `nums1` is split {maxLeft1} | {minRight1}, and `nums2` is split {maxLeft2} | {minRight2}."),
        ("if maxLeft1 <= minRight2 and maxLeft2 <= minRight1", dict(
            yes="{maxLeft1} ≤ {minRight2} and {maxLeft2} ≤ {minRight1}: every left number is ≤ every right number. "
                "The cut is **correct**.",
            no=[
                ("maxLeft1 > minRight2",
                 "{maxLeft1} > {minRight2}: a number in `nums1`'s left part is too big to be on the left. "
                 "Its cut is too far **right**."),
                (None,
                 "{maxLeft2} > {minRight1}: `nums2`'s left part holds a number bigger than one on the right of "
                 "`nums1`. The cut in `nums1` is too far **left**."),
            ])),
        ("low = partition1 + 1", "Move the cut in `nums1` to the right: `low` = {low}."),
        ("return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2",
         "There are {m + n} numbers (even), so the median is the average of the two middle ones: the largest on "
         "the left, max({maxLeft1}, {maxLeft2}) = {max(maxLeft1, maxLeft2)}, and the smallest on the right, "
         "min({minRight1}, {minRight2}) = {min(minRight1, minRight2)} → **{_ret}**."),
    ],
    time=("O(log(min(m, n)))", "The binary search runs only over cut positions of the shorter array."),
    space=("O(1)", "A handful of numbers."),
    tests=[("nums1=[1, 3], nums2=[2]", 2.0), ("nums1=[1, 2], nums2=[3, 4]", 2.5), ("nums1=[], nums2=[1]", 1.0),
           ("nums1=[2, 5, 9], nums2=[1, 3, 8]", 4.0), ("nums1=[4, 5, 6, 7], nums2=[1, 2]", 4.5)],
)

# end of c05_binary_search
