import { useState } from "react";
import { Linking, ScrollView, StyleSheet, Text } from "react-native";
import { Button, Muted } from "../components/ui";
import { restorePurchases } from "../lib/purchases";
import { useColors } from "../theme";

// À remplacer par les URL publiées (page web de Réplique).
const PRIVACY_URL = "https://example.com/confidentialite";
const TERMS_URL = "https://example.com/conditions";

export default function Settings() {
  const c = useColors();
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function restore() {
    setBusy(true);
    setStatus("");
    try {
      setStatus((await restorePurchases()) ? "Abonnement restauré ✓" : "Aucun abonnement actif trouvé.");
    } catch {
      setStatus("La restauration a échoué, réessaie.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.wrap}>
      <Text style={[styles.h2, { color: c.text }]}>Abonnement</Text>
      <Button variant="secondary" title="Restaurer mes achats" onPress={restore} loading={busy} />
      {status ? <Muted>{status}</Muted> : null}
      <Muted>Gère ou résilie ton abonnement dans les réglages de ton compte App Store ou Google Play.</Muted>

      <Text style={[styles.h2, { color: c.text }]}>Confidentialité</Text>
      <Muted>
        Les captures sont lues sur ton téléphone. Seul le texte, après masquage des prénoms et coordonnées,
        est envoyé au service d'IA Anthropic pour générer les suggestions. Réplique ne stocke pas tes conversations
        et ne demande ni compte ni email.
      </Muted>
      <Button variant="secondary" title="Politique de confidentialité" onPress={() => Linking.openURL(PRIVACY_URL)} />
      <Button variant="secondary" title="Conditions d'utilisation" onPress={() => Linking.openURL(TERMS_URL)} />
      <Muted>Réplique n'est affiliée à aucune application de rencontre. Réservé aux 18 ans et plus.</Muted>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  wrap: { padding: 20, gap: 12 },
  h2: { fontSize: 18, fontWeight: "700", marginTop: 8 },
});
