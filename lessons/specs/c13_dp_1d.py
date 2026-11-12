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
