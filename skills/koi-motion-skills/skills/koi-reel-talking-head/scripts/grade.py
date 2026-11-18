# Colorea un talking head: HLG a SDR, look cálido y aclarado suave de las ojeras.
# Se levanta solo la piel más oscura que su entorno, así ojos, cejas y barba quedan como están.
# Uso: grade.py <clip.mp4> [salida.mp4]        video completo
#      grade.py --test cuadro.png salida.png   prueba sobre un cuadro
# Para clips HDR, crear antes assets/build/hlg709.cube con make_hlg_lut.py.
import subprocess
import sys

import torch
import torch.nn.functional as F

W, H = 1080, 1920
HDR = "scale=in_color_matrix=bt2020:in_range=limited:out_range=full,format=gbrp16le,lut3d=assets/build/hlg709.cube,format=gbrp"
LOOK = "curves=r='0/0.01 0.14/0.15 0.34/0.35 0.64/0.65 1/0.95':g='0/0.015 0.14/0.145 0.34/0.335 0.64/0.615 1/0.91':b='0/0.03 0.14/0.15 0.34/0.32 0.64/0.56 1/0.84',eq=saturation=1.02"
STRENGTH = 0.72


def box(x, radius):
    k = 2 * radius + 1
    return F.avg_pool2d(F.pad(x, (radius,) * 4, mode="replicate"), k, 1)


def soft(x, low, high):
    t = ((x - low) / (high - low)).clamp(0, 1)
    return t * t * (3 - 2 * t)


def dodge(rgb):
    """rgb: 1×3×H×W in 0..1."""
    r, g, b = rgb[:, :1], rgb[:, 1:2], rgb[:, 2:3]
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    cb = (b - y) / 1.8556
    cr = (r - y) / 1.5748
    skin = soft(cr, 0.015, 0.05) * (1 - soft(cr, 0.16, 0.22)) * (1 - soft(cb, -0.01, 0.03)) * soft(y, 0.2, 0.3)
    # Only the head: the top half of the frame, away from the arms.
    rows = torch.linspace(0, 1, H).view(1, 1, H, 1)
    skin = skin * (1 - soft(rows, 0.36, 0.42))
    small = F.interpolate(torch.cat([y, skin], 1), scale_factor=0.25, mode="area")
    local = box(box(small[:, :1], 8), 8)
    mask = box(small[:, 1:], 3)
    local = F.interpolate(local, size=(H, W), mode="bilinear", align_corners=False)
    mask = F.interpolate(mask, size=(H, W), mode="bilinear", align_corners=False)
    deficit = (local - y).clamp(min=0)
    gain = 1 + STRENGTH * deficit * mask / y.clamp(min=0.05)
    out = rgb * gain.clamp(max=1.7)
    # Dark circles lean cold: warm them slightly where the lift happens.
    amount = (deficit * mask * 3).clamp(0, 1)
    out = out * torch.tensor([1.0, 1.0, 0.97]).view(1, 3, 1, 1) ** amount
    return out.clamp(0, 1)


if len(sys.argv) == 4 and sys.argv[1] == "--test":
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[2], "-vf", f"{LOOK},format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    x = torch.frombuffer(bytearray(raw), dtype=torch.uint8).view(H, W, 3).permute(2, 0, 1)[None].float() / 255
    o = (dodge(x)[0].permute(1, 2, 0) * 255).round().byte().numpy().tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", sys.argv[3]], input=o, check=True)
    sys.exit()

SOURCE = sys.argv[1]
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "assets/base.mp4"
transfer = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "csv=p=0", SOURCE], capture_output=True, text=True).stdout.strip(" ,\n")
PREFIX = f"{HDR}," if transfer == "arib-std-b67" else ""
read = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SOURCE, "-vf", f"{PREFIX}scale={W}:{H}:flags=lanczos,{LOOK},format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
write = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-g", "30", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", OUTPUT], stdin=subprocess.PIPE)
size = W * H * 3
n = 0
while True:
    raw = read.stdout.read(size)
    if len(raw) < size:
        break
    x = torch.frombuffer(bytearray(raw), dtype=torch.uint8).view(H, W, 3).permute(2, 0, 1)[None].float() / 255
    write.stdin.write((dodge(x)[0].permute(1, 2, 0) * 255).round().byte().numpy().tobytes())
    n += 1
write.stdin.close()
write.wait()
print("cuadros:", n)
