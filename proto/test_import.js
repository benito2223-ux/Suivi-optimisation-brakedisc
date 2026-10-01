/* ============================================================================
   PROTO — TEST DE LA PROJECTION
   Ce test ne tourne pas sur des données fabriquées. Il tourne sur les VRAIS
   exports du site, présents dans le dépôt : c'est la seule façon de savoir si
   l'import est « raisonnable » — un test sur un jeu synthétique ne prouve rien
   sur ce que Matis va réellement déposer.

   Il vérifie trois choses, dans cet ordre :
     1. la projection ne perd aucun chiffre de décision (prix, arêtes, charnière)
     2. elle n'en fabrique aucun (invariant 1)
     3. elle jetterait bien le poids (~98 %), et le dirait
   ========================================================================== */

const fs = require("fs");
const path = require("path");

const BASE = __dirname;
const REPO = path.join(BASE, "..");

function charger(nom) {
  const src = fs.readFileSync(path.join(BASE, nom), "utf8");
  const N = new Function(src + "\nreturn {PROTO_VERSION,fmt,fmtDispo,coutLogement,cppOutillageScenario,"
    + "cppOutillageOutil,cppParLogement,cppEssai,cheminCPP,battDe,conforme,charniereVisee,"
    + "statutEssai,statutScenario,verdictPoste,verdictLigne,decisionPoste,recapLignes};")();
  const I = new Function(fs.readFileSync(path.join(BASE, "import.js"), "utf8")
    + "\nreturn {IMPORT_VERSION,projeter,racinesLignes,codeDeOp,poids};")();
  return { N, I };
}

const { N, I } = charger("coeur.js");
const { projeter, poids } = I;

let okNb = 0, koNb = 0;
function ok(nom, obtenu, attendu) {
  const a = JSON.stringify(obtenu), b = JSON.stringify(attendu);
  if (a === b) { okNb++; console.log("  ok   " + nom); }
  else { koNb++; console.log("  KO   " + nom + "\n         obtenu  : " + a + "\n         attendu : " + b); }
}
function titre(t) { console.log("\n── " + t + " " + "─".repeat(Math.max(2, 58 - t.length))); }

function lireJson(f) {
  return JSON.parse(fs.readFileSync(path.join(REPO, f), "utf8"));
}

/* Deux parcours explicites : les données importées font cinq niveaux
   (ligne → référence → opération → scénario → essai), et une chaîne de
   forEach sur cinq niveaux devient illisible en deux tours. */
function forEachScenario(projete, fn) {
  for (const l of projete.lignes || [])
    for (const r of (l.refs || []))
      for (const op of (r.ops || []))
        for (const sc of (op.scs || [])) fn(sc);
}
function forEachEssai(projete, fn) {
  forEachScenario(projete, sc => { for (const e of (sc.essais || [])) fn(sc, e); });
}

/* ══════════════════════════════════════════════════════════════════════════
   1. LES VRAIS EXPORTS DU SITE
   ══════════════════════════════════════════════════════════════════════════ */

const EXPORTS = [
  "cloud_courant.json",
  "suivi_corrige_mabec.json",
  "base_depart_2026_2027.json",
  "IMPORT_MATIS.json"
];

const proj = {};

titre("LES EXPORTS DU SITE —ils se projettent sans erreur");
EXPORTS.forEach(f => {
  const brut = lireJson(f);
  const p = projeter(brut);
  proj[f] = { brut, p };
  ok(f + " : import accepté", p.ok, true);
});

titre("LES EXPORTS DU SITE — ce qui rentre est complet");
/* Le compte de contrôle : ce que la projection annonce doit être exactement
   ce qu'il y a dans le fichier. Un écart ici serait un mensonge de l'écran
   d'import, pas un simple détail d'affichage. */
EXPORTS.forEach(f => {
  const { brut, p } = proj[f];
  let nRef = 0, nOp = 0, nSc = 0, nEss = 0, nLog = 0;
  (brut.lignes || []).forEach(l => (l.references || []).forEach(r => {
    nRef++;
    (r.ops || []).forEach(op => {
      nOp++;
      (op.scenarios || []).forEach(sc => {
        nSc++;
        nEss += (sc.essais || []).length;
        (sc.outils || []).forEach(o => { nLog += (o.logements || []).length; });
      });
    });
  }));
  ok(f + " : " + p.rapport.lignes + " ligne(s)", p.rapport.lignes, (brut.lignes || []).length);
  ok(f + " : " + nRef + " référence(s)", p.rapport.references, nRef);
  ok(f + " : " + nOp + " opération(s)", p.rapport.ops, nOp);
  ok(f + " : " + nSc + " scénario(s)", p.rapport.scenarios, nSc);
  ok(f + " : " + nEss + " essai(s)", p.rapport.essais, nEss);
  ok(f + " : " + nLog + " logement(s)", p.rapport.logements, nLog);
});

titre("LES EXPORTS DU SITE — le poids jeté est bien jeté");
{
  const { brut, p } = proj["cloud_courant.json"];
  const w = poids(brut, p.lignes);
  console.log("         " + (w.avant / 1048576).toFixed(2) + " Mo -> "
    + (w.apres / 1024).toFixed(0) + " Ko  (ratio " + w.ratio + ")");
  ok("le fichier de 3,27 Mo devient un objet de moins de 100 Ko", w.apres < 100 * 1024, true);
  ok("plus de 95 % du poids disparaît", w.ratio < 0.05, true);
}

titre("LES EXPORTS DU SITE — AUCUN `plan` n'a survécu");
{
  let plans = 0;
  forEachScenario(proj["cloud_courant.json"].p, sc => {
    for (const o of (sc.outils || [])) {
      if ("plan" in o) plans++;
      for (const lg of (o.logements || [])) if ("plan" in lg) plans++;
    }
  });
  ok("aucun outil ne porte de plan", plans, 0);
}

/* ══════════════════════════════════════════════════════════════════════════
   2. LE CPP PLAQUETTES CALCULÉ SUR LES DONNÉES RÉELLES
   C'est LA question posée : peut-on reprendre les essais déjà faits ?
   ══════════════════════════════════════════════════════════════════════════ */

titre("LE CPP SUR LES DONNÉES RÉELLES");

/* On retrouve le premier logement chiffrable du premier scénario avec outils,
   et on vérifie que le noyau lit EXACTEMENT les mêmes chiffres que le fichier. */
function premierLogement(p) {
  for (const l of p.lignes) for (const r of (l.refs || [])) for (const op of (r.ops || []))
    for (const sc of (op.scs || [])) for (const o of (sc.outils || []))
      for (const lg of (o.logements || [])) if (N.coutLogement(lg) !== null) return lg;
  return null;
}
{
  const lg = premierLogement(proj["cloud_courant.json"].p);
  ok("un logement chiffrable est trouvé dans l'export réel", lg !== null, true);
  const attendu = parseFloat(lg.prix) / (parseFloat(lg.aretes) * parseFloat(lg.charniere));
  ok("son CPP = prix ÷ (arêtes × charnière), à la lettre", N.coutLogement(lg), attendu);
  console.log("         " + lg.nom + " · " + lg.ref + " · "
    + lg.prix + " € ÷ (" + lg.aretes + " × " + lg.charniere + ") = "
    + N.coutLogement(lg).toFixed(5) + " €/pce");
}

/* Le pont battD/battG : sans lui, les essais réimportés ne prouvent rien. */
titre("LE PONT batt / battD / battG — sans lui l'import ne prouve rien");
{
  let battSeul = 0, dgSeul = 0;
  forEachEssai(proj["cloud_courant.json"].p, (sc, e) => {
    for (const pr of (e.prelevements || [])) {
      if (!isNaN(parseFloat(pr.batt))) battSeul++;
      else if (!isNaN(parseFloat(pr.battD)) || !isNaN(parseFloat(pr.battG))) dgSeul++;
    }
  });
  console.log("         sur l'export réel : " + battSeul + " prélèvement(s) avec batt, "
    + dgSeul + " avec seulement D/G");
  ok("l'export réel contient des prélèvements que seul D/G renseigne", dgSeul > 0, true);

  ok("batt seul : la valeur est reprise telle quelle", N.battDe({ batt: 0.09, battD: 0.5 }), 0.09);
  ok("batt vide : D seul est pris", N.battDe({ batt: "", battD: 0.11, battG: "" }), 0.11);
  ok("batt vide : G seul est pris", N.battDe({ batt: "", battD: "", battG: 0.13 }), 0.13);
  ok("D et G : LE PIRE des deux, jamais la moyenne", N.battDe({ batt: "", battD: 0.08, battG: 0.14 }), 0.14);
  ok("aucun des trois : NaN, donc non mesurable", N.battDe({ batt: "", battD: "", battG: "" }), NaN);
  ok("pas de prélèvement : NaN", N.battDe(null), NaN);

  /* la conséquence sur la conformité */
  const sc = { limitOverride: false };
  ok("D dans la tolérance, G hors : NON conforme (le pire gagne)",
     N.conforme(sc, { batt: "", battD: 0.05, battG: 0.20 }), false);
  ok("D et G dans la tolérance : conforme",
     N.conforme(sc, { batt: "", battD: 0.05, battG: 0.11 }), true);
}

/* Le CPP RÉELLEMENT OBTENU : le prix vient du scénario, la charnière de l'essai. */
titre("LE CPP RÉELLEMENT OBTENU PAR ESSAI (le gain du réimport)");
{
  /* On fabrique un essai minimal où la charnière obtenue vaut le double de
     celle du scénario : le CPP doit être divisé par deux. C'est la preuve que
     la charnière de l'essai prime sur celle du scénario. */
  const sc = {
    outils: [{ numero: "T1", logements: [
      { id: "g1", nom: "Bol",  prix: 40, aretes: 2, charniere: 100 },
      { id: "g2", nom: "Piste", prix: 40, aretes: 2, charniere: 100 }
    ] }]
  };
  const prevu = N.cppOutillageScenario(sc);
  ok("le CPP prévu du scénario", prevu, 40 / 200 + 40 / 200);

  const essai = { params: { logements: [
    { logementId: "g1", logementNom: "Bol", charniere: 200 },
    { logementId: "g2", logementNom: "Piste", charniere: 200 }
  ] } };
  const obtenu = N.cppEssai(sc, essai);
  ok("le CPP obtenu est la MOITIÉ : la charnière de l'essai prime", obtenu.cpp, 0.2);
  ok("les deux logements sont comptés", obtenu.nbLogements, 2);
  ok("aucun écarté", obtenu.nonChiffrables, 0);

  const partiel = N.cppEssai(sc, { params: { logements: [
    { logementId: "g1", charniere: 200 },
    { logementId: "inconnu", charniere: 200 }
  ] } });
  ok("un logement inconnu est ÉCARTÉ, pas compté", partiel.nbLogements, 1);
  ok("et il est DIT", partiel.nonChiffrables, 1);
  ok("un essai sans paramètres ne donne pas 0, il donne null",
     N.cppEssai(sc, { params: { logements: [] } }).cpp, null);
  ok("pas de scénario : null, jamais une erreur", N.cppEssai(null, essai).cpp, null);
}

/* Sur l'export RÉEL : combien d'essais deviennent chiffrables ? */
titre("SUR L'EXPORT RÉEL — combien d'essais redeviennent chiffrables");
{
  let total = 0, chiffrables = 0;
  const obtenus = [];
  forEachEssai(proj["cloud_courant.json"].p, (sc, e) => {
    total++;
    const c = N.cppEssai(sc, e);
    if (c.cpp !== null) { chiffrables++; obtenus.push(c.cpp); }
  });
  console.log("         " + total + " essai(s) dans l'export, " + chiffrables + " chiffrable(s)");
  if (obtenus.length) {
    console.log("         CPP obtenus : " + obtenus.map(v => v.toFixed(4)).join(", ") + " €/pce");
  }
  ok("au moins un essai réel devient chiffrable", chiffrables > 0, true);
}

/* ══════════════════════════════════════════════════════════════════════════
   3. LES CAS LIMITES — ce que l'import doit refuser ou avouer
   ══════════════════════════════════════════════════════════════════════════ */

titre("LES CAS LIMITES");

ok("null : refusé, sans planter", projeter(null).ok, false);
ok("une chaîne : refusée", projeter("bonjour").ok, false);
ok("un nombre : refusé", projeter(42).ok, false);
ok("un tableau : refusé", projeter([]).ok, false);
ok("un objet vide : refusé", projeter({}).ok, false);
ok("un autre objet : refusé, avec la raison",
   projeter({ produits: [] }).erreur !== null, true);
ok("lignes vide : refusé", projeter({ lignes: [] }).ok, false);

ok("le format est lu et rapporté", projeter({ format: 8, lignes: [ligneMinimale()] })
   .rapport.format, 8);

/* format 6 : les lignes vivent dans les projets */
{
  const p = projeter({ format: 6, projets: [
    { id: "p1", nom: "A", lignes: [ligneMinimale()] },
    { id: "p2", nom: "B", lignes: [Object.assign(ligneMinimale(), { nom: "Ligne B" })] }
  ] });
  ok("le format 6 est aplati", p.ok, true);
  ok("ses deux lignes sont retrouvées", p.rapport.lignes, 2);
}

titre("UNE LIGNE SANS DONNÉES — elle existe, elle ne chiffre pas");
{
  const p = projeter({ format: 8, lignes: [{ id: "l1", nom: "Ligne nue" }] });
  ok("elle est importée quand même", p.rapport.lignes, 1);
  const v = N.verdictLigne(p.lignes[0], []);
  ok("son CPP est null, pas 0", v.cppProd, null);
  ok("elle ne se dilue pas : elle est comptée", v.nonChiffrables, 0);
}

titre("DES DONNÉES INCOMPLÈTES — l'avertissement dit vrai");
{
  const p = projeter({ format: 8, lignes: [ligneAvecLogement({ prix: "", aretes: 8, charniere: 100 })] });
  ok("un prix manquant est compté", p.rapport.sansPrix, 1);
  ok("et il est annoncé", p.rapport.avertissements.some(a => /prix/.test(a)), true);
  ok("le logement reste non chiffrable", N.coutLogement(p.lignes[0].refs[0].ops[0].scs[0].outils[0].logements[0]), null);
}
{
  const p = projeter({ format: 8, lignes: [ligneAvecLogement({ prix: 40, aretes: 0, charniere: 100 })] });
  ok("zéro arête n'est pas une durée de vie infinie", p.rapport.sansAretes, 1);
}
{
  const p = projeter({ format: 8, lignes: [ligneAvecLogement({ prix: 40, aretes: 8, charniere: "" })] });
  ok("une charnière vide est comptée", p.rapport.sansCharniere, 1);
}

titre("LE CODE D'OPÉRATION — reconstruit, jamais inventé");
ok("OP + ordre", I.codeDeOp({ nom: "OP10 Ebauche", ordre: 10 }), "OP10");
ok("ordre 40 -> OP40", I.codeDeOp({ nom: "Perçages", ordre: 40 }), "OP40");
ok("sans ordre : le nom", I.codeDeOp({ nom: "Rectification", ordre: null }), "Rectification");
ok("sans ordre mais un OP dans le nom : il est lu",
   I.codeDeOp({ nom: "OP 30 Perçages", ordre: null }), "OP30");
ok("un code déjà présent est respecté", I.codeDeOp({ nom: "x", ordre: 10, code: "SPECIAL" }), "SPECIAL");

titre("LA PROJECTION EST DETERMINISTE — deux lectures, le même objet");
{
  const brut = lireJson("cloud_courant.json");
  ok("projection égale à la relecture", JSON.stringify(projeter(brut).lignes),
     JSON.stringify(projeter(brut).lignes));
}

titre("LE POIDS — mesuré, pas promis");
{
  const brut = { lignes: [ligneAvecLogement({ prix: 40, aretes: 8, charniere: 100 })] };
  const w = poids(brut, projeter(brut).lignes);
  ok("le rapport avant/après existe", w.apres > 0 && w.avant > 0, true);
  ok("sur un petit objet, le rapport est proche de 1", w.ratio > 0.5, true);
  ok("un objet non sérialisable ne fait pas planter", poids({ x: 1n }, {}).avant, 0);
}

/* ── des aides, uniquement pour les tests ── */
function ligneMinimale() { return { id: "l1", nom: "L", references: [] }; }
function ligneAvecLogement(log) {
  return { id: "l1", nom: "L", references: [{ id: "r1", nom: "R", cibleCPP: 0.02, ops: [
    { id: "o1", nom: "OP10", ordre: 10, scenarios: [{ id: "s1", name: "Process actuel",
      baseline: true, outils: [{ id: "t1", numero: "T1", plan: "…320 Ko…", logements: [log] }],
      essais: [] }] }
  ] }] };
}

/* ══════════════════════════════════════════════════════════════════════════ */
console.log("\n" + "=".repeat(64));
console.log("PROTO IMPORT : " + (okNb + koNb) + " tests | " + koNb + " echecs");
console.log(koNb ? "IL Y A DES RESSINS" : "TOUT EST VERT");
console.log("=".repeat(64));
process.exit(koNb ? 1 : 0);
