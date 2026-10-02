/* ============================================================================
   PROJET3 — LA MIGRATION ET LA FUSION
   Reprend un export de l'app de production (formats 5, 6, 7 ou 8 — tout ce
   qu'elle a jamais produit) et le normalise vers le format 9 de la v3.

   Contrairement au proto (une projection de 49 Ko), la v3 EST l'outil : la
   migration est SANS PERTE. Photos, plans de porte-outil, relevés Marposs et
   journal de rebut sont conservés — le rapport d'import compte et nomme tout
   ce qui entre.

   Fonctions PURES : elles ne touchent ni au DOM, ni au disque, ni au réseau.
   Elles prennent des objets désérialisés et renvoient des objets — c'est ce
   qui permet de les tester en Node sur les vrais exports du site.
   ========================================================================== */

"use strict";

const IMPORT_VERSION = "1.0";

/* ============================================================================
   1. LA NORMALISATION — formats 5 → 9, sans perte
   ========================================================================== */

/* Les racines acceptées. Formats 5/7/8 : `lignes` à la racine.
   Format 6 : les lignes sont portées par des projets — on les aplatit. */
function racinesLignes(source) {
  if (Array.isArray(source.lignes) && source.lignes.length) return source.lignes;
  if (Array.isArray(source.projets) && source.projets.length
      && Array.isArray(source.projets[0].lignes)) {
    const plat = [];
    source.projets.forEach(pj => (pj.lignes || []).forEach(l => plat.push(l)));
    return plat.length ? plat : null;
  }
  return null;
}

/* Le libellé du scénario : `name` aux formats récents, `nom` aux anciens. */
function nomScenario(sc) {
  return sc.name || sc.nom || "Scénario";
}

/* Les racines de projets acceptées (les anciens formats ont pu les stocker
   ailleurs ; le format 8 les porte à la racine). */
function racinesProjets(source) {
  if (Array.isArray(source.projets)) return source.projets;
  return [];
}

function racinesResponsables(source) {
  if (Array.isArray(source.responsables)) return source.responsables.slice();
  return [];
}

function racinesLivraisons(source) {
  return Array.isArray(source.livraisons) ? source.livraisons : [];
}

function racinesBacklog(source) {
  return Array.isArray(source.backlog) ? source.backlog : [];
}

/* La normalisation d'un état ENTIER. Renvoie { ok, etat, rapport, erreur }.
   Idempotente : normaliser deux fois vaut normaliser une fois (testé). */
function normaliserEtat(source) {
  const vide = {
    ok: false, etat: null, rapport: null,
    erreur: "Ce fichier n'est pas un export du suivi d'optimisation."
  };
  if (!source || typeof source !== "object") return vide;
  const racines = racinesLignes(source);
  if (!racines) return vide;

  const r = {
    formatSource: source.format != null ? source.format : null,
    toolVersion: source.toolVersion || source.version || null,
    exporteLe: source.exporteLe || null,
    exportePar: source.exportePar || null,
    lignes: 0, references: 0, ops: 0, scenarios: 0,
    outils: 0, logements: 0, essais: 0, prelevements: 0,
    photos: 0, marposs: 0, scrapLog: 0, plans: 0,
    projets: 0, etiquettes: 0, responsables: 0, livraisons: 0, backlog: 0,
    responsablesCreés: 0,
    scenariosCibles: 0,
    sansPrix: 0, sansAretes: 0, sansCharniere: 0,
    prelevementsSansBatt: 0,
    avertissements: []
  };

  /* Les responsables existants, indexés par id — les projets migrés peuvent
     en créer. La liste est écrite dans l'état à la fin. */
  const responsables = [];
  const respParId = {};
  racinesResponsables(source).forEach(rb => {
    const rn = normaliserResponsable(rb);
    if (!rn) return;
    if (respParId[rn.id]) return;
    respParId[rn.id] = rn;
    responsables.push(rn);
    r.responsables++;
  });

  /* La migration des anciens projets : un `responsable` en texte libre
     devient une entrée de la liste gérée (CDC Projets v2 §2.1) — chaque
     valeur distincte une fois, couleur assignée dans l'ordre de la palette,
     aucune ressaisie demandée, aucune saisie perdue. */
  function responsableDeTexte(nom, palette) {
    const nomPropre = String(nom || "").trim();
    if (!nomPropre) return "";
    const deja = responsables.find(x => x.nom.toLowerCase() === nomPropre.toLowerCase());
    if (deja) return deja.id;
    const rn = {
      id: "u" + Math.random().toString(36).slice(2, 10),
      nom: nomPropre,
      couleur: palette[responsables.length % palette.length]
    };
    responsables.push(rn);
    r.responsablesCreés++;
    return rn.id;
  }

  const lignes = racines.map((lBrut, iL) => normaliserLigne(lBrut, iL, r));
  r.lignes = lignes.length;
  if (!r.lignes) return vide;

  const projets = racinesProjets(source).map((pBrut, iP) =>
    normaliserProjet(pBrut, iP, r, responsableDeTexte)).filter(Boolean);
  r.projets = projets.length;

  /* Les projets du format 6 portaient leurs lignes : ne pas les réécrire. */
  projets.forEach(pj => { delete pj.lignes; });

  const livraisons = racinesLivraisons(source).slice();
  r.livraisons = livraisons.length;
  const backlog = racinesBacklog(source).slice();
  r.backlog = backlog.length;

  const etat = {
    outil: "SPK Suivi optimisation",
    format: 9,
    toolVersion: source.toolVersion || null,
    revision: source.revision != null ? source.revision : 1,
    exporteLe: null,
    exportePar: "",
    lignes: lignes,
    projets: projets,
    responsables: responsables,
    livraisons: livraisons,
    backlog: backlog,
    activeProjetId: source.activeProjetId || "",
    activeLigneId: source.activeLigneId || (lignes[0] ? lignes[0].id : ""),
    activeReferenceId: source.activeReferenceId || "",
    activeOpId: source.activeOpId || "",
    activeScenarioId: source.activeScenarioId || "",
    modifieLe: source.modifieLe || null
  };

  /* Les avertissements disent ce qui manquera à l'écran — jamais en silence. */
  if (!r.essais) {
    r.avertissements.push("Aucun essai dans cet export : les écrans de preuve et de décision resteront vides.");
  }
  if (!r.scenariosCibles) {
    r.avertissements.push("Aucune cible CPP de site : les distances vers la cible ne pourront pas s'afficher.");
  }
  if (r.sansPrix || r.sansAretes || r.sansCharniere) {
    r.avertissements.push(
      (r.sansPrix + r.sansAretes + r.sansCharniere)
      + " logement(s) incomplet(s) sur le trio prix / arêtes / charnière : ils resteront non chiffrables, et c'est dit à l'écran.");
  }
  if (r.prelevementsSansBatt) {
    r.avertissements.push(
      r.prelevementsSansBatt + " prélèvement(s) sans battement ni côté D/G : ils ne montreront aucune conformité.");
  }
  if (r.responsablesCreés) {
    r.avertissements.push(
      r.responsablesCreés + " responsable(s) créé(s) depuis les anciens champs texte : couleurs assignées automatiquement.");
  }

  return { ok: true, etat: etat, rapport: r, erreur: null };
}

/* ---- ligne ---- */
function normaliserLigne(lBrut, iL, r) {
  const ligne = {
    id: lBrut.id || ("li" + (iL + 1) + "-" + Math.random().toString(36).slice(2, 6)),
    nom: lBrut.nom || "Ligne sans nom",
    coutHoraire: lBrut.coutHoraire != null ? lBrut.coutHoraire : "",
    observations: lBrut.observations || "",
    maintenanceDate: lBrut.maintenanceDate || "",
    maintenanceType: lBrut.maintenanceType || "",
    references: (lBrut.references || []).map((refBrut, iR) => normaliserReference(refBrut, iR, r))
  };
  return ligne;
}

function normaliserReference(refBrut, iR, r) {
  r.references++;
  const cible = (refBrut.cibleCPP === "" || refBrut.cibleCPP == null) ? "" : refBrut.cibleCPP;
  if (parseFloat(cible) > 0) r.scenariosCibles++;
  return {
    id: refBrut.id || ("re" + (iR + 1) + "-" + Math.random().toString(36).slice(2, 6)),
    nom: refBrut.nom || "Référence sans nom",
    cibleCPP: cible,
    productionAnnuelle: refBrut.productionAnnuelle != null ? refBrut.productionAnnuelle : "",
    volumeHistorique: Array.isArray(refBrut.volumeHistorique) ? refBrut.volumeHistorique.slice(0, 10) : [],
    ops: (refBrut.ops || []).map((opBrut, iO) => normaliserOp(opBrut, iO, r))
  };
}

function normaliserOp(opBrut, iO, r) {
  r.ops++;
  const code = opBrut.code && opBrut.code !== "?" ? opBrut.code : codeDeOp(opBrut);
  return {
    id: opBrut.id || ("op" + (iO + 1) + "-" + Math.random().toString(36).slice(2, 6)),
    nom: opBrut.nom || code,
    ordre: opBrut.ordre != null ? opBrut.ordre : null,
    opCode: code,
    ficheOutil: opBrut.ficheOutil || null,
    config: opBrut.config && typeof opBrut.config === "object" ? Object.assign({}, opBrut.config) : {},
    scenarios: (opBrut.scenarios || []).map((scBrut, iS) => normaliserScenario(scBrut, iS, r))
  };
}

function normaliserScenario(scBrut, iS, r) {
  r.scenarios++;
  const sc = {
    id: scBrut.id || ("sc" + (iS + 1) + "-" + Math.random().toString(36).slice(2, 6)),
    name: nomScenario(scBrut),
    cycle: scBrut.cycle != null ? scBrut.cycle : 100,
    baseline: scBrut.baseline === true,
    statut: scBrut.statut || "essai",
    statutMotif: scBrut.statutMotif || "",
    statutDate: scBrut.statutDate || "",
    emag1: scBrut.emag1 === true,
    battCotes: scBrut.battCotes || "DG",
    limitOverride: scBrut.limitOverride === true,
    limitLabel: scBrut.limitLabel || "Battement (mm)",
    limitValue: scBrut.limitValue != null ? scBrut.limitValue : "",
    limitLabel2: scBrut.limitLabel2 || "Ra (µm)",
    limitValue2: scBrut.limitValue2 != null ? scBrut.limitValue2 : "",
    critere2Actif: scBrut.critere2Actif === true,
    criteresSup: Array.isArray(scBrut.criteresSup) ? scBrut.criteresSup.slice() : [],
    validationThreshold: scBrut.validationThreshold != null ? scBrut.validationThreshold : 5,
    battActif: scBrut.battActif !== false,
    tauxRebutAnnuel: scBrut.tauxRebutAnnuel != null ? scBrut.tauxRebutAnnuel : "",
    marpossRapport: scBrut.marpossRapport || "",
    tendanceRapport: scBrut.tendanceRapport || "",
    notes: scBrut.notes || "",
    outils: (scBrut.outils || []).map(oBrut => normaliserOutil(oBrut, r)),
    essais: (scBrut.essais || []).map(eBrut => normaliserEssai(eBrut, r)),
    scrapLog: Array.isArray(scBrut.scrapLog) ? scBrut.scrapLog.slice() : []
  };
  r.scrapLog += sc.scrapLog.length;
  /* La cohérence du scénario de production : le ★ est en série, verrouillé
     (v4.4 de l'app). Une exportation ancienne peut n'avoir qu'un des deux. */
  if (sc.baseline) sc.statut = "serie";
  if (sc.statut === "serie") sc.baseline = true;
  return sc;
}

function normaliserOutil(oBrut, r) {
  r.outils++;
  if (oBrut.plan) r.plans++;
  return {
    id: oBrut.id || ("t" + Math.random().toString(36).slice(2, 8)),
    numero: oBrut.numero || "",
    correcteur: oBrut.correcteur || "",
    description: oBrut.description || "",
    plan: oBrut.plan || null,
    pieces: Array.isArray(oBrut.pieces) ? oBrut.pieces.slice() : [],
    logements: (oBrut.logements || []).map(lBrut => normaliserLogement(lBrut, r))
  };
}

function normaliserLogement(lBrut, r) {
  r.logements++;
  const trio = {
    prix: parseFloat(lBrut.prix) > 0,
    aretes: parseFloat(lBrut.aretes) > 0,
    charniere: parseFloat(lBrut.charniere) > 0
  };
  if (!trio.prix) r.sansPrix++;
  if (!trio.aretes) r.sansAretes++;
  if (!trio.charniere) r.sansCharniere++;
  return {
    id: lBrut.id || ("g" + Math.random().toString(36).slice(2, 8)),
    nom: lBrut.nom || "Logement",
    ref: lBrut.ref || "",
    codeArticle: lBrut.codeArticle || "",
    mabec: lBrut.mabec || "",
    prix: lBrut.prix != null ? lBrut.prix : "",
    aretes: lBrut.aretes != null ? lBrut.aretes : "",
    charniere: lBrut.charniere != null ? lBrut.charniere : "",
    vc: lBrut.vc != null ? lBrut.vc : "",
    f: lBrut.f != null ? lBrut.f : "",
    kappaR: lBrut.kappaR != null ? lBrut.kappaR : "",
    rayonBec: lBrut.rayonBec != null ? lBrut.rayonBec : "",
    apPiste: lBrut.apPiste != null ? lBrut.apPiste : "",
    tempsCoupe: lBrut.tempsCoupe != null ? lBrut.tempsCoupe : "",
    tempsDeplacement: lBrut.tempsDeplacement != null ? lBrut.tempsDeplacement : "",
    suiviTolerance: lBrut.suiviTolerance === true
  };
}

function normaliserEssai(eBrut, r) {
  r.essais++;
  const essai = {
    id: eBrut.id || ("e" + Math.random().toString(36).slice(2, 8)),
    titre: eBrut.titre || "Essai",
    date: eBrut.date || "",
    dateFin: eBrut.dateFin || "",
    heureDebut: eBrut.heureDebut || "",
    heureFin: eBrut.heureFin || "",
    equipe: eBrut.equipe || "",
    operateur: eBrut.operateur || "",
    redigePar: eBrut.redigePar || "",
    programme: eBrut.programme || "",
    programmeGauche: eBrut.programmeGauche || "",
    programmeDroit: eBrut.programmeDroit || "",
    maturiteBruts: eBrut.maturiteBruts || "",
    observations: eBrut.observations || eBrut.but || "",
    cloture: eBrut.cloture || null,
    params: { logements: (eBrut.params && eBrut.params.logements) || [] },
    prelevements: [],
    photos: Array.isArray(eBrut.photos) ? eBrut.photos.slice() : [],
    marpossListe: Array.isArray(eBrut.marpossListe) ? eBrut.marpossListe.slice() : [],
    marposs: eBrut.marposs || null,
    modifieLe: eBrut.modifieLe || null
  };
  r.photos += essai.photos.length;
  r.marposs += essai.marpossListe.length;
  (eBrut.prelevements || []).forEach(pBrut => {
    r.prelevements++;
    const sansBatt = isNaN(parseFloat(pBrut.batt)) && isNaN(parseFloat(pBrut.battD))
      && isNaN(parseFloat(pBrut.battG));
    if (sansBatt) r.prelevementsSansBatt++;
    essai.prelevements.push({
      id: pBrut.id || ("p" + Math.random().toString(36).slice(2, 8)),
      piece: pBrut.piece != null ? pBrut.piece : "",
      batt: pBrut.batt != null ? pBrut.batt : "",
      battD: pBrut.battD != null ? pBrut.battD : "",
      battG: pBrut.battG != null ? pBrut.battG : "",
      logementId: pBrut.logementId || "",
      pointMesure: pBrut.pointMesure || "",
      usure: pBrut.usure != null ? pBrut.usure : "",
      valeur2: pBrut.valeur2 != null ? pBrut.valeur2 : "",
      valeurs: pBrut.valeurs || {}
    });
  });
  return essai;
}

function normaliserProjet(pBrut, iP, r, responsableDeTexte) {
  if (!pBrut || typeof pBrut !== "object") return null;
  /* Le format 6 portait les lignes dans les projets : déjà aplati par
     racinesLignes, on ne relit pas `lignes` ici. */
  const tags = (Array.isArray(pBrut.tags) ? pBrut.tags : [])
    .filter(t => t && typeof t === "object")
    .map(t => ({
      ligneId: t.ligneId || "",
      referenceId: t.referenceId || "",
      opId: t.opId || "",
      scenarioId: t.scenarioId || ""
    }));
  r.etiquettes += tags.length;
  let responsableId = pBrut.responsableId || "";
  if (!responsableId && pBrut.responsable && typeof pBrut.responsable === "string") {
    responsableId = responsableDeTexte(pBrut.responsable, [
      "#3b82f6", "#14b8a6", "#a78bfa", "#f59e0b", "#22c55e", "#94a3b8", "#ec4899", "#0ea5e9"
    ]);
  }
  return {
    id: pBrut.id || ("pj" + (iP + 1) + "-" + Math.random().toString(36).slice(2, 6)),
    nom: pBrut.nom || "Projet sans nom",
    description: pBrut.description || pBrut.problematique || "",
    statut: pBrut.statut || "encours",
    dateCible: pBrut.dateCible || "",
    responsableId: responsableId,
    couleur: pBrut.couleur || "",
    creePar: pBrut.creePar || "",
    creeLe: pBrut.creeLe || "",
    modifieLe: pBrut.modifieLe || null,
    tags: tags,
    lignes: Array.isArray(pBrut.lignes) ? pBrut.lignes.slice() : undefined
  };
}

function normaliserResponsable(rb) {
  if (!rb || typeof rb !== "object") return null;
  return { id: rb.id || ("u" + Math.random().toString(36).slice(2, 10)), nom: rb.nom || "?", couleur: rb.couleur || "" };
}

/* Le code court d'une OP, dérivé — jamais une donnée saisie écrasée. */
function codeDeOp(op) {
  if (op.opCode && op.opCode !== "?") return op.opCode;
  if (op.ordre != null && !isNaN(parseFloat(op.ordre))) return "OP" + parseFloat(op.ordre);
  const m = /OP\s*0*(\d+)/i.exec(op.nom || "");
  return m ? "OP" + parseInt(m[1], 10) : "OP?";
}

/* ============================================================================
   2. LA FUSION — deux postes travaillent, aucun chiffre n'est perdu
   ========================================================================== */

/* La fusion arbitre essai par essai sur `modifieLe` (le rituel connu :
   « Fusionner plutôt que Remplacer » dès que deux personnes ont saisi chacune
   de leur côté). Les réglages restent LOCAUX (décision actée).
   Renvoie { etat, rapport }. */
function fusionnerEtat(local, arrivee) {
  const r = {
    essaisAjoutes: 0, essaisGagnesArrivee: 0, essaisGardesLocaux: 0,
    scenariosAjoutes: 0, projetsFusionnes: 0, projetsAjoutes: 0,
    etiquettesAjoutees: 0, responsablesAjoutes: 0, lignesAjoutees: 0,
    conflits: []
  };
  if (!local || !local.lignes) return { etat: arrivee, rapport: r };
  if (!arrivee || !arrivee.lignes) return { etat: local, rapport: r };

  /* Les lignes/réfs/OPs/scénarios qui n'existent que dans l'arrivée passent
     tels quels — un scénario créé de l'autre côté ne doit pas disparaître. */
  const index = indexerArbre(local);
  (arrivee.lignes || []).forEach(lA => {
    if (!index.lignes[lA.id]) {
      local.lignes.push(cloner(lA));
      r.lignesAjoutees++;
      return;
    }
    const lL = index.lignes[lA.id];
    (lA.references || []).forEach(refA => {
      const refL = lL.references.find(x => x.id === refA.id);
      if (!refL) { lL.references.push(cloner(refA)); return; }
      (refA.ops || []).forEach(opA => {
        const opL = refL.ops.find(x => x.id === opA.id);
        if (!opL) { refL.ops.push(cloner(opA)); return; }
        (opA.scenarios || []).forEach(scA => {
          const scL = opL.scenarios.find(x => x.id === scA.id);
          if (!scL) { opL.scenarios.push(cloner(scA)); r.scenariosAjoutes++; return; }
          fusionnerScenario(scL, scA, r);
        });
      });
    });
  });

  /* Les projets : ajoutés si nouveaux, fusionnés (union des étiquettes) sinon. */
  (arrivee.projets || []).forEach(pjA => {
    const pjL = (local.projets || []).find(x => x.id === pjA.id);
    if (!pjL) {
      (local.projets = local.projets || []).push(cloner(pjA));
      r.projetsAjoutes++;
      return;
    }
    r.projetsFusionnes++;
    const vu = {};
    (pjL.tags || []).forEach(t => { vu[t.ligneId + "|" + t.referenceId + "|" + t.opId + "|" + t.scenarioId] = true; });
    (pjA.tags || []).forEach(t => {
      const cle = t.ligneId + "|" + t.referenceId + "|" + t.opId + "|" + t.scenarioId;
      if (!vu[cle]) { (pjL.tags = pjL.tags || []).push(cloner(t)); r.etiquettesAjoutees++; }
    });
  });

  /* Les responsables : union par id. */
  (arrivee.responsables || []).forEach(uA => {
    if (!(local.responsables || []).some(x => x.id === uA.id)) {
      (local.responsables = local.responsables || []).push(cloner(uA));
      r.responsablesAjoutes++;
    }
  });

  /* Les livraisons et le backlog : union par id — un document figé ne se
     perd jamais dans une fusion. */
  (arrivee.livraisons || []).forEach(lv => {
    if (!(local.livraisons || []).some(x => x.id === lv.id)) (local.livraisons = local.livraisons || []).push(cloner(lv));
  });
  (arrivee.backlog || []).forEach(bk => {
    if (!(local.backlog || []).some(x => x.id === bk.id)) (local.backlog = local.backlog || []).push(cloner(bk));
  });

  return { etat: local, rapport: r };
}

function fusionnerScenario(scL, scA, r) {
  /* Les essais, arbitrage modifieLe : le plus récent gagne, à égalité le
     local garde (ne rien casser localement). */
  const essaisL = scL.essais || (scL.essais = []);
  (scA.essais || []).forEach(eA => {
    const eL = essaisL.find(x => x.id === eA.id);
    if (!eL) {
      essaisL.push(cloner(eA));
      r.essaisAjoutes++;
      return;
    }
    const tL = new Date(eL.modifieLe || 0).getTime() || 0;
    const tA = new Date(eA.modifieLe || 0).getTime() || 0;
    if (tA > tL) {
      Object.keys(eA).forEach(k => { eL[k] = cloner(eA[k]); });
      eL.modifieLe = eA.modifieLe;
      r.essaisGagnesArrivee++;
    } else if (tA < tL) {
      r.essaisGardesLocaux++;
    } else {
      r.essaisGardesLocaux++;
      if (JSON.stringify(eL) !== JSON.stringify(eA)) {
        r.conflits.push(scL.name + " · " + (eL.titre || "essai") + " : deux versions sans horodatage — la locale est gardée");
      }
    }
  });
  /* Les champs de structure d'un scénario arrivé plus récent (outils,
     limites) : on ne les écrase pas — la fusion d'outils par id est le
     chantier suivant ; ici, personne ne perd d'essai. */
}

function indexerArbre(etat) {
  const lignes = {};
  (etat.lignes || []).forEach(l => { lignes[l.id] = l; });
  return { lignes: lignes };
}

function cloner(x) {
  return x === undefined ? undefined : JSON.parse(JSON.stringify(x));
}

/* ============================================================================
   3. LE POIDS — mesuré, pas estimé
   ========================================================================== */

function poids(jsonSource, etat) {
  let avant = 0, apres = 0;
  try { avant = JSON.stringify(jsonSource).length; } catch (e) { avant = 0; }
  try { apres = JSON.stringify(etat).length; } catch (e) { apres = 0; }
  return {
    avant: avant,
    apres: apres,
    ratio: avant ? Math.round((apres / avant) * 1000) / 1000 : null
  };
}
