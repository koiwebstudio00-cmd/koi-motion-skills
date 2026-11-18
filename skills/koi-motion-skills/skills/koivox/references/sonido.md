# Sonido de Koivox

Ajustes de Tomás sobre la v02 de Cubiko 01. Pisan lo que dice `koi-base` para este formato.

## Efectos

- **Origen:** solo el **SJC SFX Pack Vol. 1** (`Kointenido/4-Produccion/motion-graphics-ia/SJC SFX Pack Vol 1 (Giveaway)`). Licencia libre para uso comercial, en `LICENSE.txt` del pack.
- **No usar** los SFX-premium (Epidemic + pack propio) que usa `koi-base`.
- `prep_sfx.sh` los convierte y los nombra:

| Tipo | Archivos del pack | Cuándo suena |
|---|---|---|
| `key-*` | Text Keyboard Short, Click Soft, Click Woodblock | Cada palabra que aparece, trazos, clics del cursor |
| `pop-*` | Tile Paper Tiles, Film Camera Handling, Pop Soft, Bubble Round | Stickers que caen, tiras, sellos, burbujas |
| `whoosh-*` | Whoosh Paper Fast, Fast Swish, Light Air, Airy Flutter | Paneos, whip, pantallas que entran, push through |

`make_fx.py` nunca repite el mismo archivo dos veces seguidas.

## Mezcla

| | koi-base | Koivox |
|---|---|---|
| La voz baja los efectos | Sí (ratio 3) | **No** |
| La voz baja la música | Ratio 6, umbral 0,02 | **Ratio 2, umbral 0,06**, ataque 20 ms, salida 300 ms |
| Nivel `key` / `pop` / `whoosh` | −11 / −10 / −6 dB | **−8 / −6 / −5 dB** |

Resultado medido en Cubiko 01 v02: −14,7 LUFS integrado, pico −0,8 dBFS.

Usar los `make_fx.py` y `make_audio.sh` de esta skill, no los de `koi-base`.
