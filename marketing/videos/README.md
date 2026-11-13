# Vidéos TikTok / Reels (test de format)

`out/` contient, pour chacune des 20 vidéos :
- `NN-nom.mp4` : vidéo verticale 1080×1920, 30 i/s, H.264, 11 à 18 s, **sans son** ;
- `NN-nom.jpg` : image de couverture ;
- `NN-nom.txt` : légende + hashtags à copier.

## Publier
1. Transfère les MP4 sur ton téléphone (AirDrop, Google Drive, ou télécharge-les depuis GitHub).
2. Dans TikTok : **+** → Importer → choisis la vidéo.
3. Ajoute un **son tendance** depuis la bibliothèque de l'app (droits inclus). N'ajoute pas de musique importée toi-même.
4. Colle la légende du fichier `.txt`.
5. Choisis la couverture (ou importe le `.jpg`).
6. Suis le planning de `marketing/scripts-videos.md` (2 vidéos/jour) et note les vues chaque soir.

Les vidéos laissent libres le bas (~400 px) et la droite (~140 px) de l'écran, où TikTok affiche ses boutons et la légende.

## Modifier ou créer une vidéo
Édite `videos.json` (étapes : `me`, `them`, `ai`, `info`, `label`, `card`), puis :
```bash
node marketing/videos/render.cjs              # toutes
node marketing/videos/render.cjs 01-ca-va-et-toi   # une seule
```
Prérequis : Node, Playwright (Chromium) et ffmpeg.
