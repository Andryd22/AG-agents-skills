# Trappole (imparate a fatica)

Le tre che bloccano più spesso sono riassunte in SKILL.md; questo è l'elenco completo.
Sintomo → causa → correzione.

- **Scatto alla giuntura** → gli estremi del connettore erano le immagini dei diorami, non i
  frame reali delle clip vicine. Estrai sempre i frame veri (passo 5 di SKILL). Il controllo SSIM
  (pipeline.md §5c) lo trova prima ancora di aprire un browser.
- **Giuntura a scatti / camera che "salta indietro"** → anche con giunture agganciate ai frame, se
  la *velocità* della camera si inverte (tuffo in avanti, poi un connettore che si tira indietro)
  si legge come un riavvolgimento. È inevitabile nell'architettura B. Per qualsiasi visita concreta
  usa l'architettura A (un'unica ripresa continua in avanti: tratti concatenati dagli ultimi frame
  reali, niente arretramenti, niente `--end-image`); vedi il passo 4 di SKILL.
- **Scatto da immagine a video al primo disegno** → il poster è l'immagine sorgente in 3:2, non il
  primo frame estratto dalla clip codificata. Collega `sections[k].poster` (pipeline.md §5b).
- **Video congelato / fermo al frame 0** → `seekable=[0,0]`; l'hosting non serve gli intervalli di
  byte. Usa gli URL dei blob (il motore lo fa).
- **File enormi** → hai usato il tutto intra. Usa `-g 8` + blob.
- **Morbido / bassa qualità** → hai ridotto la risoluzione o compresso troppo. Codifica a 1080p
  nativo, crf ≤ 20, aggiungi `unsharp`. Il video è per natura più morbido delle immagini: tieni le
  immagini come ripiego leggero con la massima fedeltà.
- **Generazioni parallele con 503 / "not_enough_credits" a raffica** → succede quando ne partono
  molte insieme; rifai quella fallita, i crediti non sono davvero finiti (verifica con
  `higgsfield workspace list`).
- **Falsi positivi NSFW (Seedance `status "nsfw"`)** → il filtro dei contenuti video blocca clip del
  tutto innocue, soprattutto in contesti **camera da letto, piscina, spa/benessere** e con parole
  come "bed", "pool", "waterfall", "wine", "swim". Dipende in parte dalle parole del prompt e in
  parte dai frame di riferimento. Correzioni, in ordine: (1) rifai: spesso non è deterministico e
  passa al 2°-3° tentativo; (2) togli le parole scatenanti e aggiungi "empty, unoccupied, no people,
  no figures, architectural, tasteful"; (3) rigenera solo quella clip con **`kling3_0`** con gli
  stessi frame iniziale e finale: il filtro di un altro fornitore spesso lascia passare quello che
  Seedance blocca. Aspettati un leggero cambio di carattere su quella clip (ogni modello ha la sua
  grana e il suo movimento); per un connettore di 5 s dietro una dissolvenza di solito è meglio
  dell'opzione (4): mettere lo slot del connettore a `null`, così il motore fa una dissolvenza diretta
  su quella giuntura (connettori facoltativi) e la pagina resta completa. Prevedi crediti e tempo in
  più per questi rifacimenti con interni e contenuti immobiliari.
- **Tema scuro / personalizzato** → il motore racchiude i suoi valori predefiniti in `@layer sw`,
  quindi un blocco `:root` / `.sw-root { --sw-bg; --sw-ink; --sw-accent; --sw-font-* }` della pagina
  vince senza problemi (nessun trucco di specificità). `--sw-ink` è il colore principale di **testi e
  titoli**; l'**accent** riempie il pulsante principale e la navigazione attiva. Per un tema scuro
  imposta `--sw-bg` scuro e `--sw-ink` chiaro: il velo dietro i testi e l'ombra del titolo seguono
  `--sw-bg` da soli.
- **Sul telefono lo scrub scatta / si congela con uno scorrimento veloce** → il master a 1080p è
  troppo pesante per il decoder del telefono e i seek si accumulano. Distribuisci le codifiche mobile
  `-m.mp4` (720p, `-g 4`) e collega `clipMobile`/`connectorsMobile` (passi 6/7 di SKILL). Il motore
  raggruppa già i seek; la codifica più leggera è l'altra metà. Ancora a scatti su un dispositivo
  economico? Stringi il GOP (`-g 2` / tutto intra).
- **Scena vuota / nera su iOS (su desktop andava)** → una stranezza di Safari su iOS: un video muto
  mai riprodotto non disegna un frame dopo un seek. Il motore la corregge tenendo il poster finché la
  clip non disegna e preparando ogni video al primo tocco: quindi **non** nascondere il poster su
  `loadedmetadata` e non togliere gli attributi `playsinline`/`muted` se adatti il motore a un framework.
- **Video congelato su iOS con il risparmio batteria** → il **Risparmio energetico** di iOS rifiuta
  perfino un `play()` muto e playsinline, e anche lo scrub con `currentTime` non funziona: nessuna
  tecnica video sopravvive. Il motore rileva la preparazione rifiutata al primo tocco e passa tutta la
  pagina a immagini con dissolvenze. Se adatti il motore, tieni questo ripiego: un `.catch()` sul
  `play()` di preparazione che entra in modalità immagini.
- **L'iPad riceve un video sfocato a 720p** → il livello delle clip dipendeva dal tipo di puntatore.
  iPadOS dichiara un puntatore grossolano E uno user agent da Mac desktop: due segnali inutili. Il
  motore divide per lato corto dello schermo (≤600 px CSS = telefono); se lo porti altrove, tieni
  questa regola (o decidi con `clientWidth × devicePixelRatio`), mai con puntatore o user agent.
- **Chi ha il risparmio dati o il 2g scarica tutto il carico dei blob** → Chromium espone
  `navigator.connection.saveData` / `effectiveType`; iOS non espone niente. La risposta del motore:
  impostazione prudente per tutti (prima i poster, download pigro dei blob vicino al viewport),
  modalità immagini con `saveData`, finestra di precaricamento ristretta su 2g/3g. Non invertirla
  (impostazione pesante + riduzione quando c'è un segnale): i dispositivi più spesso su rete mobile
  sono gli iPhone, che non mandano segnali.
- **La pagina salta mentre si scorre su mobile** → qualcosa rifà il layout al `resize` che compare e
  sparisce con la barra degli indirizzi. Il motore ignora i resize solo in altezza sui dispositivi
  touch; se l'hai portato altrove, fai scattare l'handler di resize solo quando cambia la larghezza
  (tieni il percorso `orientationchange` per la rotazione).
- **Testi nascosti dietro la barra degli indirizzi / il notch su mobile** → usa lo spostamento in
  basso del motore che tiene conto delle safe area (`env(safe-area-inset-bottom)` + `dvh`); verifica
  che il `<meta viewport>` della pagina includa `viewport-fit=cover` (il modello lo fa).
- **In verticale la scena viene ritagliata** → una clip 16:9 su un telefono alto mostra solo il
  centro. Tieni il soggetto principale di ogni scena al centro con un po' di spazio sopra (prompts.md),
  oppure genera un hero 9:16 per le scene che contano di più. Il motore ritaglia al centro
  (`object-fit:cover`); non può scontornare una composizione panoramica.
- **`--generate-audio` dà errore su seedance** → toglilo; togli l'audio nell'HTML e con `-an` in codifica.
- **Kling rifiuta i tuoi flag** → `kling3_0` **non ha il parametro `--resolution`** (non passarlo;
  codifica alla risoluzione nativa che riporta ffprobe) e **il suono è attivo di default**: passa
  `--sound off`. La durata predefinita è 5; tratti e tuffi vogliono 10.
- **Scatti solo dove hai "risparmiato crediti"** → hai cambiato modello a metà catena, o hai usato un
  modello con sola immagine iniziale dove un connettore richiede `--end-image`. Un solo modello per
  tutta la catena; l'unico livello economico è `seedance_2_0_mini`, che continua ad agganciare i frame
  e quindi resta senza giunture. (Un modello con input solo di riferimento non tiene proprio una
  giuntura: passo 4 di SKILL.)
- **Scene in un riquadro bianco** → `gpt_image_2` restituisce uno sfondo pieno; o fai coincidere lo
  sfondo della pagina, o lo togli (passo 3 di SKILL).
- **bash 3.2** su macOS → niente array associativi negli script.

## Oltre lo scrub del video: l'alternativa della sequenza di frame

Lo scrub di `video.currentTime` è la via di mezzo pragmatica. La tecnica che Apple usa davvero nelle
sue pagine a scroll è una **sequenza di immagini estratte prima e disegnate su un `<canvas>`** (e, nei
browser moderni, WebCodecs che decodifica i frame in anticipo nel canvas): il disegno dei frame è
deterministico — niente latenza di seek del decoder, niente download come blob di clip intere, i frame
arrivano un po' alla volta. Compromessi: più strumenti di costruzione (estrarre N frame per clip,
impacchettarli in webp/avif), più richieste e byte totali simili o maggiori con clip di questa
lunghezza. Se un cliente pretende fluidità anche sui dispositivi economici o il carico dei blob
(~8 MB × 2N-1 clip) è inaccettabile, porta la mappatura dello scrub del motore su un renderer a
sequenza di frame su canvas: dottrina delle giunture, calcoli della catena e manopole del ritmo
restano identici; cambia solo la primitiva "disegna il frame al tempo t".
