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
