"""ÉPISODE 09 — JOYEUX ANNIVERSAIRE."""
import math
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_in, ease_out_back

SLUG = "ep09_joyeux_anniversaire"
DUR = 20.0
COVER_T = 10.8
TABLE = 1300
NX, NH = 330, 470
CX = 700
BLOWS = [(0.55, 1.4), (3.2, 4.6), (6.3, 8.0), (9.4, 11.2)]   # (début souffle, fin)
RELIGHT = [1.6, 5.0, 8.8]


@lru_cache(maxsize=1)
def wall():
    b = Image.new("RGBA", (E.W, E.H), E.PINK + (255,))
    b.alpha_composite(E.felt_panel(E.W, E.H, (247, 190, 205), seed=91, stitch=False))
    d = ImageDraw.Draw(b)
    for y in range(120, E.H, 160):
        for x in range(60 + (y // 160 % 2) * 80, E.W, 160):
            d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(250, 220, 228, 255))
    return b


@lru_cache(maxsize=1)
def space():
    b = Image.new("RGBA", (E.W, E.H), (14, 16, 40, 255))
    r = random.Random(2)
    d = ImageDraw.Draw(b)
    for _ in range(260):
        x, y, s = r.uniform(0, E.W), r.uniform(0, 1250), r.uniform(1, 4)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 230, 255))
    earth = E.S(300, 300, [("circle", 150, 150, 150)], (90, 150, 230), seed=92)
    for (x, y, rx, ry) in ((90, 100, 70, 50), (190, 190, 80, 60)):
        cont = E.shape(2 * rx, 2 * ry, [("ellipse", 0, 0, 2 * rx, 2 * ry)], (110, 190, 110), seed=x)
        E.paste(earth.img, cont, int(x - rx), int(y - ry))
    put(b, earth, 820, 360)
    ground = E.felt_panel(E.W, E.H - 1150, (160, 160, 168), seed=93, stitch=False)
    b.alpha_composite(ground, (0, 1150))
    for (x, y, w, h) in ((150, 1220, 220, 50), (800, 1260, 160, 40), (420, 1700, 300, 80), (900, 1800, 200, 60),
                         (100, 1550, 180, 50)):
        cr = E.S(w, h, [("ellipse", 0, 0, w, h)], (130, 130, 138), seed=x)
        put(b, cr, x, y)
    return b


@lru_cache(maxsize=1)
def wall_pieces():
    w = wall()
    pieces = []
    cols, rows = 3, 2
    pw, ph = E.W // cols, (TABLE + 40) // rows
    r = random.Random(4)
    for j in range(rows):
        for i in range(cols):
            box = (i * pw, j * ph, (i + 1) * pw, (j + 1) * ph)
            im = w.crop(box)
            pieces.append((E.Sprite(im), (box[0] + pw / 2, box[1] + ph / 2), r.uniform(0.9, 1.4), r.uniform(-300, 300)))
    return pieces


@lru_cache(maxsize=1)
def bunting():
    im = Image.new("RGBA", (E.W + 100, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(x, 40 + 50 * math.sin(x / (E.W + 100) * math.pi)) for x in range(0, E.W + 101, 10)]
    d.line(pts, fill=(120, 90, 80, 255), width=5)
    cols = [(120, 200, 230), (250, 210, 90), (160, 220, 140), (190, 160, 240), (255, 140, 120)]
    for k in range(9):
        x = 40 + k * 130
        y = 40 + 50 * math.sin(x / (E.W + 100) * math.pi)
        fl = E.shape(90, 110, [("poly", [(0, 0), (90, 0), (45, 110)])], cols[k % 5], seed=100 + k)
        E.paste(im, fl, int(x), int(y))
    return E.Sprite(im)


@lru_cache(maxsize=1)
def cloth():
    sp = E.S(1000, 640, [("rect", 0, 0, 1000, 640, 30)], (252, 250, 245), seed=94, anchor="top")
    d = ImageDraw.Draw(sp.img)
    for y in range(40, 640, 110):
        for x in range(40 + (y // 110 % 2) * 55, 1000, 110):
            d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(245, 150, 175, 255))
    for x in range(0, 1010, 60):
        d.ellipse([x - 30, 610, x + 30, 670], fill=(252, 250, 245, 255))
    return sp


@lru_cache(maxsize=1)
def table_bare():
    img = Image.new("RGBA", (1000, 640), (0, 0, 0, 0))
    top = E.shape(1000, 60, [("rect", 0, 0, 1000, 60, 12)], E.WOOD, seed=95)
    E.paste(img, top, 0, 0)
    for x in (60, 900):
        leg = E.shape(50, 560, [("rect", 0, 0, 50, 560, 10)], E.darker(E.WOOD, 0.85), seed=x)
        E.paste(img, leg, x, 50)
    return E.Sprite(img, (500, 6))


@lru_cache(maxsize=1)
def cake():
    img = Image.new("RGBA", (360, 340), (0, 0, 0, 0))
    bot = E.shape(320, 150, [("rect", 0, 0, 320, 150, 26)], (245, 150, 180), seed=96)
    top = E.shape(240, 120, [("rect", 0, 0, 240, 120, 24)], (255, 240, 225), seed=97)
    E.paste(img, bot, 14, 175)
    E.paste(img, top, 54, 70)
    d = ImageDraw.Draw(img)
    for k in range(6):
        x = 70 + k * 40
        d.ellipse([x - 16, 176, x + 16, 210 + (k % 2) * 18], fill=(255, 240, 225, 255))
    for k, col in enumerate(((240, 80, 80), (90, 170, 240), (250, 210, 80), (130, 210, 120))):
        d.ellipse([90 + k * 50, 85, 102 + k * 50, 97], fill=col + (255,))
    return E.Sprite(img, (180, 330))


@lru_cache(maxsize=1)
def candle():
    sp = E.S(34, 130, [("rect", 0, 0, 34, 130, 8)], (130, 190, 250), seed=98, anchor="bottom")
    d = ImageDraw.Draw(sp.img)
    for y in range(10, 130, 30):
        d.line([(6, y + 20), (40, y)], fill=(255, 255, 255, 255), width=8)
    d.line([(23, 6), (23, -10)], fill=(40, 40, 40, 255), width=3)
    return sp


@lru_cache(maxsize=4)
def flame(size):
    s = size
    im = Image.new("RGBA", (int(80 * s) + 40, int(140 * s) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, by = im.width / 2, im.height - 20
    d.ellipse([cx - 30 * s, by - 70 * s, cx + 30 * s, by], fill=(255, 170, 40, 255))
    d.polygon([(cx - 28 * s, by - 40 * s), (cx, by - 130 * s), (cx + 28 * s, by - 40 * s)], fill=(255, 170, 40, 255))
    d.ellipse([cx - 16 * s, by - 50 * s, cx + 16 * s, by - 4], fill=(255, 235, 120, 255))
    return E.Sprite(im.filter(ImageFilter.GaussianBlur(1.5)), (cx, by))


def is_blowing(t):
    for b0, b1 in BLOWS:
        if b0 <= t < b1:
            return b0, b1
    return None


def flame_state(t):
    """(allumée, inclinaison)."""
    lit = True
    lean = math.sin(t * 9) * 4
    for (b0, b1), rl in zip(BLOWS[:3], RELIGHT):
        if b0 + 0.15 <= t < rl:
            lit = False
    bl = is_blowing(t)
    if bl and lit:
        lean = -55 + math.sin(t * 30) * 12
    return lit, lean


def scene(t):
    # fond : espace derrière, mur qui s'arrache
    c = space().copy()
    if t < 6.3:
        c.alpha_composite(wall())
    else:
        k = seg(t, 6.35, 7.6)
        for sp, (px, py), spd, rot in wall_pieces():
            ek = ease_in(k)
            vx = (px - 540) / 360
            dx = vx * 1600 * ek * spd + (rot / 300) * 300 * ek
            dy = (py - 700) * 1.2 * ek - 1600 * ek * (1.0 if abs(vx) < 0.5 else 0.35)
            put(c, sp, px + dx, py + dy, rot=rot * ease_in(k), scale=1 + 0.3 * k)
    # guirlande
    if t < 4.6:
        k = ease_in(seg(t, 3.3, 4.4))
        put(c, bunting(), 540 + 1500 * k, 140 - 300 * k, rot=-25 * k)
    # NUBO
    kw = dict(h=NH, look=(1, 0.1), tuft="curl", arms=(18, 18))
    sx = sy = 1.0
    bl = is_blowing(t)
    for b0, b1 in BLOWS:
        if b0 - 0.6 <= t < b0:
            k = seg(t, b0 - 0.6, b0)
            sx, sy = 1 + 0.12 * k, 1 + 0.05 * k
            kw["cheeks"] = True
            kw["eyes"] = 1 - 0.7 * k
    if bl:
        b0, b1 = bl
        k = seg(t, b0, b1)
        sx = 1.12 - 0.22 * ease_out(k)
        kw["eyes"] = 0.25
        kw["tuft"] = "up"
        if b0 > 9:
            sy = 1 - 0.35 * ease_out(k)
            sx = 1.12 - 0.05 * k
    if t >= 11.2:
        sy, sx = 0.65, 1.07
        kw["eyes"] = 0.55
        kw["tuft"] = "down"
        kw["look"] = (1, -0.2)
    if t >= 14.0:
        kw["eyes"] = 1.0
        kw["look"] = (1, -0.4)
    if 15.9 <= t:
        kw["scared"] = t < 16.6
        kw["tuft"] = "up" if t < 16.6 else "out"
        kw["phase"] = t * 2
    if t >= 18.2:
        kw["look"], kw["eyes"] = E.regard_eyes(t, 18.4, (1, -0.4))
    if t >= 19.75:
        kw["tuft"] = "curl"
        kw["cheeks"] = True
        sx, sy = 1.08, 1.0
    y = TABLE + 60
    put(c, E.nubo(**kw), NX, y, sx=sx, sy=sy, jid="n")
    # table
    if t < 9.5:
        put(c, cloth(), 540, TABLE, jid="cloth", jamp=1.0, jrot=0.2)
    else:
        put(c, table_bare(), 540, TABLE, jid="tb", jamp=1.0)
        k = seg(t, 9.5, 10.6)
        if k < 1:
            put(c, cloth(), 540 + 1500 * ease_in(k), TABLE - 200 * k, rot=-40 * k)
    # gâteau
    put(c, cake(), CX, TABLE + 10, jid="cake", jamp=1.0)
    lit, lean = flame_state(t)
    sc = 1.0
    if 15.0 <= t < 16.6:
        sc = 1 + 1.4 * ease_out(seg(t, 15.0, 15.8))
        lean = 40 * ease_in_out(seg(t, 15.3, 15.9))
    if t >= 16.6:
        sc = 1.0 + 0.4 * (1 - seg(t, 16.6, 17.2))
    put(c, candle(), CX, TABLE - 300, jid="cnd", jamp=0.6)
    if lit:
        E.glow(c, CX, TABLE - 470, 120 * sc, (255, 200, 100), 0.6)
        put(c, flame(round(sc * 4) / 4), CX, TABLE - 430, rot=lean, sx=1 + 0.08 * math.sin(t * 20))
    else:
        k = 1 - seg(t, 0, 99)
        E.particles(c, [(CX + math.sin(t * 5 + i) * 15, TABLE - 450 - i * 30 - (t * 80 % 30), 10 + i * 2,
                         (220, 220, 225), 0.45 - i * 0.07) for i in range(6)])
    # souffle de NUBO
    if bl:
        b0, b1 = bl
        k = seg(t, b0, b1)
        power = 1 + BLOWS.index(bl) * 0.8
        r = random.Random(int(t * 12))
        lines = []
        for i in range(int(10 * power)):
            x0 = NX + 180 + ((t * 1600 + i * 137) % 900)
            yy = TABLE - 260 + r.uniform(-120, 120) * power * 0.7
            lines.append((x0, yy, x0 + 160, yy))
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for x0, y0, x1, y1 in lines:
            d.line([(x0, y0), (x1, y1)], fill=(255, 255, 255, 150), width=6)
        c.alpha_composite(ov)
    # souffle de la bougie vers NUBO
    if 15.9 <= t < 16.7:
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for i in range(10):
            x0 = CX - 120 - ((t * 1500 + i * 97) % 380)
            yy = TABLE - 440 + (i % 5 - 2) * 30
            d.line([(x0, yy), (x0 - 130, yy + 10)], fill=(255, 255, 255, 160), width=6)
        c.alpha_composite(ov)
    put(c, E.duck(70), 980, TABLE - 8)
    return c


def frame(t):
    c = scene(t)
    shake = 0
    if 6.3 < t < 7.3:
        shake = 18
    if 9.4 < t < 10.0:
        shake = 10
    r = E.rng_for("sh", E.FRAME)
    z = 1.22
    if 15.0 <= t < 17.0:
        z = 1.22 + 0.35 * ease_in_out(seg(t, 15.0, 15.8))
    return E.camera(c, z, 540 + r.uniform(-shake, shake), 1000 + r.uniform(-shake, shake))


def sound(m):
    # « Joyeux anniversaire » (domaine public) au kazoo
    hb = [(0, "C5", 0.75), (0.75, "C5", 0.25), (1, "D5", 1), (2, "C5", 1), (3, "F5", 1), (4, "E5", 2),
          (6, "C5", 0.75), (6.75, "C5", 0.25), (7, "D5", 1), (8, "C5", 1), (9, "G5", 1), (10, "F5", 2),
          (12, "C5", 0.75), (12.75, "C5", 0.25), (13, "C6", 1), (14, "A5", 1), (15, "F5", 1), (16, "E5", 1),
          (17, "D5", 1), (18, "A#5", 0.75), (18.75, "A#5", 0.25), (19, "A5", 1), (20, "F5", 1), (21, "G5", 1),
          (22, "F5", 2)]
    bpm = 200
    kz = A.Mix(10.0)
    kz.seq(0.0, bpm, hb, A.kazoo, 0.6)
    kz.seq(0.0, bpm, [(b, n, d) for b, n, d in hb if b % 3 == 0], lambda f, d: A.pizz(f / 2, d), 0.4)
    x = kz.L
    # le souffle « tord » la musique : on la coupe au moment où les murs partent
    g = np.ones(len(x))
    g[int(6.3 * A.SR):] = 0
    for b0, b1 in BLOWS[:2]:
        a, b = int(b0 * A.SR), int(b1 * A.SR)
        g[a:b] *= 0.5 + 0.3 * np.sin(np.linspace(0, 40, b - a))
    m.add(0, x * g, 0.8)
    for i, (b0, b1) in enumerate(BLOWS):
        m.add(b0 - 0.6, A.vowel(200, 260, 0.5, ((300, 700), (700, 1200))) * np.linspace(0, 0.4, int(0.5 * A.SR)), 0.4)
        m.add(b0, A.wind(b1 - b0, 1.0 + i * 0.6, seed=i), 0.6 + i * 0.15)
        m.add(b0, A.whoosh(b1 - b0, 200, 3000, i + 3), 0.5 + 0.2 * i)
    for rl in RELIGHT:
        m.add(rl, A.pop(300, 900, 0.1), 0.7)
        m.add(rl + 0.05, A.squeak(1.2, 0.12), 0.25)
    m.add(3.4, A.flap(0.9), 0.5)
    m.add(6.3, A.crash(1.5, 4), 0.9)
    m.add(6.35, A.whoosh(1.2, 100, 1500, 9), 0.9)
    m.add(9.4, A.wind(1.8, 3.0, 11), 0.9)
    m.add(9.5, A.whoosh(1.0, 300, 3000, 12), 0.6)
    m.add(11.2, A.vowel(220, 120, 0.7, ((300, 700), (700, 1100))) * np.linspace(0.5, 0, int(0.7 * A.SR)), 0.6)
    m.add(11.2, A.drone(4.0, 55) * 0.4, 0.3)
    # la bougie inspire puis souffle
    inh = A.whoosh(0.8, 300, 2500, 13) * np.linspace(0.2, 1.2, int(0.8 * A.SR))
    m.add(15.0, inh, 0.7)
    m.add(15.9, A.wind(0.8, 1.6, 14), 0.8)
    m.add(16.6, A.tsss(1.0), 0.8)
    m.add(16.65, A.squeak(0.8, 0.25), 0.5)
    m.add(19.15, A.nub(0.85), 0.5)
    m.add(19.15, A.regard(), 0.6)
    m.add(19.75, A.pop(300, 900, 0.1), 0.6)
