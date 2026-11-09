"""ÉPISODE 02 — LE GRILLE-PAIN."""
import math
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

import audio as A
import engine as E
from engine import put, seg, ease_out, ease_in_out, ease_in, keys

SLUG = "ep02_grille_pain"
DUR = 20.0
COVER_T = 17.75
TOP = 1300            # plan de travail
TX, TY = 720, 1420    # grille-pain : centre bas
NX0 = 290             # position de NUBO
SLOT_Y = TY - 330


@lru_cache(maxsize=1)
def bg():
    b = E.room_bg(E.MINT, E.WOOD, floor_y=TOP, wall_pattern="tiles", seed=12)
    sh = E.S(300, 30, [("rect", 0, 0, 300, 30, 8)], E.WOOD, seed=3)
    put(b, sh, 200, 640)
    jar = E.S(80, 110, [("rect", 0, 0, 80, 110, 18)], E.PINK, seed=4)
    put(b, jar, 140, 570)
    put(b, E.duck(80), 250, 625)
    return b


@lru_cache(maxsize=1)
def toaster():
    w, h = 420, 330
    body = E.S(w, h, [("rect", 0, 0, w, h, 70)], E.PINK, seed=20, anchor="bottom")
    d = ImageDraw.Draw(body.img)
    p = 6
    for sx in (0.3, 0.7):
        cx = p + w * sx
        d.rounded_rectangle([cx - 70, p + 22, cx + 70, p + 46], radius=12, fill=(70, 40, 45, 255))
    d.ellipse([p + w / 2 - 34, p + h * 0.55 - 34, p + w / 2 + 34, p + h * 0.55 + 34], fill=(240, 240, 245, 255))
    d.line([p + w / 2, p + h * 0.55, p + w / 2 + 20, p + h * 0.55 - 22], fill=(80, 80, 90, 255), width=7)
    return body


@lru_cache(maxsize=1)
def lever():
    return E.S(70, 34, [("rect", 0, 0, 70, 34, 12)], (90, 90, 100), seed=21)


@lru_cache(maxsize=1)
def toast():
    w, h = 170, 180
    crust = E.S(w, h, [("ellipse", -6, 0, 176, 100), ("rect", 0, 45, 170, 180, 18)],
                (170, 105, 50), seed=30)
    inner = E.shape(w - 30, h - 30, [("ellipse", -5, 0, 145, 84), ("rect", 0, 38, 140, 150, 14)],
                    (240, 190, 110), seed=31)
    crust.img.alpha_composite(inner, (15, 15))
    return crust


@lru_cache(maxsize=1)
def bread():
    w, h = 170, 180
    crust = E.S(w, h, [("ellipse", -6, 0, 176, 100), ("rect", 0, 45, 170, 180, 18)],
                (200, 150, 90), seed=32)
    inner = E.shape(w - 30, h - 30, [("ellipse", -5, 0, 145, 84), ("rect", 0, 38, 140, 150, 14)],
                    (252, 238, 205), seed=33)
    crust.img.alpha_composite(inner, (15, 15))
    return crust


@lru_cache(maxsize=1)
def pancake():
    sp = E.S(300, 90, [("ellipse", 0, 0, 300, 90)], (225, 165, 80), seed=34)
    d = ImageDraw.Draw(sp.img)
    for x, y in ((80, 40), (150, 30), (210, 52), (120, 60)):
        d.ellipse([x, y, x + 18, y + 10], fill=(180, 115, 50, 255))
    return sp


@lru_cache(maxsize=1)
def sock():
    sp = E.S(110, 180, [("rect", 30, 0, 100, 130, 14), ("ellipse", 0, 95, 100, 175)], E.WHITE, seed=35)
    d = ImageDraw.Draw(sp.img)
    for y in (20, 55, 90):
        d.rectangle([36, y, 106, y + 16], fill=(120, 160, 230, 255))
    return sp


def pigeon(flap=0.0, look=1):
    return _pigeon(round(flap * 4) / 4)


@lru_cache(maxsize=16)
def _pigeon(flap):
    w, h = 240, 200
    img = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    body = E.shape(170, 110, [("ellipse", 0, 0, 170, 110)], (150, 150, 165), seed=40)
    tail = E.shape(80, 50, [("poly", [(0, 0), (80, 20), (80, 40), (0, 50)])], (120, 120, 135), seed=41)
    head = E.shape(80, 80, [("circle", 40, 40, 40)], (130, 130, 150), seed=42)
    E.paste(img, tail, 0, 100)
    E.paste(img, body, 40, 70)
    E.paste(img, head, 170, 30)
    d = ImageDraw.Draw(img)
    d.polygon([(250, 70), (285, 80), (250, 88)], fill=(240, 170, 80, 255))
    d.ellipse([222, 56, 238, 72], fill=(20, 20, 20, 255))
    d.ellipse([225, 58, 231, 64], fill=(255, 255, 255, 255))
    d.arc([175, 85, 245, 125], 200, 340, fill=(120, 190, 160, 255), width=8)
    wing = E.S(130, 60, [("ellipse", 0, 0, 130, 60)], (115, 115, 132), seed=43, anchor=(110, 30))
    ang = -60 * math.sin(flap * math.pi * 2) + 10
    put(img, wing, 150, 105, rot=ang)
    return E.Sprite(img, (img.width / 2, img.height - 30))


def toaster_layer(c, t, shake=0.0, lever_down=False, glow_k=0.0):
    jx = math.sin(t * 60) * shake * 6
    put(c, toaster(), TX + jx, TY, jid="toaster", jamp=1.0, jrot=0.2)
    ly = TY - 230 + (110 if lever_down else 0)
    put(c, lever(), TX + 232 + jx, ly)
    if glow_k > 0:
        for sx in (-0.2, 0.2):
            E.glow(c, TX + sx * 420 + jx, SLOT_Y + 30, 70, (255, 140, 40), 0.6 * glow_k)


def lever_state(t):
    return (3.0 <= t < 3.6) or (6.8 <= t < 7.4) or (12.4 <= t < 17.0)


def nubo_main(t):
    """(x, y, rot, sx, sy, sprite_kwargs, devant_le_grillepain)."""
    kw = dict(h=380, look=(0, 0), tuft="curl", arms=(18, 18))
    x, y, rot, sx, sy = NX0, TOP + 120, 0, 1, 1
    front = True
    if t < 1.6:
        kw["arms"] = (150, 150)
        kw["look"] = (0, -1)
        kw["phase"] = t * 4
    elif t < 3.0:
        kw["arms"] = (30, 120) if t > 2.2 else (18, 18)
        kw["look"] = (1, -0.5)
    elif t < 6.0:
        lk = keys(t, [(3.6, (1, -1)), (4.3, (0.3, -1)), (5.4, (-1, -0.2))])
        kw["look"] = lk
        if t > 3.8:
            kw["tuft"] = "question"
    elif t < 9.0:
        kw["arms"] = (30, 120) if t < 6.8 else (18, 18)
        kw["look"] = (1, -0.4) if t < 7.4 else keys(t, [(7.4, (1, -1)), (8.6, (0.6, -1))])
        if t > 7.4:
            kw["tuft"] = "up"
            kw["scared"] = True
    elif t < 11.8:
        k = ease_in_out(seg(t, 9.0, 9.6))
        x = E.lerp(NX0, TX, k)
        y = E.lerp(TOP + 120, SLOT_Y + 40, k) - math.sin(math.pi * k) * 260
        kw["look"] = (0.3, 1)
        if t > 9.8:
            rot = -14 * ease_in_out(seg(t, 9.8, 10.3))
            kw["tuft"] = "down"
            sy = 1 + 0.04 * math.sin(t * 25) * seg(t, 10.5, 11.8)
    elif t < 17.0:
        k = ease_in(seg(t, 11.8, 12.35))
        x = TX
        y = E.lerp(SLOT_Y + 40, SLOT_Y + 560, k)
        sx, sy = E.lerp(1, 0.42, min(1, k * 3)), E.lerp(1, 1.5, min(1, k * 3))
        kw["eyes"] = 0.0 if k > 0.2 else 1.0
        kw["tuft"] = "up"
        front = False
        if t > 12.4:
            return None
    else:
        kw.update(toasted=True, tuft="smoke", phase=t * 2)
        k = seg(t, 17.0, 17.9)
        if k < 1:
            x = E.lerp(TX, 540, k)
            y = E.lerp(SLOT_Y + 200, TOP + 430, k) - math.sin(math.pi * k) * 900
            rot = 360 * ease_out(k)
            kw["eyes"] = 0.0
            front = True
            if k < 0.25:
                front = False
        else:
            x, y = 540, TOP + 430
            kw["h"] = 460
            b = seg(t, 17.9, 18.2)
            sx, sy = 1 + 0.2 * math.sin(math.pi * b), 1 - 0.2 * math.sin(math.pi * b)
            look, o = E.regard_eyes(t, 18.4, (0.6, -0.3))
            kw["look"], kw["eyes"] = look, o
            if t < 18.4:
                kw["look"] = (0.6, -0.3)
        if k < 1:
            kw["h"] = 420
    return x, y, rot, sx, sy, kw, front


def scene(t):
    c = bg().copy()
    # pigeon & pancake qui reviennent attendre
    side = []
    if 13.0 < t:
        k = ease_out(seg(t, 13.0, 13.8))
        side.append(("pigeon", E.lerp(-200, 170, k), E.lerp(800, TOP + 160, k), seg(t, 13.0, 13.8) < 1))
    if 13.6 < t:
        k = ease_out(seg(t, 13.6, 14.4))
        side.append(("pancake", E.lerp(1300, 990, k), E.lerp(700, TOP + 200, k), k < 1))
    # vieux toast posé sur le plan de travail
    if 1.9 < t:
        k = seg(t, 1.6, 2.0)
        put(c, toast(), E.lerp(NX0, 90, k), E.lerp(TOP - 100, TOP + 210, k) - math.sin(math.pi * k) * 200,
            scale=0.7, rot=E.lerp(0, -380, k) if k < 1 else -20, jid="oldtoast")
    nm = nubo_main(t)
    lever_down = lever_state(t)
    shake = seg(t, 13.0, 16.9) if 12.4 < t < 17.0 else 0
    glow_k = seg(t, 12.6, 16.5) if 12.4 < t < 17.1 else 0
    behind = nm is not None and not nm[6]
    if behind:
        x, y, rot, sx, sy, kw, _ = nm
        put(c, E.nubo(**kw), x, y, rot=rot, sx=sx, sy=sy, jid="n")
    E.shadow(c, TX, TY, 470, 60)
    # pain / chaussette qui descend dans la fente
    for t0, t1, sp in ((2.2, 3.0, bread()), (6.0, 6.8, sock())):
        if t0 < t < t1 + 0.1:
            k = seg(t, t0, t1)
            px = E.lerp(NX0 + 120, TX - 84, ease_in_out(min(1, k * 1.6)))
            py = E.lerp(TOP - 80, SLOT_Y - 120, ease_in_out(min(1, k * 1.6))) + max(0, k - 0.62) * 400
            put(c, sp, px, py, scale=0.75, jid="item")
    # objets qui jaillissent
    if 3.6 <= t < 6.0:
        k = seg(t, 3.6, 4.0)
        y = SLOT_Y - 40 - ease_out(k) * 420
        g = seg(t, 4.0, 5.8)
        x = E.lerp(TX - 84, -250, ease_in_out(g))
        y += math.sin(g * 9) * 40 + g * 150
        put(c, pancake(), x, y, rot=math.sin(t * 7) * 14, sy=0.8 + 0.2 * math.sin(t * 9), jid="pc")
    if 7.4 <= t < 9.0:
        k = seg(t, 7.4, 8.9)
        x = E.lerp(TX - 84, 1250, ease_in(k))
        y = E.lerp(SLOT_Y - 30, -200, ease_out(k))
        put(c, pigeon(t * 3 % 1), x, y, rot=-15, jid="pg")
    toaster_layer(c, t, shake, lever_down, glow_k)
    for name, x, y, moving in side:
        if name == "pigeon":
            put(c, pigeon((t * 3 % 1) if moving else 0.25), x, y, jid="pg2")
        else:
            put(c, pancake(), x, y, jid="pc2")
    if nm is not None and nm[6]:
        x, y, rot, sx, sy, kw, _ = nm
        if t < 9 or t >= 17.9:
            E.shadow(c, x, y, kw["h"] * 0.9)
        put(c, E.nubo(**kw), x, y, rot=rot, sx=sx, sy=sy, jid="n")
        if t < 1.6:
            put(c, toast(), x, y - kw["h"] * 1.25, scale=0.8, jid="held")
    # miettes en fin d'épisode
    if 18.0 < t < 19.4:
        k = seg(t, 18.6, 19.4)
        E.particles(c, [(765, TOP + 250 + k * 170, 7, (170, 105, 50), 1)])
    # toast final qui part vers la caméra (raccord de boucle)
    if t >= 19.55:
        k = seg(t, 19.55, 20.0)
        put(c, toast(), E.lerp(TX - 84, 540, k), E.lerp(SLOT_Y - 60, 900, k), scale=E.lerp(0.4, 0.55, k),
            rot=k * 120)
    return c


ZOOM = (1.32, 560, 1180)


def frame(t):
    if t < 1.0:
        # ralenti : le toast fonce vers la caméra
        base = E.camera(scene(1.0), *ZOOM)
        base = base.filter(ImageFilter.GaussianBlur(6))
        k = t / 1.0
        sc = 0.55 * (7.5 / 0.55) ** k
        put(base, toast(), 540, 900 + k * 100, scale=sc, rot=120 + k * 200)
        crumbs = [(540 + math.cos(i * 2.1) * (60 + i * 25) * (0.5 + 2 * k),
                   900 + math.sin(i * 1.7) * (60 + i * 22) * (0.5 + 2 * k), 4 + 8 * k, (170, 105, 50), 1)
                  for i in range(18)]
        E.particles(base, crumbs)
        return base
    return E.camera(scene(t), *ZOOM)


def sound(m):
    # ritournelle ukulélé (1 → 9 s)
    prog = [["C4", "E4", "G4"], ["A3", "C4", "E4"], ["F3", "A3", "C4"], ["G3", "B3", "D4"]]
    beat = 60 / 132
    tt, i = 1.0, 0
    while tt < 8.9:
        ch = prog[(i // 4) % 4]
        for k, nn in enumerate(ch):
            m.add(tt + k * 0.012, A.ukulele(A.NOTE(nn), 0.5), 0.22)
        if i % 2 == 0:
            m.add(tt, A.bass(A.NOTE(ch[0]) / 2, 0.4), 0.3)
        tt += beat
        i += 1
    # slow motion d'ouverture
    m.add(0.0, A.whoosh(1.0, 150, 1500), 0.8)
    m.add(0.95, A.pop(400, 120, 0.1), 0.6)
    m.add(1.0, A.nub(1.1), 0.5)
    m.add(1.65, A.whoosh(0.3, 600, 3000, 4), 0.4)
    m.add(2.05, A.thump(90, 0.2), 0.4)
    for t0 in (3.0, 6.8, 12.4):
        m.add(t0, A.clack(), 0.8)
    for k in range(3):
        m.add(3.05 + k * 0.2, A.tick(k % 2 == 0), 0.4)
        m.add(6.85 + k * 0.2, A.tick(k % 2 == 0), 0.4)
    m.add(3.6, A.ding(2400), 0.8)
    m.add(3.65, A.boing(220, 0.5), 0.6)
    m.add(4.0, A.whoosh(1.8, 300, 2000, 7), 0.45, -0.5)
    m.add(4.2, A.squeak(0.8, 0.25), 0.4)
    m.add(7.4, A.ding(2400), 0.8)
    m.add(7.45, A.flap(1.2), 0.7, 0.4)
    m.add(7.6, A.coo(), 0.7, 0.5)
    m.add(7.55, A.nub(1.4), 0.5)
    m.add(9.0, A.boing(160, 0.5), 0.5)
    m.add(9.7, A.wind(2.2, 0.6), 0.6)
    m.add(11.8, A.schlurp(0.6), 1.0)
    m.add(12.0, A.nub(1.6), 0.4)
    m.add(12.4, A.clack(), 0.8)
    for k in range(int((17.0 - 12.6) / 0.45)):
        m.add(12.6 + k * 0.45, A.tick(k % 2 == 0), 0.45)
    m.add(12.6, A.heat_hiss(4.4), 0.8)
    m.add(13.0, A.flap(0.8), 0.4, -0.6)
    m.add(13.5, A.coo(), 0.4, -0.6)
    m.add(13.6, A.whoosh(0.8, 300, 2000, 9), 0.3, 0.6)
    m.add(17.0, A.ding(2100, 2.0, 1.4), 1.0)
    m.add(17.0, A.ding(1050, 2.0, 1.0), 0.6)
    m.add(17.05, A.whoosh(0.8, 200, 3000, 11), 0.5)
    m.add(17.9, A.thump(70, 0.4), 0.9)
    m.seq(17.95, 150, [(0, "C5", 0.5), (0.5, "E5", 0.5), (1, "G5", 0.5), (1.5, ["C6", "G5", "E5"], 2.5)],
          A.brass, 0.6)
    m.add(18.15, A.squeak(0.75, 0.2), 0.5)
    m.add(19.15, A.regard(), 0.6)
    m.add(19.15, A.nub(0.8), 0.5)
    m.add(19.55, A.ding(2400), 0.5)
    m.add(19.6, A.whoosh(0.5, 150, 1500), 0.6)
