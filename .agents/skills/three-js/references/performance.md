# Prestazioni

## Budget

| Fascia | Draw call | Triangoli | Pixel ratio | Ombre |
| --- | --- | --- | --- | --- |
| Desktop | < 100 | < 300k | min(dpr, 2) | 1 × 1024 |
| Mobile | < 50 | < 100k | min(dpr, 1.5) | nessuna |

## Misurare

Apri DevTools → Performance → registra 10 s di scroll. Segnali:

- Frame oltre il budget di 16,7 ms → cerca il punto caldo qui sotto
- Long task > 50 ms → lavoro JS da togliere dall'handler dello scroll

Console: `renderer.info.render` dopo ogni cambio di scena — guarda `calls`, `triangles`, `geometries`, `textures`.

## Punti caldi (correggili in quest'ordine)

1. **Troppe draw call** → unisci la geometria statica (`BufferGeometryUtils.mergeGeometries`), InstancedMesh per le ripetizioni, togli gli oggetti invisibili (`mesh.visible = false` salta il disegno).
2. **Fill rate** → abbassa il limite del pixel ratio, riduci il canvas sugli schermi piccoli, evita il post-processing a tutto schermo di `EffectComposer` su mobile.
3. **Texture** → KTX2/Basis compresse, mipmap attive, niente anisotropia su mobile.
4. **Costo delle ombre** → stringi il frustum di `shadow.camera`, mappa a 512 sulle GPU deboli, oppure disattivale.
5. **JS nel percorso dello scroll** → metti in cache i valori di avanzamento; nessuna lettura del layout in onUpdate; sposta il lavoro dalle callback di `scrub` a un rAF limitato, quando costa poco.

## Esempio di instancing

```js
const mesh = new THREE.InstancedMesh(geo, mat, N);
mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
for (let i = 0; i < N; i++) {
  const m = new THREE.Matrix4().setPosition(xs[i], ys[i], zs[i]);
  mesh.setMatrixAt(i, m);
}
```

## Regole contro i lampi

- Un `renderer.render` dopo la configurazione, prima del primo frame di scroll
- Precarica le texture (Promise.all) prima di far partire l'animazione di comparsa
