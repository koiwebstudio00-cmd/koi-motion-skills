#!/bin/zsh
# Prepara un reel de referencia para estudiarlo cuadro por cuadro.
# Se corre desde la carpeta del proyecto: study_refs.sh <link o archivo> [nombre]
# Deja en Reference/estudio/<nombre>/: frames/ (uno cada 0,25 s), hojas/ (1 s por hoja, 2 × 2),
# cortes.txt (segundos donde cambia el plano) y audio.wav.
SRC="${1:?Falta el link o el archivo}"
NAME="${2:-${${SRC:t}:r}}"
OUT="Reference/estudio/$NAME"

if [[ $SRC == http* ]]; then
  command -v yt-dlp >/dev/null || { echo "Falta yt-dlp: brew install yt-dlp"; exit 1; }
  mkdir -p "$OUT"
  yt-dlp -q --no-playlist -f "bv*+ba/b" --merge-output-format mp4 -o "$OUT/video.%(ext)s" "$SRC" || exit 1
  VIDEO="$OUT/video.mp4"
else
  [[ -f $SRC ]] || { echo "No existe $SRC"; exit 1; }
  VIDEO="$SRC"
fi

rm -rf "$OUT/frames" "$OUT/hojas"
mkdir -p "$OUT/frames" "$OUT/hojas"
ffmpeg -v error -y -i "$VIDEO" -vf "fps=4,scale=540:-2" -q:v 3 "$OUT/frames/f%04d.jpg" || exit 1
ffmpeg -v error -y -i "$VIDEO" -vf "fps=4,scale=540:-2,tile=2x2:padding=6:color=white" -q:v 3 "$OUT/hojas/hoja-%04d.jpg" || exit 1
ffmpeg -hide_banner -i "$VIDEO" -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$OUT/cortes.txt"
ffmpeg -v error -y -i "$VIDEO" -vn -ac 1 -ar 16000 "$OUT/audio.wav" 2>/dev/null || rm -f "$OUT/audio.wav"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
CUTS=$(wc -l < "$OUT/cortes.txt" | tr -d ' ')
SHEETS=$(ls "$OUT/hojas" | wc -l | tr -d ' ')
printf "%s: %.1f s, %s hojas, %s cortes (%.2f por segundo)\n" "$NAME" "$DUR" "$SHEETS" "$CUTS" $(( CUTS / DUR ))
echo "Leer todas las hojas de $OUT/hojas en orden. La hoja N es del segundo N-1 al N."
