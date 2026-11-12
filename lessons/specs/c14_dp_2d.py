"""2-D Dynamic Programming."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "longest-common-subsequence",
    pattern="2-D DP over two prefixes",
    statement="""Given two strings, return the length of their **longest common subsequence**:
    the longest sequence of characters that appears in both strings in the same order (the
    characters do not have to be next to each other). Return 0 if there is none.""",
    args="text1='abcde', text2='ace'",
    expected=3,
    why='The longest common subsequence is "ace".',
    idea=[
        "Solve it for short prefixes first and build up: `dp[i][j]` = answer for the first `i` letters of text1 and the first `j` letters of text2.",
        "If the two current letters **match**, that letter extends the best answer of both shorter prefixes: `1 + diagonal`.",
        "If they **differ**, at least one of them is unused: take the better of *drop text1's letter* (cell above) and *drop text2's letter* (cell to the left).",
    ],
    views=[
        Grid("dp", title="dp[i][j] = LCS of text1[:i] and text2[:j]",
             rows="['∅'] + list(text1)", cols="['∅'] + list(text2)",
             ptrs={"i, j": "(i, j)"}),
    ],
    notes=[
        ("dp = [[0] * (n + 1) for _ in range(m + 1)]",
         "Build a table with one extra row and column for the **empty prefix** (∅). An empty string has "
         "nothing in common with anything, so that row and column stay 0."),
        ("dp[i][j] = dp[i - 1][j - 1] + 1",
         "`{text1[i - 1]}` == `{text2[j - 1]}` — a **match**. This letter can end the common subsequence, so take "
         "the best answer without both letters (diagonal: {dp[i - 1][j - 1]}) and add 1 → **{dp[i][j]}**.",
         {"dp.alt": "(i - 1, j - 1)", "dp.good": "(i, j)"}),
        ("dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])",
         "`{text1[i - 1]}` ≠ `{text2[j - 1]}`. One of them must be left out: skip `{text1[i - 1]}` (cell above: "
         "{dp[i - 1][j]}) or skip `{text2[j - 1]}` (cell on the left: {dp[i][j - 1]}). Keep the larger → **{dp[i][j]}**.",
         {"dp.alt": "[(i - 1, j), (i, j - 1)]", "dp.cur": "(i, j)"}),
        ("return dp[m][n]",
         "The bottom-right cell covers **all** of both strings: the longest common subsequence has length **{_ret}**.",
         {"dp.good": "(m, n)"}),
    ],
    time=("O(m · n)", "One table cell per pair of prefixes, each filled in O(1)."),
    space=("O(m · n)", "The table has (m + 1) × (n + 1) cells."),
    tests=[("text1='abc', text2='abc'", 3), ("text1='abc', text2='def'", 0), ("text1='bl', text2='yby'", 1)],
)

lesson(
    "unique-paths",
    pattern="Grid DP: paths from above + paths from the left",
    statement="""A robot starts in the top-left corner of an `m × n` grid and can only move **right
    or down**. How many different paths lead to the bottom-right corner?""",
    args="m=3, n=4",
    expected=10,
    why="Every path consists of 2 moves down and 3 moves right in some order: 5! / (2! · 3!) = 10.",
    idea=[
        "Let `dp[i][j]` be the number of paths from the start to cell `(i, j)`.",
        "The robot can enter a cell only **from above** or **from the left**. Every path to either of those cells extends to exactly one path into this cell, so `dp[i][j] = dp[i − 1][j] + dp[i][j − 1]`.",
        "Cells in the top row or the left column can be reached in exactly one way (straight along the edge), so they are 1.",
    ],
    views=[
        Grid("dp", title="dp[i][j] = number of paths from the top-left corner to (i, j)",
             ptrs={"i, j": "(i, j)"},
             tones={"seen": "[(a, b) for a in range(m) for b in range(n) if a == 0 or b == 0 or (a, b) <= (i, j)]"}),
    ],
    notes=[
        ("dp = [[1] * n for _ in range(m)]",
         "Fill the whole table with 1. For the **top row** and the **left column** that is already the final answer: "
         "there is exactly one way to get there — straight along the edge. The inner cells are computed next."),
        ("dp[i][j] = dp[i - 1][j] + dp[i][j - 1]",
         "Cell ({i}, {j}) is entered from above ({dp[i - 1][j]} paths) or from the left ({dp[i][j - 1]} paths): "
         "{dp[i - 1][j]} + {dp[i][j - 1]} = **{dp[i][j]}** paths.",
         {"dp.alt": "[(i - 1, j), (i, j - 1)]", "dp.good": "(i, j)"}),
        ("return dp[m - 1][n - 1]", "The bottom-right cell holds the answer: **{_ret}** paths.",
         {"dp.good": "(m - 1, n - 1)"}),
    ],
    time=("O(m · n)", "Each cell is filled once with one addition."),
    space=("O(m · n)", "The table (a single row would be enough, since only the row above is read)."),
    tests=[("m=3, n=7", 28), ("m=3, n=2", 3), ("m=1, n=1", 1), ("m=1, n=9", 1), ("m=7, n=3", 28)],
)

lesson(
    "best-time-to-buy-and-sell-stock-with-cooldown",
    pattern="State-machine DP: holding / just sold / resting",
    statement="""`prices[i]` is a stock's price on day `i`. You may buy and sell as often as you
    like, holding at most one share at a time — but after you **sell**, you must wait one day (a
    *cooldown*) before buying again. Return the maximum profit.""",
    args="prices=[1, 2, 3, 0, 2]",
    expected=3,
    why="Buy at 1, sell at 2, cooldown, buy at 0, sell at 2: (2 − 1) + (2 − 0) = 3.",
    idea=[
        "At the end of any day you are in exactly one of three situations: **holding** a share, having **just sold** today, or **resting** (no share, free to buy tomorrow).",
        "Track the best profit for each situation. Holding: keep holding, or buy today — but only coming from *resting*, never directly after a sale. Just sold: you were holding and sell today. Resting: you were already resting, or you sold yesterday.",
        "Each day's three values depend only on yesterday's three, so three variables are enough. At the end you should not be holding: the answer is the better of *just sold* and *resting*.",
    ],
    init={"tb": "[]"},
    views=[
        Arr("prices", ptrs=["i"], bars=True),
        Grid("[[cell(r[k]) for r in tb] + [''] * (len(prices) - len(tb)) for k in range(3)]", id="table",
             rows="['buy', 'sell', 'cool']", cols="list(range(len(prices)))", blank=['""'],
             title="best profit at the end of each day  (buy = holding, sell = just sold, cool = resting)",
             tones={"cur": "[(0, len(tb) - 1), (1, len(tb) - 1), (2, len(tb) - 1)]"}),
        Vars("buy", "sell", "cooldown"),
    ],
    notes=[
        ("cooldown = 0", dict(
            post="Day 0. **buy** (holding a share): buying costs {prices[0]}, so the profit is {buy}. "
                 "**sell** (just sold) and **cooldown** (resting, no share) are both 0 — nothing has happened yet.",
            save={"tb": "[(buy, sell, cooldown)]"})),
        ("new_buy = max(buy, cooldown - prices[i])",
         "Day {i}, price {prices[i]}. **Holding** tonight: either we already held a share ({buy}), or we buy today. "
         "Buying is allowed only from the resting state — never the day after a sale: {cooldown} − {prices[i]} = "
         "{cooldown - prices[i]}. Best: **{new_buy}**.",
         {"table.alt": "[(0, i - 1), (2, i - 1)]"}),
        ("new_sell = buy + prices[i]",
         "**Selling** today: the share we were holding (profit {buy}) is sold for {prices[i]} → **{new_sell}**.",
         {"table.alt": "(0, i - 1)"}),
        ("new_cooldown = max(cooldown, sell)",
         "**Resting** tonight: either we were already resting ({cooldown}), or we sold yesterday ({sell}) and today is "
         "the forced cooldown day. Best: **{new_cooldown}**.",
         {"table.alt": "[(1, i - 1), (2, i - 1)]"}),
        ("buy, sell, cooldown = new_buy, new_sell, new_cooldown", dict(
            post="Day {i} is settled: holding {buy}, just sold {sell}, resting {cooldown}.",
            save={"tb": "tb + [(buy, sell, cooldown)]"})),
        ("return max(sell, cooldown)",
         "At the end, holding an unsold share is never best. Take the better of *just sold* ({sell}) and "
         "*resting* ({cooldown}): **{_ret}**."),
    ],
    time=("O(n)", "One pass over the days."),
    space=("O(1)", "Three numbers carried from day to day."),
    tests=[("prices=[1]", 0), ("prices=[1, 2]", 1), ("prices=[5, 4, 3]", 0), ("prices=[1, 2, 4]", 3),
           ("prices=[6, 1, 3, 2, 4, 7]", 6), ("prices=[]", 0)],
)

lesson(
    "coin-change-ii",
    pattern="Unbounded knapsack: count combinations",
    statement="""Given coin denominations `coins` (unlimited supply of each) and an `amount`, return
    the number of **combinations** of coins that add up to `amount`. Order does not matter:
    `1 + 2` and `2 + 1` are the same combination.""",
    args="amount=5, coins=[1, 2, 5]",
    expected=4,
    why="5 = 5 = 2+2+1 = 2+1+1+1 = 1+1+1+1+1.",
    idea=[
        "Let `dp[a]` be the number of ways to make amount `a` using the coin types allowed so far. With no coins, only amount 0 can be made — in exactly one way.",
        "Introduce the coins **one type at a time**. With a new coin `c`, every way to make `a − c` gives one more way to make `a` (append one `c`): `dp[a] += dp[a − c]`.",
        "Because a coin type is finished before the next one starts, each combination is built in one fixed order of coin types — so `1 + 2` and `2 + 1` are not counted twice.",
    ],
    views=[
        Arr("coins", ptrs={"coin": "i_coin"}),
        Arr("dp", title="dp[a] = number of ways to make amount a with the coins allowed so far", ptrs=["i"]),
    ],
    notes=[
        ("dp[0] = 1", "There is exactly **1** way to make amount 0: take no coins. Every other amount has 0 ways so far.",
         {"dp.good": "0"}),
        ("for coin in coins", dict(
            yes="Now also allow coin **{coin}**. For every amount from {coin} upward, each way to make "
                "(amount − {coin}) gives one more way: append a {coin}-coin.")),
        ("dp[i] += dp[i - coin]",
         "Amount {i}: the {plural(dp[i - coin], 'way')} to make {i - coin} can each be extended by a {coin}-coin. "
         "{was.dp[i]} + {dp[i - coin]} = **{dp[i]}**.",
         {"dp.alt": "i - coin", "dp.good": "i"}),
        ("return dp[amount]", "`dp[{amount}]` = **{_ret}** combinations.", {"dp.good": "amount"}),
    ],
    time=("O(amount × coins)", "Every amount is updated once per coin type."),
    space=("O(amount)", "One counter per amount."),
    tests=[("amount=3, coins=[2]", 0), ("amount=10, coins=[10]", 1), ("amount=0, coins=[7]", 1),
           ("amount=500, coins=[1, 2, 5]", 12701)],
)

lesson(
    "target-sum",
    pattern="Turn signs into a subset-sum count",
    statement="""Put a `+` or a `−` in front of every number in `nums` and add everything up. Return
    the number of different sign assignments whose result is exactly `S`.""",
    args="nums=[1, 2, 1], S=2",
    expected=2,
    why="+1 +2 −1 = 2 and −1 +2 +1 = 2.",
    idea=[
        "Trying all sign patterns costs 2ⁿ. Look at it differently: the numbers with `+` have some sum P, those with `−` some sum N.",
        "We need `P − N = S`, and we know `P + N = total`. Adding the two equations: `P = (total + S) / 2`. So the task is: **count the subsets of `nums` that sum to P** (everything else gets a minus).",
        "That is a classic subset-sum count: `dp[x]` = number of subsets summing to `x`; each number `num` adds `dp[x − num]` to `dp[x]`, scanning `x` downward so a number is used at most once.",
    ],
    views=[
        Arr("nums", ptrs={"num": "i_num"}),
        Arr("dp", title="dp[x] = number of subsets (of the numbers seen so far) that sum to x", ptrs=["i"]),
        Vars("total_sum", "target"),
    ],
    notes=[
        ("if (total_sum + S) % 2 != 0 or total_sum < abs(S)", dict(
            yes="P = (total + S) / 2 would not be a whole number, or S is further away than the total can reach → **0** ways.",
            no="Call the sum of the `+` numbers P and the sum of the `−` numbers N. Then P − N = {S} and "
               "P + N = {total_sum}. Add them: 2P = {total_sum + S}, so **P = {(total_sum + S) // 2}**. "
               "New question: how many subsets of `nums` sum to {(total_sum + S) // 2}?")),
        ("dp[0] = 1", "`dp[x]` counts the subsets that sum to x. The empty subset sums to 0: **1** way.", {"dp.good": "0"}),
        ("for num in nums", dict(
            yes="Next number: **{num}**. Every subset that sums to x − {num} gives a new subset that sums to x by adding "
                "{num}. The sums are scanned from high to low so that {num} is not used twice.")),
        ("dp[i] += dp[i - num]", dict(
            post="Sum {i}: every subset that sums to {i - num} ({dp[i - num]} so far) can take {num} as well → "
                 "{was.dp[i]} + {dp[i - num]} = **{dp[i]}**.",
            when="dp[i - num] > 0",
            marks={"dp.alt": "i - num", "dp.good": "i"})),
        ("return dp[target]",
         "`dp[{target}]` = **{_ret}**: that many subsets can take the `+` sign so that the total comes out as {S}.",
         {"dp.good": "target"}),
    ],
    time=("O(n × sum)", "For each number, every sum up to P is updated once."),
    space=("O(sum)", "One counter per sum."),
    tests=[("nums=[1, 1, 1, 1, 1], S=3", 5), ("nums=[1], S=1", 1), ("nums=[1], S=2", 0),
           ("nums=[0, 0, 1], S=1", 4), ("nums=[100], S=-200", 0), ("nums=[1, 2, 3], S=-6", 1)],
)

lesson(
    "interleaving-string",
    pattern="2-D DP over prefixes of both strings",
    statement="""Return `True` if `s3` can be formed by **interleaving** `s1` and `s2`: merging them
    while keeping the letters of each string in their original order.""",
    args='s1="ab", s2="ac", s3="aacb"',
    expected=True,
    why="Take `a` from s2, `a` from s1, `c` from s2 and `b` from s1: together they spell `aacb`.",
    idea=[
        "Let `dp[i][j]` say whether the first `i` letters of `s1` and the first `j` letters of `s2` can be interleaved into the first `i + j` letters of `s3`.",
        "The last letter of that prefix of `s3` came either from `s1` or from `s2`. From `s1`: then `s1[i − 1]` must equal it and `dp[i − 1][j]` must be True. From `s2`: `s2[j − 1]` must equal it and `dp[i][j − 1]` must be True.",
        "The top row uses only `s2` and the left column only `s1`. The bottom-right cell covers all three strings completely.",
    ],
    views=[
        Grid("dp", title="dp[i][j]: can s1[:i] and s2[:j] be merged into s3[:i + j]?",
             rows="['∅'] + list(s1)", cols="['∅'] + list(s2)", vals={"T": "seen"}),
        Arr("s3", title="s3"),
    ],
    notes=[
        ("if m + n != p", dict(
            yes="The lengths do not add up ({m} + {n} ≠ {p}), so `s3` cannot be an interleaving → **False**.",
            no="The lengths fit: {m} + {n} = {p}. Now build the table.")),
        ("dp[0][0] = True", "Nothing from `s1` and nothing from `s2` form the empty prefix of `s3`: **True**.",
         {"dp.good": "(0, 0)"}),
        ("dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]",
         "Top row — only `s2` is used: `{s2[:j]}` must equal the start of `s3`, `{s3[:j]}`. "
         "The cell to the left is {dp[0][j - 1]}, and the new letters are `{s2[j - 1]}` and `{s3[j - 1]}` → **{dp[0][j]}**.",
         {"dp.alt": "(0, j - 1)", "dp.cur": "(0, j)", "s3.cur": "j - 1"}),
        ("dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]",
         "Left column — only `s1` is used: `{s1[:i]}` must equal the start of `s3`, `{s3[:i]}`. "
         "The cell above is {dp[i - 1][0]}, and the new letters are `{s1[i - 1]}` and `{s3[i - 1]}` → **{dp[i][0]}**.",
         {"dp.alt": "(i - 1, 0)", "dp.cur": "(i, 0)", "s3.cur": "i - 1"}),
        ("dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (", [
            ("dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]",
             "Cell ({i}, {j}): the letter to produce is `s3[{i + j - 1}]` = `{s3[i + j - 1]}`. Take it **from s1** "
             "(`{s1[i - 1]}` matches) — the rest is the cell above, which is True → **True**."),
            ("dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]",
             "Cell ({i}, {j}): the letter to produce is `s3[{i + j - 1}]` = `{s3[i + j - 1]}`. Take it **from s2** "
             "(`{s2[j - 1]}` matches) — the rest is the cell to the left, which is True → **True**."),
            (None,
             "Cell ({i}, {j}): the letter to produce is `s3[{i + j - 1}]` = `{s3[i + j - 1]}`. From s1 it would be "
             "`{s1[i - 1]}` (cell above: {dp[i - 1][j]}), from s2 `{s2[j - 1]}` (cell to the left: {dp[i][j - 1]}). "
             "Neither option works → **False**."),
        ], {"dp.alt": "[(i - 1, j), (i, j - 1)]", "dp.cur": "(i, j)", "s3.cur": "i + j - 1"}),
        ("return dp[m][n]", "The bottom-right cell uses all of `s1`, `s2` and `s3` → **{_ret}**.", {"dp.good": "(m, n)"}),
    ],
    time=("O(m · n)", "One cell per pair of prefix lengths."),
    space=("O(m · n)", "The table has (m + 1) × (n + 1) cells; one row would be enough, since only the row above is read."),
    tests=[
        ('s1="aabcc", s2="dbbca", s3="aadbbcbcac"', True),
        ('s1="aabcc", s2="dbbca", s3="aadbbbaccc"', False),
        ('s1="", s2="", s3=""', True),
        ('s1="a", s2="", s3="c"', False),
        ('s1="a", s2="b", s3="abc"', False),
    ],
)

lesson(
    "longest-increasing-path-in-a-matrix",
    pattern="DFS with memoisation",
    statement="""Given a matrix of integers, return the length of the longest path in which every
    step moves up, down, left or right to a cell with a **strictly larger** value.""",
    args="matrix=[[9, 9, 4], [6, 6, 8], [2, 1, 1]]",
    expected=4,
    why="1 → 2 → 6 → 9 (bottom middle, bottom left, middle left, top left).",
    idea=[
        "For a single cell, the longest increasing path **starting there** is 1 plus the best path starting at any larger neighbour.",
        "Paths only climb to larger values, so they can never loop — the recursion always ends.",
        "Many paths pass through the same cells, so **remember** each cell's answer (`dp`). Every cell is then solved exactly once, and the overall answer is the largest value in `dp`.",
    ],
    views=[
        Grid("matrix", tones={"cur": "(i, j)", "alt": "(x, y)"}),
        Grid("dp", title="dp = longest path starting at each cell", blank=["-1"]),
        Calls("dfs", "dfs({i}, {j})  value {matrix[i][j]}"),
        Vars("max_path"),
    ],
    notes=[
        ("max_path = 0", "`dp` remembers the longest path starting at each cell (empty = not computed yet). Start a search from every cell."),
        ("if dp[i][j] != -1", dict(
            yes="({i}, {j}) was already solved: the longest path from it is {dp[i][j]}. Reuse that answer instead of searching again.",
            marks={"dp.good": "(i, j)"}, first=4)),
        ("dp[i][j] = 1",
         "Solve ({i}, {j}), value {matrix[i][j]}. The cell alone is a path of length 1. Now look for **larger** neighbours to continue to.",
         {"dp.cur": "(i, j)"}),
        ("dp[i][j] = max(dp[i][j], 1 + dfs(x, y))", dict(
            pre="Neighbour ({x}, {y}) holds {matrix[x][y]} > {matrix[i][j]}: the path may continue there. How long is the best path from it?",
            post="Stepping from ({i}, {j}) to ({x}, {y}) gives a path of 1 + {dp[x][y]} = {1 + dp[x][y]}. "
                 "`dp[{i}][{j}]` = **{dp[i][j]}**.",
            marks={"dp.cur": "(i, j)", "dp.alt": "(x, y)"})),
        ("max_path = max(max_path, dfs(i, j))", dict(
            post="The longest path starting at ({i}, {j}) is {dp[i][j]} → `max_path` = **{max_path}**.",
            when="max_path > was.max_path", marks={"dp.good": "(i, j)"})),
        ("return max_path", "Every cell has been solved. The longest increasing path has **{max_path}** cells."),
    ],
    time=("O(m · n)", "Thanks to the memo table every cell is solved once, looking at four neighbours."),
    space=("O(m · n)", "The memo table and, at worst, a recursion as deep as the number of cells."),
    tests=[
        ("matrix=[[3, 4, 5], [3, 2, 6], [2, 2, 1]]", 4),
        ("matrix=[[1]]", 1),
        ("matrix=[[7, 7], [7, 7]]", 1),
        ("matrix=[[1, 2, 3, 4, 5]]", 5),
    ],
)

lesson(
    "distinct-subsequences",
    pattern="2-D DP: use the letter or skip it",
    statement="""Given strings `s` and `t`, return the number of distinct **subsequences of `s`**
    that are equal to `t` — the number of ways to delete letters from `s` so that `t` remains.""",
    code="""
    class Solution:
        def numDistinct(self, s: str, t: str) -> int:
            m, n = len(s), len(t)

            # dp[i][j] = number of ways to form t[:j] from s[:i]
            dp = [[0] * (n + 1) for _ in range(m + 1)]

            # The empty target can always be formed in exactly one way.
            for i in range(m + 1):
                dp[i][0] = 1

            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if s[i - 1] == t[j - 1]:
                        # use this letter of s for t[j - 1], or skip it
                        dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
                    else:
                        # the letter cannot be used here: skip it
                        dp[i][j] = dp[i - 1][j]

            return dp[m][n]
    """,
    args='s="babag", t="bag"',
    expected=3,
    why="b(0) a(1) g(4),  b(0) a(3) g(4)  and  b(2) a(3) g(4).",
    idea=[
        "Let `dp[i][j]` be the number of ways to form the first `j` letters of `t` from the first `i` letters of `s`.",
        "Look at the last letter of that prefix of `s`. It can always be **skipped**: `dp[i − 1][j]` ways. If it equals the last needed letter of `t`, it can also be **used** for it: then the earlier letters must form the rest, `dp[i − 1][j − 1]` ways.",
        "An empty `t` can be formed in exactly one way from any prefix (delete everything), so the first column is 1.",
    ],
    views=[
        Grid("dp", title="dp[i][j] = ways to form t[:j] from s[:i]",
             rows="['∅'] + list(s)", cols="['∅'] + list(t)", ptrs={"i, j": "(i, j)"}),
    ],
    notes=[
        ("dp[i][0] = 1", dict(
            post="First column: the **empty** target can be formed from any prefix of `s` in exactly 1 way — use no letters at all.",
            when="i == m", marks={"dp.good": "[(r, 0) for r in range(m + 1)]"})),
        ("dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]",
         "`{s[i - 1]}` (s) = `{t[j - 1]}` (t). **Use** this letter as letter {j} of `t`: the earlier letters must form "
         "`{show(t[:j - 1])}` → {plural(dp[i - 1][j - 1], 'way')} (diagonal). Or **skip** it → {plural(dp[i - 1][j], 'way')} (above). "
         "Together **{dp[i][j]}**.",
         {"dp.alt": "[(i - 1, j - 1), (i - 1, j)]", "dp.good": "(i, j)"}),
        ("dp[i][j] = dp[i - 1][j]",
         "`{s[i - 1]}` (s) ≠ `{t[j - 1]}` (t): this letter of `s` cannot end `{t[:j]}`, so it must be skipped. "
         "Same count as without it (cell above): **{dp[i][j]}**.",
         {"dp.alt": "(i - 1, j)", "dp.cur": "(i, j)"}),
        ("return dp[m][n]", "The bottom-right cell uses all of `s` and all of `t`: **{_ret}** ways.", {"dp.good": "(m, n)"}),
    ],
    max_steps=140,
    time=("O(m · n)", "One cell per pair of prefix lengths."),
    space=("O(m · n)", "The table (one row would be enough)."),
    tests=[
        ('s="rabbbit", t="rabbit"', 3),
        ('s="babgbag", t="bag"', 5),
        ('s="a", t="b"', 0),
        ('s="abc", t=""', 1),
        ('s="", t="a"', 0),
        ('s="aaa", t="aa"', 3),
    ],
)

lesson(
    "edit-distance",
    pattern="2-D DP: insert, delete or replace",
    statement="""Return the minimum number of operations needed to turn `word1` into `word2`. One
    operation **inserts** a letter, **deletes** a letter or **replaces** a letter.""",
    args='word1="horse", word2="ros"',
    expected=3,
    why="horse → rorse (replace h by r) → rose (delete r) → ros (delete e).",
    idea=[
        "Let `dp[i][j]` be the cheapest way to turn the first `i` letters of `word1` into the first `j` letters of `word2`.",
        "If the two last letters are **equal**, nothing has to be done for them: `dp[i][j] = dp[i − 1][j − 1]`.",
        "Otherwise pay 1 for the best of three moves: **replace** the letter (then solve `dp[i − 1][j − 1]`), **delete** it from word1 (`dp[i − 1][j]`), or **insert** word2's letter (`dp[i][j − 1]`).",
    ],
    views=[
        Grid("dp", title="dp[i][j] = operations to turn word1[:i] into word2[:j]",
             rows="['∅'] + list(word1)", cols="['∅'] + list(word2)", ptrs={"i, j": "(i, j)"}),
    ],
    notes=[
        ("dp[i][0] = i", dict(
            post="First column: turning the first i letters of `word1` into the **empty** string takes i deletions.",
            when="i == m", marks={"dp.seen": "[(r, 0) for r in range(m + 1)]"})),
        ("dp[0][j] = j", dict(
            post="First row: building the first j letters of `word2` from the **empty** string takes j insertions.",
            when="j == n", marks={"dp.seen": "[(0, c) for c in range(n + 1)]"})),
        ("dp[i][j] = dp[i - 1][j - 1]",
         "`{word1[i - 1]}` = `{word2[j - 1]}`: the last letters already agree, so no operation is needed for them. "
         "Copy the diagonal → **{dp[i][j]}**.",
         {"dp.alt": "(i - 1, j - 1)", "dp.good": "(i, j)"}),
        ("dp[i][j] = min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]) + 1",
         "`{word1[i - 1]}` ≠ `{word2[j - 1]}`. Three moves, each costing 1: **replace** `{word1[i - 1]}` by `{word2[j - 1]}` "
         "(diagonal: {dp[i - 1][j - 1]}), **delete** `{word1[i - 1]}` (above: {dp[i - 1][j]}), or **insert** `{word2[j - 1]}` "
         "(left: {dp[i][j - 1]}). Cheapest + 1 = **{dp[i][j]}**.",
         {"dp.alt": "[(i - 1, j - 1), (i - 1, j), (i, j - 1)]", "dp.cur": "(i, j)"}),
        ("return dp[m][n]", "The bottom-right cell turns all of `{word1}` into all of `{word2}`: **{_ret}** operations.",
         {"dp.good": "(m, n)"}),
    ],
    time=("O(m · n)", "One cell per pair of prefix lengths, each in O(1)."),
    space=("O(m · n)", "The table (two rows would be enough)."),
    tests=[
        ('word1="intention", word2="execution"', 5),
        ('word1="", word2="abc"', 3),
        ('word1="abc", word2=""', 3),
        ('word1="", word2=""', 0),
        ('word1="same", word2="same"', 0),
    ],
)

lesson(
    "burst-balloons",
    pattern="Interval DP: choose the balloon that is burst last",
    statement="""Each balloon has a number. Bursting balloon `i` earns
    `nums[i − 1] · nums[i] · nums[i + 1]` coins, where the neighbours are the nearest balloons
    still **unburst** (a missing neighbour counts as 1). Burst all balloons; return the maximum
    number of coins.""",
    args="nums=[3, 1, 5]",
    expected=35,
    why="Burst 1 first (3·1·5 = 15), then 3 (1·3·5 = 15), then 5 (1·5·1 = 5): 35 coins.",
    idea=[
        "Choosing which balloon to burst **first** is messy: its two neighbours become adjacent, so the remaining parts influence each other.",
        "Think backwards — choose which balloon in an interval is burst **last**. When it finally bursts, everything else between the interval's two borders is already gone, so its neighbours are exactly those two borders. And the parts to its left and right were solved independently.",
        "`dp[left][right]` = best coins from bursting everything **strictly between** `left` and `right`. Try every `k` in between as the last balloon: `nums[left]·nums[k]·nums[right] + dp[left][k] + dp[k][right]`. Solve short intervals first.",
    ],
    views=[
        Arr("nums", ptrs=["left", "k", "right"], tones={"dim": "[0, len(nums) - 1]"},
            title="nums  (with a virtual 1 at both ends)"),
        Grid("dp", title="dp[left][right] = most coins from bursting everything strictly between left and right",
             ptrs={"left, right": "(left, right)"}),
    ],
    notes=[
        ("nums = [1] + nums + [1]",
         "Add a virtual balloon worth 1 at each end. They are never burst — they only serve as neighbours for the edge balloons."),
        ("dp = [[0] * (n + 2) for _ in range(n + 2)]",
         "`dp[left][right]` will hold the most coins obtainable by bursting **all balloons strictly between** index "
         "`left` and index `right`. Short intervals are solved first, because longer ones build on them."),
        ("right = left + length",
         "Interval ({left}, {right}): the balloons between the borders are {nums[left + 1:right]}. Which of them should be burst **last**?"),
        ("dp[left][right] = max(",
         "Let balloon {k} (value {nums[k]}) be the **last** one burst here. By then its neighbours are the borders "
         "{nums[left]} and {nums[right]}: {nums[left]} × {nums[k]} × {nums[right]} = {nums[left] * nums[k] * nums[right]}. "
         "Add the best for the part left of it ({dp[left][k]}) and right of it ({dp[k][right]}) → "
         "{nums[left] * nums[k] * nums[right] + dp[left][k] + dp[k][right]}. `dp[{left}][{right}]` = **{dp[left][right]}**.",
         {"dp.alt": "[(left, k), (k, right)]", "dp.good": "(left, right)"}),
        ("return dp[0][n + 1]",
         "`dp[0][{n + 1}]` covers every real balloon (between the two virtual ones): **{_ret}** coins.",
         {"dp.good": "(0, n + 1)"}),
    ],
    time=("O(n³)", "O(n²) intervals, and up to n choices for the last balloon in each."),
    space=("O(n²)", "The table has one cell for every pair (left, right)."),
    tests=[("nums=[3, 1, 5, 8]", 167), ("nums=[1, 5]", 10), ("nums=[7]", 7), ("nums=[9, 76, 64, 21]", 116718)],
)

lesson(
    "regular-expression-matching",
    pattern="2-D DP over string and pattern prefixes",
    statement="""Implement regular-expression matching for a string `s` and a pattern `p`, where `.`
    matches **any single character** and `*` means **zero or more of the element before it**. The
    match must cover the **entire** string.""",
    args='s="aab", p="c*a*b"',
    expected=True,
    why="`c*` stands for zero c's, `a*` for two a's, and `b` matches b.",
    idea=[
        "Let `dp[i][j]` say whether the first `i` characters of `s` match the first `j` symbols of `p`.",
        "A letter or a `.` in the pattern must match the current character of `s`; both are then consumed: `dp[i][j] = dp[i − 1][j − 1]`.",
        "A `*` belongs to the symbol before it (`x*`). Either the pair stands for **nothing** — drop it: `dp[i][j − 2]` — or it absorbs **one more** character of `s`, if that character matches `x`: `dp[i − 1][j]` (the pair stays available for more).",
    ],
    views=[
        Grid("dp", title="dp[i][j]: do the first i characters of s match the first j symbols of p?",
             rows="['∅'] + list(s)", cols="['∅'] + list(p)", vals={"T": "seen"}, ptrs={"i, j": "(i, j)"}),
    ],
    notes=[
        ("dp[0][0] = True", "The empty string matches the empty pattern: **True**.", {"dp.good": "(0, 0)"}),
        ("dp[0][j] = dp[0][j - 2]",
         "Top row (empty string): `{p[j - 2]}*` may stand for **zero** `{p[j - 2]}`'s, so the pair can simply be dropped. "
         "Copy the cell two to the left → **{dp[0][j]}**.",
         {"dp.alt": "(0, j - 2)", "dp.cur": "(0, j)"}),
        ("dp[i][j] = dp[i - 1][j - 1]", [
            ("p[j - 1] == '.'",
             "`.` matches any character, here `{s[i - 1]}`. Both are consumed, so the result is what held before them (diagonal) → **{dp[i][j]}**."),
            (None,
             "Pattern `{p[j - 1]}` matches character `{s[i - 1]}`. Both are consumed, so the result is what held before them (diagonal) → **{dp[i][j]}**."),
        ], {"dp.alt": "(i - 1, j - 1)", "dp.cur": "(i, j)"}),
        ("dp[i][j] = dp[i][j - 2] or (", [
            ("dp[i][j - 2]",
             "`{p[j - 2]}*`: let it stand for **zero** `{p[j - 2]}`'s and drop the pair — the cell two to the left is True → **True**."),
            ("dp[i][j]",
             "`{p[j - 2]}*`: dropping the pair fails (two to the left is False). But `{p[j - 2]}` matches `{s[i - 1]}`, so the star "
             "can **absorb** this character; without it the string already matched (cell above is True) → **True**."),
            ("s[i - 1] == p[j - 2] or p[j - 2] == '.'",
             "`{p[j - 2]}*`: dropping the pair fails, and although `{p[j - 2]}` matches `{s[i - 1]}`, the shorter string "
             "did not match (cell above is False) → **False**."),
            (None,
             "`{p[j - 2]}*`: dropping the pair fails (two to the left is False), and `{p[j - 2]}` does not match `{s[i - 1]}`, "
             "so the star cannot absorb it → **False**."),
        ], {"dp.alt": "[(i, j - 2), (i - 1, j)]", "dp.cur": "(i, j)"}),
        ('elif p[j - 1] == "*"', dict(
            no="Pattern `{p[j - 1]}` does not match character `{s[i - 1]}` (and it is neither `.` nor `*`) → stays **False**.",
            no_marks={"dp.bad": "(i, j)"})),
        ("return dp[m][n]", "The bottom-right cell covers the whole string and the whole pattern → **{_ret}**.",
         {"dp.good": "(m, n)"}),
    ],
    time=("O(m · n)", "One cell per pair of prefix lengths, each in O(1)."),
    space=("O(m · n)", "The table has (m + 1) × (n + 1) cells."),
    tests=[
        ('s="aa", p="a"', False),
        ('s="aa", p="a*"', True),
        ('s="ab", p=".*"', True),
        ('s="mississippi", p="mis*is*p*."', False),
        ('s="", p="a*b*"', True),
        ('s="ab", p=".*c"', False),
        ('s="aaa", p="ab*a*c*a"', True),
    ],
)

# end of c14_dp_2d
