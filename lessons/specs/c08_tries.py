"""Tries."""

from lessons.engine.api import *  # noqa: F401,F403

lesson(
    "implement-trie-prefix-tree",
    pattern="Tree of letters with end-of-word marks",
    statement="""Implement a **trie** (prefix tree) with three operations: `insert(word)` stores a
    word, `search(word)` says whether that exact word was stored, and `startsWith(prefix)` says
    whether any stored word begins with the prefix.""",
    ops=["Trie()", "insert('cat')", "insert('car')", "search('car')", "search('ca')", "search('cab')",
         "startsWith('ca')"],
    expected=[None, None, None, True, False, False, True],
    why="'car' was inserted. 'ca' is only the beginning of stored words, and 'cab' leaves the tree at b.",
    idea=[
        "Store words letter by letter in a tree: each node has one child per next letter. Words with the same beginning **share** the same path.",
        "To find a word, start at the root and follow its letters one at a time. If a letter has no branch, the word is not there.",
        "Reaching the last letter is not enough for `search` — `ca` must not count just because `cat` exists. So the node where a real word ends carries an **end-of-word mark**.",
    ],
    init={"fresh": "None"},
    views=[
        Trie("self.root", ptrs=["node"], tones={"cur": "node"}, title="trie  (a ring marks the end of a word)"),
        Vars("word", "prefix", "char"),
    ],
    notes=[
        ("self.root = TrieNode()", "The trie starts as a single empty root node. Every word begins there."),
        ("node.children[char] = TrieNode()", dict(save={"fresh": "node.children[char]"})),
        ("node = node.children[char]@1", [
            ("node is fresh", "`{char}`: there was no branch for this letter yet, so a new node is created. Step into it."),
            (None, "`{char}`: this branch already exists — it is shared with a word stored earlier. Just follow it."),
        ]),
        ("node.is_end = True",
         "Mark this node as the **end of a word**. That is what makes `{word}` a stored word and not merely a prefix."),
        ("node = node.children[char]@2", "`{char}`: the branch exists, follow it."),
        ("return False@1", "There is no `{char}` branch here, so the word was never stored → **False**."),
        ("return node.is_end", [
            ("_ret", "Every letter was found, and this node carries the end-of-word mark → **True**."),
            (None, "Every letter was found, but this node has **no end-of-word mark**: `{word}` is only the beginning "
                   "of a stored word → **False**."),
        ]),
        ("node = node.children[char]@3", "`{char}`: the branch exists, follow it."),
        ("return True", "The whole prefix could be followed. `startsWith` does not need an end mark → **True**."),
    ],
    time=("O(L) per operation", "Each operation follows one node per letter of the word (length L)."),
    space=("O(total letters)", "In the worst case every letter of every inserted word gets its own node."),
    tests=[
        (["Trie()", "insert('apple')", "search('apple')", "search('app')", "startsWith('app')", "insert('app')",
          "search('app')", "startsWith('b')"],
         [None, None, True, False, True, None, True, False]),
    ],
)

lesson(
    "design-add-and-search-words-data-structure",
    pattern="Trie + DFS for wildcards",
    statement="""Design a dictionary with `addWord(word)` and `search(word)`. In `search` the pattern
    may contain dots: each `.` matches **any single letter**.""",
    code="""
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False

    class WordDictionary:
        def __init__(self):
            self.root = TrieNode()

        def addWord(self, word: str) -> None:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end = True

        def search(self, word: str) -> bool:
            def dfs(start, node):
                # Does word[start:] match some path that begins at `node`?
                for i in range(start, len(word)):
                    char = word[i]
                    if char == ".":
                        for letter in node.children:
                            if dfs(i + 1, node.children[letter]):
                                return True
                        return False
                    if char not in node.children:
                        return False
                    node = node.children[char]
                return node.is_end

            return dfs(0, self.root)
    """,
    ops=["WordDictionary()", "addWord('bad')", "addWord('dad')", "search('pad')", "search('.ad')", "search('b..')"],
    expected=[None, None, None, False, True, True],
    why="'.ad' matches bad (and dad); 'b..' matches bad; nothing stored starts with p.",
    idea=[
        "Without dots this is exactly a trie: follow one branch per letter.",
        "A `.` can be any letter, so at that position we cannot know which branch to take — **try them all**.",
        "That is a depth-first search: for each child branch, recursively match the rest of the pattern. One success is enough; if every branch fails, the pattern does not match.",
    ],
    views=[
        Trie("self.root", ptrs=["node"], tones={"cur": "node"}, title="trie  (a ring marks the end of a word)"),
        Calls("dfs", "match {show(word[start:])} from here", title="recursive calls"),
        Vars("word", "char"),
    ],
    notes=[
        ("node.is_end = True",
         "`{word}` is stored letter by letter, exactly as in an ordinary trie, and its last node gets the end-of-word mark."),
        ("if char == ", dict(
            yes="`.` is a wildcard: it can be **any** letter. So try each branch under this node — "
                "{list(node.children)} — "
                "{'against the rest of the pattern, `' + show(word[i + 1:]) + '`' if i + 1 < len(word) else 'the pattern ends right after it'}.")),
        ("if dfs(i + 1, node.children[letter])", dict(
            pre="Let the `.` stand for `{letter}` and continue below that node.",
            yes="That choice led to a match, so pass **True** back to the caller.")),
        ("if char not in node.children@2", dict(
            yes="There is no `{char}` branch here, so this path fails → **False**.")),
        ("node = node.children[char]@2", "`{char}`: the branch exists, follow it."),
        ("return node.is_end", [
            ("_ret", "The pattern is used up, and this node ends a stored word → **True**."),
            (None, "The pattern is used up, but no stored word ends at this node → **False**."),
        ]),
    ],
    time=("O(L) to add, up to O(26ᴸ) to search", "Adding follows one branch per letter. Each dot in a search can fan out to every child, though real dictionaries cut that down quickly."),
    space=("O(total letters)", "The trie stores each distinct prefix once; the search recursion is at most L deep."),
    tests=[
        (["WordDictionary()", "addWord('bad')", "addWord('dad')", "addWord('mad')", "search('pad')", "search('bad')",
          "search('.ad')", "search('b..')", "search('b.')", "search('...')", "search('....')"],
         [None, None, None, None, False, True, True, True, False, True, False]),
    ],
)

lesson(
    "word-search-ii",
    pattern="Trie + backtracking on a grid",
    statement="""Given a grid of letters and a list of `words`, return every word that can be traced
    on the grid by moving between horizontally or vertically neighbouring cells, using each cell
    **at most once** per word.""",
    code="""
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.word = None  # set on the node where a whole word ends

    class Solution:
        def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
            root = TrieNode()
            for word in words:
                node = root
                for ch in word:
                    if ch not in node.children:
                        node.children[ch] = TrieNode()
                    node = node.children[ch]
                node.word = word

            rows, cols = len(board), len(board[0])
            found = []

            def dfs(r, c, node):
                ch = board[r][c]
                if ch not in node.children:
                    return
                node = node.children[ch]
                if node.word:
                    found.append(node.word)
                    node.word = None  # never report the same word twice
                board[r][c] = "#"  # this cell is in use on the current path
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                        dfs(nr, nc, node)
                board[r][c] = ch  # free the cell again on the way back

            for r in range(rows):
                for c in range(cols):
                    dfs(r, c, root)
            return found
    """,
    args='board=[["o", "a", "n"], ["e", "t", "a"]], words=["oat", "eat", "tan"]',
    expected=["oat", "tan"],
    unordered=1,
    why="o→a→t and t→a→n can be traced through neighbouring cells. For eat, no a is next to the e.",
    idea=[
        "Searching the grid separately for each word repeats a lot of work when words share beginnings.",
        "Put all the words in a **trie** and walk the grid and the trie *together*: from a cell, only continue while the trie has a branch for the next letter.",
        "Start such a walk from every cell (DFS with backtracking, marking cells as in use). Whenever the trie node marks the end of a word, that word has been found.",
    ],
    views=[
        Grid("board", ptrs={"r, c": "(r, c)"}, vals={"#": "win"}),
        Trie("root", end="word", tones={"cur": "node"}, title="trie of the words  (a ring = a word ends here)"),
        Items("found", title="found"),
    ],
    notes=[
        ("node.word = word",
         "Insert `{word}` into the trie: one node per letter, and the last node remembers the whole word."),
        ("rows, cols = len(board), len(board[0])",
         "The trie is ready. Now start a search from every cell, walking the board and the trie **together**: "
         "a path on the board is only followed while the trie has a matching branch."),
        ("if ch not in node.children@2", dict(
            yes=[
                ("node is root", "Try starting at ({r}, {c}): no word begins with `{ch}`. Skip this cell."),
                (None, "Neighbour ({r}, {c}) holds `{ch}`, but no word continues with `{ch}` from here. Dead end — go back."),
            ])),
        ("node = node.children[ch]@2", [
            ("was.node is root", "**Start a walk at ({r}, {c})**: `{ch}` is the first letter of some word, so step into the trie's `{ch}` branch."),
            (None, "Neighbour ({r}, {c}) holds `{ch}`, and the trie continues with `{ch}` here too. Step forward on the board **and** in the trie."),
        ]),
        ("found.append(node.word)",
         "This trie node marks the end of a word: **{found[-1]}** has been traced on the board. Record it.",
         {"found.good": "-1"}),
        ("board[r][c] = ch", dict(
            post="Every direction from ({r}, {c}) has been tried. Free the cell again so that other paths may use it.")),
        ("return found", "Every cell has served as a starting point. Words found: **{_ret}**."),
    ],
    time=("O(m · n · 4ᴸ)", "A walk starts at each of the m · n cells and branches up to 4 ways for up to L letters; the trie cuts most branches early."),
    space=("O(total letters)", "The trie, plus a recursion depth of at most L."),
    tests=[
        ('board=[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], '
         'words=["oath","pea","eat","rain"]', ["eat", "oath"]),
        ('board=[["a","b"],["c","d"]], words=["abcb"]', []),
        ('board=[["a"]], words=["a"]', ["a"]),
    ],
)

# end of c08_tries
