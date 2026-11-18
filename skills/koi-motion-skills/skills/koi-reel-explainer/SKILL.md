---
name: koi-reel-explainer
description: Crea reels verticales de Koi Studio solo con voz y motion graphics, sin filmar - storytelling cotidiano, texto cinético, interfaz propia hecha con código, fondos con grano y grid, y listas con zooms en rampa. Usala cuando pidan un explainer, un video sin filmar, un video con voz de ElevenLabs, o explicar un producto como Zyro, Toki o Cubiko con animación. Cargá también koi-base.
---

# Reel explainer

Formato: 1080 × 1920, 30 fps, entre 60 y 100 s. El texto es la imagen. Una idea visual por frase y casi sin cortes. Cargar antes `koi-base`.

## Pasos

1. **Guion con storytelling.** Escena cotidiana con dolor real y humor, y el producto entra cuando el problema ya duele (`koi-base/references/contenido.md`). Una sola historia recorre todo el producto.
2. **Comprobar funciones.** Revisar en el código del producto cada función que se muestra. Copiar etiquetas y estados reales.
3. **Guion para ElevenLabs** en `VOZ-ELEVENLABS.txt`, con etiquetas de ritmo y emoción.
4. **Storyboard** en `GUION-Y-STORYBOARD.md`: texto limpio y tabla de escenas. Esperar la aprobación.
5. **Assets.** Fondos con `make_bg.py --style grano`, efectos CC0 y pedido a Codex solo para objetos que la interfaz no resuelve.
6. **Tiempos.** Correr `align.py` con la voz final.
7. **Construir** con `hf_base.py`, una composición por escena.
8. **Audio y render** con los scripts de `koi-base`.

## Dirección visual

- **Fondos:** grainy fade + grid.
- **Interfaz:** propia, sobria, sin estética de IA genérica. Base en [references/ui-kit.css](references/ui-kit.css).
- **Chats:** burbujas liquid glass con colores de Koi, sin imitar WhatsApp. Mensajes cortos.
- **Objetos:** de vidrio, solo si suman.
- **Formas grises:** solo en pantallas de puro texto, sobre blanco o naranja.
- **Fotos de propiedades:** reales, de Unsplash.
- **Marcas:** en el guion de voz se escriben como se pronuncian; en pantalla, como se escriben.

## Patrones de escena

- **Golpe de texto:** `hf.slam()` para frases cortas de impacto.
- **Palabra por palabra:** `hf.words()` con los tiempos de la voz.
- **Lista con cámara:** lienzo grande y `hf.cam()` con rampa de un elemento a otro. Es el recurso que más dinamismo suma.
- **Interfaz con cursor:** panel `.ui` y cursor `.cur` que hace la acción cuando la voz la nombra.
- **Vuelta a la escena inicial:** mostrar la misma situación del comienzo, ahora resuelta. Da el remate del video.

## Antes de renderizar

- [ ] Cada función mostrada existe.
- [ ] No hay cifras ni testimonios inventados.
- [ ] Ningún elemento queda aparecido y quieto.
- [ ] Cada texto tiene sonido y ningún efecto se repite seguido.
- [ ] El CTA usa "probalo GRATIS" y su palabra clave.
