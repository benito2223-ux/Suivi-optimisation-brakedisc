/* ============================================================================
   2resume — LA PROJECTION
   ----------------------------------------------------------------------------
   Transformer un export de l'ancienne application (formats 1 à 8) en données
   de CET outil, et normaliser des données qui viennent d'ailleurs.

   Le principe est une LISTE BLANCHE : chaque objet est reconstruit champ par
   champ. `garder` est plus sûr que lister ce qu'on jette — un champ ajouté par
   une version future de l'app ne peut pas se glisser dans la projection.

   Ce qui n'est pas conservé est COMPTÉ et affiché. Un import qui jette en
   silence laisse croire que rien n'a été perdu ; un import qui compte ce qu'il
   jette est un import honnête.
   ========================================================================== */

const IMPORT_VERSION = "1.0";

/* Ce que la projection laisse volontairement derrière. Déclaré en dur, jamais
   inspecté — c'est un choix, et il doit se lire dans l'écran. */
const ABANDONS = [
  "plans de porte-outil (géométrie, 320 à 370 Ko par outil)",
  "photos d'essai et leurs annotations",
  "relevés Marposs (1 340 points sur un seul essai)",
  "journal de rebut",
  "fiche outil PDF",
  "carnet de sujets (backlog)"
];

/* Les marques d'ISO qu'on connaît. Sert à distinguer une référence de
   plaquette (« SNGN 090416-F ») d'un MABEC (« IM02 137 021 ») quand l'export
   ancien les a mélangés dans la même colonne. Une liste courte et déclarée
   vaut mieux qu'une regex élégante qui se trompe en silence. */
const MARQUES_ISO = ["SNGN", "SNMG", "CCMT", "CCMA", "CNMG", "CNMA", "KY", "KQ", "VB", "RCMT", "RCMX", "TCMT", "TPGT", "VBGT", "WNMG"];

function texteOuVide(v) {
  return (v === null || v === undefined) ? "" : String(v);
}
function nombreOuVide(v) {
  if (v === null || v === undefined || v === "") return "";
  const n = parseFloat(v);
  return isNaN(n) ? "" : n;
}
function booleen(v) {
  return v === true;
}

/* Un identifiant stable : on garde celui de l'export quand il existe, sinon on
   en fabrique un. Deux imports du même fichier donnent le même résultat — le
   déterminisme est testé, parce qu'un identifiant aléatoire ferait qu'une
   relecture du même export ne référence pas les mêmes logements. */
let _compteurId = 0;
function idFiable(brut, prefixe) {
  const s = brut && brut.id ? String(brut.id) : "";
  if (s) return s;
  _compteurId++;
  return prefixe + "_" + _compteurId.toString(36) + Date.now().toString(36).slice(-4);
}

/* ── Le classement d'un article ───────────────────────────────────────────── */

function classerArticle(brut) {
  const s = texteOuVide(brut && (brut.mabec || brut.codeArticle)).trim();
  const ref = texteOuVide(brut && brut.ref).trim();
  const isoExplicite = texteOuVide(brut && brut.iso).trim();
  let mabec = "", iso = "", devine = "";
  if (s) { mabec = s; }
  if (ref) {
    const maj = ref.toUpperCase();
    if (MARQUES_ISO.some(m => maj.indexOf(m) === 0)) { iso = ref; }
    else if (/^[A-Z]{1,4}\s*\d{3}/.test(maj) && !mabec) { mabec = ref; devine = "mabec"; }
    else { iso = ref; }
  }
  if (isoExplicite) iso = isoExplicite;
  return { mabec: mabec, iso: iso, devine: devine };
}

/* ── La projection objet par objet ───────────────────────────────────────── */

function garder(brut, liste) {
  const out = {};
  if (!brut) return out;
  liste.forEach(k => { if (brut[k] !== undefined) out[k] = brut[k]; });
  return out;
}

function projeterLogement(b, r) {
  const art = classerArticle(b);
  if (!b.mabec && !b.codeArticle && art.devine === "mabec") r.mabecDevines++;
  if (!art.mabec) r.sansMabec++;
  const prix = nombreOuVide(b.prix);
  const aretes = nombreOuVide(b.aretes);
  const charniere = nombreOuVide(b.charniere);
  if (!(parseFloat(prix) > 0)) r.sansPrix++;
  if (!(parseFloat(aretes) > 0)) r.sansAretes++;
  if (!(parseFloat(charniere) > 0)) r.sansCharniere++;
  r.logements++;
  return {
    id: idFiable(b, "lg"),
    nom: texteOuVide(b.nom) || "?",
    mabec: art.mabec,
    iso: art.iso,
    prix: prix, aretes: aretes, charniere: charniere,
    vc: nombreOuVide(b.vc), f: nombreOuVide(b.f),
    apPiste: nombreOuVide(b.apPiste),
    tempsCoupe: nombreOuVide(b.tempsCoupe),
    tempsDeplacement: nombreOuVide(b.tempsDeplacement),
    suiviTolerance: booleen(b.suiviTolerance)
  };
}

function projeterOutil(b, r) {
  r.outils++;
  if (!b.numero) r.outilsSansNumero++;
  return {
    id: idFiable(b, "ot"),
    numero: texteOuVide(b.numero) || "?",
    description: texteOuVide(b.description),
    correcteur: texteOuVide(b.correcteur),
    simultaneAvecPrecedent: booleen(b.simultaneAvecPrecedent) || booleen(b.outilsParalleles),
    logements: (b.logements || []).map(l => projeterLogement(l, r)),
    pieces: (b.pieces || []).map(p => ({
      id: idFiable(p, "pc"), nom: texteOuVide(p.nom),
      ref: texteOuVide(p.ref), prix: nombreOuVide(p.prix), charniere: nombreOuVide(p.charniere)
    }))
  };
}

function projeterPrelevement(b, r) {
  r.prelevements++;
  if (nb(b.batt) === null && nb(b.battD) === null && nb(b.battG) === null) r.sansBatt++;
  return {
    id: idFiable(b, "pr"),
    piece: nombreOuVide(b.piece),
    logementId: texteOuVide(b.logementId),
    pointMesure: texteOuVide(b.pointMesure),
    batt: nombreOuVide(b.batt),
    battD: nombreOuVide(b.battD),
    battG: nombreOuVide(b.battG),
    usure: texteOuVide(b.usure),
    valeur2: nombreOuVide(b.valeur2)
  };
}

function projeterEssai(b, sc, r) {
  r.essais++;
  return {
    id: idFiable(b, "es"),
    titre: texteOuVide(b.titre),
    date: texteOuVide(b.date),
    operateur: texteOuVide(b.operateur),
    equipe: texteOuVide(b.equipe),
    but: texteOuVide(b.but),
    observations: texteOuVide(b.observations),
    cloture: b.cloture ? { date: texteOuVide(b.cloture.date), motif: texteOuVide(b.cloture.motif),
                          detail: texteOuVide(b.cloture.detail) } : null,
    params: { logements: ((b.params && b.params.logements) || []).map(p => ({
      logementId: texteOuVide(p.logementId),
      logementNom: texteOuVide(p.logementNom),
      outilNumero: texteOuVide(p.outilNumero),
      charniere: nombreOuVide(p.charniere)
    })) },
    prelevements: (b.prelevements || []).map(p => projeterPrelevement(p, r))
  };
}

function projeterScenario(b, r) {
  r.scenarios++;
  /* La règle de l'app d'origine est reprise telle quelle : un scénario baseline
     EST en production. Les données réelles contiennent des cas où les deux se
     contredisent (baseline vrai, statut « essai ») — on tranche du côté de la
     production, sinon le poste paraît sans production alors qu'il tourne. */
  const statutLu = STATUTS.indexOf(b.statut) >= 0 ? b.statut : "essai";
  return {
    id: idFiable(b, "sc"),
    name: texteOuVide(b.name || b.nom) || "Scénario",
    baseline: b.baseline === true,
    statut: b.baseline === true ? "serie" : statutLu,
    statutMotif: texteOuVide(b.statutMotif),
    statutDate: texteOuVide(b.statutDate),
    emag1: booleen(b.emag1),
    battActif: b.battActif === false ? false : true,
    limitOverride: booleen(b.limitOverride),
    limitValue: nombreOuVide(b.limitValue) || SEUILS.battementDefaut,
    critere2: { actif: booleen(b.critere2Actif),
                label: texteOuVide(b.limitLabel2) || "Ra (µm)",
                valeur: nombreOuVide(b.limitValue2) || SEUILS.raDefaut },
    validationThreshold: nombreOuVide(b.validationThreshold) || SEUILS.validations,
    outils: (b.outils || []).map(o => projeterOutil(o, r)),
    essais: (b.essais || []).map(e => projeterEssai(e, b, r))
  };
}

function projeterOp(b, r) {
  r.ops++;
  return {
    id: idFiable(b, "op"),
    nom: texteOuVide(b.nom),
    code: texteOuVide(b.code) || codeDeOp(b),
    ordre: nombreOuVide(b.ordre),
    config: {
      limitLabel: texteOuVide(b.config && b.config.limitLabel) || "Battement (mm)",
      limitValue: nombreOuVide(b.config && b.config.limitValue) || SEUILS.battementDefaut,
      cycleSecActif: b.config && b.config.cycleSecActif === true,
      cycleRefSec: nombreOuVide(b.config && b.config.cycleRefSec),
      coutMachineActif: b.config && b.config.coutMachineActif === true,
      partCoupante: nombreOuVide(b.config && b.config.partCoupante) || SEUILS.partCoupante,
      coutRebutActif: b.config && b.config.coutRebutActif === true,
      coutDisque: nombreOuVide(b.config && b.config.coutDisque),
      tauxRebutAnnuel: nombreOuVide(b.tauxRebutAnnuel),
      volumeAnnuel: nombreOuVide(b.config && b.config.volumeAnnuel),
      ecartCharniereTolerance: nombreOuVide(b.config && b.config.ecartCharniereTolerance) || SEUILS.ecartCharniere
    },
    scenarios: (b.scenarios || []).map(s => projeterScenario(s, r))
  };
}

function projeterReference(b, r) {
  r.references++;
  const cible = nombreOuVide(b.cibleCPP);
  if (!(parseFloat(cible) > 0)) r.sansCible++;
  const volume = nombreOuVide(b.productionAnnuelle);
  if (!(parseFloat(volume) > 0)) r.sansVolume++;
  return {
    id: idFiable(b, "rf"),
    nom: texteOuVide(b.nom) || "Référence",
    cibleCPP: cible,
    productionAnnuelle: volume,
    ops: (b.ops || []).map(o => projeterOp(o, r))
  };
}

function projeterLigne(b, r) {
  r.lignes++;
  const refs = b.references || [];
  if (!refs.length) r.sansReference++;
  return {
    id: idFiable(b, "lg1"),
    nom: texteOuVide(b.nom) || "Ligne",
    coutHoraire: nombreOuVide(b.coutHoraire),
    observations: texteOuVide(b.observations),
    references: refs.map(x => projeterReference(x, r))
  };
}

/* ── Les racines acceptées ───────────────────────────────────────────────── */

/* Le format 6 avait le projet AU-DESSUS de la machine : Projet → Ligne →
   Référence. Il a été retiré en production. On l'accepte quand même, en
   aplatissant, et on le dit — aplatir perd le rattachement au projet, donc
   l'écran ne montrera aucun projet pour ces données. */
function racinesLignes(source) {
  if (Array.isArray(source.lignes) && source.lignes.length) return { lignes: source.lignes, forme: "lignes" };
  if (Array.isArray(source.projets) && source.projets.length
      && Array.isArray(source.projets[0].lignes) && source.projets[0].lignes.length) {
    const plat = [];
    source.projets.forEach(pj => (pj.lignes || []).forEach(l => plat.push(l)));
    return { lignes: plat, forme: "projets" };
  }
  return null;
}

function rapportVierge() {
  return {
    lignes: 0, references: 0, ops: 0, scenarios: 0, outils: 0, logements: 0,
    essais: 0, prelevements: 0,
    sansReference: 0, sansCible: 0, sansVolume: 0,
    sansPrix: 0, sansAretes: 0, sansCharniere: 0,
    sansMabec: 0, mabecDevines: 0, sansBatt: 0, outilsSansNumero: 0,
    postesSansProd: 0,
    abandons: ABANDONS.slice(),
    avertissements: []
  };
}

/* ── Le point d'entrée ───────────────────────────────────────────────────── */

function projeter(source) {
  const echec = { ok: false, erreur: "Ce fichier n'est pas un export du suivi d'optimisation." };
  if (!source || typeof source !== "object") return echec;
  const racines = racinesLignes(source);
  if (!racines) return echec;

  const r = rapportVierge();
  const lignes = racines.lignes.map(l => projeterLigne(l, r));

  /* Les postes sans scénario de production : ils restent visibles, marqués.
     Compter ici, et non à l'écran, évite qu'une ligne paraisse complète. */
  lignes.forEach(l => (l.references || []).forEach(rf => (rf.ops || []).forEach(op => {
    if (!scenarioDeProd(op.scenarios)) r.postesSansProd++;
  })));

  if (!r.essais) r.avertissements.push(
    "Aucun essai dans cet export : les écrans de preuve resteront vides.");
  if (r.sansPrix || r.sansAretes || r.sansCharniere) r.avertissements.push(
    (r.sansPrix + r.sansAretes + r.sansCharniere) +
    " logement(s) incomplet(s) sur le trio prix / arêtes / charnière : "
    + "ils resteront non chiffrables, et l'écran le dira.");
  if (r.sansBatt) r.avertissements.push(
    r.sansBatt + " prélèvement(s) sans battement ni côté D/G : "
    + "ils n'afficheront aucune conformité.");
  if (r.sansMabec) r.avertissements.push(
    r.sansMabec + " logement(s) sans MABEC : le rapprochement avec le classeur Matis "
    + "ne pourra pas se faire pour eux.");
  if (r.mabecDevines) r.avertissements.push(
    r.mabecDevines + " MABEC lu dans la colonne ISO : vérifiez le classement, "
    + "l'outil ne devine jamais en silence.");
  if (racines.forme === "projets") r.avertissements.push(
    "Ce fichier est au format 6 : les projets ont été aplatis, aucun projet ne sera montré.");
  if (r.postesSansProd) r.avertissements.push(
    r.postesSansProd + " poste(s) sans scénario de production : "
    + "ils restent visibles et le disent.");

  return { ok: true, lignes: lignes, rapport: r, forme: racines.forme };
}

/* ── Le poids jeté ────────────────────────────────────────────────────────── */

function poids(source, projete) {
  let avant = 0, apres = 0;
  try { avant = JSON.stringify(source).length; } catch (e) { avant = 0; }
  try { apres = JSON.stringify(projete).length; } catch (e) { apres = 0; }
  return { avant: avant, apres: apres,
           ratio: avant ? Math.round((apres / avant) * 1000) / 1000 : null };
}

/* ── L'aller-retour complet : ouvrir un ETAT 9 déjà produit par cet outil ─── */

function etatVierge() {
  return {
    format: FORMAT_DONNEES, outil: "Suivi CPP — Sept Fons", version: OUTIL_VERSION,
    exporteLe: "", exportePar: "",
    specsUsine: { battement: SEUILS.battementDefaut, ra: SEUILS.raDefaut },
    lignes: [], projets: [], livraisons: []
  };
}

/* Un export de cet outil est relu par la même projection que n'importe quel
   export ancien : une seule porte d'entrée, donc une seule liste de champs
   qui survit. C'est ce qui garantit qu'un aller-retour ne perd rien. */
function relireEtat(source) {
  const base = etatVierge();
  if (!source || typeof source !== "object") return base;
  base.exporteLe = texteOuVide(source.exporteLe);
  base.exportePar = texteOuVide(source.exportePar);
  const specs = source.specsUsine || {};
  base.specsUsine = {
    battement: nombreOuVide(specs.battement) || SEUILS.battementDefaut,
    ra: nombreOuVide(specs.ra) || SEUILS.raDefaut
  };
  const racines = racinesLignes(source);
  base.lignes = racines ? racines.lignes.map(l => projeterLigne(l, rapportVierge())) : [];
  base.projets = (source.projets || []).map(p => ({
    id: idFiable(p, "pj"), nom: texteOuVide(p.nom), problematique: texteOuVide(p.problematique),
    responsable: texteOuVide(p.responsable), statut: texteOuVide(p.statut) || "encours",
    dateCible: texteOuVide(p.dateCible),
    tags: (p.tags || []).map(t => ({
      ligneId: texteOuVide(t.ligneId), referenceId: texteOuVide(t.referenceId),
      opId: texteOuVide(t.opId), scenarioId: texteOuVide(t.scenarioId)
    }))
  }));
  base.livraisons = (source.livraisons || []).map(lv => ({
    id: idFiable(lv, "lv"), nom: texteOuVide(lv.nom), date: texteOuVide(lv.date),
    creePar: texteOuVide(lv.creePar), gainsActes: nb(lv.gainsActes),
    gainsEnCours: nb(lv.gainsEnCours), protocole: texteOuVide(lv.protocole)
  }));
  return base;
}
