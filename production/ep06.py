"""ÉPISODE 06 — MAUVAIS ÉTAGE."""
import math
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_out_back, keys

SLUG = "ep06_mauvais_etage"
DUR = 24.0
COVER_T = 11.6
DX0, DX1, DY0, DY1 = 250, 1010, 380, 1640
WW, WH = DX1 - DX0, DY1 - DY0
NX, NY, NH = 220, 1870, 440

# (ouverture début, ouverture fin, fermeture début, fermeture fin, monde)
STOPS = [(-1.0, 0.3, 1.0, 1.6, "bear"), (2.8, 3.2, 4.3, 4.9, "space"), (5.6, 6.0, 7.0, 7.5, "grannies"),
         (8.2, 8.6, 9.5, 10.1, "whale"), (11.0, 11.4, 13.2, 13.9, "office"), (15.2, 15.6, 21.3, 21.9, "landing"),
         (23.6, 25.0, 99, 99, "bear")]
PRESSES = [0.9, 4.2, 6.8, 7.0, 7.2, 9.4] + [12.0 + i * 0.15 for i in range(10)]


def door_open(t):
    for o0, o1, c0, c1, w in STOPS:
        if o0 <= t < c1:
            if t < o1:
                if o0 < 0:
                    return 0.55 + 0.45 * ease_out(seg(t, 0, o1)), w
                if w == "bear" and o0 > 23:
                    return 0.55 * ease_out(seg(t, o0, 24.0)), w
                return ease_out(seg(t, o0, o1)), w
            if t < c0:
                return 1.0, w
            return 1 - ease_in_out(seg(t, c0, c1)), w
    return 0.0, None


# ------------------------------------------------------------------ mondes
@lru_cache(maxsize=1)
def bear_bg():
    im = Image.new("RGBA", (WW, WH), (140, 210, 205, 255))
    d = ImageDraw.Draw(im)
    for y in range(0, WH, 90):
        for x in range(0, WW, 90):
            d.rectangle([x, y, x + 86, y + 86], fill=(150, 220, 215, 255))
    return im


@lru_cache(maxsize=4)
def bear(look=0):
    w, h = 520, 520
    img = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    body = E.shape(500, 300, [("ellipse", 0, 0, 500, 400)], (150, 100, 65), seed=10)
    E.paste(img, body, 20, 300)
    for x in (130, 390):
        ear = E.shape(110, 110, [("circle", 55, 55, 55)], (135, 90, 58), seed=11 + x)
        E.paste(img, ear, x - 55 + 20, 40)
    head = E.shape(360, 320, [("ellipse", 0, 0, 360, 320)], (150, 100, 65), seed=12)
    E.paste(img, head, 100, 70)
    snout = E.shape(150, 110, [("ellipse", 0, 0, 150, 110)], (215, 175, 130), seed=13)
    E.paste(img, snout, 205, 230)
    d = ImageDraw.Draw(img)
    d.ellipse([255, 245, 305, 280], fill=(40, 25, 25, 255))
    for ex in (225, 335):
        x = ex + look * 8
        d.ellipse([x - 16, 175, x + 16, 207], fill=(20, 18, 20, 255))
        d.ellipse([x - 9, 181, x - 2, 189], fill=(255, 255, 255, 255))
    for sx in (150, 410):
        for k in range(4):
            d.line([(sx + k * 10 - 15, 370), (sx + k * 10 + 15, 470)], fill=((220, 60, 60) if k % 2 else (250, 250, 250)) + (255,), width=10)
    return E.Sprite(img, (img.width / 2, img.height))


@lru_cache(maxsize=1)
def tub():
    return E.S(700, 220, [("rect", 0, 0, 700, 220, 60)], E.WHITE, seed=14, anchor="top")


def world_bear(t):
    im = bear_bg().copy()
    put(im, bear(1 if (t % 4) > 2 else 0), WW / 2, WH - 230 + math.sin(t * 2) * 6, jid="bear", jamp=1.5)
    water = Image.new("RGBA", (WW, 260), (110, 190, 240, 220))
    im.alpha_composite(water, (0, WH - 300))
    put(im, tub(), WW / 2, WH - 320)
    E.particles(im, [((i * 97) % WW, WH - 300 - ((t * 140 + i * 53) % 260), 8 + i % 3 * 4, (240, 250, 255), 0.8)
                     for i in range(16)])
    E.particles(im, [((i * 131) % WW + 20 * math.sin(t + i), 500 - ((t * 60 + i * 80) % 400), 40, (255, 255, 255),
                      0.12) for i in range(8)])
    return im


@lru_cache(maxsize=1)
def space_bg():
    im = Image.new("RGBA", (WW, WH), (20, 22, 55, 255))
    r = random.Random(4)
    d = ImageDraw.Draw(im)
    for _ in range(140):
        x, y, s = r.uniform(0, WW), r.uniform(0, WH), r.uniform(1, 4)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 230, 255))
    earth = E.S(520, 520, [("circle", 260, 260, 260)], (90, 150, 230), seed=20)
    for (x, y, rx, ry) in ((150, 160, 120, 90), (330, 320, 140, 100), (200, 380, 70, 50)):
        cont = E.shape(2 * rx, 2 * ry, [("ellipse", 0, 0, 2 * rx, 2 * ry)], (110, 190, 110), seed=x)
        E.paste(earth.img, cont, int(x - rx), int(y - ry))
    put(im, earth, WW - 120, WH - 160)
    return im


@lru_cache(maxsize=8)
def astronaut(wave):
    img = Image.new("RGBA", (420, 520), (0, 0, 0, 0))
    body = E.shape(240, 280, [("rect", 0, 0, 240, 280, 80)], (240, 240, 245), seed=21)
    E.paste(img, body, 90, 200)
    arm = E.S(70, 170, [("rect", 0, 0, 70, 170, 34)], (235, 235, 240), seed=22, anchor=(35, 20))
    put(img, arm, 110, 250, rot=-30)
    put(img, arm, 300, 240, rot=150 + wave * 40)
    helmet = E.shape(240, 240, [("circle", 120, 120, 120)], (245, 245, 250), seed=23)
    E.paste(img, helmet, 90, 0)
    d = ImageDraw.Draw(img)
    d.ellipse([130, 50, 300, 190], fill=(40, 50, 90, 255))
    d.arc([150, 65, 280, 175], 200, 260, fill=(200, 220, 255, 255), width=10)
    for leg in (130, 245):
        lg = E.shape(70, 130, [("rect", 0, 0, 70, 130, 30)], (235, 235, 240), seed=leg)
        E.paste(img, lg, leg - 4, 450 - 70)
    return E.Sprite(img)


def world_space(t):
    im = space_bg().copy()
    wave = (math.sin(t * 8) + 1) / 2
    put(im, astronaut(round(wave * 4) / 4), WW / 2 - 60, 520 + math.sin(t * 1.5) * 40, rot=math.sin(t) * 12,
        jid="astro", jamp=1.0)
    return im


@lru_cache(maxsize=1)
def granny_bg():
    im = Image.new("RGBA", (WW, WH), (245, 200, 210, 255))
    d = ImageDraw.Draw(im)
    for y in range(40, WH, 110):
        for x in range(30 + (y // 110 % 2) * 55, WW, 110):
            d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(230, 160, 180, 255))
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(250, 230, 120, 255))
    return im


@lru_cache(maxsize=8)
def granny(i, up):
    img = Image.new("RGBA", (260, 330), (0, 0, 0, 0))
    sweater = [(150, 120, 200), (110, 180, 170), (230, 140, 120)][i % 3]
    body = E.shape(230, 160, [("ellipse", 0, 0, 230, 260)], sweater, seed=30 + i)
    E.paste(img, body, 15, 170)
    hair = E.shape(200, 170, [("circle", 100, 100, 92), ("circle", 100, 25, 40)], (215, 215, 222), seed=31 + i)
    E.paste(img, hair, 30, 0)
    face = E.shape(150, 150, [("circle", 75, 75, 75)], (250, 205, 185), seed=32 + i)
    E.paste(img, face, 55, 70)
    d = ImageDraw.Draw(img)
    dy = -10 if up else 10
    for gx in (105, 165):
        d.ellipse([gx - 26, 132, gx + 26, 184], outline=(120, 90, 60, 255), width=5)
        d.ellipse([gx - 8, 150 + dy, gx + 8, 166 + dy], fill=(20, 18, 20, 255))
    d.line([(131, 158), (139, 158)], fill=(120, 90, 60, 255), width=5)
    d.line([(60, 300), (150, 230)], fill=(200, 200, 205, 255), width=6)
    d.line([(200, 300), (110, 230)], fill=(200, 200, 205, 255), width=6)
    doll = E.nubo(70)
    put(img, doll, 130, 300)
    return E.Sprite(img)


def world_grannies(t):
    im = granny_bg().copy()
    up = t > 6.6
    for i in range(6):
        x = 140 + (i % 3) * 240
        y = 230 + (i // 3) * 360
        knit = 0 if up else math.sin(t * 14 + i) * 4
        put(im, granny(i, up), x, y + 160 + knit, jid=("g", i), jamp=1.2)
    return im


@lru_cache(maxsize=1)
def whale_bg():
    im = Image.new("RGBA", (WW, WH), (150, 60, 80, 255))
    im.alpha_composite(E.felt_panel(WW, WH, (160, 66, 86), seed=40, stitch=False))
    for k in range(5):
        x = 60 + k * 160
        rib = E.S(80, WH, [("rect", 0, 0, 80, WH, 40)], (200, 110, 120), seed=41 + k)
        put(im, rib, x, WH / 2 - 100)
    water = E.S(WW + 40, 300, [("rect", 0, 0, WW + 40, 300, 20)], (90, 150, 210), seed=46, anchor="top")
    put(im, water, WW / 2, WH - 300)
    lh = E.S(120, 420, [("poly", [(20, 0), (100, 0), (120, 420), (0, 420)])], (245, 245, 240), seed=47, anchor="bottom")
    d = ImageDraw.Draw(lh.img)
    for y in (90, 210, 330):
        d.rectangle([0, y, 140, y + 50], fill=(220, 70, 70, 255))
    put(im, lh, WW / 2 + 140, WH - 230)
    cap = E.S(150, 90, [("rect", 0, 30, 150, 90, 10), ("poly", [(20, 30), (75, -20), (130, 30)])], (220, 70, 70),
              seed=48, anchor="bottom")
    put(im, cap, WW / 2 + 140, WH - 650)
    return im


def world_whale(t):
    im = whale_bg().copy()
    beam = Image.new("RGBA", (WW, WH), (0, 0, 0, 0))
    d = ImageDraw.Draw(beam)
    cx, cy = WW / 2 + 140, WH - 690
    a = t * 2.2
    for s in (1, -1):
        aa = a + (0 if s > 0 else math.pi)
        p1 = (cx + math.cos(aa - 0.12) * 900, cy + math.sin(aa - 0.12) * 300)
        p2 = (cx + math.cos(aa + 0.12) * 900, cy + math.sin(aa + 0.12) * 300)
        d.polygon([(cx, cy), p1, p2], fill=(255, 240, 150, 90))
    im.alpha_composite(beam.filter(ImageFilter.GaussianBlur(6)))
    E.glow(im, cx, cy, 60, (255, 240, 150), 0.9)
    y = (t * 500) % 700
    E.particles(im, [(200, 80 + y, 12, (220, 160, 170), 0.9)])
    return im


@lru_cache(maxsize=1)
def office_base():
    yy, xx = np.mgrid[0:WH, 0:WW].astype(np.float32)
    g = 150 + 40 * np.exp(-((yy - 80) / 500) ** 2) - 30 * (yy / WH)
    arr = np.dstack([g * 0.97, g * 1.0, g * 1.02])
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 820, WW, WH], fill=(105, 108, 112, 255))
    d.rectangle([60, 600, 340, 830], fill=(85, 88, 95, 255))
    d.rectangle([80, 620, 320, 780], fill=(130, 170, 200, 255))
    d.rectangle([180, 830, 220, 900], fill=(70, 70, 75, 255))
    return im


@lru_cache(maxsize=8)
def human_eye(look_k, open_k):
    """Œil humain « réaliste » (rupture de style)."""
    w, h = 640, 400
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    ex = (xx - cx) / (w * 0.46)
    ey = (yy - cy) / (h * 0.42 * max(0.05, open_k))
    inside = (ex ** 2 + ey ** 2) < 1
    skin = np.dstack([np.full_like(xx, 205), np.full_like(xx, 160), np.full_like(xx, 140)])
    shade = 1 - 0.25 * np.clip(((xx - cx) / (w / 2)) ** 2 + ((yy - cy) / (h / 2)) ** 2, 0, 1)
    skin = skin * shade[..., None]
    r2 = ex ** 2 + ((yy - cy) / (h * 0.42)) ** 2
    sclera = np.dstack([235 - 30 * r2, 228 - 50 * r2, 220 - 55 * r2])
    ix = cx + (look_k - 0.5) * 120
    ir = np.sqrt((xx - ix) ** 2 + (yy - cy) ** 2)
    ang = np.arctan2(yy - cy, xx - ix)
    fib = 0.5 + 0.5 * np.sin(ang * 40) * np.sin(ang * 13 + 1)
    iris = np.dstack([90 + 40 * fib, 110 + 30 * fib, 70 + 20 * fib]) * (1 - 0.4 * (ir / 95)[..., None])
    out = np.where(inside[..., None], sclera, skin)
    m_iris = inside & (ir < 95)
    out = np.where(m_iris[..., None], iris, out)
    out = np.where((inside & (ir < 42))[..., None], np.dstack([np.full_like(xx, 12)] * 3), out)
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    r = random.Random(7)
    for _ in range(14):
        x0 = r.choice([cx - w * 0.44, cx + w * 0.44])
        y0 = cy + r.uniform(-30, 30)
        pts = [(x0, y0)]
        for k in range(5):
            x0 += (cx - x0) * 0.18 + r.uniform(-8, 8)
            y0 += r.uniform(-14, 14)
            pts.append((x0, y0))
        d.line(pts, fill=(200, 60, 60, 160), width=2)
    d.ellipse([ix - 30, cy - 40, ix - 8, cy - 18], fill=(255, 255, 255, 230))
    # cils
    for k in range(26):
        u = k / 25
        x = cx - w * 0.44 + u * w * 0.88
        y = cy - math.sqrt(max(0, 1 - ((x - cx) / (w * 0.46)) ** 2)) * h * 0.42 * open_k
        d.line([(x, y), (x + (u - 0.5) * 30, y - 40)], fill=(40, 30, 25, 255), width=3)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, w, h], fill=255)
    im.putalpha(mask.filter(ImageFilter.GaussianBlur(30)))
    return E.Sprite(im)


def world_office(t):
    im = office_base().copy()
    flick = 1.0 if (E.FRAME % 7) else 0.55
    d = ImageDraw.Draw(im)
    d.rectangle([80, 40, WW - 80, 70], fill=(int(250 * flick), int(252 * flick), int(255 * flick), 255))
    look = ease_in_out(seg(t, 11.5, 12.3)) * 0.0 + (1 - ease_in_out(seg(t, 11.5, 12.3))) * 1.0
    op = 0.35 + 0.65 * ease_out(seg(t, 11.3, 11.9))
    put(im, human_eye(round(look * 4) / 4, round(op * 5) / 5), WW / 2, 420, scale=1.1)
    a = np.asarray(im.convert("RGB"), np.float32)
    g = a.mean(axis=2, keepdims=True)
    a = a * 0.35 + g * 0.65
    a += np.random.default_rng(E.FRAME).normal(0, 9, a.shape[:2] + (1,))
    return Image.fromarray(np.clip(a * flick ** 0.3, 0, 255).astype(np.uint8)).convert("RGBA")


@lru_cache(maxsize=1)
def landing_bg():
    im = Image.new("RGBA", (WW, WH), E.CREAM + (255,))
    im.alpha_composite(E.felt_panel(WW, WH, (250, 238, 215), seed=60, stitch=False))
    fl = E.felt_panel(WW, 300, (200, 170, 140), seed=61)
    im.alpha_composite(fl, (0, WH - 300))
    plant = E.S(150, 300, [("ellipse", 30, 0, 120, 160), ("ellipse", 0, 80, 90, 200), ("ellipse", 60, 80, 150, 210)],
                (110, 180, 120), seed=62, anchor="bottom")
    put(im, plant, 640, WH - 330)
    pot = E.S(120, 120, [("poly", [(0, 0), (120, 0), (100, 120), (20, 120)])], (210, 120, 90), seed=63,
              anchor="bottom")
    put(im, pot, 640, WH - 260)
    return im


def world_landing(t, other=True):
    im = landing_bg().copy()
    if other:
        look, o = (-0.6, 0.6), 1.0
        if 18.0 < t < 19.8:
            look, o = E.regard_eyes(t, 18.0, (-0.6, 0.6))
        E.shadow(im, 350, WH - 160, 330)
        put(im, E.nubo(370, look=look, eyes=o), 350, WH - 160, jid="other")
    return im


WORLDS = {"bear": world_bear, "space": world_space, "grannies": world_grannies, "whale": world_whale,
          "office": world_office, "landing": world_landing}


# ------------------------------------------------------------------ ascenseur
@lru_cache(maxsize=1)
def cabin():
    im = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
    wall = E.felt_panel(E.W, E.H, (196, 150, 110), seed=70, stitch=False)
    m = Image.new("L", (E.W, E.H), 255)
    ImageDraw.Draw(m).rectangle([DX0, DY0, DX1, DY1], fill=0)
    im.paste(wall, (0, 0), m)
    d = ImageDraw.Draw(im)
    d.rectangle([DX0 - 26, DY0 - 26, DX1 + 26, DY0], fill=(170, 170, 178, 255))
    d.rectangle([DX0 - 26, DY0, DX0, DY1], fill=(170, 170, 178, 255))
    d.rectangle([DX1, DY0, DX1 + 26, DY1], fill=(170, 170, 178, 255))
    for x in (40, E.W - 40):
        d.line([(x, 0), (x, E.H)], fill=(170, 125, 90, 255), width=8)
    carpet = E.felt_panel(E.W, E.H - DY1, (190, 70, 70), seed=71)
    im.alpha_composite(carpet, (0, DY1))
    ind = E.S(560, 110, [("rect", 0, 0, 560, 110, 24)], (60, 55, 60), seed=72)
    put(im, ind, (DX0 + DX1) / 2, DY0 - 120)
    panel = E.S(130, 330, [("rect", 0, 0, 130, 330, 20)], (180, 180, 190), seed=73)
    put(im, panel, 105, 1450)
    d = ImageDraw.Draw(im)
    for k in range(3):
        for j in range(2):
            x, y = 75 + j * 60, 1330 + k * 70
            d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(235, 235, 240, 255), outline=(120, 120, 130, 255), width=3)
    d.polygon([(80, 1560), (105, 1545), (105, 1575)], fill=(60, 60, 70, 255))
    d.polygon([(130, 1560), (105, 1545), (105, 1575)], fill=(60, 60, 70, 255))
    put(im, E.duck(60), 1010, 1880)
    return im


@lru_cache(maxsize=1)
def door_panel():
    sp = E.S(WW / 2 + 10, WH, [("rect", 0, 0, WW / 2 + 10, WH, 8)], (175, 178, 188), seed=74)
    d = ImageDraw.Draw(sp.img)
    d.line([(20, 40), (20, WH - 40)], fill=(150, 152, 162, 255), width=4)
    return sp


def floor_light(t):
    stops = [0, 2.8, 5.6, 8.2, 11.0, 15.2, 23.6]
    n = 0
    for i, s in enumerate(stops):
        if t >= s:
            n = i
    if 21.9 < t < 23.6:
        n = 0
    return n


def frame(t):
    c = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 255))
    o, wname = door_open(t)
    if o > 0 and wname:
        if wname == "landing":
            wimg = world_landing(t, other=t < 19.8)
            if t >= 21.2:
                # notre NUBO est désormais sur le palier
                put(wimg, E.nubo(370, look=(0.3, 0.4)), 380, WH - 160, jid="ours")
        else:
            wimg = WORLDS[wname](t)
        c.alpha_composite(wimg, (DX0, DY0))
    # portes
    pw = WW / 2
    shift = o * pw
    layer = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
    put(layer, door_panel(), DX0 + pw / 2 - shift, DY0 + WH / 2)
    put(layer, door_panel(), DX0 + pw * 1.5 + shift, DY0 + WH / 2)
    m = Image.new("L", (E.W, E.H), 0)
    ImageDraw.Draw(m).rectangle([DX0, DY0, DX1, DY1], fill=255)
    c.paste(layer, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(layer.getchannel("A")))))
    c.alpha_composite(cabin())
    # voyants d'étage
    d = ImageDraw.Draw(c)
    n = floor_light(t)
    for k in range(6):
        x = (DX0 + DX1) / 2 - 200 + k * 80
        on = k == n % 6
        d.ellipse([x - 18, DY0 - 138, x + 18, DY0 - 102], fill=(255, 190, 60, 255) if on else (90, 85, 90, 255))
    if t < 19.8 or t >= 21.2:
        draw_main(c, t)
    else:
        # échange de place : l'autre NUBO sort, le nôtre entre
        k = ease_in_out(seg(t, 19.8, 21.2))
        ox, oy = DX0 + 350, DY0 + WH - 160
        put(c, E.nubo(int(E.lerp(370, NH, k)), look=(-0.4 + 0.4 * k, 0.5)),
            E.lerp(ox, NX + 40, k), E.lerp(oy, NY, k) - abs(math.sin(k * 12)) * 20, jid="o2")
        put(c, E.nubo(int(E.lerp(NH, 370, k)), look=(0.6 - 0.3 * k, -0.4)),
            E.lerp(NX, DX0 + 380, k), E.lerp(NY, oy, k) - abs(math.sin(k * 12 + 1)) * 20, jid="n")
    return c


def draw_main(c, t):
    kw = dict(h=NH, look=(0.6, -0.5), tuft="curl", arms=(18, 18))
    sx = sy = 1
    for p in PRESSES:
        if p - 0.08 <= t < p + 0.12:
            kw["arms"] = (120, 18)
            kw["look"] = (-1, 0)
    if 11.3 < t < 13.9:
        kw["tuft"] = "up"
        kw["scared"] = True
        kw["sweat"] = True
    if 6.6 < t < 7.5:
        kw["tuft"] = "up"
    if 13.9 <= t < 15.2:
        k = seg(t, 13.9, 14.6)
        sy = 1 - 0.1 * math.sin(math.pi * k)
        sx = 1 + 0.08 * math.sin(math.pi * k)
        kw["tuft"] = "down"
        kw["eyes"] = 0.0 if t < 14.5 else 1.0
    if 15.6 <= t < 18.0:
        kw["look"] = (0.6, -0.5)
    if 18.0 <= t < 19.8:
        kw["look"], kw["eyes"] = E.regard_eyes(t, 18.0, (0.6, -0.5))
    if t >= 21.2:
        kw["look"] = (0.6, -0.5)
    if 1.6 < t < 2.8 or 4.9 < t < 5.6 or 21.9 < t < 23.6:
        sy = 1 + 0.02 * math.sin(t * 12)
    E.shadow(c, NX, NY, NH * 0.9)
    put(c, E.nubo(**kw), NX, NY, sx=sx, sy=sy, jid="n")


def sound(m):
    # bossa d'ascenseur (originale)
    beat = 60 / 112
    chords = [["F4", "A4", "C5", "E5"], ["E4", "G4", "B4", "D5"], ["D4", "F4", "A4", "C5"], ["G3", "B3", "D4", "F4"]]
    bassn = ["F2", "E2", "D2", "G2"]
    mel = [(0, "C6", 1.5), (1.5, "A5", 0.5), (2, "G5", 1), (3, "A5", 1), (4, "B5", 1.5), (5.5, "G5", 0.5),
           (6, "E5", 2), (8, "A5", 1.5), (9.5, "F5", 0.5), (10, "E5", 1), (11, "F5", 1), (12, "G5", 3)]
    bed = A.Mix(DUR)
    nb = int(DUR / beat)
    for b in range(nb):
        ch = chords[(b // 4) % 4]
        if b % 4 == 0:
            for nn in ch:
                bed.add(b * beat, A.epiano(A.NOTE(nn), beat * 3.5), 0.5)
        if b % 4 == 2:
            for nn in ch[1:]:
                bed.add(b * beat + beat * 0.5, A.epiano(A.NOTE(nn), beat * 1.5), 0.3)
        bed.add(b * beat, A.bass(A.NOTE(bassn[(b // 4) % 4]) * (1.5 if b % 2 else 1), beat), 0.5)
        bed.add(b * beat, A.shaker(), 0.4)
        bed.add(b * beat + beat / 2, A.shaker(), 0.25)
    for k in range(3):
        for bb, nn, dd in mel:
            bed.seq(k * 16 * beat, 112, [(bb, nn, dd)], A.whistle, 0.3)
    # volume du fond : plus bas pendant les mondes, coupé pendant le face-à-face
    g = np.ones(bed.n)
    def env(t0, t1, v):
        a, b = int(t0 * A.SR), int(t1 * A.SR)
        g[a:b] = v
    for o0, o1, c0, c1, w in STOPS:
        env(max(0, o0), min(DUR, c1), 0.45)
    env(15.6, 19.6, 0.0)
    env(19.6, 21.9, 0.4)
    k = int(0.05 * A.SR)
    g = np.convolve(g, np.ones(k) / k, mode="same")
    m.add(0, bed.L * g, 0.5, -0.1)
    m.add(0, bed.R * g, 0.5, 0.1)
    # dings & boutons
    for t0 in (0.0, 2.8, 5.6, 8.2, 11.0, 15.2, 23.6):
        m.add(t0, A.ding(1568, 1.5), 0.6)
    for p in PRESSES:
        m.add(p, A.click(0.02, 1500, int(p * 10)), 0.8, -0.6)
    for o0, o1, c0, c1, w in STOPS:
        if o0 >= 0 and o0 < DUR:
            m.add(o0, A.whoosh(0.4, 200, 1200, 3) * 0.6, 0.4)
        if c0 < DUR:
            m.add(c0, A.whoosh(0.5, 200, 1200, 4) * 0.6, 0.4)
            m.add(c1 - 0.05, A.thump(90, 0.2), 0.4)
    # ambiances des mondes
    m.add(0, A.bubbles(1.6, 1), 0.5)
    m.add(0.2, A.vowel(110, 90, 0.6, ((200, 600), (600, 900))) * np.linspace(1, 0, int(0.6 * A.SR)), 0.4)
    m.add(3.3, A.squeak(1.8, 0.1), 0.2)
    m.add(3.5, A.kalimba(A.NOTE("C7"), 0.5) * 0.4, 0.3)
    for k in range(10):
        m.add(5.8 + k * 0.12, A.tick(True) * 0.4, 0.3)
    m.add(6.6, A.horror_screech(0.25) * 0.6, 0.5)
    m.add(6.62, A.nub(1.3), 0.5)
    whale = np.sin(A.phase(A.glide(160, 90, 1.6), int(1.6 * A.SR))) * np.sin(np.linspace(0, np.pi, int(1.6 * A.SR)))
    m.add(8.4, A.bandpass(whale, 50, 800) * 0.8, 0.6)
    m.add(9.0, A.plop(1.4), 0.3)
    m.add(11.0, A.hum(2.9, 100) * 2, 0.5)
    m.add(11.2, A.drone(2.7, 46), 1.0)
    m.add(11.35, A.horror_screech(0.5), 0.5)
    m.add(11.4, A.nub(1.5), 0.6)
    m.add(14.0, A.wind(0.7, 0.4), 0.5)
    m.add(19.0, A.nub(1.0), 0.5)
    m.add(19.0, A.nub(1.0), 0.5, 0.4)
    m.add(19.0, A.regard(), 0.6)
    for k in range(6):
        m.add(19.9 + k * 0.22, A.tick(k % 2 == 0) * 0.5, 0.3)
