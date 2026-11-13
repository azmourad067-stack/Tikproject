import { useState } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import * as Clipboard from "expo-clipboard";
import type { SuggestResponse, Tone } from "../lib/api";
import { useColors } from "../theme";

const TONE_LABEL: Record<Tone, string> = { drole: "😂 Drôle", direct: "😎 Direct", doux: "🌹 Doux" };

export function Results({ data }: { data: SuggestResponse }) {
  const c = useColors();
  const [copied, setCopied] = useState<number | null>(null);

  async function copy(i: number, text: string) {
    await Clipboard.setStringAsync(text);
    setCopied(i);
    setTimeout(() => setCopied((v) => (v === i ? null : v)), 1500);
  }

  return (
    <View style={{ gap: 12 }}>
      {data.coach_note ? (
        <View style={[styles.note, { borderColor: c.border, backgroundColor: c.surface }]}>
          <Text style={{ color: c.text, fontSize: 15, lineHeight: 21 }}>💡 {data.coach_note}</Text>
        </View>
      ) : null}
      {data.suggestions.map((s, i) => (
        <Pressable
          key={i}
          accessibilityRole="button"
          accessibilityHint="Copie la suggestion"
          onPress={() => copy(i, s.text)}
          style={({ pressed }) => [
            styles.card,
            { backgroundColor: c.ai, borderColor: c.aiBorder, opacity: pressed ? 0.85 : 1 },
          ]}
        >
          <View style={styles.row}>
            <Text style={[styles.tone, { color: c.muted }]}>{TONE_LABEL[s.tone]}</Text>
            <Text style={[styles.tone, { color: c.accent }]}>{copied === i ? "Copié ✓" : "Copier"}</Text>
          </View>
          <Text style={{ color: c.text, fontSize: 17, lineHeight: 24 }} selectable>{s.text}</Text>
          <Text style={{ color: c.muted, fontSize: 13, marginTop: 6 }}>Pourquoi ça marche : {s.why}</Text>
        </Pressable>
      ))}
      <Text style={{ color: c.muted, fontSize: 12, textAlign: "center" }}>
        Ce sont des suggestions : adapte-les pour qu'elles te ressemblent.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: { borderWidth: 1, borderStyle: "dashed", borderRadius: 16, padding: 14 },
  note: { borderWidth: 1, borderRadius: 14, padding: 12 },
  row: { flexDirection: "row", justifyContent: "space-between", marginBottom: 6 },
  tone: { fontSize: 13, fontWeight: "700" },
});
