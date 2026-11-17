"""Backtracking."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "subsets",
    pattern="Backtracking: choose → explore → undo",
    statement="""Given an array `nums` of **unique** integers, return every possible subset (the
    power set). No subset may appear twice; any order is accepted.""",
    args="nums=[1, 2, 3]",
    expected=[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]],
    why="3 numbers, each either in or out: 2 × 2 × 2 = 8 subsets.",
    picture="""Picture filling a bag with items from a row, always adding them in the order they stand in the
    row and never going back to an earlier one. Every bag you make on the way is a subset: first the
    empty bag, then each way of adding a next item to it. When you have explored every bag that
    starts a certain way, take the last item out again (*backtrack*) and try the next item in its
    place. Because items are only ever added in row order, no bag is made twice.""",
    idea=[
        "Build subsets one number at a time. At every moment the current partial choice is itself a subset — record it.",
        "To grow it, try each number that comes **after** the last one picked. Only moving forward means the same set is never produced twice in a different order.",
        "After exploring everything that starts with a pick, **undo** it (pop) and try the next number. Choose → explore → undo is the whole backtracking pattern.",
    ],
    views=[
        Arr("nums", ptrs=["i"], tones={"good": "[nums.index(x) for x in subset]"}),
        RecTree("backtrack", "{subset}", title="recursion tree  (each box = one call, labelled with `subset`)"),
        Stack("subset", title="subset  (current choice)"),
        Items("subsets", title="subsets  (answer so far)"),
    ],
    notes=[
        ("subsets.append(subset[:])",
         "The current choice `{subset}` is a valid subset all by itself. Save a **copy** of it in the answer.",
         {"subsets.good": "-1"}),
        ("subset.append(nums[i])",
         "**Choose** {nums[i]}: add it to the current subset → `{subset}`. Next, explore everything that starts this way."),
        ("subset.pop()",
         "Everything starting with `{was.subset}` has been explored. **Undo** the choice: remove {was.subset[-1]} "
         "→ `{subset}`, so the next number can be tried in its place."),
    ],
    say={
        "def subsets": (
            "The function we must write. It gets the list `nums` and returns every subset."
        ),
        "def backtrack(start, subset)": (
            "A helper. `subset` is the bag built so far; only items from position `start` on may "
            "be added next."
        ),
        "subsets.append(subset[:])": (
            "Every bag we reach is a subset: save a copy of it. (`subset[:]` copies the list, so "
            "later changes do not touch the saved one.)"
        ),
        "for i in range(start, len(nums))": (
            "Try each item that may still be added, from position `start` to the end."
        ),
        "subset.append(nums[i])": "**Choose** it: put it in the bag.",
        "backtrack(i + 1, subset)": (
            "**Explore** every bag that starts this way, adding only items after `i` (the helper "
            "calls itself)."
        ),
        "subset.pop()": (
            "**Undo**: take the item back out, so the next item can be tried in its place. This "
            "is the *backtrack*."
        ),
        "subsets = []": "The list of all subsets found.",
        "backtrack(0, [])": "Start with an empty bag, allowed to use every item.",
        "return subsets": "Return every subset.",
    },
    time=("O(n · 2ⁿ)", "There are 2ⁿ subsets and copying each one into the answer costs up to O(n)."),
    space=("O(n)", "The recursion is at most n deep and `subset` holds at most n numbers (not counting the output)."),
    tests=[("nums=[0]", [[], [0]]), ("nums=[1, 2]", [[], [1], [1, 2], [2]])],
)

lesson(
    "combination-sum",
    pattern="Backtracking with reuse allowed",
    statement="""Given **distinct** positive integers `candidates` and a `target`, return every
    combination of candidates that adds up to `target`. The same number may be used **any number
    of times**. Two combinations are the same if they use each number the same number of times.""",
    args="candidates=[2, 3, 5], target=7",
    expected=[[2, 2, 3], [2, 5]],
    why="2 + 2 + 3 = 7 and 2 + 5 = 7. No other mix of 2s, 3s and 5s reaches exactly 7.",
    picture="""Picture paying an exact amount with coins of a few sizes, where each size can be used as often
    as you like. Add a coin and see how much is still left to pay. If that is exactly 0, you have
    found a way; a coin bigger than what is left cannot be used. When you have tried everything that
    follows from a coin, take it back out and try the next size. To avoid finding the same mix twice
    in another order, never go back to a coin size earlier in the list than the last one added.""",
    idea=[
        "Build a combination one number at a time and keep track of how much is **still missing** from the target.",
        "After picking `candidates[i]`, the next pick may be the same number again or a later one — never an earlier one. That keeps every combination in one fixed order, so `[2, 5]` is never produced again as `[5, 2]`.",
        "Missing amount 0 → a full combination, save it. A candidate larger than what is missing cannot help, so it is skipped. After exploring a pick, **undo** it and try the next candidate.",
    ],
    views=[
        Arr("candidates", ptrs=["i"]),
        RecTree("backtrack", "{combination}  need {target}",
                title="recursion tree  (each box = picks so far and what is still needed)",
                mark_call={"good": "target == 0"}),
        Stack("combination", title="combination  (picks so far)"),
        Items("result", title="result"),
    ],
    notes=[
        ("if target == 0", dict(
            yes="The picks `{combination}` add up exactly: nothing is missing any more.")),
        ("result.append(", "Save a **copy** of `{combination}` in the result.", {"result.good": "-1"}),
        ("if candidates[i] > target", dict(
            yes="{candidates[i]} is more than the {target} still needed — it would overshoot. Skip it.",
            marks={"candidates.bad": "i"})),
        ("combination.append(candidates[i])", [
            ("target == candidates[i]",
             "**Choose** {candidates[i]} → `{combination}`. Still needed: {target} − {candidates[i]} = **0**."),
            ("len(combination) == 1 and i == 0",
             "**Choose** {candidates[i]} → `{combination}`. Still needed: {target} − {candidates[i]} = "
             "**{target - candidates[i]}**. The recursive call passes `i`, not `i + 1`, so the next pick may be "
             "{candidates[i]} **again**."),
            (None,
             "**Choose** {candidates[i]} → `{combination}`. Still needed: {target} − {candidates[i]} = "
             "**{target - candidates[i]}**."),
        ], {"candidates.good": "i"}),
        ("combination.pop()",
         "Everything that starts with `{was.combination}` has been explored. **Undo** the last pick "
         "({was.combination[-1]}) → `{combination}` and try the next candidate."),
        ("return result", "Every branch has been explored. The combinations that hit the target: **{_ret}**."),
    ],
    say={
        "def combinationSum": (
            "The function we must write. It gets the numbers `candidates` and the `target`, and "
            "returns every way to reach the target."
        ),
        "def backtrack(start, target, combination)": (
            "A helper. `combination` holds the numbers chosen so far, `target` is the amount "
            "still missing, and only candidates from position `start` on may be used."
        ),
        "if target == 0": "Is nothing missing any more?",
        "result.append(": "Then this combination adds up exactly: save a copy of it.",
        "return@1": "And go back to try other choices.",
        "for i in range(start, len(candidates))": "Try each candidate from position `start` on.",
        "if candidates[i] > target": "Is it bigger than the amount still missing?",
        "continue": "Then it cannot be used here: skip it.",
        "combination.append(candidates[i])": "**Choose** it: add it to the combination.",
        "backtrack(i, target - candidates[i], combination)": (
            "**Explore** from here, with less missing. Passing `i` (not `i + 1`) lets the same "
            "number be used again."
        ),
        "combination.pop()": "**Undo**: take it back out and try the next candidate.",
        "result = []": "The list of combinations found.",
        "backtrack(0, target, [])": "Start with nothing chosen and the whole target missing.",
        "return result": "Return every combination.",
    },
    time=("O(n^(T/m))", "T is the target and m the smallest candidate: a combination has at most T/m picks, and each pick has up to n choices."),
    space=("O(T/m)", "The recursion and the current combination are at most T/m deep (not counting the output)."),
    tests=[
        ("candidates=[2, 3, 6, 7], target=7", [[2, 2, 3], [7]]),
        ("candidates=[2], target=1", []),
        ("candidates=[2, 3, 5], target=8", [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
    ],
)

lesson(
    "permutations",
    pattern="Backtracking: fill one position at a time",
    statement="""Given an array `nums` of **distinct** integers, return all possible orderings
    (permutations) of it, in any order.""",
    code="""
    class Solution:
        def permute(self, nums: List[int]) -> List[List[int]]:
            def backtrack(path):
                if len(path) == len(nums):
                    result.append(path[:])  # a full ordering: save a copy
                    return

                for num in nums:
                    if num in path:
                        continue  # already used in this ordering
                    path.append(num)
                    backtrack(path)
                    path.pop()  # undo, so another number can take this place

            result = []
            backtrack([])
            return result
    """,
    args="nums=[1, 2, 3]",
    expected=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
    why="3 choices for the first place, 2 for the second, 1 for the last: 3 × 2 × 1 = 6 orderings.",
    picture="""Picture filling a row of empty seats, one seat at a time, with people who are not seated yet.
    For the first seat, try each person in turn; for each choice, fill the remaining seats the same
    way. When every seat is taken, that is one ordering. Then the last person stands up again
    (*backtracking*) so that someone else can try that seat.""",
    idea=[
        "Fill the ordering one position at a time. For each position, try **every number that is not used yet**.",
        "When the ordering is as long as `nums`, every number has been placed: it is a complete permutation — save it.",
        "After exploring everything that starts with a choice, **undo** it (pop) so a different number can take that position.",
    ],
    views=[
        Arr("nums", ptrs={"num": "i_num"}, tones={"seen": "[nums.index(x) for x in path]"},
            title="nums  (grey = already in the path)"),
        RecTree("backtrack", "{path}", title="recursion tree  (each box = the ordering built so far)",
                mark_call={"good": "len(path) == len(nums)"}),
        Stack("path", title="path  (ordering so far)"),
        Items("result", title="result"),
    ],
    notes=[
        ("if len(path) == len(nums)", dict(
            yes="`{path}` uses all {len(nums)} numbers — a complete permutation.")),
        ("result.append(path[:])", "Save a **copy** of `{path}` in the result.", {"result.good": "-1"}),
        ("if num in path", dict(
            yes="{num} is already in `{path}`. Each number may be used only once, so skip it.",
            first=4)),
        ("path.append(num)",
         "{num} is still free: **choose** it for position {len(path) - 1} → `{path}`."),
        ("path.pop()",
         "Every ordering starting with `{was.path}` is done. **Undo**: remove {was.path[-1]} → `{path}`."),
        ("return result", "All {len(_ret)} orderings have been collected."),
    ],
    say={
        "def permute": (
            "The function we must write. It gets the list `nums` and returns every ordering of "
            "it."
        ),
        "def backtrack(path)": (
            "A helper. `path` is the ordering built so far: the seats already filled."
        ),
        "if len(path) == len(nums)": "Is every seat filled?",
        "result.append(path[:])": "Then this is a complete ordering: save a copy.",
        "return@1": "And go back to try other choices.",
        "for num in nums": "Try each number for the next seat.",
        "if num in path": "Is it already seated in this ordering?",
        "continue": "Then skip it: each number is used once.",
        "path.append(num)": "**Choose** it: seat it next.",
        "backtrack(path)": (
            "**Explore**: fill the remaining seats the same way (the helper calls itself)."
        ),
        "path.pop()": "**Undo**: the number stands up again, so another one can take this seat.",
        "result = []": "The list of all orderings found.",
        "backtrack([])": "Start with every seat empty.",
        "return result": "Return every ordering.",
    },
    time=("O(n · n!)", "There are n! permutations and copying each one costs O(n). (A `used` set would make the `in` check O(1); the overall bound stays the same.)"),
    space=("O(n)", "The recursion and `path` are at most n deep (not counting the output)."),
    tests=[
        ("nums=[0, 1]", [[0, 1], [1, 0]]),
        ("nums=[1]", [[1]]),
        ("nums=[5, 4, 6]", [[5, 4, 6], [5, 6, 4], [4, 5, 6], [4, 6, 5], [6, 5, 4], [6, 4, 5]]),
    ],
)

lesson(
    "subsets-ii",
    pattern="Backtracking + skip equal neighbours",
    statement="""Given an array `nums` that **may contain duplicates**, return all possible
    subsets. The answer must not contain the same subset twice.""",
    args="nums=[2, 1, 2]",
    expected=[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]],
    unordered=1,
    why="Both 2s are interchangeable, so [1, 2] is listed once even though either 2 could be used.",
    picture="""Picture filling bags as in Subsets, except that some items are identical twins. Sort the items
    first, so that twins stand side by side. Then, whenever you choose the next item for the same
    place in a bag, use only the first twin of each kind: choosing the second twin there would only
    build exactly the same bags again.""",
    idea=[
        "Start from the plain Subsets recipe: record the current choice, then try each later number, explore, undo.",
        "Duplicates break it: with two 2s, *picking the first 2* and *picking the second 2* for the same slot build identical subsets.",
        "Fix: **sort** so equal numbers are neighbours, and at each slot use a value only **once** — if `nums[i]` equals the number just before it (and that one was already tried for this slot), skip it.",
    ],
    views=[
        Arr("nums", ptrs=["i"]),
        RecTree("backtrack", "{subset}", title="recursion tree  (each box = one call, labelled with `subset`)"),
        Stack("subset", title="subset  (current choice)"),
        Items("subsets", title="subsets  (answer so far)"),
    ],
    notes=[
        ("nums.sort()", "Sort first → `{nums}`. Now equal numbers stand next to each other, which makes duplicates easy to spot."),
        ("subsets.append(subset[:])",
         "The current choice `{subset}` is a subset by itself. Save a **copy**.",
         {"subsets.good": "-1"}),
        ("if i > start and nums[i] == nums[i - 1]", dict(
            yes="`nums[{i}]` = {nums[i]} is the same value as `nums[{i - 1}]`, which was **already tried for this slot**. "
                "Choosing it again would rebuild exactly the same subsets — skip it.",
            marks={"nums.bad": "i", "nums.alt": "i - 1"})),
        ("subset.append(nums[i])",
         "**Choose** `nums[{i}]` = {nums[i]} → `{subset}`. Explore everything that starts this way.",
         {"nums.good": "i"}),
        ("subset.pop()",
         "Done with `{was.subset}`. **Undo**: remove {was.subset[-1]} → `{subset}`."),
        ("return subsets", "All distinct subsets: {len(_ret)} of them, none repeated."),
    ],
    say={
        "def subsetsWithDup": (
            "The function we must write. It gets the list `nums`, which may contain repeats, and "
            "returns every different subset."
        ),
        "def backtrack(start, subset)": (
            "A helper. `subset` is the bag built so far; only items from position `start` on may "
            "be added next."
        ),
        "subsets.append(subset[:])": "Every bag we reach is a subset: save a copy of it.",
        "for i in range(start, len(nums))": "Try each item that may still be added.",
        "if i > start and nums[i] == nums[i - 1]": (
            "Is it the same value as the item just before it, which this loop has already tried "
            "for this same place in the bag?"
        ),
        "continue": "Then skip it: it would only rebuild the same bags.",
        "subset.append(nums[i])": "**Choose** it: put it in the bag.",
        "backtrack(i + 1, subset)": (
            "**Explore** every bag that starts this way (the helper calls itself)."
        ),
        "subset.pop()": "**Undo**: take it back out and try the next item.",
        "nums.sort()": (
            "Sort first, so that equal values sit side by side and repeats are easy to spot."
        ),
        "subsets = []": "The list of all subsets found.",
        "backtrack(0, [])": "Start with an empty bag.",
        "return subsets": "Return every subset.",
    },
    time=("O(n · 2ⁿ)", "At most 2ⁿ subsets, each copied in O(n); sorting adds only O(n log n)."),
    space=("O(n)", "Recursion depth and `subset` are at most n (not counting the output)."),
    tests=[
        ("nums=[1, 2, 2]", [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]),
        ("nums=[0]", [[], [0]]),
        ("nums=[4, 4, 4]", [[], [4], [4, 4], [4, 4, 4]]),
    ],
)

lesson(
    "combination-sum-ii",
    pattern="Backtracking: each number once, skip equal neighbours",
    statement="""Given `candidates` (which **may contain duplicates**) and a `target`, return all
    unique combinations that add up to `target`. Each candidate may be used **at most once**.""",
    code="""
    class Solution:
        def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
            def backtrack(start, target, combination):
                if target == 0:
                    result.append(combination[:])
                    return

                for i in range(start, len(candidates)):
                    if i > start and candidates[i] == candidates[i - 1]:
                        continue  # same value already tried for this slot
                    if candidates[i] > target:
                        break  # sorted: everything after is too large as well

                    combination.append(candidates[i])
                    backtrack(i + 1, target - candidates[i], combination)
                    combination.pop()

            candidates.sort()
            result = []
            backtrack(0, target, [])
            return result
    """,
    args="candidates=[2, 5, 1, 2], target=5",
    expected=[[1, 2, 2], [5]],
    unordered=1,
    why="1 + 2 + 2 = 5 and 5 alone. [1, 2, 2] uses both 2s once each.",
    picture="""Picture paying an exact amount with a handful of coins, each usable only once, where several
    coins may have the same value. Sort the coins first. Add a coin, pay the rest with the coins
    after it, then take it back and try the next. Two rules save work. At any one point, try each
    coin value only once, because another coin of the same value would repeat the same mixes. And
    stop as soon as a coin is bigger than what is left, because every coin after it is bigger too.""",
    idea=[
        "Like Combination Sum, track how much is **still needed**. But each number can be used only once, so after picking index `i` the next pick starts at `i + 1`.",
        "Duplicates in the input would produce the same combination several times. **Sort**, and at each slot skip a value equal to the one just tried there.",
        "Sorting gives a second win: as soon as a candidate is larger than what is needed, every later one is too — **stop** the loop.",
    ],
    views=[
        Arr("candidates", ptrs=["i"]),
        RecTree("backtrack", "{combination}  need {target}",
                title="recursion tree  (each box = picks so far and what is still needed)",
                mark_call={"good": "target == 0"}),
        Stack("combination", title="combination  (picks so far)"),
        Items("result", title="result"),
    ],
    notes=[
        ("candidates.sort()", "Sort first → `{candidates}`. Equal values become neighbours, and small values come first."),
        ("if target == 0", dict(yes="`{combination}` adds up exactly — nothing is missing.")),
        ("result.append(combination[:])", "Save a **copy** of `{combination}`.", {"result.good": "-1"}),
        ("if i > start and candidates[i] == candidates[i - 1]", dict(
            yes="`candidates[{i}]` = {candidates[i]} equals the value before it, which was **already tried for this slot**. "
                "It would only repeat the same combinations — skip.",
            marks={"candidates.bad": "i", "candidates.alt": "i - 1"})),
        ("if candidates[i] > target", dict(
            yes="{candidates[i]} is more than the {target} still needed. The list is sorted, so everything after it is "
                "too large as well — **stop** trying here.",
            marks={"candidates.bad": "range(i, len(candidates))"})),
        ("combination.append(candidates[i])",
         "**Choose** {candidates[i]} → `{combination}`. Still needed: **{target - candidates[i]}**. "
         "The next pick must come from the right of index {i}.",
         {"candidates.good": "i"}),
        ("combination.pop()",
         "Done with `{was.combination}`. **Undo** the last pick ({was.combination[-1]}) → `{combination}`."),
        ("return result", "Every branch has been explored: **{_ret}**."),
    ],
    say={
        "def combinationSum2": (
            "The function we must write. It gets `candidates` (which may repeat) and the "
            "`target`, and returns every different combination, each candidate used at most once."
        ),
        "def backtrack(start, target, combination)": (
            "A helper. `combination` holds what has been chosen, `target` is the amount still "
            "missing, and only candidates from position `start` on may be used."
        ),
        "if target == 0": "Is nothing missing any more?",
        "result.append(combination[:])": "Then this combination adds up exactly: save a copy.",
        "return@1": "And go back to try other choices.",
        "for i in range(start, len(candidates))": "Try each candidate from position `start` on.",
        "if i > start and candidates[i] == candidates[i - 1]": (
            "Is it the same value as the one just tried for this same place?"
        ),
        "continue": "Then skip it: it would only repeat the same combinations.",
        "if candidates[i] > target": "Is it bigger than the amount still missing?",
        "break": (
            "Then stop this loop: the list is sorted, so every later candidate is too big as "
            "well."
        ),
        "combination.append(candidates[i])": "**Choose** it.",
        "backtrack(i + 1, target - candidates[i], combination)": (
            "**Explore** from here, with less missing. `i + 1` means each candidate is used at "
            "most once."
        ),
        "combination.pop()": "**Undo**: take it back out and try the next candidate.",
        "candidates.sort()": (
            "Sort first, so repeats sit side by side and the loop can stop early."
        ),
        "result = []": "The list of combinations found.",
        "backtrack(0, target, [])": "Start with nothing chosen.",
        "return result": "Return every combination.",
    },
    time=("O(n · 2ⁿ)", "Each candidate is either in or out, and saving a combination costs O(n). Sorting and pruning cut this down a lot in practice."),
    space=("O(n)", "Recursion depth and the combination are at most n (not counting the output)."),
    tests=[
        ("candidates=[10, 1, 2, 7, 6, 1, 5], target=8", [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
        ("candidates=[2, 5, 2, 1, 2], target=5", [[1, 2, 2], [5]]),
        ("candidates=[3], target=1", []),
        ("candidates=[1, 1, 1], target=2", [[1, 1]]),
    ],
)

lesson(
    "word-search",
    pattern="DFS with backtracking on a grid",
    statement="""Given a grid of letters `board` and a string `word`, return `True` if the word can
    be traced through horizontally or vertically neighbouring cells. A cell may be used **at most
    once** in the path.""",
    args='board=[["A", "B", "C"], ["S", "F", "C"], ["A", "D", "E"]], word="ABCCE"',
    expected=True,
    why="A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2).",
    picture="""Picture tracing the word on the grid with your finger, letter by letter. From a cell that holds
    the right letter, try to carry on in each of the four directions. Cover every cell you use with
    a coin, so the trace cannot step on it twice. If a direction leads nowhere, lift the coin on the
    way back (*backtracking*) and try another direction.""",
    idea=[
        "Every cell that holds the word's first letter is a possible start. From there, try to match the rest letter by letter.",
        "`dfs(row, col, index)` asks: *can the word from letter `index` on be traced starting at this cell?* It fails when the cell is off the board, already used, or holds the wrong letter.",
        "On a match, mark the cell as used (`#`), try all four neighbours for the next letter, then **restore** the cell so other paths can use it.",
    ],
    views=[
        Grid("board", vals={"#": "win"}, tones={"cur": "(row, col)"}),
        Arr("word", ptrs=["index"], tones={"good": "range(index)"}, title="word  (green = already matched)"),
        Calls("dfs", "dfs({row}, {col}, index {index})"),
    ],
    key={"win": "in use on the current path"},
    notes=[
        ("if board[row][col] == word[0] and dfs(row, col, 0)", dict(
            pre=[
                ("board[row][col] == word[0]", "Scan: ({row}, {col}) holds `{board[row][col]}`, the first letter of the word. Try to trace the whole word from here."),
                (None, "Scan: ({row}, {col}) holds `{board[row][col]}`, not the first letter `{word[0]}`. Move on."),
            ],
            yes="The trace starting at ({row}, {col}) succeeded.")),
        ("if index == len(word)", dict(
            yes="`index` = {index} = the length of the word: **every letter has been matched** → True.")),
        ("if (", dict(
            yes=[
                ("not (0 <= row < len(board) and 0 <= col < len(board[0]))",
                 "({row}, {col}) is **off the board** → False."),
                ("board[row][col] == '#'", "({row}, {col}) is **already used** on this path (`#`) → False."),
                (None, "({row}, {col}) holds `{board[row][col]}`, but letter {index} of the word is `{word[index]}` → False."),
            ])),
        ('board[row][col] = "#"',
         "({row}, {col}) holds `{original_char}` — letter {index} matches. Mark the cell `#` so this path cannot "
         "step on it again, then try the four neighbours (down, up, right, left) for the next letter."),
        ("board[row][col] = original_char", [
            ("found", "The rest of the word was found. Put `{original_char}` back at ({row}, {col}) and pass **True** upward."),
            (None, "No neighbour of ({row}, {col}) could continue the word. **Backtrack**: put `{original_char}` back so other paths may use this cell."),
        ]),
        ("return True@2", "The word can be traced on the board → **True**."),
        ("return False@2", "No starting cell worked → **False**."),
    ],
    allow_unused=True,
    say={
        "def exist": (
            "The function we must write. It gets the grid `board` and the `word`, and answers "
            "whether the word can be traced."
        ),
        "def dfs(row, col, index)": (
            "A helper: can the rest of the word, from letter `index` on, be traced starting at "
            "this cell?"
        ),
        "if index == len(word)": "Have all the letters been matched?",
        "return True@1": "Then the word is traced.",
        "if (": "Is this cell outside the grid, or does it hold the wrong letter?",
        "return False@1": "Then the trace cannot continue here.",
        "original_char = board[row][col]": "Remember the letter in this cell.",
        'board[row][col] = "#"': (
            "**Choose** this cell: cover it with `#`, so this trace cannot use it twice."
        ),
        "found = (": (
            "**Explore**: try to continue with the next letter in each of the four directions, "
            "down, up, right and left. `or` stops at the first direction that works."
        ),
        "board[row][col] = original_char": (
            "**Undo**: uncover the cell on the way back, so other traces can use it."
        ),
        "return found": "Report whether any direction worked.",
        "for row in range(len(board))": "Try every row of the grid…",
        "for col in range(len(board[0]))": "…and every column in it.",
        "if board[row][col] == word[0] and dfs(row, col, 0)": (
            "Does this cell hold the first letter, and can the whole word be traced from here?"
        ),
        "return True@2": "Yes: answer `True`.",
        "return False@2": "No starting cell worked: answer `False`.",
    },
    time=("O(m · n · 4ᴸ)", "Each of the m · n cells can start a search that branches up to 4 ways for each of the L letters (really 3 after the first step)."),
    space=("O(L)", "The recursion is at most L + 1 calls deep; the board itself is reused to mark visited cells."),
    tests=[
        ('board=[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCCED"', True),
        ('board=[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="SEE"', True),
        ('board=[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCB"', False),
        ('board=[["a"]], word="a"', True),
        ('board=[["a","a"]], word="aaa"', False),
    ],
)

lesson(
    "palindrome-partitioning",
    pattern="Backtracking over cut positions",
    statement="""Given a string `s`, cut it into pieces so that **every piece is a palindrome**
    (reads the same forwards and backwards). Return all possible ways to do this.""",
    args="s='aab'",
    expected=[["a", "a", "b"], ["aa", "b"]],
    why="a | a | b and aa | b. The pieces 'ab' and 'aab' are not palindromes, so no other cut works.",
    picture="""Picture cutting a ribbon of letters into pieces, where every piece must read the same both ways.
    Starting from the left, try every possible first piece: one letter, two letters, and so on. Keep
    only the pieces that are palindromes, and cut the rest of the ribbon the same way. When nothing
    is left to cut, that is one way to do it. Then undo the last cut and try a longer piece instead.""",
    idea=[
        "Decide the pieces from left to right. The first piece is some prefix `s[start:end]` — try every possible end.",
        "A prefix that is **not** a palindrome can never be part of an answer, so that branch is dropped immediately.",
        "If it is a palindrome, take it as a piece and solve the same problem for the rest of the string. Reaching the end of `s` means every piece was fine → save the partition. Then undo and try a longer piece.",
    ],
    views=[
        Arr("s", rng=("start", "end - 1", "sub", "cur"), tones={"dim": "range(start)"}),
        RecTree("backtrack", "{partition}", title="recursion tree  (each box = the pieces cut so far)",
                mark_call={"good": "start == len(s)"}),
        Stack("partition", title="partition  (pieces so far)"),
        Items("result", title="result"),
    ],
    notes=[
        ("if start == len(s)", dict(
            yes="`start` reached the end of the string: all of `s` has been cut into palindromes.")),
        ("result.append(partition[:])", "Save a **copy** of `{partition}`.", {"result.good": "-1"}),
        ("if is_palindrome(sub)", dict(
            yes="Piece `{sub}` reads the same backwards — a **palindrome**. It may be used.",
            no="Piece `{sub}` backwards is `{sub[::-1]}` — **not** a palindrome. Drop this cut and try a longer piece.")),
        ("partition.append(sub)",
         "**Cut** after `{sub}` → `{partition}`. Now partition the rest, `{show(s[end:])}`."),
        ("partition.pop()",
         "Done with everything that starts with `{was.partition}`. **Undo** the last cut → `{partition}`."),
        ("return result", "All ways to cut `{s}` into palindromes: **{_ret}**."),
    ],
    say={
        "def partition": (
            "The function we must write. It gets the text `s` and returns every way to cut it "
            "into palindromes."
        ),
        "def is_palindrome(sub)": "A helper: does `sub` read the same backwards?",
        "return sub == sub[::-1]": "`sub[::-1]` is the text written backwards. Compare the two.",
        "def backtrack(start, partition)": (
            "A helper. `partition` holds the pieces cut so far; the rest of the text starts at "
            "position `start`."
        ),
        "if start == len(s)": "Has the whole text been cut up?",
        "result.append(partition[:])": "Then this is one complete way: save a copy.",
        "return@2": "And go back to try other cuts.",
        "for end in range(start + 1, len(s) + 1)": (
            "Try every length for the next piece: it runs from `start` up to just before `end`."
        ),
        "sub = s[start:end]": "Cut out that piece.",
        "if is_palindrome(sub)": "Does it read the same both ways?",
        "partition.append(sub)": "**Choose** it as the next piece.",
        "backtrack(end, partition)": (
            "**Explore**: cut the rest of the text, after this piece, the same way (the helper "
            "calls itself)."
        ),
        "partition.pop()": "**Undo**: undo this cut, so a longer piece can be tried instead.",
        "result = []": "The list of all the ways found.",
        "backtrack(0, [])": "Start at the beginning of the text, with no pieces cut.",
        "return result": "Return every way.",
    },
    time=("O(n · 2ⁿ)", "There are 2ⁿ⁻¹ ways to place cuts; checking and copying pieces costs O(n) each."),
    space=("O(n)", "Recursion depth and the current partition are at most n (not counting the output)."),
    tests=[
        ("s='a'", [["a"]]),
        ("s='aba'", [["a", "b", "a"], ["aba"]]),
        ("s='abc'", [["a", "b", "c"]]),
    ],
)

lesson(
    "letter-combinations-of-a-phone-number",
    pattern="Backtracking: one choice per digit",
    statement="""Given a string of digits from `2` to `9`, return every letter combination the
    number could spell on a phone keypad (2 → abc, 3 → def, … 9 → wxyz). Return an empty list
    for an empty input.""",
    args="digits='23'",
    expected=["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"],
    why="3 letters for the 2 times 3 letters for the 3 = 9 combinations.",
    picture="""Picture an old phone keypad, where each digit stands for a few letters: 2 for `abc`, 3 for
    `def`, and so on. Spell the number one digit at a time. For the first digit, try each of its
    letters; for each of those, try each letter of the next digit; and so on. Every time all the
    digits have been used, the letters chosen spell one combination.""",
    idea=[
        "Each digit stands for one of its letters. A combination picks **one letter per digit**, in order.",
        "Go digit by digit: for the current digit, try each of its letters and recurse on the next digit with the longer string.",
        "When there are no digits left, the string built so far is one complete combination.",
    ],
    views=[
        Arr("digits", ptrs=["index"]),
        HMap("{d: phone_mapping[d] for d in dict.fromkeys(digits)}", id="keys", title="letters on the keys we need"),
        RecTree("backtrack", "{show(combination)}", title="recursion tree  (each box = the letters chosen so far)",
                mark_call={"good": "index == len(digits)"}),
        Items("combinations", title="combinations"),
    ],
    notes=[
        ("phone_mapping = {", "The keypad: each digit maps to its letters."),
        ("if index == len(digits)", dict(
            yes="No digits left: `{combination}` has one letter for every digit — a complete combination.")),
        ("combinations.append(combination)", "Save `{combination}`.", {"combinations.good": "-1"}),
        ("letters = phone_mapping[digit]",
         "Digit `{digit}` (position {index}) can be any of `{letters}`. Try each letter in turn.",
         {"keys.cur": "digit"}),
        ("backtrack(index + 1, combination + letter)", dict(
            pre=[
                ("index == 0 and letter == letters[0]",
                 "Pick `{letter}` for digit `{digit}` → `{combination + letter}`, and move on to the next digit. "
                 "(`combination + letter` builds a **new** string for the call, so there is nothing to undo afterwards.)"),
                (None, "Pick `{letter}` for digit `{digit}` → `{combination + letter}`."),
            ])),
        ("return combinations", "Every path through the digits has been followed: {len(_ret)} combinations."),
    ],
    allow_unused=True,
    say={
        "def letterCombinations": (
            "The function we must write. It gets the `digits` and returns every letter "
            "combination they could spell."
        ),
        "if not digits": "Were no digits given?",
        "return []": "Then there are no combinations.",
        "phone_mapping = {": "A dictionary from each digit to its letters on a phone keypad.",
        "def backtrack(index, combination)": (
            "A helper. `combination` holds the letters chosen so far, one for each digit before "
            "position `index`."
        ),
        "if index == len(digits)": "Has every digit been given a letter?",
        "combinations.append(combination)": "Then this is a complete combination: save it.",
        "return@2": "And go back to try other letters.",
        "digit = digits[index]": "The next digit to spell.",
        "letters = phone_mapping[digit]": "The letters it stands for.",
        "for letter in letters": "Try each of those letters.",
        "backtrack(index + 1, combination + letter)": (
            "Add it and move on to the next digit (the helper calls itself). A new text is made "
            "with the letter added, so nothing needs undoing afterwards."
        ),
        "combinations = []": "The list of combinations found.",
        'backtrack(0, "")': "Start at the first digit, with no letters chosen.",
        "return combinations": "Return every combination.",
    },
    time=("O(n · 4ⁿ)", "Up to 4 letters per digit gives at most 4ⁿ combinations, each of length n."),
    space=("O(n)", "The recursion is n deep (not counting the output)."),
    tests=[("digits=''", []), ("digits='2'", ["a", "b", "c"]),
           ("digits='79'", ["pw", "px", "py", "pz", "qw", "qx", "qy", "qz", "rw", "rx", "ry", "rz", "sw", "sx", "sy", "sz"])],
)

lesson(
    "n-queens",
    pattern="Backtracking row by row with attack sets",
    statement="""Place `n` queens on an `n × n` chessboard so that **no two queens attack each
    other** (no shared row, column or diagonal). Return every distinct solution; each solution is
    the board as a list of strings, `Q` for a queen and `.` for an empty square.""",
    code="""
    class Solution:
        def solveNQueens(self, n: int) -> List[List[str]]:
            cols = set()  # columns that already hold a queen
            diag = set()  # (row - col) is constant along a "\\" diagonal
            anti = set()  # (row + col) is constant along a "/" diagonal
            board = [["."] * n for _ in range(n)]
            result = []

            def place_queen(row):
                if row == n:
                    result.append(["".join(line) for line in board])
                    return

                for col in range(n):
                    if col in cols or (row - col) in diag or (row + col) in anti:
                        continue  # this square is attacked

                    board[row][col] = "Q"
                    cols.add(col)
                    diag.add(row - col)
                    anti.add(row + col)

                    place_queen(row + 1)

                    board[row][col] = "."
                    cols.remove(col)
                    diag.remove(row - col)
                    anti.remove(row + col)

            place_queen(0)
            return result
    """,
    args="n=4",
    expected=[[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]],
    unordered=1,
    why="For a 4 × 4 board there are exactly two arrangements; they are mirror images of each other.",
    picture="""Picture placing queens on a chessboard one row at a time, since every row needs exactly one. In
    the current row, try each square that no earlier queen attacks: no queen in the same column and
    none on either diagonal. Place a queen there and move on to the next row. If a row has no safe
    square left, go back, pick the previous queen up and try the next square in its row. Every time
    all `n` rows have a queen, you have a solution.""",
    idea=[
        "Every row needs exactly one queen, so place them **row by row**: for the current row, try each column.",
        "A square is safe if no earlier queen shares its column or a diagonal. Along a `\\` diagonal (top-left to bottom-right) `row − col` never changes; along a `/` diagonal (top-right to bottom-left) `row + col` never changes. Three sets remember which columns and diagonals are taken, so the check is O(1).",
        "Safe → place the queen and go to the next row. If a row has no safe square, go back, **remove** the previous queen and try its next column. Reaching row `n` means all queens are placed.",
    ],
    views=[
        Grid("board", vals={"Q": "good"}, blank=["."],
             tones={"cur": "(row, col)",
                    "bad": "[(r, c) for r in range(n) for c in range(n) if board[r][c] != 'Q' and "
                           "(c in cols or (r - c) in diag or (r + c) in anti)]"},
             title="board  (red = attacked by a queen)"),
        Vars(("cols", "sorted(cols)"), ("diag (row − col)", "sorted(diag)"), ("anti (row + col)", "sorted(anti)")),
        Items("result", title="solutions found"),
    ],
    key={"good": "a queen", "bad": "attacked by a queen"},
    notes=[
        ("board = [", "An empty {n} × {n} board. We will put one queen in each row, starting with row 0."),
        ("if row == n", dict(
            yes="Row {row} does not exist: all {n} queens are on the board and none attack each other — **a solution**.")),
        ("result.append(", "Save the board as a list of strings: `{result[-1]}`.", {"result.good": "-1"}),
        ("if col in cols or (row - col) in diag or (row + col) in anti", dict(
            yes=[
                ("col in cols", "Row {row}, column {col}: a queen already stands in **column {col}**. Attacked — skip."),
                ("(row - col) in diag", "Row {row}, column {col}: a queen is on the same **`\\` diagonal** (row − col = {row - col}). Attacked — skip."),
                (None, "Row {row}, column {col}: a queen is on the same **`/` diagonal** (row + col = {row + col}). Attacked — skip."),
            ],
            first=8)),
        ("anti.add(row + col)", [
            ("len(cols) == 1 and col == 0",
             "({row}, {col}) is safe: **place a queen**. Remember its column ({col}) and its two diagonals "
             "(row − col = {row - col}, row + col = {row + col}). Every square it attacks turns red. Continue with row {row + 1}."),
            ("row == n - 1",
             "({row}, {col}) is not attacked: **place a queen** (column {col}, diagonals {row - col} and {row + col}). "
             "That was the last row."),
            (None,
             "({row}, {col}) is not attacked: **place a queen** (column {col}, diagonals {row - col} and {row + col}). "
             "Continue with row {row + 1}."),
        ]),
        ("anti.remove(row + col)", [
            ("col == n - 1",
             "Everything with a queen on ({row}, {col}) has been explored. **Remove** it and free its column and "
             "diagonals. That was the last column of row {row}, so this row is finished."),
            (None,
             "Everything with a queen on ({row}, {col}) has been explored. **Remove** it and free its column and "
             "diagonals, then try the columns to its right."),
        ]),
        ("return result", "The search is complete: **{len(_ret)} solutions** for {n} queens."),
    ],
    max_steps=140,
    say={
        "def solveNQueens": (
            "The function we must write. It gets `n` and returns every way to place `n` queens "
            "safely."
        ),
        "cols = set()": "The columns that already hold a queen.",
        "diag = set()": (
            "The `\\` diagonals that hold a queen. Along such a diagonal `row − col` stays the "
            "same, so that number names the diagonal."
        ),
        "anti = set()": (
            "The `/` diagonals that hold a queen. Along those, `row + col` stays the same."
        ),
        'board = [["."] * n for _ in range(n)]': "An `n × n` board of empty squares (`.`).",
        "result = []": "The list of solutions found.",
        "def place_queen(row)": "A helper that places queens on `row` and on every row below it.",
        "if row == n": "Has every row got a queen?",
        'result.append(["".join(line) for line in board])': (
            "Then this is a solution: save the board, each row turned into one string such as "
            "`.Q..`."
        ),
        "return@1": "And go back to try other placements.",
        "for col in range(n)": "Try each square in this row.",
        "if col in cols or (row - col) in diag or (row + col) in anti": (
            "Is the square's column, `\\` diagonal or `/` diagonal already taken by a queen?"
        ),
        "continue": "Then the square is attacked: skip it.",
        'board[row][col] = "Q"': "**Choose**: place a queen here.",
        "cols.add(col)": "Mark its column as taken.",
        "diag.add(row - col)": "Mark its `\\` diagonal as taken.",
        "anti.add(row + col)": "Mark its `/` diagonal as taken.",
        "place_queen(row + 1)": "**Explore**: move on to the next row (the helper calls itself).",
        'board[row][col] = "."': (
            "**Undo**: pick the queen up again, so the next square in this row can be tried."
        ),
        "cols.remove(col)": "Free its column.",
        "diag.remove(row - col)": "Free its `\\` diagonal.",
        "anti.remove(row + col)": "Free its `/` diagonal.",
        "place_queen(0)": "Start with the first row.",
        "return result": "Return every solution.",
    },
    time=("O(n!)", "The first row has n choices, the next at most n − 1, and so on; the attack sets make each check O(1)."),
    space=("O(n²)", "The board is n × n; the sets and the recursion hold at most n entries (not counting the output)."),
    tests=[
        ("n=1", [["Q"]]),
        ("n=2", []),
        ("n=3", []),
    ],
)

# end of c10_backtracking
