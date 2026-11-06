---
name: koi-vsl-continua
description: Crea videos horizontales 16:9 de un solo plano continuo, donde una forma se transforma en todo sin cortes y todos los tiempos salen de la voz. Usala para VSL, videos de la web, videos institucionales de Koi Studio, motion continuo, "sin cortes" o cuando un punto deba volverse línea, tarjeta o interfaz. Cargá también koi-base.
---

# VSL de plano continuo

Formato: 1920 × 1080, 30 fps. Una sola composición, sin escenas: una forma sobrevive todo el video y cambia de función. Cargar antes `koi-base`.

Por ser institucional puede llevar isotipo, usando el archivo original. Tampoco lleva rótulos.

## La idea

Un punto se vuelve línea, la línea un cuadrado que es el tablero, y así. La técnica sale de referencias de motion continuo: se copian los principios, nunca marcas ni personajes.

Antes de animar, escribir la cadena completa de transformaciones. Ejemplo:

`punto > burbuja > contador > línea > teléfono > ícono > línea > tarjeta > puerta > foto > botón`

## Recursos

- **Punto que crece** hasta llenar el cuadro y se vuelve el fondo nuevo; adentro nace otro punto chico.
- **Forma aplastada a línea finita:** mientras está plana se cambia el contenido.
- **División como célula:** una forma se parte con un puente.
- **Línea que se ramifica** para separar temas.
- **Letras que llegan** desde puntos dispersos y se asientan.
- **Texto que sale aplastado.**
- **Rebote al aterrizar** (`back.out(1.7)`), la excepción a las curvas suaves.
- **Cámara en rampa** (`expo.inOut`) y desenfoque de movimiento fuerte.
- **Respiración lenta** de todo el cuadro: nada queda quieto.

## Pasos

1. **Guion.** Arrancar por el dolor común y separar por rubro o caso recién después. Guardarlo en `VOZ-ELEVENLABS.txt`.
2. **Storyboard** con la cadena de transformaciones. Esperar la aprobación.
3. **Tiempos desde la voz:**
   ```bash
   ~/.venvs/whisper/bin/python tools/align.py voz.mp3 VOZ-ELEVENLABS.txt
   ```
   Se puede usar una voz de prueba para los borradores.
4. **Anclas.** En `tools/build.py`, buscar cada momento por una frase del guion en vez de escribir segundos. Así, cambiar la voz resincroniza todo el video:
   ```python
   A = {}
   for key, phrase in [("mensaje", "un mensaje"), ("koi", "En KOI")]:
       i, _ = locate(phrase)
       A[key] = WORDS[i]["s"]
   ```
   `locate()` busca solo hacia adelante y falla si la frase no está. Si cambia el guion, actualizar las frases ancla. Copiarla de [references/anclas.py](references/anclas.py).
5. **Construir.** Usar `hf.setup(1920, 1080, end=fin)`, una forma con ID fijo (`#B`) y dos capas: el mundo, que se mueve con la cámara, y el HUD, fijo a la pantalla.
6. **Borrador** con `render.sh borrador.mp4 120`.
7. **Final** con `render.sh salida.mp4 180`. A 240 fps un video largo puede pedir más de 26 GB temporales.

## Antes de renderizar

- [ ] No hay ningún corte: cada forma nace de la anterior.
- [ ] Todos los tiempos salen de frases ancla.
- [ ] La cámara se mueve con rampa y nada queda quieto.
- [ ] Con la voz final se volvieron a correr `align.py` y el render.
