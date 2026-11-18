---
name: koi-recorrido-inmobiliario
description: Edita recorridos verticales de propiedades para inmobiliarias - seguimiento de persona, rampas de velocidad, cortes a la música, texto detrás del sujeto y títulos 3D pegados al piso o la pared. Usala cuando haya tomas de una casa o departamento, un video de propiedad, real estate, tour o recorrido, aunque no lo pidan con esas palabras. Sirve también para guiar cómo grabar. Estado - versión de prueba, sin aprobación final de estilo.
---

# Recorrido inmobiliario

Formato: 1080 × 1920, 30 fps, de 25 a 45 s con cierre. Cuando el proyecto es para un cliente, la marca del cliente reemplaza a la de Koi: de `koi-base` se heredan solo movimiento y sonido.

Antes de editar, leer `references/clientes/<cliente>.md` si existe. Si no, pedir el manual de marca y completar [references/plantilla-cliente.md](references/plantilla-cliente.md). Esa carpeta no se sube al repositorio.

Mostrar el storyboard antes de renderizar.

## Fórmula

- **Ritmo:** una toma nueva cada 1,4 s, voz casi constante (unas 2 palabras por segundo), música debajo y la persona como ancla cada 8 a 12 s.
- **Estructura:** gancho con persona > recorrido por ambientes > dato clave > cierre.
- **Cortes:** siempre sobre el pulso de la música, cada 2 o 4 pulsos.
- **Títulos 3D:** uno por ambiente como máximo, apoyado en piso o pared. El resto son títulos detrás del sujeto y texto chico.
- **Subtítulos:** siempre.
- **Inmueble:** corregir solo luz y encuadre. No alterarlo ni simular noche.
- **Música:** con licencia para uso comercial.

## Técnicas

1. **Seguimiento de la persona:** la cámara retrocede, baja y centrada, y la persona avanza. Es una toma real con gimbal.
2. **Texto detrás del sujeto:** título enorme arriba del pecho, tapado por cabeza y hombros.
3. **Títulos anclados:** pegados a fachada, techo o jardín, y se mueven con la cámara.
4. **Volumen 3D:** laterales apilados y sombra sobre lo que está debajo.
5. **Rampas de velocidad:** cada toma va casi quieta y acelera de golpe, entre 5 y 10 veces, para pasar a la siguiente.
6. **Transiciones:** zoom radial de 4 a 8 cuadros, paneos rápidos o puertas que tapan el corte.
7. **Palabra por palabra:** títulos apilados al ritmo de la voz, en tres tamaños, que salen con fundido o desenfoque.
8. **Texto chico en B-roll:** una o dos palabras al centro.
9. **Lente angular y cámara baja:** agrandan ambientes.
10. **Color:** bajar altas luces, recuperar cielo, unificar interiores cálidos y viñeteado suave.

## Pasos

1. Pedir clips originales: WhatsApp los baja a 464 × 832 y quedan blandos.
2. Medir el tempo de la música.
3. Copiar `scripts/make_base.py` y `scripts/ejemplo-shots.json`. Definir las tomas en pulsos.
4. Revisar un cuadro por toma:
   ```bash
   python tools/make_base.py --stills carpeta-de-prueba
   ```
5. Armar la base. Las rampas promedian cuadros reales, así la velocidad genera motion blur verdadero.
6. Recortar a la persona con `npx hyperframes remove-background` y armar `cutout.webm` con el mismo color y rampa de la base.
7. Sumar textos, subtítulos y cierre en HyperFrames.
8. Audio y render con los scripts de `koi-base`.

Para probar una sola toma, agregar su nombre: `python tools/make_base.py --stills carpeta-de-prueba frente`.

El título necesita textura: una pared lisa sin detalles no se puede seguir.

## Guía para grabar

Compartirla antes de la grabación: [references/guia-grabacion.md](references/guia-grabacion.md).
