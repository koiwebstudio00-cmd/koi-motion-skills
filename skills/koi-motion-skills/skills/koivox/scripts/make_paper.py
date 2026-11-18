# Genera las texturas de Koivox en assets/img/. Necesita numpy (sirve el Python de ~/.venvs/whisper).
# Uso: make_paper.py [--size 1080x1920] [--out assets/img] [--grid]
# Salen:
#   paper-white / paper-black / paper-orange  papel con fibras, manchas y pliegues
#   paper-cuadriculado                         papel cuadriculado claro con viñeta (R4)
#   grain-dark / grain-light                   grano con transparencia, más grande que el cuadro para kv.grain()
#   halftone / cuadricula                      parches de trama de puntos y de hoja cuadriculada para kv.shape() (R2)
import argparse
import os
import subprocess

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--size", default="1080x1920")
ap.add_argument("--out", default="assets/img")
ap.add_argument("--grid", action="store_true", help="suma el grid de 120 px de Koi")
args = ap.parse_args()
W, H = (int(v) for v in args.size.split("x"))
PAD = 120
os.makedirs(args.out, exist_ok=True)
rng = np.random.default_rng(7)

PAPERS = {"white": [242, 242, 240], "black": [11, 11, 11], "orange": [250, 93, 0]}


def blur(a, r):
    """Desenfoque de caja separable, sin dependencias."""
    k = np.ones(2 * r + 1, np.float32) / (2 * r + 1)
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)
    return np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)


def noise(h, w, scale):
    """Ruido suave: ruido chico agrandado y desenfocado."""
    small = rng.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    big = np.kron(small, np.ones((scale, scale), np.float32))[:h, :w]
    return blur(big, max(1, scale // 2))


def fibers(h, w, count):
    m = np.zeros((h, w), np.float32)
    for _ in range(count):
        x, y = rng.random() * w, rng.random() * h
        ang, length = rng.random() * np.pi, 10 + rng.random() * 50
        for t in np.linspace(0, length, int(length)):
            xi, yi = int(x + np.cos(ang) * t), int(y + np.sin(ang) * t)
            if 0 <= xi < w and 0 <= yi < h:
                m[yi, xi] += 1
    return np.clip(m, 0, 1)


def save(name, img, mode):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", mode, "-s", f"{img.shape[1]}x{img.shape[0]}", "-i", "-", f"{args.out}/{name}.png"]
    subprocess.run(cmd, input=np.clip(img, 0, 255).astype(np.uint8).tobytes(), check=True)
    print(name)


v, u = np.mgrid[0:H, 0:W].astype(np.float32)
vignette = np.clip(np.hypot((u / W - 0.5) * 1.2, v / H - 0.5) * 1.6, 0, 1) ** 2
mottle = noise(H, W, 60) - 0.5
fine = noise(H, W, 4) - 0.5
fib = fibers(H, W, 900)


def crease_map(h, w, count):
    """Pliegues de papel arrugado: líneas largas con un lado claro y otro oscuro."""
    m = np.zeros((h, w), np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for _ in range(count):
        x0, y0, ang = rng.random() * w, rng.random() * h, rng.random() * np.pi
        d = (xx - x0) * np.sin(ang) - (yy - y0) * np.cos(ang)
        along = (xx - x0) * np.cos(ang) + (yy - y0) * np.sin(ang)
        reach = np.exp(-(along / (w * (0.25 + rng.random() * 0.4))) ** 2)
        m += np.tanh(d / 2.5) * np.exp(-np.abs(d) / 14) * reach * (0.5 + rng.random())
    return m


creases = crease_map(H, W, 9)

for theme, rgb in PAPERS.items():
    base = np.ones((H, W, 3), np.float32) * np.array(rgb, np.float32)
    dark = theme == "black"
    tone = mottle * (18 if dark else 13) + fine * (14 if dark else 10)
    tone += fib * (16 if dark else -14)
    tone -= vignette * (10 if dark else 34)
    tone += creases * (10 if dark else 9)
    img = base + tone[..., None]
    if args.grid:
        line, alpha = (255.0, 0.12) if dark else (0.0, 0.08)
        mask = np.zeros((H, W), np.float32)
        mask[:, (W // 2) % 120::120] = alpha
        mask[(H // 2) % 120::120, :] = alpha
        img += (line - img) * mask[..., None]
    save(f"paper-{theme}", img, "rgb24")

GH, GW = H + 2 * PAD, W + 2 * PAD
specks = rng.random((GH, GW)).astype(np.float32)
dust = (rng.random((GH, GW)) > 0.9993).astype(np.float32)
dust = np.clip(blur(dust, 1) * 4, 0, 1)
alpha = np.clip((np.abs(specks - 0.5) * 2) ** 3 * 70 + dust * 160, 0, 255)
for name, value in [("grain-dark", 0), ("grain-light", 255)]:
    rgba = np.zeros((GH, GW, 4), np.float32)
    rgba[..., :3] = value
    rgba[..., 3] = alpha
    save(name, rgba, "rgba")

# Papel cuadriculado claro con viñeta (R4)
img = np.ones((H, W, 3), np.float32) * np.array([244, 244, 242], np.float32)
img += (mottle * 8 + fine * 6)[..., None]
mask = np.zeros((H, W), np.float32)
mask[:, (W // 2) % 90::90] = 0.10
mask[(H // 2) % 90::90, :] = 0.10
img += (60 - img) * mask[..., None]
img -= (vignette * 70)[..., None]
save("paper-cuadriculado", img, "rgb24")

# Trama de puntos que se desvanece hacia un lado (R2)
S = 600
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
cell = 9
cx, cy = (xx % cell) - cell / 2, (yy % cell) - cell / 2
radius = (cell / 2) * np.clip(1 - xx / S * 0.9 + (noise(S, S, 40) - 0.5) * 0.6, 0, 1)
dots = np.clip(radius - np.hypot(cx, cy) + 0.5, 0, 1)
rgba = np.zeros((S, S, 4), np.float32)
rgba[..., 3] = dots * 235
save("halftone", rgba, "rgba")

# Parche de hoja cuadriculada (R2)
rgba = np.zeros((S, S, 4), np.float32)
rgba[..., :3] = [250, 250, 248]
rgba[..., 3] = 235
lines = np.zeros((S, S), np.float32)
lines[:, ::24] = 1
lines[::24, :] = 1
rgba[..., :3] -= (lines * 70)[..., None] * np.array([0.9, 0.6, 0.2])
save("cuadricula", rgba, "rgba")

# Tinta de sello gastada: máscara alfa para kv.sello() (sello naranja con huecos, no un cartel liso)
SH, SW = 300, 900
blot = noise(SH, SW, 3)
rgba = np.zeros((SH, SW, 4), np.float32)
rgba[..., :3] = 255
rgba[..., 3] = np.where((blot > 0.32) & (rng.random((SH, SW)) > 0.12), 255, 0)
save("stamp-mask", rgba, "rgba")
