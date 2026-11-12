"""Greedy."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "maximum-subarray",
    pattern="Kadane's algorithm: extend or restart",
    statement="""Given an integer array `nums`, find the contiguous subarray (at least one number)
    with the **largest sum** and return that sum.""",
    args="nums=[-2, 1, -3, 4, -1, 2, 1, -5, 4]",
    expected=6,
    why="The subarray [4, -1, 2, 1] sums to 6.",
    idea=[
        "Walk through the array and keep `current_sum` = the best sum of a subarray that **ends at the current number**.",
        "That best subarray either **extends** the previous one (`current_sum + num`) or **starts fresh** at this number (`num`). Starting fresh wins exactly when the sum carried so far is negative — a negative prefix only drags the total down.",
        "The answer is the largest `current_sum` seen at any position.",
    ],
    init={"cs": "0", "best": "[]"},
    views=[
        Arr("nums", ptrs={"num": "i_num"}, rng=("cs", "i_num", "current_sum", "win"), tones={"good": "best"},
            title="nums  (green = best subarray found so far)"),
        Vars("current_sum", "max_sum"),
    ],
    notes=[
        ("current_sum = 0",
         "`current_sum` is the best sum of a subarray ending at the current number; `max_sum` is the best sum seen anywhere "
         "(−∞ so that the first number always beats it)."),
        ("current_sum = max(num, current_sum + num)", dict(
            post=[
                ("i_num == 0", "First number: the subarray is just [{num}], so `current_sum` = **{current_sum}**."),
                ("was.current_sum < 0",
                 "The sum carried so far is {was.current_sum} — **negative**, so it would only make {num} smaller. "
                 "Drop it and **start a new subarray** at {num}: `current_sum` = **{current_sum}**."),
                (None,
                 "The sum carried so far ({was.current_sum}) is not negative, so **extend** the subarray with {num}: "
                 "{was.current_sum} + {('(%d)' % num) if num < 0 else num} = **{current_sum}**."),
            ],
            save={"cs": "i_num if (i_num == 0 or was.current_sum < 0) else cs"})),
        ("max_sum = max(max_sum, current_sum)", dict(
            post=[
                ("max_sum > was.max_sum", "{current_sum} beats the best so far ({was.max_sum}) → `max_sum` = **{max_sum}**."),
                (None, "{current_sum} does not beat the best so far, so `max_sum` stays {max_sum}."),
            ],
            save={"best": "list(range(cs, i_num + 1)) if max_sum > was.max_sum else best"})),
        ("return max_sum", "The whole array has been scanned. The largest subarray sum is **{max_sum}**."),
    ],
    time=("O(n)", "One pass with O(1) work per number."),
    space=("O(1)", "Two running values."),
    tests=[("nums=[1]", 1), ("nums=[5, 4, -1, 7, 8]", 23), ("nums=[-3, -1, -2]", -1), ("nums=[0, -1, 0]", 0)],
)

lesson(
    "jump-game",
    pattern="Greedy: farthest reachable index",
    statement="""You start at index 0 of `nums`. The value `nums[i]` is the **maximum** jump length
    from index `i`. Return `True` if the last index can be reached.""",
    args="nums=[3, 2, 1, 0, 4]",
    expected=False,
    why="Every route ends up on index 3, whose jump length is 0. Index 4 can never be reached.",
    idea=[
        "It does not matter *how* we get somewhere, only **how far we can get at all**. Keep one number: `max_reachable`, the farthest index reachable so far.",
        "Walk through the indexes in order. If index `i` is within reach, then everything up to `i + nums[i]` is within reach too — update `max_reachable`.",
        "If we ever arrive at an index **beyond** `max_reachable`, there is a gap nobody can jump over → `False`. If the loop finishes, every index (including the last) was reachable → `True`.",
    ],
    views=[
        Arr("nums", ptrs=["i"], rng=("0", "min(max_reachable, len(nums) - 1)", "reachable", "win")),
        Vars("max_reachable"),
    ],
    notes=[
        ("max_reachable = 0", "`max_reachable` is the farthest index we know how to reach. At the start that is index 0, where we stand."),
        ("if i > max_reachable", dict(
            yes="Index {i} lies **beyond** the farthest reachable index ({max_reachable}). Nothing can get us here — or past it.",
            yes_marks={"nums.bad": "i"})),
        ("max_reachable = max(max_reachable, i + jump_length)", [
            ("max_reachable > was.max_reachable",
             "Index {i} is reachable, and from it we can jump up to {jump_length} → as far as index {i + jump_length}. "
             "That is farther than before: `max_reachable` = **{max_reachable}**."),
            (None,
             "Index {i} is reachable, but from it we get at most to index {i} + {jump_length} = {i + jump_length} — "
             "no farther than the {max_reachable} we already have."),
        ], {"nums.cur": "i"}),
        ("return False", "The last index cannot be reached → **False**."),
        ("return True", "Every index was within reach, including the last one → **True**."),
    ],
    allow_unused=True,
    time=("O(n)", "One pass over the array; each index is looked at once."),
    space=("O(1)", "A single number."),
    tests=[("nums=[2, 3, 1, 1, 4]", True), ("nums=[0]", True), ("nums=[1, 0, 1]", False), ("nums=[2, 0, 0]", True)],
)

lesson(
    "jump-game-ii",
    pattern="Greedy BFS over index ranges",
    statement="""You start at index 0 of `nums`, and `nums[i]` is the maximum jump length from index
    `i`. The last index is always reachable. Return the **minimum number of jumps** to reach it.""",
    args="nums=[2, 3, 1, 1, 4]",
    expected=2,
    why="Jump 1 step to index 1, then 3 steps to the last index.",
    idea=[
        "Group the indexes by **how many jumps** are needed to reach them: index 0 needs 0 jumps; the indexes it can jump to need 1; and so on. Each group is a contiguous window.",
        "While walking through the current window, record the farthest index any of its members can reach (`farthest_reachable`). That is where the **next** window ends.",
        "When the walk hits the end of the current window (`i == cur_end`), one more jump is unavoidable: count it and move the window end to `farthest_reachable`.",
    ],
    views=[
        Arr("nums", ptrs=["i"], rng=[("0", "cur_end", "reachable with `jumps` jumps", "win")],
            tones={"alt": "min(farthest_reachable, len(nums) - 1)"},
            title="nums  (purple = farthest index reachable with one more jump)"),
        Vars("jumps", "cur_end", "farthest_reachable"),
    ],
    notes=[
        ("farthest_reachable = 0",
         "With 0 jumps we can only be on index 0, so the current window ends at `cur_end` = 0. "
         "`farthest_reachable` tracks how far **one more jump** could take us."),
        ("farthest_reachable = max(farthest_reachable, i + nums[i])", [
            ("farthest_reachable > was.farthest_reachable",
             "From index {i} we can jump to index {i} + {nums[i]} = {i + nums[i]}. That is the farthest so far: "
             "`farthest_reachable` = **{farthest_reachable}**."),
            (None,
             "From index {i} we can jump to index {i + nums[i]} at most — not beyond the {farthest_reachable} already found."),
        ]),
        ("cur_end = farthest_reachable",
         "Index {i} was the **last index of the current window**. To go any further we must jump: `jumps` = **{jumps}**. "
         "The best jump from this window reaches index {cur_end}, so that is the end of the new window."),
        ("return jumps", "The window now covers the last index. Minimum number of jumps: **{jumps}**."),
    ],
    time=("O(n)", "One pass over the array; no index is ever revisited."),
    space=("O(1)", "Three numbers."),
    tests=[("nums=[2, 3, 0, 1, 4]", 2), ("nums=[0]", 0), ("nums=[1, 1, 1, 1]", 3), ("nums=[5, 1, 1, 1, 1]", 1), ("nums=[1, 2]", 1)],
)

lesson(
    "gas-station",
    pattern="Greedy: restart after the tank runs dry",
    statement="""Gas stations stand on a circular route. Station `i` gives you `gas[i]`, and driving
    from station `i` to the next one costs `cost[i]`. Starting with an empty tank, return the index
    of the station from which you can drive once around the circle, or `-1` if that is impossible.
    (If an answer exists it is unique.)""",
    args="gas=[5, 1, 2, 3, 4], cost=[4, 4, 1, 5, 1]",
    expected=4,
    why="From station 4 the tank goes 3, 4, 1, 2, 0 — it never drops below zero.",
    idea=[
        "If the total gas is less than the total cost, no start can work. If it is at least the total cost, some start **always** works.",
        "Try a start and keep the tank level. If the tank goes negative at station `i`, this start fails — and so does **every station between the start and i**: each of them would arrive at `i` with even less gas (we reached them with a non-negative tank).",
        "So skip them all: the next candidate is station `i + 1`, with an empty tank. The last candidate left after one pass is the answer (if the totals allow one).",
    ],
    views=[
        Arr("gas", ptrs=["i"]),
        Arr("cost"),
        Arr("[g - c for g, c in zip(gas, cost)]", id="net", title="gas − cost  (what each station adds to the tank)",
            rng=("start_station", "i", "trip from start_station", "win")),
        Vars("start_station", "current_gas", "total_gas"),
    ],
    notes=[
        ("start_station = 0",
         "`current_gas` is the tank on a trip starting at `start_station` (first candidate: station 0). "
         "`total_gas` adds up gas − cost over the whole circle to see whether a trip is possible at all."),
        ("current_gas += gas[i] - cost[i]",
         "Station {i}: fill up {gas[i]}, then burn {cost[i]} driving on. Net {gas[i] - cost[i]:+d} → tank = **{current_gas}** "
         "(overall balance {total_gas}).",
         {"net.cur": "i"}),
        ("start_station = i + 1", dict(save={"old": "was.start_station"})),
        ("current_gas = 0@2", [
            ("old == i",
             "The tank went **negative** right at station {i}: starting here fails. "
             "Next candidate: station **{start_station}**, with an empty tank."),
            (None,
             "The tank went **negative** after station {i}, so the trip from station {old} fails. Starting later, at "
             "{('station %d' % i) if old + 1 == i else ('stations %d … %d' % (old + 1, i))}, cannot help either: "
             "that trip would reach this point with even less gas. Skip ahead — next candidate: station "
             "**{start_station}**, with an empty tank."),
        ], {"net.bad": "i"}),
        ("return start_station if total_gas >= 0 else -1", [
            ("total_gas >= 0",
             "The overall balance is {total_gas} ≥ 0, so a full circle is possible — and station **{start_station}** is "
             "the only candidate that survived."),
            (None, "The overall balance is {total_gas} < 0: there is not enough gas on the whole circle → **-1**."),
        ], {"net.good": "start_station"}),
    ],
    time=("O(n)", "One pass over the stations."),
    space=("O(1)", "Three numbers."),
    tests=[("gas=[1, 2, 3, 4, 5], cost=[3, 4, 5, 1, 2]", 3), ("gas=[2, 3, 4], cost=[3, 4, 3]", -1), ("gas=[5], cost=[4]", 0), ("gas=[3, 1, 1], cost=[1, 2, 2]", 0),
           ("gas=[1, 2], cost=[2, 1]", 1)],
)

lesson(
    "hand-of-straights",
    pattern="Greedy: the smallest card must start a group",
    statement="""Given a hand of cards (integers) and a group size `W`, return `True` if the cards
    can be rearranged into groups of exactly `W` **consecutive** values.""",
    args="hand=[1, 2, 3, 6, 2, 3, 4, 7, 8], W=3",
    expected=True,
    why="[1, 2, 3], [2, 3, 4] and [6, 7, 8].",
    idea=[
        "Look at the **smallest** card that is still unused. Nothing smaller exists, so it cannot sit in the middle or at the end of a group — it must be the **start** of one.",
        "So the group is forced: starting at that card `c`, it needs `c, c + 1, …, c + W − 1`. Take one of each from the counts; if any is missing, the hand cannot be arranged.",
        "Repeat with the next smallest unused card until every card is used.",
    ],
    init={"groups": "[]"},
    views=[
        Arr("hand", ptrs={"card": "i_card"}),
        HMap("counter", title="counter  (how many of each card are still unused)"),
        Items("groups", title="groups formed"),
    ],
    notes=[
        ("if len(hand) % W != 0", dict(
            yes="{len(hand)} cards cannot be split into groups of {W} → **False**.",
            no="{len(hand)} cards make exactly {len(hand) // W} groups of {W}, so the count fits.")),
        ("hand.sort()", "Count how often each value occurs, and sort the hand so that the smallest cards come first."),
        ("if counter[card] > 0", dict(
            yes="Card {card} is the **smallest unused** card, so it has to start a group: "
                "{', '.join(str(card + k) for k in range(W))}.",
            no="Card {card}: every copy has already been used in an earlier group. Skip.")),
        ("if counter[card + i] <= 0", dict(
            yes="The group needs a {card + i}, but none is left → the hand cannot be arranged.")),
        ("counter[card + i] -= 1", dict(
            post="Take one **{card + i}** for this group ({counter[card + i]} left).",
            save={"groups": "groups + [[card]] if i == 0 else groups[:-1] + [groups[-1] + [card + i]]"},
            marks={"counter.cur": "card + i", "groups.good": "-1"})),
        ("return False@2", "A needed card is missing → **False**."),
        ("return True", "Every card has found its place in a group of {W} consecutive values → **True**."),
    ],
    allow_unused=True,
    time=("O(n log n)", "Sorting dominates; afterwards every card is taken from the counter exactly once."),
    space=("O(n)", "The counter holds one entry per distinct card value."),
    tests=[("hand=[1, 2, 3, 4, 5], W=4", False), ("hand=[1, 2, 3, 4, 5, 6], W=2", True), ("hand=[1, 1, 2, 2, 3, 3], W=3", True),
           ("hand=[1, 2, 4], W=3", False), ("hand=[8, 10, 12], W=3", False), ("hand=[5], W=1", True)],
)

lesson(
    "merge-triplets-to-form-target-triplet",
    pattern="Greedy: use every triplet that cannot overshoot",
    statement="""Merging two triplets takes the **maximum** in each of the three positions. Given
    `triplets` and a `target` triplet, return `True` if `target` can be obtained by merging some of
    the triplets (any number of them, in any order).""",
    args="triplets=[[2, 5, 3], [1, 8, 4], [1, 7, 5]], target=[2, 7, 5]",
    expected=True,
    why="Merging [2, 5, 3] and [1, 7, 5] gives [2, 7, 5]. The triplet [1, 8, 4] must be avoided because of its 8.",
    idea=[
        "Merging only ever makes values **larger**. A triplet with any value above the target at that position would push it past the target for good — such a triplet can never be used.",
        "Every other triplet is harmless: all its values are ≤ the target, so merging it in can never overshoot. So simply **merge all harmless triplets**.",
        "If that merged result equals the target, the answer is `True`. Otherwise some target value is not supplied by any usable triplet → `False`.",
    ],
    init={"ok": "[]", "bad": "[]"},
    views=[
        Grid("triplets", title="triplets  (one per row)",
             tones={"good": "[(r, c) for r in ok for c in range(3)]", "bad": "[(r, c) for r in bad for c in range(3)]",
                    "cur": "[(i_triplet, c) for c in range(3)]"}),
        Arr("target", idx=False),
        Arr("max_values", idx=False, title="max_values  (merge of the triplets used so far)",
            tones={"good": "[k for k in range(3) if max_values[k] == target[k]]"}),
    ],
    notes=[
        ("max_values = [0, 0, 0]",
         "`max_values` will be the merge (position-wise maximum) of every triplet we decide to use. Nothing is used yet."),
        ("if (", dict(
            yes="{triplet}: every value is ≤ the target {target} in its position, so using it can never overshoot. Merge it in.",
            no="{triplet}: position {next(k for k in range(3) if triplet[k] > target[k])} holds "
               "{triplet[next(k for k in range(3) if triplet[k] > target[k])]}, which is **larger** than the target's "
               "{target[next(k for k in range(3) if triplet[k] > target[k])]}. Merging it would overshoot for good — never use it.",
            save={"bad": "bad + [i_triplet] if any(triplet[k] > target[k] for k in range(3)) else bad",
                  "ok": "ok + [i_triplet] if all(triplet[k] <= target[k] for k in range(3)) else ok"})),
        ("max_values = [max(max_values[i], triplet[i]) for i in range(3)]",
         "Merged: `max_values` = **{max_values}**."),
        ("return max_values == target", [
            ("_ret", "`max_values` equals the target {target}: every target value is supplied by a usable triplet → **True**."),
            (None, "`max_values` = {max_values} does not equal the target {target}: some value can never be reached → **False**."),
        ]),
    ],
    time=("O(n)", "One pass over the triplets."),
    space=("O(1)", "Three numbers."),
    tests=[
        ("triplets=[[3, 4, 5], [4, 5, 6]], target=[3, 2, 5]", False),
        ("triplets=[[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], target=[5, 5, 5]", True),
        ("triplets=[[1, 1, 1]], target=[1, 1, 1]", True),
        ("triplets=[[1, 1, 1]], target=[1, 1, 2]", False),
    ],
)

lesson(
    "partition-labels",
    pattern="Greedy: stretch the part to each letter's last occurrence",
    statement="""Cut the string `s` into as **many parts as possible** so that each letter appears
    in at most one part. Return the sizes of the parts, in order.""",
    args='s="abacdcee"',
    expected=[3, 3, 2],
    why='"aba" | "cdc" | "ee" — no letter occurs in two different parts.',
    idea=[
        "If a part contains a letter, it must contain **all** occurrences of that letter — in particular the last one.",
        "So first record the **last index** of every letter. Then scan from the left with a current part `start … end`: each letter met pushes `end` out to that letter's last index (if it lies further).",
        "When the scan position reaches `end`, every letter inside the part ends inside it. Cutting here is safe, and cutting as early as possible gives the most parts.",
    ],
    views=[
        Arr("s", ptrs=["i"], rng=("start", "end", "current part", "win"), tones={"dim": "range(start)"}),
        HMap("last_index", title="last_index  (last position of each letter)"),
        Items("result", title="result  (part sizes)"),
    ],
    notes=[
        ("last_index[char] = i", dict(
            post="First pass done: for every letter we know the **last** index where it occurs.",
            when="i == len(s) - 1")),
        ("start, end = 0, 0",
         "`start … end` is the part being built. `end` is the index the part must reach **at least**; it grows as letters are met."),
        ("end = max(end, last_index[char])", [
            ("end > was.end",
             "`{char}` occurs for the last time at index {last_index[char]}. The part has to include that, so `end` "
             "moves out to **{end}**."),
            (None, "`{char}` (last occurrence at index {last_index[char]}) is already covered: `end` stays {end}."),
        ], {"last_index.cur": "char"}),
        ("result.append(end - start + 1)",
         "i = end = {i}: every letter met in this part has its last occurrence inside it. **Cut here.** "
         "The part `{s[start:end + 1]}` has size {end - start + 1}.",
         {"s.good": "range(start, end + 1)", "result.good": "-1"}),
        ("return result", "The whole string is cut. Part sizes: **{_ret}**."),
    ],
    time=("O(n)", "Two passes over the string."),
    space=("O(1)", "At most 26 entries in the last-index map (not counting the output)."),
    tests=[
        ('s="ababcbacadefegdehijhklij"', [9, 7, 8]),
        ('s="eccbbbbdec"', [10]),
        ('s="abc"', [1, 1, 1]),
        ('s="a"', [1]),
    ],
)

lesson(
    "valid-parenthesis-string",
    pattern="Greedy: track the range of possible open brackets",
    statement="""A string contains `(`, `)` and `*`. Each `*` may be treated as `(`, as `)` or as an
    empty string. Return `True` if the string can be made into a valid parenthesis string.""",
    args='s="(*))"',
    expected=True,
    why="Treat the * as an opening bracket: (()) is valid.",
    idea=[
        "Without stars, one counter of currently open brackets is enough. A star makes that count **uncertain** — so track the whole **range** of possible counts: `lower` (fewest open brackets possible) and `upper` (most possible).",
        "`(` raises both ends, `)` lowers both. A `*` lowers `lower` (if used as `)`) and raises `upper` (if used as `(`). `lower` is kept at 0 or above, because scenarios with a negative count are simply invalid.",
        "If `upper` drops below 0, even the most generous reading has too many `)` → `False`. At the end the string is valid exactly when 0 is in the range, i.e. `lower == 0`.",
    ],
    views=[
        Arr("s", ptrs={"char": "i_char"}),
        Vars("lower", "upper"),
    ],
    notes=[
        ("lower = upper = 0",
         "`lower` … `upper` is the range of how many brackets could be open right now, over all ways of reading the stars. "
         "Before any character: exactly 0."),
        ("upper += 1@1", "`(` opens a bracket in every reading: the range becomes **{lower} … {upper}**."),
        ("upper -= 1", [
            ("was.upper == upper + 1 and lower == 0",
             "`)` closes a bracket in every reading: the range becomes **{lower} … {upper}**. "
             "(`lower` is never allowed below 0 — readings that close more than is open are simply discarded.)"),
            (None, "`)` closes a bracket in every reading: the range becomes **{lower} … {upper}**."),
        ]),
        ("upper += 1@2",
         "`*` could close a bracket (lower − 1), open one (upper + 1), or do nothing: the range widens to **{lower} … {upper}**."),
        ("if upper < 0", dict(
            yes="`upper` is negative: even if every star is read as `(`, there is a `)` with nothing to close → **False**.")),
        ("return lower == 0", [
            ("_ret", "The string is used up and the range is {lower} … {upper}. It includes 0, so some reading leaves **no bracket open** → **True**."),
            (None, "The string is used up, but at least {lower} bracket(s) stay open in every reading → **False**."),
        ]),
    ],
    allow_unused=True,
    time=("O(n)", "One pass over the string, with O(1) work per character."),
    space=("O(1)", "Two counters."),
    tests=[('s="()"', True), ('s="(*)"', True), ('s=")("', False), ('s="(("', False), ('s="**("', False),
           ('s="(((((*)))**"', True), ('s=""', True)],
)

# end of c15_greedy
