# Estudio de referencias

Si se mira por arriba, se copia mal. El look sale de recorrer cada reel cuadro por cuadro.

## Cómo correrlo

Requisitos: `ffmpeg` y, para bajar links, `yt-dlp` (`brew install yt-dlp`). Desde la carpeta del proyecto:

```bash
study_refs.sh "https://www.instagram.com/reel/..." vox-01
study_refs.sh Reference/mi-video.mp4 vox-02
```

Por cada reel deja en `Reference/estudio/<nombre>/`:

- `frames/`: un cuadro cada 0,25 s, a 540 px de ancho.
- `hojas/hoja-0001.jpg`: un segundo por hoja, con 4 cuadros en grilla de 2 × 2. La hoja N muestra del segundo N−1 al N, en orden de lectura.
- `cortes.txt`: segundos donde cambia el plano.
- `audio.wav`: para escuchar ritmo y efectos con Whisper si hace falta.

## Qué anotar

Leer **todas** las hojas, no una muestra. Después sumar a `analisis-referencias.md` de esta skill una fila nueva en la tabla y lo que aporte, con:

1. **Ritmo:** cortes por segundo (sale de `cortes.txt`) y cuánto dura cada plano.
2. **Movimiento:** cuántas poses por segundo tienen los recortes. Se cuentan los cuadros en que no se mueven. ¿Hay cámara que empuja? ¿Las capas se separan?
3. **Entradas:** caen, se deslizan, aparecen de golpe. Si hay rebote, cuántas poses dura.
4. **Recortes:** grosor del borde, sombra (dura o suave y hacia dónde), si son color o blanco y negro, y si tienen trama.
5. **Texturas:** papel, grano, pliegues, cinta, manchas.
6. **Texto:** dónde se ubica, cómo entra y si va sobre tiras o etiquetas.
7. **Transiciones** entre escenas.
8. **Qué NO copiar:** logos, tipografías propias de la otra marca, personajes y frases.

Cerrar con una tabla de **"Vox → Koi"**: cada recurso observado y cómo se traduce con la marca Koi.

## Si una escena no se parece

Sacar una captura del borrador y ponerla al lado del cuadro de referencia. Preguntar: ¿qué cambia?, ¿qué falta? Hay que mirar cuadros sueltos y describir el movimiento con palabras, porque los cuadros no lo muestran.

## Tutoriales

Si un tutorial trae los archivos del proyecto (After Effects u otro), leerlos: dicen valores exactos de sombras, tiempos y capas. Después anotar qué se puede usar de verdad en HyperFrames.
