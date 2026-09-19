# Architettura della scena

## Creare il renderer

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

## Scena e camera di base

```js
const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x0b0e14, 8, 40); // come lo sfondo; nasconde la comparsa al piano lontano
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 100);

const resize = () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
};
addEventListener('resize', debounce(resize, 150));
```

## Regole sulla geometria

- Geometria statica → uniscila in un'unica BufferGeometry (`BufferGeometryUtils.mergeGeometries`).
- Oggetti ripetuti (colonne, alberi, particelle) → `InstancedMesh`, aggiorna `instanceMatrix` solo quando sono visibili.
- Mai modificare `position/rotation/scale` nei dati della geometria dopo il caricamento; trasforma le mesh, non i vertici.

## Creare i materiali (con dispose sicuro)

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

## Ordine delle luci

1. Ambient o HemisphereLight (riempimento di base, gratis)
2. DirectionalLight (luce principale, una sola) — shadow map solo su desktop, 1024, `shadow.camera` stretto
3. Facoltative: spot/point per gli accenti — contano nel budget delle draw call
4. Al massimo una luce che proietta ombre per scena

## Texture

```js
const tex = new THREE.TextureLoader().load(url);
tex.colorSpace = THREE.SRGBColorSpace;      // mappe di colore
tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
```

- Dimensioni potenza di due; KTX2/Basis per i set di texture
- `texture.generateMipmaps = true` (predefinito), tranne per la pixel art con filtro nearest

## Gruppi di scena per sezione

```js
const sections = {};
document.querySelectorAll('[data-scene]').forEach((el) => {
  sections[el.dataset.scene] = new THREE.Group(); // un gruppo per momento della storia
  scene.add(sections[el.dataset.scene]);
});
```

Dopo si anima un gruppo alla volta: una sezione si nasconde o si mostra senza toccare le altre.
