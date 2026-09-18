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
