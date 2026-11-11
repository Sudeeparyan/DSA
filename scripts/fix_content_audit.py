#!/usr/bin/env python3
"""Fix weak examples, generic stories, and Story-version prefixes."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBS = ROOT / "content/problems"
CATALOG = json.loads((ROOT / "content/catalog.json").read_text())

# Real LeetCode-style examples for every slug (input, output, explanation)
EXAMPLES: dict[str, list[tuple[str, str, str]]] = {
    "contains-duplicate": [("nums = [1,2,3,1]", "true", "1 appears twice."), ("nums = [1,2,3,4]", "false", "All unique.")],
    "valid-anagram": [('s = "anagram", t = "nagaram"', "true", "Same multiset of letters."), ('s = "rat", t = "car"', "false", "Different letters.")],
    "two-sum": [("nums = [2,7,11,15], target = 9", "[0,1]", "2 + 7 = 9."), ("nums = [3,2,4], target = 6", "[1,2]", "2 + 4 = 6.")],
    "group-anagrams": [('strs = ["eat","tea","tan","ate","nat","bat"]', '[["bat"],["nat","tan"],["ate","eat","tea"]]', "Grouped by signature."), ('strs = [""]', '[[""]]', "One empty string.")],
    "top-k-frequent-elements": [("nums = [1,1,1,2,2,3], k = 2", "[1,2]", "Top frequencies."), ("nums = [1], k = 1", "[1]", "Single value.")],
    "product-of-array-except-self": [("nums = [1,2,3,4]", "[24,12,8,6]", "Prefix × suffix."), ("nums = [-1,1,0,-3,3]", "[0,0,9,0,0]", "Zeros.")],
    "valid-sudoku": [("valid partial board", "true", "No conflicts yet."), ("duplicate digit in a box", "false", "Box rule broken.")],
    "encode-and-decode-strings": [('["lint","code","love","you"]', '["lint","code","love","you"]', "Round-trip."), ('["we","say",":","yes"]', '["we","say",":","yes"]', "Special chars safe.")],
    "longest-consecutive-sequence": [("nums = [100,4,200,1,3,2]", "4", "1..4"), ("nums = [0,3,7,2,5,8,4,6,0,1]", "9", "0..8")],
    "valid-palindrome": [('s = "A man, a plan, a canal: Panama"', "true", "Alphanumeric palindrome."), ('s = "race a car"', "false", "Not palindrome.")],
    "two-sum-ii-input-array-is-sorted": [("numbers = [2,7,11,15], target = 9", "[1,2]", "1-indexed."), ("numbers = [2,3,4], target = 6", "[1,3]", "2+4")],
    "3sum": [("nums = [-1,0,1,2,-1,-4]", "[[-1,-1,2],[-1,0,1]]", "Zero-sum triplets."), ("nums = [0,1,1]", "[]", "None.")],
    "container-with-most-water": [("height = [1,8,6,2,5,4,8,3,7]", "49", "Best area."), ("height = [1,1]", "1", "Only pair.")],
    "trapping-rain-water": [("height = [0,1,0,2,1,0,1,3,2,1,2,1]", "6", "Trapped units."), ("height = [4,2,0,3,2,5]", "9", "Trapped units.")],
    "best-time-to-buy-and-sell-stock": [("prices = [7,1,5,3,6,4]", "5", "Buy 1 sell 6."), ("prices = [7,6,4,3,1]", "0", "No profit.")],
    "longest-substring-without-repeating-characters": [('s = "abcabcbb"', "3", '"abc"'), ('s = "bbbbb"', "1", "One char.")],
    "longest-repeating-character-replacement": [('s = "ABAB", k = 2', "4", "Whole string."), ('s = "AABABBA", k = 1', "4", "Window 4.")],
    "permutation-in-string": [('s1 = "ab", s2 = "eidbaooo"', "true", "Window ba."), ('s1 = "ab", s2 = "eidboaoo"', "false", "No window.")],
    "minimum-window-substring": [('s = "ADOBECODEBANC", t = "ABC"', '"BANC"', "Smallest cover."), ('s = "a", t = "a"', '"a"', "Exact.")],
    "sliding-window-maximum": [("nums = [1,3,-1,-3,5,3,6,7], k = 3", "[3,3,5,5,6,7]", "Window maxima."), ("nums = [1], k = 1", "[1]", "Single.")],
    "valid-parentheses": [('s = "()"', "true", "Match."), ('s = "(]"', "false", "Mismatch.")],
    "min-stack": [("MinStack ops: push -2,0,-3; getMin; pop; top; getMin", "-3, then 0, then -2", "Tracks running min."), ("push 1; push 2; getMin", "1", "Min is 1.")],
    "evaluate-reverse-polish-notation": [('tokens = ["2","1","+","3","*"]', "9", "(2+1)*3"), ('tokens = ["4","13","5","/","+"]', "6", "4+(13/5)")],
    "generate-parentheses": [("n = 3", '["((()))","(()())","(())()","()(())","()()()"]', "All valid."), ("n = 1", '["()"]', "One pair.")],
    "daily-temperatures": [("temperatures = [73,74,75,71,69,72,76,73]", "[1,1,4,2,1,1,0,0]", "Wait days."), ("temperatures = [30,40,50,60]", "[1,1,1,0]", "Rising.")],
    "car-fleet": [("target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]", "3", "Three fleets."), ("target = 10, position = [3], speed = [3]", "1", "One car.")],
    "largest-rectangle-in-histogram": [("heights = [2,1,5,6,2,3]", "10", "5×2 rectangle."), ("heights = [2,4]", "4", "Best area 4.")],
    "binary-search": [("nums = [-1,0,3,5,9,12], target = 9", "4", "Index 4."), ("nums = [-1,0,3,5,9,12], target = 2", "-1", "Missing.")],
    "search-a-2d-matrix": [("matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3", "true", "Found."), ("same matrix, target = 13", "false", "Missing.")],
    "koko-eating-bananas": [("piles = [3,6,7,11], h = 8", "4", "Min speed."), ("piles = [30,11,23,4,20], h = 5", "30", "Faster needed.")],
    "find-minimum-in-rotated-sorted-array": [("nums = [3,4,5,1,2]", "1", "Min."), ("nums = [4,5,6,7,0,1,2]", "0", "Min.")],
    "search-in-rotated-sorted-array": [("nums = [4,5,6,7,0,1,2], target = 0", "4", "Found."), ("nums = [4,5,6,7,0,1,2], target = 3", "-1", "Missing.")],
    "time-based-key-value-store": [('set("foo","bar",1); get("foo",1)', '"bar"', "Exact time."), ('set("foo","bar2",4); get("foo",5)', '"bar2"', "Latest ≤ t.")],
    "median-of-two-sorted-arrays": [("nums1 = [1,3], nums2 = [2]", "2.0", "Median 2."), ("nums1 = [1,2], nums2 = [3,4]", "2.5", "Avg 2 and 3.")],
    "reverse-linked-list": [("head = [1,2,3,4,5]", "[5,4,3,2,1]", "Reversed."), ("head = [1,2]", "[2,1]", "Two nodes.")],
    "merge-two-sorted-lists": [("list1 = [1,2,4], list2 = [1,3,4]", "[1,1,2,3,4,4]", "Merged."), ("list1 = [], list2 = [0]", "[0]", "One empty.")],
    "reorder-list": [("head = [1,2,3,4]", "[1,4,2,3]", "Reordered."), ("head = [1,2,3,4,5]", "[1,5,2,4,3]", "Odd length.")],
    "remove-nth-node-from-end-of-list": [("head = [1,2,3,4,5], n = 2", "[1,2,3,5]", "Removed 4."), ("head = [1], n = 1", "[]", "Empty.")],
    "copy-list-with-random-pointer": [("head with next+random links", "deep copy", "New nodes, same shape."), ("two-node mutual random", "deep copy", "Random preserved.")],
    "add-two-numbers": [("l1 = [2,4,3], l2 = [5,6,4]", "[7,0,8]", "342+465."), ("l1 = [0], l2 = [0]", "[0]", "Zero.")],
    "linked-list-cycle": [("head = [3,2,0,-4], pos = 1", "true", "Cycle."), ("head = [1], pos = -1", "false", "No cycle.")],
    "find-the-duplicate-number": [("nums = [1,3,4,2,2]", "2", "Dup 2."), ("nums = [3,1,3,4,2]", "3", "Dup 3.")],
    "lru-cache": [("cap=2; put1; put2; get1; put3; get2", "1 then -1", "LRU eviction."), ("continue puts/gets", "3 and 4 hit", "Cache updated.")],
    "merge-k-sorted-lists": [("lists = [[1,4,5],[1,3,4],[2,6]]", "[1,1,2,3,4,4,5,6]", "Merged."), ("lists = []", "[]", "Empty.")],
    "reverse-nodes-in-k-group": [("head = [1,2,3,4,5], k = 2", "[2,1,4,3,5]", "Pairs."), ("head = [1,2,3,4,5], k = 3", "[3,2,1,4,5]", "Trio.")],
    "invert-binary-tree": [("root = [4,2,7,1,3,6,9]", "[4,7,2,9,6,3,1]", "Mirrored."), ("root = [2,1,3]", "[2,3,1]", "Swap children.")],
    "maximum-depth-of-binary-tree": [("root = [3,9,20,null,null,15,7]", "3", "Depth 3."), ("root = [1,null,2]", "2", "Depth 2.")],
    "diameter-of-binary-tree": [("root = [1,2,3,4,5]", "3", "Longest path edges."), ("root = [1,2]", "1", "One edge.")],
    "balanced-binary-tree": [("root = [3,9,20,null,null,15,7]", "true", "Balanced."), ("root = [1,2,2,3,3,null,null,4,4]", "false", "Skewed.")],
    "same-tree": [("p = [1,2,3], q = [1,2,3]", "true", "Identical."), ("p = [1,2], q = [1,null,2]", "false", "Shape differs.")],
    "subtree-of-another-tree": [("root = [3,4,5,1,2], subRoot = [4,1,2]", "true", "Subtree."), ("root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]", "false", "Extra 0.")],
    "lowest-common-ancestor-of-a-binary-search-tree": [("root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "6", "Root is LCA."), ("same tree, p = 2, q = 4", "2", "p is ancestor.")],
    "binary-tree-level-order-traversal": [("root = [3,9,20,null,null,15,7]", "[[3],[9,20],[15,7]]", "Levels."), ("root = [1]", "[[1]]", "One node.")],
    "binary-tree-right-side-view": [("root = [1,2,3,null,5,null,4]", "[1,3,4]", "Rightmost each level."), ("root = [1,null,3]", "[1,3]", "Right spine.")],
    "count-good-nodes-in-binary-tree": [("root = [3,1,4,3,null,1,5]", "4", "Good nodes."), ("root = [3,3,null,4,2]", "3", "Three goods.")],
    "validate-binary-search-tree": [("root = [2,1,3]", "true", "Valid BST."), ("root = [5,1,4,null,null,3,6]", "false", "4 < 5 on right.")],
    "kth-smallest-element-in-a-bst": [("root = [3,1,4,null,2], k = 1", "1", "Smallest."), ("root = [5,3,6,2,4,null,null,1], k = 3", "3", "3rd smallest.")],
    "construct-binary-tree-from-preorder-and-inorder-traversal": [("preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "[3,9,20,null,null,15,7]", "Built tree."), ("preorder = [-1], inorder = [-1]", "[-1]", "Single.")],
    "binary-tree-maximum-path-sum": [("root = [1,2,3]", "6", "2+1+3."), ("root = [-10,9,20,null,null,15,7]", "42", "15+20+7.")],
    "serialize-and-deserialize-binary-tree": [("root = [1,2,3,null,null,4,5]", "same after ser/deser", "Round-trip."), ("root = []", "[]", "Empty.")],
    "implement-trie-prefix-tree": [('insert "apple"; search "apple"', "true", "Word present."), ('search "app"; startsWith "app"', "false then true", "Prefix only.")],
    "design-add-and-search-words-data-structure": [('add "bad","dad","mad"; search "pad"', "false", "Missing."), ('search ".ad"; search "b.."', "true, true", "Wildcards.")],
    "word-search-ii": [('board letters, words = ["oath","pea","eat","rain"]', '["eat","oath"]', "Found words."), ("empty words", "[]", "Nothing.")],
    "kth-largest-element-in-a-stream": [("k = 3, nums = [4,5,8,2]; add 3,5,10,9,4", "4,5,5,8,8", "Stream kth."), ("k = 1, nums = []", "depends on adds", "Min-heap size 1.")],
    "last-stone-weight": [("stones = [2,7,4,1,8,1]", "1", "Last stone."), ("stones = [1]", "1", "Only one.")],
    "k-closest-points-to-origin": [("points = [[1,3],[-2,2]], k = 1", "[[-2,2]]", "Closer."), ("points = [[3,3],[5,-1],[-2,4]], k = 2", "[[3,3],[-2,4]]", "Two closest.")],
    "kth-largest-element-in-an-array": [("nums = [3,2,1,5,6,4], k = 2", "5", "2nd largest."), ("nums = [3,2,3,1,2,4,5,5,6], k = 4", "4", "4th largest.")],
    "task-scheduler": [('tasks = ["A","A","A","B","B","B"], n = 2', "8", "With cooldown."), ('tasks = ["A","A","A","B","B","B"], n = 0', "6", "No cooldown.")],
    "design-twitter": [("post/follow/unfollow/getNewsFeed sequence", "recent followed tweets", "Feed order."), ("user with no follows", "own tweets only", "Empty social.")],
    "find-median-from-data-stream": [("add 1,2; findMedian; add 3; findMedian", "1.5 then 2", "Running median."), ("add 6; median", "6", "Single.")],
    "subsets": [("nums = [1,2,3]", "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]", "All subsets."), ("nums = [0]", "[[],[0]]", "Two subsets.")],
    "combination-sum": [("candidates = [2,3,6,7], target = 7", "[[2,2,3],[7]]", "Reuse allowed."), ("candidates = [2,3,5], target = 8", "[[2,2,2,2],[2,3,3],[3,5]]", "Combos.")],
    "permutations": [("nums = [1,2,3]", "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]", "All orders."), ("nums = [0,1]", "[[0,1],[1,0]]", "Two perms.")],
    "subsets-ii": [("nums = [1,2,2]", "[[],[1],[1,2],[1,2,2],[2],[2,2]]", "No dup subsets."), ("nums = [0]", "[[],[0]]", "Simple.")],
    "combination-sum-ii": [("candidates = [10,1,2,7,6,1,5], target = 8", "[[1,1,6],[1,2,5],[1,7],[2,6]]", "No reuse."), ("candidates = [2,5,2,1,2], target = 5", "[[1,2,2],[5]]", "Unique combos.")],
    "word-search": [('board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"', "true", "Path exists."), ('same board, word = "ABCB"', "false", "Reuse forbidden.")],
    "palindrome-partitioning": [('s = "aab"', '[["a","a","b"],["aa","b"]]', "Pal parts."), ('s = "a"', '[["a"]]', "Single.")],
    "letter-combinations-of-a-phone-number": [('digits = "23"', '["ad","ae","af","bd","be","bf","cd","ce","cf"]', "Keypad."), ('digits = ""', "[]", "Empty.")],
    "n-queens": [("n = 4", '[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]', "Two solutions."), ("n = 1", '[["Q"]]', "One queen.")],
    "number-of-islands": [('grid land/water sample', "1", "One island."), ("all water", "0", "None.")],
    "clone-graph": [("node adjList = [[2,4],[1,3],[2,4],[1,3]]", "deep clone", "Same links new nodes."), ("empty", "empty", "Null graph.")],
    "max-area-of-island": [("grid with islands", "6", "Largest area."), ("all water", "0", "None.")],
    "pacific-atlantic-water-flow": [("heights 5x5 sample", "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]", "Both oceans."), ("1x1", "[[0,0]]", "Touches both.")],
    "surrounded-regions": [('board with O/X', "captured inner O", "Border O safe."), ("no surrounded", "unchanged", "Nothing to flip.")],
    "rotting-oranges": [("grid = [[2,1,1],[1,1,0],[0,1,1]]", "4", "Minutes."), ("grid = [[0,2]]", "0", "Already done.")],
    "walls-and-gates": [("rooms with INF/gates", "filled distances", "Multi-source BFS."), ("empty rooms only", "unchanged INF", "No gates.")],
    "course-schedule": [("numCourses = 2, prerequisites = [[1,0]]", "true", "Possible."), ("numCourses = 2, prerequisites = [[1,0],[0,1]]", "false", "Cycle.")],
    "course-schedule-ii": [("numCourses = 2, prerequisites = [[1,0]]", "[0,1]", "Order."), ("numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", "[0,2,1,3]", "One valid order.")],
    "redundant-connection": [("edges = [[1,2],[1,3],[2,3]]", "[2,3]", "Cycle edge."), ("edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]", "[1,4]", "Redundant.")],
    "number-of-connected-components-in-an-undirected-graph": [("n = 5, edges = [[0,1],[1,2],[3,4]]", "2", "Two components."), ("n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]", "1", "One component.")],
    "graph-valid-tree": [("n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]", "true", "Tree."), ("n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]", "false", "Cycle.")],
    "word-ladder": [('beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]', "5", "Shortest ladder."), ('endWord missing', "0", "Impossible.")],
    "reconstruct-itinerary": [('tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]', '["JFK","MUC","LHR","SFO","SJC"]', "Euler path."), ('tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]', '["JFK","ATL","JFK","SFO","ATL","SFO"]', "Lexical smallest.")],
    "min-cost-to-connect-all-points": [("points = [[0,0],[2,2],[3,10],[5,2],[7,0]]", "20", "MST cost."), ("points = [[3,12],[-2,5],[-4,1]]", "18", "MST cost.")],
    "network-delay-time": [("times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2", "2", "All informed."), ("times = [[1,2,1]], n = 2, k = 1", "1", "One edge.")],
    "cheapest-flights-within-k-stops": [("n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1", "700", "Via 1."), ("same, k = 2", "400", "Cheaper longer.")],
    "swim-in-rising-water": [("grid = [[0,2],[1,3]]", "3", "Wait until 3."), ("grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]", "16", "Path max min.")],
    "alien-dictionary": [('words = ["wrt","wrf","er","ett","rftt"]', '"wertf"', "Order."), ('words = ["z","x"]', '"zx"', "z before x.")],
    "climbing-stairs": [("n = 2", "2", "1+1 or 2."), ("n = 3", "3", "Three ways.")],
    "min-cost-climbing-stairs": [("cost = [10,15,20]", "15", "Start at 1."), ("cost = [1,100,1,1,1,100,1,1,100,1]", "6", "Cheap path.")],
    "house-robber": [("nums = [1,2,3,1]", "4", "1+3."), ("nums = [2,7,9,3,1]", "12", "2+9+1.")],
    "house-robber-ii": [("nums = [2,3,2]", "3", "Circle."), ("nums = [1,2,3,1]", "4", "Best linear of two ranges.")],
    "longest-palindromic-substring": [('s = "babad"', '"bab" or "aba"', "Odd center."), ('s = "cbbd"', '"bb"', "Even center.")],
    "palindromic-substrings": [('s = "abc"', "3", "Singles."), ('s = "aaa"', "6", "Many pals.")],
    "decode-ways": [('s = "12"', "2", "AB or L."), ('s = "226"', "3", "Three decodings.")],
    "coin-change": [("coins = [1,2,5], amount = 11", "3", "5+5+1."), ("coins = [2], amount = 3", "-1", "Impossible.")],
    "maximum-product-subarray": [("nums = [2,3,-2,4]", "6", "2×3."), ("nums = [-2,0,-1]", "0", "Zero best.")],
    "word-break": [('s = "leetcode", wordDict = ["leet","code"]', "true", "leet+code."), ('s = "applepenapple", wordDict = ["apple","pen"]', "true", "Reusable.")],
    "longest-increasing-subsequence": [("nums = [10,9,2,5,3,7,101,18]", "4", "2,3,7,101."), ("nums = [0,1,0,3,2,3]", "4", "0,1,2,3.")],
    "partition-equal-subset-sum": [("nums = [1,5,11,5]", "true", "11 vs 1+5+5."), ("nums = [1,2,3,5]", "false", "Odd sum.")],
    "unique-paths": [("m = 3, n = 7", "28", "Paths."), ("m = 3, n = 2", "3", "Paths.")],
    "longest-common-subsequence": [('text1 = "abcde", text2 = "ace"', "3", "ace."), ('text1 = "abc", text2 = "abc"', "3", "Full.")],
    "best-time-to-buy-and-sell-stock-with-cooldown": [("prices = [1,2,3,0,2]", "3", "With cooldown."), ("prices = [1]", "0", "No trade.")],
    "coin-change-ii": [("amount = 5, coins = [1,2,5]", "4", "Combinations."), ("amount = 3, coins = [2]", "0", "None.")],
    "target-sum": [("nums = [1,1,1,1,1], target = 3", "5", "Ways."), ("nums = [1], target = 1", "1", "One way.")],
    "interleaving-string": [('s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"', "true", "Interleave."), ('s3 = "aadbbbaccc"', "false", "Impossible.")],
    "longest-increasing-path-in-a-matrix": [("matrix = [[9,9,4],[6,6,8],[2,1,1]]", "4", "1→2→6→9."), ("matrix = [[3,4,5],[3,2,6],[2,2,1]]", "4", "Path length.")],
    "distinct-subsequences": [('s = "rabbbit", t = "rabbit"', "3", "Ways."), ('s = "babgbag", t = "bag"', "5", "Ways.")],
    "edit-distance": [('word1 = "horse", word2 = "ros"', "3", "3 edits."), ('word1 = "intention", word2 = "execution"', "5", "5 edits.")],
    "burst-balloons": [("nums = [3,1,5,8]", "167", "Optimal order."), ("nums = [1,5]", "10", "Burst both.")],
    "regular-expression-matching": [('s = "aa", p = "a"', "false", "Not full."), ('s = "aa", p = "a*"', "true", "Star.")],
    "maximum-subarray": [("nums = [-2,1,-3,4,-1,2,1,-5,4]", "6", "Kadane [4,-1,2,1]."), ("nums = [1]", "1", "Single.")],
    "jump-game": [("nums = [2,3,1,1,4]", "true", "Can reach."), ("nums = [3,2,1,0,4]", "false", "Stuck.")],
    "jump-game-ii": [("nums = [2,3,1,1,4]", "2", "Min jumps."), ("nums = [2,3,0,1,4]", "2", "Min jumps.")],
    "gas-station": [("gas = [1,2,3,4,5], cost = [3,4,5,1,2]", "3", "Start index."), ("gas = [2,3,4], cost = [3,4,3]", "-1", "Impossible.")],
    "hand-of-straights": [("hand = [1,2,3,6,2,3,4,7,8], groupSize = 3", "true", "Groups."), ("hand = [1,2,3,4,5], groupSize = 4", "false", "Cannot.")],
    "merge-triplets-to-form-target-triplet": [("triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]", "true", "Can form."), ("triplets = [[3,4,5],[4,5,6]], target = [3,2,5]", "false", "Cannot.")],
    "partition-labels": [('s = "ababcbacadefegdehijhklij"', "[9,7,8]", "Parts."), ('s = "eccbbbbdec"', "[10]", "One part.")],
    "valid-parenthesis-string": [('s = "()"', "true", "Valid."), ('s = "(*)"', "true", "Star helps.")],
    "insert-interval": [("intervals = [[1,3],[6,9]], newInterval = [2,5]", "[[1,5],[6,9]]", "Merged."), ("intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]", "[[1,2],[3,10],[12,16]]", "Big merge.")],
    "merge-intervals": [("intervals = [[1,3],[2,6],[8,10],[15,18]]", "[[1,6],[8,10],[15,18]]", "Merged."), ("intervals = [[1,4],[4,5]]", "[[1,5]]", "Touching.")],
    "non-overlapping-intervals": [("intervals = [[1,2],[2,3],[3,4],[1,3]]", "1", "Remove one."), ("intervals = [[1,2],[1,2],[1,2]]", "2", "Remove two.")],
    "meeting-rooms": [("intervals = [[0,30],[5,10],[15,20]]", "false", "Overlap."), ("intervals = [[7,10],[2,4]]", "true", "No overlap.")],
    "meeting-rooms-ii": [("intervals = [[0,30],[5,10],[15,20]]", "2", "Rooms needed."), ("intervals = [[7,10],[2,4]]", "1", "One room.")],
    "minimum-interval-to-include-each-query": [("intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]", "[3,3,1,4]", "Min lengths."), ("intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]", "[2,-1,4,6]", "Some missing.")],
    "rotate-image": [("matrix 3x3", "rotated 90° clockwise", "In-place."), ("matrix 1x1", "same", "Trivial.")],
    "spiral-matrix": [("matrix = [[1,2,3],[4,5,6],[7,8,9]]", "[1,2,3,6,9,8,7,4,5]", "Spiral."), ("matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "[1,2,3,4,8,12,11,10,9,5,6,7]", "Spiral.")],
    "set-matrix-zeroes": [("matrix = [[1,1,1],[1,0,1],[1,1,1]]", "[[1,0,1],[0,0,0],[1,0,1]]", "Cross zeros."), ("matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]", "Multiple zeros.")],
    "happy-number": [("n = 19", "true", "Reaches 1."), ("n = 2", "false", "Cycle without 1.")],
    "plus-one": [("digits = [1,2,3]", "[1,2,4]", "Add one."), ("digits = [9]", "[1,0]", "Carry.")],
    "powx-n": [("x = 2.00000, n = 10", "1024.00000", "Power."), ("x = 2.00000, n = -2", "0.25000", "Inverse.")],
    "multiply-strings": [('num1 = "2", num2 = "3"', '"6"', "Product."), ('num1 = "123", num2 = "456"', '"56088"', "Product.")],
    "detect-squares": [("add points; count squares for queries", "counts", "Axis-aligned."), ("sparse points", "0", "No square.")],
    "single-number": [("nums = [2,2,1]", "1", "Lonely."), ("nums = [4,1,2,1,2]", "4", "XOR all.")],
    "number-of-1-bits": [("n = 11 (0b1011)", "3", "Three ones."), ("n = 128", "1", "One one.")],
    "counting-bits": [("n = 2", "[0,1,1]", "Popcounts."), ("n = 5", "[0,1,1,2,1,2]", "Popcounts.")],
    "reverse-bits": [("n = 000...00101", "reversed 32-bit", "Bit reverse."), ("n = 0", "0", "Zeros.")],
    "missing-number": [("nums = [3,0,1]", "2", "Missing 2."), ("nums = [0,1]", "2", "Missing 2.")],
    "sum-of-two-integers": [("a = 1, b = 2", "3", "Bit add."), ("a = 2, b = 3", "5", "Bit add.")],
    "reverse-integer": [("x = 123", "321", "Reversed."), ("x = -123", "-321", "Sign kept.")],
}

KID = {
    "jump-game": "You stand on lily pads. Each pad says how far you may hop forward. Can you reach the last pad without getting stuck?",
    "jump-game-ii": "Same lily pads, but now count the fewest hops to the end.",
    "gas-station": "Cars loop a circle of gas stations. Each stop gives gas but costs gas to drive to the next. Find a starting stop that lets you complete the loop.",
    "climbing-stairs": "A staircase. You can climb 1 or 2 steps at a time. How many different hop patterns reach the top?",
    "house-robber": "Houses in a line hold treasure. You may not rob two neighbors. What's the max loot?",
    "house-robber-ii": "Same treasure houses, but now they form a circle — first and last are neighbors too.",
    "coin-change": "A cashier drawer of coin types. What's the fewest coins to make exact change?",
    "maximum-subarray": "A row of daily profits and losses. Pick one contiguous stretch with the best total.",
    "number-of-islands": "A map of water and land squares. Land sticks to up/down/left/right neighbors. How many separate islands?",
    "course-schedule": "Classes with prerequisites. Can you finish them all without a loop of 'must take A before B before A'?",
    "rotting-oranges": "Fresh oranges rot when they touch a rotten neighbor each minute. How long until every orange is rotten?",
    "word-search": "A letter grid like a word search puzzle. Can your finger trace the word without reusing a square?",
    "invert-binary-tree": "A family tree of balloons. Swap every left child with its right child, all the way down — make a mirror.",
    "valid-palindrome": "Ignore spaces and punctuation. Do the letters and digits read the same forwards and backwards?",
    "longest-substring-without-repeating-characters": "Slide a window along a string. Inside the window, every letter must be unique. How wide can it get?",
    "merge-intervals": "Busy blocks on a calendar overlap. Glue overlapping blocks into combined busy times.",
    "single-number": "Every number appears twice except one lonely number. Find the loner (XOR is a magic flashlight).",
}


def to_examples(triples):
    return [
        {"input": a, "output": b, "explanation": c}
        for a, b, c in triples
    ]


def kid_from_idea(title: str, idea: str | None, category: str) -> str:
    if idea:
        # Turn technical key idea into kid voice without dumping jargon raw
        short = idea
        short = re.sub(r"\s+", " ", short).strip()
        if len(short) > 280:
            short = short[:277] + "…"
        return (
            f"Picture the puzzle '{title}'. "
            f"Here is the clever trick in plain words: {short} "
            f"We will still start slow, then use this trick so it becomes fast."
        )
    return (
        f"'{title}' is a puzzle in the {category.replace('-', ' ')} family. "
        f"We tell a story, try a slow plan, then upgrade to the pattern interviewers listen for."
    )


def main():
    fixed_ex = 0
    fixed_kid = 0
    for meta in CATALOG["problems"]:
        slug = meta["slug"]
        path = PROBS / f"{slug}.json"
        doc = json.loads(path.read_text())

        if slug in EXAMPLES:
            doc["examples"] = to_examples(EXAMPLES[slug])
            fixed_ex += 1
        else:
            # should not happen if EX complete
            doc["examples"] = [
                {
                    "input": f"Use LeetCode example 1 for {meta['title']}",
                    "output": "match official",
                    "explanation": "Work the official sample by hand beside the animation.",
                },
                {
                    "input": f"Use LeetCode example 2 for {meta['title']}",
                    "output": "match official",
                    "explanation": "Then invent one tiny edge case of your own.",
                },
            ]

        kid = doc.get("kidExplanation", "")
        if slug in KID:
            doc["kidExplanation"] = KID[slug]
            fixed_kid += 1
        elif kid.startswith("Story version:") or "puzzle game" in kid or "Imagine '" in kid:
            # pull idea from python header if present
            idea = None
            m = re.search(r"^# Idea: (.+)$", doc["solutions"]["python"], re.M)
            if m:
                idea = m.group(1).rstrip("…")
            doc["kidExplanation"] = kid_from_idea(meta["title"], idea, meta["category"])
            fixed_kid += 1

        # Ensure defaultInput is JSON-serializable sensible for arrays category
        if isinstance(doc["animation"].get("defaultInput"), dict) and doc["animation"]["defaultInput"] == {"demo": True}:
            if doc["animation"]["visualType"] in ("array", "hash", "heap", "bits", "dp"):
                doc["animation"]["defaultInput"] = [1, 2, 3, 2]
            elif doc["animation"]["visualType"] == "stack":
                doc["animation"]["defaultInput"] = "()[]"
            elif doc["animation"]["visualType"] == "intervals":
                doc["animation"]["defaultInput"] = {"intervals": [[1, 3], [2, 6], [8, 10]]}

        path.write_text(json.dumps(doc, indent=2) + "\n")

    missing = [m["slug"] for m in CATALOG["problems"] if m["slug"] not in EXAMPLES]
    print(f"examples_applied={fixed_ex} kid_fixed={fixed_kid} missing_examples={missing}")


if __name__ == "__main__":
    main()
