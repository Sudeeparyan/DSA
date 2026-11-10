# Build Report — NeetCode 150 Learn

## Summary

| Item | Count |
| --- | --- |
| Problems in catalog | 150 |
| Problem JSON validated | 150/150 |
| Answer animations verified | 150/150 |
| Python solutions vendored | 150 |
| C++ solutions in source repo | 0 |
| Rust solutions in source repo | 0 |
| Specialty live tracers | 3 (Contains Duplicate, Two Sum, Valid Parentheses) |
| Static export pages | 177 |
| NeetCode video URLs | left `null` when not verified — never invent URLs |

## Final audit (2026-11-10)

Full write-up: [`docs/AUDIT.md`](./docs/AUDIT.md).

- Fixed Min Stack / Generate Parentheses / Reverse Integer cinema bugs
- Removed identical “Keep watching…” padding; tightened verify gate
- Enriched stub plainProblem, thinkingSteps, edgeCases, mistakes, complexity blurbs
- Live HTTP: 150/150 problem routes 200 after clean `.next`
- Browser QA: home, contains-duplicate 3D, min-stack push/getMin captions PASS

## Solutions audit

Total problems in catalog: 150  
Python present: 150 · C++ present: 0 · Rust present: 0

### Known README mismatches (fixed in catalog by trusting file numbers)
- Search in Rotated Sorted Array (33) vs Find Minimum (153): README titles/links were swapped; folders/files are correct.
- Copy List with Random Pointer: README labelled 141; files use 0138 (correct). 141 is Linked List Cycle.

### Missing language implementations
- All 150 C++ links in upstream README point to missing files.
- All 150 Rust links in upstream README point to missing files.

## How to re-check

```bash
npm run content:animate
npm run content:enrich-prose
npm run content:verify-animations
npm test && npm run lint && npm run build
```
