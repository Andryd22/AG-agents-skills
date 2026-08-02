# Scroll 3D Unifier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aggiungere skill `three-js` (Scroll 3D, modulare con references), agent `scroll-experience-architect` e workflow `/scroll-experience` al kit Antigravity, unificando three-js + scroll-film-studio + scroll-world.

**Architecture:** Skill modulare con progressive disclosure (SKILL.md core ~250 righe + 5 references on-demand), agent persona auto-detectata con le 3 skill, workflow pipeline a 5 step che delega al motore scelto (code-first Three.js, video opzionale Higgsfield). Documentazione sincronizzata (README.md + ARCHITECTURE.md + tasks/todo.md).

**Tech Stack:** Markdown-only (frontmatter YAML per agent/workflow). Nessuna dipendenza runtime. Tre.js = argomento della skill, non dipendenza del kit.

## Global Constraints

- File skill in `.agent/skills/three-js/` — SKILL.md richiesto, references in `references/`
- File agent in `.agent/agents/` — frontmatter YAML con chiavi quotate (`"name"`, `"description"`, `"model"`, `"tools"`, `"skills"`), come agent esistenti
- File workflow in `.agent/workflows/` — frontmatter `name`/`description` + body con `# /<name>`, sezioni Flow e Usage, come `scroll-film.md`
- Lingua file di contenuto: inglese (convenzione kit, es. scroll-film-studio)
- Conteggi finali: **51 skill, 26 agenti, 15 workflow** in README.md e ARCHITECTURE.md
- Commit separati per task, messaggi conventional commits
- NOTA: riga ARCHITECTURE.md:303 `| **Total Workflows** | 13 |` è bug preesistente → portare a `15` (non 14)

---

### Task 1: Skill `three-js` — SKILL.md core

**Files:**
- Create: `.agent/skills/three-js/SKILL.md`
- Verify: `ls .agent/skills/ | wc -l` (51 dopo questo task)

**Interfaces:**
- Produces: skill `three-js` referenziabile da frontmatter `skills:` di agent (Task 6) e citata in workflow (Task 7)

- [ ] **Step 1: Create SKILL.md**

```markdown
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
6. **Scroll hijacking** — never fight native scroll. Lenis (smooth) + ScrollTrigger `scrollerProxy` if you must; otherwise let native scroll drive progress via `scrollTrigger.onUpdate`.
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
```

- [ ] **Step 2: Verify**

Run: `test -f .agent/skills/three-js/SKILL.md && grep -c "^#" .agent/skills/three-js/SKILL.md`
Expected: file exists, heading count ≥ 10.

- [ ] **Step 3: Commit**

```bash
git add .agent/skills/three-js/SKILL.md
git commit -m "feat(skill): add three-js core SKILL.md for scroll-driven WebGL scenes"
```

---

### Task 2: Skill `three-js` — reference `scene-architecture.md`

**Files:**
- Create: `.agent/skills/three-js/references/scene-architecture.md`

**Interfaces:**
- Consumes: SKILL.md golden rules (Task 1)
- Produces: patterns referenced by Tasks 3-5 (scene builders, material factory)

- [ ] **Step 1: Create reference**

```markdown
# Scene Architecture

## Renderer factory

```js
const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector('.webgl-canvas'),
  antialias: matchMedia('(min-width: 1024px)').matches && !isMobile,
  powerPreference: 'high-performance',
});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
```

## Scene + camera baseline

```js
const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x0b0e14, 8, 40); // match bg; covers far plane pop
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 100);

const resize = () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
};
addEventListener('resize', debounce(resize, 150));
```

## Geometry rules

- Static geometry → merge into one BufferGeometry (`BufferGeometryUtils.mergeGeometries`).
- Repeated objects (columns, trees, particles) → `InstancedMesh`, update `instanceMatrix` only when visible.
- Never mutate `position/rotation/scale` of geometry data after upload; transform meshes, not vertices.

## Material factory (dispose-safe)

```js
const mats = new Set();
function mat(opts) {
  const m = new THREE.MeshStandardMaterial(opts);
  mats.add(m);
  return m;
}
function disposeAll() {
  mats.forEach((m) => m.dispose());
  scene.traverse((o) => o.geometry && o.geometry.dispose());
  mats.clear();
}
```

## Lighting order

1. Ambient or HemisphereLight (base fill, free)
2. DirectionalLight (key, one) — shadow maps only desktop, 1024, tight `shadow.camera`
3. Optional: spot/point for accents — count against draw budget
4. No more than one shadow-casting light per scene

## Textures

```js
const tex = new THREE.TextureLoader().load(url);
tex.colorSpace = THREE.SRGBColorSpace;      // color maps
tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
```

- Power-of-two sizes; KTX2/Basis for texture sets
- `texture.generateMipmaps = true` (default) unless nearest-filter pixel art

## Scene groups by section

```js
const sections = {};
document.querySelectorAll('[data-scene]').forEach((el) => {
  sections[el.dataset.scene] = new THREE.Group(); // one group per story beat
  scene.add(sections[el.dataset.scene]);
});
```

Later tasks animate per-group — a section hides/shows without touching others.
```

- [ ] **Step 2: Verify**

Run: `test -f .agent/skills/three-js/references/scene-architecture.md && grep -c "```" .agent/skills/three-js/references/scene-architecture.md`
Expected: code fences even count ≥ 4.

- [ ] **Step 3: Commit**

```bash
git add .agent/skills/three-js/references/scene-architecture.md
git commit -m "feat(skill): add three-js scene-architecture reference"
```

---

### Task 3: Skill `three-js` — reference `scroll-integration.md`

**Files:**
- Create: `.agent/skills/three-js/references/scroll-integration.md`

**Interfaces:**
- Consumes: scene baseline from Task 2 (`renderer`, `scene`, `camera`, `sections`)
- Produces: scroll API (single driver pattern) used by Task 4 camera choreography

- [ ] **Step 1: Create reference**

```markdown
# Scroll Integration

## One driver: GSAP ScrollTrigger + scrub

```js
gsap.registerPlugin(ScrollTrigger);

// pin a 100vh stage while progress 0→1 maps to scene timeline
gsap.to('.stage', {
  scrollTrigger: {
    trigger: '.stage',
    start: 'top top',
    end: '+=200%',
    scrub: 1,               // 1s catch-up smoothing; true = hard lock
    pin: true,
    onUpdate: (self) => timeline.progress(self.progress),
  },
});

const timeline = gsap.timeline({ paused: true });
timeline.to(sections.hero.position, { y: -6, ease: 'none' }, 0)
         .to(camera.position, { z: 4, y: 2, ease: 'none' }, 0.4);
```

Rule: scrub callbacks are the ONLY animation driver. No second rAF loop on the same objects.

## Parallax layers (no pin needed)

```js
document.querySelectorAll('[data-speed]').forEach((el) => {
  gsap.to(el, {
    yPercent: () => (el.dataset.speed - 1) * 100,
    ease: 'none',
    scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true },
  });
});
```

## Scroll-progress camera (native scroll, no pin)

```js
const tl = gsap.timeline({
  scrollTrigger: { trigger: '#story', start: 'top bottom', end: 'bottom top', scrub: true },
});
tl.fromTo(camera.position, { z: 12 }, { z: 2 })
  .fromTo(camera.rotation, { x: -0.15 }, { x: 0 }, 0);
```

## Lenis smooth scroll (optional)

```js
const lenis = new Lenis({ smoothWheel: true });
function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
requestAnimationFrame(raf);
ScrollTrigger.scrollerProxy(document.body, {
  scrollTop(value) { return arguments.length ? lenis.scrollTo(value, { immediate: true }) : lenis.scroll; },
});
```

## Pause when hidden

```js
document.addEventListener('visibilitychange', () => {
  const hidden = document.hidden;
  lenis && hidden ? lenis.stop() : lenis && lenis.start();
  gsap.globalTimeline.timeScale(hidden ? 0 : 1);
});
```

## Pitfalls

- `scrub: true` + heavy per-frame work → use `scrub: 1` and cache progress
- Pin spacing: pin pushes layout — reserve with `scrollTrigger.pinSpacing = false` + manual padding when needed
- Camera transforms fight CSS transforms on the same element — never both
```

- [ ] **Step 2: Verify**

Run: `test -f .agent/skills/three-js/references/scroll-integration.md && grep -c "ScrollTrigger" .agent/skills/three-js/references/scroll-integration.md`
Expected: ≥ 4 occurrences.

- [ ] **Step 3: Commit**

```bash
git add .agent/skills/three-js/references/scroll-integration.md
git commit -m "feat(skill): add three-js scroll-integration reference"
```

---

### Task 4: Skill `three-js` — reference `camera-choreography.md`

**Files:**
- Create: `.agent/skills/three-js/references/camera-choreography.md`

**Interfaces:**
- Consumes: scroll driver from Task 3 (timeline progress), `camera` from Task 2
- Produces: rig pattern used by workflow seam check (Task 7 mentions fly-through continuity)

- [ ] **Step 1: Create reference**

```markdown
# Camera Choreography

## Principle

Camera = narrator. Each story beat gets a "shot"; scroll progress moves between shots. Plan the path on paper before coding: `[outside → door → interior → next scene]`.

## Fixed camera, moving world (default, cheapest)

```js
// camera stays; sections move toward it
timeline.to(sections.hero.position, { z: 10, ease: 'none' }, 0)
        .to(sections.hero.rotation, { y: Math.PI * 2, ease: 'none' }, 0)
        .to(sections.interior.position, { z: 10, ease: 'none' }, 0.5);
```

## Fly-through path (CatmullRom)

```js
const path = new THREE.CatmullRomCurve3([
  new THREE.Vector3(0, 1.6, 14),
  new THREE.Vector3(0, 1.6, 8),
  new THREE.Vector3(1.2, 1.6, 4),
  new THREE.Vector3(0, 1.2, 0.5),
]);
const lookTarget = new THREE.Vector3();
timeline.to({ t: 0 }, {
  t: 1, duration: 1, ease: 'none',
  onUpdate() {
    const p = path.getPointAt(this.targets()[0].t);
    camera.position.copy(p);
    camera.lookAt(lookTarget.lerp(OUTSIDE_TARGET, this.targets()[0].t));
  },
});
```

Use `getPointAt` (arc-length) not `getPoint` — constant speed.

## Dolly + look (two-shot)

```js
timeline.fromTo(camera.position, { x: -3, z: 8 }, { x: 3, z: 4, ease: 'none' }, 0)
        .fromTo(camera.rotation, { y: 0.5 }, { y: -0.4, ease: 'none' }, 0);
```

## Orbit scrub (product viewer)

```js
timeline.fromTo(camera.position, { x: 4, z: 4 }, { x: -4, z: 4, ease: 'none' }, 0);
// keep camera.lookAt(product.position) each frame in onUpdate
```

## Shot-to-shot continuity

- End position of shot N = start of shot N+1 (match position + look target).
- Ease between shots: `ease: 'none'` inside a beat, different beats on the same timeline 0.0 / 0.33 / 0.66 marks.
- Avoid cuts: overlap beats 5-8% so the camera is mid-flight at section boundaries.
- If a hard cut is required, fade fog or flash a section background — never snap the camera.

## Easing cheat-sheet

| Motion | Ease |
| --- | --- |
| Settle into a space | `power2.inOut` |
| Explosive entry | `power4.out` |
| Constant fly-through | `none` |
| Soft drift | `sine.inOut` |
| Keyframed stops | `steps(4)` for mechanical feels |
```

- [ ] **Step 2: Verify**

Run: `test -f .agent/skills/three-js/references/camera-choreography.md && grep -c "timeline" .agent/skills/three-js/references/camera-choreography.md`
Expected: ≥ 4 occurrences.

- [ ] **Step 3: Commit**

```bash
git add .agent/skills/three-js/references/camera-choreography.md
git commit -m "feat(skill): add three-js camera-choreography reference"
```

---

### Task 5: Skill `three-js` — references `performance.md` + `verification.md`

**Files:**
- Create: `.agent/skills/three-js/references/performance.md`
- Create: `.agent/skills/three-js/references/verification.md`

**Interfaces:**
- Consumes: golden rules from Task 1 (budget numbers must match)
- Produces: jank-test procedure referenced by workflow step 4 (Task 7)

- [ ] **Step 1: Create `performance.md`**

```markdown
# Performance

## Budgets

| Tier | Draw calls | Triangles | Pixel ratio | Shadows |
| --- | --- | --- | --- | --- |
| Desktop | < 100 | < 300k | min(dpr, 2) | 1 × 1024 |
| Mobile | < 50 | < 100k | min(dpr, 1.5) | none |

## Measurement

Open DevTools → Performance → record 10s of scrolling. Flags:
- Frames > 16.7ms budget → find the hotspot below
- Long tasks > 50ms → JS work off the scroll handler

Console: `renderer.info.render` after each scene change — watch `calls`, `triangles`, `geometries`, `textures`.

## Hotspot ladder (fix in order)

1. **Draw calls too high** → merge static geometry (`BufferGeometryUtils.mergeGeometries`), InstancedMesh for repeats, remove invisible objects (`mesh.visible = false` skips draw).
2. **Fill rate** → drop pixel ratio cap, reduce canvas size on small screens, avoid full-screen `EffectComposer` post FX on mobile.
3. **Textures** → KTX2/Basis compressed, mipmaps on, drop anisotropy on mobile.
4. **Shadow cost** → shrink `shadow.camera` frustum, lower map 512 on weak GPUs, or disable.
5. **JS in scroll path** → cache progress values; no layout reads in onUpdate; move work off `scrub` callbacks into a throttled rAF when cheap.

## Instancing snippet

```js
const mesh = new THREE.InstancedMesh(geo, mat, N);
mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
for (let i = 0; i < N; i++) {
  const m = new THREE.Matrix4().setPosition(xs[i], ys[i], zs[i]);
  mesh.setMatrixAt(i, m);
}
```

## Anti-flash rules

- `renderer.render` once after setup before first scroll frame
- Preload textures (Promise.all) before starting the reveal animation
```

- [ ] **Step 2: Create `verification.md`**

```markdown
# Verification

## Jank test (manual, 10 seconds)

1. DevTools → Performance → Start recording
2. Scroll top→bottom→top at constant speed, once
3. Stop, read Frames chart: any frame > 16.7ms with red long-task marks = FAIL
4. Repeat at 2× scroll speed (wheel tick) on desktop

PASS = max frame under 24ms, no long tasks > 50ms, no dropped frames cluster > 3 consecutive.

## Console checks

- `THREE.WebGLRenderer: Context Lost` — restore handler missing → FAIL
- `[.WebGL-0000] GL_INVALID_OPERATION` — geometry/material misuse → FAIL
- `Uniform buffers overflow` — too many lights/materials → FAIL
- Warning: `THREE.ColorManagement` colorSpace mismatch — fix SRGB on textures

## GPU stats gate

Run once after build, log to console for the record:

```js
console.table({
  drawCalls: renderer.info.render.calls,
  triangles: renderer.info.render.triangles,
  geometries: renderer.info.memory.geometries,
  textures: renderer.info.memory.textures,
});
```

Compare against performance.md budgets. Over budget → fix before deploy, never ship a red budget.

## Functional checklist

- [ ] Scene renders on first paint (no flash of empty canvas)
- [ ] All data-scene sections reachable by scroll; none stuck off-path
- [ ] Camera never clips through geometry (nudge path waypoints)
- [ ] Resize works (aspect + size update, no distortion)
- [ ] Mobile: no shadows, pixel ratio ≤ 1.5, budget < 50 calls
- [ ] Tab hidden → animation paused; visible → resumes without jump
- [ ] Re-navigation: no memory growth (Performance monitor memory graph flat)

## Automated smoke

If repo has a test runner: assert `renderer.info.render.calls < budget` after scene mount + first scroll tick, and `performance.memory.usedJSHeapSize` delta < 50MB after 10 navigation cycles.
```

- [ ] **Step 3: Verify**

Run: `test -f .agent/skills/three-js/references/performance.md && test -f .agent/skills/three-js/references/verification.md && ls .agent/skills/three-js/references | wc -l`
Expected: `5`

- [ ] **Step 4: Commit**

```bash
git add .agent/skills/three-js/references/performance.md .agent/skills/three-js/references/verification.md
git commit -m "feat(skill): add three-js performance and verification references"
```

---

### Task 6: Agent `scroll-experience-architect`

**Files:**
- Create: `.agent/agents/scroll-experience-architect.md`
- Verify: `ls .agent/agents/ | wc -l` → 26

**Interfaces:**
- Consumes: skills `three-js` (Tasks 1-5), `scroll-film-studio`, `scroll-world` (esistenti)
- Produces: persona citata in SKILL.md (Task 1, sezione Delegate) e workflow (Task 7)

- [ ] **Step 1: Create agent file**

```markdown
---
"name": "scroll-experience-architect"
"description": "Creative-technical architect for immersive scroll-driven web experiences that combine 3D scenes, cinematic motion, and optionally pre-rendered video. Orchestrates three-js, scroll-film-studio, and scroll-world skills into one continuous scroll narrative. Use for scroll experiences, 3D fly-through sites, scrollytelling with WebGL, hybrid scroll sites (3D + video), diorama worlds, scroll-cinematic landing pages. Triggers on scroll experience, scroll 3D, fly-through, scrollytelling, cinematic scroll, WebGL scroll, 3D hero."
"model": "inherit"
"tools":
- "Read"
- "Grep"
- "Glob"
- "Bash"
- "Edit"
- "Write"
"skills":
- "three-js"
- "scroll-film-studio"
- "scroll-world"
---

# Scroll Experience Architect

You are a creative-technical architect who builds immersive scroll-driven web experiences. You think like a film director and build like a 3D engineer: every section is a shot, the camera is the narrator, scroll is the playhead.

## Core Philosophy

> "The user never scrolls a page — they fly through a world."

## Mindset

- **Narrative-first**: Define story beats before any geometry. Each beat = one scene group.
- **Continuity**: Shots flow into each other; no cuts unless intentional. End of shot N = start of shot N+1.
- **Code-first**: WebGL (three-js) is the default engine — works everywhere, no external API needed.
- **Video only when earned**: pre-rendered clips (scroll-world/Higgsfield) only for photo-realism or real assets, and only with explicit user approval and API access.
- **Budget-aware**: performance budget is a deliverable, not an afterthought (draw calls, fps, mobile tier).

## Engine decision

1. Ask the interview questions first (topic, beats, brand kit, budget tier, mobile tier).
2. Default: **three-js** code lane.
3. Photo-realism / real-world assets + Higgsfield access available → **scroll-world** video lane for hero or interior shots.
4. Single unbroken cinematic camera, pure code, no 3D → **scroll-film-studio** lane.
5. Mixed sections → hybrid: pick engine per section, verify seams (SSIM for video-video, visual continuity for 3D↔video↔code).

## Output format (always)

Deliver a spec with 5 blocks:

1. **Concept** — named concept + 1-paragraph narrative
2. **Scene list** — each beat: content, camera shot, engine
3. **Camera path** — waypoints per shot, continuity notes
4. **Engine** — chosen lane(s) + why; dependencies (Lenis, ScrollTrigger, Higgsfield, etc.)
5. **Budget + verification** — draw calls, fps target, mobile tier; which verification run (jank test, SSIM check)

## Boundaries

- Never invent API keys or charge video generation without user approval.
- Don't mix two animation drivers on the same object (single-driver rule from three-js skill).
- When in doubt between lanes, pick the cheaper one and say why.
```

- [ ] **Step 2: Verify**

Run: `test -f .agent/agents/scroll-experience-architect.md && grep -c '"skills"' .agent/agents/scroll-experience-architect.md`
Expected: file exists, `"skills"` present once. Also `ls .agent/agents/ | wc -l` → 26.

- [ ] **Step 3: Commit**

```bash
git add .agent/agents/scroll-experience-architect.md
git commit -m "feat(agent): add scroll-experience-architect unifying three scroll skills"
```

---

### Task 7: Workflow `/scroll-experience`

**Files:**
- Create: `.agent/workflows/scroll-experience.md`

**Interfaces:**
- Consumes: agent persona (Task 6), skills three-js / scroll-film-studio / scroll-world
- Produces: slash command listed in README.md (Task 8)

- [ ] **Step 1: Create workflow file**

```markdown
---
name: scroll-experience
description: Build an immersive scroll-driven experience orchestrating three-js, scroll-film-studio, and scroll-world — code-first WebGL, cinematic code lanes, or pre-rendered video, chosen per interview. Trigger to unify multiple scroll techniques in one continuous narrative.
---

# /scroll-experience

Use this command when you want a full scroll-driven experience that may mix multiple techniques — 3D WebGL scenes, cinematic continuous-camera code, and pre-rendered video clips — into one continuous scroll narrative.

## Flow

1. **Step 0 — Interview**: topic, story beats, brand kit, budget tier, mobile tier. Decide engine: 3D code (three-js), video (scroll-world), cinematic code (scroll-film-studio), or hybrid.
2. **Step 1 — Concept Pitch**: 2-3 named concepts, each with a camera path and engine map per section.
3. **Step 2 — Build**: delegate to the chosen engine's skill; follow its golden rules and build flow. For hybrid, build section-by-section, keeping the single-driver rule.
4. **Step 3 — Seam & Hybrid Check**: verify transitions. Video↔video: SSIM seam check (scroll-world knockout). 3D↔video↔code: visual continuity walk — end position of shot N must equal start of shot N+1; no camera snaps.
5. **Step 4 — Verify & Deploy**: run jank test + GPU budget (three-js verification.md), then optional Vercel deploy.

## Usage

```
/scroll-experience 3D fly-through world for a coffee brand
/scroll-experience hybrid scrollytelling: 3D hero + video sections
/scroll-experience diorama landing with WebGL parallax layers
```
```

- [ ] **Step 2: Verify**

Run: `test -f .agent/workflows/scroll-experience.md && head -3 .agent/workflows/scroll-experience.md`
Expected: frontmatter `---` e `name: scroll-experience`.

- [ ] **Step 3: Commit**

```bash
git add .agent/workflows/scroll-experience.md
git commit -m "feat(workflow): add /scroll-experience orchestrating three scroll skills"
```

---

### Task 8: Documentazione — README.md e ARCHITECTURE.md

**Files:**
- Modify: `README.md` (tabella componenti: righe 21-26; tabella workflow: dopo riga `/latex`)
- Modify: `.agent/ARCHITECTURE.md` (righe 11, 13, 22, 31, 200, 301, 303 + tabella Frontend & UI + tabella workflow)

**Interfaces:**
- Consumes: nomi file dai Task 1-7

- [ ] **Step 1: Update README.md componenti**

Replace:
```
| **Agenti**    | 25       | Personas AI specializzate (frontend, backend, AI/ML, IoT, LaTeX, ecc.) |
```
with:
```
| **Agenti**    | 26       | Personas AI specializzate (frontend, backend, AI/ML, IoT, LaTeX, ecc.) |
```
Replace:
```
| **Skill**     | 50       | Moduli di conoscenza specifici per dominio                         |
```
with:
```
| **Skill**     | 51       | Moduli di conoscenza specifici per dominio                         |
```
Replace:
```
| **Workflow**  | 14       | Procedure attivabili tramite slash command                         |
```
with:
```
| **Workflow**  | 15       | Procedure attivabili tramite slash command                         |
```

- [ ] **Step 2: Add workflow row in README.md**

After the `| `/latex` ...` line, insert:
```
| `/scroll-experience` | Esperienze scroll immersive unificate: 3D (three-js) + cinematico (scroll-film-studio) + video (scroll-world) |
```

- [ ] **Step 3: Update ARCHITECTURE.md conteggi**

Replace (7 punti):
- `- **25 Specialist Agents** - Role-based AI personas` → `- **26 Specialist Agents** - Role-based AI personas`
- `- **14 Workflows** - Slash command procedures` → `- **15 Workflows** - Slash command procedures`
- `├── agents/                  # 25 Specialist Agents` → `├── agents/                  # 26 Specialist Agents`
- `## 🤖 Agents (25)` → `## 🤖 Agents (26)`
- `## 🔄 Workflows (14)` → `## 🔄 Workflows (15)`
- `| **Total Agents**    | 25                            |` → `| **Total Agents**    | 26                            |`
- `| **Total Workflows** | 13                            |` → `| **Total Workflows** | 15                            |`

- [ ] **Step 4: Add skill + agent + workflow rows in ARCHITECTURE.md**

Skill (dopo riga `scroll-world` in Frontend & UI):
```
| `three-js`           | Scroll-driven Three.js/WebGL scenes — scene, camera, scroll, perf      |
```
Agent (nella tabella agenti, dopo `explorer-agent`):
```
| `scroll-experience-architect` | Scroll experiences 3D/cinematic/video      | three-js, scroll-film-studio, scroll-world |
```
Workflow (sezione `## 🔄 Workflows`, dopo riga `/latex`):
```
| `/scroll-experience` | Unifies three-js + scroll-film-studio + scroll-world in one narrative |
```

- [ ] **Step 5: Verify conteggi**

Run:
```bash
grep -c "26" .agent/ARCHITECTURE.md && grep -rn "25 Specialist\|Workflows (14)\|Total Workflows | 13" .agent/ARCHITECTURE.md README.md; echo "exit=$?"
```
Expected: grep dei residui → exit 1 (nessun match), e conteggi aggiornati (51 skill / 26 agenti / 15 workflow coerenti).

- [ ] **Step 6: Commit**

```bash
git add README.md .agent/ARCHITECTURE.md
git commit -m "docs: update counts and tables for three-js skill and scroll-experience agent/workflow"
```

---

### Task 9: `tasks/todo.md` + verifica finale

**Files:**
- Create: `tasks/todo.md`
- Create: `tasks/lessons.md` (solo se già convenzione — altrimenti saltare)
- Verify: conteggi globali

**Interfaces:**
- Consumes: completamento Task 1-8

- [ ] **Step 1: Create `tasks/todo.md`**

```markdown
# Todo — Scroll 3D Unifier

## Implementazione (2026-08-02)

- [x] Skill `three-js`: SKILL.md + 5 references
- [x] Agent `scroll-experience-architect`
- [x] Workflow `/scroll-experience`
- [x] README.md + ARCHITECTURE.md sincronizzati (51 skill / 26 agenti / 15 workflow)

## Review

- [ ] Verifica skill auto-load: description matcha richieste "3D scroll"
- [ ] Verifica conteggi installazione `npx ... init -y`
```

- [ ] **Step 2: Verifica finale conteggi**

Run:
```bash
ls .agent/skills | grep -v README.md | wc -l   # 51
ls .agent/agents | wc -l                        # 26
ls .agent/workflows | wc -l                     # 15
git status --short
```
Expected: `51`, `26`, `15`; git status mostra solo file nuovi/modificati del piano.

- [ ] **Step 3: Commit**

```bash
git add tasks/todo.md
git commit -m "chore: track scroll-3d unifier implementation in tasks/todo.md"
```

---

## Self-Review (verificato)

- **Spec coverage**: sez.1 → Task 1-5; sez.2 → Task 6; sez.3 → Task 7; sez.4 → Task 8-9. Criteri successo coperti (conteggi verificati in Task 8-9; trigger in frontmatter Task 1/6; installabilità invariata — nessun file di config toccato).
- **Placeholder scan**: nessun TBD/TODO di contenuto; ogni file ha contenuto completo inline.
- **Type consistency**: `sections`/`camera`/`renderer`/`timeline` nominati identici tra Task 2-4; nomi skill/agent/workflow identici tra Task 1/6/7/8 (`three-js`, `scroll-experience-architect`, `scroll-experience`).
