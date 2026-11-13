import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { Link, router } from "expo-router";
import { useColors } from "../theme";

const ACTIONS = [
  { href: "/reply", emoji: "💬", title: "Répondre à une conv'", desc: "Importe une capture, reçois 3 réponses." },
  { href: "/compose?mode=opener", emoji: "👋", title: "Premier message", desc: "Une accroche à partir de son profil." },
  { href: "/compose?mode=profile", emoji: "✨", title: "Améliorer mon profil", desc: "Ta bio et tes prompts réécrits." },
] as const;

export default function Home() {
  const c = useColors();
  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={[styles.h1, { color: c.text }]}>Qu'est-ce qu'on écrit aujourd'hui ?</Text>
      {ACTIONS.map((a) => (
        <Pressable
          key={a.href}
          accessibilityRole="button"
          onPress={() => router.push(a.href)}
          style={({ pressed }) => [
            styles.card,
            { backgroundColor: c.surface, borderColor: c.border, opacity: pressed ? 0.85 : 1 },
          ]}
        >
          <Text style={styles.emoji}>{a.emoji}</Text>
          <View style={{ flex: 1 }}>
            <Text style={[styles.title, { color: c.text }]}>{a.title}</Text>
            <Text style={{ color: c.muted, fontSize: 14 }}>{a.desc}</Text>
          </View>
        </Pressable>
      ))}
      <Link href="/settings" style={{ color: c.muted, textAlign: "center", padding: 12 }}>
        Réglages et confidentialité
      </Link>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  wrap: { padding: 20, gap: 14 },
  h1: { fontSize: 26, fontWeight: "800", letterSpacing: -0.5, marginBottom: 6 },
  card: { flexDirection: "row", gap: 14, alignItems: "center", borderWidth: 1, borderRadius: 18, padding: 18 },
  emoji: { fontSize: 30 },
  title: { fontSize: 17, fontWeight: "700", marginBottom: 2 },
});
