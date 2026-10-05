/* ============================================================================
   2resume — LE HARNIAIS DES ÉCRANS
   ----------------------------------------------------------------------------
   Il ne refait pas les maths (le noyau a ses tests) : il vérifie que les
   écrans AFFICHENT ce que le noyau calcule — par la VALEUR, jamais par la
   présence d'une chaîne. La leçon du Tour 54 tient ici en une ligne : un test
   qui cherche « 0,1735 » quelque part dans la page passerait avec le CPP
   PRÉVU imprimé à la place de l'OBTENU. On extrait donc le nombre du bloc
   qu'on vérifie, et on compare au calcul du noyau.

   Exécution : node test_app.js  — refuse de tourner sur un assemblage périmé.
   ========================================================================== */

const fs = require("fs");
const path = require("path");
/* L'import de bout en bout traverse un FileReader asynchrone : tout le harnais
   vit dans une fonction async — un `await` de haut niveau ferait choisir à
   Node entre CommonJS et ESM, et il choisirait mal. */
(async () => {

let total = 0, echecs = 0;
function ok(nom, obtenu, attendu, tol) {
  total++;
  let bon;
  if (typeof attendu === "number" && typeof obtenu === "number" && tol !== undefined) {
    bon = Math.abs(obtenu - attendu) <= tol;
  } else {
    bon = JSON.stringify(obtenu) === JSON.stringify(attendu);
  }
  if (!bon) { echecs++; console.log("  ECHEC " + nom + " — obtenu " + JSON.stringify(obtenu) + ", attendu " + JSON.stringify(attendu)); }
  else console.log("  ok   " + nom);
}
function okVrai(nom, condition) { ok(nom, !!condition, true); }

/* ── un DOM minimal, mais suffisant pour atteindre TOUTES les portes ─────── */
function faitElement(id) {
  return {
    id: id, innerHTML: "", textContent: "", value: "", hidden: false,
    style: {}, dataset: {},
    classList: { add() {}, remove() {}, contains() { return false; } },
    addEventListener() {}, removeEventListener() {},
    getAttribute() { return null; }, setAttribute() {}, removeAttribute() {},
    appendChild() {}, querySelector() { return null; }, querySelectorAll() { return []; },
    closest() { return null; }, click() {}, remove() {},
    scrollIntoView() {}, focus() {},
    get elements() { return []; }
  };
}
global.window = { scrollTo() {}, print() {}, addEventListener() {} };
global.document = {
  documentElement: faitElement("html"),
  getElementById(id) { return faitElement(id); },
  querySelector() { return null; }, querySelectorAll() { return []; },
  addEventListener() {}, createElement() { return faitElement("x"); },
  body: faitElement("body")
};
global.location = { href: "http://localhost/2resume" };
global.confirm = () => true;

/* Le stockage et la lecture de fichier, EN VRAI : le harnais du proto a déjà
   perdu 105 tests verts parce que sa porte d'import était inatteignable. */
const _store = new Map();
global.localStorage = {
  getItem(k) { return _store.has(k) ? _store.get(k) : null; },
  setItem(k, v) { _store.set(k, String(v)); },
  removeItem(k) { _store.delete(k); },
  clear() { _store.clear(); }
};
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
function tick() { return new Promise(r => setTimeout(r, 5)); }

/* ── le fichier assemblé ──────────────────────────────────────────────────── */
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
if (!blocs.length) { console.log("  ECHEC aucun bloc script"); process.exit(1); }

let src = blocs.join("\n");
const avant = src.length;
src = src.replace(/chargerLocal\(\);\s*\n\s*rendre\(\);\s*$/, "");
if (src.length === avant) {
  console.log("  ECHEC l'auto-rendre final n'a pas été neutralisé — le harnais ne");
  console.log("         pourrait pas distinguer une panne réelle d'un DOM absent.");
  process.exit(1);
}

let api;
try {
  api = (new Function(src + "\nreturn { R: window.resume };")).call(globalThis);
} catch (e) {
  console.log("  ECHEC l'application ne s'exécute pas : " + e.message);
  console.log(e.stack.split("\n").slice(0, 5).join("\n"));
  process.exit(1);
}
const R = api.R;
okVrai("l'application s'exécute sans exception", !!R);

/* ── L'ASSEMBLAGE EST-IL À JOUR ? sinon on refuse de tourner ─────────────── */
const crypto = require("crypto");
function empreinteSources() {
  return crypto.createHash("sha256")
    .update(["coeur.js", "donnees.js", "import.js", "app.html"]
      .map(f => fs.readFileSync(path.join(__dirname, f), "utf8"))
      .join("\u0000"), "utf8")
    .digest("hex").slice(0, 16);
}
const attendue = empreinteSources();
ok("l'assemblage index.html est à jour", R.EMPREINTE_ASSEMBLAGE, attendue);
if (R.EMPREINTE_ASSEMBLAGE !== attendue) {
  console.log("         → index.html date d'avant la dernière modification.");
  console.log("         → Relancez : python assembler.py");
  process.exit(1);
}

/* ── LES PORTES : chaque bouton a une fonction (typeof, pas lecture) ─────── */
console.log("\n── LES PORTES ──");
const PORTES = [
  ["la navigation", ["aller", "rendre", "faire"]],
  ["l'ouverture d'une ligne", ["ouvrirLigne", "ligneCourante"]],
  ["les cinq écrans", ["ecran1", "ecran2", "ecran3", "ecran4", "ecran5"]],
  ["l'import", ["ouvrirImport", "appliquerImport", "retourJeu"]],
  ["la saisie d'un essai", ["ouvrirEssai", "enregistrerEssai"]],
  ["les statuts", ["changerStatut"]],
  ["l'édition d'un logement", ["ouvrirLogement", "majChampLogement"]],
  ["les réglages et le partage", ["ouvrirReglages", "ouvrirPartage"]],
  ["l'export et la persistance", ["exporter", "sauvegarderLocal", "chargerLocal"]],
  ["la source, toujours affichée", ["badgeSource", "panoramaSiImport"]]
];
PORTES.forEach(([nom, noms]) => noms.forEach(n => ok("porte : " + n + " (" + nom + ")", typeof R[n], "function")));

console.log("\n── LE JEU D'EXEMPLE : les écrans affichent ce que le noyau calcule ──");
_store.clear();
R.chargerLocal();
const ETAT = R.ETAT;
ok("le jeu de départ est chargé", ETAT.donnees.lignes.length, 3);
ok("la source est déclarée jeu d'exemple", ETAT.source.type, "jeu");
okVrai("le bandeau source le dit (esc transforme l'apostrophe)",
  R.badgeSource().indexOf("aucun chiffre r") >= 0);

const N = (function () {
  const coeur = fs.readFileSync(path.join(__dirname, "coeur.js"), "utf8");
  return new Function(coeur + "\nreturn { recapLignes, verdictLigne, cppOutillageScenario, cppEssai, statutEssai, sommeGains, tuilesDeLignes, coutLogement };")();
})();

const e1 = R.ecran1();
okVrai("l'écran 1 nomme les trois lignes", ["EMAG 1", "EMAG 3", "PCI 4"].every(n => e1.indexOf(n) >= 0));
okVrai("l'écran 1 déclare la formule du CPP", e1.indexOf("prix ÷ (arêtes × charnière)") >= 0);
okVrai("l'écran 1 dit ce qui manque", e1.indexOf("Ce qui manque") >= 0);
okVrai("l'écran 1 déclare ce qu'il ne montre pas", e1.indexOf("ne montre pas") >= 0);
const rec = N.recapLignes(ETAT.donnees.lignes.map(l => N.verdictLigne(l)));
okVrai("le KPI « à chiffrer » affiche la valeur du noyau (" + rec.aChiffrer + ")",
  e1.indexOf("<em>" + rec.aChiffrer + "</em>") >= 0);

const e2 = R.ecran2();
const emag1 = ETAT.donnees.lignes.find(l => l.nom === "EMAG 1");
ETAT.ligneId = emag1.id;
const e2emag = R.ecran2();
okVrai("l'écran 2 ouvre sur EMAG 1", e2emag.indexOf("EMAG 1") >= 0);
const prodEmag = (function () {
  const scs = emag1.references[0].ops[0].scenarios;
  return scs.find(s => s.baseline === true) || scs.find(s => s.statut === "serie");
})();
const cppPrevu = N.cppOutillageScenario(prodEmag);
okVrai("le CPP prévu du scénario de production est affiché en valeur (" + cppPrevu.toFixed(4).replace(".", ",") + ")",
  e2emag.indexOf(cppPrevu.toFixed(4).replace(".", ",")) >= 0);
okVrai("l'écran 2 montre un essai porté par la production… ou son absence déclarée",
  e2emag.indexOf("Aucun essai porté") >= 0);
okVrai("le poste sans production d'EMAG 3 reste visible et le dit",
  (() => { const emag3 = ETAT.donnees.lignes.find(l => l.nom === "EMAG 3");
    ETAT.ligneId = emag3.id; const e = R.ecran2();
    return e.indexOf("sans scénario de production") >= 0 && e.indexOf("sans production") >= 0; })());
ETAT.ligneId = emag1.id;

const e4 = R.ecran4();
okVrai("l'écran 4 porte la décision ESSAYER du jeu", e4.indexOf("ESSAYER") >= 0);
okVrai("l'écran 4 porte la décision CHIFFRER (PCI 4)", e4.indexOf("CHIFFRER") >= 0);
okVrai("l'écran 4 sépare gain acté et projeté", e4.indexOf("Gain acté") >= 0 && e4.indexOf("Gain projeté") >= 0);
const e5 = R.ecran5();
okVrai("l'écran 5 produit une page A4 datée", e5.indexOf("Suivi d'optimisation") >= 0 && e5.indexOf("Confidentiel interne") >= 0);

console.log("\n── L'IMPORT, BOUT EN BOUT : le fichier réel traverse TOUTE la chaîne ──");
async function importer(nomReel, nomAffiche) {
  const texte = fs.readFileSync(path.join(__dirname, "..", nomReel), "utf8");
  global.__fichier = { nom: nomAffiche || nomReel, taille: texte.length, texte: texte, erreur: false };
  R.chargerLocal(); /* repartir du jeu, comme un poste vierge */
  const bon = R.appliquerImport(JSON.parse(texte), nomAffiche || nomReel, texte.length);
  await tick();
  return bon;
}
const bonImport = await importer("cloud_courant.json");
okVrai("l'import du fichier réel réussit", !!bonImport);
await tick();
ok("les dix lignes sont là", ETAT.donnees.lignes.length, 10);
ok("la source est déclarée importée", ETAT.source.type, "import");
okVrai("le bandeau porte le nom du fichier", R.badgeSource().indexOf("cloud_courant.json") >= 0);
okVrai("le panorama d'import compte ce qui est entré",
  R.panoramaSiImport().indexOf("Import réussi — cloud_courant.json") >= 0);
okVrai("il nomme ce qui a été jeté", R.panoramaSiImport().indexOf("relevés Marposs") >= 0);
ok("les essais sont repris", ETAT.donnees.lignes.reduce((a, l) => a + l.references.reduce((b, rf) =>
  b + rf.ops.reduce((c, op) => c + op.scenarios.reduce((d, sc) => d + sc.essais.length, 0), 0), 0), 0), 5);

/* LA valeur qui a motivé l'outil : le CPP obtenu du SL500, extrait du bloc
   exact de l'écran, et JAMAIS confondu avec le prévu. */
let sl500 = null;
ETAT.donnees.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op =>
  op.scenarios.forEach(sc => { if (/SL500/i.test(sc.name)) sl500 = { sc: sc, op: op, l: l }; }))));
okVrai("le scénario SL500 est trouvé après import", !!sl500);
const obtenu = N.cppEssai(sl500.sc, sl500.sc.essais[0]);
ok("le CPP obtenu calculé par le noyau", obtenu.cpp, 0.0478, 1e-9);
const ligneEssai = R.essaiLigneHTML(sl500.sc, sl500.sc.essais[0]);
const mObtenu = /CPP obtenu <b class="num">([\d,]+) €/.exec(ligneEssai);
okVrai("le bloc « CPP obtenu » existe dans la ligne d'essai", !!mObtenu);
ok("ET IL AFFICHE 0,0478 — PAS le prévu", mObtenu && mObtenu[1], "0,0478");
const mPrevu = /\(prévu ([\d,]+) €\)/.exec(ligneEssai);
ok("et le prévu, à côté, vaut 0,1735", mPrevu && mPrevu[1], "0,1735");

/* L'écran 3 montre ces scénarios hors production. */
ETAT.ligneId = sl500.l.id; ETAT.etape = 3;
const e3 = R.ecran3();
okVrai("l'écran 3 porte le scénario SL500", e3.indexOf("SNGN 090416-F SL500") >= 0);
okVrai("l'écran 3 affiche le CPP obtenu de l'essai", e3.indexOf("0,0478") >= 0);

console.log("\n── LA SAISIE : un essai créé dans l'outil est un essai du noyau ──");
R.chargerLocal(); /* retour au jeu d'exemple */
const emag3 = ETAT.donnees.lignes.find(l => l.nom === "EMAG 3");
ETAT.ligneId = emag3.id;
const op10e3 = emag3.references[0].ops[0];
const prodE3 = op10e3.scenarios[0];
R.ouvrirEssai(op10e3.id, prodE3.id);
okVrai("le formulaire s'ouvre", !!ETAT.saisie);
ok("une charnière pré-remplie depuis le scénario", ETAT.saisie.logements[0].charniere, 30);
ETAT.saisie.titre = "Série de contrôle";
ETAT.saisie.prels = [
  { piece: 5, battD: "0.05", battG: "0.06", usure: "ok", logementId: "" },
  { piece: 10, battD: "0.14", battG: "0.02", usure: "", logementId: "" }
];
R.enregistrerEssai();
ok("l'essai est entré dans le scénario", prodE3.essais.length, 1);
ok("les prélèvements sont entrés", prodE3.essais[0].prelevements.length, 2);
const st = (function () { const coeur = fs.readFileSync(path.join(__dirname, "coeur.js"), "utf8");
  return new Function(coeur + "\nreturn { statutEssai, battDe };")(); })();
const verdictSaisi = st.statutEssai(prodE3, prodE3.essais[0]);
ok("l'essai saisi est NON CONFORME (le pire côté : 0,14 > 0,12)", verdictSaisi.code, "nonconforme");
ok("la pièce fautive est la 10", verdictSaisi.piece, 10);
ETAT.etape = 2;
okVrai("et l'écran 2 de la ligne l'affiche", R.ecran2().indexOf("hors tolérance") >= 0);

console.log("\n── L'ÉDITION : corriger un prix recalcule tout l'étage au-dessus ──");
R.chargerLocal();
const emag1b = ETAT.donnees.lignes.find(l => l.nom === "EMAG 1");
ETAT.ligneId = emag1b.id;
const op10b = emag1b.references[0].ops[0];
const prodb = op10b.scenarios.find(s => s.baseline === true);
const logb = prodb.outils[0].logements[0];
R.ouvrirLogement(logb.id, prodb.id);
R.majChampLogement(logb.id, prodb.id, "prix", "14");
ok("le prix est porté par le logement", logb.prix, 14);
const nouveauCpp = N.cppOutillageScenario(prodb);
ok("le CPP du scénario a suivi (14/(2×40) + 7/(2×40))", nouveauCpp, 0.2625, 1e-12);
ETAT.etape = 2;
okVrai("et l'écran 2 affiche la NOUVELLE valeur", R.ecran2().indexOf("0,2625") >= 0);
okVrai("le MABEC saisi arrive jusqu'à l'écran",
  (R.majChampLogement(logb.id, prodb.id, "mabec", "Z000 999 888"), R.ecran2().indexOf("Z000 999 888") >= 0));

console.log("\n── LES STATUTS : passer en production change la production ──");
R.chargerLocal();
const emag1c = ETAT.donnees.lignes.find(l => l.nom === "EMAG 1");
const op10c = emag1c.references[0].ops[0];
const essaiSc = op10c.scenarios.find(s => !s.baseline);
R.changerStatut(essaiSc.id, "serie");
ok("le statut est porté", essaiSc.statut, "serie");
ok("et le scénario devient la baseline", essaiSc.baseline, true);
const coeur2 = fs.readFileSync(path.join(__dirname, "coeur.js"), "utf8");
const scen2 = new Function(coeur2 + "\nreturn { scenarioDeProd };")();
ok("le scénario de production du poste EST maintenant l'ancien essai",
  scen2.scenarioDeProd(op10c.scenarios).id, essaiSc.id);

console.log("\n── LE THÈME ET LA SOURCE ──");
R.faire("basculer-theme");
ok("le thème bascule et persiste", ETAT.theme, "dark");
okVrai("le badge source cite toujours sa source",
  R.badgeSource().indexOf("Source :") >= 0 && R.badgeSource().indexOf("v" + (ETAT.donnees.version || "0")) >= 0
    || R.badgeSource().indexOf("assemblage") >= 0);

console.log("\n── LA PERSISTANCE : ce qui est saisi survit à une relecture ──");
_store.clear();
R.chargerLocal();
const avantSauve = ETAT.donnees.lignes.length;
R.sauvegarderLocal();
ETAT.donnees = (function () { const imp = fs.readFileSync(path.join(__dirname, "import.js"), "utf8");
  return null; })() || ETAT.donnees;
ETAT.donnees = { lignes: [], projets: [], livraisons: [], specsUsine: {} }; /* on casse exprès */
R.chargerLocal();
ok("la relecture restaure les données sauvegardées", ETAT.donnees.lignes.length, avantSauve);

console.log("\n── ERREUR D'IMPORT : un mauvais fichier est refusé, avec sa raison ──");
R.appliquerImport({ foo: 1 }, "mauvais.json", 12);
ok("la source bascule en erreur", ETAT.source.type, "erreur");

console.log("\n── LE CONTRE-REGARD : la suite voit-elle la règle qu'elle protège ? ──");
/* La constitution v1.7 : 0 échec sans exécution ne veut rien dire. Ici on
   prouve le contraire : on CASSE la formule du CPP dans une copie du noyau,
   et on vérifie que l'invariant testé ci-dessus ÉCHOUE sur la copie. Si un
   jour quelqu'un casse `coutLogement` pour de bon, ce filet l'attrapera. */
const coeurSource = fs.readFileSync(path.join(__dirname, "coeur.js"), "utf8");
function chargeNoyau(codeSource) {
  return new Function(codeSource + "\nreturn { coutLogement, outillageDeScenario, cppOutillageScenario, cppEssai, battDe };")();
}
/* La règle protégée n'est PAS « la somme des parties égale le total » : cette
   égalité reste vraie même avec une formule fausse, puisqu'elle somme la même
   faute des deux côtés. La règle protégée est la VALEUR ABSOLUE : 7 € ÷
   (2 arêtes × 40 pièces) = 0,0875 €, la formule du classeur de Matis. On
   montre donc qu'une formule cassée échoue à CETTE assertion. */
const noyauBon = chargeNoyau(coeurSource);
const noyauCasse = chargeNoyau(coeurSource.replace(
  "return prix / (aretes * charniere);", "return prix * aretes * charniere;"));
ok("la formule saine vaut 0,0875 — le test du noyau la verrouille",
  noyauBon.coutLogement({ prix: 7, aretes: 2, charniere: 40 }), 0.0875, 1e-12);
okVrai("et la formule CASSÉE (multiplication) donnerait 560 : la suite la verrait",
  Math.abs(noyauCasse.coutLogement({ prix: 7, aretes: 2, charniere: 40 }) - 0.0875) > 1);
/* Contre-regard 2 : si un jour `cppEssai` renvoyait le PRÉVU au lieu de
   l'OBTENU, la valeur 0,0478 affichée plus haut ne sortirait plus. On le
   prouve en cassant la fonction sur les données réelles. */
const noyauPrevu = new Function(
  coeurSource.replace("const cpp = n ? total : null;", "const cpp = cppOutillageScenario(sc);")
  + "\nreturn { cppEssai };")();
const sl500Brut = (function () {
  const ccBrut = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "cloud_courant.json"), "utf8"));
  const proj = (function () { const imp = fs.readFileSync(path.join(__dirname, "import.js"), "utf8");
    return new Function(coeurSource + "\n" + imp + "\nreturn { projeter };")(); })().projeter(ccBrut);
  let trouve = null;
  proj.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc => {
    if (/SL500/i.test(sc.name)) trouve = sc;
  }))));
  return trouve;
})();
okVrai("le scénario SL500 existe dans la projection brute", !!sl500Brut);
ok("le noyau sain donne le CPP OBTENU 0,0478",
  noyauBon.cppEssai(sl500Brut, sl500Brut.essais[0]).cpp, 0.0478, 1e-9);
okVrai("et le noyau TRUCQUÉ (prévu à la place de l'obtenu) donnerait AUTRE CHOSE : la différence est visible",
  Math.abs(noyauPrevu.cppEssai(sl500Brut, sl500Brut.essais[0]).cpp - 0.0478) > 0.001);
/* Contre-regard 3 : le pont D/G. Si `battDe` prenait la moyenne, la pièce 10
   de l'essai saisi plus haut ne serait plus hors tolérance. */
const noyauMoyenne = new Function(
  coeurSource.replace("return Math.max.apply(null, cotes);", "return cotes.reduce((a,b)=>a+b,0)/cotes.length;")
  + "\nreturn { battDe };")();
ok("le pire côté : max(0,14 ; 0,02) = 0,14", noyauBon.battDe({ battD: 0.14, battG: 0.02 }), 0.14);
ok("la MOYENNE donnerait 0,08 — sous le seuil : le pont change le verdict, donc le test le voit",
  noyauMoyenne.battDe({ battD: 0.14, battG: 0.02 }), 0.08);

console.log("\n" + total + " tests exécutés, " + echecs + " échec(s)");
if (echecs) { console.log("ROUGE — " + echecs + " échec(s)"); process.exit(1); }
console.log("TOUT EST VERT");
})().catch(e => { console.log("  ECHEC le harnais lui-même a planté : " + e.message); process.exit(1); });
