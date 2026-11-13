import { test } from "node:test";
import assert from "node:assert/strict";
import { anonymize, isNoise, linesToMessages } from "./transcript.ts";

const W = 1000;
const line = (text: string, left: number, top: number, width = 300, height = 40) => ({
  text,
  frame: { left, top, width, height },
});

test("attribue gauche = match, droite = moi, et ignore l'interface", () => {
  const msgs = linesToMessages(
    [
      line("21:04", 450, 10, 100),
      line("Salut ça va ?", 650, 100),
      line("oui et toi", 40, 200),
      line("Vu", 900, 260, 40),
      line("oui", 800, 300, 120),
    ],
    W,
  );
  assert.deepEqual(msgs.map((m) => [m.from, m.text]), [
    ["me", "Salut ça va ?"],
    ["them", "oui et toi"],
    ["me", "oui"],
  ]);
});

test("fusionne les lignes d'une même bulle", () => {
  const msgs = linesToMessages(
    [line("J'ai fait un gâteau", 40, 100), line("qui ressemblait à un volcan", 40, 142)],
    W,
  );
  assert.equal(msgs.length, 1);
  assert.equal(msgs[0].text, "J'ai fait un gâteau qui ressemblait à un volcan");
});

test("ne fusionne pas deux bulles éloignées du même côté", () => {
  const msgs = linesToMessages([line("Message 1", 40, 100), line("Message 2", 40, 220)], W);
  assert.equal(msgs.length, 2);
});

test("isNoise garde les emojis seuls et les mots courts utiles", () => {
  assert.equal(isNoise("😂"), false);
  assert.equal(isNoise("ok"), false);
  assert.equal(isNoise("Aujourd'hui 14:02"), true);
  assert.equal(isNoise("85 %"), true);
});

test("anonymize masque prénoms, emails, téléphones, liens et pseudos", () => {
  const out = anonymize(
    "Camille, écris-moi à cam@mail.fr ou au 06 12 34 56 78, insta @cam.ille, www.site.fr. Camillette reste.",
    ["Camille"],
  );
  assert.equal(
    out,
    "[prénom], écris-moi à [email] ou au [téléphone], insta [pseudo], [lien] Camillette reste.",
  );
});

test("anonymize est insensible à la casse et ignore les noms trop courts", () => {
  assert.equal(anonymize("salut CAMILLE et Jo", ["camille", "J"]), "salut [prénom] et Jo");
});
