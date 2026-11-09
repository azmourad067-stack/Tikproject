"""ÉPISODE 01 — ATCHOUM."""
import math
import random
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, keys

SLUG = "ep01_atchoum"
DUR = 18.0
COVER_T = 10.5
FLOOR = 1470
NX, NH = 540, 520
SNEEZES = [1.2, 2.8, 4.0] + [5.0, 5.5, 5.95, 6.35, 6.75, 7.1, 7.45, 7.8, 8.1, 8.4, 8.7]
PILE_T0, PILE_T1 = 4.6, 10.2
PILE_TOP = 470


# ---------------------------------------------------------------- décors
@lru_cache(maxsize=1)
def bg_room():
    bg = E.room_bg(E.LAVENDER, E.CREAM, floor_y=FLOOR - 70, wall_pattern="dots", seed=2)
    # cadre au mur avec un soleil
    fr = E.S(300, 360, [("rect", 0, 0, 300, 360, 18), ("-rect", 34, 34, 266, 326, 8)], E.WOOD, seed=5)
    inner = E.S(232, 292, [("rect", 0, 0, 232, 292, 6)], E.MINT, seed=6)
    sun = E.S(110, 110, [("circle", 55, 55, 55)], E.DUCK, seed=7)
    hill = E.S(232, 120, [("ellipse", -60, 0, 300, 240)], E.GREEN, seed=8)
    put(bg, inner, 230, 560)
    put(bg, sun, 270, 500)
    put(bg, hill, 230, 680)
    put(bg, fr, 230, 560)
    # étagère + plante
    sh = E.S(330, 34, [("rect", 0, 0, 330, 34, 8)], E.WOOD, seed=9)
    put(bg, sh, 830, 880)
    pot = E.S(90, 90, [("poly", [(0, 0), (90, 0), (75, 90), (15, 90)])], (220, 120, 90), seed=10)
    leaf = E.S(150, 150, [("ellipse", 50, 0, 100, 110), ("ellipse", 0, 40, 70, 90), ("ellipse", 80, 40, 150, 90)],
               (110, 180, 120), seed=11)
    put(bg, leaf, 760, 780)
    put(bg, pot, 760, 820)
    return bg.convert("RGBA")


@lru_cache(maxsize=1)
def bg_shop():
    bg = E.room_bg(E.MINT, E.WOOD, floor_y=1560, wall_pattern="stripes", seed=4, baseboard=False)
    return bg


@lru_cache(maxsize=1)
def machine():
    """Distributeur de boules : (sprite corps, centre globe, rayon)."""
    w, h = 1080, 1920
    layers = []
    base = E.S(520, 560, [("poly", [(60, 0), (460, 0), (520, 560), (0, 560)])], (225, 70, 70), seed=20)
    neck = E.S(300, 80, [("rect", 0, 0, 300, 80, 16)], (200, 60, 60), seed=21)
    cap = E.S(220, 130, [("ellipse", 0, 0, 220, 220)], (225, 70, 70), seed=22)
    plate = E.S(200, 200, [("circle", 100, 100, 100)], (190, 190, 200), seed=23)
    chute = E.S(170, 120, [("rect", 0, 0, 170, 120, 22)], (120, 120, 130), seed=24)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    put(img, base, 540, 1300)
    put(img, neck, 540, 1035)
    put(img, plate, 540, 1210)
    put(img, chute, 540, 1440)
    capimg = cap
    return img, capimg


@lru_cache(maxsize=1)
def crank():
    return E.S(160, 40, [("rect", 0, 0, 160, 40, 18), ("circle", 150, 20, 26)], (150, 150, 160), seed=25,
               anchor=(20, 20))


@lru_cache(maxsize=1)
def coin():
    return E.S(70, 70, [("circle", 35, 35, 35)], (215, 215, 225), seed=26)


@lru_cache(maxsize=1)
def globe_glass():
    r = 300
    im = Image.new("RGBA", (2 * r + 40, 2 * r + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = r + 20
    d.ellipse([c - r, c - r, c + r, c + r], outline=(255, 255, 255, 120), width=8)
    d.arc([c - r * 0.8, c - r * 0.8, c + r * 0.8, c + r * 0.8], 200, 250, fill=(255, 255, 255, 200), width=18)
    d.arc([c - r * 0.7, c - r * 0.7, c + r * 0.7, c + r * 0.7], 260, 275, fill=(255, 255, 255, 170), width=12)
    return im.filter(ImageFilter.GaussianBlur(1.5))


@lru_cache(maxsize=1)
def chute_bg():
    bg = Image.new("RGBA", (E.W, E.H), (90, 90, 100, 255))
    inner = E.felt_panel(E.W, E.H, (105, 105, 118), seed=30, stitch=False)
    bg.alpha_composite(inner)
    d = ImageDraw.Draw(bg)
    for y in (300, 1650):
        d.rectangle([0, y, E.W, y + 26], fill=(70, 70, 80, 255))
    flap = E.S(1100, 300, [("rect", 0, 0, 1100, 300, 40)], (225, 70, 70), seed=31)
    put(bg, flap, 540, 120)
    floor = E.felt_panel(E.W, 400, (140, 140, 152), seed=32, stitch=True)
    bg.alpha_composite(floor, (0, 1520))
    return bg


# ---------------------------------------------------------------- tas de mini-NUBO
@lru_cache(maxsize=1)
def pile_balls():
    r = random.Random(4)
    balls = []
    dy, dx = 46, 62
    y = 1990
    row = 0
    while y > PILE_TOP - 40:
        x = -20 + (row % 2) * dx / 2
        while x < E.W + 40:
            balls.append((x + r.uniform(-8, 8), y + r.uniform(-6, 6), r.randrange(9)))
            x += dx
        y -= dy
        row += 1
    balls.sort(key=lambda b: -b[1])
    return balls


def pile_level(t):
    k = seg(t, PILE_T0, PILE_T1)
    k = 1 - (1 - k) ** 1.4
    return 2000 - k * (2000 - PILE_TOP)


LOOKS = [(-1, -0.5), (0, -1), (1, -0.5), (-1, 0.5), (0, 0), (1, 0.5), (0.6, -0.8), (-0.6, 0.8), (0, 0.6)]


@lru_cache(maxsize=64)
def mini_rot(v, blink):
    sp = mini(v, blink, 96)
    img, ax, ay = E.transform(sp, rot=(v * 37 % 50) - 25, scale=0.9 + (v * 13 % 5) * 0.06)
    return E.Sprite(img, (ax, ay))


def mini(i, blink=False, h=86):
    return E.nubo(h, look=LOOKS[i % 9], eyes=0.0 if blink else 1.0, tuft="curl")


# ---------------------------------------------------------------- NUBO principal
def sneeze_state(t):
    """(sx, sy, ouverture des yeux) autour des éternuements."""
    sx = sy = 1.0
    o = 1.0
    for st in SNEEZES:
        pre = 1.1 if st < 4.5 else 0.25
        if st - pre <= t < st:
            k = seg(t, st - pre, st)
            sy = 1 + 0.12 * k
            sx = 1 + 0.06 * k
            o = 1 - 0.8 * k
        elif st <= t < st + 0.35:
            k = seg(t, st, st + 0.35)
            sx = 1.17 - 0.17 * ease_out(k)
            sy = 0.86 + 0.14 * ease_out(k)
            o = 0.0 if k < 0.4 else 0.8
    return sx, sy, o


# Mini-NUBO explicites des premiers éternuements : (temps, x_fin, y_fin, variante)
EXPL = [(1.2, 260, 1560, 2), (2.8, 160, 1640, 5), (2.8, 820, 1600, 0), (2.8, 940, 1700, 3),
        (4.0, 380, 1720, 6), (4.0, 690, 1690, 1), (4.0, 120, 1800, 7), (4.0, 880, 1830, 4)]


def draw_room(t):
    c = bg_room().copy()
    put(c, E.duck(80), 900, 860)
    lvl = pile_level(t)
    foot = min(FLOOR, lvl + 0.45 * NH)
    # NUBO principal
    sx, sy, o = sneeze_state(t)
    look = (0, 0)
    tuft = "curl"
    if 1.5 < t < 2.5:
        look = (-1, 0.6)
    if 9.6 < t < 10.3:
        look = (-1, 0)
    elif 10.3 < t < 10.9:
        look = (1, 0)
    if 11.0 <= t < 11.6:
        o = min(o, abs(1 - 2 * seg(t, 11.0, 11.6)))
    if 5 < t < 9.2:
        tuft = "up"
    ph = t * 3 if t < 1.2 else 0
    if foot >= FLOOR - 1:
        E.shadow(c, NX, FLOOR, NH * 0.9)
    put(c, E.nubo(NH, eyes=o, look=look, tuft=tuft, phase=ph, arms=(25, 25)), NX, foot, sx=sx, sy=sy, jid="nubo")
    # mini-NUBO explicites (avant la marée)
    for i, (st, xe, ye, v) in enumerate(EXPL):
        if t < st:
            continue
        k = seg(t, st, st + 0.6)
        x = E.lerp(NX + (xe - NX) * 0.1, xe, k)
        ybase = E.lerp(FLOOR - NH * 0.55, ye, k)
        hop = math.sin(math.pi * min(1, k * 1.0)) * 260 * (1 - k * 0.5)
        y = ybase - hop
        if k >= 1:
            y = ye - abs(math.sin((t - st - 0.6) * 9)) * 30 * math.exp(-(t - st - 0.6) * 5)
        lk = (-1, -0.6) if (i == 0 and 1.6 < t < 2.6) else LOOKS[v]
        sp = E.nubo(86, look=lk, eyes=1.0)
        E.shadow(c, x, ye + 4, 70, alpha=0.2)
        put(c, sp, x, y, rot=(1 - k) * 360 * (1 if i % 2 else -1), jid=("m", i))
    # la marée orange
    balls = pile_balls()
    for i, (x, y, v) in enumerate(balls):
        if y < lvl:
            continue
        # moment d'apparition approximatif de cette boule
        appear = PILE_T0 + (PILE_T1 - PILE_T0) * (1 - ((y - PILE_TOP) / (2000 - PILE_TOP)) ** (1 / 1.4)) if y < 2000 else PILE_T0
        drop = 1 - seg(t, appear, appear + 0.3)
        blink = ((i * 7 + E.FRAME) % 53) == 0
        put(c, mini_rot(v, blink), x, y + 40 - drop * 160, jid=("b", i), jamp=1.5, jrot=0)
    return c


def draw_shop(t, interior):
    """Le distributeur ; `interior` = image de la pièce collée dans le globe."""
    c = bg_shop().copy()
    put(c, E.duck(90), 170, 1600)
    body, cap = machine()
    gx, gy, gr = 540, 700, 300
    E.shadow(c, 540, 1585, 600, 70)
    c.alpha_composite(body)
    # crank
    ang = 0
    if t > 14.4:
        ang = -360 * ease_in_out(seg(t, 14.4, 15.3))
    put(c, crank(), 540, 1210, rot=ang)
    # globe : intérieur
    m = Image.new("L", (E.W, E.H), 0)
    ImageDraw.Draw(m).ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=255)
    sc = interior.resize((2 * gr, int(2 * gr * E.H / E.W)))
    tmp = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
    tmp.paste(sc, (gx - gr, gy - int(sc.height * 0.62)))
    c.paste(tmp, (0, 0), m)
    c.alpha_composite(globe_glass(), (gx - gr - 20, gy - gr - 20))
    put(c, cap, gx, gy - gr + 10)
    # pièce
    if 13.7 < t < 14.25:
        k = ease_in_out(seg(t, 13.7, 14.2))
        put(c, coin(), 540 + 80, E.lerp(-80, 1180, k), sx=max(0.2, 1 - k * 0.5))
    # boule qui sort dans la trappe
    if t > 15.4:
        k = seg(t, 15.4, 15.7)
        put(c, mini(4, h=110), 540, E.lerp(1380, 1480, k))
    return c


def frame(t):
    if t < 13.0:
        return draw_room(t)
    if t < 15.8:
        interior = draw_room(12.9)
        shop = draw_shop(t, interior.convert("RGB"))
        k = seg(t, 13.0, 13.6)
        if k < 1:
            z = 1 + 9 * (1 - ease_out(k))
            img = E.camera(shop, z, 540, 700)
            return E.radial_blur(img, 0.12 * (1 - k), 5)
        if t > 15.6:
            return E.camera(shop, 1 + 4 * ease_in_out(seg(t, 15.6, 15.8)), 540, 1440)
        return shop
    # gros plan dans la trappe
    c = chute_bg().copy()
    k = seg(t, 15.8, 16.25)
    x = E.lerp(260, 540, k)
    y = E.lerp(500, 1560, ease_out(k) if k < 1 else 1)
    rot = (1 - k) * 380
    sx = sy = 1
    if t > 16.25:
        b = seg(t, 16.25, 16.55)
        sx = 1 + 0.18 * math.sin(math.pi * b)
        sy = 1 - 0.18 * math.sin(math.pi * b)
    look, o = E.regard_eyes(t, 16.6, (1, -0.3))
    if t < 16.6:
        look, o = (1, -0.3), 1.0
    tuft = "curl"
    if t > 17.5:
        kk = seg(t, 17.5, 18.0)
        o = 1 - 0.8 * kk
        sy *= 1 + 0.1 * kk
        sx *= 1 + 0.05 * kk
    E.shadow(c, x, 1560, 560, alpha=0.35)
    put(c, E.nubo(600, eyes=o, look=look, tuft=tuft), x, y, sx=sx, sy=sy, rot=rot, jid="nc")
    put(c, E.duck(70), 960, 1600)
    return c


# ---------------------------------------------------------------- son
def sound(m):
    # musique pizzicato qui accélère pendant la multiplication
    mel = ["C5", "E5", "G5", "E5", "F5", "A5", "G5", "E5", "D5", "F5", "E5", "C5"]
    t = 1.6
    i = 0
    while t < 9.2:
        bpm = 120 + 160 * seg(t, 4.5, 9.0)
        m.add(t, A.pizz(A.NOTE(mel[i % len(mel)])), 0.35, -0.2)
        if i % 2 == 0:
            m.add(t, A.pizz(A.NOTE(mel[i % len(mel)]) / 2), 0.3, 0.2)
        t += 60 / bpm / 2
        i += 1
    for st in SNEEZES:
        if st < 4.5:
            m.add(st - 1.1, A.sneeze_ah(1.0, 0.45), 0.5)
            m.add(st - 0.55, A.sneeze_ah(1.15, 0.5), 0.6)
            m.add(st, A.sneeze_choo(), 0.9)
        else:
            m.add(st, A.sneeze_choo(1.2), 0.5, (st * 7 % 2) - 0.5)
    for i, (st, xe, ye, v) in enumerate(EXPL):
        m.add(st + 0.05, A.plop(1.2 + 0.1 * (i % 3)), 0.5, (xe - 540) / 600)
        m.add(st + 0.6, A.plop(0.9), 0.3, (xe - 540) / 600)
    # crépitement des plops de la marée
    import numpy as np
    rng = np.random.default_rng(3)
    for k in range(160):
        tt = rng.uniform(PILE_T0, PILE_T1 - 0.3)
        m.add(tt, A.plop(rng.uniform(0.8, 1.5)), 0.12, rng.uniform(-0.8, 0.8))
    m.add(1.7, A.nub(1.4), 0.3, -0.5)  # le mini répond
    m.add(11.0, A.squeak(0.8, 0.15), 0.25)
    # reveal
    m.add(12.95, A.whoosh(0.8, 200, 3000), 0.7)
    m.add(13.6, A.hum(2.2, 50) * 0.5, 0.4)
    m.add(14.18, A.coin(), 0.6)
    for k in range(3):
        m.add(14.45 + k * 0.28, A.clack(), 0.7)
    m.add(15.65, A.plop(0.7), 0.6)
    m.add(15.8, A.whoosh(0.4, 400, 4000, 3), 0.5)
    m.add(16.25, A.thump(80, 0.4), 0.8)
    m.add(16.27, A.nub(0.9), 0.5)
    m.add(17.35, A.nub(1.0), 0.6)
    m.add(17.35, A.regard(), 0.6)
    m.add(17.55, A.sneeze_ah(1.0, 0.45), 0.5)
