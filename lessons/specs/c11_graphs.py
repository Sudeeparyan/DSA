"""Graphs."""

from lessons.engine.api import *  # noqa: F401,F403

LAND = "#3d9950"
WATER = "#1c3d5e"

lesson(
    "number-of-islands",
    pattern="Grid flood-fill (DFS)",
    statement="""You are given a grid of `"1"` (land) and `"0"` (water). An **island** is a group
    of land cells connected horizontally or vertically. Count the islands.""",
    args='grid=[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]',
    expected=3,
    why="Top-left block of four cells, the single cell in the middle, and the pair at the bottom right.",
    idea=[
        "Scan the grid cell by cell. The first time we touch a piece of land that nobody has visited, we have discovered a new island — count it.",
        "The danger is counting the same island again from another of its cells. So as soon as an island is discovered, visit **all** of it and mark every cell as visited.",
        "That *visit everything connected* step is a flood-fill (DFS): sink the cell to `0`, then recurse into its four neighbours.",
    ],
    views=[
        Grid("grid", vals={"1": LAND, "0": WATER}, changed="seen",
             ptrs={"scan": "(i, j)"}, tones={"cur": "(row, col)"}),
        Calls("dfs", "dfs({row}, {col})"),
        Vars("count"),
    ],
    notes=[
        ("count = 0",
         "The grid has {rows} rows and {cols} columns: green is land (`1`), dark blue is water (`0`). "
         "`count` holds the number of islands found so far."),
        ("count += 1",
         "The scan reaches ({i}, {j}) and finds land that nobody has visited — a **new island**. "
         "`count` becomes **{count}**."),
        ("dfs(i, j)", dict(
            pre="Flood-fill from ({i}, {j}): visit every land cell connected to it and sink it to `0`, "
                "so this island can never be counted again.",
            post="The whole island is sunk (light blue). Continue scanning for the next piece of unvisited land.")),
        ("if (", dict(
            yes="({row}, {col}) is {'outside the grid' if not (0 <= row < rows and 0 <= col < cols) else 'water or already visited'} "
                "— nothing to do here, go back.",
            first=2)),
        ('grid[row][col] = "0"',
         "Visit ({row}, {col}) and **sink** it to `0` so it counts as visited. Then try its four neighbours: "
         "down, up, right, left."),
        ("return count",
         "Every cell has been scanned. A flood-fill was started {count} times, so there are **{count} islands**."),
    ],
    time=("O(rows × cols)", "Each cell is scanned once, and each land cell is sunk at most once."),
    space=("O(rows × cols)", "If the whole grid is land, the recursion can go as deep as the number of cells."),
    tests=[
        ('grid=[["1","1","1"],["0","1","0"],["1","1","1"]]', 1),
        ('grid=[["0"]]', 0),
        ('grid=[["1","0","1","0","1"]]', 3),
    ],
)

lesson(
    "course-schedule",
    pattern="Topological sort (Kahn's algorithm)",
    statement="""There are `numCourses` courses labelled `0 … numCourses − 1`. Each pair `[a, b]`
    in `prerequisites` means you must take course `b` **before** course `a`. Return `True` if it
    is possible to finish every course.""",
    args="numCourses=4, prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]]",
    expected=True,
    why="One valid order is 0 → 1 → 2 → 3.",
    idea=[
        "Draw every rule as an arrow `b → a`. Finishing everything is impossible only when the arrows form a **cycle** (A needs B and B needs A).",
        "A course with no unmet prerequisites (in-degree 0) can be taken right now. Taking it removes its outgoing arrows, which may free other courses.",
        "Repeat with a queue. If every course gets taken → `True`. Courses on a cycle never reach in-degree 0, so they are left over → `False`.",
    ],
    init={"taken": "[]"},
    views=[
        Graph("range(numCourses)", adj="graph", directed=True,
              pos={0: (0, 1.7), 1: (-1.9, 0), 2: (1.9, 0), 3: (0, -1.7)},
              title="arrow = “must be taken before”",
              tones={"mark": "list(queue)", "good": "taken", "cur": "node"}),
        Arr("in_degree", title="in_degree  (prerequisites still missing)", tones={"good": "taken"}),
        Queue("queue", title="queue  (ready to take)"),
    ],
    notes=[
        ("graph = {i: [] for i in range(numCourses)}",
         "Treat each course as a node. We will draw an arrow **prerequisite → course**."),
        ("in_degree = [0] * numCourses",
         "`in_degree[c]` counts how many prerequisites course `c` is still waiting for."),
        ("in_degree[course] += 1",
         "Course {prereq} must come before course {course}: add the arrow {prereq} → {course}. "
         "Course {course} now waits for {plural(in_degree[course], 'prerequisite')}.",
         {"in_degree.cur": "course", "graph.cur": "course", "graph.alt": "prereq", "graph_edges.cur": "(prereq, course)"}),
        ("queue = collections.deque(",
         "Courses whose in-degree is 0 need nothing first, so they can be taken immediately. "
         "Put them in the queue: {list(queue)}."),
        ("node = queue.popleft()", dict(
            post="**Take course {node}** — nothing is blocking it. Every course that depended on it is now one step closer.",
            save={"taken": "taken + [node]"})),
        ("in_degree[neighbor] -= 1",
         "Course {neighbor} was waiting for course {node}. One prerequisite fewer: its in-degree drops to {in_degree[neighbor]}.",
         {"in_degree.cur": "neighbor", "graph.alt": "neighbor", "graph_edges.cur": "(node, neighbor)"}),
        ("queue.append(neighbor)",
         "Course {neighbor} has **no prerequisites left**, so it is ready. Add it to the queue."),
        ("return all(degree == 0 for degree in in_degree)",
         "Every course reached in-degree 0, so all {numCourses} can be taken → **{_ret}**. "
         "(Had there been a cycle, its courses would be stuck above 0.)"),
    ],
    time=("O(V + E)", "Every course (V) is queued once and every prerequisite arrow (E) is followed once."),
    space=("O(V + E)", "The adjacency list stores all arrows; the in-degree list and queue store up to V courses."),
    tests=[
        ("numCourses=2, prerequisites=[[1, 0], [0, 1]]", False),
        ("numCourses=2, prerequisites=[[1, 0]]", True),
        ("numCourses=3, prerequisites=[]", True),
    ],
)

lesson(
    "clone-graph",
    pattern="DFS + hash map (original → copy)",
    statement="""You are given one node of a connected undirected graph. Every node has a value and
    a list of its neighbours. Return a **deep copy** of the whole graph: brand-new nodes with the
    same values and the same connections.""",
    pre="""
    Node = GraphNode

    def _all(start):
        seen, order, todo = set(), [], [start]
        while todo:
            x = todo.pop(0)
            if x is None or id(x) in seen:
                continue
            seen.add(id(x))
            order.append(x)
            todo.extend(x.neighbors)
        return sorted(order, key=lambda n: n.val)

    def _adj(start):
        return {x.val: [nb.val for nb in x.neighbors] for x in _all(start)}

    def _checked(copy, original):
        if copy is None:
            return []
        if {id(x) for x in _all(copy)} & {id(x) for x in _all(original)}:
            return "the copy shares nodes with the original"
        return [[nb.val for nb in x.neighbors] for x in _all(copy)]
    """,
    args="node=G([[2, 4], [1, 3], [2, 4], [1, 3]])",
    show_input="adjList = [[2,4],[1,3],[2,4],[1,3]]   (node 1 is linked to 2 and 4, node 2 to 1 and 3, …)",
    result="_checked(_ret, node)",
    expected=[[2, 4], [1, 3], [2, 4], [1, 3]],
    show_output="a new graph with the same shape: [[2,4],[1,3],[2,4],[1,3]]",
    why="The copy has four new nodes wired exactly like the original, and shares no node with it.",
    idea=[
        "Walk the graph with DFS and create one new node for every original node.",
        "Graphs have cycles, so the walk will come back to nodes it has already seen. A hash map **original → copy** answers two questions at once: *have I copied this node?* and *where is its copy?*",
        "Register the copy in the map **before** visiting the neighbours. Then when a cycle leads back here, the existing copy is returned instead of starting an endless loop.",
    ],
    views=[
        Graph("list(_adj(node))", adj="_adj(node)", id="original", title="original graph",
              pos={1: (-1.3, 1.3), 2: (1.3, 1.3), 3: (1.3, -1.3), 4: (-1.3, -1.3)},
              tones={"seen": "[k.val for k in visited]", "cur": "original_node.val"}),
        Graph("[x.val for x in visited.values()]",
              adj="{x.val: [nb.val for nb in x.neighbors] for x in visited.values()}",
              id="clone", title="copy  (new nodes)",
              pos={1: (-1.3, 1.3), 2: (1.3, 1.3), 3: (1.3, -1.3), 4: (-1.3, -1.3)},
              tones={"good": "new_node.val"}),
        Calls("dfs", "dfs(node {original_node.val})"),
    ],
    notes=[
        ("visited = {}",
         "`visited` will map each **original node → its copy**. It makes sure every node is copied exactly once."),
        ("if original_node in visited", dict(
            yes="Node {original_node.val} has **already been copied**. Return that existing copy — do not create a "
                "second one, and do not walk around the cycle again.",
            marks={"clone.alt": "original_node.val"})),
        ("visited[original_node] = new_node",
         "First visit of node {original_node.val}: create its copy (no links yet) and register it in `visited` "
         "**right away**, before looking at any neighbour."),
        ("new_neighbor = dfs(neighbor)", dict(
            pre="Node {original_node.val} is linked to node {neighbor.val}. Ask for the **copy** of node {neighbor.val}.",
            marks={"original.alt": "neighbor.val", "original_edges.cur": "(original_node.val, neighbor.val)"})),
        ("new_node.neighbors.append(new_neighbor)",
         "Link the copies: copy {new_node.val} → copy {new_neighbor.val}, mirroring the original edge.",
         {"clone.alt": "new_neighbor.val", "clone_edges.good": "(new_node.val, new_neighbor.val)"}),
        ("return new_node", "Every neighbour of node {original_node.val} is linked. Its copy is complete — return it."),
        ("return dfs(node)", "The copy of the start node is returned. The whole graph hangs on it."),
    ],
    time=("O(V + E)", "Every node is copied once and every edge is followed once from each side."),
    space=("O(V)", "The map holds one entry per node, and the recursion can be V deep."),
    tests=[
        ("node=G([[]])", [[]]),
        ("node=G([])", []),
        ("node=G([[2], [1]])", [[2], [1]]),
        ("node=G([[2, 3], [1, 3], [1, 2]])", [[2, 3], [1, 3], [1, 2]]),
    ],
)

lesson(
    "max-area-of-island",
    pattern="Grid flood-fill (DFS) that returns a size",
    statement="""You are given a grid of `1` (land) and `0` (water). An island is a group of land
    cells connected horizontally or vertically. Return the **area** (number of cells) of the largest
    island, or 0 if there is no land.""",
    args="grid=[[1, 1, 0, 0, 0], [1, 0, 0, 1, 1], [0, 0, 1, 1, 0], [1, 0, 0, 0, 0]]",
    expected=4,
    why="The islands have 3, 4 and 1 cells; the largest covers 4.",
    idea=[
        "Scan the grid. Each time unvisited land is found, flood-fill that island — exactly as in Number of Islands.",
        "This time the flood-fill **returns how many cells it visited**: 1 for the cell itself plus whatever its four neighbours report.",
        "Sinking each visited cell to `0` guarantees no cell is counted twice. Keep the largest area seen.",
    ],
    views=[
        Grid("grid", vals={"1": LAND, "0": WATER}, changed="seen", tones={"cur": "(row, col)"}),
        Calls("dfs", "dfs({row}, {col})"),
        Vars("max_area"),
    ],
    notes=[
        ("max_area = 0", "Green is land, dark blue is water. `max_area` remembers the largest island measured so far."),
        ("if grid[row][col] == 1", dict(
            yes="The scan reaches ({row}, {col}): unvisited land — a **new island**. Flood-fill it and count its cells.")),
        ("if (", dict(
            yes="({row}, {col}) is {'off the grid' if not (0 <= row < len(grid) and 0 <= col < len(grid[0])) else 'water or already counted'}"
                " — it adds **0** cells.",
            first=2)),
        ("area = 1", dict(post=[
            ("max_area == 0 and _depth == 2",
             "Visit ({row}, {col}): sink it to `0` so it is never counted again, and count it — `area` = 1. "
             "Now add whatever its four neighbours (down, up, right, left) report."),
            (None, "Visit ({row}, {col}): sink it and count it — `area` = 1. Then ask its four neighbours."),
        ])),
        ("return area", "({row}, {col}) plus everything reached through it: **{plural(area, 'cell')}**. Report that upward."),
        ("max_area = max(max_area, dfs(row, col))", dict(post=[
            ("max_area > was.max_area",
             "That island has {max_area} cells — more than the best so far ({was.max_area}). `max_area` = **{max_area}**."),
            (None, "That island is not larger than the best so far, so `max_area` stays {max_area}."),
        ])),
        ("return max_area", "Every cell has been scanned. The largest island covers **{max_area}** cells."),
    ],
    time=("O(rows × cols)", "Each cell is scanned once and each land cell is sunk exactly once."),
    space=("O(rows × cols)", "In the worst case (all land) the recursion is as deep as the number of cells."),
    tests=[
        ("grid=[[0, 0, 0, 0]]", 0),
        ("grid=[[1]]", 1),
        ("grid=[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],"
         "[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],"
         "[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]", 6),
    ],
)

PACIFIC = "#4c8dff"
ATLANTIC = "#ff9f45"

lesson(
    "pacific-atlantic-water-flow",
    pattern="Reverse DFS from both oceans",
    statement="""`heights[r][c]` is the height of each cell of an island. The **Pacific** touches the
    top and left edges, the **Atlantic** the bottom and right edges. Rain water flows from a cell
    to a neighbour that is **equal or lower**. Return all cells from which water can reach
    **both** oceans.""",
    args="heights=[[4, 2, 3], [1, 5, 2], [3, 1, 1]]",
    expected=[[0, 2], [1, 1], [2, 0]],
    unordered=1,
    why="The two corners touch both oceans directly, and the peak (5) drains up or left into the Pacific and down or right into the Atlantic.",
    idea=[
        "Testing every cell with its own search (*can I flow down to each ocean?*) repeats a huge amount of work.",
        "Turn it around: start **at the ocean** and walk **uphill** (to neighbours that are equal or higher). Every cell reached this way can send water back down the same path into that ocean.",
        "Do this once from all Pacific border cells and once from all Atlantic border cells. The answer is the cells reached by **both** walks.",
    ],
    views=[
        Grid("heights",
             title="heights  (blue = reaches Pacific, orange = reaches Atlantic, green = both)",
             tones={PACIFIC: "pacific_reachable - atlantic_reachable",
                    ATLANTIC: "atlantic_reachable - pacific_reachable",
                    "good": "pacific_reachable & atlantic_reachable",
                    "cur": "(r, c) if _depth > 1 else None"}),
        Calls("dfs", "dfs({r}, {c})  {'Pacific' if reachable is pacific_reachable else 'Atlantic'}"),
    ],
    notes=[
        ("atlantic_reachable = set()",
         "Two sets: the cells that can drain into the Pacific, and the cells that can drain into the Atlantic. "
         "We fill them by walking **uphill from each ocean**."),
        ("reachable.add((r, c))", [
            ("_depth == 2 and (r, c) in was.reachable",
             "Border cell ({r}, {c}) is already marked for the {'Pacific' if reachable is pacific_reachable else 'Atlantic'}. "
             "Check its neighbours anyway."),
            ("_depth == 2",
             "({r}, {c}) lies on the **{'Pacific' if reachable is pacific_reachable else 'Atlantic'}** edge, so its water "
             "runs straight into that ocean. Mark it, then try to climb to each neighbour that is at least as high ({heights[r][c]})."),
            (None,
             "({r}, {c}) has height {heights[r][c]} — **not lower** than the cell we climbed from, so its water can flow "
             "back down that way into the {'Pacific' if reachable is pacific_reachable else 'Atlantic'}. Mark it and keep climbing."),
        ]),
        ("return list(pacific_reachable & atlantic_reachable)",
         "Both walks are finished. The green cells were reached from **both** oceans: {sorted(_ret)}."),
    ],
    result="sorted(_ret)",
    time=("O(rows × cols)", "Each cell is visited at most once per ocean."),
    space=("O(rows × cols)", "Two sets of cells plus the recursion stack."),
    tests=[
        ("heights=[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]",
         [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]),
        ("heights=[[1]]", [[0, 0]]),
        ("heights=[[2, 1], [1, 2]]", [[0, 0], [0, 1], [1, 0], [1, 1]]),
    ],
)

lesson(
    "surrounded-regions",
    pattern="Flood-fill from the border, then flip the rest",
    statement="""Given a board of `X` and `O`, **capture** every region of `O`s that is completely
    surrounded by `X` (on all four sides) by flipping those `O`s to `X`. A region that touches the
    border of the board can not be captured. Modify the board in place.""",
    args='board=[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]',
    result="board",
    expected=[["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]],
    why="The three O's in the middle are enclosed and get flipped. The O in the bottom row touches the border, so it survives.",
    idea=[
        "Deciding directly whether a region is surrounded is awkward. The opposite is easy: an `O` is **safe** exactly when it is connected to an `O` on the border.",
        "So start a flood-fill from every border `O` and mark everything it reaches with a temporary letter `E` (*escaped*).",
        "Afterwards every `O` that is still an `O` was never reached from the border — flip it to `X`. Turn the `E` marks back into `O`.",
    ],
    views=[
        Grid("board", vals={"O": "mark", "E": "good", "X": "dim"}, tones={"cur": "(row, col)"},
             title="board  (orange = O, green = safe, connected to the border)"),
        Calls("dfs", "dfs({row}, {col})"),
    ],
    notes=[
        ('if board[row][0] == "O"', dict(
            yes="Left border: ({row}, 0) is an `O`. It touches the edge, so it — and every `O` connected to it — can never be captured. Mark them safe.")),
        ('if board[row][len(board[0]) - 1] == "O"', dict(
            yes="Right border: ({row}, {len(board[0]) - 1}) is an `O`. Mark it and everything connected to it as safe.")),
        ('if board[0][col] == "O"', dict(
            yes="Top border: (0, {col}) is an `O`. Mark it and everything connected to it as safe.")),
        ('if board[len(board) - 1][col] == "O"', dict(
            yes="Bottom border: ({len(board) - 1}, {col}) is an `O`. It touches the edge, so it — and every `O` "
                "connected to it — can never be captured. Mark them safe.")),
        ("if (", dict(
            yes="({row}, {col}) is {'off the board' if not (0 <= row < len(board) and 0 <= col < len(board[0])) else 'not an unmarked O'}"
                " — nothing to do.",
            first=2)),
        ('board[row][col] = "E"',
         "({row}, {col}) is connected to the border: mark it `E` (escaped). Then look at its four neighbours."),
        ("for row in range(len(board)):@2",
         dict(pre="The border has been handled. Final pass over every cell: an `O` that is **still** `O` was never "
                  "reached from the border, so it is surrounded.", first=1)),
        ('board[row][col] = "X"',
         "({row}, {col}) is still `O` → surrounded on all sides. **Capture** it: flip to `X`.",
         {"board.bad": "(row, col)"}),
        ('board[row][col] = "O"',
         "({row}, {col}) carries the safe mark `E`: turn it back into `O`.",
         {"board.good": "(row, col)"}),
    ],
    allow_unused=True,
    outro="Done. The enclosed region was captured and the `O` on the border survived. The board was changed in place, so nothing is returned.",
    time=("O(rows × cols)", "Each cell is visited a constant number of times."),
    space=("O(rows × cols)", "Recursion depth in the worst case (a board full of connected O's)."),
    tests=[
        ('board=[["X"]]', [["X"]]),
        ('board=[["O","O"],["O","O"]]', [["O", "O"], ["O", "O"]]),
        ('board=[["X","X","X"],["X","O","X"],["X","X","X"]]', [["X", "X", "X"], ["X", "X", "X"], ["X", "X", "X"]]),
        ('board=[["X","O","X","X"],["X","O","O","X"],["X","X","X","X"],["X","O","O","X"],["X","X","X","X"]]',
         [["X", "O", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"]]),
    ],
)

FRESH = "#f2a33c"
ROTTEN = "#8a5a44"

lesson(
    "rotting-oranges",
    pattern="Multi-source BFS, one level per minute",
    statement="""In a grid, `0` is an empty cell, `1` a fresh orange and `2` a rotten orange. Every
    minute, each fresh orange that is next to (up, down, left, right) a rotten one becomes rotten.
    Return the number of minutes until no fresh orange is left, or `-1` if that never happens.""",
    args="grid=[[2, 1, 1], [1, 1, 0], [0, 1, 1]]",
    expected=4,
    why="The rot spreads one step per minute; the orange in the bottom-right corner is 4 steps away from the rotten one.",
    idea=[
        "Rot spreads outward from **all** rotten oranges at the same time, one step per minute. That is exactly a breadth-first search with several starting points.",
        "Put every rotten orange in a queue. Process the queue **one whole level at a time**: everything in the queue at the start of a round rots its fresh neighbours during the same minute.",
        "Count the rounds in which something new rotted. At the end, any fresh orange still left was unreachable → `-1`.",
    ],
    views=[
        Grid("grid", vals={"1": FRESH, "2": ROTTEN}, blank=["0"],
             title="grid  (orange = fresh, brown = rotten)",
             tones={"mark": "list(rotten)", "cur": "(row, col) if 'level_size' in dir() else None"}),
        Queue("rotten", title="rotten  (queue: will spread next)"),
        Vars("minutes", "fresh_count"),
    ],
    notes=[
        ("rotten.append((row, col))",
         "({row}, {col}) is rotten from the start. Put it in the queue — the rot spreads from here."),
        ("minutes = 0",
         "The scan is done: **{fresh_count} fresh** oranges, and the queue holds the rotten ones. `minutes` counts the time that passes."),
        ("level_size = len(rotten)",
         "**A new round (one minute).** The queue holds {plural(level_size, 'rotten orange')} right now. Whatever they "
         "infect rots during this same minute, so process exactly {level_size} queue {'entry' if level_size == 1 else 'entries'}."),
        ("row, col = rotten.popleft()",
         "Take the rotten orange at ({row}, {col}) and look at its four neighbours."),
        ("rotten.append((new_row, new_col))", [
            ("minutes == 0 and len(rotten) == 1",
             "({new_row}, {new_col}) is fresh and touches the rot → it **rots**. Fresh oranges left: {fresh_count}. "
             "It joins the queue and will infect its own neighbours in the **next** minute."),
            (None, "({new_row}, {new_col}) is fresh and touches the rot → it **rots** and joins the queue. Fresh oranges left: {fresh_count}."),
        ], {"grid.bad": "(new_row, new_col)"}),
        ("if rotten", dict(
            no="Nothing new rotted in this round — the spreading has stopped, so no extra minute is counted.")),
        ("minutes += 1", "New oranges rotted during this round, so one minute has passed: `minutes` = **{minutes}**."),
        ("return minutes if fresh_count == 0 else -1", [
            ("fresh_count == 0", "No fresh orange is left, so the answer is the elapsed time: **{minutes}** minutes."),
            (None, "{fresh_count} fresh orange(s) could never be reached by the rot → **-1**."),
        ]),
    ],
    time=("O(rows × cols)", "Each cell enters the queue at most once."),
    space=("O(rows × cols)", "The queue can hold a large part of the grid."),
    tests=[
        ("grid=[[2, 1, 1], [0, 1, 1], [1, 0, 1]]", -1),
        ("grid=[[0, 2]]", 0),
        ("grid=[[1]]", -1),
        ("grid=[[2, 2], [1, 1], [0, 0], [2, 0]]", 1),
    ],
)

lesson(
    "walls-and-gates",
    pattern="Multi-source BFS from every gate",
    statement="""A grid `rooms` contains `-1` (a wall), `0` (a gate) and `2147483647` (INF, an empty
    room). Fill each empty room with the number of steps to its **nearest gate**. Rooms that cannot
    reach a gate stay INF. Modify the grid in place.""",
    code="""
    class Solution:
        def wallsAndGates(self, rooms: List[List[int]]) -> None:
            INF = 2147483647
            rows, cols = len(rooms), len(rooms[0])
            queue = deque()

            for r in range(rows):
                for c in range(cols):
                    if rooms[r][c] == 0:
                        queue.append((r, c))  # every gate is a starting point

            while queue:
                row, col = queue.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                        rooms[nr][nc] = rooms[row][col] + 1
                        queue.append((nr, nc))
    """,
    args="rooms=[[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1], "
         "[2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]]",
    show_input="rooms = [[INF,-1,0,INF],[INF,INF,INF,-1],[INF,-1,INF,-1],[0,-1,INF,INF]]",
    result="rooms",
    expected=[[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]],
    why="Every room now holds its distance to the closer of the two gates.",
    idea=[
        "Running a separate search from every room (or from every gate) repeats work. Instead start a **single BFS from all gates at once**.",
        "BFS moves outward in rings: first all rooms 1 step from *some* gate, then all rooms 2 steps away, and so on.",
        "So the **first** time the search reaches a room, it has arrived from the nearest gate by a shortest route. Write the distance there; a room that already has a number is never touched again.",
    ],
    views=[
        Grid("rooms", text=lambda v: "∞" if v == 2147483647 else str(v),
             vals={"-1": "dim", "0": "good"}, changed="seen",
             title="rooms  (∞ = empty room, -1 = wall, 0 = gate)",
             tones={"mark": "list(queue)", "cur": "(row, col)"}),
        Queue("queue", title="queue  (cells whose neighbours still need a look)"),
    ],
    notes=[
        ("queue.append((r, c))", "({r}, {c}) is a **gate** (0). Every gate is a starting point of the search, so it goes into the queue."),
        ("row, col = queue.popleft()", [
            ("rooms[row][col] == 0", "Take the gate at ({row}, {col}) from the queue and look at its four neighbours."),
            (None, "Take ({row}, {col}), which is {plural(rooms[row][col], 'step')} from a gate, and look at its four neighbours."),
        ]),
        ("rooms[nr][nc] = rooms[row][col] + 1", [
            ("rooms[row][col] == 0 and len(queue) <= 1",
             "({nr}, {nc}) is an empty room (∞) that the search has not reached before, so this is the **shortest** way "
             "to it: {rooms[row][col]} + 1 = **{rooms[nr][nc]}**. Write the distance and queue the room."),
            (None, "({nr}, {nc}) is still ∞ — reached for the first time, so its distance is {rooms[row][col]} + 1 = **{rooms[nr][nc]}**."),
        ]),
        ("while queue", dict(no="The queue is empty: every reachable room has received its distance.")),
    ],
    outro="Done. Each room holds the distance to its nearest gate. The grid was changed in place, so nothing is returned.",
    time=("O(rows × cols)", "Every cell enters the queue at most once."),
    space=("O(rows × cols)", "The queue can hold a large part of the grid."),
    tests=[
        ("rooms=[[-1]]", [[-1]]),
        ("rooms=[[2147483647]]", [[2147483647]]),
        ("rooms=[[0, 2147483647, -1, 2147483647]]", [[0, 1, -1, 2147483647]]),
        ("rooms=[[0, 2147483647, 2147483647, 0]]", [[0, 1, 1, 0]]),
    ],
)

lesson(
    "course-schedule-ii",
    pattern="Topological sort (Kahn's algorithm)",
    statement="""There are `numCourses` courses labelled `0 … numCourses − 1`. A pair `[a, b]` in
    `prerequisites` means course `b` must be taken **before** course `a`. Return an order in which
    all courses can be taken, or an empty list if that is impossible.""",
    args="numCourses=4, prerequisites=[[1, 0], [2, 0], [3, 1], [3, 2]]",
    expected=[0, 1, 2, 3],
    why="Course 0 unlocks 1 and 2, and both of them are needed for 3. ([0, 2, 1, 3] would be accepted as well.)",
    idea=[
        "Draw each rule as an arrow `prerequisite → course`. A valid order lists every course after all the courses pointing at it — a **topological order**.",
        "A course whose in-degree (number of unmet prerequisites) is 0 can be taken now. Take it, append it to the order, and remove its outgoing arrows — that may free other courses.",
        "If the order ends up containing every course, return it. If some courses are left over they sit on a **cycle**, so no order exists → `[]`.",
    ],
    views=[
        Graph("range(numCourses)", adj="graph", directed=True,
              pos={0: (0, 1.7), 1: (-1.9, 0), 2: (1.9, 0), 3: (0, -1.7)},
              title="arrow = “must be taken before”",
              tones={"mark": "list(queue)", "good": "order", "cur": "node"}),
        Arr("in_degree", title="in_degree  (prerequisites still missing)", tones={"good": "order"}),
        Queue("queue", title="queue  (ready to take)"),
        Items("order", title="order  (the answer being built)"),
    ],
    notes=[
        ("order = []", "`order` will collect the courses in the sequence we take them."),
        ("in_degree[course] += 1",
         "Course {prereq} must come before course {course}: add the arrow {prereq} → {course}. "
         "Course {course} now waits for {plural(in_degree[course], 'prerequisite')}.",
         {"in_degree.cur": "course", "graph.cur": "course", "graph.alt": "prereq", "graph_edges.cur": "(prereq, course)"}),
        ("queue = collections.deque(",
         "Courses with in-degree 0 need nothing first. Put them in the queue: {list(queue)}."),
        ("order.append(node)",
         "**Take course {node}** — nothing blocks it. Append it to the order → {order}.",
         {"order.good": "-1"}),
        ("in_degree[neighbor] -= 1",
         "Course {neighbor} was waiting for course {node}. One prerequisite fewer: its in-degree drops to {in_degree[neighbor]}.",
         {"in_degree.cur": "neighbor", "graph.alt": "neighbor", "graph_edges.cur": "(node, neighbor)"}),
        ("queue.append(neighbor)",
         "Course {neighbor} has **no prerequisites left**. It is ready: add it to the queue."),
        ("return order if len(order) == numCourses else []", [
            ("len(order) == numCourses", "All {numCourses} courses were taken, so `order` is a valid schedule: **{order}**."),
            (None, "Only {len(order)} of {numCourses} courses could be taken — the rest are stuck on a cycle → **[]**."),
        ]),
    ],
    time=("O(V + E)", "Every course is queued once and every prerequisite arrow is followed once."),
    space=("O(V + E)", "The adjacency list stores all arrows; in-degrees, queue and order store up to V courses."),
    tests=[
        ("numCourses=2, prerequisites=[[1, 0]]", [0, 1]),
        ("numCourses=2, prerequisites=[[1, 0], [0, 1]]", []),
        ("numCourses=1, prerequisites=[]", [0]),
        ("numCourses=3, prerequisites=[[0, 1], [1, 2], [2, 0]]", []),
    ],
)

lesson(
    "redundant-connection",
    pattern="Union-Find (disjoint sets)",
    statement="""A tree with `n` nodes (labelled `1 … n`) had **one extra edge** added to it. You are
    given all `n` edges. Return the edge that can be removed so that the rest is a tree again; if
    there are several candidates, return the one that appears **last** in the input.""",
    pre="""
    def _root(parent, x):
        while parent[x] != x:
            x = parent[x]
        return x
    """,
    args="edges=[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]",
    expected=[1, 4],
    why="1–2, 2–3 and 3–4 already connect node 1 with node 4, so the edge 1–4 closes a cycle.",
    idea=[
        "Add the edges one at a time and keep track of which nodes are **already connected** to each other (which *group* each node is in).",
        "An edge between two nodes of **different** groups is useful: it merges the groups. An edge between two nodes of the **same** group adds a second route between them — a cycle. That is the redundant edge.",
        "Union-Find stores the groups cheaply: every node points to a parent, and following parents leads to the group's **root**. Same root ⇔ same group. `union` simply makes one root point at the other.",
    ],
    init={"drawn": "[]"},
    views=[
        Graph("range(1, n + 1)", edges="drawn", title="edges added so far",
              tones={"cur": "[u, v]"}),
        Arr("parent", title="parent[x]  (follow parents to reach the root of x's group)",
            tones={"dim": "0", "good": "[x for x in range(1, n + 1) if parent[x] == x]"}),
    ],
    notes=[
        ("parent = list(range(n + 1))",
         "Every node starts alone in its own group: `parent[x] = x`. A node that is its own parent is a **root** "
         "(green) and names its group. Index 0 is unused because nodes are numbered from 1."),
        ("u, v = edge", dict(
            post="Next edge: **{u} – {v}**. Are {u} and {v} already connected through earlier edges?",
            save={"drawn": "drawn + [(u, v)]"},
            marks={"graph_edges.cur": "(u, v)"})),
        ("parent[x] = find(parent[x])", dict(
            post="**Path compression**: while looking up the root of node {x}, point it straight at the root "
                 "({parent[x]}), so the next lookup is one step.",
            marks={"parent.cur": "x"}, when="was.parent[x] != parent[x]", first=3)),
        ("if find(u) == find(v)", dict(
            yes="Node {u} and node {v} have the **same root** ({_root(parent, u)}): they are already connected. "
                "This edge would create a second route between them — a **cycle**.",
            no="Roots differ: node {u} belongs to group {_root(parent, u)}, node {v} to group {_root(parent, v)}. "
               "The edge joins two separate groups, so it is needed.",
            marks={"parent.alt": "[_root(parent, u), _root(parent, v)]"},
            yes_marks={"graph_edges.bad": "(u, v)"})),
        ("union(u, v)", dict(
            post="**Union**: the root of {u}'s group now points to the root of {v}'s group ({_root(parent, v)}). "
                 "Both groups have become one.",
            marks={"graph_edges.good": "(u, v)", "parent.cur": "_root(parent, v)"})),
        ("return edge", "Return the edge that closed the cycle: **{edge}**.", {"graph_edges.bad": "(u, v)"}),
    ],
    allow_unused=True,
    time=("O(n log n)", "One find/union pair per edge. With path compression alone each one costs O(log n) amortised — "
                        "in practice almost constant. (Adding union by rank brings the total down to O(n · α(n)).)"),
    space=("O(n)", "The parent array."),
    tests=[
        ("edges=[[1, 2], [1, 3], [2, 3]]", [2, 3]),
        ("edges=[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]", [1, 4]),
        ("edges=[[1, 2], [2, 3], [1, 3], [3, 4]]", [1, 3]),
    ],
)

lesson(
    "number-of-connected-components-in-an-undirected-graph",
    pattern="DFS from every unvisited node",
    statement="""There are `n` nodes labelled `0 … n − 1` and a list of undirected `edges`. Return
    the number of **connected components** (groups of nodes that are linked to each other,
    directly or through other nodes).""",
    args="n=5, edges=[[0, 1], [1, 2], [3, 4]]",
    expected=2,
    why="Nodes 0, 1, 2 form one group and nodes 3, 4 another.",
    idea=[
        "Build an adjacency list so that every node knows its neighbours.",
        "Go through the nodes in order. A node that has **not been visited** yet belongs to a component nobody has seen — count one more.",
        "Then run a DFS from it to mark its **whole** component as visited, so none of its nodes is counted again.",
    ],
    views=[
        Graph("range(n)", adj="graph", tones={"seen": "visited", "cur": "node"},
              pos={0: (-2.6, 0.9), 1: (-1.3, -0.9), 2: (0, 0.9), 3: (1.6, -0.9), 4: (2.9, 0.9)}),
        Calls("dfs", "dfs({node})"),
        Vars("components"),
    ],
    notes=[
        ("graph[v].append(u)",
         "Edge {u} – {v} is undirected: {u} gets {v} as a neighbour **and** {v} gets {u}.",
         {"graph.alt": "[u, v]", "graph_edges.cur": "(u, v)"}),
        ("components = 0", "No node has been visited and no component counted yet."),
        ("if node not in visited", dict(
            yes="Node {node} has not been visited: it belongs to a component we have not seen before.",
            no="Node {node} was already visited — it is part of a component that has been counted. Skip it.")),
        ("components += 1", "Count it: `components` = **{components}**. Now visit everything reachable from node {node}."),
        ("visited.add(node)", "Visit node {node} and mark it (blue)."),
        ("if neighbor not in visited", dict(
            yes="Node {node}'s neighbour {neighbor} is unvisited — it is in the same component. Go there.",
            no="Node {node}'s neighbour {neighbor} is already visited.",
            marks={"graph_edges.cur": "(node, neighbor)"})),
        ("return components", "Every node has been checked. A DFS was started {components} times → **{components} components**."),
    ],
    time=("O(V + E)", "Every node is visited once and every edge is looked at from both ends."),
    space=("O(V + E)", "The adjacency list, the visited set and the recursion stack."),
    tests=[
        ("n=5, edges=[[0, 1], [1, 2], [2, 3], [3, 4]]", 1),
        ("n=4, edges=[]", 4),
        ("n=1, edges=[]", 1),
        ("n=6, edges=[[0, 1], [2, 3], [4, 5], [1, 2]]", 2),
    ],
)

lesson(
    "graph-valid-tree",
    pattern="Tree = connected + exactly n − 1 edges",
    statement="""There are `n` nodes labelled `0 … n − 1` and a list of undirected `edges`. Return
    `True` if these edges form a valid **tree**: all nodes connected, and no cycle.""",
    args="n=5, edges=[[0, 1], [0, 2], [0, 3], [1, 4]]",
    expected=True,
    why="4 edges for 5 nodes, every node can be reached from node 0, and there is no cycle.",
    idea=[
        "A tree on `n` nodes always has **exactly n − 1 edges**. Any other count can be rejected immediately.",
        "With the right number of edges, walk the graph by DFS from node 0. Seeing an already-visited node (other than the one we just came from) means there is a **cycle**.",
        "Finally the walk must have reached **all n nodes** — otherwise the graph is in several pieces.",
    ],
    views=[
        Graph("range(n)", adj="graph", tones={"seen": "visited", "cur": "node"},
              pos={0: (0, 1.6), 1: (-2, 0), 2: (0, 0), 3: (2, 0), 4: (-2, -1.6)}),
        Calls("dfs", "dfs(node {node}, came from {parent})"),
    ],
    notes=[
        ("if len(edges) != n - 1", dict(
            yes="A tree with {n} nodes needs exactly {n - 1} edges, but there are {len(edges)} → **False**.",
            no="{len(edges)} edges for {n} nodes — exactly n − 1, as a tree requires. Now check that it is one connected piece without a cycle.")),
        ("graph[v].append(u)",
         "Edge {u} – {v}: each end records the other as a neighbour.",
         {"graph.alt": "[u, v]", "graph_edges.cur": "(u, v)"}),
        ("visited.add(node)", [
            ("parent == -1", "Start at node 0 (it has no parent, written as −1). Mark it visited."),
            (None, "Arrive at node {node} from node {parent}. Mark it visited."),
        ]),
        ("if neighbor != parent", dict(
            no="Node {node}'s neighbour {neighbor} is the node we just came from. That is the same edge seen from the other end, not a cycle — ignore it.",
            first=2)),
        ("if neighbor in visited or not dfs(neighbor, node)", dict(
            pre=[
                ("neighbor in visited", "Node {node}'s neighbour {neighbor} is **already visited** and is not where we came from: a second route to it exists — a cycle."),
                (None, "Node {node}'s neighbour {neighbor} is new. Explore it."),
            ],
            marks={"graph_edges.cur": "(node, neighbor)"})),
        ("return False@2", "A cycle was found → **False**."),
        ("return len(visited) == n", [
            ("len(visited) == n", "No cycle, and the walk visited all {n} nodes: one connected piece → **True**."),
            (None, "The walk reached only {len(visited)} of {n} nodes: the graph is not connected → **False**."),
        ]),
    ],
    allow_unused=True,
    time=("O(V + E)", "Every node and edge is handled a constant number of times."),
    space=("O(V + E)", "Adjacency list, visited set and recursion stack."),
    tests=[
        ("n=5, edges=[[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]", False),
        ("n=4, edges=[[0, 1], [2, 3]]", False),
        ("n=1, edges=[]", True),
        ("n=4, edges=[[0, 1], [2, 3], [1, 2]]", True),
        ("n=5, edges=[[0, 1], [1, 2], [2, 0], [3, 4]]", False),
    ],
)

lesson(
    "word-ladder",
    pattern="BFS over words that differ by one letter",
    statement="""A *ladder* from `beginWord` to `endWord` changes **one letter at a time**, and every
    intermediate word must be in `wordList`. Return the number of words in the **shortest** ladder
    (counting both ends), or 0 if no ladder exists.""",
    pre="""
    def _links(words):
        out = []
        for i, a in enumerate(words):
            for b in words[i + 1:]:
                if len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1:
                    out.append((a, b))
        return out
    """,
    args='beginWord="hit", endWord="cog", wordList=["hot", "dot", "dog", "lot", "log", "cog"]',
    expected=5,
    why="hit → hot → dot → dog → cog is a shortest ladder: 5 words.",
    idea=[
        "Picture every word as a node, with a line between two words that differ in exactly one letter. A ladder is a **path** in this graph.",
        "The shortest path in an unweighted graph is found by **BFS**: it visits all words 1 step away, then all words 2 steps away, and so on — so the first time `endWord` comes out of the queue, the ladder is as short as possible.",
        "To find a word's neighbours, replace each of its letters by `a … z` and keep the results that are in the word list and not visited yet.",
    ],
    init={"lvl": "{beginWord: 1}"},
    views=[
        Graph("[beginWord] + [w for w in wordList if w != beginWord]",
              edges="_links([beginWord] + [w for w in wordList if w != beginWord])",
              title="words  (a line joins words that differ by one letter; the number is the ladder length)",
              pos={"hit": (-4.5, 0), "hot": (-2.25, 0), "dot": (0, 1.3), "lot": (0, -1.3),
                   "dog": (2.25, 1.3), "log": (2.25, -1.3), "cog": (4.5, 0)},
              badges="lvl",
              tones={"seen": "list(visited) + [beginWord]", "mark": "[w for w, _ in queue]", "cur": "word"}),
        Queue("queue", title="queue  (word, ladder length)"),
    ],
    notes=[
        ("wordSet = set(wordList)", "Put the word list into a set, so *is this a valid word?* takes O(1)."),
        ("if endWord not in wordSet", dict(
            yes="`{endWord}` is not in the word list, so no ladder can end there → **0**.",
            no="`{endWord}` is in the list, so a ladder might exist.")),
        ("queue = deque([(beginWord, 1)])",
         "Start the BFS at `{beginWord}`. The queue stores each word with the length of the ladder that reaches it; "
         "`{beginWord}` alone is a ladder of length 1."),
        ("word, level = queue.popleft()", [
            ("word == endWord", "Take `{word}` (ladder length {level}) from the queue."),
            (None, "Take `{word}` (ladder length {level}) from the queue and try every single-letter change of it."),
        ]),
        ("if word == endWord", dict(
            yes="`{word}` is the end word. BFS reaches words in order of distance, so this ladder is the **shortest**.")),
        ("queue.append((new_word, level + 1))", dict(
            post="Changing the letter at index {i} of `{word}` to `{c}` gives `{new_word}`: a valid word that has not been visited. "
                 "Mark it visited and queue it with ladder length {level + 1}.",
            save={"lvl": "{**lvl, new_word: level + 1}"},
            marks={"graph_edges.cur": "(word, new_word)", "graph.alt": "new_word"})),
        ("return level", "The shortest ladder contains **{level}** words."),
        ("return 0@2", "The queue ran empty without reaching `{endWord}` → **0**."),
    ],
    allow_unused=True,
    time=("O(N · L²)", "Each of the N words is expanded once: L positions × 26 letters, and building and looking up "
                       "each candidate word costs O(L)."),
    space=("O(N · L)", "The word set, the visited set and the queue."),
    tests=[
        ('beginWord="hit", endWord="cog", wordList=["hot", "dot", "dog", "lot", "log"]', 0),
        ('beginWord="a", endWord="c", wordList=["a", "b", "c"]', 2),
        ('beginWord="hot", endWord="dog", wordList=["hot", "dog"]', 0),
        ('beginWord="lost", endWord="cost", wordList=["most", "fist", "lost", "cost", "fish"]', 2),
    ],
)

# end of c11_graphs
