import { useState } from "react";
import { ApiError, suggest, type SuggestPayload, type SuggestResponse } from "../lib/api";
import { ensureAccess } from "../lib/purchases";

/** Vérifie l'accès (paywall si besoin), appelle le serveur, gère erreurs et chargement. */
export function useSuggest() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState<SuggestResponse | null>(null);

  async function run(payload: SuggestPayload) {
    setError("");
    setLoading(true);
    try {
      if (!(await ensureAccess())) {
        setError("Active ton essai gratuit pour obtenir des suggestions.");
        return;
      }
      setData(await suggest(payload));
    } catch (e) {
      if (e instanceof ApiError && e.code === "subscription_required") {
        // L'abonnement a expiré entre-temps : on repropose le paywall.
        if (await ensureAccess()) setData(await suggest(payload));
        else setError(e.message);
      } else {
        setError(e instanceof ApiError ? e.message : "Une erreur est survenue, réessaie.");
      }
    } finally {
      setLoading(false);
    }
  }

  return { run, loading, error, data, reset: () => setData(null) };
}
