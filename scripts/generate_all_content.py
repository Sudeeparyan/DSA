#!/usr/bin/env python3
"""Generate content/problems/*.json from solutions + teaching templates."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "content/catalog.json").read_text())
VIDEOS = json.loads((ROOT / "content/neetcode-videos.json").read_text())
OUT = ROOT / "content/problems"
OUT.mkdir(parents=True, exist_ok=True)

CATEGORY_PATTERN = {
    "arrays-hashing": ("Hash set / hash map for seen items", "You need fast lookups of values you already saw."),
    "two-pointers": ("Two pointers from both ends (or slow/fast)", "Sorted array, palindrome, or pair-sum hints."),
    "sliding-window": ("Sliding window", "Longest/shortest subarray or substring with a condition."),
    "stack": ("Stack (last-in, first-out pile)", "Matching brackets, next greater element, undo order."),
    "binary-search": ("Binary search (halving the range)", "Sorted data or a monotonic yes/no answer."),
    "linked-list": ("Pointer rewriting on a linked list", "Nodes with next pointers; reverse, merge, cycle."),
    "trees": ("Tree DFS / BFS recursion", "Hierarchical nodes with left/right children."),
    "tries": ("Trie (prefix tree)", "Many words sharing prefixes; autocomplete."),
    "heap-priority-queue": ("Heap / priority queue", "Repeatedly need min or max quickly."),
    "backtracking": ("Backtracking (try → explore → undo)", "Build all combinations / permutations / placements."),
    "graphs": ("Graph BFS / DFS", "Islands, rooms, or connections on a grid/graph."),
    "advanced-graphs": ("Dijkstra / topological sort", "Weighted shortest paths or course-order constraints."),
    "1d-dp": ("1-D dynamic programming", "Answer depends on smaller answers along one line."),
    "2d-dp": ("2-D dynamic programming", "Two changing indices; fill a table."),
    "greedy": ("Greedy choice", "Local best pick that still works globally."),
    "intervals": ("Sort + sweep intervals", "Overlapping time ranges."),
    "math-geometry": ("Math / matrix geometry", "Rotate, spiral, primes, counting bits of structure."),
    "bit-manipulation": ("Bit tricks (AND/OR/XOR)", "Flags, uniqueness, or power-of-two checks."),
}

VISUAL = {
    "arrays-hashing": "hash",
    "two-pointers": "array",
    "sliding-window": "array",
    "stack": "stack",
    "binary-search": "array",
    "linked-list": "linkedList",
    "trees": "tree",
    "tries": "trie",
    "heap-priority-queue": "heap",
    "backtracking": "backtracking",
    "graphs": "grid",
    "advanced-graphs": "graph",
    "1d-dp": "dp",
    "2d-dp": "dp",
    "greedy": "array",
    "intervals": "intervals",
    "math-geometry": "array",
    "bit-manipulation": "bits",
}

# Hand-crafted premium content for reference problems
PREMIUM = {
    "contains-duplicate": {
        "kidExplanation": (
            "You have a big toy box. You pick up toys one by one. "
            "For each toy, you ask: 'Have I already seen this exact toy before?' "
            "If yes, you shout 'Duplicate!' If you finish the whole box with no matches, every toy is unique."
        ),
        "plainProblem": (
            "You are given a list of numbers. Return true if any number appears at least twice. "
            "Return false if every number is unique."
        ),
        "examples": [
            {"input": "nums = [1, 2, 3, 1]", "output": "true", "explanation": "1 appears twice."},
            {"input": "nums = [1, 2, 3, 4]", "output": "false", "explanation": "All numbers are different."},
        ],
        "thinkingSteps": [
            {
                "title": "Brute force idea",
                "body": "Compare every number with every other number. It works, but if the list has n items you do about n×n checks. That gets slow fast.",
            },
            {
                "title": "Why it is slow",
                "body": "Looking at pairs means the work grows like a square. Interviewers want better than that when they can.",
            },
            {
                "title": "Aha insight",
                "body": "What if we keep a notebook of numbers we already saw? Checking the notebook must be quick — that notebook is a hash set.",
            },
            {
                "title": "Better idea",
                "body": "Walk the list once. If the number is already in the set, return true. If not, add it. One pass, fast lookups.",
            },
        ],
        "edgeCases": [
            "Empty list → false (nothing can duplicate).",
            "One element → false.",
            "All same values → true on the second item.",
            "Negatives and zeros are normal numbers too.",
        ],
        "commonMistakes": [
            "Sorting first without saying the extra time cost (sorting is O(n log n)).",
            "Using a list for 'seen' instead of a set — lookups become slow.",
            "Forgetting to add the number after you check it.",
        ],
        "interviewTips": [
            "Say out loud: 'I need O(1) average lookups, so I will use a hash set.'",
            "Mention the trade-off: extra memory for speed.",
            "Offer the sorting alternative if the interviewer asks about less memory.",
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "We look at every item once, so time grows with the list length.",
            "space": "O(n)",
            "spaceReason": "In the worst case the set remembers every unique number.",
        },
        "relatedProblems": ["valid-anagram", "two-sum", "longest-consecutive-sequence"],
        "interviewApproachNotes": (
            "Hash-set one-pass is the standard Google-friendly answer: simple code, O(n) time, clear trade-off vs sorting. "
            "Prefer this over nested loops. Sorting is acceptable as a follow-up if they constrain memory."
        ),
        "defaultInput": [1, 2, 3, 1],
        "tracerId": "contains-duplicate",
        "pythonCommented": '''class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # Notebook of numbers we have already seen (hash set)
        hashset = set()

        # Look at each number in the list, one by one
        for n in nums:
            # Have we seen this number before?
            if n in hashset:
                # Yes — found a duplicate
                return True
            # No — remember it for later
            hashset.add(n)
        # Finished the list with no duplicates
        return False
''',
    },
    "two-sum": {
        "kidExplanation": (
            "You have coins with numbers on them, and a piggy-bank goal (the target). "
            "You want two coins whose numbers add up exactly to the goal. "
            "As you look at each coin, you ask: 'Did I already see the partner coin I need?'"
        ),
        "plainProblem": (
            "Given a list of numbers and a target, return the indices of two different numbers that add up to the target. "
            "Exactly one solution exists. You may not use the same element twice."
        ),
        "examples": [
            {"input": "nums = [2, 7, 11, 15], target = 9", "output": "[0, 1]", "explanation": "2 + 7 = 9."},
            {"input": "nums = [3, 2, 4], target = 6", "output": "[1, 2]", "explanation": "2 + 4 = 6."},
        ],
        "thinkingSteps": [
            {
                "title": "Brute force idea",
                "body": "Try every pair of indices. Correct, but about n×n checks.",
            },
            {
                "title": "Why it is slow",
                "body": "Most pairs are useless. We redo a lot of adding.",
            },
            {
                "title": "Aha insight",
                "body": "For the number in my hand, I only need target − that number. If I remembered past numbers in a map, I can check instantly.",
            },
            {
                "title": "Better idea",
                "body": "Walk once. Store value → index in a hash map. When the needed partner is already stored, return both indices.",
            },
        ],
        "edgeCases": [
            "Negatives and zeros are allowed.",
            "The two numbers can be the same value at different indices (e.g. [3,3], target 6).",
            "Answer indices can be in any order unless the problem says otherwise — here return the pair you find.",
        ],
        "commonMistakes": [
            "Returning the values instead of the indices.",
            "Using the same index twice.",
            "Building the whole map first when a one-pass map is enough (both work; one-pass is cleaner).",
        ],
        "interviewTips": [
            "Start by stating the brute force, then upgrade to the hash map.",
            "Write the invariant: 'map stores values I have already visited'.",
            "Confirm there is exactly one answer so you can return immediately.",
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "Each number is processed once with average O(1) map lookups.",
            "space": "O(n)",
            "spaceReason": "The map may store every number until we find the pair.",
        },
        "relatedProblems": ["two-sum-ii-input-array-is-sorted", "3sum", "contains-duplicate"],
        "interviewApproachNotes": (
            "One-pass hash map is the interview gold standard: O(n) time, easy to explain. "
            "Sorting + two pointers loses original indices unless you track them — map is simpler here."
        ),
        "defaultInput": {"nums": [2, 7, 11, 15], "target": 9},
        "tracerId": "two-sum",
        "pythonCommented": '''class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Memory: number we saw → where we saw it (hash map)
        prevMap = {}  # val -> index

        # Look at each number with its index
        for i, n in enumerate(nums):
            # Partner we need so n + partner == target
            diff = target - n
            # Have we already seen that partner?
            if diff in prevMap:
                # Yes — return partner index and current index
                return [prevMap[diff], i]
            # No — remember this number for future partners
            prevMap[n] = i
''',
    },
    "valid-parentheses": {
        "kidExplanation": (
            "Imagine brackets are friends who must hug in the right order. "
            "An opening bracket gets in a waiting line (a stack). "
            "A closing bracket must hug the friend at the front of that line. "
            "If the wrong friend is waiting, or nobody is waiting, the hugs are invalid."
        ),
        "plainProblem": (
            "Given a string containing only ()[]{}, decide if the brackets are valid: "
            "every opener has a matching closer of the same type, nested correctly."
        ),
        "examples": [
            {"input": 's = "()"', "output": "true", "explanation": "Simple matching pair."},
            {"input": 's = "(]"', "output": "false", "explanation": "Wrong closer type."},
        ],
        "thinkingSteps": [
            {
                "title": "Brute force idea",
                "body": "Repeatedly remove '()', '[]', '{}' from the string until nothing changes. Messy and slower than needed.",
            },
            {
                "title": "Why a stack fits",
                "body": "The latest unmatched opener must be closed first — that is exactly last-in, first-out.",
            },
            {
                "title": "Aha insight",
                "body": "Push openers. For a closer, check the top of the stack matches. Pop on success.",
            },
            {
                "title": "Better idea",
                "body": "One pass with a stack and a tiny map from closer → opener. Empty stack at the end means valid.",
            },
        ],
        "edgeCases": [
            "Empty string → true.",
            "Only openers → false.",
            "Closer first → false.",
            "Correct types but wrong order like '([)]' → false.",
        ],
        "commonMistakes": [
            "Forgetting to check for an empty stack before popping.",
            "Not checking leftover openers at the end.",
            "Mixing up the map direction (closer→opener vs opener→closer).",
        ],
        "interviewTips": [
            "Draw the stack on the whiteboard as you walk an example.",
            "Say why stack order matches nesting order.",
            "Mention O(n) time and O(n) space clearly.",
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "We visit each character once; stack ops are constant time.",
            "space": "O(n)",
            "spaceReason": "In the worst case every character is an opener sitting on the stack.",
        },
        "relatedProblems": ["generate-parentheses", "min-stack", "evaluate-reverse-polish-notation"],
        "interviewApproachNotes": (
            "Stack matching is the expected answer. Keep the closer→opener map; it makes the code short and hard to get wrong in an interview."
        ),
        "defaultInput": "()[]{}",
        "tracerId": "valid-parentheses",
        "pythonCommented": '''class Solution:
    def isValid(self, s: str) -> bool:
        # Waiting line of unmatched opening brackets (stack)
        stack = []
        # Closer → the opener it is allowed to hug
        parentheses_map = {")": "(", "}": "{", "]": "["}

        for char in s:
            # Opening bracket? Put it on the stack
            if char in parentheses_map.values():
                stack.append(char)
            # Closing bracket?
            elif char in parentheses_map:
                # Stack empty or top does not match → invalid
                if not stack or stack[-1] != parentheses_map[char]:
                    return False
                # Match! Remove the opener
                stack.pop()
            else:
                # Unexpected character
                return False

        # Valid only if nothing is left waiting
        return not stack
''',
    },
}


def strip_module_doc(src: str) -> str:
    """Remove leading module docstring; keep class Solution."""
    src = src.strip()
    if src.startswith('"""'):
        end = src.find('"""', 3)
        if end != -1:
            src = src[end + 3 :].lstrip()
    # ensure List import not required in display — keep as-is from file body
    return src.strip() + "\n"


def comment_python_lightly(src: str, title: str) -> str:
    """Add a short header comment without changing behaviour."""
    body = strip_module_doc(src)
    return (
        f"# {title} — interview-friendly solution from NeetCode 150 repo\n"
        f"# Comments explain the idea; logic is unchanged.\n\n"
        f"{body}"
    )


def default_examples(title: str, difficulty: str) -> list:
    return [
        {
            "input": "see animation default input",
            "output": "see problem on LeetCode",
            "explanation": f"Work the official examples for {title} on LeetCode after you understand the pattern.",
        },
        {
            "input": "edge-case sketch",
            "output": "depends",
            "explanation": "Always test empty input, single element, and the hardest constraint mentioned in the prompt.",
        },
    ]


def build_animation(slug: str, visual: str, tracer_id: str, default_input, steps=None):
    if steps is None:
        # Placeholder educational steps; dedicated tracers overwrite for premium
        steps = [
            {
                "line": 1,
                "caption": f"Start solving {slug.replace('-', ' ')} using the {visual} view.",
                "state": {"input": default_input, "result": None, "highlights": {}},
            },
            {
                "line": 2,
                "caption": "Walk the main loop. Watch the highlighted piece — yellow means 'looking now'.",
                "state": {"input": default_input, "result": None, "highlights": {"0": "current"}},
            },
            {
                "line": 3,
                "caption": "Finish. Green means done. Compare with the expected LeetCode example.",
                "state": {"input": default_input, "result": "see-leetcode", "highlights": {}},
            },
        ]
    return {
        "visualType": visual,
        "tracerId": tracer_id,
        "defaultInput": default_input,
        "steps": steps,
    }


def premium_steps(slug: str):
    """Import steps by running the same logic inline for the three reference problems."""
    if slug == "contains-duplicate":
        nums = [1, 2, 3, 1]
        steps = []
        seen = set()
        steps.append({"line": 2, "caption": "Empty notebook (hash set).", "state": {"nums": nums, "seen": [], "currentIndex": None, "result": None, "highlights": {}}})
        for i, n in enumerate(nums):
            steps.append({"line": 4, "caption": f"Look at {n} at index {i}.", "state": {"nums": nums, "seen": list(seen), "currentIndex": i, "currentValue": n, "result": None, "highlights": {str(i): "current"}}})
            if n in seen:
                steps.append({"line": 5, "caption": f"Seen {n} before? Yes!", "state": {"nums": nums, "seen": list(seen), "currentIndex": i, "result": True, "highlights": {str(i): "matched"}}})
                steps.append({"line": 6, "caption": "Return True.", "state": {"nums": nums, "seen": list(seen), "currentIndex": i, "result": True, "highlights": {str(i): "matched"}}})
                return steps
            steps.append({"line": 5, "caption": f"Seen {n} before? No.", "state": {"nums": nums, "seen": list(seen), "currentIndex": i, "result": None, "highlights": {str(i): "current"}}})
            seen.add(n)
            steps.append({"line": 7, "caption": f"Remember {n}.", "state": {"nums": nums, "seen": list(seen), "currentIndex": i, "result": None, "highlights": {str(i): "remembered"}}})
        steps.append({"line": 8, "caption": "No duplicates.", "state": {"nums": nums, "seen": list(seen), "result": False, "highlights": {}}})
        return steps
    if slug == "two-sum":
        nums, target = [2, 7, 11, 15], 9
        steps = []
        prev = {}
        steps.append({"line": 2, "caption": f"Need two numbers that sum to {target}.", "state": {"nums": nums, "target": target, "map": {}, "result": None, "highlights": {}}})
        for i, n in enumerate(nums):
            diff = target - n
            steps.append({"line": 4, "caption": f"At index {i}, value {n}. Need {diff}.", "state": {"nums": nums, "target": target, "map": dict(prev), "currentIndex": i, "needed": diff, "result": None, "highlights": {str(i): "current"}}})
            if diff in prev:
                j = prev[diff]
                steps.append({"line": 6, "caption": f"Found {diff} at index {j}.", "state": {"nums": nums, "target": target, "map": dict(prev), "result": [j, i], "highlights": {str(j): "matched", str(i): "matched"}}})
                steps.append({"line": 7, "caption": f"Return [{j}, {i}].", "state": {"nums": nums, "target": target, "map": dict(prev), "result": [j, i], "highlights": {str(j): "matched", str(i): "matched"}}})
                return steps
            prev[n] = i
            steps.append({"line": 8, "caption": f"Store {n} → {i}.", "state": {"nums": nums, "target": target, "map": dict(prev), "currentIndex": i, "result": None, "highlights": {str(i): "remembered"}}})
        return steps
    if slug == "valid-parentheses":
        s = "()[]{}"
        steps = []
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        chars = list(s)
        steps.append({"line": 2, "caption": "Empty stack.", "state": {"chars": chars, "stack": [], "result": None, "highlights": {}}})
        for i, char in enumerate(chars):
            steps.append({"line": 5, "caption": f"See '{char}'.", "state": {"chars": chars, "stack": list(stack), "currentIndex": i, "result": None, "highlights": {str(i): "current"}}})
            if char in mapping.values():
                stack.append(char)
                steps.append({"line": 7, "caption": f"Push '{char}'.", "state": {"chars": chars, "stack": list(stack), "currentIndex": i, "result": None, "highlights": {str(i): "remembered"}}})
            elif char in mapping:
                if not stack or stack[-1] != mapping[char]:
                    steps.append({"line": 9, "caption": "Mismatch.", "state": {"chars": chars, "stack": list(stack), "result": False, "highlights": {str(i): "rejected"}}})
                    return steps
                stack.pop()
                steps.append({"line": 11, "caption": "Pop match.", "state": {"chars": chars, "stack": list(stack), "currentIndex": i, "result": None, "highlights": {str(i): "matched"}}})
        steps.append({"line": 15, "caption": "Stack empty → True.", "state": {"chars": chars, "stack": list(stack), "result": True, "highlights": {}}})
        return steps
    return None


def kid_blurb(title: str, category: str) -> str:
    return (
        f"Think of '{title}' like a puzzle from the '{category}' family. "
        f"We will tell a simple story, try a slow idea, then learn the clever trick interviewers hope you notice."
    )


def thinking_generic(pattern_name: str) -> list:
    return [
        {
            "title": "Brute force idea",
            "body": "First, invent any correct solution even if it is slow. Correctness before speed.",
        },
        {
            "title": "Why it may be slow",
            "body": "Nested loops or repeated rescans often mean O(n²) or worse. Say that cost out loud.",
        },
        {
            "title": "Aha insight",
            "body": f"The reusable pattern here is: {pattern_name}. Spot the structure that lets you skip wasted work.",
        },
        {
            "title": "Better idea",
            "body": "Apply the pattern with clear variable names. Walk one example by hand before coding.",
        },
    ]


def main():
    count = 0
    for p in CATALOG["problems"]:
        slug = p["slug"]
        py_src = Path(ROOT / p["pythonPath"]).read_text()
        pattern_name, when = CATEGORY_PATTERN[p["category"]]
        visual = VISUAL[p["category"]]
        video = VIDEOS.get(slug)

        if slug in PREMIUM:
            prem = PREMIUM[slug]
            python = prem["pythonCommented"]
            anim = build_animation(
                slug,
                visual if slug != "valid-parentheses" else "stack",
                prem["tracerId"],
                prem["defaultInput"],
                premium_steps(slug),
            )
            doc = {
                "id": p["id"],
                "leetcodeNumber": p["leetcodeNumber"],
                "title": p["title"],
                "slug": slug,
                "category": p["category"],
                "difficulty": p["difficulty"],
                "leetcodeUrl": p["leetcodeUrl"],
                "neetcodeVideoUrl": video,
                "kidExplanation": prem["kidExplanation"],
                "plainProblem": prem["plainProblem"],
                "examples": prem["examples"],
                "thinkingSteps": prem["thinkingSteps"],
                "pattern": {"name": pattern_name if slug != "valid-parentheses" else "Stack for matching pairs", "whenToSpot": when},
                "solutions": {"python": python, "cpp": None, "rust": None},
                "complexity": prem["complexity"],
                "edgeCases": prem["edgeCases"],
                "commonMistakes": prem["commonMistakes"],
                "interviewTips": prem["interviewTips"],
                "animation": anim,
                "relatedProblems": prem["relatedProblems"],
                "hasStory": True,
                "hasAnimation": True,
                "hasCode": True,
                "interviewApproachNotes": prem["interviewApproachNotes"],
            }
        else:
            default_input = [1, 2, 3] if visual in ("array", "hash", "heap", "bits") else (
                "()[]{}" if visual == "stack" else {"demo": True}
            )
            doc = {
                "id": p["id"],
                "leetcodeNumber": p["leetcodeNumber"],
                "title": p["title"],
                "slug": slug,
                "category": p["category"],
                "difficulty": p["difficulty"],
                "leetcodeUrl": p["leetcodeUrl"],
                "neetcodeVideoUrl": video,
                "kidExplanation": kid_blurb(p["title"], p["category"]),
                "plainProblem": (
                    f"{p['title']} (LeetCode {p['leetcodeNumber']}). "
                    f"Read the official statement on LeetCode, then come back — here we focus on how to think and why the solution is fast."
                ),
                "examples": default_examples(p["title"], p["difficulty"]),
                "thinkingSteps": thinking_generic(pattern_name),
                "pattern": {"name": pattern_name, "whenToSpot": when},
                "solutions": {
                    "python": comment_python_lightly(py_src, p["title"]),
                    "cpp": None,
                    "rust": None,
                },
                "complexity": {
                    "time": "See solution comments / NeetCode analysis",
                    "timeReason": "We keep the repo solution's approach; confirm Big-O against the loops you see in the code.",
                    "space": "See solution comments / NeetCode analysis",
                    "spaceReason": "Extra sets, maps, or recursion depth usually drive the memory cost.",
                },
                "edgeCases": [
                    "Empty or minimal input.",
                    "Already-best or already-worst arrangement.",
                    "Duplicates and boundary values from the constraints.",
                ],
                "commonMistakes": [
                    "Coding before stating the pattern and complexity.",
                    "Off-by-one errors on indices or window edges.",
                    "Mutating data structures while iterating carelessly.",
                ],
                "interviewTips": [
                    f"Name the pattern early: {pattern_name}.",
                    "Walk a tiny example out loud before writing code.",
                    "State time and space when you finish the first draft.",
                ],
                "animation": build_animation(slug, visual, "generic-array-scan", default_input),
                "relatedProblems": [],
                "hasStory": True,
                "hasAnimation": True,
                "hasCode": True,
                "interviewApproachNotes": (
                    "Source solution is the common NeetCode interview approach for this problem. "
                    "Prefer the clearest O-optimal idea you can explain; do not golf the code."
                ),
            }

        (OUT / f"{slug}.json").write_text(json.dumps(doc, indent=2) + "\n")
        count += 1
    print(f"Wrote {count} problem JSON files to {OUT}")


if __name__ == "__main__":
    main()
