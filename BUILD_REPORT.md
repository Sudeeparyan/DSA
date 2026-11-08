# Build Report — NeetCode 150 Learn

## Summary

| Item | Count |
| --- | --- |
| Problems in catalog | 150 |
| Problem JSON validated | 150/150 |
| Python solutions vendored | 150 |
| C++ solutions in source repo | 0 |
| Rust solutions in source repo | 0 |
| Premium traced animations (unit-tested) | 3 (Contains Duplicate, Two Sum, Valid Parentheses) |
| NeetCode video URLs verified & filled | 0 (all left `null` — never invent URLs) |

## Data fixes (README vs files)

Trusted **file numbers / folders**, not the upstream README table:

1. **Search in Rotated Sorted Array (33)** vs **Find Minimum in Rotated Sorted Array (153)** — README title/link rows were swapped; folders `04_Find_Minimum_.../0153-...` and `05_Search_In_.../0033-...` are correct. Catalog uses file numbers.
2. **Copy List with Random Pointer** — README labelled **141**; files are `0138-...` (**138** is correct). **141** is Linked List Cycle.
3. README claims C++/Rust for every problem; **no `.cpp` or `.rs` files exist** in `Sudeeparyan/Neetcode150` (151 `.py` files only). Site tabs show an honest empty state.

## Interview approach check (best simple optimal)

Reviewed against common Google/NeetCode expectations:

| Problem | Taught approach | Verdict |
| --- | --- | --- |
| Contains Duplicate | Hash set one-pass O(n) | Best simple interview answer |
| Two Sum | Hash map value→index O(n) | Best simple interview answer |
| Valid Parentheses | Stack + closer→opener map O(n) | Best simple interview answer |
| Valid Anagram | Count map / 26 counters | Optimal clear answer |
| Product Except Self | Prefix×suffix, no division | Expected optimal |
| Longest Consecutive | Hash set streak starts O(n) | Expected optimal |
| Top K Frequent | Frequency buckets O(n) | Preferred over full sort |

`interviewApproachNotes` on each problem JSON records the intended interview pitch: clear pattern, competitive complexity, readable code.

## Source repo notes

- Vendored into [`solutions/`](solutions/) from https://github.com/Sudeeparyan/Neetcode150
- Working site repo: https://github.com/Sudeeparyan/DSA

## How to run

See [HOW_TO_RUN.md](HOW_TO_RUN.md).

## Tests

- `npm test` — Zod schema for all 150 + tracer final-answer checks for the three reference problems
- `npm run content:validate` — same validation via script
- `npm run build` — static export of 150 problem pages + category/roadmap/search/revise/patterns

## Remaining intentional gaps

- Dedicated TypeScript tracers beyond the three reference problems fall back to authored `animation.steps` + `generic-array-scan` where applicable. Extend `src/lib/tracers/` problem-by-problem for richer live re-runs.
- NeetCode YouTube links left empty until each URL is manually verified.
- C++/Rust tabs empty until those files exist upstream.
