"""Advanced Graphs."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "reconstruct-itinerary",
    pattern="Eulerian path (Hierholzer): add an airport when it is a dead end",
    statement="""You are given airline `tickets` as pairs `[from, to]`. Build the itinerary that
    starts at `"JFK"` and uses **every ticket exactly once**. If several itineraries are possible,
    return the one that is smallest in alphabetical order.""",
    args='tickets=[["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]',
    expected=["JFK", "NRT", "JFK", "KUL"],
    why="Flying to KUL first would be alphabetically smaller, but KUL is a dead end: the other two tickets could never be used.",
    idea=[
        "Always taking the alphabetically smallest ticket can run into a **dead end** while tickets are still unused (here: JFK → KUL).",
        "Key insight: an airport where we get **stuck** (no unused ticket left) must be the **last** stop of whatever is still unplaced. So record airports at the moment we get stuck, and the route is built **from the end backwards**.",
        "That is a DFS that appends an airport *after* all its tickets are used (post-order). Reversing the list at the end gives the itinerary.",
    ],
    views=[
        Graph("sorted({a for t in tickets for a in t})", adj="graph", directed=True,
              title="unused tickets  (an arrow disappears when its ticket is used)",
              pos={"JFK": (0, 1.2), "KUL": (-2.6, -1.2), "NRT": (2.6, -1.2)},
              tones={"cur": "node", "good": "route"}),
        HMap("graph", id="tickets", title="graph  (unused tickets; pop() takes the last one)"),
        Calls("dfs", "dfs({node})"),
        Items("route", title="route  (built backwards)"),
    ],
    notes=[
        ("graph[start].append(end)", [
            ("len(graph) == 1 and len(graph[start]) == 1",
             "Ticket {start} → {end}. The tickets are added in **reverse** alphabetical order, so in every list the "
             "smallest destination ends up **last** — exactly where `pop()` will take it first."),
            (None, "Ticket {start} → {end}: the list for {start} is now {graph[start]}."),
        ]),
        ("route = []", "`route` will collect the airports — in reverse order of the final itinerary."),
        ("dfs(graph[node].pop())", dict(
            pre="At {node}, unused tickets lead to {graph[node]}. Take the alphabetically smallest one "
                "(**{graph[node][-1]}**, the last in the list) and fly there.")),
        ("route.append(node)",
         "{node} has **no unused ticket left** — we are stuck here. So {node} must be the last stop of everything "
         "not yet placed: append it. `route` = {route}.",
         {"route.good": "-1"}),
        ("return route[::-1]",
         "Every ticket has been used. `route` was built from the end, so reverse it: **{_ret}**."),
    ],
    time=("O(E log E)", "Sorting the E tickets dominates; the DFS itself uses every ticket exactly once."),
    space=("O(E)", "The adjacency lists, the route and the recursion stack."),
    tests=[
        ('tickets=[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]', ["JFK", "MUC", "LHR", "SFO", "SJC"]),
        ('tickets=[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]',
         ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]),
        ('tickets=[["JFK","AAA"],["AAA","JFK"],["JFK","AAA"]]', ["JFK", "AAA", "JFK", "AAA"]),
    ],
)

lesson(
    "min-cost-to-connect-all-points",
    pattern="Minimum spanning tree (Kruskal + Union-Find)",
    statement="""Each point is `[x, y]`. Connecting two points costs their **Manhattan distance**
    `|x1 − x2| + |y1 − y2|`. Return the minimum total cost to connect **all** points (so that any
    point can be reached from any other).""",
    pre="""
    def _root(parent, x):
        while parent[x] != x:
            x = parent[x]
        return x
    """,
    args="points=[[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]",
    expected=20,
    why="The cheapest connections are 1–3 (3), 0–1 (4), 3–4 (4) and 1–2 (9): 3 + 4 + 4 + 9 = 20.",
    idea=[
        "Connecting n points with the least total cost never needs a cycle, so the answer is a tree with n − 1 edges — a **minimum spanning tree**.",
        "Kruskal's rule: list every possible edge, sort by cost, and go from cheapest to most expensive.",
        "Take an edge if its two ends are **not connected yet**; skip it if they already are (it would only close a cycle). Union-Find answers *already connected?* almost instantly.",
    ],
    init={"mst": "[]", "cand": "[]"},
    views=[
        Graph("range(n)", edges="mst + cand", title="points  (green = edges chosen for the tree)",
              pos={0: (-3.5, -2.2), 1: (-1.5, -1.3), 2: (-0.5, 2.3), 3: (1.5, -1.3), 4: (3.5, -2.2)},
              tones={"cur": "[u, v]"}, etones={"good": "[(a, b) for a, b, _ in mst]"}),
        Arr("[f'{a}-{b}: {d}' for d, a, b in distances]", id="distances",
            title="distances  (every possible edge, cheapest first)", idx=False,
            tones={"cur": "i_u", "dim": "range(i_u)"}),
        Arr("parent", title="parent  (Union-Find: same root = already connected)"),
        Vars("mst_cost"),
    ],
    notes=[
        ("distances.sort()",
         "All {len(distances)} possible edges between the {n} points have been listed with their cost. "
         "**Sort them** so the cheapest comes first."),
        ("mst_cost = 0",
         "Union-Find setup: every point starts as its own group (`parent[x] = x`). `mst_cost` adds up the edges we take."),
        ("if find(u) != find(v)", dict(
            yes="Edge {u} – {v} costs {distance}. Points {u} and {v} are in **different groups** "
                "(roots {_root(parent, u)} and {_root(parent, v)}), so this edge connects something new. Take it.",
            no="Edge {u} – {v} costs {distance}, but {u} and {v} are **already connected** (same root "
               "{_root(parent, u)}). It would only close a cycle — skip it.",
            save={"cand": "[(u, v, distance)]"},
            no_marks={"graph_edges.bad": "(u, v)"},
            yes_marks={"graph_edges.cur": "(u, v)"})),
        ("mst_cost += distance", dict(
            post="The two groups are merged, and the edge joins the tree. Total cost so far: "
                 "{was.mst_cost} + {distance} = **{mst_cost}**.",
            save={"mst": "mst + [(u, v, distance)]", "cand": "[]"})),
        ("return mst_cost",
         "Every edge has been considered. The {len(mst)} chosen edges connect all {n} points for a total of **{mst_cost}**."),
    ],
    time=("O(n² log n)", "There are about n²/2 possible edges, and sorting them dominates."),
    space=("O(n²)", "The list of all edges."),
    tests=[
        ("points=[[3, 12], [-2, 5], [-4, 1]]", 18),
        ("points=[[0, 0]]", 0),
        ("points=[[0, 0], [1, 1], [1, 0], [-1, 1]]", 4),
        ("points=[[-1000000, -1000000], [1000000, 1000000]]", 4000000),
    ],
)

lesson(
    "network-delay-time",
    pattern="Dijkstra's shortest paths (min-heap)",
    statement="""A network has `n` nodes labelled `1 … n`. `times[i] = [u, v, w]` means a signal
    sent from `u` reaches `v` after `w` time units (one direction only). A signal starts at node
    `k`. Return the time until **all** nodes have received it, or `-1` if some node never does.""",
    args="times=[[1, 2, 4], [1, 3, 1], [3, 2, 2], [2, 4, 1]], n=4, k=1",
    expected=4,
    why="Node 3 gets the signal at time 1, node 2 at time 3 (through node 3, not the slow direct link) and node 4 at time 4.",
    idea=[
        "The signal reaches each node along its **shortest path** from `k`. The answer is the largest of these shortest times.",
        "Dijkstra's algorithm: keep the best known time for every node, and always process the unfinished node with the **smallest** time next (a min-heap hands it over).",
        "That smallest time can never be improved later — every other route is already at least as long — so the node is final. Then try to improve its neighbours through it (*relaxation*).",
    ],
    init={"final": "[]"},
    views=[
        Graph("range(1, n + 1)", adj="graph", adj_item="nb_w", directed=True,
              pos={1: (-2.8, 0), 2: (0.6, 1.5), 3: (0, -1.5), 4: (3, 0.6)},
              badges="{i: distances[i] for i in range(1, n + 1)}",
              title="network  (number beside a node = best known time)",
              tones={"good": "final", "cur": "node"}),
        Arr("distances", title="distances  (best known time to each node)", tones={"dim": "0", "good": "final"}),
        Items("sorted(pq)", id="pq", title="pq  (time, node) — smallest is popped first"),
    ],
    notes=[
        ("distances = [float(",
         "The links are stored as an adjacency list. `distances[x]` is the best known time for the signal to reach "
         "node x — nothing is known yet, so everything is ∞. (Index 0 is unused.)"),
        ("distances[k] = 0", "The signal starts at node {k}: it is there at time 0."),
        ("pq = [(0, k)]", "The priority queue holds (time, node) pairs. It starts with the source: (0, {k})."),
        ("if distance > distances[node]", dict(
            yes="Popped ({distance}, node {node}) — but node {node} has meanwhile been reached at time "
                "{distances[node]}. This entry is **out of date**; skip it.",
            no="Popped the smallest entry: node {node} at time {distance}. No other route can beat this, so "
               "node {node} is **final**. Now look at its outgoing links.",
            save={"final": "final if distance > distances[node] else final + [node]"})),
        ("if distance + weight < distances[neighbor]", dict(
            yes="Through node {node}, node {neighbor} is reached at {distance} + {weight} = **{distance + weight}** — "
                "better than the known {cell(distances[neighbor])}.",
            no="Through node {node}, node {neighbor} would be reached at {distance} + {weight} = {distance + weight}, "
               "which is not better than the known {cell(distances[neighbor])}. Ignore.",
            marks={"graph.alt": "neighbor", "graph_edges.cur": "(node, neighbor)", "distances.alt": "neighbor"})),
        ("heapq.heappush(pq, (distances[neighbor], neighbor))",
         "Record the better time, `distances[{neighbor}]` = {distances[neighbor]}, and push ({distances[neighbor]}, "
         "{neighbor}) so that node {neighbor} gets processed later.",
         {"graph.alt": "neighbor", "distances.alt": "neighbor", "pq.cur": "sorted(pq).index((distances[neighbor], neighbor))"}),
        ("max_distance = max(distances[1:])",
         "The queue is empty: all shortest times are known. The whole network has the signal when the **slowest** "
         "node gets it: max = {cell(max_distance)}."),
        ("return max_distance if max_distance < float(", [
            ("max_distance < inf", "Every node was reached → the answer is **{max_distance}**."),
            (None, "Some node is still at ∞: the signal never gets there → **-1**."),
        ]),
    ],
    time=("O(E log V)", "Each link can push one heap entry, and every push or pop costs O(log) of the heap size."),
    space=("O(V + E)", "Adjacency list, distance array and heap."),
    tests=[
        ("times=[[2, 1, 1], [2, 3, 1], [3, 4, 1]], n=4, k=2", 2),
        ("times=[[1, 2, 1]], n=2, k=1", 1),
        ("times=[[1, 2, 1]], n=2, k=2", -1),
        ("times=[[1, 2, 1], [2, 3, 2], [1, 3, 4]], n=3, k=1", 3),
    ],
)

lesson(
    "swim-in-rising-water",
    pattern="Dijkstra on a grid: minimise the highest cell on the path",
    statement="""`grid[r][c]` is the elevation of each cell of an `n × n` grid. At time `t` the water
    level is `t`, and you can swim between neighbouring cells only if **both** are at elevation
    `≤ t`. Swimming takes no time. Return the earliest time at which you can get from the top-left
    cell to the bottom-right cell.""",
    code="""
    class Solution:
        def swimInWater(self, grid: List[List[int]]) -> int:
            n = len(grid)
            visited = {(0, 0)}
            min_heap = [(grid[0][0], 0, 0)]  # (water level needed, row, col)

            while min_heap:
                time, r, c = heapq.heappop(min_heap)
                if r == n - 1 and c == n - 1:
                    return time

                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        heapq.heappush(min_heap, (max(time, grid[nr][nc]), nr, nc))
    """,
    args="grid=[[0, 1, 2], [5, 8, 3], [7, 6, 4]]",
    expected=4,
    why="The path 0 → 1 → 2 → 3 → 4 along the top and right edge never climbs above 4; every other route passes a higher cell.",
    idea=[
        "A path is usable as soon as the water covers its **highest** cell. So we want the path from the top-left to the bottom-right whose highest cell is as low as possible.",
        "Explore like Dijkstra: keep all reachable-but-unexplored cells in a min-heap, keyed by the water level needed to get there = the highest cell on the way.",
        "Always expand the cell that needs the **lowest** level. When the bottom-right cell is popped, no cheaper way to it can exist — its level is the answer.",
    ],
    init={"done": "[]"},
    views=[
        Grid("grid", title="grid  (elevations)",
             tones={"seen": "visited", "good": "done", "cur": "(r, c)"}),
        Items("sorted(min_heap)", id="heap", title="min_heap  (level needed, row, col) — smallest first"),
        Vars("time"),
    ],
    notes=[
        ("min_heap = [(grid[0][0], 0, 0)]",
         "Start in the top-left cell. A heap entry is (water level needed to reach the cell, row, col); "
         "standing on the start already needs level {grid[0][0]}."),
        ("time, r, c = heapq.heappop(min_heap)", dict(
            post="Pop the reachable cell that needs the **lowest** water level: ({r}, {c}), at level {time}.",
            save={"done": "done + [(r, c)]"})),
        ("if r == n - 1 and c == n - 1", dict(
            yes="({r}, {c}) is the bottom-right cell. Cells were expanded in order of the level they need, "
                "so no route with a lower level exists.")),
        ("heapq.heappush(min_heap, (max(time, grid[nr][nc]), nr, nc))",
         "Neighbour ({nr}, {nc}) has elevation {grid[nr][nc]}. Reaching it through here needs level "
         "max({time}, {grid[nr][nc]}) = **{max(time, grid[nr][nc])}**. Push it.",
         {"grid.alt": "(nr, nc)", "heap.cur": "sorted(min_heap).index((max(time, grid[nr][nc]), nr, nc))"}),
        ("return time", "The earliest time to swim across is **{time}**."),
    ],
    time=("O(n² log n)", "Each of the n² cells is pushed and popped at most once, at O(log n²) each."),
    space=("O(n²)", "The visited set and the heap."),
    tests=[
        ("grid=[[0, 2], [1, 3]]", 3),
        ("grid=[[0]]", 0),
        ("grid=[[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]", 16),
        ("grid=[[3, 2], [0, 1]]", 3),
    ],
)

lesson(
    "alien-dictionary",
    pattern="Build an order graph, then topological sort",
    statement="""An alien language uses the same lowercase letters but in an unknown order. You are
    given `words` that are already sorted by the alien alphabet. Return the letters in a valid
    alien order, or `""` if the list is contradictory.""",
    code="""
    class Solution:
        def alienOrder(self, words: List[str]) -> str:
            graph = {char: [] for word in words for char in word}
            in_degree = {char: 0 for char in graph}

            for i in range(len(words) - 1):
                word1, word2 = words[i], words[i + 1]
                if len(word1) > len(word2) and word1.startswith(word2):
                    return ""  # a word can never come before its own prefix
                for a, b in zip(word1, word2):
                    if a != b:
                        if b not in graph[a]:
                            graph[a].append(b)  # a comes before b
                            in_degree[b] += 1
                        break  # only the first difference tells us anything

            queue = deque(char for char in in_degree if in_degree[char] == 0)
            result = []

            while queue:
                char = queue.popleft()
                result.append(char)
                for neighbor in graph[char]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)

            if len(result) < len(in_degree):
                return ""  # a cycle: the rules contradict each other
            return "".join(result)
    """,
    args='words=["wrt", "wrf", "er", "ett", "rftt"]',
    expected="wertf",
    why="wrt < wrf gives t → f, wrf < er gives w → e, er < ett gives r → t, and ett < rftt gives e → r.",
    idea=[
        "Two **neighbouring** words in a sorted list reveal exactly one fact: at the first position where they differ, the letter of the earlier word comes before the letter of the later word.",
        "Collect these facts as arrows `a → b` (*a before b*) between letters. A valid alphabet is an ordering of the letters that respects every arrow — a **topological order**.",
        "Kahn's algorithm produces it: repeatedly take a letter with no incoming arrows. If letters are left over there is a cycle, so the input is contradictory. One more trap: a longer word listed before its own prefix (`abc` before `ab`) is invalid too.",
    ],
    views=[
        Arr("words", tones={"cur": "[i, i + 1] if not result and 'queue' not in dir() else []"}, idx=False),
        Graph("list(graph)", adj="graph", directed=True, badges="in_degree",
              title="arrow a → b = “a comes before b”  (number = in-degree)",
              pos={"w": (-4, 0.6), "e": (-2, -0.6), "r": (0, 0.6), "t": (2, -0.6), "f": (4, 0.6)},
              tones={"mark": "list(queue)", "good": "result", "cur": "char"}),
        Queue("queue", title="queue  (letters with nothing before them)"),
        Items("''.join(result)", id="result", title="result"),
    ],
    notes=[
        ("in_degree = {",
         "Every letter that occurs is a node: {list(graph)}. `in_degree[x]` will count how many letters must come before x."),
        ("word1, word2 = words[i], words[i + 1]",
         "Compare the neighbours `{word1}` and `{word2}`. Their first differing position tells us the order of two letters."),
        ("if len(word1) > len(word2) and word1.startswith(word2)", dict(
            yes="`{word1}` is listed before its own prefix `{word2}`, which no alphabet allows → return an empty string.")),
        ("in_degree[b] += 1",
         "First difference: `{a}` in `{word1}` against `{b}` in `{word2}`. Since `{word1}` is listed first, "
         "**{a} comes before {b}**: add the arrow {a} → {b}.",
         {"graph.alt": "[a, b]", "graph_edges.cur": "(a, b)"}),
        ("queue = deque(",
         "All neighbouring pairs are compared. Letters with in-degree 0 have nothing that must precede them: "
         "{list(queue)}. They can come first."),
        ("result.append(char)",
         "Take `{char}` — nothing has to come before it any more. Alphabet so far: **{''.join(result)}**."),
        ("in_degree[neighbor] -= 1",
         "`{neighbor}` had to wait for `{char}`. One requirement fewer: its in-degree is now {in_degree[neighbor]}.",
         {"graph.alt": "neighbor", "graph_edges.cur": "(char, neighbor)"}),
        ("queue.append(neighbor)", "`{neighbor}` has nothing left to wait for → add it to the queue."),
        ("if len(result) < len(in_degree)", dict(
            yes="Only {len(result)} of {len(in_degree)} letters could be placed: the remaining ones wait for each other in a cycle → return an empty string.",
            no="All {len(in_degree)} letters were placed, so the rules are consistent.")),
        ('return "".join(result)', "The alien alphabet order is **{_ret}**."),
    ],
    allow_unused=True,
    time=("O(C)", "C is the total number of characters: every pair of neighbouring words is compared once, and the graph has at most 26 nodes."),
    space=("O(1)", "At most 26 letters and 26 × 26 arrows, independent of the input size."),
    tests=[
        ('words=["z", "x"]', "zx"),
        ('words=["z", "x", "z"]', ""),
        ('words=["abc", "ab"]', ""),
        ('words=["z", "z"]', "z"),
        ('words=["ab", "abc"]', "abc"),
        ('words=["ac", "ab", "zc", "zb"]', "aczb"),
    ],
)

lesson(
    "cheapest-flights-within-k-stops",
    pattern="Bellman-Ford limited to k + 1 rounds",
    statement="""There are `n` cities and `flights[i] = [from, to, price]`. Return the cheapest
    price from `src` to `dst` using **at most `k` stops** (so at most `k + 1` flights), or `-1` if
    no such route exists.""",
    code="""
    class Solution:
        def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
            prices = [float("inf")] * n
            prices[src] = 0

            for _ in range(k + 1):  # k stops = at most k + 1 flights
                tmp = prices[:]  # the prices once one more flight is allowed
                for u, v, w in flights:
                    if prices[u] + w < tmp[v]:
                        tmp[v] = prices[u] + w
                prices = tmp

            return -1 if prices[dst] == float("inf") else prices[dst]
    """,
    args="n=4, flights=[[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], src=0, dst=3, k=1",
    expected=700,
    why="With one stop the only route is 0 → 1 → 3 for 100 + 600. The cheaper 0 → 1 → 2 → 3 (400) needs two stops.",
    idea=[
        "Plain shortest-path search ignores the stop limit: the cheapest route may simply use too many flights.",
        "So build the answer by **number of flights**. Start with only `src` reachable (cost 0). Each round allows **one more flight**: every flight `u → v` may extend a route that reached `u` in the previous round.",
        "Run `k + 1` rounds. The updates of a round are written to a **copy**, so a route cannot chain two new flights within the same round.",
    ],
    views=[
        Graph("range(n)", edges="flights", directed=True,
              pos={0: (-2.8, 0), 1: (0, 1.7), 2: (0, -1.7), 3: (2.8, 0)},
              badges="{i: prices[i] for i in range(n)}",
              title="flights  (number beside a city = cheapest price so far)",
              tones={"good": "[dst]", "cur": "u", "alt": "v"}),
        Arr("prices", title="prices  (cheapest with the flights allowed before this round)"),
        Arr("tmp", title="tmp  (prices after this round)"),
    ],
    notes=[
        ("prices[src] = 0",
         "`prices[c]` is the cheapest known price to reach city c. Before taking any flight only the start city "
         "{src} is reachable, at price 0; everything else is ∞."),
        ("tmp = prices[:]",
         "**Round {upto('for _ in range(k + 1)') + 1} of {k + 1}**: routes may now use up to "
         "{plural(upto('for _ in range(k + 1)') + 1, 'flight')}. Work on a copy `tmp`, so that each update extends a "
         "route from the *previous* round by exactly one flight."),
        ("if prices[u] + w < tmp[v]", dict(
            no=[
                ("prices[u] == inf and tmp[u] != inf",
                 "Flight {u} → {v} (price {w}): city {u} only became reachable **during this round** (it is in `tmp`, "
                 "not yet in `prices`). Using it now would chain two new flights in one round and break the stop "
                 "limit — so the flight has to wait."),
                ("prices[u] == inf",
                 "Flight {u} → {v} (price {w}): city {u} could not be reached before this round, so the flight cannot be used yet."),
                (None,
                 "Flight {u} → {v} (price {w}): {prices[u]} + {w} = {prices[u] + w}, not cheaper than the {cell(tmp[v])} already known for city {v}."),
            ],
            marks={"graph_edges.cur": "(u, v)", "prices.cur": "u", "tmp.alt": "v"})),
        ("tmp[v] = prices[u] + w",
         "Flight {u} → {v} (price {w}): city {u} was reachable for {prices[u]}, so city {v} can be reached for "
         "{prices[u]} + {w} = **{tmp[v]}** — cheaper than before ({cell(was.tmp[v])}). Update `tmp[{v}]`.",
         {"graph_edges.good": "(u, v)", "prices.cur": "u", "tmp.good": "v"}),
        ("prices = tmp", "The round is over: the copy becomes the new `prices` → [{', '.join(cell(p) for p in prices)}]."),
        ("return -1 if prices[dst] == float(", [
            ("prices[dst] == inf", "City {dst} is still at ∞: it cannot be reached within {k} stop(s) → **-1**."),
            (None, "After {k + 1} rounds the cheapest price to city {dst} is **{prices[dst]}**."),
        ]),
    ],
    time=("O(k · (n + E))", "k + 1 rounds; each one copies the n prices and looks at all E flights once."),
    space=("O(n)", "Two price arrays."),
    tests=[
        ("n=3, flights=[[0, 1, 100], [1, 2, 100], [0, 2, 500]], src=0, dst=2, k=1", 200),
        ("n=3, flights=[[0, 1, 100], [1, 2, 100], [0, 2, 500]], src=0, dst=2, k=0", 500),
        ("n=3, flights=[[0, 1, 100]], src=0, dst=2, k=1", -1),
        ("n=4, flights=[[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1]], src=0, dst=3, k=1", 6),
        ("n=5, flights=[[4, 1, 1], [1, 2, 3], [0, 3, 2], [0, 4, 10], [3, 1, 1], [1, 4, 3]], src=2, dst=1, k=1", -1),
    ],
)

# end of c12_advanced_graphs
