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
    time=("O(n!)", "The first row has n choices, the next at most n − 1, and so on; the attack sets make each check O(1)."),
    space=("O(n²)", "The board is n × n; the sets and the recursion hold at most n entries (not counting the output)."),
    tests=[
        ("n=1", [["Q"]]),
        ("n=2", []),
        ("n=3", []),
    ],
)

# end of c10_backtracking
