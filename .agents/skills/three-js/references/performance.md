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
