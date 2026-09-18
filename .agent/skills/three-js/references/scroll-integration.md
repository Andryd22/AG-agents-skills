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

Integration documented by Lenis, same as `scroll-film-studio/references/engine.md`: GSAP's ticker drives Lenis, so there is one loop and no `scrollerProxy`.

```js
const lenis = new Lenis({ smoothWheel: true });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
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
