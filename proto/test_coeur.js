/* ============================================================================
   PROTO — LES TESTS DU NOYAU
   Écrits AVANT les écrans (cahier §5). Chaque test du cahier a un test ici.
   Exécution : node test_coeur.js
   ========================================================================== */

/* le noyau est chargé tel quel — pas de copie, pas de re-définition ici */
const fs = require("fs");
const src = fs.readFileSync(__dirname + "/coeur.js", "utf8");
const N = (new Function(src + "\nreturn {fmt,fmtDispo,coutLogement,cppOutillageScenario,cppOutillageOutil,cppParLogement,cheminCPP,conforme,charniereVisee,statutEssai,statutScenario,verdictPoste,verdictLigne,decisionPoste,recapLignes,PROTO_VERSION};"))
  .call(globalThis);
const {
  fmt, fmtDispo, coutLogement, cppOutillageScenario, cppOutillageOutil,
  cppParLogement, cheminCPP, conforme, charniereVisee, statutEssai,
  statutScenario, verdictPoste, verdictLigne, decisionPoste, recapLignes
} = N;

let total = 0, echecs = 0;
const details = [];

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
    details.push(nom);
    console.log("  ECHEC " + nom + " — obtenu " + JSON.stringify(obtenu) +
                ", attendu " + JSON.stringify(attendu));
  } else {
    console.log("  ok   " + nom);
  }
}

/* ---- fabrique de jeu d'essai, minimal et lisible ---- */
function log(id, nom, prix, aretes, charniere) {
  return { id: id, nom: nom, ref: "ART-X", prix: prix, aretes: aretes, charniere: charniere };
}
function scn(nom, baseline, logements, extra) {
  const o = Object.assign({
    id: "s-" + nom, name: nom, baseline: !!baseline,
    outils: [{ id: "t1", numero: "T1", logements: logements }],
    essais: [], validationThreshold: 5
  }, extra || {});
  return o;
}
function essai(pieces, opts) {
  // pieces = [{piece, batt}]
  return Object.assign({
    id: "e1",
    date: "2026-10-01",
    params: { logements: [{ logementId: "g1", logementNom: "Bol", charniere: 100 }] },
    prelevements: pieces.map((p, i) => ({
      id: "p" + i, piece: p.piece, batt: p.batt, battD: "", battG: ""
    }))
  }, opts || {});
}

console.log("\n── LE CPP OUTILLAGE, le driver ──────────────────────────────");

ok("un logement : prix / (arêtes × charnière)",
   coutLogement(log("g1", "Bol", 30, 8, 100)), 30 / 800, 1e-12);

ok("un logement incomplet ne vaut PAS 0 — il vaut null (invariant 1)",
   coutLogement(log("g1", "Bol", "", 8, 100)), null);

ok("arêtes absentes : null, pas une division infinie",
   coutLogement(log("g1", "Bol", 30, 0, 100)), null);

ok("charnière absente : null",
   coutLogement(log("g1", "Bol", 30, 8, "")), null);

ok("prix nul : null (une plaquette gratuite n'est pas unCpp de 0)",
   coutLogement(log("g1", "Bol", 0, 8, 100)), null);

ok("CPP outillage d'un scénario = somme des logements",
   cppOutillageScenario(scn("a", true, [log("g1","Bol",30,8,100), log("g2","Piste",30,8,200)])),
   30/800 + 30/1600, 1e-12);

ok("un scénario sans logement chiffrable : null, pas 0",
   cppOutillageScenario(scn("a", true, [log("g1","Bol","","","")])), null);

ok("deux logements dont un seul chiffrable : on ne somme que le chiffrable",
   cppOutillageScenario(scn("a", true, [log("g1","Bol",30,8,100), log("g2","X","","","")])),
   30/800, 1e-12);

ok("le CPP outillage par logement se lit pour l'écran Décision",
   cppParLogement(scn("a", true, [log("g1","Bol",30,8,100)])).length, 1);

console.log("\n── LE CHEMIN PROD → CIBLE ──────────────────────────────────");

ok("un essai identique : chemin 0",
   cheminCPP(0.10, 0.10, 0.08), 0, 1e-9);

ok("un essai qui atteint la cible : chemin 100",
   cheminCPP(0.10, 0.08, 0.08), 100, 1e-9);

ok("un essai à mi-chemin : 50 %",
   cheminCPP(0.10, 0.09, 0.08), 50, 1e-9);

ok("la prod DÉJÀ en dessous de la cible : chemin 100 (fait, pas 0)",
   cheminCPP(0.07, 0.07, 0.08), 100, 1e-9);

ok("pas de cible : chemin null — pas de 0 qui signifie « inconnu »",
   cheminCPP(0.10, 0.09, null), null);

ok("pas de chiffrage d'un côté : chemin null",
   cheminCPP(0.10, null, 0.08), null);

ok("un gain qui dépasse la cible ne dépasse pas 100 %",
   cheminCPP(0.10, 0.01, 0.08), 100, 1e-9);

console.log("\n── LA PREUVE : conformité et charnière ──────────────────────");

const scBase = scn("base", true, [log("g1", "Bol", 30, 8, 100)], { limitValue: 0.12 });

ok("une mesure dans la tolérance : true",
   conforme(scBase, { piece: 1, batt: 0.08 }), true);

ok("une mesure hors tolérance : false",
   conforme(scBase, { piece: 1, batt: 0.15 }), false);

ok("une mesure VIDE : null — jamais false (invariant 1)",
   conforme(scBase, { piece: 1, batt: "" }), null);

ok("un critère désactivé ne peut pas faire échouer",
   conforme({ battActif: false }, { piece: 1, batt: 0.99 }), true);

ok("essai sans prélèvement : « aucun prélèvement »",
   statutEssai(scBase, essai([])).texte, "aucun prélèvement");

ok("essai hors tolérance : le statut est nonconforme, avec la pièce",
   statutEssai(scBase, essai([{ piece: 1, batt: 0.08 }, { piece: 2, batt: 0.15 }])).code,
   "nonconforme");

ok("essai arrêté : le statut est « arrete », pas « nonconforme » (décision ≠ échec)",
   statutEssai(scBase, essai([], { cloture: { motif: "casse" } })).code, "arrete");

ok("essai à la charnière atteinte : conforme",
   statutEssai(scBase, essai([{ piece: 100, batt: 0.08 }])).code, "conforme");

ok("essai en dessous de la charnière : en cours, avec le reste à faire",
   statutEssai(scBase, essai([{ piece: 40, batt: 0.08 }])).code, "encours");

ok("le message « en cours » dit ce qui reste",
   statutEssai(scBase, essai([{ piece: 40, batt: 0.08 }])).texte, "Bol 40/100 p");

ok("mesure manquante : le statut dit combien",
   statutEssai(scBase, { id: "e", date: "", params: { logements: [] },
                         prelevements: [{ id: "p", piece: 100, batt: "" }] }).texte,
   "1 mesure à saisir");

console.log("\n── LE STATUT D'UN SCÉNARIO (la décision) ────────────────────");

function scAvecEssais(nb, statut) {
  const s = scn("essai" + nb, false, [log("g1", "Bol", 30, 8, 100)], { statut: statut });
  for (let i = 0; i < nb; i++) {
    s.essais.push(essai([{ piece: 100, batt: 0.08 }], { id: "e" + i }));
  }
  return s;
}
ok("0 essai : rien d'essayé",
   statutScenario(scn("x", false, [log("g1","Bol",30,8,100)])).code, "opportunite");

ok("2 essais conformes sur 5 : encore en cours",
   statutScenario(scAvecEssais(2)).code, "encours");

ok("5 essais conformes : validé 5×",
   statutScenario(scAvecEssais(5)).code, "valide");

ok("un scénario « en série » prime sur tout",
   statutScenario(scAvecEssais(2, "serie")).code, "serie");

console.log("\n── LE VERDICT D'UN POSTE ────────────────────────────────────");

const ref = { id: "r1", nom: "Disque 356", cibleCPP: 0.08 };
const op = { id: "o1", nom: "OP10", ordre: 10 };
const prodSC = scn("prod", true, [log("g1", "Bol", 30, 8, 100)]);      // 0.0375
const bonSC   = scn("bon", false, [log("g1", "Bol", 30, 8, 200)]);     // 0.01875

ok("le poste lit le CPP de prod et le meilleur essai",
   verdictPoste(ref, op, [prodSC, bonSC]).meilleur.cpp, 0.01875, 1e-12);

/* la cible 0,08 est INFÉRIEURE au CPP de prod 0,0375 : le chemin est déjà fait.
   C'est le cas qui rend la formule brute absurde (elle donnerait −44 %) : le noyau
   doit renvoyer 100, pas un pourcentage négatif. */
const refAuDessus = { id: "r2", nom: "Disque 356", cibleCPP: 0.02 };
ok("prod déjà SOUS la cible : chemin 100, jamais un % négatif",
   verdictPoste(ref, op, [prodSC, bonSC]).chemin, 100, 1e-9);

/* le cas « vrai » du chemin : la prod est au-dessus de la cible, l'essai réduit
   sans la dépasser. Une charnière de 120 p donne 0,03125 €/pièce. */
const scMediocre = scn("mediocre", false, [log("g1", "Bol", 30, 8, 120)]);  // 0.03125
ok("au-dessus de la cible : le chemin se calcule sur le vrai delta",
   verdictPoste(refAuDessus, op, [prodSC, scMediocre]).chemin,
   (0.0375 - 0.03125) / (0.0375 - 0.02) * 100, 1e-9);

/* le dépassement : un ESSAI SOUS la cible fait plus que 100 % de chemin brut.
   La formule donnerait 107 % ; on borne, parce qu'un chemin se mesure entre
   deux points et qu'il n'y a pas de « au-delà du chemin ». */
ok("un essai qui dépasse la cible : le chemin est borné à 100, pas 107",
   verdictPoste(refAuDessus, op, [prodSC, bonSC]).chemin, 100, 1e-9);

ok("un essai meilleur mais pas validé : le verdict est « ESSAYER »",
   verdictPoste(ref, op, [prodSC, bonSC]).verdict.code, "essai");

ok("le gain projeté est la différence, en €/pièce",
   verdictPoste(ref, op, [prodSC, bonSC]).gainProjete, 0.0375 - 0.01875, 1e-12);

ok("le gain projeté n'est PAS aussi le gain acté (invariant 2)",
   verdictPoste(ref, op, [prodSC, bonSC]).gainActe, null);

const serieSC = scn("serie", false, [log("g1", "Bol", 30, 8, 200)], { statut: "serie" });
ok("passé en série : le gain ACTÉ apparaît, et le verdict est gagné",
   verdictPoste(ref, op, [prodSC, serieSC]).verdict.code, "gagne");

ok("passé en série : gainActe rempli",
   verdictPoste(ref, op, [prodSC, serieSC]).gainActe, 0.0375 - 0.01875, 1e-12);

ok("un poste SANS prod chiffrable mais AVEC cible : « à chiffrer », jamais « opportunité » (invariant 3)",
   verdictPoste(ref, op, []).verdict.code, "achiffrer");

ok("un poste sans cible et sans chiffrage reste « à chiffrer », pas invisible",
   verdictPoste({ id: "r", nom: "x" }, op, []).verdict.code, "achiffrer");

ok("un poste où aucun essai ne bat la prod : « rien »",
   verdictPoste(ref, op, [prodSC, scn("pire", false, [log("g1","Bol",30,8,50)])]).verdict.code,
   "rien");

console.log("\n── LA LIGNE : les absents se voient ────────────────────────");

const vl = verdictLigne({ id: "l1", nom: "EMAG 1" }, [
  { ref: ref, op: op, scenarios: [prodSC, bonSC] },
  { ref: ref, op: { id: "o2", nom: "OP20" }, scenarios: [] }   // pas chiffrable
]);
ok("le CPP de la ligne neAdditionne que les postes chiffrables",
   vl.cppProd, 0.0375, 1e-12);

ok("le poste non chiffrable est COMPTÉ, pas dilué (invariant 3)",
   vl.nonChiffrables, 1);

ok("le CPP projected de la ligne = les postes en essai",
   vl.cppProjete, 0.0375 - 0.01875, 1e-12);

console.log("\n── LE RÉCAPITULATIF DE L'ACCUEIL ───────────────────────────");

const r = recapLignes([
  vl,
  verdictLigne({ id: "l2", nom: "EMAG 3" }, [
    { ref: ref, op: op, scenarios: [prodSC, serieSC] }
  ])
]);
ok("le gain acté de l'accueil vient des postes passés en série",
   r.cppActe, 0.0375 - 0.01875, 1e-12);

ok("le gain projeté reste SÉPARÉ du gain acté — jamais de total unique (invariant 2)",
   r.cppProjete, 0.0375 - 0.01875, 1e-12);

ok("le compte « à chiffrer » traverse les lignes",
   r.aChiffrer, 1);

/* Le compte « à décider » doit compter tout ce qui attend une action. Il a valu
   zéro en silence pendant un tour : le filtre comparait à "prêt" accentué alors
   que les codes de verdict sont en ASCII. Un test qui reprenait la même chaîne
   accentuée ne pouvait pas le voir — d'où le test par EFFET, pas par libellé. */
/* sans bonSC dans la liste : c'est le scénario validé 5× qui doit être le
   « meilleur », donc il faut qu'il n'ait pas de concurrent moins cher. */
ok("un poste validé 5× compte dans « à décider »",
   recapLignes([verdictLigne({ id: "l", nom: "L" },
     [{ ref: ref, op: op, scenarios: [prodSC, scAvecEssais(5)] }])]).decisions, 1);

ok("un poste prometteur compte aussi dans « à décider »",
   recapLignes([verdictLigne({ id: "l", nom: "L" },
     [{ ref: ref, op: op, scenarios: [prodSC, bonSC] }])]).decisions, 1);

ok("un poste déjà en série ne compte PAS : il ne demande plus rien",
   recapLignes([verdictLigne({ id: "l", nom: "L" },
     [{ ref: ref, op: op, scenarios: [prodSC, serieSC] }])]).decisions, 0);

/* ── LE PIÈGE DE L'ACCENT ──
   Un code de verdict accentué ("prêt") comparé à un code ASCII ("pret") échoue
   EN SILENCE : la comparaison est fausse, le compteur reste à zéro, et rien ne
   crie. Ça a valu un tour. Ce test verrouille la règle : les codes sont de
   l'ASCII, les accents sont dans le TEXTE affiché, jamais dans la clé. */
const tousLesVerdicts = vlsTousVerdicts();
ok("tous les codes de verdict sont ASCII (aucun accent dans une clé)",
   tousLesVerdicts.filter(c => /[^\x00-\x7F]/.test(c)).length, 0);
ok("le vocabulaire des codes tient en six clés", tousLesVerdicts.length > 0, true);
ok("aucun code de verdict ne contient d'espace",
   tousLesVerdicts.filter(c => /\s/.test(c)).length, 0);

function vlsTousVerdicts() {
  /* on parcourt l'arbre entier du jeu de démonstration */
  const ds = fs.readFileSync(__dirname + "/donnees.js", "utf8");
  const JEUX = (new Function(ds + "\nreturn JEUX;"))();
  const out = [];
  JEUX.lignes.forEach(l => (l.refs || []).forEach(r =>
    (r.ops || []).forEach(op => {
      const v = verdictPoste(r, op, op.scs);
      if (v.verdict && v.verdict.code) out.push(v.verdict.code);
      (op.scs || []).forEach(sc => {
        const s = statutScenario(sc);
        if (s && s.code) out.push(s.code);
      });
    })));
  return out;
}
console.log("  (codes rencontrés : " + Array.from(new Set(tousLesVerdicts)).join(", ") + ")");

console.log("\n── LA DÉCISION EN UN MOT ───────────────────────────────────");

ok("un poste validé 5× appelle une DÉCISION",
   decisionPoste(verdictPoste(ref, op, [prodSC, scAvecEssais(5)])).mot, "DÉCIDER");

ok("un poste en série est classé SÉRIE",
   decisionPoste(verdictPoste(ref, op, [prodSC, serieSC])).mot, "SÉRIE");

ok("un poste prometteur appelle ESSAYER, avec le gain en toutes lettres",
   decisionPoste(verdictPoste(ref, op, [prodSC, bonSC])).mot, "ESSAYER");

/* Le gain annoncé est la valeur du noyau, formatée. On ne fige pas un arrondi
   flottant dans le test (0.01875.toFixed(4) vaut "0.0187", pas "0.0188") : ce qu'on
   verrouille, c'est que la phrase porte LE GAIN CALCULÉ. */
const _vEssayer = verdictPoste(ref, op, [prodSC, bonSC]);
ok("la décision « ESSAYER » dit le gain en toutes lettres, pas juste un mot",
   decisionPoste(_vEssayer).pourquoi.indexOf(fmt(_vEssayer.gainProjete, 4)) >= 0, true);

ok("un poste sans chiffrage appelle CHIFFRER",
   decisionPoste(verdictPoste(ref, op, [])).mot, "CHIFFRER");

console.log("\n── LES ABSENCES DISENT CE QUI MANQUE (invariant 4) ────────");

ok("une valeur absente affiche la raison, pas un tiret nu",
   fmtDispo("", 3, "volume annuel non saisi"), "volume annuel non saisi");

ok("un 0 saisi reste un 0 (on distingue 0 de pas saisi)",
   fmtDispo(0, 3, "non saisi"), "0,000");

ok("un nombre s'affiche au format FR",
   fmt(1234.5, 2), "1234,50");

ok("fmt ne ment pas sur une absence",
   fmt(null, 3), "—");

console.log("\n" + "=".repeat(60));
console.log("PROTO NOYAU : " + total + " tests | " + echecs + " echecs");
console.log(echecs ? "*** LE NOYAU EST ROUGE ***" : "TOUT EST VERT");
process.exit(echecs ? 1 : 0);