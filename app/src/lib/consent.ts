import { Platform } from "react-native";
import * as SecureStore from "expo-secure-store";

// Version du texte de consentement : l'incrémenter redemande le consentement.
const KEY = "consent_v1";

export async function hasConsent(): Promise<boolean> {
  if (Platform.OS === "web") return true;
  return (await SecureStore.getItemAsync(KEY)) === "yes";
}

export async function giveConsent(): Promise<void> {
  if (Platform.OS === "web") return;
  await SecureStore.setItemAsync(KEY, "yes");
}
