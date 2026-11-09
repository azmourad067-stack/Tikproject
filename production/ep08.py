"""ÉPISODE 08 — LESSIVE."""
import math
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_in, ease_out_back

SLUG = "ep08_lessive"
DUR = 18.0
COVER_T = 7.6
FLOOR = 1560
MX, MY = 540, 1560          # machine : centre bas
PX, PY, PR = 540, 1250, 205  # hublot
HINGE = PX - PR - 25
DINGS = [1.2, 6.6, 12.3]


@lru_cache(maxsize=1)
def bg():
    b = E.room_bg(E.MINT, (170, 190, 210), floor_y=FLOOR - 40, wall_pattern="tiles", seed=41)
    shelf = E.S(360, 30, [("rect", 0, 0, 360, 30, 8)], E.WOOD, seed=42)
    put(b, shelf, 820, 520)
    for i, col in enumerate(((120, 170, 240), (240, 150, 170), (250, 220, 110))):
        bt = E.S(80, 150, [("rect", 0, 30, 80, 150, 18), ("rect", 22, 0, 58, 40, 6)], col, seed=43 + i,
                 anchor="bottom")
        put(b, bt, 700 + i * 100, 508)
    put(b, E.duck(70), 980, 506)
    basket = E.S(300, 200, [("poly", [(0, 0), (300, 0), (260, 200), (40, 200)])], (215, 185, 140), seed=46,
                 anchor="bottom")
    put(b, basket, 140, FLOOR + 60)
    return b


@lru_cache(maxsize=1)
def machine_body():
    sp = E.S(660, 740, [("rect", 0, 0, 660, 740, 60)], (245, 243, 236), seed=47, anchor="bottom")
    d = ImageDraw.Draw(sp.img)
    p = 6
    d.rounded_rectangle([p + 20, p + 20, p + 640, p + 130], radius=26, fill=(215, 225, 230, 255))
    d.ellipse([p + 470, p + 40, p + 550, p + 120], fill=(200, 200, 210, 255), outline=(150, 150, 160, 255), width=5)
    d.line([(p + 510, p + 80), (p + 530, p + 55)], fill=(90, 90, 100, 255), width=6)
    for k in range(3):
        d.ellipse([p + 70 + k * 60, p + 60, p + 100 + k * 60, p + 90], fill=(120, 200, 160, 255) if k == 0 else (190, 195, 205, 255))
    cx, cy = p + 330, p + 740 - (MY - PY)
    d.ellipse([cx - PR - 30, cy - PR - 30, cx + PR + 30, cy + PR + 30], fill=(205, 208, 215, 255))
    d.ellipse([cx - PR, cy - PR, cx + PR, cy + PR], fill=(55, 60, 70, 255))
    return sp


@lru_cache(maxsize=1)
def label():
    sp = E.S(150, 190, [("rect", 0, 0, 150, 190, 10)], E.WHITE, seed=48, anchor="top")
    d = ImageDraw.Draw(sp.img)
    d.polygon([(30, 40), (120, 40), (110, 75), (40, 75)], outline=(60, 60, 70, 255), width=4)
    d.line([(45, 52), (105, 52)], fill=(90, 140, 230, 255), width=4)
    d.polygon([(75, 95), (110, 140), (40, 140)], outline=(60, 60, 70, 255), width=4)
    d.line([(35, 160), (115, 160)], fill=(60, 60, 70, 255), width=4)
    d.polygon([(45, 175), (105, 175), (95, 160), (60, 160)], outline=(60, 60, 70, 255), width=3)
    return sp


@lru_cache(maxsize=4)
def sock(i):
    col = [(120, 160, 230), (240, 120, 150), (130, 200, 140), (250, 210, 90)][i % 4]
    sp = E.S(80, 140, [("rect", 22, 0, 75, 100, 12), ("ellipse", 0, 72, 75, 136)], E.WHITE, seed=50 + i)
    d = ImageDraw.Draw(sp.img)
    for y in (16, 46, 76):
        d.rectangle([28, y, 80, y + 13], fill=col + (255,))
    return sp


@lru_cache(maxsize=1)
def drum_tex():
    im = Image.new("RGBA", (2 * PR, 2 * PR), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, 2 * PR, 2 * PR], fill=(70, 75, 88, 255))
    for r in range(40, PR, 45):
        for k in range(int(r / 12)):
            a = k / int(r / 12) * 6.283
            x, y = PR + math.cos(a) * r, PR + math.sin(a) * r
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(50, 54, 64, 255))
    return im


def drum(t, content, spin=True):
    """Intérieur du tambour avec contenu tournant."""
    im = drum_tex().rotate(-t * 300 if spin else 0, resample=Image.BICUBIC)
    rot = t * 360 if spin else 0
    if content == "nubo":
        for i in range(3):
            a = math.radians(rot + i * 120 + 60)
            put(im, sock(i), PR + math.cos(a) * 110, PR + math.sin(a) * 110, rot=-rot * 1.3 + i * 60)
        a = math.radians(rot)
        put(im, E.nubo(230, spiral=True, phase=t * 3), PR + math.cos(a) * 40, PR + 75 + math.sin(a) * 40,
            rot=-rot)
    elif content == "tiny":
        a = math.radians(rot)
        for i in range(3):
            aa = math.radians(rot + i * 120 + 60)
            put(im, sock(i), PR + math.cos(aa) * 110, PR + math.sin(aa) * 110, rot=-rot * 1.3 + i * 60)
        put(im, E.nubo(70, spiral=True, phase=t * 3), PR + math.cos(a) * 120, PR + 30 + math.sin(a) * 120, rot=-rot * 2)
    elif content == "big":
        put(im, E.nubo(500, fluffy=1.0, eyes=0.0), PR + math.sin(t * 9) * 20, PR + 330, rot=math.sin(t * 7) * 25)
    elif content == "sweater":
        put(im, sweater(1.0), PR, PR + 20, rot=-rot * 0.6 if spin else 0, scale=0.75)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * PR, 2 * PR], fill=255)
    im.putalpha(m)
    return im


@lru_cache(maxsize=12)
def sweater(o=1.0):
    w, h = 420, 360
    sp = E.S(w, h, [("rect", 80, 0, 340, 360, 30), ("poly", [(80, 10), (0, 170), (60, 210), (110, 120)]),
                    ("poly", [(340, 10), (420, 170), (360, 210), (310, 120)]), ("-ellipse", 160, -40, 260, 40)],
             (250, 140, 60), seed=55)
    d = ImageDraw.Draw(sp.img)
    p = 6
    for y in range(30, 350, 26):
        for x in range(95, 330, 26):
            d.line([(p + x, p + y), (p + x + 9, p + y + 12), (p + x + 18, p + y)], fill=(215, 110, 45, 255), width=3)
    for y in (300, 320):
        d.line([(p + 85, p + y), (p + 335, p + y)], fill=(200, 100, 40, 255), width=6)
    E._eye(sp.img, p + 175, p + 130, 26, o, (250, 140, 60))
    E._eye(sp.img, p + 245, p + 130, 26, o, (250, 140, 60))
    return sp


@lru_cache(maxsize=8)
def cat(step, dressed, o=1.0):
    img = Image.new("RGBA", (620, 460), (0, 0, 0, 0))
    grey = (165, 165, 175)
    tail = E.S(60, 260, [("rect", 0, 0, 60, 260, 30)], grey, seed=60, anchor=(30, 240))
    put(img, tail, 500, 250, rot=-35 + step * 10)
    for i, lx in enumerate((150, 220, 360, 430)):
        off = (step if i % 2 else -step) * 14
        leg = E.shape(56, 130, [("rect", 0, 0, 56, 130, 24)], E.darker(grey, 0.92), seed=61 + i)
        E.paste(img, leg, lx + int(off), 300)
    body = E.shape(400, 220, [("ellipse", 0, 0, 400, 220)], grey, seed=65)
    E.paste(img, body, 120, 130)
    if dressed:
        sw = sweater(o)
        sws = sw.img.resize((300, 260), Image.LANCZOS)
        E.paste(img, sws, 175, 115)
    head = E.shape(210, 190, [("ellipse", 0, 0, 210, 190), ("poly", [(10, 70), (30, -30), (90, 30)]),
                              ("poly", [(200, 70), (180, -30), (120, 30)])], grey, seed=66)
    E.paste(img, head, 20, 50)
    d = ImageDraw.Draw(img)
    for ex in (85, 155):
        d.arc([ex - 22, 120, ex + 22, 150], 200, 340, fill=(30, 30, 30, 255), width=6)
    d.polygon([(112, 165), (128, 165), (120, 177)], fill=(240, 140, 160, 255))
    for k in (-1, 1):
        d.line([(120, 175), (120 + k * 90, 165)], fill=(90, 90, 95, 255), width=3)
        d.line([(120, 180), (120 + k * 90, 190)], fill=(90, 90, 95, 255), width=3)
    return E.Sprite(img, (310, 435))


def door_open(t):
    o = 0.0
    for d0 in DINGS:
        if d0 + 0.3 <= t:
            o = ease_out(seg(t, d0 + 0.3, d0 + 0.7))
    if 4.6 <= t < 6.6:
        o = 1 - ease_in_out(seg(t, 4.6, 5.0))
    if 10.3 <= t < 12.3:
        o = 1 - ease_in_out(seg(t, 10.3, 10.7))
    return o


def content(t):
    if t < 2.0:
        return "nubo" if t < 1.5 else None
    if t < 4.6:
        return None
    if t < 6.9:
        return "tiny"
    if t < 10.4:
        return None
    if t < 12.7:
        return "big"
    if t < 12.9:
        return "sweater"
    return None


def scene(t):
    c = bg().copy()
    shake_y = 0
    shake_x = 0
    if 5.0 < t < 6.6 or (t < 1.3):
        shake_x = math.sin(t * 50) * 4
    if 10.7 < t < 12.3:
        shake_x = math.sin(t * 60) * 8
        shake_y = -abs(math.sin(t * 9)) * 40
    E.shadow(c, MX, MY, 640, 70)
    put(c, machine_body(), MX + shake_x, MY + shake_y, jid="mach", jamp=1.0, jrot=0.15)
    put(c, label(), MX + 380 + shake_x, 1010 + shake_y, rot=math.sin(t * 3) * 4)
    pcx, pcy = PX + shake_x, PY + shake_y
    o = door_open(t)
    ct = content(t)
    dimg = drum(t, ct, spin=o < 0.05)
    c.alpha_composite(dimg, (int(pcx - PR), int(pcy - PR)))
    # porte (anneau + vitre) pivotant sur la gauche
    sxd = max(0.05, 1 - o * 1.1)
    if sxd > 0.06:
        door_img = door_sprite()
        put(c, door_img, HINGE + shake_x, pcy, sx=sxd)
    else:
        put(c, door_sprite(), HINGE + shake_x - 30, pcy, sx=0.12, flip=True)
    # mini NUBO dehors
    if 1.9 <= t < 4.75:
        k1 = seg(t, 1.9, 2.4)
        if t < 2.4:
            x = E.lerp(pcx, 640, k1)
            y = E.lerp(pcy + 60, FLOOR + 150, k1) - math.sin(math.pi * k1) * 220
        elif t < 3.1:
            k = seg(t, 2.4, 3.1)
            x, y = E.lerp(640, 880, k), FLOOR + 150 - abs(math.sin(k * math.pi * 3)) * 50
        elif t < 4.1:
            x, y = 880, FLOOR + 150
        else:
            k = seg(t, 4.1, 4.6)
            x = E.lerp(880, pcx, k)
            y = E.lerp(FLOOR + 150, pcy + 40, k) - math.sin(math.pi * k) * 380
        look = (0.6, -1) if 3.1 <= t < 4.1 else (0.5, -0.3)
        tuft = "question" if 3.3 <= t < 4.1 else "curl"
        if t < 4.6 or k < 1:
            E.shadow(c, x, FLOOR + 150, 70)
            put(c, E.nubo(80, look=look, tuft=tuft), x, y, jid="tiny", jamp=1.0)
    # NUBO géant tout duveteux
    if 6.9 <= t < 10.4:
        k = ease_out_back(seg(t, 6.9, 7.3), 2.0)
        sc = max(0.05, 0.3 + 0.7 * k)
        if t > 9.0:
            kk = seg(t, 9.0, 10.3)
            sc = E.lerp(1.0, 0.18, ease_in(kk))
        sq = math.sin(t * 14) * 0.06 if t > 9.0 else 0
        look, oo = (0, 0), E.blink_at(t, [8.0])
        ycen = E.lerp(FLOOR + 380, pcy + 80, seg(t, 9.0, 10.3))
        put(c, E.nubo(900, fluffy=1.0, look=look, eyes=oo, tuft="up" if t < 7.6 else "curl"),
            pcx, ycen, scale=sc, sx=1 + sq, sy=1 - sq, jid="big", jamp=3)
    # pull qui sort, puis le chat
    if 12.9 <= t < 15.0:
        k = seg(t, 12.9, 13.5)
        x = E.lerp(pcx, 540, k)
        y = E.lerp(pcy, FLOOR + 200, ease_in(k))
        put(c, sweater(1.0), x, y, scale=E.lerp(0.75, 0.6, k), rot=(1 - k) * 30, jid="sw", jamp=1.2)
    if t >= 14.0:
        if t < 15.0:
            x = E.lerp(1350, 760, ease_out(seg(t, 14.0, 15.0)))
            step = math.sin(t * 12)
            dressed = False
        elif t < 15.6:
            x, step, dressed = 760, 0, t > 15.3
        else:
            x = E.lerp(760, 520, ease_in_out(seg(t, 15.6, 16.8)))
            step = math.sin(t * 10) if t < 16.8 else 0
            dressed = True
        o = 1.0
        if t > 16.8:
            o = E.regard_eyes(t, 16.7, (0, 0))[1]
        E.shadow(c, x, FLOOR + 290, 420, 60)
        put(c, cat(round(step * 2) / 2, dressed, round(o * 5) / 5), x, FLOOR + 290, jid="cat", jamp=1.5)
        if 15.0 <= t < 15.3:
            k = seg(t, 15.0, 15.3)
            put(c, sweater(1.0), E.lerp(540, x + 30, k), E.lerp(FLOOR + 200, FLOOR + 40, k) - math.sin(math.pi * k) * 160,
                scale=0.6)
    return c


@lru_cache(maxsize=1)
def door_sprite():
    R = PR + 30
    im = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0))
    ring = E.shape(2 * R, 2 * R, [("circle", R, R, R), ("-circle", R, R, PR - 10)], (190, 195, 205), seed=70)
    E.paste(im, ring, 14, 14)
    d = ImageDraw.Draw(im)
    c = R + 20
    glass = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glass)
    gd.ellipse([c - PR + 6, c - PR + 6, c + PR - 6, c + PR - 6], fill=(150, 200, 235, 70))
    gd.arc([c - PR * 0.8, c - PR * 0.8, c + PR * 0.8, c + PR * 0.8], 200, 250, fill=(255, 255, 255, 190), width=14)
    im.alpha_composite(glass)
    d.rounded_rectangle([c + R - 34, c - 50, c + R - 6, c + 50], radius=10, fill=(150, 155, 165, 255))
    return E.Sprite(im, (20, im.height / 2))


def frame(t):
    c = scene(t)
    if t < 1.0:
        return E.camera(c, 2.5, PX, PY)
    if t < 1.4:
        k = ease_out(seg(t, 1.0, 1.4))
        return E.camera(c, E.lerp(2.5, 1.15, k), E.lerp(PX, 540, k), E.lerp(PY, 1180, k))
    if 2.3 <= t < 4.7:
        k = ease_in_out(seg(t, 2.3, 2.8)) * (1 - ease_in_out(seg(t, 4.2, 4.7)))
        return E.camera(c, E.lerp(1.15, 1.8, k), E.lerp(540, 820, k), E.lerp(1180, 1450, k))
    if t >= 16.8:
        k = ease_out(seg(t, 16.8, 17.1))
        return E.camera(c, E.lerp(1.15, 2.3, k), E.lerp(540, 470, k), E.lerp(1180, 1560 + 40, k))
    return E.camera(c, 1.15, 540, 1180)


def sound(m):
    m.add(0.0, A.rumble(1.3, 1.8), 0.9)
    for k in range(4):
        m.add(0.1 + k * 0.3, A.thump(70, 0.2) * 0.4, 0.4)
    for d0 in DINGS:
        m.add(d0, A.ding(2637, 1.4) * 0.8, 0.6)
        m.add(d0 + 0.3, A.clack(), 0.6)
    # petite mélodie au mélodica
    m.seq(1.3, 140, [(0, "G5", 0.5), (0.5, "A5", 0.5), (1, "B5", 0.5), (1.5, "D6", 1),
                     (3, "C6", 0.5), (3.5, "B5", 0.5), (4, "A5", 1.5)], A.kazoo, 0.35)
    m.add(1.95, A.squeak(2.0, 0.14), 0.6)
    m.add(2.4, A.squeak(2.2, 0.08), 0.3)
    m.add(3.3, A.squeak(1.9, 0.18), 0.4)
    m.add(4.15, A.boing(400, 0.4), 0.5)
    m.add(4.7, A.thump(90, 0.2), 0.5)
    m.add(5.0, A.rumble(1.6, 2.4, 3), 0.9)
    m.add(6.9, A.pop(200, 90, 0.25) * 1.5, 0.8)
    m.add(7.0, A.squeak(0.45, 0.3), 0.8)
    m.add(7.0, A.boing(70, 0.8), 0.6)
    for k in range(6):
        m.add(9.0 + k * 0.22, A.squeak(0.5 + k * 0.08, 0.1) * 0.4, 0.4)
    m.add(10.3, A.schlurp(0.4), 0.6)
    m.add(10.7, A.rumble(1.6, 4.0, 5) * 1.3, 1.0)
    for k in range(8):
        m.add(10.75 + k * 0.2, A.thump(55, 0.25), 0.6)
    m.add(12.9, A.whoosh(0.5, 300, 2500, 6), 0.4)
    m.add(13.5, A.thump(110, 0.15) * 0.4, 0.3)
    for k in range(5):
        m.add(14.0 + k * 0.2, A.tick(k % 2 == 0) * 0.2, 0.2, 0.5)
    m.add(15.0, A.vowel(520, 700, 0.5, ((500, 1100), (1500, 2600))) * 0.6, 0.5)
    m.add(15.3, A.whoosh(0.3, 500, 3000, 8), 0.4)
    m.add(15.6, A.purr(2.4), 0.8)
    m.add(17.45, A.squeak(0.7, 0.2) * 0.6, 0.5)
    m.add(17.45, A.regard(), 0.5)
