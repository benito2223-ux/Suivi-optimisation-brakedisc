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

/* ── le stockage local et la lecture de fichier, en vrai cette fois ─────────
   Au premier jet de la v1.0, le harnais ne fournissait NI l'un NI l'autre. Le
   `try/catch` de `chargerLocal` avalait alors le ReferenceError et renvoyait
   false : les 70 tests passaient sans qu'aucun n'ait jamais fait tourner
   l'import. Un harnais qui ne peut pas atteindre une porte ne teste pas cette
   porte — il donne l'illusion qu'elle est couverte. */
const _store = new Map();
global.localStorage = {
  getItem(k) { return _store.has(k) ? _store.get(k) : null; },
  setItem(k, v) { _store.set(k, String(v)); },
  removeItem(k) { _store.delete(k); },
  clear() { _store.clear(); }
};
/* le contenu du prochain fichier « lu » — le harnais le règle avant d'appeler */
global.__fichier = { nom: "essai.json", taille: 0, texte: "", erreur: false };
global.FileReader = class {
  readAsText() {
    const f = global.__fichier;
    setTimeout(() => {
      if (f.erreur) { if (this.onerror) this.onerror(new Error("illisible")); return; }
      this.result = f.texte;
      if (this.onload) this.onload();
    }, 0);
  }
};
/* les promesses de lecture sont résolues par defers : le harnais doit attendre
   qu'elles le soient avant d'affirmer quoi que ce soit. */
function tick() { return new Promise(r => setTimeout(r, 1)); }

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
src = src.replace(/chargerLocal\(\);\s*\n\s*rendre\(\);\s*$/, "");
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

/* ── L'ASSEMBLAGE EST-IL À JOUR ? ───────────────────────────────────────────
   Ce harnais teste le FICHIER ASSEMBLÉ, donc il teste l'état du code au moment
   de la dernière couture — pas l'état du code. Modifier coeur.js et oublier de
   relancer assembler.py laissait ici 109 tests verts sur du code qui n'était
   plus dans le fichier : c'est le contre-regard du Tour 55 qui l'a révélé, en
   injectant une faute dans le noyau et en constatant que l'écran, lui, ne
   bronchait pas.

   On refuse donc de tourner sur un assemblage périmé. Mieux vaut un test qui ne
   s'exécute pas qu'un test qui ment. */
const crypto = require("crypto");
function empreinteSources() {
  return crypto.createHash("sha256")
    .update(["coeur.js", "donnees.js", "import.js", "proto.html"]
      .map(f => fs.readFileSync(path.join(__dirname, f), "utf8"))
      .join("\u0000"), "utf8")
    .digest("hex").slice(0, 16);
}
const empreinteAttendue = empreinteSources();
ok("l'assemblage index.html est à jour vis-à-vis des sources",
   P.EMPREINTE_ASSEMBLAGE, empreinteAttendue);
if (P.EMPREINTE_ASSEMBLAGE !== empreinteAttendue) {
  console.log("         → index.html date d'avant la dernière modification.");
  console.log("         → ce qui suit ne prouverait rien. Relancez : python assembler.py");
  process.exit(1);
}

console.log("\n── LES PORTES : chaque bouton a une fonction (typeof, pas lecture) ──");

/* Les portes que les écrans annoncent. Une porte sans fonction est un clic mort —
   c'est exactement le bug du Tour 52, vérifié ici par le MOTEUR. Les noms ont
   changé avec l'architecture en trois étages : ouvrir une ligne ne « bascule »
   plus, on l'ouvre. */
const PORTES = [
  ["la navigation vers un écran", ["aller", "rendre"]],
  ["l'ouverture d'une ligne", ["ouvrirLigne"]],
  ["la ligne actuellement ouverte", ["ligneCourante"]],
  ["le rendu d'une tuile", ["tuileHTML"]],
  ["le rendu d'un outil", ["outilHTML"]],
  ["le formulaire d'essai", ["essaiFormHTML", "postesChange", "scenarioChange"]],
  ["l'annulation de saisie", ["annulerSaisie"]],
  ["l'enregistrement d'un essai", ["enregistrerEssai"]],
  ["l'écran 1 — les lignes", ["ecran1"]],
  ["l'écran 2 — le détail de la ligne", ["ecran2"]],
  ["l'écran 3 — scénario et optimisation", ["ecran3"]],
  ["l'écran 4 — décision", ["ecran4"]],
  ["l'écran 5 — emporter", ["ecran5", "a4HTML"]],
  ["le noyau exposé", ["verdictPoste", "verdictLigne", "decisionPoste",
                        "cheminCPP", "coutLogement", "cppOutillageScenario",
                        "statutEssai", "statutScenario", "recapLignes"]],
  ["le noyau des deux premiers étages", ["scenarioDeProd", "postesDeLigne",
                        "cppReference", "tuileDeLigne", "tuilesDeLignes",
                        "detailLigne", "outillageDeScenario", "familleDeLigne",
                        "rangLigne", "codeLigneDe"]],
  ["la lecture du jeu de données", ["tousPostes", "verdictsLignes"]]
];
PORTES.forEach(([porte, fns]) => {
  fns.forEach(f => {
    /* typeof sur window.proto — le moteur répond, pas la source */
    const t = (P && typeof P[f] === "function") ? "function" : "ABSENT";
    ok(porte + " → " + f + "()", t, "function");
  });
});

console.log("\n── L'ÉCRAN 1 : une tuile par ligne de production ──");

const e1 = P.ecran1();
okVrai("l'écran 1 rend du HTML", e1.length > 500);
okVrai("l'écran 1 affiche un CPP par ligne chiffrée",
   (e1.match(/tuile-principal/g) || []).length > 0);
okVrai("chaque tuile porte sa famille en couleur",
   e1.indexOf("pastille") >= 0);
okVrai("l'écran 1 affiche les quatre chiffres du bandeau",
   (e1.match(/class="kpi"/g) || []).length === 4);
okVrai("l'écran 1 ne montre PAS le temps machine comme comparable",
   e1.indexOf("temps machine") >= 0 /* il est mentionné comme NON comparable */);
/* La décision du 02/10/2026 : la production hebdomadaire sort du périmètre,
   parce qu'elle est détaillée par lot de lignes. L'écran doit le DIRE, sinon
   quelqu'un reviendra l'ajouter dans six mois en croyant que c'était prévu. */
/* Le contre-regard a montré qu'une recherche de mots isolés ne voyait pas la
   disparition de la phrase : « lot » et « cadence » reparaissent ailleurs dans
   l'écran. On vérifie donc la PHRASE entière, pas deux mots. */
okVrai("l'écran 1 déclare pourquoi il n'y a pas de cadence",
   e1.indexOf("la production est détaillée par lot") >= 0);
/* Le delta théorie/réalité n'est pas branché : il doit être dit, pas inventé. */
okVrai("l'écran 1 a un dépliant « théorie et réalité »",
   e1.indexOf("Théorie et réalité") >= 0);
okVrai("et ce dépliant déclare le delta non branché",
   e1.indexOf("pas encore branché") >= 0);

console.log("\n── L'INVARIANT 3 : une ligne sans coût ne devient pas un coût ──");

const tuilesJeu = P.tuilesDeLignes(P.ETAT.lignes);
const ligneVide = tuilesJeu.find(t => t.vide);

/* La règle porte sur TOUTES les lignes, vides ou non : jamais 0 là où il n'y a
   rien. Elle se vérifie donc même quand le jeu de départ n'a aucune ligne vide
   — c'est le cas du jeu d'exemple, qui est complet par construction. */
/* L'invariant est « jamais 0 », pas « jamais null » : une ligne qui a des
   références mais aucun poste chiffrable a legitimately pas de CPP. Ce qu'elle
   ne doit JAMAIS faire, c'est afficher 0,0000 comme si elle avait été mesurée. */
okVrai("aucune tuile ne transforme « rien à chiffrer » en 0",
   tuilesJeu.every(t => t.cpp === null || t.cpp > 0));
const tuileSansChiffre = tuilesJeu.find(t => t.cpp === null && t.refs.length > 0);
if (tuileSansChiffre) {
  okVrai("la ligne qui a des références mais aucun poste chiffrable le dit",
     e1.indexOf("aucun poste chiffrable") >= 0, true);
}
if (ligneVide) {
  ok("une ligne sans référence est déclarée vide", ligneVide.vide, true);
  ok("et son CPP est null, pas 0", ligneVide.cpp, null);
  ok("elle ne se déclare pas « non chiffrable » : elle n'a rien", ligneVide.nonChiffrables, 0);
  okVrai("l'écran 1 le dit en toutes lettres",
     e1.indexOf("Aucune référence déclarée") >= 0);
}
okVrai("l'écran 1 ne montre jamais un « 0 €/pce » pour une ligne non chiffrée",
   !/0,0000 <\/small>/.test(e1));

console.log("\n── L'ÉCRAN 2 : la ligne, et son scénario de production ──");

const ligneChiffrable = tuilesJeu.find(t => t.cpp !== null);
okVrai("le jeu de départ a une ligne chiffrable", !!ligneChiffrable);
ok("aucune ligne n'est ouverte au démarrage", P.ETAT.ligne, null);
okVrai("l'écran 2 le dit plutôt que d'afficher une ligne au hasard",
   P.ecran2().indexOf("Aucune ligne ouverte") >= 0);

P.ouvrirLigne(ligneChiffrable.ligne.id);
ok("ouvrirLigne positionne la ligne", P.ligneCourante().id, ligneChiffrable.ligne.id);
ok("et mène à l'écran 2", P.ETAT.ecran, 2);

const e2 = P.ecran2();
okVrai("l'écran 2 rend", e2.length > 300);
okVrai("l'écran 2 décompose l'outillage en outils", e2.indexOf("outil-tete") >= 0);
okVrai("l'écran 2 montre le CPP de production", e2.indexOf("CPP outillage · production") >= 0);
okVrai("l'écran 2 montre la cible du site", e2.indexOf("Cible du site") >= 0);
okVrai("l'écran 2 ouvre la porte du 3e étage",
   e2.indexOf("Scénario et optimisation") >= 0);
/* Un poste sans scénario de production doit rester visible : sinon il
   disparaîtrait et l'agent croirait la ligne complète. */
const detailJeu = P.detailLigne(ligneChiffrable.ligne);
okVrai("le détail compte ses postes sans production",
   detailJeu.refs.every(r => r.postes.length === 1
     || r.postes.some(p => !!p.prod)));

console.log("\n── L'ÉCRAN 3 : les scénarios qui ne sont PAS en production ──");

const e3 = P.ecran3();
okVrai("l'écran 3 rend", e3.length > 300);
okVrai("l'écran 3 montre le formulaire d'essai", e3.indexOf('id="fEssai"') >= 0);
["cPoste", "cScenario", "cDate", "cEquipe", "cCharniere", "cBatt"].forEach(id => {
  ok("l'écran 3 a le champ " + id, e3.indexOf('id="' + id + '"') >= 0, true);
});
okVrai("l'écran 3 a un bouton d'enregistrement", e3.indexOf('type="submit"') >= 0);

/* Les deux sélecteurs du formulaire doivent regarder le MÊME poste. Le premier
   jet calculait le poste par défaut pour l'un et par l'absence de poste pour
   l'autre : l'écran annonçait « EMAG 1 · OP10 » au-dessus d'un « aucun scénario
   sur ce poste ». C'est trouvé à l'œil dans le navigateur, pas par un test —
   d'où ce test, qui pose la question au moteur. */
const optionsPoste = (e3.match(/<option value="[^"]+\|[^"]+"/g) || []);
const posteAffiche = (e3.match(/<option value="([^"]+)"\s+selected>/) || [])[1];
okVrai("le formulaire propose des postes", optionsPoste.length > 0);
okVrai("le formulaire affiche « aucun scénario » seulement si le poste n'en a pas",
   !(posteAffiche && e3.indexOf("aucun scénario sur ce poste") >= 0
     && scenariosDuPosteTest(posteAffiche).length > 0));
function scenariosDuPosteTest(cle) {
  const [lid, oid] = (cle || "").split("|");
  const p = P.postesDeLigne(ligneChiffrable.ligne);
  const t = p.find(x => x.op.id === oid);
  return t ? t.scs : [];
}
okVrai("le poste affiché par défaut appartient à la ligne ouverte",
   (posteAffiche || "").indexOf(ligneChiffrable.ligne.id) === 0, true);
/* On lit les <option> DU SÉLECTEUR DE SCÉNARIO, et on les compare à ce que le
   noyau déclare pour ce poste. C'est le test le plus direct de l'alignement. */
const blocScenario = e3.slice(e3.indexOf('id="cScenario"'));
const scsAffiches = (blocScenario.match(/<option value="([^"]+)"/g) || [])
  .map(o => o.replace(/<option value="/, "").replace(/"$/, ""))
  .filter(v => v !== "");
const scsNoyau = scenariosDuPosteTest(posteAffiche).map(x => x.id);
ok("le sélecteur de scénario propose exactement les scénarios du poste affiché",
   scsAffiches, scsNoyau);
/* Le cœur de l'étage 3 : les scénarios listés sont EXACTEMENT ceux que le noyau
   déclare hors production. Une divergence ici ferait croire qu'un scénario est
   déjà optimisé alors qu'il ne l'est pas. */
const horsProdNoyau = new Set();
detailJeu.refs.forEach(r => r.postes.forEach(p => { if (p.nbAutres) horsProdNoyau.add(p.op.id); }));
okVrai("l'écran 3 annonce le nombre de scénarios hors production",
   e3.indexOf("essais conforme") >= 0 || e3.indexOf("hors production") >= 0
   || e3.indexOf("Aucun scénario hors production") >= 0);
okVrai("si des scénarios hors production existent, l'écran 3 en montre au moins un",
   horsProdNoyau.size === 0 || e3.indexOf('class="preuve"') >= 0);

/* Le contre-regard de cet étage : l'écran 3 ne doit lister QUE les scénarios que
   le noyau déclare hors production. Le contre-regard du Tour 55 a montré qu'un
   `indexOf(...) >= 0` ne voyait pas ce défaut : l'écran pouvait donc remonter le
   scénario de production parmi les scénarios « à optimiser », et les 110 tests
   restaient verts. C'est l'erreur même que les trois étages existent pour
   empêcher — l'agent optimiserait un scénario déjà en série.

   On compare donc les ENSEMBLES, pas la présence : la liste affichée, relue
   dans le HTML, doit être exactement celle du noyau. */
function scenariosAffiches(html) {
  const out = [];
  let i = html.indexOf('<section class="preuve">');
  while (i >= 0) {
    const j = html.indexOf("<h3>", i);
    if (j < 0 || j > html.indexOf("</section>", i)) break;
    const k = html.indexOf("</h3>", j);
    out.push(html.slice(j + 4, k));
    i = html.indexOf('<section class="preuve">', k);
  }
  return out;
}
const affichesE3 = scenariosAffiches(e3);
const attendusE3 = [];
P.postesDeLigne(ligneChiffrable.ligne).forEach(p => {
  p.autres.forEach(sc => attendusE3.push(sc.name || ""));
});
ok("l'écran 3 liste exactement les scénarios hors production du noyau",
   affichesE3, attendusE3);

const nomsProd = [];
P.postesDeLigne(ligneChiffrable.ligne).forEach(p => { if (p.prod) nomsProd.push(p.prod.name); });
okVrai("aucun de ces scénarios n'est un scénario de production",
   affichesE3.every(n => nomsProd.indexOf(n) < 0));

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
okVrai("l'A4 dit que le CPP est hors temps machine", e5.indexOf("hors temps machine") >= 0);
okVrai("l'A4 a un bouton d'impression", e5.indexOf("window.print") >= 0 || e5.indexOf("Imprimer") >= 0);

console.log("\n── LA COHÉRENCE ENTRE ÉCRANS (source unique, §3.1) ──");

/* Le même chiffre doit être écrit partout : c'est la faute la plus coûteuse de
   l'app de production (deux modules, deux histoires).
   On relit la valeur DANS LE HTML RENDU — présence d'une chaîne, c'est trop
   laxiste : une panne d'affichage peut laisser tous les tests verts. */
function fmtFr(x, d) { return parseFloat(x).toFixed(d).replace(".", ","); }

/* La valeur de la tuile principale d'une ligne : le grand chiffre du bloc
   `.tuile-principal`. On isole le bloc plutôt que de ramasser le premier
   nombre de la page, qui serait le bandeau. */
function cppTuilePrincipale(html) {
  const i = html.indexOf('class="tuile-principal"');
  if (i < 0) return "bloc-absent";
  const m = html.slice(i).match(/class="cpp">([\d,]+)\s*<small>/);
  return m ? m[1] : "illisible";
}

/* La valeur d'une tuile de référence sur l'ÉCRAN 1, isolée par le nom.
   On prend la balise fermante en paramètre : la même information est rendue
   dans un <div class="nom"> sur la tuile et dans un <h2> sur le détail. Chercher
   « la première occurrence du nom » attraperait le bandeau ou une autre
   référence, et le test échouerait sans rien dire du produit. */
function cppTuileRef(html, nomRef, balise) {
  const i = html.indexOf('>' + nomRef + "</" + (balise || "div") + ">");
  if (i < 0) return "tuile-absente";
  const m = html.slice(i).match(/class="cpp">([\d,]+)\s*<small>/);
  return m ? m[1] : "illisible";
}

/* Le CPP d'une référence sur l'ÉCRAN 2 : il est dans le premier `.val` du
   bandeau de la référence, pas dans un `.cpp`. On isole le bloc de la référence
   par son <h2> pour ne pas ramasser la valeur d'une autre référence. */
function cppRefSurDetail(html, nomRef) {
  const i = html.indexOf("<h2>" + nomRef + "</h2>");
  if (i < 0) return "reference-absente";
  const m = html.slice(i).match(/class="val">([^<]+)</);
  return m ? m[1] : "illisible";
}

/* Les CPP des outils d'un poste, dans l'ordre du rendu. */
function cppDesOutils(html) {
  const out = [];
  let i = html.indexOf('class="outil-tete"><b>');
  while (i >= 0) {
    const finBloc = html.indexOf('class="paires"', i);
    const bloc = html.slice(i, finBloc < 0 ? i + 400 : finBloc);
    const m = bloc.match(/([\d,]+) €\/pce<\/span>/);
    out.push(m ? m[1] : "non chiffrable");
    i = html.indexOf('class="outil-tete"><b>', i + 1);
  }
  return out;
}

/* ── Tuile ↔ noyau ── */
const tNoyau = P.tuileDeLigne(ligneChiffrable.ligne);
ok("l'écran 1 affiche, pour cette ligne, le CPP du noyau",
   cppTuilePrincipale(e1), fmtFr(tNoyau.cpp, 4));
const refDominante = tNoyau.dominante;
okVrai("cette ligne a une référence dominante", !!refDominante);
if (refDominante) {
  ok("et la tuile de cette référence porte le CPP du noyau",
     cppTuileRef(e1, refDominante.ref.nom, "div"), fmtFr(refDominante.cpp, 4));
}

/* ── Détail ↔ noyau : le CPP d'une référence, puis le total de la ligne ── */
const dNoyau = P.detailLigne(ligneChiffrable.ligne);
const premiereRef = dNoyau.refs[0];
okVrai("le détail expose au moins une référence", !!premiereRef);
if (premiereRef) {
  ok("le CPP affiché de cette référence est celui du noyau",
     cppRefSurDetail(e2, premiereRef.nom),
     premiereRef.cpp === null ? "non chiffrable" : fmtFr(premiereRef.cpp, 4));
}

/* ── Outils ↔ noyau : chaque outil affiché porte son propre CPP ── */
const outilsDuJeu = [];
dNoyau.refs.forEach(r => r.postes.forEach(p => {
  if (!p.outillage) return;
  p.outillage.outils.forEach(o => outilsDuJeu.push(o.cpp));
}));
const outilsAffiches = cppDesOutils(e2);
ok("l'écran 2 affiche autant d'outils que le noyau en a",
   outilsAffiches.length, outilsDuJeu.length);
ok("et chaque CPP d'outil affiché est bien celui du noyau",
   outilsAffiches.map(v => v === "non chiffrable" ? null : parseFloat(v.replace(",", ".")))
     .map(v => v === null ? "nc" : v.toFixed(4)),
   outilsDuJeu.map(v => v === null ? "nc" : v.toFixed(4)));

/* ── L'unité ──
   Un NOMBRE affiché sans son unité est une faute : 0,2452 ne dit pas si c'est
   des euros, des millièmes ou une moyenne. Un tiret « — » n'est pas un nombre :
   il signifie « rien à afficher », et il n'a pas à porter d'unité. Le test
   premier jet exigeait l'unité partout, et donc échouait sur les lignes vides —
   ce qui est un faux signal : il signalait le bon comportement. */
const blocsCppE1 = e1.split('class="cpp">').slice(1);
okVrai("l'écran 1 a des blocs de CPP à examiner", blocsCppE1.length > 0);
okVrai("chaque CPP affiché porte son unité €/pce",
   blocsCppE1.every(m => m.indexOf("€/pce") >= 0 || /^\s*—/.test(m)));
okVrai("et il y en a au moins un qui la porte",
   blocsCppE1.some(m => m.indexOf("€/pce") >= 0));
okVrai("aucun CPP n'est affiché en millièmes ou en centimes (unité inventée)",
   e1.indexOf("millièmes") < 0 && e1.indexOf("centimes") < 0);

/* ── Le PPC par essai : le bénéfice de la v1.0, toujours visible ──
   On vérifie qu'il est affiché DANS L'ÉCRAN 2, sur le scénario de production :
   c'est là que sont portés les essais déjà faits, pas dans l'écran 3 qui ne
   liste que les scénarios à optimiser. */
function valeurCppEssai(html) {
  const i = html.indexOf('class="cppb">');
  if (i < 0) return "bloc-absent";
  const suite = html.slice(i + 'class="cppb">'.length);
  const fin = suite.indexOf("</div>");
  const m = suite.slice(0, fin < 0 ? 200 : fin).match(/^([\d,]+)\s*€/);
  if (m) return m[1];
  return suite.slice(0, 40).indexOf("non chiffrable") >= 0 ? "non chiffrable" : "illisible";
}

okVrai("l'écran 2 affiche les essais portés par le scénario de production",
e2.indexOf("Ce que les essais ont réellement donné") >= 0
   || e2.indexOf("Aucun essai porté par ce scénario de production") >= 0);

/* ══════════════════════════════════════════════════════════════════════════
   L'IMPORT ET LA COHÉRENCE, AU NIVEAU DES ÉCRANS
   La projection est testée ailleurs (test_import.js). Ce qui est testé ICI,
   c'est le trajet complet : un fichier réel → les écrans remplis → les chiffres
   AFFICHÉS égaux à ceux du noyau. C'est exactement le genre de chaîne que la
   seule présence de fonctions ne prouve pas.
   ══════════════════════════════════════════════════════════════════════════ */

const REPO = path.join(__dirname, "..");
const exportSite = JSON.parse(fs.readFileSync(path.join(REPO, "cloud_courant.json"), "utf8"));

async function importer(source, nom, taille) {
  const texte = JSON.stringify(source);
  global.__fichier = {
    nom: nom || "cloud_courant.json",
    taille: taille || texte.length,
    texte: texte,
    erreur: false
  };
  /* le faux input doit PORTER un vrai objet fichier : au premier jet il passait
     `{ files: [{}] }`, donc `f.name` et `f.size` étaient undefined — et trois
     tests échouaient sur une absence de donnée que le produit, lui, fournit. */
  P.chargerFichier({ files: [{ name: global.__fichier.nom, size: global.__fichier.taille }] });
  await tick();
}

(async function importation() {
  ok("la porte d'import existe", typeof P.projeter, "function");
  ok("le panneau s'ouvre", typeof P.ouvrirImport, "function");
  ok("le retour au jeu d'exemple existe", typeof P.retourJeu, "function");

console.log("\n── L'ESSAI : le CPP OBTENU reste lisible ─────────────────────");

/* Le trajet le plus facile à perdre dans une réécriture, et le plus cher.
   Un `indexOf(chaine) >= 0` NE SUFFIT PAS ici : sur un poste, le CPP PRÉVU du
   scénario est imprimé dans l'en-tête, juste au-dessus de l'ESSAI. Une faute
   qui afficherait le prévu à la place de l'obtenu laisserait tous les tests
   verts. On relit donc la VALEUR écrite dans le bloc `.cppb`, et on la compare
   à celle du noyau. */

/* Le `.cppb` d'un ESSAI, isolé par le scénario qui le porte : on cherche le
   <h3> du scénario, on s'arrête au scénario suivant, et on lit le premier
   `.cppb` de ce morceau. Sans l'arrêt, on tomberait sur l'essai du voisin. */
function cppEssaiDuScenario(html, nomScenario) {
  const i = html.indexOf("<h3>" + nomScenario + "</h3>");
  if (i < 0) return "scenario-absent";
  const j = html.indexOf('<section class="preuve">', i + 10);
  const morceau = html.slice(i, j < 0 ? html.length : j);
  const k = morceau.indexOf('class="cppb">');
  if (k < 0) return "essai-absent";
  const m = morceau.slice(k + 'class="cppb">'.length, k + 120).match(/^([\d,]+)\s*€/);
  if (m) return m[1];
  return "non chiffrable";
}

await importer(exportSite);

/* ── CE QUE DIT L'EXPORT RÉEL, avant d'écrire quoi que ce soit ──
   On mesure, on n'imagine pas. Deux faits qui gouvernent les tests :
   (a) les scénarios de PRODUCTION qui portent un essai sont rares — un seul
       sur les dix lignes de l'export ;
   (b) les scénarios où l'essai fait MIEUX que le prévu ne sont pas des
       scénarios de production : ce sont des scénarios à optimiser, donc de
       l'étage 3.
   Ces deux faits sont la raison d'être des trois étages. Le premier jet du test
   supposait le contraire et échouait : il avait raison d'échouer. */
const facts = { prodAvecEssais: [], ecarts: [] };
for (const l of P.ETAT.lignes) for (const r of (l.refs || [])) for (const op of (r.ops || [])) {
  const prod = P.scenarioDeProd(op.scs || []);
  (op.scs || []).forEach(sc => {
    if (sc === prod && (sc.essais || []).length)
      facts.prodAvecEssais.push({ ligne: l, op: op, sc: sc });
    const ob = P.cppEssai(sc, (sc.essais || [])[0]);
    if ((sc.essais || []).length && ob.cpp !== null
        && Math.abs(ob.cpp - P.cppOutillageScenario(sc)) > 1e-9)
      facts.ecarts.push({ ligne: l, op: op, sc: sc, obtenu: ob.cpp,
                          prevu: P.cppOutillageScenario(sc), estProd: sc === prod });
  });
}
okVrai("l'export réel déclare au moins un scénario de production porteur d'essais",
   facts.prodAvecEssais.length > 0);
okVrai("l'export réel contient un poste où l'essai fait MIEUX que le prévu",
   facts.ecarts.length > 0);
okVrai("et ces postes-là sont des scénarios à optimiser, pas de la production",
   facts.ecarts.length > 0 && facts.ecarts.every(x => !x.estProd));

/* ── CONTRE-REGARD 1 — l'étage 2, sur le scénario de production ─────────── */
if (facts.prodAvecEssais.length) {
  const c = facts.prodAvecEssais[0];
  P.ouvrirLigne(c.ligne.id);
  const e2essai = P.ecran2();
  /* On isole le POSTE, pas la page : sans cela on lirait le premier `.cppb` de
     l'écran, qui pourrait appartenir à un autre poste de la même ligne. */
  const code = P.detailLigne(c.ligne).refs
    .flatMap(r => r.postes).filter(p => p.prod === c.sc)[0].code;
  const debut = e2essai.indexOf("<h3>" + code + "</h3>");
  const suite = debut < 0 ? "" : e2essai.slice(debut, e2essai.indexOf("</section>", debut));
  const k = suite.indexOf('class="cppb">');
  const obtenu = P.cppEssai(c.sc, c.sc.essais[0]).cpp;
  const prevu = P.cppOutillageScenario(c.sc);
  ok("l'écran 2 affiche le CPP obtenu par l'essai du scénario de production",
     k < 0 ? "essai-absent"
           : (suite.slice(k + 'class="cppb">'.length).match(/^([\d,]+)\s*€/) || [])[1],
     fmtFr(obtenu, 4));
  /* Sur CE poste, l'essai redonne exactement le prévu. Une faute qui afficherait
     le prévu à la place de l'obtenu y serait donc INDÉTECTABLE — d'où le
     contre-regard 2, qui se place sur un poste où les deux diffèrent. On ne
     simule donc pas ici une distinction qui n'existe pas : on le déclare. */
  ok("sur ce poste, l'essai redonne le prévu : ce poste ne peut pas les distinguer",
     obtenu === prevu, true);
  okVrai("le contre-regard 2 se place sur un poste où les deux diffèrent",
     facts.ecarts.some(x => Math.abs(x.obtenu - x.prevu) > 1e-9));
}

/* ── CONTRE-REGARD 2 — l'étage 3, là où prévu et obtenu diffèrent ───────── */
const cible = facts.ecarts.find(x => x.obtenu < x.prevu);
okVrai("l'export réel contient un scénario où l'essai fait mieux que prévu", !!cible);
if (cible) {
  P.ouvrirLigne(cible.ligne.id);
  const e3essai = P.ecran3();
  ok("l'écran 3 montre ce scénario, et le range parmi les scénarios à optimiser",
     e3essai.indexOf("<h3>" + cible.sc.name + "</h3>") >= 0, true);

  const affiche = cppEssaiDuScenario(e3essai, cible.sc.name);
  ok("le CPP écrit dans le bloc essai est celui que l'essai a donné",
     affiche, fmtFr(cible.obtenu, 4));
  ok("et il n'est PAS le CPP prévu du scénario",
     affiche === fmtFr(cible.prevu, 4), false);
  ok("l'écart annoncé entre prévu et obtenu est le bon",
     e3essai.indexOf(fmtFr(Math.abs(cible.obtenu - cible.prevu), 4)) >= 0, true);
  ok("le prévu et l'obtenu sont annoncés dans la même unité",
     e3essai.indexOf("même unité que les chiffres du dessus") >= 0, true);

  /* Et l'étage 2, sur ce poste, ne doit ni montrer cet essai, ni le taire :
     il doit renvoyer vers l'étage 3. Un CPP de production affiché seul ferait
     croire que les essais n'ont jamais eu lieu. */
  const e2poste = P.ecran2();
  ok("l'écran 2 ne montre pas les essais des scénarios à optimiser",
     e2poste.indexOf(cible.sc.name) < 0, true);
  okVrai("l'écran 2 renvoie vers l'étage 3 pour ces scénarios",
     e2poste.indexOf("autre") >= 0 && e2poste.indexOf("Scénario et optimisation") >= 0);
}

P.retourJeu();

console.log("\n" + "=".repeat(60));
console.log("PROTO ÉCRANS : " + total + " tests | " + echecs + " echecs");
console.log(echecs ? "*** LE PROTO EST ROUGE ***" : "TOUT EST VERT");
process.exit(echecs ? 1 : 0);
})();
