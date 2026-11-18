# Genera fondos de marca en assets/img/.
# Uso: make_bg.py --size 1080x1920 --style plano  (negro, blanco y naranja con grid de 120 px)
#      make_bg.py --size 1920x1080 --style grano  (grainy fade + grid: explainers y VSL)
import argparse
import os
import subprocess

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--size", default="1080x1920")
ap.add_argument("--style", choices=["plano", "grano"], default="grano")
ap.add_argument("--out", default="assets/img")
args = ap.parse_args()
W, H = (int(v) for v in args.size.split("x"))
CELL = 120
os.makedirs(args.out, exist_ok=True)

BLACK, DEEP, ORANGE, AMBER, BROWN = [7, 9, 10], [114, 43, 15], [250, 93, 0], [255, 156, 28], [62, 27, 19]
PAPER, WARM, PEACH = [248, 248, 245], [246, 142, 88], [250, 191, 154]
FLAT = {"black": [11, 11, 11], "white": [242, 242, 240], "orange": ORANGE}


def color(rgb):
    return np.array(rgb, np.float32)


def mix(a, b, t):
    return a + (b - a) * t[..., None]


def blob(u, v, x, y, rx, ry):
    return np.exp(-((u - x) ** 2 / rx ** 2 + (v - y) ** 2 / ry ** 2) * 2)


def field(theme, seed):
    v, u = np.mgrid[0:H, 0:W].astype(np.float32)
    u, v = u / W, v / H
    phase = (seed % 100) / 100 * 1.8
    a = u + 0.09 * np.sin(v * 5 + phase)
    b = v + 0.065 * np.sin(u * 5 - phase)
    base = np.ones((H, W, 3), np.float32)
    if theme == "black":
        radius = np.hypot((a - 1.1) / 1.04, (b - 0.15) / 0.93)
        band = np.exp(-(((radius - 0.9) / 0.115) ** 2))
        out = mix(base * color(BLACK), color(DEEP), blob(a, b, 0.98, 0.79, 0.65, 0.65) * 0.85)
        ramp = np.clip((v - 0.33) / 0.52, 0, 1)
        return mix(out, color(ORANGE), band * 0.84 * ramp * ramp * (3 - 2 * ramp))
    if theme == "white":
        out = mix(base * color(PAPER), color(WARM), blob(a, b, 1.05, 0.98, 0.72, 0.5) * 0.74)
        out = mix(out, color(PEACH), blob(a, b, 0.08, 1.12, 0.62, 0.3) * 0.42)
        return mix(out, color([85, 64, 58]), blob(a, b, 1.14, 1.25, 0.5, 0.36) * 0.7)
    radius = np.hypot((a - 1.13) / 1.12, (b - 0.1) / 1.05)
    band = np.exp(-(((radius - 0.86) / 0.075) ** 2))
    dark = blob(a, b, 1.05, 1.07, 0.65, 0.47) + blob(a, b, 1.2, 0.02, 0.4, 0.55) * 0.65
    out = mix(base * color(ORANGE), color(BROWN), np.clip(dark, 0, 1) * 0.92)
    return mix(out, color(AMBER), band * 0.78)


def grid(img, theme):
    line, alpha = (255.0, 0.18) if theme == "black" else (0.0, 0.12)
    mask = np.zeros((H, W), np.float32)
    x0, y0 = (W // 2) % CELL, (H // 2) % CELL
    mask[:, x0::CELL] = alpha
    mask[y0::CELL, :] = alpha
    return img + (line - img) * mask[..., None]


def grain(img, theme, seed):
    rng = np.random.default_rng(seed)
    amount = 15 if theme == "white" else 22
    noise = rng.random((H, W, 3), np.float32) + rng.random((H, W, 3), np.float32) + rng.random((H, W, 3), np.float32)
    return img + (noise - 1.5) * amount


def save(name, img):
    out = np.clip(img, 0, 255).astype(np.uint8)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", f"{args.out}/{name}.png"]
    subprocess.run(cmd, input=out.tobytes(), check=True)
    print(name)


if args.style == "plano":
    for theme, rgb in FLAT.items():
        save(f"bg-{theme}", grid(np.ones((H, W, 3), np.float32) * color(rgb), theme))
else:
    for name, theme, seed, flip in [("bg-white-a", "white", 21, False), ("bg-white-b", "white", 62, True), ("bg-black", "black", 48, False), ("bg-orange", "orange", 77, False)]:
        img = field(theme, seed)
        if flip:
            img = img[::-1, ::-1]
        save(name, grain(grid(img, theme), theme, seed))
