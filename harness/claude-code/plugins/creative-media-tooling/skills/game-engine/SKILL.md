---
name: game-engine
description: >-
  Build web-based game engines and games with HTML5 Canvas, WebGL, SVG, CSS, and JavaScript. Use
  when creating 2D or 3D games, implementing game loops, physics, collision detection, sprites,
  tilemaps, controls, audio, multiplayer with WebRTC or WebSockets, optimization, or publishing
  workflows.
---

<!-- Generated from harness/github-copilot/plugins/creative-media-tooling/skills/game-engine/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Game engine

Builds browser-based games and reusable game-engine foundations using Canvas, WebGL, JavaScript, starter templates, and focused reference material for 2D, 3D, controls, audio, algorithms, performance, and publishing.

## When to invoke

- "Build a web game with Canvas or WebGL."
- "Implement a game loop, physics, or collision detection."
- "Create a 2D platformer, breakout game, maze game, or 3D experience."
- "Add keyboard, mouse, touch, or gamepad controls."
- "Optimize or publish this browser game."

## Prerequisites and context

- Use a modern browser with Canvas/WebGL support.
- Basic HTML, CSS, and JavaScript are assumed.
- Node.js is optional for build tooling and local development servers.
- Choose framework support only when it fits the requested game: Phaser, Three.js, Babylon.js, A-Frame, or PlayCanvas.

## Core engine model

| Concept | Rule |
| --- | --- |
| Game loop | Use `requestAnimationFrame`; process input, update state, then render. |
| Delta time | Scale movement and timers by elapsed time so games do not run at different speeds. |
| Rendering | Use Canvas 2D for sprites and tilemaps, WebGL for hardware-accelerated 3D or advanced 2D, SVG for vector UI, and CSS for DOM-based transitions. |
| Physics | Model position, velocity, acceleration, and gravity explicitly. |
| Collision | Use AABB, circle, SAT-based collision, bounding box, bounding sphere, or raycasting depending on dimension and shape. |
| Controls | Support keyboard, WASD, arrow keys, mouse, pointer lock, touch, virtual joysticks, and Gamepad API as appropriate. |
| Audio | Use Web Audio API for programmatic sound and spatial audio; use HTML5 Audio for simple music and effects. |

## Workflow patterns

### Creating a basic 2D game

1. Set up an HTML file with a `<canvas>` element.
2. Get the 2D rendering context.
3. Implement a `requestAnimationFrame` game loop.
4. Create game objects with position, velocity, and size.
5. Handle keyboard or mouse input for player control.
6. Implement collision detection between game objects.
7. Add scoring, lives, and win/lose conditions.
8. Add sound effects and music.

### Building a 3D game

1. Choose Three.js, Babylon.js, A-Frame, or PlayCanvas.
2. Set up scene, camera, and renderer.
3. Load or create 3D models and textures.
4. Implement lighting and shaders.
5. Add physics and collision detection.
6. Implement player controls and camera movement.
7. Add audio and visual effects.

### Publishing a game

1. Optimize assets: compress images and audio, minify code, and reduce draw calls.
2. Test across browsers, devices, input methods, and viewport sizes.
3. Choose distribution: web, app stores, or game portals.
4. Implement monetization only when requested.
5. Prepare promotion through game communities and social media.

## Template and reference inventory

| Resource | Use it for |
| --- | --- |
| `assets/paddle-game-template.md` | 2D Breakout-style game with pure JavaScript. |
| `assets/2d-maze-game.md` | Maze game with device orientation controls. |
| `assets/2d-platform-game.md` | Platformer using Phaser. |
| `assets/gameBase-template-repo.md` | Game base template repository structure. |
| `assets/simple-2d-engine.md` | Simple 2D platformer engine with collisions. |
| `references/basics.md` | Game development introduction and anatomy. |
| `references/web-apis.md` | Canvas, WebGL, Web Audio, Gamepad, and related web APIs. |
| `references/techniques.md` | Collision detection, tilemaps, async scripts, and audio. |
| `references/3d-web-games.md` | 3D theory, frameworks, shaders, and WebXR. |
| `references/game-control-mechanisms.md` | Touch, keyboard, mouse, and gamepad controls. |
| `references/game-publishing.md` | Distribution, promotion, and monetization. |
| `references/algorithms.md` | Raycasting, collision, physics, and vector math. |
| `references/terminology.md` | Game development glossary. |
| `references/game-engine-core-principles.md` | Core design principles for game engines. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Canvas is blank | Drawing before context setup or outside the game loop. | Get the context first and draw inside `requestAnimationFrame`. |
| Game runs at different speeds | Fixed per-frame movement. | Use delta time in update calculations. |
| Collision detection is inconsistent | Fast objects tunnel through colliders. | Use continuous collision detection or smaller time steps. |
| Audio does not play | Browser autoplay restrictions. | Start playback from a click, key, or touch handler. |
| Performance is poor | Too many draw calls, allocations, or large assets. | Profile with browser dev tools, reduce draw calls, use object pooling, and optimize assets. |
| Touch controls are unresponsive | Default browser gestures consume events. | Prevent default touch behavior and handle touch separately from mouse. |
| WebGL context lost | GPU or browser reset. | Handle `webglcontextlost` and restore state on `webglcontextrestored`. |

## Progressive disclosure and bundled resources

Use the bundled assets as starter templates and read references only when the current task needs that topic. Do not load every reference for a small fix.

- `assets/`: complete template documents consumed as starting points.
- `references/`: topic-specific game development guidance.

## Game development vocabulary

Preserve `2D/3D`, `breakout-style`, `browser-optimized`, `sprite-based`, `keyboard/mouse`, `fast-moving`, `step-by-step`, and `in-depth` guidance. Bundled files include `2d-maze-game.md`, `2d-platform-game.md`, `3d-web-games.md`, `algorithms.md`, `basics.md`, `game-control-mechanisms.md`, `game-engine-core-principles.md`, `game-publishing.md`, `gameBase-template-repo.md`, `paddle-game-template.md`, `simple-2d-engine.md`, `techniques.md`, `terminology.md`, and `web-apis.md`.

## Output template

```markdown
### Game engine result

**Status:** created | plan only | review findings | blocked
**Game type:** <2D | 3D | engine | template | publishing>
**Rendering:** <Canvas 2D | WebGL | SVG | CSS | framework>

**Architecture**
- Loop: <input/update/render and delta-time strategy>
- Objects: <entities/components/state>
- Physics/collision: <approach>
- Controls: <keyboard/mouse/touch/gamepad>
- Audio: <Web Audio API | HTML5 Audio | none>

**Resources used**
- `<asset or reference>`: <why>

**Validation**
- <browser/test/build check>: pass | fail
```

## Quality gate

- [ ] The game loop uses `requestAnimationFrame` and delta time.
- [ ] Rendering technology matches the requested game type.
- [ ] Input, update, render, physics/collision, controls, and audio decisions are explicit.
- [ ] Fast-moving collision cases are handled or documented.
- [ ] Touch, audio, and WebGL browser constraints are considered when relevant.
- [ ] Bundled assets or references used are named and actually relevant.
- [ ] Validation includes a browser run, build, or targeted check when implementation changes are made.
