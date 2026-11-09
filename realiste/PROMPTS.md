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

---

## 01 · ATCHOUM

Animatique / timing : `episodes/ep01_atchoum.mp4` · Bande-son : `realiste/bandes_son/ep01_atchoum.m4a`


### Plan 1 · 0.0 s → 1.2 s (1.2 s)

Guide de composition : `realiste/guides/ep01_atchoum_p01.jpg`

**Image de départ :**
```
Close-up of (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) standing in a cozy lavender living room with a framed sun picture and a wooden shelf, eyes squeezed, body inflating, about to sneeze. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on the shelf. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo inhales twice, body swelling, tuft trembling, static camera. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 1.2 s → 2.8 s (1.6 s)

Guide de composition : `realiste/guides/ep01_atchoum_p02.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) mid-sneeze in the living room; a tiny marble-sized copy of Nubo bounces on the floor. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Big cartoon sneeze, Nubo squashes, a tiny Nubo pops out and bounces, the two look at each other. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 2.8 s → 5.0 s (2.2 s)

Guide de composition : `realiste/guides/ep01_atchoum_p03.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) sneezing again, several tiny fluffy orange Nubos bouncing around on the wooden floor. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Two more sneezes, each spawning more tiny Nubos that bounce and roll, playful. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 5.0 s → 9.0 s (4.0 s)

Guide de composition : `realiste/guides/ep01_atchoum_p04.jpg`

**Image de départ :**
```
A living room rapidly filling with hundreds of tiny fluffy orange Nubos like a ball pit, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) half buried in the middle, tuft standing straight up. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Rapid machine-gun sneezes, the orange ball pit rises fast and swallows the room. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 9.0 s → 13.0 s (4.0 s)

Guide de composition : `realiste/guides/ep01_atchoum_p05.jpg`

**Image de départ :**
```
The whole room filled with tiny orange fluffy creatures; only (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat)'s two eyes and tuft stick out of the orange sea. Silence. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo looks left, looks right, slow blink. Very still. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 13.0 s → 15.8 s (2.8 s)

Guide de composition : `realiste/guides/ep01_atchoum_p06.jpg`

**Image de départ :**
```
A vintage red gumball machine on a mint-green grocery counter, its glass globe packed with tiny orange fluffy Nubos. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on the counter. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Fast camera pull-back revealing the gumball machine, a coin drops into the slot, the crank turns by itself. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 7 · 15.8 s → 18.0 s (2.2 s)

Guide de composition : `realiste/guides/ep01_atchoum_p07.jpg`

**Image de départ :**
```
Inside the metal chute of the gumball machine, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) sitting after rolling out, looking straight at the camera. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo rolls in and lands, turns its eyes to the camera, blinks twice, then starts inhaling to sneeze. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 02 · LE GRILLE-PAIN

Animatique / timing : `episodes/ep02_grille_pain.mp4` · Bande-son : `realiste/bandes_son/ep02_grille_pain.m4a`


### Plan 1 · 0.0 s → 1.0 s (1.0 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p01.jpg`

**Image de départ :**
```
Extreme slow motion: a golden slice of toast spinning straight toward the camera, crumbs floating, blurred pastel mint kitchen behind. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Toast flies at the lens in slow motion. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 1.0 s → 3.0 s (2.0 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p02.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) in a mint-tiled kitchen next to a pastel pink retro toaster, holding a toast above its head proudly. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on a shelf. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo catches the toast, tosses it aside, slides a fresh slice into the toaster. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 3.0 s → 6.0 s (3.0 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p03.jpg`

**Image de départ :**
```
A pancake popping out of the pink toaster and gliding through the kitchen like a frisbee, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) watching, tuft curled like a question mark. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Ding, the pancake shoots up and glides away, Nubo's eyes follow. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 6.0 s → 9.0 s (3.0 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p04.jpg`

**Image de départ :**
```
A grey pigeon bursting out of the pink toaster and flying away, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) startled, tuft standing straight up. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo puts a striped sock in, ding, a live pigeon flaps out and flies off. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 9.0 s → 12.4 s (3.4 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p05.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) standing on top of the pink toaster peering into the slot, its tuft pulled by suction. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo hops onto the toaster, leans over, gets sucked into the slot stretching like rubber. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 12.4 s → 17.0 s (4.6 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p06.jpg`

**Image de départ :**
```
The pink toaster glowing orange from its slots, a pigeon and a pancake waiting next to it on the counter like in a waiting room. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Lever down, ticking timer, the toaster trembles and glows. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 7 · 17.0 s → 20.0 s (3.0 s)

Guide de composition : `realiste/guides/ep02_grille_pain_p07.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) perfectly toasted golden-brown with grill marks, a wisp of smoke from its tuft, standing proudly on the counter. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo shoots out in slow motion, lands, looks at camera, blinks twice; a toast pops toward the lens. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 03 · LA PLANTE

Animatique / timing : `episodes/ep03_la_plante.mp4` · Bande-son : `realiste/bandes_son/ep03_la_plante.m4a`


### Plan 1 · 0.0 s → 5.5 s (5.5 s)

Guide de composition : `realiste/guides/ep03_la_plante_p01.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) on a sunny windowsill with pink curtains spraying water on a tiny cactus in a terracotta pot. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on the sill. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
With each spray the cactus doubles in size with a bouncy boing, the pot cracks, Nubo's tuft stands up. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 5.5 s → 10.2 s (4.7 s)

Guide de composition : `realiste/guides/ep03_la_plante_p02.jpg`

**Image de départ :**
```
A giant cactus towering over (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat), a huge pink flower blooming at its top, glowing golden center. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The bud swells and blooms in slow motion, petals unfolding, warm glow. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 10.2 s → 15.0 s (4.8 s)

Guide de composition : `realiste/guides/ep03_la_plante_p03.jpg`

**Image de départ :**
```
Macro view into the glowing center of a pink flower revealing a miniature windowsill where a tiny Nubo sprays a tiny cactus. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Continuous seamless zoom into the flower ending exactly on the opening framing (infinite Droste loop); the tiny Nubo blinks at camera. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 04 · 03:17

Animatique / timing : `episodes/ep04_0317.mp4` · Bande-son : `realiste/bandes_son/ep04_0317.m4a`


### Plan 1 · 0.0 s → 2.4 s (2.4 s)

Guide de composition : `realiste/guides/ep04_0317_p01.jpg`

**Image de départ :**
```
Grainy green night-vision security camera footage of a dark kitchen, high fisheye angle, timestamp 03:17:04, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) tiptoeing toward a tall fridge. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo tiptoes across the floor, CCTV jitter. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 2.4 s → 5.5 s (3.1 s)

Guide de composition : `realiste/guides/ep04_0317_p02.jpg`

**Image de départ :**
```
Same CCTV view, fridge door open showing a colorful disco party inside: dancing eggs, lemon, sausage and cheese with tiny eyes, a disco ball, colored lights spilling out. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The food dances to the beat, lights flash, Nubo stares. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 5.5 s → 9.0 s (3.5 s)

Guide de composition : `realiste/guides/ep04_0317_p03.jpg`

**Image de départ :**
```
Same CCTV view, fridge open with normal light, all food items perfectly still and innocent. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Door closes and reopens: everything frozen, one egg wobbles slightly. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 9.0 s → 15.8 s (6.8 s)

Guide de composition : `realiste/guides/ep04_0317_p04.jpg`

**Image de départ :**
```
Same CCTV view, all the food inside the fridge turned toward the security camera, staring; (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) in front of the fridge. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Slow creepy push-in, then Nubo slowly turns to the camera. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 17.6 s → 20.0 s (2.4 s)

Guide de composition : `realiste/guides/ep04_0317_p05.jpg`

**Image de départ :**
```
Night-vision fisheye close-up of (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat)'s face pressed against the camera lens. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo blinks twice, heavy CCTV noise, then static. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 05 · CONCOURS DE REGARD

Animatique / timing : `episodes/ep05_concours_de_regard.mp4` · Bande-son : `realiste/bandes_son/ep05_concours_de_regard.m4a`


### Plan 1 · 0.0 s → 1.0 s (1.0 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p01.jpg`

**Image de départ :**
```
Extreme close-up of (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat)'s narrowed determined eyes, western standoff style. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Slow push-in, intense. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 1.0 s → 1.8 s (0.8 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p02.jpg`

**Image de départ :**
```
Extreme close-up of a goldfish's round unblinking eye through glass, water bubbles. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Fish eye perfectly still, bubbles rise. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 1.8 s → 6.0 s (4.2 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p03.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) face to face with a round glass fishbowl containing a goldfish on a wooden table, lavender striped wall. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on the table. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Alternating dramatic zooms, a sweat drop, a tumbleweed rolls by. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 6.0 s → 10.0 s (4.0 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p04.jpg`

**Image de départ :**
```
A crowd of colorful fluffy creatures gathers behind the duel holding signs with drawings of Nubo and of a fish. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The crowd pops in and cheers silently. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 10.0 s → 14.0 s (4.0 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p05.jpg`

**Image de départ :**
```
Time-lapse: (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) with a long grey beard still staring at the goldfish; night, snow and autumn leaves passing. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Day turns to night, snow, leaves, the beard grows, the fish never moves. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 14.0 s → 17.0 s (3.0 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p06.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) with a grey beard blinking, the crowd erupting with confetti. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo's eyes tremble then blink, gong, the crowd jumps. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 7 · 17.0 s → 21.2 s (4.2 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p07.jpg`

**Image de départ :**
```
A tiny golden trophy on the fishbowl, fireworks, bearded (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) slumped and defeated. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Fireworks, Nubo collapses, then looks at camera and blinks twice. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 8 · 21.2 s → 22.0 s (0.8 s)

Guide de composition : `realiste/guides/ep05_concours_de_regard_p08.jpg`

**Image de départ :**
```
Extreme close-up of the goldfish's eye. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Still, loop back to the opening close-up. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 06 · MAUVAIS ÉTAGE

Animatique / timing : `episodes/ep06_mauvais_etage.mp4` · Bande-son : `realiste/bandes_son/ep06_mauvais_etage.m4a`


### Plan 1 · 0.0 s → 1.6 s (1.6 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p01.jpg`

**Image de départ :**
```
View from inside a warm wooden elevator: doors open on a brown bear in a striped swimsuit sitting in a bubbling hot tub, staring. (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) in the foreground left by the button panel. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Ding, doors open, the bear stares, Nubo presses the close button, doors close. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 1.6 s → 2.8 s (1.2 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p02.jpg`

**Image de départ :**
```
Elevator interior, doors closed, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) waiting, floor lights above the doors. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo bobs to the elevator music (reusable travel shot). smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 2.8 s → 4.9 s (2.1 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p03.jpg`

**Image de départ :**
```
Elevator doors open on outer space: Earth and a waving astronaut floating. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Astronaut waves, Nubo presses close. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 5.6 s → 7.5 s (1.9 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p04.jpg`

**Image de départ :**
```
Elevator doors open on a wall of grandmothers in glasses all knitting small orange Nubo dolls. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
All grannies look up at the same time, Nubo frantically presses close. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 8.2 s → 10.1 s (1.9 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p05.jpg`

**Image de départ :**
```
Elevator doors open on the inside of a whale: ribs, ankle-deep water, a red and white lighthouse with a rotating beam. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Beam sweeps, a drip falls, Nubo presses close. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 11.0 s → 13.9 s (2.9 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p06.jpg`

**Image de départ :**
```
Elevator doors open on a grey real office; a giant real human eye fills the doorway and looks at Nubo. (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) terrified, tuft up, sweating. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The eye opens and turns to Nubo, Nubo presses close ten times, doors close agonizingly slowly. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 7 · 15.2 s → 19.8 s (4.6 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p07.jpg`

**Image de départ :**
```
Elevator doors open on a cream landing with a plant where another identical (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) waits. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Both Nubos stare at each other, then both turn to the camera and blink twice in sync. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 8 · 19.8 s → 24.0 s (4.2 s)

Guide de composition : `realiste/guides/ep06_mauvais_etage_p08.jpg`

**Image de départ :**
```
The two identical Nubos crossing in the elevator doorway, swapping places. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
One steps out, one steps in, doors close, ding, doors open again on the bear. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 07 · NE PAS APPUYER

Animatique / timing : `episodes/ep07_ne_pas_appuyer.mp4` · Bande-son : `realiste/bandes_son/ep07_ne_pas_appuyer.m4a`


### Plan 1 · 0.0 s → 3.0 s (3.0 s)

Guide de composition : `realiste/guides/ep07_ne_pas_appuyer_p01.jpg`

**Image de départ :**
```
A big glossy red button on a lavender wall under a no-hands pictogram sign, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) next to it. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on the floor beside the button. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo presses, confetti bursts, Nubo spins happily. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 3.0 s → 6.2 s (3.2 s)

Guide de composition : `realiste/guides/ep07_ne_pas_appuyer_p02.jpg`

**Image de départ :**
```
A grand piano crashed on the floor right next to (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat), dust, confetti everywhere, Nubo's tuft standing straight up. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Click, a piano falls from above and crashes beside Nubo, camera shake. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 6.2 s → 9.0 s (2.8 s)

Guide de composition : `realiste/guides/ep07_ne_pas_appuyer_p03.jpg`

**Image de départ :**
```
Gravity flipped: (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) and the piano stuck upside down on the ceiling, the chick still on the floor; Nubo's arm stretching like rubber down to the button. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Everything falls up to the ceiling, Nubo's arm stretches all the way down to press the button. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 9.0 s → 12.8 s (3.8 s)

Guide de composition : `realiste/guides/ep07_ne_pas_appuyer_p04.jpg`

**Image de départ :**
```
STYLE BREAK: the same corridor rendered as a crude handmade felt stop-motion puppet set, Nubo turned into a felt puppet looking at its own hands in horror. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Everything falls back down and the world becomes cheap felt stop-motion; Nubo panics. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 12.8 s → 16.0 s (3.2 s)

Guide de composition : `realiste/guides/ep07_ne_pas_appuyer_p05.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) (back to ultra-realistic) slowly walking backward away from the red button. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo backs away very slowly, never breaking eye contact with the button, exits frame. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 16.0 s → 17.6 s (1.6 s)

Guide de composition : `realiste/guides/ep07_ne_pas_appuyer_p06.jpg`

**Image de départ :**
```
The tiny yellow chick next to the red button, alone in the corridor. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The chick slides by itself to the button, hops and presses it. Cut to black. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 08 · LESSIVE

Animatique / timing : `episodes/ep08_lessive.mp4` · Bande-son : `realiste/bandes_son/ep08_lessive.m4a`


### Plan 1 · 0.0 s → 1.4 s (1.4 s)

Guide de composition : `realiste/guides/ep08_lessive_p01.jpg`

**Image de départ :**
```
View through the round glass door of a washing machine: (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) spinning in the drum with striped socks, dizzy spiral eyes. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Drum spins, Nubo tumbles. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 1.4 s → 4.7 s (3.3 s)

Guide de composition : `realiste/guides/ep08_lessive_p02.jpg`

**Image de départ :**
```
A pea-sized tiny (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) in front of an open washing machine in a mint-tiled laundry room, looking up at a care label. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss on a shelf. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Ding, door opens, shrunken Nubo hops out, looks at label, jumps back in. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 4.7 s → 6.6 s (1.9 s)

Guide de composition : `realiste/guides/ep08_lessive_p03.jpg`

**Image de départ :**
```
The washing machine shaking, tiny Nubo spinning visible behind the glass. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Machine rumbles and vibrates. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 6.6 s → 10.4 s (3.8 s)

Guide de composition : `realiste/guides/ep08_lessive_p04.jpg`

**Image de départ :**
```
An enormous over-puffed fluffy (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) bursting out of the washing machine, filling the room. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Ding, giant fluffy Nubo squeezes out, blinks, then wiggles back inside. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 10.4 s → 12.3 s (1.9 s)

Guide de composition : `realiste/guides/ep08_lessive_p05.jpg`

**Image de départ :**
```
The washing machine hopping wildly on the floor. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Violent spin cycle, the machine jumps. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 12.3 s → 15.0 s (2.7 s)

Guide de composition : `realiste/guides/ep08_lessive_p06.jpg`

**Image de départ :**
```
An orange hand-knitted sweater with two glossy eyes lying in front of the washing machine. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Ding, the sweater slides out onto the floor. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 7 · 15.0 s → 18.0 s (3.0 s)

Guide de composition : `realiste/guides/ep08_lessive_p07.jpg`

**Image de départ :**
```
A grey cat proudly wearing the orange knitted sweater with two eyes on its chest. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The cat walks in, puts on the sweater, struts; the sweater's eyes blink twice at the camera. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 09 · JOYEUX ANNIVERSAIRE

Animatique / timing : `episodes/ep09_joyeux_anniversaire.mp4` · Bande-son : `realiste/bandes_son/ep09_joyeux_anniversaire.m4a`


### Plan 1 · 0.0 s → 3.0 s (3.0 s)

Guide de composition : `realiste/guides/ep09_joyeux_anniversaire_p01.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) with puffed cheeks behind a polka-dot party table, a pink two-layer birthday cake with one striped candle, pink wall with bunting. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo blows, the flame goes out, then relights with a pop. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 3.0 s → 6.3 s (3.3 s)

Guide de composition : `realiste/guides/ep09_joyeux_anniversaire_p02.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) blowing hard, bunting and streamers flying away. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Harder blow, decorations fly off, candle relights. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 6.3 s → 9.4 s (3.1 s)

Guide de composition : `realiste/guides/ep09_joyeux_anniversaire_p03.jpg`

**Image de départ :**
```
The walls of the room ripping away revealing outer space and a grey moon surface with Earth in the sky. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The walls are blown away like paper, the candle relights. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 9.4 s → 15.0 s (5.6 s)

Guide de composition : `realiste/guides/ep09_joyeux_anniversaire_p04.jpg`

**Image de départ :**
```
(NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) flattened like a deflated balloon next to the cake on the moon, the candle still burning. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Ultimate blow, tablecloth flies away, Nubo deflates, silence. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 15.0 s → 17.2 s (2.2 s)

Guide de composition : `realiste/guides/ep09_joyeux_anniversaire_p05.jpg`

**Image de départ :**
```
The candle flame grown huge, leaning toward flat (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat). ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The flame inhales, grows, and blows on Nubo; Nubo's tuft goes out like a wick with smoke. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 17.2 s → 20.0 s (2.8 s)

Guide de composition : `realiste/guides/ep09_joyeux_anniversaire_p06.jpg`

**Image de départ :**
```
Flat (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) with a smoking tuft on the moon looking at camera. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo blinks twice, then its tuft relights with a pop. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

---

## 10 · LE SELFIE

Animatique / timing : `episodes/ep10_le_selfie.mp4` · Bande-son : `realiste/bandes_son/ep10_le_selfie.m4a`


### Plan 1 · 0.0 s → 1.0 s (1.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p01.jpg`

**Image de départ :**
```
Phone front-camera selfie POV: (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) winking in a pastel forest, a tiny moose far away between the trees. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Camera flash, selfie pose. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 2 · 1.0 s → 3.0 s (2.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p02.jpg`

**Image de départ :**
```
Wide shot, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) holding a phone up in a pastel forest, empty forest. a tiny fluffy yellow chick sits motionless somewhere in the background, easy to miss in the grass. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo changes pose. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 3 · 3.0 s → 5.0 s (2.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p03.jpg`

**Image de départ :**
```
Selfie POV: (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) winking, the moose now mid-distance behind. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Flash. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 4 · 5.0 s → 7.0 s (2.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p04.jpg`

**Image de départ :**
```
Selfie POV: (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) with tuft trembling, a huge moose standing right behind it. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Flash, horror sting. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 5 · 7.0 s → 10.0 s (3.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p05.jpg`

**Image de départ :**
```
Wide shot, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) turned around, empty forest, shrugging with a question-mark tuft. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Nubo turns around, sees nothing, shrugs, lifts the phone again. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 6 · 10.0 s → 12.0 s (2.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p06.jpg`

**Image de départ :**
```
Selfie POV: a giant smiling moose holding the phone, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) squeezed against its cheek, stunned. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
Flash, the moose grins. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 7 · 12.0 s → 15.0 s (3.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p07.jpg`

**Image de départ :**
```
Wide shot, the moose and (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) side by side happily looking at the phone. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
They admire the photo together. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```

### Plan 8 · 15.0 s → 18.0 s (3.0 s)

Guide de composition : `realiste/guides/ep10_le_selfie_p08.jpg`

**Image de départ :**
```
The moose chewing, crumbs of phone falling, (NUBO, a small round fluffy creature covered in long soft tangerine-orange fur (#FF8A3D), round marshmallow-shaped body, two big glossy dark-brown eyes with bright catchlights, a tiny gentle closed smile, short stubby arms, two round stubby feet, a single curly fur tuft like an antenna on top of its head, about the size of a cat) next to it. ultra-realistic Pixar-quality 3D animation, cinematic CGI render, physically based fur with individual strands, soft subsurface glow, 35mm lens, shallow depth of field, warm soft key light with gentle light rays, pastel set design, vertical 9:16, 4K, highly detailed, no text, no subtitles, no watermark
```
**Mouvement (image → vidéo) :**
```
The moose eats the phone with a crunch, then both turn to the camera and blink twice in sync. Flash. smooth natural motion, consistent character design, no morphing, no extra limbs, Nubo never speaks
```
