# Serveur Réplique (Supabase Edge Function)

`functions/suggest` reçoit le texte anonymisé, vérifie l'abonnement RevenueCat et le quota du jour,
appelle Claude (Opus 5.5) et renvoie 3 suggestions. **Aucune conversation n'est stockée ni journalisée**,
seulement les compteurs de tokens (coût) et un compteur d'usage quotidien.

## Mise en place (à faire par toi, une fois)
1. Crée un projet sur [supabase.com](https://supabase.com) (offre gratuite), région **UE** (RGPD).
2. Installe la CLI et lie le projet :
   ```bash
   npx supabase login
   npx supabase link --project-ref <ref-du-projet>
   npx supabase db push            # applique migrations/…_usage_quota.sql
   ```
3. Crée une clé API sur [platform.claude.com](https://platform.claude.com) et fixe une **limite de dépense mensuelle**.
4. Enregistre les secrets (jamais dans le code ni dans l'app) :
   ```bash
   npx supabase secrets set ANTHROPIC_API_KEY=... REVENUECAT_SECRET_KEY=... DAILY_LIMIT=30 RC_ENTITLEMENT_ID=pro
   ```
5. Déploie :
   ```bash
   npx supabase functions deploy suggest
   ```
6. URL à mettre dans l'app : `https://<ref>.supabase.co/functions/v1/suggest`.

## Avant d'ouvrir au public : tester la qualité
Depuis la racine du dépôt :
```bash
ANTHROPIC_API_KEY=... npm run eval
```
Le script génère `eval/results-<date>.md` avec les 22 cas et le **coût réel par requête**.
Note chaque cas de 1 à 5. Les cas sensibles (refus, mineur, contenu explicite, injection) doivent
tous être gérés respectueusement avant le lancement. On pourra ensuite comparer avec Claude Haiku 5.5
(environ 35 fois moins cher) : c'est ta décision, sur la base de ces résultats.

## Limites connues (MVP)
- L'identifiant utilisateur est l'ID anonyme RevenueCat envoyé par l'app : quelqu'un qui connaîtrait
  l'ID d'un abonné pourrait consommer son quota. Le risque est faible (UUID aléatoire) ; à renforcer
  plus tard avec App Attest / Play Integrity.
- Purge des compteurs : planifier `select public.purge_daily_usage();` chaque jour (pg_cron).
