# Plan d'application : coach de séduction IA francophone

*Version 2, 13 novembre 2026. Elle remplace la version 1 (préparation à l'examen civique), écartée parce que son potentiel était trop faible pour l'objectif visé. L'analyse de la v1 est résumée en annexe.*

**Légende utilisée dans tout le document :**
- **[DONNÉE]** : fait tiré d'une source citée.
- **[SECONDAIRE]** : chiffre repris par un tiers (blog, estimation d'outil d'analyse), non audité.
- **[HYPOTHÈSE]** : mon estimation, à valider avant d'engager du temps ou de l'argent.

---

## 0. Cadre de décision

**Profil retenu :** budget inférieur à 1 000 €, je code et tu testes, tu es d'accord pour publier des vidéos courtes. Tes intérêts déclarés sont les apps de rencontre et l'IA, qui sont au cœur de ce projet.

**La vérité de base à garder en tête :** sur 417 apps mobiles dont le revenu est vérifié sur TrustMRR, la médiane gagne **42 $/mois**, 27 % ne gagnent rien, et environ 1 sur 6 dépasse 1 000 $/mois ([BigIdeasDB, oct. 2026](https://bigideasdb.com/how-to-build-an-app-that-makes-money)) [SECONDAIRE]. Selon RevenueCat, 4,6 % des nouvelles apps atteignent 10 k$/mois en deux ans ([RevenueCat](https://www.revenuecat.com/state-of-subscription-apps)) [SECONDAIRE]. **Ce projet vise la queue haute de cette distribution, et il a davantage de chances d'échouer que de réussir.** Le plan est donc construit pour échouer vite et pas cher, ou pour accélérer si les signaux sont bons.

---

## 1. Pourquoi cette idée (les preuves)

### 1.1 La demande et la monétisation sont prouvées
- **RizzGPT : 70 k$ de revenu récurrent mensuel et 36 k$ encaissés sur 30 jours, vérifiés via RevenueCat** selon TrustMRR (instantané du 23 mars 2026). Les prix sont de 3,99 $/semaine, 8,99 $/mois et 44,99 $/an ([TrustMRR](https://trustmrr.com/startup/ai-dating-assistant-1)) [DONNÉE vérifiée par un tiers].
- **Rizz (le leader)** : environ 300 k$/mois et 200 k téléchargements/mois selon les estimations d'Adapty ([Adapty](https://adapty.io/paywall-library/rizz/)), plus de 7,5 M de téléchargements depuis 2022 ([Starter Story](https://www.starterstory.com/rizz-breakdown)) [SECONDAIRE, les chiffres divergent selon les sources].
- **Les leaders ont démarré sans gros budget** : Rizz aurait été lancé en autofinancement et aurait grandi via TikTok, avec des formats de captures d'écran et de vidéos « sans visage » cumulant des centaines de millions de vues ([Shortimize](https://www.shortimize.com/blog/rizz-apps-b-roll-strategy-that-got-them-half-a-billion-views-on-tiktok), [Stormy](https://stormy.ai/blog/rizz-app-viral-growth-hacking-lessons)) [SECONDAIRE, ces sources vendent des services marketing]. Une source affirme au contraire que Rizz dépend aujourd'hui de la publicité payante. **Le récit « 100 % organique » est donc à prendre avec prudence.**

### 1.2 L'angle choisi : le français d'abord
- Les apps visibles sur l'App Store français (Rizz Up, AI Wingman, RARE…) ont **des descriptions en anglais** ou sont des traductions génériques ([Rizz Up FR](https://apps.apple.com/fr/app/id6475344381), [AI Wingman FR](https://apps.apple.com/fr/app/ai-wingman/id6458177920)) [DONNÉE]. **[HYPOTHÈSE]** Un produit pensé pour les codes culturels français, avec un ton naturel, de l'humour français et les apps utilisées en France (Tinder, Hinge, Bumble, Fruitz, happn), se différencie mieux qu'un énième clone anglophone.
- Hinge a lancé en France une fonction intégrée de retour IA sur les profils ([Presse-citron](https://www.presse-citron.net/comment-hinge-va-vous-aider-a-pecho-grace-a-sa-nouvelle-fonctionnalite-ia/)) [DONNÉE]. C'est une **validation** du besoin, mais aussi une **menace** : les apps de rencontre internalisent la fonction.

### 1.3 Ce qui peut faire échouer le projet

| Risque | Gravité | Ce qu'on fait |
|---|---|---|
| **Rejet par Apple (règle 4.3(b))** : les apps de rencontre font partie des catégories saturées. La règle a été durcie en juin 2026 contre les apps « indiscernables de l'existant » ([MacRumors](https://macrumors.com/2026/06/09/app-store-guidelines-low-quality-apps/), [forums Apple](https://developer.apple.com/forums/thread/777838)). | Élevée | Ne **pas** être une app de rencontre : c'est un outil de **coaching et d'écriture**. Une différenciation visible (français, explications pédagogiques, analyse de profil) et une vraie profondeur fonctionnelle. Prévoir un appel en cas de rejet. |
| **Saturation** : des dizaines de clones, la plupart sous 10 k$/mois ([AppGoblin](https://appgoblin.info/apps/6748056633)) | Élevée | Niche francophone, qualité des réponses, contenu vidéo. |
| **La viralité ne prend pas** | Élevée | C'est **le** facteur décisif. Critères d'arrêt chiffrés (§4.4). |
| **RGPD** : les captures de conversations contiennent les données personnelles d'un tiers (le match) | Moyenne | **Reconnaissance du texte (OCR) sur le téléphone**, prénoms masqués, envoi du texte seul, aucun stockage (§3.3). Validation par un juriste recommandée. |
| **Règle Apple 5.1.2(i)** (nov. 2025) : consentement explicite obligatoire avant d'envoyer des données personnelles à une IA tierce ([TechCrunch](https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai)) | Moyenne | Écran de consentement dédié à l'onboarding. |
| **Les apps de rencontre internalisent l'IA** (Hinge) | Moyenne, à moyen terme | Couvrir plusieurs apps et faire du coaching, pas seulement de la génération de messages. |
| **Image** : un « outil de drague manipulateur » peut faire l'objet d'un bad buzz ou d'un refus de contenu | Moyenne | Positionnement « confiance en soi et authenticité », règles anti-manipulation dans le prompt. |

### 1.4 Niveau de confiance
- **La demande existe et paie** : **élevée** (revenus vérifiés chez un concurrent).
- **Passer la review Apple** : **moyenne**, à cause de la règle 4.3(b).
- **Dépasser 1 k$/mois** : **faible à moyenne**, si la vidéo prend.
- **Dépasser 10 k$/mois** : **faible**. C'est un pari avec un potentiel élevé, pas une certitude.

---

## 2. Produit

### 2.1 Proposition de valeur
> « Ton coach de séduction en français : un meilleur profil, de meilleures accroches, des réponses qui te ressemblent. »

### 2.2 Fonctionnalités de la V1 (MVP, 4 à 5 semaines de développement)
1. **Répondre à un message** : l'utilisateur importe une capture d'écran de conversation. Le texte est extrait **sur l'appareil**, les prénoms sont masqués, et l'app propose 3 réponses dans des tons au choix (drôle, direct, romantique, décalé), avec **une ligne d'explication** (« pourquoi ça marche »). C'est la fonction virale.
2. **Accroche d'ouverture** : à partir des centres d'intérêt du match, que l'utilisateur tape ou extrait par OCR, l'app propose 3 premiers messages.
3. **Audit de mon profil** : l'utilisateur colle sa bio et ses prompts Hinge, et reçoit une note avec des réécritures. L'analyse des photos est réservée à la V2, à cause du coût et du risque de modération.
4. **Paywall dur avec essai de 3 jours** dès l'onboarding. Le taux de conversion essai → payant est de 10,7 % avec paywall dur, contre 2,1 % en freemium ([RevenueCat 2026](https://www.revenuecat.com/state-of-subscription-apps-2026/)) [SECONDAIRE].

**Hors V1, volontairement :** analyse de photos, clavier iOS personnalisé, coach en conversation libre. On ne les construit que si la traction est là.

### 2.3 Garde-fous de contenu (à inscrire dans le prompt système)
- Réservé aux **18 ans et plus** (classification d'âge App Store adaptée).
- Pas de messages sexuellement explicites, de pression, de manipulation ou d'insistance après un refus.
- Pas d'usurpation d'identité : les suggestions sont des propositions que l'utilisateur adapte.

---

## 3. Choix techniques

### 3.1 Architecture

```
iPhone/Android (Expo React Native)
   │  OCR sur l'appareil (Apple Vision / ML Kit)
   │  → texte anonymisé seulement
   ▼
Fonction serveur (Supabase Edge Function ou Cloudflare Worker)
   │  vérifie : utilisateur anonyme + abonnement actif (RevenueCat) + limite de requêtes
   │  détient la clé API (jamais dans l'app)
   ▼
API Claude (SDK officiel @anthropic-ai/sdk)
```

| Composant | Choix | Raison |
|---|---|---|
| App | **React Native + Expo** (TypeScript) | iOS et Android avec un seul code. Compilation iOS dans le cloud via EAS, donc pas besoin de Mac. |
| OCR | Sur l'appareil (Apple Vision / Google ML Kit, via un module Expo) | **RGPD** : on n'envoie que du texte, pas l'image, et ça réduit fortement le coût IA. |
| Backend | Une seule fonction serveur | La clé API reste côté serveur. Aucune base de conversations : **rien n'est stocké**. |
| Comptes | Identifiant anonyme RevenueCat, sans email | Minimisation des données et pas d'obligation de suppression de compte. |
| Paiements | **RevenueCat + StoreKit** | Gère les abonnements iOS et Android, l'essai, la restauration d'achat et les statistiques. |
| Analytique | TelemetryDeck ou PostHog en mode anonyme | Pas de traceur publicitaire, donc pas d'écran ATT. |

### 3.2 Modèle d'IA et coût par requête

Les tarifs officiels de l'API Claude (au 3 nov. 2026) sont :

| Modèle | Entrée $/M tokens | Sortie $/M tokens |
|---|---|---|
| **Claude Opus 5.5** (`claude-opus-5-5`, modèle par défaut recommandé) | 4,00 | 20,00 |
| Claude Haiku 5.5 (`claude-haiku-5-5`) | 0,10 | 0,50 |

**Estimation [HYPOTHÈSE]** pour une requête « 3 réponses » en texte seul : environ 1 500 tokens en entrée (instructions + conversation) et environ 800 en sortie (réflexion + réponses).
- **Opus 5.5** : ≈ 0,006 + 0,016 = **≈ 0,022 $ par requête**. Avec 100 requêtes par abonné et par mois, cela fait ≈ 2,20 $/mois, pour un abonnement autour de 8 à 9 €/mois. La marge reste correcte, mais elle est rognée de 25 à 30 %.
- **Haiku 5.5** : ≈ **0,0006 $ par requête**, soit environ 35 fois moins cher.

**Ma recommandation :** démarrer avec **Opus 5.5**, car en séduction la qualité et le naturel du français sont le produit lui-même. Le prompt système doit être mis en cache pour réduire le coût d'entrée, avec l'effort réglé sur `low` ou `medium`. **C'est à toi de décider** de passer à Haiku 5.5 après un test à l'aveugle sur 50 vraies conversations. Si la qualité se tient, la marge devient quasi totale.

Points techniques à respecter :
- Gérer le cas `stop_reason: "refusal"` (refus du modèle) avec le mécanisme de repli serveur (`fallbacks: "default"`).
- Mesurer les vrais tokens via `count_tokens` avant de fixer les prix.
- Plafonner l'usage, par exemple à 30 requêtes par jour et par abonné, pour éviter les abus.

### 3.3 Conformité RGPD (à faire valider)
- **Minimisation** : OCR local, masquage des prénoms, envoi du texte seul, **aucun stockage** côté serveur. Vérifier les conditions de conservation des données chez le fournisseur d'IA.
- **Consentement** : écran explicite « Le texte est envoyé à un service d'IA tiers (Anthropic) pour générer des suggestions », exigé par la règle Apple 5.1.2(i).
- **Données de tiers** : le message du match est une donnée personnelle. La base légale (intérêt légitime ?) et la mention d'information sont **à valider avec un juriste**. Je ne peux pas trancher ce point juridique.

---

## 4. Croissance (sans budget) : l'acquisition est le vrai projet

### 4.1 Le moteur : la vidéo courte « avant / après »
Format éprouvé chez les concurrents [SECONDAIRE] :
1. Capture d'une conversation **qui tombe à plat** (« Salut ça va ? » → « oui et toi »).
2. L'app propose une réponse drôle ou habile.
3. On montre (ou on met en scène) la réponse du match.
4. Texte à l'écran, musique tendance, **sans visage nécessaire**.

### 4.2 Le rythme (c'est l'engagement que tu prends)
- **2 à 3 comptes** TikTok et Instagram (par exemple « répliques », « coach », « histoires de dates »).
- **1 à 3 vidéos par jour pendant 8 semaines**, soit environ 100 à 150 vidéos au total. **Je génère les scripts, les conversations fictives et les textes. Toi, tu montes (CapCut) et tu publies.**
- Conversations **fictives** et clairement présentées comme des exemples. On ne publie jamais les vraies conversations d'utilisateurs.

### 4.3 Canaux complémentaires gratuits
- Les mots-clés de la fiche App Store (ASO) en français : « réponse tinder », « accroche hinge », « coach drague ».
- Une page web avec des articles qui se référencent sur Google (« comment répondre à… », « 50 accroches Hinge »).
- Reddit et forums francophones, en apportant de la valeur et sans spam.

### 4.4 Indicateurs et critères d'arrêt (fixés à l'avance)

| Indicateur | Référence | Seuil d'arrêt après 8 semaines |
|---|---|---|
| Vues cumulées | — | Moins de 200 k vues malgré plus de 100 vidéos → le format ne prend pas |
| Téléchargements | — | Moins de 1 000 |
| Essai → payant | 10,7 % de médiane avec paywall dur [SECONDAIRE] | Moins de 4 % → le produit ou le prix est à revoir |
| Note App Store | — | Moins de 4,0 → la qualité des réponses est insuffisante |

Si les seuils sont dépassés nettement (par exemple une vidéo à plus de 1 M de vues ou plus de 300 abonnés), on accélère : V2, puis réinvestissement d'une partie des revenus en publicités ciblées.

### 4.5 Scénarios de revenus (tout est hypothèse)

Hypothèses : revenu net moyen d'environ 6 € par abonné et par mois après Apple (15 %), TVA et coût IA ; abonnements surtout hebdomadaires et annuels.

| Scénario | Abonnés actifs à 6 mois | Revenu net mensuel |
|---|---|---|
| Échec (le plus probable) | moins de 30 | moins de 200 € |
| Moyen | 300 | ≈ 1 800 € |
| Succès | 3 000 | ≈ 18 000 € |

---

## 5. Plan de réalisation de A à Z

### Semaines 1–2 : valider avant de coder
| Action | Qui |
|---|---|
| Publier 15 à 20 vidéos de test (réponses générées à la main avec l'IA, sans app). **C'est le test le plus important** : si personne ne regarde, l'app ne servira à rien. | **Moi** pour les scripts, **toi** pour la publication |
| Page d'atterrissage avec liste d'attente (lien en bio) | **Moi** pour la page et les textes, **toi** pour la mise en ligne |
| Audit de 5 concurrents disponibles en France (prix, qualité du français, avis négatifs) | **Moi** pour la grille, **toi** pour tester sur ton téléphone |
| Consultation juridique courte sur le RGPD (données de tiers) | **Toi** |
| **Go / no-go** : plus de 50 k vues cumulées ou plus de 100 inscrits | ensemble |

### Semaines 3–6 : développement
1. Projet Expo, navigation, interface et accessibilité (**moi**).
2. Module OCR sur l'appareil et masquage des prénoms (**moi**).
3. Fonction serveur : vérification de l'abonnement, limite de requêtes, appel à Claude, gestion des refus (**moi**). **Toi** : créer la clé API Anthropic et le projet Supabase, puis les configurer comme secrets.
4. Prompt système en français, avec ton, garde-fous et explication pédagogique, plus un jeu de 50 conversations de test pour mesurer la qualité (**moi**). **Toi** : juger la qualité, car tu es le public cible.
5. Paywall, essai de 3 jours et RevenueCat (**moi**). **Toi** : créer les produits dans App Store Connect.
6. Onboarding, consentement IA (règle 5.1.2(i)), écran 18 ans et plus (**moi**).

### Semaines 6–7 : tests
- Tests automatisés du serveur (limites, abonnement expiré, refus du modèle) et de l'interface (**moi**).
- Achats en sandbox, bêta TestFlight avec 10 à 20 personnes de la liste d'attente (**toi**).
- Contrôle du coût réel par requête dans les journaux (**moi**).

### Semaines 7–8 : soumission
1. **Toi** : compte Apple Developer (99 €/an), Google Play (25 $), « Paid Apps Agreement », compte bancaire et fiscalité, **statut de commerçant (DSA)** obligatoire dans l'UE.
2. **Toi** : créer une **micro-entreprise**. Le choix du régime et de la TVA est à vérifier auprès de l'Urssaf ou d'un comptable.
3. **Moi** : fiche App Store en français (nom, sous-titre, mots-clés), captures d'écran, politique de confidentialité, conditions d'utilisation (à faire relire), réponses au formulaire « App Privacy ».
4. **Moi** : note à l'attention de l'équipe de review d'Apple, qui explique la **différenciation** (coaching francophone, pas une app de rencontre) pour anticiper la règle 4.3(b).
5. Catégorie suggérée : **Style de vie**, pas « Rencontres » [HYPOTHÈSE à tester].
6. En cas de rejet : je rédige la réponse et l'appel. Prévoir 1 à 3 allers-retours.

### Semaines 8–16 : croissance et décision
- Vidéos quotidiennes, mesure par rapport aux critères d'arrêt du §4.4, itérations sur le prompt selon les avis.
- Décision à la semaine 16 : **arrêt, pivot ou accélération** (V2 : analyse de photos, clavier iOS, Android si ce n'est pas encore fait).

---

## 6. Répartition des rôles

**Ce que je prends en charge :**
- Tout le code (app, serveur, tests), l'architecture et la configuration de build.
- Le prompt système, le jeu de test de qualité et le suivi des coûts.
- Les scripts vidéo, les conversations fictives et les textes des réseaux sociaux.
- La fiche App Store, la page web et les articles.
- Les brouillons de politique de confidentialité et de conditions d'utilisation.
- Les réponses aux rejets d'Apple.

**Ce qui relève de toi (non délégable) :**
- **Publier les vidéos chaque jour pendant 8 semaines.** C'est le facteur n°1 de réussite.
- Les comptes Apple, Google, Anthropic et Supabase, les paiements, ton identité et ton compte bancaire.
- La micro-entreprise et la fiscalité.
- La validation juridique (RGPD, conditions d'utilisation).
- Les tests sur un vrai téléphone et le jugement de la qualité des réponses.

**Budget estimé la première année** [HYPOTHÈSE] : Apple 99 € + Google environ 25 € + IA environ 20 à 50 € pendant les tests (puis payée par les revenus) + juriste 0 à 300 €, soit **environ 150 à 500 €**.

---

## 7. Points non vérifiés
- Les revenus de Rizz : les estimations divergent (300 k$ à 1,5 M$/mois) et aucune n'est auditée. Seul RizzGPT est vérifié, via TrustMRR.
- La part réelle d'organique et de payant dans la croissance des leaders.
- Le niveau de concurrence **en français**, mesuré sur la fiche de chaque app et non sur des agrégateurs.
- Le nombre de tokens réel par requête, à mesurer.
- Le texte exact actuel des règles Apple 4.3(b) et 5.1.2(i), à relire sur la page officielle avant soumission.
- Le cadre RGPD applicable aux données du match.

---

## Annexe : résumé de l'analyse initiale (v1)
Pistes écartées pour un développeur seul à petit budget :
- **Tracker de calories IA** : environ 46 800 apps sur le mot-clé, médiane de 2 857 installations.
- **Facturation électronique** : les leaders sont des Plateformes Agréées gratuites.
- **Code de la route** : la banque de questions n'est pas publique et les acteurs en place sont puissants.
- **Examen civique** : demande réelle (71 125 candidats au 26 mai 2026), mais plafond estimé à quelques milliers d'euros par an. Écarté parce que le potentiel est trop faible pour l'objectif.
- **Aviation, musique, randonnée, impression 3D** : contenu verrouillé, acteurs dominants ou absence de preuve de monétisation.

## Sources
- [TrustMRR, RizzGPT](https://trustmrr.com/startup/ai-dating-assistant-1) · [Adapty, Rizz](https://adapty.io/paywall-library/rizz/) · [Starter Story, Rizz](https://www.starterstory.com/rizz-breakdown) · [Shortimize](https://www.shortimize.com/blog/rizz-apps-b-roll-strategy-that-got-them-half-a-billion-views-on-tiktok) · [Stormy](https://stormy.ai/blog/rizz-app-viral-growth-hacking-lessons) · [AppGoblin](https://appgoblin.info/apps/6748056633)
- [BigIdeasDB](https://bigideasdb.com/how-to-build-an-app-that-makes-money) · [RevenueCat, State of Subscription Apps 2026](https://www.revenuecat.com/state-of-subscription-apps-2026/)
- [MacRumors, règles Apple juin 2026](https://macrumors.com/2026/06/09/app-store-guidelines-low-quality-apps/) · [Forums Apple, 4.3(b) et apps de rencontre](https://developer.apple.com/forums/thread/777838) · [TechCrunch, règle 5.1.2(i)](https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai)
- [Presse-citron, Hinge IA](https://www.presse-citron.net/comment-hinge-va-vous-aider-a-pecho-grace-a-sa-nouvelle-fonctionnalite-ia/) · [Rizz Up FR](https://apps.apple.com/fr/app/id6475344381) · [AI Wingman FR](https://apps.apple.com/fr/app/ai-wingman/id6458177920)
