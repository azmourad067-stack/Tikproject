import { Platform } from "react-native";

// Valeurs publiques, injectées au build via des variables EXPO_PUBLIC_* (voir app/README.md).
// Aucune clé secrète ici : la clé Anthropic et la clé secrète RevenueCat restent côté serveur.
export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "";
export const SUPABASE_ANON_KEY = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY ?? "";
export const REVENUECAT_API_KEY =
  Platform.OS === "ios"
    ? (process.env.EXPO_PUBLIC_RC_IOS_KEY ?? "")
    : (process.env.EXPO_PUBLIC_RC_ANDROID_KEY ?? "");
export const ENTITLEMENT_ID = "pro";
