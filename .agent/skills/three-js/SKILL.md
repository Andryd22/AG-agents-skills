---
name: three-js
description: >
  Build scroll-driven 3D scenes and immersive fly-through web experiences with
  Three.js and WebGL. Covers scene architecture (geometry, materials, lighting,
  textures, scene graph), scroll integration (GSAP ScrollTrigger + Lenis scrub,
  parallax, scroll-progress-driven animation), camera choreography (rigs,
  fly-through paths, easing), and performance budgets (draw calls, instancing,
  LOD, pixel ratio, 60fps target). Use when the user wants a 3D scene, WebGL
  experience, scroll-scrubbed 3D hero, 3D camera fly-through, parallax layers,
  product viewer, or immersive scroll 3D — and the answer should be code-rendered
  WebGL rather than pre-rendered video. Complements scroll-film-studio (cinematic
  code lanes) and scroll-world (pre-rendered video clips).
---

# Three.js — Scroll 3D

Build code-rendered WebGL scenes driven by scroll. Camera is the narrator; scroll is the playhead.

## When to use

| Request shape | Skill |
| --- | --- |
| 3D scene, WebGL, scroll 3D, camera fly-through, parallax, product viewer — code-rendered | **three-js** (this) |
| Cinematic continuous-camera site, pure-code GSAP/Lenis scrub, single unbroken shot | `scroll-film-studio` |
| Photo-realistic fly-through with pre-rendered video clips (Higgsfield) | `scroll-world` |
| Mixed sections (3D hero + video + code) | delegate to agent `scroll-experience-architect` |

## Golden rules

1. **Scene graph hygiene** — one renderer, one scene, one camera per page. Group by transform hierarchy; never mutate geometry on the fly (dispose + recreate instead).
2. **Draw call budget** — target < 100 draw calls desktop, < 50 mobile. Merge meshes, use InstancedMesh for repeated objects (trees, particles, crowd), bake what stands still.
3. **Renderer config** — `antialias: true` only on desktop; cap `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`; mobile cap 1.5.
4. **Dispose pattern** — every `new THREE.XxxGeometry/Material/Texture` must have a matching `.dispose()` on teardown. Use `renderer.dispose()`, traverse scene and dispose children, remove listeners. Memory leak = page death on re-navigation.
5. **No rAF conflict** — drive animation from ONE source. If GSAP ScrollTrigger scrubs, use `scrub: true` callbacks, not a separate rAF loop mutating the same transforms. Pause heavy work when tab hidden (visibilitychange).
6. **Scroll hijacking** — never fight native scroll. If you need smoothing, use Lenis driven by `gsap.ticker` with `lenis.on('scroll', ScrollTrigger.update)` (see `references/scroll-integration.md`); otherwise let native scroll drive progress via `scrollTrigger.onUpdate`.
7. **Lighting** — cheap lights first: ambient + directional, or hemisphere + one directional. Shadow maps only on desktop, small map size (1024), `shadow.camera` frustum tightly fitted.
8. **Textures** — power-of-two sizes, `colorSpace = THREE.SRGBColorSpace`, `texture.anisotropy = renderer.capabilities.getMaxAnisotropy()` when magnifying. Compress with basis/KTX2 for big sets.

## Build flow

1. HTML shell — canvas fixed full-viewport (`.webgl-canvas`), scrollable content sections with data-attributes as scene markers
2. Scene — renderer, camera (perspective, fov 45-60), fog matching design, background
3. Camera rig — see `references/camera-choreography.md`; start simple (fixed camera + moving world) before flying the camera
4. Scroll integration — ScrollTrigger pinning, scrub, progress mapping — see `references/scroll-integration.md`
5. Content — geometry/materials/textures per section, instanced where repeated
6. Performance — run `references/performance.md` budget checks before calling done
7. Verify — `references/verification.md` checklist, jank test, GPU stats

## Common errors

- **Leak**: forgot dispose → create on scene change, page slows then dies. Always pair create/dispose.
- **z-fighting**: coplanar surfaces → add `polygonOffset` or nudge geometry 0.001.
- **Fog vs far plane**: fog hides far plane pop — set `scene.fog` and renderer far together, or objects clip visibly.
- **Pixel ratio 4 on phone**: heavy fill rate → cap as in rule 3.
- **ScrollTrigger + transform fights**: two controllers writing same transform → pick one owner (rule 5).
- **Sizes on resize**: camera aspect + renderer size must update in one resize handler; debounce.

## Checklist (final)

- [ ] Scene graph: 1 renderer/scene/camera, groups clean
- [ ] Draw calls within budget (see performance.md)
- [ ] Pixel ratio capped; antialias desktop-only
- [ ] All creates have matching dispose; listeners removed
- [ ] Single animation driver; visibilitychange pauses heavy work
- [ ] Resize handler updates aspect + size
- [ ] jank test passes (verification.md)
- [ ] Works on mobile tier (tap targets, no heavy shadows)

## Delegate

Mixed-media or multi-section experiences (3D + video + cinematic code) → agent `scroll-experience-architect`. Don't improvise seam handling.
