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
4. **Step 3 — Seam & Hybrid Check**: verify transitions. Video↔video: SSIM seam check (scroll-world `references/pipeline.md` §5c; `knockout.py` only removes backgrounds). 3D↔video↔code: visual continuity walk — end position of shot N must equal start of shot N+1; no camera snaps.
5. **Step 4 — Verify & Deploy**: run jank test + GPU budget (three-js verification.md), then optional Vercel deploy.

## Usage

```
/scroll-experience 3D fly-through world for a coffee brand
/scroll-experience hybrid scrollytelling: 3D hero + video sections
/scroll-experience diorama landing with WebGL parallax layers
```
