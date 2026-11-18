#!/bin/zsh
# Copia a assets/sfx/ los efectos de Koivox desde el SJC SFX Pack Vol. 1, con los prefijos que lee make_fx.py.
# Se corre desde la carpeta del proyecto: prep_sfx.sh [carpeta del pack]
# Pedido de Tomás: usar SIEMPRE los de esta carpeta. Los SFX-premium (Epidemic) no van en Koivox.
PACK="${1:-$HOME/Desktop/Kointenido/4-Produccion/motion-graphics-ia/SJC SFX Pack Vol 1 (Giveaway)}"
[[ -d "$PACK" ]] || { echo "No encuentro el pack en $PACK"; exit 1; }
U="$PACK/UI & Motion"; C="$PACK/Camera"
mkdir -p assets/sfx
conv() { ffmpeg -v error -y -i "$1" -ac 2 -ar 44100 -b:a 192k "assets/sfx/$2.mp3" || exit 1; }
# key: cada palabra que aparece
conv "$U/Text/SJC_TEXT_Keyboard Short_01.wav" key-a
conv "$U/Text/SJC_TEXT_Keyboard Short_02.wav" key-b
conv "$U/Click/SJC_CLICK_Soft Click_01.wav" key-c
conv "$U/Click/SJC_CLICK_Soft Click_02.wav" key-d
conv "$U/Click/SJC_CLICK_Soft Click_03.wav" key-e
conv "$U/Click/SJC_CLICK_Woodblock_01.wav" key-f
conv "$U/Click/SJC_CLICK_Woodblock_02.wav" key-g
# pop: stickers que caen, tiras, sellos
conv "$U/Tile/SJC_TILE_Paper Tiles_01.wav" pop-a
conv "$C/Film Camera/SJC_FILMCAMERA_Handling_01.wav" pop-b
conv "$C/Film Camera/SJC_FILMCAMERA_Handling_02.wav" pop-c
conv "$C/Film Camera/SJC_FILMCAMERA_Handling_03.wav" pop-d
conv "$U/Pop/SJC_POP_PopUp Soft_01.wav" pop-e
conv "$U/Pop/SJC_POP_PopUp Soft_02.wav" pop-f
conv "$U/Pop/SJC_POP_Bubble Round_01.wav" pop-g
# whoosh: paneos, whip, pantallas que entran
conv "$U/Whoosh/SJC_WHOOSH_Paper Fast_01.wav" whoosh-a
conv "$U/Whoosh/SJC_WHOOSH_Paper Fast_02.wav" whoosh-b
conv "$U/Whoosh/SJC_WHOOSH_Fast Swish_01.wav" whoosh-c
conv "$U/Whoosh/SJC_WHOOSH_Fast Swish_02.wav" whoosh-d
conv "$U/Whoosh/SJC_WHOOSH_Light Air_01.wav" whoosh-e
conv "$U/Whoosh/SJC_WHOOSH_Airy Flutter_01.wav" whoosh-f
printf 'Todos los efectos: SJC SFX Pack Vol. 1 (Sam John Creates). Licencia en LICENSE.txt del pack.\n' > assets/sfx/CREDITOS.txt
ls assets/sfx | wc -l
