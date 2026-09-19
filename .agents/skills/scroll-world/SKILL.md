---
name: scroll-world
description: >
  Costruisce con Higgsfield una landing page immersiva "volo attraverso il mondo", guidata dallo scroll, per qualsiasi settore o
  marchio. Mentre il visitatore scorre, una camera pre-renderizzata vola da fuori ogni scena fin dentro il suo interno e poi
  prosegue verso la scena successiva SENZA tagli: un unico volo continuo e collegato (mondo a diorama isometrico in stile Emons, o
  qualsiasi direzione artistica scelta). La skill intervista l'utente su argomento, momenti/sezioni della storia e brand kit, poi
  genera con Higgsfield scene coerenti e clip di camera senza giunture e collega un motore di scrub portabile, indipendente dal
  framework. Usala quando l'utente vuole un hero "mondo 3D" / "viaggio dentro il settore", uno scroll cinematico, una landing a
  diorama, o trasformare un'attività in un mondo da scorrere.
---

# scroll-world

Produce una landing page in cui **lo scroll guida una camera**: si tuffa da fuori una scena
dentro il suo interno, poi esce e vola dentro la scena successiva, senza interruzioni e
senza tagli visibili. Le immagini sono generate dall'AI (Higgsfield); la pagina fa solo lo
scrub di video pre-renderizzati in base alla posizione dello scroll. È la stessa tecnica
delle pagine prodotto di Apple: la camera si muove davvero, lo scroll guida solo il tempo.

**Cosa generi:** N immagini delle scene (dopo l'approvazione dell'anchor) → N clip di camera
"tuffo" → N-1 clip "connettori" che uniscono senza giunture le scene consecutive → clip
codificate + poster estratti → un controllo SSIM automatico delle giunture → un motore di
scrub portabile che riproduce tutta la catena come un unico volo. Per impostazione
predefinita le clip della catena si generano prima al livello previz economico; i crediti
del modello completo si spendono solo dopo che l'utente ha approvato la bozza.

**L'unica regola che decide tutto:** le giunture devono essere *identiche frame per frame*.
Leggi i passi 4 e 5 prima di generare qualsiasi clip: sbagliare qui è l'errore più comune
(uno "scatto"). I prompt per i modelli di immagine e video restano in inglese.

Non dare per scontato un framework frontend. Il motore di scrub in `references/scrub-engine.js`
è JavaScript puro autosufficiente (costruisce il suo DOM e inietta il suo CSS in un
contenitore che gli passi), quindi va in HTML semplice, Next.js, Vue, una pagina servita da
Python, qualsiasi cosa. Il valore di questa skill è la pipeline di Higgsfield, i prompt e il
metodo delle giunture, non il framework.

---

## Passo 0 — Preparazione

1. **CLI di Higgsfield.** Se `higgsfield` non è nel `$PATH`, installala seguendo la skill
   `higgsfield-generate`. Se `higgsfield workspace list` fallisce l'autenticazione, chiedi
   all'utente di lanciare `higgsfield auth login` (OAuth interattivo: non puoi farlo tu) e,
   se serve, `higgsfield workspace set <id>`. Verifica che i crediti bastino: una corsa è `N`
   generazioni di immagini + `N` generazioni video (architettura A) o `(2N-1)` (architettura
   B), più i rifacimenti; `N` lo fissa la fascia di budget del passo 1.
2. **ffmpeg / ffprobe** nel `$PATH` (estrazione dei frame e codifica).
3. **Uno strumento per le immagini** per togliere lo sfondo, se vuoi le scene sospese: PIL
   (`python3 -c "import PIL"`), oppure `cwebp`/`sips`. Facoltativo: vedi il passo 3.
4. Avvertenze: macOS ha **bash 3.2** (niente `declare -A`): negli script niente array
   associativi. Ogni generazione di Higgsfield dura **3-8 minuti**: lanciale sempre staccate
   (in background) e controllale, mai una chiamata bloccante in primo piano. Il riferimento
   per UUID del job è rifiutato dai flag dei media: passa **percorsi di file locali** a
   `--image/--start-image/--end-image`. I modelli video accettano parametri diversi (es.
   Kling non ha `--resolution`) e non tutti supportano il condizionamento con immagine
   iniziale/finale: prima di lanciare un lotto, conferma lo schema del modello scelto con
   `higgsfield model get <job_type>` e guarda la tabella dei modelli del passo 4.

---

## Passo 1 — Intervista l'utente

L'**argomento lo decide l'utente: chiedilo come domanda aperta, in prosa**, mai con una
scelta multipla inventata. Un elenco di settori inventato lo condiziona e sembra che tu
stia decidendo la sua attività al posto suo; lascia che risponda con parole sue (la sua
attività, quella di un cliente, o qualsiasi idea). Tieni le domande a scelta (con opzioni)
per le decisioni davvero enumerabili e meno importanti qui sotto — direzione artistica e
brand kit — e anche lì fai capire che può fare a modo suo ("Altro"). Chiedi solo quello
che non puoi decidere tu in modo sensato. Copri:

1. **Argomento** (domanda aperta, non a scelta multipla) — "Di cosa deve parlare questo
   mondo? La tua attività, quella di un cliente o qualsiasi idea: basta una parola o una
   frase." Raccogli settore/prodotto + una presentazione in una riga (es. "un'azienda di
   bubble tea, dalla foglia all'ultimo sorso") e il nome del marchio, se c'è; altrimenti
   ne proporrai uno qui sotto.
2. **Brand kit** — offri tre strade, scegline una:
   - Importazione da un URL: `higgsfield marketing-studio brand-kits fetch --url <sito> --wait`
     (prende nome, colori, tono). Poi rileggilo con `brand-kits list --json`.
   - L'utente ti dà direttamente palette, nome e tono.
   - Proponi tu palette e nome e lui li approva.
   Raccogli **4-6 valori hex con un nome**, un nome da mostrare e una o due parole di tono.
3. **Direzione artistica** — il predefinito è "soft matte low-poly **clay diorama**,
   isometric, tilt-shift miniature, warm light". Offri alternative (carta piatta, giocattolo
   lucido, plastilina, notte al neon). Quella scelta diventa il **preambolo di stile**
   condiviso, riusato identico in ogni prompt di scena (è quello che rende coerente il mondo).
4. **Fascia di budget — chiedila PRIMA di proporre il viaggio; il costo lo fanno i video.**
   Il conto cresce con il numero di scene e con l'architettura: architettura A (ripresa in
   avanti) = `N` video, architettura B (tuffi + connettori) = `2N-1` video, più `N` immagini
   e un margine del ~20-30% per i rifacimenti. Una corsa in B con 6 scene è ~17 generazioni:
   un bel morso a un abbonamento. Fai la domanda a scelta con numeri concreti:
   - **Leggera (~8 generazioni)** — 4 scene, architettura A (4 immagini + 4 tratti), niente
     previz (le corse piccole costano meno da rifare che da provare prima). Stesso sito,
     stesso volo continuo: solo 4 momenti invece di 6.
   - **Standard (~11-13 generazioni)** — 5 scene; architettura A (10) o B (5 + 9 = 14).
   - **Vetrina (~17+ generazioni)** — 6-7 scene, mondo completo in B, passaggio previz, fasce mobile.
   **Meno scene ≠ sito più povero.** 3-4 momenti scelti bene si leggono come un mondo
   completo: dai a ogni scena più scroll (`scroll: 1.6-2`) e `linger`, e lascia che i testi
   portino di più a ogni momento. Un mondo compatto di 4 scene batte uno di 6 a corto di budget.
   Altre due leve se l'utente vuole l'estetica B con un budget leggero: i connettori sono
   **facoltativi uno per uno** (uno slot `null` fa una dissolvenza diretta su quella giuntura:
   il compromesso onesto è che quella transizione è una dissolvenza, non un volo; spendi i
   connettori sulle giunture intorno alle scene principali) e `seedance_2_0_mini` PUÒ essere
   il modello finale se l'utente accetta il 720p: aggancia i frame, quindi il sito resta senza giunture.
5. **Il viaggio (sezioni)** — le scene in ordine attraversate dalla camera, **dimensionate
   sulla fascia di budget**. Proponi un insieme ricavato dalla catena del valore
   dell'argomento e lascia che l'utente lo modifichi. Esempio boba (vetrina da 6 scene):
   piantagioni → cucina delle perle → negozio principale → consegna → piazza della comunità
   → il prodotto di punta; versione leggera da 4: piantagioni → cucina → negozio → prodotto
   di punta. Ogni sezione ha bisogno di: una breve descrizione del soggetto (cosa c'È nel
   diorama), un occhiello, un titolo, una riga di testo e 0-3 etichette. L'ultima sezione di
   solito è il prodotto di punta + la CTA.
6. **Fascia mobile — chiedila SEMPRE; mai generare materiale in più senza dirlo.** Su
   telefono l'animazione di scroll completa c'è in ogni fascia: le protezioni del motore
   (seek raggruppati, preparazione per iOS + ripiego sulle immagini con Risparmio energetico,
   CSS per le safe area, riduzione con il risparmio dati) sono sempre attive; le fasce
   decidono solo quale MATERIALE esiste. Fai la domanda a scelta, opzioni in quest'ordine,
   con il costo in crediti indicato:
   - **Ritaglio sicuro (predefinito, nessun costo in più)** — i telefoni fanno lo scrub delle
     clip desktop, ritagliate al centro in verticale. Ogni prompt compone già i soggetti
     principali al sicuro nel centro (prompts.md), quindi per quasi tutti i mondi va bene.
   - **Codifiche mobile (consigliato, niente crediti in più: solo tempo di codifica)** —
     varianti `-m.mp4` (720p, `-g 4`, passo 6) + collegamento di `clipMobile`/`connectorsMobile`/`posterMobile`
     (passo 7) + QA mobile (passo 8). I dispositivi di classe telefono (NON i tablet: il
     motore divide per schermo, l'iPad riceve il master) fanno lo scrub dei file più leggeri.
   - **Hero reinquadrato (piccolo costo in crediti: dillo)** — codifiche mobile + rigenerazioni
     in 9:16 delle 1-2 scene in cui il soggetto non regge un ritaglio al centro (di solito
     hero e finale). Collegale scena per scena come clip/poster mobile.
   - **Catena verticale completa (fascia oro, ≈2× i crediti video: dillo)** — una catena 9:16
     parallela: immagini verticali, passaggi di frame propri, connettori propri, controllo SSIM
     proprio (i formati non si mescolano a metà catena: una clip 9:16 non continua un frame 16:9).
     È quello che fa Apple: il materiale mobile è una resa inquadrata in modo diverso, non un
     ritaglio. Proponila solo quando l'utente fa capire che il traffico mobile conta o il budget
     è largo.

Il modello video **non** è una domanda dell'intervista: usa `seedance_2_0` senza chiedere. Se
l'utente indica una preferenza, rispettala **solo se il modello può agganciare i frame delle
giunture** (elenco del passo 4: `seedance_2_0`, `kling3_0`, `seedance_2_0_mini`). Questa skill
produce solo risultati senza giunture, quindi un modello che non aggancia i frame si rifiuta
con una riga di spiegazione, non si sostituisce: usa un modello dell'elenco.

**Chiudi l'intervista con una stima della spesa e ottieni il via libera esplicito prima di
qualsiasi generazione.** Indica il conto in numeri semplici dalla fascia scelta: `N`
generazioni di immagini + generazioni video (`N` per l'architettura A, `2N-1` per la B; nelle
corse vetrina la previz aggiunge una catena al livello mini) + un budget di rifacimenti (~20-30%
in più sugli interni, per colpa del filtro NSFW), più gli eventuali extra della fascia mobile,
e più o meno quanto dura (3-8 minuti per generazione; l'architettura A va in sequenza).
L'utente approva la spesa una volta, qui: dopo gli unici altri controlli sono l'approvazione
dell'immagine anchor (passo 2) e la revisione della previz (passo 4), che servono entrambe a
non sprecare la spesa grossa, non a richiedere il permesso.

La meccanica dello scroll resta fissa (volo continuo): è lo scopo della skill. La checklist
dell'intervista e la struttura dei testi sono in `references/prompts.md`.

---

## Passo 2 — Genera le immagini delle scene

Un'immagine per sezione, **tutte con lo stesso preambolo di stile** per la coerenza. Modello
predefinito **`gpt_image_2`** (nitido, ottimo nell'illustrazione isometrica; restituisce uno
sfondo pieno/bianco, perfetto per le "isole" di diorama sospese). Usa `nano_banana_2` solo se
il brief è pieno di personaggi o cartoni (nota: `nano_banana_2` è un alias della CLI che punta
a `nano_banana_pro`; con quel nome non compare in `higgsfield model list`).

Forma del prompt (i modelli completi sono in `references/prompts.md`):

```text
<STYLE PREAMBLE, identical every time>. On a plain solid <bg> background with a soft
contact shadow. <PALETTE hexes>. No text, no letters, no logos, centered, 3:2.
Subject: <what is in THIS diorama>.
```

- **Prima l'anchor: mai un lotto di N a freddo.** Genera UNA immagine anchor (la scena più
  rappresentativa), mostrala all'utente e rifinisci il preambolo di stile finché non la
  approva. Solo allora lancia le altre N-1 **passando l'anchor approvata come `--image`** per
  bloccare lo stile. Uno stile sbagliato sull'anchor costa 1 generazione; dopo un lotto a
  freddo ne costa N. È un blocco rigido: non andare oltre un'anchor non approvata.
- Lancia le altre in parallelo, staccate. Comando per scena:
  `higgsfield generate create gpt_image_2 --prompt "$(cat scene_i.txt)" --image anchor.png --aspect_ratio 3:2 --resolution 2k --quality high --wait --wait-timeout 15m --json > scene_i.json 2>scene_i.err`
- L'URL del risultato è `.[]0.result_url` nell'output di `--wait --json`. Scaricalo con `curl`.
- Una generazione può fallire per un problema passeggero (HTTP 503): rifai solo quella, non
  ripartire con tutto il lotto.
- **Rivedi il lotto prima di continuare.** Deve leggersi come un unico mondo coerente (stessa
  angolazione, palette, luce). Rifai una per una le scene fuori stile: il blocco di stile
  dell'anchor resta attivo.

Lo script esatto del lotto è in `references/pipeline.md` (idempotente: se lo rilanci salta il
materiale già finito, quindi un crash o un rifacimento non fa mai ripagare il lavoro fatto).

---

## Passo 3 — (Facoltativo) Scene sospese

Se vuoi che i diorami galleggino sopra uno sfondo d'atmosfera invece di stare in un riquadro
pieno, rendi trasparente lo sfondo piatto con `references/knockout.py` (riempimento a
partire dai bordi: conserva i colori interni uguali allo sfondo, es. le pareti crema). Poi
codifica in webp. Se preferisci restare sul semplice, dai alla pagina lo stesso colore dello
sfondo delle scene e salta questo passo.

Tieni comunque le immagini: sono **la grafica per il movimento ridotto e il ripiego senza clip**. (I poster di caricamento NON sono le immagini: si estraggono dalle clip codificate al passo 6, così il passaggio da immagine a video non fa scatti.)

---

## Passo 4 — Architettura della camera (scegline una: decide la sensazione)

Come si muove la camera *tra* una scena e l'altra è la leva di qualità più grande. Due forme;
scegli in base all'estetica.

### Modello video: UNO per tutta la catena

Si possono usare solo i modelli che agganciano i frame di una giuntura: ogni clip della catena
richiede `--start-image`, i connettori anche `--end-image`. Elenco predefinito: `seedance_2_0`
(predefinito), `kling3_0` (720p nativo, `--sound off`, il ripiego per l'NSFW), `seedance_2_0_mini`
(livello previz). Fai prima la previz di tutta la catena con `seedance_2_0_mini`, a meno che la
corsa non abbia ≤4 scene, e usa **un solo modello per tutte le clip della catena**. Flag,
confronto completo e regole sono in `references/video-models.md`: leggilo prima della prima generazione.

### A) Ripresa continua in avanti — CONSIGLIATA per mondi concreti / realistici / visite

Una camera che scivola solo **in avanti**, dalla prima scena all'ultima, come un'unica ripresa.
Genera i tratti **in sequenza**: il tratto 0 dall'immagine della scena 0 (scivola in avanti
dentro di essa); poi lo `--start-image` di ogni tratto = **l'ultimo frame REALE del tratto
precedente** (estratto con ffmpeg), prompt *"continue gliding smoothly FORWARD into [scene i],
never pulling back"* (oppure un movimento espressivo a metà tratto secondo il contratto di
passaggio del movimento: vedi **Grammatica della camera** qui sotto), e **niente `--end-image`**:
un end-image di un campo lungo costringe la camera a tirarsi indietro, la prima causa di scatti.
Estrai l'ultimo frame di ogni tratto per alimentare il successivo. Risultato: ogni giuntura è
identica frame per frame **e** la camera non torna mai indietro. **Niente connettori** (salta il
passo 5): i tratti SONO il viaggio. Collega ogni tratto come clip di sezione con `connectors: []`
e un piccolo `crossfade` (~0.08). Anche senza `--end-image` i tratti arrivano in stanze distinte
(il prompt guida il contenuto). Costo: rigorosamente **in sequenza** (non si parallelizza) e più
lento; gli interni fanno scattare il filtro NSFW, quindi prevedi rifacimenti (3 tentativi per tratto).

### B) Tuffo + connettore aereo — solo per mondi a diorama / in miniatura / visti dall'alto

Una clip "tuffo dentro ogni scena" + un connettore che sale **su e fuori** e vola fino alla
scena successiva (passo 5). L'uscita **inverte la direzione della camera a ogni giuntura**
(tuffo in avanti → uscita all'indietro). In un mondo in miniatura si legge come un voluto
"allarga sulla mappa, vola alla prossima isola"; in una visita concreta in prima persona si legge
come un fastidioso **riavvolgimento/scatto**. Usa B solo per l'estetica da mappa. Nel dubbio, A.

### Grammatica della camera — il movimento deve adattarsi al concept (A NON è "solo in avanti")

"Solo in avanti" è la regola delle *giunture*, non dei *tratti*: dentro un tratto la camera è
libera (orbita, gru, carrellata laterale), ma non deve mai invertire **attraverso** una giuntura.
Ogni tratto finisce assestandosi in una lenta deriva in avanti (l'ultimo ~1 s) e il tratto
successivo comincia continuandola: tieni identiche entrambe le frasi nei prompt. La tabella
concept → movimento, i costi dei rifacimenti e le manopole del ritmo (`scroll`, `linger`) sono
in `references/camera-grammar.md`.

**Per B**, un volo di camera per scena: parte in alto/fuori, scende nell'interno, la struttura
si apre. Modello: quello della catena scelto sopra (predefinito **`seedance_2_0`**),
`--start-image = l'immagine della scena`.

- Usa come immagine iniziale **l'immagine con lo sfondo pieno** (non quella trasparente), così
  il video ha un frame completo.
- Prompt: "Single continuous cinematic camera move, no cuts. Begin high and far looking at the
  whole [scene] from outside … descend and fly inside toward [focal point] … the roof/walls
  gently open to reveal the interior. [style], smooth graceful slow motion. No text." (Modello
  in `references/prompts.md`.)
- Parametri (seedance): `--mode std --resolution 1080p --aspect_ratio 16:9 --duration 8`.
  Per Kling: togli `--resolution` (il parametro non esiste), aggiungi `--sound off`, `--duration 10`.
  **Non** passare `--generate-audio` (su seedance dà errore; l'audio è comunque sprecato: lo toglierai).
- Lanciale in parallelo, staccate, poi scarica ogni `.result_url`. Rifai una per una quelle che
  falliscono. Tieni le sorgenti grezze a 1080p: ti servono i loro frame dopo.

---

## Passo 5 — Connettori (solo architettura B)

Salta tutto questo passo con l'architettura **A**: la ripresa in avanti non ha connettori; i
suoi tratti sono già concatenati senza giunture. Questo passo vale per **B** (diorama/miniatura),
con l'avvertenza sull'inversione del passo 4.

Le clip connettore sono quello che fa sembrare il mondo *collegato* invece che tagliato. Un
connettore vola dalla fine della scena i, esce ed entra nell'inizio della scena i+1. **Entrambi
i suoi estremi devono essere i FRAME REALMENTE RENDERIZZATI delle clip vicine, mai l'immagine
originale del diorama.**

Perché: ogni generazione di Higgsfield rende in modo leggermente diverso. Se un connettore
*finisce* su una nuova resa del "diorama della cucina", ma la clip di tuffo successiva *inizia*
con una sua resa diversa dello stesso diorama, le due non coincidono e alla giuntura c'è uno
scatto. La soluzione è passarsi i pixel esatti:

```text
For each connector between dive_i and dive_{i+1}:
  start-image = the LAST frame extracted from dive_i's rendered video
  end-image   = the FIRST frame extracted from dive_{i+1}'s rendered video
```

Ora ogni giuntura è identica frame per frame da *entrambi* i lati:
`dive_i.end == connector.start` e `connector.end == dive_{i+1}.start`.

Estrai i frame di confine dai tuffi renderizzati (non dalle immagini):

```bash
ffmpeg -sseof -0.15 -i dive_i.mp4   -frames:v 1 -q:v 2 dive_i_last.png    # interno di i
ffmpeg -ss 0      -i dive_{i+1}.mp4 -frames:v 1 -q:v 2 dive_next_first.png # campo lungo di i+1
```

Genera il connettore (`--duration 5` basta e avanza). I connettori richiedono `--end-image`,
quindi il modello deve accettarlo: tutti i modelli dell'elenco lo fanno (`seedance_2_0`,
`seedance_2_0_mini`, `kling3_0`):

```bash
higgsfield generate create "$VMODEL" \
  --prompt "$(cat connector_i.txt)" \
  --start-image dive_i_last.png --end-image dive_next_first.png \
  $VOPTS --aspect_ratio 16:9 --duration 5 --wait --json
# seedance: VOPTS="--mode std --resolution 1080p"; kling3_0: VOPTS="--mode std --sound off"
```

Prompt del connettore: "Single continuous camera move, no cuts. Pull up and back out of [scene i], rise into the sky, glide across the connected miniature world, and arrive above [scene i+1], beginning to descend toward it. Seamless flowing aerial transition. [style]. No text." (Modello in `references/prompts.md`.)

Assicurazione: Seedance arriva *vicino* all'end-image ma non sempre al pixel, quindi il motore
applica comunque una **breve dissolvenza** (pochi frame) a ogni giuntura. Estremi agganciati ai
frame + una piccola dissolvenza = nessun taglio visibile. Mai saltare il passaggio dei frame
reali contando solo sulla dissolvenza: un grosso salto di contenuto non si nasconde con una dissolvenza.

Se un passaggio ha davvero tenuto si **controlla in automatico**: non aspettare la QA nel
browser per scoprirlo. Dopo la codifica esegui il controllo SSIM delle giunture
(`references/pipeline.md` §5c): un vero passaggio di frame reali fa ≥0.95 attraverso il
confine; <0.75 vuol dire che un estremo era un'immagine o il frame sbagliato. Rieseguilo dopo
ogni rifacimento: sostituire una clip tocca, senza dirlo, ENTRAMBE le sue giunture.

---

## Passo 6 — Codifica per uno scrub fluido

Scrub = impostare `video.currentTime` dallo scroll. Contano due cose, e spesso si sbagliano:

1. **Quello che fa funzionare lo scrub è la possibilità di fare seek, non la densità dei
   keyframe.** Molti hosting statici (e `python -m http.server`) non servono le richieste HTTP
   a intervalli di byte, il che blocca `video.seekable` a `[0,0]` e riporta *ogni* seek al frame
   0: il video sembra congelato. La soluzione robusta è **scaricare ogni clip come `Blob` e
   riprodurla da un object URL in memoria** (sui blob il seek funziona sempre). Il motore fa
   così. Per questo **non** serve un video tutto intra.
2. **Non abbassare la qualità per avere seek fluidi.** Codifica alla **risoluzione nativa**
   (1080p da Seedance: non ridurla), `crf ~20`, un **GOP piccolo** (`-g 8`) invece del tutto
   intra (il tutto intra gonfia una clip di 8 s a ~25 MB; GOP 8 fa ~8 MB e con il blob scorre
   bene). Togli l'audio, aggiungi faststart, e un leggero `unsharp` compensa la morbidezza del
   video:

```bash
ffmpeg -i src.mp4 -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart out.mp4
```

Codifica tutte le 2N-1 clip (tuffi + connettori) con le stesse impostazioni, per una qualità uniforme.

**Estrai i poster dalle clip CODIFICATE** (`references/pipeline.md` §5b). L'immagine è in 3:2;
la clip è una *nuova resa* in 16:9: se il poster di caricamento è l'immagine, il primo disegno
del video fa un salto visibile (ritaglio + differenze di resa) proprio sulla prima scena che il
visitatore vede. Stessa dottrina dei connettori, applicata alla giuntura zero: il poster deve
essere il primo frame estratto dalla clip stessa. Collegalo come `sections[k].poster` (passo 7);
tieni l'immagine come grafica per il movimento ridotto.

Poi esegui il **controllo automatico delle giunture** (`references/pipeline.md` §5c) prima di
aprire un browser: ogni giuntura con SSIM ≥0.90, altrimenti hai un rifacimento, non una nota di QA.

**Codifiche mobile (solo se l'utente ha scelto una fascia oltre il ritaglio sicuro al passo 1.6).**
I decoder video dei telefoni fanno i seek molto più lentamente di un portatile, e il costo del seek
cresce con la lunghezza del GOP, quindi il master 1080p `-g 8` che scorre fluido su desktop può
scattare su un telefono. Produci una variante `-m.mp4` più leggera per ogni clip — **720p, `-g 4`**
(più keyframe = seek meno costosi; un keyframe ogni 4-10 frame è la ricetta del settore per uno
scrub fluido su mobile), crf 23 — e collegale come `clipMobile` / `connectorsMobile` (passo 7).
Estrai il primo frame di ogni codifica mobile come suo `posterMobile` (stessa dottrina del §5b: il
poster deve corrispondere alla codifica che il dispositivo riceve davvero). Il motore serve i file
mobile solo ai dispositivi di classe telefono (lato corto dello schermo ≤600 px CSS: tablet e iPad
ricevono il master) e se mancano usa la clip desktop. Script in `references/pipeline.md` §6; per le
fasce hero reinquadrato / catena verticale vedi §7. Se l'utente ha scelto il ritaglio sicuro, salta
questa parte: il motore protegge comunque lo scrub sui telefoni (seek raggruppati, preparazione per
iOS, ripiego sulle immagini con Risparmio energetico), quindi la pagina si degrada con garbo invece di rompersi.

---

## Passo 7 — Monta la pagina

Copia `references/scrub-engine.js` (e, se vuoi una pagina del tutto autonoma, il piccolo
`references/index-template.html`) nel progetto dell'utente, oppure adattalo al suo framework.
È guidato dalla configurazione e autosufficiente:

```js
mountScrollWorld(document.getElementById('world'), {
  brand: { name: 'Pearl & Co.' },
  diveScroll: 1.3, connScroll: 0.9,          // altezze di viewport di scroll per clip
  sections: [
    { id:'farm', label:'Le piantagioni', still:'assets/farm.webp',
      poster:'assets/farm-poster.webp',          // primo frame estratto dalla clip codificata (passo 6)
      clip:'assets/vid/farm.mp4', clipMobile:'assets/vid/farm-m.mp4',   // solo con le codifiche mobile
      scroll: 1.6, linger: 0.45,   // ritmo facoltativo: sosta più lunga + camera che si assesta a metà scena
      accent:'#8FB98A', eyebrow:'Dalla foglia all\'ultimo sorso', title:'Tutto comincia in collina.',
      body:'…', tags:['Monorigine','Raccolto a mano'] },
    // …una per sezione; l'ultima può avere una `cta`
  ],
  connectors:       ['assets/vid/conn1.mp4','assets/vid/conn2.mp4',   /* … lunghezza = sezioni-1 */],
  connectorsMobile: ['assets/vid/conn1-m.mp4','assets/vid/conn2-m.mp4' /* … stessa lunghezza; solo con le codifiche mobile */],
});
```

Il motore gestisce: la catena ordinata di tuffi e connettori, scroll→currentTime con smussatura
via rAF, caricamento come blob, precaricamento pigro delle clip vicine, dissolvenze agganciate ai
frame, testi fissati per sezione (la prima sezione accoglie all'arrivo, l'ultima tiene la sua CTA),
una barra del percorso, `prefers-reduced-motion` e mobile. **Ritmo per sezione:** `scroll` sostituisce
`diveScroll` per quella scena (più scroll = sosta più lunga) e `linger` (0-1, tienilo ≤ 0.6)
rimappa il tempo in modo che la camera si assesti a metà scena, proprio mentre i testi sono al
massimo, e poi acceleri verso la giuntura; i frame delle giunture non cambiano (f(0)=0, f(1)=1).
Dai alle scene hero e finale uno `scroll` più alto + un po' di `linger`; tieni svelte le scene di
passaggio. Il tema si fa con le variabili CSS (`--accent`, `--sw-bg`, `--sw-ink`, …): l'identità
visiva viene dalle clip generate, quindi l'interfaccia resta discreta. Configurazione completa e
variabili CSS sono nell'intestazione di `scrub-engine.js`.

**Sui telefoni il motore si adatta da solo, lungo due assi distinti.** *Il livello delle clip*
(quale file) lo decide la classe del dispositivo: lato corto dello schermo ≤600 px CSS = telefono →
`clipMobile`/`posterMobile`; tablet (iPad Pro compreso: puntatore grossolano ma schermo e decoder da
desktop) e desktop ricevono il master. *Le protezioni* (come si comporta) dipendono da puntatore
grossolano / viewport ≤860 px: **seek raggruppati** (non accoda mai un nuovo `currentTime` a metà di
un seek: è quello che evita che uno scorrimento veloce congeli la clip), poster tenuto finché la clip
non disegna, **preparazione del video al primo tocco** (correzione per iOS, che non mostra niente finché
non riproduce), uno scroll più lungo per scena (`scrollMobileFactor`, predefinito 1.2: nei viewport
piccoli lo stesso volo sembra più veloce), niente particelle, resize che non risentono della barra
degli indirizzi, margini delle safe area. **Ripiego automatico sulle immagini:** `prefers-reduced-motion`,
il risparmio dati di Chromium e il **Risparmio energetico** di iOS (rilevato a runtime: un `play()`
muto rifiutato al primo tocco) portano la pagina a immagini con dissolvenze invece di un video
congelato. Su 2g/3g (segnale di Chromium) la finestra di precaricamento delle clip si restringe. Tutto
questo è attivo di default, senza configurazione. Le codifiche `clipMobile`/`connectorsMobile`/`posterMobile`
sono le fasce facoltative del passo 1.6: collegale solo se l'utente ne ha scelta una.

**I testi per la SEO non sono facoltativi: è una landing page.** Il motore disegna tutti i testi
lato client, quindi da sola la pagina non ha testo indicizzabile. Metti sempre dentro il contenitore
una copia dei testi in markup semplice (h1 = frase dell'hero, un h2 + p per scena, link veri per la
CTA) in un blocco `data-sw-seo`: il motore lo nasconde al montaggio, crawler, anteprime dei link e
visitatori senza JS lo leggono dall'HTML servito. `references/index-template.html` contiene già il
blocco; quando adatti a un framework, fallo renderizzare dal server.

Per backend senza JS (Python/Rails/ecc.): servi gli asset e metti lo `<script>` del motore
nell'HTML renderizzato; niente è specifico di un framework.

---

## Passo 8 — QA delle giunture (non saltarla)

**Prima il controllo automatico:** il controllo SSIM delle giunture (`references/pipeline.md` §5c)
deve essere già verde: ogni giuntura ≥0.90 (0.75-0.90 solo dove hai guardato la dissolvenza e l'hai
accettata). Se l'hai saltato, eseguilo adesso: la QA nel browser qui sotto verifica la *pagina*, il
controllo SSIM verifica il *materiale*, e un materiale rosso non diventa una pagina verde con la QA.

Poi guida la pagina in un browser headless e verifica, seguendo la checklist completa di
`references/qa-checklist.md`:

- i frame appena prima e appena dopo ogni giuntura sono quasi identici;
- il primo disegno è pulito (il poster si vede, nessuno spostamento quando il video subentra al
  poster), nessun errore in console, `video.seekable.end(0) > 0`;
- i ripieghi sulle immagini funzionano (risparmio dati, Risparmio energetico, il tablet riceve la clip desktop);
- la checklist mobile, solo se l'utente ha scelto una fascia mobile (passo 1.6);
- con il movimento ridotto si passa alle immagini.

---

## Trappole — le prime 3 qui; l'elenco completo in `references/gotchas.md`

Leggi `references/gotchas.md` appena una generazione fallisce o un controllo di QA dà un risultato
strano: collega sintomo → causa → correzione per ogni errore visto in produzione (codifica, tema,
telefono, iOS, flag di Kling, ritagli verticali, video congelato, crediti contesi e altro).
Le tre che bloccano più spesso:

- **Scatto alla giuntura** → gli estremi del connettore erano le immagini dei diorami, non i frame
  reali delle clip vicine. Estrai sempre i frame veri (passo 5); il controllo SSIM (pipeline §5c)
  lo trova prima ancora di aprire un browser.
- **Giuntura a scatti / camera che "salta indietro"** → la *velocità* della camera si inverte
  attraverso una giuntura (inevitabile con le uscite dell'architettura B). Le visite concrete devono
  usare l'architettura A (passo 4).
- **Falsi positivi NSFW (Seedance `status "nsfw"`)** → blocca interni innocui (camera da letto,
  piscina, spa; parole come "bed", "wine", "swim"). In ordine: rifai (spesso passa al 2°-3° tentativo)
  → togli le parole scatenanti + aggiungi "empty, unoccupied, no people, architectural" → rigenera
  quella clip con `kling3_0` con gli stessi frame iniziale e finale → metti lo slot del connettore a
  `null` (il motore fa una dissolvenza diretta su quella giuntura). Prevedi rifacimenti sugli interni.

## Riferimenti

- `references/prompts.md` — checklist dell'intervista, schema del preambolo di stile e ogni
  modello di prompt (immagine della scena, tuffo, connettore) con gli spazi da riempire.
- `references/pipeline.md` — script da copiare per tutta la corsa (immagini con anchor → previz →
  tuffi → frame → connettori → codifica → poster → controllo SSIM → codifica mobile),
  idempotenti e compatibili con bash 3.2.
- `references/scrub-engine.js` — il motore di scrub portabile e guidato dalla configurazione
  (costruisce il DOM e inietta il CSS; seek su blob, caricamento pigro, dissolvenza alle giunture,
  poster dai frame estratti, blocco di testo statico `data-sw-seo` nascosto, testi, barra del
  percorso, movimento ridotto e protezioni per i telefoni: codifiche mobile, seek raggruppati,
  preparazione per iOS, safe area, resize senza salti).
- `references/index-template.html` — una pagina autonoma minima che monta il motore, con il
  blocco di testo indicizzabile `data-sw-seo`.
- `references/knockout.py` — rimozione dello sfondo a partire dai bordi, per le scene sospese.
- `references/gotchas.md` — l'elenco completo sintomo → causa → correzione, più l'alternativa della
  sequenza di frame su canvas per quando lo scrub del video non è abbastanza fluido.
- `references/video-models.md` — l'elenco dei modelli che agganciano i frame, flag e regola della previz (passo 4).
- `references/camera-grammar.md` — regole di movimento tra giunture e tratti, tabella concept → movimento, ritmo (passo 4).
- `references/qa-checklist.md` — la checklist completa di QA nel browser, mobile compreso (passo 8).
