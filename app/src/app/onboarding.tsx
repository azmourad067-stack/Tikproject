import { useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { router } from "expo-router";
import { Button, Muted } from "../components/ui";
import { giveConsent } from "../lib/consent";
import { useColors } from "../theme";

function Check(props: { checked: boolean; onToggle: () => void; children: string }) {
  const c = useColors();
  return (
    <Pressable
      accessibilityRole="checkbox"
      accessibilityState={{ checked: props.checked }}
      onPress={props.onToggle}
      style={styles.check}
    >
      <View style={[styles.box, { borderColor: c.accent, backgroundColor: props.checked ? c.accent : "transparent" }]}>
        {props.checked ? <Text style={{ color: c.accentText, fontWeight: "800" }}>✓</Text> : null}
      </View>
      <Text style={{ color: c.text, flex: 1, fontSize: 15, lineHeight: 21 }}>{props.children}</Text>
    </Pressable>
  );
}

export default function Onboarding() {
  const c = useColors();
  const [adult, setAdult] = useState(false);
  const [ai, setAi] = useState(false);

  async function start() {
    await giveConsent();
    router.replace("/");
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: c.bg }}>
      <ScrollView contentContainerStyle={styles.wrap}>
        <Text style={[styles.title, { color: c.text }]}>
          Ré<Text style={{ color: c.accent }}>plique</Text>
        </Text>
        <Text style={[styles.lead, { color: c.text }]}>
          Ton coach de séduction en français : de meilleures accroches, des réponses qui te ressemblent.
        </Text>

        <View style={[styles.card, { backgroundColor: c.surface, borderColor: c.border }]}>
          <Text style={[styles.h2, { color: c.text }]}>Comment tes données sont traitées</Text>
          <Muted>• Les captures d'écran sont lues sur ton téléphone. L'image n'est jamais envoyée.</Muted>
          <Muted>• Les prénoms que tu indiques, emails, numéros et liens sont masqués avant l'envoi.</Muted>
          <Muted>
            • Le texte restant est envoyé à un service d'IA tiers (Anthropic, Claude) uniquement pour générer
            les suggestions. Réplique ne conserve pas tes conversations.
          </Muted>
          <Muted>• Pas de compte, pas d'email, pas de publicité.</Muted>
        </View>

        <Check checked={adult} onToggle={() => setAdult(!adult)}>J'ai 18 ans ou plus.</Check>
        <Check checked={ai} onToggle={() => setAi(!ai)}>
          J'accepte que le texte que je soumets soit envoyé au service d'IA Anthropic pour générer des suggestions.
        </Check>

        <Button title="Commencer" onPress={start} disabled={!adult || !ai} />
        <Muted>Tu pourras retrouver ces informations dans les réglages.</Muted>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  wrap: { padding: 20, gap: 18 },
  title: { fontSize: 40, fontWeight: "800", letterSpacing: -1, marginTop: 24 },
  lead: { fontSize: 19, lineHeight: 27 },
  card: { borderWidth: 1, borderRadius: 16, padding: 16, gap: 8 },
  h2: { fontSize: 16, fontWeight: "700", marginBottom: 2 },
  check: { flexDirection: "row", gap: 12, alignItems: "flex-start", minHeight: 44 },
  box: { width: 26, height: 26, borderRadius: 7, borderWidth: 2, alignItems: "center", justifyContent: "center" },
});
