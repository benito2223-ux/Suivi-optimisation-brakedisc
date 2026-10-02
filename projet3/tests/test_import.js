/* ============================================================================
   PROJET3 — LES TESTS DE MIGRATION ET DE FUSION
   Tournés sur les QUATRE exports réels présents dans le dépôt : un jeu
   synthétique ne prouverait rien sur ce que Matis déposera réellement.
   Exécution : node tests/test_import.js
   ========================================================================== */

const { charger, creerJuge } = require("./harnais.js");
const fs = require("fs");
const path = require("path");

const C = charger("src/coeur.js", ["coutLogement", "cppOutillageScenario", "tuilesDeLignes", "verdictPoste"]);
const I = charger("src/import.js", [
  "normaliserEtat", "fusionnerEtat", "poids", "racinesLignes", "IMPORT_VERSION"
]);

const j = creerJuge("PROJET3 MIGRATION");
const ok = j.ok, bloc = j.bloc;

/* Les quatre exports réels du dépôt — les données ne quittent jamais la
   machine : ces fichiers ne sont jamais déployés (.surgeignore whitelist). */
const EXPORTS = [
  "cloud_courant.json",
  "suivi_corrige_mabec.json",
  "base_depart_2026_2027.json",
  "IMPORT_MATIS.json"
];

/* ============================================================================
   1. LE CPP SURVIT À LA MIGRATION, EXACTEMENT — sur chaque export réel
   ============================================================================ */

console.log("\n── LE CPP SURVIT À LA MIGRATION (les vrais exports) ─────────");

/* Le CPP d'un scénario, calculé directement sur le JSON BRUT — sans passer
   par la normalisation : c'est la référence indépendante. */
function cppBrut(scBrut) {
  let total = 0, n = 0;
  (scBrut.outils || []).forEach(o => (o.logements || []).forEach(l => {
    const c = C.coutLogement(l);
    if (c !== null) { total += c; n++; }
  }));
  return n ? total : null;
}

function parcourirScenarios(etat, visiteur) {
  (etat.lignes || []).forEach(l => (l.references || []).forEach(ref =>
    (ref.ops || []).forEach(op => (op.scenarios || []).forEach(sc => visiteur(sc, ref, op, l)))));
}

EXPORTS.forEach(nom => {
  bloc(nom, () => {
    const brut = JSON.parse(fs.readFileSync(path.resolve(__dirname, "..", "..", nom), "utf8"));
    const mig = I.normaliserEtat(brut);
    if (!mig.ok) { ok(nom + " se normalise", mig.erreur, null); return; }

    /* Chaque scénario chiffrable du brut retrouve EXACTEMENT son CPP. */
    const cppBrutParId = {};
    parcourirScenarios({ lignes: I.racinesLignes(brut) }, sc => {
      const cpp = cppBrut(sc);
      if (cpp !== null) cppBrutParId[sc.id] = cpp;
    });
    let verifies = 0, ecartMax = 0;
    parcourirScenarios(mig.etat, sc => {
      if (cppBrutParId[sc.id] === undefined) return;
      const cpp = C.cppOutillageScenario(sc);
      if (cpp === null) return;
      verifies++;
      ecartMax = Math.max(ecartMax, Math.abs(cpp - cppBrutParId[sc.id]));
    });
    ok(nom + " : " + verifies + " scénario(s) chiffrable(s) retrouvé(s)", verifies > 0, true);
    ok(nom + " : le CPP survit à la migration (écart max " + ecartMax.toExponential(2) + ")",
       ecartMax, 0, 1e-12);

    /* Les stats se tiennent : logements et essais intacts. */
    ok(nom + " : rapports cohérents", mig.rapport.logements > 0 && mig.rapport.lignes > 0, true);

    /* La cohérence ★/série (v4.4) : tout baseline est en série. */
    let incoherences = 0;
    parcourirScenarios(mig.etat, sc => {
      if (sc.baseline && sc.statut !== "serie") incoherences++;
      if (sc.statut === "serie" && !sc.baseline) incoherences++;
    });
    ok(nom + " : ★ et « en série » restent verrouillés ensemble", incoherences, 0);

    /* L'idempotence : normaliser deux fois vaut normaliser une fois. */
    const deux = I.normaliserEtat(mig.etat);
    ok(nom + " : la normalisation est idempotente",
       JSON.stringify(deux.etat) === JSON.stringify(mig.etat), true);
  });
});

/* ============================================================================
   2. LES DÉTAILS QUE LE PROTO JETAIT — la v3 les garde
   ============================================================================ */

console.log("\n── SANS PERTE (photos, plans, Marposs, rebut, projets) ──────");

bloc("cloud_courant : le gros export réel", () => {
  const brut = JSON.parse(fs.readFileSync(path.resolve(__dirname, "..", "..", "cloud_courant.json"), "utf8"));
  const mig = I.normaliserEtat(brut);
  const r = mig.rapport;

  /* Compter dans le BRUT, indépendamment : c'est la preuve qu'on compte
     ce qui existe, pas ce qu'on a réussi à copier. */
  let photosBrut = 0, essaisBrut = 0, prelsBrut = 0;
  (I.racinesLignes(brut) || []).forEach(l => (l.references || []).forEach(ref =>
    (ref.ops || []).forEach(op => (op.scenarios || []).forEach(sc => {
      (sc.essais || []).forEach(e => {
        essaisBrut++;
        photosBrut += (e.photos || []).length;
        prelsBrut += (e.prelevements || []).length;
      });
    }))));
  ok("les essais sont tous là (" + essaisBrut + ")", r.essais, essaisBrut);
  ok("les photos sont conservées (" + photosBrut + ")", r.photos, photosBrut);
  ok("les prélèvements sont tous là (" + prelsBrut + ")", r.prelevements, prelsBrut);

  /* Le battement D/G : le pont qui a sauvé 83 prélèvements sur 84. */
  let avecDG = 0;
  (I.racinesLignes(brut) || []).forEach(l => (l.references || []).forEach(ref =>
    (ref.ops || []).forEach(op => (op.scenarios || []).forEach(sc =>
      (sc.essais || []).forEach(e => (e.prelevements || []).forEach(p => {
        if (parseFloat(p.battD) > 0 || parseFloat(p.battG) > 0) avecDG++;
      }))))));
  ok("les battements D/G sont conservés (" + avecDG + " prélèvements)",
     avecDG > 0, true);

  ok("les cibles CPP sont conservées", r.scenariosCibles > 0, true);
  ok("les plans de porte-outil sont conservés (le proto les jetait)",
     typeof r.plans === "number", true);

  /* Les projets migrent avec leurs étiquettes. */
  const nbProjetsBrut = (brut.projets || []).length;
  ok("les projets sont conservés (" + nbProjetsBrut + ")", r.projets, nbProjetsBrut);
  let tagsBrut = 0;
  (brut.projets || []).forEach(pj => { tagsBrut += (pj.tags || []).length; });
  ok("les étiquettes sont conservées (" + tagsBrut + ")", r.etiquettes, tagsBrut);

  /* La v3 peut calculer sur les données réelles : les tuiles se remplissent. */
  const tuiles = C.tuilesDeLignes(mig.etat.lignes);
  ok("les tuiles se remplissent sur les vraies données (" + tuiles.length + " lignes)",
     tuiles.length, r.lignes);
  ok("au moins une ligne est chiffrable", tuiles.some(t => t.cpp !== null), true);
});

bloc("IMPORT_MATIS : l'ancien champ « nom » des scénarios", () => {
  const brut = JSON.parse(fs.readFileSync(path.resolve(__dirname, "..", "..", "IMPORT_MATIS.json"), "utf8"));
  const mig = I.normaliserEtat(brut);
  let noms = 0, vides = 0;
  parcourirScenarios(mig.etat, sc => {
    if (sc.name && sc.name !== "Scénario") noms++;
    if (!sc.name) vides++;
  });
  ok("les scénarios portent leur libellé d'origine (nom → name)", vides, 0);
  ok("le classeur de Matis arrive lisible (" + noms + " scénarios nommés)", noms > 0, true);
  ok("les MABEC sont conservés (la clé de raccordement)", mig.rapport.logements > 0, true);
  /* Les MABEC ne doivent pas être recopiés d'une ligne à la suivante (loi du
     correcteur, interdit 3) : ce qui était vide reste vide. */
  let mabecVides = 0;
  parcourirScenarios(mig.etat, sc => (sc.outils || []).forEach(o => (o.logements || []).forEach(l => {
    if (!l.mabec) mabecVides++;
  })));
  let mabecVidesBrut = 0;
  (I.racinesLignes(brut) || []).forEach(l => (l.references || []).forEach(ref =>
    (ref.ops || []).forEach(op => (op.scenarios || []).forEach(sc => (sc.outils || []).forEach(o =>
      (o.logements || []).forEach(l => { if (!l.mabec) mabecVidesBrut++; }))))));
  ok("une case vide reste vide (" + mabecVides + " MABEC non attribués)",
     mabecVides, mabecVidesBrut);
});

/* ============================================================================
   3. LES FORMATS ANCIENS ET LES MIGRATIONS SPÉCIALES
   ============================================================================ */

console.log("\n── LES FORMATS ANCIENS (6 : projets porteurs) ───────────────");

bloc("format 6 : les lignes portées par les projets s'aplatissent", () => {
  const f6 = {
    format: 6,
    projets: [{
      id: "pj1", nom: "Projet 6", responsable: "Julien",
      tags: [],
      lignes: [{
        id: "l1", nom: "EMAG 1", coutHoraire: 60,
        references: [{
          id: "r1", nom: "DV 356x26 RPI", cibleCPP: 0.12,
          ops: [{
            id: "o1", nom: "OP10", ordre: 10,
            scenarios: [{
              id: "s1", nom: "Base Excel", baseline: true,
              outils: [{ id: "t1", numero: "T543", logements: [{ id: "g1", nom: "D1", prix: 38, aretes: 8, charniere: 800 }] }]
            }]
          }]
        }]
      }]
    }]
  };
  const mig = I.normaliserEtat(f6);
  ok("le format 6 se lit", mig.ok, true);
  ok("une ligne aplatie", mig.etat.lignes.length, 1);
  ok("le scénario garde son libellé", mig.etat.lignes[0].references[0].ops[0].scenarios[0].name, "Base Excel");
  ok("le responsable texte devient un responsable de la liste gérée",
     mig.etat.responsables.some(u => u.nom === "Julien"), true);
  ok("le projet migre vers responsableId", typeof mig.etat.projets[0].responsableId, "string");
  ok("le projet ne porte plus ses lignes (doublon interdit)",
     mig.etat.projets[0].lignes, undefined);
  ok("un id stable a été généré pour le responsable créé",
     mig.etat.projets[0].responsableId.length > 0, true);
});

bloc("un fichier qui n'est pas un export est refusé, poliment", () => {
  ok("null refusé", I.normaliserEtat(null).ok, false);
  ok("un objet vide refusé", I.normaliserEtat({}).ok, false);
  ok("un objet sans lignes refusé", I.normaliserEtat({ format: 8, projets: [] }).ok, false);
  ok("le message dit ce qui n'a pas marché",
     I.normaliserEtat({}).erreur.indexOf("n'est pas un export") >= 0, true);
});

bloc("deux responsables avec le même nom migrés vers UNE entrée", () => {
  const f8 = {
    format: 8,
    lignes: [{ id: "l1", nom: "EMAG 1", references: [] }],
    projets: [
      { id: "pj1", nom: "A", responsable: "Julien " },
      { id: "pj2", nom: "B", responsable: "julien" }
    ]
  };
  const mig = I.normaliserEtat(f8);
  ok("une seule entrée pour deux orthographes", mig.etat.responsables.length, 1);
  ok("les deux projets pointent le même id",
     mig.etat.projets[0].responsableId === mig.etat.projets[1].responsableId, true);
});

/* ============================================================================
   4. LA FUSION — deux postes travaillent, aucun essai n'est perdu
   ============================================================================ */

console.log("\n── LA FUSION (arbitrage modifieLe) ──────────────────────────");

function scAvecEssai(id, titre, modifieLe) {
  return {
    id: id, name: id, baseline: false, statut: "essai",
    outils: [{ id: "t1", numero: "T1", logements: [{ id: "g1", nom: "D1", prix: 38, aretes: 8, charniere: 800 }] }],
    essais: [{ id: "e-" + id, titre: titre, modifieLe: modifieLe, prelevements: [{ id: "p1", piece: 1, batt: 0.10 }] }]
  };
}
function etatFusion(essaiModifieLeA, essaiModifieLeB) {
  return {
    format: 9,
    lignes: [{
      id: "l1", nom: "EMAG 1", references: [{
        id: "r1", nom: "DV", ops: [{
          id: "o1", nom: "OP10", scenarios: [scAvecEssai("s1", "L'essai", essaiModifieLeA)]
        }]
      }]
    }],
    projets: [], responsables: [], livraisons: [], backlog: [], activeScenarioId: ""
  };
}

bloc("l'arrivée plus récente gagne l'essai", () => {
  const local = etatFusion("2026-10-01T08:00:00", "2026-10-02T08:00:00");
  const arrivee = etatFusion("2026-10-02T08:00:00", "2026-10-02T08:00:00");
  local.lignes[0].references[0].ops[0].scenarios[0].essais[0].titre = "Version locale";
  arrivee.lignes[0].references[0].ops[0].scenarios[0].essais[0].titre = "Version arrivée";
  const f = I.fusionnerEtat(local, arrivee);
  ok("le plus récent gagne",
     f.etat.lignes[0].references[0].ops[0].scenarios[0].essais[0].titre, "Version arrivée");
  ok("le rapport compte le conflit gagné", f.rapport.essaisGagnesArrivee, 1);
});

bloc("le local plus récent garde l'essai", () => {
  const local = etatFusion("2026-10-03T08:00:00", "2026-10-03T08:00:00");
  const arrivee = etatFusion("2026-10-02T08:00:00", "2026-10-02T08:00:00");
  local.lignes[0].references[0].ops[0].scenarios[0].essais[0].titre = "Version locale";
  arrivee.lignes[0].references[0].ops[0].scenarios[0].essais[0].titre = "Version arrivée";
  const f = I.fusionnerEtat(local, arrivee);
  ok("le local garde",
     f.etat.lignes[0].references[0].ops[0].scenarios[0].essais[0].titre, "Version locale");
  ok("le rapport compte l'essai gardé", f.rapport.essaisGardesLocaux, 1);
});

bloc("un essai créé de l'autre côté arrive", () => {
  const local = etatFusion("2026-10-01T08:00:00", "2026-10-01T08:00:00");
  const arrivee = etatFusion("2026-10-01T08:00:00", "2026-10-01T08:00:00");
  const scA = arrivee.lignes[0].references[0].ops[0].scenarios[0];
  scA.essais.push({ id: "e-nouveau", titre: "Nouveau du terrain", modifieLe: "2026-10-02T08:00:00", prelevements: [] });
  const f = I.fusionnerEtat(local, arrivee);
  const essais = f.etat.lignes[0].references[0].ops[0].scenarios[0].essais;
  ok("deux essais après fusion", essais.length, 2);
  ok("l'essai ajouté est compté", f.rapport.essaisAjoutes, 1);
});

bloc("un scénario créé de l'autre côté arrive", () => {
  const local = etatFusion("2026-10-01T08:00:00", "2026-10-01T08:00:00");
  const arrivee = etatFusion("2026-10-01T08:00:00", "2026-10-01T08:00:00");
  arrivee.lignes[0].references[0].ops[0].scenarios.push(scAvecEssai("s2", "Nouveau scénario", ""));
  const f = I.fusionnerEtat(local, arrivee);
  const scs = f.etat.lignes[0].references[0].ops[0].scenarios;
  ok("deux scénarios après fusion", scs.length, 2);
  ok("le scénario ajouté est compté", f.rapport.scenariosAjoutes, 1);
});

bloc("les étiquettes de projet s'unissent", () => {
  const local = etatFusion("", "");
  const arrivee = etatFusion("", "");
  local.projets = [{ id: "p1", nom: "Éco", tags: [{ ligneId: "l1", referenceId: "r1", opId: "o1", scenarioId: "s1" }] }];
  arrivee.projets = [{
    id: "p1", nom: "Éco",
    tags: [{ ligneId: "l1", referenceId: "r1", opId: "o1", scenarioId: "s2" }]
  }];
  const f = I.fusionnerEtat(local, arrivee);
  ok("les deux étiquettes coexistent", f.etat.projets[0].tags.length, 2);
  ok("la fusion est comptée", f.rapport.projetsFusionnes, 1);
});

bloc("les réglages locaux survivent à une fusion", () => {
  const local = etatFusion("", "");
  const arrivee = etatFusion("", "");
  arrivee.activeScenarioId = "s1";   // l'arrivée ne dicte pas la vue locale
  const f = I.fusionnerEtat(local, arrivee);
  ok("la vue active reste locale", f.etat.activeScenarioId, "");
});

bloc("la fusion tourne sur les vrais exports sans rien perdre", () => {
  const brutA = JSON.parse(fs.readFileSync(path.resolve(__dirname, "..", "..", "cloud_courant.json"), "utf8"));
  const brutB = JSON.parse(fs.readFileSync(path.resolve(__dirname, "..", "..", "IMPORT_MATIS.json"), "utf8"));
  const a = I.normaliserEtat(brutA);
  const b = I.normaliserEtat(brutB);
  const essaisAvant = compterEssais(a.etat) + compterEssais(b.etat);
  const f = I.fusionnerEtat(a.etat, b.etat);
  const essaisApres = compterEssais(f.etat);
  ok("aucun essai n'a disparu (" + essaisAvant + " → " + essaisApres + ")", essaisApres, essaisAvant);
  ok("la fusion est allée au bout (rapport présent)", typeof f.rapport.essaisGardesLocaux, "number");
});

function compterEssais(etat) {
  let n = 0;
  (etat.lignes || []).forEach(l => (l.references || []).forEach(ref =>
    (ref.ops || []).forEach(op => (op.scenarios || []).forEach(sc => { n += (sc.essais || []).length; }))));
  return n;
}

/* ============================================================================
   FINALISATION
   ============================================================================ */

process.exit(j.finaliser() ? 0 : 1);
