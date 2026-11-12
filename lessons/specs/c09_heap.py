"""Heap / Priority Queue."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "last-stone-weight",
    pattern="Max-heap: repeatedly take the largest",
    statement="""You have stones with positive weights. Each turn, smash the **two heaviest**
    stones `x ≥ y` together: if they are equal both are destroyed, otherwise the lighter one is
    destroyed and the heavier one is left with weight `x − y`. Return the weight of the last
    remaining stone, or 0 if none is left.""",
    args="stones=[2, 7, 4, 1, 8, 1]",
    expected=1,
    why="8 vs 7 → 1,  4 vs 2 → 2,  2 vs 1 → 1,  1 vs 1 → gone. One stone of weight 1 remains.",
    idea=[
        "Every turn we need the two heaviest stones *right now* — and the list keeps changing as new stones are pushed back.",
        "Re-sorting after every smash is wasteful. A **max-heap** hands us the largest item in O(log n) and accepts new items in O(log n).",
        "Python only has a min-heap, so store each weight as a **negative** number: the heaviest stone becomes the smallest value and sits on top.",
    ],
    views=[
        Heap("max_heap", title="max-heap  (heaviest stone on top)", neg=True, tones={"cur": "0"}),
        Vars("x", "y"),
    ],
    notes=[
        ("max_heap = [-stone for stone in stones]",
         "Python's `heapq` is a **min**-heap. Storing every weight as a negative number turns it into a "
         "max-heap. (The picture shows the real, positive weights.)"),
        ("heapq.heapify(max_heap)",
         "Heapify rearranges the list into a heap in O(n). The heaviest stone, **{-max_heap[0]}**, is now on top."),
        ("x = -heapq.heappop(max_heap)", "Pop the heaviest stone: `x` = **{x}**."),
        ("y = -heapq.heappop(max_heap)", "Pop the next heaviest: `y` = **{y}**. Smash {x} against {y}."),
        ("if x != y", dict(
            no="Both stones weigh {x}, so they destroy each other completely. Nothing goes back into the heap.")),
        ("heapq.heappush(max_heap, -(x - y))",
         "They differ, so the lighter one is destroyed and {x} − {y} = **{x - y}** is left. Push that back into the heap."),
        ("while len(max_heap) > 1", dict(
            no="Fewer than two stones remain, so there is nothing left to smash.")),
        ("return -max_heap[0] if max_heap else 0",
         "{'One stone is left with weight ' + str(-max_heap[0]) if max_heap else 'No stones are left'} → return **{_ret}**."),
    ],
    time=("O(n log n)", "At most n smashes, and each one does a few heap pushes/pops costing O(log n)."),
    space=("O(n)", "The heap holds every stone."),
    tests=[("stones=[1]", 1), ("stones=[2, 2]", 0), ("stones=[3, 7, 2]", 2)],
)

lesson(
    "kth-largest-element-in-a-stream",
    pattern="Min-heap of size k",
    statement="""Design a class that is given `k` and some starting numbers. Each call `add(val)`
    adds a number to the stream and returns the **k-th largest** number seen so far.""",
    ops=["KthLargest(3, [4, 5, 8])", "add(3)", "add(5)", "add(10)", "add(9)"],
    expected=[None, 4, 5, 5, 8],
    why="After adding 9 the numbers are 3, 4, 5, 5, 8, 9, 10 — the third largest is 8.",
    idea=[
        "Only the **k largest** numbers matter. Anything smaller than all of them can never become the k-th largest later, because numbers are only ever added.",
        "Keep exactly those k numbers in a **min-heap**. Its top is the smallest of the k largest — which is precisely the k-th largest overall.",
        "To add a number: push it, and if the heap now holds k + 1 numbers, pop the smallest. The answer is the new top.",
    ],
    views=[
        Heap("self.min_heap", id="heap", title="min_heap  (the k largest so far; the smallest of them on top)",
             tones={"cur": "0"}),
        Vars(("k", "self.k"), "val"),
    ],
    notes=[
        ("self.k = k",
         "The heap will hold only the **k = {k} largest** numbers. The starting numbers are added one by one "
         "through the same `add` method."),
        ("heapq.heappush(self.min_heap, val)", "Push {val} into the min-heap."),
        ("if len(self.min_heap) > self.k", dict(
            no="The heap holds {plural(len(self.min_heap), 'number')} — not more than k = {self.k} — so nothing is removed.")),
        ("heapq.heappop(self.min_heap)", dict(
            pre="Now it holds {len(self.min_heap)}: one more than k = {self.k}. The smallest, **{self.min_heap[0]}**, "
                "can never be among the {self.k} largest again. Pop it.")),
        ("return self.min_heap[0]", dict(
            post="The heap holds the {self.k} largest numbers so far, and its top is the smallest of them: the "
                 "{ordinal(self.k)} largest overall is **{_ret}**.",
            when="_depth == 1")),
    ],
    time=("O(log k) per add", "One push and at most one pop on a heap of size k."),
    space=("O(k)", "The heap never keeps more than k numbers."),
    tests=[
        (["KthLargest(3, [4, 5, 8, 2])", "add(3)", "add(5)", "add(10)", "add(9)", "add(4)"], [None, 4, 5, 5, 8, 8]),
        (["KthLargest(1, [])", "add(-3)", "add(-2)", "add(-4)"], [None, -3, -2, -2]),
    ],
)

lesson(
    "k-closest-points-to-origin",
    pattern="Heap ordered by distance",
    statement="""Given a list of points `[x, y]` and an integer `k`, return the `k` points closest to
    the origin (0, 0). The answer may be in any order.""",
    args="points=[[3, 3], [5, -1], [-2, 4], [1, 1]], k=2",
    expected=[[1, 1], [3, 3]],
    unordered=1,
    why="Squared distances are 18, 26, 20 and 2, so the two closest points are (1, 1) and (3, 3).",
    idea=[
        "The distance from (x, y) to the origin is √(x² + y²). To *compare* distances the square root is not needed: x² + y² orders the points the same way.",
        "We need the k smallest distances, not a full sort.",
        "Put every (distance, point) pair in a **min-heap** and pop k times. Each pop hands back the closest point that is still left.",
    ],
    views=[
        Arr("points", text=lambda p: f"({p[0]},{p[1]})"),
        Heap("min_heap", title="min_heap of  distance² : point", tones={"cur": "0"},
             text=lambda e: f"{e[0]}: ({e[1][0]},{e[1][1]})"),
        Items("result", title="result", text=lambda p: f"({p[0]},{p[1]})"),
    ],
    notes=[
        ("min_heap = [(distance(point), point) for point in points]",
         "For every point compute x² + y² — the squared distance to the origin — and pair it with the point: "
         "{[d for d, _ in min_heap]}."),
        ("heapq.heapify(min_heap)", "Heapify: the pair with the **smallest distance** is now on top."),
        ("result.append(heapq.heappop(min_heap)[1])",
         "Pop the closest point that is still in the heap: **({result[-1][0]}, {result[-1][1]})**, at squared "
         "distance {distance(result[-1])}.",
         {"result.good": "-1"}),
        ("return result", "After {k} pops we have the {k} closest points: **{_ret}**."),
    ],
    time=("O(n + k log n)", "Heapify is O(n); each of the k pops costs O(log n)."),
    space=("O(n)", "The heap holds every point."),
    tests=[("points=[[1, 3], [-2, 2]], k=1", [[-2, 2]]), ("points=[[3, 3], [5, -1], [-2, 4]], k=2", [[3, 3], [-2, 4]])],
)

lesson(
    "kth-largest-element-in-an-array",
    pattern="Min-heap of size k",
    statement="""Given an integer array `nums` and an integer `k`, return the **k-th largest**
    element (in sorted order, not the k-th distinct one).""",
    args="nums=[3, 2, 1, 5, 6, 4], k=2",
    expected=5,
    why="Sorted from the largest: 6, 5, 4, 3, 2, 1 — the second one is 5.",
    idea=[
        "Sorting the whole array works in O(n log n), but we only care about the top k.",
        "Keep a **min-heap that never holds more than k numbers**: the k largest seen so far.",
        "Push every number; whenever the heap has k + 1 numbers, pop the smallest. At the end the top of the heap is the smallest of the k largest — the k-th largest.",
    ],
    views=[
        Arr("nums", ptrs={"num": "at('for num in nums')"},
            tones={"dim": "range(upto('for num in nums'))", "cur": "at('for num in nums')"}),
        Heap("min_heap", title="min_heap  (the k largest so far)", tones={"cur": "0"}),
        Vars("k"),
    ],
    notes=[
        ("min_heap = []",
         "The heap will hold only the **k = {k} largest** numbers seen so far. Being a min-heap, the smallest "
         "of them sits on top, ready to be thrown out."),
        ("heapq.heappush(min_heap, num)",
         "Next number: **{num}**. Push it onto the heap — it might be one of the {k} largest."),
        ("if len(min_heap) > k", dict(
            no="The heap holds {plural(len(min_heap), 'number')} — not more than k = {k} — so everything stays.")),
        ("heapq.heappop(min_heap)", dict(
            pre="The heap holds {len(min_heap)} numbers, one too many. The smallest, **{min_heap[0]}**, cannot be among the "
                "{k} largest. Pop it.")),
        ("return min_heap[0]",
         "The heap now holds the {k} largest numbers, and its top is the smallest of them: the {ordinal(k)} largest is **{_ret}**."),
    ],
    time=("O(n log k)", "Each of the n numbers costs one push (and maybe one pop) on a heap of size k."),
    space=("O(k)", "The heap never holds more than k + 1 numbers."),
    tests=[("nums=[3, 2, 3, 1, 2, 4, 5, 5, 6], k=4", 4), ("nums=[1], k=1", 1), ("nums=[7, 7, 7], k=2", 7)],
)

lesson(
    "task-scheduler",
    pattern="Greedy with a max-heap: most frequent task first",
    statement="""A CPU must run the given `tasks` (letters), one per time slot. Two runs of the **same**
    task must be at least `n` slots apart; if nothing may run, the CPU stays idle for that slot.
    Return the smallest number of slots needed to finish everything.""",
    args="tasks=['A', 'A', 'A', 'B', 'B', 'B'], n=2",
    expected=8,
    why="One best schedule is A B idle A B idle A B — eight slots.",
    idea=[
        "The task with the most runs left is the bottleneck: its runs must be spread out, so it should be started as early and as often as allowed.",
        "Work in blocks of `n + 1` slots. Inside one block each task runs at most once — that automatically keeps equal tasks `n` slots apart.",
        "Fill each block with the tasks that have the most runs left (a max-heap gives them). A full block costs `n + 1` slots, idle ones included; only the very last block costs just the slots it actually used.",
    ],
    views=[
        HMap("task_counts", title="task_counts"),
        Heap("max_heap", title="max_heap  (runs left; biggest on top)", neg=True, tones={"cur": "0"}),
        Arr("temp", title="temp  (runs left for the tasks used in this block)", text=lambda c: str(-c), idx=False),
        Vars("n", "cooldown"),
    ],
    notes=[
        ("task_counts = Counter(tasks)", "Count how many times each task has to run."),
        ("heapq.heapify(max_heap)",
         "From here on only the **counts** matter, not the letters. They go into a max-heap (stored as negative "
         "numbers), so the task with the most runs left is always on top."),
        ("temp = []",
         "Start a block of n + 1 = {n + 1} slots. Within one block every task may run at most once, which keeps "
         "two runs of the same task at least {n} slots apart."),
        ("temp.append(heapq.heappop(max_heap) + 1)",
         "Next slot: run the task with the most runs left. It had {-temp[-1] + 1} to go; now {-temp[-1]}."),
        ("if max_heap:@1", dict(
            no="Every available task has already run in this block, so nothing can run in this slot.")),
        ("cooldown += n + 1",
         "The tasks that still have runs left went back into the heap. More work is coming, so this block counts "
         "in full — idle slots included: time so far **{cooldown}**."),
        ("cooldown += len(temp)",
         "No task has runs left, so this was the last block. It only costs the {plural(len(temp), 'slot')} actually used: "
         "total **{cooldown}**."),
        ("return cooldown", "The CPU needs **{_ret}** time slots."),
    ],
    time=("O(T · n)", "T = number of tasks, n = the gap. Counting takes O(T). The loop then walks every slot of every "
                      "block, idle ones included, and there can be as many blocks as the most common task has runs. "
                      "The heap never holds more than 26 letters, so each heap operation is effectively O(1). "
                      "(A formula based only on the most common task gets the same answer in O(T).)"),
    space=("O(1)", "At most 26 counts."),
    tests=[("tasks=['A', 'A', 'A', 'B', 'B', 'B'], n=0", 6),
           ("tasks=['A','A','A','A','A','A','B','C','D','E','F','G'], n=2", 16), ("tasks=['A'], n=5", 1)],
)

lesson(
    "design-twitter",
    pattern="Hash maps + a heap that merges each person's newest tweets",
    statement="""Design a tiny Twitter: `postTweet(user, tweetId)`, `follow(a, b)`, `unfollow(a, b)`
    and `getNewsFeed(user)`, which returns the ids of the 10 most recent tweets posted by the user
    or by anyone the user follows, newest first.""",
    code="""
    import heapq

    class Twitter:
        def __init__(self):
            self.user_tweets = {}  # user -> list of (time, tweetId), oldest first
            self.user_followees = {}  # user -> set of the people they follow
            self.timestamp = 0

        def postTweet(self, userId: int, tweetId: int) -> None:
            self.timestamp += 1
            if userId not in self.user_tweets:
                self.user_tweets[userId] = []
            self.user_tweets[userId].append((self.timestamp, tweetId))

        def getNewsFeed(self, userId: int) -> List[int]:
            feed = []
            heap = []  # (-time, tweetId, user, index of that user's next older tweet)

            # Each person enters with their newest tweet only
            for user in self.user_followees.get(userId, set()) | {userId}:
                tweets = self.user_tweets.get(user, [])
                if tweets:
                    last = len(tweets) - 1
                    time, tweet_id = tweets[last]
                    heap.append((-time, tweet_id, user, last - 1))
            heapq.heapify(heap)

            # Take the newest tweet overall, then let that person's next older tweet compete
            while heap and len(feed) < 10:
                time, tweet_id, user, older = heapq.heappop(heap)
                feed.append(tweet_id)
                if older >= 0:
                    time, tweet_id = self.user_tweets[user][older]
                    heapq.heappush(heap, (-time, tweet_id, user, older - 1))

            return feed

        def follow(self, followerId: int, followeeId: int) -> None:
            if followerId != followeeId:
                if followerId not in self.user_followees:
                    self.user_followees[followerId] = set()
                self.user_followees[followerId].add(followeeId)

        def unfollow(self, followerId: int, followeeId: int) -> None:
            if followerId in self.user_followees:
                self.user_followees[followerId].discard(followeeId)
    """,
    ops=["Twitter()", "postTweet(1, 5)", "follow(1, 2)", "postTweet(2, 6)", "postTweet(1, 7)", "getNewsFeed(1)",
         "unfollow(1, 2)", "getNewsFeed(1)"],
    expected=[None, None, None, None, None, [7, 6, 5], None, [7, 5]],
    why="While user 1 follows user 2, tweet 6 sits between user 1's own tweets, in order of time. After unfollowing, it is gone from the feed.",
    idea=[
        "Two hash maps hold everything: each user's own tweets (oldest first), and the set of people each user follows.",
        "*Most recent* needs an order across users, so a global counter stamps every tweet with a **timestamp**.",
        "A feed needs only the 10 newest tweets, so do not gather and sort everything. Each person's list is already in time order: put just their **newest** tweet into a max-heap, take the newest overall, and replace it with that person's next older tweet. This is the *merge k sorted lists* idea.",
    ],
    views=[
        HMap("self.user_tweets", id="tweets", title="user_tweets  (user → tweets written as id@time)",
             val=lambda ts: " ".join(f"{tid}@{t}" for t, tid in ts)),
        HMap("self.user_followees", id="follows", title="user_followees  (user → who they follow)"),
        Heap("heap", title="heap  (one candidate per person: id@time, newest on top)",
             text=lambda e: f"{e[1]}@{-e[0]}", tones={"cur": "0"}),
        Items("feed", title="feed  (newest first)"),
    ],
    notes=[
        ("self.timestamp = 0",
         "Three pieces of state: every user's tweets, who each user follows, and a clock that ticks once per "
         "tweet so that tweets can be ordered by time."),
        ("self.user_tweets[userId].append((self.timestamp, tweetId))",
         "The clock ticks to {self.timestamp}. Store tweet {tweetId} for user {userId}, stamped with that time.",
         {"tweets.cur": "userId"}),
        ("heap.append((-time, tweet_id, user, last - 1))", [
            ("user == userId",
             "User {userId}'s own newest tweet is {tweet_id} (time {time}). It becomes that user's candidate for the feed."),
            (None,
             "User {userId} follows user {user}, whose newest tweet is {tweet_id} (time {time}). "
             "It becomes user {user}'s candidate."),
         ],
         {"tweets.cur": "user", "follows.cur": "userId"}),
        ("heapq.heapify(heap)",
         "The heap holds **one candidate per person** — their newest tweet — with the newest of all on top. "
         "Older tweets wait in their lists."),
        ("feed.append(tweet_id)",
         "The top of the heap is the newest tweet that is not in the feed yet: tweet {tweet_id}. Take it.",
         {"feed.good": "-1"}),
        ("if older >= 0", dict(
            no="User {user} has no older tweet, so nobody takes its place in the heap.")),
        ("heapq.heappush(heap, (-time, tweet_id, user, older - 1))",
         "User {user}'s next older tweet, {tweet_id} (time {time}), now competes in its place.",
         {"tweets.cur": "user"}),
        ("return feed", "The feed, newest first (never more than 10 tweets): **{_ret}**."),
        ("self.user_followees[followerId].add(followeeId)", "User {followerId} now follows user {followeeId}.",
         {"follows.cur": "followerId"}),
        ("self.user_followees[followerId].discard(followeeId)",
         "User {followerId} no longer follows user {followeeId}.", {"follows.cur": "followerId"}),
    ],
    time=("O(f) per feed", "f = the number of people in the feed (the user and everyone they follow). Building the heap "
                           "from one tweet per person is O(f); after that at most 10 tweets are taken out, each in "
                           "O(log f). Posting and (un)following are O(1)."),
    space=("O(U + T)", "One entry per user, plus every tweet ever posted. A feed's heap holds at most one tweet per person."),
    tests=[
        (["Twitter()", "postTweet(1, 1)", "postTweet(1, 2)", "getNewsFeed(1)", "follow(2, 1)", "getNewsFeed(2)",
          "unfollow(2, 1)", "getNewsFeed(2)", "follow(1, 1)", "unfollow(3, 1)"],
         [None, None, None, [2, 1], None, [2, 1], None, [], None, None]),
        (["Twitter()"] + [f"postTweet({1 + i % 2}, {100 + i})" for i in range(14)] + ["follow(1, 2)", "getNewsFeed(1)",
          "getNewsFeed(2)"],
         [None] * 15 + [None, [113, 112, 111, 110, 109, 108, 107, 106, 105, 104], [113, 111, 109, 107, 105, 103, 101]]),
    ],
)

lesson(
    "find-median-from-data-stream",
    pattern="Two heaps: smaller half and larger half",
    statement="""Design a class that receives numbers one at a time (`addNum`) and can report the
    **median** of everything received so far (`findMedian`). With an even count, the median is
    the average of the two middle numbers.""",
    ops=["MedianFinder()", "addNum(5)", "addNum(2)", "findMedian()", "addNum(8)", "findMedian()", "addNum(1)",
         "findMedian()"],
    expected=[None, None, None, 3.5, None, 5, None, 3.5],
    why="After 5, 2: median (2 + 5) / 2 = 3.5. After 8: the middle of 2, 5, 8 is 5. After 1: (2 + 5) / 2 = 3.5.",
    idea=[
        "Re-sorting after every insertion is too slow. But the median only depends on the **middle** of the sorted order.",
        "Split the numbers into a smaller half and a larger half. Keep the smaller half in a max-heap (its largest on top) and the larger half in a min-heap (its smallest on top). The middle values are then always at the two tops.",
        "After every insertion, rebalance so the halves differ in size by at most one (the smaller half may hold the extra number). The median is that extra top, or the average of both tops.",
    ],
    views=[
        Heap("self.max_heap", id="small", neg=True, title="max_heap  (smaller half — its largest on top)",
             tones={"cur": "0"}),
        Heap("self.min_heap", id="large", title="min_heap  (larger half — its smallest on top)",
             tones={"cur": "0"}),
        Vars("num"),
    ],
    notes=[
        ("self.max_heap = []",
         "The numbers are kept in two halves. `max_heap` holds the **smaller half** with its largest on top; "
         "`min_heap` holds the **larger half** with its smallest on top. The median is always at those tops."),
        ("heapq.heappush(self.max_heap, -num)", [
            ("len(self.max_heap) == 1 and not self.min_heap", "The first number, {num}, goes into the smaller half."),
            (None, "{num} is not larger than the top of the smaller half, so it belongs in the **smaller half**."),
        ]),
        ("heapq.heappush(self.min_heap, num)",
         "{num} is larger than {-self.max_heap[0]}, the top of the smaller half, so it belongs in the **larger half**."),
        ("heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))",
         "The smaller half now has two more numbers than the larger half. Rebalance: its largest, **{self.min_heap[0]}**, "
         "moves over to the larger half."),
        ("heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))",
         "The larger half now has more numbers. Rebalance: its smallest, **{-self.max_heap[0]}**, moves over to "
         "the smaller half."),
        ("return (-self.max_heap[0] + self.min_heap[0]) / 2",
         "Both halves hold the same amount, so the median is the average of the two tops: "
         "({-self.max_heap[0]} + {self.min_heap[0]}) / 2 = **{_ret}**."),
        ("return -self.max_heap[0]",
         "The smaller half holds one extra number, and its top is the middle value: **{_ret}**."),
    ],
    time=("O(log n) per add, O(1) per median", "Adding does a constant number of heap pushes and pops; the median just reads the tops."),
    space=("O(n)", "Every number is stored in one of the two heaps."),
    tests=[
        (["MedianFinder()", "addNum(1)", "addNum(2)", "findMedian()", "addNum(3)", "findMedian()"],
         [None, None, None, 1.5, None, 2]),
    ],
)

# end of c09_heap
