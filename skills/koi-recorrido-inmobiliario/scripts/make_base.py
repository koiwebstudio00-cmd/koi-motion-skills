"""Arma assets/build/base.mp4: tomas con rampas de velocidad, color, títulos 3D pegados y transiciones.
Rampa: cada cuadro final promedia los cuadros de origen que recorre, así que la velocidad genera motion blur real.
Se configura con shots.json en la carpeta del proyecto (ver ejemplo-shots.json). Necesita opencv-python, numpy y Pillow.
Uso: make_base.py                   (todo)
     make_base.py --stills carpeta  (un cuadro por toma, para revisar)"""
import json, os, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.getcwd()
CFG = json.load(open(os.path.join(ROOT, 'shots.json'), encoding='utf-8'))
FONT = os.path.join(ROOT, CFG['font'])
W, H, FPS = 1080, 1920, 30
BEAT = 60 / CFG['bpm']
b = lambda n: n * BEAT
FACE, SIDE = tuple(CFG['face_rgb'][::-1]), tuple(CFG['side_rgb'][::-1])  # BGR
SHOTS = [dict(sh, f=os.path.join(ROOT, sh['f'])) for sh in CFG['shots']]
END_VIDEO = b(SHOTS[-1]['e'])

_lut = np.interp(np.arange(256), [0, 30, 90, 150, 205, 245, 255], [4, 24, 84, 150, 200, 232, 240]).astype(np.uint8)
_y, _x = np.mgrid[0:H, 0:W].astype(np.float32)
_v = 1 - .24 * np.clip((((_x - W / 2) / (W * .62)) ** 2 + ((_y - H / 2) / (H * .62)) ** 2) - .42, 0, 1) ** 1.2
_v = _v[..., None]


def grade(f):
    """Baja altas luces, da contraste y oscurece esquinas. No altera el inmueble."""
    f = cv2.LUT(f, _lut)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * .92, 0, 255)
    f = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    f = f + .45 * (f - cv2.GaussianBlur(f, (0, 0), 2.2))
    return np.clip(f * _v, 0, 255).astype(np.uint8)


def read(sh):
    c = cv2.VideoCapture(sh['f'])
    fps = c.get(cv2.CAP_PROP_FPS)
    fr = []
    t0 = sh['a']
    for _ in range(round(t0 * fps)):   # avanza leyendo: saltar directo falla en algunos clips
        c.grab()
    while True:
        ok, f = c.read()
        if not ok or t0 + len(fr) / fps > sh['z']:
            break
        h, w = f.shape[:2]
        if w > h:
            crop = h * 9 // 16
            x = (w - crop) // 2
            f = f[:, x:x + crop]
        fr.append(f)
    return fr, fps


def timing(sh, n, L):
    """Tiempo de origen por cuadro final: quieto en el medio y rapido en los bordes (rampa)."""
    u = (np.arange(n * 8) + .5) / (n * 8)
    pk, a = 7.0, .13
    w = 1 + (pk - 1) * (sh['ramp'][0] * np.exp(-(u / a) ** 2) + sh['ramp'][1] * np.exp(-((1 - u) / a) ** 2))
    s = np.concatenate([[0], np.cumsum(w)])
    s = s / s[-1] * (L - 1)
    return s[::8]


def track(gray, A, region, sc, a, z):
    lk = dict(winSize=(21, 21), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, .01))
    reg = (np.float32(region) / sc).reshape(-1, 1, 2)

    def mask(Hm):
        m = np.zeros(gray[0].shape, np.uint8)
        cv2.fillPoly(m, [cv2.perspectiveTransform(reg, Hm).astype(np.int32)], 255)
        return m

    def run(step):
        Hs = {A: np.eye(3)}
        i, p = A, None
        while a <= i + step < z:
            j = i + step
            if p is None or len(p) < 60 or abs(i - A) % 8 == 0:
                p = cv2.goodFeaturesToTrack(gray[i], 400, .006, 7, mask=mask(Hs[i]))
            if p is None:
                Hs[j] = Hs[i]; i = j; continue
            q, st, _ = cv2.calcOpticalFlowPyrLK(gray[i], gray[j], p, None, **lk)
            bk, st2, _ = cv2.calcOpticalFlowPyrLK(gray[j], gray[i], q, None, **lk)
            good = (st.ravel() == 1) & (st2.ravel() == 1) & (np.abs(p - bk).reshape(-1, 2).max(1) < .7)
            if good.sum() < 10:
                Hs[j] = Hs[i]; p = None; i = j; continue
            h, inl = cv2.findHomography(p[good], q[good], cv2.RANSAC, 1.5)
            if h is None:
                Hs[j] = Hs[i]; p = None; i = j; continue
            Hs[j] = h @ Hs[i]
            p = q[good][inl.ravel() == 1].reshape(-1, 1, 2)
            i = j
        return Hs

    return {**run(-1), **run(1)}


class Title:
    TW, TH = 2000, 620

    def __init__(self, t, fr, fps, sh, sc):
        self.t = t
        im = Image.new('L', (self.TW, self.TH), 0)
        d = ImageDraw.Draw(im)
        font = ImageFont.truetype(FONT, t['size'])
        bb = d.textbbox((0, 0), t['text'], font=font)
        d.text(((self.TW - (bb[2] - bb[0])) / 2 - bb[0], (self.TH - (bb[3] - bb[1])) / 2 - bb[1]), t['text'], font=font, fill=255)
        self.a = np.array(im)
        A = int(round((t['anchor'] - sh['a']) * fps))
        gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr]
        Hs = track(gray, A, t['region'], sc, 0, len(fr))
        q = (np.float32(t['quad']) / sc).reshape(-1, 1, 2)
        Q = np.array([cv2.perspectiveTransform(q, Hs[k]).reshape(-1) * sc for k in range(len(fr))])
        K = np.array([1, 2, 3, 2, 1.]) / 9
        self.Q = np.stack([np.convolve(np.pad(Q[:, c], 2, 'edge'), K, 'valid') for c in range(8)], 1).reshape(-1, 4, 2)

    def draw(self, img, k, prog):
        if prog <= 0:
            return img
        c = self.Q[k]
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [self.TW, 0], [self.TW, self.TH], [0, self.TH]]), c.astype(np.float32))
        A = cv2.warpPerspective(self.a, M, (W, H), flags=cv2.INTER_LINEAR)
        if not A.any():
            return img
        sc = min(1.6, np.linalg.norm(c[2] - c[3]) / 800)
        ext = max(1, int(self.t['ext'] * sc * prog))
        ker = np.ones((2 * ext + 1, 1), np.uint8)
        ker[ext + 1:] = 0  # crece solo hacia arriba
        side = cv2.dilate(A, ker[::-1])
        top = np.roll(A, -ext, 0)
        al = min(1, prog * 1.5)
        sh = cv2.GaussianBlur(cv2.resize(A, (W // 4, H // 4)), (0, 0), 5)
        sh = cv2.resize(sh, (W, H)).astype(np.float32)[..., None] / 255 * .42 * al
        img = img.astype(np.float32) * (1 - sh)
        for lay, col in ((side, SIDE), (top, FACE)):
            m = lay.astype(np.float32)[..., None] / 255 * al
            img = img * (1 - m) + np.float32(col) * m
        return img


def zoom_blur(f, amt):
    """Desenfoque radial: el zoom que atraviesa la imagen."""
    out = np.zeros_like(f, np.float32)
    n = 7
    for i in range(n):
        s = 1 + amt * i / (n - 1)
        out += cv2.warpAffine(f, np.float32([[s, 0, W / 2 * (1 - s)], [0, s, H / 2 * (1 - s)]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return (out / n).astype(np.uint8)


def transition(f, t, cuts):
    d = min(cuts, key=lambda c: abs(t + .5 / FPS - c)) - (t + .5 / FPS)
    x = abs(d) / .2
    if x >= 1:
        return f
    amt = .34 * (1 - x) ** 1.6
    if d > 0:      # saliendo: acelera hacia adentro
        s = 1 + .3 * (1 - x) ** 2
    else:          # entrando: frena desde cerca
        s = 1 + .12 * (1 - x) ** 2
    f = cv2.warpAffine(f, np.float32([[s, 0, W / 2 * (1 - s)], [0, s, H / 2 * (1 - s)]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return zoom_blur(f, amt)


def main():
    stills = '--stills' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--') and not (stills and a == sys.argv[sys.argv.index('--stills') + 1])]
    cuts = [b(s['s']) for s in SHOTS[1:]] + [END_VIDEO]
    pipe = None
    os.makedirs(ROOT + '/assets/build', exist_ok=True)
    if not stills:
        pipe = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                 '-c:v', 'libx264', '-crf', '13', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                                 ROOT + '/assets/build/base.mp4'], stdin=subprocess.PIPE)
    written = 0
    for sh in SHOTS:
        if only and sh['n'] not in only:
            continue
        fr, fps = read(sh)
        h, w = fr[0].shape[:2]
        sc = W / w
        title = Title(sh['title'], fr, fps, sh, sc) if 'title' in sh else None
        n = round(b(sh['e']) * FPS) - round(b(sh['s']) * FPS)
        s = timing(sh, n, len(fr))
        print(sh['n'], 'origen', len(fr), 'cuadros a', round(fps), 'fps -> final', n, flush=True)
        ks = [n // 2] if stills else range(n)
        for k in ks:
            t = (round(b(sh['s']) * FPS) + k) / FPS
            a, z = s[k], max(s[k + 1], s[k] + 1e-3)
            idx = np.unique(np.linspace(a, z - 1e-3, 8).astype(int).clip(0, len(fr) - 1))
            prog = 1.0
            if title:
                x = np.clip((k / FPS - title.t['on']) / .45, 0, 1)
                prog = 1 - (1 - x) ** 3 if k / FPS >= title.t['on'] else 0
                prog *= 1 - np.clip((k / FPS - title.t['off']) / .22, 0, 1)
            wts = np.ones(len(idx)) / len(idx)
            if len(idx) == 1 and not sh.get('person') and int(a) + 1 < len(fr):   # camara lenta: funde cuadros vecinos
                idx = np.array([int(a), int(a) + 1])
                wts = np.array([1 - (a - int(a)), a - int(a)])
            acc = 0
            for i, wt in zip(idx, wts):
                f = cv2.resize(fr[i], (W, H), interpolation=cv2.INTER_LANCZOS4)
                if title:
                    f = title.draw(f, i, prog)
                acc = acc + np.float32(f) * wt
            f = grade(acc.clip(0, 255).astype(np.uint8))
            f = transition(f, t, cuts)
            if stills:
                cv2.imwrite(f'{sys.argv[sys.argv.index("--stills") + 1]}/{sh["n"]}.jpg', cv2.resize(f, (405, 720)), [cv2.IMWRITE_JPEG_QUALITY, 88])
            else:
                pipe.stdin.write(f.tobytes())
                written += 1
    if pipe:
        pipe.stdin.close()
        pipe.wait()
        print('cuadros', written, 'duracion', round(written / FPS, 2))


if __name__ == '__main__':
    main()
