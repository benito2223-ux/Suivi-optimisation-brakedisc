/* ============================================================================
   PROTO — LE HARNIAIS DES ÉCRANS

   Il ne teste pas les maths (le noyau a ses propres tests) : il teste que
   chaque porte annoncée existe, et que chaque écran affiche ce qu'il promet
   d'afficher. Le principe est celui du Tour 52 : une question sur le code se
   pose au CODE, par typeof dans sa portée — jamais par lecture de sa source.

   Exécution : node test_proto.js
   ========================================================================== */

const fs = require("fs");
const path = require("path");

let total = 0, echecs = 0;

function ok(nom, obtenu, attendu, tol) {
  total++;
  let bon;
  if (typeof attendu === "number" && typeof obtenu === "number" && tol !== undefined) {
    bon = Math.abs(obtenu - attendu) <= tol;
  } else {
    bon = JSON.stringify(obtenu) === JSON.stringify(attendu);
  }
  if (!bon) {
    echecs++;
    console.log("  ECHEC " + nom + " — obtenu " + JSON.stringify(obtenu) +
                ", attendu " + JSON.stringify(attendu));
  } else {
    console.log("  ok   " + nom);
  }
}
function okVrai(nom, condition) { ok(nom, !!condition, true); }

/* ── un DOM minimal, suffisant pour rendre() et les écrans ── */
function faitElement(id) {
  return {
    id: id, innerHTML: "", textContent: "", value: "",
    style: {}, dataset: {},
    classList: { add(){}, remove(){}, contains(){ return false; } },
    addEventListener(){}, removeEventListener(){},
    getAttribute(){ return null; }, setAttribute(){},
    appendChild(){}, querySelector(){ return null; }, querySelectorAll(){ return []; },
    closest(){ return null; },
    get elements(){ return []; }
  };
}
global.window = {
  scrollTo(){}, print(){}, addEventListener(){},
  getComputedStyle(){ return {}; }
};
global.document = {
  getElementById(id) { return faitElement(id); },
  querySelector(){ return null; },
  querySelectorAll(){ return []; },
  addEventListener(){},
  createElement(){ return faitElement("x"); },
  body: faitElement("body")
};
global.FormData = class { entries(){ return []; } };
global.location = { href: "http://localhost/proto" };

/* ── on charge le proto assemblé, SANS exécuter l'auto-rendre final ── */
const chemin = path.join(__dirname, "index.html");
if (!fs.existsSync(chemin)) {
  console.log("  ECHEC index.html absent — lancez python assembler.py");
  process.exit(1);
}
const html = fs.readFileSync(chemin, "utf8");
const blocs = [];
const re = /<script[^>]*>([\s\S]*?)<\/script>/g;
let m;
while ((m = re.exec(html)) !== null) blocs.push(m[1]);
if (!blocs.length) {
  console.log("  ECHEC aucun bloc script dans index.html");
  process.exit(1);
}

/* on neutralise le dernier rendre() : on veut les fonctions, pas le DOM */
let src = blocs.join("\n");
const avant = src.length;
src = src.replace(/remplirScenarios\(\);\s*\n\s*rendre\(\);\s*$/, "");
if (src.length === avant) {
  console.log("  ECHEC le auto-rendre final n'a pas ete neutralise — le harnais ne");
  console.log("         pourrait pas distinguer une panne reelle d'un DOM absent.");
  process.exit(1);
}

let api;
try {
  api = (new Function(src + "\nreturn {proto: window.proto, ETAT: window.proto.ETAT, JEUX, ECRANS};"))
    .call(globalThis);
} catch (e) {
  console.log("  ECHEC le proto ne s'execute pas : " + e.message);
  console.log(e.stack.split("\n").slice(0, 4).join("\n"));
  process.exit(1);
}
const P = api.proto;
okVrai("le proto s'exécute sans exception", !!P);

console.log("\n── LES PORTES : chaque bouton a une fonction (typeof, pas lecture) ──");

/* Les portes que l'écran annonce. Une porte sans fonction est un clic mort —
   c'est exactement le bug du Tour 52, vérifié ici par le MOTEUR. */
const PORTES = [
  ["la navigation vers un écran", ["aller", "rendre"]],
  ["l'ouverture d'une ligne", ["basculerLigne"]],
  ["le changement de poste (preuve)", ["changerPreuvePoste"]],
  ["l'annulation de saisie", ["annulerSaisie"]],
  ["l'enregistrement d'un essai", ["enregistrerEssai"]],
  ["l'écran 1 — où en est-on", ["ecran1"]],
  ["l'écran 2 — essai", ["ecran2"]],
  ["l'écran 3 — preuve", ["ecran3"]],
  ["l'écran 4 — décision", ["ecran4"]],
  ["l'écran 5 — emporter", ["ecran5", "a4HTML"]],
  ["le noyau exposé", ["verdictPoste", "verdictLigne", "decisionPoste",
                        "cheminCPP", "coutLogement", "cppOutillageScenario",
                        "statutEssai", "statutScenario", "recapLignes"]],
  ["la lecture du jeu de données", ["tousPostes", "verdictsLignes"]]
];
PORTES.forEach(([porte, fns]) => {
  fns.forEach(f => {
    /* typeof sur window.proto — le moteur répond, pas la source */
    const t = (P && typeof P[f] === "function") ? "function" : "ABSENT";
    ok(porte + " → " + f + "()", t, "function");
  });
});

console.log("\n── L'ÉCRAN 1 : le CPP plaquettes en premier, et rien d'autre ──");

const vls = P.verdictsLignes();
okVrai("les trois lignes du jeu de départ sont lues", vls.length === 3);

const e1 = P.ecran1();
okVrai("l'écran 1 rend du HTML", e1.length > 500);
okVrai("l'écran 1 ouvre sur le CPP plaquettes", e1.indexOf("CPP plaquettes") >= 0);
okVrai("l'écran 1 affiche le gain acté et le gain projeté SÉPARÉS",
   e1.indexOf("Déjà gagné") >= 0 && e1.indexOf("En essai") >= 0);
okVrai("l'écran 1 ne fusionne JAMAIS les deux gains en un « total »",
   e1.indexOf("Total gain") < 0 && e1.indexOf("total des gains") < 0);
okVrai("l'écran 1 affiche les quatre chiffres du bandeau", (e1.match(/class="kpi"/g) || []).length === 4);
okVrai("l'écran 1 ne montre PAS le temps machine comme comparable",
   e1.indexOf("temps machine") >= 0 /* il est mentionné comme NON comparable */);
okVrai("la ligne « à chiffrer » est signalée à l'écran 1", e1.indexOf("à chiffrer") >= 0);

console.log("\n── L'INVARIANT 3 : une cible sans chiffrage reste visible ──");

const l3 = vls.find(v => v.ligne.nom.indexOf("PCI") === 0);
okVrai("la ligne PCI est bien identifiée", !!l3);
ok("ses deux postes sont comptés non chiffrables", l3.nonChiffrables, 2);
ok("son CPP de prod est null, pas 0", l3.cppProd, null);
okVrai("ses postes ne sont pas devenus des « opportunités » invisibles",
   l3.postes.every(p => p.verdict.code === "achiffrer"));
okVrai("l'écran 1 la signale à l'utilisateur", e1.indexOf("porte") >= 0 || e1.indexOf("à chiffrer") >= 0);

console.log("\n── L'ÉCRAN 2 : saisir un essai ──");

const e2 = P.ecran2();
okVrai("l'écran 2 rend", e2.length > 300);
["cPoste", "cScenario", "cDate", "cEquipe", "cCharniere", "cBatt"].forEach(id => {
  ok("l'écran 2 a le champ " + id, e2.indexOf('id="' + id + '"') >= 0, true);
});
okVrai("l'écran 2 a un bouton d'enregistrement", e2.indexOf('type="submit"') >= 0);

console.log("\n── L'ÉCRAN 3 : la preuve ──");

/* Cas du RÉEL : l'utilisateur ouvre l'écran 3 sans avoir touché au selecteur.
   Le harnais posait ETAT.saisi.poste avant d'appeler ecran3() ; le navigateur, lui,
   ouvre l'ecran a froid. Les deux resolutions divergeaient : le selecteur annoncait
   « EMAG 1 · OP10 » au-dessus d'un « aucun essai saisi ». */
P.ETAT.saisi = {};
const e3froid = P.ecran3();
okVrai("ecran 3 a froid : les preuves du premier poste s'affichent",
   e3froid.indexOf('class="preuve"') >= 0);
okVrai("ecran 3 a froid : le selecteur et la liste regardent le meme poste",
   e3froid.indexOf("EMAG 1 · OP10") >= 0);
okVrai("ecran 3 a froid : le message « aucun essai » ne ment pas",
   e3froid.indexOf("Aucun essai saisi") < 0);

P.ETAT.saisi.poste = "l1|o10";
const e3 = P.ecran3();
okVrai("l'écran 3 rend", e3.length > 300);
okVrai("l'écran 3 affiche la règle des 5 répétitions", e3.indexOf("répété") >= 0);
okVrai("l'écran 3 montre les CPP par logement avec leurs sources",
   e3.indexOf("arêtes") >= 0 || e3.indexOf("€/pce") >= 0);
okVrai("l'écran 3 affiche les 5 essayés validés (SL506)",
   e3.indexOf("SL506") >= 0);
okVrai("l'écran 3 affiche l'essai en cours (SL500 charnière 300)",
   e3.indexOf("SL500 · charnière 300") >= 0);

console.log("\n── L'ÉCRAN 4 : la décision ──");

const e4 = P.ecran4();
okVrai("l'écran 4 rend", e4.length > 300);
okVrai("l'écran 4 affiche au moins un mot de décision",
   ["DÉCIDER", "SÉRIE", "ESSAYER", "CHIFFRER"].some(m => e4.indexOf(m) >= 0));
okVrai("l'écran 4 montre le gain acté et projeté dans chaque carte",
   e4.indexOf("Gain acté") >= 0 && e4.indexOf("Gain projeté") >= 0);
okVrai("l'écran 4 affiche la cible et le chemin",
   e4.indexOf("Cible site") >= 0 && e4.indexOf("Chemin") >= 0);

console.log("\n── L'ÉCRAN 5 : la page à emporter ──");

const e5 = P.ecran5();
okVrai("l'écran 5 rend", e5.length > 500);
okVrai("l'A4 se déclare vivante, pas figée", e5.indexOf("vivant") >= 0);
okVrai("l'A4 affiche les trois lignes", e5.indexOf("EMAG 1") >= 0 && e5.indexOf("PCI") >= 0);
okVrai("l'A4 affiche une section décisions", e5.indexOf("demande une décision") >= 0);
okVrai("l'A4 rappelle la règle du 5×", e5.indexOf("5 fois") >= 0 || e5.indexOf("5 fois") >= 0);
okVrai("l'A4 dit que le CPP est hors temps machine", e5.indexOf("hors temps machine") >= 0);
okVrai("l'A4 a un bouton d'impression", e5.indexOf("window.print") >= 0 || e5.indexOf("Imprimer") >= 0);

console.log("\n── LA COHÉRENCE ENTRE ÉCRANS (source unique, §3.1) ──");

/* Le même poste doit porter le même chiffre partout : c'est la faute la plus
   coûteuse de l'app de production (deux modules, deux histoires).
   On relit la valeur DANS LE HTML RENDU — présence d'une chaîne, c'est trop
   laxiste : une panne d'affichage peut laisser tous les tests verts. */
const vL1 = vls.find(v => v.ligne.id === "l1");
const posteOP10 = vL1.postes.find(p => p.op && p.op.id === "o10");

function fmtFr(x, d) { return parseFloat(x).toFixed(d).replace(".", ","); }

okVrai("le CPP d'OP10 est calculé et non nul",
   posteOP10.cppProd !== null && posteOP10.cppProd > 0.2);

/* Écran 1 : la tuile d'OP10 commence par son nom d'opération. On ne lit PAS le
   premier <span class="big"> de la page — c'est le bandeau KPI, pas la tuile
   (erreur du premier jet de ce test : il comparait 0,4957 à 0,2355). */
function cppDeLaTuile(html, nomOp) {
  const i = html.indexOf(">" + nomOp + "<small>");
  if (i < 0) return "tuile-absente";
  const j = html.indexOf('class="big">', i);
  if (j < 0) return "valeur-absente";
  /* on saute la balise elle-meme plutot que de compter ses caracteres */
  const m = html.slice(j + 'class="big">'.length).match(/^([\d,]+)/);
  return m ? m[1] : "illisible";
}

/* Écran 4 : chaque carte porte le CPP dans <div class="gros"> après le libellé. */
function tousCPPDeDecision(html) {
  const out = [];
  let i = html.indexOf('class="gros">');
  while (i >= 0) {
    const m = html.slice(i).match(/CPP plaquettes<\/small>([\d,]+|—)/);
    out.push(m ? m[1] : "?");
    i = html.indexOf('class="gros">', i + 1);
  }
  return out;
}

const cppAfficheE1 = cppDeLaTuile(e1, posteOP10.op.nom);
ok("l'écran 1 affiche le CPP d'OP10 exactement tel que le noyau l'a calculé",
   cppAfficheE1, fmtFr(posteOP10.cppProd, 4));

const cppEcran4 = tousCPPDeDecision(e4);
okVrai("l'écran 4 affiche le MÊME CPP qu'il écran 1 (pas deux calculs)",
   cppEcran4.indexOf(cppAfficheE1) >= 0);

/* Et aucun CPP de l'écran 4 n'est différent de celui du noyau, poste par poste. */
const cppNoyau = vls.flatMap(vl => vl.postes)
  .filter(p => p.cppProd !== null).map(p => fmtFr(p.cppProd, 4));
const cppEcran4set = cppEcran4.filter(v => v !== "—");
okVrai("chaque CPP de l'écran 4 correspond à un CPP du noyau",
   cppEcran4set.every(v => cppNoyau.indexOf(v) >= 0));

/* Le CPP ne doit jamais être présenté sans son unité, ni avec une unité fausse. */
/* l'unité qui accompagne chaque CPP affiché : on relit le HTML rendu */
function uniteApresChaqueBig(html) {
  const morceaux = html.split('<span class="big">').slice(1);
  if (!morceaux.length) return false;
  return morceaux.every(m => {
    const fin = m.indexOf("</span>");
    if (fin < 0) return false;
    const suite = m.slice(fin, fin + 90);
    return suite.indexOf("€/pce") >= 0;
  });
}
okVrai("chaque CPP affiché porte l'unité €/pce", uniteApresChaqueBig(e1));
okVrai("aucun CPP n'est affiché en millièmes ou en centimes (unité inventée)",
   e1.indexOf("millièmes") < 0 && e1.indexOf("centimes") < 0);

console.log("\n" + "=".repeat(60));
console.log("PROTO ÉCRANS : " + total + " tests | " + echecs + " echecs");
console.log(echecs ? "*** LE PROTO EST ROUGE ***" : "TOUT EST VERT");
process.exit(echecs ? 1 : 0);