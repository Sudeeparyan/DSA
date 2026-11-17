"""1-D Dynamic Programming."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "climbing-stairs",
    pattern="DP on the last move (Fibonacci)",
    statement="""You are climbing a staircase with `n` stairs. Each move you can climb **1 or 2**
    stairs. In how many distinct ways can you reach the top?""",
    args="n=5",
    expected=8,
    why="The counts for stairs 1 to 5 are 1, 2, 3, 5, 8 — each is the sum of the two before it.",
    picture="""Picture standing on any stair. Your last move got you there from either one stair below or two
    stairs below. So the number of ways to reach a stair is the ways to reach the stair below plus
    the ways to reach the stair two below. Work upward from the bottom, remembering just the last
    two answers: each new answer is their sum.""",
    idea=[
        "Think about the **last move** that lands on stair `i`. It was either a single step from stair `i − 1` or a double step from stair `i − 2` — there is no other possibility.",
        "So every way to reach stair `i − 1` and every way to reach stair `i − 2` gives exactly one way to reach stair `i`: `ways(i) = ways(i − 1) + ways(i − 2)`.",
        "Start from the two obvious answers (stair 1: 1 way, stair 2: 2 ways) and work upward. Only the last two values are ever needed, so two variables are enough.",
    ],
    init={"ways": "[1, 2]"},
    views=[
        Arr("list(range(1, n + 1))", id="stairs", bars=True, idx=False, title="stairs 1 … n",
            tones={"cur": "i - 1", "alt": "[i - 2, i - 3]"}),
        Arr("ways + ['?'] * (n - len(ways))", id="ways", idx=False, title="ways to reach each stair",
            tones={"good": "len(ways) - 1"}),
        Vars("prev1", "prev2", "current"),
    ],
    notes=[
        ("if n <= 2", dict(
            yes="With {n} stair(s) the answer is simply {n}.",
            no="n = {n} is more than 2, so build the answer up from the small cases.")),
        ("prev2 = 2",
         "Stair 1 can be reached in **1** way (one single step). Stair 2 in **2** ways (1 + 1, or one double step). "
         "`prev1` and `prev2` always hold the counts for the two stairs just below the one we are working on."),
        ("current = prev1 + prev2", dict(
            post="Stair {i}: the last move came from stair {i - 1} ({plural(prev2, 'way')}) or from stair {i - 2} ({plural(prev1, 'way')}). "
                 "Together {prev1} + {prev2} = **{current}** ways.",
            save={"ways": "ways + [current]"})),
        ("prev1, prev2 = prev2, current",
         "Slide the window up by one stair: `prev1` = {prev1} (stair {i - 1}) and `prev2` = {prev2} (stair {i})."),
        ("return prev2", "`prev2` now holds the count for stair {n}: **{prev2}** ways."),
    ],
    say={
        "def climbStairs": (
            "The function we must write. It gets the number of stairs `n` and returns how many "
            "different ways there are to climb them."
        ),
        "if n <= 2": (
            "With 1 or 2 stairs the answer is simply `n`: one way to climb 1 stair, two ways to "
            "climb 2."
        ),
        "return n": "So return `n`.",
        "prev1 = 1": "The number of ways to reach stair 1: just one.",
        "prev2 = 2": "The number of ways to reach stair 2: two (1 + 1, or a single 2).",
        "for i in range(3, n + 1)": "Work up through stairs 3, 4, … up to `n`.",
        "current = prev1 + prev2": (
            "Ways to reach this stair = ways to reach the stair two below + ways to reach the "
            "stair just below."
        ),
        "prev1, prev2 = prev2, current": (
            "Move up one stair: the last two answers are now the old `prev2` and the new "
            "`current`."
        ),
        "return prev2": "`prev2` now holds the number of ways to reach stair `n`.",
    },
    time=("O(n)", "One addition per stair."),
    space=("O(1)", "Only the last two counts are kept."),
    tests=[("n=1", 1), ("n=2", 2), ("n=3", 3), ("n=10", 89), ("n=45", 1836311903)],
)

lesson(
    "min-cost-climbing-stairs",
    pattern="DP: cheapest way to stand on each step",
    statement="""`cost[i]` is the price of stepping on stair `i`. After paying it you may climb **one
    or two** stairs. You may start on stair 0 or stair 1. Return the minimum total cost to reach
    the top (the floor just past the last stair).""",
    args="cost=[10, 15, 20, 5, 30]",
    expected=20,
    why="Start on stair 1 (pay 15), jump to stair 3 (pay 5), then jump over stair 4 to the top: 15 + 5 = 20.",
    picture="""Picture a price tag on every stair. To stand on a stair you pay its price, arriving from one or
    two stairs below, so the cheapest way to stand there is its price plus the cheaper of those two.
    Work up from the bottom, writing each answer into a row of boxes. The top is reached from one of
    the last two stairs, so the answer is the cheaper of those two boxes.""",
    idea=[
        "Let `dp[i]` be the cheapest total for **standing on stair i** (its own cost included).",
        "You arrive on stair `i` from stair `i − 1` or stair `i − 2`. Come from whichever was cheaper, then pay `cost[i]`: `dp[i] = min(dp[i − 1], dp[i − 2]) + cost[i]`.",
        "The top is reached from either of the last two stairs for free, so the answer is the smaller of their totals.",
    ],
    views=[
        Arr("cost", ptrs=["i"]),
        Arr("dp", title="dp[i] = cheapest total to stand on stair i"),
    ],
    notes=[
        ("dp = [0] * n", "`dp[i]` will hold the cheapest total cost to be standing on stair i."),
        ("dp[0] = cost[0]", "You may start on stair 0: the only cost is the stair itself, {cost[0]}.",
         {"dp.good": "0", "cost.cur": "0"}),
        ("dp[1] = cost[1]", "You may also start directly on stair 1: cost {cost[1]}.",
         {"dp.good": "1", "cost.cur": "1"}),
        ("dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i]",
         "Stair {i} is reached from stair {i - 1} (total {dp[i - 1]}) or stair {i - 2} (total {dp[i - 2]}). "
         "Come from the cheaper one and pay this stair: {min(dp[i - 1], dp[i - 2])} + {cost[i]} = **{dp[i]}**.",
         {"dp.alt": "[i - 1, i - 2]", "dp.good": "i"}),
        ("return min(dp[n - 1], dp[n - 2])",
         "The top lies just past the last stair. It can be reached from stair {n - 1} (total {dp[n - 1]}) or from "
         "stair {n - 2} (total {dp[n - 2]}) without paying anything more. The cheaper one: **{_ret}**.",
         {"dp.alt": "[n - 1, n - 2]"}),
    ],
    say={
        "def minCostClimbingStairs": (
            "The function we must write. It gets the price `cost` of each stair and returns the "
            "cheapest way to the top."
        ),
        "n = len(cost)": "The number of stairs.",
        "if n <= 1": "With at most one stair, you can step straight to the top from the start.",
        "return 0": "So it costs nothing.",
        "dp = [0] * n": (
            "A row of boxes: `dp[i]` will be the cheapest total for standing on stair `i`."
        ),
        "dp[0] = cost[0]": "Starting on stair 0 costs just its own price.",
        "dp[1] = cost[1]": "Starting on stair 1 costs just its own price.",
        "for i in range(2, n)": "Fill in the rest of the boxes, from stair 2 up.",
        "dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i]": (
            "To stand on stair `i`, arrive from the cheaper of the two stairs below it, then pay "
            "this stair's price."
        ),
        "return min(dp[n - 1], dp[n - 2])": (
            "The top is one step above the last stair or two above the one before it: return the "
            "cheaper of those two totals."
        ),
    },
    time=("O(n)", "One pass over the stairs."),
    space=("O(n)", "The dp array (two variables would be enough, since only the last two entries are used)."),
    tests=[
        ("cost=[10, 15, 20]", 15),
        ("cost=[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]", 6),
        ("cost=[0, 0]", 0),
        ("cost=[5, 3]", 3),
    ],
)

lesson(
    "house-robber",
    pattern="DP: rob this house or skip it",
    statement="""`nums[i]` is the money in house `i` along a street. Robbing two **adjacent** houses
    triggers the alarm. Return the maximum amount you can rob.""",
    args="nums=[2, 7, 9, 3, 1]",
    expected=12,
    why="Rob houses 0, 2 and 4: 2 + 9 + 1 = 12. No two of them are neighbours.",
    picture="""Picture walking down the street, deciding house by house. At each house there are two choices:
    rob it and add the best total from two houses back (the house just before must be skipped), or
    skip it and keep the best total up to the house just before. A row of boxes remembers the best
    total up to each house, and each new box needs only the two before it.""",
    idea=[
        "Go along the street and let `dp[i]` be the most money obtainable from houses `0 … i`.",
        "For house `i` there are only two choices. **Rob it**: house `i − 1` is then forbidden, so add the best of houses `0 … i − 2`. **Skip it**: keep the best of houses `0 … i − 1`.",
        "`dp[i] = max(dp[i − 2] + nums[i], dp[i − 1])`. The last entry is the answer.",
    ],
    views=[
        Arr("nums", ptrs=["i"], bars=True, title="nums  (money in each house)"),
        Arr("dp", title="dp[i] = best loot from houses 0 … i"),
    ],
    notes=[
        ("dp[0] = nums[0]", "With only house 0 available, rob it: {nums[0]}.", {"dp.good": "0", "nums.cur": "0"}),
        ("dp[1] = max(nums[0], nums[1])",
         "With houses 0 and 1 — neighbours, so only one of them — take the richer: max({nums[0]}, {nums[1]}) = **{dp[1]}**.",
         {"dp.good": "1", "nums.cur": "[0, 1]"}),
        ("dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])", [
            ("dp[i] > dp[i - 1]",
             "House {i} holds {nums[i]}. **Rob it**: house {i - 1} must be skipped, so add the best up to house {i - 2}: "
             "{dp[i - 2]} + {nums[i]} = {dp[i - 2] + nums[i]}. **Skip it**: keep {dp[i - 1]}. Robbing wins → `dp[{i}]` = **{dp[i]}**."),
            (None,
             "House {i} holds {nums[i]}. **Rob it**: {dp[i - 2]} + {nums[i]} = {dp[i - 2] + nums[i]}. "
             "**Skip it**: keep {dp[i - 1]}. Skipping is at least as good → `dp[{i}]` = **{dp[i]}**."),
        ], {"dp.alt": "[i - 2, i - 1]", "dp.good": "i"}),
        ("return dp[-1]", "The last entry covers the whole street: the most that can be robbed is **{_ret}**.",
         {"dp.good": "-1"}),
    ],
    say={
        "def rob": (
            "The function we must write. It gets the money in each house, `nums`, and returns the"
            " most that can be robbed."
        ),
        "n = len(nums)": "The number of houses.",
        "if n == 0": "Are there no houses?",
        "return 0": "Then nothing can be robbed.",
        "if n == 1": "Is there only one house?",
        "return nums[0]": "Then rob it.",
        "dp = [0] * n": "A row of boxes: `dp[i]` will be the most money from houses 0 to `i`.",
        "dp[0] = nums[0]": "With only the first house, rob it.",
        "dp[1] = max(nums[0], nums[1])": (
            "With the first two, rob whichever has more (not both: they are neighbours)."
        ),
        "for i in range(2, n)": "Fill in the rest of the boxes, house by house.",
        "dp[i] = max(dp[i - 2] + nums[i], dp[i - 1])": (
            "Either rob this house and add the best from two houses back, or skip it and keep the"
            " best up to the house before. Take the better."
        ),
        "return dp[-1]": "The last box (`[-1]`) holds the best total for the whole street.",
    },
    time=("O(n)", "One pass over the houses."),
    space=("O(n)", "The dp array (two variables would do, since only the last two entries are read)."),
    tests=[("nums=[1, 2, 3, 1]", 4), ("nums=[5]", 5), ("nums=[2, 1, 1, 2]", 4), ("nums=[0, 0, 0]", 0), ("nums=[]", 0)],
)

lesson(
    "house-robber-ii",
    pattern="Circular street = two straight-line problems",
    statement="""Same rule as House Robber — never rob two adjacent houses — but now the houses
    stand in a **circle**, so the first and the last house are neighbours too. Return the maximum
    amount you can rob.""",
    pre="""
    def _line(houses):
        prev = curr = 0
        for x in houses:
            prev, curr = curr, max(prev + x, curr)
        return curr
    """,
    args="nums=[2, 7, 9, 3, 1]",
    expected=11,
    why="On a straight street 2 + 9 + 1 = 12 would work, but in a circle house 0 and house 4 are neighbours. The best is 2 + 9 = 11.",
    picture="""Picture the same street bent into a circle, so the first and the last house are neighbours and
    can never both be robbed. Solve it as two ordinary streets: one without the first house, one
    without the last. Each is the plain House Robber problem, and the better of the two answers is
    the answer for the circle.""",
    idea=[
        "The only new rule: the first and the last house cannot **both** be robbed.",
        "So one of them is certainly left alone. Case A: house 0 is left out → an ordinary straight street of houses `1 … n − 1`. Case B: the last house is left out → a straight street of houses `0 … n − 2`.",
        "Solve both with the ordinary House Robber (here with two variables instead of an array) and return the larger result.",
    ],
    views=[
        Arr("_args['nums']", id="houses", bars=True,
            title="nums  (a circle: the last house is next to the first)",
            ptrs={"num": ("(1 if not _done('houseRobber', 'nums') else 0) + i_num", "_depth == 2")},
            rng=("(1 if not _done('houseRobber', 'nums') else 0) if _depth == 2 else None",
                 "(1 if not _done('houseRobber', 'nums') else 0) + len(nums) - 1 if _depth == 2 else None",
                 "this run", "win")),
        Vars("prev", "curr"),
    ],
    notes=[
        ("if len(nums) == 1", dict(
            yes="There is a single house: rob it.",
            no="The street is a circle, so house 0 and house {len(nums) - 1} are neighbours — they can never both be robbed. "
               "Split into two straight-line problems: one **without house 0**, one **without the last house**.")),
        ("curr = 0", [
            ("not _done('houseRobber', 'nums')",
             "**Run 1 — leave out house 0**: houses 1 … {len(_args['nums']) - 1} form a straight street {nums}. "
             "`curr` is the best loot so far, `prev` the best loot not using the previous house."),
            (None,
             "**Run 2 — leave out the last house**: houses 0 … {len(_args['nums']) - 2} form a straight street {nums}. "
             "Same procedure."),
        ]),
        ("prev = temp",
         "House with {num}. **Rob it**: {was.prev} + {num} = {was.prev + num} (best without the previous house, plus this one). "
         "**Skip it**: {prev}. Keep the larger → `curr` = **{curr}**."),
        ("return curr", "This run's best: **{curr}**."),
        ("return max(houseRobber(nums[1:]), houseRobber(nums[:-1]))",
         "Without house 0 the best is {_line(nums[1:])}; without the last house it is {_line(nums[:-1])}. "
         "The answer is the larger: **{_ret}**."),
    ],
    allow_unused=True,
    say={
        "def rob": (
            "The function we must write. It gets the money in each house of the circle and "
            "returns the most that can be robbed."
        ),
        "def houseRobber": (
            "A helper: the plain House Robber answer for houses standing in a line."
        ),
        "n = len(nums)": "The number of houses in this line.",
        "if n == 0": "Are there no houses?",
        "return 0": "Then nothing can be robbed.",
        "if n == 1": "Is there only one house?",
        "return nums[0]@1": "Then rob it.",
        "prev = 0": "The best total up to two houses back.",
        "curr = 0": "The best total up to the house just before.",
        "for num in nums": "Go along the houses; `num` is the money in this one.",
        "temp = curr": "Keep the old `curr` for a moment.",
        "curr = max(prev + num, curr)": (
            "Rob this house (plus the best from two back) or skip it (keep the best so far): take"
            " the better."
        ),
        "prev = temp": "Move along: the old best-so-far becomes the best from two back.",
        "return curr": "The best total for this line of houses.",
        "if len(nums) == 1": "Is there only one house in the whole circle?",
        "return nums[0]@2": "Then rob it: it has no neighbours to worry about.",
        "return max(houseRobber(nums[1:]), houseRobber(nums[:-1]))": (
            "Solve two lines, one without the first house (`nums[1:]`) and one without the last "
            "(`nums[:-1]`). The better answer wins."
        ),
    },
    time=("O(n)", "Two passes over the houses."),
    space=("O(n)", "The two slices; the robbing itself uses only two variables."),
    tests=[("nums=[2, 3, 2]", 3), ("nums=[1, 2, 3, 1]", 4), ("nums=[1, 2, 3]", 3), ("nums=[7]", 7), ("nums=[1, 2]", 2)],
)

lesson(
    "longest-palindromic-substring",
    pattern="Expand around every centre",
    statement="""Given a string `s`, return the longest substring of `s` that is a **palindrome**
    (reads the same forwards and backwards).""",
    args="s='babad'",
    expected="bab",
    why="'bab' is a palindrome of length 3. ('aba' is just as long; this code keeps the first one it finds.)",
    picture="""Picture every palindrome growing outward from its middle, like ripples: `aba` grows from the
    `b`, and `abba` grows from the gap between the two `b`s. So stand at every possible middle, each
    letter and each gap between two letters, and grow outward while the letters on both sides match.
    Keep the longest palindrome you grow.""",
    idea=[
        "A palindrome is symmetric around its **centre**. So instead of testing every substring, pick a centre and grow outward as long as the two ends match.",
        "A palindrome of odd length has a letter as its centre (`aba`); one of even length has a gap between two letters as its centre (`abba`). Try both kinds at every position: 2n − 1 centres.",
        "Each expansion stops at the first mismatch (or at the edge of the string). Keep the longest palindrome found.",
    ],
    views=[
        Arr("s", ptrs={"left": ("left", "_depth == 2"), "right": ("right", "_depth == 2"), "i": ("i", "_depth == 1")},
            rng=("left + 1 if _depth == 2 else None", "right - 1 if _depth == 2 else None", "palindrome", "good")),
        Vars("longest"),
    ],
    notes=[
        ('longest = ""', "`longest` will hold the longest palindrome found so far."),
        ("while left >= 0 and right < len(s) and s[left] == s[right]", dict(
            yes=[
                ("left == right", "Centre on the letter `{s[left]}` (index {left}). A single letter is always a palindrome — now grow outward."),
                (None, "`s[{left}]` and `s[{right}]` are both `{s[left]}`: the ends match, so `{s[left:right + 1]}` is a palindrome. Grow outward again."),
            ],
            no=[
                ("right - left == 1 and right >= len(s)", "Nothing follows index {left}, so there is no even-length centre here."),
                ("left < 0 or right >= len(s)", "The expansion would leave the string → stop. This centre gives `{s[left + 1:right]}`."),
                ("right - left == 1", "Centre on the gap between index {left} and {right}: `{s[left]}` ≠ `{s[right]}`, so there is no even-length palindrome here."),
                (None, "`s[{left}]` = `{s[left]}` and `s[{right}]` = `{s[right]}` differ → stop. This centre gives `{s[left + 1:right]}`."),
            ])),
        ("longest = palindrome1",
         "`{palindrome1}` (length {len(palindrome1)}) is longer than the best so far → `longest` = `{longest}`."),
        ("longest = palindrome2",
         "`{palindrome2}` (length {len(palindrome2)}) is longer than the best so far → `longest` = `{longest}`."),
        ("return longest", "Every centre has been tried. The longest palindrome is **`{longest}`**."),
    ],
    allow_unused=True,
    say={
        "def longestPalindrome": (
            "The function we must write. It gets the text `s` and returns its longest palindrome."
        ),
        "def expandAroundCenter": (
            "A helper that grows a palindrome outward from a middle between `left` and `right`, "
            "and returns the longest one found there."
        ),
        "while left >= 0 and right < len(s) and s[left] == s[right]": (
            "Are both ends still inside the text, and do their letters match?"
        ),
        "left -= 1": "Then grow: move the left end one step outward.",
        "right += 1": "And the right end one step outward.",
        "return s[left + 1 : right]": (
            "The ends have gone one step too far, so the palindrome is the text from `left + 1` "
            "up to just before `right`."
        ),
        "if len(s) < 2": "Is the text shorter than 2 letters?",
        "return s@2": "Then the whole text is its own longest palindrome.",
        'longest = ""': "The longest palindrome found so far.",
        "for i in range(len(s))": "Try every position as a middle.",
        "palindrome1 = expandAroundCenter(i, i)": (
            "A palindrome of odd length has one middle letter: grow from `i` itself."
        ),
        "if len(palindrome1) > len(longest)": "Is it longer than the best so far?",
        "longest = palindrome1": "Then keep it.",
        "palindrome2 = expandAroundCenter(i, i + 1)": (
            "A palindrome of even length has its middle between two letters: grow from between "
            "`i` and `i + 1`."
        ),
        "if len(palindrome2) > len(longest)": "Is that one longer than the best so far?",
        "longest = palindrome2": "Then keep it.",
        "return longest": "Return the longest palindrome.",
    },
    time=("O(n²)", "2n − 1 centres, and each expansion can run across the whole string."),
    space=("O(n)", "Every expansion hands back its palindrome as a new string of up to n characters. "
                   "(Returning the two indexes instead would need only O(1).)"),
    tests=[("s='cbbd'", "bb"), ("s='a'", "a"), ("s='ac'", "a"), ("s='racecar'", "racecar"), ("s='abba'", "abba")],
)

lesson(
    "palindromic-substrings",
    pattern="Expand around every centre and count",
    statement="""Given a string `s`, return the **number** of substrings that are palindromes.
    Substrings at different positions count separately, even if they consist of the same letters.""",
    args="s='abba'",
    expected=6,
    why="The four single letters, plus 'bb' and 'abba'.",
    picture="""Picture every palindrome growing outward from its middle, one matching pair of letters at a
    time, where each step of growth is one more palindrome. So stand at every middle (each letter,
    and each gap between two letters), grow outward while the two ends match, and count every step.
    The total is the number of palindromic substrings.""",
    idea=[
        "Every palindrome has a centre: a letter (odd length) or a gap between two letters (even length).",
        "Grow outward from a centre while the two ends match. **Each successful step is one more palindrome** — a bigger one around the same centre.",
        "Do this for all 2n − 1 centres and add up the counts.",
    ],
    views=[
        Arr("s", ptrs={"left": ("left", "_depth == 2"), "right": ("right", "_depth == 2"), "i": ("i", "_depth == 1")},
            rng=("left + 1 if _depth == 2 else None", "right - 1 if _depth == 2 else None", "palindrome", "good")),
        Vars("total_palindromes", "count"),
    ],
    notes=[
        ("total_palindromes = 0", "`total_palindromes` adds up the palindromes found around every centre."),
        ("count += 1", [
            ("right - left == 2",
             "The single letter `{s[left + 1]}` (index {left + 1}) is a palindrome by itself. Count it, then try to grow outward."),
            (None,
             "The two ends match, so `{s[left + 1:right]}` is a palindrome. Count it ({count} around this centre) and try to grow further."),
        ]),
        ("while left >= 0 and right < len(s) and s[left] == s[right]", dict(
            no=[
                ("left < 0 or right >= len(s)", "The expansion would leave the string → stop."),
                (None, "`s[{left}]` = `{s[left]}` and `s[{right}]` = `{s[right]}` differ → stop."),
            ])),
        ("total_palindromes += expandAroundCenter(i, i)@1", dict(
            post="Centre on the letter at index {i}: {plural(total_palindromes - was.total_palindromes, 'palindrome')}. "
                 "Total so far: **{total_palindromes}**.")),
        ("total_palindromes += expandAroundCenter(i, i + 1)", dict(
            post="Centre on the gap between index {i} and {i + 1}: {plural(total_palindromes - was.total_palindromes, 'palindrome')}. "
                 "Total so far: **{total_palindromes}**.")),
        ("return total_palindromes", "All centres are done: **{total_palindromes}** palindromic substrings."),
    ],
    say={
        "def countSubstrings": (
            "The function we must write. It gets the text `s` and returns how many of its "
            "substrings are palindromes."
        ),
        "def expandAroundCenter": (
            "A helper that grows outward from a middle and counts the palindromes it passes."
        ),
        "count = 0": "Palindromes found from this middle so far.",
        "while left >= 0 and right < len(s) and s[left] == s[right]": (
            "Are both ends inside the text, and do their letters match? Then the text from `left`"
            " to `right` is a palindrome."
        ),
        "left -= 1": "Grow: move the left end one step outward.",
        "right += 1": "And the right end one step outward.",
        "count += 1": "Count the palindrome just found.",
        "return count": "Report how many were found from this middle.",
        "if not s": "Is the text empty?",
        "return 0": "Then there are none.",
        "total_palindromes = 0": "The total found so far.",
        "for i in range(len(s))": "Try every position as a middle.",
        "total_palindromes += expandAroundCenter(i, i)": (
            "Count the odd-length palindromes centred on letter `i`."
        ),
        "total_palindromes += expandAroundCenter(i, i + 1)": (
            "And the even-length ones centred between `i` and `i + 1`."
        ),
        "return total_palindromes": "Return the total.",
    },
    time=("O(n²)", "2n − 1 centres, each expanded up to n/2 times."),
    space=("O(1)", "A few counters and indices."),
    tests=[("s='abc'", 3), ("s='aaa'", 6), ("s='a'", 1), ("s=''", 0), ("s='racecar'", 10)],
)

lesson(
    "decode-ways",
    pattern="DP on the last one or two digits",
    statement="""Letters are encoded as numbers: `A → 1`, `B → 2`, … `Z → 26`. Given a string of
    digits `s`, return the number of ways to decode it into letters. A group may not have a leading
    zero (`06` is not `6`), and `0` alone is not a letter.""",
    args="s='11106'",
    expected=2,
    why='"1 1 10 6" (AAJF) and "11 10 6" (KJF). The 0 can only be used as part of "10".',
    picture="""Picture reading the digits from the left and asking at each point: in how many ways can the
    digits so far be read? The last piece is either one digit (any digit except 0 is a letter) or
    two digits (10 to 26 is a letter). So the ways up to here are the ways up to one digit back, if
    the last digit can stand alone, plus the ways up to two digits back, if the last two can stand
    together. A row of boxes keeps every count.""",
    idea=[
        "Let `dp[i]` be the number of ways to decode the **first i digits**.",
        "The last letter of such a decoding comes from the last digit alone (valid if it is 1–9) or from the last two digits (valid if they form 10–26).",
        "If the single digit is valid, every decoding of the first `i − 1` digits can be extended: add `dp[i − 1]`. If the pair is valid, add `dp[i − 2]`. A `0` therefore contributes nothing on its own.",
    ],
    views=[
        Arr("s", rng=("i - 2", "i - 1", "last two", "alt"), tones={"cur": "i - 1"}),
        Arr("dp", title="dp[i] = ways to decode the first i digits"),
        Vars("one_digit", "two_digits"),
    ],
    notes=[
        ("dp[0] = 1",
         "`dp[i]` counts the decodings of the first i digits. For zero digits there is exactly **1** way: decode nothing. "
         "(This makes the additions below work out.)",
         {"dp.good": "0"}),
        ("dp[1] = (", [
            ("dp[1] == 1", "The first digit `{s[0]}` is a letter by itself → `dp[1]` = 1."),
            (None, "The first digit is `0`, which is not a letter → `dp[1]` = 0."),
        ], {"dp.good": "1", "s.cur": "0"}),
        ("two_digits = int(s[i - 2 : i])",
         "Now the first {i} digits, `{s[:i]}`. Its last letter is made from the last digit alone (`{s[i - 1]}`) "
         "or from the last two digits (`{s[i - 2:i]}`)."),
        ("if one_digit != 0", dict(
            no="`0` on its own is not a letter, so this option adds nothing.")),
        ("dp[i] += dp[i - 1]",
         "`{one_digit}` alone is a letter. Every decoding of the first {plural(i - 1, 'digit')} can be extended by it: "
         "add `dp[{i - 1}]` = {dp[i - 1]} → `dp[{i}]` = {dp[i]}.",
         {"dp.alt": "i - 1", "dp.cur": "i"}),
        ("if 10 <= two_digits <= 26", dict(
            no="`{s[i - 2:i]}` is not between 10 and 26, so the last two digits do not form a letter. "
               "`dp[{i}]` stays **{dp[i]}**.",
            no_marks={"dp.good": "i"})),
        ("dp[i] += dp[i - 2]",
         "The pair `{s[i - 2:i]}` is a letter (10–26). Every decoding of the first {plural(i - 2, 'digit')} can be extended by it: "
         "add `dp[{i - 2}]` = {dp[i - 2]} → `dp[{i}]` = **{dp[i]}**.",
         {"dp.alt": "i - 2", "dp.good": "i"}),
        ("return dp[n]", "`dp[{n}]` covers the whole string: **{_ret}** ways to decode it.", {"dp.good": "n"}),
    ],
    say={
        "def numDecodings": (
            "The function we must write. It gets the digits `s` and returns in how many ways they"
            " can be read as letters."
        ),
        "n = len(s)": "The number of digits.",
        "dp = [0] * (n + 1)": (
            "A row of boxes: `dp[i]` will be the number of ways to read the first `i` digits."
        ),
        "dp[0] = 1": (
            "Zero digits can be read in exactly one way: as nothing. This makes the counting work"
            " out."
        ),
        "dp[1] = (": (
            "The first digit alone: one way if it is not `0` (no letter has the number 0), "
            "otherwise none."
        ),
        "for i in range(2, n + 1)": "Fill in the boxes for 2 digits, 3 digits, and so on.",
        "one_digit = int(s[i - 1])": "The last digit, as a number.",
        "two_digits = int(s[i - 2 : i])": "The last two digits together, as a number.",
        "if one_digit != 0": "Can the last digit stand alone as a letter (1 to 9)?",
        "dp[i] += dp[i - 1]": (
            "Then every way of reading the digits before it still works: add those ways."
        ),
        "if 10 <= two_digits <= 26": (
            "Can the last two digits stand together as a letter (10 to 26)?"
        ),
        "dp[i] += dp[i - 2]": "Then add every way of reading the digits before those two.",
        "return dp[n]": "The number of ways to read all the digits.",
    },
    time=("O(n)", "One pass over the digits."),
    space=("O(n)", "The dp array (the last two entries would be enough)."),
    tests=[("s='12'", 2), ("s='226'", 3), ("s='06'", 0), ("s='0'", 0), ("s='10'", 1), ("s='27'", 1), ("s='100'", 0)],
)

lesson(
    "coin-change",
    pattern="Unbounded knapsack: fewest coins for every amount",
    statement="""You have coins of the given denominations (as many of each as you like). Return the
    **fewest** coins needed to make up exactly `amount`, or `-1` if it cannot be done.""",
    args="coins=[1, 3, 4], amount=6",
    expected=2,
    why="3 + 3 = 6 uses two coins. (Greedy — always taking the largest coin — would give 4 + 1 + 1, three coins.)",
    picture="""Picture a row of boxes, one for each amount from 0 up to the target, each saying *the fewest
    coins that make this amount*. The box for 0 says 0. With a coin worth 3, an amount `i` can be
    made from amount `i − 3` plus that one coin, so its box may improve to *box `i − 3`, plus 1*.
    Try every coin on every amount, and the last box holds the answer, or stays *impossible*.""",
    idea=[
        "Taking the largest coin first can fail (see the example), so compute the best answer for **every** amount from 0 up to the target.",
        "`dp[a]` = fewest coins that add up to `a`. If the last coin used is `c`, the rest is the amount `a − c`, so `dp[a] = dp[a − c] + 1`.",
        "Try each coin as that last coin and keep the minimum. Amounts that cannot be made stay at ∞.",
    ],
    views=[
        Arr("coins", ptrs={"coin": "i_coin"}),
        Arr("dp", title="dp[a] = fewest coins that add up to amount a", ptrs=["i"]),
    ],
    notes=[
        ("dp = [float(", "`dp[a]` will hold the fewest coins needed for amount a. ∞ means *not possible (so far)*."),
        ("dp[0] = 0", "Amount 0 needs **0** coins.", {"dp.good": "0"}),
        ("for coin in coins", dict(
            yes="Now allow the coin **{coin}**. For every amount from {coin} upward: would using a {coin}-coin give a better result?")),
        ("dp[i] = min(dp[i], dp[i - coin] + 1)", [
            ("dp[i] < was.dp[i]",
             "Amount {i}: use a {coin}-coin, and the remaining {i - coin} needs {plural(dp[i - coin], 'coin')} → "
             "{dp[i - coin]} + 1 = **{dp[i]}**. Better than {was.dp[i]} → update."),
            (None,
             "Amount {i}: with a {coin}-coin it would take {dp[i - coin]} + 1 = {dp[i - coin] + 1} coins — "
             "not better than the {dp[i]} already known. Keep {dp[i]}."),
        ], {"dp.alt": "i - coin", "dp.good": "i"}),
        ('return dp[amount] if dp[amount] != float(', [
            ("dp[amount] != inf", "`dp[{amount}]` = **{dp[amount]}**: that is the fewest coins for the target amount."),
            (None, "`dp[{amount}]` is still ∞: the amount cannot be made with these coins → **-1**."),
        ], {"dp.good": "amount"}),
    ],
    say={
        "def coinChange": (
            "The function we must write. It gets the `coins` and the `amount`, and returns the "
            "fewest coins that make it, or -1."
        ),
        'dp = [float("inf")] * (amount + 1)': (
            "One box per amount from 0 to `amount`: the fewest coins that make it. Infinity means"
            " *not possible (yet)*."
        ),
        "dp[0] = 0": "Making 0 needs no coins.",
        "for coin in coins": "Try each coin in turn.",
        "for i in range(coin, amount + 1)": (
            "Go through every amount this coin fits into, from the coin's value up to `amount`."
        ),
        "dp[i] = min(dp[i], dp[i - coin] + 1)": (
            "Make amount `i` from amount `i − coin` plus this one coin, if that uses fewer coins "
            "than the best way known so far."
        ),
        'return dp[amount] if dp[amount] != float("inf") else -1': (
            "If the box for `amount` was filled, return it. If it still says infinity, the amount"
            " cannot be made: return -1."
        ),
    },
    time=("O(amount × coins)", "Every amount is checked once for every coin."),
    space=("O(amount)", "One dp entry per amount."),
    tests=[
        ("coins=[1, 2, 5], amount=11", 3),
        ("coins=[2], amount=3", -1),
        ("coins=[1], amount=0", 0),
        ("coins=[186, 419, 83, 408], amount=6249", 20),
    ],
)

lesson(
    "maximum-product-subarray",
    pattern="Track both the largest and the smallest product",
    statement="""Given an integer array `nums`, find the contiguous subarray with the **largest
    product** and return that product.""",
    args="nums=[2, -3, 4, -2]",
    expected=48,
    why="The whole array: 2 × (−3) × 4 × (−2) = 48. The two negative numbers cancel each other.",
    picture="""Picture walking along the numbers with two notes in your pocket: the biggest and the smallest
    product of a run that ends right here. You need the smallest one too, because a negative number
    flips signs: the most negative product, times a negative number, becomes the biggest. At each
    number, either start a fresh run there or extend the runs on your notes, and keep the best
    product seen anywhere.""",
    idea=[
        "For sums, remembering the best subarray *ending here* is enough. For products that fails: a **negative** number turns a very small (very negative) product into a very large one.",
        "So remember two values for subarrays ending at the current index: the **largest** and the **smallest** product.",
        "At a negative number the two swap roles. Then each is either extended by the current number or restarted from it. The answer is the largest `max_product` ever seen.",
    ],
    views=[
        Arr("nums", ptrs=["i"]),
        Vars("max_product", "min_product", "result"),
    ],
    notes=[
        ("max_product = min_product = result = nums[0]",
         "Start with the first number, {nums[0]}: it is the largest product, the smallest product and the best result so far.",
         {"nums.cur": "0"}),
        ("max_product, min_product = min_product, max_product",
         "`nums[{i}]` = {nums[i]} is **negative**. Multiplying by it flips the order — the smallest product becomes "
         "the largest. So swap the two first: `max_product` = {max_product}, `min_product` = {min_product}."),
        ("max_product = max(nums[i], max_product * nums[i])",
         "Largest product **ending at index {i}**: start fresh with {nums[i]}, or extend: {was.max_product} × {nums[i]} = "
         "{was.max_product * nums[i]}. The larger is **{max_product}**."),
        ("min_product = min(nums[i], min_product * nums[i])",
         "Smallest product ending here: {nums[i]} alone, or {was.min_product} × {nums[i]} = {was.min_product * nums[i]}. "
         "The smaller is **{min_product}** — worth keeping, because a later negative number can flip it into a big positive."),
        ("result = max(result, max_product)",
         "Best product seen anywhere: max({was.result}, {max_product}) = **{result}**."),
        ("return result", "The largest product of any contiguous subarray is **{result}**."),
    ],
    say={
        "def maxProduct": (
            "The function we must write. It gets the list `nums` and returns the largest product "
            "of a run of neighbouring numbers."
        ),
        "max_product = min_product = result = nums[0]": (
            "Start with the first number: it is the biggest product, the smallest product and the"
            " best answer so far."
        ),
        "for i in range(1, len(nums))": "Go through the rest of the numbers.",
        "if nums[i] < 0": "Is this number negative?",
        "max_product, min_product = min_product, max_product": (
            "Then multiplying by it will flip biggest and smallest, so swap the two notes first."
        ),
        "max_product = max(nums[i], max_product * nums[i])": (
            "The biggest product of a run ending here: start fresh at this number, or extend the "
            "biggest run by it."
        ),
        "min_product = min(nums[i], min_product * nums[i])": (
            "The smallest product of a run ending here, found the same way."
        ),
        "result = max(result, max_product)": "Keep the best product seen anywhere.",
        "return result": "Return the best product.",
    },
    time=("O(n)", "One pass over the array, with a constant amount of work per number."),
    space=("O(1)", "Three numbers."),
    tests=[("nums=[2, 3, -2, 4]", 6), ("nums=[-2, 0, -1]", 0), ("nums=[-2]", -2), ("nums=[-2, 3, -4]", 24),
           ("nums=[0, 2]", 2), ("nums=[-1, -2, -3]", 6)],
)

lesson(
    "word-break",
    pattern="DP over prefixes",
    statement="""Given a string `s` and a dictionary of words, return `True` if `s` can be cut into
    a sequence of dictionary words. A word may be used more than once.""",
    args='s="catsand", wordDict=["cats", "and", "cat"]',
    expected=True,
    why='"cats" + "and". (Starting with "cat" leaves "sand", which is not a word — the DP still finds the other cut.)',
    picture="""Picture marking the points in the text where a cut could go, with every piece before it being a
    real word. The very start is such a point. A later point `i` is one too if, from some earlier
    marked point `j`, the text between `j` and `i` is a dictionary word. Mark the points from left
    to right: the text can be broken up exactly when the very end gets marked.""",
    idea=[
        "Let `dp[i]` say whether the **first i letters** can be cut into dictionary words. `dp[0]` is True: the empty prefix needs no words.",
        "The first `i` letters can be cut if there is some position `j` where the part before it works (`dp[j]` is True) **and** the remaining piece `s[j:i]` is a word.",
        "Fill `dp` from left to right. `dp[len(s)]` answers the question for the whole string.",
    ],
    views=[
        Arr("s", rng=("0", "i - 1", "first i letters", "win")),
        Arr("dp", title="dp[i] = can the first i letters be cut into words?"),
        HMap("wordSet", title="wordSet"),
    ],
    notes=[
        ("dp[0] = True", "`dp[i]` answers: can the first i letters be cut into words? For 0 letters: yes, trivially.",
         {"dp.good": "0"}),
        ("for i in range(1, len(s) + 1)", dict(
            yes=[
                ("i == 1",
                 "Can the first letter, `{s[:i]}`, be cut into words? Look for a split point j: the part before j "
                 "must be cuttable (`dp[j]` is True), and the piece after it, `s[j:{i}]`, must be a word."),
                (None, "Can the first {i} letters, `{s[:i]}`, be cut into words? Try every split point j."),
            ])),
        ("dp[i] = True",
         "Split at j = {j}: `dp[{j}]` is True (`{show(s[:j])}` can be cut) and the rest `{s[j:i]}` is in the dictionary "
         "→ `dp[{i}]` = **True**.",
         {"s.good": "range(j, i)", "s.seen": "range(j)", "dp.alt": "j", "dp.good": "i", "wordSet.good": "s[j:i]"}),
        ("for j in range(i)", dict(
            no="No split point works for `{s[:i]}` → `dp[{i}]` stays False.",
            no_marks={"dp.bad": "i"})),
        ("return dp[len(s)]", "`dp[{len(s)}]` covers the whole string → **{_ret}**.", {"dp.good": "len(s)"}),
    ],
    say={
        "def wordBreak": (
            "The function we must write. It gets the text `s` and the words `wordDict`, and "
            "answers whether the text can be cut into dictionary words."
        ),
        "wordSet = set(wordDict)": (
            "Put the words in a set, so *is this a word?* is answered instantly."
        ),
        "dp = [False] * (len(s) + 1)": (
            "One box per cutting point: `dp[i]` says whether the first `i` letters can be cut "
            "into words."
        ),
        "dp[0] = True": "Before any letters, nothing needs cutting: the start is marked.",
        "for i in range(1, len(s) + 1)": "Look at each cutting point after the start.",
        "for j in range(i)": "Try every earlier point `j` as the start of the last word.",
        "if dp[j] and s[j:i] in wordSet": (
            "Can the letters before `j` be cut into words, and is the piece from `j` to `i` a "
            "word?"
        ),
        "dp[i] = True": "Then the first `i` letters can be cut into words too.",
        "break": "One way is enough: stop trying other values of `j`.",
        "return dp[len(s)]": "Can the whole text be cut into words?",
    },
    time=("O(n³)", "There are about n² pairs (j, i), and cutting out the piece `s[j:i]` and looking it up "
                   "costs up to O(n) more."),
    space=("O(n)", "The dp array (plus the word set)."),
    tests=[
        ('s="leetcode", wordDict=["leet", "code"]', True),
        ('s="applepenapple", wordDict=["apple", "pen"]', True),
        ('s="catsandog", wordDict=["cats", "dog", "sand", "and", "cat"]', False),
        ('s="a", wordDict=["b"]', False),
    ],
)

lesson(
    "longest-increasing-subsequence",
    pattern="DP: best subsequence ending at each index",
    statement="""Given an integer array `nums`, return the length of the longest **strictly
    increasing subsequence**. A subsequence keeps the original order but may skip elements.""",
    args="nums=[3, 1, 4, 2, 5]",
    expected=3,
    why="For example 1, 4, 5 (or 3, 4, 5, or 1, 2, 5). No increasing subsequence has four elements.",
    picture="""Picture each number asking: *what is the longest rising chain that ends with me?* A number can
    join the end of any chain that finishes with a smaller number before it, making that chain one
    longer. So each number looks back at every earlier, smaller number and extends the best chain it
    can. The longest chain anywhere is the answer.""",
    idea=[
        "Let `dp[i]` be the length of the longest increasing subsequence that **ends exactly at index i**. Alone, every element is a subsequence of length 1.",
        "The element before `nums[i]` in such a subsequence must be an earlier, **smaller** number `nums[j]`. Then `nums[i]` extends the best subsequence ending at `j`: length `dp[j] + 1`.",
        "Try every earlier `j` and keep the best. The answer is the largest value in `dp` — the subsequence may end anywhere.",
    ],
    views=[
        Arr("nums", ptrs=["i", "j"]),
        Arr("dp", title="dp[i] = longest increasing subsequence ending at index i"),
    ],
    notes=[
        ("dp = [1] * len(nums)", "Every number on its own is an increasing subsequence of length 1, so every `dp[i]` starts at 1."),
        ("for i in range(len(nums))", dict(
            yes=[
                ("i == 0", "Index 0 (value {nums[0]}) has nothing before it: `dp[0]` stays 1."),
                (None, "Index {i} (value {nums[i]}): which earlier, **smaller** numbers could come right before it?"),
            ],
            marks={"nums.cur": "i", "dp.cur": "i"})),
        ("if nums[i] > nums[j]", dict(
            no="`nums[{j}]` = {nums[j]} is not smaller than {nums[i]}, so {nums[i]} cannot follow it. Skip.",
            marks={"nums.cur": "i", "nums.alt": "j"})),
        ("dp[i] = max(dp[i], dp[j] + 1)", [
            ("dp[i] > was.dp[i]",
             "`nums[{j}]` = {nums[j]} < {nums[i]}: put {nums[i]} after the best subsequence ending at index {j} "
             "(length {dp[j]}) → length {dp[j] + 1}. Better than {was.dp[i]} → `dp[{i}]` = **{dp[i]}**."),
            (None,
             "`nums[{j}]` = {nums[j]} < {nums[i]}: extending the subsequence ending at index {j} gives length {dp[j] + 1} — "
             "not better than the {dp[i]} we already have."),
        ], {"nums.cur": "i", "nums.alt": "j", "dp.alt": "j", "dp.good": "i"}),
        ("return max(dp)", "The longest increasing subsequence may end at any index: the largest `dp` value is **{_ret}**.",
         {"dp.good": "dp.index(max(dp))"}),
    ],
    say={
        "def lengthOfLIS": (
            "The function we must write. It gets the list `nums` and returns the length of the "
            "longest rising subsequence."
        ),
        "if not nums": "Is the list empty?",
        "return 0": "Then the longest one has length 0.",
        "dp = [1] * len(nums)": (
            "One box per number: `dp[i]` is the longest rising chain that ends with `nums[i]`. "
            "Each number alone is a chain of 1."
        ),
        "for i in range(len(nums))": "Go through the numbers, one by one.",
        "for j in range(i)": "Look back at every number before it.",
        "if nums[i] > nums[j]": (
            "Is this number bigger than that earlier one? Then it can join the end of that one's "
            "chain."
        ),
        "dp[i] = max(dp[i], dp[j] + 1)": (
            "Joining makes a chain one longer than `dp[j]`. Keep it if it is the best for "
            "`nums[i]` so far."
        ),
        "return max(dp)": "The longest chain ending anywhere is the answer.",
    },
    time=("O(n²)", "Every pair (j, i) is compared once. (A patience-sorting variant with binary search reaches O(n log n).)"),
    space=("O(n)", "The dp array."),
    tests=[
        ("nums=[10, 9, 2, 5, 3, 7, 101, 18]", 4),
        ("nums=[0, 1, 0, 3, 2, 3]", 4),
        ("nums=[7, 7, 7, 7]", 1),
        ("nums=[5]", 1),
        ("nums=[]", 0),
    ],
)

lesson(
    "partition-equal-subset-sum",
    pattern="0/1 knapsack: which sums are reachable?",
    statement="""Given an array of positive integers `nums`, return `True` if it can be split into
    two subsets whose sums are **equal**.""",
    args="nums=[1, 5, 11, 5]",
    expected=True,
    why="{1, 5, 5} and {11} both sum to 11.",
    picture="""Picture splitting the numbers into two piles with equal sums: each pile must hold exactly half
    of the total. So the question becomes: can some of the numbers add up to that half? Keep a row
    of boxes, one for every sum from 0 to the half, ticked when that sum can be made. At first only
    0 is ticked. Each number then ticks every sum it can reach from an already ticked one. Going
    through the sums from the top down makes sure no number is used twice.""",
    idea=[
        "Two equal halves must each sum to `total / 2`. If the total is odd, that is impossible. Otherwise the question becomes: **can some of the numbers add up to exactly `total / 2`?** (The rest then automatically forms the other half.)",
        "Keep a table `dp[x]`: *can the numbers looked at so far reach the sum x?* Initially only 0 is reachable (take nothing).",
        "Each new number `num` makes `x` reachable whenever `x − num` already was. Going through the sums **from high to low** ensures the same number is not used twice.",
    ],
    views=[
        Arr("nums", ptrs={"num": "i_num"}),
        Arr("dp", title="dp[x] = can some of the numbers seen so far add up to x?",
            tones={"seen": "[x for x in range(len(dp)) if dp[x]]"}, ptrs=["i"]),
        Vars("total_sum", "target_sum"),
    ],
    notes=[
        ("if total_sum % 2 != 0", dict(
            yes="The total is {total_sum} — odd. Two equal whole-number halves are impossible → **False**.",
            no="The total is {total_sum}, so each half must sum to {total_sum // 2}. "
               "Question: can some of the numbers add up to exactly {total_sum // 2}?")),
        ("dp[0] = True", "`dp[x]` = *is the sum x reachable?* Before using any number only 0 is reachable (take nothing)."),
        ("for num in nums", dict(
            yes="Now allow the number **{num}**. Any reachable sum x makes x + {num} reachable too. "
                "The sums are scanned from {target_sum} downward, so {num} cannot be counted twice.")),
        ("dp[i] = dp[i] or dp[i - num]", dict(
            post="Sum {i - num} was reachable, so with {num} the sum **{i}** becomes reachable.",
            when="dp[i] and not was.dp[i]",
            marks={"dp.alt": "i - num", "dp.good": "i"})),
        ("return dp[target_sum]", [
            ("_ret", "`dp[{target_sum}]` is True: some numbers add up to {target_sum}, and the rest make up the other half → **True**."),
            (None, "`dp[{target_sum}]` is False: no subset sums to {target_sum} → **False**."),
        ], {"dp.good": "target_sum"}),
    ],
    say={
        "def canPartition": (
            "The function we must write. It gets the list `nums` and answers whether it splits "
            "into two piles with equal sums."
        ),
        "total_sum = sum(nums)": "Add up all the numbers.",
        "if total_sum % 2 != 0": "Is the total odd? (`%` gives the remainder after dividing.)",
        "return False": "Then it cannot be split into two equal whole halves.",
        "target_sum = total_sum // 2": "Each pile must add up to exactly half the total.",
        "dp = [False] * (target_sum + 1)": (
            "A row of boxes, one for every sum from 0 to `target_sum`: can some of the numbers "
            "add up to it?"
        ),
        "dp[0] = True": "A sum of 0 can always be made, by taking nothing.",
        "for num in nums": "Bring in the numbers one at a time.",
        "for i in range(target_sum, num - 1, -1)": (
            "Go through the sums from the top down to `num`. Going downwards stops this number "
            "from being used twice in one sum."
        ),
        "dp[i] = dp[i] or dp[i - num]": (
            "Sum `i` can be made if it already could, or if `i − num` could and this number is "
            "added to it."
        ),
        "return dp[target_sum]": "Can some of the numbers make exactly half the total?",
    },
    time=("O(n × sum)", "For every number, every sum up to total / 2 is checked once."),
    space=("O(sum)", "One boolean per possible sum."),
    tests=[
        ("nums=[1, 2, 3, 5]", False),
        ("nums=[1, 2, 5]", False),
        ("nums=[2, 2]", True),
        ("nums=[3, 3, 3, 4, 5]", True),
        ("nums=[100]", False),
    ],
)

# end of c13_dp_1d
