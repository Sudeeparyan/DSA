"""Math & Geometry."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "rotate-image",
    pattern="Transpose, then reverse each row",
    statement="""Rotate an `n × n` matrix by **90 degrees clockwise**, in place (without allocating
    a second matrix).""",
    args="matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]",
    result="matrix",
    expected=[[7, 4, 1], [8, 5, 2], [9, 6, 3]],
    why="The first column, read from the bottom up (7, 4, 1), has become the first row.",
    picture="""Picture the numbers printed on a square card. A quarter turn clockwise can be done with two
    flips. First flip the card over the diagonal that runs from the top-left corner to the
    bottom-right one, so every row becomes a column. Then flip each row left to right. Together the
    two flips put every number exactly where a quarter turn would.""",
    idea=[
        "Moving every element straight to its rotated position needs careful four-way swaps. Two simple mirror operations give the same result.",
        "**Transpose** the matrix: swap `matrix[i][j]` with `matrix[j][i]`, mirroring it across the main diagonal. Rows become columns.",
        "Then **reverse every row**. Together: element `(i, j)` goes to `(j, i)` and then to `(j, n − 1 − i)` — exactly a clockwise quarter turn.",
    ],
    views=[
        Grid("matrix", tones={"cur": "(i, j)", "alt": "(j, i)"}),
    ],
    notes=[
        ("n = len(matrix)",
         "A 90° clockwise rotation = **transpose** (mirror across the diagonal from top-left to bottom-right), "
         "then **reverse each row**. Step 1: transpose."),
        ("matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]", dict(
            post="Swap ({i}, {j}) with its mirror cell ({j}, {i}): {was.matrix[i][j]} and {was.matrix[j][i]} trade places.",
            when="i != j")),
        ("matrix[i].reverse()", [
            ("i == 0",
             "The matrix is transposed: its rows have become its columns. Step 2: reverse each row. "
             "Row 0: {was.matrix[0]} → **{matrix[0]}**."),
            (None, "Reverse row {i}: {was.matrix[i]} → **{matrix[i]}**."),
        ], {"matrix.good": "[(i, c) for c in range(n)]"}),
    ],
    outro="Done. The matrix is rotated 90° clockwise: `{matrix}`. It was changed in place, so nothing is returned.",
    key={"alt": "its mirror cell", "good": "row just reversed"},
    say={
        "def rotate": (
            "The function we must write. It gets the square `matrix` and turns it in place; it "
            "returns nothing."
        ),
        '"""@1': (
            "A note from LeetCode (a *docstring*): change the matrix itself, and do not return "
            "anything."
        ),
        "n = len(matrix)": (
            "`n` is the number of rows, and also of columns, since the matrix is square."
        ),
        "for i in range(n)@1": "Flip 1, over the diagonal: go through every row `i`,",
        "for j in range(i, n)": (
            "and every column `j` from the diagonal onwards. Starting at `i` swaps each pair only"
            " once; a second swap would undo the first."
        ),
        "matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]": (
            "Swap the cell in row `i`, column `j` with its mirror cell in row `j`, column `i`. "
            "Python can swap two things in one line like this."
        ),
        "for i in range(n)@2": "Flip 2: go through every row,",
        "matrix[i].reverse()": "and reverse it, so its last number comes first.",
    },
    time=("O(n²)", "Every cell is touched a constant number of times."),
    space=("O(1)", "Only swaps inside the matrix."),
    tests=[
        ("matrix=[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]",
         [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]),
        ("matrix=[[1]]", [[1]]),
        ("matrix=[[1, 2], [3, 4]]", [[3, 1], [4, 2]]),
    ],
)

lesson(
    "spiral-matrix",
    pattern="Peel off layers with four boundaries",
    statement="""Given an `m × n` matrix, return all of its elements in **spiral order**: along the
    top row, down the right column, back along the bottom row, up the left column, and so on
    inward.""",
    args="matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]",
    expected=[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
    why="Once around the outside (1 … 5), then the two cells left in the middle (6, 7).",
    picture="""Picture walking round a rectangular garden from the outside in. Walk along the top edge, down
    the right edge, back along the bottom and up the left. Each edge you finish is fenced off by
    moving a boundary one step inward, so the next lap is one ring smaller. Stop when the boundaries
    cross: nothing is left inside them.""",
    idea=[
        "Keep four boundaries — `top`, `bottom`, `left`, `right` — around the part of the matrix that has not been read yet.",
        "Read the **top row** left to right and move `top` down; read the **right column** top to bottom and move `right` left; read the **bottom row** right to left and move `bottom` up; read the **left column** bottom to top and move `left` right.",
        "Repeat while the boundaries have not crossed. Before the bottom row and the left column, check that a row / column is actually left — otherwise a single remaining row or column would be read twice.",
    ],
    init={"seen": "[]"},
    views=[
        Grid("matrix", title="matrix  (teal = not read yet, between the four boundaries)",
             tones={"win": "[(r, c) for r in range(top, bottom + 1) for c in range(left, right + 1)]",
                    "seen": "seen"}),
        Vars("top", "bottom", "left", "right"),
        Items("result", title="result"),
    ],
    notes=[
        ("top, bottom, left, right = 0, rows - 1, 0, cols - 1",
         "Four boundaries enclose everything that is still unread: rows `top` … `bottom`, columns `left` … `right`. "
         "At first that is the whole matrix."),
        ("result.append(matrix[top][j])", dict(
            post="**Top row**, left → right: read {matrix[top][j]}.",
            save={"seen": "seen + [(top, j)]"}, marks={"matrix.cur": "(top, j)", "result.good": "-1"})),
        ("top += 1", "The top row is finished: move `top` down to {top}."),
        ("result.append(matrix[i][right])", dict(
            post="**Right column**, top → bottom: read {matrix[i][right]}.",
            save={"seen": "seen + [(i, right)]"}, marks={"matrix.cur": "(i, right)", "result.good": "-1"})),
        ("right -= 1", [
            ("top > bottom", "No rows are left between `top` and `bottom`, so the right column had nothing to read. `right` still moves left to {right}."),
            (None, "The right column is finished: move `right` left to {right}."),
        ]),
        ("if top <= bottom", dict(
            no="`top` ({top}) has passed `bottom` ({bottom}): there is no separate bottom row left — skip it, or cells would be read twice.")),
        ("result.append(matrix[bottom][j])", dict(
            post="**Bottom row**, right → left: read {matrix[bottom][j]}.",
            save={"seen": "seen + [(bottom, j)]"}, marks={"matrix.cur": "(bottom, j)", "result.good": "-1"})),
        ("bottom -= 1", "The bottom row is finished: move `bottom` up to {bottom}."),
        ("if left <= right", dict(
            no="`left` ({left}) has passed `right` ({right}): there is no separate left column left — skip it.")),
        ("result.append(matrix[i][left])", dict(
            post="**Left column**, bottom → top: read {matrix[i][left]}.",
            save={"seen": "seen + [(i, left)]"}, marks={"matrix.cur": "(i, left)", "result.good": "-1"})),
        ("left += 1", [
            ("top > bottom", "Nothing was left for the left column either. `left` moves right to {left}."),
            (None, "The left column is finished: move `left` right to {left}. One full layer has been peeled off."),
        ]),
        ("return result", "The boundaries have crossed: everything has been read. **{_ret}**"),
    ],
    allow_unused=True,
    key={"win": "not read yet", "seen": "already read"},
    say={
        "def spiralOrder": (
            "The function we must write. It gets the `matrix` and returns its numbers in spiral "
            "order."
        ),
        "if not matrix": "Is the matrix empty?",
        "return []": "Then there is nothing to read.",
        "rows, cols = len(matrix), len(matrix[0])": "Count the rows and the columns.",
        "result = []": "The numbers in the order we read them.",
        "top, bottom, left, right = 0, rows - 1, 0, cols - 1": (
            "Four boundaries around the part not read yet: its first and last row, its first and "
            "last column. At first that is the whole matrix."
        ),
        "while top <= bottom and left <= right": (
            "Keep going while something is left between the boundaries."
        ),
        "for j in range(left, right + 1)": (
            "Top edge: go along the columns from `left` to `right`. (`range` stops just before "
            "its end, hence `right + 1`.)"
        ),
        "result.append(matrix[top][j])": "Read the number in the top row, column `j`.",
        "top += 1": "The top row is done: move the top boundary down one row.",
        "for i in range(top, bottom + 1)": "Right edge: go down the rows from `top` to `bottom`.",
        "result.append(matrix[i][right])": "Read the number in row `i` of the right column.",
        "right -= 1": "The right column is done: move the right boundary one column left.",
        "if top <= bottom": (
            "Is a row still left? If not, the bottom row would be one we have already read."
        ),
        "for j in range(right, left - 1, -1)": (
            "Bottom edge: go along the columns backwards, from `right` to `left`. The last `-1` "
            'means "count down".'
        ),
        "result.append(matrix[bottom][j])": "Read the number in the bottom row, column `j`.",
        "bottom -= 1": "The bottom row is done: move the bottom boundary up one row.",
        "if left <= right": "Is a column still left?",
        "for i in range(bottom, top - 1, -1)": (
            "Left edge: go up the rows, from `bottom` to `top`."
        ),
        "result.append(matrix[i][left])": "Read the number in row `i` of the left column.",
        "left += 1": (
            "The left column is done: move the left boundary one column right. One lap is "
            "complete."
        ),
        "return result": "Return the numbers in the order they were read.",
    },
    time=("O(m · n)", "Every element is read exactly once."),
    space=("O(1)", "Four boundaries (not counting the output list)."),
    tests=[
        ("matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]", [1, 2, 3, 6, 9, 8, 7, 4, 5]),
        ("matrix=[[1]]", [1]),
        ("matrix=[[1, 2, 3]]", [1, 2, 3]),
        ("matrix=[[1], [2], [3]]", [1, 2, 3]),
        ("matrix=[[1, 2], [3, 4], [5, 6], [7, 8]]", [1, 2, 4, 6, 8, 7, 5, 3]),
    ],
)

lesson(
    "set-matrix-zeroes",
    pattern="Record first, change afterwards",
    statement="""Given an `m × n` matrix, if an element is `0`, set its **entire row and column** to
    `0`. Do it in place.""",
    args="matrix=[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]",
    result="matrix",
    expected=[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]],
    why="The zeros at (0, 0) and (0, 3) clear row 0 and columns 0 and 3.",
    picture="""Picture a sheet of numbers where every 0 must wipe out its whole row and column. If you wiped
    while still reading, the zeros you had just written would look like original ones and wipe out
    even more. So work in two rounds. First only read, jotting down on a notepad which rows and
    which columns hold a 0. Then go over the sheet again and clear every number whose row or column
    is on the notepad.""",
    idea=[
        "Writing zeros while scanning is a trap: a freshly written 0 is indistinguishable from an original one and would wipe out further rows and columns.",
        "So separate the two jobs. **Pass 1**: only look, and record which rows and which columns contain an original 0.",
        "**Pass 2**: set every cell to 0 whose row or column was recorded.",
    ],
    views=[
        Grid("matrix", tones={"mark": "[(r, c) for r in range(rows) for c in range(cols) if r in zero_rows or c in zero_cols]",
                              "cur": "(i, j)"},
             title="matrix  (orange = in a recorded row or column)"),
        Vars(("zero_rows", "sorted(zero_rows)"), ("zero_cols", "sorted(zero_cols)")),
    ],
    notes=[
        ("zero_rows, zero_cols = set(), set()",
         "Pass 1 only **records** where the zeros are: `zero_rows` and `zero_cols` collect the rows and columns that must be cleared. "
         "Nothing is changed yet."),
        ("zero_cols.add(j)", "({i}, {j}) is 0 → remember **row {i}** and **column {j}**."),
        ("for i in range(rows):@2", dict(
            yes="Pass 1 is done. Pass 2: go through every cell again and clear it if its row or its column was recorded.",
            first=1)),
        ("matrix[i][j] = 0", dict(
            post="({i}, {j}) lies in {'recorded row %d' % i if i in zero_rows else 'recorded column %d' % j} → set it to 0.",
            when="was.matrix[i][j] != 0", marks={"matrix.bad": "(i, j)"})),
    ],
    outro="Done. Every row and column that contained a 0 is cleared. The matrix was changed in place, so nothing is returned.",
    key={"mark": "in a recorded row or column", "bad": "just set to 0"},
    say={
        "def setZeroes": (
            "The function we must write. It gets the `matrix` and changes it in place; it returns"
            " nothing."
        ),
        '"""@1': (
            "A note from LeetCode (a *docstring*): change the matrix itself, and do not return "
            "anything."
        ),
        "rows, cols = len(matrix), len(matrix[0])": "Count the rows and the columns.",
        "zero_rows, zero_cols = set(), set()": (
            "Two empty **sets** (collections without repeats): the rows and the columns that hold"
            " a 0. This is the notepad."
        ),
        "for i in range(rows):@1": "Round 1, only reading: go through every row,",
        "for j in range(cols):@1": "and every column in it.",
        "if matrix[i][j] == 0": "Is this number a 0?",
        "zero_rows.add(i)": "Then write down its row,",
        "zero_cols.add(j)": "and its column.",
        "for i in range(rows):@2": "Round 2, clearing: go through every row again,",
        "for j in range(cols):@2": "and every column.",
        "if i in zero_rows or j in zero_cols": "Is this cell's row or its column on the notepad?",
        "matrix[i][j] = 0": "Then set it to 0.",
    },
    time=("O(m · n)", "Two passes over the matrix."),
    space=("O(m + n)", "The two sets. (The first row and column of the matrix itself can serve as the markers to reach O(1).)"),
    tests=[
        ("matrix=[[1, 1, 1], [1, 0, 1], [1, 1, 1]]", [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
        ("matrix=[[1, 2], [3, 4]]", [[1, 2], [3, 4]]),
        ("matrix=[[0]]", [[0]]),
        ("matrix=[[1, 0, 3]]", [[0, 0, 0]]),
    ],
)

lesson(
    "happy-number",
    pattern="Cycle detection with slow and fast pointers",
    statement="""Replace a number by the **sum of the squares of its digits**, and repeat. A number
    is *happy* if this process reaches `1`. Otherwise it loops forever without ever reaching 1.
    Return `True` if `n` is happy.""",
    pre="""
    def _nx(x):
        return sum(int(d) ** 2 for d in str(x))

    def _sq(x):
        return " + ".join(d + "²" for d in str(x))

    def _seq(x, limit=14):
        out = []
        while x not in out and len(out) < limit:
            out.append(x)
            x = _nx(x)
        return out
    """,
    args="n=19",
    expected=True,
    why="19 → 82 → 68 → 100 → 1.",
    picture="""Picture a chain where every number points to exactly one next number: the sum of its digits
    squared. Following it, you either reach 1 (and stay there) or go round in a circle forever. To
    tell which without writing every number down, send two walkers along the chain: one takes one
    step at a time, the other two. If there is a circle, the fast walker catches up with the slow
    one, the way a fast runner laps a slow one on a track.""",
    idea=[
        "Each number leads to exactly one next number, like a linked list. The chain either arrives at 1 (and then stays there, since 1² = 1) or runs into a **cycle**.",
        "A cycle can be detected without remembering every number seen: let `slow` advance one step at a time and `fast` two steps. In a cycle, `fast` eventually catches up with `slow`.",
        "So loop until `fast` reaches 1 (happy) or `fast` meets `slow` (a cycle that does not contain 1).",
    ],
    views=[
        Arr("_seq(n)", id="chain", idx=False, title="the chain: each number → sum of its squared digits",
            ptrs={"slow": ("_seq(n).index(slow)", "slow in _seq(n)"), "fast": ("_seq(n).index(fast)", "fast in _seq(n)")}),
        Vars("slow", "fast"),
    ],
    notes=[
        ("slow, fast = n, get_next(n)", dict(
            post="`slow` starts on {slow}. `fast` starts one step ahead: {_sq(n)} = **{fast}**.")),
        ("slow = get_next(slow)", "`slow` moves **one** step: {_sq(was.slow)} = **{slow}**."),
        ("fast = get_next(get_next(fast))",
         "`fast` moves **two** steps: {was.fast} → {_nx(was.fast)} → **{fast}**."),
        ("while fast != 1 and slow != fast", dict(
            no=[
                ("fast == 1", "`fast` has reached **1**. The chain ends there, so the number is happy."),
                (None, "`fast` has caught up with `slow` at {slow}: the chain goes round in a **cycle** that never contains 1."),
            ])),
        ("return fast == 1", [
            ("_ret", "The chain reached 1, so the number is happy → **True**."),
            (None, "The chain is stuck in a cycle without 1, so the number is not happy → **False**."),
        ]),
    ],
    say={
        "def isHappy": (
            "The function we must write. It gets the number `n` and answers whether it is happy."
        ),
        "def get_next(num)": (
            "A small helper that works out the next number in the chain: the sum of the squares "
            "of `num`'s digits."
        ),
        "next_num = 0": "The sum so far.",
        "while num > 0": "While digits are left:",
        "num, digit = divmod(num, 10)": (
            "`divmod(num, 10)` splits off the last digit: for 82 it gives 8 (the rest) and 2 (the"
            " last digit)."
        ),
        "next_num += digit**2": 'Add that digit squared. `**2` means "to the power 2".',
        "return next_num": "Hand back the sum.",
        "slow, fast = n, get_next(n)": (
            "Two walkers on the chain: `slow` starts at `n`, `fast` one step ahead."
        ),
        "while fast != 1 and slow != fast": (
            "Keep going while `fast` has not reached 1 and has not caught up with `slow`."
        ),
        "slow = get_next(slow)": "`slow` takes one step.",
        "fast = get_next(get_next(fast))": "`fast` takes two steps.",
        "return fast == 1": (
            "If `fast` stopped at 1, the number is happy (`True`). Otherwise it met `slow` in a "
            "circle (`False`)."
        ),
    },
    time=("O(log n)", "The numbers shrink very quickly (any number below 1000 maps to at most 243), and the cycle is short."),
    space=("O(1)", "Two numbers — no set of seen values."),
    tests=[("n=2", False), ("n=1", True), ("n=7", True), ("n=4", False), ("n=100", True)],
)

lesson(
    "plus-one",
    pattern="Add from the right, carry while the digit is 9",
    statement="""A large integer is given as an array of its `digits`, most significant digit first.
    Add one to the integer and return the resulting array of digits.""",
    args="digits=[1, 9, 9]",
    expected=[2, 0, 0],
    why="199 + 1 = 200: both 9s roll over to 0 and the carry finally lands on the 1.",
    picture="""Picture the mileage counter in a car rolling over from 199 to 200. Adding one turns the last
    wheel first. A wheel showing less than 9 simply moves up one, and nothing else moves. A wheel
    showing 9 rolls round to 0 and nudges the wheel on its left. If every wheel showed 9, a new
    wheel showing 1 is needed at the front.""",
    idea=[
        "Adding one affects the **last** digit first, exactly as on paper.",
        "If that digit is less than 9, increase it and stop — nothing else changes. If it is 9, it becomes 0 and the `+1` **carries** to the digit on its left.",
        "If the carry runs past the first digit (the number was all 9s), the result needs one more digit: a leading 1.",
    ],
    views=[
        Arr("digits", ptrs=["i"]),
    ],
    notes=[
        ("digits[i] += 1",
         "The digit at index {i} is {was.digits[i]}, less than 9: add 1 → **{digits[i]}**. No carry is produced, so we are finished.",
         {"digits.good": "i"}),
        ("digits[i] = 0",
         "The digit at index {i} is 9: 9 + 1 = 10. Write **0** here and **carry** the 1 to the digit on the left.",
         {"digits.bad": "i"}),
        ("return digits", "The carry has been absorbed: **{_ret}**."),
        ("return [1] + digits",
         "Every digit was 9 and is now 0, but the carry is still left over. Put a new **1** in front: **{_ret}**."),
    ],
    allow_unused=True,
    key={"good": "+1 absorbed here", "bad": "9 rolled over to 0"},
    say={
        "def plusOne": (
            "The function we must write. It gets the `digits` of a number and returns the digits "
            "of that number plus one."
        ),
        "n = len(digits)": "How many digits there are.",
        "for i in range(n - 1, -1, -1)": (
            "Go through the positions from the last back to the first. `range(n - 1, -1, -1)` "
            "counts down from `n - 1` to 0."
        ),
        "if digits[i] < 9": "Is this digit less than 9?",
        "digits[i] += 1": 'Then add 1 to it. `+=` means "increase by".',
        "return digits": "Nothing carries any further: we are finished.",
        "digits[i] = 0": (
            "The digit was 9, and 9 + 1 = 10: write 0 here and carry the 1 to the digit on the "
            "left, in the next round of the loop."
        ),
        "return [1] + digits": (
            "Every digit was 9 and is now 0: put a new 1 in front, as in 999 + 1 = 1000."
        ),
    },
    time=("O(n)", "At most one pass over the digits; usually it stops at the last digit."),
    space=("O(1)", "In place (a new list is built only when every digit was 9)."),
    tests=[("digits=[1, 2, 3]", [1, 2, 4]), ("digits=[9]", [1, 0]), ("digits=[9, 9]", [1, 0, 0]),
           ("digits=[0]", [1]), ("digits=[4, 3, 2, 1]", [4, 3, 2, 2])],
)

lesson(
    "powx-n",
    pattern="Fast exponentiation (square the half)",
    statement="""Implement `pow(x, n)`: compute `x` raised to the integer power `n` (which may be
    negative).""",
    args="x=2.0, n=10",
    expected=1024.0,
    why="2¹⁰ = (2⁵)² = 32² = 1024.",
    picture="""Picture working out 2¹⁰ by halving. 2¹⁰ is 2⁵ times 2⁵, so work out 2⁵ just once and multiply it
    by itself. 2⁵ is 2 × 2² × 2², and so on, down to a power of 0. Each step halves the power, so
    even a power of a billion takes about 30 steps instead of a billion multiplications.""",
    idea=[
        "Multiplying `x` by itself `n` times costs O(n) — far too slow for exponents in the billions.",
        "Use `xⁿ = (x^(n/2))²`: compute the **half** power once and square it. If `n` is odd, one extra factor `x` is needed: `xⁿ = x · (x^(n//2))²`.",
        "Each call halves the exponent, so only about log₂(n) multiplications are needed. A negative exponent is handled first with `x⁻ⁿ = (1/x)ⁿ`.",
    ],
    views=[
        RecTree("helper", "{cell(base)}^{exp}", title="recursion  (each call halves the exponent)", ret=True),
        Vars("temp"),
    ],
    notes=[
        ("if n < 0", dict(
            yes="The exponent is negative. Use x⁻ⁿ = (1/x)ⁿ: replace x by 1/x and make the exponent positive.",
            no="The exponent {n} is not negative, so x and n can be used as they are.")),
        ("if exp == 0", dict(yes="Anything to the power 0 is **1**. This is where the halving stops.")),
        ("temp = helper(base, exp // 2)", dict(
            pre="{cell(base)}^{exp}: instead of {exp} separate multiplications, compute the **half** power "
                "{cell(base)}^{exp // 2} once and square it.")),
        ("return temp * temp",
         "{exp} is **even**: {cell(base)}^{exp} = ({cell(base)}^{exp // 2})² = {cell(temp)} × {cell(temp)} = **{cell(_ret)}**."),
        ("return base * temp * temp",
         "{exp} is **odd**: one extra factor is needed. {cell(base)}^{exp} = {cell(base)} × ({cell(base)}^{exp // 2})² = "
         "{cell(base)} × {cell(temp)} × {cell(temp)} = **{cell(_ret)}**."),
        ("return helper(x, n)", "The answer is **{cell(_ret)}**."),
    ],
    key={"win": "call waiting for its half power"},
    say={
        "def myPow": (
            "The function we must write. It gets a number `x` and a whole-number power `n`, and "
            "returns `x` to the power `n`."
        ),
        "def helper(base, exp)": (
            "A helper that works out `base` to the power `exp` (0 or more). It calls itself on "
            "half the power."
        ),
        "if exp == 0": "Is the power 0?",
        "return 1.0": "Any number to the power 0 is 1.",
        "temp = helper(base, exp // 2)": (
            "Work out the half power once. `//` divides and drops the remainder, so 5 // 2 is 2."
        ),
        "if exp % 2 == 0": (
            'Is the power even? `%` gives the remainder after dividing, so this asks "does 2 go '
            'into it exactly?"'
        ),
        "return temp * temp": "Then the answer is the half power times itself.",
        "else:": "Otherwise the power is odd,",
        "return base * temp * temp": (
            "and the two halves miss one factor: multiply in one more `base`."
        ),
        "if n < 0": "Is the power negative?",
        "x = 1 / x": "Then use x⁻ⁿ = (1/x)ⁿ: replace `x` by 1 divided by `x`,",
        "n = -n": "and make the power positive.",
        "return helper(x, n)": "Work out the power with the helper and return it.",
    },
    time=("O(log n)", "The exponent is halved on every call."),
    space=("O(log n)", "The recursion is about log₂(n) calls deep."),
    tests=[("x=2.1, n=3", 9.261), ("x=2.0, n=-2", 0.25), ("x=5.0, n=0", 1.0), ("x=1.0, n=2147483647", 1.0),
           ("x=-2.0, n=3", -8.0)],
)

lesson(
    "multiply-strings",
    pattern="Grade-school multiplication, digit by digit",
    statement="""Two non-negative integers are given as strings `num1` and `num2`. Return their
    product as a string — without converting the whole strings to integers.""",
    args='num1="23", num2="45"',
    expected="1035",
    why="23 × 45 = 1035.",
    picture="""Picture long multiplication on paper, with a row of boxes for the answer. Multiply every digit
    of the first number by every digit of the second. Where each small product goes depends only on
    the two digits' positions: digit `i` times digit `j` lands in box `i + j + 1`. Add it to what
    that box already holds, keep the last digit there, and carry the rest into the box on its left.""",
    idea=[
        "Multiply the way it is done on paper: every digit of `num1` times every digit of `num2`.",
        "Where does each small product go? Digit `i` of `num1` times digit `j` of `num2` contributes to position **`i + j + 1`** of the result, and its carry to position **`i + j`**. (An m-digit number times an n-digit number has at most m + n digits.)",
        "Working from the right, add each product to what is already in its cell, keep the last digit there and push the carry one cell to the left.",
    ],
    views=[
        Arr("num1", ptrs=["i"]),
        Arr("num2", ptrs=["j"]),
        Arr("result", title="result  (one digit per cell)"),
    ],
    notes=[
        ("if num1 == ", dict(yes="One factor is 0, so the product is 0.")),
        ("result = [0] * (m + n)",
         "A {m}-digit number times a {n}-digit number has at most {m + n} digits, so `result` gets {m + n} cells. "
         "The product of digit i and digit j belongs in cell **i + j + 1**; its carry goes to cell **i + j**."),
        ("result[i + j] += sum_val // 10",
         "{num1[i]} × {num2[j]} = {product}. Add what is already in cell {i + j + 1}: {sum_val}. "
         "Keep its last digit **{sum_val % 10}** in cell {i + j + 1} and carry **{sum_val // 10}** into cell {i + j}.",
         {"result.cur": "i + j + 1", "result.alt": "i + j"}),
        ('return "".join(map(str, result)).lstrip("0")',
         "Join the cells into a string and strip leading zeros: **{_ret}**."),
    ],
    allow_unused=True,
    key={"cur": "box i + j + 1: keeps the last digit", "alt": "box i + j: gets the carry"},
    say={
        "def multiply": (
            "The function we must write. It gets two numbers written as text, `num1` and `num2`, "
            "and returns their product as text."
        ),
        'if num1 == "0" or num2 == "0"': "Is either number 0?",
        'return "0"': "Then the product is 0.",
        "m, n = len(num1), len(num2)": "Count the digits of each number.",
        "result = [0] * (m + n)": (
            "A row of `m + n` boxes, all 0. An `m`-digit number times an `n`-digit number has at "
            "most `m + n` digits."
        ),
        "for i in range(m - 1, -1, -1)": (
            "Go through the digits of `num1` from the last to the first,"
        ),
        "for j in range(n - 1, -1, -1)": (
            "and for each one, through the digits of `num2` from the last to the first."
        ),
        "product = int(num1[i]) * int(num2[j])": (
            'Multiply the two digits. `int(...)` turns a character such as "3" into the number 3.'
        ),
        "sum_val = product + result[i + j + 1]": "Add what box `i + j + 1` already holds.",
        "result[i + j + 1] = sum_val % 10": (
            "Keep the last digit in that box. `% 10` is the remainder after dividing by 10, which"
            " is the last digit."
        ),
        "result[i + j] += sum_val // 10": (
            "Carry the rest into the box on its left. `// 10` divides by 10 and drops the "
            "remainder."
        ),
        'return "".join(map(str, result)).lstrip("0")': (
            "Turn every box back into a character, glue them together, and strip the 0s at the "
            "front."
        ),
    },
    time=("O(m · n)", "Every pair of digits is multiplied once."),
    space=("O(m + n)", "The result array."),
    tests=[('num1="2", num2="3"', "6"), ('num1="123", num2="456"', "56088"), ('num1="0", num2="52"', "0"),
           ('num1="999", num2="999"', "998001"), ('num1="9", num2="9"', "81")],
)

lesson(
    "detect-squares",
    pattern="Hash map of points; fix one side, look up the other two corners",
    statement="""Design a structure that receives points on the plane. `add(point)` stores a point
    (duplicates are allowed and count separately). `count(point)` returns how many **axis-aligned
    squares** with positive area can be formed using the query point and three stored points.""",
    pre="""
    def _pts(obj, extra=None):
        pts = {(px, py) for px, col in obj.points.items() for py, c in col.items() if c}
        if extra is not None:
            pts.add(tuple(extra))
        return sorted(pts)
    """,
    ops=["DetectSquares()", "add([3, 10])", "add([11, 2])", "add([3, 2])", "count([11, 10])", "count([14, 8])",
         "add([11, 2])", "count([11, 10])"],
    expected=[None, None, None, None, 1, 0, None, 2],
    why="(11, 10) completes a square with the three stored points. Adding (11, 2) a second time makes two such squares.",
    picture="""Picture pins stuck in a corkboard, some of them pinned more than once. A square with sides along
    the grid lines that has the query point as a corner needs another corner straight above or below
    it, and that pin fixes the side length. The other two corners must then be that far to the left
    or to the right. If those pins are there, the number of squares is the product of how many times
    each of the three corners was pinned.""",
    idea=[
        "Store how often each point was added: `points[x][y]` = count. Looking up whether a point exists is then O(1).",
        "An axis-aligned square through the query point `(x, y)` has another corner **straight above or below it**, at `(x, y2)`. That fixes the side length `|y2 − y|`.",
        "The remaining two corners must then be at `(x ± side, y)` and `(x ± side, y2)`. If they exist, the number of squares is the **product of the three corner counts** (duplicates give separate squares).",
    ],
    init={"sq": "[]"},
    views=[
        Graph("_pts(self, point if 'point' in dir() else None)", edges="sq", id="plane",
              title="points on the plane",
              pos={(3, 10): (-2.6, 1.8), (11, 2): (1.4, -1.8), (3, 2): (-2.6, -1.8), (11, 10): (1.4, 1.8), (14, 8): (2.9, 0.9)},
              labels="{k: '%d,%d' % k for k in _pts(self, point if 'point' in dir() else None)}",
              badges="{k: 'x%d' % self.points[k[0]][k[1]] for k in _pts(self) if self.points[k[0]][k[1]] > 1}",
              tones={"cur": "tuple(point)"}),
        Vars("count", "side_length"),
    ],
    notes=[
        ("self.points = defaultdict(",
         "`points[x][y]` counts how many times the point (x, y) has been added. Duplicates are counted, not merged."),
        ("self.points[x][y] += 1", "Store ({x}, {y}). It has now been added {plural(self.points[x][y], 'time')}."),
        ("count = 0", dict(
            post="Count the squares that have ({x}, {y}) as a corner. Every such square has another corner **directly "
                 "above or below** the query point, so go through the stored points with the same x = {x}.",
            save={"sq": "[]"})),
        ("side_length = abs(y2 - y)",
         "({x}, {y2}) is stored and lies straight {'below' if y2 < y else 'above'} the query point: a vertical side of "
         "length **{side_length}**. The other two corners must be {side_length} to the right (x = {x + side_length}) "
         "or to the left (x = {x - side_length}).",
         {"plane.alt": "(x, y2)"}),
        ("if x2 in self.points and y in self.points[x2]", dict(
            no="x = {x2}: the corner ({x2}, {y}) is not stored, so there is no square on this side.")),
        ("count += (", dict(
            post=[
                ("count > was.count",
                 "x = {x2}: the corners ({x2}, {y}) and ({x2}, {y2}) are both stored — a square. Multiply the three "
                 "corner counts: {self.points[x2][y]} × {self.points[x2][y2]} × {self.points[x][y2]} = "
                 "{count - was.count}. `count` = **{count}**."),
                (None, "x = {x2}: ({x2}, {y}) is stored, but the fourth corner ({x2}, {y2}) is not. No square."),
            ],
            save={"sq": "[((x, y), (x2, y)), ((x2, y), (x2, y2)), ((x2, y2), (x, y2)), ((x, y2), (x, y))] if count > was.count else sq"},
            marks={"plane.good": "[(x2, y), (x2, y2), (x, y2)]"})),
        ("return count", [
            ("not [k for k in self.points[x] if k != y]",
             "No stored point lies directly above or below ({x}, {y}), so no square can have it as a corner → **0**."),
            (None, "Squares with ({x}, {y}) as a corner: **{count}**."),
        ]),
    ],
    allow_unused=True,
    key={"cur": "point being added or asked about", "alt": "corner straight above or below", "good": "the other corners of a possible square"},
    say={
        "class DetectSquares": "The class we must write. It stores points and counts squares.",
        "def __init__": "Runs once, when a `DetectSquares` is created.",
        "self.points = defaultdict(lambda: defaultdict(int))": (
            "`points[x][y]` counts how many times the point (x, y) was added. Both levels are "
            "`defaultdict`s, so a point never added simply counts as 0."
        ),
        "def add": "Store one more point.",
        "x, y = point@1": "Unpack the point into its `x` and `y`.",
        "self.points[x][y] += 1": "Count it once more.",
        "def count": "Count the squares that have `point` as one corner.",
        "x, y = point@2": "Unpack the query point.",
        "count = 0": "Squares found so far.",
        "for y2 in self.points[x]": (
            "Go through every stored point with the same `x`: each lies straight above or below "
            "the query point."
        ),
        "if y2 != y": "Skip the query point's own height: a square needs a side longer than 0.",
        "side_length = abs(y2 - y)": (
            "The vertical side runs from `y` to `y2`. `abs` makes its length positive."
        ),
        "for x2 in (x + side_length, x - side_length)": (
            "The square can stick out to the right or to the left: try both."
        ),
        "if x2 in self.points and y in self.points[x2]": "Is a corner stored at (`x2`, `y`)?",
        "count += (": (
            "Then add the number of squares: the three corner counts multiplied. A missing fourth"
            " corner counts 0, so it adds nothing."
        ),
        "return count": "Return the number of squares.",
    },
    time=("O(1) add, O(n) count", "`count` looks at every stored point that shares the query's x-coordinate."),
    space=("O(n)", "One counter per distinct point."),
    tests=[
        (["DetectSquares()", "add([0, 0])", "add([0, 2])", "add([2, 0])", "count([2, 2])", "add([4, 2])", "add([4, 0])",
          "count([2, 2])", "count([0, 0])", "count([1, 1])"],
         [None, None, None, None, 1, None, None, 2, 0, 0]),
        (["DetectSquares()", "add([5, 5])", "add([5, 5])", "count([5, 5])"], [None, None, None, 0]),
    ],
)

# end of c17_math_geometry
