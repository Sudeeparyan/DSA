#!/usr/bin/env python3
"""Enrich problem JSON with docstring complexity, unique stories, and related links."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "content/catalog.json").read_text())
PROBLEMS = ROOT / "content/problems"

STORIES = {
    "valid-anagram": "Two word-boxes of fridge magnets. Can you rearrange the first box to spell the second word exactly? Same letters, same counts.",
    "group-anagrams": "A classroom of words. Put classmates who are rearrangements of each other into the same lunch table.",
    "top-k-frequent-elements": "A popularity contest. Count how often each number appears, then crown the k loudest numbers.",
    "product-of-array-except-self": "Each kid wants the product of everyone else's scores — but not their own — without using division.",
    "valid-sudoku": "Check a Sudoku sheet: every row, column, and 3×3 box may hold each digit at most once.",
    "encode-and-decode-strings": "Pack many messages into one suitcase string, then unpack them perfectly later — even if messages contain weird symbols.",
    "longest-consecutive-sequence": "Scatter numbered beads. What is the longest run of neighbors like 3,4,5,6 if order in the bag does not matter?",
    "valid-palindrome": "Read only letters and digits, ignoring case and junk. Does the sentence sound the same forwards and backwards?",
    "two-sum-ii-input-array-is-sorted": "A sorted row of coins. Two fingers — one at each end — hunt for a pair that hits the target sum.",
    "3sum": "Find three numbers that add to zero. After sorting, fix one number and let two fingers hunt the rest.",
    "container-with-most-water": "Vertical sticks in a row. Choose two sticks as walls; rainwater forms a rectangle. Maximize the water.",
    "trapping-rain-water": "Bars of a skyline. How much rain sits in the valleys after a storm?",
    "best-time-to-buy-and-sell-stock": "Stock prices across days. Buy once, sell once later. Maximize profit (or take zero).",
    "longest-substring-without-repeating-characters": "A sliding peephole on a string that may only show unique letters. How wide can it get?",
    "longest-repeating-character-replacement": "You may repaint up to k letters. Make the longest stretch of the same letter you can.",
    "permutation-in-string": "Does string s2 hide any scramble of s1 as a contiguous block?",
    "minimum-window-substring": "Smallest window of s that still covers every required character from t (with counts).",
    "sliding-window-maximum": "A window of width k slides across an array. Report the max in every window position.",
    "min-stack": "Build a stack that also answers 'what is the smallest value right now?' in constant time.",
    "evaluate-reverse-polish-notation": "Tokens in RPN: numbers wait on a stack; an operator pops two, computes, pushes back.",
    "generate-parentheses": "How many ways can you write n pairs of parentheses that always stay correctly nested?",
    "daily-temperatures": "For each day, how many days until a warmer day? Use a stack of colder days waiting for heat.",
    "car-fleet": "Cars race toward a destination. Faster cars stuck behind slower ones form fleets.",
    "largest-rectangle-in-histogram": "Bars in a histogram. What is the largest rectangle you can draw under the bars?",
    "binary-search": "A sorted bookshelf. Always open the middle book and throw away half the shelf.",
    "search-a-2d-matrix": "A matrix where each row is sorted and rows increase. Treat it like one long sorted list.",
    "koko-eating-bananas": "Koko must finish banana piles before guards return. Find the slowest eating speed that still works.",
    "find-minimum-in-rotated-sorted-array": "A sorted array was rotated. Find the smallest value with binary search.",
    "search-in-rotated-sorted-array": "Rotated sorted array. Still find a target in logarithmic time by checking which half is sorted.",
    "time-based-key-value-store": "Remember values with timestamps. Ask for a key at time t: latest value not after t.",
    "median-of-two-sorted-arrays": "Two sorted lists. Find the overall median without fully merging.",
    "reverse-linked-list": "A conga line of nodes. Flip every arrow so the line dances the other way.",
    "merge-two-sorted-lists": "Two sorted lines of kids by height. Weave them into one sorted line.",
    "reorder-list": "List L0→L1→…→Ln. Reorder to L0→Ln→L1→Ln-1→…",
    "remove-nth-node-from-end-of-list": "Delete the n-th node from the end in one pass with two pointers a gap apart.",
    "copy-list-with-random-pointer": "Clone a list where each node also points somewhere random — copy both kinds of arrows.",
    "add-two-numbers": "Digits live in reverse linked lists. Add them like paper addition with carry.",
    "linked-list-cycle": "Do the arrows ever loop? A slow turtle and a fast rabbit will meet if there is a cycle.",
    "find-the-duplicate-number": "Numbers 1…n in a list of n+1 entries. Find the duplicate without mutating (Floyd cycle idea).",
    "lru-cache": "A cache that evicts the least recently used item when full — hash map + doubly linked list.",
    "merge-k-sorted-lists": "Many sorted lists. Merge them efficiently (heap of heads).",
    "reverse-nodes-in-k-group": "Reverse the list in chunks of exactly k nodes; leave a short tail alone.",
}


def extract_complexity(src: str) -> tuple[str, str, str, str]:
    time_m = re.search(r"Time Complexity:\s*(?:The time complexity of this (?:approach|solution) is )?O\(([^)]+)\)", src, re.I)
    space_m = re.search(r"Space Complexity:\s*(?:The space complexity (?:of this (?:approach|solution) )?is )?O\(([^)]+)\)", src, re.I)
    time = f"O({time_m.group(1)})" if time_m else "See code"
    space = f"O({space_m.group(1)})" if space_m else "See code"
    # grab sentence after time complexity header if present
    time_reason = "We follow the loops in the solution — usually one main pass means linear time."
    space_reason = "Extra memory comes from sets, maps, stacks, or recursion depth."
    if "hash" in src.lower() and "set" in src.lower():
        time_reason = "Each element is handled a constant number of times with average O(1) hash lookups."
        space_reason = "The hash structure may store up to all unique elements."
    return time, time_reason, space, space_reason


def kid_for(slug: str, title: str, category: str) -> str:
    if slug in STORIES:
        return STORIES[slug]
    return (
        f"Imagine '{title}' as a puzzle game. "
        f"We are in the {category.replace('-', ' ')} world. "
        f"First we invent any correct plan, then we upgrade it with the pattern for this family, "
        f"so a 10-year-old could retell the steps."
    )


def plain_for(title: str, num: int) -> str:
    return (
        f"LeetCode {num}: {title}. "
        f"Restate the official prompt in your own words, list inputs and outputs, "
        f"then solve a tiny example by hand before coding."
    )


def examples_for(title: str) -> list:
    return [
        {
            "input": f"(open LeetCode example 1 for {title})",
            "output": "(match the official output)",
            "explanation": "Pause the animation on each caption and predict the next variable change.",
        },
        {
            "input": f"(open LeetCode example 2 for {title})",
            "output": "(match the official output)",
            "explanation": "After watching, close the site and redraw the data structure from memory.",
        },
    ]


def related(slug: str, category_slugs: list[str]) -> list[str]:
    if slug not in category_slugs:
        return category_slugs[:3]
    i = category_slugs.index(slug)
    out = []
    if i > 0:
        out.append(category_slugs[i - 1])
    if i + 1 < len(category_slugs):
        out.append(category_slugs[i + 1])
    if i + 2 < len(category_slugs):
        out.append(category_slugs[i + 2])
    return out[:3]


def main():
    by_cat = {}
    for p in CATALOG["problems"]:
        by_cat.setdefault(p["category"], []).append(p["slug"])

    for p in CATALOG["problems"]:
        path = PROBLEMS / f"{p['slug']}.json"
        doc = json.loads(path.read_text())
        src = Path(ROOT / p["pythonPath"]).read_text()
        t, tr, s, sr = extract_complexity(src)

        # Keep premium untouched for the three reference problems' stories etc., but sync complexity if needed
        if p["slug"] not in ("contains-duplicate", "two-sum", "valid-parentheses"):
            doc["kidExplanation"] = kid_for(p["slug"], p["title"], p["category"])
            doc["plainProblem"] = plain_for(p["title"], p["leetcodeNumber"])
            doc["examples"] = examples_for(p["title"])
            doc["complexity"] = {
                "time": t,
                "timeReason": tr,
                "space": s,
                "spaceReason": sr,
            }
            doc["relatedProblems"] = related(p["slug"], by_cat[p["category"]])
            # Stronger thinking steps tailored lightly
            pname = doc["pattern"]["name"]
            doc["thinkingSteps"] = [
                {
                    "title": "Brute force idea",
                    "body": f"For {p['title']}, first describe a slow but correct approach (often nested loops or rescanning).",
                },
                {
                    "title": "Why it is slow",
                    "body": "Count the loops. If work looks like n×n, say so. Google interviewers want that honesty.",
                },
                {
                    "title": "Aha insight",
                    "body": f"Reach for this pattern: {pname}. Ask what information you can remember to avoid redo work.",
                },
                {
                    "title": "Better idea",
                    "body": "Write the optimal plan in 3 bullets, then code. Walk example 1 with your finger on each variable.",
                },
            ]
            doc["interviewTips"] = [
                f"Open with: 'This looks like {pname}.'",
                "Narrate one example before typing.",
                f"Close with complexity: {t} time, {s} space, and why.",
            ]
            doc["interviewApproachNotes"] = (
                f"NeetCode's published approach for {p['title']} is the usual interview target: "
                f"clear {pname.lower()} with competitive complexity ({t} time). "
                "Prefer readable code over micro-optimizations; explain trade-offs if a simpler slower method exists."
            )

        path.write_text(json.dumps(doc, indent=2) + "\n")
    print("Enriched", len(CATALOG["problems"]), "problems")


if __name__ == "__main__":
    main()
