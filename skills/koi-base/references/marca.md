# Marca

## Tipografía

| Rol | Fuente | Tamaño / interlínea |
|---|---|---|
| Título de escena | Manrope 800 | 64 / 70 px |
| Título de impacto | Manrope 800 | 88 / 92 px |
| Acento dentro de un título | Instrument Serif Italic 400 | 72 / 76 px |
| Texto explicativo | Manrope 400 | 38 / 49 px |
| Etiquetas y numeración | Manrope 600 | 28 / 34 px como mínimo en video |
| CTA | Manrope 800 | 36 / 43 px |
| Subtítulos | Manrope 800 | 62 px |

- Tracking de −0,025 em en títulos Manrope; 0 en texto y serif.
- Instrument Serif solo en una palabra o fragmento por título. Nunca en párrafos ni subtítulos.
- Máximo 3 líneas de título; lo normal son 2.
- Usar archivos de fuente locales en `assets/fonts/`. No simular negrita ni cursiva.
- Fórmula de título: línea sans + palabra clave en serif italic. Ejemplo: `Menos caos.` / *`Más control.`*

Los tamaños están en escala 1080 × 1920. Las palabras gigantes de impacto pueden ser mucho más grandes y salirse del cuadro.

## Color

| Uso | Color |
|---|---|
| Acento único | `#FA5D00` |
| Fondo oscuro | `#0B0B0B` |
| Superficies sobre oscuro | `#222222` |
| Fondo claro | `#F2F2F0` |
| Texto sobre oscuro | `#FFFFFF` |
| Texto sobre claro y sobre naranja | `#000000` |

- Sobre blanco, el naranja va solo en acentos grandes, no en texto chico.
- No crear un color por producto. Se distinguen con etiquetas, lenguaje y objetos del rubro.
- Temas: oscuro por defecto, claro para demostraciones y naranja para portadas y cierres.

## Fondos

- **Reels con persona:** color plano (negro, blanco o naranja) con grid fino de 120 px y líneas de 1 px. Blanco al 18 % sobre negro y negro al 12 % sobre blanco y naranja.
- **Explainers y VSL:** grainy fade + grid. Esta combinación fue pedida por dirección y pisa la regla de "grano o grid, nunca los dos".

Generarlos con `make_bg.py`.

## Imágenes e interfaz

- Pocas imágenes generadas: primero interfaz propia, sobria y sin estética de IA genérica.
- Pedir a Codex solo los objetos que la interfaz no resuelve, y mostrar la lista antes de arrancar.
- Objetos del rubro: llaves, vehículos, tickets, consultas, pedidos.
- Nunca robots, cerebros ni circuitos para representar a la IA.
- Burbujas de chat en liquid glass con colores de Koi. No imitar la interfaz de WhatsApp.
- Fotos de propiedades: reales, de Unsplash con licencia gratuita, no ilustraciones.
- Capturas de un producto: recrear la interfaz con código y cambiar marca del cliente, nombres, teléfonos, correos, direcciones, precios y fotos.
- Si se muestra algo chico, ampliar el detalle en vez de mostrar el panel entero.

## Formas grises de fondo

En fondos blancos y naranjas, solo en pantallas de puro texto: íconos grises desenfocados en diagonal, arriba y abajo. Bien visibles, entrando, flotando y saliendo. Nunca anclados. Se hacen por código.

## Color de la grabación

- Natural y cálido, con sombras levemente azuladas. Sin amarillear la piel ni aplastar los negros.
- Se aplica solo a la grabación, nunca a gráficos ni fondos de marca.
- Revisar si el clip es HDR (`color_transfer=arib-std-b67`). Si lo es, convertirlo antes o se ve lavado.
- Al convertir HDR con `-vf`, cerrar con `setparams` en bt709; si no, el archivo sigue marcado como HDR.
