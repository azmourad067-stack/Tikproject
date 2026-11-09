"""ÉPISODE 05 — LE CONCOURS DE REGARD."""
import math
import random
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_out_back, keys

SLUG = "ep05_concours_de_regard"
DUR = 22.0
COVER_T = 13.2
TABLE = 1420
NX, NH = 300, 440
BX, BY, BR = 790, 1180, 240   # bocal


@lru_cache(maxsize=1)
def bg():
    b = E.room_bg(E.LAVENDER, E.WOOD, floor_y=TABLE - 60, wall_pattern="stripes", seed=21, baseboard=False)
    edge = E.S(1100, 60, [("rect", 0, 0, 1100, 60, 12)], E.darker(E.WOOD, 0.85), seed=22, anchor="top")
    put(b, edge, 540, TABLE - 70)
    put(b, E.duck(70), 1000, TABLE + 140)
    return b


@lru_cache(maxsize=4)
def fish(blink=False):
    w, h = 230, 150
    img = Image.new("RGBA", (w + 120, h + 60), (0, 0, 0, 0))
    tail = E.shape(110, 130, [("poly", [(0, 65), (110, 0), (85, 65), (110, 130)])], (245, 150, 50), seed=31)
    body = E.shape(w, h, [("ellipse", 0, 0, w, h)], (250, 165, 50), seed=32)
    fin = E.shape(80, 60, [("poly", [(0, 60), (40, 0), (80, 60)])], (240, 140, 45), seed=33)
    E.paste(img, tail, w - 10, 30)
    E.paste(img, fin, 90, 0)
    E.paste(img, body, 0, 30)
    d = ImageDraw.Draw(img)
    ex, ey, r = 62, 85, 26
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 255, 255, 255))
    d.ellipse([ex - 15, ey - 15, ex + 13, ey + 13], fill=(20, 20, 20, 255))
    d.ellipse([ex - 9, ey - 10, ex - 2, ey - 3], fill=(255, 255, 255, 255))
    d.arc([22, 105, 52, 125], 200, 340, fill=(160, 70, 20, 255), width=4)
    return E.Sprite(img, (img.width / 2, img.height / 2))


@lru_cache(maxsize=1)
def bowl_back():
    im = Image.new("RGBA", (2 * BR + 40, 2 * BR + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = BR + 20
    d.ellipse([c - BR, c - BR, c + BR, c + BR], fill=(220, 240, 255, 60))
    water = Image.new("L", im.size, 0)
    ImageDraw.Draw(water).ellipse([c - BR + 6, c - BR + 6, c + BR - 6, c + BR - 6], fill=255)
    cut = Image.new("L", im.size, 0)
    ImageDraw.Draw(cut).rectangle([0, c - BR * 0.45, im.width, im.height], fill=255)
    from PIL import ImageChops
    wm = ImageChops.multiply(water, cut)
    wl = Image.new("RGBA", im.size, (120, 190, 235, 0))
    wl.putalpha(wm.point(lambda v: int(v * 0.55)))
    im.alpha_composite(wl)
    sand = E.shape(2 * BR * 0.8, 70, [("ellipse", 0, 0, 2 * BR * 0.8, 120)], (235, 210, 160), seed=34)
    E.paste(im, sand, int(c - BR * 0.8 - 6), int(c + BR - 85))
    return im


@lru_cache(maxsize=1)
def bowl_front():
    im = Image.new("RGBA", (2 * BR + 40, 2 * BR + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = BR + 20
    d.ellipse([c - BR, c - BR, c + BR, c + BR], outline=(255, 255, 255, 140), width=7)
    d.arc([c - BR * 0.85, c - BR * 0.85, c + BR * 0.85, c + BR * 0.85], 200, 245, fill=(255, 255, 255, 210), width=16)
    d.ellipse([c - BR * 0.62, c - BR - 16, c + BR * 0.62, c - BR + 30], outline=(255, 255, 255, 170), width=8)
    return im.filter(ImageFilter.GaussianBlur(1.2))


@lru_cache(maxsize=1)
def trophy():
    return E.S(170, 210, [("ellipse", 0, 0, 170, 120), ("rect", 65, 90, 105, 170, 6), ("rect", 25, 160, 145, 210, 10),
                          ("-ellipse", 30, 0, 140, 50)], (245, 200, 60), seed=40, anchor="bottom")


@lru_cache(maxsize=1)
def tumbleweed():
    r = random.Random(3)
    im = Image.new("RGBA", (190, 190), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(40):
        a0 = r.uniform(0, 360)
        rr = r.uniform(30, 85)
        cx, cy = 95 + r.uniform(-15, 15), 95 + r.uniform(-15, 15)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a0 + r.uniform(60, 200), fill=(170, 130, 80, 255), width=5)
    return E.Sprite(im)


CROWD_COLS = [(120, 200, 230), (240, 140, 180), (160, 220, 140), (250, 210, 100), (190, 160, 240), (240, 160, 120),
              (140, 180, 250), (230, 120, 120)]


@lru_cache(maxsize=64)
def fan(i, closed=False, look=0):
    col = CROWD_COLS[i % len(CROWD_COLS)]
    w = 150 + (i * 37) % 50
    h = 170 + (i * 53) % 60
    sp = E.S(w, h, [("ellipse", 0, 0, w, h * 1.3)], col, seed=50 + i, anchor="bottom")
    img = sp.img.crop((0, 0, sp.img.width, int(h + 6)))
    d = ImageDraw.Draw(img)
    for sx in (0.36, 0.64):
        x, y = 6 + w * sx + look * 6, 6 + h * 0.35
        if closed:
            d.arc([x - 10, y - 8, x + 10, y + 8], 20, 160, fill=(20, 20, 20, 255), width=4)
        else:
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(20, 20, 20, 255))
            d.ellipse([x - 6, y - 7, x - 1, y - 2], fill=(255, 255, 255, 255))
    return E.Sprite(img, (img.width / 2, img.height))


@lru_cache(maxsize=2)
def banner(kind):
    im = Image.new("RGBA", (210, 330), (0, 0, 0, 0))
    stick = E.shape(16, 200, [("rect", 0, 0, 16, 200, 4)], E.WOOD, seed=60)
    E.paste(im, stick, 97, 120)
    board = E.shape(200, 140, [("rect", 0, 0, 200, 140, 10)], E.WHITE, seed=61)
    E.paste(im, board, 0, 0)
    d = ImageDraw.Draw(im)
    if kind == 0:
        d.ellipse([60, 30, 150, 120], fill=E.ORANGE + (255,))
        d.ellipse([82, 62, 94, 74], fill=(0, 0, 0, 255))
        d.ellipse([116, 62, 128, 74], fill=(0, 0, 0, 255))
        d.line([(110, 30), (106, 12), (120, 8)], fill=E.ORANGE + (255,), width=7)
    else:
        d.ellipse([50, 45, 140, 105], fill=(250, 165, 50, 255))
        d.polygon([(135, 75), (175, 45), (175, 105)], fill=(245, 150, 50, 255))
        d.ellipse([66, 64, 80, 78], fill=(0, 0, 0, 255))
    return E.Sprite(im, (105, 320))


FANS = [(i, 60 + (i % 7) * 160 + (i // 7) * 70, 900 + (i // 7) * 120, 6.0 + i * 0.16) for i in range(14)]


def wide(t, mood=None):
    c = bg().copy()
    # cycle du temps (accéléré)
    night = 0
    if 10.0 < t < 14.0:
        night = max(seg(t, 10.0, 10.6) * (1 - seg(t, 11.4, 12.0)), 0)
    # supporters
    if t > 6.0:
        for i, x, y, t0 in FANS:
            if t < t0:
                continue
            k = ease_out_back(seg(t, t0, t0 + 0.35))
            jump = 0
            if 15.5 < t < 18.5:
                jump = abs(math.sin((t - 15.5) * 9 + i)) * 60
            else:
                jump = abs(math.sin(t * 5 + i)) * 10
            closed = night > 0.5 and i % 3 != 0
            look = 1 if (int(t * 1.3) + i) % 2 else -1
            put(c, fan(i, closed, look), x, y - jump, scale=max(0.05, k), jid=("f", i), jamp=1.2)
            if i in (2, 9) and k > 0.5:
                put(c, banner(0 if i == 2 else 1), x + 50, y - 60 - jump, rot=math.sin(t * 4 + i) * 8, jid=("b", i))
    # bocal & poisson
    c.alpha_composite(bowl_back(), (BX - BR - 20, BY - BR - 20))
    fy = BY + 40 + math.sin(t * 1.7) * 14
    put(c, fish(), BX - 10 + math.sin(t * 0.9) * 6, fy, jid="fish", jamp=1.0)
    bub = [(BX - 60 + 30 * math.sin(i + t), BY + 160 - ((t * 60 + i * 70) % 300), 6 + i % 3, (230, 245, 255), 0.7)
           for i in range(4)]
    E.particles(c, bub)
    c.alpha_composite(bowl_front(), (BX - BR - 20, BY - BR - 20))
    if t > 17.0:
        k = seg(t, 17.0, 17.45)
        y = E.lerp(-200, BY - BR + 10, E.bounce_out(k))
        put(c, trophy(), BX, y, jid="trophy", jamp=1.0)
    # NUBO
    kw = dict(h=NH, look=(1, 0), eyes=0.45, tuft="curl", arms=(18, 18))
    sx = sy = 1.0
    if t > 4.0:
        kw["sweat"] = 15.8 > t
    if 10.0 < t:
        kw["beard"] = ease_in_out(seg(t, 10.2, 13.8))
    if 14.0 < t < 15.5:
        r = E.rng_for("tr", E.FRAME)
        kw["look"] = (1 + r.uniform(-0.25, 0.25), r.uniform(-0.25, 0.25))
        kw["eyes"] = 0.45 + r.uniform(-0.15, 0.25)
        kw["tuft"] = "up"
    if 15.5 <= t < 17.2:
        kw["eyes"] = 0.0 if t < 15.85 else 1.0
        kw["scared"] = True
        kw["tuft"] = "up"
    if t >= 17.2:
        k = ease_out(seg(t, 17.2, 17.6))
        sy, sx = 1 - 0.18 * k, 1 + 0.08 * k
        kw["tuft"] = "down"
        kw["eyes"] = 0.6
        kw["look"] = (0.5, 0.6)
        if t > 19.2:
            look, o = E.regard_eyes(t, 19.2, (0.5, 0.6))
            kw["look"], kw["eyes"] = look, o
    E.shadow(c, NX, TABLE + 40, NH * 0.9)
    put(c, E.nubo(**kw), NX, TABLE + 40, sx=sx, sy=sy, jid="n")
    # virevoltant
    if 4.4 < t < 6.4:
        k = seg(t, 4.4, 6.4)
        put(c, tumbleweed(), E.lerp(-150, 1250, k), TABLE + 120 - abs(math.sin(k * 14)) * 50, rot=-k * 900)
    # nuit / neige / feuilles
    if night > 0:
        ov = Image.new("RGBA", c.size, (20, 25, 70, int(150 * night)))
        c.alpha_composite(ov)
        stars = [((i * 137) % E.W, (i * 89) % 700 + 60, 4, (255, 255, 220), night) for i in range(30)]
        E.particles(c, stars)
        put(c, moon(), 880, 260 - seg(t, 10.0, 11.8) * 120, alpha=night)
    if 11.6 < t < 12.9:
        k = seg(t, 11.6, 12.9)
        E.particles(c, [((i * 97 + 30 * math.sin(t * 2 + i)) % E.W, (i * 173 + t * 420) % E.H, 7 + i % 4,
                         (255, 255, 255), 0.9 * math.sin(math.pi * k)) for i in range(70)])
    if 12.6 < t < 14.0:
        k = seg(t, 12.6, 14.0)
        cols = [(230, 120, 40), (210, 70, 40), (240, 180, 60)]
        r = random.Random(5)
        for i in range(26):
            x = (r.uniform(0, E.W) + 40 * math.sin(t * 3 + i)) % E.W
            y = (r.uniform(0, E.H) + t * 300) % E.H
            put(c, leaf(i % 3), x, y, rot=t * 200 + i * 40, alpha=math.sin(math.pi * k))
    # feux d'artifice
    for t0, fx, fy, col in ((17.3, 300, 380, (255, 120, 180)), (17.8, 800, 300, (120, 220, 255)),
                            (18.4, 540, 520, (255, 230, 90)), (18.9, 200, 600, (160, 255, 140))):
        if t0 < t < t0 + 1.0:
            k = seg(t, t0, t0 + 1.0)
            E.particles(c, [(fx + math.cos(a / 14 * 6.283) * 260 * ease_out(k),
                             fy + math.sin(a / 14 * 6.283) * 260 * ease_out(k) + 80 * k * k, 10 * (1 - k) + 3,
                             col, 1 - k) for a in range(14)])
    # confettis
    if 15.5 < t < 18.0:
        r = random.Random(9)
        k = seg(t, 15.5, 18.0)
        conf = []
        for i in range(60):
            x = r.uniform(0, E.W) + math.sin(t * 4 + i) * 30
            y = -50 + (r.uniform(0, 400) + (t - 15.5) * r.uniform(300, 700))
            conf.append((x, y, 9, CROWD_COLS[i % 8], 1 - k * 0.5))
        E.particles(c, conf)
    return c


@lru_cache(maxsize=1)
def moon():
    return E.S(140, 140, [("circle", 70, 70, 70), ("-circle", 105, 50, 60)], (250, 245, 200), seed=70)


@lru_cache(maxsize=3)
def leaf(i):
    cols = [(230, 120, 40), (210, 70, 40), (240, 180, 60)]
    return E.S(46, 30, [("ellipse", 0, 0, 46, 30)], cols[i], seed=80 + i)


@lru_cache(maxsize=1)
def water_bg():
    b = Image.new("RGBA", (E.W, E.H), (110, 180, 225, 255))
    b.alpha_composite(E.felt_panel(E.W, E.H, (120, 185, 230), seed=90, stitch=False))
    return b


def fish_ecu(t):
    c = water_bg().copy()
    sc = 1 + 0.08 * seg(t % 2, 0, 1)
    eye = E.S(820, 820, [("circle", 410, 410, 410)], (250, 160, 50), seed=91)
    put(c, eye, 540, 960, scale=sc, jid="fe", jamp=3)
    d = ImageDraw.Draw(c)
    cx, cy = 520, 960
    for r, col in ((300 * sc, (255, 255, 255)), (210 * sc, (215, 160, 40)), (140 * sc, (15, 15, 18))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,))
    d.ellipse([cx - 110 * sc, cy - 120 * sc, cx - 30 * sc, cy - 40 * sc], fill=(255, 255, 255, 240))
    d.ellipse([cx + 50 * sc, cy + 50 * sc, cx + 80 * sc, cy + 80 * sc], fill=(255, 255, 255, 150))
    E.particles(c, [(200 + i * 160, (1700 - (t * 300 + i * 260) % 1900), 14 + i % 3 * 6, (225, 245, 255), 0.7)
                    for i in range(5)])
    return c


@lru_cache(maxsize=1)
def bg_blur():
    return bg().filter(ImageFilter.GaussianBlur(14))


def nubo_ecu(t):
    c = bg_blur().copy()
    eyes = 0.45
    sp = E.nubo(1100, eyes=eyes, look=(0.3, 0), tuft="curl")
    sc = 1.55 + 0.06 * t
    put(c, sp, 540, 960 + 0.586 * 1100 * sc, scale=sc, jid="ne", jamp=4)
    return c


def frame(t):
    if t < 1.0:
        return nubo_ecu(t)
    if t < 1.8 or t >= 21.2:
        return fish_ecu(t)
    w = wide(t)
    if 3.0 <= t < 3.5:
        return E.camera(w, 2.4, NX, TABLE - 0.586 * NH)
    if 3.5 <= t < 4.0:
        return E.camera(w, 2.4, BX, BY + 40)
    if 4.0 <= t < 4.4:
        return E.camera(w, 3.0, NX, TABLE - 0.586 * NH)
    if 14.0 <= t < 15.5:
        z = 1 + 1.4 * ease_in_out(seg(t, 14.0, 15.4))
        return E.camera(w, z, NX + 60, TABLE - 0.586 * NH)
    return E.camera(w, 1.22, 540, 1090)


def sound(m):
    # thème de western sifflé (original)
    m.add(0.03, A.ding(1250, 2.0, 1.5), 0.7)
    m.add(1.0, A.karplus(82, 1.4, 0.998), 0.8)
    m.add(1.85, A.ding(1250, 2.0, 1.5), 0.5)
    m.seq(2.0, 100, [(0, "A5", 0.5), (0.5, "D6", 0.5), (1, "A5", 0.5), (1.5, "D6", 0.5), (2, "A5", 2),
                     (4, "F5", 0.5), (4.5, "G5", 0.5), (5, "D5", 2.5)], A.whistle, 0.55)
    for b in range(0, 8, 2):
        m.add(2.0 + b * 0.6, A.karplus(73.4, 1.0, 0.997, seed=b), 0.6)
    m.add(3.0, A.whoosh(0.35, 500, 4000, 2), 0.5)
    m.add(3.5, A.whoosh(0.35, 500, 4000, 3), 0.5)
    m.add(4.0, A.whoosh(0.35, 500, 4000, 4), 0.5)
    m.add(4.4, A.wind(2.2, 0.8), 0.6)
    # foule
    m.add(6.0, A.crowd(4.0, 3), 0.35)
    for i, x, y, t0 in FANS:
        m.add(t0, A.pop(500 + i * 40, 900 + i * 40, 0.08), 0.25, (x - 540) / 600)
    # accéléré
    m.add(10.0, A.whoosh(4.0, 150, 1500, 8), 0.6)
    m.add(10.0, A.boing(90, 4.0) * 0.4, 0.4)
    for k in range(12):
        m.add(10.1 + k * 0.32, A.tick(k % 2 == 0), 0.35)
    m.add(11.6, A.wind(1.4, 0.7, 4), 0.5)
    # tension
    m.add(14.0, A.drone(1.6, 73), 0.9)
    m.add(14.0, A.horror_screech(1.5) * 0.25, 0.3)
    m.add(15.5, A.gong(4.0, 70), 1.0)
    m.add(15.55, A.crowd(3.0, 7), 0.8)
    for t0 in (17.3, 17.8, 18.4, 18.9):
        m.add(t0 - 0.5, A.firework(int(t0 * 10)), 0.5, (t0 * 3 % 2) - 1)
    m.add(17.35, A.ding(1800, 1.0), 0.5)
    m.seq(17.6, 90, [(0, "D4", 0.9), (1, "C#4", 0.9), (2, "C4", 0.9)], A.brass, 0.6)
    m.add(17.6 + 3 * 60 / 90, A.brass(A.NOTE("B3"), 1.4) * 1.0, 0.6)
    m.add(19.95, A.nub(0.85), 0.5)
    m.add(19.95, A.regard(), 0.6)
    m.add(21.2, A.ding(1250, 1.0, 1.5) * 0.6, 0.5)
