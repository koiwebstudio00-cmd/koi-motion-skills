# Entrega en Kointenido

"Subilo al Kointenido" quiere decir copiarlo a la carpeta de contenido del día, con la misma forma que los talking heads.

## Dónde

`~/Desktop/Kointenido/1-Contenido/AAAA-MM/Semana-NN/AAAA-MM-DD-Dia/Koivox/`

- Si no se sabe qué día se publica, usar el día de hoy y decirlo.
- La semana sale de las carpetas que ya existen (Semana-01 = 3 al 9 de noviembre de 2026, y así).
- Al terminar, abrir la carpeta en Finder (`open -R <archivo>`) y dar la ruta escrita desde el Escritorio: Tomás la busca a mano.

## Qué va

| Archivo | Contenido |
|---|---|
| `KVNN-<Producto>-<Titulo>-liviano.mp4` | El máster reexportado liviano (abajo) |
| `Textos/caption.txt` | Gancho, desarrollo corto y CTA "Escribinos <PALABRA> por WhatsApp y probalo GRATIS. Enlace de WhatsApp en la bio." |
| `Textos/guion.txt` | Título, guion completo, textos en pantalla, notas pendientes y ruta del máster |

## Exportar liviano

El grano de papel hace que el máster de `render.sh` pese unos 600 MB por minuto. Para publicar:

```bash
ffmpeg -i Export/borradores/vNN.mp4 -c:v libx264 -preset medium -crf 24 -maxrate 3.5M -bufsize 7M -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 192k -movflags +faststart <destino>-liviano.mp4
```

Queda en unos 27 MB para 70 s. Correrlo en segundo plano y no cortarlo: un mp4 cortado queda sin `moov` y no abre.

## Limpieza de borradores

Solo con el OK de Tomás:

- Las versiones viejas van a la Papelera (`mv` a `~/.Trash`), no se borran del todo.
- El máster vigente se comprime a unos 80 MB y sigue sirviendo para reexportar:

```bash
ffmpeg -i vNN.mp4 -c:v libx264 -preset slow -crf 20 -maxrate 9M -bufsize 18M -pix_fmt yuv420p -c:a copy -movflags +faststart vNN-tmp.mp4 && mv vNN-tmp.mp4 vNN.mp4
```
