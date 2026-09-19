---
name: three-js
description: >
  Costruisce scene 3D guidate dallo scroll ed esperienze web immersive da
  attraversare in volo con Three.js e WebGL. Copre l'architettura della scena
  (geometrie, materiali, luci, texture, scene graph), l'integrazione con lo
  scroll (GSAP ScrollTrigger + scrub con Lenis, parallasse, animazioni guidate
  dall'avanzamento dello scroll), la coreografia della camera (rig, percorsi di
  volo, easing) e i budget di prestazioni (draw call, instancing, LOD, pixel
  ratio, obiettivo 60 fps). Usala quando l'utente vuole una scena 3D,
  un'esperienza WebGL, un hero 3D guidato dallo scroll, un volo della camera in
  3D, livelli di parallasse, un visualizzatore di prodotto o uno scroll 3D
  immersivo, e la risposta giusta è WebGL scritto in codice, non video
  pre-renderizzato. Si affianca a scroll-film (percorsi cinematici in codice) e
  scroll-world (clip video pre-renderizzate).
---

# Three.js — scroll 3D

Costruisci scene WebGL scritte in codice e guidate dallo scroll. La camera è il narratore; lo scroll è la testina di riproduzione.

## Quando usarla

| Tipo di richiesta | Skill |
| --- | --- |
| Scena 3D, WebGL, scroll 3D, volo della camera, parallasse, visualizzatore di prodotto, in codice | **three-js** (questa) |
| Sito cinematico con camera continua, solo codice con scrub GSAP/Lenis, un'unica inquadratura ininterrotta | `scroll-film` |
| Volo fotorealistico con clip video pre-renderizzate (Higgsfield) | `scroll-world` |
| Sezioni miste (hero 3D + video + codice) | passa il lavoro all'agente `scroll-experience-architect` |

## Regole d'oro

1. **Scene graph in ordine** — un renderer, una scena, una camera per pagina. Raggruppa per gerarchia di trasformazioni; mai modificare la geometria al volo (meglio dispose + ricreare).
2. **Budget di draw call** — obiettivo < 100 draw call su desktop, < 50 su mobile. Unisci le mesh, usa InstancedMesh per gli oggetti ripetuti (alberi, particelle, folle), fai il bake di quello che sta fermo.
3. **Configurazione del renderer** — `antialias: true` solo su desktop; limita `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`; su mobile al massimo 1.5.
4. **Dispose** — ogni `new THREE.XxxGeometry/Material/Texture` deve avere il suo `.dispose()` quando si smonta. Usa `renderer.dispose()`, attraversa la scena e fai dispose dei figli, togli i listener. Memory leak = pagina che muore quando si torna a navigarla.
5. **Niente conflitti di rAF** — l'animazione ha UNA sola sorgente. Se fa lo scrub GSAP ScrollTrigger, usa le callback di `scrub: true`, non un altro ciclo rAF che modifica le stesse trasformazioni. Metti in pausa il lavoro pesante quando la scheda è nascosta (visibilitychange).
6. **Scroll hijacking** — mai combattere lo scroll nativo. Se ti serve lo smoothing, usa Lenis guidato da `gsap.ticker` con `lenis.on('scroll', ScrollTrigger.update)` (vedi `references/scroll-integration.md`); altrimenti lascia che lo scroll nativo guidi l'avanzamento con `scrollTrigger.onUpdate`.
7. **Luci** — prima le luci economiche: ambientale + direzionale, oppure emisferica + una direzionale. Shadow map solo su desktop, mappa piccola (1024), frustum di `shadow.camera` stretto intorno alla scena.
8. **Texture** — dimensioni potenza di due, `colorSpace = THREE.SRGBColorSpace`, `texture.anisotropy = renderer.capabilities.getMaxAnisotropy()` quando si ingrandisce. Comprimi con basis/KTX2 i set grandi.

## Procedura

1. Struttura HTML — canvas fisso a tutto schermo (`.webgl-canvas`), sezioni di contenuto scorrevoli con data-attribute come marcatori delle scene
2. Scena — renderer, camera (prospettica, fov 45-60), nebbia coerente con il design, sfondo
3. Rig della camera — vedi `references/camera-choreography.md`; parti semplice (camera ferma + mondo che si muove) prima di far volare la camera
4. Integrazione con lo scroll — pin di ScrollTrigger, scrub, mappatura dell'avanzamento — vedi `references/scroll-integration.md`
5. Contenuti — geometrie/materiali/texture per sezione, con instancing dove si ripetono
6. Prestazioni — esegui i controlli di budget di `references/performance.md` prima di dire che è finito
7. Verifica — checklist di `references/verification.md`, test di jank, statistiche della GPU

## Errori comuni

- **Leak**: dispose dimenticato → a ogni cambio di scena si crea, la pagina rallenta e poi muore. Abbina sempre creazione e dispose.
- **Z-fighting**: superfici complanari → aggiungi `polygonOffset` o sposta la geometria di 0.001.
- **Nebbia e piano lontano**: la nebbia nasconde la comparsa al piano lontano — imposta insieme `scene.fog` e il far del renderer, altrimenti gli oggetti si vedono tagliare.
- **Pixel ratio 4 sul telefono**: fill rate pesante → limitalo come nella regola 3.
- **ScrollTrigger e trasformazioni in lotta**: due controller scrivono la stessa trasformazione → scegli un solo proprietario (regola 5).
- **Dimensioni al resize**: aspect della camera e dimensioni del renderer si aggiornano in un unico handler di resize; con debounce.

## Checklist (finale)

- [ ] Scene graph: 1 renderer/scena/camera, gruppi in ordine
- [ ] Draw call dentro il budget (vedi performance.md)
- [ ] Pixel ratio limitato; antialias solo su desktop
- [ ] Ogni creazione ha il suo dispose; listener tolti
- [ ] Un solo driver di animazione; visibilitychange mette in pausa il lavoro pesante
- [ ] L'handler di resize aggiorna aspect e dimensioni
- [ ] Il test di jank passa (verification.md)
- [ ] Funziona nella fascia mobile (aree di tocco, niente ombre pesanti)

## Delega

Esperienze con media misti o più sezioni (3D + video + codice cinematico) → agente `scroll-experience-architect`. Non improvvisare la gestione delle giunture.
