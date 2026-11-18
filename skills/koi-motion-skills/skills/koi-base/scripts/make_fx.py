# Coloca los efectos de sonido sin repetir nunca el mismo archivo dos veces seguidas.
# Lee assets/build/fx_plan.json y escribe assets/build/fx.wav. Uso: make_fx.py <duracion_s>
#
# Formato de fx_plan.json:
# {
#   "events": [[1.2, "key"], [2.0, "whoosh"], [3.1, "pop"]],
#   "risers": [[12.4, "riser-a", 0.9, -18.0]],   tiempo del pico, archivo, segundos antes del pico, nivel
#   "drops":  [[12.5, "boom", -16.0]]            tiempo, archivo, nivel
# }
# Los archivos van en assets/sfx/ como key-a.mp3, whoosh-a.mp3, pop-a.mp3, run-a.mp3. El prefijo define el tipo.
import glob
import json
import os
import subprocess
import sys

import numpy as np

SR, FPS = 44100, 30
SFX = "assets/sfx"
LENGTH = float(sys.argv[1])
LEVEL = {"key": -11.0, "whoosh": -6.0, "pop": -10.0, "run": -15.0}
TAIL = {"key": 0.1, "whoosh": 0.3, "pop": 0.12, "run": 0.55}

plan = json.load(open("assets/build/fx_plan.json"))
events = sorted(tuple(e) for e in plan.get("events", []))
pools = {kind: sorted(os.path.basename(p)[:-4] for p in glob.glob(f"{SFX}/{kind}-*.mp3")) for kind in LEVEL}
for kind in {k for _, k in events}:
    if len(pools.get(kind, [])) < 2:
        sys.exit(f"Hacen falta al menos 2 archivos {kind}-*.mp3 en {SFX} para no repetir")


def load(name):
    cmd = ["ffmpeg", "-v", "error", "-i", f"{SFX}/{name}.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def prepare(name, peak_db, tail, head=None):
    audio = load(name)
    env = np.abs(audio).max(axis=1)
    win = int(SR * 0.01)
    smooth = np.convolve(env, np.ones(win) / win, mode="same")
    peak = int(smooth.argmax())
    end = min(len(audio), peak + int(tail * SR))
    begin = max(0, peak - int(head * SR)) if head else 0
    clip = audio[begin:end]
    peak -= begin
    fade = min(int(0.03 * SR), len(clip))
    clip[-fade:] *= np.linspace(1, 0, fade)[:, None]
    if head:
        clip[:fade] *= np.linspace(0, 1, fade)[:, None]
    clip *= 10 ** (peak_db / 20) / max(float(np.abs(clip).max()), 1e-6)
    return clip, peak


def place(bus, clip, peak, at):
    start = int((at + 1 / FPS) * SR) - peak
    if start < 0:
        clip, start = clip[-start:], 0
    room = len(bus) - start
    if room > 0:
        bus[start:start + min(room, len(clip))] += clip[:room]


bus = np.zeros((int(SR * LENGTH), 2), np.float32)
placed = []
for at, name, head, level in plan.get("risers", []):
    placed.append((at, name, level, 0.05, head))
for at, name, level in plan.get("drops", []):
    placed.append((at, name, level, 0.9, None))

# Se ordenan todos juntos: la regla mira los tipos mezclados, no cada lista por separado.
timeline = sorted([(at, kind, None) for at, kind in events] + [(p[0], None, p) for p in placed], key=lambda x: x[0])
played, turn = [], {k: 0 for k in pools}
for index, (at, kind, fixed) in enumerate(timeline):
    if fixed:
        _, name, level, tail, head = fixed
        place(bus, *prepare(name, level, tail, head), at)
    else:
        pool = pools[kind]
        name = pool[turn[kind] % len(pool)]
        turn[kind] += 1
        following = timeline[index + 1][2][1] if index + 1 < len(timeline) and timeline[index + 1][2] else None
        if name in (played[-1][1] if played else None, following):
            name = next(n for n in pool[turn[kind] % len(pool):] + pool if n not in (played[-1][1] if played else None, following))
            turn[kind] += 1
        place(bus, *prepare(name, LEVEL[kind], TAIL[kind]), at)
    played.append((at, name))

repeats = [(a, b) for a, b in zip(played, played[1:]) if a[1] == b[1]]
assert not repeats, f"efecto repetido: {repeats}"

cmd = ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", "assets/build/fx.wav"]
subprocess.run(cmd, input=bus.tobytes(), check=True)
print("efectos colocados:", len(played), "- sin repetidos seguidos")
