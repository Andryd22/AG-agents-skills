# Modelli di prompt e intervista

Qui è tutto da riempire negli spazi. Tieni il **preambolo di stile** identico byte per byte in
tutte le immagini delle scene: è quel testo identico a far sembrare il mondo un unico luogo. I
prompt per i modelli di immagine e video sono in inglese, perché i modelli li seguono meglio;
i testi del sito sono nella lingua del pubblico del marchio.

## Checklist dell'intervista (passo 1)

Raccogli e annota:

- `SUBJECT` — l'attività + la presentazione in una riga.
- `BRAND_NAME` — il nome da mostrare.
- `PALETTE` — 4-6 hex con un nome, es. `taro #9B7EBD, cream #F5EDE0, caramel #C88A5A, matcha #8FB98A, plum #3A2E48`. Scegline UNO come colore di **sfondo** delle scene (di solito il più chiaro) e uno come **accent** principale.
- `TONE` — una o due parole (accogliente/premium, giocoso, industriale…).
- `STYLE` — la direzione artistica (predefinita qui sotto).
- `BUDGET_TIER` — leggera (~8 generazioni, 4 scene, arch. A) / standard (~11-14) / vetrina (17+). **Si chiede PRIMA del viaggio** (passo 1.4 di SKILL): numero di scene e architettura ne derivano. Il costo lo fanno i video: arch. A = N video, arch. B = 2N-1.
- `SECTIONS[]` — elenco ordinato **dimensionato su BUDGET_TIER**; per ciascuna: `id`, `label`, `subject` (cosa c'è nel diorama), `eyebrow`, `title`, `body` (≤ 1 frase), `tags[]` (0-3). Ultima sezione = prodotto di punta + CTA.
- `MOBILE` — fascia: ritaglio sicuro / codifiche mobile / hero reinquadrato / catena verticale. **Si chiede sempre** (passo 1.6 di SKILL) indicando i costi in crediti. Decide le codifiche `-m.mp4` + `posterMobile` (pipeline §6), le rese 9:16 (pipeline §7) e la QA mobile completa. I telefoni hanno l'animazione di scroll completa in ogni fascia.

## Preambolo di stile (predefinito: diorama di argilla)

Riusalo identico in ogni prompt di scena. Sostituisci le parti tra parentesi quadre con
palette e sfondo del marchio.

```text
Isometric low-poly 3D diorama floating as a small rounded island on a plain solid
[BG_HEX] background with a soft contact shadow beneath it. Soft matte clay 3D render,
rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift
miniature look. Cohesive color palette of [PALETTE]. Highly detailed, centered
composition, absolutely no text, no letters, no numbers, no logos.
```

Direzioni alternative (sostituisci le prime due frasi, tieni la coda con palette e "no text"):

- **Carta piatta:** "Isometric layered paper-craft diorama, matte cardstock, clean die-cut edges, subtle drop shadows between layers."
- **Giocattolo lucido:** "Isometric glossy vinyl-toy diorama, smooth plastic shading, soft rim light, collectible figurine look."
- **Plastilina:** "Isometric stop-motion clay set, visible thumbprints, handmade plasticine texture, soft studio softbox light."
- **Notte al neon:** "Isometric miniature at night, warm interior glow and neon signage, moody rim light, wet reflective ground."
- **Architettura fotorealistica** (immobiliare, ospitalità, premium/lusso): "Ultra-photorealistic architectural photography of a single cohesive [subject], cinematic wide-angle, warm golden-hour light, natural materials, restrained designer furnishings, a breathtaking view, editorial magazine quality (Architectural Digest), shallow depth of field, no people." Con il fotorealismo togli l'inquadratura a isola sospesa e la rimozione dello sfondo (passo 3): le scene sono **a tutta pagina** (uno sfondo scuro della pagina dà un'aria premium), il "tuffo" scivola *attraverso porte e vetrate* invece di aprire un tetto, e la coerenza viene tutta dal preambolo identico (NON passare un riferimento `--image`: clonerebbe la stessa stanza). Gli interni fanno scattare spesso il filtro NSFW di Seedance; vedi le Trappole di SKILL.

## Prompt dell'immagine della scena (passo 2)

```text
[STYLE PREAMBLE]
Subject: [SECTION.subject — describe the miniature scene: the building/space, a few
characters doing the work, the props that signal this stage of the business].
```

Consigli:

- Nomina oggetti concreti (ancorano la scena): vasche, calderoni, nastri trasportatori, casse, tende da sole, lucine, panchine, scooter, segnaposto sulla mappa.
- Per la sezione finale del "prodotto di punta" togli l'inquadratura a isola di diorama e chiedi
  un unico prodotto enorme al centro, sospeso sullo stesso sfondo, con qualche piccolo oggetto
  che gli orbita intorno.
- **Componi per il centro.** La pagina mostra ogni clip con `object-fit:cover`, e un telefono in
  verticale ritaglia un frame 16:9 più o meno alla sua metà centrale. Tieni il soggetto principale
  centrato in orizzontale con un po' di spazio sopra, e non mettere niente di essenziale ai bordi
  estremi a destra e a sinistra: sui telefoni verrebbe tagliato. Così anche il punto focale del
  tuffo (verso cui vola la camera) resta dentro il ritaglio mobile. Per una scena che deve per forza
  mostrare tutta la larghezza su mobile, genera una variante 9:16 separata.
- Formato `3:2`, `--resolution 2k --quality high`.

## Prompt del tratto — architettura A, ripresa continua in avanti (passo 4)

`--start-image = l'ultimo frame REALE del tratto precedente` (tratto 0: l'immagine della prima
scena). **Niente `--end-image`.** Le frasi in grassetto sono il contratto di passaggio del
movimento: tienile identiche; l'espressività sta nel movimento a metà tratto.

```text
Single continuous cinematic camera move, no cuts. **Continue the same slow, steady
forward glide.** [MID-LEG MOVE — optional, from the library below.] The camera moves
into [SCENE i] toward [FOCAL POINT]. **In the final second, settle back into a slow,
steady forward glide toward [the doorway / opening / direction of the next scene].**
[STYLE tail + PALETTE]. Smooth, graceful, slow motion, subtle parallax. No text, no captions.
```

### Repertorio dei movimenti a metà tratto (scegli in base al concept; ometti per una scivolata semplice)

Le inversioni sono sicure *dentro* un tratto (è un'unica resa continua): solo una giuntura non
deve mai invertire. Per questo "ease back out" va bene a metà tratto.

- **Mezza orbita** (prodotto, lusso): "sweeping in a slow half-orbit around [the hero
  object], keeping it centered, then continuing past it"
- **Rivelazione in gru** (scala, atri, campus): "rising smoothly as the full scale of
  [the space] reveals below"
- **Carrellata laterale bassa** (linee di produzione, banconi, scaffali): "tracking low and level
  alongside [the line], foreground objects sliding past in parallax"
- **Avvicinamento + arretramento** (artigianato, dettagli): "pushing in close to [the craft moment] until
  it nearly fills the frame, then easing gently back out"
- **Salita e picchiata** (viaggi, all'aperto): "climbing in a gentle arc over [the terrain],
  then swooping down toward [the next focal point]"

Dopo aver reso ogni tratto, **controlla il suo ultimo frame** prima di generare il successivo:
deve sembrare un frame di una calma scivolata in avanti (niente mosso laterale, niente orbita a
metà). Se non è così, rifai questo tratto: un frame di passaggio sbagliato avvelena tutti i tratti dopo.

## Prompt della clip di tuffo (passo 4)

`--start-image = l'immagine della scena` (versione con sfondo pieno).

```text
Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the
whole [SECTION.subject] from outside like a tiny model. The camera slowly glides forward
and descends toward it, sweeping in toward [FOCAL POINT — the counter/the cauldrons/the
people], as if flying inside. As the camera pushes in, the roof and upper structure
gently lift and open away to reveal the warm interior. [STYLE tail: soft matte clay
diorama, tilt-shift miniature, warm light, [PALETTE]]. Smooth, graceful, slow motion,
subtle parallax. No text, no captions.
```

Per le scene senza un edificio da aprire (un campo, una piazza, una strada), sostituisci la frase
del tetto con "the camera flies low across [the scene] toward [focal point]."

Parametri per modello della catena (tabella del passo 4 di SKILL): seedance —
`--mode std --resolution 1080p --aspect_ratio 16:9 --duration 8`, nessun flag per l'audio;
kling3_0 — `--mode std --sound off --aspect_ratio 16:9 --duration 10` (nessun parametro
`--resolution`). Gli stessi per i tratti dell'architettura A.

## Prompt della clip connettore (passo 5)

`--start-image = ULTIMO frame di dive_i` (estratto), `--end-image = PRIMO frame di dive_{i+1}`
(estratto). Entrambi dai video RENDERIZZATI, non dalle immagini.

```text
Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back
out of [SCENE i], rising into the sky, then glides forward across the connected miniature
world and arrives above [SCENE i+1], beginning to descend toward it. One connected
miniature clay world, seamless flowing aerial transition. [STYLE tail + PALETTE]. Smooth
graceful slow motion. No text, no captions.
```

Per l'ultimo connettore verso un finale con il prodotto di punta: "…glides forward and the world
dissolves toward a single giant [PRODUCT] floating in soft [BG] space, arriving in front
of it."

seedance: `--mode std --resolution 1080p --aspect_ratio 16:9 --duration 5`; kling3_0:
`--mode std --sound off --aspect_ratio 16:9 --duration 5`. I connettori richiedono `--end-image`
→ usa un modello dell'elenco che lo accetta (passo 4).

## Testi per sezione (per la configurazione del motore)

- `eyebrow` — 2-4 parole, dall'aria maiuscola (un'etichetta di valore).
- `title` — 3-6 parole, il titolo del momento. Prima sezione = la frase hero del sito; ultima =
  la conclusione, e porta la CTA.
- `body` — una frase, semplice, dal punto di vista del visitatore.
- `tags` — 0-3 brevi etichette di prova (es. "Cucinato al momento", "Consegna in 30 minuti").
