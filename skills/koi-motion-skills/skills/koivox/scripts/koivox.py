# Ayudantes de Koivox sobre hf_base.py. Copiar a tools/ del proyecto junto a hf_base.py.
#
#   import hf_base as hf, koivox as kv
#   hf.setup(1080, 1920, end=70.0)
#   body = kv.layer("l-fondo", kv.paper("white")) \
#        + kv.layer("l-formas", kv.shape("c1", "circulo", 200, 520, 680)) \
#        + kv.layer("l-sujeto", kv.sticker("ana", "assets/images/s01-ana.png", 240, 620, 600), 2) \
#        + kv.grain_html("g1")
#   js = kv.drop("#ana", 1.2) + kv.boil("#ana-img", 1.7, 6.0) \
#      + kv.parallax([("#l-fondo", 0.3), ("#l-sujeto", 1.0)], 0, 6, dy=-40, ds=0.04) \
#      + kv.grain("#g1", 0, 6)
#   hosts = [hf.scene("s1", 0, 6, kv.css(), body, js)]
#
# Dos modos de movimiento, como en las referencias:
#   PAPEL  (collage): a saltos, alternando poses de 2 y 3 cuadros = 12 poses por segundo.
#                     stop, poses, drop, grow, slap, pop_in, enter, fly_out, boil, parallax, pan, grain, marker, burst, typed.
#   FLUIDO (fotos, cámara, texto documental): curvas suaves con blur.
#                     focus_in, focus_out, rack, push_through, whip, slide.
#
# Estructura de cada sticker: .layer (parallax) > .pos (drop / stop) > img.cut (boil).
# Cada transformación va en un elemento distinto para que no se pisen.
#
# Las poses de PAPEL caen justo en un cuadro de 30 fps. Así render.sh mezcla el motion blur
# dentro de cada cuadro y los saltos quedan nítidos, sin fantasmas entre poses.
import math
import random

import hf_base as hf

STEPS = (2, 3)  # cuadros por pose, alternados: 12 poses por segundo, medido en las referencias
EPS = 0.001  # adelanta cada pose un pelito para que no caiga después del borde del cuadro
ORANGE, PEACH = "#FA5D00", "#FABF9A"


# ---------- tiempos ----------

def ease(name, p):
    """Las mismas curvas de GSAP que usa koi-base, calculadas en Python."""
    if p <= 0 or p >= 1 or name in ("none", "linear"):
        return min(max(p, 0.0), 1.0)
    kind, _, mode = name.partition(".")
    if kind == "sine":
        f_in, f_out = lambda x: 1 - math.cos(x * math.pi / 2), lambda x: math.sin(x * math.pi / 2)
    elif kind == "expo":
        f_in, f_out = lambda x: 2 ** (10 * x - 10), lambda x: 1 - 2 ** (-10 * x)
    else:
        n = int(kind.replace("power", "") or 1) + 1
        f_in, f_out = lambda x: x ** n, lambda x: 1 - (1 - x) ** n
    if mode == "in":
        return f_in(p)
    if mode == "out":
        return f_out(p)
    return f_in(p * 2) / 2 if p < 0.5 else 0.5 + f_out(p * 2 - 1) / 2


def frame(t):
    """Redondea un tiempo al cuadro de 30 fps más cercano."""
    return round(t * hf.FPS) / hf.FPS


def _steps(steps):
    return (steps,) if isinstance(steps, int) else tuple(steps)


def _grid(f, steps):
    """Cuadros de pose de todo el video: con (2, 3) son 0, 2, 5, 7, 10… Así todo el collage salta junto."""
    cycle, marks, acc = sum(steps), [], 0
    for s in steps:
        marks.append(acc)
        acc += s
    k, rest = divmod(f, cycle)
    for m in marks:
        if rest <= m:
            return k * cycle + m
    return (k + 1) * cycle


def beats(at, count, steps=STEPS):
    """Tiempos de `count` poses seguidas desde `at`, en la grilla común de poses (2 y 3 cuadros alternados).
    La primera pose cae en el primer cuadro de la grilla a partir de `at`."""
    steps = _steps(steps)
    f, out = _grid(round(at * hf.FPS), steps), []
    while len(out) < count:
        out.append(f / hf.FPS)
        f = _grid(f + 1, steps)
    return out


def until(start, end, steps=STEPS):
    """Tiempos de pose desde `start` hasta antes de `end`."""
    steps = _steps(steps)
    n = int((end - start) * hf.FPS / min(steps)) + 2
    start = max(start, 0)
    return [t for t in beats(start, n, steps) if t < end]


def at_rel(t):
    return max(0.0, round(t - hf.OFFSET - EPS, 4))


def pose(sel, t, values):
    return f'tl.set("{sel}", {{{hf.props(values)}}}, {at_rel(t)});\n'


def hidden(sel):
    """Arranca oculto. hf.scene lo pasa al CSS para que no parpadee."""
    return f'tl.set("{sel}", {{opacity:0}}, 0);\n'


# ---------- modo PAPEL (a saltos) ----------

def stop(sel, at, dur, frm, end, curve=hf.SMOOTH, steps=STEPS):
    """Como hf.move, pero a saltos: muestrea la curva en poses de 2 y 3 cuadros."""
    steps = _steps(steps)
    n = max(1, round(dur * hf.FPS / (sum(steps) / len(steps))))
    js = ""
    for i, t in enumerate(beats(at, n + 1, steps)):
        p = ease(curve, i / n)
        js += pose(sel, t, {k: round(frm[k] + (end[k] - frm[k]) * p, 3) for k in frm})
    return js


def poses(sel, at, frames, steps=STEPS):
    """Lista de poses a mano."""
    return "".join(pose(sel, t, v) for t, v in zip(beats(at, len(frames), steps), frames))


def drop(sel, at, y=-320, rot=-9, sound=True):
    """Cae desde arriba con un rebote corto en 5 poses. Suena papel (pop-papel-*.mp3)."""
    if sound:
        hf.snd(beats(at, 3)[2], "pop")
    return hidden(sel) + poses(sel, at, [
        {"opacity": 1, "y": y, "rotation": rot},
        {"y": round(y * 0.35), "rotation": round(rot * 0.4, 2)},
        {"y": 16, "rotation": round(-rot * 0.25, 2)},
        {"y": -5, "rotation": round(rot * 0.08, 2)},
        {"y": 0, "rotation": 0},
    ])


def grow(sel, at, sound=True):
    """Crece desde la línea del piso (edificios, plantas, pilas de billetes), en 5 poses (R5)."""
    if sound:
        hf.snd(frame(at), "pop")
    return hidden(sel) + poses(sel, at, [
        {"opacity": 1, "scaleY": 0.15, "transformOrigin": "50% 100%"},
        {"scaleY": 0.55}, {"scaleY": 1.08}, {"scaleY": 0.97}, {"scaleY": 1},
    ])


def slap(sel, at, scale=1.25, sound=True):
    """Aparece de golpe como un papel apoyado: grande, se asienta en 3 poses."""
    if sound:
        hf.snd(frame(at), "pop")
    return hidden(sel) + poses(sel, at, [
        {"opacity": 1, "scale": scale, "rotation": -3},
        {"scale": 0.97, "rotation": 1.2},
        {"scale": 1, "rotation": 0},
    ])


def pop_in(sel, at, sound=True):
    """Aparece desde chico con rebote: íconos, estrellitas, signos de pregunta."""
    if sound:
        hf.snd(frame(at), "pop")
    return hidden(sel) + poses(sel, at, [
        {"opacity": 1, "scale": 0.2}, {"scale": 1.18}, {"scale": 0.94}, {"scale": 1},
    ])


def enter(sel, at, x=0, y=0, rot=0, dur=0.42, sound=True):
    """Entra de costado a saltos y frena (manos, autos, billetes)."""
    if sound:
        hf.snd(frame(at) + dur * 0.4, "whoosh")
    return hidden(sel) + pose(sel, at, {"opacity": 1}) + stop(sel, at, dur, {"x": x, "y": y, "rotation": rot}, {"x": 0, "y": 0, "rotation": 0}, "power3.inOut")


def fly_out(sel, at, x=0, y=-900, rot=14, dur=0.35):
    """Sale volando a saltos (para desarmar el collage)."""
    return stop(sel, at, dur, {"x": 0, "y": 0, "rotation": 0}, {"x": x, "y": y, "rotation": rot}, "power2.in")


def boil(sel, start, end, amp=2.5, rot=0.7, steps=STEPS, seed=None):
    """Temblor de sticker: nada queda quieto. Va en el elemento de adentro (img.cut)."""
    r = random.Random(seed if seed is not None else sel)
    return "".join(pose(sel, t, {"x": round(r.uniform(-amp, amp), 1), "y": round(r.uniform(-amp, amp), 1), "rotation": round(r.uniform(-rot, rot), 2)}) for t in until(start, end, steps))


def parallax(layers, at, dur, dx=0, dy=0, ds=0.0, curve=hf.SLOW, steps=STEPS):
    """Empuja todas las capas a la vez; cada una se mueve según su factor de profundidad."""
    return "".join(
        stop(sel, at, dur, {"x": 0, "y": 0, "scale": 1}, {"x": round(dx * f, 1), "y": round(dy * f, 1), "scale": round(1 + ds * f, 4)}, curve, steps)
        for sel, f in layers
    )


def pan(sel, at, dur, frm_x, to_x, frm_y=0, to_y=0):
    """Cámara lateral a saltos sobre un lienzo largo: la composición siguiente ya está ahí (R2)."""
    hf.snd(frame(at) + dur * 0.4, "whoosh")
    return stop(sel, at, dur, {"x": -frm_x, "y": -frm_y}, {"x": -to_x, "y": -to_y}, "power3.inOut")


def grain(sel, start, end, steps=STEPS, seed=0):
    """Mueve la capa de grano a un lugar distinto en cada pose."""
    r = random.Random(seed)
    return "".join(pose(sel, t, {"x": r.randint(-110, 110), "y": r.randint(-110, 110)}) for t in until(start, end, steps))


def marker(sel, at, dur=0.5, sound=True):
    """Dibuja a saltos un trazo de stroke(): subrayado, círculo, flecha o línea de etiqueta."""
    if sound:
        hf.snd(frame(at), "key")
    svg = sel.split(" ")[0]
    return pose(svg, at, {"opacity": 1}) + stop(sel, at, dur, {"strokeDashoffset": 1}, {"strokeDashoffset": 0}, "power2.inOut")


def burst(prefix, src, at, count, x, y, spread=260, rise=420, size=70, seed=1, sound=True):
    """Stickers chicos que brotan de un punto y suben (corazones, notificaciones, billetes) (R1). Devuelve (html, js)."""
    r = random.Random(seed)
    html, js = "", ""
    for i in range(count):
        sid = f"{prefix}{i}"
        t0 = at + i * r.uniform(0.08, 0.18)
        dx, dy = r.uniform(-spread, spread), -rise * r.uniform(0.6, 1.2)
        s = r.uniform(0.7, 1.15)
        html += f'<img id="{sid}" class="chispa" src="{src}" style="left:{x - size / 2:.0f}px;top:{y - size / 2:.0f}px;width:{size}px">'
        js += hidden(f"#{sid}")
        js += poses(f"#{sid}", t0, [{"opacity": 1, "scale": 0.2, "x": 0, "y": 0}, {"scale": round(s * 1.15, 2), "x": round(dx * 0.15), "y": round(dy * 0.15), "rotation": round(r.uniform(-20, 20))}])
        js += stop(f"#{sid}", beats(t0, 2)[1], 1.1, {"x": round(dx * 0.15), "y": round(dy * 0.15), "opacity": 1}, {"x": round(dx), "y": round(dy), "opacity": 0}, "sine.inOut")
        if sound and i % 3 == 0:
            hf.snd(frame(t0), "pop")
    return html, js


def typed(prefix, timed, sound=True):
    """Texto palabra por palabra, sin animación: cada palabra aparece con la voz (R1, R5). Devuelve (html, js)."""
    html, js = "", ""
    for i, (at, text) in enumerate(timed):
        html += f'<span id="{prefix}{i}" class="w">{text}</span>' + (" " if i + 1 < len(timed) else "")
        js += hidden(f"#{prefix}{i}") + pose(f"#{prefix}{i}", max(at - 0.03, 0), {"opacity": 1})
        if sound and i % 2 == 0:
            hf.snd(at, "key")
    return html, js


# ---------- modo FLUIDO (cámara, fotos, texto documental) ----------

def focus_in(sel, at, dur=0.32, blur=18, scale=1.12, key=True):
    """Entra desenfocado y se enfoca (R4)."""
    if key:
        hf.snd(at + 0.03, "key")
    return hf.move(sel, at, dur, {"opacity": 0, "scale": scale, "filter": f"blur({blur}px)"}, {"opacity": 1, "scale": 1, "filter": "blur(0px)"}, hf.SOFT)


def focus_out(sel, at, dur=0.35, blur=26):
    """Salida de escena: se desenfoca y se apaga (la transición más usada en las referencias)."""
    return hf.to(sel, at, dur, {"opacity": 0, "filter": f"blur({blur}px)"}, hf.SOFT)


def rack(sel, at, dur=0.4, blur=10):
    """Cambio de foco: desenfoca una capa (el fondo cuando entra el texto). blur=0 la vuelve a enfocar (R3)."""
    return hf.to(sel, at, dur, {"filter": f"blur({blur}px)"}, hf.SMOOTH)


def push_through(sel, at, dur=0.9, scale=4.0):
    """Atraviesa un marco o un objeto: empuje que acelera y se desenfoca al final (R3)."""
    hf.snd(at + dur * 0.6, "whoosh")
    return hf.to(sel, at, dur, {"scale": scale}, "expo.in") + hf.to(sel, at + dur * 0.7, dur * 0.3, {"filter": "blur(22px)", "opacity": 0}, hf.SOFT)


def whip(sel, at, dur=0.36, x=-1080, y=0):
    """Paneo rápido: render.sh le pone el motion blur (R1)."""
    hf.snd(at + dur * 0.5, "whoosh")
    return hf.to(sel, at, dur, {"x": x, "y": y}, "expo.inOut")


def slide(sel, at, dur=0.55, x=0, y=0):
    """Entra de costado con curva suave y frena: objetos fotográficos (R4)."""
    hf.snd(at + dur * 0.4, "whoosh")
    return hf.move(sel, at, dur, {"opacity": 1, "x": x, "y": y}, {"x": 0, "y": 0}, "expo.inOut")


# ---------- HTML ----------

def layer(lid, inner, z=1):
    return f'<div id="{lid}" class="layer" style="z-index:{z}">{inner}</div>'


def paper(theme="white"):
    """Fondo de papel de make_paper.py: white, black, orange o cuadriculado."""
    return f'<img class="fill" src="assets/img/paper-{theme}.png">'


def sticker(cid, src, left, top, width, tone=None, cls=""):
    """Sticker recortado.
    tone=None   deja la imagen como viene (las de Codex ya traen el naranja Koi).
    tone="naranja" pasa una imagen de internet a duotono Koi: grises con tinte naranja (como R1).
    tone="bn"   la deja en blanco y negro contrastado, para que otro elemento lleve el color."""
    klass = "pos" + (f" {tone}" if tone else "") + (f" {cls}" if cls else "")
    img = f'<img id="{cid}-img" class="cut" src="{src}">'
    tint = f'<div class="tinte" style="-webkit-mask-image:url({src});mask-image:url({src})"></div>' if tone == "naranja" else ""
    return f'<div id="{cid}" class="{klass}" style="left:{left}px;top:{top}px;width:{width}px">{img}{tint}</div>'


def shape(sid, kind, left, top, size, color=PEACH, opacity=0.85, rot=0):
    """Forma plana detrás del sujeto: circulo, medio, triangulo, trama (halftone) o cuadricula."""
    style = f"left:{left}px;top:{top}px;width:{size}px;height:{size}px;transform:rotate({rot}deg);opacity:{opacity}"
    if kind in ("trama", "cuadricula"):
        name = "halftone" if kind == "trama" else "cuadricula"
        return f'<img id="{sid}" class="forma" src="assets/img/{name}.png" style="{style}">'
    clip = {"circulo": "circle(50% at 50% 50%)", "medio": "polygon(0 50%,100% 50%,100% 100%,0 100%)", "triangulo": "polygon(50% 8%,100% 100%,0 100%)"}[kind]
    radius = "border-radius:50%;" if kind == "medio" else ""
    return f'<div id="{sid}" class="forma" style="{style};background:{color};{radius}clip-path:{clip}"></div>'


def torn(seed=0, teeth=14, depth=2.2):
    """clip-path con bordes rotos a izquierda y derecha, para tiras de papel."""
    r = random.Random(seed)
    left = [(round(r.uniform(0, depth), 1), round(i * 100 / teeth, 1)) for i in range(teeth + 1)]
    right = [(round(100 - r.uniform(0, depth), 1), round(100 - i * 100 / teeth, 1)) for i in range(teeth + 1)]
    return "polygon(" + ",".join(f"{x}% {y}%" for x, y in left + right) + ")"


def tira(tid, text, left, top, kind="papel", size=34, seed=0):
    """Tira de papel roto con texto (R2, R3). kind: papel, negra o naranja. Se anima por su id."""
    return f'<div id="{tid}" class="tira-wrap" style="left:{left}px;top:{top}px"><div class="tira {kind}" style="font-size:{size}px;clip-path:{torn(seed)}">{text}</div></div>'


def subtitle(sid, text, top=1380):
    """Subtítulo en caja blanca con texto negro (R1). Una frase corta por vez."""
    return f'<div id="{sid}" class="sub" style="top:{top}px"><span>{text}</span></div>'


def stroke(sid, d, left, top, w, h, color=ORANGE, width=10):
    """Trazo a mano para marker(): subrayado, círculo, flecha o línea de etiqueta. d en coordenadas del SVG.
    Animar con marker(f"#{sid} path", at)."""
    return f'<svg id="{sid}" class="marca" style="left:{left}px;top:{top}px;opacity:0" width="{w}" height="{h}"><path pathLength="1" d="{d}" stroke="{color}" stroke-width="{width}"/></svg>'


def label(lid, text, left, top, to_x, to_y):
    """Etiqueta naranja con línea que apunta a un objeto (R5). (to_x, to_y): punto del objeto en el cuadro.
    Animar con: marker(f"#{lid}-l path", at) + slap(f"#{lid}", at + 0.3)."""
    x0, y0 = left, top + 30
    minx, miny = min(x0, to_x) - 10, min(y0, to_y) - 10
    w, h = abs(to_x - x0) + 20, abs(to_y - y0) + 20
    mid = (x0 + to_x) / 2
    d = f"M{x0 - minx:.0f} {y0 - miny:.0f} L{mid - minx:.0f} {y0 - miny:.0f} L{to_x - minx:.0f} {to_y - miny:.0f}"
    line = stroke(f"{lid}-l", d, minx, miny, w, h, "#0B0B0B", 4)
    box = f'<div id="{lid}" class="etiqueta" style="left:{left}px;top:{top}px">{text}</div>'
    return line + box


def sello(sid, text, left, top, size=64, rot=-9):
    """Sello de goma naranja con tinta gastada (assets/img/stamp-mask.png de make_paper.py).
    Va sobre una zona clara (pared, mesa, papel), nunca sobre una cara. Animar con slap(f"#{sid}", at, 1.5)."""
    return (f'<div id="{sid}" class="pos" style="left:{left}px;top:{top}px">'
            f'<div class="sellado" style="font-size:{size}px;transform:rotate({rot}deg)">{text}</div></div>')


def grain_html(gid, light=False):
    src = "grain-light" if light else "grain-dark"
    blend = "screen" if light else "multiply"
    return f'<img id="{gid}" class="grain" src="assets/img/{src}.png" style="mix-blend-mode:{blend}">'


def vignette():
    """Viñeta oscura en los bordes del papel (R4)."""
    return '<div class="vineta"></div>'


def css():
    return f"""
.layer {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
.pos {{ position: absolute; transform-origin: 50% 85%; }}
.cut {{ display: block; width: 100%; height: auto; filter: drop-shadow(0 10px 14px rgba(0,0,0,.28)); }}
.pos.bn > .cut, .pos.naranja > .cut {{ filter: grayscale(1) contrast(1.3) drop-shadow(0 10px 14px rgba(0,0,0,.28)); }}
.tinte {{ position: absolute; inset: 0; background: {ORANGE}; mix-blend-mode: multiply; opacity: .9;
  -webkit-mask-size: 100% 100%; mask-size: 100% 100%; pointer-events: none; }}
.forma {{ position: absolute; }}
.chispa {{ position: absolute; filter: drop-shadow(0 6px 8px rgba(0,0,0,.25)); }}
.tira-wrap {{ position: absolute; filter: drop-shadow(6px 8px 0 rgba(0,0,0,.22)); }}
.tira {{ padding: 14px 34px; background: #F2F2F0; color: #000; font-weight: 600; white-space: nowrap; }}
.tira.negra {{ background: #0B0B0B; color: #fff; }}
.tira.naranja {{ background: {ORANGE}; color: #000; }}
.sub {{ position: absolute; left: 0; width: {hf.W}px; text-align: center; }}
.sub span {{ display: inline-block; background: #fff; color: #000; font-weight: 800; font-size: 46px; padding: 6px 16px; letter-spacing: -0.02em; }}
.etiqueta {{ position: absolute; background: {ORANGE}; color: #000; font-weight: 800; font-size: 40px; padding: 10px 22px; }}
.marca {{ position: absolute; overflow: visible; }}
.marca path {{ fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }}
.grain {{ position: absolute; left: -120px; top: -120px; width: {hf.W + 240}px; height: {hf.H + 240}px; z-index: 50; pointer-events: none; }}
.vineta {{ position: absolute; inset: 0; z-index: 49; pointer-events: none;
  background: radial-gradient(ellipse 75% 60% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.38) 100%); }}
.placa {{ position: absolute; inset: 0; background: #0B0B0B; }}
.tinta {{ color: #0B0B0B; }}  /* texto sobre papel claro: hf_base deja el texto blanco por defecto */
.sellado {{ position: relative; padding: 10px 30px; border: 11px solid {ORANGE}; border-radius: 10px; color: {ORANGE};
  font-weight: 800; letter-spacing: .05em; white-space: nowrap; mix-blend-mode: multiply; opacity: .95;
  -webkit-mask-image: url(assets/img/stamp-mask.png); mask-image: url(assets/img/stamp-mask.png);
  -webkit-mask-size: 100% 100%; mask-size: 100% 100%; }}
/* Orden de capas: el texto siempre arriba de los stickers, y los trazos (la X, flechas) arriba del objeto que marcan.
   Las .layer tienen z-index, así que sin esto un texto suelto queda debajo del collage. */
.line {{ z-index: 25; }}
.sub {{ z-index: 30; }}
.tira-wrap {{ z-index: 20; }}
.layer > .pos, .layer > .pan, .layer > .phone, .layer > .cur, .layer > .card {{ z-index: 10; }}
.layer > .marca {{ z-index: 11; }}
"""
