#!/bin/zsh
# Renderiza con motion blur real: exporta a muchos cuadros por segundo y los mezcla hasta llegar a 30.
# Se corre desde la carpeta del proyecto: render.sh <salida.mp4> [240|180|120]
# 240 es el final ideal. 180 o 120 si falta disco. 120 también sirve para borradores.
OUT="${1:?Falta el archivo de salida}"
FPS="${2:-240}"
case $FPS in
  240) MIX=6; STEP=8; PICK=5 ;;
  180) MIX=5; STEP=6; PICK=4 ;;
  120) MIX=3; STEP=4; PICK=2 ;;
  *) echo "Cuadros por segundo no válidos: usá 240, 180 o 120"; exit 1 ;;
esac
RAW="assets/build/raw$FPS.mp4"
mkdir -p assets/build "${OUT:h}"
[[ -f tools/build.py ]] && { python3 tools/build.py || exit 1; }
npx --yes hyperframes@0.9.10 render --fps $FPS --sdr --crf 14 --page-motion-blur off -w 3 -o "$RAW" . || exit 1
ffmpeg -v error -y -i "$RAW" -i assets/mix.m4a -filter_complex "[0:v]tmix=frames=$MIX,select='eq(mod(n,$STEP),$PICK)',setpts=N/30/TB,fps=30,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]" \
  -map '[v]' -map 1:a -r 30 -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart -shortest "$OUT" || exit 1
rm -f "$RAW"
ffprobe -v error -show_entries format=duration:stream=codec_name,nb_frames,r_frame_rate,color_transfer -of compact=p=0 "$OUT"
