import { API_URL, SUPABASE_ANON_KEY } from "./config";
import { getUserId } from "./purchases";

export type Mode = "reply" | "opener" | "profile";
export type Tone = "drole" | "direct" | "doux";

export interface Suggestion {
  tone: Tone;
  text: string;
  why: string;
}

export interface SuggestResponse {
  suggestions: Suggestion[];
  coach_note: string;
}

export interface SuggestPayload {
  mode: Mode;
  messages?: { from: "me" | "them"; text: string }[];
  context?: string;
  goal?: string;
}

export class ApiError extends Error {
  constructor(public code: string, message: string) {
    super(message);
  }
}

const MESSAGES: Record<string, string> = {
  subscription_required: "Ton essai ou ton abonnement n'est pas actif.",
  daily_limit: "Tu as atteint la limite du jour. Reviens demain !",
  refused: "Je ne peux pas aider sur ce message. Essaie de reformuler.",
  invalid_request: "Le texte envoyé n'est pas valide.",
  busy: "Beaucoup de demandes en ce moment, réessaie dans un instant.",
};

export async function suggest(payload: SuggestPayload): Promise<SuggestResponse> {
  if (!API_URL) throw new ApiError("config", "EXPO_PUBLIC_API_URL n'est pas configurée.");
  let res: Response;
  try {
    res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Clé publique Supabase (passerelle des Edge Functions), pas un secret.
        Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
        "x-app-user-id": await getUserId(),
      },
      body: JSON.stringify(payload),
    });
  } catch {
    throw new ApiError("network", "Pas de connexion. Vérifie ton réseau.");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const code = typeof data?.error === "string" ? data.error : "unknown";
    throw new ApiError(code, MESSAGES[code] ?? "Une erreur est survenue, réessaie.");
  }
  return data as SuggestResponse;
}
