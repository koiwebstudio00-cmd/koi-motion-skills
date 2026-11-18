# Pedido de stickers para Codex

Copiar en `PEDIDO-CODEX.md`, completar y pasarlo a Codex. Después frenar hasta que el usuario avise que las imágenes están listas.

Antes, armar la lista desde el storyboard. Se piden a Codex los **protagonistas**: personajes, objetos con humor y lo que lleva el naranja. Lo genérico (fondos de lugares, texturas, objetos de relleno) puede salir de internet ([assets-online.md](assets-online.md)). Lo que el código resuelve (texto, tiras, formas, trazos, grano) no se pide.

```markdown
# Pedido para Codex: stickers de [VIDEO]

Guardá cada imagen en `[RUTA]/assets/images/` con el nombre exacto de la lista.

## Reglas para todas las imágenes

- PNG con transparencia real (canal alfa). Stickers: 1600 px en el lado mayor. Fondos de escena: 1080 × 1920, sin transparencia.
- No dibujes un tablero de cuadritos ni un fondo blanco que simule transparencia. Si no podés generar alfa real, generá sobre verde plano #00FF00 y avisá.
- Estilo: sticker recortado de foto, como un collage editorial de revista. Grano de película fino y contraste alto.
- Color: tonos naranja Koi. La foto base en grises o sepia cálido, y el sujeto o la parte que marca la lista en naranja Koi #FA5D00, con sombras en naranja oscuro #7A2A00 y luces en durazno #FABF9A. Ningún otro color saturado.
- Recorte limpio, sin borde blanco, sin sombra en el piso y sin halo.
- Un solo sujeto por imagen, completo y con margen. Las personas van de cuerpo entero o de cintura para arriba, con los brazos completos.
- Sin texto, logos, marcas, interfaz de apps ni personas reales o famosas.
- Nunca robots, cerebros ni circuitos.

## Imágenes

| # | Archivo | Sujeto | Qué va en naranja |
|---|---|---|---|
| 1 | `s01-[nombre].png` | [Persona u objeto, pose, qué hace, desde dónde lo vemos] | [Todo el sujeto / solo la remera / solo la pantalla del celular] |
| 2 | `s02-[nombre].png` | [Objeto con humor: un hombre con un buzón en lugar de cabeza] | [El buzón] |
| 3 | `icono-[nombre].png` | [Ícono chico para kv.burst(): notificación, corazón, billete, 400 px] | [Todo] |

Empezá solo con la primera. Cuando se confirme que la transparencia y el tono naranja están bien, generá las demás.
```

## Al recibirlas

- Si alguna vino sobre verde: `ffmpeg -i in.png -vf "colorkey=0x00FF00:0.28:0.08,despill=type=green" out.png`.
- Revisar que el naranja sea el de Koi y no rojo ni amarillo, que no haya otros colores saturados y que los bordes no tengan halo.
- Revisar que no haya manos o brazos que floten ni objetos cortados.
- Todas las personas tienen que mirar o moverse hacia algo que tenga sentido en la escena.
