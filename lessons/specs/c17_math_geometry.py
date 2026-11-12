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
