# Architecture

The site is a set of **static pages** (Next.js `output: "export"`) built from **generated lesson
files**. There is no server, no database and no login. This page explains how the pieces fit, so
that a change lands in the right place.

## The two halves

```
 ┌─────────────── Python: WHAT to teach ───────────────┐      ┌──────────── TypeScript: HOW it looks ────────────┐
 │                                                      │      │                                                  │
 │  content/catalog.json   the 150 problems, in order   │      │  src/lib/lesson.ts      the lesson-file format   │
 │  solutions/<…>.py       the solution that runs       │      │  src/lib/lessons.ts     reads the files at build │
 │  lessons/specs/*.py     question, idea, captions     │      │  src/app/…              the pages                │
 │  lessons/engine/        tracer + data-structure      │ JSON │  src/components/lesson  page, controls, code     │
 │                         views                        │ ───► │  src/components/stage3d the 3D stage             │
 │  lessons/build.py       writes content/lessons/      │      │                                                  │
 │  lessons/verify.py      brute-force cross-check      │      │                                                  │
 └──────────────────────────────────────────────────────┘      └──────────────────────────────────────────────────┘
```

The only thing that crosses from one half to the other is `content/lessons/<slug>.json`. Its
format is defined once, in `src/lib/lesson.ts` (a Zod schema), and `src/lib/lessons.test.ts` checks
every file against it.

## 1. Building a lesson (Python)

`python lessons/build.py` (or `npm run lessons`) does this for every problem in the catalog:

1. **Load the spec.** `lessons/specs/cNN_<topic>.py` holds one `lesson("slug", ...)` call per
   problem: statement, idea, the example input and expected answer, extra tests, which data
   structures to draw (`views=`), and captions tied to code lines (`notes=`).
2. **Load the code.** The solution in `solutions/` (path from `catalog.json`), cleaned of its header
   docstring and LeetCode boilerplate, or the spec's own `code=` where that version teaches better
   (18 lessons; listed in [LESSONS.md](./LESSONS.md)).
3. **Prove it.** Run the example and every extra test. A wrong answer stops the build.
4. **Record it.** Run the example again under `sys.settrace` (`lessons/engine/core.py`). Each time a
   line that has a note finishes, a **step** is saved: the caption with its `{expressions}` filled in,
   the line number, and a snapshot of every view, made from the solution's live variables.
5. **Write** `content/lessons/<slug>.json`. The output is deterministic: rebuilding an unchanged spec
   gives byte-identical files.

`python lessons/verify.py` (`npm run lessons:verify`) is a second, independent proof: for each
problem, `lessons/checks/` has a random-input generator and a slow, obviously correct reference.
Every solution is run on many random inputs and must agree with it.

Helpers for authors: `lessons/show.py <slug>` prints the cleaned solution with line numbers, and
`lessons/trace.py <slug>` prints a built lesson as text (captions plus what each view shows).

## 2. Showing a lesson (TypeScript)

| File | Job |
| --- | --- |
| `src/app/layout.tsx` | Site shell: fonts, header, footer, service worker |
| `src/app/page.tsx` → `components/lesson/ProblemList.tsx` | Home: all problems by topic, search, progress, "Continue" |
| `src/app/problem/[slug]/page.tsx` → `components/lesson/LessonPage.tsx` | One page per lesson (150 static pages) |
| `components/lesson/Walkthrough.tsx` | Step controls, auto-play, keyboard, full screen, `?step=N` links |
| `components/lesson/CodePanel.tsx` + `python.ts` | The code with the running line lit up; a tiny Python colouriser |
| `components/lesson/Rich.tsx` | Turns `**bold**`, `*em*` and `` `code` `` in lesson text into elements |
| `components/stage3d/Stage.tsx` | The three.js canvas, camera, lights; picks a component for each view |
| `components/stage3d/layout.ts` | Plans where every structure sits (see below) |
| `components/stage3d/views/*View3D.tsx` | One component per kind of structure |
| `components/stage3d/primitives.tsx` | Shared 3D pieces (blocks, labels, arrows) and the easing that animates them |
| `components/stage3d/theme.ts` | Colours of the stage and what each highlight colour means |
| `src/lib/progress.ts` | "I understand this one" ticks and the last lesson opened (`localStorage`) |
| `src/app/lesson.css` / `globals.css` | All page styles / the CSS reset and base rules |

**How the stage stays calm.** Before a lesson plays, `planStage()` looks at *every* step and gives
each view (by its `id`) one fixed slot, sized for the largest it will ever get. So nothing jumps
around and the camera never re-frames mid-lesson. Moving to another step only changes what is
inside the slots; the components ease from the old picture to the new one.

**Colours mean the same thing everywhere.** A highlight is a *tone*: `cur` looking at now, `alt`
compared with, `good` match / answer, `bad` rejected, `seen` visited, `win` current range / path,
`mark` queued / flagged, `dim` no longer needed. The tones are defined in `lessons/engine/core.py`
(`TONES`) and `components/stage3d/theme.ts`, and the tests reject any other tone.

**Views that are not 3D.** `vars` (plain variables) and `ops` (the calls of a design problem such as
LRU Cache) are drawn as HTML cards beside the code, not on the stage. Below 1080 px wide the side
cards sit under the walkthrough, so the caption box repeats the calls, the running line and the
variables, and the step buttons float at the bottom of the screen (all in `Walkthrough.tsx` and
`lesson.css`).

## 3. Shipping

- `npm run build` writes the static site to `out/`: the home page, 150 lesson pages and a 404 page.
  Any static host works (Vercel, GitHub Pages, Netlify). `next.config.ts` sets `output: "export"`
  and `trailingSlash: true`, so links end in `/` (`/problem/two-sum/`).
- `public/sw.js` makes visited pages work offline: pages and data are network-first with a cached
  fallback; fingerprinted build files and fonts are cache-first. Bump `CACHE` in it if its caching
  rules change.

## Adding a new kind of structure to the stage

The stage already draws arrays, maps and sets, stacks and queues, call stacks, linked lists, trees,
heaps, tries, recursion trees, graphs, grids, intervals and bits. To add another kind:

1. **Python view**: a `View` subclass in `lessons/engine/views.py` whose `render()` returns a dict
   with a new `"t"`; export it from `lessons/engine/api.py`.
2. **Format**: add its schema to the `ViewSchema` union in `src/lib/lesson.ts`.
3. **Test**: add a `case` for it in `viewProblems()` in `src/lib/lessons.test.ts` (dangling ids,
   bad tones, out-of-range pointers).
4. **Plan**: a `measureX()` plus a `Metrics` entry in `components/stage3d/layout.ts`, and a `case`
   in its `measure()` switch.
5. **Draw**: `components/stage3d/views/XView3D.tsx`, and a line for it in `SlotView` in `Stage.tsx`.
6. **Proof-read**: teach `lessons/trace.py` to describe it.

TypeScript will point at any `switch` that misses the new kind once step 2 is done.
