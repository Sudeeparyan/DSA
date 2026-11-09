---
name: dsa-answer-cinema
description: Adapt blender-skills cinematic cameras into Three.js answer stages so students understand algorithm solutions by watching a 3D scene, not reading walls of text.
---

# DSA Answer Cinema

Maps [blender-skills](https://github.com/Sudeeparyan/blender-skills) camera language onto in-browser Three.js lessons.

## Why

Blender skills are for product showcase film. Algorithms need the same storytelling:

| Blender skill | DSA teach moment |
|---------------|------------------|
| `crane-shot` | Reveal the input structure from below → overhead map |
| `slow-zoom` | Push into the *current* cell / pointer the teacher is naming |
| `dolly-rotate` | Sweep along the array while the algorithm walks |
| `turntable` / `perfect-loop` | Showcase the finished memory shelf / final answer |
| `dynamic-full-loop` | Whip-cut when a match / return fires |
| `threejs-export` | Ship interactive OrbitControls + studio lights in the web app |

Blender MCP is optional. This site implements the camera math in `src/lib/cinemaCameras.ts` and the stage in `src/components/answer3d/`.

## Teacher rules

1. Camera move always answers: **what should the student look at now?**
2. One caption per beat — never denser than the visual.
3. Prefer showing the answer forming (shelf filling, pointers meeting) over showing code first.
4. End with a calm turntable of the solved state, then unseal code.
