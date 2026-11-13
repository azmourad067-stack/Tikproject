# Plan d'application mobile : analyse de marché, choix argumenté, plan de A à Z

*Rédigé le 13 novembre 2026. Les recherches web ont été faites le même jour.*

**Légende utilisée partout dans ce document :**
- **[DONNÉE]** : chiffre ou fait tiré d'une source citée.
- **[SECONDAIRE]** : chiffre repris par un blog ou un comparatif, pas vérifié à la source primaire.
- **[HYPOTHÈSE]** : mon estimation, à valider avant d'y engager de l'argent.

---

## 0. Hypothèses de départ retenues

Tu n'as pas précisé ton profil. J'ai donc retenu les hypothèses suivantes. Si l'une d'elles est fausse, une partie du plan change :

| Sujet | Hypothèse | Ce qui changerait si c'est faux |
|---|---|---|
| Budget | Moins de 1 000 € la première année, essentiellement le compte Apple (99 €/an) et éventuellement Google (25 $ une fois) | Avec plus de 5 à 10 k€ d'acquisition payante, des marchés plus concurrentiels deviennent jouables. |
| Niveau technique | Débutant ou intermédiaire. J'écris le code, tu le lances et tu le testes. | Avec un développeur iOS expérimenté, une app native en SwiftUI devient raisonnable. |
| Temps | Projet à côté d'une autre activité, 5 à 10 h par semaine | À plein temps, on peut viser plus large. |
| Localisation | France, francophone (ta question est en français) | Le choix final s'appuie sur un marché réglementaire français. |
| Statut | Pas encore de structure juridique | Il en faudra une pour vendre (voir §3.9). |

---

## 1. Analyse de marché avant toute décision

### 1.1 Le contexte général : l'argent existe, mais il est très concentré

- **[DONNÉE]** En 2025, les dépenses des consommateurs dans les apps hors jeux ont dépassé celles dans les jeux pour la première fois : environ 85,5 Md$ (+21 % sur un an) contre 81,8 Md$ pour les jeux. La catégorie « IA » a dépassé 5 Md$ ([TechCrunch, janv. 2026](https://techcrunch.com/2026/01/21/consumers-spent-more-on-mobile-apps-than-games-in-2025-driven-by-ai-app-adoption)).
- **[DONNÉE]** L'App Store a reçu environ 557 000 nouvelles soumissions en 2025, soit +24 %. C'est la première hausse notable depuis 2016 ([Appfigures](https://appfigures.com/resources/insights/20251205?f=2)). La concurrence s'intensifie, en grande partie à cause des apps générées avec l'IA.
- **[SECONDAIRE, d'après RevenueCat, State of Subscription Apps 2026]** :
  - Une app d'abonnement médiane gagne **environ 72 $/mois** un an après son lancement. Le top 10 % dépasse 2 574 $/mois ([tasu.ai](https://tasu.ai/library/how-much-money-do-subscription-apps-make), [ppc.land](https://ppc.land/the-app-middle-class-is-dying-and-revenuecats-data-shows-exactly-how-fast/)).
  - Seules **4,6 %** des nouvelles apps atteignent 10 k$/mois dans les deux ans ([RevenueCat](https://www.revenuecat.com/state-of-subscription-apps)).
  - Le taux de conversion essai → payant est de **10,7 % avec un paywall dur** contre **2,1 % en freemium** ([RevenueCat 2026](https://www.revenuecat.com/state-of-subscription-apps-2026/)).
  - Photo & Vidéo est la catégorie où la part de nouvelles apps dépassant 1 k$/mois est la plus élevée (21,4 %). Éducation, Productivité, Voyage, Shopping et Business sont les plus difficiles.

  Je n'ai pas pu ouvrir le rapport original, dont le domaine est bloqué par le réseau de la session. Ces chiffres viennent de reprises secondaires concordantes.

**Conclusion honnête de cette section :** la « certitude fondée sur des données » que tu demandes n'existe pas pour une app pas encore lancée. Les données disponibles disent au contraire que **le résultat le plus probable pour une nouvelle app est un revenu faible**. Une bonne idée ne peut qu'améliorer les probabilités. Le plan ci-dessous est donc construit pour **tester vite et à bas coût**, avec des critères d'arrêt chiffrés.

### 1.2 Les modèles de monétisation qui fonctionnent réellement

| Modèle | Quand il marche | Preuve ou limite |
|---|---|---|
| Abonnement avec paywall dur et essai | Besoin récurrent, valeur continue (santé, productivité, IA) | Conversion de 10,7 % contre 2,1 % en freemium [SECONDAIRE]. Apple exige une « valeur continue » pour les abonnements (règle 3.1.2). |
| Achat unique / accès limité dans le temps | Besoin ponctuel avec une échéance (examen, projet) | Les apps d'examen concurrentes vendent des accès « à vie » à 19,99–24,99 $ (fiche App Store de Francopass) [DONNÉE]. |
| Publicité | Très gros volumes, usage quotidien | Peu adaptée à un solo sans trafic : il faut des centaines de milliers d'utilisateurs actifs [HYPOTHÈSE]. |
| Freemium + IAP | Contenu découpable | Conversion plus faible. Utile pour l'ASO et le bouche-à-oreille. |

### 1.3 Les cinq opportunités examinées

#### A. Tracker de calories par photo avec IA (type Cal AI)
- **Pour** : la demande est prouvée. Cal AI aurait fait environ 30 à 40 M$ de revenus annuels avant d'être racheté ([Latka](https://getlatka.com/companies/calai.app)) [SECONDAIRE, chiffres incohérents entre sources].
- **Contre** : le marché est saturé. AppGoblin recense environ **46 800 apps** sur le mot-clé « calorie counter », avec une **médiane de 2 857 installations**, et les petits clones plafonnent à quelques centaines ou milliers d'installations ([AppGoblin via recherche](https://appgoblin.info/apps/6744978762/keywords/discovery)). Cal AI était une équipe financée (7 à 17 personnes), pas un solo. Le succès venait d'un marketing d'influence massif, pas du produit seul. Il faut aussi payer des coûts d'API IA à chaque photo. Enfin, Apple a retiré temporairement Cal AI en avril 2026 pour un parcours de facturation trompeur ([MacRumors](https://www.macrumors.com/2026/04/21/apple-cal-ai-app-store-removal)).
- **Verdict : rejeté.** Sans budget d'acquisition, une app de plus est invisible.

#### B. Facturation électronique pour micro-entrepreneurs (France)
- **Pour** : le moteur est réglementaire et le marché est grand. Environ 3,19 M de micro-entrepreneurs sont inscrits, dont environ 1,59 M économiquement actifs mi-2025 ([TPE Actu / Urssaf](https://tpeactu.fr/2026/01/29/auto-entrepreneurs-chiffre-affaires-urssaf-2025/)). La réception de factures électroniques est obligatoire depuis le 1er sept. 2026, et l'émission le sera le 1er sept. 2027 ([Dougs](https://www.dougs.fr/blog/facturation-electronique-auto-entrepreneur/)).
- **Contre, et c'est rédhibitoire** : il faut passer par une **Plateforme Agréée** immatriculée par la DGFiP, ce qui est hors de portée d'un solo. Les leaders sont déjà agréés et **gratuits** : Abby, avec un premier palier payant à environ 7,20 €/mois, et Tiime ([tool-advisor](https://tool-advisor.fr/logiciel-facturation/comparatif/plateforme-agreee-gratuite/)) [SECONDAIRE]. On ne gagne pas contre du gratuit et réglementé.
- **Verdict : rejeté.**

#### C. Révision du Code de la route (France)
- **Pour** : la demande est énorme et récurrente. Plus de 2,2 M de passages à l'examen théorique (ETG) en 2024 selon une réponse parlementaire ([Assemblée nationale](https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE4069.pdf)), avec un taux de réussite d'environ 50 % ([Ornikar](https://www.ornikar.com/code/taux-de-reussite-code-de-la-route)).
- **Contre** : la banque officielle de questions n'est **pas publique**. Il faudrait produire plus de 1 000 questions avec des photos et vidéos de situations réelles, ce qui est coûteux et risqué juridiquement. Les incumbents (Ornikar, Stych, Codes Rousseau, En Voiture Simone) sont puissants et vendent le code avec les heures de conduite.
- **Verdict : rejeté** pour un démarrage à petit budget.

#### D. Préparation à l'examen civique et au niveau de français exigé pour les titres de séjour et la naturalisation (France)
- **Pour** :
  - **Nouvelle obligation légale [DONNÉE]** : depuis le 1er janvier 2026, un examen civique (QCM de 40 questions, 80 % requis) est obligatoire pour la première carte pluriannuelle, la carte de résident et la naturalisation ([Service-Public](https://www.service-public.gouv.fr/particuliers/actualites/A18713?lang=fr), [Assemblée nationale](https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE11488)).
  - **Demande mesurée par une source officielle [DONNÉE]** : **71 125 personnes** ont passé l'examen au 26 mai 2026, dans 444 centres, avec 81 % de réussite (même réponse ministérielle). Cela fait environ **170 000 candidats par an** en extrapolant [HYPOTHÈSE : rythme constant].
  - **Les exigences de français ont augmenté au même moment [SECONDAIRE]** : A2 pour la carte pluriannuelle (aucun niveau auparavant), B1 pour la carte de résident (A2 auparavant), B2 pour la naturalisation (B1 auparavant), à prouver par DELF, TCF IRN ou TEF IRN ([Digischool](https://www.digischool.fr/articles/fle/niveau-de-francais-naturalisation-2026/), [integrationfrance](https://www.integrationfrance.fr/articles/niveau-francais-a2-b1-b2-titre-sejour)). Ce besoin est plus difficile, plus long à préparer et vaut plus cher que l'examen civique.
  - **Contenu réutilisable [DONNÉE, licence à vérifier]** : le ministère publie les listes officielles de questions (191 pour la carte pluriannuelle, 209 pour la carte de résident, environ 258 pour la naturalisation), y compris sur **data.gouv.fr** ([dataset CSP](https://www.data.gouv.fr/datasets/examen-civique-csp)). Les mises en situation ne sont pas publiées. Le coût de contenu est donc faible.
  - **Concurrence App Store encore immature [DONNÉE]** : les apps trouvées (« Examen Civique Français 2026 », Francopass, « Mon Test Civique »…) ont **0 ou 1 note** sur leur fiche ([App Store](https://apps.apple.com/us/app/-/id6759701806), [AppGoblin](https://appgoblin.info/apps/6757424625)). Aucun leader ne s'est encore imposé sur iOS.
- **Contre** :
  - **Une concurrence gratuite existe** sur le web (integrationfrance.fr se présente comme « 100 % gratuit », plus prepacivique, Digischool…) et les questions officielles sont publiques. On ne peut donc pas vendre « les questions ». Il faut vendre l'**efficacité** : explications, traduction, entraînement ciblé, préparation au français.
  - **Un taux de réussite élevé (81 %) réduit l'anxiété**, et donc la disposition à payer pour le seul module civique.
  - **Le besoin est ponctuel** : on achète, on réussit, on part. C'est un achat unique ou un accès de 3 mois, pas un abonnement durable. Le revenu à vie par client est donc plafonné.
  - **Le marché est petit** : de l'ordre de 170 k candidats par an pour le civique, ce qui est loin d'un marché de masse.
  - **Le risque politique est réel** : les règles peuvent encore changer (report, modification du format).
- **Verdict : meilleur rapport preuves/coût, mais plafond modeste.** Voir §2.

#### E. Utilitaire Photo & Vidéo générique
- **Pour** : c'est la catégorie où la part d'apps dépassant 1 k$/mois est la plus forte (21,4 %) [SECONDAIRE].
- **Contre** : cette statistique concerne une catégorie, pas une idée. Je n'ai **aucune idée précise** que je puisse adosser à des données. La catégorie est aussi dominée par de gros éditeurs qui investissent en acquisition payante.
- **Verdict : non retenu**, faute de preuve spécifique. Ce serait de l'enthousiasme, pas des données.

### 1.4 Tableau comparatif

| Critère | A. Calories IA | B. Facturation | C. Code route | D. Civique + FLE | E. Photo |
|---|---|---|---|---|---|
| Demande prouvée | ✅ forte | ✅ forte | ✅ très forte | ✅ mesurée par l'État | ⚠️ catégorie seulement |
| Concurrence pour un solo | ❌ saturée | ❌ gratuite et agréée | ❌ incumbents puissants | ✅ immature sur iOS, ⚠️ gratuite sur le web | ❌ |
| Coût du contenu ou de la tech | ⚠️ API IA | ❌ réglementaire | ❌ médias coûteux | ✅ données ouvertes | ⚠️ |
| Disposition à payer | ✅ | ⚠️ | ✅ | ⚠️ civique / ✅ français B1-B2 | ? |
| Taille du marché | grande | grande | grande | **petite** | grande |
| Faisable avec moins de 1 k€ | ❌ | ❌ | ❌ | ✅ | ⚠️ |

---

## 2. Délibération et choix argumenté

### 2.1 Recommandation

**Je recommande l'idée D, mais sous forme d'expérience à petit coût avec des critères d'arrêt, et pas comme un pari « à fort potentiel ».**

Produit : **une app iOS (et Android) de préparation aux exigences d'intégration de 2026**, construite en deux étapes :
1. **V1 (examen civique)** : les questions officielles par parcours (carte pluriannuelle, carte de résident, naturalisation), des explications claires, **la traduction des explications** (arabe, anglais, espagnol, portugais, turc, etc. [HYPOTHÈSE sur les langues à prioriser, à confirmer avec les statistiques de titres de séjour par nationalité]), la répétition espacée sur les questions ratées et des examens blancs chronométrés de 40 questions en 45 minutes.
2. **V2 (français A2/B1/B2 pour TCF/TEF IRN)**, **seulement si la V1 valide la traction**. C'est là que se trouvent la disposition à payer et la durée d'usage. C'est aussi beaucoup plus de travail, et la concurrence y est plus sérieuse (TV5Monde gratuit, organismes de formation).

### 2.2 Pourquoi D l'emporte

1. **C'est la seule option dont la demande est mesurée par une source officielle** (71 125 candidats en 5 mois) et **créée par la loi**, donc non dépendante d'une mode.
2. **C'est la seule où un solo sans budget n'affronte pas de leader iOS installé** : les fiches concurrentes n'ont presque pas d'avis.
3. **Le contenu de base est en données ouvertes**, donc la V1 coûte très peu à produire.
4. **Le public a un besoin linguistique réel** (non-francophones), ce qui donne un angle de différenciation concret, la traduction des explications, que les sites gratuits ne couvrent pas tous [HYPOTHÈSE à vérifier en auditant 5 concurrents].
5. **Le recherche par mot-clé est naturelle** (« examen civique », « naturalisation », « carte de résident ») : l'ASO peut suffire sans publicité [HYPOTHÈSE].

### 2.3 Ordre de grandeur des revenus (scénarios, tout est hypothèse)

Prix supposé : 12,99 € pour un accès complet (achat unique), soit environ 9,20 € nets après 15 % de commission Apple (Small Business Program) et la TVA d'environ 20 %.

| Scénario | Téléchargements/an | Conversion payante | Revenu net/an |
|---|---|---|---|
| Pessimiste | 3 000 | 3 % | ≈ 830 € |
| Central | 15 000 | 6 % | ≈ 8 300 € |
| Optimiste (V1 + module français) | 40 000 | 8 % à prix moyen plus élevé (≈ 20 € net) | ≈ 64 000 € |

Le scénario central suppose de capter environ 9 % des candidats annuels en téléchargements. C'est ambitieux, mais plausible si l'app est n°1 sur ses mots-clés [HYPOTHÈSE].

### 2.4 Niveau de confiance

- **Que la demande existe** : **élevée**, grâce à la source officielle.
- **Qu'une app bien faite soit rentable au-delà de ses coûts (< 1 k€/an)** : **moyenne**.
- **Que ce soit une app « à fort potentiel » (> 10 k€/mois)** : **faible**. Je te le dis franchement : **aucune des idées étudiées ne mérite une confiance élevée sur ce critère** pour un solo à petit budget. D est le meilleur pari *ajusté au risque*, pas une certitude de gros revenus.

### 2.5 Risques qui invalideraient la conclusion

1. **Les sites gratuits suffisent aux candidats.** Test : moins de 2 % de conversion sur les 1 000 premiers téléchargements.
2. **Un concurrent bien financé** (Digischool, Ornikar-like, un organisme de FLE) lance une app soignée et prend le top des recherches.
3. **Un changement réglementaire** (report, suppression, modification du QCM).
4. **La licence des données ouvertes n'autorise pas la réutilisation commerciale.** Je pense qu'il s'agit de la Licence Ouverte Etalab, qui l'autorise avec attribution, mais **je ne l'ai pas vérifié** : c'est la première chose à contrôler.
5. **Un rejet Apple pour « spam » (règle 4.3)**, puisque beaucoup d'apps similaires existent déjà. La différenciation doit être visible dès les captures d'écran.

### 2.6 Critères d'arrêt (à fixer *avant* de lancer)

- 8 semaines après la publication : **moins de 500 téléchargements organiques** ou **conversion inférieure à 2 %** → on arrête ou on pivote.
- Plus de 5 % de conversion et des avis positifs → on lance la V2 (module français).

---

## 3. Plan de réalisation de A à Z

### 3.1 Validation avant de coder (semaines 1–2, quasiment gratuit)

| Action | Qui |
|---|---|
| Vérifier la licence du dataset data.gouv.fr et l'origine exacte des listes (ministère) | **Toi** (lecture) avec mon aide pour l'interprétation |
| Auditer 5 apps concurrentes et 3 sites gratuits (fonctions, prix, avis, langues) | **Moi** pour la grille d'analyse, **toi** pour installer et tester sur un iPhone |
| Analyser 30 à 50 avis et posts (Reddit r/france/r/expats, groupes Facebook d'expatriés, forums) pour repérer les frustrations | **Moi** (synthèse) et **toi** (accès aux groupes privés) |
| Page d'atterrissage avec liste d'attente, et 1 ou 2 posts dans des groupes communautaires | **Moi** (page et textes) et **toi** (publication) |
| Seuil de passage : plus de 100 inscrits en liste d'attente ou des signaux qualitatifs forts | ensemble |

### 3.2 Conception produit (semaine 2)

- **Parcours** : choix du titre visé → test de positionnement de 10 questions → entraînement par thème → examens blancs → tableau de « prêt pour l'examen ».
- **Gratuit** : environ 30 questions et 1 examen blanc, pour montrer la valeur et alimenter les avis.
- **Payant** : toutes les questions des 3 parcours, les examens illimités, les explications traduites, la révision des erreurs et l'audio (lecture des questions).
- **Mises en situation** : elles ne sont pas publiées par le ministère. On rédige des exemples *originaux*, clairement présentés comme tels.
- **Avertissement visible** : « Application indépendante, non affiliée au Ministère de l'Intérieur ».

### 3.3 Choix techniques

| Composant | Choix | Raison |
|---|---|---|
| Framework | **React Native + Expo** (TypeScript) | Un seul code pour iOS et Android. Le public visé utilise probablement beaucoup Android [HYPOTHÈSE]. La compilation iOS se fait dans le cloud via EAS, donc **tu n'as pas forcément besoin d'un Mac**. |
| Données | Banque de questions en JSON embarquée dans l'app | Fonctionne hors-ligne, sans serveur, coût nul |
| Progression | Stockage local (SQLite ou MMKV) | Pas de compte, donc pas de données personnelles sensibles |
| Paiements | **StoreKit via RevenueCat** (gratuit jusqu'à 2 500 $/mois de revenu suivi [SECONDAIRE, à vérifier]) | Gère iOS et Android, les restaurations d'achat et les reçus |
| Analytique | TelemetryDeck ou PostHog, en mode anonyme | Compatible RGPD, sans traceur publicitaire, donc pas d'écran ATT |
| Traductions | Rédigées avec l'IA puis **relues par des locuteurs natifs** | Une erreur de traduction sur un sujet juridique détruit la confiance |
| Backend | **Aucun en V1** | Moins de coûts, moins de failles, moins d'obligations légales |

**Point de vigilance RGPD** : un utilisateur de l'app révèle implicitement qu'il est étranger en démarche de séjour. **On ne collecte ni compte, ni nationalité, ni titre de séjour.** C'est un choix de conception délibéré.

### 3.4 Développement (semaines 3–6)

1. Initialiser le projet Expo, la navigation, le thème, l'accessibilité et les grandes polices (**moi**).
2. Script d'import qui transforme le dataset officiel en JSON versionné, avec contrôle d'intégrité (**moi**).
3. Moteur de quiz : tirage pondéré par thème, minuterie de 45 minutes, score sur 80 %, répétition espacée (**moi**).
4. Écrans : accueil, choix de parcours, entraînement, examen blanc, résultats, révision, paywall, réglages (**moi**).
5. Intégration RevenueCat et du produit non-consumable « Accès complet » (**moi** pour le code, **toi** pour créer le produit dans App Store Connect).
6. Rédaction des explications et des mises en situation originales (**moi** pour les brouillons, **toi** ou un relecteur pour la validation).
7. Traductions et relecture native (**moi** pour les brouillons, **toi** pour trouver 2 à 3 relecteurs, par exemple sur Malt, Fiverr ou dans ton réseau).

### 3.5 Tests (semaines 6–7)

- **Tests unitaires** du moteur de quiz et du calcul de score (**moi**).
- **Tests de bout en bout** des parcours clés, y compris l'achat en sandbox (**moi** pour l'écriture, **toi** pour l'exécution sur appareil).
- **Bêta TestFlight** avec 10 à 20 vrais candidats recrutés via la liste d'attente (**toi**).
- **Contrôle du contenu** : aucune réponse officielle erronée. Une erreur sur une question officielle est l'avis 1 étoile assuré.

### 3.6 Monétisation

- **Achat unique** « Accès complet » à 12,99 € (à tester entre 9,99 et 19,99 €). **Pas d'abonnement en V1** : le besoin est ponctuel, et un abonnement sur un besoin ponctuel génère des remboursements et de mauvais avis [HYPOTHÈSE cohérente avec les prix des concurrents].
- Paywall affiché après le test de positionnement, au moment où l'utilisateur voit ses lacunes.
- Inscription au **Small Business Program** d'Apple : commission de **15 %** au lieu de 30 % sous 1 M$ de revenu annuel.
- V2 : pack « Français B1/B2 » vendu séparément ou en bundle.

### 3.7 Conformité App Store (règles à respecter)

| Règle Apple | Ce qu'elle implique ici |
|---|---|
| 3.1.1 Achats intégrés | Le contenu numérique doit être vendu via IAP, pas de paiement externe (sauf exceptions régionales UE à étudier plus tard). |
| 2.3 Métadonnées exactes | Ne pas laisser penser à une app officielle : pas de logo Marianne ni de « officiel » dans le nom. |
| 4.3 Spam / clones | Montrer la différenciation (traductions, parcours) dans les captures et la description. |
| 5.1.1 Confidentialité | Politique de confidentialité obligatoire, « App Privacy » remplie honnêtement. Sans comptes, pas d'obligation de suppression de compte. |
| 5.2 Propriété intellectuelle | Respecter la licence des données publiques avec attribution, et n'utiliser aucun contenu copié chez un concurrent. |
| DSA (UE) | Déclarer le **statut de commerçant** dans App Store Connect. Ton adresse et ton contact seront affichés publiquement dans l'UE. |

### 3.8 Soumission et déploiement (semaines 7–8)

1. **Toi** : créer le compte Apple Developer (99 €/an) avec une pièce d'identité, puis le compte Google Play (25 $).
2. **Toi** : renseigner les accords, la fiscalité et le compte bancaire dans App Store Connect (« Paid Apps Agreement »). Sans cela, aucun achat intégré ne fonctionne.
3. **Moi** : préparer la fiche App Store (nom, sous-titre et mots-clés optimisés pour l'ASO, description en FR, EN et AR…), les captures d'écran (générées depuis le simulateur avec des cadres) et la politique de confidentialité.
4. **Moi** : configurer EAS Build et Submit (`eas build`, `eas submit`). **Toi** : lancer les commandes avec tes identifiants.
5. Soumission en review. Il faut compter 1 à 3 jours, et prévoir une éventuelle réponse à un rejet (**moi** pour rédiger la réponse).
6. Lancement : posts communautaires, page web avec SEO sur « examen civique » (**moi** pour le contenu, **toi** pour la diffusion).

### 3.9 Ce qui relève de toi (non délégable)

- **Créer une structure pour vendre.** Une micro-entreprise suffit au départ. Vérifie le régime (BNC ou BIC) et la TVA avec l'Urssaf ou un comptable. **Je ne suis pas qualifié pour te donner un avis fiscal définitif.**
- Comptes Apple et Google, paiements, identité, coordonnées bancaires.
- Validation juridique de la licence des données et de l'avertissement de non-affiliation. Une consultation courte avec un juriste est recommandée si le budget le permet.
- Relecture native des traductions.
- Tests sur un iPhone réel et publication dans les communautés.

### 3.10 Ce que je prends en charge

- Tout le code de l'app (Expo/TypeScript), les tests, les scripts d'import de données et la configuration de build.
- L'architecture, les choix de librairies et l'intégration RevenueCat.
- Les textes : explications, onboarding, paywall, fiche App Store, politique de confidentialité (à faire valider), page web.
- Les brouillons de traduction, les icônes et captures d'écran (assets simples ; un graphiste fera mieux pour l'icône finale).
- Les réponses aux rejets App Store et le suivi des métriques par rapport aux critères d'arrêt.

### 3.11 Calendrier indicatif (5 à 10 h par semaine)

| Semaines | Étape |
|---|---|
| 1–2 | Validation (licence, concurrents, liste d'attente) puis décision go/no-go |
| 3–6 | Développement de la V1 et du contenu |
| 6–7 | Tests et bêta TestFlight |
| 7–8 | Soumission et lancement |
| 9–16 | Mesure par rapport aux critères d'arrêt, puis décision sur la V2 « Français » |

---

## 4. Ce que je n'ai pas pu vérifier

- Le **rapport RevenueCat original** et les pages TechCrunch n'ont pas pu être ouverts depuis cette session (accès réseau bloqué). Leurs chiffres viennent de reprises secondaires concordantes.
- **La licence exacte** du dataset data.gouv.fr de l'examen civique.
- **Les revenus réels** des apps concurrentes sur ce créneau. Aucune donnée publique fiable n'existe, et les fiches ont trop peu d'avis pour estimer quoi que ce soit.
- **La répartition iOS/Android** du public visé et ses langues prioritaires.
- Le chiffre de 81 % de réussite (source parlementaire) contredit les 72 % avancés par des sites commerciaux. J'ai retenu la source officielle.

## Sources

- [TechCrunch, dépenses apps vs jeux 2025](https://techcrunch.com/2026/01/21/consumers-spent-more-on-mobile-apps-than-games-in-2025-driven-by-ai-app-adoption)
- [Appfigures, soumissions App Store 2025](https://appfigures.com/resources/insights/20251205?f=2)
- [RevenueCat, State of Subscription Apps 2026](https://www.revenuecat.com/state-of-subscription-apps-2026/) · [tasu.ai](https://tasu.ai/library/how-much-money-do-subscription-apps-make) · [ppc.land](https://ppc.land/the-app-middle-class-is-dying-and-revenuecats-data-shows-exactly-how-fast/)
- [Latka, Cal AI](https://getlatka.com/companies/calai.app) · [MacRumors, retrait de Cal AI](https://www.macrumors.com/2026/04/21/apple-cal-ai-app-store-removal) · [AppGoblin](https://appgoblin.info/apps/6744978762/keywords/discovery)
- [Dougs, facturation électronique](https://www.dougs.fr/blog/facturation-electronique-auto-entrepreneur/) · [TPE Actu, micro-entrepreneurs 2025](https://tpeactu.fr/2026/01/29/auto-entrepreneurs-chiffre-affaires-urssaf-2025/) · [tool-advisor, plateformes agréées gratuites](https://tool-advisor.fr/logiciel-facturation/comparatif/plateforme-agreee-gratuite/)
- [Assemblée nationale, ETG 2024](https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE4069.pdf) · [Ornikar, taux de réussite](https://www.ornikar.com/code/taux-de-reussite-code-de-la-route)
- [Service-Public, examen civique](https://www.service-public.gouv.fr/particuliers/actualites/A18713?lang=fr) · [Assemblée nationale, modalités et chiffres de l'examen civique](https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE11488) · [data.gouv.fr, Examen civique CSP](https://www.data.gouv.fr/datasets/examen-civique-csp) · [France Éducation International](https://france-education-international.fr/examen-civique/examen-civique-informations-pour-les-candidats)
- [Digischool, niveau de français 2026](https://www.digischool.fr/articles/fle/niveau-de-francais-naturalisation-2026/) · [integrationfrance](https://www.integrationfrance.fr/articles/niveau-francais-a2-b1-b2-titre-sejour)
- Fiches App Store concurrentes : [Examen Civique Français 2026](https://apps.apple.com/us/app/-/id6759701806) · [Mon Test Civique](https://apps.apple.com/fr/app/id6758161534) · [AppGoblin, Examen Civique Français](https://appgoblin.info/apps/6757424625)
