import { useState } from "react";
import { Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { Results } from "../components/Results";
import { Button, ErrorText, Field, Muted } from "../components/ui";
import { useSuggest } from "../hooks/useSuggest";
import { anonymize, type Message } from "../lib/transcript";
import { useColors } from "../theme";

let nextId = 1000;

export default function Reply() {
  const c = useColors();
  const [messages, setMessages] = useState<Message[]>([]);
  const [names, setNames] = useState("");
  const [goal, setGoal] = useState("");
  const [reading, setReading] = useState(false);
  const [ocrError, setOcrError] = useState("");
  const { run, loading, error, data } = useSuggest();

  async function pickScreenshot() {
    setOcrError("");
    const res = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ["images"], quality: 1 });
    if (res.canceled || !res.assets[0]) return;
    const asset = res.assets[0];
    setReading(true);
    try {
      // Import dynamique : le module natif n'existe pas sur le web ni dans Expo Go.
      const { readConversation } = await import("../lib/ocr");
      const msgs = await readConversation(asset.uri, asset.width);
      if (msgs.length === 0) setOcrError("Aucun texte trouvé. Essaie une autre capture ou écris les messages.");
      setMessages(msgs);
    } catch {
      setOcrError("Lecture impossible sur cet appareil. Ajoute les messages à la main ci-dessous.");
    } finally {
      setReading(false);
    }
  }

  function update(id: string, patch: Partial<Message>) {
    setMessages((ms) => ms.map((m) => (m.id === id ? { ...m, ...patch } : m)));
  }

  function add(from: Message["from"]) {
    setMessages((ms) => [...ms, { id: String(nextId++), from, text: "" }]);
  }

  function submit() {
    const nameList = names.split(",");
    run({
      mode: "reply",
      messages: messages
        .filter((m) => m.text.trim())
        .map((m) => ({ from: m.from, text: anonymize(m.text, nameList) })),
      goal: anonymize(goal, nameList),
    });
  }

  const canSubmit = messages.some((m) => m.text.trim());

  return (
    <ScrollView contentContainerStyle={styles.wrap} keyboardShouldPersistTaps="handled">
      {Platform.OS !== "web" ? (
        <Button title={reading ? "Lecture…" : "📷 Importer une capture d'écran"} onPress={pickScreenshot} loading={reading} />
      ) : null}
      <ErrorText>{ocrError}</ErrorText>

      {messages.length > 0 ? (
        <Muted>Vérifie la conversation : touche « Moi / Match » pour corriger qui parle, et modifie le texte si besoin.</Muted>
      ) : (
        <Muted>Ou ajoute les messages à la main :</Muted>
      )}

      {messages.map((m) => (
        <View key={m.id} style={[styles.msgRow, m.from === "me" && { flexDirection: "row-reverse" }]}>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`Auteur : ${m.from === "me" ? "moi" : "match"}. Toucher pour changer`}
            onPress={() => update(m.id, { from: m.from === "me" ? "them" : "me" })}
            style={[styles.who, { borderColor: c.border }]}
          >
            <Text style={{ color: c.muted, fontSize: 12, fontWeight: "700" }}>{m.from === "me" ? "Moi" : "Match"}</Text>
          </Pressable>
          <TextInput
            value={m.text}
            onChangeText={(t) => update(m.id, { text: t })}
            multiline
            placeholder="Message…"
            placeholderTextColor={c.muted}
            style={[
              styles.bubble,
              m.from === "me"
                ? { backgroundColor: c.accent, color: c.accentText }
                : { backgroundColor: c.them, color: c.text },
            ]}
          />
          <Pressable accessibilityLabel="Supprimer le message" onPress={() => setMessages((ms) => ms.filter((x) => x.id !== m.id))} style={styles.del}>
            <Text style={{ color: c.muted, fontSize: 18 }}>×</Text>
          </Pressable>
        </View>
      ))}

      <View style={{ flexDirection: "row", gap: 10 }}>
        <View style={{ flex: 1 }}><Button variant="secondary" title="+ Match" onPress={() => add("them")} /></View>
        <View style={{ flex: 1 }}><Button variant="secondary" title="+ Moi" onPress={() => add("me")} /></View>
      </View>

      <Field
        label="Prénoms à masquer (séparés par des virgules)"
        value={names}
        onChangeText={setNames}
        placeholder="ex. Camille, Léo"
        autoCapitalize="words"
      />
      <Field
        label="Ton objectif (facultatif)"
        value={goal}
        onChangeText={setGoal}
        placeholder="ex. proposer un verre, relancer, faire rire"
        maxLength={200}
      />

      <Button title="Obtenir 3 réponses" onPress={submit} disabled={!canSubmit} loading={loading} />
      <ErrorText>{error}</ErrorText>
      {data ? <Results data={data} /> : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  wrap: { padding: 20, gap: 14, paddingBottom: 60 },
  msgRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  who: { borderWidth: 1, borderRadius: 10, paddingHorizontal: 8, paddingVertical: 10, minWidth: 56, alignItems: "center" },
  bubble: { flex: 1, borderRadius: 18, paddingHorizontal: 14, paddingVertical: 10, fontSize: 16 },
  del: { padding: 8, minWidth: 32, alignItems: "center" },
});
