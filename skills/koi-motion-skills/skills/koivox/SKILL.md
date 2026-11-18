---
name: koivox
description: Koivox - el formato de reels verticales de Koi Studio que cuenta la historia como documental estilo Vox (stickers recortados en tonos naranja Koi, collage de papel, stop-motion a 12 poses por segundo, desenfoques y capas con profundidad) y muestra el producto con la interfaz Koi de siempre. Usala cuando pidan un Koivox, un video "estilo Vox", documental, collage, stickers, recortes, stop-motion o una historia contada con imágenes recortadas, aunque no lo digan con esas palabras. Incluye el análisis de las referencias, el estudio cuadro por cuadro de reels nuevos, el pedido de stickers a Codex y un flujo de revisiones con versiones numeradas. Cargá también koi-base.
---

# Koivox

Formato: 1080 × 1920, 30 fps, entre 45 y 90 s. Cargar antes `koi-base`. Esta skill pisa algunas reglas de `koi-base`, y cada una está marcada como **pisa koi-base**.

**La idea:** la historia (el dolor cotidiano) se cuenta como documental Vox: stickers en tonos naranja Koi sobre papel, collage que se arma de a una pieza, saltos de stop-motion y desenfoques. Cuando entra el producto, el video pasa a la interfaz Koi limpia, con movimiento suave y cursor. El cierre vuelve al collage, ahora ordenado.

Todo sale del análisis de 5 reels de referencia: [references/analisis-referencias.md](references/analisis-referencias.md). Leerlo antes de escribir el guion.

## Scripts

Copiar a `tools/` del proyecto junto a los de `koi-base`, y correrlos desde la carpeta del proyecto. Los de Python necesitan numpy (sirve el Python de `~/.venvs/whisper`).

| Script | Para qué sirve |
|---|---|
| `study_refs.sh` | Baja o toma un reel y lo deja en cuadros cada 0,25 s, hojas de 1 s y cortes |
| `make_paper.py` | Papeles (blanco, negro, naranja, cuadriculado), grano, trama de puntos y parche cuadriculado |
| `koivox.py` | Movimiento en modo papel y modo fluido, stickers, formas, tiras, etiquetas, subtítulos, trazos y sello |
| `prep_sfx.sh` | Copia los efectos del SJC SFX Pack a `assets/sfx/` con los prefijos de `make_fx.py` |
| `make_fx.py` | Igual que el de `koi-base`, con los efectos más fuertes. **Reemplaza** al de `koi-base` |
| `make_audio.sh` | Igual que el de `koi-base`, pero la voz no baja los efectos y baja poco la música. **Reemplaza** al de `koi-base` |

Proyecto completo de ejemplo, aprobado: [references/ejemplo-build-cubiko-01.py](references/ejemplo-build-cubiko-01.py) (Cubiko, "¿Cuánto le pagarías?", 12 escenas). Partir de ahí en vez de escribir el `build.py` de cero.

## Pasos

1. **Referencias nuevas (opcional).** Si el usuario trae más reels, estudiarlos con `study_refs.sh` ([references/estudio-referencias.md](references/estudio-referencias.md)) y sumar lo nuevo a `analisis-referencias.md`.
2. **Brief cerrado** en `BRIEF.md`: historia, reglas de look, lista de "nunca" y duración. Solo lo que el usuario aprobó ([references/revisiones.md](references/revisiones.md)).
3. **Guion** con la columna de las referencias: gancho en 3 s, dato, giro con pregunta, respuesta en 3 y remate. La historia la trae el usuario. Si hay datos, cada uno lleva su fuente en el brief.
4. **Comprobar funciones** del producto en su código, igual que en `koi-reel-explainer`.
5. **Audio primero:** `VOZ-ELEVENLABS.txt`, voz final y música. Si la voz queda larga, se recorta el guion. Después se corre `align.py`.
6. **Storyboard por capas** en `GUION-Y-STORYBOARD.md`: por escena, fondo, formas, sticker, frente, texto, modo (papel o fluido) y transición de salida, más la lista de imágenes con su origen (Codex o internet). Esperar la aprobación.
7. **Imágenes:**
   - **Stickers a Codex** con [references/pedido-codex-stickers.md](references/pedido-codex-stickers.md). **Frenar acá** hasta que el usuario avise que están listos.
   - **Assets de internet** mientras tanto, según [references/assets-online.md](references/assets-online.md).
8. **Texturas y sonidos:** `make_paper.py` (incluye la tinta del sello), fondos de interfaz con `make_bg.py --style grano` y `prep_sfx.sh` para los efectos.
9. **Construir** con `hf_base.py` y `koivox.py`, una composición por escena.
10. **Borrador** con `render.sh Export/borradores/v01.mp4 120`. Revisar, juntar notas en `FIXES.md`, y la versión siguiente cambia solo lo que figura en la lista.
11. **Audio** con `make_fx.py` y `make_audio.sh` de esta skill (no los de `koi-base`). Ver [references/sonido.md](references/sonido.md).
12. **Render final** con `render.sh` a 240.
13. **Entrega en Kointenido** según [references/entrega.md](references/entrega.md): versión liviana, caption y guion en `1-Contenido`, y limpieza de borradores.

## Dirección visual

Detalle completo en [references/estilo.md](references/estilo.md).

- **Stickers en tonos naranja Koi:** base gris o sepia y el sujeto, o una parte clave, en naranja. Borde limpio y sombra suave.
- **Papel:** arrugado, cuadriculado, trama de puntos, cinta y formas planas en durazno y naranja translúcido.
- **Dos modos de movimiento:** **papel** (collage a saltos, 12 poses por segundo) y **fluido** (fotos, cámara, desenfoques y texto documental).
- **Texto:** palabra por palabra con la voz. Palabra clave en Instrument Serif Italic naranja. Frases documentales enteras en serif itálica. Subtítulos en caja blanca.
- **Producto:** interfaz propia de `koi-reel-explainer` (`ui-kit.css`), modo fluido.

## Patrones aprobados

- **Orden de capas:** el texto va siempre arriba del collage, y un trazo (la X, una flecha) va arriba del objeto que marca. `kv.css()` ya lo resuelve; no sacar esas reglas.
- **Sello:** `kv.sello()`, naranja con tinta gastada, sobre una zona clara y nunca sobre una cara. Un cartel liso o negro no se lee.
- **Burbujas de chat sobre papel:** caja blanca o naranja con encabezado chico ("Instagram · 23:07"). Nunca usar la clase `w`: `hf_base` la reserva para las palabras y fuerza todo en una línea.
- **"Creadora de contenido" o cualquier función que transforma material:** mostrar el antes y el después en **un mockup de celular**. Las fotos salen de la interfaz y vuelan al celular, y en la pantalla van pasando web → reel → carrusel → historias, cada una entrando de costado con la voz. Una tira negra abajo nombra el formato. Nada de tarjetas sueltas tiradas. Ver la escena 9 del ejemplo.
- **Fotos de propiedades:** revisar que no se lean carteles ni marcas de otras inmobiliarias.

## Reglas que pisan koi-base

- **Movimiento a saltos** en el modo papel: las curvas suaves se muestrean alternando poses de 2 y 3 cuadros. **Pisa koi-base** ("curvas suaves siempre").
- **Motion blur:** igual se renderiza con `render.sh`. `koivox.py` pone cada pose justo en un cuadro de 30 fps, así que el blur no la ensucia.
- **Imágenes:** acá son protagonistas, entre 20 y 40 por reel. **Pisa koi-base** ("pocas imágenes generadas"). Siguen prohibidos los robots, cerebros y circuitos.
- **Subtítulos en caja blanca** con texto negro, abajo al centro. **Pisa koi-base** ("subtítulos sin resaltado, a la altura del pecho").
- **Efectos solo del SJC SFX Pack Vol. 1** (`prep_sfx.sh`). Los SFX-premium de `koi-base` no van: a Tomás le parecieron "horribles" en este formato. **Pisa koi-base.**
- **Mezcla:** la voz no baja los efectos y baja la música apenas (ratio 2). Efectos más fuertes que en `koi-base`. **Pisa koi-base.**

## Antes de renderizar

- [ ] El gancho tiene imagen y texto antes de la primera palabra.
- [ ] Hay una escena nueva cada 2 a 7 s, y algo cambia cada 0,3 a 0,8 s.
- [ ] Cada escena tiene al menos 3 capas, y el naranja va en un solo elemento por escena.
- [ ] Ningún sticker queda quieto: si no se mueve, tiembla con `kv.boil()`.
- [ ] El grano de papel está encima de todo en el modo papel.
- [ ] Textos y subtítulos dentro de la zona segura de Instagram.
- [ ] Cada asset de internet tiene su licencia anotada en `ASSETS.md`.
- [ ] Cada función mostrada existe y no hay cifras ni testimonios inventados.
- [ ] El CTA usa "probalo GRATIS" y su palabra clave.
- [ ] Textos, X y flechas arriba de los stickers; el sello se lee y no tapa caras.
- [ ] Los efectos son del SJC SFX Pack y se escuchan con la voz encima.
- [ ] La versión nueva es un archivo nuevo: nunca se pisa una anterior.
