# Changing a lesson

Every lesson is one `lesson(...)` call in `lessons/specs/cNN_<topic>.py`. After changing one, run

```bash
npm run lessons -- two-sum          # rebuild one lesson (leave out the slug to rebuild all 150)
npm run lessons:verify -- two-sum   # compare the solution with its brute-force reference
npm test                            # schema and consistency checks over all lesson files
```

(These call `lessons/build.py` and `lessons/verify.py` with whichever Python is installed; running
`python lessons/build.py two-sum` directly works too.) Then proof-read the result without a browser
with `python lessons/trace.py two-sum`, or open `/problem/two-sum/` in `npm run dev`.

Commit the rebuilt `content/lessons/<slug>.json` together with the spec change. The site only
reads those files, and the GitHub check fails if they are out of date.

The builder runs the real solution on the example under a tracer. A step is recorded whenever a
line that has a note finishes running. It stops with a clear error if the answer differs from
`expected=`, if a test fails, if a note's anchor matches no line, or if a caption expression breaks.

## An example

```python
lesson(
    "two-sum",
    pattern="Hash map lookup",
    statement="""Given a list of integers `nums` and a number `target`, ...""",
    args="nums=[3, 11, 5, 6], target=9",          # the example the walkthrough solves
    expected=[0, 3],
    why="nums[0] + nums[3] = 3 + 6 = 9.",
    idea=["...", "...", "..."],
    views=[                                       # what is drawn on the 3D stage
        Arr("nums", ptrs=["i"], tones={"seen": "list(prevMap.values())", "cur": "i"}),
        HMap("prevMap", title="prevMap  (value → index)"),
        Vars("target", "diff"),                   # plain variables, shown beside the code
    ],
    notes=[                                       # (start of a code line, caption[, highlights])
        ("diff = target - n",
         "Index {i} holds **{n}**. To reach {target} it needs a partner worth **{diff}**."),
        ("if diff in prevMap", dict(
            yes="Is {diff} in the map? **Yes** — we met it earlier at index {prevMap[diff]}.",
            no="Is {diff} in the map? Not yet, so {n} has no partner so far.")),
    ],
    time=("O(n)", "One pass over the list; every map lookup and insert is O(1) on average."),
    space=("O(n)", "In the worst case the map stores almost every number before the pair appears."),
    tests=[("nums=[2, 7, 11, 15], target=9", [0, 1])],
)
```

Design problems (LRU Cache, Min Stack, ...) use `ops=["LRUCache(2)", "put(1, 10)", ...]` instead
of `args=`, and `expected=` lists what each call returns.

## Written for people new to coding

Many readers have never written code, so every lesson has two more fields that explain it without
jargon. Both are required: the build stops without them.

```python
    picture="""Picture a party where every guest wears a number, ... A guest book records every
    number seen and where that guest is standing, so the answer is one glance away.""",
    say={                                         # code line (an anchor, as in notes) → plain words
        "prevMap = {}": "Make an empty **dictionary** (a hash map). It will pair each number we "
                        "pass with its position.",
        "for i, n in enumerate(nums)": "Go through the list one number at a time. `enumerate` "
                                       "hands us both the position `i` and the number `n`.",
        "diff = target - n": "Work out the partner this number needs: `target` minus `n`.",
    },
```

- `picture=` is an everyday picture of the idea (a notebook, a party, a pile of cards). It is shown
  in a box above the idea's numbered points. It must describe the *same* method the code uses.
- `say=` reads code lines in plain words. The page shows the reading of the running line under
  the code (and in the caption box on narrow screens); pointing at or tapping another line shows
  that line's reading. Explain Python syntax the first time it matters (`//`, `+=`, `.get(k, 0)`,
  `range(n - 1, -1, -1)`), say *why* where it is not obvious, and keep each reading to one or two
  short sentences. Anchors work like note anchors (`"return False@2"` is the second match).
- Every line the walkthrough stops on must have a reading: the build stops and names any line it
  misses. `class Solution:` and `import heapq` get a standard reading (`COMMON_SAY` in
  `lessons/build.py`) unless the lesson gives its own. A line that only continues a statement
  (the rest of a multi-line `if (` or `count += (`) shares the reading of the line it starts on.
- Read them back with `python lessons/trace.py <slug>`, which prints both fields.
- `key=` names the colours of the legend under the stage: a lesson's own colours
  (`key={LAND: "land (1)", WATER: "water (0)"}`) or a standard tone that means something more
  specific in this lesson (`"good": "gate (0)"`). Use it whenever a colour would otherwise be
  unexplained, or its usual label ("match / answer") would be misleading. The build rejects a key
  for a colour the lesson never draws.

## Notes (captions)

- The anchor is the start of a code line (`"diff = target - n"`). `"...@2"` picks the second line
  that starts that way.
- `{expression}` in a caption is evaluated with the solution's variables at that moment. Also
  available: `was.x` (the value before the line ran), `_ret` (a return value), helpers such as
  `plural(n, "node")`, `ordinal(k)`, `show(x)`, `nv(node)`.
- A caption can be a dict: `yes=` / `no=` for an `if`/`while`/`for` line (did it enter the body?),
  `pre=` (before the line runs), `first=N` (only the first N times), `save={"name": expr}`
  (remember a value for later captions; start it with `init={"name": expr}` on the lesson).
- A caption can be a list of `(condition, text)` pairs; the first condition that holds wins.
- Highlights are `{"view.tone": expr}`; the tones are `cur` (looking at now), `alt` (compared with),
  `good` (match / answer), `bad` (rejected), `seen` (visited), `win` (current range / path),
  `mark` (queued / flagged) and `dim` (no longer needed).

## Views

`Arr`, `HMap`, `Stack`, `Queue`, `Items`, `Vars`, `Calls` (the recursion call stack), `LinkedList`,
`Chain`, `Tree`, `Heap`, `Trie`, `RecTree` (recursion tree), `Graph`, `Grid`, `Intervals`, `Bits`.
Their options are documented at the top of each class in `lessons/engine/views.py`.

## Lessons with their own code

By default a lesson runs `solutions/<slug>.py`. A lesson can give its own `code=` instead. These 18
do, because the repository version is wrong, slower than the well-known solution, or harder to
follow: encode-and-decode-strings, minimum-window-substring, reverse-nodes-in-k-group,
binary-tree-right-side-view, kth-smallest-element-in-a-bst,
construct-binary-tree-from-preorder-and-inorder-traversal, serialize-and-deserialize-binary-tree,
design-add-and-search-words-data-structure, word-search-ii, design-twitter, permutations,
combination-sum-ii, n-queens, walls-and-gates, swim-in-rising-water, alien-dictionary
(the repository version gives wrong answers), cheapest-flights-within-k-stops, distinct-subsequences.

## The brute-force checks

`lessons/checks/` holds one `@check(slug)` per problem: a random-input generator plus either the
expected answer from a slow, obviously correct method, or a judge (`Ok(...)`) when several answers
are allowed. `python lessons/verify.py --cases 400` runs 400 random inputs per problem.
