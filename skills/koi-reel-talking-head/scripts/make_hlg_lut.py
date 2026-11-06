# Crea un LUT 3D que convierte HLG BT.2020 a SDR BT.709. Se usa cuando el clip es HDR.
# Este ffmpeg no trae el filtro zscale, por eso la conversión se calcula acá.
# Uso: make_hlg_lut.py <salida.cube>
import sys

import numpy as np

SIZE = 65
A, B, C = 0.17883277, 0.28466892, 0.55991073
PEAK, WHITE = 1000.0, 203.0
KNEE = 0.72
TO_709 = np.array(
    [[1.6605, -0.5876, -0.0728], [-0.1246, 1.1329, -0.0083], [-0.0182, -0.1006, 1.1187]]
)
LUMA_2020 = np.array([0.2627, 0.6780, 0.0593])


def hlg_inverse(v):
    return np.where(v <= 0.5, v * v / 3, (np.exp((v - C) / A) + B) / 12)


def shoulder(x):
    """Keeps values below the knee and rolls highlights off towards 1."""
    over = np.maximum(x - KNEE, 0) / (1 - KNEE)
    return np.where(x <= KNEE, x, KNEE + (1 - KNEE) * (over / (1 + over)))


def oetf(x):
    x = np.clip(x, 0, 1)
    return np.where(x < 0.018, 4.5 * x, 1.099 * x ** 0.45 - 0.099)


axis = np.linspace(0, 1, SIZE)
b, g, r = np.meshgrid(axis, axis, axis, indexing="ij")
rgb = np.stack([r, g, b], axis=-1).reshape(-1, 3)

scene = hlg_inverse(rgb)
luma = np.maximum(scene @ LUMA_2020, 1e-6)
display = scene * (luma ** 0.2)[:, None] * PEAK / WHITE
linear = np.clip(display @ TO_709.T, 0, None)
out = oetf(shoulder(linear))

with open(sys.argv[1], "w") as f:
    f.write(f"LUT_3D_SIZE {SIZE}\n")
    np.savetxt(f, out, fmt="%.6f")
print("LUT lista", sys.argv[1])
