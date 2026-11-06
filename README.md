# Koi Motion Skills

Skills de Claude Code para producir videos de Koi Studio con HyperFrames. Reúnen las reglas, técnicas y scripts aprendidos en producción.

## Skills

| Skill | Para qué sirve | Estado |
|---|---|---|
| `koi-base` | Marca, movimiento, sonido, contenido, flujo y scripts comunes | Aprobada |
| `koi-reel-talking-head` | Reels con persona: ojeras, recorte, títulos detrás y carrusel orbital | Aprobada |
| `koi-reel-explainer` | Reels sin filmar: storytelling, texto cinético e interfaz propia | Aprobada |
| `koi-vsl-continua` | Video 16:9 de un solo plano, sincronizado con la voz | En uso |
| `koi-recorrido-inmobiliario` | Propiedades: rampas, cortes a la música y títulos 3D | Prueba |

`koi-base` se carga junto con las demás. En los recorridos para clientes, la marca del cliente reemplaza a la de Koi.

## Instalación

Copiar las carpetas de `skills/` a `.claude/skills/` del proyecto de video, o a `~/.claude/skills/` para usarlas en todos los proyectos.

```bash
git clone https://github.com/koiwebstudio00-cmd/koi-motion-skills.git
```

```bash
cp -R koi-motion-skills/skills/* ~/.claude/skills/
```

## Requisitos

- [HyperFrames](https://github.com/heygen-com/hyperframes) 0.9.10 y sus skills
- FFmpeg
- Node.js
- Python con numpy
- Whisper y PyTorch, para sincronizar la voz y colorear talking heads
- `opencv-python` y Pillow, para los recorridos inmobiliarios
- Manrope e Instrument Serif en `assets/fonts/` de cada proyecto

## Qué no está en este repositorio

- Videos, voces, música ni efectos. La música y los efectos deben tener licencia para su uso.
- Fuentes, logos ni imágenes.
- Manuales de marca y datos de clientes: van en `references/clientes/`, que Git ignora.
