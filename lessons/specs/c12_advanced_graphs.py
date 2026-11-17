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
    picture="""Picture a traveller with a pile of tickets who must use every one. From each airport, always
    take the alphabetically smallest ticket that is left. Sometimes that leads to a dead end before
    every ticket is used, and the traveller has to back up. The trick is to write an airport down
    only once you are *stuck* there, with no tickets left from it. That list comes out back to
    front, so reversing it at the end gives the route.""",
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
    say={
        "def findItinerary": (
            "The function we must write. It gets the `tickets` and returns the route that uses "
            "every ticket, starting at JFK."
        ),
        "graph = collections.defaultdict(list)": (
            "For each airport, the list of places its tickets go to (a new airport gets an empty "
            "list by itself)."
        ),
        "for start, end in sorted(tickets, reverse=True)": (
            "Go through the tickets sorted *backwards*, Z to A, so that each airport's list ends "
            "with its alphabetically smallest destination."
        ),
        "graph[start].append(end)": "Record the ticket from `start` to `end`.",
        "route = []": (
            "The airports, written down as we get stuck at them. This list comes out back to "
            "front."
        ),
        "def dfs(node)": "A helper: fly on from airport `node` while it still has tickets.",
        "while graph[node]": "Is there a ticket left from this airport?",
        "dfs(graph[node].pop())": (
            "Use the alphabetically smallest one: `.pop()` takes it off the end of the list. Then"
            " fly on from there (the helper calls itself)."
        ),
        "route.append(node)": (
            "No tickets are left from here, so this airport's place is fixed: write it down."
        ),
        'dfs("JFK")': "Start at JFK.",
        "return route[::-1]": (
            "The airports were written down from the end of the trip backwards, so reverse the "
            "list (`[::-1]`) to get the route."
        ),
    },
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
    picture="""Picture connecting houses with cables, where a cable costs its length along the streets. List
    every possible cable from cheapest to dearest. Go down the list and lay each cable, unless its
    two houses are already connected some other way, because then it would be wasted. When you reach
    the end, every house is connected for the lowest total cost. (This is known as Kruskal's
    method.)""",
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
    say={
        "def minCostConnectPoints": (
            "The function we must write. It gets the `points` and returns the cheapest total cost"
            " to connect them all."
        ),
        "def distance(p1, p2)": "A helper: the cost of joining two points.",
        "return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])": (
            "The Manhattan distance: how far apart the points are left to right, plus up and down"
            " (`abs` drops any minus sign)."
        ),
        "n = len(points)": "`n` is the number of points.",
        "distances = []": "Every possible connection, as `(cost, point i, point j)`.",
        "for i in range(n)": "Go through every point.",
        "for j in range(i + 1, n)": (
            "Pair it with every later point, so each pair is listed only once."
        ),
        "distances.append((distance(points[i], points[j]), i, j))": (
            "Record that connection with its cost."
        ),
        "distances.sort()": "Sort the connections from cheapest to dearest.",
        "parent = list(range(n))": (
            "Every point starts as the leader of its own group of connected points."
        ),
        "rank = [0] * n": (
            "A rough size for each group, used to keep the chains of leaders short."
        ),
        "mst_cost = 0": "The total cost of the connections laid so far.",
        "def find(node)": "A helper that finds the leader of a point's group.",
        "if parent[node] != node": "Is this point not its own leader?",
        "parent[node] = find(parent[node])": (
            "Then follow its parent up to the top leader and point straight at it, so later "
            "searches are quicker."
        ),
        "return parent[node]": "Return the leader.",
        "def union(node1, node2)": "A helper that merges the groups of two points.",
        "root1 = find(node1)": "The leader of the first point's group.",
        "root2 = find(node2)": "The leader of the second point's group.",
        "if root1 != root2": "Are they in different groups?",
        "if rank[root1] > rank[root2]": "Is the first group the bigger one?",
        "parent[root2] = root1": "Then hang the smaller group under the bigger one's leader.",
        "parent[root1] = root2": "Otherwise hang the first group under the second one's leader.",
        "if rank[root1] == rank[root2]": "Were the two groups the same size?",
        "rank[root2] += 1": "Then the merged group is bigger: raise its rank.",
        "for distance, u, v in distances": "Go through the connections, cheapest first.",
        "if find(u) != find(v)": "Are the two points not connected yet?",
        "union(u, v)": "Then lay this connection: merge their groups.",
        "mst_cost += distance": "And add its cost.",
        "return mst_cost": "Return the total cost.",
    },
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
    picture="""Picture news spreading from one town along one-way roads that take different times to travel.
    Always deal next with the town the news reaches *earliest* among those not dealt with yet; a
    heap keeps that town on top. From it, check whether its roads bring the news to a neighbour
    sooner than any route found before. When every reachable town is done, the answer is when the
    last town hears the news, or -1 if some town never does. (This is known as Dijkstra's method.)""",
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
    say={
        "def networkDelayTime": (
            "The function we must write. It gets the travel `times`, the number of nodes `n` and "
            "the start node `k`, and returns how long until every node has the signal."
        ),
        "graph = defaultdict(list)": (
            "For each node, the list of `(neighbour, travel time)` pairs leaving it."
        ),
        "for u, v, w in times": "Go through the connections: from `u` to `v`, taking time `w`.",
        "graph[u].append((v, w))": "Record it (one direction only).",
        'distances = [float("inf")] * (n + 1)': (
            "The earliest time the signal is known to reach each node; infinity means *not "
            "reached yet*. (Position 0 is unused, since nodes are numbered from 1.)"
        ),
        "distances[k] = 0": "The signal starts at node `k`, at time 0.",
        "pq = [(0, k)]": (
            "A heap of `(arrival time, node)`, earliest first. It starts with the start node."
        ),
        "while pq": "Repeat while there are arrivals to deal with.",
        "distance, node = heapq.heappop(pq)": "Take the earliest arrival.",
        "if distance > distances[node]": (
            "Is it out of date, because a quicker route to this node has been found since it was "
            "added?"
        ),
        "continue": "Then skip it.",
        "for neighbor, weight in graph[node]": "Look at each connection leaving this node.",
        "if distance + weight < distances[neighbor]": (
            "Would the signal reach that neighbour sooner this way than by any route found so "
            "far?"
        ),
        "distances[neighbor] = distance + weight": "Then record the new, earlier time.",
        "heapq.heappush(pq, (distances[neighbor], neighbor))": (
            "And add the arrival to the heap, so that the neighbour's own connections are looked "
            "at later."
        ),
        "max_distance = max(distances[1:])": (
            "The last node to get the signal decides the answer: take the largest time (`[1:]` "
            "skips the unused position 0)."
        ),
        'return max_distance if max_distance < float("inf") else -1': (
            "If every node was reached, return that time; if some node never was, return -1."
        ),
    },
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
    picture="""Picture a pool of uneven tiles with the water slowly rising. You can step onto a tile once the
    water covers it, so a route needs a water level as high as its highest tile. Explore from the
    corner, always taking next the reachable tile that needs the *lowest* water level; a heap keeps
    that tile on top. Carry along the highest level the route has needed so far. The first time you
    reach the far corner, that level is the answer.""",
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
    say={
        "def swimInWater": (
            "The function we must write. It gets the `grid` of heights and returns the lowest "
            "water level that lets you swim from one corner to the other."
        ),
        "n = len(grid)": "The grid is `n × n`.",
        "visited = {(0, 0)}": "The cells already added to the heap. The start cell is the first.",
        "min_heap = [(grid[0][0], 0, 0)]": (
            "A heap of `(water level needed, row, column)`, lowest level first. It starts with "
            "the top-left cell."
        ),
        "while min_heap": "Repeat while there are cells to explore.",
        "time, r, c = heapq.heappop(min_heap)": (
            "Take the cell that needs the lowest water level to reach."
        ),
        "if r == n - 1 and c == n - 1": "Is it the bottom-right corner?",
        "return time": (
            "Then this is the lowest level that works, because cells are taken in order of the "
            "level they need."
        ),
        "for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))": "Look at its four neighbours.",
        "nr, nc = r + dr, c + dc": "The neighbour's row and column.",
        "if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited": (
            "Is it inside the grid and not added yet?"
        ),
        "visited.add((nr, nc))": "Mark it as added.",
        "heapq.heappush(min_heap, (max(time, grid[nr][nc]), nr, nc))": (
            "Reaching it needs the route's level so far or the neighbour's own height, whichever "
            "is higher. Add it to the heap with that level."
        ),
    },
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
    picture="""Picture a dictionary written in an unknown alphabet. Compare each word with the next one: the
    first place where they differ gives one rule, *this letter comes before that one*. Collect all
    such rules. Then build the alphabet like a course timetable: start with the letters that need
    nothing before them, and every letter placed frees the letters waiting for it. If letters are
    left over, the rules go round in a circle and there is no valid order.""",
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
    say={
        "def alienOrder": (
            "The function we must write. It gets the `words`, sorted in the alien alphabet, and "
            "returns that alphabet's order (or an empty string if there is none)."
        ),
        "graph = {char: [] for word in words for char in word}": (
            "For every letter that appears, a list of the letters that must come after it. All "
            "empty at first."
        ),
        "in_degree = {char: 0 for char in graph}": (
            "For every letter, how many letters must come before it."
        ),
        "for i in range(len(words) - 1)": "Compare each word with the word after it.",
        "word1, word2 = words[i], words[i + 1]": "The two neighbouring words.",
        "if len(word1) > len(word2) and word1.startswith(word2)": (
            "Is the first word longer and does it *start with* the second (like `abc` before "
            "`ab`)? No alphabet can put a word before its own beginning."
        ),
        'return ""@1': "Then the order is impossible: return an empty string.",
        "for a, b in zip(word1, word2)": (
            "Walk through both words side by side, letter by letter (`zip` pairs them up)."
        ),
        "if a != b": "Is this the first place where they differ?",
        "if b not in graph[a]": "Is the rule *`a` comes before `b`* new?",
        "graph[a].append(b)": "Then record it.",
        "in_degree[b] += 1": "`b` now has one more letter that must come before it.",
        "break": (
            "Only the first difference tells us anything, so stop comparing these two words."
        ),
        "queue = deque(char for char in in_degree if in_degree[char] == 0)": (
            "Start a queue with the letters that need nothing before them."
        ),
        "result = []": "The alphabet, built in order.",
        "while queue": "Repeat while some letter is ready to be placed.",
        "char = queue.popleft()": "Take the next ready letter.",
        "result.append(char)": "Place it next in the alphabet.",
        "for neighbor in graph[char]": "Look at each letter that had to come after it.",
        "in_degree[neighbor] -= 1": "One fewer letter is still in its way.",
        "if in_degree[neighbor] == 0": "Is nothing in its way any more?",
        "queue.append(neighbor)": "Then it is ready: add it to the queue.",
        "if len(result) < len(in_degree)": "Were some letters never placed?",
        'return ""@2': (
            "Then the rules contradict each other (they go round in a circle): return an empty "
            "string."
        ),
        'return "".join(result)': "Join the letters into one string: the alien alphabet.",
    },
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
    picture="""Picture planning trips in rounds, where each round allows one more flight. At first only the
    start city has a known price, 0. In each round, try every flight once: if getting to `u` and
    then flying on to `v` is cheaper than what you knew for `v`, write the new price down. After `k
    + 1` rounds you know the cheapest price with at most `k + 1` flights, which means at most `k`
    stops. Each round reads only the previous round's prices, so no trip can sneak in an extra
    flight.""",
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
    say={
        "def findCheapestPrice": (
            "The function we must write. It gets the cities, the `flights`, the start `src`, the "
            "destination `dst` and `k`, and returns the cheapest price with at most `k` stops, or"
            " -1."
        ),
        'prices = [float("inf")] * n': (
            "The cheapest known price to reach each city. Infinity means *not reachable yet*."
        ),
        "prices[src] = 0": "Being at the start costs nothing.",
        "for _ in range(k + 1)": "One round per flight: `k` stops means at most `k + 1` flights.",
        "tmp = prices[:]": (
            "A copy of the prices, to hold this round's improvements. Reading from the old list "
            "stops one round from chaining two flights."
        ),
        "for u, v, w in flights": "Try every flight: from `u` to `v` for price `w`.",
        "if prices[u] + w < tmp[v]": (
            "Is reaching `u` (as of the last round) and then taking this flight cheaper than the "
            "best price for `v` so far?"
        ),
        "tmp[v] = prices[u] + w": "Then write down the cheaper price.",
        "prices = tmp": "The round is done: its prices are the ones the next round builds on.",
        'return -1 if prices[dst] == float("inf") else prices[dst]': (
            "If the destination was never reached, return -1; otherwise return its cheapest "
            "price."
        ),
    },
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
