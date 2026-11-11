# Extending the app

How to keep improving without breaking the cinema pipeline.

## Add or upgrade one problem’s animation

1. Prefer a **specialty tracer** when the algorithm is deterministic and small:
   - Create `src/lib/tracers/my-problem.ts` exporting `traceMyProblem(input)`
   - Register it in `src/lib/tracers/index.ts` (or call `registerTracer`)
   - Set `animation.tracerId` to that id in `content/problems/<slug>.json`
2. Or regenerate authored cinema steps:
   ```bash
   npm run content:animate
   npm run content:verify-animations
   ```
3. Hand-tune captions / `defaultInput` / `highlights` in the JSON if needed.
4. Open `/problem/<slug>/` → **Answer in 3D** and play.

## Add a new visual payload key

1. Document it in `src/lib/animation/state.ts`
2. Teach `readPrimaryValues` / `readMemoryShelf` (or add a new reader)
3. Render it in `AlgoWorld` (3D) and `GenericScene` (2D) if needed
4. Extend `animationQualityReport` so verify fails if the key is missing when required
5. Update `scripts/generate_answer_animations.py` generators

## Add a cinema camera shot

1. Add a shot id to `CinemaShot` in `src/lib/cinemaCameras.ts`
2. Implement `poseForShot` math (see blender-skills under `skills/`)
3. Map it in `shotForAlgoMoment`
4. Document the teach moment in `skills/dsa-answer-cinema/SKILL.md`

## Add a lesson chapter / beat kind

1. Extend `BeatKind` in `src/lib/lessonScript.ts`
2. Emit the beat from `buildLessonScript`
3. Render it in `LessonTheater` `StageBody`
4. Keep autoplay rules intentional (interactive beats should pause outer play)

## Content pipeline commands

| Command | Purpose |
|---------|---------|
| `npm run content:animate` | Fill stub animations from examples |
| `npm run content:verify-animations` | Fail CI-style if any of 150 are stubby |
| `npm run content:validate` | Zod + premium tracer checks |
| `npm run content:audit` | Solution path audit |
| `npm test` | Unit + full 150 animation gate |
| `npm run build` | Static export |

## File map for newcomers

```
docs/ARCHITECTURE.md          system design
docs/EXTENDING.md             this file
skills/dsa-answer-cinema/     blender → web camera map
content/problems/             150 lesson JSON files
src/lib/animation/            resolve + state contract
src/lib/tracers/              specialty simulators
src/components/theater/       lesson UI
src/components/answer3d/      3D answer cinema
scripts/generate_answer_animations.py
scripts/verify_all_animations.ts
```

## Rules that keep the app scalable

- One public import surface for animation: `@/lib/animation`
- JSON steps stay serializable (no functions / class instances)
- Never bypass `resolveAnimationSteps` in UI players
- Never commit stub captions (`Start solving…`, `see-leetcode`)
- Run verify after every content or tracer change
