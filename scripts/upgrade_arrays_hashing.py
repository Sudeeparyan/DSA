#!/usr/bin/env python3
"""Upgrade Arrays & Hashing problems to full teaching quality."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "content/problems"

DATA = {
    "valid-anagram": {
        "kidExplanation": "Two piles of letter tiles. If you can rearrange pile A to look exactly like pile B, they are anagrams — same letters, same counts, maybe different order.",
        "plainProblem": "Given two strings s and t, return true if t is an anagram of s (same characters with the same frequencies).",
        "examples": [
            {"input": 's = "anagram", t = "nagaram"', "output": "true", "explanation": "Same letters rearranged."},
            {"input": 's = "rat", t = "car"', "output": "false", "explanation": "Different letters."},
        ],
        "thinkingSteps": [
            {"title": "Brute force idea", "body": "Sort both strings and compare. Easy to understand."},
            {"title": "Why sorting may be enough", "body": "Sorting is O(n log n). Fine for interviews, but counting can be linear."},
            {"title": "Aha insight", "body": "Anagrams have identical character counts. A hash map (or 26 counters) remembers frequencies."},
            {"title": "Better idea", "body": "Count letters in s, subtract letters in t (or compare two maps). If all counts end at zero, they match."},
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "We scan each string once; map updates are average O(1).",
            "space": "O(1)",
            "spaceReason": "If we only use lowercase English letters, 26 counters are constant space (or O(k) for alphabet size).",
        },
        "python": '''class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Different lengths can never be anagrams
        if len(s) != len(t):
            return False

        # Count letters in each string (hash maps)
        countS, countT = {}, {}

        for i in range(len(s)):
            # Add one for this letter in s
            countS[s[i]] = 1 + countS.get(s[i], 0)
            # Add one for this letter in t
            countT[t[i]] = 1 + countT.get(t[i], 0)
        # Compare the two notebooks of counts
        return countS == countT
''',
        "interviewApproachNotes": "Counting with a hash map (or 26-length array) is the classic O(n) interview answer. Mention sorting as a clear alternative.",
        "defaultInput": ["anagram", "nagaram"],
    },
    "group-anagrams": {
        "kidExplanation": "A box of words. Words that are rearrangements of each other sit at the same lunch table. We need every table of anagram friends.",
        "plainProblem": "Group strings that are anagrams of each other. Return the groups in any order.",
        "examples": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]', "explanation": "Groups share letter counts."},
            {"input": 'strs = [""]', "output": '[[""]]', "explanation": "Single empty string."},
        ],
        "thinkingSteps": [
            {"title": "Brute force idea", "body": "Compare every pair to see if they are anagrams. Too many comparisons."},
            {"title": "Aha insight", "body": "Anagrams share a signature: sorted letters, or a count tuple."},
            {"title": "Better idea", "body": "Map signature → list of words. One pass builds all groups."},
            {"title": "Why it is fast", "body": "Each word is processed once; sorting letters of a word costs its length."},
        ],
        "complexity": {
            "time": "O(n * k log k)",
            "timeReason": "n words; sorting each word of length k costs k log k (count-signature is O(n*k)).",
            "space": "O(n * k)",
            "spaceReason": "We store all words in the groups map.",
        },
        "interviewApproachNotes": "Signature via sorted string or 26-count tuple is optimal interview style. Prefer count tuple if you want strictly O(n*k).",
    },
    "top-k-frequent-elements": {
        "kidExplanation": "Numbers shout how often they appear. You only want the k loudest voices on the podium.",
        "plainProblem": "Return the k most frequent elements in the array. Order among the top-k does not matter.",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears thrice, 2 twice."},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Only one element."},
        ],
        "thinkingSteps": [
            {"title": "Brute force idea", "body": "Count frequencies, sort all unique numbers by count, take k."},
            {"title": "Why sorting works", "body": "Simple, O(m log m) for m unique values."},
            {"title": "Aha insight", "body": "Bucket sort by frequency: index = count, values = numbers with that count."},
            {"title": "Better idea", "body": "Fill frequency buckets, then walk from high frequency down until you collect k numbers."},
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "Counting is O(n); bucket walk is O(n) because total bucket entries equal n.",
            "space": "O(n)",
            "spaceReason": "Frequency map and buckets store up to n items.",
        },
        "interviewApproachNotes": "Bucket sort by frequency is the NeetCode favorite and impresses more than sorting when you explain why it is linear. Heap of size k is also acceptable O(n log k).",
    },
    "product-of-array-except-self": {
        "kidExplanation": "Each kid wants the product of everyone else's scores — not their own — and you are not allowed to use division.",
        "plainProblem": "Return an array answer where answer[i] equals the product of all elements except nums[i]. O(n) without division.",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]", "explanation": "For index 0: 2*3*4=24."},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]", "explanation": "Zeros affect products carefully."},
        ],
        "thinkingSteps": [
            {"title": "Brute force idea", "body": "For each i, multiply everything except i. O(n²)."},
            {"title": "Division trick (not allowed / fragile)", "body": "Total product / nums[i] breaks on zeros and is often disallowed."},
            {"title": "Aha insight", "body": "answer[i] = product of left side × product of right side."},
            {"title": "Better idea", "body": "One pass builds prefix products into the output; a second pass multiplies suffix products."},
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "Two linear passes over the array.",
            "space": "O(1)",
            "spaceReason": "Output array does not count as extra space per the usual problem note; only a few variables otherwise.",
        },
        "interviewApproachNotes": "Prefix/suffix products without division is the expected optimal answer. Draw left and right products on the board.",
    },
    "valid-sudoku": {
        "kidExplanation": "A Sudoku page. Every row, every column, and every 3×3 box may show each digit at most once. Empty cells are fine.",
        "plainProblem": "Determine if a 9×9 board is valid Sudoku so far (not necessarily solvable). '.' means empty.",
        "examples": [
            {"input": "board with one duplicate in a row", "output": "false", "explanation": "A repeated digit breaks validity."},
            {"input": "partial valid board", "output": "true", "explanation": "No conflicts yet."},
        ],
        "thinkingSteps": [
            {"title": "Brute force idea", "body": "For each filled cell, scan its row, column, and box."},
            {"title": "Aha insight", "body": "Keep three families of hash sets: rows, cols, boxes."},
            {"title": "Better idea", "body": "One pass: if a digit already sits in that row/col/box set, invalid; else add it."},
            {"title": "Box index trick", "body": "box = (r // 3) * 3 + (c // 3) labels the nine boxes."},
        ],
        "complexity": {
            "time": "O(1)",
            "timeReason": "The board is fixed 9×9, so work is constant (or O(n²) for an n×n generalization).",
            "space": "O(1)",
            "spaceReason": "At most 9×9 entries across the sets for a standard board.",
        },
        "interviewApproachNotes": "Hash sets per row/col/box is the clear interview solution. Mention the box index formula out loud.",
    },
    "encode-and-decode-strings": {
        "kidExplanation": "Pack many postcards into one suitcase string, then unpack them later without mixing — even if a postcard contains commas or weird marks.",
        "plainProblem": "Design encode/decode for a list of strings so encode(decode(strs)) restores the original list.",
        "examples": [
            {"input": '["lint","code","love","you"]', "output": '["lint","code","love","you"]', "explanation": "Round-trip must be perfect."},
            {"input": '["we","say",":","yes"]', "output": '["we","say",":","yes"]', "explanation": "Delimiters inside strings must not break parsing."},
        ],
        "thinkingSteps": [
            {"title": "Naive delimiter", "body": "Joining with commas fails if a string contains commas."},
            {"title": "Aha insight", "body": "Store length prefixes: 4#lint4#code … so you always know how many characters to read."},
            {"title": "Better idea", "body": "Encode walks strings appending len + '#' + body. Decode reads numbers until '#', then slices."},
            {"title": "Why interviewers like it", "body": "Shows careful parsing and edge-case thinking."},
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "We read and write each character a constant number of times.",
            "space": "O(n)",
            "spaceReason": "The encoded string and decoded list hold all character data.",
        },
        "interviewApproachNotes": "Length-prefix encoding is the standard robust answer. Do not invent escaping schemes that are hard to prove correct under pressure.",
    },
    "longest-consecutive-sequence": {
        "kidExplanation": "Numbered beads in a bag. Ignore the bag order. What is the longest run of neighbors like 3–4–5–6?",
        "plainProblem": "Return the length of the longest consecutive elements sequence. Aim for O(n).",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4", "explanation": "1,2,3,4 is length 4."},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9", "explanation": "0 through 8."},
        ],
        "thinkingSteps": [
            {"title": "Brute force idea", "body": "Sort, then scan streaks. O(n log n)."},
            {"title": "Aha insight", "body": "Put numbers in a hash set. A streak should start only when num-1 is missing."},
            {"title": "Better idea", "body": "For each start, walk num+1, num+2… while present, tracking the best length."},
            {"title": "Why O(n)", "body": "Each number is visited a constant number of times across all walks."},
        ],
        "complexity": {
            "time": "O(n)",
            "timeReason": "Set builds in O(n); consecutive walks amortize to O(n).",
            "space": "O(n)",
            "spaceReason": "The hash set stores unique numbers.",
        },
        "interviewApproachNotes": "Hash-set start-of-streak method is the O(n) interview target. Sorting is the honest fallback if hashing is disallowed.",
    },
}


def main():
    for slug, meta in DATA.items():
        path = P / f"{slug}.json"
        doc = json.loads(path.read_text())
        for k in ("kidExplanation", "plainProblem", "examples", "thinkingSteps", "complexity", "interviewApproachNotes"):
            if k in meta:
                doc[k] = meta[k]
        if "python" in meta:
            doc["solutions"]["python"] = meta["python"]
        if "defaultInput" in meta:
            doc["animation"]["defaultInput"] = meta["defaultInput"]
        doc["hasStory"] = True
        doc["hasAnimation"] = True
        doc["hasCode"] = True
        doc["edgeCases"] = doc.get("edgeCases") or [
            "Empty input",
            "Single element",
            "Duplicates / already-best arrangement",
        ]
        doc["commonMistakes"] = doc.get("commonMistakes") or [
            "Skipping the brute-force explanation",
            "Wrong complexity for the approach you coded",
            "Off-by-one on indices",
        ]
        doc["interviewTips"] = [
            f"Name the pattern: {doc['pattern']['name']}.",
            "Walk example 1 aloud before coding.",
            f"State {doc['complexity']['time']} time and {doc['complexity']['space']} space at the end.",
        ]
        path.write_text(json.dumps(doc, indent=2) + "\n")
        print("upgraded", slug)
    # mark progress
    prog = (ROOT / "PROGRESS.md").read_text()
    for slug in list(DATA) + ["contains-duplicate", "two-sum"]:
        # mark lines containing the slug
        lines = []
        for line in prog.splitlines():
            if f"(`{slug}`)" in line:
                line = line.replace("- [ ]", "- [x]")
            lines.append(line)
        prog = "\n".join(lines) + "\n"
    (ROOT / "PROGRESS.md").write_text(prog)


if __name__ == "__main__":
    main()
