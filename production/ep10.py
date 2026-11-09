"""ÉPISODE 10 — LE SELFIE."""
import math
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_in, ease_out_back

SLUG = "ep10_le_selfie"
DUR = 18.0
COVER_T = 10.6
GROUND = 1500
FLASHES = [0.0, 3.0, 5.0, 10.0, 17.95]
SELFIES = [(0.0, 1.0, 1), (3.0, 5.0, 2), (5.0, 7.0, 3), (10.0, 12.0, 4)]
BROWN = (135, 90, 60)


@lru_cache(maxsize=2)
def forest(blur=False):
    b = Image.new("RGBA", (E.W, E.H), (200, 235, 225, 255))
    b.alpha_composite(E.felt_panel(E.W, E.H, (195, 232, 222), seed=11, stitch=False))
    r = random.Random(3)
    for depth, (col, sc, y0) in enumerate((((160, 210, 175), 0.6, 1250), ((120, 190, 140), 0.85, 1380),
                                            ((95, 170, 120), 1.15, 1560))):
        for k in range(6 - depth):
            x = r.uniform(-60, E.W + 60)
            w, h = 260 * sc, 300 * sc
            trunk = E.S(50 * sc, 380 * sc, [("rect", 0, 0, 50 * sc, 380 * sc, 10)], E.darker(E.WOOD, 0.8 - 0.05 * depth),
                        seed=depth * 10 + k, anchor="bottom")
            put(b, trunk, x, y0)
            can = E.S(w, h, [("ellipse", 0, 0, w, h)], col, seed=depth * 10 + k + 50)
            put(b, can, x, y0 - 380 * sc)
    ground = E.felt_panel(E.W, E.H - GROUND, (150, 205, 130), seed=12, stitch=False)
    b.alpha_composite(ground, (0, GROUND))
    for k in range(7):
        x, y = r.uniform(40, E.W - 40), r.uniform(GROUND + 60, E.H - 40)
        fl = E.S(40, 40, [("circle", 20, 20, 20)], ((255, 200, 220), (255, 240, 150), (220, 200, 255))[k % 3], seed=k)
        put(b, fl, x, y)
    mush = E.S(120, 110, [("ellipse", 0, 0, 120, 70), ("rect", 40, 40, 80, 110, 10)], (230, 90, 80), seed=13,
               anchor="bottom")
    put(b, mush, 120, GROUND + 120)
    put(b, E.duck(70), 940, GROUND + 230)
    if blur:
        b = b.filter(ImageFilter.GaussianBlur(7))
    return b


@lru_cache(maxsize=32)
def moose(o=1.0, look=(0, 0), smile=False, mouth=0.0):
    w, h = 760, 1000
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for lx in (250, 450):
        leg = E.shape(60, 330, [("rect", 0, 0, 60, 330, 20)], E.darker(BROWN, 0.85), seed=lx)
        E.paste(img, leg, lx, 650)
    body = E.shape(520, 340, [("ellipse", 0, 0, 520, 340)], E.darker(BROWN, 0.92), seed=21)
    E.paste(img, body, 120, 420)
    # bois
    for sgn in (-1, 1):
        cx = w / 2 + sgn * 210
        ant = E.S(260, 170, [("ellipse", 0, 40, 260, 170)] + [("circle", 30 + i * 50, 40, 26) for i in range(5)],
                  (225, 195, 145), seed=22 + sgn)
        put(img, ant, cx, 150, rot=-15 * sgn, flip=sgn < 0)
        stem = E.S(40, 120, [("rect", 0, 0, 40, 120, 14)], (215, 185, 135), seed=24 + sgn)
        put(img, stem, w / 2 + sgn * 90, 230, rot=45 * sgn)
        ear = E.S(110, 60, [("ellipse", 0, 0, 110, 60)], BROWN, seed=26 + sgn)
        put(img, ear, w / 2 + sgn * 160, 300, rot=-20 * sgn)
    head = E.shape(270, 420, [("ellipse", 0, 0, 270, 420)], BROWN, seed=27)
    E.paste(img, head, int(w / 2 - 135 - 6), 210)
    snout = E.shape(320, 220, [("ellipse", 0, 0, 320, 220)], (175, 125, 85), seed=28)
    E.paste(img, snout, int(w / 2 - 160 - 6), 450)
    d = ImageDraw.Draw(img)
    for sgn in (-1, 1):
        d.ellipse([w / 2 + sgn * 70 - 22, 530, w / 2 + sgn * 70 + 22, 565], fill=(60, 35, 30, 255))
    if mouth > 0.05:
        d.ellipse([w / 2 - 80, 600 - 10 * mouth, w / 2 + 80, 610 + 60 * mouth], fill=(70, 30, 35, 255))
    elif smile:
        d.arc([w / 2 - 110, 540, w / 2 + 110, 640], 20, 160, fill=(60, 35, 30, 255), width=10)
    else:
        d.line([(w / 2 - 60, 612), (w / 2 + 60, 612)], fill=(60, 35, 30, 255), width=8)
    for sgn in (-1, 1):
        E._eye(img, w / 2 + sgn * 80 + look[0] * 10, 345 + look[1] * 8, 24, o, BROWN)
    bell = E.shape(70, 110, [("ellipse", 0, 0, 70, 110)], E.darker(BROWN, 0.9), seed=29)
    E.paste(img, bell, int(w / 2 - 41), 640)
    return E.Sprite(img, (w / 2, 980))


@lru_cache(maxsize=1)
def phone():
    sp = E.S(80, 140, [("rect", 0, 0, 80, 140, 16)], (45, 45, 55), seed=30)
    d = ImageDraw.Draw(sp.img)
    d.rounded_rectangle([14, 16, 78, 132], radius=8, fill=(150, 200, 240, 255))
    return sp


@lru_cache(maxsize=1)
def phone_ui():
    im = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
    m = Image.new("L", (E.W, E.H), 255)
    ImageDraw.Draw(m).rounded_rectangle([34, 34, E.W - 34, E.H - 34], radius=70, fill=0)
    black = Image.new("RGBA", (E.W, E.H), (15, 15, 18, 255))
    im.paste(black, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.ellipse([E.W / 2 - 75, E.H - 260, E.W / 2 + 75, E.H - 110], outline=(255, 255, 255, 240), width=10)
    d.ellipse([E.W / 2 - 58, E.H - 243, E.W / 2 + 58, E.H - 127], fill=(255, 255, 255, 230))
    d.rounded_rectangle([E.W / 2 - 110, 60, E.W / 2 + 110, 110], radius=25, fill=(15, 15, 18, 255))
    return im


def selfie(t, n):
    c = forest(True).copy()
    if n == 1:
        put(c, moose(), 935, 1240, scale=0.2, jid="m")
    elif n == 2:
        put(c, moose(), 790, 1500, scale=0.55, jid="m")
    elif n == 3:
        put(c, moose(), 600, 2350, scale=2.2, jid="m")
    if n < 4:
        tuft = "up" if n == 3 else "curl"
        sp = E.nubo(800, eyes=(1.0, 0.0) if n != 2 else (0.0, 1.0), look=(0, 0), tuft=tuft, phase=t * 6,
                    arms=(18, 120))
        put(c, sp, 500, 1860, jid="ns", jamp=3)
    else:
        put(c, moose(1.0, (0, 0), True), 580, 2650, scale=2.4, jid="m4")
        sp = E.nubo(560, scared=True, tuft="up", look=(0.3, 0))
        put(c, sp, 250, 1780, rot=-14, sx=0.9, jid="n4", jamp=3)
    c.alpha_composite(phone_ui())
    return c


def wide(t):
    c = forest(False).copy()
    nx, ny, nh = 400, GROUND + 260, 420
    kw = dict(h=nh, look=(0.4, -0.5), arms=(18, 140), tuft="curl")
    sx = 1
    if 1.0 <= t < 3.0:
        kw["eyes"] = (1.0, 0.0) if t < 2.0 else (0.0, 1.0)
        kw["look"] = (0, -0.3)
    if 7.0 <= t < 10.0:
        kw["arms"] = (18, 18)
        kw["tuft"] = "up" if t < 8.6 else "question"
        if t < 7.4:
            sx = math.cos(seg(t, 7.0, 7.4) * math.pi * 2)
        kw["look"] = keys3(t)
        if 8.6 <= t < 9.4:
            kw["arms"] = (95, 95)
            kw["look"] = (0, 0)
        if t >= 9.4:
            kw["arms"] = (18, 140)
    if 12.0 <= t:
        mx = 760
        mo, mlook, smile, mouth = 1.0, (-0.6, 0.6), True, 0.0
        if 15.0 <= t < 17.0:
            smile = False
            mouth = abs(math.sin((t - 15.3) * 9)) if t > 15.3 else seg(t, 15.0, 15.3)
            mlook = (0, -0.5)
        if t >= 16.6:
            mlook, mo = E.regard_eyes(t, 16.6, (0, -0.5))
            mouth = 0.0
        E.shadow(c, mx, GROUND + 270, 420, 60)
        put(c, moose(round(mo * 5) / 5, (round(mlook[0], 1), round(mlook[1], 1)), smile, round(mouth * 4) / 4),
            mx, GROUND + 270, scale=0.95, jid="mw")
        kw["arms"] = (18, 18)
        kw["look"] = (1, -0.6)
        if t >= 15.3:
            kw["tuft"] = "up"
            kw["look"] = (1, -0.9)
        if t >= 16.6:
            kw["look"], kw["eyes"] = E.regard_eyes(t, 16.6, (1, -0.9))
        # téléphone
        if t < 15.3:
            k = seg(t, 15.0, 15.3)
            px = E.lerp(600, mx, k)
            py = E.lerp(GROUND - 140, GROUND - 330, k)
            put(c, phone(), px, py, rot=-10 + 10 * k, jid="ph")
    E.shadow(c, nx, ny, nh * 0.9)
    put(c, E.nubo(**kw), nx, ny, sx=sx, jid="n")
    if t < 12.0 and kw["arms"][1] > 100:
        put(c, phone(), nx + 230, ny - 400, rot=15, jid="ph2")
    # miettes de téléphone
    if 15.3 < t < 16.8:
        r = random.Random(int(t * 12))
        E.particles(c, [(760 + r.uniform(-60, 60), GROUND - 340 + r.uniform(0, 200), 6, (60, 60, 70), 1)
                        for _ in range(6)])
    return c


def keys3(t):
    if t < 7.4:
        return (0, 0)
    if t < 7.9:
        return (-1, -0.2)
    if t < 8.4:
        return (1, -0.2)
    return (0, 0)


def frame(t):
    for (s0, s1, n) in SELFIES:
        if s0 <= t < s1:
            img = selfie(t, n)
            break
    else:
        img = E.camera(wide(t), 1.25, 560, 1250)
    for f in FLASHES:
        if f <= t < f + 0.35:
            img = E.flash(img, 1 - seg(t, f, f + 0.35))
    if t >= 17.95:
        img = E.flash(img, 1.0)
    return img


def sound(m):
    m.add(0, A.birds(DUR, 3), 0.6)
    m.add(0, A.wind(DUR, 0.15, 2), 0.3)
    for f in FLASHES:
        m.add(f, A.shutter(), 0.9)
        m.add(f, np.sin(A.phase(A.glide(3000, 900, 0.25), int(0.25 * A.SR))) * 0.15, 0.3)
    m.add(0.1, A.horror_screech(0.25) * 0.4, 0.3)
    m.add(3.1, A.horror_screech(0.35) * 0.7, 0.45)
    m.add(5.1, A.horror_screech(0.6), 0.6)
    m.add(5.2, A.squeak(1.6, 0.12), 0.4)
    m.add(10.05, A.horror_screech(0.35), 0.6)
    m.add(10.1, A.squeak(1.8, 0.2), 0.6)
    # petites notes de pose
    m.seq(1.2, 120, [(0, "E5", 0.5), (0.5, "G5", 0.5), (1, "C6", 1)], A.music_box, 0.5)
    m.add(7.0, A.whoosh(0.4, 400, 3000, 2), 0.5)
    m.add(7.4, A.whoosh(0.3, 400, 3000, 3), 0.3)
    m.add(7.9, A.whoosh(0.3, 400, 3000, 4), 0.3)
    m.add(8.7, A.squeak(1.1, 0.22), 0.4)
    # ukulélé joyeux (10.4 → 15)
    prog = [["C4", "E4", "G4", "C5"], ["G3", "D4", "G4", "B4"], ["A3", "E4", "A4", "C5"], ["F3", "C4", "F4", "A4"]]
    beat = 60 / 140
    i, tt = 0, 10.4
    while tt < 15.0:
        ch = prog[(i // 4) % 4]
        for k, nn in enumerate(ch):
            m.add(tt + k * 0.015, A.ukulele(A.NOTE(nn), 0.5), 0.25)
        tt += beat
        i += 1
    m.seq(10.4, 140, [(0, "E5", 1), (1, "G5", 1), (2, "C6", 2), (4, "B5", 1), (5, "G5", 1), (6, "D5", 2),
                      (8, "C5", 1), (9, "E5", 1), (10, "A5", 2)], A.whistle, 0.4)
    m.add(12.2, A.vowel(130, 160, 0.6, ((300, 800), (800, 1300))) * np.linspace(0.6, 0, int(0.6 * A.SR)), 0.5, 0.3)
    m.add(15.3, A.crunch(1.4, 4), 0.9, 0.3)
    m.add(15.35, A.squeak(1.5, 0.15), 0.4, -0.3)
    for k in range(4):
        m.add(15.8 + k * 0.33, A.crunch(0.2, 10 + k), 0.6, 0.3)
    m.add(17.35, A.nub(0.9), 0.5, -0.3)
    m.add(17.35, A.vowel(110, 90, 0.35, ((250, 700), (700, 1000))) * 0.6, 0.5, 0.3)
    m.add(17.35, A.regard(), 0.6)
