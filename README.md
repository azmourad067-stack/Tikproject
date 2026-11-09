# Tikproject — NUBO 🟠

Chaîne TikTok internationale sans dialogue : **NUBO**, une créature en feutrine qui transforme chaque tâche banale en catastrophe absurde.

## 📦 Contenu du dépôt

| Dossier / fichier | Contenu |
|---|---|
| [`NUBO_BIBLE.md`](./NUBO_BIBLE.md) | Stratégie complète : 5 concepts évalués, identité, formule des vidéos, prompts IA, croissance, tests |
| [`episodes/`](./episodes) | **Les 10 premiers épisodes prêts à publier** (MP4 1080×1920 + vignettes) |
| [`episodes/PUBLICATION.md`](./episodes/PUBLICATION.md) | Kit de publication : calendrier, légendes emoji, hashtags, couvertures, commentaires épinglés |
| [`production/`](./production) | Le studio : moteur d'animation « feutrine stop-motion » + synthétiseur audio + 1 script par épisode |

## 🎬 Les 10 épisodes

| # | Fichier | Durée | Pitch |
|---|---|---|---|
| 01 | `ep01_atchoum.mp4` | 18 s | Chaque éternuement crée des mini-NUBO… jusqu'à remplir un distributeur de bonbons |
| 02 | `ep02_grille_pain.mp4` | 20 s | Le grille-pain ne rend jamais ce qu'on lui donne. NUBO en ressort doré |
| 03 | `ep03_la_plante.mp4` | 15 s | Chaque pschitt fait doubler le cactus → zoom infini dans la fleur |
| 04 | `ep04_0317.mp4` | 20 s | Caméra de surveillance, 03:17 : fête disco dans le frigo |
| 05 | `ep05_concours_de_regard.mp4` | 22 s | NUBO vs un poisson rouge. (Les poissons n'ont pas de paupières.) |
| 06 | `ep06_mauvais_etage.mp4` | 24 s | Chaque étage de l'ascenseur ouvre sur un monde plus absurde |
| 07 | `ep07_ne_pas_appuyer.mp4` | 20 s | Le bouton rouge interdit… et le canard témoin bouge pour la 1ʳᵉ fois |
| 08 | `ep08_lessive.mp4` | 18 s | Rétréci, puis trop gonflé, puis… devenu pull porté par un chat |
| 09 | `ep09_joyeux_anniversaire.mp4` | 20 s | La bougie farceuse résiste jusqu'à la Lune — et souffle NUBO |
| 10 | `ep10_le_selfie.mp4` | 18 s | À chaque selfie, l'élan est plus proche. Puis il mange le téléphone |

## 🛠️ Régénérer les vidéos

Prérequis : Python 3 avec `numpy` et `Pillow`, et `ffmpeg`.

```bash
cd production
python3 render.py ep01          # rend episodes/ep01_atchoum.mp4 (+ vignette)
./finalize.sh                   # normalise le volume de tous les épisodes à -14 LUFS
```

Aucun service externe ni modèle d'IA n'est nécessaire : images, textures de laine, bruitages et musiques sont entièrement générés par le code (donc libres de droits).
