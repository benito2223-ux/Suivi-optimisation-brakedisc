/* ============================================================================
   PROTO — LE NOYAU
   Fonctions PURES. Aucun DOM, aucun état global, aucune lecture de l'app.
   Ce fichier est écrit et testé AVANT le moindre écran (cahier §5).

   Le CPP plaquettes est le driver (cahier §2) :
     coutOutillage(logements) = Σ prix / (arêtes × charnière)
   C'est le seul chiffre comparable au classeur de Matis.

   Toute absence dit ce qui manque (cahier §4.4). Aucun « — » nu.
   ========================================================================== */

const PROTO_VERSION = "2.0";

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

/* Le CPP RÉELLEMENT OBTENU par un essai — le prix et les arêtes viennent de la
   définition du logement dans le scénario, la charnière de l'essai lui-même.
   C'est le seul endroit où « ce qu'on a prévu » et « ce qu'on a obtenu » se
   séparent : sans cette fonction, un essai qui tient mieux que prévu ne se voit
   nulle part, et un réimport des essais existants ne rendrait RIEN.

   Invariant 3 : un logement non chiffrable est COMPTE, pas dilué. On renvoie
   donc le total des chiffrables ET le nombre de ceux qui ont été écartés. */
function cppEssai(scenario, essai) {
  const vide = { cpp: null, nbLogements: 0, nonChiffrables: 0 };
  if (!scenario || !essai) return vide;
  const definition = {};                       // logementId -> { prix, aretes }
  (scenario.outils || []).forEach(o => (o.logements || []).forEach(l => {
    definition[l.id] = l;
  }));
  const suivis = (essai.params && essai.params.logements) || [];
  if (!suivis.length) return vide;
  let total = 0, n = 0, ecartes = 0;
  suivis.forEach(p => {
    const def = definition[p.logementId];
    // le prix et les arêtes peuvent aussi être portés par le prélèvement lui-même
    const prix = def && def.prix !== "" && def.prix != null ? def.prix : p.prix;
    const aretes = def && def.aretes !== "" && def.aretes != null ? def.aretes : p.aretes;
    const charniere = (p.charniere !== "" && p.charniere != null)
      ? p.charniere : (def ? def.charniere : null);
    const c = coutLogement({ prix: prix, aretes: aretes, charniere: charniere });
    if (c === null) { ecartes++; return; }
    total += c; n++;
  });
  return {
    cpp: n ? total : null,
    nbLogements: n,
    nonChiffrables: ecartes
  };
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

/* La battement d'un prélèvement. Deux government's selon les mesures :
   EMAG 1 relève DROITE et GAUCHE séparément, l'app ancienne ne remplit `batt`
   que pour les autres scénarios. Sur les données du site, `batt` est vide sur
   83 prélèvements sur 84 — et `battD`/`battG` sont pleines.

   On prend donc `batt` si elle existe, sinon LE PIRE des deux côtés. Le pire,
   pas la moyenne : un état des lieux ne doit jamais flatter une pièce qui
   déborde d'un côté. C'est la seule règle qui ne perd aucune mesure et qui ne
   peut pas rendre conforme ce qui ne l'est pas. */
function battDe(prel) {
  if (!prel) return NaN;
  const b = parseFloat(prel.batt);
  if (!isNaN(b)) return b;
  const cotes = [parseFloat(prel.battD), parseFloat(prel.battG)].filter(v => !isNaN(v));
  if (!cotes.length) return NaN;
  return Math.max.apply(null, cotes);
}

/* Un prélèvement est-il dans la tolérance ? null = « non mesurable », jamais false.
   (cahier §4.1 : un absent ne se comble pas, il se signale) */
function conforme(sc, prel) {
  if (!prel) return null;
  if (sc && sc.battActif === false) return true;   // critère volontairement désactivé
  const limit = sc && sc.limitOverride ? parseFloat(sc.limitValue) : parseFloat(0.12);
  if (isNaN(limit)) return null;
  const b = battDe(prel);
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

/* ============================================================================
   7. LE RÉFÉRENTIEL DES LIGNES — quatre familles, quatre couleurs
   ============================================================================ */

/* Benjamin, à l'atelier : « Weisser Rouge, Emag Gris, Hessapp vert, PCI bleu ».
   Ces quatre familles EXISTENT déjà dans l'app de production (référentiel
   LIGNES_SEPT_FONS, Tour 50 du proto) — on le porte tel quel, pas on le
   réinvente. Les couleurs ne sont pas dans les données : elles sont dans le
   code, et c'est le bon endroit, parce qu'elles sont un fait d'atelier et pas
   une mesure. */
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

/* L'ordre physique de l'atelier, du fond vers l'entrée (fait d'atelier, pas un
   tri alphabétique). Une ligne inconnue se range après le référentiel, jamais
   avant : une ligne hors nomenclature ne doit pas passer devant Weisser. */
const RANG_LIGNES = [
  "weisser 1", "weisser 2", "weisser 3", "weisser 4",
  "hessapp", "emag 1", "emag 2", "emag 3", "pci 1", "pci 2", "pci 3", "pci 4"
];
function rangLigne(nom) {
  const n = String(nom || "").trim().toLowerCase();
  const i = RANG_LIGNES.indexOf(n);
  return i === -1 ? RANG_LIGNES.length : i;
}

/* Le code que Matis donne à une ligne (E1, E2, E3, HESSAPP). C'est ce code qui
   fait le pont avec le classeur : les feuilles s'appellent « Coût pièce E1 … ».
   On le déduit du NOM, jamais stocké en double — deux sources pour un fait,
   c'est une source de désaccord. */
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
   8. LES POSTES, LA TUILE ET LE DÉTAIL — les deux premiers étages
   ============================================================================ */

/* Quel est le scénario EN PRODUCTION d'une opération ?
   L'app de production exige `baseline === true` ET `statut === "serie"`. On
   reprend cet ordre de recherche, du plus sûr au plus douteux :
     1. le scénario marqué baseline
     2. à défaut, celui qui est en série (l'app les tient verrouillés ensemble,
        mais un export ancien peut n'avoir qu'un des deux)
     3. à défaut, celui dont le nom dit « base excel » — c'est le fallback que
        l'app utilise déjà pour les lignes importées d'un classeur.
   Jamais « le premier de la liste » : sans règle explicite, deux scénarios
   equally claimed would silently pick one. */
function scenarioDeProd(scs) {
  const liste = scs || [];
  return liste.find(s => s && s.baseline === true)
      || liste.find(s => s && s.statut === "serie")
      || liste.find(s => s && /base excel/i.test(s.name || ""))
      || null;
}

/* Les postes d'une ligne : une opération sur une référence, avec son scénario
   de production. C'est la structure du DÉTAIL (étage 2) — et la tuile s'y
   branche au lieu de recalculer sa propre version. */
function postesDeLigne(ligne) {
  const out = [];
  ((ligne && ligne.refs) || []).forEach(ref => {
    ((ref && ref.ops) || []).forEach(op => {
      const scs = op.scs || [];
      const prod = scenarioDeProd(scs);       // UN SEUL calcul, réutilisé
      out.push({
        ref: ref,
        op: op,
        scs: scs,
        prod: prod,
        autres: prod ? scs.filter(s => s && s !== prod) : scs.filter(Boolean)
      });
    });
  });
  return out;
}

/* Le CPP outillage d'une RÉFÉRENCE : la somme sur ses postes, en ne gardant que
   les postes chiffrables — et en COMPTANT les autres. Invariant 3 : un poste non
   chiffrable ne se dilue pas dans le total, il se dit.

   `distanceCible` est l'écart brut au-dessus de la cible, en €/pièce. On ne calcule
   PAS de pourcentage de « chemin » ici : `cheminCPP` a besoin du MEILLEUR essai
   disponible, et à l'étage 1 il n'y en a pas de calculé — lui passer null
   donnerait un pourcentage qui ne repose sur rien. Le pourcentage reste réservé
   à l'étage 3, où l'on sait enfin de quel essai on parle. */
function cppReference(ligne, ref) {
  const postes = postesDeLigne(ligne).filter(p => p.ref.id === ref.id);
  let total = 0, chiffres = 0, nonChiffrables = 0, sansScenario = 0;
  postes.forEach(p => {
    if (!p.prod) { sansScenario++; nonChiffrables++; return; }
    const c = cppOutillageScenario(p.prod);
    if (c === null) { nonChiffrables++; return; }
    total += c; chiffres++;
  });
  const cpp = chiffres ? total : null;
  const cible = (ref && ref.cibleCPP !== "" && ref.cibleCPP != null
                 && !isNaN(parseFloat(ref.cibleCPP))) ? parseFloat(ref.cibleCPP) : null;
  const distanceCible = (cpp !== null && cible !== null) ? cpp - cible : null;
  return {
    ref: ref,
    cpp: cpp,
    nbPostes: postes.length,
    chiffres: chiffres,
    nonChiffrables: nonChiffrables,
    sansScenario: sansScenario,
    cible: cible,
    distanceCible: distanceCible
  };
}

/* LA TUILE — l'étage 1. Une tuile par ligne de production, et rien d'autre que
   ce qu'un chef d'atelier regarde en passant : la référence en production, son
   CPP outillage actuel, et où il se situe par rapport à la cible.

   Ce qui n'y est PAS, et pourquoi — c'est écrit ici pour qu'on ne le relogue
   pas dans trois mois sans s'en souvenir :
     · la production hebdomadaire. Décision de Benjamin le 02/10/2026 : elle est
       détaillée par lot de lignes, donc elle ne parle pas d'un poste d'outillage.
       L'accueil n'affiche donc ni cadence, ni cumul, ni taux d'atteinte.
     · le delta théorie/réalité. Il exige le classeur de Matis, qui n'est pas
       encore branché (Tour 56). La tuile le DIT au lieu de l'inventer.
     · un coût partiel présenté comme un coût complet. Une opération non
       chiffrable est comptée, et la tuile l'annonce sous le chiffre. */
function tuileDeLigne(ligne) {
  const famille = familleDeLigne(ligne && ligne.nom);
  const refs = ((ligne && ligne.refs) || []).map(r => cppReference(ligne, r));
  const chiffres = refs.filter(r => r.cpp !== null);
  /* Les postes non chiffrables se comptent sur TOUTES les références, pas
     seulement sur celles qui ont un CPP. Le premier jet sommait `nonChiffrables`
     dans la boucle des références chiffrables : une référence dont AUCUN poste
     n'est chiffrable verrait ses postes non chiffrables disparaître du compte —
     exactement le silence que l'invariant 3 interdit. Le total, lui, ne prend
     que ce qui est chiffrable. */
  let cppLigne = 0, nonChiffrables = 0, sansScenario = 0;
  refs.forEach(r => {
    if (r.cpp !== null) cppLigne += r.cpp;
    nonChiffrables += r.nonChiffrables;
    sansScenario += r.sansScenario;
  });

  /* La référence en production : celle qui a le plus de postes chiffrés. En cas
     d'égalité, la première dans l'ordre du fichier — jamais un tri par nom,
     qui ferait jumping d'une tuile à l'autre d'une version à l'autre. */
  let dominante = null;
  chiffres.forEach(r => {
    if (!dominante || r.chiffres > dominante.chiffres) dominante = r;
  });

  return {
    ligne: ligne,
    nom: (ligne && ligne.nom) || "Ligne sans nom",
    famille: famille,
    encre: famille ? FAMILLES_LIGNE[famille].encre : "#545e68",
    code: codeLigneDe(ligne && ligne.nom),
    rang: rangLigne(ligne && ligne.nom),
    refs: refs,
    dominante: dominante,
    cpp: chiffres.length ? cppLigne : null,
    nbRefs: refs.length,
    nbChiffres: chiffres.length,
    nonChiffrables: nonChiffrables,
    sansScenario: sansScenario,
    vide: refs.length === 0
  };
}

/* Les tuiles, dans l'ordre de l'atelier. */
function tuilesDeLignes(lignes) {
  return (lignes || []).map(tuileDeLigne)
    .sort((a, b) => a.rang - b.rang || a.nom.localeCompare(b.nom));
}

/* LE DÉTAIL — l'étage 2. Une ligne, ses références, ses opérations, et POUR LE
   SCÉNARIO DE PRODUCTION SEUL. C'est une règle de lecture, pas une limitation :
   les autres scénarios existent et sont comptés, mais l'étage 2 ne les montre
   pas — ils sont l'objet de l'étage 3. Une exception : si une opération n'a
   AUCUN scénario de production, elle est quand même montrée, marquée « aucun
   scénario en production » — sinon une opération vide disparaîtrait de l'écran
   et l'agent croirait la ligne complète. */
function detailLigne(ligne) {
  const postes = postesDeLigne(ligne);
  const parRef = [];
  ((ligne && ligne.refs) || []).forEach(ref => {
    const siens = postes.filter(p => p.ref.id === ref.id);
    if (!siens.length) return;
    const c = cppReference(ligne, ref);
    parRef.push({
      ref: ref,
      nom: ref.nom || "Référence sans nom",
      cpp: c.cpp,
      cible: c.cible,
      distanceCible: c.distanceCible,
      nonChiffrables: c.nonChiffrables,
      postes: siens.map(p => ({
        op: p.op,
        code: p.op.code || p.op.nom || "OP",
        nom: p.op.nom || "",
        prod: p.prod,
        cpp: p.prod ? cppOutillageScenario(p.prod) : null,
        outillage: p.prod ? outillageDeScenario(p.prod) : null,
        essais: p.prod ? (p.prod.essais || []).length : 0,
        nbAutres: p.autres.length
      }))
    });
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

/* L'outillage d'un scénario, décomposé : outil par outil, logement par
   logement. C'est ce que l'étage 2 montre sous chaque opération, et c'est la
   seule décomposition qui permet de voir OÙ part l'argent.

   Chaque outil porte SES logements, calculés sur place. Deux jet ont fait
   autrement et deux ont failli :
     · le premier passait par `cppParLogement(sc)`, qui perd l'identité de
       l'outil et ne rend que son numéro — la décomposition était donc fausse
       dès qu'un outil n'a pas de CPP ;
     · le deuxième regroupait les logements par numéro d'outil avant de les
       redistribuer : deux outils PORTAIENT le même numéro se retrouvaient donc
       dans le même seau, et le premier affichait les logements du second. Aucun
       export du site ne porte ce cas ; `test_tuiles.js` le fabrique exprès.
   Un seau par outil, et le seau se remplit en parcourant cet outil. */
function outillageDeScenario(sc) {
  if (!sc) return { outils: [], cpp: null, nonChiffrables: 0 };
  const outils = [];
  let total = 0, chiffres = 0, nonChiffrables = 0;
  (sc.outils || []).forEach(o => {
    const numero = o.numero || "?";
    const logements = (o.logements || []).map(l => {
      const cpp = coutLogement(l);
      if (cpp === null) nonChiffrables++;
      return {
        outilNumero: numero,
        logementNom: l.nom || "?",
        article: l.ref || "",
        cpp: cpp,
        prix: parseFloat(l.prix),
        aretes: parseFloat(l.aretes),
        charniere: parseFloat(l.charniere)
      };
    });
    const valeurs = logements.filter(x => x.cpp !== null).map(x => x.cpp);
    const cpp = valeurs.length ? valeurs.reduce((a, b) => a + b, 0) : null;
    if (cpp !== null) { total += cpp; chiffres++; }
    outils.push({
      numero: numero,
      description: o.description || "",
      correcteur: o.correcteur || "",
      cpp: cpp,
      logements: logements
    });
  });
  return {
    outils: outils,
    cpp: chiffres ? total : null,
    nonChiffrables: nonChiffrables
  };
}