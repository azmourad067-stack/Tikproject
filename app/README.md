# Réplique : app mobile (Expo / React Native)

## Structure
```
src/app/          écrans (Expo Router) : onboarding, accueil, répondre, composer, réglages
src/components/   boutons, champs, cartes de résultats
src/hooks/        useSuggest (paywall → appel serveur → erreurs)
src/lib/          api, achats (RevenueCat), OCR (ML Kit), transcript (OCR→messages + anonymisation)
```
Serveur : `../supabase/functions/suggest` · Tests : `npm test` à la racine du dépôt.

## Lancer en local (aperçu web, sans OCR ni paiement)
```bash
cd app
npm install
cp .env.example .env.local   # renseigner EXPO_PUBLIC_API_URL au minimum
npx expo start --web
```
En mode développement sans clé RevenueCat, le paywall est ignoré. Côté serveur, il faut alors
`DEV_SKIP_ENTITLEMENT=true` (jamais en production).

## Tester sur ton iPhone (OCR + achats)
L'OCR (ML Kit) et RevenueCat sont des modules natifs : **Expo Go ne suffit pas**, il faut un
« development build » compilé dans le cloud par EAS (pas besoin de Mac) :
```bash
npm install -g eas-cli
eas login
eas build --profile development --platform ios
```
Installe le build sur ton iPhone (lien fourni par EAS), puis `npx expo start` et scanne le QR code.

⚠️ **Point à vérifier au premier build** : `@react-native-ml-kit/text-recognition` est un module
« ancienne architecture ». S'il ne se charge pas, l'app affiche un message et l'utilisateur peut saisir
les messages à la main. On remplacera alors le module (ex. `expo-text-extractor`).

## Avant la publication
- [ ] Remplacer `fr.replique.app` (app.json) par ton identifiant de bundle définitif.
- [ ] Remplacer l'icône et le splash (`assets/`).
- [ ] Renseigner les URL de confidentialité et de conditions (`src/app/settings.tsx`).
- [ ] Configurer RevenueCat : produits App Store, entitlement **`pro`**, offering avec un paywall.
