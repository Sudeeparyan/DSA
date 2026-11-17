"""Linked List."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "reverse-linked-list",
    pattern="Three pointers: prev / current / next",
    statement="""Given the `head` of a singly linked list, reverse the list and return the new
    head.""",
    args="head=L([1, 2, 3])",
    expected=[3, 2, 1],
    why="Every arrow now points the other way, so the old tail (3) is the new head.",
    picture="""Picture a conga line where everyone has a hand on the shoulder of the person in front. To
    reverse the line, walk along it and turn each person around, so that their hand points at the
    person who was behind them. Before you turn someone, note who was in front of them, or you would
    lose track of the rest of the line.""",
    idea=[
        "Each node only knows its `next`. Reversing the list means making every arrow point the other way.",
        "Walk the list once with three pointers: `prev` (head of the part already reversed), `current` (the node being flipped) and `next_node` (a saved copy of the way forward).",
        "For each node: **save** its next → **flip** its arrow back to `prev` → **slide** `prev` and `current` one step forward.",
    ],
    views=[
        LinkedList(ptrs=["prev", "current", "next_node"], tones={"good": "chain(prev)", "cur": "current"}),
    ],
    notes=[
        ("prev = None",
         "`prev` is the head of the part that is **already reversed**. Nothing is reversed yet, so it starts as None."),
        ("current = head", "`current` is the node we are about to flip. Start at the head, node {current.val}."),
        ("next_node = current.next",
         "We are about to overwrite `current.next`, so first **save** where it points: `next_node` = {nv(next_node)}. "
         "Without this we would lose the rest of the list."),
        ("current.next = prev",
         "**Flip the arrow**: node {current.val} now points back to {nv(prev)} instead of forward."),
        ("prev = current",
         "Node {current.val} is now the head of the reversed part, so move `prev` onto it."),
        ("current = next_node",
         "Step forward using the saved pointer: `current` = {nv(current)}."),
        ("while current", dict(
            no="`current` is None — we walked off the end, so every arrow has been flipped.")),
        ("return prev", "`prev` is on node {prev.val}, the new head. Return it."),
    ],
    say={
        "def reverseList": (
            "The function we must write. It gets the first node of the list (`head`) and returns "
            "the first node of the reversed list."
        ),
        "prev = None": (
            "`prev` is the node just behind the one we are fixing. Behind the first node there is"
            " nothing (`None`), and that is what the new last node will point to."
        ),
        "current = head": "`current` is the node we are fixing now. Start at the front.",
        "while current": (
            "Repeat until we have walked off the end of the list (`current` is `None`)."
        ),
        "next_node = current.next": (
            "Remember the node after `current` before its arrow changes, or the rest of the list "
            "would be lost."
        ),
        "current.next = prev": "Turn `current`'s arrow around: it now points back at `prev`.",
        "prev = current": "Move `prev` forward onto `current`.",
        "current = next_node": "Move `current` on to the node we remembered.",
        "return prev": "`prev` is on the old last node, which is now the first node: return it.",
    },
    time=("O(n)", "Each node is visited exactly once."),
    space=("O(1)", "Only three pointers are used, no matter how long the list is."),
    tests=[("head=L([1, 2])", [2, 1]), ("head=L([])", []), ("head=L([1, 2, 3, 4, 5])", [5, 4, 3, 2, 1])],
)

lesson(
    "merge-two-sorted-lists",
    pattern="Dummy head + two pointers",
    statement="""Given the heads of two **sorted** linked lists, merge them into one sorted list
    built from the same nodes, and return its head.""",
    args="l1=L([1, 4, 5]), l2=L([2, 3, 6])",
    expected=[1, 2, 3, 4, 5, 6],
    why="Repeatedly taking the smaller front node gives 1, 2, 3, 4, 5, 6.",
    picture="""Picture two sorted queues of people merging into one at a gate. At each step the gatekeeper
    compares the two people at the front and waves the smaller one through to the end of the new
    line. When one queue is empty, the rest of the other walks through just as it is, already in
    order. A placeholder (the *dummy*) stands at the very start of the new line, so there is always
    someone to join on behind.""",
    idea=[
        "Both lists are sorted, so the smallest node not yet used is always at the **front** of one of them.",
        "Compare the two fronts, link the smaller one onto the end of the merged list, and move that list's pointer forward.",
        "A **dummy** node at the start means the first real node needs no special case. When one list runs out, the rest of the other is already sorted — attach it in one go.",
    ],
    views=[
        LinkedList(ptrs=["l1", "l2", "current"], rows=["l1 · first list", "l2 · second list"],
                   place={"dummy": (0.5, -1)}, names={"dummy": "dummy"},
                   tones={"good": "span(dummy.next, current)", "cur": "current"}),
    ],
    final={"list.good": "chain(_ret)"},
    notes=[
        ("dummy = ListNode()",
         "Create a **dummy** node. The merged list is built after it, so even the first real node is just "
         "*attached to something*."),
        ("current = dummy", "`current` always marks the **last node of the merged list** so far."),
        ("current.next = l1@1",
         "{l1.val} < {l2.val}, so `l1`'s front node is the smaller one. Link it after `current`."),
        ("current.next = l2@1",
         "{l2.val} ≤ {l1.val}, so take `l2`'s front node. Link it after `current`."),
        ("current = current.next",
         "The list we took from has moved to its next node, and `current` steps onto node {current.val}, "
         "the new end of the merged list."),
        ("current.next = l2@2",
         "`l1` has run out. The rest of `l2` is already sorted, so attach all of it at once."),
        ("return dummy.next",
         "The merged list starts right after the dummy, at node {dummy.next.val}. Return it."),
    ],
    say={
        "def mergeTwoLists": (
            "The function we must write. It gets the first nodes of two sorted lists, `l1` and "
            "`l2`, and returns the first node of the merged list."
        ),
        "dummy = ListNode()": (
            "A placeholder node to start the new list from. It is not part of the answer; it just"
            " gives the first real node something to hang on."
        ),
        "current = dummy": "`current` is the last node of the merged list so far.",
        "while l1 and l2": "Repeat while both lists still have nodes.",
        "if l1.val < l2.val": "Which front node holds the smaller value (`.val`)?",
        "current.next = l1@1": "`l1`'s is smaller: hang that node on the end of the merged list.",
        "l1 = l1.next": "And move `l1` on to its next node.",
        "current.next = l2@1": (
            "Otherwise `l2`'s is smaller (or they are equal): hang that node on the end."
        ),
        "l2 = l2.next": "And move `l2` on to its next node.",
        "current = current.next": "The node just attached is now the end of the merged list.",
        "if l1:": "One list has run out. Does `l1` still have nodes?",
        "current.next = l1@2": "Then attach all of them at once: they are already in order.",
        "elif l2": "Otherwise, does `l2` still have nodes?",
        "current.next = l2@2": "Then attach all of them at once.",
        "return dummy.next": (
            "The merged list starts just after the placeholder: return that node."
        ),
    },
    time=("O(n + m)", "Each step links one node, and there are n + m nodes."),
    space=("O(1)", "The existing nodes are re-linked; only a dummy node is created."),
    tests=[("l1=L([1, 2, 4]), l2=L([1, 3, 4])", [1, 1, 2, 3, 4, 4]), ("l1=L([]), l2=L([])", []),
           ("l1=L([]), l2=L([0])", [0]), ("l1=L([5]), l2=L([1, 2])", [1, 2, 5])],
)

lesson(
    "reorder-list",
    pattern="Find middle → reverse second half → weave",
    statement="""Reorder a linked list `L0 → L1 → … → Ln` in place into
    `L0 → Ln → L1 → Ln−1 → L2 → …`: first node, last node, second node, second-to-last, and so on.
    Node values may not be changed — only the links.""",
    args="head=L([1, 2, 3, 4, 5])",
    expected=[1, 5, 2, 4, 3],
    result="head",
    why="Take alternately from the front and from the back: 1, 5, 2, 4, 3.",
    picture="""Picture a row of cards that you want to deal first, last, second, second-to-last, and so on. Do
    it in three moves. Find the middle: one finger moves two cards for every one card the other
    moves, so when the fast finger reaches the end, the slow one is halfway. Turn the back half
    around, so its last card comes first. Then weave the two halves together, one card from each in
    turn.""",
    idea=[
        "We need nodes from the back, but a singly linked list cannot be walked backwards.",
        "So split it in the middle and **reverse the second half**. Now the back nodes are available in exactly the order we need them.",
        "Three steps, each a classic: find the middle with slow/fast pointers, reverse the second half, then weave the two halves together one node at a time.",
    ],
    views=[
        LinkedList(ptrs={
            "slow": ("slow", "'p1' not in globals()"),
            "fast": ("fast", "'prev' not in globals()"),
            "prev": ("prev", "'p1' not in globals()"),
            "current": ("current", "'p1' not in globals()"),
            "p1": "p1",
            "p2": "p2",
        }),
    ],
    final={"list.good": "chain(head)"},
    notes=[
        ("slow, fast = head, head",
         "**Step 1 — find the middle.** `slow` moves one node at a time and `fast` moves two. When `fast` "
         "reaches the end, `slow` is in the middle."),
        ("fast = fast.next.next", "`slow` steps to node {slow.val}; `fast` jumps to node {fast.val}."),
        ("prev, current = None, slow.next",
         "`fast` cannot jump any further, so `slow` (node {slow.val}) is the middle. "
         "**Step 2 — reverse the second half**, which starts at node {current.val}."),
        ("slow.next = None", "Cut the list after the middle: the first half now ends at node {slow.val}."),
        ("current.next = prev",
         "Flip the arrow of node {current.val} so it points back at {nv(prev)}."),
        ("p1, p2 = head, prev",
         "The second half is reversed and now starts at node {p2.val}. **Step 3 — weave** the two halves, "
         "taking one node from each in turn."),
        ("p1.next = p2", "Link node {p1.val} → node {p2.val} (from the reversed half)."),
        ("p2.next = next_p1", "Then link node {p2.val} → {nv(next_p1)} (back into the first half)."),
        ("p1, p2 = next_p1, next_p2", "Move both pointers on: `p1` = {nv(p1)}, `p2` = {nv(p2)}."),
        ("while p2", dict(no="`p2` is None: the reversed half is used up, so the list is fully reordered.")),
    ],
    say={
        "def reorderList": (
            "The function we must write. It gets the first node and rearranges the list in place;"
            " it returns nothing."
        ),
        "if not head or not head.next or not head.next.next": (
            "With fewer than three nodes the order cannot change."
        ),
        "return": "So stop here.",
        "slow, fast = head, head": (
            "Two pointers at the front. `fast` will move two nodes for every one `slow` moves."
        ),
        "while fast.next and fast.next.next": "Repeat while `fast` can still take two steps.",
        "slow = slow.next": "`slow` moves one node.",
        "fast = fast.next.next": (
            "`fast` moves two. When it can go no further, `slow` is at the middle."
        ),
        "prev, current = None, slow.next": (
            "The second half starts right after the middle. Get ready to reverse it."
        ),
        "slow.next = None": "Cut the list in two: the first half now ends at the middle.",
        "while current": "Reverse the second half, one node at a time.",
        "next_node = current.next": "Remember the next node before its arrow changes.",
        "current.next = prev": "Turn this node's arrow around, to point back.",
        "prev = current": "Move `prev` forward.",
        "current = next_node": "Move `current` on to the remembered node.",
        "p1, p2 = head, prev": (
            "`p1` walks the first half from the front; `p2` walks the reversed second half, which"
            " now starts with the old last node."
        ),
        "while p2": "Repeat while the second half still has nodes to weave in.",
        "next_p1, next_p2 = p1.next, p2.next": "Remember where each half continues.",
        "p1.next = p2": "After `p1` comes `p2`, a node from the back half.",
        "p2.next = next_p1": "After that comes the next node of the front half.",
        "p1, p2 = next_p1, next_p2": "Move both pointers on to the next pair.",
    },
    time=("O(n)", "Each of the three steps is one pass over (part of) the list."),
    space=("O(1)", "Only a handful of pointers; the nodes are re-linked in place."),
    tests=[("head=L([1, 2, 3, 4])", [1, 4, 2, 3]), ("head=L([1])", [1]), ("head=L([1, 2])", [1, 2])],
)

lesson(
    "remove-nth-node-from-end-of-list",
    pattern="Two pointers a fixed distance apart",
    statement="""Given the head of a linked list, remove the `n`-th node **counted from the end**
    and return the head of the list.""",
    args="head=L([1, 2, 3, 4, 5]), n=2",
    expected=[1, 2, 3, 5],
    why="The 2nd node from the end is 4, so it is removed.",
    picture="""Picture two people walking along the list with exactly `n` nodes between them. When the one in
    front reaches the last node, the one behind is standing just before the node that must go, so it
    can step over it. A placeholder node in front of the head gives the one behind somewhere to
    stand even when the very first node is the one to remove.""",
    idea=[
        "We cannot walk backwards from the end, and we do not know the length without a first pass.",
        "Trick: use two pointers that stay **n nodes apart**. Move both forward together; when the front one reaches the last node, the back one is exactly before the node to delete.",
        "A dummy node in front of the head makes deleting the head itself work the same way as deleting any other node.",
    ],
    views=[
        LinkedList(ptrs=["slow", "fast"], place={"dummy": (0, -1)}, names={"dummy": "dummy"},
                   tones={"bad": "[x for x in nodes() if x not in chain(dummy)]"}),
    ],
    notes=[
        ("dummy.next = head",
         "Put a **dummy** node in front of the head. Even if the head is the one to delete, there is now a "
         "node before it to re-link."),
        ("fast = slow = dummy", "Both pointers start on the dummy."),
        ("fast = fast.next@1", "Give `fast` a head start: it moves to node {fast.val}."),
        ("slow = slow.next",
         "Move both one step: `fast` → node {fast.val}, `slow` → {'the dummy' if slow is dummy else 'node ' + str(slow.val)}. "
         "They stay {n} nodes apart."),
        ("while fast.next", dict(
            no="`fast` is on the last node. `slow` is {n} nodes behind it — standing **just before** the node "
               "to remove (node {slow.next.val}).")),
        ("slow.next = slow.next.next",
         "Skip over it: node {slow.val} now points straight to {nv(slow.next)}. The skipped node is out of the list."),
        ("return dummy.next", "Return the node after the dummy: the head of the updated list."),
    ],
    say={
        "def removeNthFromEnd": (
            "The function we must write. It gets the first node and `n`, and returns the first "
            "node after removing the `n`-th node from the end."
        ),
        "dummy = ListNode(0)": "A placeholder node to put in front of the list.",
        "dummy.next = head": "Point it at the real first node.",
        "fast = slow = dummy": "Both pointers start on the placeholder.",
        "for _ in range(n)": "Repeat `n` times. (`_` is the name for a counter we do not need.)",
        "fast = fast.next@1": (
            "Move `fast` one node ahead. After this loop it is `n` nodes ahead of `slow`."
        ),
        "while fast.next": "Repeat until `fast` is on the last node.",
        "fast = fast.next@2": "Move `fast` one node on.",
        "slow = slow.next": "Move `slow` one node on too, so the gap stays the same.",
        "slow.next = slow.next.next": (
            "`slow` is just before the node to remove. Skip over it: point `slow` at the node "
            "after it."
        ),
        "return dummy.next": "Return the node after the placeholder: the first node of the list.",
    },
    time=("O(n)", "One pass: `fast` walks the list once."),
    space=("O(1)", "Two pointers and one dummy node."),
    tests=[("head=L([1]), n=1", []), ("head=L([1, 2]), n=1", [1]), ("head=L([1, 2]), n=2", [2])],
)

lesson(
    "copy-list-with-random-pointer",
    pattern="Interleave copies with the originals",
    statement="""Every node of a linked list has a `next` pointer and also a `random` pointer that
    may point to **any** node in the list (or to nothing). Build a completely separate deep copy
    of the list and return its head.""",
    pre="Node = RandomListNode",
    args="head=LR([[7, None], [13, 0], [11, 1]])",
    show_input="head = 7 → 13 → 11, where 13.random = 7, 11.random = 13 and 7.random = None",
    result="[[x.val, x.random.val if x.random else None] for x in chain(_ret)]",
    expected=[[7, None], [13, 7], [11, 13]],
    show_output="a new list 7 → 13 → 11 with the same random links, sharing no nodes with the original",
    why="The copy has the same values and the same shape, but every pointer leads to a copied node.",
    outro="Done. The bottom row is a complete, independent copy: same values, same `next` order and the same "
          "random links, all pointing at copied nodes.",
    picture="""Picture copying a treasure hunt in which every clue also has a secret note pointing to some
    other clue. First, slip a blank copy in right after each original clue. Now every copy sits just
    behind its original, so a copy's secret note is easy to fill in: it points to the copy sitting
    just behind the original's target. Finally, pull the copies out into a line of their own and put
    the originals back as they were.""",
    idea=[
        "Copying `next` is easy. The hard part is `random`: when we copy a node, the copy of the node its random points to may not exist yet — and afterwards, how do we find it?",
        "Trick: put each copy **right after its original** (A → A′ → B → B′ …). Then the copy of any node `x` is simply `x.next`.",
        "So: (1) weave the copies in, (2) set each copy's random to `original.random.next`, (3) unweave the two lists again.",
    ],
    views=[
        LinkedList(ptrs=["current", "original"], rows=["original", "copy"], tones={"cur": "current"},
                   title="purple arcs are random pointers"),
    ],
    notes=[
        ("duplicate = Node(current.val)", "**Step 1.** Make a copy of node {current.val}."),
        ("current.next = duplicate",
         "Slip the copy in right **after** its original: {current.val} → copy of {current.val} → {nv(duplicate.next)}."),
        ("current = head@2",
         "Every original is now followed by its own copy. **Step 2 — random pointers.** The copy of any "
         "node `x` is simply `x.next`."),
        ("if current.random", dict(
            no="Node {current.val} has no random pointer, so its copy keeps None.")),
        ("current.next.random = current.random.next",
         "Node {current.val}'s random points to node {current.random.val}. So its copy's random must point to the "
         "**copy** of {current.random.val} — which is `current.random.next`."),
        ("duplicate_head = head.next",
         "**Step 3 — separate the two lists.** The copied list starts at the copy of the head."),
        ("original.next = original.next.next",
         "Restore the original: node {original.val} points past its copy again, to {nv(original.next)}."),
        ("current.next = current.next.next",
         "And the copy of {current.val} points past the next original, to the copy of {current.next.val}."),
        ("return duplicate_head",
         "The two lists share nothing any more. Return the head of the copy."),
    ],
    say={
        "def copyRandomList": (
            "The function we must write. It gets the first node and returns the first node of a "
            "complete copy."
        ),
        "if not head": "An empty list has nothing to copy.",
        "return None": "So return nothing (`None`).",
        "current = head@1": "Step 1: walk the original list from the front.",
        "while current@1": "Repeat for every original node.",
        "duplicate = Node(current.val)": "Make a new node with the same value.",
        "duplicate.next = current.next": (
            "Point the copy at the node that came after the original."
        ),
        "current.next = duplicate": (
            "Then point the original at its copy. The copy now sits right after its original."
        ),
        "current = duplicate.next": "Jump to the next original node, just past the copy.",
        "current = head@2": "Step 2: walk the combined list again, from the front.",
        "while current@2": "Repeat for every original node.",
        "if current.random": "Does this original have a random pointer?",
        "current.next.random = current.random.next": (
            "Its copy (`current.next`) must point to the *copy* of the random target, and that "
            "copy sits right after the target: `current.random.next`."
        ),
        "current = current.next.next": "Jump two nodes: past the copy, to the next original.",
        "original = head": (
            "Step 3: pull the two lists apart. `original` walks along the original nodes."
        ),
        "duplicate_head = head.next": (
            "The first copy sits right after the first original. It will be the head of the "
            "answer."
        ),
        "current = duplicate_head": "`current` walks along the copies.",
        "while original": "Repeat for every original node.",
        "original.next = original.next.next": (
            "Point the original past its copy, back to the next original."
        ),
        "if current.next": "Is there another copy after this one?",
        "current.next = current.next.next": (
            "Then point this copy past the next original, to the next copy."
        ),
        "original = original.next": "Move on to the next original.",
        "current = current.next@2": "Move on to the next copy.",
        "return duplicate_head": "Return the first node of the copy.",
    },
    time=("O(n)", "Three passes over the list."),
    space=("O(1)", "No hash map is needed — the weaving itself remembers which copy belongs to which node."),
    tests=[("head=LR([[1, 1], [2, 1]])", [[1, 2], [2, 2]]), ("head=LR([])", [])],
)

lesson(
    "add-two-numbers",
    pattern="Digit-by-digit addition with a carry",
    statement="""Two non-negative integers are stored as linked lists with their digits in
    **reverse order** (ones digit first). Add them and return the sum as a linked list in the
    same format.""",
    args="l1=L([5, 6]), l2=L([7, 8, 9])",
    expected=[2, 5, 0, 1],
    why="The lists mean 65 and 987. 65 + 987 = 1052, which is stored as 2 → 5 → 0 → 1.",
    picture="""Picture adding two long numbers on paper, column by column, starting with the ones. You write
    down the last digit of each column's sum and carry the 1, if there is one, into the next column.
    Here the digits are stored ones first, which is exactly the order you add them in, so you simply
    walk along both lists side by side.""",
    idea=[
        "The digits come lowest first — exactly the order in which we add by hand: ones, then tens, then hundreds.",
        "Walk both lists together. At each position add the two digits and the **carry** from the previous position. Write down `total % 10` and carry `total // 10`.",
        "If one list is shorter, treat its missing digits as 0. If a carry is left at the very end, it becomes one more digit.",
    ],
    views=[
        LinkedList(ptrs=["l1", "l2", "current"], rows=["l1 · first number", "l2 · second number", "the sum"], names={"dummy": "dummy"},
                   tones={"good": "chain(dummy.next)"}),
        Vars("val1", "val2", "carry", "total", "digit"),
    ],
    notes=[
        ("carry = 0",
         "The answer is built after a dummy node. `carry` holds what spills over into the next digit; it starts at 0."),
        ("total = val1 + val2 + carry",
         "This column: {val1} + {val2} + carry {carry} = **{total}**."
         "{'' if l1 and l2 else ' (A list that has run out counts as 0.)'}"),
        ("digit = total % 10",
         "Write down {total} % 10 = **{digit}**, and carry {total} // 10 = **{carry}** into the next column."),
        ("current = current.next", "Append a new node holding {current.val} to the answer."),
        ("current.next = ListNode(carry)",
         "Both lists are finished, but a carry of {carry} is still left. It becomes one more digit."),
        ("return dummy.next", "The sum starts right after the dummy. Return it."),
    ],
    say={
        "def addTwoNumbers": (
            "The function we must write. It gets two numbers stored as lists of digits (ones "
            "first) and returns their sum, stored the same way."
        ),
        "dummy = ListNode()": "A placeholder node to hang the answer's digits on.",
        "current = dummy": "`current` is the last digit written so far.",
        "carry = 0": "What carries into the next column. Nothing at first.",
        "while l1 or l2": "Repeat while either number still has digits.",
        "val1 = l1.val if l1 else 0": (
            "This column's digit from the first number, or 0 if it has run out."
        ),
        "val2 = l2.val if l2 else 0": "The same for the second number.",
        "total = val1 + val2 + carry": "Add the two digits and the carry.",
        "carry = total // 10": (
            "The tens part carries into the next column: `total // 10` is 1 when the total is 10 "
            "or more, and 0 otherwise."
        ),
        "digit = total % 10": (
            "The ones part is this column's digit: `total % 10` is the remainder after dividing "
            "by 10."
        ),
        "current.next = ListNode(digit)": (
            "Write that digit as a new node at the end of the answer."
        ),
        "current = current.next": "The new node is now the end of the answer.",
        "if l1": "Does the first number have more digits?",
        "l1 = l1.next": "Then move on to its next digit.",
        "if l2": "Does the second number have more digits?",
        "l2 = l2.next": "Then move on to its next digit.",
        "if carry": "Is there a carry left after the last column?",
        "current.next = ListNode(carry)": "Then it becomes one more digit at the end.",
        "return dummy.next": "The answer starts just after the placeholder: return that node.",
    },
    time=("O(max(n, m))", "One step per digit of the longer number."),
    space=("O(max(n, m))", "The result list has one node per digit (plus possibly one for the last carry)."),
    tests=[("l1=L([2, 4, 3]), l2=L([5, 6, 4])", [7, 0, 8]), ("l1=L([0]), l2=L([0])", [0]),
           ("l1=L([9, 9, 9]), l2=L([1])", [0, 0, 0, 1])],
)

lesson(
    "linked-list-cycle",
    pattern="Fast and slow pointers",
    statement="""Given the head of a linked list, return `True` if the list contains a **cycle** —
    that is, if following `next` pointers eventually leads back to a node already visited.""",
    args="head=L([3, 2, 0, -4], pos=1)",
    show_input="head = [3,2,0,-4], where the last node links back to the node at index 1",
    expected=True,
    why="After −4 the list goes back to 2, so walking it never ends.",
    picture="""Picture two runners, one twice as fast as the other. If the path is a straight road, the fast
    runner simply reaches its end. If the path loops, the fast runner keeps going around and must
    eventually catch the slow one from behind. So a catch-up means there is a loop, and reaching the
    end means there is none.""",
    idea=[
        "We could remember every visited node in a set and stop when one repeats, but that costs O(n) memory.",
        "Instead, send two runners down the list: `slow` moves one node per step, `fast` moves two.",
        "With no cycle, `fast` simply reaches the end. With a cycle, `fast` can never leave it and closes the gap to `slow` by one node per step — so they are guaranteed to meet.",
    ],
    views=[
        LinkedList(ptrs=["slow", "fast"], tones={"cur": "slow", "alt": "fast"}),
    ],
    final={"list.good": "slow"},
    notes=[
        ("fast = head.next",
         "Two runners: `slow` takes 1 step at a time and `fast` takes 2. If there is a loop, `fast` cannot run "
         "off the end — it keeps circling and must catch `slow`."),
        ("fast = fast.next.next", "`slow` steps to node {slow.val}; `fast` jumps two nodes to node {fast.val}."),
        ("while slow != fast", dict(
            no="`slow` and `fast` are standing on the **same node** ({slow.val}). That can only happen inside a loop.",
            no_marks={"list.good": "slow"})),
        ("return True", "The runners met, so the list has a cycle → **True**.", {"list.good": "slow"}),
    ],
    say={
        "def hasCycle": (
            "The function we must write. It gets the first node and answers `True` if following "
            "the arrows ever loops back."
        ),
        "if not head or not head.next": (
            "With no node, or one node with nothing after it, there can be no loop."
        ),
        "return False@1": "So answer `False`.",
        "slow = head": "The slow runner starts on the first node.",
        "fast = head.next": "The fast runner starts one node ahead.",
        "while slow != fast": "Repeat until the two runners are on the same node.",
        "if not fast or not fast.next": "Has the fast runner reached the end of the list?",
        "return False@2": "Then the list has an end, so there is no loop: answer `False`.",
        "slow = slow.next": "The slow runner moves one node.",
        "fast = fast.next.next": "The fast runner moves two.",
        "return True": "They met, which can only happen on a loop: answer `True`.",
    },
    time=("O(n)", "Once both runners are in the cycle, the gap shrinks by one every step."),
    space=("O(1)", "Just two pointers."),
    tests=[("head=L([1, 2], pos=0)", True), ("head=L([1])", False), ("head=L([1, 2, 3, 4])", False)],
)

lesson(
    "find-the-duplicate-number",
    pattern="Cycle detection on index → value links",
    statement="""`nums` holds n + 1 integers, each between 1 and n, so at least one value must
    repeat. Exactly one value is repeated (possibly several times). Find it **without modifying
    the array** and using only constant extra space.""",
    args="nums=[1, 3, 4, 2, 2]",
    expected=2,
    why="The value 2 appears at index 3 and at index 4.",
    picture="""Picture each position as a stepping stone with an arrow painted on it: the value at position `i`
    says which stone to hop to next. One value repeats, so two arrows lead to the same stone, and
    the path runs into a loop whose entrance is exactly that repeated value. First find the loop
    with a slow runner and a fast one. Then send one runner back to the start and move both one hop
    at a time: they meet at the entrance.""",
    idea=[
        "Read every value as a pointer: from index `i`, go to index `nums[i]`. Starting at index 0 this traces a path.",
        "Two indexes hold the duplicate value, so two arrows lead to the same place. That makes the path loop — and the **entrance of the loop is the duplicate**.",
        "Find the loop with slow/fast pointers (Floyd's algorithm). Then restart one pointer from the beginning and move both one hop at a time: they meet exactly at the entrance.",
    ],
    views=[
        Arr("nums", ptrs=["slow", "fast"]),
        Graph("range(len(nums))", edges="[(j, nums[j]) for j in range(len(nums))]", directed=True,
              title="arrow: index i → index nums[i]",
              pos={0: (-4.4, 0), 1: (-2.2, 0), 3: (0, 0), 2: (2.2, 0), 4: (4.4, 0)},
              tones={"cur": "slow", "alt": "fast"}),
    ],
    notes=[
        ("fast = nums[0]",
         "Follow the arrows *index → value*. Two indexes hold the same value, so two arrows lead to the same "
         "place and the path runs into a **loop**. Both runners take the first hop from index 0 to {slow}."),
        ("fast = nums[nums[fast]]", "`slow` takes one hop to {slow}; `fast` takes two hops to {fast}."),
        ("slow = nums[0]@2",
         "They met inside the loop, at {fast}. Now send `slow` back to the start. From here both move **one hop "
         "at a time**, and they will meet exactly where the loop is entered."),
        ("fast = nums[fast]", "One hop each: `slow` → {slow}, `fast` → {fast}."),
        ("while slow != fast", dict(
            no="They meet at **{slow}**. Two different arrows lead here, which means two indexes hold the value {slow}.",
            no_marks={"graph.good": "slow"})),
        ("return slow", "The repeated number is **{_ret}**.", {"graph.good": "slow"}),
    ],
    say={
        "def findDuplicate": (
            "The function we must write. It gets the list `nums` and returns the number that "
            "repeats."
        ),
        "slow = nums[0]@1": (
            "The slow runner takes its first hop: follow the arrow at position 0."
        ),
        "fast = nums[0]": "The fast runner takes the same first hop.",
        "while True": "Repeat until `break` stops it.",
        "slow = nums[slow]@1": "Slow runner: one hop (to the position its value names).",
        "fast = nums[nums[fast]]": "Fast runner: two hops.",
        "if slow == fast": "Are they on the same position? That can only happen inside the loop.",
        "break": "Then leave this first loop.",
        "slow = nums[0]@2": (
            "Phase 2: send the slow runner back to the start (one hop from position 0 again)."
        ),
        "while slow != fast": "Repeat until the two runners meet.",
        "slow = nums[slow]@2": "Move the slow runner one hop.",
        "fast = nums[fast]": "Move the other runner one hop too, no longer two.",
        "return slow": "They meet at the loop's entrance, which is the repeated number.",
    },
    time=("O(n)", "Both phases walk at most a few times around the path."),
    space=("O(1)", "Two index variables; the array is never changed."),
    tests=[("nums=[3, 1, 3, 4, 2]", 3), ("nums=[1, 1]", 1), ("nums=[2, 2, 2, 2, 2]", 2)],
)

lesson(
    "lru-cache",
    pattern="Hash map + doubly linked list",
    statement="""Design a cache that holds at most `capacity` keys. `get(key)` returns the value or
    −1. `put(key, value)` inserts or updates; if that would exceed the capacity, the **least
    recently used** key is evicted first. Both operations must run in O(1).""",
    ops=["LRUCache(2)", "put(1, 10)", "put(2, 20)", "get(1)", "put(3, 30)", "get(2)", "get(3)"],
    expected=[None, None, None, 10, None, -1, 30],
    why="Reading key 1 made it recently used, so when key 3 arrived it was key 2 that got evicted.",
    picture="""Picture a small shelf that holds only `capacity` books, and a list of those books in order of
    use, the most recently used at the front. Reading or adding a book moves it to the front of the
    list. When a new book needs room on a full shelf, the book at the back of the list, unused for
    the longest, has to go. A dictionary finds any book instantly, and the linked list makes moving
    a book to the front instant too.""",
    idea=[
        "A hash map gives O(1) lookup, but it has no idea which key was used longest ago.",
        "A **doubly linked list** can keep the keys ordered by use: most recent at the front, least recent at the back. Moving a node to the front or removing the last one is O(1) — if we can find the node instantly.",
        "So combine them: the map finds things in O(1), the list keeps the order. Every `get` and `put` moves its key to the front; eviction removes the back.",
    ],
    views=[
        HMap("self.cache", id="cache", title="cache  (key → value)"),
        Chain("self.order.head", id="order", title="order of use  (most recent first)",
              label="{'head' if n is self.order.head else 'tail' if n is self.order.tail else n.key}"),
    ],
    notes=[
        ("self.order = DoublyLinkedList()",
         "Two structures work together: a **hash map** for instant lookup, and a **doubly linked list** that "
         "keeps the keys in order of use — most recent at the front, least recent at the back."),
        ("if key in self.cache@1", dict(
            yes="Key {key} is in the cache.",
            no="Key {key} is **not** in the cache.",
            yes_marks={"cache.cur": "key"})),
        ("self.order.move_to_front(key)@1",
         "Reading key {key} counts as using it, so it moves to the **front** of the order list.",
         {"cache.cur": "key"}),
        ("return self.cache[key]", "Return its value, **{_ret}**.", {"cache.good": "key"}),
        ("return -1", "Return **-1** to say *not found*."),
        ("if len(self.cache) >= self.capacity", dict(
            yes="The cache already holds {len(self.cache)} keys — its full capacity. One has to go before key "
                "{key} can come in.",
            no="There is room: {len(self.cache)} of {self.capacity} slots are in use.")),
        ("removed_key = self.order.remove_last()",
         "The **least recently used** key is at the back of the list: key {removed_key}. Unlink it from the list…",
         {"cache.bad": "removed_key"}),
        ("del self.cache[removed_key]", "…and delete it from the map. Key {removed_key} is evicted."),
        ("self.cache[key] = value@2", "Store {key} → {value} in the map.", {"cache.cur": "key"}),
        ("self.order.add_to_front(key)",
         "Put key {key} at the **front** of the order list: it is now the most recently used.",
         {"cache.cur": "key"}),
    ],
    say={
        "class LRUCache": "The problem asks for a class called `LRUCache`.",
        "def __init__(self, capacity": (
            "Runs once, when the cache is created with its `capacity`."
        ),
        "self.capacity = capacity": "Remember how many keys fit.",
        "self.cache = {}": "A dictionary from each key to its value.",
        "self.order = DoublyLinkedList()": (
            "The keys in order of use, most recent first (the class below)."
        ),
        "def get": "Called for `get(key)`.",
        "if key in self.cache@1": "Is the key in the cache?",
        "self.order.move_to_front(key)@1": (
            "Yes: it has just been used, so move it to the front of the order."
        ),
        "return self.cache[key]": "Return its value.",
        "return -1": "Not in the cache: return -1.",
        "def put": "Called for `put(key, value)`.",
        "if key in self.cache@2": "Is the key already in the cache?",
        "self.cache[key] = value@1": "Yes: store the new value.",
        "self.order.move_to_front(key)@2": "And move it to the front: it has just been used.",
        "if len(self.cache) >= self.capacity": "A new key. Is the cache already full?",
        "removed_key = self.order.remove_last()": (
            "Then take the key at the back of the order, the least recently used, out of the "
            "list."
        ),
        "del self.cache[removed_key]": "And delete it from the dictionary too.",
        "self.cache[key] = value@2": "Store the new key with its value.",
        "self.order.add_to_front(key)": "Put the new key at the front of the order.",
        "class DoublyLinkedList": (
            "A linked list in which every node points both forward (`next`) and back (`prev`), so"
            " a node can be unhooked from the middle instantly."
        ),
        "def __init__(self):": "Runs when the list is created.",
        "self.head = ListNode()": "A placeholder node that always stays at the front.",
        "self.tail = ListNode()": (
            "And one that always stays at the back. Real nodes go between them."
        ),
        "self.head.next = self.tail": (
            "Start empty: the front placeholder points straight to the back one."
        ),
        "self.tail.prev = self.head": "And the back one points back to the front one.",
        "self.nodes = {}": "A dictionary from each key to its node, to find a node instantly.",
        "def add_to_front": "Put a new node for `key` right after the front placeholder.",
        "node = ListNode(key)": "Make a node holding the key.",
        "node.next = self.head.next": "It points forward to the node that used to be first.",
        "node.prev = self.head": "And back to the front placeholder.",
        "self.head.next.prev = node": "The old first node now points back to it.",
        "self.head.next = node": "And the placeholder points forward to it: it is first now.",
        "self.nodes[key] = node": "Remember which node holds this key.",
        "def move_to_front": "Move a key that is already in the list to the front.",
        "node = self.nodes[key]": "Find its node instantly.",
        "node.prev.next = node.next": "Unhook it: the node before it now points past it.",
        "node.next.prev = node.prev": "And the node after it points back past it.",
        "self.add_to_front(key)": "Then add the key at the front again, as a new node.",
        "def remove_last": "Remove the least recently used key and report which one it was.",
        "node = self.tail.prev": "The last real node sits just before the back placeholder.",
        "node.prev.next = self.tail": (
            "Unhook it: the node before it now points to the back placeholder."
        ),
        "self.tail.prev = node.prev": "And the placeholder points back to that node.",
        "del self.nodes[node.key]": "Forget this key's node.",
        "return node.key": "Report which key was removed.",
        "class ListNode": "One node of that list: it holds a key and its two arrows.",
        "def __init__(self, key=None)": "A new node starts with its key and no neighbours.",
        "self.key = key": "The key it holds.",
        "self.prev = None": "No node behind it yet.",
        "self.next = None": "No node after it yet.",
    },
    time=("O(1) per operation", "A map lookup plus a constant number of pointer changes in the list."),
    space=("O(capacity)", "One map entry and one list node per stored key."),
    tests=[
        (["LRUCache(2)", "put(1, 1)", "put(2, 2)", "get(1)", "put(3, 3)", "get(2)", "put(4, 4)", "get(1)",
          "get(3)", "get(4)"],
         [None, None, None, 1, None, -1, None, -1, 3, 4]),
        (["LRUCache(1)", "put(2, 1)", "put(2, 5)", "get(2)", "put(3, 9)", "get(2)"],
         [None, None, None, 5, None, -1]),
    ],
)

lesson(
    "merge-k-sorted-lists",
    pattern="Min-heap of the list fronts",
    statement="""You are given `k` linked lists, each sorted in increasing order. Merge them all into
    **one** sorted linked list and return it.""",
    args="lists=[L([1, 4]), L([2, 5]), L([3])]",
    expected=[1, 2, 3, 4, 5],
    why="Taking the smallest front node again and again gives 1, 2, 3, 4, 5.",
    picture="""Picture `k` sorted queues and one gate. A small waiting area (a heap) holds only the person at
    the front of each queue, and it always shows the smallest one first. Wave that person through to
    the merged line, and let the next person from the same queue step into the waiting area. The
    waiting area never holds more than `k` people, so finding the smallest stays quick.""",
    idea=[
        "The next node of the merged list is always the smallest among the **current front nodes** of the k lists.",
        "Finding that smallest by scanning all k fronts costs O(k) every time. A **min-heap** holding one entry per list finds it in O(log k).",
        "Pop the smallest, append it to the result, and push the next node from the same list (if there is one). The heap never holds more than k entries.",
    ],
    views=[
        LinkedList(ptrs={"lists[0]": "lists[0]", "lists[1]": "lists[1]", "lists[2]": "lists[2]",
                         "current": "current"},
                   rows=["list 0", "list 1", "list 2", "merged"], names={"dummy": "dummy"},
                   tones={"good": "chain(dummy.next)"}),
        Heap("min_heap", title="min_heap of (value, list index)", tones={"cur": "0"}),
    ],
    notes=[
        ("heapq.heappush(min_heap, (l.val, i))",
         "Put the **front node** of list {i} into the heap as (value {l.val}, list {i}). The heap keeps the "
         "smallest value on top."),
        ("current = dummy", "A dummy node starts the merged list, and `current` marks its last node."),
        ("val, idx = heapq.heappop(min_heap)",
         "Pop the smallest of all the fronts: **{val}**, which comes from list {idx}."),
        ("current = current.next", "Append a node holding {val} to the merged list."),
        ("if lists[idx].next", dict(
            no="List {idx} has no node after that one, so it contributes nothing more to the heap.")),
        ("heapq.heappush(min_heap, (lists[idx].next.val, idx))",
         "List {idx} has another node, {lists[idx].next.val}. Push it, so the heap again holds one front per "
         "unfinished list."),
        ("return dummy.next", "The heap is empty: every node has been merged. Return the list after the dummy."),
    ],
    say={
        "def mergeKLists": (
            "The function we must write. It gets `k` sorted linked lists and returns one merged, "
            "sorted list."
        ),
        "min_heap = []": (
            "A heap of `(value, which list)` pairs, smallest value first: one entry for the front"
            " node of each list."
        ),
        "for i, l in enumerate(lists)": (
            "Go through the lists: `i` is the list's number, `l` its first node."
        ),
        "if l:": "Is this list non-empty?",
        "heapq.heappush(min_heap, (l.val, i))": (
            "Put its first value into the heap, together with the list's number, so we know where"
            " it came from."
        ),
        "dummy = ListNode()": "A placeholder node to hang the merged list on.",
        "current = dummy": "`current` is the end of the merged list so far.",
        "while min_heap": "Repeat while some list still has nodes waiting.",
        "val, idx = heapq.heappop(min_heap)": (
            "Take the smallest value out of the heap, with the number of the list it came from."
        ),
        "current.next = ListNode(val)": (
            "Add a node with that value to the end of the merged list."
        ),
        "current = current.next": "It is now the end of the merged list.",
        "if lists[idx].next": "Does that list have another node after the one just used?",
        "heapq.heappush(min_heap, (lists[idx].next.val, idx))": (
            "Then put that next value into the heap, ready to compete."
        ),
        "lists[idx] = lists[idx].next": "And move that list's front on by one node.",
        "return dummy.next": "The merged list starts just after the placeholder: return it.",
    },
    time=("O(N log k)", "Each of the N nodes is pushed and popped once from a heap of at most k entries."),
    space=("O(k)", "The heap holds one entry per list (this version also builds new nodes for the result)."),
    tests=[("lists=[L([1, 4, 5]), L([1, 3, 4]), L([2, 6])]", [1, 1, 2, 3, 4, 4, 5, 6]), ("lists=[]", []),
           ("lists=[L([])]", [])],
)

lesson(
    "reverse-nodes-in-k-group",
    pattern="Reverse k nodes, recurse on the rest",
    statement="""Reverse the nodes of a linked list `k` at a time and return the new head. If fewer
    than `k` nodes remain at the end, leave them in their original order. Only the links may
    change, not the values.""",
    code="""
    class Solution:
        def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
            if not head or k == 1:
                return head

            # Are at least k nodes left?  Look only k nodes ahead.
            count = 0
            current = head
            while current and count < k:
                count += 1
                current = current.next

            if count < k:
                return head

            # Reverse the first k nodes
            prev, current = None, head
            for _ in range(k):
                next_node = current.next
                current.next = prev
                prev = current
                current = next_node

            # Recursively reverse the remaining part of the list
            head.next = self.reverseKGroup(current, k)

            return prev
    """,
    args="head=L([1, 2, 3, 4, 5]), k=2",
    expected=[2, 1, 4, 3, 5],
    why="1,2 becomes 2,1 and 3,4 becomes 4,3. The single node 5 is fewer than k, so it stays.",
    picture="""Picture a line of people split into teams of `k`, where each team turns around on its own: the
    first team reverses, then the next, and so on. A team at the end with fewer than `k` people
    stays as it is. Once a team has turned around, its old first person is now its last, so that
    person holds hands with whatever the rest of the line becomes.""",
    idea=[
        "Handle one group at a time: check that at least `k` nodes are left, then reverse exactly those `k` with the usual prev / current / next technique.",
        "After reversing, the group's old first node has become its **last** node — the right place to attach whatever comes next.",
        "What comes next is the same problem on the rest of the list, so solve it recursively and attach the result. A leftover of fewer than `k` nodes is returned unchanged.",
    ],
    views=[
        LinkedList(ptrs=["head", "prev", "current"]),
        Calls("reverseKGroup", "reverseKGroup(head = {nv(head)})"),
    ],
    final={"list.good": "chain(_ret)"},
    notes=[
        ("if count < k", dict(
            yes="Starting at node {head.val} only {plural(count, 'node')} remain{'s' if count == 1 else ''} — "
                "fewer than k = {k}. {'It stays as it is' if count == 1 else 'They stay as they are'}.",
            no="Counting ahead from node {head.val} found {k} nodes, so a full group of k = {k} is there. "
               "Reverse those {k}.")),
        ("return head@2", "Return node {head.val} unchanged."),
        ("current.next = prev", "Flip the arrow of node {current.val} so it points back at {nv(prev)}."),
        ("head.next = self.reverseKGroup(current, k)", dict(
            pre="This group is reversed: node {prev.val} is its new front and node {head.val} its new end. "
                "Now solve **the rest of the list** (starting at {nv(current)}) in the same way.",
            post="The rest came back with {nv(head.next)} in front. Attach it after node {head.val}, the end "
                 "of this group.")),
        ("return prev", "Return node {prev.val}, the new front of this group."),
    ],
    say={
        "def reverseKGroup": (
            "The function we must write. It gets the first node and `k`, and returns the first "
            "node after reversing every full group of `k`."
        ),
        "if not head or k == 1": "An empty list, or groups of just one node, need no change.",
        "return head@1": "So return the list as it is.",
        "count = 0": "Count how many nodes are left, but only up to `k`.",
        "current = head": "Start counting from the first node.",
        "while current and count < k": (
            "Repeat while there is a node and fewer than `k` have been counted."
        ),
        "count += 1": "Count this node.",
        "current = current.next": "Move on to the next node.",
        "if count < k": "Are there fewer than `k` nodes left?",
        "return head@2": "Then this last group is too short: leave it as it is.",
        "prev, current = None, head": "Get ready to reverse this group of `k` nodes.",
        "for _ in range(k)": "Repeat `k` times, once for each node of the group.",
        "next_node = current.next": (
            "Remember the node after `current` before its arrow changes, or the rest of the list "
            "would be lost."
        ),
        "current.next = prev": "Turn `current`'s arrow around: it now points back at `prev`.",
        "prev = current": "Move `prev` forward onto `current`.",
        "current = next_node": "Move `current` on to the node we remembered.",
        "head.next = self.reverseKGroup(current, k)": (
            "The group's old first node (`head`) is now its last. Point it at the result of doing"
            " the same to the rest of the list: the function calls itself."
        ),
        "return prev": "`prev` is the group's new first node: return it.",
    },
    time=("O(n)", "Every node is counted once (the count stops after k nodes) and has its arrow flipped once."),
    space=("O(n / k)", "One recursive call per group waits on the call stack. (Doing the same group by group "
                       "in a loop, with a dummy node in front, needs only O(1).)"),
    tests=[("head=L([1, 2, 3, 4, 5]), k=3", [3, 2, 1, 4, 5]), ("head=L([1, 2]), k=2", [2, 1]),
           ("head=L([1]), k=1", [1])],
)

# end of c06_linked_list
