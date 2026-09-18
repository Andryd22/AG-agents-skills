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
