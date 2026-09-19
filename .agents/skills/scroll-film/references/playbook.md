# Il playbook dello scroll film (percorso B — riprese cinematiche)

Regole imparate a fatica per fare di tutta la pagina un unico film continuo di Higgsfield.
Sono un pavimento, non un soffitto: violale sapendo quello che fai, mai per sbaglio.

## 1. Legge: prima le riprese

Il film è la fonte di verità; il sito è un lettore. Progetta prima l'arco della camera (un
unico viaggio continuo, ~5 capitoli), poi costruisci la pagina intorno alle riprese che
arrivano davvero. Mai fare lo storyboard del sito e forzare le riprese ad adattarsi: le
riprese derivano, i testi si spostano facilmente.

## 2. Legge della concatenazione (giunture perfette)

Lo `--start-image` di ogni clip è **l'ultimo frame letterale estratto con ffmpeg** dalla
clip precedente: non un fotogramma che gli somiglia, i pixel veri:

```bash
ffmpeg -sseof -0.05 -i clipN.mp4 -update 1 -q:v 1 clipN-last.png
higgsfield generate create seedance_2_0 --prompt "..." \
  --start-image clipN-last.png --duration 5 --resolution 1080p \
  --mode std --generate-audio false
```

Solo il fotogramma iniziale (Nano Banana Pro) apre la catena; ogni start-image successivo è
un vero ultimo frame. Mantieni un'unica direzione di camera (sempre in discesa / sempre in
avanti): le inversioni si leggono come tagli. Clip della stessa durata = scrub a velocità
costante.

## 3. Il controllo delle giunture (misurato, mai a occhio)

```bash
ffmpeg -i A-last.png -i B-first.png -lavfi ssim -f null - 2>&1 | grep All
```

- **≥ 0.88 superato** · 0.80-0.88 guardalo in movimento · un vero fallimento è **strutturale**.
- L'SSIM sottostima le texture casuali (nuvole ~0.66, braci ~0.72, caustiche dei liquidi
  ~0.60 possono essere tutte senza giuntura visibile). Il numero dice *dove* guardare; decide
  il confronto affiancato.
- Il fallimento vero più comune è la **deriva di colore o di geometria** (un'alba inventata,
  un nuovo orizzonte). Si corregge rigenerando con: *"Continue the exact same shot from the
  reference frame, identical framing, identical colour grade. Do not change the colour
  grade."* (i prompt per il modello video restano in inglese).
- **Vietate le dissolvenze/incroci sopra una giuntura venuta male**: con lo scrub l'utente
  può fermarsi sulla giuntura, e la maschera si vede subito. Correggi la giuntura, non
  nasconderla.

## 4. La verità sui costi (verificala con la differenza di saldo, non con la documentazione)

- `--generate-audio false` è *la* leva dei costi: l'audio acceso triplica il conto senza avvisare.
- Prezzi misurati per clip da 5 s (conferma con `higgsfield generate cost`):
  1080p/std ≈ 45 · 720p/std ≈ 22,5 · 720p/fast ≈ 17,5 · 480p/fast ≈ 7,5. 10 s = 2×5 s.
- **Fai la bozza di tutta la catena a 480p/fast per convalidarla, poi rigenera i prompt
  approvati a 1080p.** Rigenerare al livello di bozza costa una frazione di una generazione
  completa.
- Circa il 15% dei job fallisce lato server senza motivo e non viene addebitato: ripeti la
  stessa chiamata.

## 5. Montaggio

- Concatena togliendo il frame duplicato alla giuntura (`select='gte(n,1)'` dalla clip 2 in
  poi) e **sempre `-fps_mode vfr`** nella codifica finale: la sincronizzazione CFR predefinita
  aggiunge ~5 frame duplicati per giuntura = zone di scrub congelate.
- Estrai un frame ogni 2 in ~300 JPEG a ~1280 px, `-q:v 4`. (Le riprese scure e granulose
  quasi raddoppiano i byte dei JPEG: 1280/q4 tiene leggero il carico senza perdite visibili
  con il riempimento a copertura.)
- Campiona il colore del bordo dell'ultimo frame → l'hex della giuntura per il passaggio
  film→contenuti.

`scripts/chain-step.sh` e `scripts/assemble.sh` fanno tutto questo.

## 6. Il motore di scrub (perché non ha jank)

- **Canvas + JPEG estratti prima**, mai lo scrub con `<video currentTime>` (scatti di seek).
- **Finestra scorrevole di ImageBitmap**: `drawImage(HTMLImageElement)` costringe a una
  decodifica JPEG *sincrona* al primo disegno (e dopo che la cache è stata svuotata): quel
  picco di decodifica *è* il jank frame per frame. `createImageBitmap` decodifica fuori dal
  thread principale; tieni una finestra di bitmap decodificate intorno alla testina (±18 in
  avanti, libera/chiudi oltre ±28), così ogni disegno è una pura copia sulla GPU.
- Interpola l'indice del frame (`current += (target-current)*0.14`) per la morbidezza.
  Limita il DPR a ~1.5.
- Scroll morbido con Lenis; una pompa di immagini con concorrenza limitata; ripiego
  `nearestFrame()`, così un frame mancante non svuota mai il canvas.
- **Misura il jank con i delta di rAF (p95/massimo), non con gli fps medi.** Obiettivo
  massimo < 50 ms.

## 7. Interfaccia, giuntura e livello di sfondo

- **Header adattivo**: campiona la luminanza della striscia in alto del frame disegnato
  (~ogni 180 ms) → attiva o disattiva una classe `.on-light`. Un'interfaccia fissa sopra un
  film che cambia non può avere un solo colore fisso.
- **Passaggio senza giuntura**: fai partire il gradiente di sfondo della sezione successiva
  dal colore *campionato* dell'ultimo frame. Nessuna linea visibile tra film e contenuti.
- **Livello hero di sfondo** (facoltativo, gratis): particelle su canvas a tema con il
  mondo (neve che brilla, polline d'oro) sopra il primo frame fermo, che svaniscono nel primo
  ~7% dello scroll: l'hero sembra vivo prima che parta lo scrub. Usa uno sprite fuori schermo
  con gradiente radiale + un `drawImage` per particella (mai `shadowBlur`); smetti del tutto
  di disegnare ad alpha 0.
- Grana e vignettatura vendono la sensazione di "unica inquadratura"; falle svanire entrambe
  al passaggio.

## 8. Strumento di verifica

Le anteprime dell'host rallentano le schede nascoste (rAF congelato → screenshot vecchi).
La strada affidabile: puppeteer-core + Chrome di sistema + un contratto di sviluppo nella
pagina:

- `?jump=<scrollY>` → apri la pagina già scrollata e assesta a forza tutto lo stato dello scroll.
- `window.__ready = true` solo dopo che i frame sono decodificati e assestati.
- Cattura: `goto → waitForFunction(__ready) → aspetta ~1200 ms → screenshot`. Fotografa ogni
  posizione dei momenti *e* ogni giuntura. Nascondi qualsiasi elemento che segue il cursore
  fino al primo vero mousemove, altrimenti compare nelle catture a 0,0.

`scripts/verify.js` fa cattura e test di jank.

## 9. Chi fa cosa

Gusto e codice del design li fa solo il modello principale (quello che esegue la skill). I
passaggi meccanici (ffmpeg, SSIM, puppeteer, vercel) sono codice puro, senza modello. Indica
i crediti prima di spendere; mostra il saldo dopo. Un'unica inquadratura continua, un mondo
per marchio.
