import { test } from "node:test";
import assert from "node:assert/strict";
import Anthropic from "@anthropic-ai/sdk";
import {
  buildUserContent,
  OutputError,
  parseOutput,
  scrubPII,
  SYSTEM_PROMPT,
  validateRequest,
  ValidationError,
} from "./core.ts";
import { generateSuggestions, RefusalError } from "./claude.ts";

test("validateRequest accepte une conversation valide et retire les messages vides", () => {
  const r = validateRequest({
    mode: "reply",
    messages: [{ from: "me", text: " Salut " }, { from: "them", text: "" }],
  });
  assert.deepEqual(r, { mode: "reply", messages: [{ from: "me", text: "Salut" }], context: "", goal: "" });
});

test("validateRequest refuse les entrées invalides", () => {
  for (const body of [
    null,
    { mode: "x" },
    { mode: "reply", messages: [] },
    { mode: "reply", messages: [{ from: "bot", text: "a" }] },
    { mode: "opener", context: "" },
    { mode: "reply", messages: [{ from: "me", text: "a".repeat(601) }] },
    { mode: "reply", messages: Array.from({ length: 41 }, () => ({ from: "me", text: "a" })) },
  ]) {
    assert.throws(() => validateRequest(body), ValidationError, JSON.stringify(body)?.slice(0, 60));
  }
});

test("scrubPII masque les données de contact", () => {
  assert.equal(
    scrubPII("mail a.b@c.fr tel +33 6 12 34 56 78 insta @abc https://x.y"),
    "mail [email] tel [téléphone] insta [pseudo] [lien]",
  );
});

test("buildUserContent balise les données et nettoie", () => {
  const c = buildUserContent({
    mode: "reply",
    messages: [{ from: "me", text: "Salut" }, { from: "them", text: "mon 0612345678" }],
    context: "",
    goal: "proposer un verre",
  });
  assert.match(c, /<conversation>\nUTILISATEUR : Salut\nMATCH : mon \[téléphone\]\n<\/conversation>/);
  assert.match(c, /<objectif_utilisateur>\nproposer un verre/);
});

test("le prompt système ne contient aucune donnée variable (cache)", () => {
  assert.doesNotMatch(SYSTEM_PROMPT, /\d{4}-\d{2}-\d{2}/);
});

test("parseOutput valide, nettoie et limite à 3", () => {
  const out = parseOutput(JSON.stringify({
    suggestions: [
      { tone: "drole", text: " A ", why: "w" },
      { tone: "inconnu", text: "B", why: "w" },
      { tone: "doux", text: "", why: "w" },
      { tone: "direct", text: "C", why: "w" },
      { tone: "doux", text: "D", why: "w" },
      { tone: "drole", text: "E", why: "w" },
    ],
    coach_note: " note ",
  }));
  assert.deepEqual(out.suggestions.map((s) => s.text), ["A", "C", "D"]);
  assert.equal(out.coach_note, "note");
  assert.throws(() => parseOutput("pas du json"), OutputError);
  assert.throws(() => parseOutput('{"suggestions":[]}'), OutputError);
});

// Faux client : vérifie les paramètres envoyés sans appeler l'API.
function fakeClient(reply: Record<string, unknown>, capture: { params?: any }) {
  return {
    beta: {
      messages: {
        create: async (params: unknown) => {
          capture.params = params;
          return reply;
        },
      },
    },
  } as unknown as Anthropic;
}

test("generateSuggestions envoie les bons paramètres et parse la réponse", async () => {
  const cap: { params?: any } = {};
  const client = fakeClient({
    model: "claude-opus-5-5",
    stop_reason: "end_turn",
    content: [{ type: "text", text: '{"suggestions":[{"tone":"direct","text":"Un verre ?","why":"clair"}],"coach_note":""}' }],
    usage: { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 3 },
  }, cap);
  const r = await generateSuggestions(client, validateRequest({ mode: "reply", messages: [{ from: "them", text: "hey" }] }));
  assert.equal(r.response.suggestions[0].text, "Un verre ?");
  assert.deepEqual(r.usage, { input: 10, output: 5, cacheRead: 3 });
  assert.equal(cap.params.model, "claude-opus-5-5");
  assert.equal(cap.params.fallbacks, "default");
  assert.deepEqual(cap.params.betas, ["server-side-fallback-2026-07-01"]);
  assert.equal(cap.params.output_config.format.type, "json_schema");
  assert.equal(cap.params.system, SYSTEM_PROMPT);
});

test("generateSuggestions lève RefusalError sur un refus", async () => {
  const client = fakeClient({ model: "m", stop_reason: "refusal", content: [], usage: { input_tokens: 0, output_tokens: 0 } }, {});
  await assert.rejects(
    generateSuggestions(client, validateRequest({ mode: "opener", context: "aime le ski" })),
    RefusalError,
  );
});
