---
name: koi-reel-talking-head
description: Edita reels verticales con una persona hablando a cámara para Koi Studio - color y ojeras, recorte del sujeto, títulos detrás de la persona, carrusel orbital de cards, pantalla dividida y brolls. Usala siempre que haya un clip grabado de alguien hablando a cámara, un "talking head" o un reel con persona, incluso si solo piden "editá este video". Cargá también koi-base.
---

# Reel talking head

Formato: 1080 × 1920, 30 fps, 60 a 120 s (puede ser más corto si el guion lo pide). Cargar antes `koi-base`.

## Dirección de estilo

Fondos planos con grid, imágenes de vidrio, palabras gigantes, zooms, curvas suaves, motion blur y muchos efectos. No cambiar el fondo real detrás de la persona: el recorte sirve solo para poner texto detrás y delante.

## Pantallas

**A. Pantalla dividida** (la principal, cerca de 2 de cada 3 momentos)
- Gráficos de `y 0` a `y 1250`.
- Panel de la persona desde `y 1404` hasta abajo, con márgenes de 68 px y esquinas superiores de 28 px.
- Subtítulo centrado en `y 1287`, título arriba en `y 180`, ancho máximo de texto de 856 px.

**B. Plano completo** (énfasis, de 1 a 4 s)
- Cara en el tercio superior y subtítulo cerca de `y 1257`.
- Si el fondo es claro y con dibujo, subir el subtítulo a `y 1080`, sobre la ropa oscura.
- Reencuadre lento del 100 % al 105 %.

**C. Gráfico completo:** solo para el marco general o un resumen.

Para explicar, bajar a la persona al panel con motion graphics arriba.

## Pasos

1. Transcribir con `align.py` de `koi-base`.
2. Quitar silencios y repeticiones. No acelerar la voz.
3. Si el clip es HDR, crear el LUT:
   ```bash
   python scripts/make_hlg_lut.py assets/build/hlg709.cube
   ```
4. Colorear y suavizar ojeras con `scripts/grade.py`. Probar primero sobre un cuadro con `--test`. No marcar las ojeras: si se notan más, bajar `STRENGTH`.
5. Crear el recorte de la persona:
   ```bash
   npx hyperframes remove-background assets/base.mp4 -o assets/cutout.webm
   ```
6. Armar `tools/build.py` con estas capas, de abajo hacia arriba:
   1. Grabación (`base.mp4`)
   2. Fondos
   3. Títulos detrás y cards traseras
   4. Persona recortada (`cutout.webm`, `z-index: 4`)
   5. Cards delanteras
   6. Subtítulos
7. Audio y render con los scripts de `koi-base`.

## Recursos propios

**Títulos detrás del sujeto:** palabra enorme arriba del pecho, con sombra para que tenga contraste. Se tapan letras sin miedo porque la voz completa la lectura.

**Carrusel orbital:** cards que giran alrededor de la persona. `scripts/orbit.py` calcula las posiciones como keyframes, para que cada cuadro sea exacto, y genera dos capas: una detrás del recorte, desenfocada, y otra delante. La card del frente cambia cuando la voz nombra la siguiente.

```python
import orbit
cards = [("1", "¿Quién se hace cargo?"), ("2", "¿Qué pasa después?"), ("3", "¿Dónde queda lo hablado?")]
giros = [(6.6, 7.4), (10.3, 11.1)]
hosts = [orbit.layer(hf, "back", False, cards, 2.9, 13.8, giros), orbit.layer(hf, "front", True, cards, 2.9, 13.8, giros)]
```

Montar `back` debajo del recorte y `front` encima, ajustando el `z-index` de cada una en `index.html`.

`hyperframes check` marca `text_occluded` cuando una card pasa detrás de otra. En el carrusel es el efecto buscado, no un error.

## Antes de renderizar

- [ ] Las ojeras se ven naturales.
- [ ] Ningún título tapa la boca.
- [ ] El recorte no tiembla en bordes ni en pelo.
- [ ] Las cards pasan por detrás sin saltos.
