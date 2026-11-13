import { Platform } from "react-native";
import Purchases, { LOG_LEVEL } from "react-native-purchases";
import RevenueCatUI, { PAYWALL_RESULT } from "react-native-purchases-ui";
import { ENTITLEMENT_ID, REVENUECAT_API_KEY } from "./config";

let configured = false;

export function configurePurchases(): void {
  if (configured || Platform.OS === "web" || !REVENUECAT_API_KEY) return;
  if (__DEV__) Purchases.setLogLevel(LOG_LEVEL.WARN);
  // Sans appUserID : RevenueCat crée un identifiant anonyme (pas d'email, pas de compte).
  Purchases.configure({ apiKey: REVENUECAT_API_KEY });
  configured = true;
}

export function purchasesReady(): boolean {
  return configured;
}

export async function getUserId(): Promise<string> {
  if (!configured) return "dev-user";
  return Purchases.getAppUserID();
}

/**
 * Affiche le paywall RevenueCat si l'utilisateur n'a pas l'accès « pro ».
 * Renvoie true si l'accès est (désormais) actif.
 */
export async function ensureAccess(): Promise<boolean> {
  if (!configured) return __DEV__; // en dev sans clé RevenueCat, on laisse passer
  const result = await RevenueCatUI.presentPaywallIfNeeded({
    requiredEntitlementIdentifier: ENTITLEMENT_ID,
  });
  return (
    result === PAYWALL_RESULT.NOT_PRESENTED ||
    result === PAYWALL_RESULT.PURCHASED ||
    result === PAYWALL_RESULT.RESTORED
  );
}

export async function restorePurchases(): Promise<boolean> {
  if (!configured) return false;
  const info = await Purchases.restorePurchases();
  return ENTITLEMENT_ID in info.entitlements.active;
}
