"""Arrays & Hashing."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "contains-duplicate",
    pattern="Hash set of seen values",
    statement="""Given an integer array `nums`, return `True` if any value appears **at least
    twice**, and `False` if every element is different.""",
    args="nums=[1, 2, 3, 1]",
    expected=True,
    why="The value 1 appears at index 0 and again at index 3.",
    idea=[
        "Comparing every number with every other number works, but that is O(n²) comparisons.",
        "What we really need is a fast way to ask *have I seen this number before?*",
        "A **hash set** answers that in O(1). Walk the list once: if the current number is already in the set it is a duplicate; otherwise add it and move on.",
    ],
    views=[
        Arr("nums", ptrs={"n": "at('for n in nums')"},
            tones={"seen": "range(upto('for n in nums'))", "cur": "at('for n in nums')"}),
        HMap("hashset", title="hashset  (numbers seen so far)"),
    ],
    notes=[
        ("hashset = set()",
         "Start with an empty **hash set**. It will hold every number we have already walked past."),
        ("if n in hashset", dict(
            yes="Is {n} already in the set? **Yes** — we have met {n} before, so the list has a duplicate.",
            no="Is {n} already in the set? No — this is the first time we see {n}.",
            yes_marks={"hashset.good": "n", "nums.good": "[nums.index(n), at('for n in nums')]"})),
        ("return True",
         "Return **True** straight away. There is no need to look at the rest of the list.",
         {"hashset.good": "n", "nums.good": "[nums.index(n), at('for n in nums')]"}),
        ("hashset.add(n)",
         "Add {n} to the set, so a later copy of it will be recognised instantly.",
         {"hashset.cur": "n"}),
    ],
    time=("O(n)", "One pass; each set lookup and insert takes O(1) on average."),
    space=("O(n)", "If all numbers are different, the set ends up holding every one of them."),
    tests=[("nums=[1, 2, 3, 4]", False), ("nums=[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]", True), ("nums=[7]", False)],
)

lesson(
    "valid-anagram",
    pattern="Count letters with a hash map",
    statement="""Given two strings `s` and `t`, return `True` if `t` is an **anagram** of `s` —
    it uses exactly the same letters the same number of times, just in a different order.""",
    args="s='apple', t='papel'",
    expected=True,
    why="Both words contain a×1, p×2, l×1, e×1.",
    idea=[
        "Two words are anagrams when every letter appears the same number of times in both.",
        "Count the letters of `s` in a hash map: letter → how many.",
        "Then walk through `t` and *use up* one count per letter. If a letter is missing or already used up, it is not an anagram. Equal lengths guarantee nothing is left over at the end.",
    ],
    views=[
        Arr("s", ptrs={"char": "at('for char in s')"},
            tones={"dim": "range(upto('for char in s'))", "cur": "at('for char in s')"}),
        Arr("t", ptrs={"char": "at('for char in t')"},
            tones={"dim": "range(upto('for char in t'))", "cur": "at('for char in t')"}),
        HMap("char_frequency", title="char_frequency  (letter → how many left)"),
    ],
    notes=[
        ("if len(s) != len(t)", dict(
            no="Both strings have {len(s)} letters, so they *could* be anagrams. "
               "(Different lengths would mean **False** immediately.)")),
        ("char_frequency = {}", "Create a map that will count how many times each letter appears in `s`."),
        ("char_frequency[char] = char_frequency.get(char, 0) + 1",
         "Count `{char}` from `s`: the map now has {char_frequency[char]} of it.",
         {"char_frequency.cur": "char"}),
        ("for char in t", dict(
            yes="The map now describes `s` exactly. Next, walk through `t` and **use up** one count for each letter.",
            first=1)),
        ("char_frequency[char] -= 1",
         "`{char}` from `t`: the map still has {was.char_frequency[char]} of it, so it can be matched. "
         "Use one up → {char_frequency[char]} left.",
         {"char_frequency.good": "char"}),
        ("return True",
         "Every letter of `t` found a partner, and the lengths are equal, so nothing is left over. "
         "They are anagrams → **True**."),
    ],
    time=("O(n)", "One pass over `s` to count and one pass over `t` to match."),
    space=("O(1)", "The map holds at most one entry per distinct letter (26 for lowercase English)."),
    tests=[("s='rat', t='car'", False), ("s='ab', t='abc'", False), ("s='aacc', t='ccac'", False)],
)

lesson(
    "two-sum",
    pattern="Hash map lookup",
    statement="""Given a list of integers `nums` and a number `target`, find the two numbers that
    add up to `target` and return their **indices**. Exactly one pair works, and you may not use
    the same element twice.""",
    args="nums=[3, 11, 5, 6], target=9",
    expected=[0, 3],
    why="nums[0] + nums[3] = 3 + 6 = 9.",
    idea=[
        "Checking every pair works but costs O(n²): for each number we search the whole list for its partner.",
        "For a number `n` the partner is fixed: it must be `target − n`. So the only question is *have I already seen that value?*",
        "A hash map answers that instantly. Walk the list once: look up the partner, and if it is not there yet, store the current number with its index.",
    ],
    views=[
        Arr("nums", ptrs=["i"], tones={"seen": "list(prevMap.values())", "cur": "i"}),
        HMap("prevMap", title="prevMap  (value → index)"),
        Vars("target", "diff"),
    ],
    notes=[
        ("prevMap = {}",
         "Start with an empty hash map. It will remember every number we have passed, and the index where we saw it."),
        ("diff = target - n",
         "Index {i} holds **{n}**. To reach {target} it needs a partner worth {target} − {n} = **{diff}**."),
        ("if diff in prevMap", dict(
            yes="Is {diff} in the map? **Yes** — we met it earlier at index {prevMap[diff]}.",
            no="Is {diff} in the map? Not yet, so {n} has no partner so far.",
            yes_marks={"prevMap.good": "diff", "nums.good": "[prevMap[diff], i]"})),
        ("return [prevMap[diff], i]",
         "{nums[prevMap[diff]]} + {n} = {target}, so return their indices **{_ret}**.",
         {"prevMap.good": "diff", "nums.good": "[prevMap[diff], i]"}),
        ("prevMap[n] = i",
         "Remember **{n} → index {i}**. If a later number needs {n}, we can answer in one lookup.",
         {"prevMap.cur": "n"}),
    ],
    time=("O(n)", "One pass over the list; every map lookup and insert is O(1) on average."),
    space=("O(n)", "In the worst case the map stores almost every number before the pair appears."),
    tests=[
        ("nums=[2, 7, 11, 15], target=9", [0, 1]),
        ("nums=[3, 2, 4], target=6", [1, 2]),
        ("nums=[3, 3], target=6", [0, 1]),
    ],
)

lesson(
    "group-anagrams",
    pattern="Hash map keyed by a canonical form",
    statement="""Given a list of strings, group the **anagrams** together (words made of exactly
    the same letters). The groups and the words inside them may be returned in any order.""",
    args="strs=['eat', 'tea', 'tan', 'ate', 'nat', 'bat']",
    expected=[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]],
    why="eat / tea / ate share the letters a, e, t; tan / nat share a, n, t; bat is alone.",
    unordered=2,
    idea=[
        "Anagrams contain exactly the same letters. We need a *label* that is identical for all anagrams and different for everything else.",
        "**Sort the letters** of a word: `eat`, `tea` and `ate` all become `aet`. That sorted string is the label.",
        "Use the label as a hash-map key and append each word to its key's list. Each list in the map is one group.",
    ],
    views=[
        Arr("strs", ptrs={"word": "at('for word in strs')"},
            tones={"dim": "range(upto('for word in strs'))", "cur": "at('for word in strs')"}),
        HMap("anagrams_map", title="anagrams_map  (sorted letters → words)"),
        Vars("sorted_word"),
    ],
    notes=[
        ("anagrams_map = {}", "The map will go from a *sorted-letters key* to the list of words that share it."),
        ("sorted_word =",
         "Sort the letters of `{word}` → `{sorted_word}`. Every anagram of `{word}` produces this very same key."),
        ("anagrams_map[sorted_word].append(word)",
         "The key `{sorted_word}` already exists, so `{word}` joins that group: {anagrams_map[sorted_word]}.",
         {"anagrams_map.good": "sorted_word"}),
        ("anagrams_map[sorted_word] = [word]",
         "No group has the key `{sorted_word}` yet. Start a new group containing `{word}`.",
         {"anagrams_map.cur": "sorted_word"}),
        ("return list(anagrams_map.values())", "Each value in the map is one complete group of anagrams. Return them all."),
    ],
    time=("O(n · k log k)", "n words, and sorting a word of length k costs k log k."),
    space=("O(n · k)", "The map stores every word once."),
    tests=[("strs=['']", [[""]]), ("strs=['a']", [["a"]]), ("strs=['ab', 'ba', 'abc']", [["ab", "ba"], ["abc"]])],
)

lesson(
    "top-k-frequent-elements",
    pattern="Count, then keep the top k in a min-heap",
    statement="""Given an integer array `nums` and an integer `k`, return the `k` values that
    appear **most often**. The answer may be in any order.""",
    args="nums=[5, 3, 3, 5, 5, 8], k=2",
    expected=[3, 5],
    why="5 appears three times and 3 appears twice; 8 appears only once.",
    unordered=1,
    idea=[
        "First count how often every number appears, with a hash map.",
        "We then need the k largest counts. Sorting all of them works, but we never need the full order — only the top k.",
        "Keep a **min-heap of size k**. Its top is the *weakest* candidate. Push each (count, number); whenever the heap grows past k, pop the top. What survives is the top k.",
    ],
    views=[
        Arr("nums", ptrs={"num": "at('for num in nums')"},
            tones={"dim": "range(upto('for num in nums'))", "cur": "at('for num in nums')"}),
        HMap("frequency_map", title="frequency_map  (number → count)"),
        Heap("min_heap", title="min_heap of (count, number): smallest count on top"),
    ],
    notes=[
        ("frequency_map = {}", "Step 1: count how often each number appears."),
        ("frequency_map[num] = frequency_map.get(num, 0) + 1",
         "Count {num}: seen {plural(frequency_map[num], 'time')} so far.",
         {"frequency_map.cur": "num"}),
        ("min_heap = []",
         "Step 2: keep only the best **k = {k}** candidates. In a min-heap ordered by count, the *least* "
         "frequent candidate is always on top, ready to be thrown out."),
        ("heapq.heappush(min_heap, (frequency, num))",
         "Push ({frequency}, {num}): number {num} with count {frequency}.",
         {"frequency_map.cur": "num"}),
        ("if len(min_heap) > k", dict(
            no="The heap holds {plural(len(min_heap), 'entry', 'entries')} — not more than k = {k} — so everyone stays.")),
        ("heapq.heappop(min_heap)",
         "The heap holds {len(was.min_heap)} entries, one more than k = {k}. Pop the top: number {was.min_heap[0][1]}, "
         "which has the **smallest count** ({was.min_heap[0][0]})."),
        ("return [num for frequency, num in min_heap]",
         "The {k} numbers still in the heap are the most frequent ones: **{_ret}**."),
    ],
    time=("O(n log k)", "Counting is O(n). Each distinct number is pushed into a heap that never holds more than k + 1 items."),
    space=("O(n)", "The count map can hold every distinct number; the heap holds at most k + 1."),
    tests=[("nums=[1], k=1", [1]), ("nums=[1, 1, 1, 2, 2, 3], k=2", [1, 2]), ("nums=[4, 4, 6, 6, 6, 7], k=1", [6])],
)

lesson(
    "product-of-array-except-self",
    pattern="Prefix product × suffix product",
    statement="""Given an integer array `nums`, return an array where `answer[i]` is the product of
    **every element except** `nums[i]`. It must run in O(n) time and may **not use division**.""",
    args="nums=[1, 2, 3, 4]",
    expected=[24, 12, 8, 6],
    why="24 = 2·3·4,  12 = 1·3·4,  8 = 1·2·4,  6 = 1·2·3.",
    idea=[
        "The product of everything except `nums[i]` splits into two parts: (everything to the **left** of i) × (everything to the **right** of i).",
        "A running product gives all the left parts in one left-to-right pass.",
        "A second pass from right to left carries the running product of the right parts and multiplies it in. Two passes, no division.",
    ],
    views=[
        Arr("nums", ptrs=["i"], tones={"cur": "i"}),
        Arr("result", ptrs=["i"], tones={"cur": "i"}),
        Vars("left_product", "right_product"),
    ],
    final={"result.good": "range(n)"},
    notes=[
        ("result = [1] * n", "Every answer slot starts at 1 (the neutral value for multiplication)."),
        ("left_product = 1",
         "**Pass 1, left → right.** `left_product` is the product of all numbers to the *left* of the "
         "current index. Nothing is left of index 0, so it starts at 1."),
        ("result[i] *= left_product",
         "Index {i}: everything to its left multiplies to {left_product}. Store it: `result[{i}]` = {result[i]}."),
        ("left_product *= nums[i]",
         "Include `nums[{i}]` = {nums[i]} for the next index: `left_product` = {left_product}."),
        ("right_product = 1",
         "**Pass 2, right → left.** `right_product` is the product of all numbers to the *right* of the "
         "current index. It also starts at 1."),
        ("result[i] *= right_product",
         "Index {i}: left part {was.result[i]} × right part {right_product} = **{result[i]}**. This slot is finished.",
         {"result.good": "range(i, n)"}),
        ("right_product *= nums[i]",
         "Include `nums[{i}]` = {nums[i]} for the next index to the left: `right_product` = {right_product}.",
         {"result.good": "range(i, n)"}),
        ("return result", "Every slot holds the product of all the *other* numbers: **{_ret}**."),
    ],
    time=("O(n)", "Two passes over the array."),
    space=("O(1)", "Only two running products are stored besides the output array."),
    tests=[("nums=[-1, 1, 0, -3, 3]", [0, 0, 9, 0, 0]), ("nums=[2, 3]", [3, 2])],
)


def _sudoku_fact(k) -> str:
    if len(k) == 3:
        return f"box{k[0]}{k[1]}:{k[2]}"
    if isinstance(k[0], int):
        return f"row{k[0]}:{k[1]}"
    return f"col{k[1]}:{k[0]}"


_SUDOKU_BAD = """board=[
 ["8","3",".",".","7",".",".",".","."],
 ["6",".",".","1","9","5",".",".","."],
 [".","9","8",".",".",".",".","6","."],
 ["8",".",".",".","6",".",".",".","3"],
 ["4",".",".","8",".","3",".",".","1"],
 ["7",".",".",".","2",".",".",".","6"],
 [".","6",".",".",".",".","2","8","."],
 [".",".",".","4","1","9",".",".","5"],
 [".",".",".",".","8",".",".","7","9"]]"""

_SUDOKU_OK = _SUDOKU_BAD.replace('["8","3",".",".","7"', '["5","3",".",".","7"', 1)

_SAME_UNIT = ("[(r, c) for r in range(9) for c in range(9) if board[r][c] == num and "
              "(r == i or c == j or (r // 3 == i // 3 and c // 3 == j // 3))]")

lesson(
    "valid-sudoku",
    pattern="One hash set of row / column / box facts",
    statement="""Decide whether a partly filled 9×9 Sudoku board is **valid so far**: no digit may
    repeat within a row, within a column, or within any of the nine 3×3 boxes. Empty cells are
    `.` and are ignored. (The board does not have to be solvable.)""",
    args=_SUDOKU_BAD,
    expected=False,
    why="There are two 8s in the top-left 3×3 box: at (0, 0) and at (2, 2).",
    idea=[
        "Each filled cell must be unique in three places at once: its row, its column and its 3×3 box.",
        "Turn that into three *facts* per digit — **row r has d**, **column c has d**, **box b has d** — and keep all facts in one hash set. The box of cell (r, c) is (r // 3, c // 3).",
        "Scan the board once. If any of a digit's three facts is already in the set, the board is invalid. Otherwise add the three facts and continue.",
    ],
    views=[
        Grid("board", blank={"."}, ptrs={"i, j": "(i, j)"},
             tones={"win": "[(i, c) for c in range(9)] + [(r, j) for r in range(9)] + "
                           "[(r, c) for r in range(i // 3 * 3, i // 3 * 3 + 3) for c in range(j // 3 * 3, j // 3 * 3 + 3)]",
                    "cur": "(i, j)"}),
        HMap("seen", title="seen  (facts recorded so far)", key=_sudoku_fact),
    ],
    notes=[
        ("seen = set()",
         "One set will remember three facts about every digit we pass: its **row**, its **column** and its "
         "**3×3 box**. The highlighted band shows the row, column and box of the cell being checked."),
        ("if (", dict(
            yes="Cell ({i}, {j}) holds **{num}**. One of its three facts is **already in the set**: "
                "{num} appears twice in the same "
                "{'row' if (i, num) in seen else 'column' if (num, j) in seen else '3×3 box'}.",
            yes_marks={"board.bad": _SAME_UNIT})),
        ("return False", "A repeated digit breaks the rules → **False**.", {"board.bad": _SAME_UNIT}),
        ("seen.add((i // 3, j // 3, num))",
         "Cell ({i}, {j}) holds **{num}**. None of its facts was in the set, so it is legal so far. Record "
         "them: row {i} has {num}, column {j} has {num}, box ({i // 3}, {j // 3}) has {num}.",
         {"seen.cur": "[(i, num), (num, j), (i // 3, j // 3, num)]"}),
    ],
    time=("O(1)", "The board is always 9×9 = 81 cells, each checked with three O(1) set lookups."),
    space=("O(1)", "At most 3 facts for each of the 81 cells."),
    tests=[(_SUDOKU_OK, True)],
)

lesson(
    "encode-and-decode-strings",
    pattern="Length prefix + delimiter",
    statement="""Design `encode`, which packs a list of strings into **one** string, and `decode`,
    which turns that string back into the original list. The strings may contain **any**
    characters — including whatever delimiter you choose.""",
    code="""
    class Codec:
        def encode(self, strs: List[str]) -> str:
            parts = []
            for s in strs:
                parts.append(str(len(s)) + "#" + s)
            return "".join(parts)

        def decode(self, s: str) -> List[str]:
            decoded = []
            i = 0
            while i < len(s):
                delimiter_pos = s.find("#", i)
                size = int(s[i:delimiter_pos])
                start_pos = delimiter_pos + 1
                end_pos = start_pos + size
                decoded.append(s[start_pos:end_pos])
                i = end_pos
            return decoded
    """,
    ops=["Codec()", "encode(['lee', 'code', '#hi'])", "decode(_out[1])"],
    expected=[None, "3#lee4#code3##hi", ["lee", "code", "#hi"]],
    why="Each word is written as its length, a #, then the word — so even a word containing # is read back correctly.",
    idea=[
        "Simply joining with a separator such as `,` breaks as soon as a string contains that separator.",
        "Instead write each string as **its length, then `#`, then the string**: `lee` becomes `3#lee`.",
        "To decode, read digits up to the next `#` to learn the length, then take exactly that many characters — no matter what they are. Repeat until the end.",
    ],
    views=[
        Arr("(strs, parts)[0]", id="strs", title="strs",
            ptrs={"s": "at('for s in strs')"}, tones={"dim": "range(upto('for s in strs'))", "cur": "at('for s in strs')"}),
        Arr("(''.join(parts), strs)[0]", id="encoded", title="encoded so far  (the pieces, joined)"),
        Arr("(s, decoded)[0]", id="text", title="s  (the encoded text)",
            ptrs={"i": "i", "#": "delimiter_pos"}, rng=("start_pos", "end_pos - 1", "{end_pos - start_pos} characters")),
        Items("decoded", title="decoded"),
    ],
    notes=[
        ("parts = []",
         "We will write each string as **length + `#` + string**. The length is what makes decoding safe."),
        ('parts.append(str(len(s)) + "#" + s)',
         "`{s}` has {len(s)} characters, so write the piece `{len(s)}#{s}`."),
        ('return "".join(parts)', "Join the pieces: the whole list is now one string, `{_ret}`."),
        ("decoded = []", "Decoding reads one *length#string* chunk at a time, starting at index 0."),
        ('delimiter_pos = s.find("#", i)',
         "From `i` = {i}, find the next `#`: it is at index {delimiter_pos}. Everything between is the length."),
        ("size = int(s[i:delimiter_pos])",
         "The digits `{s[i:delimiter_pos]}` say that the next string is **{size}** characters long."),
        ("end_pos = start_pos + size",
         "So the string occupies indexes {start_pos}–{end_pos - 1}. We take exactly {size} characters, "
         "whatever they are — even another `#`."),
        ("decoded.append(s[start_pos:end_pos])", "Read `{decoded[-1]}` and add it to the result.",
         {"decoded.good": "-1"}),
        ("i = end_pos", "Jump `i` to index {i}: the start of the next chunk."),
        ("while i < len(s)", dict(no="`i` has reached the end of the text — every chunk is decoded.")),
        ("return decoded", "We are back to the original list: **{_ret}**."),
    ],
    time=("O(n)", "Both functions touch each character a constant number of times (n = total characters). "
                  "The pieces are joined once at the end, so nothing is copied again and again."),
    space=("O(n)", "The encoded string and the decoded list are as large as the input."),
    tests=[
        (["Codec()", "encode([''])", "decode(_out[1])"], [None, "0#", [""]]),
        (["Codec()", "encode(['a#b', '12#', ''])", "decode(_out[1])"], [None, "3#a#b3#12#0#", ["a#b", "12#", ""]]),
    ],
)

lesson(
    "longest-consecutive-sequence",
    pattern="Hash set + only count from sequence starts",
    statement="""Given an unsorted array of integers, return the length of the longest run of
    **consecutive values** (such as 1, 2, 3, 4). The values can be anywhere in the array, and
    the algorithm must run in O(n) time.""",
    args="nums=[100, 4, 200, 1, 3, 2]",
    expected=4,
    why="The values 1, 2, 3, 4 are all present, a run of length 4.",
    idea=[
        "Sorting would line the runs up, but sorting costs O(n log n). We need O(n).",
        "Put all numbers in a hash set. A number `x` **starts** a run exactly when `x − 1` is *not* in the set.",
        "Only from such a start, count upward: x + 1, x + 2, … while they are in the set. Numbers in the middle of a run are skipped, so every number is counted just once.",
    ],
    views=[
        Arr("nums"),
        HMap("num_set", title="num_set"),
        Vars("current_num", "current_length", "max_length"),
    ],
    notes=[
        ("num_set = set(nums)",
         "Put every number into a **hash set**. Now *is x present?* is answered in O(1), and duplicates disappear."),
        ("if num - 1 not in num_set", dict(
            yes="Take {num}. Is {num - 1} in the set? No — nothing comes right before {num}, so it **starts** a run.",
            no="Take {num}. {num - 1} is in the set, so {num} is in the *middle* of a run. Skip it — "
               "that run gets counted from its start.",
            yes_marks={"num_set.cur": "num"},
            no_marks={"num_set.dim": "num", "num_set.alt": "num - 1"})),
        ("current_length += 1",
         "{current_num} is in the set too, so the run grows: {num} … {current_num}, length **{current_length}**.",
         {"num_set.good": "range(num, current_num + 1)"}),
        ("while current_num + 1 in num_set", dict(
            no="{current_num + 1} is not in the set, so the run that started at {num} ends at {current_num}.",
            no_marks={"num_set.good": "range(num, current_num + 1)"})),
        ("max_length = max(max_length, current_length)",
         "This run has length {current_length}. Longest so far: **{max_length}**.",
         {"num_set.good": "range(num, current_num + 1)"}),
        ("return max_length", "Every run was counted exactly once, from its start. The longest has length **{_ret}**."),
    ],
    time=("O(n)", "The inner loop only runs from the start of a run, so each number is visited at most twice in total."),
    space=("O(n)", "The set stores every distinct number."),
    tests=[("nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]", 9), ("nums=[]", 0), ("nums=[1, 2, 0, 1]", 3)],
)
