/* ============================================================================
   2resume — LES TESTS DE LA PROJECTION
   ----------------------------------------------------------------------------
   Ils tournent sur les QUATRE exports réels présents dans le dépôt. Un jeu
   synthétique ne prouverait rien sur ce que Matis déposera réellement.

   Les comptes attendus ont été MESURÉS sur les fichiers, puis figés ici : si
   un de ces chiffres bouge, soit les données ont changé, soit la projection
   a commencé à perdre quelque chose. Dans les deux cas, il faut savoir lequel.
   Exécution : node test_import.js
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
  if (!bon) { echecs++; console.log("  ECHEC " + nom + " — obtenu " + JSON.stringify(obtenu) + ", attendu " + JSON.stringify(attendu)); }
  else console.log("  ok   " + nom);
}
function okVrai(nom, condition) { ok(nom, !!condition, true); }

const src = fs.readFileSync(path.join(__dirname, "coeur.js"), "utf8") + "\n"
  + fs.readFileSync(path.join(__dirname, "import.js"), "utf8");
const N = new Function(src + "\nreturn { projeter, poids, relireEtat, etatVierge, racinesLignes, classerArticle, codeDeOp, cppOutillageScenario, outillageDeScenario, cppEssai, battDe, statutScenario, santeDonnees, scenarioDeProd, nb, FORMAT_DONNEES };")();

const REPO = path.join(__dirname, "..");
function lit(nom) { return JSON.parse(fs.readFileSync(path.join(REPO, nom), "utf8")); }

const FICHIERS = ["cloud_courant.json", "suivi_corrige_mabec.json",
  "base_depart_2026_2027.json", "IMPORT_MATIS.json"];

/* ── les comptes MESURÉS, figés ──────────────────────────────────────────── */
const ATTENDU = {
  "cloud_courant.json": { lignes: 10, references: 6, ops: 17, scenarios: 23, outils: 121,
    logements: 135, essais: 5, prelevements: 84,
    sansPrix: 2, sansAretes: 0, sansCharniere: 5, sansMabec: 34, mabecDevines: 89,
    sansBatt: 43, sansCible: 0, sansVolume: 1, sansReference: 6, outilsSansNumero: 2,
    postesSansProd: 1, ratio: 0.021 },
  "suivi_corrige_mabec.json": { lignes: 10, references: 6, ops: 17, scenarios: 23, outils: 121,
    logements: 135, essais: 5, prelevements: 84,
    sansPrix: 2, sansAretes: 0, sansCharniere: 5, sansMabec: 7, mabecDevines: 19,
    sansBatt: 43, sansCible: 0, sansVolume: 1, sansReference: 6, outilsSansNumero: 2,
    postesSansProd: 1, ratio: 0.021 },
  "base_depart_2026_2027.json": { lignes: 4, references: 16, ops: 16, scenarios: 16, outils: 210,
    logements: 210, essais: 0, prelevements: 0,
    sansPrix: 0, sansAretes: 0, sansCharniere: 0, sansMabec: 63, mabecDevines: 147,
    sansBatt: 0, sansCible: 16, sansVolume: 11, sansReference: 0, outilsSansNumero: 0,
    postesSansProd: 0, ratio: 1.473 },
  "IMPORT_MATIS.json": { lignes: 4, references: 12, ops: 44, scenarios: 44, outils: 129,
    logements: 192, essais: 0, prelevements: 0,
    sansPrix: 0, sansAretes: 0, sansCharniere: 40, sansMabec: 6, mabecDevines: 1,
    sansBatt: 0, sansCible: 3, sansVolume: 8, sansReference: 0, outilsSansNumero: 0,
    postesSansProd: 0, ratio: 1.653 }
};

const P = {};

console.log("\n── LES QUATRE EXPORTS RÉELS ENTRENT ──");
FICHIERS.forEach(f => {
  const s = lit(f);
  const p = N.projeter(s);
  P[f] = p;
  ok(f + " est accepté", p.ok, true);
});

console.log("\n── LES COMPTES DE CONTRÔLE, valeur par valeur ──");
FICHIERS.forEach(f => {
  const r = P[f].rapport, a = ATTENDU[f];
  ["lignes", "references", "ops", "scenarios", "outils", "logements", "essais",
   "prelevements", "sansPrix", "sansAretes", "sansCharniere", "sansMabec",
   "mabecDevines", "sansBatt", "sansCible", "sansVolume", "sansReference",
   "outilsSansNumero", "postesSansProd"].forEach(k => {
    ok(f + " · " + k, r[k], a[k]);
  });
});

console.log("\n── LE POIDS JETÉ ──");
FICHIERS.forEach(f => {
  const s = lit(f);
  const w = N.poids(s, P[f].lignes);
  ok(f + " · ratio", w.ratio, ATTENDU[f].ratio, 0.002);
});

console.log("\n── CE QUE LE RÉIMPORT A RÉVÉLÉ : le CPP prévu contre obtenu ──");
/* Les chiffres qui ont motivé cet outil. S'ils bougent sans raison, la
   projection ou le noyau a changé de comportement. */
const cc = P["cloud_courant.json"];
let sl500 = null, ky3500 = null;
cc.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc => {
  if (/SL500/i.test(sc.name)) sl500 = { l: l, op: op, sc: sc };
  if (/KY3500/i.test(sc.name)) ky3500 = { l: l, op: op, sc: sc };
}))));
okVrai("le scénario SL500 existe dans l'export réel", !!sl500);
okVrai("le scénario KY3500 existe dans l'export réel", !!ky3500);
ok("SL500 : le CPP prévu", N.cppOutillageScenario(sl500.sc), 0.17348194444444445, 1e-9);
ok("SL500 : le CPP OBTENU par l'essai", N.cppEssai(sl500.sc, sl500.sc.essais[0]).cpp, 0.0478, 1e-9);
ok("KY3500 : le CPP prévu", N.cppOutillageScenario(ky3500.sc), 0.24518194444444447, 1e-9);
ok("KY3500 : le CPP OBTENU", N.cppEssai(ky3500.sc, ky3500.sc.essais[0]).cpp, 0.07966666666666668, 1e-9);
okVrai("et ces deux scénarios ne sont PAS en production (d'où l'étage 3)",
  sl500.sc.statut !== "serie" && ky3500.sc.statut !== "serie");

console.log("\n── LES PORTES QUE LE PROTO AVAIT LAISSÉES OUVERTES ──");
/* Le journal du Tour 54 le disait : personne ne vérifiait que battD/battG
   SURVIVAIENT à la projection. Si elle cesse de les copier, le noyau recevra
   undefined, battra en silence, et ces tests-ci resteront verts — sauf celui-là. */
let dgSeuls = 0, battSeuls = 0, aucun = 0, transportes = 0;
cc.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc =>
  sc.essais.forEach(e => e.prelevements.forEach(p => {
    const battLu = N.nb(p.batt), dLu = N.nb(p.battD), gLu = N.nb(p.battG);
    if (battLu !== null) battSeuls++;
    else if (dLu !== null || gLu !== null) dgSeuls++;
    else aucun++;
    if (p.battD !== "" || p.battG !== "" || p.batt !== "") transportes++;
  }))))));
ok("les prélèvements batt-seul mesurés", battSeuls, 1);
ok("les prélèvements D/G-seuls EXISTENT et sont transportés", dgSeuls, 40);
ok("ceux qui n'ont rien restent comptés", aucun, 43);
ok("le pire des deux côtés est bien appliqué sur les données réelles",
  (() => { let pire = 0;
    cc.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc =>
      sc.essais.forEach(e => e.prelevements.forEach(p => {
        const d = N.nb(p.battD), g = N.nb(p.battG);
        if (N.nb(p.batt) === null && d !== null && g !== null && d !== g
          && N.battDe(p) === Math.max(d, g)) pire++;
      }))))));
    return pire > 0; })(), true);
okVrai("les 84 prélèvements sont tous transportés (le champ existe, même vide)", transportes === 84 - aucun);

console.log("\n── LES CIBLES DU SITE : en valeur, pas en présence ──");
const cibles = {};
cc.lignes.forEach(l => l.references.forEach(rf => { cibles[rf.nom] = rf.cibleCPP; }));
ok("DV302x26RPI", cibles["DV302x26RPI"], 0.129, 1e-9);
ok("DV 356x26 RPI", cibles["DV 356x26 RPI"], 0.575, 1e-9);
ok("DV 304x28 RPE", cibles["DV 304x28 RPE"], 0.212, 1e-9);
ok("DP 290x12", cibles["DP 290x12"], 0.232, 1e-9);
ok("DP 330x14", cibles["DP 330x14"], 0.384, 1e-9);
ok("DV 330x28 RPE K0", cibles["DV 330x28 RPE K0"], 0.218, 1e-9);

console.log("\n── L'IDENTITÉ DES OPÉRATIONS : le nom de l'atelier ──");
let codesReels = {};
cc.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => { codesReels[op.nom] = op.code; })));
ok("« OP40 Finition Pistes » s'appelle OP40", codesReels["OP40 Finition Pistes"], "OP40");
ok("« OP 30 Perçages » s'appelle OP30", codesReels["OP 30 Perçages"], "OP30");
ok("« OP20 Ebauche piste Exter » s'appelle OP20", codesReels["OP20 Ebauche piste Exter"], "OP20");
ok("« OP15 » garde son numéro", codesReels["OP15"], "OP15");

console.log("\n── LE MABEC : rangé, jamais mélangé en silence ──");
ok("un ISO connu reste une plaquette", N.classerArticle({ ref: "SNGN 090416-F" }).iso, "SNGN 090416-F");
ok("un code article Z000 est un MABEC — et c'est compté comme déduit",
   [N.classerArticle({ ref: "Z000 546 265" }).mabec, N.classerArticle({ ref: "Z000 546 265" }).devine], ["Z000 546 265", "mabec"]);
ok("IMPORT_MATIS : le MABEC explicite est conservé tel quel",
   N.classerArticle({ mabec: "IM02 137 021", ref: "KY3500" }).mabec, "IM02 137 021");
ok("IMPORT_MATIS : l'ISO explicite aussi", N.classerArticle({ mabec: "IM02 137 021", ref: "KY3500" }).iso, "KY3500");
let matisSansMabec = 0;
P["IMPORT_MATIS.json"].lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op =>
  op.scenarios.forEach(sc => sc.outils.forEach(o => o.logements.forEach(lg => { if (!lg.mabec) matisSansMabec++; }))))));
ok("les logements de Matis sans MABEC (le classeur ne les donne pas)", matisSansMabec, 6);

console.log("\n── LES INVARIANTS SUR TOUT L'EXPORT ──");
let ecarts = 0, scn = 0, nonCh = 0, incoherents = 0;
cc.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc => {
  scn++;
  const o = N.outillageDeScenario(sc), s = N.cppOutillageScenario(sc);
  if ((o.cpp === null) !== (s === null)) ecarts++;
  else if (o.cpp !== null && Math.abs(o.cpp - s) > 1e-9) ecarts++;
  nonCh += o.nonChiffrables;
  if (sc.baseline === true && sc.statut !== "serie") incoherents++;
}))));
ok("la somme des outils EST le CPP du scénario, sur les " + scn + " scénarios réels", ecarts, 0);
ok("les logements non chiffrables de la décomposition", nonCh, 5);
ok("baseline ⇒ statut série, sans exception restante", incoherents, 0);

console.log("\n── LE DÉTERMINISME : deux lectures, un même résultat ──");
const deuxieme = N.projeter(lit("cloud_courant.json"));
ok("deux projections produisent le même JSON",
  JSON.stringify(deuxieme.lignes), JSON.stringify(cc.lignes), true);

console.log("\n── LES IDENTIFIANTS : stables quand ils existent ──");
let idsExportes = 0, idsGardes = 0;
cc.lignes.forEach(l => { if (/^l/.test(l.id) || l.id.length > 3) idsExportes++;
  l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc =>
    sc.outils.forEach(o => o.logements.forEach(lg => { idsExportes++; }))))); });
ok("des identifiants existent dans l'export et sont REPRIS tels quels",
  (() => { const brut = lit("cloud_courant.json");
    let gardes = 0, total = 0, trouves = new Set();
    const traverse = (o) => { if (!o || typeof o !== "object") return;
      if (o.id && typeof o.id === "string") trouves.add(o.id);
      Object.values(o).forEach(traverse); };
    traverse(brut.lignes);
    cc.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc =>
      sc.outils.forEach(o => o.logements.forEach(lg => {
        total++;
        if (trouves.has(lg.id)) gardes++;
      }))))));
    return [total > 100, gardes === total]; })(), [true, true]);

console.log("\n── LES REFUS : ce qui n'est pas un export ne rentre pas ──");
ok("null refusé", N.projeter(null).ok, false);
ok("42 refusé", N.projeter(42).ok, false);
ok("un objet vide refusé", N.projeter({}).ok, false);
ok("un tableau refusé", N.projeter([1, 2]).ok, false);
ok("des lignes vides refusées", N.projeter({ lignes: [] }).ok, false);
ok("le message dit ce qui manque", N.projeter({}).erreur.length > 0, true);

console.log("\n── LE FORMAT 6 : aplati, et le dit ──");
const f6 = N.projeter({ projets: [{ nom: "P", lignes: [{ nom: "EMAG 1", references: [] }] }] });
okVrai("le format 6 entre", f6.ok);
ok("sa forme est déclarée", f6.forme, "projets");
okVrai("l'avertissement d'aplatissement est affiché",
  f6.rapport.avertissements.some(a => a.indexOf("aplatis") >= 0));

console.log("\n── L'ALLER-RETOUR : relire un état de CET outil ne perd rien ──");
const etat9 = N.relireEtat({ lignes: cc.lignes, projets: [], livraisons: [] });
ok("l'état relu porte le format courant", etat9.format, N.FORMAT_DONNEES);
const recompte = N.projeter(etat9).rapport;
ok("l'aller-retour conserve le nombre de lignes", recompte.lignes, 10);
ok("et de références", recompte.references, 6);
ok("et de scénarios", recompte.scenarios, 23);
ok("et de logements", recompte.logements, 135);
ok("et d'essais", recompte.essais, 5);
ok("et de prélèvements", recompte.prelevements, 84);
ok("et les cibles", recompte.sansCible, 0);

console.log("\n── LA SANTÉ, mesurée sur l'export réel ──");
const sante = N.santeDonnees({ lignes: cc.lignes });
ok("lignes", sante.lignes, 10);
ok("lignes sans référence (Weisser 1-4, PCI 4-5)", sante.sansReference, 6);
ok("postes", sante.postes, 17);
ok("postes sans production", sante.sansProd, 1);
ok("logements non chiffrables", sante.nonChiffrables, 5);
ok("logements sans MABEC", sante.sansMabec, 34);
ok("prélèvements sans battement", sante.sansBatt, 43);
ok("références sans volume annuel", sante.referencesSansVolume, 1);

console.log("\n" + total + " tests exécutés, " + echecs + " échec(s)");
if (echecs) { console.log("ROUGE — " + echecs + " échec(s)"); process.exit(1); }
console.log("TOUT EST VERT");
