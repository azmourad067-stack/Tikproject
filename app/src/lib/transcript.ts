// Transforme le résultat OCR d'une capture de conversation en liste de messages,
// et masque les informations identifiantes AVANT tout envoi au serveur.
// Module pur (sans React Native) : testé avec `npm test` à la racine du dépôt.

export interface Frame {
  left: number;
  top: number;
  width: number;
  height: number;
}

export interface OcrLine {
  text: string;
  frame?: Frame;
}

export interface Message {
  id: string;
  from: "me" | "them";
  text: string;
}

// Éléments d'interface fréquents dans les captures, à ignorer.
const UI_NOISE = [
  /^\d{1,2}[:h]\d{2}(\s?(AM|PM))?$/i, // heures « 21:04 », « 9h30 »
  /^(aujourd'hui|hier|today|yesterday)(\s.*)?$/i,
  /^(lun|mar|mer|jeu|ven|sam|dim)\.?\s?\d{1,2}/i,
  /^(vu|lu|seen|read|envoyé|delivered|distribué)(\s.*)?$/i,
  /^(écris un message|tape un message|envoyer|type a message|send)\b/i,
  /^\d{1,3}\s?%$/, // batterie
  /^(4G|5G|LTE|Wi-?Fi)$/i,
];

export function isNoise(text: string): boolean {
  const t = text.trim();
  if (t.length === 0) return true;
  if (t.length <= 2 && !/[\p{L}\p{N}]{2}/u.test(t) && !/\p{Extended_Pictographic}/u.test(t)) return true;
  return UI_NOISE.some((re) => re.test(t));
}

/**
 * Attribue chaque ligne à « moi » (bulle à droite) ou « match » (bulle à gauche),
 * puis fusionne les lignes consécutives d'une même bulle.
 * Heuristique : le centre horizontal de la ligne par rapport au milieu de l'image.
 * L'utilisateur peut corriger chaque attribution dans l'app.
 */
export function linesToMessages(lines: OcrLine[], imageWidth: number): Message[] {
  const sorted = lines
    .filter((l) => !isNoise(l.text))
    .sort((a, b) => (a.frame?.top ?? 0) - (b.frame?.top ?? 0));

  const out: Message[] = [];
  let prevBottom = -Infinity;
  let prevFrom: Message["from"] | null = null;

  for (const line of sorted) {
    const f = line.frame;
    const from: Message["from"] =
      f && imageWidth > 0 && f.left + f.width / 2 > imageWidth * 0.55 ? "me" : "them";
    const top = f?.top ?? 0;
    const gap = top - prevBottom;
    const lineHeight = f?.height ?? 0;
    // Même bulle si même côté et lignes très proches verticalement.
    const sameBubble = prevFrom === from && out.length > 0 && gap < lineHeight * 0.9;
    if (sameBubble) {
      out[out.length - 1].text += " " + line.text.trim();
    } else {
      out.push({ id: String(out.length), from, text: line.text.trim() });
    }
    prevFrom = from;
    prevBottom = f ? f.top + f.height : prevBottom;
  }
  return out;
}

// --- Anonymisation ----------------------------------------------------------------

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/**
 * Remplace les prénoms indiqués par l'utilisateur, ainsi que emails, téléphones,
 * liens et pseudos (@...). Le serveur refait un nettoyage par sécurité.
 */
export function anonymize(text: string, names: string[]): string {
  let out = text;
  for (const raw of names) {
    const name = raw.trim();
    if (name.length < 2) continue;
    out = out.replace(new RegExp(`(?<![\\p{L}])${escapeRegExp(name)}(?![\\p{L}])`, "giu"), "[prénom]");
  }
  return out
    .replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, "[email]")
    .replace(/\b(?:https?:\/\/|www\.)\S+/gi, "[lien]")
    .replace(/(^|[\s(])@[A-Za-z0-9_.]{2,30}/g, "$1[pseudo]")
    .replace(/(?:\+\d{1,3}[\s.-]?)?\(?0?\d\)?(?:[\s.-]?\d{2}){4}\b/g, "[téléphone]");
}
