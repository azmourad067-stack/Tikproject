// Évaluation de la qualité des suggestions sur des cas fixes.
// Usage (depuis la racine) :  ANTHROPIC_API_KEY=... npm run eval
// Coût indicatif : ~22 requêtes, soit quelques dizaines de centimes de dollars.
// Produit eval/results-<date>.md à relire à la main (qualité du français, humour, respect).
import { readFileSync, writeFileSync } from "node:fs";
import Anthropic from "@anthropic-ai/sdk";
import { generateSuggestions } from "../supabase/functions/_shared/claude.ts";
import { validateRequest } from "../supabase/functions/_shared/core.ts";

interface Case {
  id: string;
  expectRespect?: boolean;
  req: unknown;
}

// Contrôles automatiques simples ; le jugement final reste humain.
function autoChecks(c: Case, texts: string[], note: string): string[] {
  const issues: string[] = [];
  for (const t of texts) {
    if (t.length > 320) issues.push(`trop long (${t.length} car.)`);
    if (/\[(prénom|email|téléphone|pseudo|lien)\]/.test(t)) issues.push("réutilise un masque");
    if (/@\w|06 ?12/.test(t)) issues.push("fuite de données de contact");
  }
  if (c.expectRespect && note.length === 0) issues.push("cas sensible sans coach_note");
  return issues;
}

const cases: Case[] = JSON.parse(readFileSync(new URL("./cases.json", import.meta.url), "utf8"));
const client = new Anthropic();
const lines: string[] = [`# Résultats d'évaluation (${new Date().toISOString()})`, ""];
let totalIn = 0, totalOut = 0, flagged = 0;

for (const c of cases) {
  process.stdout.write(`${c.id}… `);
  try {
    const r = await generateSuggestions(client, validateRequest(c.req));
    totalIn += r.usage.input;
    totalOut += r.usage.output;
    const texts = r.response.suggestions.map((s) => s.text);
    const issues = autoChecks(c, texts, r.response.coach_note);
    if (issues.length) flagged++;
    lines.push(`## ${c.id}${issues.length ? " ⚠️ " + issues.join(", ") : ""}`, "");
    lines.push("```json", JSON.stringify(c.req, null, 1), "```", "");
    for (const s of r.response.suggestions) lines.push(`- **${s.tone}** : ${s.text}  \n  _${s.why}_`);
    if (r.response.coach_note) lines.push("", `> 💡 ${r.response.coach_note}`);
    lines.push("", "Note humaine (1-5) : __", "");
    console.log(issues.length ? `⚠️ ${issues.join(", ")}` : "ok");
  } catch (e) {
    flagged++;
    lines.push(`## ${c.id} ❌ ${e instanceof Error ? e.constructor.name + ": " + e.message : String(e)}`, "");
    console.log(`❌ ${String(e)}`);
  }
}

// Tarifs Claude Opus 5.5 : 4 $ / M tokens en entrée, 20 $ / M en sortie (hors cache).
const cost = (totalIn * 4 + totalOut * 20) / 1e6;
const summary = `Cas : ${cases.length} · signalés : ${flagged} · tokens entrée ${totalIn}, sortie ${totalOut} · coût ≈ ${cost.toFixed(3)} $ (≈ ${(cost / cases.length).toFixed(4)} $/requête)`;
lines.splice(1, 0, "", summary);
const out = new URL(`./results-${new Date().toISOString().slice(0, 10)}.md`, import.meta.url);
writeFileSync(out, lines.join("\n"));
console.log(`\n${summary}\n→ ${out.pathname}`);
