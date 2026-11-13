// Appel à l'API Claude. Le client est injecté pour pouvoir le simuler en test.
import Anthropic from "@anthropic-ai/sdk";
import {
  buildUserContent,
  MODEL,
  OUTPUT_SCHEMA,
  parseOutput,
  SYSTEM_PROMPT,
  type SuggestRequest,
  type SuggestResponse,
} from "./core.ts";

export class RefusalError extends Error {}

export interface SuggestResult {
  response: SuggestResponse;
  model: string;
  usage: { input: number; output: number; cacheRead: number };
}

export async function generateSuggestions(
  client: Anthropic,
  req: SuggestRequest,
): Promise<SuggestResult> {
  const message = await client.beta.messages.create({
    model: MODEL,
    max_tokens: 4000,
    // Si le modèle décline, l'API rejoue la requête sur le modèle de repli recommandé.
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    // Met en cache le prompt système (identique pour toutes les requêtes).
    cache_control: { type: "ephemeral" },
    output_config: {
      // Tâche courte : effort bas pour réduire coût et latence. À ajuster après l'éval.
      effort: "low",
      format: { type: "json_schema", schema: OUTPUT_SCHEMA as unknown as Record<string, unknown> },
    },
    system: SYSTEM_PROMPT,
    messages: [{ role: "user", content: buildUserContent(req) }],
  });

  if (message.stop_reason === "refusal") throw new RefusalError("Requête déclinée");

  const text = message.content
    .filter((b) => b.type === "text")
    .map((b) => (b as { text: string }).text)
    .join("");

  return {
    response: parseOutput(text),
    model: message.model,
    usage: {
      input: message.usage.input_tokens,
      output: message.usage.output_tokens,
      cacheRead: message.usage.cache_read_input_tokens ?? 0,
    },
  };
}
