# Carrusel orbital de cards que pasa delante y detrás de la persona.
# Las posiciones se calculan acá y se escriben como keyframes para que cada cuadro sea exacto.
# El carrusel se genera dos veces: una capa debajo del recorte y otra encima.
#
#   import orbit
#   back = orbit.layer(hf, "back", False, cards, start=2.9, end=13.8, changes=[(6.6, 7.4), (10.3, 11.1)])
#   front = orbit.layer(hf, "front", True, cards, start=2.9, end=13.8, changes=[(6.6, 7.4), (10.3, 11.1)])
#
# cards: lista de (numero, texto). changes: tramos donde gira para traer la card siguiente al frente.
import math

FPS = 30
CARD_CSS = """
.lg { position: absolute; font-weight: 800; color: #000; overflow: hidden; }
.lg::before { content: ""; position: absolute; left: 4%; right: 4%; top: 6px; height: 44%; border-radius: 40px 40px 90px 90px; background: linear-gradient(180deg, rgba(255,255,255,.66), rgba(255,255,255,0)); }
.lg::after { content: ""; position: absolute; inset: 0; border-radius: inherit; box-shadow: inset 0 2px 2px rgba(255,255,255,.95), inset 0 -3px 6px rgba(255,255,255,.4), inset 0 -22px 34px rgba(255,255,255,.2); }
.lg.lw { background: linear-gradient(145deg, rgba(255,255,255,.88), rgba(255,255,255,.58)); border: 2px solid rgba(255,255,255,.9); box-shadow: 0 24px 50px rgba(40,20,5,.3); backdrop-filter: blur(20px) saturate(1.4); }
.card { position: absolute; left: 200px; top: 1120px; width: 680px; height: 340px; border-radius: 56px; padding: 36px 40px 0 136px; font-size: 46px; line-height: 56px; letter-spacing: -0.02em; will-change: transform; }
.card b { position: absolute; left: 34px; top: 40px; width: 78px; height: 78px; border-radius: 50%; background: #FA5D00; text-align: center; font-size: 44px; line-height: 78px; z-index: 1; }
.card span { position: relative; z-index: 1; }
"""


def smooth(p):
    return p * p * (3 - 2 * p)


def clamp(p):
    return min(max(p, 0), 1)


def spin(t, changes, step):
    rot = 0.0
    for start, end in changes:
        p = clamp((t - start) / (end - start))
        rot += step * p * p * p * (p * (6 * p - 15) + 10)
    return rot + 3.5 * math.sin(t * 1.1)


def frames(card, total, start, end, changes):
    keys, states = [], []
    t, dt = start, 1 / FPS
    gap = 360 / total
    while t < end:
        grow = smooth(clamp((t - start - 0.1) / 0.6))
        leave = smooth(clamp((t - end + 1.18) / 0.6))
        angle = math.radians(card * gap + spin(t, changes, -gap) + 300 * leave)
        depth = math.cos(angle)
        radius = 470 * (0.55 + 0.45 * grow) * (1 + 0.5 * leave)
        x = radius * math.sin(angle)
        y = -150 * (1 - depth) / 2
        scale = (0.56 + 0.44 * (1 + depth) / 2) * (0.5 + 0.5 * grow)
        keys.append(f"{{x:{x:.1f},y:{y:.1f},scale:{scale:.4f},duration:{dt:.5f},ease:'none'}}")
        states.append((round(t, 4), depth >= 0, grow * (1 - leave)))
        t += dt
    return keys, states


def layer(hf, sid, front, cards, start, end, changes):
    """Devuelve la escena de HyperFrames de una de las dos capas."""
    hf.OFFSET = start
    body, js = "", ""
    for i, (num, text) in enumerate(cards):
        cid = f"{sid}{i}"
        body += f'<div id="{cid}" class="card lg lw"><b>{num}</b><span>{text}</span></div>'
        keys, states = frames(i, len(cards), start, end, changes)
        js += f'tl.to("#{cid}", {{keyframes:[{",".join(keys)}]}}, 0);\n'
        js += f'tl.set("#{cid}", {{opacity:0}}, 0);\n'
        last = 0
        for when, is_front, alpha in states[::2]:
            value = round(alpha, 2) if is_front == front else 0
            if value != last:
                js += f'tl.set("#{cid}", {{opacity:{value}}}, {round(when - start, 3)});\n'
                last = value
    css = CARD_CSS + (".card { filter: blur(2px); }" if not front else "")
    scene = hf.scene(sid, start, end + 0.1, css, body, js)
    hf.OFFSET = 0
    return scene
