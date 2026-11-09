"""ÉPISODE 07 — NE PAS APPUYER."""
import math
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_in, ease_out_back

SLUG = "ep07_ne_pas_appuyer"
DUR = 20.0
COVER_T = 10.6
FLOOR = 1460
CEIL = 170
NX, NH = 470, 440
BX, BY = 720, 1170
DUCK0 = 880
CLICKS = [1.0, 3.3, 6.2, 8.8, 12.0, 12.2, 12.4, 12.6, 17.6]


@lru_cache(maxsize=1)
def bg():
    b = E.room_bg((200, 186, 236), E.CREAM, floor_y=FLOOR - 50, wall_pattern="stripes", seed=31)
    ceil = E.felt_panel(E.W, CEIL, (170, 155, 205), seed=32, stitch=True)
    b.alpha_composite(ceil, (0, 0))
    lamp = E.S(180, 70, [("ellipse", 0, 0, 180, 140)], (255, 240, 200), seed=33)
    put(b, lamp, 540, CEIL + 10)
    plate = E.S(260, 260, [("rect", 0, 0, 260, 260, 40)], (175, 175, 185), seed=34)
    put(b, plate, BX, BY)
    sign = E.S(220, 170, [("rect", 0, 0, 220, 170, 16)], E.WHITE, seed=35)
    d = ImageDraw.Draw(sign.img)
    cx, cy = 116, 91
    d.rounded_rectangle([cx - 30, cy - 10, cx + 30, cy + 50], radius=14, fill=(240, 190, 150, 255))
    for k in range(4):
        x = cx - 28 + k * 16
        d.rounded_rectangle([x, cy - 55 + abs(k - 1.5) * 6, x + 13, cy], radius=6, fill=(240, 190, 150, 255))
    d.rounded_rectangle([cx + 22, cy - 5, cx + 50, cy + 12], radius=7, fill=(240, 190, 150, 255))
    d.ellipse([cx - 72, cy - 72, cx + 72, cy + 72], outline=(220, 40, 40, 255), width=13)
    d.line([(cx - 50, cy - 50), (cx + 50, cy + 50)], fill=(220, 40, 40, 255), width=13)
    put(b, sign, BX, BY - 260)
    return b


@lru_cache(maxsize=2)
def button(pressed):
    sp = E.S(180, 180, [("circle", 90, 90, 90)], (225, 50, 50), seed=36)
    d = ImageDraw.Draw(sp.img)
    d.ellipse([45, 35, 90, 70], fill=(255, 160, 160, 200))
    return sp


@lru_cache(maxsize=1)
def piano():
    img = Image.new("RGBA", (460, 420), (0, 0, 0, 0))
    body = E.shape(440, 300, [("rect", 0, 0, 440, 300, 20)], (90, 55, 40), seed=40)
    E.paste(img, body, 10, 0)
    keys = E.shape(420, 70, [("rect", 0, 0, 420, 70, 6)], E.WHITE, seed=41)
    E.paste(img, keys, 20, 200)
    d = ImageDraw.Draw(img)
    for k in range(14):
        x = 26 + k * 30
        d.line([(x, 206), (x, 276)], fill=(120, 120, 120, 255), width=2)
        if k % 7 not in (2, 6):
            d.rectangle([x + 18, 206, x + 38, 246], fill=(30, 30, 30, 255))
    for x in (40, 400):
        leg = E.shape(36, 130, [("rect", 0, 0, 36, 130, 8)], (80, 48, 35), seed=x)
        E.paste(img, leg, x, 290)
    return E.Sprite(img, (230, 416))


CONF_COLS = [(255, 120, 160), (120, 210, 255), (255, 220, 80), (150, 240, 140), (200, 150, 255)]


def confetti(t, t0, flip=False):
    r = random.Random(11)
    out = []
    for i in range(70):
        dt = t - t0
        if dt < 0:
            continue
        x = r.uniform(80, 1000) + math.sin(dt * 3 + i) * 40
        y0 = r.uniform(-300, 200)
        vy = r.uniform(250, 520)
        y = y0 + vy * dt
        if flip:
            y = min(y, FLOOR - 10)
        out.append((x, min(y, FLOOR + 30 + (i % 5) * 20), 10, CONF_COLS[i % 5], 1.0))
    return out


def gravity(t):
    """0 = sol, 1 = plafond."""
    if t < 6.2:
        return 0.0
    if t < 8.8:
        return ease_in(seg(t, 6.25, 6.85))
    return 1 - ease_in(seg(t, 8.9, 9.4))


def realistic(img):
    im = img.convert("RGB").filter(ImageFilter.UnsharpMask(3, 160, 2))
    a = np.asarray(im, np.float32)
    g = a.mean(axis=2, keepdims=True)
    a = a * 0.45 + g * 0.55
    a = (a - 128) * 1.35 + 118
    a *= np.array([0.9, 0.97, 1.08], np.float32)
    a += np.random.default_rng(E.FRAME).normal(0, 16, a.shape[:2] + (1,))
    yy, xx = np.mgrid[0:E.H, 0:E.W].astype(np.float32)
    v = 1 - 0.6 * (((xx - E.W / 2) / E.W) ** 2 + ((yy - E.H / 2) / E.H) ** 2) * 2.5
    a *= np.clip(v, 0.3, 1)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


@lru_cache(maxsize=1)
def stretch_arm_base():
    return None


def stretch_arm(c, x0, y0, x1, y1):
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 10:
        return
    sp = E.S(L, 60, [("rect", 0, 0, L, 60, 30)], E.darker(E.ORANGE, 0.95), seed=50, anchor=(0, 30))
    ang = -math.degrees(math.atan2(y1 - y0, x1 - x0))
    put(c, sp, x0, y0, rot=ang)


def scene(t):
    c = bg().copy()
    g = gravity(t)
    pressed = any(p <= t < p + 0.15 for p in CLICKS)
    put(c, button(pressed), BX, BY + (8 if pressed else 0), sy=0.9 if pressed else 1.0)
    # canard témoin (reste au sol, même quand la gravité s'inverse)
    dx = DUCK0
    dy = FLOOR + 30
    if t > 16.4:
        dx = E.lerp(DUCK0, BX + 30, ease_in_out(seg(t, 16.4, 17.2)))
    if t > 17.25:
        k = seg(t, 17.25, 17.6)
        dx = E.lerp(BX + 30, BX + 10, k)
        dy = E.lerp(FLOOR + 30, BY + 120, ease_out(k))
    put(c, E.duck(110), dx, dy, jid="duck", jamp=0.6, jrot=0.2)
    # piano
    if t > 3.3:
        k = seg(t, 3.3, 3.75)
        py = E.lerp(-500, FLOOR + 40, ease_in(k))
        if g > 0:
            py = E.lerp(FLOOR + 40, CEIL + 380, g)
        rot = 180 * g
        if k >= 1 and g == 0:
            E.shadow(c, 220, FLOOR + 40, 420, 50)
        put(c, piano(), 220, py, rot=rot if g < 1 else 180, jid="piano", jamp=1.0)
        if 3.75 < t < 4.6:
            kk = seg(t, 3.75, 4.6)
            E.particles(c, [(220 + math.cos(i) * 300 * kk, FLOOR + 20 - abs(math.sin(i * 1.3)) * 150 * kk,
                             30 + 30 * kk, (230, 220, 210), 0.7 * (1 - kk)) for i in range(12)])
    # NUBO
    kw = dict(h=NH, look=(1, -0.3), tuft="curl", arms=(18, 18))
    x, y, rot, sx, sy = NX, FLOOR + 30, 0, 1, 1
    if 1.0 <= t < 3.0:
        k = seg(t, 1.1, 2.1)
        sx = math.cos(k * math.pi * 4) if k < 1 else 1
        kw["arms"] = (140, 140)
        kw["look"] = (0, -1)
    if 3.75 <= t < 6.2:
        kw["tuft"] = "up"
        kw["scared"] = True
        kw["look"] = (-1, 0.2)
    if g > 0:
        y = E.lerp(FLOOR + 30, CEIL + 10, g)
        rot = 180 * min(1, g * 1.2)
        kw["tuft"] = "up"
        kw["look"] = (0.6, 0.6) if g > 0.9 else (0, 0)
        kw["scared"] = True
    real = 9.4 <= t < 12.8
    if real:
        kw.update(furry=True, scared=True, tuft="up", arms=(120, 120), look=(0, 1))
        if t > 11.4:
            kw["look"] = (1, -0.3)
    if 12.8 <= t < 13.0:
        kw["tuft"] = "down"
    if t >= 13.0:
        k = seg(t, 13.0, 16.0)
        x = E.lerp(NX, -260, ease_in_out(k))
        y -= abs(math.sin(k * 20)) * 12
        kw["look"] = (1, -0.4)
        kw["tuft"] = "curl"
    if pressed or (0.8 <= t < 1.0):
        kw["arms"] = (18, 100)
    if g < 0.05:
        E.shadow(c, x, FLOOR + 30, NH * 0.9)
    put(c, E.nubo(**kw), x, y, rot=rot, sx=sx, sy=sy, jid="n")
    # bras élastique quand NUBO est au plafond
    if 8.4 < t < 9.0:
        k = ease_out(seg(t, 8.4, 8.8))
        sx0, sy0 = NX + 120, CEIL + 0.5 * NH
        stretch_arm(c, sx0, sy0, E.lerp(sx0, BX, k), E.lerp(sy0, BY, k))
    # confettis
    if t > 1.0:
        conf = confetti(t, 1.0)
        if g > 0:
            conf = [(xx, E.lerp(yy, CEIL + 20 + (i % 5) * 15, g), r, col, a) for i, (xx, yy, r, col, a) in enumerate(conf)]
        E.particles(c, conf)
    return c, real


def frame(t):
    if t >= 17.6 and t < 19.6:
        return Image.new("RGBA", (E.W, E.H), (0, 0, 0, 255))
    if t >= 19.6:
        c, _ = scene(0.0)
        img = E.camera(c, 2.0, BX - 60, BY + 40)
        return E.fade_black(img, 1 - seg(t, 19.6, 20.0))
    c, real = scene(t)
    if t < 1.0:
        z = 2.0 - 0.15 * t
        return E.camera(c, z, BX - 60, BY + 40)
    if 1.0 <= t < 1.4:
        k = ease_out(seg(t, 1.0, 1.4))
        return E.camera(c, E.lerp(1.85, 1.15, k), E.lerp(BX - 60, 560, k), E.lerp(BY + 40, 1100, k))
    shake = 0
    if 3.75 < t < 4.2:
        shake = 22 * (1 - seg(t, 3.75, 4.2))
    if 9.35 < t < 9.6:
        shake = 14
    r = E.rng_for("shake", E.FRAME)
    img = E.camera(c, 1.15, 560 + r.uniform(-shake, shake), 1000 + r.uniform(-shake, shake))
    if real:
        img = realistic(img)
    return img


def sound(m):
    for p in CLICKS[:8]:
        m.add(p, A.click(0.03, 900, int(p * 7)), 1.0)
        m.add(p, A.thump(160, 0.12) * 0.5, 0.5)
    m.add(17.6, A.click(0.03, 900, 5) * 1.5, 1.0)
    m.add(17.6, A.thump(120, 0.3), 0.8)
    # confettis + petite fanfare
    m.add(1.0, A.pop(300, 1200, 0.15), 0.8)
    m.add(1.05, A.crunch(1.2, 2) * 0.3, 0.4)
    m.seq(1.05, 180, [(0, "C6", 0.5), (0.5, "E6", 0.5), (1, "G6", 1.5)], A.kazoo, 0.5)
    m.add(1.2, A.nub(1.3), 0.5)
    # piano
    m.add(2.9, A.whoosh(0.9, 200, 2500, 2), 0.6)
    m.add(3.75, A.piano_crash(2.2), 1.0)
    m.add(3.9, A.nub(1.5), 0.5)
    # gravité inversée
    m.add(6.2, A.whoosh(0.9, 150, 2000, 5) * 1.2, 0.7)
    m.add(6.25, np.sin(A.phase(A.glide(150, 900, 0.7), int(0.7 * A.SR))) * 0.5, 0.6)
    m.add(6.85, A.thump(70, 0.3), 0.7)
    m.add(6.9, A.piano_crash(1.4) * 0.5, 0.6)
    m.add(8.4, np.sin(A.phase(A.glide(300, 1200, 0.4), int(0.4 * A.SR))) * 0.4 * np.linspace(1, 0.3, int(0.4 * A.SR)), 0.6)
    # retour + monde « réel »
    m.add(9.0, np.sin(A.phase(A.glide(900, 120, 0.5), int(0.5 * A.SR))) * 0.5, 0.6)
    m.add(9.38, A.crash(0.8), 0.8)
    m.add(9.4, A.hum(3.4, 120) * 1.8, 0.6)
    m.add(9.4, A.drone(3.4, 41), 0.9)
    m.add(9.6, A.vowel(130, 100, 0.8, ((300, 800), (900, 1400))) * np.linspace(1, 0, int(0.8 * A.SR)), 0.4)
    m.add(12.8, A.pop(400, 900, 0.1), 0.6)
    m.add(12.85, A.nub(1.0), 0.5)
    # recul prudent
    for k in range(9):
        m.add(13.0 + k * 0.33, A.tick(k % 2 == 0) * 0.35, 0.3, -0.3 - k * 0.07)
    m.add(16.4, A.scrape(0.8), 0.6, 0.4)
    m.add(17.25, A.squeak(2.0, 0.08), 0.3, 0.3)
    m.add(18.4, A.nub(0.65), 0.6)
