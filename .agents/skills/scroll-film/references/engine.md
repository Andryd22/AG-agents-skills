# Ricette del motore — come si costruisce la pagina (entrambi i percorsi)

Non è un modello. Sono i meccanismi portanti che scrivi *dentro* ogni costruzione su
misura. Tutto il resto — markup, stili, forma del movimento, testi — lo progetti da zero
per ogni marchio.

---

## Motore di scrub (percorso B) — canvas + frame, mai `<video>`

Lo scrub con `<video currentTime>` scatta (latenza di seek). L'unica strada senza jank:
frame JPEG estratti prima e disegnati su un `<canvas>` a tutto schermo, guidati dallo scroll.

**Struttura:** un contenitore di scroll alto (`~170vh per capitolo`, es. `850vh` per 5) che
contiene uno stage `position:sticky; top:0; height:100vh` con il canvas e i livelli
sovrapposti. Avanzamento del film:

```js
const r = filmScroll.getBoundingClientRect();
const p = Math.max(0, Math.min(1, -r.top / (r.height - innerHeight)));
```

**Testina interpolata** (è quello che dà la morbidezza: la mappatura diretta sembra meccanica):

```js
currentFrame += (target - currentFrame) * 0.14;   // target = p * (FRAME_COUNT - 1)
```

**Il cuore contro il jank: finestra scorrevole di ImageBitmap.** `drawImage(HTMLImageElement)`
costringe a una decodifica JPEG *sincrona* sul thread principale al primo disegno, e di
nuovo quando il browser svuota la cache: quei picchi di decodifica sono l'effetto "a scatti
frame per frame". Decodifica fuori dal thread principale intorno alla testina, così ogni
disegno è una pura copia sulla GPU:

```js
const bitmaps = new Map(), decoding = new Set();
const B_AHEAD = 18, B_KEEP = 28; let bmpCenter = -999;
function ensureBitmaps(center){
  if (Math.abs(center - bmpCenter) < 3) return;
  bmpCenter = center;
  const lo = Math.max(0, center - B_AHEAD), hi = Math.min(FRAME_COUNT - 1, center + B_AHEAD);
  for (let i = lo; i <= hi; i++){
    if (bitmaps.has(i) || decoding.has(i) || !images[i]) continue;
    decoding.add(i);
    createImageBitmap(images[i]).then(b => {
      decoding.delete(i);
      if (Math.abs(i - bmpCenter) > B_KEEP){ b.close(); return; }
      bitmaps.set(i, b);
      if (i === displayed) drawFrame(i, true);      // ridisegna se il frame mostrato è migliorato
    }).catch(() => decoding.delete(i));
  }
  for (const k of Array.from(bitmaps.keys()))
    if (k < center - B_KEEP || k > center + B_KEEP){ bitmaps.get(k).close(); bitmaps.delete(k); }
}
// disegno: preferisci bitmaps.get(idx), altrimenti l'HTMLImageElement caricato più vicino
```

Chiama `ensureBitmaps(Math.round(currentFrame))` a ogni tick, **prepara in anticipo i frame
intorno al frame 0 all'avvio** e limita `devicePixelRatio` a **1.5** (2.0 raddoppia il costo
della copia per un guadagno che non si vede).

**Caricamento dei frame:** una pompa con concorrenza limitata (~10 in volo) che riempie un
array, un loader con una vera barra di avanzamento e un ripiego `nearestFrame()` (cerca
verso l'esterno a partire dall'indice richiesto), così un frame mancante non svuota mai il
canvas.

**Peso dei frame:** ~300 frame, larghi ~1280 px, JPEG `-q:v 4`. Le riprese scure o granulose
quasi raddoppiano i byte dei JPEG: resisti alla tentazione di andare più grande.

## Testi sui momenti (testo sopra il film)

Livelli in posizione assoluta con inviluppi di avanzamento, guidati dallo stesso tick:

```html
<div class="beat" data-in="0.16" data-peak="0.235" data-out="0.31"><h2>…</h2></div>
```

```js
function beatAlpha(b, p){
  if (p < b.in || p > b.out) return 0;
  if (p < b.peak) return (p - b.in) / Math.max(1e-4, b.peak - b.in);
  if (b.out > 1.5) return 1;                    // finale: data-out="2" non svanisce mai
  return 1 - (p - b.peak) / Math.max(1e-4, b.out - b.peak);
}
// alpha → style.opacity, più un piccolo translateY contro la direzione dello scroll
```

Il momento dell'hero deve essere visibile a scroll 0: `data-in="-0.1" data-peak="0"`. Se il
frame finale è un prodotto o un soggetto al centro, ancora il pannello finale a sinistra,
così il soggetto resta protagonista.

## Header adattivo (interfaccia fissa sopra un film che cambia)

Ogni ~180 ms campiona la striscia in alto del frame disegnato in un canvas fuori schermo
16×4, fai la media della luminanza e attiva o disattiva una classe `.on-light` (soglia
≈ 138). Tutti i colori dell'header passano da `currentColor`, così una sola classe cambia
tutto. Un **indicatore di capitolo** (etichetta + sottile barra di avanzamento) fa sia da
racconto sia da interfaccia di avanzamento, oppure dagli un tema (es. un altimetro che
scende insieme al film).

## Passaggio alla giuntura (film → contenuti, senza linea visibile)

Lo script di montaggio campiona il colore della striscia in basso dell'ultimo frame del
film. Fai iniziare lo sfondo della sezione successiva **esattamente con quell'hex**, e
aggiungi sullo stage del film una sfumatura in basso che entra nell'ultimo ~8%
dell'avanzamento (`(p - 0.92) / 0.08`). Con la stessa rampa fai svanire grana e vignettatura.
Se il film finisce scuro e i contenuti sono chiari, costruisci una "zona di atterraggio" alta
con un gradiente che passa dallo scuro al chiaro del marchio lungo il primo blocco di contenuti.

## Livello hero di sfondo (facoltativo, gratis, vende l'apertura)

Particelle su canvas a tema (neve che brilla, polline d'oro, braci) sopra il primo frame
fermo, che svaniscono nel primo ~7% dello scroll: uno sprite fuori schermo di 32 px con
gradiente radiale, un `drawImage` per particella con profondità diversa per ciascuna
(dimensione/velocità/alpha), scintillio o pulsazione basati su sin. Mai `shadowBlur` (costa
troppo). Smetti del tutto di disegnare quando l'alpha arriva a 0. Salta tutto con
`prefers-reduced-motion`.

## Il contratto di sviluppo (agganci per la verifica — in ogni costruzione)

```js
const JUMP = new URLSearchParams(location.search).get('jump');
if (JUMP !== null) history.scrollRestoration = 'manual';   // e salta l'avvio dello scroll morbido
// quando tutto è caricato e assestato:
if (JUMP !== null){ scrollTo(0, +JUMP || 0); /* ricalcola l'avanzamento, disegna, un tick */ }
window.__ready = true;
```

`?jump=<y>` deve aprire la pagina già scrollata con tutto lo stato guidato dallo scroll
assestato (nelle costruzioni solo codice: `ScrollTrigger.update()` e poi imposta
esplicitamente il `totalProgress` di ogni animazione con scrub). `__ready` fa da via libera
allo strumento degli screenshot. Nascondi qualsiasi elemento che segue il cursore fino al
primo vero `mousemove`, altrimenti compare nelle catture a (0,0).

Misuratore di jank per la console: tieni traccia dei delta di rAF per frame e scrivi il
`max` ogni 2 s. Giudica p95/massimo, mai gli fps medi: una media di 60 fps nasconde
perfettamente picchi di decodifica da 80 ms.

---

## Film solo in codice (percorso A) — il vocabolario del movimento

Il "film" è una sequenza di scene guidate dallo scroll. Collega Lenis al ticker di GSAP:

```js
const lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
```

Vocabolario da cui comporre (scegli quello che racconta il viaggio di *questo* marchio):

- **Rivelazione dell'hero lettera per lettera** — dividi il logotipo in span, sfasa
  `yPercent:120 → 0` con `power4.out`.
- **Scene fissate con scrub** — timeline con `pin: true, scrub: true, end: '+=140%'`
  (una forma che cresce o ruota, un "vortice" di fusione, una maschera che si apre a tutta
  pagina).
- **Scorrimento orizzontale fissato** — trasla una traccia `width:max-content` di
  `-(scrollWidth - innerWidth)`; dai agli elementi figli la loro parallasse con
  `containerAnimation`. Usa `invalidateOnRefresh: true`.
- **Rivelazioni con clip-path** — `inset(0 0 100% 0) → inset(0)` allo scroll per le righe
  editoriali.
- **Inclinazione in base alla velocità** — inclina un ticker/marquee con
  `ScrollTrigger.getVelocity()` limitato.
- **Contatori** — trigger con `once: true` e `snap: { textContent: 1 }`.
- **Marquee in deriva** — `xPercent: -50, repeat: -1` su una riga raddoppiata.

**Legge sull'ordine (killer silenzioso):** gli ScrollTrigger si aggiornano *nell'ordine di
creazione*. Crea **prima** tutte le scene fissate, **dopo** i trigger di sfondo: altrimenti
le posizioni calcolate prima che esistano gli spazi dei pin sono sbagliate senza nessun
errore (gli effetti scattano migliaia di pixel prima).

Prestazioni: solo proprietà gestite dalla GPU (transform/opacity), `will-change` sui pochi
nodi che si muovono, nessuna lettura del layout nei ticker. Stesso contratto di sviluppo e
stesso misuratore di jank del percorso B.
