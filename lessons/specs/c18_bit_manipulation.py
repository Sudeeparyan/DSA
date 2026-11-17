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
    picture="""Picture the number written in binary as a row of light switches, each on (1) or off (0): 11 is
    `1011`. To count the switches that are on, look only at the last one and note whether it is on.
    Then slide the whole row one place to the right, so the last switch drops off and the next one
    takes its place. Repeat until every switch has dropped off.""",
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
    say={
        "def hammingWeight": (
            "The function we must write. It gets a number `n` and returns how many 1s its binary "
            "form has."
        ),
        "count = 0": "The 1s counted so far.",
        "while n": "Keep going while `n` is not 0, that is while some 1 is left.",
        "count += n & 1": "`n & 1` is the last binary digit of `n`, 0 or 1. Add it to the count.",
        "n = n >> 1": (
            "`>> 1` shifts every binary digit one place right, so the last one drops off. (For "
            "whole numbers this is the same as halving and rounding down.)"
        ),
        "return count": "Return the count.",
    },
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
    picture="""Picture a row of light switches, all off. Each number says which switches to flip: the ones
    where its binary form has a 1. Flipping a switch twice puts it back, so a number that comes
    twice undoes itself. Once every number has had its turn, the switches show exactly the number
    that came only once. Flipping like this is what XOR (`^`) does.""",
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
    say={
        "def singleNumber": (
            "The function we must write. It gets the list `nums` and returns the number that "
            "appears only once."
        ),
        "result = 0": "Start at 0: all switches off.",
        "for num in nums": "Go through the numbers one at a time.",
        "result ^= num": (
            "XOR it in: `^` flips the bits of `result` wherever `num` has a 1. A number seen "
            "twice flips the same bits back."
        ),
        "return result": "Every pair has cancelled out. What is left is the single number.",
    },
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
    picture="""Picture the numbers written in binary. Dropping the last digit of a number is the same as
    halving it and rounding down: 5 is `101`, and without its last digit it is `10`, which is 2. So
    the 1s in 5 are the 1s in 2, which we already counted, plus 1 if the dropped digit was a 1.
    Filling the table from small to large, every answer is one look-up and one addition.""",
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
    key={"alt": "i // 2: i without its last bit", "good": "box just filled in"},
    say={
        "def countBits": (
            "The function we must write. It gets `num` and returns, for every number from 0 to "
            "`num`, how many 1s its binary form has."
        ),
        "bits_count = [0] * (num + 1)": (
            "A table with one box per number from 0 to `num`, all 0. 0 has no 1s, so its box is "
            "already right."
        ),
        "for i in range(1, num + 1)": "Fill the boxes from 1 up to `num`, small numbers first.",
        "bits_count[i] = bits_count[i // 2] + (i % 2)": (
            "`i // 2` is `i` with its last binary digit dropped: a smaller number, already in the"
            " table. `i % 2` is the dropped digit. Together they give the count for `i`."
        ),
        "return bits_count": "Return the filled table.",
    },
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
    picture="""Picture a string of 32 beads, each black (1) or white (0). Take beads off its right end one at a
    time and thread each onto the right end of a second string, first pushing the beads already
    there one place to the left. The bead taken first gets pushed left 31 times and ends up at the
    far left. After all 32 beads, the second string holds them in reverse order.""",
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
    say={
        "def reverseBits": (
            "The function we must write. It gets a 32-bit number `n` and returns it with its bits"
            " in reverse order."
        ),
        "reversed_num = 0": "The answer, built one bit at a time. It starts as all zeros.",
        "for _ in range(32)": (
            "Repeat 32 times, once per bit. `_` is the name for a counter we never use."
        ),
        "reversed_num = (reversed_num << 1) | (n & 1)": (
            "`<< 1` shifts the answer left, making room at its right end. `n & 1` is the last bit"
            " of `n`, and `|` drops it into that free place."
        ),
        "n = n >> 1": (
            "Shift `n` right: the bit just used drops off and the next one becomes the last."
        ),
        "return reversed_num": "The bits are now in reverse order: return the number.",
    },
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
    picture="""Picture two piles of cards: one with every number from 0 to `n`, and one with the numbers in the
    list. Every number except the missing one is in both piles. Pair up equal cards and throw each
    pair away: the one card left is the missing number. XOR (`^`) does exactly this pairing, because
    a number XOR-ed with itself cancels to 0.""",
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
    say={
        "def missingNumber": (
            "The function we must write. It gets the list `nums` and returns the number from 0 to"
            " `n` that is missing."
        ),
        "n = len(nums)": "How many numbers the list holds. The full range is 0 to `n`.",
        "missing_num = n": (
            "Start with `n`. The loop below supplies 0 to `n - 1`, so `n` is put in here."
        ),
        "for i in range(n)": "Go through the positions 0 to `n - 1`.",
        "missing_num ^= i ^ nums[i]": (
            "XOR in the position `i` (a card from the full range) and the value `nums[i]` (a card"
            " from the list). A number put in twice cancels out."
        ),
        "return missing_num": "Everything present has cancelled out; the missing number is left.",
    },
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
    picture="""Picture adding two binary numbers on paper in two separate passes. Pass one writes each column's
    digit but ignores carries: 0 + 1 is 1, and 1 + 1 is 0. That is XOR. Pass two writes only the
    carries, each moved one column left; a carry appears where both digits are 1. That is AND, then
    a shift. The answer is these two numbers added together, which is another addition, so repeat
    until no carries are left.""",
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
    key={"good": "sum without carries (a ^ b)", "mark": "the carries ((a & b) << 1)"},
    say={
        "def getSum": (
            "The function we must write. It gets two numbers `a` and `b` and returns their sum, "
            "without using `+` or `-`."
        ),
        "MASK = 0xFFFFFFFF": (
            "A number made of 32 ones in binary (`0x` means it is written in hexadecimal). `& "
            "MASK` keeps only the lowest 32 bits, the way a 32-bit number would."
        ),
        "MAX_INT = 0x7FFFFFFF": "The largest positive 32-bit number: a 0 followed by 31 ones.",
        "while b != 0": "Keep going while there are carries left to add.",
        "a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK": (
            "Both at once: `a` becomes the sum without carries (`a ^ b`), and `b` the carries (`a"
            " & b`, where both bits are 1) moved one column left (`<< 1`)."
        ),
        "return a if a <= MAX_INT else ~(a ^ MASK)": (
            "If `a` fits as a positive number, return it. Otherwise its top bit marks it as "
            "negative in 32-bit form, and `~(a ^ MASK)` turns it into the same negative number in"
            " Python."
        ),
    },
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
    picture="""Picture taking the last digit off the end of the number and writing it at the end of a new
    number, again and again: from 123 you write 3, then 32, then 321. The sign is set aside at the
    start and put back at the end. Before writing each digit, check that the new number will not
    grow too big for 32 bits; if it would, the answer is 0.""",
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
    key={"good": "digit just written"},
    say={
        "def reverse": (
            "The function we must write. It gets a whole number `x` and returns it with its "
            "digits reversed, or 0 if that is too big."
        ),
        "INT_MAX = 2**31 - 1": (
            'The largest number that fits in 32 bits: 2,147,483,647. `**` means "to the power".'
        ),
        "INT_MIN = -(2**31)": "The smallest one: -2,147,483,648.",
        "reversed_num = 0": "The reversed number, built one digit at a time.",
        "sign = 1 if x > 0 else -1": "Remember the sign: 1 if `x` is positive, otherwise -1.",
        "x = abs(x)": "Carry on with the number without its sign.",
        "while x != 0": "While digits are left:",
        "pop = x % 10": "`x % 10` is the last digit of `x`: the remainder after dividing by 10.",
        "x //= 10": "Remove that digit. `//= 10` divides by 10 and drops the remainder.",
        "if reversed_num > (INT_MAX - pop) // 10": (
            "Would writing this digit at the end make the number bigger than `INT_MAX`?"
        ),
        "return 0": "Then the reversed number does not fit, and the rules say to return 0.",
        "reversed_num = reversed_num * 10 + pop": (
            "Write the digit at the end of the new number: times 10 makes room, then add the "
            "digit."
        ),
        "return reversed_num * sign": "Put the sign back and return the result.",
    },
    time=("O(log x)", "One round per digit of x."),
    space=("O(1)", "A few numbers."),
    tests=[("x=123", 321), ("x=120", 21), ("x=0", 0), ("x=1534236469", 0), ("x=-2147483648", 0), ("x=1463847412", 2147483641)],
)

# end of c18_bit_manipulation
