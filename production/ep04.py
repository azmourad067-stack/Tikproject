"""ÉPISODE 04 — 03:17 (caméra de surveillance)."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, keys

SLUG = "ep04_0317"
DUR = 20.0
COVER_T = 3.6
POST = False
FX0, FY0, FX1, FY1 = 600, 330, 1010, 1330   # frigo (face avant)
FLOOR_Y = 1330
NH = 230

# fenêtres d'ouverture de porte : (début ouverture, fin ouverture, début fermeture, fin fermeture, mode)
DOORS = [(2.4, 2.8, 5.0, 5.5, "party"), (6.6, 6.75, 8.6, 9.0, "freeze"), (11.0, 11.12, 99, 99, "stare")]


@lru_cache(maxsize=1)
def bg():
    b = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 255))
    wall = E.felt_panel(E.W, FLOOR_Y, (200, 205, 190), seed=80, stitch=False)
    b.alpha_composite(wall)
    floor = Image.new("RGBA", (E.W, E.H - FLOOR_Y), (0, 0, 0, 0))
    d = ImageDraw.Draw(floor)
    s = 135
    for yi in range(0, E.H - FLOOR_Y, s):
        for xi in range(0, E.W, s):
            c = (235, 230, 215) if ((xi // s + yi // s) % 2 == 0) else (170, 200, 185)
            d.rectangle([xi, yi, xi + s, yi + s], fill=c + (255,))
    fl = E.felt(Image.new("L", floor.size, 255), (255, 255, 255), seed=81, rim=0, fuzz=0, light=False)
    arr = np.asarray(floor, np.float32) * (np.asarray(fl, np.float32) / 255.0)
    b.alpha_composite(Image.fromarray(arr.astype(np.uint8), "RGBA"), (0, FLOOR_Y))
    # plan de travail + placards
    cab = E.S(560, 420, [("rect", 0, 0, 560, 420, 14)], (160, 190, 210), seed=82, anchor="top")
    put(b, cab, 290, FLOOR_Y - 420)
    top = E.S(600, 50, [("rect", 0, 0, 600, 50, 10)], E.WOOD, seed=83)
    put(b, top, 290, FLOOR_Y - 430)
    d = ImageDraw.Draw(b)
    for x in (150, 430):
        d.rounded_rectangle([x - 110, FLOOR_Y - 380, x + 110, FLOOR_Y - 40], radius=12, outline=(110, 140, 160, 255), width=6)
        d.ellipse([x + 70, FLOOR_Y - 230, x + 90, FLOOR_Y - 210], fill=(90, 90, 100, 255))
    up = E.S(560, 300, [("rect", 0, 0, 560, 300, 14)], (160, 190, 210), seed=84, anchor="top")
    put(b, up, 290, 250)
    kettle = E.S(140, 130, [("ellipse", 0, 20, 140, 130), ("rect", 50, 0, 90, 30, 8)], (230, 120, 110), seed=85,
                 anchor="bottom")
    put(b, kettle, 400, FLOOR_Y - 455)
    put(b, E.duck(70), 160, FLOOR_Y - 452)
    # frigo (caisse)
    fr = E.S(FX1 - FX0 + 40, FY1 - FY0 + 30, [("rect", 0, 0, FX1 - FX0 + 40, FY1 - FY0 + 30, 40)], (235, 238, 240),
             seed=86, anchor="top")
    put(b, fr, (FX0 + FX1) / 2, FY0 - 20)
    return b


@lru_cache(maxsize=1)
def interior_base():
    w, h = FX1 - FX0 - 40, FY1 - FY0 - 50
    im = Image.new("RGBA", (w, h), (225, 235, 240, 255))
    d = ImageDraw.Draw(im)
    for y in (h * 0.33, h * 0.66):
        d.rectangle([0, y, w, y + 14], fill=(190, 210, 225, 255))
    return im


@lru_cache(maxsize=1)
def door():
    w, h = FX1 - FX0, FY1 - FY0
    sp = E.S(w, h, [("rect", 0, 0, w, h, 34)], (245, 246, 248), seed=87)
    d = ImageDraw.Draw(sp.img)
    d.rounded_rectangle([30, h * 0.35, 54, h * 0.62], radius=10, fill=(170, 175, 185, 255))
    return sp


def eyes_on(img, pts, r, look, closed=False):
    d = ImageDraw.Draw(img)
    for x, y in pts:
        x += look[0] * r * 0.4
        y += look[1] * r * 0.4
        if closed:
            d.arc([x - r, y - r, x + r, y + r], 20, 160, fill=(20, 20, 20, 255), width=max(2, int(r * 0.4)))
            continue
        d.ellipse([x - r, y - r, x + r, y + r], fill=(20, 18, 20, 255))
        d.ellipse([x - r * 0.5, y - r * 0.6, x - r * 0.05, y - r * 0.15], fill=(255, 255, 255, 230))


@lru_cache(maxsize=64)
def item(kind, look, closed=False):
    if kind == "egg":
        sp = E.S(90, 116, [("ellipse", 0, 0, 90, 116)], (250, 248, 240), seed=90)
        eyes_on(sp.img, [(36, 56), (62, 56)], 7, look, closed)
    elif kind == "sausage":
        sp = E.S(200, 70, [("rect", 0, 0, 200, 70, 35)], (205, 110, 95), seed=91)
        eyes_on(sp.img, [(150, 32), (176, 32)], 7, look, closed)
    elif kind == "lemon":
        sp = E.S(140, 100, [("ellipse", 0, 0, 140, 100), ("ellipse", -10, 38, 30, 62), ("ellipse", 120, 38, 160, 62)],
                 (250, 225, 80), seed=92)
        eyes_on(sp.img, [(60, 46), (88, 46)], 8, look, closed)
    elif kind == "cheese":
        sp = E.S(150, 110, [("poly", [(0, 110), (150, 110), (150, 0)])], (250, 205, 90), seed=93)
        eyes_on(sp.img, [(100, 76), (124, 76)], 7, look, closed)
    elif kind == "milk":
        sp = E.S(100, 200, [("rect", 0, 40, 100, 200, 18), ("rect", 25, 0, 75, 50, 8)], E.WHITE, seed=94)
        ImageDraw.Draw(sp.img).rectangle([31, 6, 81, 30], fill=(90, 140, 230, 255))
        eyes_on(sp.img, [(42, 110), (68, 110)], 8, look, closed)
    else:  # jelly
        sp = E.S(130, 100, [("ellipse", 0, 0, 130, 70), ("rect", 0, 35, 130, 100, 10)], (240, 90, 120), seed=95)
        eyes_on(sp.img, [(52, 50), (80, 50)], 8, look, closed)
    sp.anchor = (sp.img.width / 2, sp.img.height - 6)
    return sp


ITEMS = [("egg", 0.18, 0.31), ("egg", 0.38, 0.31), ("egg", 0.58, 0.31), ("cheese", 0.82, 0.31),
         ("sausage", 0.3, 0.64), ("lemon", 0.72, 0.64), ("milk", 0.22, 0.985), ("jelly", 0.62, 0.985)]


def door_state(t):
    """(ouverture 0..1, mode)."""
    for o0, o1, c0, c1, mode in DOORS:
        if o0 <= t < c1:
            if t < o1:
                return ease_out(seg(t, o0, o1)), mode
            if t < c0:
                return 1.0, mode
            return 1 - ease_in_out(seg(t, c0, c1)), mode
    return 0.0, None


def interior(t, mode):
    im = interior_base().copy()
    w, h = im.size
    beat = 60 / 118
    if mode == "party":
        ph = (t % beat) / beat
        cols = [(255, 120, 200), (120, 230, 255), (255, 230, 90), (160, 255, 140)]
        tint = cols[int(t / beat) % 4]
        ov = Image.new("RGBA", im.size, tint + (90,))
        im.alpha_composite(ov)
    for i, (k, fx, fy) in enumerate(ITEMS):
        x, y = fx * w, fy * h - 12
        rot, dy = 0, 0
        look, closed = (0, 0), False
        if mode == "party":
            ph = t / beat * math.pi
            dy = -abs(math.sin(ph + i)) * 30
            rot = math.sin(ph + i * 0.7) * 16
            look = (1, 0) if i % 2 else (-1, 0)
            closed = (int(t / beat) + i) % 3 == 0
        elif mode == "freeze":
            look = (0.4, -0.8) if i % 2 else (-0.4, -0.8)
            if k == "egg" and i == 1 and 7.2 < t < 8.2:
                rot = math.sin((t - 7.2) * 25) * 10 * (1 - seg(t, 7.2, 8.2))
        elif mode == "stare":
            look = (-0.5, -1)
        put(im, item(k, look, closed), x, y + dy, rot=rot, jid=("it", i), jamp=1.0, jrot=0.4)
    if mode == "party":
        # boule à facettes
        bx, by = w / 2, 60
        d = ImageDraw.Draw(im)
        d.line([bx, 0, bx, by - 40], fill=(120, 120, 120, 255), width=4)
        d.ellipse([bx - 45, by - 45, bx + 45, by + 45], fill=(190, 195, 205, 255))
        rot = t * 3
        for a in range(0, 360, 30):
            aa = math.radians(a) + rot
            d.line([bx + math.cos(aa) * 45, by - 45, bx + math.cos(aa) * 45, by + 45], fill=(150, 155, 170, 255), width=2)
        for yy in (-25, 0, 25):
            d.line([bx - 45, by + yy, bx + 45, by + yy], fill=(150, 155, 170, 255), width=2)
        r = E.rng_for("sp", E.FRAME)
        for _ in range(10):
            sx, sy = r.uniform(0, w), r.uniform(0, h)
            d.line([sx - 10, sy, sx + 10, sy], fill=(255, 255, 255, 220), width=3)
            d.line([sx, sy - 10, sx, sy + 10], fill=(255, 255, 255, 220), width=3)
    return im


def nubo_pos(t):
    k = seg(t, 0.2, 2.3)
    x = E.lerp(-120, FX0 - 30, k)
    y = FLOOR_Y + 200 - abs(math.sin(k * math.pi * 6)) * 30 * (1 if k < 1 else 0)
    return x, y


def color_scene(t):
    """Scène en couleur ; renvoie (image, couche couleur de l'intérieur du frigo)."""
    c = bg().copy()
    o, mode = door_state(t)
    x, y = nubo_pos(t)
    look = (1, 0)
    arms = (18, 18)
    if 2.3 < t < 2.9 or 6.5 < t < 6.8 or 10.9 < t < 11.2:
        arms = (18, 120)
    if t > 13.5:
        k = ease_in_out(seg(t, 13.5, 15.2))
        look = (1 - 1.5 * k, -k)
    tuft = "up" if t > 11.0 else "curl"
    eyes = 1.0
    if 11.0 < t < 13.5:
        eyes = 1.0
    E.shadow(c, x, y, NH * 0.9)
    color_layer = None
    if o > 0:
        inner = interior(t, mode)
        color_layer = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
        color_layer.alpha_composite(inner, (FX0 + 20, FY0 + 25))
        if mode == "party":
            d = ImageDraw.Draw(color_layer)
            beat = 60 / 118
            cols = [(255, 90, 200), (90, 220, 255), (255, 230, 80), (140, 255, 120)]
            for k2 in range(3):
                cc = cols[(int(t / beat) + k2) % 4]
                x0 = FX0 + 40 + k2 * 120
                d.polygon([(x0, FY1 - 50), (x0 + 90, FY1 - 50), (x0 - 300 + k2 * 120, E.H), (x0 - 520 + k2 * 120, E.H)],
                          fill=cc + (70,))
        # porte : panneau qui pivote vers la droite
        dw = (FX1 - FX0) * (1 - o)
        if dw > 4:
            dimg, ax, ay = E.transform(door(), sx=max(0.02, dw / (FX1 - FX0)))
            color_layer.alpha_composite(dimg, (int(FX1 - dimg.width + 6), FY0 - 6))
        slab = E.S(70, FY1 - FY0, [("rect", 0, 0, 70, FY1 - FY0, 20)], (235, 237, 240), seed=96)
        put(color_layer, slab, FX1 + 35 * o, (FY0 + FY1) / 2, sx=max(0.05, o))
    else:
        put(c, door(), (FX0 + FX1) / 2, (FY0 + FY1) / 2, jid="door", jamp=0.5, jrot=0.1)
    nub = E.nubo(NH, look=look, arms=arms, tuft=tuft, eyes=eyes)
    return c, color_layer, (nub, x, y)


# ------------------------------------------------------------------ effet caméra de surveillance
@lru_cache(maxsize=4)
def barrel_map(k):
    yy, xx = np.mgrid[0:E.H, 0:E.W].astype(np.float32)
    nx = (xx - E.W / 2) / (E.W / 2)
    ny = (yy - E.H / 2) / (E.W / 2)
    r2 = nx * nx + ny * ny
    f = 1 / (1 + k * r2) if k > 0 else 1
    sx = np.clip(nx * f * (1 + k * 0.9) * (E.W / 2) + E.W / 2, 0, E.W - 1).astype(np.int32)
    sy = np.clip(ny * f * (1 + k * 0.9) * (E.W / 2) + E.H / 2, 0, E.H - 1).astype(np.int32)
    return sy, sx


@lru_cache(maxsize=1)
def scanlines():
    a = np.ones((E.H, 1, 1), np.float32)
    a[::4] = 0.82
    a[1::4] = 0.9
    yy, xx = np.mgrid[0:E.H, 0:E.W].astype(np.float32)
    d = np.sqrt(((xx - E.W / 2) / (E.W * 0.55)) ** 2 + ((yy - E.H / 2) / (E.H * 0.58)) ** 2)
    vig = np.clip(1.15 - 0.55 * d ** 2, 0.1, 1)[..., None]
    return a * vig


def cctv(img_rgb, color=None, k=0.14, ts=None):
    a = np.asarray(img_rgb.convert("RGB"), np.float32)
    g = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11
    g = np.clip((g / 255) ** 1.6 * 255 * 0.85, 0, 255)
    out = np.dstack([g * 0.72, g * 0.92, g * 0.76])
    if color is not None:
        ca = np.asarray(color, np.float32)
        al = ca[..., 3:4] / 255
        out = out * (1 - al) + ca[..., :3] * 0.92 * al
    rng = np.random.default_rng(E.FRAME)
    out += rng.normal(0, 11, (E.H, E.W, 1)).astype(np.float32)
    sy, sx = barrel_map(k)
    out = out[sy, sx]
    out *= scanlines()
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    if ts:
        timg = E.text_img(ts, 64, (235, 245, 235))
        im.paste(timg, (60, 70), timg)
    if (E.FRAME // 6) % 2 == 0:
        d.ellipse([E.W - 110, 82, E.W - 64, 128], fill=(230, 40, 40))
    return im


def timestamp(t):
    s = 4 + int(t)
    return f"03:17:{s:02d}"


def frame(t):
    if t < 15.8:
        c, color_layer, (nub, x, y) = color_scene(t)
        put(c, nub, x, y, jid="n")
        if color_layer is not None:
            # NUBO passe devant la lumière du frigo
            nl = Image.new("RGBA", (E.W, E.H), (0, 0, 0, 0))
            put(nl, nub, x, y, jid="n")
            ca = np.asarray(color_layer, np.float32)
            na = np.asarray(nl, np.float32)[..., 3:4] / 255
            ca[..., 3:4] *= (1 - na)
            color_layer = Image.fromarray(ca.astype(np.uint8), "RGBA")
        if t > 11.2:
            z = 1 + 0.35 * ease_in_out(seg(t, 11.2, 15.6))
            c = E.camera(c, z, 760, 1000)
            if color_layer is not None:
                color_layer = E.camera(color_layer, z, 760, 1000)
        return cctv(c, color_layer, 0.14, timestamp(t))
    if t < 17.6 or t > 19.75:
        a = (np.random.default_rng(E.FRAME).random((E.H // 4, E.W // 4)) * 255).astype(np.uint8)
        im = Image.fromarray(a).resize((E.W, E.H), Image.NEAREST).convert("RGB")
        if t > 19.75:
            return im
        return im
    # NUBO collé à l'objectif
    c = Image.new("RGBA", (E.W, E.H), (60, 60, 60, 255))
    look, o = E.regard_eyes(t, 17.8, (0.3, 0.2))
    sp = E.nubo(1000, look=look, eyes=o, tuft="up")
    wob = math.sin(t * 2) * 10
    put(c, sp, 540 + wob, 960 + 586 * 1.5, scale=1.5, jid="face", jamp=6)
    return cctv(c, None, 0.3, timestamp(t))


def sound(m):
    # bourdonnement du frigo + souffle de caméra
    m.add(0, A.hum(DUR, 50) * 0.8, 0.5)
    m.add(0, A.bandpass(A.noise(DUR, 2), 2000, 9000) * 0.05, 0.6)
    for k in range(8):
        m.add(0.3 + k * 0.27, A.tick(k % 2 == 0) * 0.5, 0.25, -0.5 + k * 0.1)
    m.add(2.4, A.clack(), 0.6, 0.3)
    m.add(6.6, A.clack(), 0.6, 0.3)
    m.add(11.0, A.clack(), 0.8, 0.3)
    m.add(5.4, A.thump(70, 0.3), 0.6, 0.3)
    m.add(8.95, A.thump(70, 0.3), 0.6, 0.3)
    # disco : forte porte ouverte, étouffée porte fermée, coupée net quand on ouvre « en mode figé »
    bpm = 118
    beat = 60 / bpm
    def disco(t0, t1, muffled):
        mm = A.Mix(t1 - t0 + 1)
        bl = ["C3", "C3", "C4", "C3", "A#2", "A#2", "A#3", "A#2"]
        for i in range(int((t1 - t0) / (beat / 2)) + 1):
            tt = i * beat / 2
            if i % 2 == 0:
                mm.add(tt, A.kick(), 0.9)
            else:
                mm.add(tt, A.hat(0.08), 0.6)
                if i % 4 == 3:
                    mm.add(tt, A.snare(), 0.5)
            mm.add(tt, A.bass(A.NOTE(bl[i % 8]), beat / 2), 0.6)
            if i % 4 == 0:
                for nn in (["E5", "G5", "C6"] if (i // 8) % 2 == 0 else ["D5", "F5", "A#5"]):
                    mm.add(tt, A.brass(A.NOTE(nn), beat * 0.4), 0.25)
        x = mm.L[:int((t1 - t0) * A.SR)]
        if muffled:
            x = A.bandpass(x, 30, 300) * 1.4
        return x
    m.add(2.8, disco(2.8, 5.0, False), 0.7)
    m.add(5.0, disco(5.0, 5.5, False) * np.linspace(1, 0.3, int(0.5 * A.SR)), 0.7)
    m.add(5.5, disco(5.5, 6.6, True), 0.6)
    m.add(9.0, disco(9.0, 11.0, True), 0.6)
    m.add(7.2, A.squeak(0.5, 0.12) * 0.3, 0.3, 0.3)
    m.add(11.1, A.drone(6.0, 55), 0.8)
    m.add(11.15, A.horror_screech(0.25), 0.3)
    m.add(15.2, A.nub(0.8), 0.4)
    m.add(15.8, A.static_noise(1.8), 0.5)
    m.add(17.6, A.thump(50, 0.3), 0.7)
    m.add(18.55, A.nub(0.9), 0.6)
    m.add(18.55, A.regard(), 0.5)
    m.add(19.75, A.static_noise(0.25), 0.5)
