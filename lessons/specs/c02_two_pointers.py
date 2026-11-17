"""Two Pointers."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "container-with-most-water",
    pattern="Two pointers moving inward",
    statement="""`height[i]` is the height of a vertical wall at position `i`. Pick two walls;
    together with the floor they form a container. Return the largest amount of water any pair
    of walls can hold. Water can only rise to the **shorter** of the two walls.""",
    args="height=[1, 8, 6, 2, 5, 4, 8, 3, 7]",
    expected=49,
    why="Walls at index 1 (height 8) and index 8 (height 7): min(8, 7) × (8 − 1) = 49.",
    picture="""Picture a row of fence posts of different heights. Pick any two, and water can fill the space
    between them, but only as high as the **shorter** post. Start with the two posts that are
    farthest apart. Then, again and again, give up the shorter post and step inward from that side.
    Giving up the taller post could never help: the container would get narrower and would still be
    held down by the same short post.""",
    idea=[
        "Water held = **width × shorter wall**. Trying every pair of walls is O(n²).",
        "Start with the widest container (both ends). Any other container is narrower, so it can only win by having a taller *shorter wall*.",
        "Therefore always move the pointer at the **shorter** wall inward. Moving the taller one cannot help: the width shrinks and the height is still capped by the shorter wall.",
    ],
    views=[
        Arr("height", bars=True, ptrs=["left", "right"],
            pool=("left", "right", "min(height[left], height[right])"),
            tones={"cur": "[left, right]"}),
        Vars("current_area", "max_area"),
    ],
    notes=[
        ("left, right = 0, len(height) - 1",
         "Put one pointer on each end. This is the **widest** possible container."),
        ("max_area = max(max_area, current_area)",
         "The walls of height {height[left]} and {height[right]} are {right - left} apart. Water rises to the shorter one: "
         "min({height[left]}, {height[right]}) × {right - left} = **{current_area}**. Best so far: **{max_area}**."),
        ("left += 1",
         "The left wall ({height[left - 1]}) is the shorter one. Every narrower container that keeps it "
         "is still capped at {height[left - 1]}, so it can never beat what we have. Move `left` inward."),
        ("right -= 1",
         "The right wall ({height[right + 1]}) is the shorter one"
         "{' (or as short as the left one)' if height[right + 1] == height[left] else ''}. Every narrower "
         "container that keeps it is still capped at {height[right + 1]}, so it can never beat what we have. "
         "Move `right` inward."),
        ("while left < right", dict(
            no="The pointers have met — every pair that could have won has been checked.")),
        ("return max_area", "The largest area we saw is **{max_area}**."),
    ],
    say={
        "def maxArea": (
            "The function we must write. It gets the wall heights `height` and returns the most "
            "water any two walls can hold."
        ),
        "left, right = 0, len(height) - 1": (
            "Put `left` on the first wall and `right` on the last one. (`len(height) - 1` is the "
            "last position, because counting starts at 0.)"
        ),
        "max_area = 0": "The most water found so far. None yet.",
        "while left < right": "Repeat while the two pointers have not met.",
        "current_area = min(height[left], height[right]) * (right - left)": (
            "The water between these two walls: the shorter wall's height (`min` picks the "
            "smaller) times the distance between them."
        ),
        "max_area = max(max_area, current_area)": (
            "Keep whichever is bigger: the best so far or this container."
        ),
        "if height[left] < height[right]": (
            "Which wall is shorter? That wall is the one that limits the water."
        ),
        "left += 1": "The left wall is shorter: move `left` one step inward (`+= 1` adds one).",
        "right -= 1": (
            "Otherwise the right wall is shorter (or the two are equal): move `right` one step "
            "inward (`-= 1` takes one away)."
        ),
        "return max_area": "Return the most water found.",
    },
    time=("O(n)", "Each step moves one pointer inward, so the two pointers take n − 1 steps in total."),
    space=("O(1)", "Only two pointers and two numbers are stored."),
    tests=[("height=[1, 1]", 1), ("height=[4, 3, 2, 1, 4]", 16), ("height=[1, 2, 1]", 2)],
)

lesson(
    "valid-palindrome",
    pattern="Two pointers from both ends",
    statement="""A phrase is a **palindrome** if, after ignoring everything that is not a letter or
    digit and ignoring upper/lower case, it reads the same forwards and backwards. Given a string
    `s`, return `True` if it is a palindrome.""",
    args="s='A Toyota!'",
    expected=True,
    why='Keeping only letters and lowering them gives "atoyota", which reads the same both ways.',
    picture="""Picture two people reading the same sign: one starts at the front, the other at the back, and
    they walk toward each other. At each step both call out a letter, skipping spaces and
    punctuation. If the two letters ever differ, the sign is not a palindrome. If they meet in the
    middle without a difference, it is.""",
    idea=[
        "A palindrome's first character equals its last, its second equals its second-to-last, and so on.",
        "So put one pointer at each end and compare the two characters, moving both inward after every match.",
        "Spaces and punctuation do not count: whenever a pointer lands on one, just step over it. Compare letters in lower case.",
    ],
    views=[
        Arr("s", ptrs=["left", "right"],
            tones={"dim": "list(range(left)) + list(range(right + 1, len(s)))", "cur": "[left, right]"}),
    ],
    notes=[
        ("left, right = 0, len(s) - 1",
         "Put `left` on the first character and `right` on the last. We compare them pair by pair, moving inward."),
        ("left += 1@1",
         "`{show(s[left - 1])}` is not a letter or digit, so it does not count. Step `left` over it."),
        ("right -= 1@1",
         "`{show(s[right + 1])}` is not a letter or digit, so it does not count. Step `right` over it."),
        ("if s[left].lower() != s[right].lower()", dict(
            no="Compare `{s[left]}` with `{s[right]}`, ignoring case: `{s[left].lower()}` equals "
               "`{s[right].lower()}` — this pair **matches**.",
            no_marks={"s.good": "[left, right]"})),
        ("right -= 1@2", "The pair matched, so move both pointers one step inward."),
        ("while left < right:", dict(
            no="The pointers have met in the middle. Every pair matched.")),
        ("return True", "No mismatch was found, so the phrase is a palindrome → **True**."),
    ],
    say={
        "def isPalindrome": (
            "The function we must write. It gets the text `s` and answers `True` or `False`."
        ),
        "left, right = 0, len(s) - 1": (
            "Put `left` on the first character and `right` on the last one."
        ),
        "while left < right:": "Repeat while the two pointers have not met in the middle.",
        "while left < right and not s[left].isalnum()": (
            "Is `left` on something that is not a letter or a digit? (`.isalnum()` is `True` only"
            " for letters and digits.)"
        ),
        "left += 1@1": "Then step `left` over it, one character to the right.",
        "while left < right and not s[right].isalnum()": (
            "Is `right` on something that is not a letter or a digit?"
        ),
        "right -= 1@1": "Then step `right` over it, one character to the left.",
        "if s[left].lower() != s[right].lower()": (
            "Compare the two characters in lower case, so that `A` and `a` count as the same. Are"
            " they different (`!=`)?"
        ),
        "return False": (
            "They differ, so the text does not read the same both ways: answer `False`."
        ),
        "left += 1@2": "The pair matched: move `left` one step inward.",
        "right -= 1@2": "Move `right` one step inward too, ready to compare the next pair.",
        "return True": "The pointers met without finding a mismatch: answer `True`.",
    },
    time=("O(n)", "Each pointer only moves inward, so every character is looked at once."),
    space=("O(1)", "Just two pointers — no cleaned-up copy of the string is built."),
    tests=[("s='race a car'", False), ("s=' '", True), ("s='0P'", False),
           ("s='A man, a plan, a canal: Panama'", True)],
)

lesson(
    "two-sum-ii-input-array-is-sorted",
    pattern="Two pointers on a sorted array",
    statement="""`numbers` is sorted in increasing order. Find the two numbers that add up to
    `target` and return their positions, counting from **1**. Exactly one answer exists, and
    only constant extra space may be used.""",
    args="numbers=[1, 3, 4, 6, 8, 11], target=10",
    expected=[3, 4],
    why="The 3rd and 4th numbers are 4 and 6, and 4 + 6 = 10.",
    picture="""Picture the numbers lined up from smallest to largest, with one finger on each end. Add the two
    numbers under your fingers. Too small? Move the left finger right, to a bigger number. Too big?
    Move the right finger left, to a smaller one. Because the line is sorted, every move steers the
    sum toward the target, and the fingers never skip past the answer.""",
    idea=[
        "Because the array is sorted, the sum of two numbers can be steered: a number further right is bigger, one further left is smaller.",
        "Start with the smallest and the largest number. If their sum is too small, the smallest one is useless with *every* partner — move `left` right. If it is too big, the largest is useless — move `right` left.",
        "Each step throws one number away for good, so the pointers meet the answer in a single pass, with no extra memory.",
    ],
    views=[
        Arr("numbers", ptrs=["left", "right"],
            tones={"dim": "list(range(left)) + list(range(right + 1, len(numbers)))", "cur": "[left, right]"}),
        Vars("target", "current_sum"),
    ],
    notes=[
        ("left, right = 0, len(numbers) - 1",
         "The array is sorted, so start with the **smallest** number (`left`) and the **largest** (`right`)."),
        ("current_sum = numbers[left] + numbers[right]",
         "{numbers[left]} + {numbers[right]} = **{current_sum}**. The target is {target}."),
        ("return [left + 1, right + 1]",
         "{current_sum} is exactly the target. Positions are counted from 1, so return **{_ret}**.",
         {"numbers.good": "[left, right]"}),
        ("left += 1",
         "{current_sum} is too **small**. {numbers[left - 1]} is already paired with the largest number left, "
         "so it can never reach the target. Move `left` to a bigger number."),
        ("right -= 1",
         "{current_sum} is too **big**. {numbers[right + 1]} is already paired with the smallest number left, "
         "so it can never work. Move `right` to a smaller number."),
    ],
    say={
        "def twoSum": (
            "The function we must write. It gets the sorted list `numbers` and the `target`, and "
            "returns two positions counted from 1."
        ),
        "left, right = 0, len(numbers) - 1": (
            "Put `left` on the smallest number (the first) and `right` on the largest (the last)."
        ),
        "while left < right": "Repeat while the two pointers have not met.",
        "current_sum = numbers[left] + numbers[right]": (
            "Add the two numbers the pointers are on."
        ),
        "if current_sum == target": (
            "Is the sum exactly the target? (`==` asks *is it equal?*; a single `=` would store a"
            " value instead.)"
        ),
        "return [left + 1, right + 1]": (
            "Yes: return the two positions. The problem counts from 1, so add 1 to each."
        ),
        "elif current_sum < target": "Otherwise, is the sum too small? (`elif` means *else if*.)",
        "left += 1": "Too small: move `left` right, to a bigger number.",
        "right -= 1": "Too big: move `right` left, to a smaller number.",
        "return [-1, -1]": (
            "Reached only if no pair works. The problem promises that one always does."
        ),
    },
    time=("O(n)", "Every step moves one pointer inward, so there are at most n steps."),
    space=("O(1)", "Only the two pointers are stored."),
    tests=[("numbers=[2, 7, 11, 15], target=9", [1, 2]), ("numbers=[2, 3, 4], target=6", [1, 3]),
           ("numbers=[-1, 0], target=-1", [1, 2])],
)

lesson(
    "3sum",
    pattern="Sort, fix one number, two pointers for the rest",
    statement="""Given an integer array `nums`, return every triplet of three **different
    positions** whose values add up to 0. The answer must not contain the same triplet twice.""",
    args="nums=[-1, 0, 1, 2, -1, -4]",
    expected=[[-1, -1, 2], [-1, 0, 1]],
    why="(-1) + (-1) + 2 = 0 and (-1) + 0 + 1 = 0. No other distinct triplet sums to 0.",
    unordered=2,
    picture="""Picture picking teams of three whose scores add up to exactly zero. First line everyone up by
    score. Then let each person in turn be the team's first member, and find the other two among the
    people to their right, with one finger at each end of that part of the line: move the left
    finger to raise the total, the right finger to lower it. Because equal scores now stand side by
    side, it is easy to avoid picking the same team twice.""",
    idea=[
        "Trying all triples is O(n³). Fix **one** number instead; what remains is *find two numbers that sum to its negative* — the Two Sum II problem.",
        "Sort the array once. Then for each first number, run two pointers over the part to its right, steering the sum toward 0.",
        "Sorting also puts equal values side by side, so duplicates are easy to skip: never start from the same first value twice.",
    ],
    views=[
        Arr("nums", ptrs=["i", "left", "right"],
            tones={"dim": "range(i)", "alt": "i", "cur": "[left, right]"}),
        Items("result", title="result  (triplets found)"),
        Vars("current_sum"),
    ],
    notes=[
        ("nums.sort()",
         "Sort first. In sorted order two pointers can steer a sum up or down, and equal numbers sit next to "
         "each other so duplicates are easy to skip."),
        ("if i > 0 and nums[i] == nums[i - 1]", dict(
            yes="`nums[{i}]` = {nums[i]} is the same as the previous first number. It could only rebuild the same "
                "triplets, so skip it.")),
        ("left, right = i + 1, n - 1",
         "Fix the first number: `nums[{i}]` = **{nums[i]}**. Now look to its right for two numbers that add up to "
         "{-nums[i]}, with one pointer at each end."),
        ("current_sum = nums[i] + nums[left] + nums[right]",
         "{nums[i]} + {nums[left]} + {nums[right]} = **{current_sum}**."),
        ("result.append([nums[i], nums[left], nums[right]])",
         "The sum is 0 — a triplet. Save [{nums[i]}, {nums[left]}, {nums[right]}].",
         {"nums.good": "[i, left, right]", "result.good": "-1"}),
        ("right -= 1@2",
         "Move **both** pointers inward to look for another pair that works with {nums[i]}."),
        ("left += 1@3",
         "{current_sum} is below 0, so the sum has to grow. Move `left` to a bigger number."),
        ("right -= 1@3",
         "{current_sum} is above 0, so the sum has to shrink. Move `right` to a smaller number."),
        ("while left < right:", dict(
            no="`left` and `right` have met: there are no more pairs for the first number {nums[i]}.")),
        ("return result", "Every possible first number has been tried. Return the triplets: **{_ret}**."),
    ],
    say={
        "def threeSum": (
            "The function we must write. It gets the list `nums` and returns every group of three"
            " numbers that adds up to 0."
        ),
        "nums.sort()": "Sort the numbers from smallest to largest.",
        "result = []": "An empty list for the triplets we find.",
        "n = len(nums)": "`n` is how many numbers there are.",
        "for i in range(n - 2)": (
            "Let each position `i` in turn hold the first number of a triplet. (`range(n - 2)` "
            "stops early, because two more numbers are needed to its right.)"
        ),
        "if i > 0 and nums[i] == nums[i - 1]": (
            "Is this first number the same as the one just before it? It would only find the same"
            " triplets again."
        ),
        "continue": "So skip it: `continue` jumps straight to the next `i`.",
        "left, right = i + 1, n - 1": (
            "Put `left` just after `i`, and `right` on the last number."
        ),
        "while left < right:": "Repeat while those two pointers have not met.",
        "current_sum = nums[i] + nums[left] + nums[right]": "Add up the three numbers.",
        "if current_sum == 0": "Is the total exactly 0?",
        "result.append([nums[i], nums[left], nums[right]])": (
            "Yes: add this triplet to the end of `result`."
        ),
        "while left < right and nums[left] == nums[left + 1]": (
            "Is the next number on the left a copy of this one? Using it would rebuild the same "
            "triplet."
        ),
        "left += 1@1": "So step `left` past the copy.",
        "while left < right and nums[right] == nums[right - 1]": (
            "Is the next number on the right a copy of this one?"
        ),
        "right -= 1@1": "So step `right` past the copy.",
        "left += 1@2": "Now move `left` inward, onto a new number.",
        "right -= 1@2": "And move `right` inward too, to look for another pair.",
        "elif current_sum < 0": "Otherwise, is the total below 0?",
        "left += 1@3": "Too small: move `left` right, to a bigger number.",
        "right -= 1@3": "Too big (above 0): move `right` left, to a smaller number.",
        "return result": "Return every triplet found.",
    },
    time=("O(n²)", "Sorting is O(n log n); then each of the n first numbers gets one O(n) two-pointer sweep."),
    space=("O(1)", "Apart from the output (and the sort), only a few pointers are used."),
    tests=[("nums=[0, 1, 1]", []), ("nums=[0, 0, 0]", [[0, 0, 0]]), ("nums=[-2, 0, 0, 2, 2]", [[-2, 0, 2]])],
)

lesson(
    "trapping-rain-water",
    pattern="Two pointers with running maximums",
    statement="""`height[i]` is the height of a bar of width 1. After it rains, water is trapped
    in the dips between bars. Return the total amount of trapped water.""",
    args="height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]",
    expected=6,
    why="1 unit sits at index 2, then 1 + 2 + 1 units at indexes 4–6, and 1 unit at index 9.",
    picture="""Picture rain falling on a row of bars. The water over a bar can only rise to the lower of two
    walls: the tallest bar somewhere on its left and the tallest somewhere on its right. Any higher
    and it would spill. Two people walk inward from the two ends, each remembering the tallest bar
    behind them. The one standing on the lower bar moves next: the other side is known to have a bar
    at least that tall, so the water here depends only on the tallest bar behind them.""",
    idea=[
        "Water above a bar rises to the **lower** of the tallest wall on its left and the tallest wall on its right. Anything higher would spill over that lower wall.",
        "Use a pointer at each end and remember the tallest wall seen so far from each side (`max_left`, `max_right`).",
        "Always process the side whose bar is **lower**. The other side is known to have a wall at least that tall, so the water on this bar depends only on its own side's maximum: `max − height`.",
    ],
    init={"water": "[0] * len(height)"},
    views=[
        Arr("height", bars=True, ptrs=["left", "right"], water="water", tones={"cur": "[left, right]"}),
        Vars("max_left", "max_right", "trapped_water"),
    ],
    notes=[
        ("left, right = 0, len(height) - 1", "Start with a pointer on the first bar and one on the last bar."),
        ("max_left, max_right = 0, 0",
         "`max_left` and `max_right` remember the tallest wall seen so far from each side. Water can only "
         "be held below those walls."),
        ("max_left = height[left]",
         "The left bar ({height[left]}) is the lower side, so it is the one we can decide now. It is at least "
         "as tall as every wall seen from the left, so nothing can sit on top of it. It becomes `max_left` = {max_left}."),
        ("trapped_water += max_left - height[left]", dict(
            post="The left bar ({height[left]}) is below `max_left` ({max_left}), and the right side has a wall at "
                 "least as tall. Water fills the gap: {max_left} − {height[left]} = **{max_left - height[left]}**. "
                 "Total so far: **{trapped_water}**.",
            save={"water": "water[:left] + [max_left - height[left]] + water[left + 1:]"})),
        ("max_right = height[right]",
         "The right bar ({height[right]}) is the lower side this time. It is at least as tall as every wall seen "
         "from the right, so it holds no water and becomes `max_right` = {max_right}."),
        ("trapped_water += max_right - height[right]", dict(
            post="The right bar ({height[right]}) is below `max_right` ({max_right}), and the left side has a taller "
                 "wall. Water fills the gap: {max_right} − {height[right]} = **{max_right - height[right]}**. "
                 "Total so far: **{trapped_water}**.",
            save={"water": "water[:right] + [max_right - height[right]] + water[right + 1:]"})),
        ("while left < right", dict(no="The pointers have met — every bar has been handled.")),
        ("return trapped_water", "Adding up the water above every bar gives **{_ret}** units."),
    ],
    say={
        "def trap": (
            "The function we must write. It gets the bar heights `height` and returns how much "
            "water is trapped."
        ),
        "left, right = 0, len(height) - 1": (
            "Put `left` on the first bar and `right` on the last one."
        ),
        "max_left, max_right = 0, 0": (
            "The tallest bar seen so far from each side. Nothing seen yet, so both start at 0."
        ),
        "trapped_water = 0": "The total amount of water found so far.",
        "while left < right": "Repeat while the two pointers have not met.",
        "if height[left] <= height[right]": (
            "Is the left bar the lower one (or are they equal)? Then the left side is the one we "
            "can settle now."
        ),
        "if height[left] >= max_left": (
            "Is this bar at least as tall as everything seen from the left?"
        ),
        "max_left = height[left]": (
            "Yes: it becomes the tallest left wall. No water can sit on top of it."
        ),
        "trapped_water += max_left - height[left]": (
            "No: water fills it up to the tallest left wall. Add that depth, `max_left − "
            "height[left]`, to the total."
        ),
        "left += 1": "This bar is done: move `left` one step right.",
        "if height[right] >= max_right": (
            "Otherwise the right bar is the lower one. Is it at least as tall as everything seen "
            "from the right?"
        ),
        "max_right = height[right]": "Yes: it becomes the tallest right wall.",
        "trapped_water += max_right - height[right]": (
            "No: water fills it up to the tallest right wall. Add `max_right − height[right]` to "
            "the total."
        ),
        "right -= 1": "This bar is done: move `right` one step left.",
        "return trapped_water": "Return the total amount of water.",
    },
    time=("O(n)", "Each step moves one pointer inward; every bar is handled once."),
    space=("O(1)", "Two pointers, two maximums and a running total."),
    tests=[("height=[4, 2, 0, 3, 2, 5]", 9), ("height=[1, 2, 3]", 0), ("height=[3, 0, 3]", 3)],
)

# end of c02_two_pointers
