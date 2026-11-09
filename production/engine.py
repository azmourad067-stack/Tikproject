"""NUBO — moteur d'animation procédural « feutrine stop-motion ».

Tout est dessiné en code (PIL + numpy) : textures de laine, ombrages,
saccades stop-motion à 12 images/s, post-traitement chaud.
"""
import math
import os
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 12
FRAME = 0  # index de l'image en cours (mis à jour par le moteur de rendu)

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------
ORANGE = (255, 138, 61)
ORANGE_D = (226, 108, 40)
MINT = (189, 231, 211)
LAVENDER = (205, 189, 240)
CREAM = (255, 243, 224)
PINK = (247, 198, 207)
DUCK = (255, 212, 59)
WOOD = (214, 170, 120)
GREY = (150, 150, 158)
WHITE = (250, 248, 242)
BLACK = (28, 24, 26)
SKY = (180, 220, 245)
GREEN = (120, 190, 120)
RED = (230, 70, 70)
BROWN = (150, 100, 65)

FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def mix(c1, c2, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))


def darker(c, k=0.8):
    return tuple(int(v * k) for v in c)


# --------------------------------------------------------------------------
# Easing / timing helpers
# --------------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    """Progression 0..1 de t entre a et b."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def ease_in_out(x):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def ease_out_back(x, s=1.7):
    x = clamp(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def bounce_out(x):
    x = clamp(x)
    n1, d1 = 7.5625, 2.75
    if x < 1 / d1:
        return n1 * x * x
    if x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    if x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    x -= 2.625 / d1
    return n1 * x * x + 0.984375


def lerp(a, b, k):
    return a + (b - a) * k


def keys(t, pts, ease=ease_in_out):
    """Interpolation par clés : pts = [(t0, v0), (t1, v1), ...] (v scalaire ou tuple)."""
    if t <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t <= t1:
            k = ease(seg(t, t0, t1))
            if isinstance(v0, tuple):
                return tuple(lerp(a, b, k) for a, b in zip(v0, v1))
            return lerp(v0, v1, k)
    return pts[-1][1]


def blink_at(t, times, dur=0.17):
    """Ouverture des yeux (1 = ouverts) avec des clignements aux instants donnés."""
    o = 1.0
    for bt in times:
        if bt <= t <= bt + dur:
            k = (t - bt) / dur
            o = min(o, abs(1 - 2 * k))
    return o


def rng_for(*key):
    return random.Random(hash(key) & 0xFFFFFFFF)


def jit(obj_id, amp=2.0, ramp=0.6):
    """Saccade stop-motion déterministe pour un objet et l'image courante."""
    r = rng_for(obj_id, FRAME)
    return (r.uniform(-amp, amp), r.uniform(-amp, amp), r.uniform(-ramp, ramp))


# --------------------------------------------------------------------------
# Texture de laine
# --------------------------------------------------------------------------
_TEX_PATH = os.path.join(os.path.dirname(__file__), ".cache_tex.npy")


def _make_tex(n=2048, seed=7):
    rng = np.random.default_rng(seed)
    img = Image.new("L", (n, n), 128)
    d = ImageDraw.Draw(img)
    count = n * n // 38
    xs = rng.integers(0, n, count)
    ys = rng.integers(0, n, count)
    ang = rng.random(count) * math.pi
    ln = rng.integers(3, 13, count)
    val = rng.integers(70, 190, count)
    for x, y, a, l, v in zip(xs, ys, ang, ln, val):
        dx, dy = math.cos(a) * l, math.sin(a) * l
        d.line((x - dx, y - dy, x + dx, y + dy), fill=int(v), width=1)
    img = img.filter(ImageFilter.GaussianBlur(0.7))
    arr = np.asarray(img, np.float32)
    arr += rng.normal(0, 10, arr.shape).astype(np.float32)
    # légère variation basse fréquence (feutre irrégulier)
    low = Image.fromarray(rng.integers(0, 255, (n // 64, n // 64)).astype(np.uint8)).resize(
        (n, n), Image.BICUBIC)
    arr += (np.asarray(low, np.float32) - 128) * 0.25
    arr = (arr - arr.mean()) / (arr.std() * 2.2)
    return np.clip(arr, -1, 1).astype(np.float32)


def get_tex():
    global _TEX
    try:
        return _TEX
    except NameError:
        pass
    if os.path.exists(_TEX_PATH):
        _TEX = np.load(_TEX_PATH)
    else:
        _TEX = _make_tex()
        np.save(_TEX_PATH, _TEX)
    return _TEX


def tex_crop(w, h, seed=0):
    t = get_tex()
    n = t.shape[0]
    if w > n or h > n:
        t = np.tile(t, (h // n + 1, w // n + 1))
    ox = (seed * 389) % max(1, t.shape[1] - w)
    oy = (seed * 211) % max(1, t.shape[0] - h)
    return t[oy:oy + h, ox:ox + w]


# --------------------------------------------------------------------------
# Feutrine : transforme un masque en matière laineuse ombrée
# --------------------------------------------------------------------------
def felt(mask, color, seed=0, tex=0.15, rim=0.5, fuzz=0.9, light=True, radius=None):
    w, h = mask.size
    bbox = mask.getbbox()
    if bbox is None:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))
    size = min(bbox[2] - bbox[0], bbox[3] - bbox[1])
    r = radius if radius else max(1.5, size * 0.11)
    b = np.asarray(mask.filter(ImageFilter.GaussianBlur(r)), np.float32) / 255.0
    f = 1 - rim * (1 - np.clip(b * 1.7, 0, 1))
    if light:
        dd = int(r * 0.9)
        sh = ImageChops.offset(mask, -dd, -dd)
        ls = np.asarray(sh.filter(ImageFilter.GaussianBlur(r)), np.float32) / 255.0
        f = f * (0.8 + 0.3 * ls)
    t = tex_crop(w, h, seed)
    col = np.array(color, np.float32)[None, None, :] * f[..., None] * (1 + tex * t[..., None])
    mb = np.asarray(mask.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255.0
    band = 4 * mb * (1 - mb)
    a = np.clip(mb + fuzz * t * band, 0, 1)
    out = np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def mk_mask(w, h, fn, ss=2):
    im = Image.new("L", (int(w * ss), int(h * ss)), 0)
    d = ImageDraw.Draw(im)
    fn(d, ss)
    return im.resize((int(w), int(h)), Image.LANCZOS)


def shape(w, h, items, color, seed=0, pad=6, **kw):
    """Sprite feutrine à partir d'une liste de primitives.

    items : ('ellipse', x0,y0,x1,y1) | ('rect', x0,y0,x1,y1,rad) | ('poly', [(x,y)...])
            | ('line', [(x,y)...], width) | ('circle', cx,cy,r) ; préfixe '-' = découpe.
    """
    W2, H2 = int(w + 2 * pad), int(h + 2 * pad)

    def fn(d, s):
        for it in items:
            kind = it[0]
            fill = 255
            if kind.startswith("-"):
                kind, fill = kind[1:], 0
            P = lambda v: (v + pad) * s
            if kind == "ellipse":
                d.ellipse([P(it[1]), P(it[2]), P(it[3]), P(it[4])], fill=fill)
            elif kind == "circle":
                cx, cy, r = it[1:4]
                d.ellipse([P(cx - r), P(cy - r), P(cx + r), P(cy + r)], fill=fill)
            elif kind == "rect":
                rad = it[5] if len(it) > 5 else 0
                d.rounded_rectangle([P(it[1]), P(it[2]), P(it[3]), P(it[4])], radius=rad * s, fill=fill)
            elif kind == "poly":
                d.polygon([(P(x), P(y)) for x, y in it[1]], fill=fill)
            elif kind == "line":
                pts = [(P(x), P(y)) for x, y in it[1]]
                d.line(pts, fill=fill, width=int(it[2] * s), joint="curve")
                r = it[2] * s / 2
                for x, y in (pts[0], pts[-1]):
                    d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    m = mk_mask(W2, H2, fn)
    return felt(m, color, seed=seed, **kw)


class Sprite:
    """Image RGBA + point d'ancrage (en pixels de l'image)."""

    def __init__(self, img, anchor=None):
        self.img = img
        self.anchor = anchor if anchor else (img.width / 2, img.height / 2)


def S(w, h, items, color, seed=0, anchor="center", pad=6, **kw):
    img = shape(w, h, items, color, seed=seed, pad=pad, **kw)
    if anchor == "center":
        a = (img.width / 2, img.height / 2)
    elif anchor == "bottom":
        a = (img.width / 2, h + pad)
    elif anchor == "top":
        a = (img.width / 2, pad)
    else:
        a = (anchor[0] + pad, anchor[1] + pad)
    return Sprite(img, a)


def stack(size, layers, anchor=None):
    """Assemble plusieurs (Sprite|Image, (x, y) coin haut-gauche) en un Sprite."""
    base = Image.new("RGBA", size, (0, 0, 0, 0))
    for im, (x, y) in layers:
        if isinstance(im, Sprite):
            im = im.img
        paste(base, im, int(round(x)), int(round(y)))
    return Sprite(base, anchor)


# --------------------------------------------------------------------------
# Composition
# --------------------------------------------------------------------------
def paste(canvas, im, x, y, alpha=1.0):
    """alpha_composite tolérant les coordonnées hors champ."""
    if alpha <= 0:
        return
    if alpha < 1:
        im = im.copy()
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im.putalpha(a)
    cw, ch = canvas.size
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(cw, x + im.width), min(ch, y + im.height)
    if x1 <= x0 or y1 <= y0:
        return
    crop = im.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    canvas.alpha_composite(crop, (x0, y0))


def transform(sp, scale=1.0, sx=1.0, sy=1.0, rot=0.0, flip=False):
    img = sp.img
    ax, ay = sp.anchor
    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        ax = img.width - ax
    fx, fy = scale * sx, scale * sy
    if abs(fx - 1) > 1e-3 or abs(fy - 1) > 1e-3:
        nw, nh = max(1, int(img.width * fx)), max(1, int(img.height * fy))
        img = img.resize((nw, nh), Image.BICUBIC if fx > 1 else Image.LANCZOS)
        ax, ay = ax * nw / sp.img.width, ay * nh / sp.img.height
    if abs(rot) > 0.05:
        R = int(math.ceil(max(math.hypot(ax, ay), math.hypot(img.width - ax, ay),
                              math.hypot(ax, img.height - ay),
                              math.hypot(img.width - ax, img.height - ay)))) + 2
        sq = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
        sq.alpha_composite(img, (int(R - ax), int(R - ay)))
        img = sq.rotate(rot, resample=Image.BICUBIC, center=(R, R))
        ax, ay = R, R
    return img, ax, ay


def put(canvas, sp, x, y, scale=1.0, sx=1.0, sy=1.0, rot=0.0, alpha=1.0, flip=False,
        jid=None, jamp=2.0, jrot=0.6):
    """Pose un sprite : (x, y) = position de l'ancre."""
    if sp is None or alpha <= 0:
        return
    if sx < 0:
        sx, flip = -sx, not flip
    sx = max(sx, 0.04)
    sy = max(sy, 0.04)
    if jid is not None:
        jx, jy, jr = jit(jid, jamp, jrot)
        x, y, rot = x + jx, y + jy, rot + jr
    img, ax, ay = transform(sp, scale, sx, sy, rot, flip)
    paste(canvas, img, int(round(x - ax)), int(round(y - ay)), alpha)


def shadow(canvas, x, y, w, h=None, alpha=0.28):
    h = h if h else w * 0.22
    key = (int(w), int(h))
    img = _shadow_img(*key)
    paste(canvas, img, int(x - img.width / 2), int(y - img.height / 2), alpha)


@lru_cache(maxsize=64)
def _shadow_img(w, h):
    pad = int(h) + 10
    im = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    ImageDraw.Draw(im).ellipse([pad, pad, pad + w, pad + h], fill=200)
    im = im.filter(ImageFilter.GaussianBlur(h * 0.35 + 2))
    out = Image.new("RGBA", im.size, (40, 25, 30, 0))
    out.putalpha(im)
    return out


def glow(canvas, x, y, r, color=(255, 220, 150), alpha=0.6):
    img = _glow_img(int(r), color)
    paste(canvas, img, int(x - img.width / 2), int(y - img.height / 2), alpha)


@lru_cache(maxsize=32)
def _glow_img(r, color):
    im = Image.new("L", (4 * r, 4 * r), 0)
    ImageDraw.Draw(im).ellipse([r, r, 3 * r, 3 * r], fill=255)
    im = im.filter(ImageFilter.GaussianBlur(r * 0.6))
    out = Image.new("RGBA", im.size, color + (0,))
    out.putalpha(im)
    return out


def camera(img, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0, clamp_view=True):
    """Recadrage caméra (zoom > 1 = rapproché) autour de (cx, cy)."""
    if abs(zoom - 1) < 1e-3 and abs(rot) < 1e-3 and abs(cx - W / 2) < 0.5 and abs(cy - H / 2) < 0.5:
        return img
    cw, ch = W / zoom, H / zoom
    if clamp_view and zoom >= 1:
        cx = min(max(cx, cw / 2), W - cw / 2)
        cy = min(max(cy, ch / 2), H - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    out = img.transform((W, H), Image.EXTENT, box, resample=Image.BICUBIC)
    if abs(rot) > 1e-3:
        out = out.rotate(rot, resample=Image.BICUBIC)
    return out


def motion_blur(img, amount=8, vertical=False):
    if amount < 1:
        return img
    arr = np.asarray(img.convert("RGB"), np.float32)
    acc = np.zeros_like(arr)
    n = int(amount)
    for i in range(-n, n + 1, max(1, n // 4)):
        acc += np.roll(arr, i, axis=0 if vertical else 1)
    acc /= len(range(-n, n + 1, max(1, n // 4)))
    return Image.fromarray(acc.astype(np.uint8)).convert("RGBA")


def radial_blur(img, strength=0.15, steps=6):
    """Flou de zoom (pour les travellings rapides)."""
    base = img.convert("RGB")
    acc = np.asarray(base, np.float32).copy()
    for i in range(1, steps + 1):
        z = 1 + strength * i / steps
        acc += np.asarray(camera(base.convert("RGBA"), z).convert("RGB"), np.float32)
    acc /= steps + 1
    return Image.fromarray(acc.astype(np.uint8)).convert("RGBA")


# --------------------------------------------------------------------------
# Post-traitement : vignettage chaud + grain
# --------------------------------------------------------------------------
_VIG = None
_GRAIN = None


def _post_maps():
    global _VIG, _GRAIN
    if _VIG is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        _VIG = np.clip(1 - 0.32 * d ** 2.2, 0.55, 1)[..., None]
        rng = np.random.default_rng(3)
        _GRAIN = [rng.normal(0, 4.0, (H, W, 1)).astype(np.float32) for _ in range(6)]
    return _VIG, _GRAIN


def post(img, warm=True, grain=True, vignette=True):
    vig, gr = _post_maps()
    a = np.asarray(img.convert("RGB"), np.float32)
    if warm:
        a = a * np.array([1.03, 1.0, 0.95], np.float32)
    if vignette:
        a = a * vig
    if grain:
        a = a + gr[FRAME % len(gr)]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# --------------------------------------------------------------------------
# Décors
# --------------------------------------------------------------------------
def felt_panel(w, h, color, seed=0, stitch=True, rim=0.25, pad=0):
    m = Image.new("L", (w, h), 255)
    img = felt(m, color, seed=seed, rim=0.0, fuzz=0.0, light=False, tex=0.12)
    if stitch:
        d = ImageDraw.Draw(img)
        sc = darker(color, 0.78)
        for x in range(18, w, 22):
            d.line((x, 14, x + 11, 14), fill=sc + (255,), width=3)
            d.line((x, h - 14, x + 11, h - 14), fill=sc + (255,), width=3)
    return img


def room_bg(wall=LAVENDER, floor=CREAM, floor_y=1380, seed=1, baseboard=True, wall_pattern=None):
    """Fond générique : mur + sol en feutrine."""
    bg = Image.new("RGBA", (W, H), wall + (255,))
    wallimg = felt_panel(W, floor_y + 20, wall, seed=seed, stitch=False)
    bg.alpha_composite(wallimg, (0, 0))
    d = ImageDraw.Draw(bg)
    if wall_pattern == "dots":
        r = rng_for("dots", seed)
        for y in range(80, floor_y - 40, 130):
            for x in range(60 + (y // 130 % 2) * 65, W, 130):
                c = darker(wall, 0.9)
                d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c + (255,))
    elif wall_pattern == "tiles":
        c = darker(wall, 0.86)
        for y in range(0, floor_y, 120):
            d.line((0, y, W, y), fill=c + (255,), width=4)
            for x in range(0 + (y // 120 % 2) * 60, W, 120):
                d.line((x, y, x, y + 120), fill=c + (255,), width=4)
    elif wall_pattern == "stripes":
        c = darker(wall, 0.93)
        for x in range(0, W, 90):
            d.rectangle([x, 0, x + 40, floor_y], fill=c + (255,))
    fl = felt_panel(W, H - floor_y, floor, seed=seed + 5, stitch=True)
    bg.alpha_composite(fl, (0, floor_y))
    if baseboard:
        bb = felt_panel(W, 34, darker(wall, 0.82), seed=seed + 9, stitch=False)
        bg.alpha_composite(bb, (0, floor_y - 20))
    # ombre douce au pied du mur
    sh = Image.new("L", (W, 80), 0)
    ImageDraw.Draw(sh).rectangle([0, 0, W, 30], fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    shimg = Image.new("RGBA", (W, 80), (60, 40, 50, 0))
    shimg.putalpha(sh)
    bg.alpha_composite(shimg, (0, floor_y + 12))
    return bg


# --------------------------------------------------------------------------
# NUBO
# --------------------------------------------------------------------------
def _superellipse(cx, cy, rx, ry, n=2.4, k=72, wobble=0.018, seed=3):
    r = random.Random(seed)
    ph = [r.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(k):
        a = 2 * math.pi * i / k
        c, s = math.cos(a), math.sin(a)
        x = abs(c) ** (2 / n) * (1 if c >= 0 else -1)
        y = abs(s) ** (2 / n) * (1 if s >= 0 else -1)
        w = 1 + wobble * (math.sin(3 * a + ph[0]) + 0.6 * math.sin(5 * a + ph[1]))
        # base plus large (forme guimauve / patate)
        bw = 1 + 0.06 * max(0, s)
        pts.append((cx + rx * x * w * bw, cy + ry * y * w))
    return pts


def _tuft_path(kind, x0, y0, h, phase=0.0):
    """Points de la mèche (coordonnées base)."""
    pts = []
    if kind in ("curl", "smoke", "out"):
        for i in range(40):
            u = i / 39
            if u < 0.55:
                k = u / 0.55
                pts.append((x0 + math.sin(k * 1.4 + phase) * 0.03 * h, y0 - k * 0.2 * h))
            else:
                k = (u - 0.55) / 0.45
                a = -math.pi / 2 + k * 1.9 * math.pi
                rr = 0.07 * h * (1 - 0.45 * k)
                cx, cy = x0 + 0.07 * h + math.sin(1.4 + phase) * 0.03 * h, y0 - 0.2 * h
                pts.append((cx + math.cos(a + math.pi) * rr + 0.0, cy + math.sin(a + math.pi) * rr))
    elif kind == "up":
        for i in range(30):
            u = i / 29
            pts.append((x0 + math.sin(u * 18 + phase * 3) * 0.025 * h, y0 - u * 0.36 * h))
    elif kind == "down":
        for i in range(30):
            u = i / 29
            pts.append((x0 + u * 0.2 * h, y0 - math.sin(u * math.pi * 0.9) * 0.1 * h + u * u * 0.06 * h))
    elif kind == "question":
        for i in range(44):
            u = i / 43
            if u < 0.3:
                k = u / 0.3
                pts.append((x0, y0 - k * 0.1 * h))
            else:
                k = (u - 0.3) / 0.7
                a = math.pi / 2 + k * 1.5 * math.pi
                pts.append((x0 + math.cos(a) * 0.08 * h * -1 + 0.0, y0 - 0.19 * h - math.sin(a) * 0.08 * h))
    elif kind == "flat":
        for i in range(20):
            u = i / 19
            pts.append((x0 + u * 0.14 * h, y0 - math.sin(u * 3) * 0.02 * h))
    return pts


@lru_cache(maxsize=2048)
def _nubo_cached(h, eyes, look, tuft, color, beard, sweat, spiral, arms, fluffy, toasted,
                 phase, scared_eyes, smile, furry, cheeks):
    pad = 0.45 * h
    cw, ch = int(h * 1.25 + 2 * pad), int(h * 1.35 + 2 * pad)
    cx = cw / 2
    foot = ch - pad * 0.6
    bw, bh = 0.96 * h, 0.86 * h
    if cheeks:
        bw *= 1.0
    btop = foot - 0.07 * h - bh
    bcy = btop + bh / 2
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    col = color
    if toasted:
        col = (205, 140, 70)
    seed = 11

    # pieds
    fcol = darker(col, 0.86)
    for sgn in (-1, 1):
        fx = cx + sgn * 0.21 * h
        fs = shape(0.28 * h, 0.14 * h, [("ellipse", 0, 0, 0.28 * h, 0.14 * h)], fcol, seed=seed + sgn)
        paste(canvas, fs, int(fx - fs.width / 2), int(foot - 0.14 * h - 6))

    # bras (derrière le corps si baissés, ils dépassent sur les côtés)
    arm_imgs = []
    for side, ang in ((-1, arms[0]), (1, arms[1])):
        aw, al = 0.13 * h, 0.27 * h
        a = shape(aw, al, [("ellipse", 0, 0, aw, al)], darker(col, 0.95), seed=seed + 4 + side)
        sp = Sprite(a, (a.width / 2, 6 + aw * 0.5))
        rot = (-ang if side < 0 else ang)
        arm_imgs.append((sp, cx + side * 0.43 * h, bcy + 0.04 * h, rot))
    for sp, x, y, rot in arm_imgs:
        put(canvas, sp, x, y, rot=rot)

    # corps
    pts = _superellipse(cx, bcy, bw / 2, bh / 2, wobble=0.018 + 0.03 * fluffy)

    def body_fn(d, s):
        d.polygon([(x * s, y * s) for x, y in pts], fill=255)

    m = mk_mask(cw, ch, body_fn)
    if fluffy:
        m = m.filter(ImageFilter.GaussianBlur(fluffy * 6)).point(lambda v: 255 if v > 90 else int(v * 2.6))
    body = felt(m, col, seed=seed, fuzz=0.9 + 2.5 * fluffy, tex=0.15 + 0.1 * fluffy)
    canvas.alpha_composite(body)
    d = ImageDraw.Draw(canvas)

    if toasted:
        # dorure : bord supérieur plus foncé + traces de grille
        tm = Image.new("L", (cw, ch), 0)
        td = ImageDraw.Draw(tm)
        for i in range(3):
            yy = btop + bh * (0.25 + 0.22 * i)
            td.line((cx - bw * 0.42, yy, cx + bw * 0.42, yy), fill=150, width=int(0.035 * h))
        tm = ImageChops.multiply(tm.filter(ImageFilter.GaussianBlur(4)), m)
        burn = Image.new("RGBA", (cw, ch), (110, 60, 25, 0))
        burn.putalpha(tm)
        canvas.alpha_composite(burn)

    if furry:
        r = random.Random(5)
        fur = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fur)
        marr = np.asarray(m)
        for _ in range(int(h * 14)):
            x = r.uniform(cx - bw / 2, cx + bw / 2)
            y = r.uniform(btop, foot)
            if marr[int(min(ch - 1, y)), int(min(cw - 1, x))] < 128:
                continue
            ang = math.atan2(y - bcy, x - cx) + r.uniform(-0.5, 0.5)
            L = r.uniform(0.02, 0.06) * h
            c = mix(col, (90, 45, 20), r.uniform(0, 0.6))
            fd.line((x, y, x + math.cos(ang) * L, y + math.sin(ang) * L), fill=c + (200,), width=2)
        canvas.alpha_composite(fur)

    # joues gonflées
    if cheeks:
        for sgn in (-1, 1):
            gx, gy = cx + sgn * 0.3 * h, bcy + 0.12 * h
            gl = _glow_img(int(0.07 * h), (255, 120, 120))
            paste(canvas, gl, int(gx - gl.width / 2), int(gy - gl.height / 2), 0.5)

    # yeux
    er = 0.072 * h * (1.25 if scared_eyes else 1.0) * (1.25 if furry else 1)
    ey = btop + 0.4 * bh
    lx, ly = look
    for i, sgn in enumerate((-1, 1)):
        ex = cx + sgn * 0.2 * h + lx * 0.07 * h
        eyy = ey + ly * 0.06 * h
        o = eyes[i]
        if spiral:
            sp = []
            for k in range(60):
                a = k / 59 * 4.5 * math.pi
                rr = er * 1.2 * k / 59
                sp.append((ex + math.cos(a + phase * 4) * rr, eyy + math.sin(a + phase * 4) * rr))
            d.line(sp, fill=BLACK + (255,), width=max(2, int(0.012 * h)))
            continue
        _eye(canvas, ex, eyy, er, o, col, furry)

    # sourire (rarissime : réservé à certains gags)
    if smile:
        d.arc([cx - 0.12 * h, ey + 0.05 * h, cx + 0.12 * h, ey + 0.2 * h], 20, 160,
              fill=BLACK + (255,), width=max(2, int(0.015 * h)))

    # barbe (nuage de laine grise)
    if beard > 0:
        bl = beard * 0.62 * h
        rb = random.Random(9)
        blobs = []
        n = 16
        for k in range(n):
            u = k / (n - 1)
            yy = ey + 0.1 * h + u * bl
            wid = 0.3 * h * (1 - u) + 0.03 * h
            cols = 4 if u < 0.4 else (3 if u < 0.75 else 1)
            for j in range(cols):
                fx = (j / (cols - 1) - 0.5) if cols > 1 else 0
                blobs.append((cx + fx * wid * 1.6 + rb.uniform(-5, 5), yy + rb.uniform(-4, 4),
                              0.075 * h * (1 - 0.55 * u) + 3))
        # moustache
        for sgn in (-1, 1):
            for k in range(6):
                u = k / 5
                blobs.append((cx + sgn * (0.03 * h + u * 0.2 * h), ey + 0.12 * h - math.sin(u * 2.6) * 0.05 * h,
                              0.045 * h * (1 - 0.4 * u)))
        def beard_fn(dd, s):
            for x, y, r in blobs:
                dd.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=255)

        bm = mk_mask(cw, ch, beard_fn)
        canvas.alpha_composite(felt(bm, (208, 206, 214), seed=33, fuzz=1.8, tex=0.14, rim=0.45))

    # mèche
    tx, ty = cx + 0.02 * h, btop + 0.035 * h
    path = _tuft_path(tuft, tx, ty, h, phase)
    if path:
        tw = 0.055 * h
        tm = Image.new("L", (cw, ch), 0)

        def tuft_fn(dd, s):
            r = tw / 2 * s
            for x, y in path:
                dd.ellipse([x * s - r, y * s - r, x * s + r, y * s + r], fill=255)

        tm = mk_mask(cw, ch, tuft_fn)
        tcol = darker(col, 0.92)
        canvas.alpha_composite(felt(tm, tcol, seed=21, fuzz=1.5, radius=tw * 0.3))
        if tuft in ("smoke", "out"):
            ex, ey2 = path[-1] if tuft == "out" else path[len(path) // 2]
            sm = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
            sd = ImageDraw.Draw(sm)
            for k in range(4):
                u = ((phase * 0.5 + k / 4) % 1)
                rr = (0.03 + 0.07 * u) * h
                px = ex + math.sin(u * 6 + k) * 0.05 * h
                py = ey2 - 0.05 * h - u * 0.45 * h
                sd.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(235, 235, 240, int(170 * (1 - u))))
            canvas.alpha_composite(sm.filter(ImageFilter.GaussianBlur(0.012 * h + 1)))
        if tuft == "out":
            ex, ey2 = path[-1]
            ImageDraw.Draw(canvas).ellipse([ex - tw * 0.7, ey2 - tw * 0.7, ex + tw * 0.7, ey2 + tw * 0.7],
                                           fill=(40, 30, 30, 255))

    if sweat:
        sx0, sy0 = cx + 0.36 * h, btop + 0.12 * h
        sm = shape(0.07 * h, 0.1 * h, [("ellipse", 0, 0.03 * h, 0.07 * h, 0.1 * h),
                                       ("poly", [(0.035 * h, 0), (0.0, 0.06 * h), (0.07 * h, 0.06 * h)])],
                   (180, 225, 255), seed=4, fuzz=0.2)
        paste(canvas, sm, int(sx0), int(sy0))
    return canvas, (cx, foot)


def _eye(canvas, ex, ey, er, o, lidcol, furry=False):
    pad = int(er) + 4
    size = int(2 * er + 2 * pad)
    ss = 3
    big = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    c = size * ss / 2
    R = er * ss
    # perle noire
    d.ellipse([c - R, c - R, c + R, c + R], fill=(22, 18, 22, 255))
    d.ellipse([c - R * 0.8, c - R * 0.85, c + R * 0.6, c + R * 0.55], fill=(45, 40, 48, 255))
    d.ellipse([c - R * 0.55, c - R * 0.65, c - R * 0.05, c - R * 0.15], fill=(255, 255, 255, 235))
    d.ellipse([c + R * 0.25, c + R * 0.25, c + R * 0.5, c + R * 0.5], fill=(255, 255, 255, 140))
    if furry:
        for k in range(8):
            a = k * 0.8
            d.line((c + math.cos(a) * R * 0.98, c + math.sin(a) * R * 0.98,
                    c + math.cos(a + 0.2) * R * 0.7, c + math.sin(a + 0.2) * R * 0.7),
                   fill=(150, 30, 30, 200), width=2)
    if o < 0.98:
        # paupière en feutrine qui descend
        lid = Image.new("L", big.size, 0)
        ld = ImageDraw.Draw(lid)
        cover = (1 - o) * 2 * R
        ld.rectangle([0, c - R - 4, big.width, c - R + cover], fill=255)
        circ = Image.new("L", big.size, 0)
        ImageDraw.Draw(circ).ellipse([c - R - 3, c - R - 3, c + R + 3, c + R + 3], fill=255)
        lid = ImageChops.multiply(lid, circ)
        lidimg = Image.new("RGBA", big.size, darker(lidcol, 0.93) + (0,))
        lidimg.putalpha(lid)
        big.alpha_composite(lidimg)
        yline = c - R + cover
        if o < 0.06:
            d.arc([c - R, c - R * 1.1, c + R, c + R * 0.9], 25, 155, fill=darker(lidcol, 0.55) + (255,),
                  width=int(R * 0.18))
        else:
            hw = math.sqrt(max(0, R * R - (yline - c) ** 2))
            d.line((c - hw, yline, c + hw, yline), fill=darker(lidcol, 0.6) + (255,), width=int(R * 0.12))
    small = big.resize((size, size), Image.LANCZOS)
    paste(canvas, small, int(ex - size / 2), int(ey - size / 2))


def nubo(h=300, eyes=1.0, look=(0, 0), tuft="curl", color=ORANGE, beard=0.0, sweat=False,
         spiral=False, arms=(18, 18), fluffy=0.0, toasted=False, phase=0.0, scared=False, smile=False,
         furry=False, cheeks=False):
    if not isinstance(eyes, tuple):
        eyes = (eyes, eyes)
    q = lambda v, s=0.1: round(v / s) * s
    key = (int(h), (q(eyes[0]), q(eyes[1])), (q(look[0]), q(look[1])), tuft, tuple(color),
           q(beard), sweat, spiral, (int(arms[0] / 5) * 5, int(arms[1] / 5) * 5), q(fluffy), toasted,
           q(phase, 0.25), scared, smile, furry, cheeks)
    img, anchor = _nubo_cached(*key)
    return Sprite(img, anchor)


def regard_eyes(t, t0, look_from=(1, 0)):
    """Le REGARD : à partir de t0, NUBO tourne les yeux vers la caméra puis cligne 2 fois."""
    k = ease_in_out(seg(t, t0, t0 + 0.5))
    look = (look_from[0] * (1 - k), look_from[1] * (1 - k))
    o = blink_at(t, [t0 + 0.75, t0 + 1.15], 0.2)
    return look, o


# --------------------------------------------------------------------------
# Accessoires communs
# --------------------------------------------------------------------------
@lru_cache(maxsize=8)
def duck(h=90, look_cam=False):
    w = h * 1.25
    body = shape(w, h, [("ellipse", 0, h * 0.35, w, h),
                        ("circle", w * 0.36, h * 0.3, h * 0.27),
                        ("poly", [(w * 0.85, h * 0.55), (w * 1.05, h * 0.3), (w * 0.95, h * 0.7)])],
                 DUCK, seed=41, rim=0.4)
    d = ImageDraw.Draw(body)
    pad = 6
    bx, by = w * 0.06 + pad, h * 0.3 + pad
    d.polygon([(bx + 4, by - 2), (bx - h * 0.2, by + h * 0.05), (bx + 4, by + h * 0.12)], fill=(250, 140, 40, 255))
    ex, ey = w * 0.3 + pad, h * 0.22 + pad
    r = h * 0.055
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(20, 20, 20, 255))
    d.ellipse([ex - r * 0.4, ey - r * 0.6, ex, ey - r * 0.1], fill=(255, 255, 255, 230))
    return Sprite(body, (body.width / 2, h + pad))


def text_img(txt, size, color=(255, 255, 255), font=FONT_MONO, stroke=0):
    f = ImageFont.truetype(font, size)
    bb = f.getbbox(txt, stroke_width=stroke)
    im = Image.new("RGBA", (bb[2] - bb[0] + 10, bb[3] - bb[1] + 10), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((5 - bb[0], 5 - bb[1]), txt, font=f, fill=color + (255,),
                            stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return im


def particles(canvas, items):
    """items: liste de (x, y, r, color, alpha) — composés par-dessus le canevas."""
    items = [it for it in items if it[4] > 0.01]
    if not items:
        return
    x0 = int(max(0, min(x - r for x, y, r, c, a in items) - 2))
    y0 = int(max(0, min(y - r for x, y, r, c, a in items) - 2))
    x1 = int(min(canvas.width, max(x + r for x, y, r, c, a in items) + 2))
    y1 = int(min(canvas.height, max(y + r for x, y, r, c, a in items) + 2))
    if x1 <= x0 or y1 <= y0:
        return
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x, y, r, c, a in items:
        d.ellipse([x - r - x0, y - r - y0, x + r - x0, y + r - y0], fill=tuple(int(v) for v in c) + (int(255 * min(1, a)),))
    canvas.alpha_composite(layer, (x0, y0))


def flash(img, k):
    if k <= 0:
        return img
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    return Image.blend(img.convert("RGBA"), white, clamp(k))


def fade_black(img, k):
    if k <= 0:
        return img
    black = Image.new("RGBA", img.size, (0, 0, 0, 255))
    return Image.blend(img.convert("RGBA"), black, clamp(k))
