# Integrazione con lo scroll

## Un solo driver: GSAP ScrollTrigger + scrub

```js
gsap.registerPlugin(ScrollTrigger);

// fissa (pin) uno stage alto 100vh mentre l'avanzamento 0→1 guida la timeline della scena
gsap.to('.stage', {
  scrollTrigger: {
    trigger: '.stage',
    start: 'top top',
    end: '+=200%',
    scrub: 1,               // 1 s di recupero morbido; true = aggancio rigido
    pin: true,
    onUpdate: (self) => timeline.progress(self.progress),
  },
});

const timeline = gsap.timeline({ paused: true });
timeline.to(sections.hero.position, { y: -6, ease: 'none' }, 0)
         .to(camera.position, { z: 4, y: 2, ease: 'none' }, 0.4);
```

Regola: le callback dello scrub sono l'UNICO driver dell'animazione. Nessun secondo ciclo rAF sugli stessi oggetti.

## Livelli di parallasse (senza pin)

```js
document.querySelectorAll('[data-speed]').forEach((el) => {
  gsap.to(el, {
    yPercent: () => (el.dataset.speed - 1) * 100,
    ease: 'none',
    scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true },
  });
});
```

## Camera guidata dall'avanzamento (scroll nativo, senza pin)

```js
const tl = gsap.timeline({
  scrollTrigger: { trigger: '#story', start: 'top bottom', end: 'bottom top', scrub: true },
});
tl.fromTo(camera.position, { z: 12 }, { z: 2 })
  .fromTo(camera.rotation, { x: -0.15 }, { x: 0 }, 0);
```

## Scroll morbido con Lenis (facoltativo)

L'integrazione documentata da Lenis, la stessa di `scroll-film/references/engine.md`: il ticker di GSAP guida Lenis, quindi c'è un solo ciclo e niente `scrollerProxy`.

```js
const lenis = new Lenis({ smoothWheel: true });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

## Pausa quando la scheda è nascosta

```js
document.addEventListener('visibilitychange', () => {
  const hidden = document.hidden;
  lenis && hidden ? lenis.stop() : lenis && lenis.start();
  gsap.globalTimeline.timeScale(hidden ? 0 : 1);
});
```

## Trappole

- `scrub: true` + lavoro pesante a ogni frame → usa `scrub: 1` e metti in cache l'avanzamento
- Spazio del pin: il pin sposta il layout — riservalo con `scrollTrigger.pinSpacing = false` + padding manuale quando serve
- Le trasformazioni della camera litigano con le trasformazioni CSS sullo stesso elemento: mai entrambe
