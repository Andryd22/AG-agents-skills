---
name: scroll-film
description: 'Costruisce un sito animato "scroll film" davvero bello: tutta la pagina è un''unica inquadratura cinematica continua che scorre mentre il visitatore fa scroll. Fa una breve intervista, propone 2-3 concept con un nome, cura la direzione artistica del mondo e poi lo costruisce da zero. Due percorsi: movimento solo in codice con GSAP/Lenis, gratuito (nessuna configurazione, funziona per chiunque), oppure un film di riprese cinematiche generate con il motore image-to-video dell''utente (Higgsfield Seedance è il riferimento; vanno bene Kie.ai, fal, Replicate o qualsiasi modello che accetta un''immagine iniziale). Si attiva su "scroll-film", "sito cinematico allo scroll", "sito scrollytelling", "fammi un sito animato / allo scroll", "sito film-scroll", "sito in un''unica inquadratura", o qualsiasi richiesta di un sito premium animato con lo scrub dello scroll. NON per presentazioni, spiegazioni in HTML o siti vetrina statici. Usala quando l''utente lancia /scroll-film.'
---

# Scroll-Film Studio

Costruisci **siti scroll film**: l'hero *è* la pagina, un'unica inquadratura cinematica
ininterrotta che avanza mentre il visitatore scorre e poi si scioglie senza giunture nei
contenuti sotto. Questa skill è un **processo, non uno scheletro**: non ci sono pagine
modello da copiare. Ogni sito si progetta e si scrive da zero per il suo marchio, seguendo
il processo qui sotto e le regole tecniche in `references/`.

Due modi per fare il film:

- **Percorso A — Solo codice (predefinito, nessuna configurazione):** il "film" è
  movimento GSAP + Lenis: scene fissate, parallasse, rivelazioni con clip-path, scorrimenti
  orizzontali. Non costa niente, non servono account, funziona per chiunque scarichi la skill.
- **Percorso B — Riprese cinematiche (su richiesta):** il film è video generato davvero,
  concatenato inquadratura dopo inquadratura e fatto scorrere su un canvas. Funziona con
  **qualsiasi motore image-to-video che accetta un'immagine iniziale**: Higgsfield Seedance
  2.0 è l'implementazione di riferimento (script inclusi); Kie.ai Seedance/Veo, fal,
  Replicate ecc. seguono lo stesso contratto di concatenazione. Servono un account
  dell'utente e i suoi crediti. È il look distintivo.

Tutti ottengono un risultato splendido. Il percorso A c'è sempre; il B si sblocca quando
l'utente ha un motore video.

---

## LA REGOLA D'ORO — il design lo fai tu, il modello principale

Ogni decisione che richiede **gusto** la prendi tu, il modello che esegue questa skill
(usa il più forte che l'IDE offre): concept, direzione artistica, palette, caratteri,
layout, motion design, testi, la costruzione stessa (tutto HTML/CSS/JS) e la revisione
finale del design. **Nessun altro modello tocca mai il design.** Se deleghi, delega solo:

- **Lavoro meccanico** → shell/codice puro, *senza nessun modello* (ffmpeg, punteggi
  SSIM, estrazione dei frame, verifica, deploy).
- **Bozze circoscritte** → sub-agent con lo *stesso modello* (es. la bozza del prompt video
  di un capitolo, una sezione dopo il film). Mai affidare design o codice a un modello
  diverso o più debole.

Non è negoziabile ed è così che la qualità resta alta e i token restano pochi.

---

## PASSO 0 — L'intervista

Fai queste domande subito (tutte insieme; se l'host ha un'interfaccia per domande
strutturate, usala). **Ogni domanda creativa ha l'opzione "decidi tu"**: se l'utente
lascia a te, fai tu la direzione artistica e vai avanti. Non bloccarti mai su una risposta
di design che sai dare bene da solo.

1. **Cosa costruiamo, e l'atmosfera in una riga?**
   Nome del marchio/prodotto, cos'è e la sensazione. (es. *"VOLTA — una scuderia da corsa
   elettrica. Aggressiva, elettrica, veloce."*)
2. **Materiale del marchio, o creo io il mondo?**
   Logo, colori, font e immagini reali esistenti, oppure piena libertà creativa.
3. **Il viaggio: l'unica inquadratura continua, dall'alto in basso.**
   Dove parte la camera e dove arriva: la *trasformazione*. (es. *"campo al chiaro di luna
   → dentro un solo fiore → una goccia d'oro → la bottiglia."*) Oppure: "disegna tu l'arco
   partendo dal mio marchio." **È il cuore di tutta la costruzione.**
4. **Video vero o solo movimento?** → sceglie il percorso B o A. Nel dubbio, o se non si
   vuole configurare niente, **percorso A (solo codice)**.
5. **(Solo percorso B) "Usi Higgsfield o qualcos'altro?"** Chiedilo esplicitamente. La CLI
   di Higgsfield è il percorso di riferimento (script inclusi); vanno bene anche Kie.ai,
   fal, Replicate o qualsiasi modello image-to-video che accetta un'immagine iniziale.
   Poi: è installato e autenticato? Quanti capitoli (clip)? Un tetto di crediti? — Farai
   le bozze a basso costo, confermerai la spesa e genererai la versione finale in piena
   risoluzione solo dopo la sua approvazione. Se non ha un motore, torna al percorso A.
6. **Cosa viene dopo il film?** Le sezioni sotto lo scroll (formazione / collezione /
   prenotazioni / manifesto…), la call-to-action principale, contatti e social.
7. **Dove va online?** Solo in locale, oppure pubblicato sul *suo* Vercel.

---

## PASSO 1 — Proponi i concept (prima di costruire qualsiasi cosa)

Dall'intervista sviluppa **2-3 concept creativi con un nome** e proponili. Regole:

- Apri con il concept **che raccomandi**, segnato esplicitamente "(Consigliato)".
- Ogni concept ha un *racconto concreto di cosa si vede*, non una tesi in una riga:
  racconta lo scroll: cosa vede il visitatore in cima, cosa succede mentre scorre, cosa
  mostra ogni capitolo, come il film si risolve nei contenuti.
  (es. *"Si apre su un campo di fiori al chiaro di luna, con un enorme logotipo serif che
  galleggia sopra. Scroll: la camera si tuffa in un solo fiore… i petali si aprono… stai
  cadendo tra braci d'oro… una goccia d'oro liquido cade in una pozza… la camera arretra:
  sei dentro la bottiglia, su marmo nero. Poi la pagina si scioglie nella collezione."*)
- Dai un nome a ogni concept (il titolo è metà della vendita), indica il percorso che usa,
  il numero di capitoli e (percorso B) i crediti stimati.
- **Confronto facoltativo con un secondo modello (se c'è):** prima di presentare, controlla
  se sul computer dell'utente c'è la CLI di un secondo modello di frontiera (es. `codex`,
  `gemini` o simili: qualsiasi modello diverso da quello che esegue questa skill). Se c'è,
  passagli i concept *come testo* e chiedigli di (a) attaccarli uno per uno — il viaggio si
  capisce? resta in mente? si fa in N capitoli? — e (b) proporre un'angolazione a sorpresa
  che non hai considerato. Metti nella proposta quello che regge (cita il confronto in una
  riga). **È solo critica di strategia: l'altro modello non scrive mai testi, codice o
  decisioni di design; decidi e scrivi tu.** Se non c'è un secondo modello, salta in
  silenzio: la skill basta a se stessa con il solo modello principale.
- Lascia che l'utente scelga o mescoli; se dice "scegli tu", prendi quello consigliato e vai.

Solo dopo che è stato scelto un concept si costruisce.

---

## PASSO 2 — Direzione artistica del mondo (solo tu)

Decidi e impegnati: palette (hex esatti), un **abbinamento di caratteri** titolo+testo con
vera personalità (mai i font di sistema: cerca caratteri da titolo espressivi), il logo
(SVG inline), la sensazione del movimento e i nomi dei capitoli. Font e mondo diversi per
ogni marchio: mai due marchi che sembrano lo stesso sito. Per ogni strumento di terze parti
citato usa il logo vero come SVG inline (mai un'imitazione disegnata a mano di un logo reale).

---

## PERCORSO A — Solo codice (predefinito)

Scrivi da zero una sola pagina HTML autosufficiente per questo marchio. Carica GSAP,
ScrollTrigger e Lenis da CDN (copiali in locale per la produzione). Componi il film con il
vocabolario di movimento di `references/engine.md` §Film solo in codice — scene fissate, timeline
con scrub, rivelazione dell'hero lettera per lettera, scorrimenti orizzontali fissati con
parallasse via containerAnimation, inclinazione in base alla velocità, contatori, marquee —
disposti per raccontare il viaggio di *questo* marchio (il racconto del passo 1 è il tuo
storyboard). Poi le sezioni dopo il film + footer (SVG veri dei social), verifica e
(se richiesto) deploy.

Legge critica sull'ordine: **crea gli ScrollTrigger degli effetti di sfondo DOPO le scene
fissate**: l'ordine di creazione è l'ordine di refresh; se lo violi, tutto quello che sta
dopo uno spazio di pin finisce nel posto sbagliato, senza nessun errore.

---

## PERCORSO B — Riprese cinematiche (qualsiasi motore image-to-video)

Leggi prima `references/playbook.md`: è la legge di questo percorso. Il playbook e
`scripts/chain-step.sh` implementano già il percorso di riferimento **Higgsfield
Seedance**. Per qualsiasi altro motore (Kie.ai Seedance/Veo, fal, Replicate…) tieni
identico il contratto di concatenazione — genera → aspetta → scarica → estrai l'ultimo
frame → controllo SSIM della giuntura — e cambia solo le chiamate di generazione, attesa e
download con la CLI o l'API di quel motore. In breve:

1. **Storyboard** del concept scelto in N capitoli (5 è il numero ideale), con un'unica
   direzione di camera continua dall'inizio alla fine.
2. **Genera il fotogramma iniziale** (Nano Banana Pro), poi concatena N clip in cui **lo
   `--start-image` di ogni clip è letteralmente l'ultimo frame della clip precedente**
   (`scripts/chain-step.sh` fa genera → aspetta → scarica → estrai i frame → controllo SSIM
   della giuntura). Prima una bozza economica di tutta la catena; la versione finale in
   piena risoluzione solo dopo l'approvazione.
3. **Controlla ogni giuntura** — misurata, mai a occhio; si ripara rigenerando con il
   linguaggio di continuazione esatta del playbook. Vietate le dissolvenze sopra le giunture
   venute male.
4. **Monta** con `scripts/assemble.sh` (toglie i frame duplicati alle giunture, codifica con
   `-fps_mode vfr`, estrae ~300 frame, campiona il colore della giuntura).
5. **Costruisci la pagina da zero** intorno alle riprese: il motore di scrub su canvas di
   `references/engine.md` §Motore di scrub (finestra scorrevole di ImageBitmap — il cuore
   contro il jank — indice del frame interpolato, header a contrasto adattivo, indicatore di
   capitolo/altimetro, testi sovrapposti ai momenti, passaggio alla giuntura, livello hero
   di sfondo facoltativo, il contratto di sviluppo `?jump`/`__ready`). Scrivilo per questo
   marchio; non copiare un sito precedente.

**Circa il 15% dei job di Higgsfield fallisce lato server senza motivo e non viene
addebitato: riprova.**

---

## IL MODELLO DI DELEGA (come si risparmiano token)

Sei l'orchestratore e il designer. Spendi token di frontiera solo dove serve il gusto.

| Lavoro | Chi lo fa | Costo |
| --- | --- | --- |
| Concept, direzione artistica, palette, caratteri, layout, movimento, testi finali, costruzione, revisione del design | **Tu (il modello principale)** — mai delegato. Il design va sul modello più forte disponibile. | di frontiera, ne vale la pena |
| Confronto sui concept — attaccare la proposta, un'angolazione a sorpresa (facoltativo, se c'è una seconda CLI) | **Un altro modello di frontiera** (es. GPT/Codex, Claude, Gemini — quello che non sei tu) — solo testo di strategia, mai design | una chiamata economica |
| Solo prime bozze: il prompt video di un capitolo, i testi di una sezione dopo il film — **ogni bozza la rivedi e la riscrivi tu; niente di quello che scrive un sub-agent esce senza modifiche** | **Sub-agent** con lo stesso modello, in parallelo | economico, in parallelo |
| Estrazione dei frame, controllo SSIM, montaggio, campionamento delle giunture, test di jank, screenshot, deploy | **Solo shell, nessun modello** (`scripts/*`, ffmpeg, puppeteer, vercel) | quasi gratis |

Fai andare in parallelo i pezzi indipendenti; la spina dorsale che richiede gusto la tieni tu.

---

## DISCIPLINA DEI COSTI (percorso B)

1. **Audio SPENTO** — `--generate-audio false`. L'audio acceso triplica il conto senza avvisare.
2. **Conferma prima di spendere.** Indica il totale dei crediti *prima* di ogni generazione;
   mostra il saldo dopo.
3. **Bozza economica, versione finale una volta.** Convalida tutta la catena al livello più
   economico (480p/fast), poi rigenera solo i prompt approvati in piena risoluzione
   (1080p/std sul motore di riferimento).
4. **Riusa le riprese.** Un film può alimentare più direzioni: il costo sono le riprese,
   cambiare veste è gratis.

---

## VERIFICA (entrambi i percorsi)

In ogni costruzione implementa il contratto di sviluppo: `?jump=<scrollY>` apre la pagina
già scrollata con tutto lo stato dello scroll assestato, e `window.__ready = true` scatta
solo quando la pagina è davvero pronta. Poi `scripts/verify.js` (puppeteer-core + Chrome di
sistema) fa screenshot di qualsiasi posizione di scroll ed esegue il **test di jank**
(delta di rAF per frame: giudica p95/massimo, *mai* gli fps medi; obiettivo massimo < 50 ms).
Fai lo screenshot di ogni momento e di ogni giuntura. Mai chiedere all'utente di guardare a
occhio quello che puoi dimostrare. Le anteprime dell'host rallentano le schede nascoste (rAF
congelato → screenshot vecchi): per questo esiste questo strumento.

---

## DEPLOY (su richiesta, sul suo Vercel)

Prima prepara una copia **snella**: `index.html` + librerie copiate in locale (risolvi i
link simbolici con `cp -RL`) + solo i `frames/`/`assets/` usati a runtime. Mai caricare i
file intermedi della costruzione (clip grezze, fotogrammi chiave: spesso oltre 100 MB). Poi
`vercel deploy --prod --yes` dalla cartella snella. Avvisa l'utente che i progetti Vercel
nuovi spesso stanno dietro la **Deployment Protection** (un muro di login); renderli
pubblici è un'impostazione del suo account (Project → Settings → Deployment Protection):
indicagliela, non cambiare tu le sue impostazioni di sicurezza.

---

## REGOLE DI SICUREZZA

- **Questa skill non contiene dati personali**: niente chiavi API, niente account, niente
  percorsi personali. Ogni utente porta il suo motore video e il suo Vercel. Mai scrivere
  credenziali nel codice.
- Design e costruzione restano sul modello principale. Il lavoro meccanico va al codice; il
  design mai.
- Conferma i crediti prima di spendere; mostra il saldo dopo.
- Un'unica inquadratura continua; un mondo per marchio; nessuna giuntura visibile; nessuna
  dissolvenza per mascherare.
- Rispetta `prefers-reduced-motion` in ogni costruzione.
- File di riferimento: `references/playbook.md` (legge delle riprese), `references/engine.md`
  (ricette di costruzione), `scripts/chain-step.sh`, `scripts/assemble.sh`, `scripts/verify.js`.
  Gli script `.sh` sono bash: macOS e Linux li eseguono così come sono, su Windows usa Git
  Bash o WSL.

## Uso

```text
/scroll-film sito a camera continua per la scuderia elettrica VOLTA
/scroll-film pagina scrollytelling per un marchio di profumi di lusso
```
