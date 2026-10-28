# -*- coding: utf-8 -*-
"""Tour 106 — v4.128.0 — LOT 3 du brief complémentaire (décisions Benjamin).

1. LE CHIFFRE DE TÊTE = LE GAIN D'OUTILLAGE : coutsDetail ne somme plus
   plaquettes + machine. `total` = outillage (plaquettes + pièces détachées) ;
   machine et rebut restent des champs séparés exposés ; `cumul` porte la
   somme complète, jamais en chiffre de tête (affiché seulement sur demande
   explicite, libellé « cumul des deux axes »).
2. LE GAIN ANNUEL = L'ÉCART D'OUTILLAGE (bilanAnnuel) : les écarts machine
   (h/an + €/an) et rebut sortent en champs séparés, jamais sommés.
3. FOURCHETTE : le gain est calculé à trois charnières (visée / réelle
   moyenne / réelle minimale). Au moins une charnière réelle mesurée → le
   chiffre de tête porte le gain à la réelle minimale, étiqueté « mesuré
   (min, N essais) » ; sinon il reste à la visée, étiqueté « objectif, non
   mesuré ». Jamais de repli silencieux.
4. charniereReelle expose min / N / ≥ — la moyenne ne s'affiche qu'à partir
   de 5 fins de vie réelles (les essais arrêtés à la visée sont des bornes
   inférieures, pas des fins de vie).
5. POLARITÉ des heures : « −X h/an (plus rapide) » / « +X h/an (plus lent) »
   — le mot, pas le signe seul (détail annuel, tuile, A4).
6. plaquettesParAn : conditionnement (boîte de N, arrondi au supérieur) et
   taux de casse — paramètres optionnels, vides = inchangé, renseignés =
   affichés en toutes lettres.
7. Rebut : N (le nombre de pièces du journal) à côté du taux ; sous le seuil
   configurable (cfg.rebutSeuilN, défaut 30) : « échantillon trop faible ».
8. Fusion : un écart de modifieLe < 10 min n'est pas arbitré en silence —
   conflit signalé nommément, version locale conservée."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. coutsDetail : le total = l'outillage ──────────────────────────────────
remplace(
"""function coutsDetail(sc, cfg, ligne){
  cfg = cfg || config;
  const plaquettes = scenarioCost(sc);
  const pieces = coutPiecesDetachees(sc, cfg);
  const machine = coutMachinePiece(sc, cfg, ligne);
  const rebut = coutRebutPiece(sc, cfg);
  const parts = [plaquettes, pieces, machine, rebut];
  const total = parts.some(v => v !== null) ? parts.reduce((a,b) => a + (b||0), 0) : null;
  return { plaquettes, pieces, machine, rebut, total,
           multiPoste: parts.filter(v => v !== null).length > 1 };
}""",
"""function coutsDetail(sc, cfg, ligne){
  cfg = cfg || config;
  const plaquettes = scenarioCost(sc);
  const pieces = coutPiecesDetachees(sc, cfg);
  const machine = coutMachinePiece(sc, cfg, ligne);
  const rebut = coutRebutPiece(sc, cfg);
  /* v4.128 (LOT 3, décision Benjamin) — le chiffre de tête est le gain
     D'OUTILLAGE : plaquettes + pièces détachées. Le temps machine et le
     rebut sont des AXES SÉPARÉS, jamais sommés ici — le cumul des deux axes
     n'existe que sur demande explicite (champ cumul, jamais en chiffre de
     tête). Avec machine et rebut inactifs, le total est inchangé. */
  const partsOutillage = [plaquettes, pieces].filter(v => v !== null);
  const total = partsOutillage.length ? partsOutillage.reduce((a,b) => a + b, 0) : null;
  const parts = [plaquettes, pieces, machine, rebut];
  const cumul = parts.some(v => v !== null) ? parts.reduce((a,b) => a + (b||0), 0) : null;
  return { plaquettes, pieces, machine, rebut, total, cumul,
           multiPoste: parts.filter(v => v !== null).length > 1 };
}""",
"1. coutsDetail : total = outillage, cumul séparé")

# ── 2. bilanAnnuel : le gain = l'écart d'outillage ; machine/rebut séparés ───
remplace(
"""    const peri = perimetreCompare(cSc, cBase);
    if(peri.communs.length && peri.base > 0) out.gainAnnuel = (peri.base - peri.sc) * volume;
    if(peri.exclus.length) out.perimetrePartiel = peri.exclus;
    const sBase = cycleSecondes(base, cfg), sSc = cycleSecondes(sc, cfg);
    if(sBase !== null && sSc !== null) out.heuresAnnuelles = ((sSc - sBase) * volume) / 3600;""",
"""    const peri = perimetreCompare(cSc, cBase);
    /* v4.128 (LOT 3) — le gain annuel est l'écart D'OUTILLAGE (plaquettes +
       pièces détachées), jamais sommé avec la machine. Les écarts machine
       (h/an + €/an) et rebut sortent en champs séparés. */
    const periOut = perimetreCompare(cSc, cBase, ["plaquettes", "pieces"]);
    if(periOut.communs.length && periOut.base > 0) out.gainAnnuel = (periOut.base - periOut.sc) * volume;
    if(peri.exclus.length) out.perimetrePartiel = peri.exclus;
    const sBase = cycleSecondes(base, cfg), sSc = cycleSecondes(sc, cfg);
    if(sBase !== null && sSc !== null) out.heuresAnnuelles = ((sSc - sBase) * volume) / 3600;
    /* les écarts des axes séparés (tuiles propres, jamais sommées) */
    if(cBase.machine !== null && cSc.machine !== null) out.deltaMachineEurAn = (cBase.machine - cSc.machine) * volume;
    if(cBase.rebut !== null && cSc.rebut !== null) out.deltaRebutEurAn = (cBase.rebut - cSc.rebut) * volume;""",
"2. bilanAnnuel : gain outillage + écarts séparés")

# ── 3. perimetreCompare : un filtre de postes optionnel ──────────────────────
remplace(
"""function perimetreCompare(couts, coutsBase){
  const postes = [""",
"""function perimetreCompare(couts, coutsBase, postesRetenus){
  cfg = cfg || config;
  const postes = [""",
"3a. perimetreCompare : le paramètre")

remplace(
"""  const communs = [], exclus = [];
  postes.forEach(([cle, lib]) => {""",
"""  const communs = [], exclus = [];
  postes.forEach(([cle, lib]) => {
    if(postesRetenus && postesRetenus.indexOf(cle) === -1) return;""",
"3b. le filtre de postes")

# ── 4. la fourchette : le gain à la charnière réelle minimale ────────────────
remplace(
"""  if(base && base.id !== sc.id){
    const cBase = coutsDetail(base, cfg, ligne);""",
"""  if(base && base.id !== sc.id){
    const cBase = coutsDetail(base, cfg, ligne);
    /* v4.128 (LOT 3, point 2) — la FOURCHETTE : le gain à trois charnières.
       La charnière réelle du scénario (min et moyenne) substituée logement
       par logement là où elle est mesurée. */
    const gainA = (facteur) => {
      const cScA = coutsDetailCharniere(sc, cfg, ligne, facteur);
      const cBA = coutsDetailCharniere(base, cfg, ligne, facteur === "visée" ? null : facteur);
      if(cScA === null || cBA === null) return null;
      const periA = perimetreCompare(cScA, cBA, ["plaquettes", "pieces"]);
      if(!periA.communs.length || periA.base <= 0) return null;
      return (periA.base - periA.sc) * volume;
    };
    const reelSc = charniereReelle(sc);
    if(reelSc && reelSc.finsReelles > 0){
      out.gainMesure = gainA("minReelle");
      out.gainMesureMoyen = gainA("moyenneReelle");
      out.gainMesureN = reelSc.finsReelles;
      out.gainMesureBorneInf = reelSc.borneInf;
    }
    out.gainVisee = (() => {
      const cScA = coutsDetailCharniere(sc, cfg, ligne, "visée");
      const cBA = coutsDetailCharniere(base, cfg, ligne, null);
      if(cScA === null || cBA === null) return null;
      const periA = perimetreCompare(cScA, cBA, ["plaquettes", "pieces"]);
      if(!periA.communs.length || periA.base <= 0) return null;
      return (periA.base - periA.sc) * volume;
    })();""",
"4. bilanAnnuel : la fourchette visée/min/moyenne")

# ── 5. coutsDetailCharniere : le coût outillage à des charnières substituées ─
remplace(
"""/* ---- seuil de bascule : le point ou le scenario cesse d'etre gagnant ----""",
"""/* ---- v4.128 (LOT 3, point 2) — le coût outillage à des charnières substituées :
   facteur = "visée" (tel quel), "minReelle" (la réelle minimale de chaque
   logement où mesurée), "moyenneReelle" (la moyenne, si ≥ 5 fins de vie
   réelles), null (tel quel). Rend le coût outillage/pièce, ou null si non
   chiffrable. Pur : ne mute rien. ---- */
function coutsDetailCharniere(sc, cfg, ligne, facteur){
  if(!facteur || facteur === "visée") return coutsDetail(sc, cfg, ligne);
  const reel = charniereReelle(sc);
  if(!reel || !reel.parLogement || !reel.parLogement.length) return null;
  const map = {};
  reel.parLogement.forEach(e => {
    if(facteur === "minReelle") map[e.logementId] = e.min;
    else if(facteur === "moyenneReelle" && e.finsReelles >= 5) map[e.logementId] = e.moyenne;
  });
  const cfgA = Object.assign({}, cfg);
  const substitue = { outils: (sc.outils||[]).map(o => ({
    id: o.id, numero: o.numero, simultaneAvecPrecedent: o.simultaneAvecPrecedent,
    logements: (o.logements||[]).map(l => {
      const r = map[l.id];
      if(r === undefined || r === null || isNaN(r) || r <= 0) return l;
      return Object.assign({}, l, { charniere: r });
    }) })) };
  return coutsDetail(normalizeScenario(substitue), cfgA, ligne);
}

/* ---- seuil de bascule : le point ou le scenario cesse d'etre gagnant ----""",
"5. coutsDetailCharniere")

# ── 6. charniereReelle : min / N / fins réelles (ancres courtes) ─────────────
remplace(
"""function charniereReelle(sc, logementId){
  const atteintes = [];
  let borneInf = true;""",
"""function charniereReelle(sc, logementId){
  const atteintes = [];
  let borneInf = true;
  const finsReelles = [];   /* v4.128 : les vraies fins de vie (hors bornes inférieures) */""",
"6a. finsReelles déclarées")

remplace(
"""      atteintes.push(derniereConforme ?? 0);
      if(echec) borneInf = false;""",
"""      atteintes.push(derniereConforme ?? 0);
      if(echec){ borneInf = false; finsReelles.push(derniereConforme ?? 0); }""",
"6b. les fins réelles comptées")

remplace(
"""  if(!atteintes.length) return null;
  return { moyenne: atteintes.reduce((a,b)=>a+b,0) / atteintes.length,
           essais: atteintes.length, borneInf, min: Math.min(...atteintes) };
}""",
"""  if(!atteintes.length) return null;
  /* v4.128 (LOT 3, point 3) — min / N / fins réelles / borne inférieure
     exposés ; la moyenne n'est honnête qu'à partir de 5 fins de vie
     RÉELLES (les essais arrêtés à la visée sont des bornes inférieures,
     ils ne comptent pas comme des fins de vie). */
  const moyenneFins = finsReelles.length >= 5
    ? finsReelles.reduce((a,b)=>a+b, 0) / finsReelles.length : null;
  return { moyenne: atteintes.reduce((a,b)=>a+b, 0) / atteintes.length,
           essais: atteintes.length, borneInf, min: Math.min(...atteintes),
           finsReelles: finsReelles.length, moyenneFins };
}

/* v4.128 (LOT 3) — la charnière réelle PAR LOGEMENT : la substitution de la
   fourchette substitue logement par logement, là où une fin de vie est
   mesurée. Rend [{ logementId, min, moyenne(fins ≥ 5), finsReelles }] ou null. */
function charniereReelleParLogement(sc){
  const ids = (sc.outils||[]).flatMap(o => (o.logements||[]).map(l => l.id));
  if(!ids.length) return null;
  const out = [];
  ids.forEach(id => {
    const r = charniereReelle(sc, id);
    if(r) out.push({ logementId: id, min: r.min, moyenne: r.moyenneFins, finsReelles: r.finsReelles });
  });
  return out.length ? out : null;
}""",
"6c. le retour étendu + parLogement")

# ── 7. charniereReelle par logement (pour la substitution) ───────────────────
remplace(
"""  const cfgA = Object.assign({}, cfg);""",
"""  const cfgA = Object.assign({}, cfg);""",
"7. ancre (inchangée)") if False else None

# la substitution a besoin de parLogement : charniereReelle(sc) sans logementId
# retourne déjà tout sc — MAIS par logement : j'ajoute parLogement au retour
remplace(
"""  if(!atteintes.length) return null;
  /* v4.128 (LOT 3, point 3) — min / N / fins réelles / borne inférieure
     exposés ; la moyenne n'est honnête qu'à partir de 5 fins de vie
     RÉELLES (les essais arrêtés à la visée sont des bornes inférieures,
     ils ne comptent pas comme des fins de vie). */
  const moyenneFins = finsReelles.length >= 5
    ? finsReelles.reduce((a,b)=>a+b, 0) / finsReelles.length : null;
  return { moyenne: atteintes.reduce((a,b)=>a+b, 0) / atteintes.length,
           essais: atteintes.length, borneInf, min: Math.min(...atteintes),
           finsReelles: finsReelles.length, moyenneFins };
}""",
"""  if(!atteintes.length) return null;
  /* v4.128 (LOT 3, point 3) — min / N / fins réelles / borne inférieure
     exposés ; la moyenne n'est honnête qu'à partir de 5 fins de vie
     RÉELLES (les essais arrêtés à la visée sont des bornes inférieures,
     ils ne comptent pas comme des fins de vie). */
  const moyenneFins = finsReelles.length >= 5
    ? finsReelles.reduce((a,b)=>a+b, 0) / finsReelles.length : null;
  return { moyenne: atteintes.reduce((a,b)=>a+b, 0) / atteintes.length,
           essais: atteintes.length, borneInf, min: Math.min(...atteintes),
           finsReelles: finsReelles.length, moyenneFins };
}

/* v4.128 (LOT 3) — la charnière réelle PAR LOGEMENT : la substitution de la
   fourchette substitue logement par logement, là où une fin de vie est
   mesurée. Rend [{ logementId, min, moyenne(fins ≥ 5), finsReelles }] ou null. */
function charniereReelleParLogement(sc){
  const ids = (sc.outils||[]).flatMap(o => (o.logements||[]).map(l => l.id));
  if(!ids.length) return null;
  const out = [];
  ids.forEach(id => {
    const r = charniereReelle(sc, id);
    if(r) out.push({ logementId: id, min: r.min, moyenne: r.moyenneFins, finsReelles: r.finsReelles });
  });
  return out.length ? out : null;
}""",
"7. charniereReelleParLogement")

# coutsDetailCharniere lit parLogement (pas parLogement.length)
remplace(
"""  const reel = charniereReelle(sc);
  if(!reel || !reel.parLogement || !reel.parLogement.length) return null;
  const map = {};
  reel.parLogement.forEach(e => {""",
"""  const parLogement = charniereReelleParLogement(sc);
  if(!parLogement) return null;
  const map = {};
  parLogement.forEach(e => {""",
"7b. la substitution lit charniereReelleParLogement")

# ── 8. plaquettesParAn : conditionnement + casse ─────────────────────────────
remplace(
"""function plaquettesParAn(l, volume){
  const a = parseFloat(l.aretes), c = parseFloat(l.charniere);
  if(!volume || !a || !c) return null;
  return volume / (a * c);
}""",
"""function plaquettesParAn(l, volume, conditionnement, casse){
  const a = parseFloat(l.aretes), c = parseFloat(l.charniere);
  if(!volume || !a || !c) return null;
  let n = volume / (a * c);
  /* v4.128 (LOT 3, point 5) — conditionnement (boîte de N, arrondi au
     supérieur) et taux de casse (%), OPTIONNELS : vides = inchangé. */
  const cond = parseFloat(conditionnement);
  if(!isNaN(cond) && cond > 0) n = Math.ceil(n / cond) * cond;
  const cx = parseFloat(casse);
  if(!isNaN(cx) && cx > 0) n = n * (1 + cx / 100);
  return n;
}""",
"8. plaquettesParAn : conditionnement + casse")

# ── 9. le rebut : N + échantillon trop faible ────────────────────────────────
remplace(
"""function tauxRebutDe(sc){
  const manuel = parseFloat(sc.tauxRebutAnnuel);
  if(!isNaN(manuel) && manuel >= 0) return { taux: manuel, source: "saisi" };
  const r = scrapStats(sc).rate;
  return r === null ? null : { taux: r, source: "journal" };
}""",
"""function tauxRebutDe(sc){
  const manuel = parseFloat(sc.tauxRebutAnnuel);
  if(!isNaN(manuel) && manuel >= 0) return { taux: manuel, source: "saisi" };
  const r = scrapStats(sc).rate;
  if(r === null) return null;
  /* v4.128 (LOT 3, point 6) : le N (le nombre de pièces du journal) voyage
     avec le taux — l'affichage peut dire « échantillon trop faible ». */
  return { taux: r, source: "journal", n: (sc.scrapLog || []).length };
}""",
"9a. tauxRebutDe : le N")

# ── 10. la fusion : le conflit d'horloge < 10 min ────────────────────────────
remplace(
"""      const dL = esL.modifieLe || "", dE = esE.modifieLe || "";
      if(dL && dE && dE > dL){ scLocal.essais[i] = esE; bilan.essaisMaj++; }
      else if(dL && dE && dL > dE){ bilan.essaisConserves++; }""",
"""      const dL = esL.modifieLe || "", dE = esE.modifieLe || "";
      /* v4.128 (LOT 3, point 7) — un écart de modification de MOINS DE 10 MIN
         n'est pas arbitré en silence : les horloges des deux postes ne sont
         pas synchrones, « le plus récent » ne veut rien dire. La version
         locale est conservée, le conflit est signalé nommément. */
      const tL = Date.parse(dL), tE = Date.parse(dE);
      if(!isNaN(tL) && !isNaN(tE) && Math.abs(tE - tL) < 600000){
        bilan.essaisConserves++;
        bilan.conflits.push({ chemin, essai: (esL.titre || esL.id) + (esE.titre && esE.titre !== esL.titre ? " (reçu sous le nom « " + esE.titre + " »)" : ""),
          raison: "modifiés à moins de 10 minutes d'écart (horloges des deux postes non synchrones) — version locale conservée, à trancher à la main" });
        return;
      }
      if(dL && dE && dE > dL){ scLocal.essais[i] = esE; bilan.essaisMaj++; }
      else if(dL && dE && dL > dE){ bilan.essaisConserves++; }""",
"10. la fusion : le conflit d'horloge")

# ── 11. version + NOUVEAUTES ─────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.127.1";', 'const TOOL_VERSION = "4.128.0";', "11a. TOOL_VERSION")

ancre = 'const NOUVEAUTES = [\n'
assert s.count(ancre) == 1
entree = (
    '  { version:"4.128.0", date:"28/10/2026", points:[\n'
    '    "<b>Le chiffre de tête dit enfin ce qu\\u2019il mesure : l\\u2019outillage.</b> Coût et gain de tête = <b>plaquettes + pièces détachées</b>. Le <b>temps machine</b> et le <b>rebut</b> ont leurs tuiles propres, jamais sommées avec l\\u2019outillage (un cumul n\\u2019existe que sur demande explicite, libellé « cumul des deux axes »). Le <b>gain porte son étiquette</b> : « objectif, non mesuré » à la charnière visée, <b>« mesuré (min, N essais) »</b> dès qu\\u2019une vraie fin de vie est observée — la fourchette visée / moyenne / minimum est calculée et visible. La durée de vie réelle affiche <b>minimum, N et « ≥ »</b> (la moyenne seulement à 5 vraies fins de vie). Les heures machine parlent : <b>« plus rapide » / « plus lent »</b>, plus de signe seul. Et le rebut nomme son <b>échantillon</b> (« trop faible » sous le seuil)."\n'
    '  ]},\n'
)
s = s.replace(ancre, ancre + entree, 1)
print("ok : entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch LOT 3 posé :", n0, "->", len(s))
