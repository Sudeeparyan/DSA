"""Intervals."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "merge-intervals",
    pattern="Sort by start, then sweep",
    statement="""Given a list of intervals `[start, end]`, merge all intervals that overlap and
    return the resulting list of non-overlapping intervals that covers the same ranges.""",
    args="intervals=[[1, 3], [8, 10], [2, 6], [15, 18]]",
    expected=[[1, 6], [8, 10], [15, 18]],
    why="[1,3] and [2,6] overlap and become [1,6]; the other two touch nothing.",
    idea=[
        "Unsorted, any interval might overlap any other one. **Sort by start time** and overlapping intervals end up next to each other.",
        "Keep the last merged interval. The next interval overlaps it exactly when it **starts no later than the last one ends**.",
        "Overlap → stretch the last interval's end to the larger of the two ends. No overlap → the next interval starts a new group.",
    ],
    init={"shown": "[list(x) for x in intervals]"},
    views=[
        Intervals([("intervals", "shown", {"cur": "i_interval + 1"}), ("result", "result")]),
    ],
    notes=[
        ("intervals.sort(key=lambda x: x[0])", dict(
            post="Sort by start time. Now intervals that overlap sit **next to each other**, so one left-to-right pass is enough.",
            save={"shown": "[list(x) for x in intervals]"})),
        ("result = [intervals[0]]",
         "Start the answer with the first interval {result[0]}. `result[-1]` is always the group we are still growing.",
         {"intervals.cur": "0", "result.good": "-1"}),
        ("if interval[0] <= result[-1][1]", dict(
            yes="{interval} starts at {interval[0]}, which is **not after** {result[-1]} ends ({result[-1][1]}) — they **overlap**.",
            no="{interval} starts at {interval[0]}, **after** {result[-1]} ends ({result[-1][1]}) — no overlap.",
            marks={"result.alt": "-1"})),
        ("result[-1][1] = max(result[-1][1], interval[1])",
         "Merge: the group's end becomes max({was.result[-1][1]}, {interval[1]}) = {result[-1][1]}. The group is now {result[-1]}.",
         {"result.good": "-1"}),
        ("result.append(interval)",
         "{interval} starts a **new group**: append it to the result.",
         {"result.good": "-1"}),
        ("return result", "All intervals processed. Return the merged list **{_ret}**."),
    ],
    time=("O(n log n)", "Sorting dominates; the merge pass afterwards is a single O(n) sweep."),
    space=("O(n)", "The result list can hold up to n intervals when nothing overlaps."),
    tests=[
        ("intervals=[[1, 4], [4, 5]]", [[1, 5]]),
        ("intervals=[[1, 4], [2, 3]]", [[1, 4]]),
        ("intervals=[[5, 6]]", [[5, 6]]),
    ],
)

lesson(
    "insert-interval",
    pattern="One pass: left of it, right of it, or overlapping",
    statement="""`intervals` is a list of non-overlapping intervals **sorted by start**. Insert
    `newInterval` so that the list stays sorted and non-overlapping, merging wherever necessary.""",
    args="intervals=[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], newInterval=[4, 8]",
    expected=[[1, 2], [3, 10], [12, 16]],
    why="[4, 8] overlaps [3, 5], [6, 7] and [8, 10]; together they become [3, 10].",
    idea=[
        "Carry one **pending** interval (at first the new one) through the sorted list and compare it with each interval.",
        "An interval that ends **before** the pending one starts lies completely to its left: copy it to the result. An interval that **overlaps** the pending one is absorbed: stretch the pending interval to cover both.",
        "The first interval that starts **after** the pending one ends lies completely to its right: the pending interval is finished and goes into the result — and that interval becomes the new pending one. Append whatever is pending at the end.",
    ],
    init={"old": "[]"},
    views=[
        Intervals([("intervals", "intervals", {"cur": "i_interval"}),
                   ("pending", "[[new_start, new_end]]", {"alt": "0"}),
                   ("result", "result")]),
    ],
    notes=[
        ("new_start, new_end = newInterval",
         "The interval to insert, [{new_start}, {new_end}], is the **pending** interval (purple). "
         "Walk through the sorted list and compare each interval with it."),
        ("result.append(interval)",
         "{interval} ends at {interval[1]}, **before** the pending interval starts ({new_start}). It lies entirely to "
         "the left — copy it to the result unchanged.",
         {"result.good": "-1"}),
        ("new_start, new_end = interval",
         "{interval} starts at {interval[0]}, **after** the pending interval {result[-1]} ends. Nothing later can "
         "overlap it either, so {result[-1]} goes into the result — and {interval} becomes the new pending interval.",
         {"result.good": "-1"}),
        ("new_start = min(new_start, interval[0])", dict(save={"old": "[was.new_start, new_end]"})),
        ("new_end = max(new_end, interval[1])",
         "{interval} **overlaps** the pending interval {old}. Absorb it: start = min({old[0]}, {interval[0]}) = "
         "{new_start}, end = max({old[1]}, {interval[1]}) = {new_end}. Pending is now **[{new_start}, {new_end}]**."),
        ("result.append([new_start, new_end])@2",
         "The list is finished. Whatever is still pending, [{new_start}, {new_end}], is appended last.",
         {"result.good": "-1"}),
        ("return result", "The new interval has been inserted and merged: **{_ret}**."),
    ],
    time=("O(n)", "One pass over the intervals."),
    space=("O(n)", "The result list."),
    tests=[
        ("intervals=[[1, 3], [6, 9]], newInterval=[2, 5]", [[1, 5], [6, 9]]),
        ("intervals=[], newInterval=[5, 7]", [[5, 7]]),
        ("intervals=[[1, 5]], newInterval=[6, 8]", [[1, 5], [6, 8]]),
        ("intervals=[[3, 5]], newInterval=[0, 1]", [[0, 1], [3, 5]]),
        ("intervals=[[1, 5]], newInterval=[2, 3]", [[1, 5]]),
    ],
)

lesson(
    "non-overlapping-intervals",
    pattern="Greedy: keep the interval that ends first",
    statement="""Given a list of intervals, return the **minimum number of intervals to remove** so
    that the rest do not overlap. Intervals that only touch (`[1, 2]` and `[2, 3]`) do not overlap.""",
    args="intervals=[[1, 2], [2, 3], [3, 4], [1, 3]]",
    expected=1,
    why="Removing [1, 3] leaves [1, 2], [2, 3], [3, 4], which only touch.",
    idea=[
        "Removing as few as possible means **keeping as many as possible**.",
        "Sort by **end** time. The interval that ends earliest leaves the most room for everything after it, so keeping it is never a mistake.",
        "Then go through the rest: an interval that starts at or after the end of the last kept one fits — keep it. Otherwise it overlaps and is removed. The answer is the total minus the number kept.",
    ],
    init={"shown": "[list(x) for x in intervals]", "kept": "[]", "gone": "[]"},
    views=[
        Intervals([("intervals", "shown", {"good": "kept", "bad": "gone", "cur": "i"})],
                  marks={"prev_end": "prev_end"},
                  title="intervals  (green = kept, red = removed)"),
        Vars("non_overlapping", "prev_end"),
    ],
    notes=[
        ("intervals.sort(key=lambda x: x[1])", dict(
            post="Sort by **end** time. The interval that finishes first blocks the least of what comes after it.",
            save={"shown": "[list(x) for x in intervals]"})),
        ("prev_end = intervals[0][1]", dict(
            post="Keep the first interval {intervals[0]} — it ends earliest. `prev_end` = {prev_end} marks where the last kept interval ends.",
            save={"kept": "[0]"})),
        ("if intervals[i][0] >= prev_end", dict(
            yes="{intervals[i]} starts at {intervals[i][0]}, not before `prev_end` = {prev_end}: it does **not overlap** the last kept interval. Keep it.",
            no="{intervals[i]} starts at {intervals[i][0]}, before `prev_end` = {prev_end}: it **overlaps** the last kept interval. "
               "Remove it — it ends later than the one we kept, so it would only block more.",
            save={"gone": "gone + [i] if intervals[i][0] < prev_end else gone"})),
        ("prev_end = intervals[i][1]", dict(
            post="Now {non_overlapping} intervals are kept, and the last one ends at `prev_end` = {prev_end}.",
            save={"kept": "kept + [i]"})),
        ("return len(intervals) - non_overlapping",
         "{non_overlapping} of the {len(intervals)} intervals can stay, so **{_ret}** must be removed."),
    ],
    time=("O(n log n)", "Sorting dominates; the scan afterwards is a single pass."),
    space=("O(1)", "A counter and one end time (besides the sort)."),
    tests=[
        ("intervals=[[1, 2], [1, 2], [1, 2]]", 2),
        ("intervals=[[1, 2], [2, 3]]", 0),
        ("intervals=[[1, 100], [11, 22], [1, 11], [2, 12]]", 2),
        ("intervals=[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]]", 2),
    ],
)

lesson(
    "meeting-rooms",
    pattern="Sort by start, compare neighbours",
    statement="""Given the `[start, end]` times of meetings, return `True` if one person could
    attend **all** of them, that is, if no two meetings overlap. A meeting may start exactly when
    another one ends.""",
    args="intervals=[[7, 10], [0, 5], [9, 12]]",
    expected=False,
    why="The meeting [7, 10] is still running when [9, 12] starts.",
    idea=[
        "Comparing every pair of meetings would take O(n²). **Sort by start time** instead.",
        "After sorting, a clash can only happen between **neighbours**: if a meeting overlaps any earlier one, it overlaps the one directly before it or that one already clashed.",
        "So one pass is enough: a meeting that starts before the previous one has ended means `False`.",
    ],
    init={"shown": "[list(x) for x in intervals]"},
    views=[
        Intervals([("intervals", "shown", {"cur": "i", "alt": "i - 1"})]),
    ],
    notes=[
        ("intervals.sort(key=lambda x: x[0])", dict(
            post="Sort the meetings by start time. Now each meeting only needs to be compared with the one right before it.",
            save={"shown": "[list(x) for x in intervals]"})),
        ("if intervals[i][0] < intervals[i - 1][1]", dict(
            yes="{intervals[i]} starts at {intervals[i][0]}, but the meeting before it, {intervals[i - 1]}, runs until "
                "{intervals[i - 1][1]}. They **overlap**.",
            no="{intervals[i]} starts at {intervals[i][0]}, when {intervals[i - 1]} has already ended "
               "({intervals[i - 1][1]}). No clash.",
            yes_marks={"intervals.bad": "[i - 1, i]"})),
        ("return False", "Two meetings overlap, so one person cannot attend them all → **False**."),
        ("return True@2", "No neighbouring meetings overlap → **True**."),
    ],
    allow_unused=True,
    time=("O(n log n)", "Sorting; the check itself is one pass."),
    space=("O(1)", "Nothing besides the sort."),
    tests=[
        ("intervals=[[7, 10], [2, 4]]", True),
        ("intervals=[]", True),
        ("intervals=[[1, 5], [5, 8]]", True),
        ("intervals=[[1, 5], [4, 8]]", False),
        ("intervals=[[0, 30], [5, 10], [15, 20]]", False),
    ],
)

lesson(
    "meeting-rooms-ii",
    pattern="Sort by start + min-heap of end times",
    statement="""Given the `[start, end]` times of meetings, return the **minimum number of rooms**
    needed so that no two meetings in the same room overlap.""",
    args="intervals=[[0, 30], [15, 20], [5, 10]]",
    expected=2,
    why="[0, 30] occupies one room the whole time; [5, 10] and [15, 20] can share a second room.",
    idea=[
        "Handle the meetings in order of **start time**. When a meeting starts, the only question is: has some room become free by now?",
        "Keep a **min-heap of end times**, one entry per room in use. Its top is the room that frees up first — if even that one is still busy, every room is.",
        "If the earliest-ending room is free (its end ≤ this start), reuse it: pop its end time. Either way push this meeting's end time. The heap's size at the end is the number of rooms.",
    ],
    init={"shown": "[list(x) for x in intervals]"},
    views=[
        Intervals([("intervals", "shown", {"cur": "i"})], marks={"earliest end": "min_heap[0]"}),
        Heap("min_heap", title="min_heap  (end time of the meeting in each room)"),
    ],
    notes=[
        ("intervals.sort(key=lambda x: x[0])", dict(
            post="Sort the meetings by start time, so they are handled in the order they begin.",
            save={"shown": "[list(x) for x in intervals]"})),
        ("heapq.heappush(min_heap, intervals[0][1])",
         "The first meeting {intervals[0]} takes a room. The heap stores, for each room in use, **when its meeting ends** "
         "— the top is the room that frees up first.",
         {"intervals.cur": "0"}),
        ("if intervals[i][0] >= min_heap[0]", dict(
            yes="Meeting {intervals[i]} starts at {intervals[i][0]}. The earliest room is free from {min_heap[0]} — in time. "
                "**Reuse that room.**",
            no="Meeting {intervals[i]} starts at {intervals[i][0]}, but even the room that frees up first is busy until "
               "{min_heap[0]}. A **new room** is needed.")),
        ("heapq.heappush(min_heap, intervals[i][1])",
         "This meeting's room is now busy until {intervals[i][1]}. Rooms in use: **{len(min_heap)}**."),
        ("return len(min_heap)", "Every meeting has a room. Rooms needed: **{_ret}**."),
    ],
    time=("O(n log n)", "Sorting, plus one heap push/pop per meeting."),
    space=("O(n)", "The heap can hold one end time per meeting."),
    tests=[
        ("intervals=[[7, 10], [2, 4]]", 1),
        ("intervals=[]", 0),
        ("intervals=[[1, 5], [2, 6], [3, 7]]", 3),
        ("intervals=[[1, 5], [5, 8], [8, 9]]", 1),
        ("intervals=[[0, 30], [5, 10], [15, 20]]", 2),
    ],
)

lesson(
    "minimum-interval-to-include-each-query",
    pattern="Sort queries + min-heap of candidate intervals",
    statement="""Given `intervals` and a list of `queries` (numbers), find for each query the
    **size of the smallest interval that contains it** (`size = end − start + 1`), or `-1` if no
    interval contains it. Return the answers in the original order of the queries.""",
    args="intervals=[[1, 4], [2, 4], [3, 6], [4, 4]], queries=[2, 3, 4, 5]",
    expected=[3, 3, 1, 4],
    why="2 and 3 are inside [2, 4] (size 3); 4 is inside [4, 4] (size 1); 5 is only inside [3, 6] (size 4).",
    idea=[
        "Answer the queries in **increasing order** (remembering where each came from). Then intervals can be handled in order of start time, each one only once.",
        "For the current query, push every interval that **starts at or before it** onto a min-heap keyed by size. Those are the only intervals that might contain it.",
        "Pop intervals from the top while they **end before the query** — they cannot contain this query or any later one. The top that remains is the smallest interval containing the query.",
    ],
    init={"shown": "[list(x) for x in intervals]"},
    views=[
        Intervals([("intervals", "shown", {"seen": "range(i)"})], marks={"query": "query"},
                  title="intervals  (blue = already pushed onto the heap)"),
        Items("sorted(min_heap)", id="heap", title="min_heap  (size, end) — smallest size first"),
        Arr("queries", tones={"cur": "query_index"}),
        Arr("ans"),
    ],
    notes=[
        ("queries_sorted = sorted(enumerate(queries), key=lambda x: x[1])", dict(
            post="Sort the intervals by start, and the queries by value (each keeps its original position so the answer "
                 "can be stored in the right place).",
            save={"shown": "[list(x) for x in intervals]"})),
        ("for query_index, query in queries_sorted", dict(
            yes="Next query, in increasing order: **{query}** (it was at position {query_index}).")),
        ("heapq.heappush(min_heap, (end - start + 1, end))",
         "[{start}, {end}] starts at or before {query}, so it may contain the query. Push it with its size: ({end - start + 1}, end {end}).",
         {"heap.cur": "sorted(min_heap).index((end - start + 1, end))"}),
        ("heapq.heappop(min_heap)",
         "The smallest interval on the heap ends at {was.min_heap[0][1]} — **before** {query}. It cannot contain this "
         "query or any later one, so discard it."),
        ("ans[query_index] = min_heap[0][0]",
         "The top of the heap is now the **smallest** interval that contains {query}: size {min_heap[0][0]}. "
         "Store it at position {query_index}.",
         {"ans.good": "query_index", "heap.good": "0"}),
        ("if min_heap", dict(
            no="No interval on the heap contains {query}: the answer at position {query_index} stays **-1**.")),
        ("return ans", "All queries are answered, in their original order: **{_ret}**."),
    ],
    allow_unused=True,
    time=("O(n log n + q log q)", "Sorting both lists; each interval is pushed and popped at most once."),
    space=("O(n + q)", "The heap, the sorted queries and the answer array."),
    tests=[
        ("intervals=[[2, 3], [2, 5], [1, 8], [20, 25]], queries=[2, 19, 5, 22]", [2, -1, 4, 6]),
        ("intervals=[[1, 1]], queries=[1, 2]", [1, -1]),
        ("intervals=[[5, 9]], queries=[1]", [-1]),
        ("intervals=[[4, 5], [5, 8], [1, 9], [8, 10], [1, 6]], queries=[7, 9, 3, 9, 3]", [4, 3, 6, 3, 6]),
    ],
)

# end of c16_intervals
