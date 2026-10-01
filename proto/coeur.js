/* ============================================================================
   PROTO — LE NOYAU
   Fonctions PURES. Aucun DOM, aucun état global, aucune lecture de l'app.
   Ce fichier est écrit et testé AVANT le moindre écran (cahier §5).

   Le CPP plaquettes est le driver (cahier §2) :
     coutOutillage(logements) = Σ prix / (arêtes × charnière)
   C'est le seul chiffre comparable au classeur de Matis.

   Toute absence dit ce qui manque (cahier §4.4). Aucun « — » nu.
   ========================================================================== */

const PROTO_VERSION = "0.1";

/* ---- le formatage, pur lui aussi ---- */
function fmt(v, d) {
  if (v === null || v === undefined || v === "" || isNaN(parseFloat(v))) return "—";
  const n = parseFloat(v);
  return n.toFixed(d === undefined ? 3 : d).replace(".", ",");
}
/* la même chose, mais en gardant le nombre si la saisie est un champ vide :
   utilisé quand on veut distinguer « 0 » de « pas saisi » */
function fmtDispo(v, d, manque) {
  if (v === null || v === undefined || v === "") return manque || "— non saisi";
  if (isNaN(parseFloat(v))) return manque || "— non saisi";
  return fmt(v, d);
}

/* ============================================================================
   1. LE CPP OUTILLAGE — le driver
   ========================================================================== */

/* Le coût d'UN logement : prix de la plaquette divisé par ce qu'elle rend.
   Le prix est en €, les arêtes en nombre d'arêtes, la charnière en pièces.
   -> € par pièce usinée.
   Une donnée manquante ne donne pas 0 : elle donne null (non chiffrable). C'est
   l'invariant 1 du cahier : un absent ne se comble jamais. */
function coutLogement(log) {
  if (!log) return null;
  const prix = parseFloat(log.prix);
  const aretes = parseFloat(log.aretes);
  const charniere = parseFloat(log.charniere);
  if (isNaN(prix) || prix <= 0) return null;
  if (isNaN(aretes) || aretes <= 0) return null;
  if (isNaN(charniere) || charniere <= 0) return null;
  return prix / (aretes * charniere);
}

/* Le CPP outillage d'un scénario = la somme sur TOUS ses logements.
   Le CPP outillage d'un outil, de la même façon. */
function cppOutillageScenario(scenario) {
  if (!scenario || !scenario.outils) return null;
  const parts = [];
  scenario.outils.forEach(o => {
    (o.logements || []).forEach(l => {
      const c = coutLogement(l);
      if (c !== null) parts.push(c);
    });
  });
  if (!parts.length) return null;
  return parts.reduce((a, b) => a + b, 0);
}

function cppOutillageOutil(outil) {
  if (!outil || !outil.logements) return null;
  const parts = (outil.logements || []).map(coutLogement).filter(v => v !== null);
  if (!parts.length) return null;
  return parts.reduce((a, b) => a + b, 0);
}

/* Les CPP par logement, pour l'écran Décision (où part l'argent). */
function cppParLogement(scenario) {
  const out = [];
  (scenario.outils || []).forEach(o => {
    (o.logements || []).forEach(l => {
      out.push({
        outilNumero: o.numero || "?",
        logementNom: l.nom || "?",
        article: l.ref || "",
        cpp: coutLogement(l),
        prix: parseFloat(l.prix),
        aretes: parseFloat(l.aretes),
        charniere: parseFloat(l.charniere)
      });
    });
  });
  return out;
}

/* ============================================================================
   2. LE CHEMIN PROD → CIBLE
   ========================================================================== */

/* Combien de chemin a fait le meilleur essai disponible vers la cible CPP ?
   (cahier §4.3 : une cible sans chiffrage reste visible, elle ne disparaît pas)
   Renvoie null si on ne peut pas calculer — et l'appelant affiche pourquoi. */
function cheminCPP(coutProd, coutMeilleur, cible) {
  if (cible === null || cible === undefined || isNaN(parseFloat(cible))) return null;
  if (isNaN(coutProd) || isNaN(coutMeilleur)) return null;
  const c = parseFloat(cible);
  const p = parseFloat(coutProd);
  const m = parseFloat(coutMeilleur);
  // déjà en dessous de la cible : le chemin est fait, 100 %
  if (p <= c) return 100;
  if (p <= 0) return null;
  const pct = ((p - m) / (p - c)) * 100;
  return Math.max(0, Math.min(100, pct));
}

/* ============================================================================
   3. LA PREUVE — conformité, charnière, répétitions
   ========================================================================== */

/* Un prélèvement est-il dans la tolérance ? null = « non mesurable », jamais false.
   (cahier §4.1 : un absent ne se comble pas, il se signale) */
function conforme(sc, prel) {
  if (!prel) return null;
  if (sc && sc.battActif === false) return true;   // critère volontairement désactivé
  const limit = sc && sc.limitOverride ? parseFloat(sc.limitValue) : parseFloat(0.12);
  if (isNaN(limit)) return null;
  const b = parseFloat(prel.batt);
  if (isNaN(b)) return null;
  return b <= limit;
}

/* La charnière visée d'un logement (pour un essai donné). */
function charniereVisee(scenario, essai, logementId) {
  const liste = (essai && essai.params && essai.params.logements) || [];
  const trouve = liste.find(p => p.logementId === logementId);
  if (trouve) {
    const v = parseFloat(trouve.charniere);
    if (!isNaN(v)) return v;
  }
  // repli : la charnière du logement dans le scénario
  let out = null;
  (scenario.outils || []).forEach(o => (o.logements || []).forEach(l => {
    if (l.id === logementId) {
      const v = parseFloat(l.charniere);
      if (!isNaN(v)) out = v;
    }
  }));
  return out;
}

/* Le statut d'un ESSAI : conforme / non conforme / arrêté / en cours.
   L'ordre est délibéré — un arrêt est une décision, pas un échec (§ essaiStats). */
function statutEssai(sc, essai) {
  if (!essai) return { code: "vide", texte: "aucun essai" };
  const prels = essai.prelevements || [];
  if (essai.cloture && essai.cloture.motif) {
    return { code: "arrete", texte: "arrêté — " + (essai.cloture.motif || "sans motif") };
  }
  const mesures = prels.map(p => conforme(sc, p));
  const evalues = mesures.filter(v => v !== null);
  if (!prels.length) return { code: "attente", texte: "aucun prélèvement" };
  if (evalues.some(v => v === false)) {
    const premier = prels[mesures.indexOf(false)];
    return {
      code: "nonconforme",
      texte: "hors tolérance",
      piece: premier ? parseFloat(premier.piece) : null
    };
  }
  const manquantes = prels.length - evalues.length;
  // la charnière : chaque logement suivi doit être atteint
  const suivis = (essai.params && essai.params.logements) || [];
  const restants = [];
  suivis.forEach(p => {
    const cible = charniereVisee(sc, essai, p.logementId);
    if (isNaN(cible) || cible === null) return;
    const pieces = prels.map(x => parseFloat(x.piece)).filter(v => !isNaN(v));
    const derniere = pieces.length ? Math.max(...pieces) : null;
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
      texte: restants.map(r => r.logementNom + " " + r.dernier + "/" + r.cible).join(" · ") + " p"
    };
  }
  if (manquantes > 0) {
    return { code: "attente", texte: manquantes + " mesure" + (manquantes > 1 ? "s" : "") + " à saisir" };
  }
  return { code: "conforme", texte: "conforme — charnière atteinte" };
}

/* Le statut d'un SCÉNARIO : c'est le verdict de la décision (écran 4).
   séries = validé en prod, valide = validé 5× mais pas encore en prod. */
function statutScenario(sc) {
  const essais = sc.essais || [];
  const verdi = essais.map(e => statutEssai(sc, e));
  if (sc.statut === "serie") return { code: "serie", texte: "en série" };
  const conformes = verdi.filter(v => v.code === "conforme").length;
  if (conformes >= (sc.validationThreshold || 5)) {
    return { code: "valide", texte: "validé 5× — à passer en série", validations: conformes };
  }
  if (essais.length) return { code: "encours", texte: "essai en cours", validations: conformes };
  return { code: "opportunite", texte: "rien d'essayé" };
}

/* ============================================================================
   4. LE VERDICT D'UN POSTE — ce que l'écran 1 montre, et l'écran 4 tranche
   ========================================================================== */

/* Un poste = une opération sur une ligne. Il a une prod (scénario de base),
   peut-être des essais, et une cible CPP du site.
   Renvoie tout ce dont les écrans ont besoin — mais le CALCUL est ici, jamais
   dans le rendu (cahier §5). */
function verdictPoste(ref, op, scenarios) {
  const scs = scenarios || (op && op.scenarios) || [];
  const prod = scs.find(s => s.baseline) || scs.find(s => /base excel/i.test(s.name || ""));
  const cppProd = prod ? cppOutillageScenario(prod) : null;
  const cible = ref && ref.cibleCPP !== "" && ref.cibleCPP != null && !isNaN(parseFloat(ref.cibleCPP))
    ? parseFloat(ref.cibleCPP) : null;

  // le MEILLEUR essai disponible : celui dont le CPP outillage est le plus bas
  let meilleur = null;
  scs.forEach(s => {
    if (prod && s.id === prod.id) return;
    const cpp = cppOutillageScenario(s);
    if (cpp === null) return;
    if (!meilleur || cpp < meilleur.cpp) meilleur = { sc: s, cpp: cpp };
  });

  const chemin = (cppProd !== null && meilleur) ? cheminCPP(cppProd, meilleur.cpp, cible) : null;

  // le statut de la décision
  let verdict;
  const sMeilleur = meilleur ? statutScenario(meilleur.sc) : null;
  if (!prod || cppProd === null) {
    verdict = { code: "achiffrer", texte: cible !== null ? "cible connue, à chiffrer" : "à chiffrer" };
  } else if (sMeilleur && sMeilleur.code === "serie") {
    verdict = { code: "gagne", texte: "gagné — en série" };
  } else if (sMeilleur && sMeilleur.code === "valide") {
    verdict = { code: "pret", texte: "validé 5× — décision à prendre" };
  } else if (meilleur && meilleur.cpp < cppProd) {
    verdict = { code: "essai", texte: "essai prometteur" };
  } else {
    verdict = { code: "rien", texte: "rien à faire ici" };
  }

  // le gain CPP, JAMAIS fusionné avec un autre (§3.4 du cahier) :
  //  - gainProjete : le meilleur essai disponible, pas encore acté
  //  - gainActe : ce qui est réellement passé en série
  let gainProjete = null, gainActe = null;
  if (cppProd !== null && meilleur && meilleur.cpp < cppProd) {
    gainProjete = cppProd - meilleur.cpp;
  }
  const enSerie = scs.filter(s => s.statut === "serie");
  if (cppProd !== null && enSerie.length) {
    const cppSerie = cppOutillageScenario(enSerie[0]);
    if (cppSerie !== null && cppSerie < cppProd) gainActe = cppProd - cppSerie;
  }

  return {
    ref, op, prod, cppProd, cible, chemin,
    meilleur, gainProjete, gainActe, verdict
  };
}

/* Le verdict d'une LIGNE : le CPP outillage total de la prod, et le chemin vers la cible.
   C'est la somme des postes CHIFFRABLES seulement — une OP non chiffrable est
   comptée à part, elle ne se dilue pas dans le total (§3.2 de la constitution). */
function verdictLigne(ligne, postes) {
  let cppProd = 0, cppActe = 0, cppProjete = 0;
  let nonChiffrables = 0, enAttente = 0;
  const liste = [];
  (postes || []).forEach(p => {
    const v = verdictPoste(p.ref, p.op, p.scenarios);
    liste.push(v);
    if (v.cppProd === null) { nonChiffrables++; return; }
    cppProd += v.cppProd;
    if (v.gainActe) cppActe += v.gainActe;
    else if (v.gainProjete) cppProjete += v.gainProjete;
    if (v.verdict.code === "essai") enAttente++;
  });
  return {
    ligne, postes: liste,
    cppProd: cppProd || null,
    cppActe: cppActe || 0,
    cppProjete: cppProjete || 0,
    nonChiffrables, enAttente
  };
}

/* ============================================================================
   5. LA DÉCISION — l'écran 4, en une phrase
   ========================================================================== */

/* Que fait-on de ce poste ? Un seul mot, pour qu'on puisse le lire en 15 s. */
function decisionPoste(v) {
  if (!v) return { mot: "—", pourquoi: "" };
  switch (v.verdict.code) {
    case "gagne":
      return { mot: "SÉRIE", pourquoi: "l'essai est passé en production" };
    case "pret":
      return {
        mot: "DÉCIDER",
        pourquoi: "validé " + (v.verdict.validations || 5) + " fois — il reste à dire oui ou non"
      };
    case "essai":
      return {
        mot: "ESSAYER",
        pourquoi: "l'essai gagne " + fmt(v.gainProjete, 4) + " €/pièce — à confirmer sur " +
                   ((v.meilleur && v.meilleur.sc.validationThreshold) || 5) + " pièces"
      };
    case "achiffrer":
      return { mot: "CHIFFRER", pourquoi: v.verdict.texte };
    default:
      return { mot: "RIEN", pourquoi: "aucun essai ne fait mieux que la prod" };
  }
}

/* ============================================================================
   6. LE RÉCAPITULATIF — l'écran 1 en un objet
   ========================================================================== */

/* Les quatre chiffres du bandeau. Chacun remonte à sa source, et une absence
   dit ce qui manque (invariant 4). */
function recapLignes(verdictsLignes) {
  let cppActe = 0, cppProjete = 0, aChiffrer = 0;
  verdictsLignes.forEach(vl => {
    cppActe += vl.cppActe;
    cppProjete += vl.cppProjete;
    vl.postes.forEach(p => { if (p.verdict.code === "achiffrer") aChiffrer++; });
  });
  /* « À décider » = tout ce qui attend une action : un validé 5× à confirmer, ou un
     essai prometteur à confirmer. Compter seulement les validés 5× donnait « 0 » alors
     que l'écran regorge d'appels à l'action — et un 0 lu comme « rien à faire » est un
     mensonge (§3.5).
     Les codes de verdict sont en ASCII ("pret", pas "prêt") : l'accent ici faisait
     échouer la comparaison en silence et le compte restait à zéro. */
  const decisions = verdictsLignes.reduce((a, vl) =>
    a + vl.postes.filter(p => p.verdict.code === "pret" || p.verdict.code === "essai").length, 0);
  return {
    cppActe,          // €/pièce déjà gagnés, actés en série
    cppProjete,       // €/pièce prometteurs, pas encore actés
    aChiffrer,        // combien de postes sans chiffrage malgré une cible
    decisions         // combien de postes attendent une action de l'atelier
  };
}