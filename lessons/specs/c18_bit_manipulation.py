"""Bit Manipulation."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "number-of-1-bits",
    pattern="Read the lowest bit, then shift",
    statement="""Given a positive integer `n`, return how many `1` bits its binary representation
    contains (its *Hamming weight*).""",
    args="n=11",
    expected=3,
    why="11 in binary is 1011, which contains three 1s.",
    idea=[
        "A number is stored as bits. `n & 1` keeps only the **lowest** bit — it is 1 exactly when the last binary digit is 1.",
        "`n >> 1` shifts every bit one place to the right: the lowest bit drops off and the next one takes its place.",
        "Repeat *read the lowest bit, then shift* until nothing is left (n becomes 0), adding up the bits we read.",
    ],
    views=[
        Bits([("n", "n"), ("n & 1", "n & 1", "cur")], width=8, hi="0"),
        Vars("count"),
    ],
    notes=[
        ("count = 0", "`count` will hold the number of 1 bits. In binary, {n} is `{binary(n)}`."),
        ("count += n & 1",
         "`n & 1` reads the **lowest bit** of n, which is {n & 1}. Add it: `count` = **{count}**."),
        ("n = n >> 1",
         "Shift right by one. The bit we just counted falls off and the next bit moves into the lowest place. "
         "n is now {n} (`{binary(n)}`)."),
        ("while n", dict(no="n is 0 — there are no bits left to read.")),
        ("return count", "We counted **{count}** one-bits."),
    ],
    time=("O(log n)", "One loop per binary digit of n — at most 32 for a 32-bit integer."),
    space=("O(1)", "Only a counter is stored."),
    tests=[("n=128", 1), ("n=2147483645", 30), ("n=1", 1)],
)

lesson(
    "single-number",
    pattern="XOR cancels pairs",
    statement="""In the array `nums` every number appears **exactly twice**, except for one number
    that appears only once. Find that single number, using constant extra space.""",
    args="nums=[4, 1, 2, 1, 2]",
    expected=4,
    why="1 and 2 each appear twice; 4 appears once.",
    idea=[
        "XOR (`^`) compares two numbers bit by bit: equal bits give 0, different bits give 1.",
        "Two facts follow: `a ^ a = 0` (a number cancels itself) and `a ^ 0 = a`. And the order of XOR operations does not matter.",
        "So XOR **all** numbers together: every pair cancels to 0, and what is left is the number without a partner.",
    ],
    views=[
        Arr("nums", ptrs={"num": "i_num"}),
        Bits([("result before", "was.result"), ("num", "num", "alt"), ("result", "result", "good")], width=4,
             title="result ^ num  (a column gives 1 when its two bits differ)"),
        Vars("result"),
    ],
    notes=[
        ("result = 0", "Start with 0: XOR with 0 changes nothing (`0 ^ a = a`)."),
        ("result ^= num", [
            ("num in nums[:i_num]",
             "{was.result} ^ {num} = **{result}**  (`{binary(was.result, 4)}` ^ `{binary(num, 4)}` = `{binary(result, 4)}`). "
             "This is the **second** {num}: its bits cancel the bits the first {num} put in."),
            (None,
             "{was.result} ^ {num} = **{result}**  (`{binary(was.result, 4)}` ^ `{binary(num, 4)}` = `{binary(result, 4)}`)."),
        ]),
        ("return result", "Every pair has cancelled itself out. What remains is the single number: **{result}**."),
    ],
    time=("O(n)", "One XOR per number."),
    space=("O(1)", "One variable."),
    tests=[("nums=[2, 2, 1]", 1), ("nums=[1]", 1), ("nums=[-1, 7, -1]", 7), ("nums=[0, 3, 3]", 0)],
)

lesson(
    "counting-bits",
    pattern="DP on bits: drop the last bit",
    statement="""Given an integer `num`, return an array where entry `i` (for every `i` from 0 to
    `num`) is the **number of 1 bits** in the binary form of `i`.""",
    args="num=5",
    expected=[0, 1, 1, 2, 1, 2],
    why="0 = 0, 1 = 1, 2 = 10, 3 = 11, 4 = 100, 5 = 101 in binary.",
    idea=[
        "Counting the bits of each number separately works, but the numbers are closely related — reuse earlier answers.",
        "Dropping the last binary digit of `i` gives `i // 2`, a **smaller** number whose bit count is already known.",
        "The dropped digit is `i % 2`. So `bits(i) = bits(i // 2) + (i % 2)` — one lookup and one addition per number.",
    ],
    views=[
        Bits([("i", "i"), ("i // 2", "i // 2", "alt")], width=4, hi="0",
             title="i and i // 2  (i without its last bit)"),
        Arr("bits_count", ptrs=["i"], title="bits_count[i] = number of 1 bits in i"),
    ],
    notes=[
        ("bits_count = [0] * (num + 1)", "`bits_count[i]` will be the number of 1 bits in i. The number 0 has none, so `bits_count[0]` = 0 is already right."),
        ("bits_count[i] = bits_count[i // 2] + (i % 2)",
         "{i} is `{binary(i, 4)}`. Without its last bit it is `{binary(i // 2, 4)}` = {i // 2}, which has "
         "{plural(bits_count[i // 2], 'one-bit')} (already computed). The last bit is {i % 2}. "
         "So `bits_count[{i}]` = {bits_count[i // 2]} + {i % 2} = **{bits_count[i]}**.",
         {"bits_count.alt": "i // 2", "bits_count.good": "i"}),
        ("return bits_count", "Every number from 0 to {num} is done: **{_ret}**."),
    ],
    time=("O(n)", "One table lookup per number."),
    space=("O(1)", "Nothing besides the output array."),
    tests=[("num=2", [0, 1, 1]), ("num=0", [0]), ("num=8", [0, 1, 1, 2, 1, 2, 2, 3, 1])],
)

lesson(
    "reverse-bits",
    pattern="Take the lowest bit, append it to the result",
    statement="""Reverse the bits of a 32-bit unsigned integer `n`: the lowest bit becomes the
    highest, the second lowest the second highest, and so on.""",
    args="n=11",
    expected=3489660928,
    why="11 is 000…01011. Reversed, the bits read 11010…000, which is 3489660928.",
    idea=[
        "Build the result one bit at a time. `n & 1` reads the **lowest** bit of `n`.",
        "Shift the result **left** by one to make room, and put that bit into the free lowest place. Then shift `n` **right** so its next bit becomes the lowest.",
        "Do this exactly 32 times. The bit read first is pushed left 31 more times and ends up highest — the order is reversed.",
    ],
    views=[
        Bits([("n", "n"), ("reversed_num", "reversed_num", "good")], width=32, hi="0",
             title="32-bit view  (the lowest bit is on the right)"),
    ],
    notes=[
        ("reversed_num = 0", "`reversed_num` starts empty (all zeros). We will feed it the bits of n, lowest bit first."),
        ("reversed_num = (reversed_num << 1) | (n & 1)", dict(
            post="Round {i__ + 1}: shift the result left by one, then drop in the lowest bit of n, which is **{n & 1}**.",
            first=5)),
        ("n = n >> 1", dict(
            post="Shift n right by one: the bit just used falls off, and the next bit moves into the lowest place.",
            first=5)),
        ("for _ in range(32)", dict(
            yes="The same two moves repeat for all 32 bits. n has no 1-bits left, so from now on only zeros are appended — "
                "each round still pushes the bits already placed one position further left.",
            when="i__ == 5")),
        ("return reversed_num",
         "After 32 rounds the bit that was lowest has travelled to the highest place: the bits are reversed. "
         "As a number: **{reversed_num}**."),
    ],
    time=("O(1)", "Always exactly 32 rounds."),
    space=("O(1)", "One result variable."),
    tests=[("n=43261596", 964176192), ("n=4294967293", 3221225471), ("n=0", 0), ("n=1", 2147483648)],
)

lesson(
    "missing-number",
    pattern="XOR every index with every value",
    statement="""`nums` contains `n` **distinct** numbers taken from the range `0 … n`, so exactly one
    number of that range is missing. Return the missing number.""",
    args="nums=[3, 0, 1]",
    expected=2,
    why="The range is 0 … 3, and 2 is the only number that does not appear.",
    idea=[
        "Imagine two lists: all the numbers `0 … n`, and the values in `nums`. Every number except the missing one appears in **both** lists.",
        "XOR cancels pairs (`a ^ a = 0`). So XOR-ing both lists together cancels everything that is present, and only the missing number survives.",
        "The loop supplies the indexes `0 … n − 1` and the values; the remaining number `n` is put in as the starting value.",
    ],
    views=[
        Arr("nums", ptrs=["i"]),
        Bits([("missing_num", "missing_num", "good"), ("i", "i"), ("nums[i]", "nums[i]", "alt")], width=4),
        Vars("missing_num"),
    ],
    notes=[
        ("missing_num = n",
         "The full range is 0 … {n}. The loop will XOR in the indexes 0 … {n - 1}, so start with the one number it never "
         "visits: `missing_num` = **{n}**."),
        ("missing_num ^= i ^ nums[i]", [
            ("i == 0",
             "XOR in the index {i} and the value {nums[i]}: {was.missing_num} ^ {i} ^ {nums[i]} = **{missing_num}**. "
             "Any number that has been put in **twice** (once from the range, once as a value) has cancelled out."),
            (None, "XOR in the index {i} and the value {nums[i]}: {was.missing_num} ^ {i} ^ {nums[i]} = **{missing_num}**."),
        ]),
        ("return missing_num",
         "All indexes 0 … {n} and all values have been XOR-ed together. Every number present cancelled itself; "
         "what is left is the missing one: **{missing_num}**."),
    ],
    time=("O(n)", "One pass over the array, with two XOR operations per index."),
    space=("O(1)", "One variable."),
    tests=[("nums=[0, 1]", 2), ("nums=[9, 6, 4, 2, 3, 5, 7, 0, 1]", 8), ("nums=[0]", 1), ("nums=[1]", 0)],
)

lesson(
    "sum-of-two-integers",
    pattern="Add with XOR, carry with AND",
    statement="""Return the sum of two integers `a` and `b` **without using `+` or `−`**.""",
    args="a=5, b=3",
    expected=8,
    why="5 + 3 = 8, obtained with XOR, AND and shifts only.",
    idea=[
        "Look at one binary column: `0 + 0 = 0`, `0 + 1 = 1`, `1 + 1 = 0 carry 1`. Ignoring the carry, that is exactly **XOR**. So `a ^ b` adds every column without carries.",
        "A carry arises precisely where **both** bits are 1 — that is `a & b`. A carry belongs one column to the left, so shift it: `(a & b) << 1`.",
        "The true sum is *(sum without carries) + (carries)* — another addition. Repeat with those two numbers until there are no carries left. (The mask keeps the numbers within 32 bits, because Python integers never overflow.)",
    ],
    views=[
        Bits([("a", "a"), ("b", "b", "alt"), ("a ^ b", "(a ^ b) & 0xFFFFFFFF", "good"),
              ("(a & b) << 1", "((a & b) << 1) & 0xFFFFFFFF", "mark")], width=8,
             title="a ^ b = sum without carries      (a & b) << 1 = the carries"),
    ],
    notes=[
        ("MAX_INT = 0x7FFFFFFF",
         "`a ^ b` adds each column while ignoring carries; `(a & b) << 1` collects the carries, moved one column left. "
         "The two masks only serve to imitate 32-bit integers."),
        ("a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK", [
            ("b == 0",
             "Sum without carries: {was.a} ^ {was.b} = **{a}**. Carries: ({was.a} & {was.b}) << 1 = **0** — "
             "no column produced a carry this time."),
            (None,
             "Sum without carries: {was.a} ^ {was.b} = **{a}**. Carries: ({was.a} & {was.b}) << 1 = **{b}**. "
             "The true total is {a} + {b}, which is again an addition — so repeat with these two numbers."),
        ]),
        ("while b != 0", dict(no="There are **no carries left** (b = 0), so `a` now holds the complete sum.")),
        ("return a if a <= MAX_INT else ~(a ^ MASK)", [
            ("a <= MAX_INT", "`a` = {a} fits into a signed 32-bit integer as it is → **{_ret}**."),
            (None, "The top (sign) bit of `a` is set, so in 32-bit arithmetic it is a negative number. Convert it back to Python's representation → **{_ret}**."),
        ]),
    ],
    time=("O(1)", "At most 32 rounds, because every round moves the carries one bit to the left."),
    space=("O(1)", "Only the two numbers a and b are stored."),
    tests=[("a=1, b=2", 3), ("a=2, b=3", 5), ("a=-2, b=3", 1), ("a=-1, b=-1", -2), ("a=0, b=0", 0), ("a=-5, b=5", 0),
           ("a=1000, b=-1000", 0)],
)

lesson(
    "reverse-integer",
    pattern="Pop the last digit, push it onto the result",
    statement="""Given a signed 32-bit integer `x`, return `x` with its digits reversed. If the
    reversed value does not fit into a signed 32-bit integer, return `0`.""",
    args="x=-123",
    expected=-321,
    why="The digits 1, 2, 3 are reversed to 3, 2, 1; the sign stays.",
    idea=[
        "`x % 10` is the last digit of `x`, and `x // 10` removes it. That is a **pop** from the end of the number.",
        "`reversed_num * 10 + digit` appends a digit to the end of the result — a **push**. Popping from one number and pushing onto the other reverses the order.",
        "Before each push, check that it will not exceed the 32-bit limit; if it would, the answer is 0. The sign is put aside at the start and restored at the end.",
    ],
    views=[
        Arr("list(str(x))", id="x", idx=False, title="x  (digits still to be moved)"),
        Arr("list(str(reversed_num))", id="rev", idx=False, title="reversed_num",
            tones={"good": "len(str(reversed_num)) - 1"}),
        Vars("pop", "sign"),
    ],
    notes=[
        ("x = abs(x)", "Remember the sign (`sign` = {sign}) and continue with the absolute value {x}."),
        ("x //= 10", "**Pop** the last digit: `x % 10` = {pop}. What remains: x = {x}."),
        ("if reversed_num > (INT_MAX - pop) // 10", dict(
            yes="Appending {pop} to {reversed_num} would go beyond the 32-bit limit ({INT_MAX}) → return 0.")),
        ("reversed_num = reversed_num * 10 + pop",
         "**Push** it onto the result: {was.reversed_num} × 10 + {pop} = **{reversed_num}**."),
        ("return reversed_num * sign", "All digits have been moved. Restore the sign: {reversed_num} × {sign} = **{_ret}**."),
    ],
    allow_unused=True,
    time=("O(log x)", "One round per digit of x."),
    space=("O(1)", "A few numbers."),
    tests=[("x=123", 321), ("x=120", 21), ("x=0", 0), ("x=1534236469", 0), ("x=-2147483648", 0), ("x=1463847412", 2147483641)],
)

# end of c18_bit_manipulation
