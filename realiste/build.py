"""Génère le pack ultra-réaliste : images-guides, bandes-son et PROMPTS.md à partir de shots.py."""
import os
import subprocess

from shots import CHICK, EPISODES, MOTION, NUBO, STYLE

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = os.path.join(os.path.dirname(HERE), "episodes")


def fill(s):
    return s.replace("[NUBO]", "(" + NUBO + ")").replace("[CHICK]", CHICK)


lines = []
for slug, title, shots in EPISODES:
    src = os.path.join(EPS, slug + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-c:a", "copy",
                    os.path.join(HERE, "bandes_son", slug + ".m4a")], check=True)
    num = slug[2:4]
    lines.append(f"\n---\n\n## {num} · {title}\n")
    lines.append(f"Animatique / timing : `episodes/{slug}.mp4` · Bande-son : `realiste/bandes_son/{slug}.m4a`\n")
    for i, (t0, t1, tg, img, mot) in enumerate(shots, 1):
        guide = f"guides/{slug}_p{i:02d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(tg), "-i", src, "-frames:v", "1",
                        "-vf", "scale=540:960", "-q:v", "4", os.path.join(HERE, guide)], check=True)
        lines.append(f"\n### Plan {i} · {t0:.1f} s → {t1:.1f} s ({t1 - t0:.1f} s)\n")
        lines.append(f"Guide de composition : `realiste/{guide}`\n")
        lines.append("**Image de départ :**\n```\n" + fill(img) + " " + STYLE + "\n```")
        lines.append("**Mouvement (image → vidéo) :**\n```\n" + fill(mot) + " " + MOTION + "\n```")

header = open(os.path.join(HERE, "PROMPTS_HEADER.md"), encoding="utf-8").read()
with open(os.path.join(HERE, "PROMPTS.md"), "w", encoding="utf-8") as f:
    f.write(header + "\n".join(lines) + "\n")
print("OK")
