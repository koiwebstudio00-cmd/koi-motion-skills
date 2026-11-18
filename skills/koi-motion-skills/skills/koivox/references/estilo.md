# Estilo Koivox

Reglas que salen de [analisis-referencias.md](analisis-referencias.md), ya traducidas a la marca Koi.

## Color

- **Base:** papel `#F2F2F0`, negro `#0B0B0B` y grises.
- **Acento único:** naranja `#FA5D00` en un solo elemento por escena: el sticker protagonista, la palabra clave o la etiqueta.
- **Formas planas:** durazno `#FABF9A` y naranja translúcido (opacidad 0,25–0,4). Reemplazan los verdes y rosas de las referencias.
- **Fotos de internet:** pasar a blanco y negro (`tone="bn"`) o a duotono naranja (`tone="naranja"`).

## Stickers

- **Los de Codex vienen ya en tonos naranja Koi:** base en grises o sepia y el sujeto, o su parte clave, en naranja (como la casa de R2 o el personaje de R1).
- **Borde:** sin borde blanco grueso. El recorte es limpio, con sombra suave hacia abajo.
- **Escala:** el sujeto principal ocupa entre el 40 y el 60 % del ancho.
- **Humor visual:** cabeza reemplazada por un objeto, manos que entregan o empujan cosas, objetos de época mezclados con cosas actuales.

## Capas de una escena

| Orden | Capa | Movimiento típico |
|---|---|---|
| 1 | Fondo: papel, cuadriculado o foto desaturada | Empuje lento, factor 0,3 |
| 2 | Formas: círculo, medio círculo, triángulo, trama, parche cuadriculado | Factor 0,6 |
| 3 | Sticker protagonista | Entra (`drop`, `grow`, `enter`) y tiembla (`boil`), factor 1 |
| 4 | Frente: objeto cercano desenfocado en un borde | Factor 1,6, con `filter: blur(6px)` |
| 5 | Texto: palabras, tiras, etiquetas, trazos | Con la voz |
| 6 | Textura: grano y viñeta | Siempre encima |

## Modo papel o modo fluido

| Usar papel (a saltos) para | Usar fluido (suave + blur) para |
|---|---|
| Collage de stickers | Fotos de lugares, cámara que empuja |
| Entradas: `drop`, `grow`, `slap`, `pop_in`, `enter` | Entradas: `focus_in`, `slide` |
| Cámara lateral: `pan` | Transiciones: `focus_out`, `push_through`, `whip` |
| Loops chicos: `burst`, `boil` | Cambio de foco: `rack` |
| Trazos y etiquetas: `marker`, `label` | Interfaz del producto |

En una misma escena se pueden mezclar: el fondo fotográfico empuja suave y los stickers encima van a saltos.

## Texto

| Uso | Estilo | Función |
|---|---|---|
| Frase del gancho o del giro | Manrope 800, palabra por palabra | `kv.typed()` |
| Palabra clave | Instrument Serif Italic naranja, más grande | `kv.focus_in()` |
| Frase documental | Instrument Serif Italic blanca o negra, entera | `kv.focus_in()` |
| Subtítulo | Caja blanca, Manrope 800 negro, 46 px | `kv.subtitle()` |
| Rótulo | Tira de papel roto negra, papel o naranja | `kv.tira()` + `slap` |
| Señalar algo | Etiqueta naranja con línea | `kv.label()` + `marker` + `slap` |
| Subrayar o tachar | Trazo naranja, siempre arriba del objeto | `kv.stroke()` + `marker` |
| Sello ("ALQUILADA", "VENDIDA") | Naranja con tinta gastada, sobre zona clara | `kv.sello()` + `slap` |
| Placa de pausa | Fondo negro, texto centrado y palabra clave naranja | `.placa` + `typed` |

**Color del texto:** negro sobre papel claro (sumar la clase `tinta` a `.line`), blanco sobre papel negro y fotos oscuras, y la palabra clave siempre en naranja (`serif or`).

**Tamaño escalonado:** en una frase de 3 partes, la última es la más grande ("Entró / una consulta / a las 3 AM").

## Transiciones

Elegir una por cambio de escena y no repetir la misma dos veces seguidas:

1. `focus_out` + `focus_in` (la base).
2. `push_through` en un marco, un celular o una puerta: del otro lado, la escena siguiente.
3. `whip` hacia el costado.
4. Corte seco a `.placa` negra con texto.
5. `pan` a la composición vecina del mismo lienzo.
6. `fly_out` de todos los stickers: el collage se desarma.

## Pasaje historia → producto

1. El collage se desarma con `fly_out`, o se atraviesa con `push_through` la pantalla del celular del sticker.
2. Entra la interfaz Koi en modo fluido. El grano se apaga en 0,3 s.
3. La parte producto sigue `koi-reel-explainer`.
4. El cierre vuelve al papel: la escena del comienzo, ordenada. CTA en una placa negra con la palabra clave en naranja.

## Producto que transforma material

Cuando una función convierte algo en otra cosa (fotos en reel, carrusel e historias), se muestra en un **mockup de celular**: el formulario se achica a un costado, las fotos vuelan al celular con una flecha a mano, y en la pantalla van entrando de costado web, reel (foto que se acerca y corte), carrusel (fotos que se deslizan con puntitos) e historias (barras que se llenan). Una tira negra abajo nombra cada formato con la voz. Ejemplo: escena 9 de `ejemplo-build-cubiko-01.py`.

## Zona segura de Instagram (1080 × 1920)

- Arriba: dejar libres 220 px.
- Abajo: dejar libres 420 px (descripción y botones).
- Derecha: dejar libres 140 px (íconos).
- Textos clave y subtítulos dentro de x 60–940 y y 220–1500.

## Nunca

- Collage plano de una sola imagen cortada en partes.
- Stickers quietos sin temblor.
- Más de un elemento naranja fuerte por escena.
- Los verdes, rosas o amarillos de las referencias.
- Movimiento a saltos en la interfaz del producto.
- Fuentes nuevas: todo va en Manrope e Instrument Serif.
- Personas reales reconocibles, logos de terceros, robots, cerebros o circuitos.
