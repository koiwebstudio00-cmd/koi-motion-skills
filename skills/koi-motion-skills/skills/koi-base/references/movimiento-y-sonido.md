# Movimiento y sonido

## Movimiento

- **Curvas:** siempre con entrada y salida suaves (`power3.inOut`, `sine.inOut`). Nunca solo `in` u `out`. La excepción es el rebote al aterrizar del plano continuo.
- **Duración:** entradas de 0,5 a 0,8 s con curvas largas.
- **Nada quieto:** cada escena sigue derivando lento hasta salir. Algo tiene que cambiar cada 1 a 2 s.
- **Sincronía:** cada gráfico aparece cuando se nombra, con la palabra, no antes.
- **Zooms:** acercar y alejar seguido, también en la persona.
- **Pasadas:** zoom que atraviesa, desenfoque y fundidos de luz naranja, en vez de corte directo.
- **Tipografía protagonista:** una palabra gigante en Instrument Serif Italic, que puede salirse del encuadre o quedar detrás de un objeto.
- **Pantalla nunca vacía:** si termina un gráfico, entra otro.
- **Una dirección por pieza:** un recurso principal y uno de apoyo. El glow va solo en el elemento activo.

## Listas con cámara

Cuando la voz nombra varios elementos, presentarlos rápido y viajar de uno a otro. Evitar elementos que aparecen y quedan quietos.

1. Armar la lista en un lienzo más grande que el cuadro.
2. Mover una cámara virtual con `hf.cam()` y curva `expo.inOut`: casi quieta en cada elemento, muy rápida entre ellos.
3. Llegar a cada elemento justo cuando se nombra.

## Patrones de gráficos

1. **Marco que vuelve:** un esquema central reaparece antes de cada paso, con el paso nuevo encendido.
2. **Documento:** tarjeta con líneas que se resaltan al nombrarse.
3. **Comparación:** dos tarjetas, antes y después.
4. **Lista que se llena:** los ítems aparecen al ritmo de la voz.
5. **Teléfono o interfaz:** muestra el producto funcionando.
6. **Palabra anotada:** palabra clave con una flecha dibujada a mano.

## Subtítulos

- Una palabra por vez, a veces 2 o 3 si son muy cortas.
- Cambian exactamente al empezar cada palabra, sin animación.
- Blancos con sombra negra suave; negros sobre fondo claro.
- Centrados a la altura del pecho, nunca sobre la boca. Sin resaltado: el énfasis lo dan los títulos.

## Sonido

| Dato | Valor |
|---|---|
| Volumen final | −14 LUFS integrados, 3 LU de rango |
| Voz | Protagonista, comprimida y limpia |
| Música | `volume=0.36` con ducking de ratio 6 |
| Pasadas | Whoosh en cada una |
| Elementos | Pop o tic en cada uno |
| Textos | Sonido de teclado en cada texto que aparece |
| Momentos fuertes | Risers que llevan a ellos y golpes en graves |

- **Nunca el mismo archivo dos veces seguidas**, mirando todos los tipos juntos. `make_fx.py` lo comprueba y frena si pasa. Conseguir varias tomas CC0 de cada tipo antes de editar.
- Los golpes no van fuertes sobre una palabra: lo primero es entender la voz.
- Música y efectos bajan solos cuando se habla. Rellenar con `apad` la señal de la voz, o música y efectos se cortan cuando termina; `make_audio.sh` ya lo hace.
- 0.36 es un punto de partida. Con otra canción, igualar el volumen percibido en vez de copiar el número.

## Ritmo

- No acelerar la voz: el ritmo se logra quitando pausas y repeticiones.
- Pausa máxima de 0,35 s.
- Primer cambio de pantalla entre los 3 y 5 s.
- Mantener el cierre al menos 2 s en pantalla.

## Render y motion blur

El motion blur es obligatorio y se logra renderizando muchos cuadros y mezclándolos a 30. El blur propio de HyperFrames no actúa dentro de las sub-composiciones, por eso va apagado.

| Calidad | Comando | Uso |
|---|---|---|
| Ideal | `render.sh salida.mp4 240` | Reels cortos |
| Media | `render.sh salida.mp4 180` | Videos largos: 240 puede pedir más de 26 GB temporales |
| Liviana | `render.sh salida.mp4 120` | Poco disco o borradores |

En una Mac de 8 GB, cerrar otras apps antes de exportar.
