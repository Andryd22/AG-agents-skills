# Coreografia della camera

## Principio

Camera = narratore. Ogni momento della storia ha una sua "inquadratura"; l'avanzamento dello scroll passa da un'inquadratura all'altra. Pianifica il percorso su carta prima di scrivere codice: `[esterno → porta → interno → scena successiva]`.

## Camera ferma, mondo in movimento (predefinito, il più economico)

```js
// la camera resta ferma; le sezioni le vengono incontro
timeline.to(sections.hero.position, { z: 10, ease: 'none' }, 0)
        .to(sections.hero.rotation, { y: Math.PI * 2, ease: 'none' }, 0)
        .to(sections.interior.position, { z: 10, ease: 'none' }, 0.5);
```

## Percorso di volo (CatmullRom)

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

Usa `getPointAt` (lunghezza d'arco), non `getPoint`: velocità costante.

## Carrello + sguardo (due inquadrature)

```js
timeline.fromTo(camera.position, { x: -3, z: 8 }, { x: 3, z: 4, ease: 'none' }, 0)
        .fromTo(camera.rotation, { y: 0.5 }, { y: -0.4, ease: 'none' }, 0);
```

## Orbita con lo scrub (visualizzatore di prodotto)

```js
timeline.fromTo(camera.position, { x: 4, z: 4 }, { x: -4, z: 4, ease: 'none' }, 0);
// in onUpdate, a ogni frame: camera.lookAt(product.position)
```

## Continuità tra inquadrature

- Posizione finale dell'inquadratura N = inizio della N+1 (stessa posizione e stesso punto guardato).
- Easing tra le inquadrature: `ease: 'none'` dentro un momento, momenti diversi sulla stessa timeline ai segni 0.0 / 0.33 / 0.66.
- Evita i tagli: sovrapponi i momenti del 5-8%, così ai confini tra sezioni la camera è in pieno volo.
- Se serve un taglio netto, sfuma la nebbia o fai lampeggiare lo sfondo di una sezione: mai far scattare la camera.

## Promemoria degli easing

| Movimento | Easing |
| --- | --- |
| Assestarsi in uno spazio | `power2.inOut` |
| Ingresso esplosivo | `power4.out` |
| Volo a velocità costante | `none` |
| Deriva morbida | `sine.inOut` |
| Fermate a scatti | `steps(4)` per un effetto meccanico |
