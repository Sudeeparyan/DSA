# NeetCode 150, step by step

A study site for **understanding** the NeetCode 150. It has no practice editor and no quizzes. Each
problem gets one page with four parts:

1. **The question** in plain words, with a worked example.
2. **The idea** that solves it, in two to four short points.
3. **Watch it solve the example**: a 3D walkthrough of the real solution running one line at a
   time. The running line is lit up in the code, and a caption explains each step.
4. **How fast is it?** Time and extra space, each with the reason.

```bash
npm install
npm run dev        # then open http://localhost:3000
```

Step-by-step setup for beginners: **[HOW_TO_RUN.md](./HOW_TO_RUN.md)**.

## How it works

The walkthrough is recorded from the code, so the animation can never disagree with it:

```
lessons/specs/*.py  ──►  lessons/build.py  ──►  content/lessons/<slug>.json  ──►  the web page
 what to teach:           runs the REAL           every step: caption, code        plays the steps
 question, idea,          solution under a        line, and a snapshot of          on a 3D stage
 example, captions        line-by-line tracer     each data structure              (Next.js + three.js)
```

- **Python** (`lessons/`) decides *what* is shown. It runs each solution, checks the answer, and
  writes one JSON file per problem.
- **The website** (`src/`) decides *how* it looks. It only reads those JSON files and draws them.
- The JSON files are committed, so running the site needs Node.js only; Python is needed only to
  change a lesson.

Details: **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)**. Changing a lesson:
**[docs/LESSONS.md](./docs/LESSONS.md)**. Rules for anyone (or any AI assistant) changing the
code: **[AGENTS.md](./AGENTS.md)**.

## Checks

Every solution is tested three ways before the site is built:

```bash
npm run lessons          # rebuild all 150 lessons; fails if any answer or test is wrong
npm run lessons:verify   # run each solution on thousands of random inputs vs a brute-force answer
npm test                 # every lesson file is valid and drawable; unit tests for the app code
npm run check            # all of the above, plus type check, lint and the production build
```

`npm run check` must pass before any change is merged. The same check runs on GitHub for every
push and pull request (`.github/workflows/check.yml`).

## Where things are

| Path | What it is |
| --- | --- |
| `content/catalog.json` | The 150 problems: titles, topics, difficulty, order, solution file |
| `solutions/` | One Python solution per problem (the code each lesson runs by default) |
| `lessons/specs/` | One `lesson(...)` per problem: the teaching text and captions, by topic |
| `lessons/engine/` | The tracer and the data-structure "views" the specs use |
| `lessons/checks/` | Brute-force references used by `lessons/verify.py` |
| `content/lessons/` | Built lesson files (**generated**, never edit by hand) |
| `src/app/` | Pages: home (`page.tsx`) and one lesson page per problem (`problem/[slug]/`) |
| `src/components/lesson/` | The lesson page, walkthrough controls and code panel |
| `src/components/stage3d/` | The 3D stage: layout planner, camera, one component per structure |
| `src/lib/lesson.ts` | The lesson-file format (a Zod schema shared by the app and the tests) |
| `src/lib/progress.ts` | The "I understand this one" ticks, kept in the browser |
| `public/sw.js` | Offline support |

Progress is saved in the browser (`localStorage`) on each device; there is no server or account.
