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
    picture="""Picture each interval as a strip of tape stuck along a ruler. Lay the strips out in order of
    where they start. Then walk along them: if the next strip starts before the current one ends,
    the two overlap, so join them into one longer strip. If it starts later, the current strip is
    finished and the next one begins a new strip.""",
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
    say={
        "def merge": (
            "The function we must write. It gets the `intervals` and returns them with every "
            "overlapping group joined into one."
        ),
        "if not intervals": "Is the list empty?",
        "return []": "Then there is nothing to merge.",
        "intervals.sort(key=lambda x: x[0])": (
            'Sort by start. `key=lambda x: x[0]` means "compare the intervals by their first '
            'number", the start.'
        ),
        "result = [intervals[0]]": (
            "The answer starts with the first interval. `result[-1]` (the last one) is the group "
            "we are still growing."
        ),
        "for interval in intervals[1:]": (
            'Go through the other intervals in order. `intervals[1:]` means "all but the first".'
        ),
        "if interval[0] <= result[-1][1]": (
            "Does this interval start before (or just as) the last group ends? Then they overlap."
        ),
        "result[-1][1] = max(result[-1][1], interval[1])": (
            "Join them: the group now ends at whichever end is later."
        ),
        "else:": "Otherwise it starts after the group ends: no overlap.",
        "result.append(interval)": "It begins a new group: add it to the answer.",
        "return result": "Return the merged intervals.",
    },
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
    picture="""Picture a row of booked time slots, in order and not overlapping, and one new booking to fit in.
    Walk along the row. A slot that ends before the new booking starts stays as it is. A slot that
    overlaps the new booking melts into it, stretching it. Once a slot starts after the new booking
    ends, the booking cannot grow any more: put it in, and carry on with the rest of the row.""",
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
    key={"alt": "pending interval"},
    say={
        "def insert": (
            "The function we must write. It gets the sorted `intervals` and the `newInterval` to "
            "fit in, and returns the new list."
        ),
        "result = []": "The answer, built from left to right.",
        "new_start, new_end = newInterval": (
            "The pending interval: at first, the one to insert. This unpacks its two numbers into"
            " `new_start` and `new_end`."
        ),
        "for interval in intervals": "Go through the intervals in order.",
        "if interval[1] < new_start": (
            "Does this interval end before the pending one starts? Then it lies completely to its"
            " left."
        ),
        "result.append(interval)": "Copy it into the answer unchanged.",
        "elif interval[0] > new_end": (
            "Otherwise, does it start after the pending one ends? Then it lies completely to its "
            "right."
        ),
        "result.append([new_start, new_end])@1": (
            "The pending interval cannot grow any more: put it into the answer."
        ),
        "new_start, new_end = interval": (
            "This interval becomes the pending one. Nothing later overlaps it, so it will simply "
            "be added in turn."
        ),
        "else:": "Otherwise the two overlap.",
        "new_start = min(new_start, interval[0])": (
            "Absorb it: the pending interval starts at the earlier of the two starts,"
        ),
        "new_end = max(new_end, interval[1])": "and ends at the later of the two ends.",
        "result.append([new_start, new_end])@2": (
            "After the loop the last pending interval has not been added yet: add it."
        ),
        "return result": "Return the new list.",
    },
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
    picture="""Picture booking one room for as many meetings as possible. Always take the meeting that finishes
    first: it frees the room soonest, so it leaves the most time for the others. Then take the next
    meeting that starts after it finishes, and so on. Every meeting you could not take is one that
    must be removed.""",
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
    key={"good": "kept", "bad": "removed"},
    say={
        "def eraseOverlapIntervals": (
            "The function we must write. It gets the `intervals` and returns the fewest that must"
            " be removed so the rest do not overlap."
        ),
        "if not intervals": "Are there no intervals at all?",
        "return 0": "Then nothing needs removing.",
        "intervals.sort(key=lambda x: x[1])": (
            'Sort by end. `key=lambda x: x[1]` means "compare the intervals by their second '
            'number", the end.'
        ),
        "non_overlapping = 1": (
            "How many intervals we keep. The first one, which ends earliest, is always kept."
        ),
        "prev_end = intervals[0][1]": "Where the last kept interval ends.",
        "for i in range(1, len(intervals))": "Go through the other intervals, in order of end.",
        "if intervals[i][0] >= prev_end": (
            "Does this one start at or after the last kept one ends? Then it fits. If not, it is "
            "skipped, which means removed."
        ),
        "non_overlapping += 1": "Keep it: one more kept interval.",
        "prev_end = intervals[i][1]": "It is now the last kept one: remember where it ends.",
        "return len(intervals) - non_overlapping": (
            "Every interval not kept must be removed: return how many that is."
        ),
    },
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
    picture="""Picture one person's diary with the meetings written in order of start time. Now a clash can
    only show up between a meeting and the one written just before it. So read down the diary once:
    if any meeting starts before the one above it has finished, the person cannot go to both.""",
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
    key={"bad": "clash"},
    say={
        "def canAttendMeetings": (
            "The function we must write. It gets the meeting times `intervals` and answers "
            "whether one person can attend them all."
        ),
        "if not intervals": "Are there no meetings at all?",
        "return True@1": "Then nothing can clash.",
        "intervals.sort(key=lambda x: x[0])": (
            'Sort the meetings by start time. `key=lambda x: x[0]` means "compare them by their '
            'first number", the start.'
        ),
        "for i in range(1, len(intervals))": (
            "Go through the meetings from the second one on, comparing each with the one before "
            "it."
        ),
        "if intervals[i][0] < intervals[i - 1][1]": (
            "Does this meeting start before the previous one ends?"
        ),
        "return False": "Then they clash: answer `False`.",
        "return True@2": (
            "No meeting clashed with the one before it, so none clash at all: answer `True`."
        ),
    },
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
    picture="""Picture a manager handing out rooms as meetings begin, earliest start first. On a board they
    keep, for every room in use, the time its meeting ends, with the soonest at the top. When a
    meeting starts they only look at the top: if that room is already free, the new meeting takes it
    over. If not, every room is busy and one more room is opened. The number of rooms on the board
    at the end is the answer.""",
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
    say={
        "def minMeetingRooms": (
            "The function we must write. It gets the meeting times `intervals` and returns the "
            "fewest rooms needed."
        ),
        "if not intervals": "Are there no meetings at all?",
        "return 0": "Then no rooms are needed.",
        "intervals.sort(key=lambda x: x[0])": (
            "Sort the meetings by start time, so they are handled in the order they begin."
        ),
        "min_heap = []": (
            "A **min-heap**: a pile that always keeps its smallest number on top. It holds the "
            "end time of the meeting in each room in use."
        ),
        "heapq.heappush(min_heap, intervals[0][1])": (
            "The first meeting takes a room: push its end time."
        ),
        "for i in range(1, len(intervals))": (
            "Go through the other meetings in order of start time."
        ),
        "if intervals[i][0] >= min_heap[0]": (
            "`min_heap[0]` is the earliest end time: the room that frees up first. Is it free by "
            "the time this meeting starts?"
        ),
        "heapq.heappop(min_heap)": (
            "Then this meeting takes over that room: remove the old end time."
        ),
        "heapq.heappush(min_heap, intervals[i][1])": (
            "Either way, this meeting holds a room until it ends: push its end time."
        ),
        "return len(min_heap)": (
            "One end time per room in use, so the heap's size is the number of rooms needed."
        ),
    },
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
    picture="""Picture rulers of different lengths lying along a number line, and a list of numbers to look up.
    Look the numbers up from smallest to largest, so you only ever move forward. Before each number,
    add every ruler that starts at or before it to a pile that keeps the shortest ruler on top.
    Throw away rulers from the top that end before the number: later numbers are even bigger, so
    those rulers will never be useful again. The shortest ruler left on top is the answer for that
    number.""",
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
    key={"seen": "already pushed onto the heap"},
    say={
        "def minInterval": (
            "The function we must write. It gets the `intervals` and the `queries`, and returns "
            "for each query the size of the smallest interval that contains it."
        ),
        "intervals.sort(key=lambda x: x[0])": (
            "Sort the intervals by start, so they can be taken in order as the queries grow."
        ),
        "queries_sorted = sorted(enumerate(queries), key=lambda x: x[1])": (
            "Pair each query with its position (`enumerate`), then sort the pairs by value. The "
            "position says where each answer belongs."
        ),
        "min_heap = []": (
            "A **min-heap** of `(size, end)` pairs: the smallest interval is always on top."
        ),
        "ans = [-1] * len(queries)": (
            'One answer per query, all `-1` ("no interval") to start with.'
        ),
        "i = 0": "The first interval not yet added to the heap.",
        "for query_index, query in queries_sorted": (
            "Take the queries from smallest to largest: `query` is the value, `query_index` its "
            "original position."
        ),
        "while i < len(intervals) and intervals[i][0] <= query": (
            "While some interval not yet added starts at or before this query:"
        ),
        "start, end = intervals[i]": "take its start and end,",
        "heapq.heappush(min_heap, (end - start + 1, end))": (
            "push it with its size `end - start + 1` first, so the heap orders by size,"
        ),
        "i += 1": "and move on to the next interval.",
        "while min_heap and min_heap[0][1] < query": (
            "While the smallest interval on the heap ends before this query:"
        ),
        "heapq.heappop(min_heap)": (
            "throw it away. It cannot contain this query or any later, bigger one."
        ),
        "if min_heap": "Is any interval left on the heap?",
        "ans[query_index] = min_heap[0][0]": (
            "The top one contains the query, and it is the smallest that does: store its size at "
            "the query's original position."
        ),
        "return ans": "Return the answers in the queries' original order.",
    },
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
