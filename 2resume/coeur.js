/* ============================================================================
   2resume — LE NOYAU
   ----------------------------------------------------------------------------
   Fonctions PURES. Aucun DOM, aucun localStorage, aucun réseau, aucune horloge :
   tout ce qui se calcule se calcule ici, et se teste ici. Le rendu lit, il ne
   calcule rien (cahier §8).

   Deux règles de fabrication qui ont un prix, et que ce fichier paie volontairement :

   1. `coutLogement()` est le SEUL endroit où un coût de plaquette est calculé.
      Si une seconde formule apparaît un jour, c'est un bug : la constitution §3.1
      l'interdit, et la comparaison avec le classeur de Matis tient à ce que la
      formule soit unique, terme pour terme.

   2. Une absence n'est jamais un zéro. `nb()` renvoie `null` pour « pas saisi »,
      et tout l'outil raisonne sur ce `null` : un poste non chiffrable se DÉCLARE,
      il ne devient pas 0 (constitution §3.5).
   ========================================================================== */

const OUTIL_VERSION = "1.0.0";
const FORMAT_DONNEES = 9;

/* ── 1. LE RÉFÉRENTIEL ─────────────────────────────────────────────────────
   Ce qui est constant du site est déclaré ICI, une fois, avec sa source. Toute
   valeur affichée doit pouvoir remonter à l'une de ces lignes ou à une saisie
   de l'atelier. C'est la traduction en code de la règle §5.6 de la constitution
   (« un chiffre qu'on ne peut pas justifier n'est pas affiché »). */

const FAMILLES_LIGNE = {
  weisser: { libelle: "Weisser", encre: "#B30016" },
  hessapp: { libelle: "Hessapp", encre: "#556B2F" },
  emag:    { libelle: "EMAG",    encre: "#545E68" },
  pci:     { libelle: "PCI",     encre: "#1B5EA6" }
};
const ORDRE_FAMILLES = ["weisser", "hessapp", "emag", "pci"];

/* L'ordre de l'atelier. Toute ligne absente de cette liste passe en queue : on ne
   trie JAMAIS par nom, sinon une tuile change de place d'une version à l'autre
   et l'agent cherche sa machine. Le proto s'arrêtait à PCI 4 alors que le site
   a un PCI 5 : toute ligne hors liste est donc rejetée par un test. */
const RANG_LIGNES = [
  "weisser 1", "weisser 2", "weisser 3", "weisser 4",
  "hessapp", "emag 1", "emag 2", "emag 3",
  "pci 1", "pci 2", "pci 3", "pci 4", "pci 5"
];

/* Les seuils du site. Ce sont les SEULS seuils : aucun nombre magique dans le
   rendu. Une valeur relevée dans l'atelier et pas validée ici n'est pas un
   seuil, c'est une mesure. */
const SEUILS = {
  battementDefaut: 0.12,     /* mm — tolérance de battement d'un disque */
  raDefaut: 0.8,             /* µm — rugosité cible */
  validations: 5,            /* le protocole du site : 5 essais conformes */
  partCoupante: 100,         /* % du cycle réellement en coupe */
  ecartCharniere: 0.5,       /* µm — tolérance sur l'épaisseur visée */
  cycleRefSec: 42            /* s — cycle de référence quand rien n'est saisi */
};

/* Les statuts d'un scénario. Le code ne parle JAMAIS en majuscules : les clés
   sont en ASCII, parce qu'un accent dans une clé de comparaison a déjà coûté un
   compteur qui restait à zéro sans jamais lever le moindre signal. */
const STATUTS = ["etude", "essai", "valide", "serie", "abandonne"];
const STATUT_LABELS = {
  etude: "à l'étude", essai: "en essai", valide: "validé",
  serie: "en production", abandonne: "abandonné"
};
const MOTIFS_ARRET = ["casse", "horsTolerance", "brut", "machine", "autre"];
const MOTIF_LABELS = {
  casse: "casse / éclat d'arête", horsTolerance: "hors tolérance",
  brut: "problème de brut", machine: "incident machine", autre: "autre"
};
const USURE_LABELS = { ok: "OK", limite: "usure limite", changer: "à changer" };

/* Les quatre postes de coût de la pièce. `comparable` = comparable à la colonne I
   du classeur de Matis. Un seul l'est ; c'est écrit ici, une fois, pour que
   personne n'additionne jamais un total d'outil à une cible du classeur
   (constitution §2 quater §3). */
const COUT_POSTES = [
  { cle: "plaquettes", libelle: "Plaquettes", comparable: true },
  { cle: "temps", libelle: "Temps machine", comparable: false },
  { cle: "rebut", libelle: "Rebut", comparable: false },
  { cle: "pieces", libelle: "Pièces détachées", comparable: false }
];

/* ── 2. LES PRIMITIVES ────────────────────────────────────────────────────── */

/* Le seul convertisseur du fichier. `""`, null, undefined, "abc", 0 et NaN
   rentrent tous par la même porte et en sortent en `null` — sauf 0, qui est un
   nombre valide et reste 0. Un prix à 0 n'est pas une absence ; il faut dire
   « prix non saisi » séparément quand c'est 0 qu'on veut, parce que les deux
   veulent dire des choses différentes. */
function nb(v) {
  if (v === null || v === undefined || v === "" || typeof v === "boolean") return null;
  const n = parseFloat(v);
  return isNaN(n) ? null : n;
}

/* Un nombre strictement positif : les trois facteurs d'un CPP le sont tous. */
function pos(v) {
  const n = nb(v);
  return (n === null || n <= 0) ? null : n;
}

/* L'arrondi DECIMAL, pas binaire. `toFixed` arrondit la valeur TELLE QUE
   stockée en IEEE754 : 3,5/80 = 0,04375 exactement en décimal, mais le double
   le plus proche est légèrement EN DESSOUS, et toFixed(4) affichait 0,0437 —
   le juge visuel l'a vu (2 × 0,0437 ne faisait pas le total affiché 0,0875).
   L'epsilon relatif ne déplace que les vraies égalités décimales : il ne peut
   pas faire franchir une frontière à une valeur qui en est vraiment éloignée. */
function arrondiDec(n, d) {
  return (n + n * 1e-12).toFixed(d);
}

function fmt(v, d) {
  const n = nb(v);
  if (n === null) return "—";
  return arrondiDec(n, d === undefined ? 3 : d).replace(".", ",");
}

function fmtEuro(v, d) {
  const n = nb(v);
  if (n === null) return "—";
  return arrondiDec(n, d === undefined ? 4 : d).replace(".", ",") + " €";
}

function fmtEnt(v) {
  const n = nb(v);
  if (n === null) return "—";
  return Math.round(n).toLocaleString("fr-FR");
}

function pct(v, d) {
  const n = nb(v);
  if (n === null) return "—";
  return (n * 100).toFixed(d === undefined ? 0 : d).replace(".", ",") + " %";
}

/* Un affichage qui n'invente rien : quand la valeur manque, on écrit POURQUOI.
   C'est l'invariant 4 du cahier, et il se joue ici, à un seul endroit. */
function dispo(v, d, manque) {
  const n = nb(v);
  return n === null ? (manque || "— non saisi") : fmt(n, d);
}

/* ── 3. L'IDENTITÉ DES OPÉRATIONS ─────────────────────────────────────────── */

/* L'`opCode` est DÉRIVÉ, jamais stocké : le nom libre de l'opération est saisi
   par l'atelier (« OP 30 Perçages », « OP10 Ebauche piste Inter ») et n'est
   jamais une clé. Le nom prime : c'est LUI que l'atelier lit à la machine. Le
   champ `ordre` n'est qu'un repli pour les noms sans numéro — mesuré sur
   l'export réel, l'ordre inverse faisait apparaître « OP40 Finition Pistes »
   sous le code OP30, parce que son champ ordre vaut 30. Un agent qui cherche
   l'OP40 ne le trouve pas : le nom gagne. */
function codeDeOp(op) {
  if (!op) return "OP";
  if (op.code) return op.code;
  const m = /OP\s*0*(\d+)/i.exec(String(op.nom || ""));
  if (m) return "OP" + parseInt(m[1], 10);
  const o = nb(op.ordre);
  if (o !== null) return "OP" + Math.round(o);
  return op.nom || "OP";
}

function familleDeLigne(nom) {
  const n = String(nom || "").trim().toLowerCase();
  if (n.indexOf("weisser") === 0) return "weisser";
  if (n.indexOf("hessap") === 0) return "hessapp";
  if (n.indexOf("emag") === 0) return "emag";
  if (n.indexOf("pci") === 0) return "pci";
  return "";
}

function rangLigne(nom) {
  const n = String(nom || "").trim().toLowerCase();
  const i = RANG_LIGNES.indexOf(n);
  return i === -1 ? RANG_LIGNES.length : i;
}

function codeLigneDe(nom) {
  const n = String(nom || "").trim().toUpperCase();
  const m = /^EMAG\s*(\d+)$/.exec(n);
  if (m) return "E" + m[1];
  if (n.indexOf("HESSAPP") === 0) return "HESSAPP";
  const w = /^WEISSER\s*(\d+)$/.exec(n);
  if (w) return "W" + w[1];
  const p = /^PCI\s*(\d+)$/.exec(n);
  if (p) return "P" + p[1];
  return "";
}

function encreDe(nom) {
  const f = familleDeLigne(nom);
  return f ? FAMILLES_LIGNE[f].encre : "#545E68";
}

/* ── 4. LE SCÉNARIO DE PRODUCTION ─────────────────────────────────────────── */

/* Un poste peut avoir zéro, un ou plusieurs scénarios en production dans les
   données anciennes. La règle est UN SEUL appel à cette fonction, partout : le
   proto en rédérivait le même choix à deux endroits, et les deux règles avaient
   fini par diverger. On lit donc, dans l'ordre : le drapeau `baseline`, sinon
   le statut « en série », sinon un scénario nommé « base excel ». */
function scenarioDeProd(scs) {
  const liste = scs || [];
  return liste.find(s => s && s.baseline === true)
      || liste.find(s => s && s.statut === "serie")
      || liste.find(s => s && /base\s*excel/i.test(s.name || ""))
      || null;
}

/* ── 5. LE CPP OUTILLAGE — le driver ───────────────────────────────────────── */

/* LE point de calcul. `prix / (arêtes × charnière)`, terme pour terme la formule
   de la colonne I du classeur de Matis. Toute valeur non strictement positive
   rend le coût NON CHIFFRABLE, jamais 0 : un logement dont le prix est saisi
   mais pas la charnière ne coûte pas zéro, il n'est pas chiffré. */
function coutLogement(l) {
  if (!l) return null;
  const prix = pos(l.prix);
  if (prix === null) return null;
  const aretes = pos(l.aretes);
  if (aretes === null) return null;
  const charniere = pos(l.charniere);
  if (charniere === null) return null;
  return prix / (aretes * charniere);
}

/* Ce qu'il manque à un logement pour être chiffré — le motif est affiché tel quel,
   parce que « non chiffrable » sans raison oblige l'agent à deviner. */
function motifLogement(l) {
  if (!l) return "logement absent";
  if (pos(l.prix) === null) return "prix non saisi";
  if (pos(l.aretes) === null) return "nombre d'arêtes non saisi";
  if (pos(l.charniere) === null) return "charnière non saisie";
  return "";
}

function cppParLogement(sc) {
  const out = [];
  ((sc && sc.outils) || []).forEach(o => {
    (o.logements || []).forEach(l => {
      out.push({
        outilId: o.id, outilNumero: o.numero || "?",
        logementId: l.id, logementNom: l.nom || "?",
        mabec: l.mabec || "", article: l.ref || "",
        cpp: coutLogement(l), motif: motifLogement(l),
        prix: nb(l.prix), aretes: nb(l.aretes), charniere: nb(l.charniere)
      });
    });
  });
  return out;
}

function cppOutillageOutil(o) {
  if (!o) return null;
  const parts = (o.logements || []).map(coutLogement).filter(v => v !== null);
  return parts.length ? parts.reduce((a, b) => a + b, 0) : null;
}

function cppOutillageScenario(sc) {
  if (!sc) return null;
  const parts = [];
  (sc.outils || []).forEach(o => {
    (o.logements || []).forEach(l => {
      const c = coutLogement(l);
      if (c !== null) parts.push(c);
    });
  });
  return parts.length ? parts.reduce((a, b) => a + b, 0) : null;
}

/* La décomposition par outil. Le seau est ici, et nulle part ailleurs : c'est
   ce qui permet à l'écran de garantir que la somme des outils est exactement le
   CPP du scénario. Le test le vérifie sur l'export réel du site. */
function outillageDeScenario(sc) {
  if (!sc) return { outils: [], cpp: null, nonChiffrables: 0, total: 0 };
  const outils = [];
  let total = 0, chiffres = 0, nonChiffrables = 0;
  (sc.outils || []).forEach(o => {
    const logements = (o.logements || []).map(l => ({
      id: l.id, nom: l.nom || "?", mabec: l.mabec || "", article: l.ref || "",
      cpp: coutLogement(l), motif: motifLogement(l),
      prix: nb(l.prix), aretes: nb(l.aretes), charniere: nb(l.charniere)
    }));
    logements.forEach(x => { if (x.cpp === null) nonChiffrables++; });
    const valeurs = logements.map(x => x.cpp).filter(v => v !== null);
    const cpp = valeurs.length ? valeurs.reduce((a, b) => a + b, 0) : null;
    if (cpp !== null) { total += cpp; chiffres++; }
    outils.push({
      id: o.id, numero: o.numero || "?", description: o.description || "",
      correcteur: o.correcteur || "", simultane: o.simultaneAvecPrecedent === true,
      cpp: cpp, nbLogements: logements.length, logements: logements
    });
  });
  return { outils: outils, cpp: chiffres ? total : null, nonChiffrables: nonChiffrables, total: total };
}

/* Le CPP RÉELLEMENT OBTENU par un essai. C'est la différence entre l'outil et ce
   qui existe : le prévu dit ce qu'on croit, l'obtenu dit ce qui s'est passé.
   Le prix et les arêtes viennent de la DÉFINITION du logement (ils ne changent
   pas d'un essai à l'autre) ; la charnière vient de l'ESSAI, parce que c'est
   elle qu'on mesure. Si le prix du scénario a bougé depuis, c'est la définition
   d'aujourd'hui qui fait foi — c'est dit, jamais supposé. */
function cppEssai(sc, essai) {
  const vide = { cpp: null, prevu: null, nbLogements: 0, nonChiffrables: 0, ecart: null };
  if (!sc || !essai) return vide;
  const definition = {};
  (sc.outils || []).forEach(o => (o.logements || []).forEach(l => { definition[l.id] = l; }));
  const suivis = (essai.params && essai.params.logements) || [];
  if (!suivis.length) return vide;
  let total = 0, n = 0, ecartes = 0;
  suivis.forEach(p => {
    const def = definition[p.logementId];
    const prix = def ? def.prix : p.prix;
    const aretes = def ? def.aretes : p.aretes;
    const charniere = (p.charniere !== "" && p.charniere != null)
      ? p.charniere : (def ? def.charniere : null);
    const c = coutLogement({ prix: prix, aretes: aretes, charniere: charniere });
    if (c === null) { ecartes++; return; }
    total += c; n++;
  });
  const cpp = n ? total : null;
  return {
    cpp: cpp, prevu: cppOutillageScenario(sc), nbLogements: n,
    nonChiffrables: ecartes,
    ecart: (cpp !== null && n) ? cpp - cppOutillageScenario(sc) : null
  };
}

/* ── 6. LE TEMPS, LE REBUT, LES PIÈCES — les axes non comparables ─────────── */

/* Le taux horaire est stocké en CHAINE par l'ancien modèle (« » = non saisi).
   On lit donc par `nb()`, jamais par `parseFloat` direct. */
function tauxHoraire(ligne) {
  return pos(ligne && ligne.coutHoraire);
}

/* Le temps de cycle en secondes. Le scénario porte un INDICE base 100 dans le
   modèle d'origine ; converti en secondes seulement si la conversion est
   demandée et possible. Un indice sans base n'est pas un temps : il ne devient
   pas 1 s. */
function cycleSecondes(sc, config) {
  const idx = nb(sc && sc.cycle);
  if (idx === null || idx <= 0) return null;
  if (!(config && config.cycleSecActif)) return null;
  const ref = pos(config.cycleRefSec) || SEUILS.cycleRefSec;
  return idx * ref / 100;
}

function partCoupante(config) {
  const p = nb(config && config.partCoupante);
  if (p === null || p <= 0) return null;
  return Math.min(100, p) / 100;
}

/* Le coût machine de la pièce : (taux horaire / 3600) × cycle × part en coupe.
   Les trois facteurs sont obligatoires. Un seul qui manque, le poste n'est pas
   chiffrable — il ne devient pas 0, ce qui ferait croire à un poste gratuit. */
function coutMachinePiece(ligne, sc, config) {
  const taux = tauxHoraire(ligne);
  if (taux === null) return null;
  const cycle = cycleSecondes(sc, config);
  if (cycle === null) return null;
  const part = partCoupante(config);
  if (part === null) return null;
  return (taux / 3600) * cycle * part;
}

/* Le rebut : un coût par disque perdu, multiplié par le taux de rebut mesuré.
   Sans taux mesuré, le poste n'est pas chiffrable. */
function coutRebut(config) {
  if (!(config && config.coutRebutActif)) return null;
  const disque = pos(config.coutDisque);
  if (disque === null) return null;
  const taux = pos(config.tauxRebutAnnuel);
  if (taux === null) return null;
  return disque * taux / 100;
}

function coutPieces(outil) {
  let total = 0, n = 0;
  ((outil && outil.pieces) || []).forEach(p => {
    const c = pos(p.prix);
    if (c === null) return;
    total += c; n++;
  });
  return n ? total : null;
}

/* ── 7. LE COÛT DE LA PIÈCE, poste par poste ──────────────────────────────── */

/* Un seul point de vérité du coût complet. Chaque poste porte sa valeur ET son
   motif d'absence : c'est ce qui permet à l'écran 3 de dire « hors 1 opération
   non chiffrée » au lieu d'afficher un total qui ment par silence
   (constitution §5.6). */
function coutsDetail(sc, ligne, config) {
  const postes = {};
  const manque = {};
  const put = (cle, valeur, motif) => {
    postes[cle] = valeur;
    manque[cle] = valeur === null ? (motif || "") : "";
  };
  const cpp = cppOutillageScenario(sc);
  put("plaquettes", cpp, cpp === null ? "aucun logement chiffrable" : "");
  const temps = coutMachinePiece(ligne, sc, config);
  put("temps", temps, temps === null
      ? (!tauxHoraire(ligne) ? "taux horaire de ligne non saisi"
        : !cycleSecondes(sc, config) ? "temps de cycle non saisi"
        : "part en coupe non saisie")
      : "");
  const rebut = coutRebut(config);
  put("rebut", rebut, rebut === null
      ? (config && config.coutRebutActif ? "coût du disque ou taux de rebut non saisi" : "poste désactivé")
      : "");
  let pieces = 0, nbPieces = 0;
  (sc && sc.outils || []).forEach(o => {
    const c = coutPieces(o);
    if (c !== null) { pieces += c; nbPieces++; }
  });
  put("pieces", nbPieces ? pieces : null, nbPieces ? "" : "aucune pièce détachée chiffrée");

  const chiffres = COUT_POSTES.filter(p => postes[p.cle] !== null);
  return {
    postes: postes, manque: manque,
    total: chiffres.length ? chiffres.reduce((a, p) => a + postes[p.cle], 0) : null,
    postesChiffres: chiffres.map(p => p.cle),
    complets: chiffres.length === COUT_POSTES.length,
    manquants: COUT_POSTES.filter(p => postes[p.cle] === null).map(p => p.cle)
  };
}

/* Le PÉRIMÈTRE COMMUN : la seule façon de soustraire deux coûts. On ne compare
   que les postes chiffrables des DEUX côtés, et — pour parler du classeur de
   Matis — seulement ceux qui y figurent. Un écart sur un périmètre partiel est
   affiché AVEC son périmètre, jamais nu (constitution §5.6). */
function perimetreCommun(a, b, seulementClasseur) {
  const postes = [];
  COUT_POSTES.forEach(p => {
    if (seulementClasseur && !p.comparable) return;
    if (!a || !b) return;
    if (a.postes[p.cle] !== null && a.postes[p.cle] !== undefined
     && b.postes[p.cle] !== null && b.postes[p.cle] !== undefined) postes.push(p.cle);
  });
  return postes;
}

function deltaCouts(ref, cand, seulementClasseur) {
  const perimetre = perimetreCommun(ref, cand, seulementClasseur);
  if (!perimetre.length) {
    return { comparable: false, perimetre: [], ecart: null,
      motif: "aucun poste de coût chiffrable des deux côtés" };
  }
  const ecart = perimetre.reduce((a, c) => a + (cand.postes[c] - ref.postes[c]), 0);
  return { comparable: true, perimetre: perimetre, ecart: ecart,
    complet: perimetre.length === COUT_POSTES.length, motif: "" };
}

/* ── 8. LE VOLUME ANNUEL — d'où vient l'euro par an ────────────────────────── */

/* Le gain annuel est le gain par pièce multiplié par un volume. Ce volume a deux
   sources possibles et il faut les nommer toutes les deux : le volume de la
   RÉFÉRENCE (pièces/an) et le volume de l'OP (issu du classeur). Quand les deux
   existent et diffèrent, on affiche la référence et on signale l'écart — deux
   chiffres qui divergent tuent la confiance plus vite qu'une information
   manquante. */
function volumeAnnuel(ref, op) {
  const parRef = pos(ref && ref.productionAnnuelle);
  const parOp = pos(op && op.config && op.config.volumeAnnuel);
  if (parRef !== null) {
    return { valeur: parRef, source: "référence", divergent: parOp !== null && parOp !== parRef,
             autre: parOp };
  }
  if (parOp !== null) return { valeur: parOp, source: "opération", divergent: false, autre: null };
  return { valeur: null, source: "", divergent: false, autre: null };
}

/* ── 9. LE CHEMIN VERS LA CIBLE ───────────────────────────────────────────── */

/* Combien du chemin vers la cible du site le meilleur scénario disponible a-t-il
   fait. borné à [0, 100] : un gain supérieur à l'écart total est arithmétiquement
   possible si le candidat passe SOUS la cible, et il doit alors afficher 100 %
   fait, pas 340 % — le 100 % se lit « le chemin est fait », pas « le gain »,
   qui est écrit à part. */
function cheminCPP(coutProd, coutMeilleur, cible) {
  const c = nb(cible);
  const p = nb(coutProd);
  const m = nb(coutMeilleur);
  if (c === null || p === null || m === null) return null;
  if (p <= 0) return null;
  if (p <= c) return 100;
  const v = ((p - m) / (p - c)) * 100;
  return Math.max(0, Math.min(100, v));
}

/* ── 10. LA CONFORMITÉ ─────────────────────────────────────────────────────── */

/* `batt` est vide sur 83 prélèvements sur 84 dans les données du site : EMAG 1
   relève DROITE et GAUCHE séparément. Sans pont, tous les essais réimportés
   afficheraient « aucune mesure », en silence, sans une seule erreur console.
   On prend `batt` si elle existe, sinon LE PIRE des deux côtés — jamais la
   moyenne : un état des lieux ne doit jamais flatter une pièce qui déborde
   d'un côté. Et jamais 0 non plus : NaN signifie « non mesurable ». */
function battDe(prel) {
  if (!prel) return NaN;
  const b = nb(prel.batt);
  if (b !== null) return b;
  const cotes = [nb(prel.battD), nb(prel.battG)].filter(v => v !== null);
  if (!cotes.length) return NaN;
  return Math.max.apply(null, cotes);
}

function seuilBattement(sc) {
  if (!sc) return SEUILS.battementDefaut;
  if (sc.battActif === false) return null;          /* critère désactivé */
  const v = pos(sc.limitOverride ? sc.limitValue : SEUILS.battementDefaut);
  return v;
}

/* Trois états, jamais deux : `true`, `false`, ou `null` = non mesurable.
   L'asymétrie est volontaire — une absence ne peut jamais rendre NON conforme,
   sinon un oubli de saisie ferait échouer un essai. */
function conforme(sc, prel) {
  if (!prel) return null;
  const seuil = seuilBattement(sc);
  if (seuil === null) return true;                  /* désactivé = rien à juger */
  const b = battDe(prel);
  if (isNaN(b)) return null;
  return b <= seuil;
}

function seuilRa(sc) {
  if (!sc || !sc.critere2 || sc.critere2.actif !== true) return null;
  return pos(sc.critere2.valeur);
}

function conformeRa(sc, prel) {
  const seuil = seuilRa(sc);
  if (seuil === null) return true;
  const v = nb(prel && prel.valeur2);
  if (v === null) return null;
  return v <= seuil;
}

/* L'état d'usure ne rend jamais non conforme à lui seul : c'est un constat,
   pas un critère. Il se lit, il ne se note pas. */
function usureDe(prel) {
  const u = (prel && prel.usure) || "";
  return USURE_LABELS[u] || "";
}

function conformeEssai(sc, essai) {
  const prels = (essai && essai.prelevements) || [];
  if (!prels.length) return { verdict: null, mesures: 0, nonMesurables: 0, hors: [] };
  let conformes = 0, nonMesurables = 0;
  const hors = [];
  prels.forEach(p => {
    const b = conforme(sc, p);
    const r = conformeRa(sc, p);
    if (b === false || r === false) { hors.push(p); return; }
    /* Le battement attendu mais non mesuré rend le prélèvement NON MESURABLE,
       même si le critère Ra est inactif : « rien à juger » (Ra) ne doit jamais
       masquer « pas mesuré » (battement) — c'est exactement la faute que la
       première version de cette fonction commettait, et le test l'a vue. */
    if (b === null) { nonMesurables++; return; }
    conformes++;
  });
  return { verdict: hors.length ? false : (conformes ? true : null),
           mesures: conformes, nonMesurables: nonMesurables, hors: hors };
}

/* ── 11. LA PREUVE : LA CHARNIÈRE ATTEINTE, LOGEMENT PAR LOGEMENT ─────────── */

/* Le protocole du site : chaque logement suivi doit atteindre sa charnière visée.
   On lit le PLUS GRAND numéro de pièce relevé pour ce logement, et on le compare
   à la charnière visée. Le détail est affiché tel quel — « D1 12/30 p » — parce
   qu'un « en cours » sans chiffres fait perdre le temps qu'il est censé gagner. */
function charniereVisee(sc, essai, logementId) {
  const liste = (essai && essai.params && essai.params.logements) || [];
  const trouve = liste.find(p => p.logementId === logementId);
  const v = trouve ? pos(trouve.charniere) : null;
  if (v !== null) return v;
  let out = null;
  ((sc && sc.outils) || []).forEach(o => (o.logements || []).forEach(l => {
    if (l.id === logementId) { const c = pos(l.charniere); if (c !== null) out = c; }
  }));
  return out;
}

function suiviEssai(sc, essai) {
  const liste = (essai && essai.params && essai.params.logements) || [];
  const prels = (essai && essai.prelevements) || [];
  return liste.map(p => {
    const cible = charniereVisee(sc, essai, p.logementId);
    let dernier = null;
    prels.forEach(x => {
      if (x.logementId !== p.logementId) return;
      const n = nb(x.piece);
      if (n !== null && (dernier === null || n > dernier)) dernier = n;
    });
    return {
      logementId: p.logementId,
      logementNom: p.logementNom || "?",
      outilNumero: p.outilNumero || "",
      cible: cible,
      atteint: dernier === null ? 0 : dernier,
      fait: cible !== null && dernier !== null && dernier >= cible,
      interne: cible !== null && cible > 0 ? Math.min(1, (dernier || 0) / cible) : null
    };
  });
}

function suiviAtteint(sc, essai) {
  const s = suiviEssai(sc, essai);
  const visees = s.filter(x => x.cible !== null);
  if (!visees.length) return null;
  return visees.filter(x => x.fait).length;
}

/* Hiérarchie ordonnée, pas un score : arrêt > non-conformité > mesures
   manquantes > charnières non atteintes > conforme. C'est l'ordre du site. */
function statutEssai(sc, essai) {
  if (!essai) return { code: "vide", texte: "aucun essai" };
  if (essai.cloture && essai.cloture.motif) {
    return { code: "arrete", texte: "arrêté — " + (MOTIF_LABELS[essai.cloture.motif] || essai.cloture.motif) };
  }
  const c = conformeEssai(sc, essai);
  if (c.verdict === false) {
    const premier = c.hors[0];
    return { code: "nonconforme", texte: "hors tolérance",
             piece: premier ? nb(premier.piece) : null };
  }
  const s = suiviEssai(sc, essai);
  const visees = s.filter(x => x.cible !== null);
  const restants = visees.filter(x => !x.fait);
  if (restants.length) {
    return { code: "encours", restants: restants,
      texte: restants.map(r => r.logementNom + " " + r.atteint + "/" + Math.round(r.cible) + " p").join(" · ") };
  }
  if (c.nonMesurables > 0) {
    return { code: "attente", texte: c.nonMesurables + " mesure" + (c.nonMesurables > 1 ? "s" : "") + " à saisir" };
  }
  if (!c.mesures) return { code: "attente", texte: "aucune mesure exploitable" };
  return { code: "conforme", texte: "conforme — charnière atteinte" };
}

function statutScenario(sc) {
  const essais = (sc && sc.essais) || [];
  const seuil = (sc && nb(sc.validationThreshold)) || SEUILS.validations;
  const verdi = essais.map(e => statutEssai(sc, e));
  if (sc && sc.statut === "serie") return { code: "serie", texte: "en production", validations: verdi.filter(v => v.code === "conforme").length };
  if (sc && sc.statut === "abandonne") return { code: "abandonne", texte: "abandonné", validations: 0 };
  const conformes = verdi.filter(v => v.code === "conforme").length;
  if (!essais.length) return { code: "rien", texte: "aucun essai", validations: 0 };
  if (conformes >= seuil) return { code: "pret", texte: "validé " + conformes + " fois", validations: conformes };
  if (conformes > 0) return { code: "encours", texte: conformes + "/" + seuil + " validés", validations: conformes };
  return { code: "essai", texte: "en essai", validations: 0 };
}

/* ── 12. L'ARBRE : POSTE, RÉFÉRENCE, LIGNE ────────────────────────────────── */

/* Le poste est DÉRIVÉ — ligne × opCode — jamais stocké. C'est lui qui rend
   impossible la dérive `coutEnCours` de l'app de production : il n'existe qu'en
   un seul endroit, calculé par `verdictPoste`. */
function postesDeLigne(ligne) {
  const out = [];
  ((ligne && ligne.references) || []).forEach(ref => {
    ((ref && ref.ops) || []).forEach(op => {
      const scs = (op && op.scenarios) || [];
      const prod = scenarioDeProd(scs);
      out.push({
        ligne: ligne, ref: ref, op: op, scs: scs, prod: prod,
        code: codeDeOp(op),
        autres: prod ? scs.filter(s => s && s.id !== prod.id) : scs.filter(Boolean)
      });
    });
  });
  return out;
}

function cppReference(ligne, ref) {
  const postes = postesDeLigne(ligne).filter(p => p.ref.id === ref.id);
  let total = 0, chiffres = 0, nonChiffrables = 0, sansProd = 0;
  postes.forEach(p => {
    if (!p.prod) { sansProd++; nonChiffrables++; return; }
    const c = cppOutillageScenario(p.prod);
    if (c === null) { nonChiffrables++; return; }
    total += c; chiffres++;
  });
  const cpp = chiffres ? total : null;
  const cible = pos(ref && ref.cibleCPP);
  return {
    ref: ref, cpp: cpp, nbPostes: postes.length, chiffres: chiffres,
    nonChiffrables: nonChiffrables, sansProd: sansProd, cible: cible,
    ecartCible: (cpp !== null && cible !== null) ? cpp - cible : null
  };
}

function tuileDeLigne(ligne) {
  const refs = ((ligne && ligne.references) || []).map(r => cppReference(ligne, r));
  const chiffres = refs.filter(r => r.cpp !== null);
  /* Les postes non chiffrables se comptent sur TOUTES les références, pas
     seulement sur celles qui ont un CPP : sinon une référence entièrement
     non chiffrable verrait ses postes disparaître du compte — exactement le
     silence que l'invariant 3 du cahier interdit. Le total, lui, ne prend que
     ce qui est chiffrable. */
  let cpp = 0, nonChiffrables = 0, sansProd = 0, cibles = 0;
  refs.forEach(r => {
    if (r.cpp !== null) cpp += r.cpp;
    nonChiffrables += r.nonChiffrables;
    sansProd += r.sansProd;
    if (r.cible !== null) cibles++;
  });
  let dominante = null;
  chiffres.forEach(r => { if (!dominante || r.chiffres > dominante.chiffres) dominante = r; });
  return {
    ligne: ligne, nom: (ligne && ligne.nom) || "Ligne sans nom",
    famille: familleDeLigne(ligne && ligne.nom),
    encre: encreDe(ligne && ligne.nom),
    code: codeLigneDe(ligne && ligne.nom), rang: rangLigne(ligne && ligne.nom),
    refs: refs, dominante: dominante,
    cpp: chiffres.length ? cpp : null,
    nbRefs: refs.length, nbChiffres: chiffres.length,
    nbPostes: postesDeLigne(ligne).length,
    nonChiffrables: nonChiffrables, sansProd: sansProd, nbCibles: cibles,
    vide: refs.length === 0
  };
}

function tuilesDeLignes(lignes) {
  return (lignes || []).map(tuileDeLigne)
    .sort((a, b) => a.rang - b.rang || a.nom.localeCompare(b.nom));
}

/* ── 13. LE VERDICT D'UN POSTE — une seule fois, un seul calcul ───────────── */

/* C'est ICI, et nulle part ailleurs, que se décide l'état d'un poste. L'écran
   1, l'écran 2, l'écran 4 et l'A4 lisent tous ce résultat : un même chiffre
   affiché par deux chemins est la panne la plus coûteuse qu'un outil puisse
   avoir (constitution §3.1). */
function verdictPoste(ligne, ref, op) {
  const scs = (op && op.scenarios) || [];
  const prod = scenarioDeProd(scs);
  const cible = pos(ref && ref.cibleCPP);
  const coutsProd = prod ? coutsDetail(prod, ligne, op && op.config) : null;
  const cppProd = coutsProd ? coutsProd.postes.plaquettes : null;

  /* Le MEILLEUR scénario disponible : celui dont le CPP outillage est le plus
     bas, hors production. On ne compare jamais un total d'outil à une cible de
     classeur : le gain se calcule périmètre à périmètre, donc sur le poste
     `plaquettes` des deux côtés. */
  let meilleur = null;
  scs.forEach(s => {
    if (prod && s.id === prod.id) return;
    const c = cppOutillageScenario(s);
    if (c === null) return;
    if (!meilleur || c < meilleur.cpp) meilleur = { sc: s, cpp: c };
  });

  const chemin = (cppProd !== null && meilleur) ? cheminCPP(cppProd, meilleur.cpp, cible) : null;
  const enSerie = scs.filter(s => s && s.statut === "serie" && (!prod || s.id !== prod.id));

  /* Deux gains, jamais fusionnés (constitution §3.4) : ce qui est réellement
     passé en production, et ce qui n'est encore qu'une promesse d'essai. */
  let gainActe = null, gainProjete = null, deltaComplet = null;
  if (cppProd !== null) {
    if (meilleur && meilleur.cpp < cppProd) gainProjete = cppProd - meilleur.cpp;
    if (enSerie.length) {
      const cppSerie = cppOutillageScenario(enSerie[0]);
      if (cppSerie !== null && cppSerie < cppProd) {
        gainActe = cppProd - cppSerie;
        deltaComplet = deltaCouts(coutsProd, coutsDetail(enSerie[0], ligne, op && op.config), true);
      }
    }
  }

  const vol = volumeAnnuel(ref, op);
  const gainProjeteAnnuel = (gainProjete !== null && vol.valeur !== null) ? gainProjete * vol.valeur : null;
  const gainActeAnnuel = (gainActe !== null && vol.valeur !== null) ? gainActe * vol.valeur : null;

  let verdict, code;
  if (!prod) { code = "achiffrer"; verdict = "poste sans scénario de production"; }
  else if (cppProd === null) { code = "achiffrer"; verdict = cible !== null ? "cible connue, coût à chiffrer" : "coût à chiffrer"; }
  else if (enSerie.length && gainActe !== null) { code = "gagne"; verdict = "gagné — en production"; }
  else if (meilleur && statutScenario(meilleur.sc).code === "pret") { code = "pret"; verdict = "validé 5 fois — décision à prendre"; }
  else if (gainProjete !== null) { code = "essai"; verdict = "essai prometteur"; }
  else { code = "rien"; verdict = "aucun essai ne fait mieux que la production"; }

  return {
    ligne: ligne, ref: ref, op: op,
    opCode: codeDeOp(op), nomOp: (op && op.nom) || "",
    /* `code` est le CODE DU VERDICT (essai, gagne, achiffrer…) : c'est lui que
       tous les écrans lisent. Le code d'opération vit à côté, dans `opCode` —
       la première version écrasait l'un par l'autre, et le test l'a attrapé. */
    code: code,
    scs: scs, prod: prod, autres: scs.filter(s => s && (!prod || s.id !== prod.id)),
    coutsProd: coutsProd, cppProd: cppProd, cible: cible,
    ecartCible: (cppProd !== null && cible !== null) ? cppProd - cible : null,
    meilleur: meilleur, chemin: chemin,
    gainActe: gainActe, gainProjete: gainProjete,
    gainActeAnnuel: gainActeAnnuel, gainProjeteAnnuel: gainProjeteAnnuel,
    volume: vol, deltaComplet: deltaComplet,
    verdict: verdict
  };
}

function decisionPoste(v) {
  if (!v) return { mot: "—", pourquoi: "" };
  switch (v.code) {
    case "gagne":
      return { mot: "SÉRIE", pourquoi: v.gainActeAnnuel !== null
          ? "l'essai est en production — " + fmtEuro(v.gainActe) + "/pièce, " + fmtEnt(v.gainActeAnnuel) + " €/an"
          : "l'essai est en production — " + fmtEuro(v.gainActe) + "/pièce" };
    case "pret":
      return { mot: "DÉCIDER", pourquoi: "validé " + SEUILS.validations + " fois — il reste à dire oui ou non" };
    case "essai":
      return { mot: "ESSAYER", pourquoi: v.gainProjeteAnnuel !== null
          ? "l'essai gagne " + fmtEuro(v.gainProjete) + "/pièce — " + fmtEnt(v.gainProjeteAnnuel) + " €/an, à confirmer sur " + SEUILS.validations + " pièces"
          : "l'essai gagne " + fmtEuro(v.gainProjete) + "/pièce (volume annuel non saisi)" };
    case "achiffrer":
      return { mot: "CHIFFRER", pourquoi: v.verdict };
    default:
      return { mot: "RIEN", pourquoi: v.verdict };
  }
}

function verdictLigne(ligne) {
  const postes = postesDeLigne(ligne).map(p => verdictPoste(ligne, p.ref, p.op));
  return { ligne: ligne, tuile: tuileDeLigne(ligne), postes: postes };
}

function recapLignes(verdicts) {
  let cppActe = 0, cppProjete = 0, aChiffrer = 0, decisions = 0, postes = 0;
  (verdicts || []).forEach(vl => {
    vl.postes.forEach(p => {
      postes++;
      if (p.code === "achiffrer") aChiffrer++;
      if (p.code === "pret" || p.code === "essai") decisions++;
      if (p.gainActe) cppActe += p.gainActe;
      else if (p.gainProjete) cppProjete += p.gainProjete;
    });
  });
  return { cppActe: cppActe, cppProjete: cppProjete, aChiffrer: aChiffrer,
           decisions: decisions, postes: postes };
}

/* La somme d'un champ de gain sur une liste de postes. Vit dans le noyau et pas
   dans l'écran : deux façons de sommer les gains, c'est deux chiffres. */
function sommeGains(postes, cle) {
  let s = 0, n = 0;
  (postes || []).forEach(p => { const v = nb(p && p[cle]); if (v !== null) { s += v; n++; } });
  return n ? s : null;
}

/* ── 14. LA SANTÉ DES DONNÉES — ce qui manque, compté et nommé ─────────────── */

/* Un outil qui n'affiche que ce qu'il sait faire laisse croire que le reste est
   faux. On compte donc les trous, et on les affiche : c'est la version
   industrialisée du rapport d'import du proto, devenu permanent. */
function santeDonnees(etat) {
  const s = { lignes: 0, sansReference: 0, postes: 0, sansProd: 0, scenarios: 0,
              outils: 0, sansNumero: 0, logements: 0, nonChiffrables: 0,
              sansMabec: 0, essais: 0, prelevements: 0, sansBatt: 0,
              referencesSansCible: 0, referencesSansVolume: 0, remontees: [] };
  ((etat && etat.lignes) || []).forEach(l => {
    s.lignes++;
    const refs = l.references || [];
    if (!refs.length) { s.sansReference++; s.remontees.push(l.nom + " : aucune référence"); }
    refs.forEach(ref => {
      if (pos(ref.cibleCPP) === null) s.referencesSansCible++;
      if (pos(ref.productionAnnuelle) === null) s.referencesSansVolume++;
      (ref.ops || []).forEach(op => {
        s.postes++;
        const scs = op.scenarios || [];
        s.scenarios += scs.length;
        if (!scenarioDeProd(scs)) s.sansProd++;
        scs.forEach(sc => {
          (sc.outils || []).forEach(o => {
            s.outils++;
            if (!o.numero) s.sansNumero++;
            (o.logements || []).forEach(log => {
              s.logements++;
              if (coutLogement(log) === null) s.nonChiffrables++;
              if (!log.mabec) s.sansMabec++;
            });
          });
          (sc.essais || []).forEach(e => {
            s.essais++;
            (e.prelevements || []).forEach(p => {
              s.prelevements++;
              if (isNaN(battDe(p))) s.sansBatt++;
            });
          });
        });
      });
    });
  });
  return s;
}

/* ── 15. LE DÉCOMPTE DES ESSAIS PAR POSTE (le « y en a-t-il assez ? ») ────── */

function essaisDuScenario(sc) {
  return (sc && sc.essais) || [];
}

function scenariosAOptimiser(v) {
  return (v && v.autres) || [];
}

function nbScenariosHorsProd(v) {
  return scenariosAOptimiser(v).length;
}

/* Les scénarios qui portent une preuve d'essai, tous postes confondus : c'est
   ce que l'écran 1 annonce quand il dit « N scénarios testés ». */
function postesAvecEssais(ligne) {
  return postesDeLigne(ligne).filter(p => p.scs.some(s => (s.essais || []).length));
}
