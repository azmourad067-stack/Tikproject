"""NUBO — synthétiseur de bruitages et de musiques (100 % original, aucun droit tiers)."""
import math
import wave

import numpy as np

SR = 44100


def T(d):
    return np.arange(int(d * SR)) / SR


def noise(d, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, int(d * SR))


def bandpass(x, lo=None, hi=None, soft=0.15):
    n = len(x)
    if n == 0:
        return x
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi:
        g *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, n)


def phase(freq, n):
    if np.isscalar(freq):
        freq = np.full(n, float(freq))
    return 2 * np.pi * np.cumsum(freq) / SR


def osc(freq, d, kind="sine"):
    n = int(d * SR)
    ph = phase(freq, n)
    if kind == "sine":
        return np.sin(ph)
    if kind == "saw":
        return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if kind == "square":
        return np.sign(np.sin(ph))
    if kind == "tri":
        return 2 * np.abs(2 * ((ph / (2 * np.pi)) % 1) - 1) - 1
    raise ValueError(kind)


def glide(f0, f1, d, curve="exp"):
    n = int(d * SR)
    u = np.linspace(0, 1, n)
    if curve == "exp":
        return f0 * (f1 / f0) ** u
    return f0 + (f1 - f0) * u


def env(n, a=0.005, r=0.05, d=None):
    """Enveloppe attaque / relâchement linéaires (n échantillons)."""
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na > 0:
        e[:na] = np.linspace(0, 1, min(na, n))[:min(na, n)]
    if nr > 0 and nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def decay(n, tau):
    return np.exp(-np.arange(n) / SR / tau)


def NOTE(name):
    names = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
             "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    p, o = name[:-1], int(name[-1])
    m = names[p] + 12 * (o + 1)
    return 440.0 * 2 ** ((m - 69) / 12)


# --------------------------------------------------------------------------
# Signature NUBO
# --------------------------------------------------------------------------
def squeak(p=1.0, d=0.2):
    """Le « nüb! » : couinement de jouet en caoutchouc."""
    n = int(d * SR)
    t = np.arange(n) / SR
    a = int(0.045 * SR)
    f = np.concatenate([glide(950 * p, 1650 * p, 0.045), glide(1650 * p, 1150 * p, d - 0.045)])[:n]
    if len(f) < n:
        f = np.pad(f, (0, n - len(f)), mode="edge")
    ph = phase(f, n)
    s = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.18 * np.sin(3 * ph)
    s *= 1 + 0.3 * np.sin(2 * np.pi * 34 * t)
    e = np.minimum(1, t / 0.008) * np.clip((d - t) / 0.06, 0, 1)
    air = bandpass(noise(d, 3), 2500, 7000) * 0.25
    return (s * 0.6 + air) * e


def nub(p=1.0):
    return squeak(p, 0.19)


def kalimba(f, d=1.3):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2)
    s += 0.35 * np.sin(2 * np.pi * f * 5.43 * t) * np.exp(-t * 28)
    s += 0.15 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 6)
    s[:60] *= np.linspace(0, 1, 60)
    return s * 0.7


def regard():
    """Le « ting-ting » du REGARD."""
    out = np.zeros(int(1.8 * SR))
    a = kalimba(NOTE("E6"))
    b = kalimba(NOTE("B6"))
    out[:len(a)] += a
    o = int(0.2 * SR)
    out[o:o + len(b)] += b[:len(out) - o]
    return out * 0.8


# --------------------------------------------------------------------------
# Bruitages
# --------------------------------------------------------------------------
def ding(f=2093, d=1.6, bright=1.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for ratio, amp, tau in ((1, 1, 0.9), (2.0, 0.35, 0.5), (2.76, 0.5 * bright, 0.35),
                            (5.4, 0.25 * bright, 0.15), (8.93, 0.1 * bright, 0.08)):
        s += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    s[:40] *= np.linspace(0, 1, 40)
    return s * 0.45


def pop(f0=700, f1=160, d=0.09):
    n = int(d * SR)
    s = np.sin(phase(glide(f0, f1, d), n)) * decay(n, d / 3)
    return s * 0.8


def plop(p=1.0):
    return pop(500 * p, 120 * p, 0.12) + 0.2 * bandpass(noise(0.12, 9), 500, 3000) * decay(int(0.12 * SR), 0.02)


def boing(f=170, d=0.7):
    n = int(d * SR)
    t = np.arange(n) / SR
    fr = f * (1 + 0.55 * np.sin(2 * np.pi * 11 * t) * np.exp(-4 * t)) * (1 + 0.6 * t)
    ph = phase(fr, n)
    s = (0.7 * np.sin(ph) + 0.3 * np.sign(np.sin(ph)) * 0.4) * np.exp(-t * 3.5)
    return s * 0.8


def whoosh(d=0.6, lo=250, hi=3500, seed=1):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bandpass(noise(d, seed), lo, hi)
    e = np.sin(np.pi * t / d) ** 2
    return x * e * 1.6


def thump(f=60, d=0.45):
    n = int(d * SR)
    s = np.sin(phase(glide(f * 2.5, f, d), n)) * decay(n, 0.12)
    s[:200] += bandpass(noise(200 / SR, 4), 100, 2000) * 0.5
    return s


def crash(d=1.2, seed=2):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bandpass(noise(d, seed), 80, 6000) * np.exp(-t * 4)
    x += thump(45, d) * 1.2
    return x * 0.8


def piano_crash(d=2.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    rng = np.random.default_rng(1)
    for f in [NOTE(x) for x in ("C2", "F#2", "C3", "D#3", "A3", "C#4", "G4", "B4")]:
        f2 = f * rng.uniform(0.98, 1.03)
        s += (osc(f2, d, "saw") * 0.3 + np.sin(2 * np.pi * f2 * t)) * np.exp(-t * rng.uniform(1.5, 3))
    s = bandpass(s, 60, 4000) * 0.18
    return s + crash(d) * 0.9


def click(d=0.012, lo=1500, seed=5):
    n = int(d * SR)
    return bandpass(noise(d, seed), lo, 12000) * decay(n, d / 4)


def clack():
    c = click(0.02, 800)
    t = np.arange(len(c)) / SR
    return c + 0.4 * np.sin(2 * np.pi * 1700 * t) * decay(len(c), 0.005)


def tick(high=True):
    c = click(0.015, 2500 if high else 900, seed=7 if high else 8)
    t = np.arange(len(c)) / SR
    return c * 0.8 + 0.5 * np.sin(2 * np.pi * (3200 if high else 1900) * t) * decay(len(c), 0.004)


def spray(d=0.35):
    n = int(d * SR)
    t = np.arange(n) / SR
    return bandpass(noise(d, 11), 3500, 11000) * np.minimum(1, t / 0.01) * np.exp(-t * 6) * 1.4


def crunch(d=0.55, seed=3):
    n = int(d * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(seed)
    for _ in range(int(d * 55)):
        p = rng.integers(0, n - 800)
        g = bandpass(noise(0.012, int(rng.integers(0, 999))), 700, 6000)
        g *= decay(len(g), 0.003) * rng.uniform(0.3, 1)
        out[p:p + len(g)] += g
    return out * 1.2


def schlurp(d=0.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = glide(160, 900, d) * (1 + 0.15 * np.sin(2 * np.pi * 18 * t))
    s = np.sin(phase(f, n)) * 0.5 + bandpass(noise(d, 21), 300, 2500) * 0.5
    return s * np.sin(np.pi * t / d) ** 0.5


def coin():
    a = ding(3600, 0.6, 0.6) * 0.8
    b = ding(4300, 0.4, 0.3) * 0.4
    a[:len(b)] += b
    return a


def static_noise(d, seed=6):
    x = noise(d, seed) * 0.5
    rng = np.random.default_rng(seed)
    for p in rng.integers(0, len(x) - 100, int(d * 40)):
        x[p:p + 60] += rng.uniform(-1, 1)
    return x * 0.6


def hum(d, f=60):
    t = T(d)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t) + 0.25 * np.sin(2 * np.pi * 3 * f * t)
    return (s + 0.1 * bandpass(noise(d, 2), 50, 400)) * 0.15


def rumble(d, rate=1.6, seed=4):
    t = T(d)
    x = bandpass(noise(d, seed), 30, 260)
    x *= 0.55 + 0.45 * np.sin(2 * np.pi * rate * t)
    return x * 2.2


def purr(d):
    t = T(d)
    x = bandpass(noise(d, 31), 40, 350)
    return x * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t)) ** 2 * 3.0


def wind(d, strength=1.0, seed=8):
    t = T(d)
    x = bandpass(noise(d, seed), 120, 1400)
    m = 0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t + 1) * np.sin(2 * np.pi * 0.31 * t)
    return x * m * strength * 2.0


def birds(d, seed=12):
    n = int(d * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(seed)
    t0 = 0.1
    while t0 < d - 0.4:
        base = rng.uniform(2800, 4200)
        for k in range(rng.integers(2, 4)):
            c = np.sin(phase(glide(base, base * 1.35, 0.045), int(0.045 * SR)))
            c *= np.sin(np.pi * np.linspace(0, 1, len(c)))
            p = int((t0 + k * 0.07) * SR)
            if p + len(c) < n:
                out[p:p + len(c)] += c * 0.25
        t0 += rng.uniform(0.5, 1.4)
    return out


def shutter():
    out = np.zeros(int(0.15 * SR))
    a, b = click(0.02, 1200, 1), click(0.03, 600, 2)
    out[:len(a)] += a
    p = int(0.06 * SR)
    out[p:p + len(b)] += b
    return out * 1.3


def vowel(f0, f1, d, formants=((750, 1150), (1100, 1600), (2400, 3000)), seed=0):
    n = int(d * SR)
    s = osc(glide(f0, f1, d), d, "saw")
    out = np.zeros(n)
    for lo, hi in formants:
        out += bandpass(s, lo, hi)
    out += 0.15 * bandpass(noise(d, seed), 800, 5000)
    return out


def sneeze_ah(p=1.0, d=0.5):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = vowel(240 * p, 330 * p, d)
    return s * (t / d) ** 1.5 * np.clip((d - t) / 0.04, 0, 1) * 0.9


def sneeze_choo(p=1.0):
    d = 0.38
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bandpass(noise(d, 14), 1800, 8000) * np.exp(-t * 9) * 1.6
    x += vowel(300 * p, 200 * p, d, ((300, 700), (700, 1000))) * np.exp(-t * 6) * 0.6
    return x


def gong(d=3.5, f=82):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for ratio, amp, tau in ((1, 1, 2.0), (1.41, 0.6, 1.5), (1.73, 0.5, 1.2), (2.31, 0.45, 0.9),
                            (2.82, 0.35, 0.7), (3.61, 0.25, 0.5), (4.9, 0.15, 0.35)):
        s += amp * np.sin(2 * np.pi * f * ratio * t * (1 + 0.002 * np.sin(2 * np.pi * 0.7 * t))) * np.exp(-t / tau)
    s *= np.minimum(1, t / 0.01)
    return s * 0.5


def crowd(d, seed=5):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = bandpass(noise(d, seed), 300, 3000) * 1.4
    rng = np.random.default_rng(seed)
    for _ in range(int(d * 14)):
        st = rng.uniform(0, max(0.01, d - 0.5))
        dd = rng.uniform(0.25, 0.6)
        f0 = rng.uniform(250, 600)
        v = vowel(f0, f0 * rng.uniform(1.2, 1.7), dd, seed=int(rng.integers(0, 99)))
        v *= np.sin(np.pi * np.linspace(0, 1, len(v)))
        p = int(st * SR)
        out_len = min(len(v), n - p)
        x[p:p + out_len] += v[:out_len] * 0.35
    e = np.minimum(1, t / 0.3) * np.clip((d - t) / 0.6, 0, 1)
    return x * e


def firework(seed=1):
    d = 1.6
    n = int(d * SR)
    out = np.zeros(n)
    w = np.sin(phase(glide(900, 2200, 0.5), int(0.5 * SR))) * 0.15
    out[:len(w)] += w * np.linspace(0.3, 1, len(w))
    b = thump(70, 0.6) * 0.8
    p = int(0.5 * SR)
    out[p:p + len(b)] += b
    rng = np.random.default_rng(seed)
    for _ in range(60):
        q = p + int(rng.uniform(0.05, 1.0) * SR)
        c = click(0.01, 2000, int(rng.integers(0, 99))) * rng.uniform(0.2, 0.7)
        if q + len(c) < n:
            out[q:q + len(c)] += c
    return out


def horror_screech(d=0.6):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 1900 * (1 + 0.02 * np.sin(2 * np.pi * 7 * t))
    s = bandpass(osc(f, d, "saw"), 1200, 7000) * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * t))
    s += bandpass(osc(f * 1.06, d, "saw"), 1200, 7000) * 0.6
    return s * np.minimum(1, t / 0.02) * np.clip((d - t) / 0.1, 0, 1) * 0.5


def drone(d, f=55, seed=0):
    t = T(d)
    s = osc(f, d, "saw") + osc(f * 1.498, d, "saw") * 0.7 + osc(f * 1.01, d, "saw")
    s = bandpass(s, 30, 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t))
    return s * np.minimum(1, t / 1.0) * 0.4


def heat_hiss(d):
    t = T(d)
    return bandpass(noise(d, 77), 3000, 9000) * 0.15 * np.minimum(1, t / 0.5)


def tsss(d=0.9):
    t = T(d)
    return bandpass(noise(d, 66), 3000, 10000) * np.exp(-t * 3) * 0.9


def scrape(d=1.2):
    t = T(d)
    return bandpass(noise(d, 55), 400, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * 0.6


def coo():
    d = 0.7
    t = T(d)
    f = 520 * (1 + 0.15 * np.sin(2 * np.pi * 3 * t))
    s = bandpass(osc(f, d, "tri"), 200, 1500) * np.sin(np.pi * t / d) ** 2
    return s * 0.7


def flap(d=0.6):
    n = int(d * SR)
    out = np.zeros(n)
    for k in range(int(d / 0.09)):
        w = bandpass(noise(0.05, k), 300, 3000) * decay(int(0.05 * SR), 0.015)
        p = int(k * 0.09 * SR)
        out[p:p + len(w)] += w
    return out * 0.9


def bubbles(d, seed=4):
    n = int(d * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(seed)
    for _ in range(int(d * 18)):
        p = int(rng.uniform(0, d - 0.1) * SR)
        b = pop(rng.uniform(400, 1400), rng.uniform(900, 2400), 0.05) * 0.25
        out[p:p + len(b)] += b
    return out


# --------------------------------------------------------------------------
# Instruments
# --------------------------------------------------------------------------
def karplus(f, d, damp=0.996, bright=0.5, seed=0):
    n = int(d * SR)
    N = max(2, int(SR / f))
    rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, N)
    if bright < 1:
        buf = np.convolve(buf, np.ones(3) / 3, mode="same")
    out = np.zeros(n)
    blocks = n // N + 1
    prev = buf
    pos = 0
    for _ in range(blocks):
        L = min(N, n - pos)
        if L <= 0:
            break
        out[pos:pos + L] = prev[:L]
        nxt = damp * 0.5 * (prev + np.roll(prev, 1))
        prev = nxt
        pos += L
    return out * 0.6


def pizz(f, d=0.45):
    return karplus(f, d, 0.985) * 1.2


def ukulele(f, d=0.8):
    return karplus(f, d, 0.993, seed=int(f)) * 0.9


def epiano(f, d=1.2):
    t = T(d)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) + 0.08 * np.sin(2 * np.pi * 7 * f * t) * np.exp(-t * 20)
    return s * np.exp(-t * 1.8) * (1 + 0.1 * np.sin(2 * np.pi * 4.5 * t)) * 0.35


def music_box(f, d=1.2):
    t = T(d)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 4.2 * f * t) * np.exp(-t * 10)
    s *= np.exp(-t * 2.2)
    s[:30] *= np.linspace(0, 1, 30)
    return s * 0.35


def whistle(f, d):
    t = T(d)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.15)
    s = np.sin(phase(f * vib, len(t))) + 0.05 * bandpass(noise(d, 2), 1000, 6000)
    return s * np.minimum(1, t / 0.03) * np.clip((d - t) / 0.06, 0, 1) * 0.4


def kazoo(f, d, seed=0):
    t = T(d)
    vib = 1 + 0.015 * np.sin(2 * np.pi * 6 * t)
    s = osc(f * vib, d, "saw")
    s = s * (1 + 0.35 * bandpass(noise(d, seed), 50, 400))
    s = bandpass(s, 250, 3500)
    return s * np.minimum(1, t / 0.02) * np.clip((d - t) / 0.04, 0, 1) * 0.35


def brass(f, d):
    t = T(d)
    s = bandpass(osc(f, d, "saw") + 0.5 * osc(f * 1.003, d, "saw"), 100, 2500)
    return s * np.minimum(1, t / 0.04) * np.clip((d - t) / 0.08, 0, 1) * 0.35


def bass(f, d):
    t = T(d)
    s = np.sin(2 * np.pi * f * t) + 0.3 * bandpass(osc(f, d, "saw"), 20, 600)
    return s * np.minimum(1, t / 0.01) * np.exp(-t * 2.5) * 0.6


def kick():
    d = 0.3
    n = int(d * SR)
    s = np.sin(phase(glide(140, 45, 0.12).tolist() + [45] * (n - int(0.12 * SR)), n))
    return s * decay(n, 0.09) * 1.0


def hat(d=0.05):
    return bandpass(noise(d, 3), 7000, 16000) * decay(int(d * SR), 0.015) * 0.6


def shaker():
    d = 0.08
    t = T(d)
    return bandpass(noise(d, 9), 5000, 12000) * np.sin(np.pi * t / d) * 0.3


def snare():
    d = 0.18
    t = T(d)
    return (bandpass(noise(d, 1), 1200, 7000) * 0.8 + 0.4 * np.sin(2 * np.pi * 190 * t)) * np.exp(-t * 18)


def choir(freqs, d):
    t = T(d)
    out = np.zeros(len(t))
    for i, f in enumerate(freqs):
        for det in (0.996, 1.0, 1.004):
            out += vowel(f * det, f * det, d, seed=i)[:len(t)] * 0.12
    return out * np.minimum(1, t / 0.6) * np.clip((d - t) / 0.5, 0, 1)


# --------------------------------------------------------------------------
# Mixage
# --------------------------------------------------------------------------
class Mix:
    def __init__(self, dur):
        self.dur = dur
        self.n = int(dur * SR)
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)

    def add(self, t, snd, gain=1.0, pan=0.0):
        if snd is None or len(snd) == 0:
            return
        p = int(t * SR)
        if p >= self.n:
            return
        if p < 0:
            snd = snd[-p:]
            p = 0
        pan = max(-1.0, min(1.0, pan))
        L = min(len(snd), self.n - p)
        gl = gain * math.sqrt(0.5 * (1 - pan))
        gr = gain * math.sqrt(0.5 * (1 + pan))
        self.L[p:p + L] += snd[:L] * gl
        self.R[p:p + L] += snd[:L] * gr

    def seq(self, t0, bpm, notes, inst, gain=1.0, pan=0.0):
        """notes = [(temps_en_beats, freq|nom|liste, durée_en_beats)]."""
        beat = 60 / bpm
        for b, f, dur in notes:
            fs = f if isinstance(f, (list, tuple)) else [f]
            for ff in fs:
                if ff is None:
                    continue
                fr = NOTE(ff) if isinstance(ff, str) else ff
                self.add(t0 + b * beat, inst(fr, dur * beat), gain, pan)

    def write(self, path, fade_tail=0.0):
        L, R = self.L.copy(), self.R.copy()
        peak = max(np.abs(L).max(), np.abs(R).max(), 1e-6)
        k = 0.95 / peak
        L, R = np.tanh(L * k * 1.15) * 0.92, np.tanh(R * k * 1.15) * 0.92
        if fade_tail > 0:
            nf = int(fade_tail * SR)
            L[-nf:] *= np.linspace(1, 0, nf)
            R[-nf:] *= np.linspace(1, 0, nf)
        data = np.empty(self.n * 2, np.int16)
        data[0::2] = (L * 32767).astype(np.int16)
        data[1::2] = (R * 32767).astype(np.int16)
        with wave.open(path, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(data.tobytes())
