# Architecture

NeetCode 150 **Play** is a static Next.js app that teaches each problem as a
**teacher-led lesson** with a **3D answer cinema** stage.

Design goal: keep improving forever without rewriting the core. Content,
tracers, cameras, and UI stages are separate extension points.

```
content/problems/*.json     ← source of truth for each lesson
        │
        ▼
src/lib/schema.ts           ← Zod contracts
src/lib/problems.ts         ← catalog + loaders
        │
        ├── src/lib/animation/     ← resolve steps + shared state readers
        ├── src/lib/tracers/       ← optional specialty simulators
        ├── src/lib/cinemaCameras.ts
        └── src/lib/lessonScript.ts
                │
                ▼
src/components/theater/     ← chapter playthrough + teacher bar
src/components/answer3d/    ← Three.js answer stage (blender-skills cameras)
src/components/visualiser/  ← 2D lab desk / free-play engine
```

## Layers

| Layer | Responsibility | Extend by |
|-------|----------------|-----------|
| **Content** | JSON problem + authored cinema steps | `npm run content:animate` / hand-edit JSON |
| **Schema** | Validation | `src/lib/schema.ts` |
| **Animation resolve** | Pick tracer vs authored steps | `src/lib/animation/resolve.ts` |
| **Tracers** | Deterministic step emitters | `registerTracer()` + file in `tracers/` |
| **Lesson script** | Teacher beats / chapters | `src/lib/lessonScript.ts` |
| **Cinema cameras** | Crane / zoom / dolly / whip / turntable | `src/lib/cinemaCameras.ts` |
| **Answer Stage 3D** | WebGL world + HUD | `src/components/answer3d/` |
| **Visualiser 2D** | Lab desk free-play | `src/components/visualiser/` |
| **Progress** | localStorage status / notes / Leitner | `src/lib/progress.ts` |

## Animation state contract

All steps share a JSON-serializable `state` object. Readers live in
`src/lib/animation/state.ts`:

- **Primary row:** `nums` | `chars` | `nodes` | `bits` | `heap` | `path`
- **Memory shelf:** `seen` | `map` | `stack` | `visible`
- **Spatial:** `grid` | `table` | `intervals` | `edges`
- **Focus:** `currentIndex`, `highlights`, `result`

2D and 3D renderers both consume this contract — do not invent one-off keys
unless you also teach the readers.

## Step resolution order

`resolveAnimationSteps(problem, input)`:

1. Specialty tracer (`tracerId` registered, not `authored` / `generic-array-scan`)
2. Rich authored steps (≥5 beats, non-stub captions)
3. Generic fallback tracer
4. Authored steps as last resort

## Quality gate

```bash
npm run content:verify-animations   # 150/150 cinema quality
npm test                            # includes animations.verify.test.ts
npm run content:validate            # Zod + premium tracer checks
npm run build                       # static export
```

Never ship a problem that fails the verify loop.

## Skills

Blender camera skills are vendored under `skills/blender-skills/` and mapped in
`skills/dsa-answer-cinema/SKILL.md`. The web app ports the **camera language**,
not Blender MCP itself.

## Deprecated

`src/components/mission/` was an earlier stage-wizard UI and has been removed.
The live path is `LessonTheater` → `AnswerStage`.
