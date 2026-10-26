# -*- coding: utf-8 -*-
"""Tour 95 — v4.112.0 — complément Hermes du 26/10 soir (décisions Benjamin).

A. L'APPARIEMENT DE SECOURS INTRA-OUTIL (option a tranchée) : dans un outil
   déjà apparié par numéro, des logements aux noms divergents mais en nombre
   ÉGAL s'apparient par position à l'intérieur de l'outil — jamais entre
   outils, toujours tracé (« apparié par secours — noms divergents » dans le
   dépliant, « N logement(s) apparié(s) par secours » dans la réconciliation).
   Compteurs inégaux → PAS de repli : le déséquilibre reste visible.
B. LA MENTION DES SORTIS SUR LE BADGE DU GROUPE : « groupe : cycle −15 % ·
   dont 1 poste sorti » — un outil de la référence est « sorti » quand aucun
   de ses logements n'est apparié ; il compte dans le groupe ref dont il
   était simultané. Le détail chiffré reste dans « non réparti »."""
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


# ── A1. la passe 1 devient outil par outil : noms, puis secours tracé ────────
remplace(
"""  const paires = [], prisA = new Set(), prisB = new Set();
  /* passe 1 — numéro d'outil puis nom de logement */
  const index = new Map();
  B.forEach((fb, j) => {
    if(!numeroFiable(fb)) return;
    const k = numDe(fb) + "·" + nomDe(fb);
    if(!index.has(k)) index.set(k, j);
  });
  A.forEach((fa, i) => {
    if(!numeroFiable(fa)) return;
    const k = numDe(fa) + "·" + nomDe(fa);
    const j = index.get(k);
    if(j !== undefined && !prisB.has(j)){
      paires.push({ a: fa, b: B[j], parPosition: false });
      prisA.add(i); prisB.add(j); index.delete(k);
    }
  });""",
"""  const paires = [], prisA = new Set(), prisB = new Set();
  let nbParSecours = 0;
  /* passe 1 — numéro d'outil puis nom de logement. v4.112 (décision Benjamin
     du 26/10 soir) : à l'intérieur d'un outil déjà apparié par numéro, des
     logements aux noms divergents mais en nombre ÉGAL s'apparient par SECOURS
     positionnel — jamais entre outils, toujours tracé. Des compteurs inégaux
     ne se replient pas : le déséquilibre reste visible (sortie + ajout nommés,
     c'est l'information). */
  const parNumeroA = new Map(), parNumeroB = new Map();
  A.forEach((fa, i) => { if(!numeroFiable(fa)) return; const n = numDe(fa);
    if(!parNumeroA.has(n)) parNumeroA.set(n, []);
    parNumeroA.get(n).push({ fa, i }); });
  B.forEach((fb, j) => { if(!numeroFiable(fb)) return; const n = numDe(fb);
    if(!parNumeroB.has(n)) parNumeroB.set(n, []);
    parNumeroB.get(n).push({ fb, j }); });
  parNumeroA.forEach((coteA, n) => {
    const coteB = parNumeroB.get(n) || [];
    coteA.forEach(({ fa, i }) => {
      const m = coteB.findIndex(({ fb, j }) => !prisB.has(j) && nomDe(fb) === nomDe(fa));
      if(m > -1){ paires.push({ a: fa, b: coteB[m].fb, parPosition: false });
        prisA.add(i); prisB.add(coteB[m].j); }
    });
    const restesA = coteA.filter(({ i }) => !prisA.has(i));
    const restesB = coteB.filter(({ j }) => !prisB.has(j));
    if(restesA.length && restesA.length === restesB.length){
      for(let k = 0; k < restesA.length; k++){
        paires.push({ a: restesA[k].fa, b: restesB[k].fb, parPosition: false, parSecours: true });
        prisA.add(restesA[k].i); prisB.add(restesB[k].j);
        nbParSecours++;
      }
    }
  });""",
"A1. passe 1 : noms puis secours intra-outil tracé")

# ── A2. le rendu porte le compte de secours ──────────────────────────────────
remplace(
'  return { paires, sorties, ajouts, nbParPosition: paires.filter(p => p.parPosition).length };',
'  return { paires, sorties, ajouts, nbParPosition: paires.filter(p => p.parPosition).length, nbParSecours };',
"A2. rendu : nbParSecours")

# ── A3. verdictParOutil : propage parSecours, compte les outils sortis par groupe ref ──
remplace(
"""    const g = parCle.get(cle);
    g.paires.push(pr);
    if(pr.parPosition) g.parPosition = true;
  });""",
"""    const g = parCle.get(cle);
    g.paires.push(pr);
    if(pr.parPosition) g.parPosition = true;
    if(pr.parSecours) g.parSecours = true;
  });""",
"A3a. le groupe d'outils trace le secours")

remplace(
"""      return { lRef: lB, lSc: lS, parPosition: pr.parPosition, indice,""",
"""      return { lRef: lB, lSc: lS, parPosition: pr.parPosition, parSecours: !!pr.parSecours, indice,""",
"A3b. le logement porte parSecours")

# ── A4. sortisGroupe : les outils entièrement sortis du groupe de référence ──
remplace(
"""  outils.forEach(g => {
    g.gainEurAn = (g.techniqueEurAn !== null || g.prodEurAn !== null)
      ? (g.techniqueEurAn || 0) + (g.prodEurAn || 0) : null;
  });""",
"""  outils.forEach(g => {
    g.gainEurAn = (g.techniqueEurAn !== null || g.prodEurAn !== null)
      ? (g.techniqueEurAn || 0) + (g.prodEurAn || 0) : null;
  });
  /* v4.112 — la mention des postes sortis du groupe (complément §2) : un
     outil de la référence est « sorti » quand AUCUN de ses logements n'est
     apparié ; il compte dans le groupe ref dont il était simultané. Le détail
     chiffré reste dans « non réparti », sémantique 4.111 inchangée. */
  const apparieRef = new Set();
  appar.paires.forEach(pr => apparieRef.add(pr.a.o));
  const outilsSortisRef = (base.outils || []).filter(o => (o.logements || []).length && !apparieRef.has(o));
  const groupesRef = [];
  (base.outils || []).forEach((o, i) => {
    if(i > 0 && o.simultaneAvecPrecedent && groupesRef.length) groupesRef[groupesRef.length - 1].push(o);
    else groupesRef.push([o]);
  });
  outils.forEach(g => {
    const gr = groupesRef.find(m => m.indexOf(g.oRef) > -1) || [];
    g.sortisGroupe = outilsSortisRef.filter(o => gr.indexOf(o) > -1).length;
  });""",
"A4. sortisGroupe (outils entièrement sortis, par groupe de référence)")

# ── A5. parLogement porte le compte pour le badge du groupe ─────────────────
remplace(
"""  outils.forEach(g => g.logements.forEach(x => parLogement.set(x.lSc.id, {
    indice: x.indice, pctCycle: x.pctCycle, vfSc: x.vfSc, parPosition: x.parPosition,""",
"""  outils.forEach(g => g.logements.forEach(x => parLogement.set(x.lSc.id, {
    indice: x.indice, pctCycle: x.pctCycle, vfSc: x.vfSc, parPosition: x.parPosition, parSecours: x.parSecours,
    sortisGroupe: g.sortisGroupe,""",
"A5. parLogement : parSecours + sortisGroupe")

remplace(
"""           outils, sorties, ajouts, nbParPosition: appar.nbParPosition,""",
"""           outils, sorties, ajouts, nbParPosition: appar.nbParPosition, nbParSecours: appar.nbParSecours,""",
"A6. le rendu porte nbParSecours")

# ── A7. le dépliant trace le secours ─────────────────────────────────────────
remplace(
'      ${vpLog.parPosition ? `<div class="ap-detail-l"><span>Appariement</span><b>par position — numéro d\'outil absent ou en doublon (défaut tracé)</b></div>` : ""}',
'      ${vpLog.parPosition ? `<div class="ap-detail-l"><span>Appariement</span><b>par position — numéro d\'outil absent ou en doublon (défaut tracé)</b></div>` : ""}\n      ${vpLog.parSecours ? `<div class="ap-detail-l"><span>Appariement</span><b>par secours — noms divergents (même outil, même nombre de logements)</b></div>` : ""}',
"A7. dépliant : la ligne de secours")

# ── A8. la réconciliation compte les secours ─────────────────────────────────
remplace(
'outil(s) apparié(s) par position (numéro absent ou en doublon)` : ""}${vp.chronoComplet',
'outil(s) apparié(s) par position (numéro absent ou en doublon)` : ""}${vp.nbParSecours ? ` · ${vp.nbParSecours} logement(s) apparié(s) par secours (noms divergents)` : ""}${vp.chronoComplet',
"A8. réconciliation : les secours comptés")

# ── B. le badge du groupe porte la mention des sortis ────────────────────────
remplace(
"""  /* le ratio du GROUPE simultané = celui de son membre le plus long (min Vc·f) */
  const grpPctCycle = g => {
    if(!vp) return null;
    let best = null;
    g.forEach(oi => (sc.outils[oi].logements || []).forEach(l => {
      const e = vp.parLogement.get(l.id);
      if(e && e.pctCycle !== null && e.vfSc !== null && (best === null || e.vfSc < best.vfSc)) best = e;
    }));
    return best ? best.pctCycle : null;
  };""",
"""  /* le ratio du GROUPE simultané = celui de son membre le plus long (min Vc·f) */
  const grpPctCycle = g => {
    if(!vp) return null;
    let best = null;
    g.forEach(oi => (sc.outils[oi].logements || []).forEach(l => {
      const e = vp.parLogement.get(l.id);
      if(e && e.pctCycle !== null && e.vfSc !== null && (best === null || e.vfSc < best.vfSc)) best = e;
    }));
    return best ? best.pctCycle : null;
  };
  /* v4.112 — la mention des postes sortis (complément §2) : les membres du
     groupe candidat partagent le groupe de référence de leurs paires ; le
     compte des outils entièrement sortis de ce groupe dit ce que le badge du
     groupe a perdu. Le détail chiffré reste dans « non réparti ». */
  const grpSortis = g => {
    if(!vp) return 0;
    let n = 0;
    g.forEach(oi => (sc.outils[oi].logements || []).forEach(l => {
      const e = vp.parLogement.get(l.id);
      if(e && e.sortisGroupe > n) n = e.sortisGroupe;
    }));
    return n;
  };""",
"B1. grpSortis pour le badge du groupe")

remplace(
"""    const gPct = grpPctCycle(g);
    const gBadge = gPct !== null ? ` <span class="ap-cycle ${gPct > 0 ? "rapide" : gPct < 0 ? "lent" : ""}" title="Ratio des temps du groupe, porté par son outil le plus long — estimation par les conditions de coupe (Vc·f), jamais des secondes.">${gPct > 0 ? "groupe : cycle −" + gPct + " %" : gPct < 0 ? "groupe : cycle +" + Math.abs(gPct) + " %" : "groupe : cycle = réf."}</span>` : "";""",
"""    const gPct = grpPctCycle(g);
    const gS = grpSortis(g);
    const gMention = gS ? ` · dont ${gS} poste${gS > 1 ? "s" : ""} sorti${gS > 1 ? "s" : ""}` : "";
    const gBadge = (gPct !== null || gMention) ? ` <span class="ap-cycle ${gPct > 0 ? "rapide" : gPct < 0 ? "lent" : ""}" title="Ratio des temps du groupe, porté par son outil le plus long — estimation par les conditions de coupe (Vc·f), jamais des secondes. Les postes sortis de la référence ne comptent pas dans le ratio : leur coût vit dans « non réparti » de la réconciliation.">groupe :${gPct !== null ? (gPct > 0 ? " cycle −" + gPct + " %" : gPct < 0 ? " cycle +" + Math.abs(gPct) + " %" : " cycle = réf.") : ""}${gMention}</span>` : "";""",
"B2. le badge du groupe porte la mention")

io.open(p, "w", encoding="utf-8").write(s)
print("patch A posé :", n0, "->", len(s))
