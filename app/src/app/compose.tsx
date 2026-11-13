import { useState } from "react";
import { ScrollView, StyleSheet } from "react-native";
import { Stack, useLocalSearchParams } from "expo-router";
import { Results } from "../components/Results";
import { Button, ErrorText, Field, Muted } from "../components/ui";
import { useSuggest } from "../hooks/useSuggest";
import { anonymize } from "../lib/transcript";

const COPY = {
  opener: {
    title: "Premier message",
    label: "Ce que tu sais de ton match",
    placeholder: "ex. Adore la randonnée, photo avec un chien, prompt Hinge : « Mon dimanche idéal : brunch et expo »",
    help: "Décris son profil avec tes mots ou colle ses prompts. Évite son nom complet ou ses réseaux.",
    button: "Trouver 3 accroches",
  },
  profile: {
    title: "Améliorer mon profil",
    label: "Ta bio actuelle et/ou tes prompts",
    placeholder: "ex. 28 ans. J'aime les voyages, le sport et les sorties entre amis.",
    help: "Tu recevras 3 réécritures (drôle, directe, douce) qui gardent tes vrais centres d'intérêt.",
    button: "Réécrire mon profil",
  },
} as const;

export default function Compose() {
  const params = useLocalSearchParams<{ mode?: string }>();
  const mode = params.mode === "profile" ? "profile" : "opener";
  const copy = COPY[mode];
  const [context, setContext] = useState("");
  const { run, loading, error, data } = useSuggest();

  return (
    <ScrollView contentContainerStyle={styles.wrap} keyboardShouldPersistTaps="handled">
      <Stack.Screen options={{ title: copy.title }} />
      <Field
        label={copy.label}
        value={context}
        onChangeText={setContext}
        placeholder={copy.placeholder}
        multiline
        maxLength={1500}
      />
      <Muted>{copy.help}</Muted>
      <Button
        title={copy.button}
        onPress={() => run({ mode, context: anonymize(context, []) })}
        disabled={context.trim().length < 5}
        loading={loading}
      />
      <ErrorText>{error}</ErrorText>
      {data ? <Results data={data} /> : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({ wrap: { padding: 20, gap: 14, paddingBottom: 60 } });
