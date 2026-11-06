---
name: koi-base
description: Reglas comunes de todos los videos de Koi Studio - marca, tipografía, color, movimiento, sonido, contenido, CTA y flujo de trabajo con HyperFrames. Usala siempre que se haga, edite o revise un video de Koi, Zyro, Toki o Cubiko, aunque no se pida explícitamente, y cargala junto con la skill del formato (koi-reel-talking-head, koi-reel-explainer, koi-vsl-continua). También para guiones de video, storyboards y pedidos de imágenes a Codex.
---

# Base Koi

Reúne lo que vale para cualquier video. Cada formato tiene su propia skill y puede pisar estas reglas solo donde lo indique.

**Prioridad cuando dos reglas chocan:** archivos originales del logo > manual de marca > decisión más reciente de dirección > estas guías > referencias. De las referencias se aprende el método de edición, nunca la identidad de otra persona o marca.

## Herramientas

Requisitos: HyperFrames 0.9.10 (`npx hyperframes`), FFmpeg, Python con numpy y Whisper. Se apoya en las skills `hyperframes`, `hyperframes-cli`, `hyperframes-registry` y `media-use`, que se instalan desde `heygen-com/hyperframes`.

Whisper conviene tenerlo en un entorno aislado, por ejemplo `~/.venvs/whisper`.

Scripts en `scripts/`. Copiarlos a `tools/` del proyecto y correrlos desde la carpeta del proyecto:

| Script | Para qué sirve |
|---|---|
| `hf_base.py` | Ayudantes para generar escenas de HyperFrames desde Python |
| `align.py` | Le da un tiempo a cada palabra del guion a partir de la voz |
| `make_bg.py` | Crea los fondos de marca, planos o con grano |
| `make_fx.py` | Coloca efectos sin repetir el mismo archivo seguido |
| `make_audio.sh` | Mezcla voz, música y efectos |
| `render.sh` | Exporta con motion blur real |

## Flujo de trabajo

1. **Leer las reglas.** Cargar esta skill y la del formato antes de editar.
2. **Revisar el guion contra la realidad.** Si promete una función de un producto, confirmarla en el código del producto antes de mostrarla. Si no existe, avisar.
3. **Pedir todos los assets antes de editar.** Hacer la lista de lo que falta, con nombres exactos. Si hay imágenes, dejar el pedido listo para pegar en Codex ([references/pedido-codex.md](references/pedido-codex.md)).
4. **Mostrar un storyboard** y esperar la aprobación antes de renderizar. Evita perder horas de exportación.
5. **Construir** con un `tools/build.py` que genera todo el proyecto. Los tiempos salen de la voz, no se ajustan a mano.
6. **Vista previa corta y en baja resolución.** Revisar cuadros con `npx hyperframes check` y `snapshot`.
7. **Render final** con `render.sh`, con otras apps cerradas. Si faltan fuentes o imágenes, frenar: no exportar con reemplazos.
8. **Comprobar la salida:** duración, volumen de −14 LUFS, color bt709 y que la voz se entienda. Pasar Whisper sobre la mezcla final ayuda a detectar palabras tapadas.

Explicar cada paso en español simple, sin términos técnicos sin aclarar, y avisar antes de cualquier cosa que pida una contraseña.

## Carpetas del proyecto

- `Raw footage/`: solo video. Voces en `Raw footage/Assets/Explainers/`, música en `Raw footage/Assets/Musica/`.
- `Reference/`: videos de referencia.
- `Export/`: másters finales.
- Cada video es una carpeta propia con `index.html`, `compositions/`, `assets/` y `tools/`.

## Lo mínimo que no se negocia

- **Sin logo** en piezas de contenido de Koi. Los videos institucionales pueden llevarlo, usando el archivo original sin modificar.
- **Sin rótulos** como "Ejemplo ilustrativo" o "Ejemplo con datos ficticios". Los datos sensibles se cambian igual.
- **CTA:** "Escribinos [PRODUCTO] por WhatsApp y probalo GRATIS", con GRATIS en mayúsculas. La palabra clave permite saber de qué pieza llega cada conversación. No inventar duración ni condiciones de la prueba.
- **Sin cifras, testimonios ni integraciones inventadas.**
- **Curvas con entrada y salida suaves y motion blur siempre.**
- **Un solo acento de color:** naranja `#FA5D00`.
- **Música y efectos con licencia libre.**

## Guías detalladas

Leer según la tarea:

- [references/marca.md](references/marca.md): tipografía, color, logo, fondos y correcciones de color.
- [references/movimiento-y-sonido.md](references/movimiento-y-sonido.md): curvas, zooms, listas con cámara, subtítulos, efectos, música y render.
- [references/contenido.md](references/contenido.md): voz de marca, storytelling, hook, estructura y guiones para ElevenLabs.
- [references/pedido-codex.md](references/pedido-codex.md): plantilla para pedir imágenes de vidrio.
