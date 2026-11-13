import { useEffect, useState } from "react";
import { Stack, router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { hasConsent } from "../lib/consent";
import { configurePurchases } from "../lib/purchases";
import { useColors } from "../theme";

export default function RootLayout() {
  const c = useColors();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    configurePurchases();
    hasConsent().then((ok) => {
      setChecked(true);
      if (!ok) router.replace("/onboarding");
    });
  }, []);

  return (
    <>
      <StatusBar style="auto" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: c.bg },
          headerTintColor: c.text,
          headerShadowVisible: false,
          contentStyle: { backgroundColor: c.bg },
          headerBackButtonDisplayMode: "minimal",
        }}
      >
        <Stack.Screen name="index" options={{ title: "Réplique", headerShown: checked }} />
        <Stack.Screen name="onboarding" options={{ headerShown: false, gestureEnabled: false }} />
        <Stack.Screen name="reply" options={{ title: "Répondre" }} />
        <Stack.Screen name="compose" options={{ title: "" }} />
        <Stack.Screen name="settings" options={{ title: "Réglages" }} />
      </Stack>
    </>
  );
}
