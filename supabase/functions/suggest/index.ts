// Supabase Edge Function « suggest » (Deno).
// Flux : identifiant RevenueCat → abonnement actif ? → quota du jour → Claude → JSON.
// Aucune conversation n'est stockée ni journalisée.
import Anthropic from "@anthropic-ai/sdk";
import { generateSuggestions, RefusalError } from "../_shared/claude.ts";
import { OutputError, validateRequest, ValidationError } from "../_shared/core.ts";

const ENTITLEMENT = Deno.env.get("RC_ENTITLEMENT_ID") ?? "pro";
const DAILY_LIMIT = Number(Deno.env.get("DAILY_LIMIT") ?? "30");
const RC_SECRET = Deno.env.get("REVENUECAT_SECRET_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
// Mode développement : saute la vérification d'abonnement (ne JAMAIS activer en production).
const SKIP_ENTITLEMENT = Deno.env.get("DEV_SKIP_ENTITLEMENT") === "true";

const anthropic = new Anthropic(); // lit ANTHROPIC_API_KEY

function json(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
}

async function hasActiveEntitlement(appUserId: string): Promise<boolean> {
  if (SKIP_ENTITLEMENT) return true;
  const res = await fetch(
    `https://api.revenuecat.com/v1/subscribers/${encodeURIComponent(appUserId)}`,
    { headers: { Authorization: `Bearer ${RC_SECRET}` } },
  );
  if (!res.ok) return false;
  const data = await res.json();
  const ent = data?.subscriber?.entitlements?.[ENTITLEMENT];
  if (!ent) return false;
  // expires_date null = achat à vie ; sinon doit être dans le futur (essai inclus).
  return ent.expires_date === null || Date.parse(ent.expires_date) > Date.now();
}

/** Incrémente le compteur du jour ; false si le quota est dépassé. */
async function consumeQuota(appUserId: string): Promise<boolean> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/consume_quota`, {
    method: "POST",
    headers: {
      apikey: SERVICE_ROLE,
      Authorization: `Bearer ${SERVICE_ROLE}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ p_user_id: appUserId, p_limit: DAILY_LIMIT }),
  });
  if (!res.ok) throw new Error(`quota rpc ${res.status}`);
  return (await res.json()) === true;
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return json(405, { error: "method_not_allowed" });

  const appUserId = req.headers.get("x-app-user-id")?.trim() ?? "";
  if (!appUserId || appUserId.length > 128) return json(401, { error: "missing_user" });

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return json(400, { error: "invalid_json" });
  }

  try {
    const request = validateRequest(body);
    if (!(await hasActiveEntitlement(appUserId))) return json(402, { error: "subscription_required" });
    if (!(await consumeQuota(appUserId))) return json(429, { error: "daily_limit" });

    const result = await generateSuggestions(anthropic, request);
    // Journalise uniquement des métriques de coût, jamais le contenu.
    console.log(JSON.stringify({ event: "suggest", mode: request.mode, model: result.model, ...result.usage }));
    return json(200, result.response);
  } catch (err) {
    if (err instanceof ValidationError) return json(400, { error: "invalid_request", detail: err.message });
    if (err instanceof RefusalError) return json(422, { error: "refused" });
    if (err instanceof OutputError) return json(502, { error: "bad_model_output" });
    if (err instanceof Anthropic.RateLimitError) return json(503, { error: "busy" });
    if (err instanceof Anthropic.APIError) {
      console.error(JSON.stringify({ event: "anthropic_error", status: err.status }));
      return json(502, { error: "upstream" });
    }
    console.error(JSON.stringify({ event: "error", message: String(err) }));
    return json(500, { error: "internal" });
  }
});
