# 🟠 NUBO ULTRA-RÉALISTE : pack de production

Ce pack sert à refaire les 10 épisodes dans le style de `realiste/reference_nubo.png` : un rendu CGI façon Pixar, avec une vraie fourrure.

## Le principe : les vidéos actuelles servent d'animatiques

Les 10 MP4 du dossier `episodes/` deviennent le **squelette** de la version réaliste :

- **Timing :** chaque plan ci-dessous indique son début et sa fin exacts.
- **Bande-son :** elle est prête dans `realiste/bandes_son/` (bruitages et musiques originaux, volume déjà normalisé). Il suffit de caler les plans IA dessus.
- **Composition :** chaque plan a une image-guide extraite de l'animatique, dans `realiste/guides/`.

## Le pipeline (par plan)

1. **Verrouiller le personnage (à faire une seule fois).** Chargez `reference_nubo.png` comme référence de personnage dans l'outil : *Character / Elements / Reference* dans Kling, *Ingredients* dans Veo, *References* dans Runway. Faites-en une planche de 4 à 6 vues et gardez-les.
2. **Créer l'image de départ.** Utilisez le prompt « Image de départ », la référence du personnage et l'image-guide comme référence de composition (*structure / image-to-image* à force moyenne, autour de 0,4).
3. **Animer l'image.** Lancez le prompt « Mouvement » en image vers vidéo, sur une durée de 5 à 10 s, au format 9:16.
4. **Faire 2 ou 3 essais par plan** et garder le meilleur. Jetez tout plan où NUBO change d'apparence.
5. **Monter.** Dans CapCut ou DaVinci, posez la bande-son de l'épisode, puis placez chaque plan à son horodatage et coupez à la durée indiquée. Exportez en 1080×1920.

## Outils conseillés (à comparer sur un plan test)

| Outil | Points forts |
|---|---|
| **Kling** | Très bon rapport qualité/prix, cohérence de personnage via *Elements* |
| **Google Veo** | Rendu le plus cinématographique, très bonne physique |
| **Runway** | Contrôle fin de la caméra, références multiples |
| **Hailuo / MiniMax** | Bon marché, très bon pour l'animation de fourrure |

**Budget indicatif :** environ 200 s de film, soit 600 à 800 s générées en comptant les essais. Selon l'outil et l'abonnement, comptez de quelques dizaines à quelques centaines d'euros pour les 10 épisodes. Vérifiez les tarifs du moment, ils évoluent vite.

## Changements par rapport à la version feutrine

- **NUBO** reprend exactement l'apparence de votre image de référence : fourrure orange longue, yeux bruns brillants et **petit sourire fermé**. Il ne parle toujours jamais.
- **Le témoin caché** devient le **petit poussin jaune** de la référence, à la place du canard. Le principe reste le même : il apparaît dans chaque vidéo et bouge pour la première fois dans l'épisode 07.
- **Épisode 07 :** la « rupture de style » s'inverse. Le monde réaliste devient soudain un **décor en feutrine bon marché**, ce qui renvoie un clin d'œil à la version originale.
- **LE REGARD** reste la signature de fin : deux clignements face caméra.

## Blocs réutilisables (déjà intégrés aux prompts)

**Personnage :**
```
NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat
```

**Prompt négatif (si l'outil l'accepte) :**
```
text, letters, subtitles, watermark, logo, open mouth, teeth, talking, extra limbs, extra eyes, deformed, morphing character, inconsistent fur color, blurry character
```

# Plans par épisode
