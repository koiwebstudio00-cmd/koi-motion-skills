# Assets de internet

Sirven para fondos de lugares, objetos de relleno, texturas y fotos de época. Los protagonistas con el naranja se piden a Codex.

## Dónde buscar

| Sitio | Para qué | Licencia |
|---|---|---|
| Unsplash, Pexels | Fotos de lugares, objetos y manos | Uso libre, sin atribución obligatoria |
| Wikimedia Commons | Fotos de época y documentos | Solo los marcados "Public domain" o CC0 |
| Smithsonian Open Access, The Met Open Access, Rawpixel (dominio público) | Grabados, ilustraciones antiguas y objetos | CC0 / dominio público |
| Texturelabs | Papel, grano, polvo y pliegues | Gratis para uso comercial, sin revender las texturas |
| Freesound (CC0), Pixabay | Sonidos de papel, cinta y máquina de escribir | Solo CC0 |

## Reglas

- Cada archivo descargado se anota en `ASSETS.md` con link, autor y licencia.
- Nada con logos, marcas visibles o personas reales reconocibles. Las personas de fotos de stock solo van de espaldas, recortadas o de lejos.
- Las fotos se pasan a tono Koi en el código: `kv.sticker(..., tone="bn")` o `tone="naranja"`.
- Para recortar el fondo de una foto se usa la skill `media-use` (cutouts) o se pide a Codex.
- Descargar a `assets/images/web/` con nombres descriptivos: `web-oficina-ventana.jpg`.
- Antes de bajar, mostrar al usuario la lista con link y licencia.
