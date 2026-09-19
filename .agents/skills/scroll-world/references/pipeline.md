# Pipeline: script da copiare (compatibili con bash 3.2)

Impostale una volta. `NAMES` sono gli id delle sezioni in ordine; l'ultimo è l'hero/finale.

```bash
WORK=/tmp/scroll-world           # cartella di lavoro per prompt, sorgenti, frame
ASSETS=./assets                  # dove il sito legge immagini (webp) e clip (mp4)
mkdir -p "$WORK" "$ASSETS/vid"
NAMES="farm kitchen shop delivery plaza finale"   # <-- gli id delle tue sezioni, in ordine

# Modello video della catena: UNO per tutte le clip concatenate (elenco del passo 4 di SKILL).
# Deve accettare --start-image E --end-image (verifica: higgsfield model get <modello>):
# seedance_2_0 | kling3_0 | seedance_2_0_mini (livello bozza). I modelli solo di riferimento non
# tengono una giuntura; i modelli senza --mode (es. kling3_0_turbo) vogliono un loro ramo di flag qui sotto.
VMODEL=seedance_2_0
case "$VMODEL" in                                  # flag e durate per modello (compatibile con bash 3.2)
  kling3_0)          VOPTS="--mode std --sound off";          DIVE_DUR=10; CONN_DUR=5 ;;  # Kling non ha --resolution
  seedance_2_0_mini) VOPTS="--mode std --resolution 720p";    DIVE_DUR=8;  CONN_DUR=5 ;;  # previz economica che aggancia i frame
  *)                 VOPTS="--mode std --resolution 1080p";   DIVE_DUR=8;  CONN_DUR=5 ;;  # seedance_2_0, predefinito
esac
```

Le generazioni di Higgsfield durano minuti: ogni chiamata `higgsfield ... --wait` qui sotto va
eseguita dentro uno script **in background**. Lancia tutto lo script con la modalità in
background/staccata del tuo strumento e controlla il log di avanzamento; mai bloccare il primo piano.

**Ripresa / idempotenza.** Ogni funzione `gen_*` qui sotto salta il lavoro il cui file di output
esiste già e non è vuoto: `$WORK` *è* lo stato della corsa. Un crash, i crediti finiti o un
rifacimento per l'NSFW non costano mai il materiale già finito: rilancia lo stesso ciclo e si
rigenerano solo i pezzi mancanti. Per forzare il rifacimento di un pezzo, cancella prima il suo
file (`rm "$WORK/dive_shop.mp4"; gen_dive shop`). Per vedere a che punto è una corsa:

```bash
status() { for n in $NAMES; do
  printf '%-10s immagine:%s tuffo:%s\n' "$n" \
    "$([ -s "$WORK/still_$n.png" ] && echo ok || echo -- )" \
    "$([ -s "$WORK/dive_$n.mp4" ] && echo ok || echo -- )"
done; ls "$WORK"/conn_*.mp4 2>/dev/null | while read f; do printf 'connettore: %s ok\n' "$f"; done; }
```

**Prima la previz (predefinita consigliata).** Esegui tutta la catena una volta al livello di bozza
prima di spendere i crediti del modello completo:

```bash
VMODEL=seedance_2_0_mini   # aggancio dei frame intatto (~720p): le giunture si comportano come nella versione finale
# … esegui §2-§5, rivedi la pagina montata, sistema viaggio/prompt/giunture spendendo poco …
VMODEL=seedance_2_0        # poi togli le clip di bozza e rigenera la versione finale
rm -f "$WORK"/dive_*.mp4 "$WORK"/conn_*.mp4 "$WORK"/first_*.png "$WORK"/last_*.png
```

Siccome il livello mini aggancia comunque i frame, tutto quello che convalidi (viaggio, grammatica
della camera, continuità delle giunture, ritmo dei testi) vale direttamente per la versione finale.
Le immagini si riusano così come sono: si rifanno solo i passaggi video. Salta la previz solo per le
corse piccole (≤4 scene), dove rifare con il modello completo costa meno del passaggio in più.

## 1. Immagini delle scene (passo 2) — prima l'anchor, poi il lotto

Scrivi un file di prompt per sezione in `$WORK/still_<nome>.txt` (vedi prompts.md).

**NON lanciare subito tutte le N.** Genera prima UNA immagine anchor (la scena più
rappresentativa), fatti approvare la direzione artistica dall'utente, poi lancia le altre passando
l'anchor approvata come `--image` per bloccare lo stile. Uno stile sbagliato trovato sull'anchor
costa 1 generazione; trovato dopo il lotto ne costa N.

```bash
STYLE_LOCK=""   # impostala sull'anchor approvata dopo il controllo qui sotto
gen_still() { # nome
  [ -s "$WORK/still_$1.png" ] && { echo "immagine $1 già pronta"; return 0; }
  higgsfield generate create gpt_image_2 --prompt "$(cat "$WORK/still_$1.txt")" \
    ${STYLE_LOCK:+--image "$STYLE_LOCK"} \
    --aspect_ratio 3:2 --resolution 2k --quality high --wait --wait-timeout 15m --json \
    > "$WORK/still_$1.json" 2> "$WORK/still_$1.err"
  url=$(jq -r '.[0].result_url // empty' "$WORK/still_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/still_$1.png" && echo "immagine $1 ok" || echo "immagine $1 FALLITA"
}

# 1. Anchor + approvazione (scegli la scena che esprime meglio il mondo):
gen_still farm                      # ← la tua sezione anchor
# → MOSTRA all'utente still_farm.png; rifinisci il preambolo di stile finché non la approva.
#   Anchor rifiutata: correggi il preambolo in TUTTI i file di prompt, cancella il png, rifai.

# 2. Poi lancia le altre, con lo stile bloccato sull'anchor approvata:
STYLE_LOCK="$WORK/still_farm.png"
for n in $NAMES; do gen_still "$n" & done ; wait   # l'anchor si salta da sola (già pronta)
```

Converti in webp per il sito (e, se vuoi la trasparenza, lancia prima knockout.py):

```bash
for n in $NAMES; do cwebp -quiet -q 84 -resize 1800 0 "$WORK/still_$n.png" -o "$ASSETS/$n.webp"; done
```

Controlla la coerenza del lotto prima di continuare. Rifai quelle fuori stile
(`rm "$WORK/still_shop.png"; gen_still shop`: il blocco di stile è ancora attivo).

## 2. Clip di tuffo (passo 4)

File di prompt in `$WORK/dive_<nome>.txt`. Immagine iniziale = il PNG con lo sfondo pieno.

```bash
gen_dive() { # nome                       ($VOPTS è senza virgolette apposta: i flag vanno divisi)
  [ -s "$WORK/dive_$1.mp4" ] && { echo "tuffo $1 già pronto"; return 0; }
  higgsfield generate create "$VMODEL" --prompt "$(cat "$WORK/dive_$1.txt")" \
    --start-image "$WORK/still_$1.png" \
    $VOPTS --aspect_ratio 16:9 --duration "$DIVE_DUR" \
    --wait --wait-timeout 20m --json > "$WORK/dive_$1.json" 2> "$WORK/dive_$1.err"
  url=$(jq -r '.[0].result_url // empty' "$WORK/dive_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/dive_$1.mp4" && echo "tuffo $1 ok" || echo "tuffo $1 FALLITO"
}
for n in $NAMES; do gen_dive "$n" & done ; wait
```

Rifai una per una quelle fallite (503 e crediti contesi sono passeggeri):
`gen_dive shop` (solo quella).

## 3. Estrai i frame di confine — il passaggio alla giuntura (passo 5)

Per ogni coppia vicina, l'inizio del connettore = l'ULTIMO frame di dive_i, la fine = il PRIMO frame
di dive_{i+1}, estratti dai **video renderizzati**, mai dalle immagini.

```bash
set -- $NAMES
prev=""
for n in "$@"; do
  ffmpeg -v error -ss 0 -i "$WORK/dive_$n.mp4" -frames:v 1 -q:v 2 "$WORK/first_$n.png"      # campo lungo
  ffmpeg -v error -sseof -0.15 -i "$WORK/dive_$n.mp4" -frames:v 1 -q:v 2 "$WORK/last_$n.png" # interno
done
```

## 4. Clip connettore (passo 5)

File di prompt in `$WORK/conn_<i>.txt` (i = 1..N-1). Scorri le coppie vicine:

```bash
gen_conn() { # i pngIniziale pngFinale     (serve l'end-image → solo seedance/kling3_0)
  [ -s "$WORK/conn_$1.mp4" ] && { echo "connettore $1 già pronto"; return 0; }
  higgsfield generate create "$VMODEL" --prompt "$(cat "$WORK/conn_$1.txt")" \
    --start-image "$2" --end-image "$3" \
    $VOPTS --aspect_ratio 16:9 --duration "$CONN_DUR" \
    --wait --wait-timeout 20m --json > "$WORK/conn_$1.json" 2> "$WORK/conn_$1.err"
  url=$(jq -r '.[0].result_url // empty' "$WORK/conn_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/conn_$1.mp4" && echo "connettore $1 ok" || echo "connettore $1 FALLITO"
}
set -- $NAMES ; i=0 ; prev=""
for n in "$@"; do
  if [ -n "$prev" ]; then i=$((i+1)); gen_conn "$i" "$WORK/last_$prev.png" "$WORK/first_$n.png" & fi
  prev="$n"
done ; wait
```

## 5. Codifica tutto per lo scrub (passo 6)

Risoluzione nativa (1080p da seedance std; kling3_0 std nelle prove ha restituito **720p**: mai
ingrandire, codifica quello che riporta ffprobe), crf 20, GOP 8, leggera nitidezza, niente audio,
faststart. Uguale per tuffi e connettori.

```bash
enc() { ffmpeg -v error -y -i "$1" -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$2"; echo "codificato $2 $(du -h "$2"|cut -f1)"; }

for n in $NAMES; do enc "$WORK/dive_$n.mp4" "$ASSETS/vid/$n.mp4"; done
i=0; for f in "$WORK"/conn_*.mp4; do i=$((i+1)); enc "$f" "$ASSETS/vid/conn$i.mp4"; done
```

Ora nella configurazione del motore `sections[k].clip = assets/vid/<nome>.mp4` e
`connectors = [assets/vid/conn1.mp4, …]` (lunghezza N-1, in ordine).

## 5b. Poster — estratti dalle clip CODIFICATE (niente scatto da immagine a video)

L'immagine generata è in 3:2 e la clip ne è una nuova resa in 16:9, quindi se il poster di
caricamento è l'immagine, nel momento in cui il video disegna c'è un salto visibile di ritaglio e
resa, proprio sulla prima scena che il visitatore vede. Stessa dottrina dei connettori: passarsi i
frame reali. Il poster deve essere il primo frame della clip codificata stessa:

```bash
for n in $NAMES; do
  ffmpeg -v error -y -ss 0 -i "$ASSETS/vid/$n.mp4" -frames:v 1 -q:v 2 "$WORK/poster_$n.png"
  cwebp -quiet -q 84 "$WORK/poster_$n.png" -o "$ASSETS/$n-poster.webp"
done
```

Collegalo come `sections[k].poster = 'assets/<nome>-poster.webp'`. Tieni anche `still`: resta la
grafica per il movimento ridotto e il ripiego senza clip (il motore preferisce `poster` quando una
clip sta per caricarsi, altrimenti `still`).

## 5c. Verifica le giunture — in automatico, prima di guardarle a occhio

L'assenza di giunture è il prodotto: non consegnarla strizzando gli occhi. Ogni giuntura della
catena deve essere quasi identica tra i suoi frame di confine. Controllale tutte con l'SSIM dai file
codificati (ordine della catena: dive0, conn1, dive1, conn2, …; per l'architettura A è solo leg0, leg1, …):

```bash
# ultimo frame di A contro primo frame di B, punteggio SSIM su stdout
seam_ssim() { # fileA fileB
  ffmpeg -v error -y -sseof -0.05 -i "$1" -frames:v 1 "$WORK/_sa.png"
  ffmpeg -v error -y -ss 0      -i "$2" -frames:v 1 "$WORK/_sb.png"
  ffmpeg -v info -i "$WORK/_sa.png" -i "$WORK/_sb.png" -lavfi ssim -f null - 2>&1 \
    | grep -o 'All:[0-9.]*' | cut -d: -f2
}

check() { # fileA fileB etichetta
  s=$(seam_ssim "$1" "$2")
  case $(awk -v s="${s:-0}" 'BEGIN{ if (s>=0.90) print "pass"; else if (s>=0.75) print "warn"; else print "fail" }') in
    pass) echo "OK      $3  ssim=$s" ;;
    warn) echo "AVVISO  $3  ssim=$s (la dissolvenza la nasconderà quasi del tutto: guarda questa giuntura)" ;;
    *)    echo "KO      $3  ssim=$s — gli estremi NON sono i frame delle clip vicine; rifai questo connettore (passo 5 di SKILL)" ;;
  esac
}

# Architettura B (tuffi e connettori alternati):
set -- $NAMES ; i=0 ; prev=""
for n in "$@"; do
  if [ -n "$prev" ]; then i=$((i+1))
    check "$ASSETS/vid/$prev.mp4" "$ASSETS/vid/conn$i.mp4" "$prev>conn$i"
    check "$ASSETS/vid/conn$i.mp4" "$ASSETS/vid/$n.mp4"    "conn$i>$n"
  fi ; prev="$n"
done
# Architettura A (tratti in sequenza): controlla le coppie "$ASSETS/vid/legI.mp4" "$ASSETS/vid/legI+1.mp4".
```

Soglie ricavate dalla fisica del passaggio dei frame: un vero passaggio di frame reali fa ≥0.95
anche dopo la codifica; ≥0.90 superato, 0.75-0.90 avviso (l'end-image di Seedance è arrivata vicina
ma non esatta: di solito la dissolvenza del motore la copre), <0.75 vuol dire che come estremo è
stata usata un'immagine o è stato estratto il frame sbagliato: rigenera, non cercare giustificazioni.
Eseguilo anche dopo ogni rifacimento: sostituire una clip può rompere, senza dirlo, ENTRAMBE le sue giunture.

## 6. Codifiche mobile (passo 6) — solo se l'utente ha scelto una fascia mobile

**Salta questa sezione se nell'intervista del passo 1 l'utente ha scelto il ritaglio sicuro.** Lo
scrub imposta `currentTime` a ogni frame, e **il costo di un seek sul decoder di un telefono cresce
con il numero di frame da decodificare a partire dal keyframe più vicino**: così un master 1080p
`-g 8` che scorre bene su un portatile scatta su un telefono. Un **frame più piccolo + un GOP più
stretto** lo risolve (e dimezza i byte su rete mobile). Produci una variante `-m.mp4` per ogni clip:

```bash
# 720p, GOP 4 (il doppio dei keyframe = ~metà del lavoro di decodifica nei seek), crf 23, stessa nitidezza e faststart.
encm() { ffmpeg -v error -y -i "$1" -an -vf "scale=-2:720,unsharp=5:5:0.6:5:5:0.0" \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$2"; echo "codificato mobile $2 $(du -h "$2"|cut -f1)"; }

for n in $NAMES; do encm "$WORK/dive_$n.mp4" "$ASSETS/vid/$n-m.mp4"; done
i=0; for f in "$WORK"/conn_*.mp4; do i=$((i+1)); encm "$f" "$ASSETS/vid/conn$i-m.mp4"; done
```

Estrai il primo frame di ogni codifica mobile come suo poster (dottrina del §5b: il poster deve
corrispondere alla codifica che il dispositivo riceve davvero):

```bash
for n in $NAMES; do
  ffmpeg -v error -y -ss 0 -i "$ASSETS/vid/$n-m.mp4" -frames:v 1 -q:v 2 "$WORK/poster_${n}_m.png"
  cwebp -quiet -q 84 "$WORK/poster_${n}_m.png" -o "$ASSETS/$n-poster-m.webp"
done
```

Collega le varianti nella configurazione del motore: il motore le serve ai dispositivi di classe
telefono (lato corto dello schermo ≤600 px CSS; tablet e iPad ricevono il master) e usa la `clip`
desktop quando manca quella mobile:

```js
sections[k].clipMobile   = 'assets/vid/<nome>-m.mp4';
sections[k].posterMobile = 'assets/<nome>-poster-m.webp';
connectorsMobile = ['assets/vid/conn1-m.mp4', …];   // lunghezza N-1, in ordine
```

Se lo scrub sul telefono scatta ancora, stringi ancora il GOP (`-g 2`, o `-g 1` per il tutto intra =
seek istantanei al prezzo di file più grandi); se preoccupa di più il peso su rete mobile, alza il
`crf` (24-26) o scendi a `scale=-2:600`. Se il master è già a 720p (es. kling3_0 std), la codifica
mobile conviene comunque: è il GOP più stretto a rendere economici i seek sul telefono. Le codifiche
della fascia mobile semplice restano in 16:9: il motore le ritaglia al centro; per materiale davvero
verticale vedi §7.

## 7. Fasce verticali (passo 1.6: hero reinquadrato / catena verticale completa) — crediti in più

Il massimo per il mobile è una **resa inquadrata in modo diverso, non un ritaglio** (Apple distribuisce
materiale con una direzione artistica diversa per ogni breakpoint). Due livelli:

**Hero reinquadrato (economico).** Per le 1-2 scene il cui soggetto non regge un ritaglio al centro
(di solito hero e finale): rigenera SOLO quelle immagini in 9:16 (stesso prompt + anchor di stile,
ricomposte in verticale), rendi un tuffo 9:16 da ciascuna, codifica con le impostazioni di `encm()`,
collegale come `clipMobile`/`posterMobile` di quella scena. Le altre scene tengono la codifica mobile
16:9 ritagliata. Giunture: un tuffo verticale passa i frame solo dentro la sua clip, quindi nella
catena 16:9 non cambia niente: il telefono fa una dissolvenza tra un connettore ritagliato e il tuffo
verticale; tieni la composizione reinquadrata centrata sullo stesso punto focale, così la transizione si legge.

**Catena verticale completa (oro, ≈2× i crediti video).** Una catena 9:16 completa e parallela:

- Immagini 9:16 (oppure riusa le immagini 16:9 come riferimenti di stile `--image` e chiedi nel prompt
  la ricomposizione verticale), poi tutto il flusso dei passi 4/5 con `--aspect_ratio 9:16`: estrazioni
  dei frame proprie, connettori propri, passaggi propri. **I formati non si mescolano a metà catena**:
  una clip 9:16 non continua un frame 16:9, quindi la catena verticale si genera dall'inizio alla fine
  come un mondo a sé.
- Esegui il controllo SSIM del §5c sulla catena verticale separatamente (con il suo elenco di giunture).
- Codifica con `encm()` (già in classe 720; in verticale con `scale=720:-2`), estrai i poster verticali,
  collega TUTTO come `clipMobile`/`connectorsMobile`/`posterMobile`.
- Stessa regola del modello unico, stesso budget di rifacimenti per l'NSFW: vale tutto quello della catena 16:9.

Indica all'utente il costo in crediti prima di iniziare una delle due fasce (passo 1.6 di SKILL).

## Note

- `.[0].result_url` è il campo dell'oggetto job di `--wait --json`. `.min_result_url` è un'anteprima
  a risoluzione più bassa, se mai ti servisse.
- **Ripiego per l'NSFW con un altro modello**: se una clip continua a essere bloccata su seedance
  anche dopo rifacimenti e pulizia del prompt, rigenera solo quella con `kling3_0` e gli STESSI frame
  iniziale e finale: `VMODEL=kling3_0; VOPTS="--mode std --sound off"; gen_conn 3 …`, poi rimetti il
  modello della catena. Il compromesso è spiegato nelle Trappole di SKILL.
- **Previz**: il passaggio al livello di bozza è la scelta predefinita consigliata: vedi il blocco di
  configurazione in cima. Non usare per la previz modelli solo di riferimento: senza
  `--start/--end-image` non tengono una giuntura, quindi il loro output non si concatena (regola del passo 4).
- Se un intero lotto si blocca, controlla i crediti con `higgsfield workspace list` e il motivo in
  `$WORK/*.err`.
- Concorrenza: lanciare ~5-6 generazioni insieme va bene; molte di più possono causare errori
  passeggeri di crediti contesi: scaglionale o rifalle.
