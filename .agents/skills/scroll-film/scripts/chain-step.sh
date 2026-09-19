#!/usr/bin/env bash
# chain-step.sh <cartella-assets> <nome-clip> <immagine-iniziale> <prompt> [ultimo-png-precedente] [risoluzione]
#
# Genera UNA clip Higgsfield Seedance concatenata a partire da <immagine-iniziale>, aspetta,
# scarica, estrae il primo e l'ultimo frame e controlla con l'SSIM la giuntura con <ultimo-png-precedente>.
# Lavoro meccanico, nessun modello. Richiede: CLI higgsfield (con login), ffmpeg, python3, curl.
#
#   La risoluzione predefinita è 1080p. Usa 480p per le bozze economiche (la modalità passa da sola a fast).
set -e -o pipefail
DIR=$1; NAME=$2; START=$3; PROMPT=$4; PREV=$5; RES=${6:-1080p}
if [[ -z "$DIR" || -z "$NAME" || -z "$START" || -z "$PROMPT" ]]; then
  echo "uso: chain-step.sh <cartella-assets> <nome-clip> <immagine-iniziale> <prompt> [ultimo-png-precedente] [risoluzione]"; exit 1
fi
[[ -r "$START" ]] || { echo "immagine iniziale non leggibile: $START"; exit 1; }
for bin in higgsfield ffmpeg python3 curl; do command -v $bin >/dev/null || { echo "dipendenza mancante: $bin"; exit 1; }; done
MODE=std; [[ "$RES" == "480p" || "$RES" == "720p" ]] && MODE=fast
mkdir -p "$DIR"

echo "[$NAME] creo il job ($RES/$MODE, audio spento)..."
CREATE=$(higgsfield generate create seedance_2_0 \
  --prompt "$PROMPT" \
  --start-image "$START" \
  --duration 5 --resolution "$RES" --mode "$MODE" --generate-audio false \
  --json 2>&1)
ID=$(echo "$CREATE" | python3 -c "import sys,re;s=sys.stdin.read();m=re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',s);print(m[0] if m else '')")
if [[ -z "$ID" ]]; then
  echo "[$NAME] FALLITO — nessun ID del job nell'output di create (non lo cerco nella lista dei job:"
  echo "[$NAME] potrei agganciarmi a un job che non c'entra). Ultime righe dell'output:"
  echo "$CREATE" | tail -5; exit 1
fi
echo "[$NAME] job $ID — in attesa..."

WAIT=$(higgsfield generate wait "$ID" --timeout 15m --interval 5s --json 2>&1)
URL=$(echo "$WAIT" | python3 -c "import sys,re;s=sys.stdin.read();m=re.findall(r'https://[^\"\s]+\.mp4[^\"\s]*',s);print(m[-1] if m else '')")
if [[ -z "$URL" ]]; then
  echo "[$NAME] FALLITO — nessun URL mp4 (i fallimenti lato server non si pagano: riprova)."
  echo "$WAIT" | tail -5; exit 1
fi

curl -fsSL -o "$DIR/$NAME.mp4" "$URL"
ffmpeg -y -v error -i "$DIR/$NAME.mp4" -vf "select=eq(n\,0)" -frames:v 1 -update 1 -q:v 1 "$DIR/$NAME-first.png"
ffmpeg -y -v error -sseof -0.05 -i "$DIR/$NAME.mp4" -update 1 -q:v 1 "$DIR/$NAME-last.png"
echo "[$NAME] scaricata: $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$DIR/$NAME.mp4")"

if [[ -n "$PREV" ]]; then
  SSIM=$( (ffmpeg -i "$PREV" -i "$DIR/$NAME-first.png" -lavfi ssim -f null - 2>&1 || true) | grep -o 'All:[0-9.]*' | cut -d: -f2)
  ffmpeg -y -v error -i "$PREV" -i "$DIR/$NAME-first.png" -filter_complex "[0][1]hstack" "$DIR/$NAME-junction-compare.jpg" || true
  if [[ -z "$SSIM" ]]; then echo "[$NAME] impossibile calcolare l'SSIM della giuntura — guarda $NAME-junction-compare.jpg"; exit 2; fi
  echo "[$NAME] SSIM DELLA GIUNTURA con $(basename $PREV): $SSIM   (affiancate: $NAME-junction-compare.jpg)"
  PASS=$(python3 -c "print(1 if float('$SSIM') >= 0.80 else 0)")
  if [[ "$PASS" == "0" ]]; then
    echo "[$NAME] GIUNTURA DA CONTROLLARE (<0.80). L'SSIM sottostima le texture casuali (nuvole,"
    echo "[$NAME] particelle, caustiche possono non avere giunture visibili anche a 0.6): guarda le immagini"
    echo "[$NAME] affiancate. Un cambio strutturale (nuovo orizzonte, oggetti, colore) è un vero fallimento:"
    echo "[$NAME] rigenera con 'Continue the exact same shot from the reference frame, identical framing,"
    echo "[$NAME] identical colour grade. Do not change the colour grade.'"
    exit 2   # uscita 2 = clip scaricata, ma la giuntura va guardata prima di andare avanti
  fi
fi
echo "[$NAME] FATTO"
