# NeetCode 150 Play

Teacher-led, offline-friendly study site for the **NeetCode 150**.  
Each problem is a lesson: feel the question → **watch the answer in 3D cinema** → unseal the blueprint.

## Quick start

See **[HOW_TO_RUN.md](./HOW_TO_RUN.md)**.

```bash
npm install
npm run dev
```

Open http://localhost:3000 → **Play lesson 1** → chapter **Answer in 3D**.

## Architecture (read this before changing code)

- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** — layers, contracts, quality gate
- **[docs/EXTENDING.md](./docs/EXTENDING.md)** — how to add tracers, cameras, chapters, payloads
- **[skills/dsa-answer-cinema/SKILL.md](./skills/dsa-answer-cinema/SKILL.md)** — blender-skills → web cameras

### Extension surfaces

| Want to… | Touch |
|----------|--------|
| Upgrade one algorithm simulation | `src/lib/tracers/` + `registerTracer` |
| Change 3D / 2D shared payloads | `src/lib/animation/state.ts` |
| Change camera storytelling | `src/lib/cinemaCameras.ts` |
| Change lesson chapters | `src/lib/lessonScript.ts` + `components/theater` |
| Regenerate cinema steps | `npm run content:animate` |
| Gate quality for all 150 | `npm run content:verify-animations` |

## Content pipeline

```bash
npm run content:animate              # fill / refresh authored steps from examples
npm run content:verify-animations    # must be 150/150
npm run content:validate             # Zod + specialty tracer checks
npm test                             # unit + full animation gate
npm run build                        # static export → out/
```

## What’s inside

- `content/problems/` — 150 validated lesson JSON files
- `solutions/` — Python from [`Sudeeparyan/Neetcode150`](https://github.com/Sudeeparyan/Neetcode150)
- `src/lib/animation/` — reusable resolve + state contract
- `src/components/answer3d/` — Three.js answer cinema
- `src/components/theater/` — teacher playthrough UI
- Progress / notes / Leitner cards in `localStorage`
- Static export (`output: 'export'`) for GitHub Pages / Vercel

## Notes

Audit history: [BUILD_REPORT.md](./BUILD_REPORT.md). Teaching checklist: [PROGRESS.md](./PROGRESS.md).
