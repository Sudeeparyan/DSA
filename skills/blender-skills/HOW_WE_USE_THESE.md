# How this site uses blender-skills

Source: https://github.com/Sudeeparyan/blender-skills

Blender MCP is **not required** to run the learning site. We reused the *camera storytelling language* from these skills inside the browser:

| Skill | In-app implementation |
|-------|------------------------|
| `crane-shot` | `poseForShot("crane")` — low→high reveal of the input pedestal |
| `slow-zoom` | `poseForShot("slowZoom")` — push into the current cell |
| `dolly-rotate` | `poseForShot("dollyRotate")` — sweep while the algo walks |
| `turntable` / `perfect-loop` | `poseForShot("turntable")` — orbit the solved memory shelf |
| `dynamic-full-loop` | `poseForShot("whip")` — fast cut when a match fires |
| `threejs-export` | Live `AnswerStage` Canvas + OrbitControls + studio lights |

Code:
- `src/lib/cinemaCameras.ts`
- `src/components/answer3d/`
- Lesson chapter **Answer in 3D** (`lessonScript` beat `answer3d`)

If Blender MCP is available later, you can still render ProRes hero clips with the vendored skill scripts under this folder and drop them into `public/cinema/`.
