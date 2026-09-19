#!/usr/bin/env bash
# assemble.sh <cartella-assets> <cartella-frame> <clip1> <clip2> ...  (nomi delle clip senza .mp4, in ordine)
#
# Concatena le clip della catena (togliendo il frame duplicato alla giuntura dalla clip 2 in poi),
# codifica il master con -fps_mode vfr (il riempimento CFR crea zone di scrub congelate), estrae
# ~300 frame JPEG a 1280 px per lo scrub su canvas e stampa il colore della giuntura dell'ultimo
# frame per il passaggio ai contenuti.
# Lavoro meccanico, nessun modello. Richiede: bash, ffmpeg >= 5.1 (-fps_mode), xxd.
set -e -o pipefail
shopt -s nullglob   # un glob senza corrispondenze non produce niente
if (( $# < 4 )); then   # prima di shift 2: con meno argomenti set -e uscirebbe senza messaggio
  echo "uso: assemble.sh <cartella-assets> <cartella-frame> <clip1> <clip2> ... (almeno 2 clip)"; exit 1
fi
A=$1; F=$2; shift 2
for CLIP in "$@"; do [[ -r "$A/$CLIP.mp4" ]] || { echo "clip mancante: $A/$CLIP.mp4"; exit 1; }; done
mkdir -p "$F"

INPUTS=(); FILTER=""; N=0
for CLIP in "$@"; do
  INPUTS+=(-i "$A/$CLIP.mp4")
  if (( N == 0 )); then FILTER+="[${N}:v]setpts=PTS-STARTPTS[v${N}];"
  else FILTER+="[${N}:v]select='gte(n\\,1)',setpts=PTS-STARTPTS[v${N}];"; fi
  N=$((N+1))
done
CONCAT=""; for ((i=0;i<N;i++)); do CONCAT+="[v${i}]"; done
FILTER+="${CONCAT}concat=n=${N}:v=1:a=0[out]"

ffmpeg -y -v error "${INPUTS[@]}" -filter_complex "$FILTER" -map "[out]" \
  -fps_mode vfr -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p "$A/master.mp4"
echo "master: $(ffprobe -v error -select_streams v -show_entries stream=width,height,nb_frames -of csv=p=0 "$A/master.mp4")"

rm -f "$F"/f_*.jpg
ffmpeg -v error -i "$A/master.mp4" -vf "select='not(mod(n\\,2))',scale=1280:-2" -vsync vfr -q:v 4 "$F/f_%04d.jpg"
FRAMES=("$F"/f_*.jpg)
COUNT=${#FRAMES[@]}
if (( COUNT == 0 )); then echo "FALLITO — nessun frame estratto"; exit 1; fi
echo "frame: $COUNT a 1280 px di larghezza, $(du -sh "$F" | cut -f1)  ->  imposta FRAME_COUNT=$COUNT nel motore"

LAST=${FRAMES[$((COUNT-1))]}   # bash 3.2 (macOS) non ha gli indici negativi
SEAM=$(ffmpeg -v error -i "$LAST" -vf "crop=iw:ih*0.12:0:ih*0.88,scale=1:1" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p | cut -c1-6)
if [[ -z "$SEAM" ]]; then echo "avviso: impossibile campionare il colore della giuntura, campiona $LAST a mano"; else
echo "colore della giuntura di $(basename $LAST): #$SEAM   (fai partire da qui lo sfondo della sezione dopo il film)"; fi
