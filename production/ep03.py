"""ÉPISODE 03 — LA PLANTE (boucle infinie)."""
import math
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_out_back

SLUG = "ep03_la_plante"
DUR = 15.0
COVER_T = 9.6
SILL = 1690
NX, NH = 290, 420
PX = 740
SPRAYS = [0.25, 1.45, 2.65, 3.85, 5.05]
HEIGHTS = [80, 160, 300, 520, 800, 1080]
ZOOM_T0, ZOOM_T1 = 10.2, 14.6


@lru_cache(maxsize=1)
def bg():
    b = Image.new("RGBA", (E.W, E.H), E.CREAM + (255,))
    b.alpha_composite(E.felt_panel(E.W, E.H, (250, 236, 214), seed=50, stitch=False))
    # fenêtre
    sky = E.S(820, 1080, [("rect", 0, 0, 820, 1080, 10)], E.SKY, seed=51)
    put(b, sky, 540, 950)
    for cx, cy, s in ((330, 610, 1.0), (760, 830, 0.8), (480, 1090, 0.7)):
        cl = E.S(260 * s, 120 * s, [("ellipse", 0, 30 * s, 160 * s, 120 * s), ("ellipse", 70 * s, 0, 260 * s, 110 * s)],
                 E.WHITE, seed=int(cx))
        put(b, cl, cx, cy)
    fr = E.S(900, 1160, [("rect", 0, 0, 900, 1160, 20), ("-rect", 40, 40, 860, 1120, 8)], E.WOOD, seed=52)
    put(b, fr, 540, 950)
    bar = E.S(30, 1090, [("rect", 0, 0, 30, 1090, 8)], E.WOOD, seed=53)
    put(b, bar, 540, 950)
    bar2 = E.S(830, 30, [("rect", 0, 0, 830, 30, 8)], E.WOOD, seed=54)
    put(b, bar2, 540, 950)
    # rideaux
    for x, flip in ((90, False), (990, True)):
        cu = E.S(240, 1300, [("poly", [(0, 0), (240, 0), (150, 650), (210, 1300), (0, 1300)])], E.PINK, seed=55)
        put(b, cu, x, 890, flip=flip)
    sill = E.S(1180, 120, [("rect", 0, 0, 1180, 120, 16)], E.WOOD, seed=56, anchor="top")
    put(b, sill, 540, SILL - 30)
    wall2 = E.felt_panel(E.W, E.H - SILL - 90, (238, 222, 200), seed=57, stitch=False)
    b.alpha_composite(wall2, (0, SILL + 90))
    put(b, E.duck(80), 960, SILL)
    return b


@lru_cache(maxsize=1)
def pot(cracked=False):
    sp = E.S(200, 170, [("poly", [(0, 0), (200, 0), (170, 170), (30, 170)])], (214, 110, 75), seed=60,
             anchor="bottom")
    rim = E.shape(230, 50, [("rect", 0, 0, 230, 50, 12)], (200, 98, 66), seed=61)
    img = Image.new("RGBA", (sp.img.width + 40, sp.img.height + 30), (0, 0, 0, 0))
    img.alpha_composite(sp.img, (20, 26))
    E.paste(img, rim, 0, 10)
    if cracked:
        d = ImageDraw.Draw(img)
        d.line([(120, 60), (100, 100), (130, 130), (110, 180)], fill=(90, 40, 30, 255), width=6)
    return E.Sprite(img, (img.width / 2, img.height - 4))


@lru_cache(maxsize=64)
def cactus(hq):
    h = hq
    w = min(300, 70 + 0.28 * h)
    sp = E.S(w, h, [("rect", 0, 0, w, h + w * 0.3, w / 2)], (110, 185, 115), seed=62, anchor="bottom")
    d = ImageDraw.Draw(sp.img)
    p = 6
    for k in (0.3, 0.5, 0.7):
        d.line([(p + w * k, p + w * 0.4), (p + w * k, p + h - 10)], fill=(80, 150, 90, 255), width=max(2, int(w * 0.03)))
    import random
    r = random.Random(int(h))
    for _ in range(int(h * w / 2200) + 6):
        x = p + r.uniform(0.15, 0.85) * w
        y = p + r.uniform(0.1, 0.95) * h
        d.line([(x, y), (x + 6, y - 6)], fill=(250, 245, 220, 255), width=2)
    # le sprite est plus haut que h : on recadre au niveau du pot
    img = sp.img.crop((0, 0, sp.img.width, int(h + p)))
    return E.Sprite(img, (img.width / 2, img.height))


@lru_cache(maxsize=1)
def bottle():
    body = E.S(90, 140, [("rect", 0, 30, 90, 140, 22)], (160, 210, 240), seed=63)
    head = E.shape(110, 60, [("rect", 0, 0, 70, 50, 10), ("rect", 50, 10, 110, 34, 6)], E.WHITE, seed=64)
    E.paste(body.img, head, 10, -4)
    return body


def cactus_h(t):
    h = HEIGHTS[0]
    for i, st in enumerate(SPRAYS):
        if t >= st:
            k = ease_out_back(seg(t, st + 0.1, st + 0.45), 2.2)
            h = HEIGHTS[i] + (HEIGHTS[i + 1] - HEIGHTS[i]) * k
    return h


@lru_cache(maxsize=40)
def petal(L):
    return E.S(L * 0.55, L, [("ellipse", 0, 0, L * 0.55, L)], (247, 160, 190), seed=70, anchor="bottom")


@lru_cache(maxsize=1)
def bud():
    return E.S(160, 190, [("ellipse", 0, 0, 160, 190)], (240, 140, 175), seed=71)


@lru_cache(maxsize=1)
def heart():
    return E.S(200, 200, [("circle", 100, 100, 100)], (255, 220, 110), seed=72)


def flower_center(t):
    h = cactus_h(t)
    return PX, SILL - 150 - h + 10


def scene(t, inner_blink=False):
    """La scène normale à l'instant t (avant zoom)."""
    c = bg().copy()
    h = cactus_h(t)
    top_y = SILL - 150 - h
    # cactus derrière le pot
    put(c, cactus(int(h)), PX, SILL - 150 + 18, sy=1 + 0.05 * math.sin(t * 3), jid="cac", jamp=1.2)
    E.shadow(c, PX, SILL, 260, 40)
    put(c, pot(t > 4.6), PX, SILL + 4, jid="pot", jamp=1.0)
    # fleur
    fx, fy = flower_center(t)
    if t > 6.0:
        kb = ease_out_back(seg(t, 6.0, 6.5))
        open_k = ease_in_out(seg(t, 7.0, 9.6))
        if open_k <= 0.02:
            put(c, bud(), fx, fy - 40, scale=max(0.05, kb), jid="bud")
        else:
            L = 120 + 170 * open_k
            for i in range(8):
                ang = i * 45 + 22.5 * (1 - open_k) + t * 4
                spread = 15 + 165 * open_k
                put(c, petal(int(L)), fx, fy, rot=ang if open_k > 0.5 else ang * open_k,
                    sx=0.4 + 0.6 * open_k, jid=("p", i), jamp=1.0)
            E.glow(c, fx, fy, 220, (255, 240, 170), 0.9 * open_k)
            put(c, heart(), fx, fy, scale=0.9 * open_k)
    # NUBO
    look = (1, 0)
    if t < 0.25 or inner_blink:
        look = (1, 0)
    elif t > 1.0:
        look = (0.6, -min(1.0, (h - 100) / 500))
    tuft = "curl"
    sc = False
    if t > 4.6:
        tuft = "up"
        sc = True
    eyes = 1.0
    if inner_blink:
        look, eyes = inner_blink
    E.shadow(c, NX, SILL, NH * 0.9)
    put(c, E.nubo(NH, look=look, tuft=tuft, eyes=eyes, scared=sc, arms=(18, 75), phase=t * 2), NX, SILL, jid="n")
    # vaporisateur dans la main
    put(c, bottle(), NX + 250, SILL - 290, rot=-10, jid="bt", jamp=1.0)
    # brume
    for st in SPRAYS:
        if st <= t < st + 0.5:
            k = seg(t, st, st + 0.5)
            pts = []
            for i in range(26):
                u = (i / 26 + k) % 1
                x = NX + 320 + u * (PX - NX - 340)
                y = SILL - 320 + math.sin(i * 3.1) * 40 * u + 20 * u
                pts.append((x, y, 4 + 10 * u, (220, 240, 255), 0.8 * (1 - u) * (1 - k * 0.6)))
            E.particles(c, pts)
    return c


def inner_state(t):
    """État du NUBO miniature au cœur de la fleur (mini-REGARD)."""
    look, o = E.regard_eyes(t, 12.2, (1, 0))
    if t > 13.6:
        k = ease_in_out(seg(t, 13.6, 14.2))
        look = (k, 0)
    return (look, o)


def frame(t):
    if t < ZOOM_T0:
        return scene(t)
    outer = scene(min(t, ZOOM_T0 + 0.01))
    # pétales qui continuent de s'ouvrir
    inner = scene(0.0, inner_blink=inner_state(t))
    R0 = 92
    TZ = ZOOM_T1 - 0.45
    zend = 540 / R0
    u = seg(t, ZOOM_T0, TZ)
    z = zend ** (u ** 1.5)
    fx, fy = flower_center(t)
    e = ease_in_out(seg(t, ZOOM_T0, ZOOM_T0 + 2.5))
    ccx, ccy = E.lerp(540, fx, e), E.lerp(960, fy, e)
    out = E.camera(outer, z, ccx, ccy, clamp_view=False)
    dcx, dcy = (fx - ccx) * z + 540, (fy - ccy) * z + 960
    R = R0 * z
    iw = 2 * R
    if t > TZ:
        R = E.lerp(540, 1120, ease_in_out(seg(t, TZ, ZOOM_T1)))
    if t >= ZOOM_T1:
        return inner
    ih = iw * E.H / E.W
    small = inner.resize((max(2, int(iw)), max(2, int(ih))), Image.LANCZOS)
    mask = Image.new("L", (E.W, E.H), 0)
    ImageDraw.Draw(mask).ellipse([dcx - R, dcy - R, dcx + R, dcy + R], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(1, R * 0.03)))
    layer = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
    s_ = ease_in_out(seg(t, ZOOM_T0 + 1.2, TZ))
    offx = (520 - E.W / 2) * (iw / E.W) * (1 - s_)
    offy = (1430 - E.H / 2) * (iw / E.W) * (1 - s_)
    layer.paste(small, (int(round(dcx - iw / 2 - offx)), int(round(dcy - ih / 2 - offy))))
    out = out.convert("RGBA")
    out.paste(layer, (0, 0), mask)
    return out


def sound(m):
    # boîte à musique en boucle (3/4)
    mel = ["E6", "G6", "C7", "B6", "G6", "E6", "F6", "A6", "D7", "C7", "A6", "F6",
           "E6", "G6", "C7", "D7", "B6", "G6", "C7", "G6", "E6", "C6", None, None]
    beat = 60 / 150
    for i in range(int(DUR / beat)):
        nn = mel[i % len(mel)]
        if nn:
            m.add(i * beat, A.music_box(A.NOTE(nn), 1.2), 0.35)
        if i % 3 == 0:
            m.add(i * beat, A.music_box(A.NOTE(["C5", "F5", "C5", "G5"][(i // 12) % 4]), 1.6), 0.25)
    for i, st in enumerate(SPRAYS):
        m.add(st, A.spray(0.35), 0.7, -0.3)
        m.add(st + 0.1, A.boing(260 - i * 35, 0.7), 0.6 + i * 0.05, 0.3)
    m.add(4.6, A.crunch(0.25, 7), 0.6, 0.3)
    m.add(4.65, A.squeak(1.25, 0.2), 0.5)
    m.add(6.0, A.pop(500, 900, 0.12), 0.5)
    m.add(7.0, A.choir([A.NOTE("C4"), A.NOTE("E4"), A.NOTE("G4"), A.NOTE("C5")], 3.2), 0.9)
    m.add(ZOOM_T0, A.whoosh(4.4, 200, 2500, 5) * 0.6, 0.5)
    m.add(12.95, A.regard() * 0.5, 0.5)
    m.add(12.95, A.squeak(1.6, 0.14), 0.25)
