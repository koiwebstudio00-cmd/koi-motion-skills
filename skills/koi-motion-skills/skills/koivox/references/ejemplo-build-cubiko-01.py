# Koivox Cubiko 01 · "¿Cuánto le pagarías?"
# Genera index.html y compositions/*.html. Tiempos de assets/build/palabras.json (voz final).
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hf_base as hf  # noqa: E402
import koivox as kv  # noqa: E402

END = 69.6
hf.setup(1080, 1920, end=END, background="#0B0B0B")
IMG = "assets/images"
CASA = "assets/img/casa"

# ------------------------------------------------------------------ estilos propios

UI_CSS = """
.line { line-height: 1.12; z-index: 25; }
.sub { z-index: 30; }
.tira-wrap { z-index: 20; }
.layer > .pos, .layer > .pan, .layer > .phone, .layer > .cur, .layer > .card { z-index: 10; }
.layer > .marca { z-index: 11; }
.big { font-size: 66px; }
.kw { font-size: 104px; line-height: 1; }
.bub { position: absolute; max-width: 470px; padding: 20px 28px; border-radius: 36px; font-weight: 700; font-size: 31px; line-height: 40px; letter-spacing: -0.01em; color: #000; }
.bub.in { left: 24px; background: #fff; box-shadow: 0 8px 20px rgba(90,45,15,.12); }
.bub.out { right: 24px; background: linear-gradient(145deg,#FF8A40,#FA5D00 60%,#E24A00); }
.bigbub { position: relative; padding: 26px 34px; border-radius: 40px; font-weight: 800; font-size: 40px; line-height: 50px; letter-spacing: -0.02em; color: #000; box-shadow: 0 14px 30px rgba(0,0,0,.22); }
.bigbub small { display: block; font-size: 24px; line-height: 30px; font-weight: 700; color: #6f6d68; margin-bottom: 6px; }
.bigbub.wh { background: #fff; }
.bigbub.o { background: linear-gradient(145deg,#FF8A40,#FA5D00 60%,#E24A00); }
.bigbub.o small { color: rgba(0,0,0,.6); }
.phone { position: absolute; width: 640px; height: 1180px; border-radius: 84px; background: #0B0B0B; padding: 14px; box-shadow: 0 40px 90px rgba(90,45,15,.28); transform-origin: 50% 50%; }
.scr { position: relative; width: 612px; height: 1152px; border-radius: 72px; overflow: hidden; background: #F7F4F0; }
.hd { position: absolute; left: 0; right: 0; top: 0; height: 150px; padding: 58px 32px 0; display: flex; gap: 20px; align-items: center; border-bottom: 1px solid rgba(0,0,0,.08); background: #F7F4F0; z-index: 2; }
.av { flex: none; width: 64px; height: 64px; border-radius: 50%; background: #FA5D00; text-align: center; font-weight: 800; font-size: 30px; line-height: 64px; color: #000; }
.av.g { background: #DEDAD0; }
.hn { font-weight: 800; font-size: 32px; line-height: 38px; color: #000; }
.ho { font-weight: 500; font-size: 24px; line-height: 30px; color: #6f6d68; }
.thread { position: absolute; left: 0; top: 0; width: 612px; height: 2000px; }
.media { position: absolute; right: 24px; width: 420px; height: 300px; }
.media .ph { position: absolute; width: 207px; height: 147px; overflow: hidden; border-radius: 18px; }
.media img { width: 100%; height: 100%; object-fit: cover; display: block; }
.play { position: absolute; left: 50%; top: 50%; width: 64px; height: 64px; margin: -32px 0 0 -32px; border-radius: 50%; background: rgba(0,0,0,.55); }
.play::after { content: ""; position: absolute; left: 25px; top: 18px; border-left: 22px solid #fff; border-top: 14px solid transparent; border-bottom: 14px solid transparent; }
.sys { position: absolute; left: 0; width: 612px; text-align: center; }
.sys span { display: inline-block; padding: 10px 22px; border-radius: 30px; background: #E9E6DF; color: #5C584C; font-weight: 700; font-size: 24px; line-height: 32px; }
.sys.k span { background: #0B0B0B; color: #fff; }
.pan { position: absolute; background: #FAF9F5; border: 2px solid #DEDDD6; border-radius: 30px; box-shadow: 0 24px 60px rgba(90,45,15,.17); color: #3D3929; overflow: hidden; }
.pt { padding: 32px 36px 4px; font-weight: 800; font-size: 46px; line-height: 54px; letter-spacing: -0.02em; color: #0B0B0B; }
.ps { padding: 0 36px 24px; font-size: 24px; line-height: 32px; color: #7A7667; font-weight: 500; border-bottom: 2px solid #E9E7DE; }
.cols { display: flex; padding: 16px 36px; font-size: 20px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; color: #7A7667; border-bottom: 2px solid #E9E7DE; }
.row { position: absolute; left: 0; right: 0; height: 150px; display: flex; align-items: center; gap: 20px; padding: 0 36px; border-bottom: 2px solid #E9E7DE; }
.nm { font-weight: 800; font-size: 30px; line-height: 36px; color: #0B0B0B; }
.cp { font-size: 22px; line-height: 30px; color: #6E6A5C; font-weight: 500; }
.chn { position: absolute; left: 470px; padding: 8px 16px; border-radius: 14px; background: #EFEDE4; font-weight: 700; font-size: 24px; color: #3D3929; }
.est { position: absolute; left: 676px; width: 190px; height: 46px; }
.est span { position: absolute; left: 0; top: 0; padding: 8px 16px; border-radius: 14px; font-weight: 800; font-size: 23px; white-space: nowrap; }
.est .e1 { background: #E9E6DF; color: #5C584C; }
.est .e2 { background: #FA5D00; color: #000; opacity: 0; }
.rr { display: flex; justify-content: space-between; padding: 20px 32px; font-size: 28px; line-height: 36px; border-bottom: 2px solid #E9E7DE; }
.rr span { color: #7A7667; font-weight: 500; }
.rr b { color: #0B0B0B; font-weight: 800; }
.fl { font-size: 21px; color: #7A7667; font-weight: 800; text-transform: uppercase; letter-spacing: .05em; }
.fv { margin-top: 10px; padding: 0 22px; border: 2px solid #DEDDD6; border-radius: 16px; background: #fff; font-size: 30px; font-weight: 700; color: #0B0B0B; height: 70px; line-height: 66px; }
.fblk { position: absolute; left: 36px; right: 36px; }
.seg span { display: inline-block; margin-top: 10px; margin-right: 10px; padding: 12px 28px; border-radius: 14px; border: 2px solid #DEDDD6; font-weight: 700; font-size: 26px; background: #fff; }
.seg .on { background: #0B0B0B; color: #fff; border-color: #0B0B0B; }
.slots { position: absolute; left: 36px; right: 36px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.slot { position: relative; height: 160px; border-radius: 16px; background: #EFEDE4; border: 2px dashed #CFCBBE; overflow: hidden; }
.slot img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; }
.btn { position: absolute; padding: 20px 40px; border-radius: 20px; background: linear-gradient(145deg,#FF8A40,#FA5D00 60%,#E24A00); color: #000; font-size: 32px; font-weight: 800; box-shadow: 0 12px 26px rgba(250,93,0,.35); }
.cur { position: absolute; left: 0; top: 0; z-index: 30; filter: drop-shadow(0 6px 10px rgba(0,0,0,.3)); }
.card { position: absolute; }
.card > .in { position: relative; width: 100%; height: 100%; background: #fff; padding: 10px; box-shadow: 0 14px 26px rgba(0,0,0,.25); }
.card .ft { position: relative; width: 100%; overflow: hidden; }
.card .ft img { width: 100%; height: 100%; object-fit: cover; display: block; filter: saturate(.55) contrast(1.05); }
.card .cl { font-weight: 800; font-size: 24px; line-height: 34px; color: #0B0B0B; padding-top: 6px; }
.bars { position: absolute; left: 10px; right: 10px; top: 10px; display: flex; gap: 6px; }
.bars i { flex: 1; height: 5px; border-radius: 3px; background: rgba(255,255,255,.55); }
.bars i:first-child { background: #fff; }
.dots { position: absolute; left: 0; right: 0; bottom: 8px; text-align: center; }
.dots i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #CFCBBE; margin: 0 4px; }
.dots i:first-child { background: #0B0B0B; }
.webbar { height: 34px; display: flex; gap: 8px; align-items: center; padding-left: 6px; }
.webbar i { width: 12px; height: 12px; border-radius: 50%; background: #DEDAD0; }
.wbtn { display: inline-block; margin-top: 8px; padding: 10px 20px; border-radius: 12px; background: #0B0B0B; color: #fff; font-size: 20px; font-weight: 800; }
.sellado { position: absolute; padding: 10px 30px; border: 11px solid #FA5D00; border-radius: 10px; color: #FA5D00; font-weight: 800; font-size: 92px; letter-spacing: .05em; mix-blend-mode: multiply; opacity: .95; -webkit-mask-image: url(assets/img/stamp-mask.png); mask-image: url(assets/img/stamp-mask.png); -webkit-mask-size: 100% 100%; mask-size: 100% 100%; }
.patch { position: absolute; background: #F2F2F0; box-shadow: 6px 10px 0 rgba(0,0,0,.18); padding: 34px; }
.patch img { width: 100%; display: block; }
.dim { position: absolute; inset: 0; background: #0B0B0B; z-index: 40; }
.notif { position: absolute; padding: 14px 24px; border-radius: 26px; background: rgba(255,255,255,.94); color: #0B0B0B; font-weight: 800; font-size: 28px; line-height: 34px; white-space: nowrap; box-shadow: 0 12px 26px rgba(0,0,0,.4); }
.notif b { color: #FA5D00; }
.paperx { position: absolute; top: 0; width: 1080px; height: 1920px; }
"""
CSS = kv.css() + UI_CSS

CURSOR = '<svg width="58" height="72" viewBox="0 0 58 72"><path d="M4 4 L4 58 L18 46 L28 68 L38 63 L28 42 L46 42 Z" fill="#0B0B0B" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>'


# ------------------------------------------------------------------ ayudantes

def st(cid, name, left, top, width, tone=None):
    return kv.sticker(cid, f"{IMG}/{name}.png", left, top, width, tone)


def say(prefix, items, top, cls="", size=66, left=108, width=864):
    """Frase palabra por palabra. items: (t, texto[, clase[, modo]]). modo: 'f' foco (fluido), 's' slap.
    texto '/' es salto de línea."""
    html, js, n = "", "", 0
    for it in items:
        t, text = it[0], it[1]
        klass = it[2] if len(it) > 2 else ""
        mode = it[3] if len(it) > 3 else ""
        if text == "/":
            html += "<br>"
            continue
        wid = f"{prefix}{n}"
        html += f'<span id="{wid}" class="w {klass}">{text}</span> '
        if mode == "f":
            js += kv.focus_in(f"#{wid}", t)
        elif mode == "s":
            js += kv.slap(f"#{wid}", t, 1.4)
        else:
            js += kv.hidden(f"#{wid}") + kv.pose(f"#{wid}", max(t - 0.03, 0), {"opacity": 1})
            if n % 2 == 0:
                hf.snd(t, "key")
        n += 1
    line = f'<div id="{prefix}" class="line {cls}" style="top:{top}px;left:{left}px;width:{width}px;font-size:{size}px">{html}</div>'
    return line, js


def off(sel, t):
    return kv.pose(sel, t, {"opacity": 0})


def subs(prefix, items, top=1440):
    html, js = "", ""
    for i, (a, b, text) in enumerate(items):
        sid = f"{prefix}{i}"
        html += kv.subtitle(sid, text, top)
        js += kv.hidden(f"#{sid}") + kv.pose(f"#{sid}", a, {"opacity": 1}) + off(f"#{sid}", b)
    return html, js


def boils(ids, end):
    return "".join(kv.boil(f"#{cid}-img", t, end, seed=i) for i, (cid, t) in enumerate(ids))


def grain(gid, start, end, light=False):
    return kv.grain_html(gid, light), kv.grain(f"#{gid}", start, end, seed=int(start))


def bub(bid, text, left, top, width, kind="wh", head=""):
    small = f"<small>{head}</small>" if head else ""
    return f'<div id="{bid}" class="pos" style="left:{left}px;top:{top}px;width:{width}px"><div class="bigbub {kind}">{small}{text}</div></div>'


def card(cid, kind, photo, left, top, w, h, rot=0, label=""):
    """Tarjeta de redes como papel: reel, historia o carrusel."""
    ph = h - 20 - (40 if label else 0)
    extra = ""
    if kind == "reel":
        extra = '<div class="play"></div>'
    elif kind == "historia":
        extra = '<div class="bars"><i></i><i></i><i></i></div>'
    elif kind == "carrusel":
        extra = '<div class="dots"><i></i><i></i><i></i><i></i></div>'
    lab = f'<div class="cl">{label}</div>' if label else ""
    return (f'<div id="{cid}" class="card pos" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">'
            f'<div class="in" style="transform:rotate({rot}deg)"><div class="ft" style="height:{ph}px"><img src="{CASA}/{photo}.png">{extra}</div>{lab}</div></div>')


def web_card(cid, left, top, w, rot=0):
    return (f'<div id="{cid}" class="card pos" style="left:{left}px;top:{top}px;width:{w}px">'
            f'<div class="in" style="transform:rotate({rot}deg);border-radius:14px;padding:12px 14px 18px">'
            f'<div class="webbar"><i></i><i></i><i></i></div>'
            f'<div class="ft" style="height:230px;border-radius:8px"><img src="{CASA}/01-entrada.png"></div>'
            f'<div class="cl" style="font-size:26px;padding-top:12px">Casa con pileta en Yerba Buena</div>'
            f'<div class="cl" style="font-size:20px;font-weight:600;color:#7A7667;padding-top:0">Alquiler · Casa · Fotos 6 · Video 1</div>'
            f'<div class="wbtn">Consultar por WhatsApp</div></div></div>')


def clock(prefix, left, top, width):
    """Reloj de pared con dos agujas que giran desde su centro."""
    h = width * 1066 / 1600
    cx, cy = left + width * 0.4956, top + h * 0.5
    html = st(f"{prefix}r", "reloj-pared", left, top, width)
    for name, scale in (("m", 0.27), ("h", 0.19)):
        aw = width * scale * 1600 / 1600
        ah = aw * 1066 / 1600
        al, at = cx - aw * 0.5, cy - ah * 0.82
        html += (f'<div id="{prefix}{name}" class="pos" style="left:{al:.1f}px;top:{at:.1f}px;width:{aw:.1f}px;transform-origin:50% 82%">'
                 f'<img class="cut" src="{IMG}/agujas-reloj.png" style="filter:none"></div>')
    return html


def x_stroke(sid, left, top, w, h):
    d = f"M18 18 L{w - 18} {h - 18} M{w - 18} 18 L18 {h - 18}"
    return kv.stroke(sid, d, left, top, w, h, kv.ORANGE, 16)


hosts = []

# ================================================================== 1. Gancho (0 – 7.92)
S, E = 0.0, 7.92
hf.OFFSET = S
l1, j1 = say("p1", [(0.0, "Si"), (0.18, "te"), (0.28, "ofrecieran"), (0.74, "un"), (0.86, "vendedor"), (1.30, "que"), (1.48, "nunca"), (1.90, "duerme…", "serif or kw")], 250, "tinta")
l2, j2 = say("p2", [(2.80, "que"), (3.24, "nunca"), (3.62, "se"), (3.84, "olvida"), (4.08, "de"), (4.22, "un"), (4.30, "cliente…", "serif or kw")], 250, "tinta")
l3, j3 = say("p3", [(5.24, "y"), (5.48, "que"), (5.54, "contesta"), (5.94, "en"), (6.08, "cuatro", "serif or kw"), (6.38, "redes", "serif or kw"), (6.78, "a"), (6.94, "la"), (7.00, "vez…")], 250, "tinta")
icons = [("i1", "icono-chat", 70, 560, 5.54), ("i2", "icono-camara", 840, 590, 6.08), ("i3", "icono-pulgar", 60, 840, 6.38), ("i4", "icono-nota", 850, 860, 6.78)]
bh, bj = kv.burst("nt", f"{IMG}/icono-notificacion.png", 6.5, 9, 540, 780, spread=420, rise=360, size=96, seed=3)
gh, gj = grain("g1", S, E)
sub = "".join(st(c, n, x, y, 170) for c, n, x, y, _ in icons)
body = (kv.layer("l1f", kv.paper("white"))
        + kv.layer("l1s", kv.shape("c1", "circulo", 150, 560, 780) + kv.shape("t1", "trama", 650, 330, 420, "#000", 0.22), 2)
        + kv.layer("l1m", st("m1", "martina-espaldas", 200, 577, 680)
                   + st("alm", "almohada", 660, 1180, 380) + x_stroke("ax", 700, 1180, 300, 230)
                   + st("lib", "libreta-ficha", 20, 1130, 440) + sub + bh, 3)
        + kv.tira("tr1", "NUNCA SE OLVIDA", 70, 1395, "negra", 40, 2)
        + l1 + l2 + l3 + kv.vignette() + gh)
js = (j1 + off("#p1", 2.78) + j2 + off("#p2", 5.2) + j3
      + kv.drop("#m1", 0.0, -260) + kv.drop("#alm", 1.9) + kv.marker("#ax path", 2.25, 0.4)
      + kv.drop("#lib", 3.84, -300, 8) + kv.slap("#tr1", 4.3)
      + "".join(kv.pop_in(f"#{c}", t) for c, _, _, _, t in icons) + bj
      + boils([("m1", 0.2), ("alm", 2.1), ("lib", 4.0)] + [(c, t) for c, _, _, _, t in icons], E)
      + kv.parallax([("#l1f", 0.3), ("#l1s", 0.6), ("#l1m", 1.0)], S, E, dy=-30, ds=0.06)
      + gj)
hosts.append(hf.scene("s01", S, E, CSS, body, js))

# ================================================================== 2. Placa (7.92 – 9.6)
S, E = 7.92, 9.6
hf.OFFSET = S
l, j = say("q1", [(7.92, "¿Cuánto"), (8.18, "le"), (8.0, "/"), (8.28, "pagarías?", "serif or", "f")], 760, "", 100)
gh, gj = grain("g2", S, E, True)
body = '<div class="placa"></div>' + l + gh
js = j + hf.to("#q1", 8.5, 1.1, {"scale": 1.05}, hf.SLOW) + gj
hosts.append(hf.scene("s02", S, E, CSS + "\n#q12 { font-size: 170px; line-height: 1; } #q1 { transform-origin: 50% 50%; }", body, js))

# ================================================================== 3. Domingo (9.6 – 14.88)
S, E = 9.6, 14.88
hf.OFFSET = S
sh, sj = subs("sb3", [(9.6, 11.4, "Domingo, once de la noche."), (11.44, 13.05, "Carla escribe por Instagram."), (13.08, 14.85, "Busca una casa para alquilar.")])
gh, gj = grain("g3", S, E)
body = ('<div id="all3" class="layer">'
        + kv.layer("l3f", kv.paper("cuadriculado"))
        + kv.layer("l3s", kv.shape("c3", "circulo", 130, 600, 820), 2)
        + kv.layer("l3m", st("cs", "carla-sillon", 150, 560, 780), 3)
        + bub("bq3", "¡Hola! ¿Sigue disponible la casa de Yerba Buena?", 300, 390, 640, "wh", "Instagram · 23:07")
        + kv.tira("tr3", "DOMINGO · 23:07", 80, 250, "negra", 46, 5)
        + kv.vignette() + '</div>' + sh + gh)
js = (kv.slap("#tr3", 9.6) + kv.drop("#cs", 9.75, -300, 6) + kv.pop_in("#bq3", 12.28)
      + boils([("cs", 10.0)], E) + kv.boil("#bq3", 12.5, E, 1.5, 0.4)
      + kv.parallax([("#l3f", 0.3), ("#l3s", 0.6), ("#l3m", 1.0)], S, E, dy=-20, ds=0.07)
      + sj + kv.focus_out("#all3", 14.6, 0.28) + gj)
hosts.append(hf.scene("s03", S, E, CSS, body, js))

# ================================================================== 4. Nadie contesta → Lunes → alquiló (14.88 – 21.62)
S, E = 14.88, 21.62
hf.OFFSET = S
R = 1080
l, j = say("p4", [(14.88, "Nadie"), (15.40, "contesta.")], 250, "tinta", 100)
sh, sj = subs("sb4", [(16.5, 18.2, "Lunes, nueve de la mañana."), (18.26, 19.4, "Alguien le responde."), (19.44, 20.3, "Carla ya alquiló"), (20.36, 21.5, "con otra inmobiliaria.")])
gh, gj = grain("g4", S, E)
body = ('<div id="lz4" class="layer" style="width:2160px">'
        + f'<img class="paperx" src="assets/img/paper-white.png" style="left:0"><img class="paperx" src="assets/img/paper-white.png" style="left:{R}px">'
        + kv.shape("q4", "cuadricula", 560, 230, 460, "#000", 0.45)
        + clock("rl", 170, 330, 700)
        + st("esc", "escritorio", 70, 1010, 940)
        + st("cel", "celular-boca-abajo", 420, 990, 300)
        + bub("bq4", "¡Hola Carla! Sí, sigue disponible.", 110, 760, 640, "wh", "Lunes · 9:02")
        + kv.tira("tr4", "LUNES · 9:00", 80, 250, "negra", 46, 7)
        + kv.shape("c4", "circulo", R + 150, 520, 780)
        + st("foto4", "../img/casa/06-comedor", R + 470, 330, 470, "bn")
        + st("cll", "carla-llaves", R + 110, 440, 760)
        + st("sel", "sello-alquilada", R + 620, 1230, 400)
        + f'<div id="imp" class="pos" style="left:{R + 530}px;top:950px"><div class="sellado" style="font-size:64px;position:relative;transform:rotate(-9deg)">ALQUILADA</div></div>'
        + '</div>' + l + kv.vignette() + sh + gh)
js = (j + off("#p4", 16.45) + kv.slap("#tr4", 16.5)
      + kv.stop("#rlm", 14.88, 1.5, {"rotation": 0}, {"rotation": 1080}, "power2.inOut")
      + kv.stop("#rlh", 14.88, 1.5, {"rotation": 0}, {"rotation": 90}, "power2.inOut")
      + kv.stop("#rlm", 16.5, 0.6, {"rotation": 1080}, {"rotation": 1440}, "power2.out")
      + kv.stop("#rlh", 16.5, 0.6, {"rotation": 90}, {"rotation": 270}, "power2.out")
      + kv.pop_in("#bq4", 18.26) + kv.boil("#bq4", 18.5, E, 1.5, 0.4)
      + kv.pan("#lz4", 19.05, 0.5, 0, R)
      + kv.drop("#cll", 19.3, -280, -7) + kv.drop("#sel", 20.36, -360, 12) + kv.slap("#imp", 20.64, 1.5)
      + kv.hidden("#foto4") + kv.pose("#foto4", 18.9, {"opacity": 1})
      + boils([("rlr", S), ("esc", S), ("cel", S), ("cll", 19.5), ("sel", 20.6), ("foto4", 18.9)], E)
      + kv.fly_out("#cll", 21.28, -300, -1000, -16, 0.3) + kv.fly_out("#sel", 21.25, 500, -900, 25, 0.3)
      + kv.fly_out("#imp", 21.3, 200, -1100, 10, 0.3) + kv.fly_out("#foto4", 21.32, 600, -700, 20, 0.3)
      + sj + gj)
hosts.append(hf.scene("s04", S, E, CSS, body, js))

# ================================================================== 5. Subamos la oferta (21.62 – 32.12)
S, E = 21.62, 32.12
hf.OFFSET = S
l, j = say("p5", [(21.62, "Ahora,"), (22.24, "subamos"), (22.54, "la"), (22.68, "oferta.", "serif or kw")], 250, "tinta", 70)
q, qj = say("q5", [(30.64, "¿Cuánto"), (30.90, "le"), (31.00, "pagarías"), (31.0, "/"), (31.36, "ahora?", "serif or", "f")], 760, "", 100)
sh, sj = subs("sb5", [(23.36, 24.1, "¿Y si además fuera"), (24.12, 24.82, "tu community manager?"), (24.86, 26.45, "¿Y tu creadora de contenido?"),
                      (26.48, 28.0, "Que cada casa que cargás"), (28.02, 29.62, "tenga su reel, su carrusel"), (29.66, 30.55, "y sus historias.")])
bh, bj = kv.burst("ch", f"{IMG}/icono-chat.png", 23.75, 6, 1010, 900, spread=150, rise=340, size=74, seed=5)
ic5 = [("k1", "icono-chat", 290, 590), ("k2", "icono-camara", 410, 540), ("k3", "icono-pulgar", 550, 540), ("k4", "icono-nota", 670, 590)]
gh, gj = grain("g5", S, E)
body = ('<div id="col5" class="layer">'
        + kv.layer("l5f", kv.paper("white"))
        + kv.layer("l5s", kv.shape("c5", "circulo", 220, 650, 640) + kv.shape("t5", "trama", 40, 420, 380, "#000", 0.2), 2)
        + kv.layer("l5m", st("m5", "martina-espaldas", 270, 690, 540)
                   + "".join(st(c, n, x, y, 110) for c, n, x, y in ic5)
                   + st("lib5", "libreta-ficha", 30, 1250, 300) + st("alm5", "almohada", 740, 1290, 280)
                   + st("meg", "megafono", 640, 830, 390) + bh
                   + st("cla", "claqueta", 10, 820, 400)
                   + card("rc", "reel", "04-quincho-pileta", 80, 1050, 200, 380, -7, "Reel")
                   + card("cc", "carrusel", "02-living", 400, 1110, 270, 330, 2, "Carrusel")
                   + card("hc", "historia", "05-cocina", 770, 1050, 200, 380, 8, "Historias"), 3)
        + kv.tira("tr5a", "COMMUNITY MANAGER", 520, 740, "negra", 34, 9)
        + kv.tira("tr5b", "CREADORA DE CONTENIDO", 20, 1095, "negra", 34, 11)
        + kv.vignette() + '</div>'
        + l + sh + '<div id="dim5" class="dim"></div>' + f'<div style="position:absolute;inset:0;z-index:45">{q}</div>' + gh)
js = (j + off("#p5", 23.3)
      + kv.pop_in("#c5", 21.62) + kv.drop("#m5", 21.62, -200)
      + "".join(kv.pop_in(f"#{c}", 21.75 + i * 0.07, i == 0) for i, (c, *_r) in enumerate(ic5))
      + kv.pop_in("#lib5", 21.9, False) + kv.pop_in("#alm5", 22.0)
      + kv.drop("#meg", 23.36, -300, 10) + bj + kv.slap("#tr5a", 24.22)
      + kv.drop("#cla", 24.86, -300, -10) + kv.slap("#tr5b", 25.54)
      + kv.drop("#rc", 28.46, -220, -6) + kv.drop("#cc", 29.02, -220, 5) + kv.drop("#hc", 29.80, -220, 8)
      + boils([("m5", 21.9), ("lib5", 22.1), ("alm5", 22.1), ("meg", 23.6), ("cla", 25.1)] + [(c, 22.0) for c, *_r in ic5], E)
      + kv.boil("#rc", 28.7, E, 1.5, 0.5, seed=1) + kv.boil("#cc", 29.3, E, 1.5, 0.5, seed=2) + kv.boil("#hc", 30.0, E, 1.5, 0.5, seed=3)
      + kv.parallax([("#l5f", 0.3), ("#l5s", 0.6), ("#l5m", 1.0)], S, 30.6, dy=-20, ds=0.06)
      + sj
      + kv.hidden("#dim5") + hf.move("#dim5", 30.5, 0.3, {"opacity": 0}, {"opacity": 0.62}, hf.SOFT)
      + kv.rack("#col5", 30.5, 0.4, 12) + qj
      + hf.to("#q5", 31.4, 0.7, {"scale": 1.04}, hf.SLOW)
      + kv.focus_out("#q5", 31.85, 0.25) + gj)
hosts.append(hf.scene("s05", S, E, CSS + "\n#q53 { font-size: 170px; line-height: 1; }", body, js))

# ================================================================== 6. Se llama Martina (32.12 – 34.48)
S, E = 32.12, 34.48
hf.OFFSET = S
sh, sj = subs("sb6", [(32.12, 32.9, "Se llama Martina."), (32.92, 34.1, "Y ya trabaja en Cubiko.")])
gh, gj = grain("g6", S, E)
t_giro, t_frente = kv.beats(32.46, 3)[0], kv.beats(32.46, 3)[2]
body = ('<div id="all6" class="layer">'
        + kv.layer("l6f", kv.paper("white"))
        + kv.layer("l6s", kv.shape("c6", "circulo", 90, 560, 900) + kv.shape("t6", "trama", 0, 260, 420, "#000", 0.2)
                   + '<div id="lg6" class="patch pos" style="left:600px;top:250px;width:330px;transform:rotate(5deg)"><img src="assets/img/cubiko-logo-transparente.png"></div>', 2)
        + kv.layer("l6m", st("me", "martina-espaldas", 110, 330, 860) + st("mg", "martina-giro", 110, 330, 860) + st("mf", "martina-frente", 110, 330, 860), 3)
        + kv.tira("tr6", "MARTINA", 90, 1190, "naranja", 72, 13)
        + kv.vignette() + '</div>' + sh + gh)
js = (kv.pop_in("#c6", 32.12, False) + kv.slap("#me", 32.12, 1.08)
      + kv.hidden("#mg") + kv.hidden("#mf")
      + kv.pose("#mg", t_giro, {"opacity": 1}) + off("#me", t_giro)
      + kv.pose("#mf", t_frente, {"opacity": 1}) + off("#mg", t_frente)
      + kv.slap("#tr6", 32.46, 1.4) + kv.slap("#lg6", 33.86, 1.3)
      + boils([("me", 32.2), ("mg", t_giro), ("mf", t_frente)], E) + kv.boil("#lg6", 34.0, E, 2, 0.6)
      + kv.parallax([("#l6f", 0.3), ("#l6s", 0.6), ("#l6m", 1.0)], S, 34.0, dy=-10, ds=0.05)
      + sj + kv.push_through("#all6", 34.06, 0.42, 3.2) + gj)
hosts.append(hf.scene("s06", S, E, CSS + "\n#all6 { transform-origin: 50% 32%; }", body, js))

# ================================================================== 7. Vendedora (34.48 – 46.08)
S, E = 34.48, 46.08
hf.OFFSET = S
TH = [  # (id, html, y, t)
    ("m1", '<div class="bub in">¡Hola! ¿Sigue disponible la casa de Yerba Buena?</div>', 175, None),
    ("m2", '<div class="bub out">¡Hola Carla! Sí, está disponible. Te paso fotos y video.</div>', 365, 35.40),
    ("m4", '<div class="bub out">¿Querés verla el sábado a las 11?</div>', 865, 38.22),
    ("m5", '<div class="sys k"><span>Visita · Sáb 11:00 · A confirmar</span></div>', 1005, 38.90),
    ("m6", '<div class="sys"><span>Sin respuesta</span></div>', 1090, 39.74),
    ("m7", '<div class="bub out">Carla, ¿te quedó alguna duda? Te guardo el sábado a las 11.</div>', 1165, 42.24),
    ("m8", '<div class="bub in">¡Sí! El sábado voy.</div>', 1345, 42.95),
]
thread = "".join(f'<div id="{i}" style="position:absolute;left:0;top:{y}px;width:612px">{h}</div>' for i, h, y, _t in TH)
photos = [("02-living", 0, 0, 36.62), ("03-patio", 213, 0, 36.82), ("05-cocina", 0, 153, 36.92), ("04-quincho-pileta", 213, 153, 37.52)]
media = "".join(f'<div id="md{k}" class="ph" style="left:{x}px;top:{y}px"><img src="{CASA}/{p}.png">{"<div class=play></div>" if k == 3 else ""}</div>'
                for k, (p, x, y, _t) in enumerate(photos))
thread += f'<div class="media" style="top:545px">{media}</div>'
phone = (f'<div id="ph7" class="phone" style="left:220px;top:350px"><div class="scr">'
         f'<div class="hd"><div class="av">C</div><div><div class="hn">Carla</div><div class="ho">Instagram · ahora</div></div></div>'
         f'<div id="th7" class="thread">{thread}</div></div></div>')
rows = [("Consultó por", "Casa en Yerba Buena"), ("Operación", "Alquiler"), ("Canal", "Instagram"), ("Visita", "Sáb 11:00"), ("Estado", "En contacto")]
res = (f'<div id="rs7" class="pan" style="left:410px;top:560px;width:540px">'
       f'<div class="pt" style="font-size:36px;line-height:44px;padding:28px 32px 2px">Resumen para el asesor</div>'
       f'<div class="ps" style="padding:0 32px 18px">Martina · Carla</div>'
       + "".join(f'<div id="rr{i}" class="rr"><span>{a}</span><b>{b}</b></div>' for i, (a, b) in enumerate(rows)) + '</div>')
gh, gj = grain("g7", S, E)
body = ('<div id="all7" class="layer">' + kv.layer("l7f", kv.paper("white"), 0)
        + kv.shape("c7", "circulo", 120, 500, 860, kv.PEACH, 0.55)
        + phone + res + kv.tira("tr7", "VENDEDORA", 60, 240, "naranja", 48, 17) + '</div>' + gh)
js = (kv.focus_in("#ph7", 34.48, 0.4) + kv.slap("#tr7", 34.64, 1.3))
for i, h, y, t in TH:
    if t:
        js += hf.pop(f"#{i}", t)
for k, (_p, _x, _y, t) in enumerate(photos):
    js += hf.pop(f"#md{k}", t, 0.3, 20)
js += (hf.to("#th7", 39.6, 0.6, {"y": -480}, hf.SMOOTH)
       + hf.to("#ph7", 43.3, 0.8, {"x": -250, "scale": 0.84}, hf.SMOOTH)
       + kv.hidden("#rs7") + hf.move("#rs7", 44.3, 0.55, {"opacity": 0, "x": 620}, {"opacity": 1, "x": 0}, "expo.out"))
hf.snd(44.45, "whoosh")
for i in range(len(rows)):
    js += hf.rise(f"#rr{i}", 44.6 + i * 0.16, 0.28, i % 2 == 0)
js += kv.whip("#all7", 45.8, 0.3, -1080) + gj
hosts.append(hf.scene("s07", S, E, CSS, body, js))

# ================================================================== 8. Community manager (46.08 – 51.16)
S, E = 46.08, 51.16
hf.OFFSET = S
CH = [("Lucía Paz", "Depto 2 ambientes, Barrio Norte", "WhatsApp", 47.50), ("Carla Ríos", "Casa en Yerba Buena", "Instagram", 48.28),
      ("Diego Sosa", "Local en calle Mendoza", "Facebook", 49.10), ("Ana Ruiz", "Casa con pileta", "TikTok", 49.48)]
rws = ""
for i, (n, c, ch, _t) in enumerate(CH):
    rws += (f'<div id="cr{i}" class="row" style="top:{226 + i * 150}px"><div class="av g">{n[0]}</div>'
            f'<div><div class="nm">{n}</div><div class="cp">{c}</div></div>'
            f'<div class="chn">{ch}</div><div id="es{i}" class="est"><span class="e1">Nueva</span><span id="eo{i}" class="e2">En contacto</span></div></div>')
tb = (f'<div id="tb8" class="pan" style="left:60px;top:380px;width:900px;height:1000px">'
      f'<div class="pt">Consultas</div><div class="ps">Todo lo que entra por el sitio y lo que carga el equipo.</div>'
      f'<div class="cols"><span style="width:410px">Nombre</span><span style="width:206px">Canal</span><span>Estado</span></div>'
      f'<div style="position:absolute;left:0;right:0;top:0">{rws}</div></div>')
gh, gj = grain("g8", S, E)
body = ('<div id="all8" class="layer">' + kv.layer("l8f", kv.paper("white"), 0)
        + kv.shape("c8", "circulo", 520, 1000, 700, kv.PEACH, 0.55) + tb
        + kv.tira("tr8", "COMMUNITY MANAGER", 60, 240, "naranja", 48, 19) + '</div>' + gh)
js = hf.move("#all8", 46.08, 0.42, {"x": 1080}, {"x": 0}, "expo.out") + kv.slap("#tr8", 46.4, 1.3)
for i, (_n, _c, _ch, t) in enumerate(CH):
    js += kv.hidden(f"#cr{i}") + hf.move(f"#cr{i}", t, 0.32, {"opacity": 0, "x": 60}, {"opacity": 1, "x": 0}, "expo.out")
    hf.snd(t + 0.05, "pop")
    js += hf.move(f"#eo{i}", t + 0.55, 0.22, {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, hf.SOFT)
    hf.snd(t + 0.58, "key")
for i in range(4):
    js += hf.to(f"#es{i}", 50.06 + i * 0.08, 0.18, {"scale": 1.12}, hf.SOFT) + hf.to(f"#es{i}", 50.24 + i * 0.08, 0.25, {"scale": 1}, hf.SOFT)
js += kv.focus_out("#all8", 50.9, 0.26) + gj
hosts.append(hf.scene("s08", S, E, CSS, body, js))

# ================================================================== 9. Creadora de contenido (51.16 – 59.18)
S, E = 51.16, 59.18
hf.OFFSET = S
slots = "".join(f'<div class="slot"><img id="sl{i}" src="{CASA}/{p}.png"></div>' for i, p in enumerate(
    ["01-entrada", "02-living", "03-patio", "04-quincho-pileta", "05-cocina", "06-comedor"]))
fm = (f'<div id="fm9" class="pan" style="left:90px;top:360px;width:900px;height:1060px;transform-origin:50% 0">'
      f'<div class="pt">Nueva propiedad</div><div class="ps">Información principal</div>'
      f'<div class="fblk" style="top:170px"><div class="fl">Título</div><div class="fv"><span id="tt9">Casa con pileta en Yerba Buena</span></div></div>'
      f'<div class="fblk" style="top:300px"><div class="fl">Operación</div><div class="seg"><span>Venta</span><span class="on">Alquiler</span></div></div>'
      f'<div class="fblk" style="top:300px;left:470px"><div class="fl">Tipo</div><div class="fv">Casa</div></div>'
      f'<div class="fblk" style="top:440px"><div class="fl">Fotos</div></div>'
      f'<div class="slots" style="top:480px">{slots}</div>'
      f'<div id="pb9" class="btn" style="right:36px;bottom:36px">Publicar</div></div>')
SCR_CSS = """
#ph9w { position: absolute; left: 380px; top: 420px; width: 668px; height: 1208px; }
#ph9w .phone { left: 0; top: 0; transform: scale(.78); }
.scrn { position: absolute; left: 0; top: 0; width: 612px; height: 1152px; overflow: hidden; background: #fff; }
.scrn .cov { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.addr { position: absolute; left: 40px; right: 40px; top: 62px; height: 46px; border-radius: 23px; background: #EFEDE4; }
.wtt { font-weight: 800; font-size: 40px; line-height: 48px; color: #0B0B0B; letter-spacing: -0.02em; }
.wsb { font-weight: 600; font-size: 26px; line-height: 34px; color: #6E6A5C; margin-top: 8px; }
.wbt { display: inline-block; margin-top: 26px; padding: 18px 30px; border-radius: 18px; background: #0B0B0B; color: #fff; font-size: 28px; font-weight: 800; }
.grad { position: absolute; left: 0; right: 0; bottom: 0; height: 420px; background: linear-gradient(180deg, rgba(0,0,0,0), rgba(0,0,0,.7)); }
.tag { position: absolute; left: 34px; top: 66px; padding: 8px 18px; border-radius: 14px; background: rgba(0,0,0,.45); color: #fff; font-weight: 800; font-size: 26px; }
.capw { position: absolute; left: 34px; right: 34px; bottom: 70px; color: #fff; font-weight: 800; font-size: 34px; line-height: 42px; }
.hb { position: absolute; left: 24px; right: 24px; top: 40px; display: flex; gap: 8px; z-index: 3; }
.hb > div { flex: 1; height: 6px; border-radius: 3px; background: rgba(255,255,255,.45); overflow: hidden; }
.hb i { display: block; width: 100%; height: 100%; background: #fff; transform-origin: 0 50%; transform: scaleX(0); }
.flyp { position: absolute; width: 150px; height: 110px; object-fit: cover; border-radius: 10px; border: 5px solid #fff; box-shadow: 0 10px 20px rgba(0,0,0,.25); z-index: 12; }
"""
CAR = ["02-living", "05-cocina", "06-comedor"]
HIS = ["01-entrada", "05-cocina", "03-patio"]
screens = (
    '<div id="sw" class="scrn"><div class="addr"></div>'
    f'<div style="position:absolute;left:0;top:140px;width:612px;height:520px;overflow:hidden"><img class="cov" src="{CASA}/01-entrada.png"></div>'
    '<div style="position:absolute;left:40px;right:40px;top:700px"><div class="wtt">Casa con pileta en Yerba Buena</div>'
    '<div class="wsb">Alquiler · Casa · Fotos 6 · Video 1</div><div class="wbt">Consultar por WhatsApp</div></div></div>'
    f'<div id="sr" class="scrn"><img id="sri" class="cov" src="{CASA}/04-quincho-pileta.png"><img id="sri2" class="cov" src="{CASA}/03-patio.png">'
    '<div class="grad"></div><div class="tag">Reel</div><div class="play" style="width:110px;height:110px;margin:-55px 0 0 -55px"></div>'
    '<div class="capw">Casa con pileta en Yerba Buena</div></div>'
    '<div id="sc" class="scrn" style="background:#F7F4F0"><div class="hd" style="height:150px"><div class="av">C</div><div><div class="hn">Carrusel</div><div class="ho">Casa con pileta en Yerba Buena</div></div></div>'
    '<div style="position:absolute;left:0;top:190px;width:612px;height:612px;overflow:hidden">'
    f'<div id="scs" style="position:absolute;left:0;top:0;width:1836px;height:612px;display:flex">{"".join(f"<img src={chr(34)}{CASA}/{p}.png{chr(34)} style={chr(34)}width:612px;height:612px;object-fit:cover;display:block{chr(34)}>" for p in CAR)}</div></div>'
    '<div style="position:absolute;left:0;right:0;top:830px;text-align:center"><span style="position:relative;display:inline-block;width:96px;height:14px">'
    '<i style="position:absolute;left:0;width:14px;height:14px;border-radius:50%;background:#CFCBBE"></i><i style="position:absolute;left:41px;width:14px;height:14px;border-radius:50%;background:#CFCBBE"></i>'
    '<i style="position:absolute;left:82px;width:14px;height:14px;border-radius:50%;background:#CFCBBE"></i><i id="scd" style="position:absolute;left:0;width:14px;height:14px;border-radius:50%;background:#0B0B0B"></i></span></div>'
    '<div style="position:absolute;left:36px;right:36px;top:890px" class="wsb">Living, cocina y comedor. Escribinos para coordinar la visita.</div></div>'
    '<div id="sh" class="scrn">' + "".join(f'<img id="sh{i}" class="cov" src="{CASA}/{p}.png">' for i, p in enumerate(HIS))
    + '<div class="hb">' + "".join(f'<div><i id="hb{i}"></i></div>' for i in range(3)) + '</div>'
    '<div class="grad"></div><div class="tag" style="top:80px">Historias</div><div class="capw">Casa con pileta en Yerba Buena</div></div>')
phone9 = f'<div id="ph9w"><div class="phone"><div class="scr">{screens}</div></div></div>'
FLY = [("01-entrada", 160, 560, 0.0), ("03-patio", 250, 610, 0.08), ("05-cocina", 190, 660, 0.16)]
fly = "".join(f'<img id="fp{i}" class="flyp" src="{CASA}/{p}.png" style="left:{x}px;top:{y}px">' for i, (p, x, y, _d) in enumerate(FLY))
arrow = kv.stroke("ar9", "M14 14 Q20 170 190 186 M160 160 L190 186 L156 214", 250, 800, 230, 240, "#0B0B0B", 7)
FMT = [("Web", 54.54, 55.9), ("Reel", 55.9, 56.5), ("Carrusel", 56.5, 57.3), ("Historias", 57.3, E)]
tiras = "".join(kv.tira(f"fm{i}", t, 80, 1250, "negra", 56, 31 + i) for i, (t, _a, _b) in enumerate(FMT))
l, j = say("p9", [(58.16, "En"), (58.32, "un"), (58.46, "clic.", "serif or kw", "f")], 1520, "tinta", 80)
gh, gj = grain("g9", S, E)
body = ('<div id="st9" class="layer">' + kv.layer("l9f", kv.paper("white"), 0)
        + kv.shape("c9", "circulo", 260, 640, 760, kv.PEACH, 0.6) + fm
        + f'<div id="cu9" class="cur">{CURSOR}</div>' + phone9 + fly + arrow + tiras
        + '</div>' + kv.tira("tr9", "CREADORA DE CONTENIDO", 60, 240, "naranja", 48, 23) + l + kv.vignette() + gh)
js = (kv.focus_in("#fm9", 51.16, 0.4) + kv.slap("#tr9", 51.42, 1.3)
      + hf.move("#tt9", 52.74, 0.3, {"opacity": 0, "x": -20}, {"opacity": 1, "x": 0}, hf.SOFT))
hf.snd(52.77, "key")
for i in range(6):
    js += hf.move(f"#sl{i}", 53.0 + i * 0.07, 0.25, {"opacity": 0, "scale": 1.3}, {"opacity": 1, "scale": 1}, hf.SOFT)
hf.snd(53.05, "pop")
js += (hf.move("#cu9", 53.2, 0.55, {"opacity": 0, "x": 520, "y": 1240}, {"opacity": 1, "x": 880, "y": 1385}, "power3.out")
       + hf.to("#cu9", 53.86, 0.08, {"scale": 0.82}, hf.SOFT) + hf.to("#cu9", 53.94, 0.12, {"scale": 1}, hf.SOFT)
       + hf.to("#pb9", 53.86, 0.08, {"scale": 0.94}, hf.SOFT) + hf.to("#pb9", 53.94, 0.16, {"scale": 1}, hf.SOFT)
       + hf.to("#cu9", 54.1, 0.2, {"opacity": 0}, hf.SOFT)
       + hf.to("#fm9", 54.15, 0.55, {"scale": 0.38, "x": -250}, "expo.inOut")
       + kv.focus_in("#ph9w", 54.3, 0.4, 16, 1.08, False))
hf.snd(53.88, "key")
hf.snd(54.35, "whoosh")
for i, (_p, x, y, d) in enumerate(FLY):
    js += (kv.hidden(f"#fp{i}") + kv.pose(f"#fp{i}", 54.3 + d, {"opacity": 1})
           + hf.to(f"#fp{i}", 54.34 + d, 0.55, {"x": 690 - x, "y": 900 - y, "scale": 0.25, "rotation": 12, "opacity": 0}, "power2.in"))
js += kv.marker("#ar9 path", 54.4, 0.4, False)
for i, (_t, a, b) in enumerate(FMT):
    js += kv.slap(f"#fm{i}", a, 1.3) + (off(f"#fm{i}", b) if b < E else "")
for sid, t in (("#sr", 55.9), ("#sc", 56.5), ("#sh", 57.3)):
    js += kv.hidden(sid) + hf.move(sid, t, 0.34, {"opacity": 1, "x": 612}, {"x": 0}, "expo.inOut")
    hf.snd(t + 0.12, "whoosh")
js += (hf.to("#sri", 55.9, 1.6, {"scale": 1.18}, hf.SLOW) + kv.hidden("#sri2") + kv.pose("#sri2", 56.22, {"opacity": 1})
       + hf.to("#sri2", 56.22, 1.0, {"scale": 1.12}, hf.SLOW)
       + hf.to("#scs", 56.85, 0.24, {"x": -612}, "power3.inOut") + hf.to("#scd", 56.85, 0.24, {"x": 41}, "power3.inOut")
       + hf.to("#scs", 57.1, 0.24, {"x": -1224}, "power3.inOut") + hf.to("#scd", 57.1, 0.24, {"x": 82}, "power3.inOut")
       + kv.hidden("#sh1") + kv.hidden("#sh2"))
hf.snd(56.86, "key")
hf.snd(57.11, "key")
for i, (a, b) in enumerate(((57.3, 57.75), (57.75, 58.2), (58.2, 59.1))):
    js += hf.move(f"#hb{i}", a, b - a, {"scaleX": 0}, {"scaleX": 1}, "none")
    if i:
        js += kv.pose(f"#sh{i}", a, {"opacity": 1})
js += (hf.to("#st9", 54.8, 3.2, {"scale": 1.04}, hf.SLOW) + kv.rack("#st9", 58.05, 0.3, 6) + j + gj)
hosts.append(hf.scene("s09", S, E, CSS + SCR_CSS + "\n#st9 { transform-origin: 50% 40%; } #p92 { font-size: 150px; }", body, js))

# ================================================================== 10. Domingo, resuelto (59.18 – 65.12)
S, E = 59.18, 65.12
hf.OFFSET = S
sh, sj = subs("sb10", [(59.18, 60.9, "Domingo, once de la noche."), (60.96, 61.95, "Carla escribe."), (62.0, 63.2, "Martina contesta."), (63.24, 65.0, "El sábado, Carla va a verla.")])
gh, gj = grain("g10", S, E)
body = ('<div id="lz10" class="layer" style="width:2160px">'
        + f'<img class="paperx" src="assets/img/paper-cuadriculado.png" style="left:0"><img class="paperx" src="assets/img/paper-white.png" style="left:{R}px">'
        + kv.shape("c10", "circulo", 40, 700, 760)
        + st("cs10", "carla-sillon", 30, 700, 640)
        + bub("bq10", "¡Hola! ¿Sigue disponible la casa de Yerba Buena?", 380, 380, 580, "wh", "Instagram · 23:07")
        + bub("br10", "¡Hola Carla! Sí. Te paso fotos y video. ¿Querés verla el sábado?", 300, 640, 640, "o", "Martina · 23:07")
        + kv.tira("tr10", "DOMINGO · 23:07", 80, 250, "negra", 46, 5)
        + kv.shape("c10b", "circulo", R + 140, 500, 800)
        + st("foto10", "../img/casa/01-entrada", R + 440, 380, 500, "bn")
        + st("cl10", "carla-llaves", R + 60, 500, 740)
        + kv.tira("tr10b", "SÁBADO · 11:00", R + 80, 250, "negra", 46, 29)
        + '</div>' + kv.vignette() + sh + gh)
js = (kv.slap("#tr10", 59.18) + kv.drop("#cs10", 59.3, -280, 6) + kv.pop_in("#bq10", 60.96) + kv.pop_in("#br10", 62.0)
      + kv.boil("#bq10", 61.2, E, 1.5, 0.4) + kv.boil("#br10", 62.2, E, 1.5, 0.4)
      + kv.pan("#lz10", 63.0, 0.5, 0, R)
      + kv.hidden("#foto10") + kv.pose("#foto10", 62.9, {"opacity": 1})
      + kv.drop("#cl10", 63.3, -260, -7) + kv.slap("#tr10b", 63.4)
      + boils([("cs10", 59.5), ("foto10", 62.9), ("cl10", 63.5)], E) + sj + gj)
hosts.append(hf.scene("s10", S, E, CSS, body, js))

# ================================================================== 11. Y vos… dormiste (65.12 – 66.54)
S, E = 65.12, 66.54
hf.OFFSET = S
l, j = say("p11", [(65.12, "Y"), (65.20, "vos…"), (66.02, "dormiste.", "serif or kw")], 250, "", 80)
nts = [("n1", "<b>●</b> Consulta respondida", 65.35, 420), ("n2", "<b>●</b> Visita · Sáb 11:00", 65.5, 510), ("n3", "<b>●</b> Seguimiento enviado", 65.65, 600)]
gh, gj = grain("g11", S, E, True)
body = (kv.layer("l11f", kv.paper("black"))
        + kv.layer("l11m", st("du", "duenio-durmiendo", 120, 500, 600) + st("esc11", "escritorio", 60, 1120, 960)
                   + st("cel11", "celular-boca-arriba", 560, 1150, 330)
                   + "".join(f'<div id="{i}" class="notif" style="left:500px;top:{y}px">{t}</div>' for i, t, _a, y in nts), 2)
        + l + kv.vignette() + gh)
js = (j + kv.pop_in("#du", 65.12, False) + "".join(kv.pop_in(f"#{i}", a) for i, _t, a, _y in nts)
      + boils([("du", 65.2), ("esc11", S), ("cel11", S)], E)
      + kv.parallax([("#l11f", 0.3), ("#l11m", 1.0)], S, E, dy=-10, ds=0.04) + gj)
hosts.append(hf.scene("s11", S, E, CSS, body, js))

# ================================================================== 12. CTA (66.54 – 69.6)
S, E = 66.54, END
hf.OFFSET = S
l, j = say("p12", [(66.54, "Escribinos"), (66.6, "/"), (67.40, "CUBIKO", "serif or", "f"), (67.5, "/"), (67.80, "por"), (67.96, "WhatsApp"), (68.0, "/"),
                   (68.26, "y"), (68.54, "probalo"), (68.6, "/"), (68.90, "GRATIS.", "", "s")], 640, "", 84)
gh, gj = grain("g12", S, E, True)
body = '<div class="placa"></div>' + l + '<img id="lo12" src="assets/img/cubiko-logo-transparente.png" style="position:absolute;left:450px;top:1300px;width:180px">' + gh
js = j + kv.pop_in("#lo12", 67.6) + hf.to("#p12", 67.0, 2.6, {"scale": 1.04}, hf.SLOW) + gj
hosts.append(hf.scene("s12", S, E, CSS + "\n#p121 { font-size: 200px; line-height: 1.05; } #p126 { font-size: 150px; }", body, js))

hf.index(hosts)
hf.save_events()
print(f"{len(hosts)} escenas, {len(hf.EVENTS)} sonidos")
