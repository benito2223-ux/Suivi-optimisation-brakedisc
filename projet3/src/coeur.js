/* ============================================================================
   PROJET3 — LE NOYAU
   Fonctions PURES. Aucun DOM, aucun état global, aucune lecture du disque.
   Écrites et testées AVANT le moindre écran (cahier §8).

   Le driver (cahier §3) :
     CPP outillage = Σ prix / (arêtes × charnière)      — comparable au classeur
     Chaque CPP affiché porte deux chiffres : le PRÉVU du scénario et l'OBTENU
     par l'essai. Le temps machine se lit à côté, jamais fusionné.

   Toute absence dit ce qui manque (cahier §5.2). Aucun « — » nu.
   Les codes de verdict sont en ASCII : un accent dans un code a déjà fait
   échouer une comparaison en silence (leçon proto, recapLignes).
   ========================================================================== */

"use strict";

const VERSION = "3.0.0";
const APP_NOM = "Suivi optimisation SPK";
const FORMAT_ACTUEL = 9;

/* ============================================================================
   0. LE FORMATAGE — pur lui aussi
   ========================================================================== */

function fmt(v, d) {
  if (v === null || v === undefined || v === "" || isNaN(parseFloat(v))) return "—";
  const n = parseFloat(v);
  return n.toFixed(d === undefined ? 3 : d).replace(".", ",");
}

/* Garde la distinction « 0 » (mesuré) / « pas saisi » (absent) : le champ vide
   ne s'affiche pas comme 0, il s'affiche comme ce qui manque (cahier §5.2). */
function fmtDispo(v, d, manque) {
  if (v === null || v === undefined || v === "") return manque || "— non saisi";
  if (isNaN(parseFloat(v))) return manque || "— non saisi";
  return fmt(v, d);
}

function fmtEuro(v, d) {
  if (v === null || v === undefined || v === "" || isNaN(parseFloat(v))) return "—";
  return fmt(v, d === undefined ? 4 : d) + " €";
}

function nombre(v) {
  const n = parseFloat(v);
  return isNaN(n) ? null : n;
}

/* ============================================================================
   1. LE CPP OUTILLAGE — le driver
   ========================================================================== */

/* Le coût d'UN logement : le prix de la plaquette divisé par ce qu'elle rend.
   prix en €, arêtes en nombre d'arêtes, charnière en pièces -> € par pièce.
   Une donnée manquante ou absurde donne null (non chiffrable) — jamais 0. */
function coutLogement(log) {
  if (!log) return null;
  const prix = nombre(log.prix);
  const aretes = nombre(log.aretes);
  const charniere = nombre(log.charniere);
  if (prix === null || prix <= 0) return null;
  if (aretes === null || aretes <= 0) return null;
  if (charniere === null || charniere <= 0) return null;
  return prix / (aretes * charniere);
}

/* Le CPP outillage d'un scénario = la somme sur TOUS ses logements.
   Invariant : un logement non chiffrable est COMPTE, pas dilué — l'appelant
   dispose de cppScenarioDetail() pour savoir combien ont été écartés. */
function cppOutillageScenario(sc) {
  const d = cppScenarioDetail(sc);
  return d.cpp;
}

function cppScenarioDetail(sc) {
  const vide = { cpp: null, nbChiffrables: 0, nbNonChiffrables: 0 };
  if (!sc || !sc.outils) return vide;
  let total = 0, n = 0, ecartes = 0;
  (sc.outils || []).forEach(o => {
    (o.logements || []).forEach(l => {
      const c = coutLogement(l);
      if (c === null) { ecartes++; return; }
      total += c; n++;
    });
  });
  return { cpp: n ? total : null, nbChiffrables: n, nbNonChiffrables: ecartes };
}

function cppOutillageOutil(outil) {
  if (!outil || !outil.logements) return null;
  const parts = (outil.logements || []).map(coutLogement).filter(v => v !== null);
  if (!parts.length) return null;
  return parts.reduce((a, b) => a + b, 0);
}

/* La décomposition logement par logement, outil par outil — l'endroit où
   l'argent part. Un seau par outil : le seau se remplit en parcourant CET
   outil, jamais par regroupement sur le numéro (deux outils peuvent porter
   le même numéro sur des lignes différentes). */
function outillageDeScenario(sc) {
  if (!sc) return { outils: [], cpp: null, nonChiffrables: 0 };
  const outils = [];
  let total = 0, chiffres = 0, nonChiffrables = 0;
  (sc.outils || []).forEach(o => {
    const logements = (o.logements || []).map(l => ({
      outilId: o.id || "",
      outilNumero: o.numero || "?",
      outilDescription: o.description || "",
      logementId: l.id || "",
      logementNom: l.nom || "?",
      article: l.ref || "",
      mabec: l.mabec || "",
      cpp: coutLogement(l),
      prix: nombre(l.prix),
      aretes: nombre(l.aretes),
      charniere: nombre(l.charniere)
    }));
    logements.forEach(x => {
      if (x.cpp === null) { nonChiffrables++; return; }
      total += x.cpp; chiffres++;
    });
    const cppOutil = logements.some(x => x.cpp !== null)
      ? logements.filter(x => x.cpp !== null).reduce((a, b) => a + b.cpp, 0)
      : null;
    outils.push({
      id: o.id || "",
      numero: o.numero || "?",
      description: o.description || "",
      correcteur: o.correcteur || "",
      cpp: cppOutil,
      logements: logements
    });
  });
  return {
    outils: outils,
    cpp: chiffres ? total : null,
    nonChiffrables: nonChiffrables
  };
}

/* ============================================================================
   2. LE CPP OBTENU PAR ESSAI — ce qu'on a prévu contre ce qu'on a eu
   ========================================================================== */

/* Le prix et les arêtes viennent de la définition du logement dans le
   scénario ; la charnière vient de l'essai lui-même (charnière mesurée).
   C'est le seul endroit où prévu et obtenu se séparent : sans lui, un essai
   qui tient mieux que prévu ne se voit nulle part.
   Invariant : un logement non chiffrable est compté (nonChiffrables), pas dilué. */
function cppEssaiObtenu(scenario, essai) {
  const vide = { cpp: null, nbLogements: 0, nonChiffrables: 0 };
  if (!scenario || !essai) return vide;
  const definition = {};
  (scenario.outils || []).forEach(o => (o.logements || []).forEach(l => {
    definition[l.id] = l;
  }));
  const suivis = (essai.params && essai.params.logements) || [];
  if (!suivis.length) return vide;
  let total = 0, n = 0, ecartes = 0;
  suivis.forEach(p => {
    const def = definition[p.logementId];
    const prix = (def && def.prix !== "" && def.prix != null) ? def.prix : p.prix;
    const aretes = (def && def.aretes !== "" && def.aretes != null) ? def.aretes : p.aretes;
    const charniere = (p.charniere !== "" && p.charniere != null)
      ? p.charniere : (def ? def.charniere : null);
    const c = coutLogement({ prix: prix, aretes: aretes, charniere: charniere });
    if (c === null) { ecartes++; return; }
    total += c; n++;
  });
  return { cpp: n ? total : null, nbLogements: n, nonChiffrables: ecartes };
}

/* Le CPP PRÉVU d'un scénario d'essai (la somme des logements), à côté de
   l'obtenu — les deux dans la même unité, donc comparables. */
function essaisAvecCPP(sc) {
  return (sc && sc.essais || []).map(e => {
    const obtenu = cppEssaiObtenu(sc, e);
    return { essai: e, obtenu: obtenu };
  });
}

/* ============================================================================
   3. LE TEMPS MACHINE — l'axe secondaire, jamais comparable au classeur
   ========================================================================== */

/* (taux horaire ÷ 3600) × temps de cycle, en €/pièce. Renvoie null tant que
   le taux horaire de la ligne ou le cycle n'est pas chiffrable — l'écran dit
   alors « temps non chiffrable », il n'affiche pas 0. */
function coutMachinePiece(sc, ligne) {
  if (!sc || !ligne) return null;
  const taux = nombre(ligne.coutHoraire);
  if (taux === null || taux <= 0) return null;
  const sec = cycleSecondes(sc);
  if (sec === null) return null;
  return (taux / 3600) * sec;
}

/* Le cycle en secondes. Chiffrable seulement si le détail du cycle est saisi
   pour tous les logements (temps coupe / déplacement) — sinon null, et c'est
   dit. Un indice base 100 seul ne donne pas des secondes. */
function cycleSecondes(sc) {
  if (!sc) return null;
  let total = 0;
  let groupe = null;           // temps du groupe d'outils en cours (simultanés)
  (sc.outils || []).forEach(o => {
    let tOutil = 0, complet = (o.logements || []).length > 0;
    (o.logements || []).forEach(l => {
      const tc = nombre(l.tempsCoupe);
      const td = nombre(l.tempsDeplacement);
      if (tc === null && td === null) { complet = false; return; }
      tOutil += (tc || 0) + (td || 0);
    });
    if (!complet) { total = NaN; return; }
    if (o.simultaneAvecPrecedent) {
      // les outils simultanés tournent ensemble : le groupe prend le plus long
      if (groupe === null) groupe = tOutil; else groupe = Math.max(groupe, tOutil);
    } else {
      if (groupe !== null) { total += groupe; groupe = null; }
      groupe = tOutil;
    }
  });
  if (groupe !== null) total += groupe;
  if (isNaN(total) || total <= 0) return null;
  return total;
}

/* ============================================================================
   4. LE CHEMIN PROD → CIBLE
   ========================================================================== */

/* Combien de chemin a fait le meilleur scénario disponible vers la cible ?
   Renvoie null si on ne peut pas calculer — et l'appelant affiche pourquoi.
   Déjà sous la cible : le chemin est fait (100). */
function cheminCPP(coutProd, coutMeilleur, cible) {
  const c = nombre(cible);
  if (c === null) return null;
  const p = nombre(coutProd);
  const m = nombre(coutMeilleur);
  if (p === null || m === null) return null;
  if (p <= c) return 100;
  if (p <= 0) return null;
  const pct = ((p - m) / (p - c)) * 100;
  return Math.max(0, Math.min(100, pct));
}

/* ============================================================================
   5. LA PREUVE — battement, Ra, répétitions
   ========================================================================== */

/* Le battement d'un prélèvement. EMAG 1 relève droite et gauche séparément
   (battD / battG) : sur les données réelles du site, `batt` est vide sur 83
   prélèvements sur 84. On prend `batt` si elle existe, sinon LE PIRE des deux
   côtés — jamais la moyenne : un état des lieux ne doit pas flatter une pièce
   qui déborde d'un seul côté. */
function battDe(prel) {
  if (!prel) return NaN;
  const b = nombre(prel.batt);
  if (b !== null) return b;
  const cotes = [nombre(prel.battD), nombre(prel.battG)].filter(v => v !== null);
  if (!cotes.length) return NaN;
  return Math.max.apply(null, cotes);
}

const BATTEMENT_DEFAUT = 0.12;
const RA_DEFAUT = 0.8;

/* Le Ra d'un prélèvement (2e critère) : champ `valeur2`, ou `valeurs.cs1.v`
   (ancienne forme). Absent = null, jamais 0. */
function raDe(prel) {
  if (!prel) return null;
  const v2 = nombre(prel.valeur2);
  if (v2 !== null) return v2;
  if (prel.valeurs && prel.valeurs.cs1) return nombre(prel.valeurs.cs1.v);
  return null;
}

/* Un prélèvement respecte-t-il tous les critères actifs du scénario ?
   Renvoie { ok: true|false|null, motif } — null = non mesurable, jamais false. */
function conforme(sc, prel) {
  if (!prel) return { ok: null, motif: "aucun prélèvement" };
  const critereBattement = !(sc && sc.battActif === false);
  if (critereBattement) {
    const limite = (sc && sc.limitOverride && sc.limitValue !== "" && sc.limitValue != null)
      ? nombre(sc.limitValue) : BATTEMENT_DEFAUT;
    if (limite === null) return { ok: null, motif: "limite de battement non saisie" };
    const b = battDe(prel);
    if (isNaN(b)) return { ok: null, motif: "battement non relevé" };
    if (b > limite) return { ok: false, motif: "battement " + fmt(b, 3) + " > " + fmt(limite, 3) };
  }
  if (sc && sc.critere2Actif) {
    const limite2 = nombre(sc.limitValue2);
    if (limite2 !== null) {
      const ra = raDe(prel);
      if (ra === null) return { ok: null, motif: "Ra non relevé" };
      if (ra > limite2) return { ok: false, motif: "Ra " + fmt(ra, 2) + " > " + fmt(limite2, 2) };
    }
  }
  const sups = (sc && sc.criteresSup || []).filter(c => c && c.actif);
  for (let i = 0; i < sups.length; i++) {
    const c = sups[i];
    const cle = c.id || ("cs" + (i + 1));
    const v = (prel.valeurs && prel.valeurs[cle]) ? nombre(prel.valeurs[cle].v) : null;
    if (v === null) continue;              // critère supplémentaire non relevé : il ne bloque pas
    const maxi = nombre(c.maxi);
    const mini = (c.miniActif) ? nombre(c.mini) : null;
    if (maxi !== null && v > maxi) return { ok: false, motif: (c.label || cle) + " " + fmt(v, 3) + " > " + fmt(maxi, 3) };
    if (mini !== null && v < mini) return { ok: false, motif: (c.label || cle) + " " + fmt(v, 3) + " < " + fmt(mini, 3) };
  }
  return { ok: true, motif: "" };
}

/* La charnière visée d'un logement pour un essai donné : la charnière mesurée
   saisie dans l'essai, à défaut celle du logement dans le scénario. */
function charniereVisee(scenario, essai, logementId) {
  const liste = (essai && essai.params && essai.params.logements) || [];
  const trouve = liste.find(p => p.logementId === logementId);
  if (trouve) {
    const v = nombre(trouve.charniere);
    if (v !== null) return v;
  }
  let out = null;
  (scenario.outils || []).forEach(o => (o.logements || []).forEach(l => {
    if (l.id === logementId) {
      const v = nombre(l.charniere);
      if (v !== null) out = v;
    }
  }));
  return out;
}

/* Le statut d'un ESSAI. L'ordre est délibéré : un essai arrêté est une
   décision, pas un échec ; une pièce hors tolérance est un fait, pas une
   opinion ; une charnière non atteinte est un travail en cours. */
function statutEssai(sc, essai) {
  if (!essai) return { code: "vide", texte: "aucun essai" };
  const prels = essai.prelevements || [];
  if (essai.cloture && essai.cloture.motif) {
    return { code: "arrete", texte: "arrêté — " + (essai.cloture.motif || "sans motif") };
  }
  if (!prels.length) return { code: "attente", texte: "aucun prélèvement" };
  const juges = prels.map(p => conforme(sc, p));
  const premierKO = juges.findIndex(j => j.ok === false);
  if (premierKO >= 0) {
    return {
      code: "nonconforme",
      texte: "hors tolérance — " + juges[premierKO].motif,
      piece: nombre(prels[premierKO].piece)
    };
  }
  const nonMesurables = juges.filter(j => j.ok === null).length;
  // la charnière : chaque logement suivi doit être atteint
  const suivis = (essai.params && essai.params.logements) || [];
  const pieces = prels.map(x => nombre(x.piece)).filter(v => v !== null);
  const derniere = pieces.length ? Math.max.apply(null, pieces) : null;
  const restants = [];
  suivis.forEach(p => {
    const cible = charniereVisee(sc, essai, p.logementId);
    if (cible === null) return;
    if (derniere === null || derniere < cible) {
      restants.push({
        logementNom: p.logementNom || "?",
        dernier: derniere === null ? 0 : derniere,
        cible: cible
      });
    }
  });
  if (restants.length) {
    return {
      code: "encours",
      texte: restants.map(r => r.logementNom + " " + fmt(r.dernier, 0) + "/" + fmt(r.cible, 0) + " p").join(" · ")
    };
  }
  if (nonMesurables > 0) {
    return { code: "attente", texte: nonMesurables + " mesure" + (nonMesurables > 1 ? "s" : "") + " à saisir" };
  }
  return { code: "conforme", texte: "conforme — charnière atteinte" };
}

/* Le statut d'un SCÉNARIO : le verdict de la décision.
   « valide » = protocole 5× complété, pas encore passé en série. */
function statutScenario(sc) {
  if (!sc) return { code: "opportunite", texte: "rien d'essayé" };
  if (sc.baseline || sc.statut === "serie") return { code: "serie", texte: "en série" };
  const essais = sc.essais || [];
  const juges = essais.map(e => statutEssai(sc, e));
  const conformes = juges.filter(v => v.code === "conforme").length;
  const seuil = nombre(sc.validationThreshold) || 5;
  if (conformes >= seuil) {
    return { code: "valide", texte: "validé " + conformes + "× — à passer en série", validations: conformes };
  }
  if (essais.length) return { code: "encours", texte: "essai en cours", validations: conformes };
  return { code: "opportunite", texte: "rien d'essayé" };
}

/* ============================================================================
   6. LE VERDICT D'UN POSTE — ce que la tuile montre, l'écran décision tranche
   ========================================================================== */

/* Quel est le scénario EN PRODUCTION d'une opération ? Dans l'ordre du plus
   sûr au plus douteux :
     1. le scénario marqué ★ (baseline)
     2. à défaut, celui qui est en série
     3. à défaut, celui dont le nom dit « base excel » (fallback d'import)
   Jamais « le premier de la liste » : sans règle explicite, deux scénarios
   peuvent revendiquer la prod et l'un passerait en silence. */
function scenarioDeProd(scs) {
  const liste = scs || [];
  return liste.find(s => s && s.baseline === true)
      || liste.find(s => s && s.statut === "serie")
      || liste.find(s => s && /base excel/i.test(s.name || s.nom || ""))
      || null;
}

/* Un poste = une opération portée par une référence, avec son scénario de
   production et ses scénarios d'optimisation. Le CALCUL est ici, jamais dans
   le rendu (cahier §5.1). */
function verdictPoste(ref, op, scs) {
  const liste = scs || (op && op.scenarios) || [];
  const prod = scenarioDeProd(liste);
  const dProd = prod ? cppScenarioDetail(prod) : { cpp: null, nbNonChiffrables: 0 };
  const cppProd = dProd.cpp;
  const cible = (ref && ref.cibleCPP !== "" && ref.cibleCPP != null) ? nombre(ref.cibleCPP) : null;

  /* Le MEILLEUR scénario d'optimisation, par CPP prévu — tous statuts, la
     prod exclue. C'est lui qui donne le chemin vers la cible et le verdict. */
  let meilleur = null;
  liste.forEach(s => {
    if (!s || (prod && s.id === prod.id)) return;
    const cpp = cppOutillageScenario(s);
    if (cpp === null) return;
    if (!meilleur || cpp < meilleur.cpp) meilleur = { sc: s, cpp: cpp };
  });

  /* Le meilleur CPP OBTENU par essai, tous scénarios confondus — la preuve
     que le terrain donne parfois mieux que le prévu (EMAG 1 · OP40 : prévu
     0,2452, obtenu 0,0797). Distinct du prévu, jamais mélangé avec lui. */
  let meilleurObtenu = null;
  liste.forEach(s => {
    (s && s.essais || []).forEach(e => {
      const o = cppEssaiObtenu(s, e);
      if (o.cpp === null) return;
      if (!meilleurObtenu || o.cpp < meilleurObtenu.cpp) {
        meilleurObtenu = { sc: s, essai: e, cpp: o.cpp, nbLogements: o.nbLogements, nonChiffrables: o.nonChiffrables };
      }
    });
  });

  const chemin = (cppProd !== null && meilleur) ? cheminCPP(cppProd, meilleur.cpp, cible) : null;

  let verdict;
  const stMeilleur = meilleur ? statutScenario(meilleur.sc) : null;
  if (!liste.length) {
    verdict = { code: "vide", texte: "aucun scénario posé sur ce poste" };
  } else if (!prod || cppProd === null) {
    verdict = { code: "achiffrer", texte: cible !== null ? "cible connue, à chiffrer" : "à chiffrer" };
  } else if (stMeilleur && stMeilleur.code === "serie") {
    verdict = { code: "gagne", texte: "gagné — en série" };
  } else if (stMeilleur && stMeilleur.code === "valide") {
    verdict = { code: "pret", texte: "validé " + (stMeilleur.validations || 5) + "× — décision à prendre" };
  } else if (meilleur && meilleur.cpp < cppProd) {
    verdict = { code: "essai", texte: "essai prometteur" };
  } else {
    verdict = { code: "rien", texte: "au meilleur connu — rien de mieux testé" };
  }

  /* Deux gains, jamais sommés (cahier §5.3) :
     gainProjete — le meilleur scénario disponible qui attend encore une
                   décision (un scénario déjà passé en série est couvert par
                   le gain acté : le compter aussi en projeté serait compter
                   deux fois le même essai) ;
     gainActe    — ce qui est réellement passé en série (un scénario « serie »
                   différent de la prod, forcément meilleur). */
  let gainProjete = null, gainActe = null;
  const dejaSerie = meilleur && (meilleur.sc.statut === "serie" || meilleur.sc.baseline === true);
  if (cppProd !== null && meilleur && meilleur.cpp < cppProd && !dejaSerie) {
    gainProjete = cppProd - meilleur.cpp;
  }
  const enSerie = liste.filter(s => s && s.statut === "serie" && !(prod && s.id === prod.id) && s.baseline !== true);
  if (cppProd !== null && enSerie.length) {
    const cppSerie = cppOutillageScenario(enSerie[0]);
    if (cppSerie !== null && cppSerie < cppProd) gainActe = cppProd - cppSerie;
  }

  /* Le gain annuel ne se calcule que si le volume annuel de la référence est
     saisi — sinon null, et l'écran dit « — volume annuel non saisi ». */
  const volume = (ref && ref.productionAnnuelle !== "" && ref.productionAnnuelle != null) ? nombre(ref.productionAnnuelle) : null;
  const gainAnnuelActe = (gainActe !== null && volume !== null) ? gainActe * volume : null;
  const gainAnnuelProjete = (gainProjete !== null && volume !== null) ? gainProjete * volume : null;

  return {
    ref: ref, op: op, scs: liste, prod: prod,
    cppProd: cppProd, nonChiffrables: dProd.nbNonChiffrables,
    cible: cible, chemin: chemin,
    meilleur: meilleur, meilleurObtenu: meilleurObtenu,
    gainProjete: gainProjete, gainActe: gainActe,
    gainAnnuelProjete: gainAnnuelProjete, gainAnnuelActe: gainAnnuelActe,
    volume: volume,
    verdict: verdict
  };
}

/* Que fait-on de ce poste ? Un seul mot — l'écran décision se lit en 15 s. */
function decisionPoste(v) {
  if (!v) return { mot: "—", pourquoi: "" };
  switch (v.verdict.code) {
    case "gagne":
      return { mot: "SÉRIE", pourquoi: "l'essai est passé en production" };
    case "pret":
      return { mot: "DÉCIDER", pourquoi: "validé " + (v.verdict.validations || 5) + " fois — il reste à dire oui ou non" };
    case "essai":
      return {
        mot: "ESSAYER",
        pourquoi: "l'essai gagne " + fmt(v.gainProjete, 4) + " €/pièce — à confirmer sur "
                  + ((v.meilleur && v.meilleur.sc.validationThreshold) || 5) + " essais conformes"
      };
    case "achiffrer":
      return { mot: "CHIFFRER", pourquoi: v.verdict.texte };
    case "vide":
      return { mot: "POSER", pourquoi: "aucun scénario posé — commencez par ce qui tourne réellement" };
    default:
      return { mot: "GARDER", pourquoi: "au meilleur connu — aucun essai ne fait mieux que la prod" };
  }
}

/* ============================================================================
   7. LES POSTES, LES RÉFÉRENCES, LES TUILES — les deux premiers étages
   ========================================================================== */

/* Le code court d'une opération (OP10, OP40). L'opCode est DÉRIVÉ, jamais
   stocké comme clé (constitution §2) — mais on le stocke comme cache à la
   normalisation, dérivé du nom, et le calcul sait le refaire. */
function opCodeDe(op) {
  if (!op) return "OP?";
  if (op.opCode && op.opCode !== "?") return op.opCode;
  if (op.ordre != null && !isNaN(parseFloat(op.ordre))) return "OP" + parseFloat(op.ordre);
  const m = /OP\s*0*(\d+)/i.exec(op.nom || "");
  return m ? "OP" + parseInt(m[1], 10) : "OP?";
}

/* Les postes d'une ligne : une opération sur une référence, avec son scénario
   de production. Un seul calcul par poste, réutilisé partout (source unique). */
function postesDeLigne(ligne) {
  const out = [];
  ((ligne && ligne.references) || []).forEach(ref => {
    ((ref && ref.ops) || []).forEach(op => {
      const scs = op.scenarios || [];
      const prod = scenarioDeProd(scs);
      out.push({
        ref: ref, op: op, scs: scs, prod: prod,
        autres: prod ? scs.filter(s => s !== prod) : scs.filter(Boolean),
        verdict: null   // rempli par verdictsDeLigne, jamais recalculé à la main
      });
    });
  });
  return out;
}

/* Le verdict pour chaque poste, posé UNE fois — le rendu lit le tableau,
   il ne recalcule pas (source unique). */
function verdictsDeLigne(ligne) {
  const postes = postesDeLigne(ligne);
  postes.forEach(p => { p.verdict = verdictPoste(p.ref, p.op, p.scs); });
  return postes;
}

/* Le CPP outillage d'une RÉFÉRENCE : la somme de ses postes chiffrables, les
   autres comptés à part (« hors n opérations non chiffrées »). */
function cppReference(postes, ref) {
  const siens = postes.filter(p => p.ref === ref || (p.ref.id && ref.id && p.ref.id === ref.id));
  let total = 0, chiffres = 0, nonChiffrables = 0, sansProd = 0;
  siens.forEach(p => {
    if (!p.prod) { sansProd++; nonChiffrables++; return; }
    const c = p.verdict ? p.verdict.cppProd : cppOutillageScenario(p.prod);
    if (c === null) { nonChiffrables++; return; }
    total += c; chiffres++;
  });
  const cible = (ref && ref.cibleCPP !== "" && ref.cibleCPP != null) ? nombre(ref.cibleCPP) : null;
  const cpp = chiffres ? total : null;
  return {
    ref: ref, cpp: cpp, nbPostes: siens.length,
    chiffres: chiffres, nonChiffrables: nonChiffrables, sansProd: sansProd,
    cible: cible,
    distanceCible: (cpp !== null && cible !== null) ? cpp - cible : null
  };
}

/* LA TUILE — l'étage 1. Une tuile par ligne, rien qu'un chef d'atelier lit en
   passant : la référence dominante, le CPP outillage, l'écart à la cible, ce
   qui attend une décision, et la prochaine étape en toutes lettres.

   Ce qui n'y est PAS (écrit pour qu'on ne le relogue pas) :
   · la cadence et la production hebdomadaire — pas de cadence mesurée par
     ligne, et la production se détaille par lot, pas par poste d'outillage ;
     l'accueil l'écrit au lieu de se taire ;
   · le delta classeur — la question modèle est à Matis, pas encore tranchée. */
function tuileDeLigne(ligne) {
  const postes = verdictsDeLigne(ligne);
  const refs = ((ligne && ligne.references) || []).map(r => cppReference(postes, r));
  const chiffrees = refs.filter(r => r.cpp !== null);

  let cppLigne = 0, nonChiffrables = 0;
  refs.forEach(r => {
    if (r.cpp !== null) cppLigne += r.cpp;
    nonChiffrables += r.nonChiffrables;
  });

  /* La référence dominante : celle qui a le plus de postes chiffrés. À égalité,
     la première du fichier — jamais un tri par nom qui ferait sauter la
     dominante d'une version à l'autre. */
  let dominante = null;
  chiffrees.forEach(r => {
    if (!dominante || r.chiffres > dominante.chiffres) dominante = r;
  });

  const famille = familleDeLigne(ligne && ligne.nom);
  const cible = dominante ? dominante.cible : null;
  const distance = dominante ? dominante.distanceCible : null;

  /* Les décisions en attente : validé 5× à confirmer, ou essai prometteur.
     Un 0 ici voudrait dire « rien à faire » — c'est un mensonge si l'écran
     regorge d'appels à l'action, donc on compte les deux codes. */
  const decisions = postes.filter(p => p.verdict.verdict.code === "pret" || p.verdict.verdict.code === "essai").length;
  const aChiffrer = postes.filter(p => p.verdict.verdict.code === "achiffrer").length;

  return {
    ligne: ligne,
    nom: (ligne && ligne.nom) || "Ligne sans nom",
    code: codeLigneDe(ligne && ligne.nom),
    famille: famille,
    encre: famille ? FAMILLES_LIGNE[famille].encre : "#545e68",
    rang: rangLigne(ligne && ligne.nom),
    postes: postes,
    refs: refs,
    dominante: dominante,
    cpp: chiffrees.length ? cppLigne : null,
    nonChiffrables: nonChiffrables,
    cible: cible,
    distanceCible: distance,
    decisions: decisions,
    aChiffrer: aChiffrer,
    nbEssais: postes.reduce((a, p) => a + (p.verdict.meilleur ? 1 : 0), 0),
    vide: refs.length === 0
  };
}

/* Les tuiles, dans l'ordre physique de l'atelier — pas un tri alphabétique.
   La tuile porte son rang, calculé comme le reste : une seule source. */
function tuilesDeLignes(lignes) {
  return (lignes || []).map(tuileDeLigne)
    .sort((a, b) => (a.rang - b.rang) || a.nom.localeCompare(b.nom));
}

/* Le détail d'une ligne — l'étage 2 : ses références, leurs opérations, et
   pour CHACUNE le scénario de production décomposé jusqu'au logement. Une OP
   sans scénario de production reste visible, marquée « sans production » :
   si elle disparaissait, la ligne paraîtrait complète à tort. */
function detailLigne(ligne) {
  const postes = verdictsDeLigne(ligne);
  const parRef = ((ligne && ligne.references) || []).map(ref => {
    const c = cppReference(postes, ref);
    return {
      ref: ref,
      nom: ref.nom || "Référence sans nom",
      cpp: c.cpp,
      cible: c.cible,
      distanceCible: c.distanceCible,
      nonChiffrables: c.nonChiffrables,
      postes: postes.filter(p => p.ref === ref).map(p => ({
        op: p.op,
        code: opCodeDe(p.op),
        nom: p.op && p.op.nom ? p.op.nom : "",
        prod: p.prod,
        cpp: p.verdict.cppProd,
        nonChiffrables: p.verdict.nonChiffrables,
        outillage: p.prod ? outillageDeScenario(p.prod) : null,
        nbEssaisProd: p.prod ? (p.prod.essais || []).length : 0,
        nbAutres: p.autres.length,
        verdict: p.verdict
      }))
    };
  });
  return {
    ligne: ligne,
    tuile: tuileDeLigne(ligne),
    refs: parRef,
    nbPostes: postes.length,
    nbPostesSansProd: postes.filter(p => !p.prod).length,
    nbScenariosAutres: postes.reduce((a, p) => a + p.autres.length, 0)
  };
}

/* ============================================================================
   8. LES GAINS — actés d'un côté, projetés de l'autre, jamais sommés
   ========================================================================== */

/* Le rollup d'une ligne, poste par poste. gainActe et gainProjete vivent
   dans des blocs distincts à chaque niveau (poste, ligne, atelier). Un poste
   non chiffrable est compté, il ne se dilue pas dans un total silencieux. */
function gainLigne(ligne) {
  const postes = verdictsDeLigne(ligne);
  const parPoste = [];
  let acte = 0, projete = 0, acteAnnuel = 0, projeteAnnuel = 0;
  let chiffrables = 0, nonChiffrables = 0;
  let heuresProjetees = null;
  postes.forEach(p => {
    const v = p.verdict;
    parPoste.push(v);
    if (v.cppProd === null) { nonChiffrables++; return; }
    chiffrables++;
    if (v.gainActe !== null) { acte += v.gainActe; }
    if (v.gainProjete !== null) { projete += v.gainProjete; }
    if (v.gainAnnuelActe !== null) acteAnnuel += v.gainAnnuelActe;
    if (v.gainAnnuelProjete !== null) projeteAnnuel += v.gainAnnuelProjete;
  });

  const dominante = tuileDeLigne(ligne).dominante;

  return {
    ligne: ligne,
    postes: parPoste,
    gainActe: chiffrables ? acte : null,
    gainProjete: chiffrables ? projete : null,
    gainAnnuelActe: acteAnnuel || null,
    gainAnnuelProjete: projeteAnnuel || null,
    chiffrables: chiffrables,
    nonChiffrables: nonChiffrables,
    refDominante: dominante ? dominante.ref : null,
    decisions: postes.filter(p => p.verdict.verdict.code === "pret" || p.verdict.verdict.code === "essai").length
  };
}

/* Le récapitulatif de l'atelier — le bandeau d'accueil. Chaque chiffre
   remonte à sa source ; une absence est nommée, jamais comblée. */
function recapAtelier(lignes) {
  let acte = 0, acteAnnuel = 0, projete = 0, projeteAnnuel = 0;
  let decisions = 0, aChiffrer = 0, lignesEngagees = 0;
  const tuiles = tuilesDeLignes(lignes);
  tuiles.forEach(t => {
    acte += t.postes.reduce((a, p) => a + (p.verdict.gainActe || 0), 0);
    projete += t.postes.reduce((a, p) => a + (p.verdict.gainProjete || 0), 0);
    acteAnnuel += t.postes.reduce((a, p) => a + (p.verdict.gainAnnuelActe || 0), 0);
    projeteAnnuel += t.postes.reduce((a, p) => a + (p.verdict.gainAnnuelProjete || 0), 0);
    decisions += t.decisions;
    aChiffrer += t.aChiffrer;
    if (t.postes.some(p => ["gagne", "pret", "essai"].includes(p.verdict.verdict.code))) lignesEngagees++;
  });
  return {
    tuiles: tuiles,
    gainActe: acte || null,
    gainProjete: projete || null,
    gainAnnuelActe: acteAnnuel || null,
    gainAnnuelProjete: projeteAnnuel || null,
    decisions: decisions,
    aChiffrer: aChiffrer,
    lignesEngagees: lignesEngagees,
    nbLignes: tuiles.length
  };
}

/* ============================================================================
   9. LE RÉFÉRENTIEL DES LIGNES — quatre familles, quatre couleurs (fait
      d'atelier, pas une mesure : Weisser rouge, Hessapp vert, EMAG gris, PCI bleu)
   ========================================================================== */

const FAMILLES_LIGNE = {
  weisser: { libelle: "Weisser", encre: "#E2001A", alpha: 0.07 },
  hessapp: { libelle: "Hessapp", encre: "#556b2f", alpha: 0.13 },
  emag:    { libelle: "EMAG",    encre: "#545e68", alpha: 0.08 },
  pci:     { libelle: "PCI",     encre: "#1b5ea6", alpha: 0.07 }
};
const ORDRE_FAMILLES = ["weisser", "hessapp", "emag", "pci"];

function familleDeLigne(nom) {
  const n = String(nom || "").trim().toLowerCase();
  if (n.startsWith("weisser")) return "weisser";
  if (n.startsWith("hessap")) return "hessapp";
  if (n.startsWith("emag")) return "emag";
  if (n.startsWith("pci")) return "pci";
  return "";
}

/* L'ordre physique de l'atelier. Une ligne inconnue se range APRÈS le
   référentiel, jamais devant Weisser. */
const RANG_LIGNES = [
  "weisser 1", "weisser 2", "weisser 3", "weisser 4",
  "hessapp", "emag 1", "emag 2", "emag 3", "pci 1", "pci 2", "pci 3", "pci 4"
];
function rangLigne(nom) {
  const n = String(nom || "").trim().toLowerCase();
  const i = RANG_LIGNES.indexOf(n);
  return i === -1 ? RANG_LIGNES.length : i;
}

/* Le code que Matis donne à une ligne (E1, W3, HESSAPP) — le pont avec son
   classeur. Déduit du nom, jamais stocké en double. */
function codeLigneDe(nom) {
  const n = String(nom || "").trim().toUpperCase();
  const m = /^EMAG\s*(\d+)$/.exec(n);
  if (m) return "E" + m[1];
  if (n.startsWith("HESSAP")) return "HESSAPP";
  const w = /^WEISSER\s*(\d+)$/.exec(n);
  if (w) return "W" + w[1];
  const p = /^PCI\s*(\d+)$/.exec(n);
  if (p) return "P" + p[1];
  return "";
}

/* ============================================================================
   10. LES PROJETS — étiquettes posées sur les scénarios (jamais propriétaires)
   ========================================================================== */

/* Palette cyclique partagée avec les outils de l'app 4.x : le mécanisme
   (index, modulo) est réutilisé, pas réinventé (CDC Projets v2 §0). */
const PALETTE_PROJETS = ["#3b82f6", "#14b8a6", "#a78bfa", "#f59e0b", "#22c55e", "#94a3b8", "#ec4899", "#0ea5e9"];

/* La couleur d'un projet est assignée UNE fois à sa création et stockée avec
   lui — jamais recalculée au rendu, sinon les couleurs sautent d'une session
   à l'autre (CDC Projets v2 §7). */
function couleurProjetLibre(etat) {
  const prises = {};
  ((etat && etat.projets) || []).forEach(p => { if (p && p.couleur) prises[p.couleur] = true; });
  for (let i = 0; i < PALETTE_PROJETS.length; i++) {
    if (!prises[PALETTE_PROJETS[i]]) return PALETTE_PROJETS[i];
  }
  return PALETTE_PROJETS[((etat && etat.projets) || []).length % PALETTE_PROJETS.length];
}

/* Les scénarios d'un projet : parcours des étiquettes, résolues contre
   l'arbre. Une étiquette orpheline (scénario supprimé) est signalée, pas
   silencieusement oubliée. */
function scenariosDeProjet(etat, projet) {
  const out = [], orphelins = [];
  ((projet && projet.tags) || []).forEach(tag => {
    const ligne = ((etat.lignes) || []).find(l => l.id === tag.ligneId);
    const ref = ligne ? ((ligne.references) || []).find(r => r.id === tag.referenceId) : null;
    const op = ref ? ((ref.ops) || []).find(o => o.id === tag.opId) : null;
    const sc = op ? ((op.scenarios) || []).find(s => s.id === tag.scenarioId) : null;
    if (sc) out.push({ ligne: ligne, ref: ref, op: op, sc: sc, tag: tag });
    else orphelins.push(tag);
  });
  return { lies: out, orphelins: orphelins };
}

/* Les projets qui touchent un scénario donné. */
function projetsDeScenario(etat, ligneId, referenceId, opId, scenarioId) {
  return ((etat.projets) || []).filter(pj =>
    ((pj.tags) || []).some(t => t.ligneId === ligneId && t.referenceId === referenceId
      && t.opId === opId && t.scenarioId === scenarioId));
}

/* Le résumé « 2 projets sur cet OP » (CDC Projets v2 §1.4) — un affichage,
   aucun changement de modèle. */
function projetsDeOP(etat, ligneId, referenceId, opId) {
  return ((etat.projets) || []).filter(pj =>
    ((pj.tags) || []).some(t => t.ligneId === ligneId && t.referenceId === referenceId && t.opId === opId));
}

const PROJET_STATUTS = { encours: "En cours", pause: "En pause", termine: "Terminé", abandonne: "Abandonné" };

/* Le responsable d'un projet, résolu contre la liste gérée. La suppression
   d'un responsable renvoie les projets à « aucun responsable », jamais
   l'inverse (CDC Projets v2 §2.2). */
function responsableDe(etat, projet) {
  if (!projet) return null;
  return ((etat.responsables) || []).find(r => r.id === projet.responsableId) || null;
}

/* ============================================================================
   11. LES LIVRAISONS — l'instantané figé que la hiérarchie lit
   ========================================================================== */

/* Une livraison fige les chiffres du jour : elle ne se recalcule JAMAIS
   après coup — c'est tout son intérêt (document qui ne bouge plus). */
function capturerLivraison(etat, nom, auteur) {
  const rec = recapAtelier(etat.lignes || []);
  return {
    id: uid("lv"),
    nom: nom || ("Livraison du " + dateCourte()),
    date: new Date().toISOString(),
    creePar: auteur || "",
    gainsActes: rec.gainActe,
    gainsEnCours: rec.gainProjete,
    gainAnnuelActe: rec.gainAnnuelActe,
    gainAnnuelProjete: rec.gainAnnuelProjete,
    decisions: rec.decisions,
    aChiffrer: rec.aChiffrer,
    plan: rec.tuiles.map(t => ({
      ligne: t.nom,
      code: t.code,
      cpp: t.cpp,
      cible: t.cible,
      distance: t.distanceCible,
      decisions: t.decisions,
      aChiffrer: t.aChiffrer,
      dominante: t.dominante ? t.dominante.ref.nom : null
    })),
    toolVersion: VERSION
  };
}

/* ============================================================================
   12. OUTILS DIVERS — ids, dates, clés de rapprochement
   ========================================================================== */

function uid(prefix) {
  return (prefix || "x") + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

function dateCourte(d) {
  const t = d ? new Date(d) : new Date();
  if (isNaN(t.getTime())) return "";
  const pad = n => (n < 10 ? "0" : "") + n;
  return pad(t.getDate()) + "/" + pad(t.getMonth() + 1) + "/" + t.getFullYear();
}

function dateHeure(d) {
  const t = d ? new Date(d) : new Date();
  if (isNaN(t.getTime())) return "";
  const pad = n => (n < 10 ? "0" : "") + n;
  return dateCourte(t) + " " + pad(t.getHours()) + ":" + pad(t.getMinutes());
}

/* La clé de rapprochement d'un porte-outil (loi du correcteur, interdit 2) :
   `T 513 D1` et `T513 D1` sont le MÊME outil — la clé ignore espaces, tirets
   et points, en majuscules. L'affichage garde la forme de l'atelier. */
function clePorteOutil(numero) {
  return String(numero || "").toUpperCase().replace(/[\s\-.]/g, "");
}
