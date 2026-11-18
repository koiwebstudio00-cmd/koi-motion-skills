# Ayudantes para generar un proyecto de HyperFrames desde Python.
# Copiar a tools/ del proyecto y usar desde tools/build.py:
#
#   import hf_base as hf
#   hf.setup(1080, 1920, end=30.0)
#   html, js = hf.words("t", [(0.4, "Menos"), (0.8, "caos.")])
#   hosts = [hf.scene("s1", 0, 4, "", f'<div class="line" style="top:800px;font-size:88px">{html}</div>', js)]
#   hf.index(hosts)
#   hf.save_events()
#
# Cada texto y cada movimiento anota su sonido, así la imagen y el audio salen de los mismos tiempos.
import json
import os
import re

FPS = 30
W, H, END = 1080, 1920, 0.0
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BACKGROUND = "#0B0B0B"

SMOOTH = "power3.inOut"
SOFT = "power2.inOut"
SLOW = "sine.inOut"
RAMP = "expo.inOut"

OFFSET = 0.0
EVENTS = []


def setup(width, height, end, background="#0B0B0B", root=None):
    global W, H, END, BACKGROUND, ROOT
    W, H, END, BACKGROUND = width, height, end, background
    if root:
        ROOT = root


def shared_css():
    return f"""
#root {{ position: absolute; inset: 0; font-family: Manrope, sans-serif; color: #fff; overflow: hidden; }}
.serif {{ font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; letter-spacing: 0; }}
.obj {{ position: absolute; display: block; }}
.line {{ position: absolute; left: {round(W * .1)}px; width: {round(W * .8)}px; text-align: center; font-weight: 800; letter-spacing: -0.025em; }}
.w {{ display: inline-block; white-space: pre; }}
.or {{ color: #FA5D00; }}
.fill {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
"""


def props(values):
    return ",".join(f"{k}:{v!r}" if isinstance(v, str) else f"{k}:{v}" for k, v in values.items())


def rel(at):
    return round(at - OFFSET, 3)


def move(sel, at, dur, frm, end, ease=SMOOTH):
    return f'tl.fromTo("{sel}", {{{props(frm)}}}, {{{props(end)},duration:{dur},ease:"{ease}"}}, {rel(at)});\n'


def to(sel, at, dur, values, ease=SMOOTH):
    return f'tl.to("{sel}", {{{props(values)},duration:{dur},ease:"{ease}"}}, {rel(at)});\n'


def snd(at, kind):
    EVENTS.append([round(at, 3), kind])


def rise(sel, at, dur=0.3, key=True):
    """Muestra un texto. Cada texto que aparece lleva sonido de teclado."""
    if key:
        snd(at + 0.03, "key")
    return move(sel, at, dur, {"opacity": 0, "y": 24, "filter": "blur(10px)"}, {"opacity": 1, "y": 0, "filter": "blur(0px)"}, SOFT)


def slam(sel, at, dur=0.44, scale=1.6):
    snd(at + 0.1, "key")
    return move(sel, at, dur, {"opacity": 0, "scale": scale, "filter": "blur(20px)"}, {"opacity": 1, "scale": 1, "filter": "blur(0px)"})


def pop(sel, at, dur=0.36, y=34):
    snd(at + 0.06, "pop")
    return move(sel, at, dur, {"opacity": 0, "y": y, "scale": 0.86}, {"opacity": 1, "y": 0, "scale": 1})


def out(sel, at, dur=0.28, y=-50):
    return to(sel, at, dur, {"opacity": 0, "y": y, "filter": "blur(14px)"})


def words(prefix, timed):
    """Texto palabra por palabra: timed es una lista de (segundo, palabra)."""
    html, js = "", ""
    for i, (at, text) in enumerate(timed):
        html += f'<span id="{prefix}{i}" class="w">{text}</span>' + (" " if i + 1 < len(timed) else "")
        js += rise(f"#{prefix}{i}", max(at - 0.04, 0), key=i % 2 == 0)
    return html, js


def cam(sel, at, dur, cx, cy, s, ease=RAMP):
    """Mueve un lienzo para que el punto (cx, cy) llegue al centro del cuadro."""
    snd(at + dur * 0.5, "whoosh")
    return to(sel, at, dur, {"x": round(W / 2 - cx * s, 1), "y": round(H / 2 - cy * s, 1), "scale": s}, ease)


def cam_set(sel, cx, cy, s):
    return f'tl.set("{sel}", {{x:{round(W / 2 - cx * s, 1)},y:{round(H / 2 - cy * s, 1)},scale:{s},transformOrigin:"0 0"}}, 0);\n'


def scene(sid, start, end, css, body, js):
    dur = round(end - start, 4)
    os.makedirs(f"{ROOT}/compositions", exist_ok=True)
    # Lo que arranca oculto va en CSS: así no parpadea en el primer cuadro.
    hidden = re.findall(r'tl\.set\("([^"]+)", \{opacity:0\}, 0\);\n', js)
    js = re.sub(r'tl\.set\("[^"]+", \{opacity:0\}, 0\);\n', "", js)
    if hidden:
        css += "\n" + ",".join(hidden) + " { opacity: 0; }"
    html = f"""<template>
  <style>
    {shared_css()}
    {css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap data-layout-allow-overflow>
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    tl.set({{}}, {{}}, {dur});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    with open(f"{ROOT}/compositions/{sid}.html", "w", encoding="utf-8") as f:
        f.write(html)
    return (sid, round(start, 4), dur)


def index(hosts):
    mounts = "\n".join(
        f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start}" data-duration="{dur}" data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:5"></div>'
        for sid, start, dur in hosts
    )
    html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: Manrope; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
      @font-face {{ font-family: "Instrument Serif"; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); font-style: italic; font-weight: 400; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {BACKGROUND}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="{W}" data-height="{H}">
      <audio id="mix" src="assets/mix.m4a" data-start="0" data-duration="{END}" data-track-index="1" data-volume="1"></audio>
{mounts}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {END});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    with open(f"{ROOT}/index.html", "w", encoding="utf-8") as f:
        f.write(html)


def save_events(risers=None, drops=None):
    """Escribe assets/build/fx_plan.json para make_fx.py."""
    os.makedirs(f"{ROOT}/assets/build", exist_ok=True)
    with open(f"{ROOT}/assets/build/fx_plan.json", "w", encoding="utf-8") as f:
        json.dump({"events": sorted(EVENTS), "risers": risers or [], "drops": drops or []}, f)
