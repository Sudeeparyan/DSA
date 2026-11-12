# Working on this project

Read this before changing anything. It applies to people and to AI coding assistants alike.

## What this is, and for whom

A study site for **understanding** the NeetCode 150 (Google interview preparation). Each problem
page shows the question in plain words, the idea, a 3D walkthrough of the real solution running
line by line, and the time and space cost with reasons. Readers may be beginners.

Overview of the code: [README.md](./README.md) · how it fits together:
[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) · changing a lesson: [docs/LESSONS.md](./docs/LESSONS.md).

## Rules

1. **Correct before anything else.** A solution, expected answer, caption or complexity claim is
   only changed with proof: `npm run lessons` and `npm run lessons:verify` must pass, and a
   complexity claim must match the code as shown (not some other version of it). Prefer the
   well-known optimal approach an interviewer expects.
2. **Learning only.** No quizzes, practice editors, accounts or extra modes. Keep the page
   uncluttered and the wording plain: short sentences, say *why*, put identifiers in `` `code` ``.
3. **Never edit `content/lessons/*.json` by hand.** They are generated. Change
   `lessons/specs/*.py` (or the solution) and run `npm run lessons`, then commit the spec and the
   rebuilt JSON together. CI fails when they disagree.
4. **One home for each fact.** Problem list, titles, order and difficulty: `content/catalog.json`.
   Lesson-file format: `src/lib/lesson.ts`. Highlight colours: `lessons/engine/core.py` (`TONES`)
   and `src/components/stage3d/theme.ts`. Page styles: `src/app/lesson.css`.
5. **Static site only.** `next.config.ts` exports plain files (`output: "export"`): no API routes,
   no server actions, no runtime data fetching, and every link ends in `/` (`/problem/two-sum/`).
6. **Keep saved progress working.** `src/lib/progress.ts` reads keys and a format that real
   browsers already hold; change them only with a migration, and keep its tests passing.
7. **Ask before adding a dependency.** The app needs few: Next.js, React, three.js
   (`@react-three/fiber`, `drei`) and Zod. Pin exact or caret versions in `package.json`.
8. **Do not bring back the removed first version** (lesson "theater", `answer3d`, `tracers`,
   `content/problems/`, the roadmap / patterns / revise / search pages). It lives in git history
   (commit `f90df17`) if something from it is ever needed.

## Where to change what

| To change… | Edit | Then run |
| --- | --- | --- |
| A question, idea, caption, example or complexity text | `lessons/specs/cNN_<topic>.py` | `npm run lessons -- <slug>` |
| The code a lesson shows and runs | `solutions/…/<slug>.py`, or `code=` in the spec | `npm run lessons -- <slug>` and `npm run lessons:verify -- <slug>` |
| The brute-force reference | `lessons/checks/cNN_to_cMM.py` | `npm run lessons:verify -- <slug>` |
| How a data structure is captured | `lessons/engine/views.py` | `npm run lessons` (all 150) |
| How a data structure is drawn | `src/components/stage3d/views/` | look at a few lessons that use it |
| A new kind of structure | see "Adding a new kind of structure" in docs/ARCHITECTURE.md | `npm run check` |
| Page layout or wording outside lessons | `src/components/lesson/`, `src/app/` | `npm run dev` |
| Colours, spacing, fonts | `src/app/lesson.css` (stage: `stage3d/theme.ts`) | `npm run dev` |

## Done means

- `npm run check` passes (rebuilds and verifies all lessons, type check, tests, lint, build).
- `content/lessons/` has no uncommitted changes after `npm run lessons`.
- For anything visible: you looked at the page at desktop width **and** phone width (about 390 px),
  including a lesson with an "Operations" card (e.g. `/problem/lru-cache/`) and a busy one
  (e.g. `/problem/word-search-ii/`).
- New behaviour in `src/lib/` or `src/components/lesson/*.ts` has a unit test (`*.test.ts` next to it).
- Docs updated if a command, a folder or a rule changed.

## Traps already hit once

- **Measuring inside a scrolling box**: use `getBoundingClientRect()` relative to the box, not
  `offsetTop` (that is relative to the nearest *positioned* ancestor, which may be outside the box).
  This once scrolled the running code line out of sight. The box can also change height without
  the line changing (a shorter caption on the next step), so `CodePanel` re-checks on resize.
- **Narrow screens**: anything showing a problem title (prev / next / continue buttons) or a long
  value without spaces (`["ad","ae",…]` in a caption) must be able to wrap at 390 px, or the whole
  page scrolls sideways.
- **Spaces next to elements inside `display: flex`** are trimmed. Wrap mixed text in one `<span>`.
- **Code wrapping**: a line may break right after `-`, which split `->` in two. Operators are their
  own `tok-op` spans with `white-space: nowrap`.
- **Keyboard shortcuts** on the lesson page must not swallow keys meant for a focused control
  (buttons, links, `<summary>`, inputs). See `Walkthrough.tsx`.
- **The 3D stage only runs in the browser** (`dynamic(..., { ssr: false })`) and must keep working
  without WebGL (it shows a text fallback) and with `prefers-reduced-motion` (no easing).
- **`npm run dev` after `npm run build`** can fail on a stale `.next` folder: delete it and restart.

## Commands

```bash
npm run dev               # site at http://localhost:3000
npm run lessons           # rebuild all lessons (add `-- <slug>` for one)
npm run lessons:verify    # brute-force cross-check (add `-- <slug>` for one)
npm test                  # lesson-file checks + unit tests
npm run check             # everything, as CI runs it
python lessons/trace.py <slug>   # print a built lesson as text, to proof-read it
python lessons/show.py <slug>    # print the cleaned solution with line numbers
```
