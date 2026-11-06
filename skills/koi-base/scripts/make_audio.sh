#!/bin/zsh
# Arma assets/mix.m4a: voz adelante, música debajo y efectos. Música y efectos bajan solos cuando se habla.
# Se corre desde la carpeta del proyecto: make_audio.sh <voz> <musica> <duracion_s> [volumen_musica]
# 0.36 es el nivel aprobado. Con otra canción, igualar el volumen percibido en vez de copiar el número.
VOICE="${1:?Falta la voz}"
SONG="${2:?Falta la música}"
DUR="${3:?Falta la duración en segundos}"
LEVEL="${4:-0.36}"
FADE=$(( DUR - 1.4 ))
mkdir -p assets/build
FX=assets/build/fx.wav
[[ -f $FX ]] || { echo "Falta $FX: correr make_fx.py primero"; exit 1; }
ffmpeg -v error -y -i "$VOICE" -t "$DUR" -i "$SONG" -i "$FX" -filter_complex "
[0:a]aresample=44100,aformat=channel_layouts=stereo,highpass=f=80,acompressor=threshold=-24dB:ratio=3:attack=8:release=120:makeup=4dB,loudnorm=I=-15.5:TP=-2:LRA=7:linear=false,aresample=44100,asplit=3[voice][key][fxkey];
[fxkey]apad[fxk];
[2:a][fxk]sidechaincompress=threshold=0.04:ratio=3:attack=4:release=120[fx];
[1:a]aformat=channel_layouts=stereo,volume=$LEVEL,afade=t=out:st=$FADE:d=1.4[bed];
[key]apad[bedk];
[bed][bedk]sidechaincompress=threshold=0.02:ratio=6:attack=12:release=280[music];
[voice][music][fx]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.84:level=false,aresample=48000[mix]" \
  -map '[mix]' -t "$DUR" -c:a aac -b:a 256k assets/mix.m4a || exit 1
ffmpeg -nostats -i assets/mix.m4a -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2
