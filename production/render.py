"""Rendu d'un épisode NUBO : images (multiprocessus) -> ffmpeg + audio synthétisé.

Usage :
  python render.py ep01            # rend la vidéo finale
  python render.py ep01 --sheet    # planche-contact (1 image / seconde) pour vérification
  python render.py ep01 --at 3.5   # une seule image
"""
import importlib
import os
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image

import engine as E

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(ROOT), "episodes")
_MOD = None


def _init(name):
    global _MOD
    _MOD = importlib.import_module(name)


def _frame(fi):
    E.FRAME = fi
    img = _MOD.frame(fi / E.FPS)
    if getattr(_MOD, "POST", True):
        img = E.post(img)
    return img.convert("RGB")


def _work(fi):
    return _frame(fi).tobytes()


def render_video(name, slug):
    mod = importlib.import_module(name)
    os.makedirs(OUT, exist_ok=True)
    n = int(round(mod.DUR * E.FPS))
    wav = os.path.join(OUT, f".{slug}.wav")
    from audio import Mix
    mix = Mix(mod.DUR)
    mod.sound(mix)
    mix.write(wav)
    mp4 = os.path.join(OUT, f"{slug}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{E.W}x{E.H}", "-r", str(E.FPS), "-i", "-", "-i", wav,
           "-vf", "fps=30", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "7M", "-bufsize", "14M",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4, initializer=_init, initargs=(name,)) as pool:
        for i, buf in enumerate(pool.imap(_work, range(n), chunksize=2)):
            p.stdin.write(buf)
            if i % 48 == 0:
                print(f"  {name}: {i}/{n}", flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    # vignette de couverture
    _init(name)
    cover = _frame(int(getattr(mod, "COVER_T", mod.DUR / 2) * E.FPS))
    cover.save(os.path.join(OUT, f"{slug}_cover.jpg"), quality=92)
    print("OK", mp4)


def sheet(name, path, step=1.0, times=None):
    _init(name)
    times = times or [i * step for i in range(int(_MOD.DUR / step) + 1)]
    times = [min(t, _MOD.DUR - 1 / E.FPS) for t in times]
    th = [_frame(int(round(t * E.FPS))).resize((270, 480)) for t in times]
    cols = 6
    rows = (len(th) + cols - 1) // cols
    out = Image.new("RGB", (cols * 270, rows * 480), "black")
    for i, im in enumerate(th):
        out.paste(im, ((i % cols) * 270, (i // cols) * 480))
    out.save(path)
    print(path)


if __name__ == "__main__":
    name = sys.argv[1]
    if "--sheet" in sys.argv:
        step = float(sys.argv[sys.argv.index("--sheet") + 1]) if len(sys.argv) > sys.argv.index("--sheet") + 1 else 1.0
        sheet(name, sys.argv[-1] if sys.argv[-1].endswith(".png") else f"/tmp/{name}_sheet.png", step)
    elif "--at" in sys.argv:
        t = float(sys.argv[sys.argv.index("--at") + 1])
        _init(name)
        _frame(int(t * E.FPS)).save(sys.argv[-1])
    else:
        render_video(name, getattr(importlib.import_module(name), "SLUG", name))
