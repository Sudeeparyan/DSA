"""Stack."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "valid-parentheses",
    pattern="Stack of unclosed brackets",
    statement="""Given a string made only of the characters `( ) [ ] { }`, decide whether it is
    valid: every opening bracket must be closed by the **same type** of bracket, and brackets
    must be closed in the correct order.""",
    args="s='([]{})'",
    expected=True,
    why="Every bracket is closed by its own kind, innermost first.",
    idea=[
        "The bracket opened **last** must be the one closed **first**. That is exactly how a stack behaves: last in, first out.",
        "See an opening bracket → push it. It waits on the stack for its partner.",
        "See a closing bracket → it must match the **top** of the stack. If it does, pop. If it does not (or the stack is empty), the string is invalid.",
        "At the end the stack must be empty — anything left was never closed.",
    ],
    views=[
        Arr("s", ptrs={"char": "at('for char in s')"},
            tones={"dim": "range(upto('for char in s'))", "cur": "at('for char in s')"}),
        Stack("stack"),
        HMap("parentheses_map", title="closing → opening it needs"),
    ],
    notes=[
        ("stack = []",
         "We keep a **stack** of opening brackets that are still waiting to be closed. It starts empty."),
        ("parentheses_map =",
         "This map tells us which opening bracket each closing bracket needs."),
        ("stack.append(char)",
         "`{char}` is an **opening** bracket. Push it — it now waits on top of the stack for its partner."),
        ("elif char in parentheses_map", dict(
            yes="`{char}` is a **closing** bracket. It has to match the most recent unclosed opening "
                "bracket, which is the **top of the stack**: `{stack[-1] if stack else 'nothing'}`.",
            yes_marks={"stack.alt": "-1", "parentheses_map.cur": "char"})),
        ("stack.pop()",
         "The top is `{was.stack[-1]}`, exactly what `{char}` needs. The pair is complete, so pop it."),
        ("return not stack",
         "All characters are processed and the stack is **empty**: every opening bracket found its partner. "
         "Return **{_ret}**."),
    ],
    time=("O(n)", "Each character is pushed and popped at most once."),
    space=("O(n)", "A string of only opening brackets puts every character on the stack."),
    tests=[("s='()[]{}'", True), ("s='(]'", False), ("s='(['", False), ("s=']'", False)],
)

lesson(
    "min-stack",
    pattern="Second stack that tracks the minimum",
    statement="""Design a stack that supports `push`, `pop`, `top`, and `getMin` — where `getMin`
    returns the smallest value currently in the stack — with **every operation in O(1) time**.""",
    ops=["MinStack()", "push(5)", "push(3)", "push(7)", "getMin()", "pop()", "pop()", "getMin()", "top()"],
    expected=[None, None, None, None, 3, None, None, 5, 5],
    why="After popping 7 and 3 only 5 is left, so it is both the top and the minimum.",
    idea=[
        "A normal stack gives push, pop and top in O(1). The hard part is `getMin` — scanning the stack would be O(n).",
        "Trick: keep a **second stack** whose top is always the current minimum.",
        "Push onto it only when the new value is ≤ the current minimum. Pop from it only when the value leaving the main stack *is* that minimum. Then the old minimum is right underneath, ready to take over.",
    ],
    views=[
        Stack("self.stack", title="stack", id="stack"),
        Stack("self.min_stack", title="min_stack  (top = current minimum)", id="min_stack"),
    ],
    notes=[
        ("self.min_stack = []",
         "Two stacks: `stack` holds every value, `min_stack` holds the minimums — its top is always the smallest value in `stack`."),
        ("self.stack.append(val)", "Push {val} onto the main stack.", {"stack.cur": "-1"}),
        ("if not self.min_stack or val <= self.min_stack[-1]", dict(
            no="{val} is larger than the current minimum {self.min_stack[-1]}, so the minimum does not change. "
               "`min_stack` is left alone.",
            no_marks={"stack.cur": "-1", "min_stack.alt": "-1"})),
        ("self.min_stack.append(val)",
         "{val} is {'the first value' if len(self.min_stack) == 1 else 'not larger than the old minimum ' + str(self.min_stack[-2])}, "
         "so it is the **new minimum**. Push it onto `min_stack` too.",
         {"stack.cur": "-1", "min_stack.good": "-1"}),
        ("if self.stack[-1] == self.min_stack[-1]", dict(
            no="The value leaving is {self.stack[-1]}, but the minimum is {self.min_stack[-1]}. "
               "The minimum survives, so `min_stack` is untouched.",
            no_marks={"stack.bad": "-1", "min_stack.alt": "-1"})),
        ("self.min_stack.pop()",
         "The value leaving ({self.stack[-1]}) **is** the current minimum, so remove it from `min_stack` as well. "
         "The previous minimum underneath takes over.",
         {"stack.bad": "-1"}),
        ("self.stack.pop()", "Pop the top of the main stack."),
        ("return self.min_stack[-1]",
         "The minimum is simply the top of `min_stack`: **{_ret}**. No searching needed.",
         {"min_stack.good": "-1"}),
        ("return self.stack[-1]", "`top` is the top of the main stack: **{_ret}**.", {"stack.good": "-1"}),
    ],
    time=("O(1)", "Every operation only touches the tops of the two stacks."),
    space=("O(n)", "In the worst case (values pushed in decreasing order) both stacks hold n values."),
    tests=[
        (["MinStack()", "push(-2)", "push(0)", "push(-3)", "getMin()", "pop()", "top()", "getMin()"],
         [None, None, None, None, -3, None, 0, -2]),
    ],
)

lesson(
    "evaluate-reverse-polish-notation",
    pattern="Stack of operands",
    statement="""Evaluate an arithmetic expression written in **Reverse Polish Notation**, where
    each operator comes *after* its two operands (`3 4 +` means 3 + 4). The operators are
    `+ - * /`, and division truncates toward zero.""",
    args="tokens=['4', '13', '5', '/', '+']",
    expected=6,
    why="13 / 5 = 2 (truncated), then 4 + 2 = 6.",
    idea=[
        "In this notation an operator always applies to the **two most recent values** — either numbers just read, or results just computed.",
        "*Most recent first* is exactly what a stack gives. Number → push it. Operator → pop two values, combine them, and push the result back.",
        "The first value popped is the **right-hand** operand. That matters for `−` and `/`. At the end, the one value left on the stack is the answer.",
    ],
    views=[
        Arr("tokens", ptrs={"token": "at('for token in tokens')"},
            tones={"dim": "range(upto('for token in tokens'))", "cur": "at('for token in tokens')"}),
        Stack("stack"),
        Vars("num1", "num2"),
    ],
    notes=[
        ("stack = []", "Numbers wait on a stack until an operator comes along to use them."),
        ("stack.append(int(token))", "`{token}` is a number. Push it onto the stack.", {"stack.cur": "-1"}),
        ("num1 = stack.pop()",
         "`{token}` is an **operator**. It uses the two most recent values, so pop them: first the right-hand "
         "one, `num2` = {num2}, then the left-hand one, `num1` = {num1}."),
        ("stack.append(num1 + num2)",
         "{num1} + {num2} = **{num1 + num2}**. Push the result back — it may be an operand for a later operator.",
         {"stack.good": "-1"}),
        ("stack.append(int(num1 / num2))",
         "{num1} / {num2} = {num1 / num2:.2f}, truncated toward zero → **{int(num1 / num2)}**. Push the result "
         "back — it may be an operand for a later operator.",
         {"stack.good": "-1"}),
        ("return stack[0]",
         "Every token has been used. The single value left on the stack is the answer: **{_ret}**.",
         {"stack.good": "0"}),
    ],
    time=("O(n)", "Each token is handled once with O(1) stack work."),
    space=("O(n)", "The stack can hold up to about half of the tokens."),
    tests=[("tokens=['2', '1', '+', '3', '*']", 9),
           ("tokens=['10','6','9','3','+','-11','*','/','*','17','+','5','+']", 22),
           ("tokens=['3', '-4', '-']", 7)],
)

lesson(
    "generate-parentheses",
    pattern="Backtracking with open / close counts",
    statement="""Given `n` pairs of parentheses, generate **every** well-formed combination. For
    n = 3 there are five, such as `((()))` and `()(())`.""",
    args="n=3",
    expected=["((()))", "(()())", "(())()", "()(())", "()()()"],
    why="These are the only 5 ways to arrange three ( and three ) so that every ) closes an earlier (.",
    idea=[
        "Build the string one character at a time, and only ever make moves that keep it valid — then every finished string is automatically well-formed.",
        "Rule 1: a `(` may be added while fewer than `n` have been used.",
        "Rule 2: a `)` may be added only while there are more `(` than `)` so far, so it has something to close. Try both moves wherever they are allowed (backtracking).",
    ],
    views=[
        RecTree("backtrack", "{s if s else '\"\"'}", title="recursion tree  (each box is the string built so far)",
                mark_call={"good": "len(s) == 2 * n"}),
        Items("result", title="result"),
        Vars("open_count", "close_count"),
    ],
    notes=[
        ("result.append(s)",
         "`{s}` has length {2 * n}: all {n} pairs are placed. Only legal moves were made, so it is well-formed. Save it.",
         {"result.good": "-1"}),
        ('backtrack(s + "("', dict(
            pre="`{show(s)}` has used {open_count} of its {n} opening brackets, so another `(` is allowed. Try `{s}(`.")),
        ('backtrack(s + ")"', dict(
            pre="`{show(s)}` has {open_count} `(` but only {close_count} `)`, so a `)` has something to close. Try `{s})`.")),
    ],
    time=("O(4ⁿ / √n)", "There are about 4ⁿ / (n · √n) valid strings (the Catalan numbers), and each one takes O(n) to build."),
    space=("O(n)", "The recursion is 2n deep (not counting the output list)."),
    tests=[("n=1", ["()"]), ("n=2", ["(())", "()()"])],
)

lesson(
    "daily-temperatures",
    pattern="Monotonic stack",
    statement="""Given the daily `temperatures`, return a list where `answer[i]` is the number of
    days you have to wait after day `i` for a **warmer** temperature. Use 0 if no warmer day
    ever comes.""",
    args="temperatures=[73, 74, 75, 71, 69, 72, 76, 73]",
    expected=[1, 1, 4, 2, 1, 1, 0, 0],
    why="For example day 2 (75°) waits 4 days for day 6 (76°); days 6 and 7 never see a warmer day.",
    idea=[
        "For each day, scanning forward for the next warmer day is O(n²).",
        "Walk **from right to left** and keep a stack of later days that could still be someone's *next warmer day*.",
        "A later day that is not warmer than today is useless from now on: today is closer *and* at least as warm, so today hides it. Pop those. Whatever is then on top is today's next warmer day.",
    ],
    views=[
        Arr("temperatures", ptrs=["i"], tones={"seen": "stack", "cur": "i"}),
        Arr("result", ptrs=["i"]),
        Stack("[f'{j}:{temperatures[j]}' for j in stack]", id="stack",
              title="stack  (day:temperature — candidates to the right)"),
    ],
    notes=[
        ("stack = []",
         "We walk the days from **right to left**. The stack holds later days that could still be the "
         "*next warmer day* for someone."),
        ("result = [0] * len(temperatures)", "Every answer starts at 0, meaning *no warmer day found*."),
        ("stack.pop()",
         "Day {was.stack[-1]} ({temperatures[was.stack[-1]]}°) is not warmer than day {i} ({temperatures[i]}°). "
         "Day {i} is closer and at least as warm, so day {was.stack[-1]} can never be an answer again. Pop it."),
        ("if stack", dict(
            no="The stack is empty: no later day is warmer than day {i} ({temperatures[i]}°). Its answer stays 0.")),
        ("result[i] = stack[-1] - i",
         "The top of the stack, day {stack[-1]} ({temperatures[stack[-1]]}°), is the **next warmer day** after "
         "day {i} ({temperatures[i]}°). Wait: {stack[-1]} − {i} = **{result[i]}**.",
         {"result.good": "i", "temperatures.good": "stack[-1]", "stack.good": "-1"}),
        ("stack.append(i)",
         "Push day {i} ({temperatures[i]}°): it may be the next warmer day for a colder day further left.",
         {"stack.cur": "-1"}),
        ("return result", "Every day has its waiting time: **{_ret}**."),
    ],
    time=("O(n)", "Each day is pushed once and popped at most once."),
    space=("O(n)", "When every day is colder than the next one (temperatures rising from left to right), nothing is ever popped and the stack ends up holding every day."),
    tests=[("temperatures=[30, 40, 50, 60]", [1, 1, 1, 0]), ("temperatures=[30, 60, 90]", [1, 1, 0]),
           ("temperatures=[90, 80, 70]", [0, 0, 0])],
)

lesson(
    "car-fleet",
    pattern="Sort by position, compare arrival times",
    statement="""Cars drive along a one-lane road toward `target`. Car `i` starts at `position[i]`
    with `speed[i]`. A car cannot overtake: when it catches a slower car it slows down and they
    continue together as one **fleet**. Return how many fleets arrive at the target.""",
    args="target=12, position=[10, 8, 0, 5, 3], speed=[2, 4, 1, 1, 3]",
    expected=3,
    why="The cars at 10 and 8 arrive together, the cars at 5 and 3 merge, and the car at 0 arrives alone.",
    idea=[
        "A car can only be held up by cars **ahead** of it. So handle the cars from the one nearest the target back to the farthest.",
        "For each car compute the time it would need to reach the target *if the road were empty*: `(target − position) / speed`.",
        "If that time is not longer than the fleet in front needs, the car catches up and joins it. If it is longer, it never catches up — it leads a new fleet.",
    ],
    init={"groups": "[]"},
    views=[
        Arr("cars", title="cars as (position, speed), nearest the target first",
            ptrs={"car": "at('for pos, spd in cars')"},
            tones={"dim": "range(upto('for pos, spd in cars'))", "cur": "at('for pos, spd in cars')"}),
        Items("groups", title="fleets  (start positions of the cars in each)"),
        Vars("target", "time", "prev_time", "fleets"),
    ],
    notes=[
        ("cars = sorted(zip(position, speed), reverse=True)",
         "Pair each position with its speed and sort so the car **nearest the target comes first**. "
         "Only cars ahead can slow a car down, so we go from front to back."),
        ("prev_time = -1.0", "`prev_time` is when the fleet directly ahead arrives. There is no fleet yet."),
        ("time = (target - pos) / spd",
         "The car at position {pos} with speed {spd} has {target} − {pos} = {target - pos} to go. On an empty road "
         "that takes {target - pos} / {spd} = **{time:g}** (its travel time)."),
        ("if time > prev_time", dict(
            yes=[
                ("prev_time < 0", "It is the first car, with nothing ahead of it, so it leads the first fleet."),
                (None, "A travel time of {time:g} is **longer** than the fleet ahead needs ({prev_time:g}). It never "
                       "catches up, so it leads a **new fleet**."),
            ],
            no="A travel time of {time:g} is not longer than the fleet ahead needs ({prev_time:g}). It **catches up**, "
               "has to slow down, and arrives as part of that fleet.",
            save={"groups": "groups + [[pos]] if time > prev_time else groups[:-1] + [groups[-1] + [pos]]"},
            marks={"groups.good": "-1"})),
        ("prev_time = time",
         "That makes **{plural(fleets, 'fleet')}** so far. A car further back joins this fleet unless its travel "
         "time is longer than {time:g}."),
        ("return fleets", "**{_ret}** separate fleets reach the target."),
    ],
    time=("O(n log n)", "Sorting the cars dominates; the scan afterwards is O(n)."),
    space=("O(n)", "The sorted list of cars."),
    tests=[("target=10, position=[3], speed=[3]", 1), ("target=100, position=[0, 2, 4], speed=[4, 2, 1]", 1),
           ("target=10, position=[6, 8], speed=[3, 2]", 2)],
)

lesson(
    "largest-rectangle-in-histogram",
    pattern="Monotonic increasing stack",
    statement="""`heights[i]` is the height of a bar of width 1 in a histogram. Return the area of
    the largest rectangle that fits entirely inside the bars.""",
    args="heights=[2, 1, 5, 6, 2, 3]",
    expected=10,
    why="The bars of height 5 and 6 share a rectangle of height 5 and width 2: area 10.",
    idea=[
        "Every candidate rectangle has the full height of some bar and stretches left and right until it hits a **shorter** bar.",
        "Scan left to right with a stack of bars whose rectangle is still *open* (it has not met a shorter bar on its right yet). Their heights increase up the stack.",
        "When a shorter bar arrives, it closes every taller bar on the stack. Pop each one: its right edge is the current bar, its left edge is the bar now below it on the stack. Compute the area and keep the best.",
    ],
    init={"rect": "None"},
    views=[
        Arr("heights", bars=True, ptrs=["i"], box=("rect[0]", "rect[1]", "rect[2]"),
            tones={"seen": "stack", "cur": "i"}),
        Stack("[f'{j}:{heights[j]}' for j in stack]", id="stack", title="stack  (index:height — still open)"),
        Vars("height", "width", "max_area"),
    ],
    notes=[
        ("stack = []",
         "The stack holds bars whose rectangle is still **open**: no shorter bar has been met on their right yet. "
         "Heights always increase from the bottom of the stack to the top."),
        ("height = heights[stack.pop()]@1",
         "Bar {i} (height {heights[i]}) is **shorter** than the bar on top of the stack (height {height}). "
         "A rectangle of height {height} cannot continue past here, so pop it and measure it."),
        ("width = i if not stack else i - stack[-1] - 1", dict(
            post="It reaches left as far as {'the start' if not stack else 'index ' + str(stack[-1] + 1)} "
                 "(the bar below it on the stack is the first shorter one) and right as far as index {i - 1}: "
                 "width **{width}**.",
            save={"rect": "((stack[-1] + 1) if stack else 0, i - 1, height)"})),
        ("max_area = max(max_area, height * width)@1",
         "Area = {height} × {width} = **{height * width}**. Largest so far: **{max_area}**."),
        ("stack.append(i)", dict(
            post=[
                ("len(stack) == 1",
                 "Nothing is open below bar {i} (height {heights[i]}), so it simply opens a new rectangle. Push it."),
                (None,
                 "Bar {i} (height {heights[i]}) is at least as tall as the bar below it on the stack, so its "
                 "rectangle is open too. Push it."),
            ],
            save={"rect": "None"})),
        ("while stack:", dict(
            yes="All bars have been read. The ones still on the stack were never cut off by a shorter bar, so "
                "their rectangles run all the way to the **right edge**.",
            first=1)),
        ("width = len(heights) if not stack", dict(
            post="Pop height {height}. It reaches from {'the start' if not stack else 'index ' + str(stack[-1] + 1)} "
                 "to the right edge: width **{width}**.",
            save={"rect": "((stack[-1] + 1) if stack else 0, len(heights) - 1, height)"})),
        ("max_area = max(max_area, height * width)@2",
         "Area = {height} × {width} = **{height * width}**. Largest so far: **{max_area}**."),
        ("return max_area", "The largest rectangle has area **{_ret}**."),
    ],
    time=("O(n)", "Each bar is pushed once and popped once."),
    space=("O(n)", "The stack holds every bar when the heights keep increasing."),
    tests=[("heights=[2, 4]", 4), ("heights=[1]", 1), ("heights=[2, 1, 2]", 3), ("heights=[6, 5, 4, 3]", 12)],
)

# end of c04_stack
