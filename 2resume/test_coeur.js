/* ============================================================================
   2resume — LES TESTS DU NOYAU
   ----------------------------------------------------------------------------
   Le noyau est pur, donc testable sans DOM, sans fichier, sans réseau.
   Les valeurs attendues sont écrites À LA MAIN : c'est le seul moyen de savoir
   si la formule calcule ce qu'on croit. Le jeu JEUX (donnees.js) sert de
   structure ; les cas limites sont fabriqués exprès.
   Exécution : node test_coeur.js
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

const src = fs.readFileSync(path.join(__dirname, "coeur.js"), "utf8")
  + "\n" + fs.readFileSync(path.join(__dirname, "donnees.js"), "utf8");
const N = new Function(src + "\nreturn { nb, pos, fmt, fmtEuro, fmtEnt, pct, dispo, codeDeOp, familleDeLigne, rangLigne, codeLigneDe, encreDe, scenarioDeProd, coutLogement, motifLogement, cppParLogement, cppOutillageOutil, cppOutillageScenario, outillageDeScenario, cppEssai, tauxHoraire, cycleSecondes, coutMachinePiece, coutRebut, coutPieces, coutsDetail, perimetreCommun, deltaCouts, volumeAnnuel, cheminCPP, battDe, seuilBattement, conforme, conformeRa, conformeEssai, charniereVisee, suiviEssai, statutEssai, statutScenario, postesDeLigne, cppReference, tuileDeLigne, tuilesDeLignes, verdictPoste, decisionPoste, verdictLigne, recapLignes, santeDonnees, essaisDuScenario, postesAvecEssais, sommeGains, SEUILS, COUT_POSTES, STATUTS, RANG_LIGNES };")();

console.log("\n── LES PRIMITIVES : une absence n'est jamais un zéro ──");
ok("nb('') est une absence", N.nb(""), null);
ok("nb(null) est une absence", N.nb(null), null);
ok("nb(undefined) est une absence", N.nb(undefined), null);
ok("nb('abc') est une absence", N.nb("abc"), null);
ok("nb(0) est un nombre, PAS une absence", N.nb(0), 0);
ok("nb('0') est un nombre", N.nb("0"), 0);
ok("nb(true) est refusé", N.nb(true), null);
ok("pos(0) n'est pas positif", N.pos(0), null);
ok("pos(-3) n'est pas positif", N.pos(-3), null);
ok("pos('7') est positif", N.pos("7"), 7);
ok("fmt d'une absence", N.fmt(null), "—");
ok("fmt d'un nombre", N.fmt(0.0875, 4), "0,0875");
ok("l'arrondi est DÉCIMAL : 3,5/80 = 0,04375 s'affiche 0,0438 (vu par le juge visuel)",
   N.fmt(3.5 / 80, 4), "0,0438");
ok("et une valeur vraiment sous la frontière ne bouge pas", N.fmt(0.043749, 4), "0,0437");
ok("fmtEuro", N.fmtEuro(0.0875, 4), "0,0875 €");
ok("fmtEnt formate les milliers (espace fine ou insécable)", /^\d{3}[\s\u202F\u00A0]\d{3}$/.test(N.fmtEnt(148942)), true);
ok("dispo dit POURQUOI ça manque", N.dispo("", 2, "— prix non saisi"), "— prix non saisi");
ok("dispo affiche la valeur quand elle existe", N.dispo(12, 0), "12");

console.log("\n── LE CODE D'OPÉRATION : le nom de l'atelier gagne ──");
ok("un nom simple", N.codeDeOp({ nom: "OP10" }), "OP10");
ok("un nom libre « OP 30 Perçages »", N.codeDeOp({ nom: "OP 30 Perçages" }), "OP30");
ok("un nom avec suffixe « OP10 Ebauche piste »", N.codeDeOp({ nom: "OP10 Ebauche piste" }), "OP10");
ok("le nom PRIME sur l'ordre — panne mesurée sur l'export réel", N.codeDeOp({ nom: "OP40 Finition Pistes", ordre: 30 }), "OP40");
ok("un nom sans numéro retombe sur l'ordre", N.codeDeOp({ nom: "Ebauche", ordre: 20 }), "OP20");
ok("rien de tout ça : le nom entier", N.codeDeOp({ nom: "Perçage" }), "Perçage");

console.log("\n── LE RÉFÉRENTIEL DES LIGNES ──");
ok("famille EMAG", N.familleDeLigne("EMAG 1"), "emag");
ok("famille Hessapp, casse ignorée", N.familleDeLigne("hessapp"), "hessapp");
ok("famille inconnue", N.familleDeLigne("Mazak X"), "");
ok("PCI 5 existe dans le rang — le proto s'était arrêté à PCI 4", N.RANG_LIGNES.indexOf("pci 5") >= 0, true);
ok("rang Weisser 2 avant Hessapp", N.rangLigne("WEISSER 2") < N.rangLigne("HESSAPP"), true);
ok("une ligne inconnue passe en queue", N.rangLigne("Mazak X"), N.RANG_LIGNES.length);
ok("code ligne EMAG 2", N.codeLigneDe("EMAG 2"), "E2");
ok("code ligne Hessapp", N.codeLigneDe("HESSAPP"), "HESSAPP");
ok("code ligne PCI 5", N.codeLigneDe("PCI 5"), "P5");
ok("les codes de statut sont en ASCII", N.STATUTS.every(s => /^[]?[a-z]+$/.test(s)), true);

console.log("\n── LE SCÉNARIO DE PRODUCTION : une seule règle, un seul appel ──");
ok("le baseline gagne", N.scenarioDeProd([{ id: "a", baseline: false }, { id: "b", baseline: true }]).id, "b");
ok("sinon le statut série", N.scenarioDeProd([{ id: "a", statut: "essai" }, { id: "b", statut: "serie" }]).id, "b");
ok("sinon le nom « base excel »", N.scenarioDeProd([{ id: "a", name: "Prod actuelle (base excel 2026)" }]).id, "a");
ok("sinon rien", N.scenarioDeProd([{ id: "a", name: "Essai" }]), null);
ok("liste vide", N.scenarioDeProd([]), null);

console.log("\n── LE CPP OUTILLAGE : LE point de calcul ──");
ok("7 € ÷ (2 arêtes × 40 pièces)", N.coutLogement({ prix: 7, aretes: 2, charniere: 40 }), 0.0875, 1e-12);
ok("un prix manquant rend le logement NON CHIFFRABLE, pas gratuit", N.coutLogement({ prix: "", aretes: 2, charniere: 40 }), null);
ok("un prix à zéro n'est pas un coût", N.coutLogement({ prix: 0, aretes: 2, charniere: 40 }), null);
ok("des arêtes manquantes", N.coutLogement({ prix: 7, aretes: "", charniere: 40 }), null);
ok("une charnière manquante", N.coutLogement({ prix: 7, aretes: 2, charniere: null }), null);
ok("le motif dit ce qui manque", N.motifLogement({ prix: "", aretes: 2, charniere: 40 }), "prix non saisi");
ok("le motif des arêtes", N.motifLogement({ prix: 7, aretes: 0, charniere: 40 }), "nombre d'arêtes non saisi");
ok("un logement absent", N.coutLogement(null), null);

console.log("\n── LA DÉCOMPOSITION : la somme des logements EST le CPP du scénario ──");
const jp1 = N.JEUX_faux || null; /* pas de jeu ici : les structures viennent de donnees.js */
const seed = new Function(src + "\nreturn JEUX;")();
const emag1 = seed.lignes.find(l => l.nom === "EMAG 1");
const op10 = emag1.references[0].ops.find(o => o.ordre === 10 || o.nom === "OP10");
const prod = N.scenarioDeProd(op10.scenarios);
const out = N.outillageDeScenario(prod);
ok("le scénario de production d'EMAG 1 OP10 existe", !!prod, true);
ok("deux logements sur l'outil", out.outils[0].logements.length, 2);
ok("CPP du scénario = somme des deux logements (7€/2×40 ×2)", N.cppOutillageScenario(prod), 0.175, 1e-12);
ok("le CPP de l'outil est la moitié", N.cppOutillageOutil(prod.outils[0]), 0.175, 1e-12);
ok("la décomposition retombe EXACTEMENT sur le total",
   out.outils.reduce((a, o) => a + (o.cpp || 0), 0), N.cppOutillageScenario(prod), 1e-12);
ok("aucun logement non chiffrable ici", out.nonChiffrables, 0);
ok("cppParLogement porte prix, arêtes, charnière",
   N.cppParLogement(prod)[0].prix, 7);

console.log("\n── LE CPP OBTENU PAR ESSAI : prévu contre réel ──");
const essaiSc = op10.scenarios.find(s => s !== prod);
const obt = N.cppEssai(op10.scenarios.find(s => s.id !== prod.id), null);
ok("un essai absent ne donne rien", obt.cpp, null);
const jp2 = essaiSc;
const essai = jp2.essais[0];
const obt2 = N.cppEssai(jp2, essai);
ok("le CPP prévu de l'essai est celui du scénario", obt2.prevu, 0.0875, 1e-12);
ok("le CPP OBTENU vient de la charnière mesurée (40 p, même formule)", obt2.cpp, 0.0875, 1e-12);
ok("et l'écart prévu/obtenu est zéro ici", obt2.ecart, 0, 1e-12);
const essaiMoitie = JSON.parse(JSON.stringify(essai));
essaiMoitie.params.logements.forEach(l => { l.charniere = 80; });
ok("charnière doublée ⇒ CPP obtenu MOITIÉ (la mesure porte)",
   N.cppEssai(jp2, essaiMoitie).cpp, 0.04375, 1e-12);
const essaiTrou = JSON.parse(JSON.stringify(essai));
essaiTrou.params.logements[1].charniere = "";
const scTrou = JSON.parse(JSON.stringify(jp2));
scTrou.outils[0].logements[1].charniere = "";
ok("un logement sans charnière NULLE PART est ÉCARTÉ et compté, jamais inventé",
   [N.cppEssai(scTrou, essaiTrou).cpp, N.cppEssai(scTrou, essaiTrou).nonChiffrables], [0.04375, 1], 1e-12);
const essaiVideSeul = JSON.parse(JSON.stringify(essai));
essaiVideSeul.params.logements[1].charniere = "";
ok("une charnière d'essai vide retombe sur la DÉFINITION du scénario (40 p)",
   N.cppEssai(jp2, essaiVideSeul).cpp, 0.0875, 1e-12);

console.log("\n── LES AXES NON COMPARABLES : déclarés, jamais mélangés ──");
const cfg = { cycleSecActif: true, cycleRefSec: 42, partCoupante: 100, coutRebutActif: true, coutDisque: 20, tauxRebutAnnuel: 2 };
const ligneRiche = { nom: "EMAG 1", coutHoraire: 60 };
const prodCycle = Object.assign({}, prod, { cycle: 100 });
const det = N.coutsDetail(prodCycle, ligneRiche, cfg);
ok("plaquettes chiffrables", det.postes.plaquettes, 0.175, 1e-12);
ok("temps = 60/3600 × 42 s × 100 %", det.postes.temps, 0.7, 1e-12);
ok("rebut = 20 € × 2 %", det.postes.rebut, 0.4, 1e-12);
ok("pièces détachées : rien de saisi, poste déclaré", det.postes.pieces, null);
ok("le total n'existe que si AU MOINS un poste est chiffré", det.total, 1.275, 1e-12);
ok("les manquants sont nommés", det.manquants, ["pieces"]);
ok("un scénario SANS indice de cycle n'invente pas de temps",
   N.coutsDetail(prod, ligneRiche, cfg).manque.temps, "temps de cycle non saisi");
const detNu = N.coutsDetail(prod, { nom: "EMAG 1", coutHoraire: "" }, {});
ok("sans taux ni cycle, le temps est non chiffrable AVEC sa raison",
   [detNu.postes.temps, detNu.manque.temps], [null, "taux horaire de ligne non saisi"]);
ok("un indice sans conversion n'est pas un temps",
   N.cycleSecondes({ cycle: 100 }, { cycleSecActif: false }), null);
ok("l'indice convertit quand la conversion est demandée",
   N.cycleSecondes({ cycle: 183.7 }, { cycleSecActif: true, cycleRefSec: 42 }), 77.154, 0.001);

console.log("\n── LE PÉRIMÈTRE COMMUN : on ne compare que le comparable ──");
const a = { postes: { plaquettes: 0.175, temps: 0.7, rebut: null, pieces: null } };
const b = { postes: { plaquettes: 0.0875, temps: null, rebut: null, pieces: null } };
ok("côté classeur : seul « plaquettes » se compare", N.perimetreCommun(a, b, true), ["plaquettes"]);
ok("l'écart se calcule sur CE périmètre", N.deltaCouts(a, b, true).ecart, -0.0875, 1e-12);
ok("et il est déclaré comparable", N.deltaCouts(a, b, true).comparable, true);
const c = { postes: { plaquettes: null, temps: null, rebut: null, pieces: null } };
ok("rien de commun ⇒ non comparable, avec la raison",
   [N.deltaCouts(a, c, true).comparable, N.deltaCouts(a, c, true).motif.length > 0], [false, true]);

console.log("\n── LE VOLUME ANNUEL : la source est nommée ──");
ok("volume de la référence", N.volumeAnnuel({ productionAnnuelle: 148942 }, {}).source, "référence");
ok("repli sur le volume de l'opération", N.volumeAnnuel({ productionAnnuelle: "" }, { config: { volumeAnnuel: 2490 } }).source, "opération");
ok("les deux vides : pas de gain annuel, et c'est dit",
   N.volumeAnnuel({ productionAnnuelle: "" }, { config: {} }).valeur, null);
ok("divergence détectée", N.volumeAnnuel({ productionAnnuelle: 100 }, { config: { volumeAnnuel: 200 } }).divergent, true);

console.log("\n── LE CHEMIN VERS LA CIBLE : borné, jamais embellie ──");
ok("un chemin partiel", N.cheminCPP(0.2, 0.1, 0.05), 66.6667, 0.001);
ok("déjà sous la cible : chemin fait, 100 %", N.cheminCPP(0.04, 0.03, 0.05), 100);
ok("un gain au-delà de la cible sature à 100 %", N.cheminCPP(0.2, 0.01, 0.05), 100);
ok("rien du tout : 0 %", N.cheminCPP(0.2, 0.2, 0.05), 0);
ok("cible absente : pas de chemin", N.cheminCPP(0.2, 0.1, null), null);
ok("production absente : pas de chemin", N.cheminCPP(null, 0.1, 0.05), null);

console.log("\n── LE PIRE DES DEUX CÔTÉS : le pont batt D/G ──");
ok("batt seul", N.battDe({ batt: 0.05 }), 0.05);
ok("batt vide, D et G : LE PIRE, jamais la moyenne", N.battDe({ batt: "", battD: 0.08, battG: 0.14 }), 0.14);
ok("D seul", N.battDe({ battD: 0.06 }), 0.06);
ok("G seul", N.battDe({ battG: 0.09 }), 0.09);
ok("rien : non mesurable (NaN), jamais 0", Number.isNaN(N.battDe({ batt: "", battD: "", battG: "" })), true);
ok("un prélèvement absent", Number.isNaN(N.battDe(null)), true);

console.log("\n── LA CONFORMITÉ : trois états, l'absence ne condamne pas ──");
ok("sous le seuil : conforme", N.conforme({}, { batt: 0.05 }), true);
ok("au-dessus : non conforme", N.conforme({}, { batt: 0.5 }), false);
ok("sans mesure : NULL — un oubli de saisie ne fait pas échouer un essai", N.conforme({}, { batt: "" }), null);
ok("le seuil par défaut du site", N.seuilBattement({}), 0.12, 1e-12);
ok("le seuil surchargé du scénario", N.seuilBattement({ limitOverride: true, limitValue: 0.04 }), 0.04, 1e-12);
ok("critère désactivé : rien à juger", N.conforme({ battActif: false }, { batt: 9 }), true);
ok("le pire côté décide : D bon, G mauvais ⇒ NON conforme",
   N.conforme({}, { batt: "", battD: 0.05, battG: 0.5 }), false);
ok("Ra : sans critère actif, rien à juger", N.conformeRa({}, { valeur2: 12 }), true);
ok("Ra : au-dessus du seuil actif", N.conformeRa({ critere2: { actif: true, valeur: 0.8 } }, { valeur2: 12 }), false);
ok("Ra : sans mesure, null", N.conformeRa({ critere2: { actif: true, valeur: 0.8 } }, { valeur2: "" }), null);

console.log("\n── LA PREUVE : la charnière atteinte, logement par logement ──");
const scCharn = { outils: [{ id: "o1", logements: [{ id: "l1", charniere: 30 }, { id: "l2", charniere: 50 }] }] };
const essaiCharn = {
  params: { logements: [{ logementId: "l1", logementNom: "D1", charniere: 30 }, { logementId: "l2", logementNom: "D2", charniere: 50 }] },
  prelevements: [
    { piece: 10, logementId: "l1", batt: 0.05 },
    { piece: 30, logementId: "l1", batt: 0.06 },
    { piece: 20, logementId: "l2", batt: 0.05 }
  ]
};
const su = N.suiviEssai(scCharn, essaiCharn);
ok("D1 lu à sa dernière pièce (30, pas 10)", su.find(x => x.logementId === "l1").atteint, 30);
ok("D1 a atteint sa charnière", su.find(x => x.logementId === "l1").fait, true);
ok("D2 non atteinte (20/50)", su.find(x => x.logementId === "l2").fait, false);
ok("le repli sur la charnière du scénario marche",
   N.charniereVisee(scCharn, { params: { logements: [] } }, "l2"), 50);

console.log("\n── LE STATUT D'UN ESSAI : une hiérarchie ordonnée, pas un score ──");
ok("arrêté d'abord", N.statutEssai({}, { cloture: { motif: "casse" }, prelevements: [] }).code, "arrete");
ok("le motif est traduit en français d'atelier", N.statutEssai({}, { cloture: { motif: "casse" }, prelevements: [] }).texte, "arrêté — casse / éclat d'arête");
ok("hors tolérance ensuite", N.statutEssai({}, { prelevements: [{ batt: 0.5 }] }).code, "nonconforme");
ok("la pièce fautive est nommée", N.statutEssai({}, { prelevements: [{ piece: 15, batt: 0.5 }] }).piece, 15);
ok("charnière en cours ensuite", N.statutEssai(scCharn, essaiCharn).code, "encours");
ok("le détail du reste à parcourir ne montre que ce qui reste", N.statutEssai(scCharn, essaiCharn).texte, "D2 20/50 p");
ok("mesures à saisir ensuite — un battement non mesuré N'EST PAS conforme, même Ra inactif",
   N.statutEssai({}, { prelevements: [{ batt: "", battD: "", battG: "" }] }).code, "attente");
ok("conforme enfin", N.statutEssai(scCharn, {
  params: { logements: [{ logementId: "l1", logementNom: "D1", charniere: 30 }] },
  prelevements: [{ piece: 30, logementId: "l1", batt: 0.05 }]
}).code, "conforme");
ok("un essai vide", N.statutEssai({}, null).code, "vide");

console.log("\n── LE STATUT D'UN SCÉNARIO : le protocole du site, 5 preuves ──");
ok("en production", N.statutScenario({ statut: "serie" }).code, "serie");
ok("abandonné", N.statutScenario({ statut: "abandonne" }).code, "abandonne");
ok("rien du tout", N.statutScenario({ essais: [] }).code, "rien");
const conf = p => ({ params: { logements: [{ logementId: "l1", logementNom: "D1", charniere: 30 }] }, prelevements: [{ piece: 30, logementId: "l1", batt: 0.05 }] });
ok("4 conformes ne valident pas", N.statutScenario({ essais: [conf(), conf(), conf(), conf()] }).code, "encours");
ok("et le compte est dit", N.statutScenario({ essais: [conf(), conf(), conf(), conf()] }).texte, "4/5 validés");
ok("5 conformes : décision à prendre", N.statutScenario({ essais: [conf(), conf(), conf(), conf(), conf()] }).code, "pret");
ok("le seuil est lisible dans les données",
   N.statutScenario({ essais: [conf(), conf()], validationThreshold: 2 }).code, "pret");

console.log("\n── LE VERDICT : un mot par poste, avec sa raison ──");
const vlEmag = N.verdictLigne(emag1);
const vOp10 = vlEmag.postes.find(v => v.nomOp === "OP10");
ok("le poste OP10 d'EMAG 1 est un gain projeté", vOp10.code, "essai");
ok("son gain : 0,175 − 0,0875", vOp10.gainProjete, 0.0875, 1e-12);
ok("le volume manque dans le jeu : pas de gain annuel inventé", vOp10.gainProjeteAnnuel, null);
ok("le chemin est fait (coût déjà sous la cible)", vOp10.chemin, 100);
ok("la décision dit « ESSAYER »", N.decisionPoste(vOp10).mot, "ESSAYER");
ok("et pourquoi", N.decisionPoste(vOp10).pourquoi.indexOf("0,0875") >= 0, true);
const emag3 = seed.lignes.find(l => l.nom === "EMAG 3");
const vRien = N.verdictLigne(emag3).postes[0];
ok("un poste sans alternative : RIEN, et la raison", [vRien.code, vRien.verdict], ["rien", "aucun essai ne fait mieux que la production"]);
const pci4 = seed.lignes.find(l => l.nom === "PCI 4");
const vChiffrer = N.verdictLigne(pci4).postes[0];
ok("un poste non chiffrable reste visible : CHIFFRER", N.decisionPoste(vChiffrer).mot, "CHIFFRER");
ok("avec la raison exacte", vChiffrer.verdict, "cible connue, coût à chiffrer");
ok("« rien » ne se transforme pas en 0", N.sommeGains(N.verdictLigne(emag3).postes, "gainProjete"), null);

console.log("\n── LES GAINS : acté et projeté ne se fusionnent jamais ──");
const rec = N.recapLignes([N.verdictLigne(emag1), N.verdictLigne(emag3), N.verdictLigne(pci4)]);
ok("le gain projeté du jeu", rec.cppProjete, 0.0875, 1e-12);
ok("rien d'acté dans le jeu", rec.cppActe, 0);
ok("un poste à chiffrer (PCI 4) ET un poste sans production (EMAG 3 OP20)", rec.aChiffrer, 2);
ok("une décision en attente (EMAG 1 OP10)", rec.decisions, 1);
ok("cinq postes suivis", rec.postes, 5);

console.log("\n── LES TUILES : l'ordre de l'atelier ──");
const tuiles = N.tuilesDeLignes(seed.lignes);
ok("l'ordre est celui du rang déclaré", tuiles.map(t => t.nom), ["EMAG 1", "EMAG 3", "PCI 4"]);
ok("EMAG 1 est chiffrée", tuiles[0].cpp !== null, true);
ok("la dominante est une référence de la ligne", tuiles[0].dominante.ref.id, emag1.references[0].id);
ok("une ligne sans référence est déclarée vide", tuiles.find(t => t.nom === "PCI 4").vide, false);

console.log("\n── LA SANTÉ DES DONNÉES : les trous comptés et nommés ──");
const sante = N.santeDonnees({ lignes: seed.lignes });
ok("trois lignes", sante.lignes, 3);
ok("un poste sans production (EMAG 3 OP20)", sante.sansProd, 1);
ok("un logement non chiffrable (PCI 4, prix manquant)", sante.nonChiffrables, 1);
ok("tous les MABEC du jeu sont vides — et comptés", sante.sansMabec, 7);
ok("trois références sans volume annuel", sante.referencesSansVolume, 3);
ok("aucune référence sans cible dans le jeu", sante.referencesSansCible, 0);
const santeVide = N.santeDonnees(null);
ok("un état absent ne fait pas planter la santé", santeVide.lignes, 0);

console.log("\n── LES PORTES DU CAHIER (§6, invariants) ──");
ok("le CPP du scénario est la somme de sa décomposition sur le jeu complet",
   (() => { let bon = true;
     seed.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(op => op.scenarios.forEach(sc => {
       const o = N.outillageDeScenario(sc), s = N.cppOutillageScenario(sc);
       if ((o.cpp === null) !== (s === null)) bon = false;
       else if (o.cpp !== null && Math.abs(o.cpp - s) > 1e-9) bon = false;
     }))));
     return bon; })(), true);
ok("postesAvecEssais voit l'essai du jeu", N.postesAvecEssais(emag1).length, 1);

console.log("\n" + total + " tests exécutés, " + echecs + " échec(s)");
if (echecs) { console.log("ROUGE — " + echecs + " échec(s)"); process.exit(1); }
console.log("TOUT EST VERT");
