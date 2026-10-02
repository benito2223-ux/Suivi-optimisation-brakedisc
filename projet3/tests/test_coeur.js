/* ============================================================================
   PROJET3 — LES TESTS DU NOYAU
   Écrits AVANT les écrans (cahier §8). Chaque invariant du cahier a un test ici.
   Exécution : node tests/test_coeur.js
   ========================================================================== */

const { charger, creerJuge } = require("./harnais.js");

const N = charger("src/coeur.js", [
  "VERSION", "fmt", "fmtDispo", "fmtEuro", "nombre",
  "coutLogement", "cppOutillageScenario", "cppScenarioDetail", "cppOutillageOutil",
  "outillageDeScenario", "cppEssaiObtenu", "essaisAvecCPP",
  "coutMachinePiece", "cycleSecondes", "cheminCPP",
  "battDe", "raDe", "conforme", "charniereVisee", "statutEssai", "statutScenario",
  "scenarioDeProd", "verdictPoste", "decisionPoste",
  "opCodeDe", "postesDeLigne", "verdictsDeLigne", "cppReference",
  "tuileDeLigne", "tuilesDeLignes", "detailLigne",
  "gainLigne", "recapAtelier",
  "familleDeLigne", "rangLigne", "codeLigneDe",
  "PALETTE_PROJETS", "rangLigne", "couleurProjetLibre", "scenariosDeProjet",
  "projetsDeScenario", "projetsDeOP", "PROJET_STATUTS", "responsableDe",
  "capturerLivraison", "uid", "dateCourte", "dateHeure", "clePorteOutil"
]);

const j = creerJuge("PROJET3 NOYAU");
const ok = j.ok, bloc = j.bloc;

/* ---- fabriques, minimales et lisibles ---- */
function log(id, nom, prix, aretes, charniere, extra) {
  return Object.assign({ id: id, nom: nom, ref: "ART-X", prix: prix, aretes: aretes, charniere: charniere }, extra || {});
}
function outil(id, numero, logements, extra) {
  return Object.assign({ id: id, numero: numero, logements: logements }, extra || {});
}
function scn(id, nom, baseline, outils, extra) {
  return Object.assign({
    id: id, name: nom, baseline: !!baseline, statut: baseline ? "serie" : "etude",
    outils: outils, essais: [], validationThreshold: 5
  }, extra || {});
}
function refEx(id, nom, cible, volume) {
  return { id: id, nom: nom, cibleCPP: cible, productionAnnuelle: volume };
}
function opEx(id, nom, scs, extra) {
  return Object.assign({ id: id, nom: nom, scenarios: scs }, extra || {});
}
function ligneEx(id, nom, refs) { return { id: id, nom: nom, coutHoraire: 60, references: refs }; }
function essaiEx(id, opts) {
  return Object.assign({
    id: id, titre: "Essai", date: "2026-10-01",
    params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 100 }] },
    prelevements: []
  }, opts || {});
}

/* ============================================================================
   1. LE FORMATAGE — un absent ne dit jamais 0
   ============================================================================ */

console.log("\n── LE FORMATAGE ──────────────────────────────────────────────");

ok("fmt(null) reste un tiret", N.fmt(null, 3), "—");
ok("fmt('') reste un tiret", N.fmt("", 3), "—");
ok("fmt(NaN) reste un tiret", N.fmt(NaN, 3), "—");
ok("fmt formate en virgule française", N.fmt(1234.5, 2), "1234,50");
ok("fmt 0 est un vrai 0 (mesuré)", N.fmt(0, 3), "0,000");
ok("fmtDispo distingue 0 de pas saisi", N.fmtDispo(0, 3, "non saisi"), "0,000");
ok("fmtDispo dit ce qui manque", N.fmtDispo("", 3, "— volume annuel non saisi"), "— volume annuel non saisi");
ok("fmtEuro fait 4 décimales par défaut", N.fmtEuro(0.17352), "0,1735 €");
ok("nombre(null) est null", N.nombre(null), null);
ok("nombre('abc') est null", N.nombre("abc"), null);
ok("nombre('38.0') vaut 38", N.nombre("38.0"), 38);

/* ============================================================================
   2. LE CPP OUTILLAGE — le driver
   ============================================================================ */

console.log("\n── LE CPP OUTILLAGE (prix ÷ (arêtes × charnière)) ───────────");

ok("un logement simple : 38 / (8 × 800)", N.coutLogement(log("g1", "D1", 38, 8, 800)), 0.0059375, 1e-9);
ok("prix manquant -> non chiffrable, jamais 0", N.coutLogement(log("g2", "D2", "", 8, 800)), null);
ok("prix 0 -> non chiffrable (un prix nul n'est pas gratuit)", N.coutLogement(log("g3", "D3", 0, 8, 800)), null);
ok("arêtes manquantes -> non chiffrable", N.coutLogement(log("g4", "D4", 38, "", 800)), null);
ok("charnière manquante -> non chiffrable", N.coutLogement(log("g5", "D5", 38, 8, "")), null);
ok("charnière 0 -> non chiffrable", N.coutLogement(log("g6", "D6", 38, 8, 0)), null);

const scChiffre = scn("s1", "Prod", true, [
  outil("t1", "T511", [log("g1", "D1", 38, 8, 800), log("g2", "D2", 19, 4, 700)])
]);
ok("CPP scénario = somme des logements", N.cppOutillageScenario(scChiffre),
   38 / 6400 + 19 / 2800, 1e-9);

const scIncomplet = scn("s2", "Incomplet", false, [
  outil("t1", "T511", [log("g1", "D1", 38, 8, 800), log("g2", "D2", 19, 4, "")])
]);
ok("un scénario à un logement incomplet reste chiffrable sur ses logements remplis",
   N.cppOutillageScenario(scIncomplet), 38 / 6400, 1e-9);
ok("…et le logement écarté est COMPTE, pas dilué",
   N.cppScenarioDetail(scIncomplet).nbNonChiffrables, 1);
ok("un scénario sans logement chiffrable -> null",
   N.cppOutillageScenario(scn("s3", "Vide", false, [outil("t1", "T1", [log("g1", "D1", "", "", "")])])), null);
ok("un scénario sans outils -> null", N.cppOutillageScenario(scn("s4", "Nu", false, [])), null);

ok("CPP d'un outil", N.cppOutillageOutil(scChiffre.outils[0]), 38 / 6400 + 19 / 2800, 1e-9);

/* La décomposition : un seau par outil, même numéro ≠ même seau. */
const scDeuxOutilsMemeNumero = scn("s5", "Deux seaux", false, [
  outil("tA", "T513", [log("gA1", "D1", 10, 4, 100)]),
  outil("tB", "T513", [log("gB1", "D1", 20, 4, 100)])
]);
const dec = N.outillageDeScenario(scDeuxOutilsMemeNumero);
ok("deux outils du même numéro restent deux seaux", dec.outils.length, 2);
ok("le premier seau porte le prix du premier outil", dec.outils[0].logements[0].prix, 10);
ok("le deuxième seau porte le prix du deuxième outil", dec.outils[1].logements[0].prix, 20);
ok("le CPP de chaque seau est le sien", dec.outils[0].cpp, 10 / 400, 1e-9);
ok("le CPP total est la somme des seaux", dec.cpp, 10 / 400 + 20 / 400, 1e-9);

/* ============================================================================
   3. LE CPP OBTENU PAR ESSAI — prévu contre obtenu
   ============================================================================ */

console.log("\n── LE CPP OBTENU PAR ESSAI (prévu ≠ obtenu) ─────────────────");

const scEssai = scn("s6", "Essai SL500", false, [
  outil("t1", "T511", [log("g1", "D1", 38, 8, 800)])
]);
scEssai.essais.push(essaiEx("e1", {
  params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 2400 }] },
  prelevements: [{ id: "p1", piece: 1, batt: 0.10 }]
}));
const obtenu = N.cppEssaiObtenu(scEssai, scEssai.essais[0]);
ok("la charnière mesurée de l'essai change le CPP obtenu", obtenu.cpp, 38 / 19200, 1e-9);
ok("le CPP prévu du scénario reste celui des logements", N.cppOutillageScenario(scEssai), 38 / 6400, 1e-9);
ok("un essai sans logement suivi n'est pas chiffrable",
   N.cppEssaiObtenu(scEssai, essaiEx("e2", { params: { logements: [] } })).cpp, null);
ok("un essai qui suit un logement inconnu est compté écarté",
   N.cppEssaiObtenu(scEssai, essaiEx("e3", {
     params: { logements: [{ logementId: "inconnu", logementNom: "X", charniere: 100 }] }
   })).nonChiffrables, 1);
ok("le prix peut venir du prélèvement si la définition manque",
   N.cppEssaiObtenu(scn("s7", "Nu", false, [outil("t1", "T1", [log("g1", "D1", "", "", "")])]),
     essaiEx("e4", { params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 100, prix: 10, aretes: 4 }] } })).cpp,
   10 / 400, 1e-9);
ok("essaisAvecCPP donne prévu (scénario) et obtenu (essai) côte à côte",
   N.essaisAvecCPP(scEssai).length, 1);

/* ============================================================================
   4. LE TEMPS MACHINE — secondaire, jamais comparable au classeur
   ============================================================================ */

console.log("\n── LE TEMPS MACHINE (à côté, jamais fusionné) ───────────────");

ok("cycle non saisi -> non chiffrable", N.cycleSecondes(scChiffre), null);
const scCycle = scn("s8", "Avec cycle", false, [
  outil("t1", "T1", [log("g1", "D1", 38, 8, 800, { tempsCoupe: 30, tempsDeplacement: 10 })])
]);
ok("cycle complet = somme coupe + déplacement", N.cycleSecondes(scCycle), 40, 1e-9);
const scCycleVide = scn("s9", "Cycle vide", false, [outil("t1", "T1", [])]);
ok("un outil sans logement n'est pas un cycle complet", N.cycleSecondes(scCycleVide), null);
const scSimu = scn("s10", "Simultané", false, [
  outil("t1", "T1", [log("g1", "D1", 38, 8, 800, { tempsCoupe: 30, tempsDeplacement: 0 })]),
  outil("t2", "T2", [log("g2", "D2", 19, 4, 700, { tempsCoupe: 60, tempsDeplacement: 0 })], { simultaneAvecPrecedent: true })
]);
ok("des outils simultanés prennent le plus long, pas la somme", N.cycleSecondes(scSimu), 60, 1e-9);
ok("le temps machine = (taux/3600) × cycle", N.coutMachinePiece(scCycle, ligneEx("l1", "EMAG 1", [])), (60 / 3600) * 40, 1e-9);
ok("sans taux horaire, le temps machine n'est pas chiffrable", N.coutMachinePiece(scCycle, { id: "l2", nom: "PCI 1", coutHoraire: "", references: [] }), null);

/* ============================================================================
   5. LE CHEMIN VERS LA CIBLE
   ============================================================================ */

console.log("\n── LE CHEMIN PROD → CIBLE ───────────────────────────────────");

ok("chemin complet sous la cible = 100", N.cheminCPP(0.10, 0.08, 0.11), 100);
ok("chemin partiel", N.cheminCPP(0.20, 0.15, 0.10), 50, 1e-9);
ok("clampé à 0 si l'essai fait pire", N.cheminCPP(0.20, 0.25, 0.10), 0);
ok("sans cible, pas de chemin (null, pas 0)", N.cheminCPP(0.20, 0.15, ""), null);
ok("sans prod, pas de chemin", N.cheminCPP(null, 0.15, 0.10), null);

/* ============================================================================
   6. LA PREUVE — battement pire des deux côtés, Ra, critères
   ============================================================================ */

console.log("\n── LA PREUVE (le pire des deux côtés, jamais la moyenne) ────");

ok("batt rempli s'il existe", N.battDe({ batt: 0.10, battD: 0.20, battG: 0.05 }), 0.10);
ok("batt vide -> le PIRE des deux côtés", N.battDe({ batt: "", battD: 0.20, battG: 0.05 }), 0.20);
ok("batt vide et un seul côté -> ce côté", N.battDe({ batt: "", battD: "", battG: 0.05 }), 0.05);
ok("rien du tout -> non mesurable", isNaN(N.battDe({ batt: "", battD: "", battG: "" })), true);

ok("Ra vient de valeur2", N.raDe({ valeur2: 0.7 }), 0.7);
ok("Ra vient de l'ancienne forme valeurs.cs1.v", N.raDe({ valeurs: { cs1: { v: 0.9 } } }), 0.9);
ok("Ra absent -> null, jamais 0", N.raDe({}), null);

const scConf = scn("s11", "Prod", true, [outil("t1", "T1", [log("g1", "D1", 38, 8, 800)])]);
ok("conforme : battement dans la limite", N.conforme(scConf, { batt: 0.10 }).ok, true);
ok("non conforme : battement dépassé, avec le motif",
   N.conforme(scConf, { batt: 0.15 }).ok, false);
ok("le motif porte les deux chiffres",
   N.conforme(scConf, { batt: 0.15 }).motif.indexOf("0,150") >= 0, true);
ok("le pire des deux côtés juge la conformité",
   N.conforme(scConf, { batt: "", battD: 0.13, battG: 0.05 }).ok, false);
ok("battement non relevé -> non mesurable (null), jamais false",
   N.conforme(scConf, { batt: "", battD: "", battG: "" }).ok, null);
ok("critère désactivé -> conforme par ce critère",
   N.conforme(scn("s12", "Sans batt", false, [outil("t1", "T1", [])], { battActif: false }), { batt: 9.9 }).ok, true);
ok("limite du scénario (limitOverride) gagne sur le défaut",
   N.conforme(scn("s13", "Perso", false, [outil("t1", "T1", [])], { limitOverride: true, limitValue: 0.05 }), { batt: 0.06 }).ok, false);
ok("Ra dépassé -> non conforme",
   N.conforme(scn("s14", "Ra", false, [outil("t1", "T1", [])], { critere2Actif: true, limitValue2: 0.8 }), { batt: 0.10, valeur2: 0.9 }).ok, false);
ok("critère supplémentaire mini/maxi",
   N.conforme(scn("s15", "Sup", false, [outil("t1", "T1", [])],
     { criteresSup: [{ id: "cs1", label: "Fuite", maxi: 5, miniActif: true, mini: 1, actif: true }] }),
     { batt: 0.10, valeurs: { cs1: { v: 0.5 } } }).ok, false);

/* ============================================================================
   7. LES STATUTS D'ESSAI ET DE SCÉNARIO
   ============================================================================ */

console.log("\n── LES STATUTS (l'ordre est délibéré) ───────────────────────");

ok("un essai arrêté est une décision, pas un échec",
   N.statutEssai(scConf, essaiEx("e1", { cloture: { motif: "brut cassé" } })).code, "arrete");
ok("un essai sans prélèvement attend", N.statutEssai(scConf, essaiEx("e2", {})).code, "attente");
ok("la première pièce hors tolérance nomme la raison et la pièce",
   N.statutEssai(scConf, essaiEx("e3", {
     prelevements: [{ id: "p1", piece: 12, batt: 0.05 }, { id: "p2", piece: 13, batt: 0.20 }]
   })).texte.indexOf("hors tolérance") >= 0, true);
ok("la charnière non atteinte = essai en cours (D1 60/100 p)",
   N.statutEssai(scConf, essaiEx("e4", {
     params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 100 }] },
     prelevements: [{ id: "p1", piece: 60, batt: 0.05 }]
   })).texte, "D1 60/100 p");
ok("charnière atteinte et tout conforme = conforme",
   N.statutEssai(scConf, essaiEx("e5", {
     params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 100 }] },
     prelevements: [{ id: "p1", piece: 100, batt: 0.05 }]
   })).code, "conforme");
ok("des mesures incomplètes après charnière atteinte restent à saisir",
   N.statutEssai(scConf, essaiEx("e6", {
     params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 100 }] },
     prelevements: [{ id: "p1", piece: 100, batt: 0.05 }, { id: "p2", piece: 101, batt: "" }]
   })).code, "attente");

/* Le protocole 5× : conformes consignées. */
function scnAvecEssais(nbConformes, nbAttente) {
  const s = scn("sX", "Optim", false, [outil("t1", "T1", [log("g1", "D1", 38, 8, 800)])]);
  for (let i = 0; i < nbConformes; i++) {
    s.essais.push(essaiEx("ec" + i, {
      params: { logements: [{ logementId: "g1", logementNom: "D1", charniere: 100 }] },
      prelevements: [{ id: "p" + i, piece: 100, batt: 0.05 }]
    }));
  }
  for (let i = 0; i < (nbAttente || 0); i++) s.essais.push(essaiEx("ea" + i, {}));
  return s;
}
ok("5 essais conformes = validé, à passer en série",
   N.statutScenario(scnAvecEssais(5, 0)).code, "valide");
ok("4 essais conformes = encore en cours",
   N.statutScenario(scnAvecEssais(4, 0)).code, "encours");
ok("le scénario de prod est en série par définition",
   N.statutScenario(scn("sS", "Prod", true, [outil("t1", "T1", [])])).code, "serie");
ok("un scénario sans essai est une opportunité",
   N.statutScenario(scn("sO", "Vierge", false, [outil("t1", "T1", [])])).code, "opportunite");

/* ============================================================================
   8. LE SCÉNARIO DE PROD — jamais « le premier de la liste »
   ============================================================================ */

console.log("\n── LE SCÉNARIO DE PRODUCTION (baseline > série > base excel) ─");

const a = scn("a", "A", false, []), b = scn("b", "B", false, []), c = scn("c", "C", false, []);
b.statut = "serie"; c.name = "Base excel du site";
ok("baseline gagne", N.scenarioDeProd([a, c, scn("d", "Prod", true, [])]).id, "d");
ok("à défaut, le scénario en série", N.scenarioDeProd([a, c, b]).id, "b");
ok("à défaut, le nom « base excel »", N.scenarioDeProd([a, c]).id, "c");
ok("rien ne ressemble à une prod -> null", N.scenarioDeProd([a]), null);
ok("liste vide -> null", N.scenarioDeProd([]), null);

/* ============================================================================
   9. LE VERDICT DE POSTE — deux gains, jamais sommés
   ============================================================================ */

console.log("\n── LE VERDICT DE POSTE (prévu, obtenu, acté, projeté) ───────");

const REF = refEx("r1", "304x28 RPE", 0.12, 50000);
const PROD = scn("sp", "Prod actuelle", true, [outil("t1", "T511", [log("g1", "D1", 38, 8, 800)])]);
const BON = scn("sb", "SL500", false, [outil("t2", "T513", [log("g2", "D1", 19, 8, 800)])]);

const vEssai = N.verdictPoste(REF, opEx("o1", "OP10", [PROD, BON]));
ok("CPP prod = 38/6400", vEssai.cppProd, 38 / 6400, 1e-9);
ok("le meilleur scénario est celui qui coûte moins", vEssai.meilleur.sc.id, "sb");
ok("gain projeté = prod − meilleur", vEssai.gainProjete, 38 / 6400 - 19 / 6400, 1e-9);
ok("le gain projeté reste projeté (pas de gain acté ici)", vEssai.gainActe, null);
ok("le gain annuel porte le volume (50000 pièces)", vEssai.gainAnnuelProjete,
   (38 / 6400 - 19 / 6400) * 50000, 1e-6);
ok("verdict « essai » tant que rien n'est validé 5×", vEssai.verdict.code, "essai");

/* Un scénario déjà en série, différent de la prod : gain ACTÉ. */
const SERIE = scn("ss", "Passé en série", false, [outil("t3", "T514", [log("g3", "D1", 10, 8, 800)])]);
SERIE.statut = "serie"; SERIE.baseline = false;
const vActe = N.verdictPoste(REF, opEx("o2", "OP20", [PROD, SERIE]));
ok("le gain acté vient d'un scénario en série meilleur que la prod",
   vActe.gainActe, 38 / 6400 - 10 / 6400, 1e-9);
ok("acté et projeté ne se mélangent jamais", vActe.gainProjete, null);
ok("verdict gagné", vActe.verdict.code, "gagne");

/* Un poste validé 5× : la décision reste à prendre. */
const vPret = N.verdictPoste(REF, opEx("o3", "OP30", [PROD, scnAvecEssais(5, 0)]));
ok("validé 5× = prêt à décider", vPret.verdict.code, "pret");

/* Un poste sans AUCUN scénario : « vide » (jamais travaillé) — visible et
   nommé, distinct de « à chiffrer » qui suppose un scénario existant. */
const vVide = N.verdictPoste(refEx("r2", "Nue", 0.12, ""), opEx("o4", "OP40", []));
ok("sans aucun scénario : le poste est « vide », visible et nommé", vVide.verdict.code, "vide");
ok("la décision appelle POSER", N.decisionPoste(vVide).mot, "POSER");

/* Un poste AVEC un scénario non chiffrable : à chiffrer, la cible connue
   se dit dans la raison. */
const scNonChiffrable = scn("sn", "Brouillon", false, [outil("t9", "T9", [log("g9", "D1", "", "", "")])]);
const vChiffrer = N.verdictPoste(refEx("r2b", "Nue avec scénario", 0.12, ""), opEx("o4b", "OP40", [scNonChiffrable]));
ok("un scénario non chiffrable avec cible : à chiffrer", vChiffrer.verdict.code, "achiffrer");
ok("…avec la cible connue dans le texte", vChiffrer.verdict.texte, "cible connue, à chiffrer");
ok("sans volume annuel, pas de gain annuel (null, jamais estimé)",
   N.verdictPoste(refEx("r3", "Sans volume", 0.12, ""), opEx("o5", "OP10", [PROD, BON])).gainAnnuelProjete, null);

/* Le CPP obtenu par essai remonte dans le verdict — la preuve du terrain. */
const scObtenu = scn("so", "Essai obtenu", false, [outil("t4", "T515", [log("g4", "D1", 38, 8, 800)])]);
scObtenu.essais.push(essaiEx("eo", {
  params: { logements: [{ logementId: "g4", logementNom: "D1", charniere: 2400 }] },
  prelevements: [{ id: "p1", piece: 1, batt: 0.08 }]
}));
const vObtenu = N.verdictPoste(REF, opEx("o6", "OP50", [PROD, scObtenu]));
ok("le meilleur CPP OBTENU se distingue du prévu",
   vObtenu.meilleurObtenu.cpp, 38 / 19200, 1e-9);
ok("le prévu reste le prévu", vObtenu.meilleur.cpp, 38 / 6400, 1e-9);

ok("la décision « ESSAYER » dit le gain en toutes lettres",
   N.decisionPoste(vEssai).pourquoi.indexOf(N.fmt(vEssai.gainProjete, 4)) >= 0, true);
ok("un poste à chiffrer appelle CHIFFRER", N.decisionPoste(vChiffrer).mot, "CHIFFRER");
ok("un poste gagné appelle SÉRIE", N.decisionPoste(vActe).mot, "SÉRIE");

/* Un poste au meilleur connu : GARDER, avec sa raison. */
const vRien = N.verdictPoste(REF, opEx("o7", "OP60", [PROD, scn("sru", "Essai plus cher", false, [outil("t7", "T7", [log("g7", "D1", 99, 8, 800)])])]));
ok("aucun essai meilleur que la prod : verdict « rien » (au meilleur connu)", vRien.verdict.code, "rien");
ok("la décision appelle GARDER avec sa raison",
   N.decisionPoste(vRien).mot === "GARDER" && N.decisionPoste(vRien).pourquoi.indexOf("aucun essai ne fait mieux") >= 0, true);

/* ============================================================================
   10. LES POSTES, LES RÉFÉRENCES, LES TUILES
   ============================================================================ */

console.log("\n── LES POSTES ET LES TUILES (l'accueil) ─────────────────────");

ok("opCode dérivé du nom", N.opCodeDe(opEx("o1", "OP 040 Ébauche", [])), "OP40");
ok("opCode dérivé de l'ordre", N.opCodeDe({ id: "o2", nom: "Finition", ordre: 30, scenarios: [] }), "OP30");
ok("opCode inconnu dit inconnu", N.opCodeDe({ id: "o3", nom: "Contrôle", scenarios: [] }), "OP?");

const LIGNE = ligneEx("l1", "EMAG 1", [
  Object.assign({}, REF, {
    ops: [opEx("o1", "OP10", [PROD, BON]), opEx("o2", "OP20", [PROD, SERIE])]
  })
]);
const postes = N.verdictsDeLigne(LIGNE);
ok("deux postes sur la ligne", postes.length, 2);
ok("le verdict est posé UNE fois par poste (source unique)", postes[0].verdict.cppProd, 38 / 6400, 1e-9);

const refSum = N.cppReference(postes, LIGNE.references[0]);
ok("CPP référence = somme des postes chiffrables", refSum.cpp, 38 / 6400 * 2, 1e-9);
ok("distance à la cible", refSum.distanceCible, 38 / 6400 * 2 - 0.12, 1e-9);

const refIncomplète = refEx("r9", "Sans prod", 0.12, "");
const LIGNE2 = ligneEx("l9", "EMAG 2", [
  Object.assign({}, refIncomplète, { ops: [opEx("o9", "OP10", [scn("sx", "Vierge", false, [outil("t1", "T1", [log("g1", "D1", "", "", "")])])])] })
]);
const refSum2 = N.cppReference(N.verdictsDeLigne(LIGNE2), LIGNE2.references[0]);
ok("un poste non chiffrable est compté, pas dilué", refSum2.nonChiffrables, 1);
ok("…et la référence reste sans CPP", refSum2.cpp, null);

const tuile = N.tuileDeLigne(LIGNE);
ok("la tuile porte le CPP de la ligne", tuile.cpp, 38 / 6400 * 2, 1e-9);
ok("la tuile connaît sa famille (EMAG gris)", tuile.famille, "emag");
ok("la tuile connaît son code (E1)", tuile.code, "E1");
ok("la référence dominante est celle qui a le plus de postes chiffrés",
   tuile.dominante.ref.id, "r1");
ok("les décisions en attente sont comptées", tuile.decisions, 1);
ok("la ligne inconnue se range après le référentiel",
   N.rangLigne("Mystère 9") > N.rangLigne("PCI 4"), true);
ok("famille reconnue pour Weisser", N.familleDeLigne("Weisser 2"), "weisser");
ok("code ligne Hessapp", N.codeLigneDe("HESSAPP"), "HESSAPP");
ok("code ligne PCI", N.codeLigneDe("PCI 2"), "P2");

const tuiles = N.tuilesDeLignes([ligneEx("lx", "PCI 1", []), LIGNE, ligneEx("lw", "Weisser 1", [])]);
ok("l'ordre physique de l'atelier (Weisser devant EMAG, PCI après)",
   tuiles.map(t => t.nom).join("|"), "Weisser 1|EMAG 1|PCI 1");
ok("une tuile vide reste visible", tuiles[2].vide, true);

const det = N.detailLigne(LIGNE2);
ok("une OP sans production reste visible dans le détail", det.nbPostesSansProd, 1);

/* ============================================================================
   11. LES GAINS — acté et projeté dans des blocs distincts
   ============================================================================ */

console.log("\n── LES GAINS (acté ≠ projeté, jamais sommés) ────────────────");

const gl = N.gainLigne(LIGNE);
ok("le gain acté est le sien", gl.gainActe, 38 / 6400 - 10 / 6400, 1e-9);
ok("le gain projeté est le sien (poste 1)", gl.gainProjete, 38 / 6400 - 19 / 6400, 1e-9);
ok("acté + projeté ne se fusionnent jamais : ils restent deux champs distincts",
   (gl.gainActe + gl.gainProjete) !== gl.gainActe || gl.gainProjete === 0, true);
ok("le gain annuel acté porte le volume", gl.gainAnnuelActe, (38 / 6400 - 10 / 6400) * 50000, 1e-6);

const rec = N.recapAtelier([LIGNE, LIGNE2]);
ok("le récap compte les décisions", rec.decisions, 1);
ok("le récap compte les postes à chiffrer", rec.aChiffrer, 1);
ok("le récap compte les lignes engagées", rec.lignesEngagees, 1);
ok("le récap compte les lignes", rec.nbLignes, 2);

/* ============================================================================
   12. LES PROJETS — étiquettes, couleurs stables, responsables
   ============================================================================ */

console.log("\n── LES PROJETS (étiquettes, jamais propriétaires) ───────────");

const etatVide = { projets: [], responsables: [] };
ok("la première couleur libre est la première de la palette",
   N.couleurProjetLibre(etatVide), N.PALETTE_PROJETS[0]);
const etat1 = { projets: [{ id: "p1", couleur: N.PALETTE_PROJETS[0] }], responsables: [] };
ok("la couleur prise est évitée", N.couleurProjetLibre(etat1), N.PALETTE_PROJETS[1]);
const etatToutes = { projets: N.PALETTE_PROJETS.map(c => ({ couleur: c })), responsables: [] };
ok("palette épuisée -> cycle modulo", N.couleurProjetLibre(etatToutes), N.PALETTE_PROJETS[8 % 8]);

const ETAT = {
  lignes: [LIGNE],
  projets: [{
    id: "p1", nom: "Économie OP10", statut: "encours", responsableId: "u1",
    couleur: "#3b82f6",
    tags: [{ ligneId: "l1", referenceId: "r1", opId: "o1", scenarioId: "sb" }]
  }, {
    id: "p2", nom: "Projet fantôme", statut: "pause", responsableId: "",
    couleur: "#14b8a6",
    tags: [{ ligneId: "l1", referenceId: "r1", opId: "o1", scenarioId: "disparu" }]
  }],
  responsables: [{ id: "u1", nom: "Matis", couleur: "#e2001a" }]
};
const lies = N.scenariosDeProjet(ETAT, ETAT.projets[0]);
ok("l'étiquette résout vers le scénario", lies.lies.length, 1);
ok("…et porte la ligne, la référence et l'OP", lies.lies[0].op.id, "o1");
const fantome = N.scenariosDeProjet(ETAT, ETAT.projets[1]);
ok("une étiquette orpheline est signalée, pas oubliée", fantome.orphelins.length, 1);
ok("les projets d'un scénario se retrouvent par les étiquettes",
   N.projetsDeScenario(ETAT, "l1", "r1", "o1", "sb").map(p => p.id).join(","), "p1");
ok("le résumé « projets sur cet OP » compte sans scénario précis",
   N.projetsDeOP(ETAT, "l1", "r1", "o1").length, 2);
ok("le responsable se résout contre la liste gérée",
   N.responsableDe(ETAT, ETAT.projets[0]).nom, "Matis");
ok("un responsable supprimé renvoie le projet à aucun responsable",
   N.responsableDe(ETAT, { responsableId: "u-disparu" }), null);
ok("les statuts de projet sont les statuts de l'app",
   N.PROJET_STATUTS.encours, "En cours");

/* ============================================================================
   13. LES LIVRAISONS — l'instantané figé
   ============================================================================ */

console.log("\n── LES LIVRAISONS (le document qui ne bouge plus) ───────────");

const liv = N.capturerLivraison({ lignes: [LIGNE] }, "Fin de semaine", "Benjamin");
ok("la livraison fige le gain acté", liv.gainsActes, 38 / 6400 - 10 / 6400, 1e-9);
ok("la livraison fige le gain en cours séparément", liv.gainsEnCours, 38 / 6400 - 19 / 6400, 1e-9);
ok("le plan porte les lignes", liv.plan.length, 1);
ok("le plan porte la dominante", liv.plan[0].dominante, "304x28 RPE");
ok("la livraison porte l'auteur et la date", liv.creePar, "Benjamin");

/* ============================================================================
   14. LES OUTILS DIVERS
   ============================================================================ */

console.log("\n── LES OUTILS DIVERS ────────────────────────────────────────");

ok("la clé de porte-outil ignore espaces et tirets",
   N.clePorteOutil("T 513 D1"), N.clePorteOutil("T513 D1"));
ok("la clé ignore aussi les points", N.clePorteOutil("T.513"), "T513");
ok("uid préfixé", N.uid("sc").slice(0, 2), "sc");
ok("date courte au format FR", /^\d{2}\/\d{2}\/\d{4}$/.test(N.dateCourte("2026-10-02T10:00:00")), true);
ok("date heure lisible", N.dateHeure("2026-10-02T18:30:00").indexOf("02/10/2026") >= 0, true);
ok("uid de deux appels sont différents", N.uid("a") !== N.uid("a"), true);

/* ============================================================================
   FINALISATION — comptés, pas seulement échoués (constitution §6.10)
   ============================================================================ */

process.exit(j.finaliser() ? 0 : 1);
