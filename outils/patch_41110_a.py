# -*- coding: utf-8 -*-
"""Tour 94 — v4.111.0 — LE VERDICT PAR OUTIL (demande Hermes/Benjamin du
26/10, incident T543 D1). Ancres exactes + assert avant chaque remplacement.

  1. CSS : badges cycle/gain, outil sorti/ajouté, dégradé du gain (jamais
     imprimé), ligne de réconciliation, ligne « dont sorties » du verdict.
  2. Module : appariementOutils (par numéro, repli positionnel tracé),
     verdictParOutil (indices Vc·f, deux leviers, sorties/ajouts,
     réconciliation), verdictSortiesHTML (la ligne dédiée du verdict).
  3. Tuile : l'indice vient de l'appariement par numéro (plus jamais
     flatsSc.indexOf), badges visibles sans déplier, dépliant deux leviers,
     dégradé data-gain.
  4. Composition : verdictParOutil une fois par fiche, badge du groupe
     simultané, badges côté base (sorti de : …), ligne de réconciliation.
  5. Verdict : la ligne « dont sorties du scénario ».
  6. Version 4.111.0 + NOUVEAUTES + tests runTests.
"""
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


# ── 1. CSS ───────────────────────────────────────────────────────────────────
remplace(
""".ap-manque{font-family:var(--font-mono); font-size:11px; font-weight:500; color:var(--amber); margin-top:6px;}
.ap-manque.ap-bloquant{color:var(--red);}""",
""".ap-manque{font-family:var(--font-mono); font-size:11px; font-weight:500; color:var(--amber); margin-top:6px;}
.ap-manque.ap-bloquant{color:var(--red);}
/* v4.111 — verdict par outil : badges cycle/gain, outil sorti/ajouté, dégradé du gain */
.ap-badges{display:flex; gap:6px; flex-wrap:wrap; margin:-3px 0 8px;}
.ap-cycle{display:inline-block; padding:2px 8px; border-radius:999px; font-family:var(--font-mono); font-size:10.5px; font-weight:500; background:var(--gray-100); color:var(--ink-soft); white-space:nowrap;}
.ap-cycle.rapide{background:var(--blue-light); color:var(--blue);}
.ap-cycle.lent{background:color-mix(in srgb, var(--red-dark) 12%, var(--surface)); color:var(--red-dark);}
.ap-hors{display:inline-block; padding:2px 8px; border-radius:999px; font-family:var(--font-mono); font-size:10.5px; font-weight:500;
  background:color-mix(in srgb, var(--red-dark) 10%, var(--surface)); color:var(--red-dark);
  box-shadow:inset 0 0 0 1px color-mix(in srgb, var(--red-dark) 35%, transparent); white-space:nowrap;}
.ap-tuile[data-gain]{border-left-color:var(--gain-coul, var(--outil-couleur, var(--blue)));
  background:linear-gradient(90deg, color-mix(in srgb, var(--gain-coul) 9%, var(--surface-alt)) 0%, var(--surface-alt) 60%);}
@media print{ .ap-tuile[data-gain]{border-left-color:var(--outil-couleur, var(--blue)); background:var(--surface-alt);} }
.ap-reconcil{margin-top:10px; padding:9px 12px; border:1px dashed var(--border); border-radius:var(--radius-sm); font-size:12px; line-height:1.5; color:var(--ink-soft);}
.ap-reconcil b{color:var(--ink);}
.foot-verdict .fv-sortie{margin-top:6px; font-size:12px; font-weight:600; color:var(--on-fill-bad); line-height:1.45;}""",
"1. CSS verdict par outil")

# ── 2. le module ─────────────────────────────────────────────────────────────
remplace(
"""  return corps ? `<div class="foot-detail-inner">${corps}</div>` : "";
}

/* ---- seuil de bascule : le point ou le scenario cesse d'etre gagnant ----""",
"""  return corps ? `<div class="foot-detail-inner">${corps}</div>` : "";
}

/* ---- v4.111 — LE VERDICT PAR OUTIL (demande Hermes/Benjamin du 26/10) ----
   L'incident : le verdict « +16,8 k€/an » du SL500 sur EMAG 1 incluait
   SILENCIEUSEMENT la suppression du logement T543 D1 (9,8 k€/an de la
   référence à lui seul). Contre-mesure structurelle : un verdict global
   qu'on ne peut plus refaire en additionnant les tuiles n'existe plus.

   L'appariement va par NUMÉRO d'outil puis nom de logement — JAMAIS par
   position dans la liste (supprimer un outil du milieu décalait toutes les
   comparaisons). Un outil sans numéro ou en doublon : repli positionnel
   pour celui-là seul, avec le défaut tracé (« apparié par position »). */
function appariementOutils(scRef, scCand){
  const flats = sc => (sc.outils || []).flatMap(o => (o.logements || []).map(l => ({ o, l })));
  const A = flats(scRef), B = flats(scCand);
  const numDe = f => String((f.o && f.o.numero) || "").trim().toUpperCase();
  const nomDe = f => String((f.l && f.l.nom) || "").trim().toUpperCase();
  const compteNumeros = sc => {
    const m = new Map();
    (sc.outils || []).forEach(o => {
      const n = String(o.numero || "").trim().toUpperCase();
      if(n) m.set(n, (m.get(n) || 0) + 1);
    });
    return m;
  };
  const cA = compteNumeros(scRef), cB = compteNumeros(scCand);
  const numeroFiable = f => { const n = numDe(f); return !!n && cA.get(n) === 1 && cB.get(n) === 1; };
  const paires = [], prisA = new Set(), prisB = new Set();
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
  });
  /* passe 2 — repli positionnel, outils SANS numéro fiable seulement */
  const rA = [], rB = [];
  A.forEach((fa, i) => { if(!prisA.has(i) && !numeroFiable(fa)) rA.push(i); });
  B.forEach((fb, j) => { if(!prisB.has(j) && !numeroFiable(fb)) rB.push(j); });
  const nRepli = Math.min(rA.length, rB.length);
  for(let k = 0; k < nRepli; k++){
    paires.push({ a: A[rA[k]], b: B[rB[k]], parPosition: true });
    prisA.add(rA[k]); prisB.add(rB[k]);
  }
  const sorties = [], ajouts = [];
  A.forEach((fa, i) => { if(!prisA.has(i)) sorties.push(fa); });
  B.forEach((fb, j) => { if(!prisB.has(j)) ajouts.push(fb); });
  return { paires, sorties, ajouts, nbParPosition: paires.filter(p => p.parPosition).length };
}
/* Le verdict par outil : les indices par logement, les deux leviers séparés,
   les sorties/ajouts nommés, et la réconciliation qui refait le verdict en
   additionnant les tuiles. Sans chrono complet des deux côtés : pas de levier
   productivité — le % de conditions (Vc·f) reste un pourcentage, jamais des
   secondes inventées (décision Benjamin du 26/10). */
function verdictParOutil(sc, cfg, ligne, ref, baseCmp){
  cfg = cfg || config;
  const base = baseCmp || baselineScenario();
  if(!base || base.id === sc.id || sc.baseline) return null;
  const volume = volumeAnnuel(ref, cfg);
  const appar = appariementOutils(base, sc);
  const nb = v => { const x = parseFloat(v); return isNaN(x) ? null : x; };
  const chronoComplet = cycleDetailStatus(base, cfg).complete && cycleDetailStatus(sc, cfg).complete;
  const lg = ligne || getActiveLigne();
  const tBrut = lg ? parseFloat(lg.coutHoraire) : NaN;
  const taux = (chronoComplet && !isNaN(tBrut) && tBrut > 0) ? tBrut : null;
  const tempsOutil = o => {
    let s = 0, n = 0;
    (o.logements || []).forEach(l => { const c = parseFloat(l.tempsCoupe); if(!isNaN(c)){ s += c; n++; } });
    return n ? s : null;
  };
  const numeroDe = f => String((f.o && f.o.numero) || "").trim().toUpperCase() || "?";
  /* les paires regroupées par outil de la référence */
  const outils = [], parCle = new Map();
  appar.paires.forEach(pr => {
    const cle = numeroDe(pr.a) + "|" + (pr.a.o.id || "");
    if(!parCle.has(cle)) parCle.set(cle, { numero: numeroDe(pr.a), numeroSc: numeroDe(pr.b),
      oRef: pr.a.o, oSc: pr.b.o, paires: [], parPosition: false,
      prodEurAn: null, bottleneck: false, simultane: false });
    const g = parCle.get(cle);
    g.paires.push(pr);
    if(pr.parPosition) g.parPosition = true;
  });
  parCle.forEach(g => {
    g.logements = g.paires.map(pr => {
      const lB = pr.a.l, lS = pr.b.l;
      const vB = nb(lB.vc) * nb(lB.f), vS = nb(lS.vc) * nb(lS.f);
      const indice = (vB > 0 && vS > 0) ? vB / vS * 100 : null;
      const pcB = posCost(lB), pcS = posCost(lS);
      /* le levier TECHNIQUE — toujours, dès que les deux coûts pièce existent */
      const technique = (pcB !== null && pcS !== null && volume) ? (pcB - pcS) * volume : null;
      /* le levier parle métier : ce qui a bougé sur le logement */
      let levier = "";
      if(technique !== null && Math.abs(technique) >= 0.5){
        const vieUp = nb(lS.charniere) !== null && nb(lB.charniere) !== null && nb(lS.charniere) > nb(lB.charniere);
        const prixBaisse = nb(lS.prix) !== null && nb(lB.prix) !== null && nb(lS.prix) < nb(lB.prix);
        levier = vieUp && prixBaisse ? "charnière améliorée + prix plaquette"
               : vieUp ? "charnière améliorée"
               : prixBaisse ? "prix plaquette" : "défavorable";
      }
      return { lRef: lB, lSc: lS, parPosition: pr.parPosition, indice,
               vfSc: vS > 0 ? vS : null,
               pctCycle: indice === null ? null : Math.round(100 - indice),
               pcB, pcS, technique, levier };
    });
    g.techniqueEurAn = (volume && g.logements.every(x => x.technique !== null))
      ? g.logements.reduce((a, x) => a + x.technique, 0) : null;
  });
  /* le levier PRODUCTIVITÉ : groupes simultanés du scénario — max, jamais la
     somme (le groupe vaut son outil le plus long, comme le cycle mesuré) */
  if(chronoComplet && taux && volume){
    const matchedSc = new Map();
    outils.forEach(g => matchedSc.set(g.oSc, g));
    const groupes = [];
    sc.outils.forEach((o, i) => {
      if(i > 0 && o.simultaneAvecPrecedent && groupes.length) groupes[groupes.length - 1].push(o);
      else groupes.push([o]);
    });
    groupes.forEach(membres => {
      const tSc = membres.map(tempsOutil);
      if(tSc.some(v => v === null)) return;
      const maxSc = Math.max(...tSc);
      const refs = membres.map(o => matchedSc.get(o)).filter(g => g && tempsOutil(g.oRef) !== null);
      if(!refs.length) return;
      const maxRef = Math.max(...refs.map(g => tempsOutil(g.oRef)));
      const prod = (maxRef - maxSc) * (taux / 3600) * volume;
      const g = matchedSc.get(membres[tSc.indexOf(maxSc)]);
      if(g){ g.prodEurAn = prod; g.bottleneck = true; g.simultane = membres.length > 1; }
    });
  }
  outils.forEach(g => {
    g.gainEurAn = (g.techniqueEurAn !== null || g.prodEurAn !== null)
      ? (g.techniqueEurAn || 0) + (g.prodEurAn || 0) : null;
  });
  /* sorties et ajouts, chiffrés du seul côté où ils existent */
  const chiffre = (f, signe) => { const pc = posCost(f.l);
    return { numero: numeroDe(f), nom: f.l.nom || "—",
             coutEurAn: (pc !== null && volume) ? signe * pc * volume : null }; };
  const sorties = appar.sorties.map(f => chiffre(f, 1));
  const ajouts = appar.ajouts.map(f => chiffre(f, -1));
  const coutParOutil = liste => {
    const m = new Map();
    liste.forEach(f => {
      const pc = posCost(f.l);
      const cur = m.get(f.o) || { cout: 0, complet: true };
      if(pc === null || !volume) cur.complet = false; else cur.cout += pc * volume;
      m.set(f.o, cur);
    });
    return m;
  };
  /* la réconciliation : tuiles + sorties − ajouts + non réparti = verdict.
     L'écart résiduel (rebut, pièces détachées, outils sans pendant) sort en
     clair — jamais masqué (§3.5). */
  const annuel = volume ? bilanAnnuel(sc, cfg, ligne, ref, base) : null;
  const verdict = (annuel && annuel.gainAnnuel !== undefined) ? annuel.gainAnnuel : null;
  const sommeTuiles = outils.reduce((a, g) => a + (g.gainEurAn || 0), 0);
  const sommeSorties = sorties.reduce((a, s) => a + (s.coutEurAn || 0), 0);
  const sommeAjouts = ajouts.reduce((a, s) => a + (s.coutEurAn || 0), 0);
  const nonReparti = (verdict !== null) ? verdict - sommeTuiles - sommeSorties - sommeAjouts : null;
  const gains = outils.map(g => g.gainEurAn).filter(v => v !== null);
  const maxAbsGain = gains.length ? Math.max(...gains.map(Math.abs)) : null;
  const parLogement = new Map();
  outils.forEach(g => g.logements.forEach(x => parLogement.set(x.lSc.id, {
    indice: x.indice, pctCycle: x.pctCycle, vfSc: x.vfSc, parPosition: x.parPosition,
    technique: x.technique, levier: x.levier,
    gainOutil: g.gainEurAn, prodOutil: g.prodEurAn, bottleneck: g.bottleneck,
    simultane: g.simultane, numero: g.numero })));
  return { volume, chronoComplet, taux, baseNom: base.name || "référence",
           outils, sorties, ajouts, nbParPosition: appar.nbParPosition,
           sommeTuiles, sommeSorties, sommeAjouts, verdict, nonReparti,
           maxAbsGain, parLogement,
           ajoutsParOutil: coutParOutil(appar.ajouts),
           sortiesParOutil: coutParOutil(appar.sorties) };
}
/* la ligne dédiée du verdict — l'incident T543 D1 rendu impossible à rater */
function verdictSortiesHTML(vpo){
  if(!vpo || (!vpo.sorties.length && !vpo.ajouts.length)) return "";
  const parts = [];
  if(vpo.sorties.length)
    parts.push(`dont sorties du scénario : ${vpo.sommeSorties > 0 ? "−" + fmtEuroCourt(Math.round(vpo.sommeSorties)) + "/an" : "non chiffrable (prix ou charnière manquants)"} (${vpo.sorties.map(s => s.numero + " · " + s.nom).join(", ")} — un poste de la référence supprimé, pas une plaquette améliorée)`);
  if(vpo.ajouts.length)
    parts.push(`dont ajouts hors référence : ${vpo.sommeAjouts !== 0 ? "+" + fmtEuroCourt(Math.round(Math.abs(vpo.sommeAjouts))) + "/an" : "non chiffrable"} (${vpo.ajouts.map(s => s.numero + " · " + s.nom).join(", ")})`);
  return `<div class="fv-sortie" title="La composition du gain, poste par poste — la contre-mesure de l'incident du 26/10 (T543 D1).">${parts.join(" · ")}</div>`;
}

/* ---- seuil de bascule : le point ou le scenario cesse d'etre gagnant ----""",
"2. module appariementOutils + verdictParOutil + verdictSortiesHTML")

# ── 3a. la tuile : signature ─────────────────────────────────────────────────
remplace(
"function apercuLogementHTML(sc, o, l, couleur, oi, volume, totalAnnuel, partRef){",
"function apercuLogementHTML(sc, o, l, couleur, oi, volume, totalAnnuel, partRef, vp, ajoutCoutEur, sortieInfos){",
"3a. signature apercuLogementHTML")

# ── 3b. l'indice par appariement + badges + dégradé + dépliant ───────────────
remplace(
"""  let indiceCond = null;
  if(!sc.baseline){
    const flatsSc = sc.outils.flatMap(o => o.logements||[]);
    const baseB = baselineScenario();
    const lb = baseB ? (baseB.outils.flatMap(o => o.logements||[]))[flatsSc.indexOf(l)] : null;
    if(lb){
      const vSc = parseFloat(l.vc) * parseFloat(l.f), vB = parseFloat(lb.vc) * parseFloat(lb.f);
      if(vSc > 0 && vB > 0) indiceCond = vB / vSc * 100;
    }
  }""",
"""  /* v4.111 — l'indice vient de l'APARIEMENT PAR NUMÉRO (verdictParOutil),
     plus jamais de la position dans la liste : supprimer un outil du milieu
     ne doit décaler aucune comparaison (le piège n°1 de la demande du 26/10). */
  const vpLog = (vp && vp.parLogement.get(l.id)) || null;
  const indiceCond = vpLog ? vpLog.indice : null;
  /* les badges du verdict par outil, visibles SANS déplier (décision §4.4) */
  const apBadges = [];
  if(vpLog){
    if(vpLog.pctCycle !== null){
      apBadges.push(`<span class="ap-cycle ${vpLog.pctCycle > 0 ? "rapide" : vpLog.pctCycle < 0 ? "lent" : ""}" title="Estimation par les conditions de coupe (Vc·f) : ratio des temps à géométrie égale — jamais un temps en secondes.">${vpLog.pctCycle > 0 ? "cycle −" + vpLog.pctCycle + " %" : vpLog.pctCycle < 0 ? "cycle +" + Math.abs(vpLog.pctCycle) + " %" : "cycle = réf."}</span>`);
    } else if(vpLog.indice === null){
      apBadges.push(`<span class="ap-cycle" title="Vc ou f manque d'un côté — rien n'est estimé.">cycle —</span>`);
    }
    if(vpLog.gainOutil !== null)
      apBadges.push(`<span class="ap-cycle ${vpLog.gainOutil >= 0 ? "rapide" : "lent"}" title="Gain de l'outil = somme de ses leviers (technique, plus productivité si le chrono est complet). C'est lui qui colore la tuile.">${vpLog.gainOutil >= 0 ? "+" : "−"} ${fmtEuroCourt(Math.abs(vpLog.gainOutil))}/an</span>`);
  }
  if(ajoutCoutEur)
    apBadges.push(`<span class="ap-hors" title="Cet outil n'existe pas dans la référence : son coût n'est pas un gain de plaquettes — il change le périmètre de la comparaison, et la réconciliation le dit.">ajouté — absent de la référence : ${ajoutCoutEur.complet ? fmtEuroCourt(Math.round(ajoutCoutEur.cout)) + " €/an" : "prix ou charnière incomplets"}</span>`);
  if(sortieInfos && sortieInfos.length)
    apBadges.push(`<span class="ap-hors" title="Cet outil a été retiré de ces scénarios : leur verdict porte la ligne « dont sorties du scénario » qui le nomme.">sorti de : ${sortieInfos.map(s => escapeAttr(s.nom) + " (" + fmtEuroCourt(Math.round(s.cout)) + " €/an)").join(", ")}</span>`);
  /* le dégradé rouge → vert porte le gain €/an de l'outil (le verdict
     financier) ; 0 = gris neutre, jamais imprimé (règle des couleurs de ligne) */
  const gainCouleur = (() => {
    if(!vp || !vpLog || vpLog.gainOutil === null || vp.maxAbsGain === null) return null;
    if(Math.abs(vpLog.gainOutil) < 0.5) return "var(--ink-faint)";
    const t = Math.min(100, Math.round(Math.abs(vpLog.gainOutil) / vp.maxAbsGain * 100));
    return vpLog.gainOutil > 0 ? `color-mix(in srgb, var(--ink-faint), var(--green) ${t}%)`
                               : `color-mix(in srgb, var(--ink-faint), var(--red-dark) ${t}%)`;
  })();
  /* le dépliant : les deux leviers séparés, jamais fondus (§4.3) */
  const detailVerdict = (vpLog && (vpLog.technique !== null || vpLog.parPosition || vpLog.gainOutil !== null)) ? `
      <div class="ap-detail-sep">Verdict par outil — vs « ${escapeAttr(vp ? vp.baseNom : "référence")} »</div>
      ${vpLog.parPosition ? `<div class="ap-detail-l"><span>Appariement</span><b>par position — numéro d'outil absent ou en doublon (défaut tracé)</b></div>` : ""}
      ${vpLog.technique !== null ? `<div class="ap-detail-l"><span>Levier technique — Δ plaquettes (réf − scénario) × production${vpLog.levier ? " · " + escapeAttr(vpLog.levier) : ""}</span><b>${vpLog.technique >= 0 ? "+" : "−"} ${escapeAttr(fmtEuroCourt(Math.abs(vpLog.technique)))}/an</b></div>`
        : `<div class="ap-detail-l"><span>Levier technique</span><b>— prix, arêtes ou charnière incomplets d'un côté</b></div>`}
      ${vp && vp.chronoComplet === false ? `<div class="ap-detail-l"><span>Levier productivité</span><b>hors temps machine — mesures de cycle incomplètes (tout en %, jamais des secondes inventées)</b></div>`
        : (vpLog.simultane && !vpLog.bottleneck ? `<div class="ap-detail-l"><span>Levier productivité</span><b>porté par l'outil le plus long du groupe simultané</b></div>` : "")}
      ${vpLog.bottleneck && vpLog.prodOutil !== null ? `<div class="ap-detail-l"><span>Levier productivité — Δ temps machine × taux horaire${vpLog.simultane ? " (groupe simultané : le plus long pilote)" : ""}</span><b>${vpLog.prodOutil >= 0 ? "+" : "−"} ${escapeAttr(fmtEuroCourt(Math.abs(vpLog.prodOutil)))}/an</b></div>` : ""}
      ${vpLog.gainOutil !== null ? `<div class="ap-detail-l ap-detail-total"><span>Gain de l'outil — somme des leviers disponibles</span><b>${vpLog.gainOutil >= 0 ? "+" : "−"} ${escapeAttr(fmtEuroCourt(Math.abs(vpLog.gainOutil)))}/an</b></div>` : ""}` : "";""",
"3b. indice par appariement + badges + dégradé + dépliant deux leviers")

# ── 3c. le dépliant du cycle : % estimé + section verdict ────────────────────
remplace(
"""      ${indiceCond !== null ? `<div class="ap-detail-l"><span>Indice conditions vs base (Vc·f, 100 = base)</span><b>${fmt(indiceCond,0)}</b></div>` : ""}
      ${!stC.complete ? `<div class="ap-detail-l"><span>Pris en compte dans le cycle</span><b>non — ${stC.filled}/${stC.total} logements renseignés, l'indice global s'applique</b></div>` : ""}`;""",
"""      ${indiceCond !== null ? `<div class="ap-detail-l"><span>Indice conditions vs base (Vc·f, 100 = base)</span><b>${fmt(indiceCond,0)}</b></div>` : ""}
      ${vpLog && vpLog.pctCycle !== null ? `<div class="ap-detail-l"><span>Cycle estimé vs base — ratio des temps à géométrie égale (jamais des secondes)</span><b>${vpLog.pctCycle > 0 ? "−" + vpLog.pctCycle + " % (plus rapide)" : vpLog.pctCycle < 0 ? "+" + Math.abs(vpLog.pctCycle) + " % (plus lent)" : "= base"}</b></div>` : ""}
      ${!stC.complete ? `<div class="ap-detail-l"><span>Pris en compte dans le cycle</span><b>non — ${stC.filled}/${stC.total} logements renseignés, l'indice global s'applique</b></div>` : ""}${detailVerdict}`;""",
"3c. dépliant cycle + section verdict")

# ── 3d. la tuile : dégradé + rangée de badges ────────────────────────────────
remplace(
"""  return `
    <div class="ap-tuile${detailOuvert ? " ouvert" : ""}" data-cle-detail="${escapeAttr(cleDetail)}" title="Cliquer pour déplier le détail du calcul${annuel !== null ? " du coût annuel" : ""}" style="--outil-couleur:${couleur};">""",
"""  return `
    <div class="ap-tuile${detailOuvert ? " ouvert" : ""}" data-cle-detail="${escapeAttr(cleDetail)}" title="Cliquer pour déplier le détail du calcul${annuel !== null ? " du coût annuel" : ""}" style="--outil-couleur:${couleur};${gainCouleur ? "--gain-coul:" + gainCouleur + ";" : ""}"${gainCouleur ? ` data-gain="1"` : ""}>""",
"3d. tuile data-gain")

remplace(
"""      <div class="ap-ref">${l.ref ? escapeAttr(l.ref) : `<em>référence plaquette non renseignée</em>`}</div>""",
"""      <div class="ap-ref">${l.ref ? escapeAttr(l.ref) : `<em>référence plaquette non renseignée</em>`}</div>
      ${apBadges.length ? `<div class="ap-badges">${apBadges.join("")}</div>` : ""}""",
"3e. rangée de badges sur la tuile")

# ── 4a. la composition : verdict par outil + sorties côté base ───────────────
remplace(
"""  const refSc = getActiveReference();
  const volume = refSc ? parseFloat(refSc.productionAnnuelle) : NaN;
  const nbLogements = sc.outils.reduce((n, o) => n + o.logements.length, 0);""",
"""  const refSc = getActiveReference();
  const volume = refSc ? parseFloat(refSc.productionAnnuelle) : NaN;
  const nbLogements = sc.outils.reduce((n, o) => n + o.logements.length, 0);
  /* v4.111 — le verdict par outil : la fiche se refait en additionnant les tuiles */
  const vp = !sc.baseline ? verdictParOutil(sc, config, null, refSc, null) : null;
  /* §4.4 côté référence — la base ouverte nomme les scénarios qui ont sorti l'outil */
  const sortiePar = new Map();
  if(sc.baseline && volume > 0){
    const opB = opContenantScenario(sc.id);
    if(opB) (opB.scenarios || []).forEach(cand => {
      if(cand.baseline || cand.id === sc.id) return;
      appariementOutils(sc, cand).sorties.forEach(f => {
        const pc = posCost(f.l);
        if(pc === null) return;
        if(!sortiePar.has(f.o)) sortiePar.set(f.o, []);
        sortiePar.get(f.o).push({ nom: cand.name || "scénario", cout: pc * volume });
      });
    });
  }
  const ajoutCout = new Map();
  if(vp) vp.ajoutsParOutil.forEach((v, o) => ajoutCout.set(o, v));
  /* le ratio du GROUPE simultané = celui de son membre le plus long (min Vc·f) */
  const grpPctCycle = g => {
    if(!vp) return null;
    let best = null;
    g.forEach(oi => (sc.outils[oi].logements || []).forEach(l => {
      const e = vp.parLogement.get(l.id);
      if(e && e.pctCycle !== null && e.vfSc !== null && (best === null || e.vfSc < best.vfSc)) best = e;
    }));
    return best ? best.pctCycle : null;
  };
  /* la réconciliation — la contre-mesure de l'incident du 26/10 (T543 D1) */
  const sgnEuro = v => (v >= 0 ? "+" : "−") + fmtEuroCourt(Math.round(Math.abs(v)));
  const reconcilHtml = (vp && vp.verdict !== null) ? `
      <div class="ap-reconcil" title="Le verdict global se refait en additionnant les tuiles. L'écart résiduel (rebut, pièces détachées, outils sans pendant) sort en clair, jamais masqué (§3.5)."><b>Réconciliation</b> — tuiles ${sgnEuro(vp.sommeTuiles)} · sorties ${sgnEuro(vp.sommeSorties)} · ajouts ${sgnEuro(vp.sommeAjouts)} · non réparti <b>${sgnEuro(vp.nonReparti)}</b> = <b>verdict ${sgnEuro(vp.verdict)}</b> /an${vp.nbParPosition ? ` · ${vp.nbParPosition} outil(s) apparié(s) par position (numéro absent ou en doublon)` : ""}${vp.chronoComplet ? "" : " · hors temps machine (mesures de cycle incomplètes)"}</div>` : "";""",
"4a. composition : verdict par outil + sortiePar + réconciliation")

# ── 4b. les tuiles reçoivent le verdict ──────────────────────────────────────
remplace(
"""  const tuileOutil = (o, oi) =>
    o.logements.map(l => apercuLogementHTML(sc, o, l, OUTIL_COLORS[oi % OUTIL_COLORS.length], oi, volume, totalAnnuelSc, partRefSc));""",
"""  const tuileOutil = (o, oi) =>
    o.logements.map(l => apercuLogementHTML(sc, o, l, OUTIL_COLORS[oi % OUTIL_COLORS.length], oi, volume, totalAnnuelSc, partRefSc, vp, ajoutCout.get(o), sortiePar.get(o)));""",
"4b. tuileOutil passe le verdict")

# ── 4c. le badge du groupe simultané ─────────────────────────────────────────
remplace(
"""    if(g.length === 1) return tuilesG.join("");
    return `<div class="ap-groupe-sim"><div class="ap-gs-tete">⇉ Travail simultané — ${g.length} outils usinent ensemble, seul le plus long compte dans le cycle</div><div class="ap-gs-tuiles">${tuilesG.join("")}</div></div>`;""",
"""    if(g.length === 1) return tuilesG.join("");
    const gPct = grpPctCycle(g);
    const gBadge = gPct !== null ? ` <span class="ap-cycle ${gPct > 0 ? "rapide" : gPct < 0 ? "lent" : ""}" title="Ratio des temps du groupe, porté par son outil le plus long — estimation par les conditions de coupe (Vc·f), jamais des secondes.">${gPct > 0 ? "groupe : cycle −" + gPct + " %" : gPct < 0 ? "groupe : cycle +" + Math.abs(gPct) + " %" : "groupe : cycle = réf."}</span>` : "";
    return `<div class="ap-groupe-sim"><div class="ap-gs-tete">⇉ Travail simultané — ${g.length} outils usinent ensemble, seul le plus long compte dans le cycle${gBadge}</div><div class="ap-gs-tuiles">${tuilesG.join("")}</div></div>`;""",
"4c. badge du groupe simultané")

# ── 4d. la ligne de réconciliation sous la grille ────────────────────────────
remplace(
"""      <div class="ap-grille">${tuiles}</div>
    </div>`;
}""",
"""      <div class="ap-grille">${tuiles}</div>
      ${reconcilHtml}
    </div>`;
}""",
"4d. réconciliation sous la grille")

# ── 5. le verdict : la ligne « dont sorties du scénario » ────────────────────
remplace(
"""  const horsMachine = !!(periVerdict && periVerdict.exclus.includes("temps machine"));
  const annuel = bilanAnnuel(sc);""",
"""  const horsMachine = !!(periVerdict && periVerdict.exclus.includes("temps machine"));
  const annuel = bilanAnnuel(sc);
  /* v4.111 — la composition du gain, nommée : l'incident du 26/10 (un
     « +16,8 k€/an » qui incluait silencieusement la suppression du T543 D1,
     9,8 k€/an) ne passe plus inaperçu. */
  const vpo = !sc.baseline ? verdictParOutil(sc, config, null, null, base) : null;""",
"5a. verdict : le verdict par outil")

remplace(
"""  return `<div class="foot-verdict ${classe}">
    <p class="fv-eyebrow">${eyebrow}</p>
    <div class="fv-titre">${titre}</div>
    ${sousTitre ? `<div class="fv-sous">${sousTitre}</div>` : ""}
  </div>`;""",
"""  return `<div class="foot-verdict ${classe}">
    <p class="fv-eyebrow">${eyebrow}</p>
    <div class="fv-titre">${titre}</div>
    ${sousTitre ? `<div class="fv-sous">${sousTitre}</div>` : ""}
    ${verdictSortiesHTML(vpo)}
  </div>`;""",
"5b. verdict : la ligne dédiée")

# ── 6. version + NOUVEAUTES ──────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.110.0";', 'const TOOL_VERSION = "4.111.0";', "6a. TOOL_VERSION")

remplace(
"""const NOUVEAUTES = [
  { version:"4.110.0", date:"26/10/2026", points:[""",
"""const NOUVEAUTES = [
  { version:"4.111.0", date:"26/10/2026", points:[
    "<b>Le verdict par outil : le gain se refait en additionnant les tuiles.</b> L'incident du 26/10 — un « +16,8 k€/an » qui incluait <b>silencieusement</b> la suppression du logement T543 D1 (9,8 k€/an de la référence à lui seul) — ne peut plus se reproduire. Chaque tuile outil porte son <b>badge de cycle estimé</b> par les conditions de coupe (« cycle −15 % » — Vc·f, jamais des secondes inventées) et son <b>gain €/an</b> qui colore la tuile du rouge au vert ; le dépliant détaille <b>deux leviers séparés</b> : technique (charnière/prix, toujours) et productivité (temps machine, seulement si le chrono est complet). Un outil supprimé ou ajouté face à la référence porte un <b>badge explicite</b>, le verdict affiche « <b>dont sorties du scénario</b> » en rouge, et une <b>ligne de réconciliation</b> refait le verdict en additionnant les tuiles — l'écart résiduel sort en clair. Les outils s'apparient par <b>numéro</b> (plus jamais par position dans la liste)."
  ]},
  { version:"4.110.0", date:"26/10/2026", points:[""",
"6b. entrée NOUVEAUTES")

# ── 7. les tests runTests ────────────────────────────────────────────────────
remplace(
"""          ok("badge codification : la fiche « Scénarios en validation » porte le badge — état et codification visibles ensemble",
             [planScenariosHTML(recapB).indexOf("codification attendue") > -1,
              planScenariosHTML(recapB).indexOf("En série — gain acté") > -1],
             [true, true]);
        } finally { catalogue = catAvB; }
      }""",
"""          ok("badge codification : la fiche « Scénarios en validation » porte le badge — état et codification visibles ensemble",
             [planScenariosHTML(recapB).indexOf("codification attendue") > -1,
              planScenariosHTML(recapB).indexOf("En série — gain acté") > -1],
             [true, true]);
        } finally { catalogue = catAvB; }
      }
      {
        /* v4.111 — LE VERDICT PAR OUTIL : appariement par numéro (jamais la
           position), deux leviers séparés, réconciliation tuiles = verdict.
           Le cas T543 D1 de la demande du 26/10, en fixture. */
        const mkV = (id, name, baseline, defs) => normalizeScenario({ id, name, baseline,
          outils: defs.map(d => ({ id: d.tid, numero: d.numero, simultaneAvecPrecedent: !!d.sim,
            logements: d.logements.map(g => ({ id: g.gid, nom: g.nom, prix: g.prix, aretes: g.aretes,
              charniere: g.charn, vc: g.vc, f: g.f, tempsCoupe: g.tps })) })) });
        const baseV = mkV("sVB", "Base VPO", true, [
          { tid: "tb1", numero: "T541", logements: [ { gid: "gb1", nom: "D1", prix: 40, aretes: 8, charn: 100, vc: 200, f: 0.3 } ] },
          { tid: "tb2", numero: "T543", logements: [ { gid: "gb2", nom: "D1", prix: 38, aretes: 4, charn: 700, vc: 180, f: 0.25 } ] },
          { tid: "tb3", numero: "T548", logements: [ { gid: "gb3", nom: "D1", prix: 30, aretes: 8, charn: 100, vc: 220, f: 0.3 } ] } ]);
        const candV = mkV("sVC", "Candidat VPO", false, [
          { tid: "tc1", numero: "T541", logements: [ { gid: "gc1", nom: "D1", prix: 40, aretes: 8, charn: 150, vc: 240, f: 0.3 } ] },
          { tid: "tc3", numero: "T548", logements: [ { gid: "gc3", nom: "D1", prix: 30, aretes: 8, charn: 120, vc: 260, f: 0.3 } ] } ]);
        const apV = appariementOutils(baseV, candV);
        ok("verdict par outil : l'appariement va par NUMÉRO — supprimer l'outil du milieu ne décale aucune comparaison",
           [apV.paires.length,
            apV.paires[0].a.o.numero + "↔" + apV.paires[0].b.o.numero,
            apV.paires[1].a.o.numero + "↔" + apV.paires[1].b.o.numero,
            apV.sorties.length, apV.sorties[0].o.numero, apV.nbParPosition],
           [2, "T541↔T541", "T548↔T548", 1, "T543", 0]);
        const baseP = mkV("sPB", "B pos", true, [ { tid: "tp1", numero: "", logements: [ { gid: "gp1", nom: "D1", prix: 10, aretes: 8, charn: 100, vc: 200, f: 0.3 } ] } ]);
        const candP = mkV("sPC", "C pos", false, [ { tid: "tp2", numero: "", logements: [ { gid: "gp2", nom: "D1", prix: 10, aretes: 8, charn: 150, vc: 200, f: 0.3 } ] } ]);
        ok("verdict par outil : sans numéro (ou en doublon) = repli positionnel pour celui-là seul, défaut TRACÉ",
           (() => { const a = appariementOutils(baseP, candP); return [a.paires.length, a.nbParPosition]; })(),
           [1, 1]);
        /* sans chrono : technique seule, réconciliation EXACTE (le poste T543
           D1 sorti de la référence est compté, jamais fondu) */
        const cfgV = Object.assign({}, config, { volumeActif: true });
        const refV = { productionAnnuelle: 10000 };
        const vpo = verdictParOutil(candV, cfgV, { coutHoraire: "45" }, refV, baseV);
        ok("verdict par outil : sans chrono — technique au centime, productivité absente, réconciliation EXACTE",
           [vpo.chronoComplet,
            Math.round(vpo.outils[0].techniqueEurAn * 100) / 100,
            Math.round(vpo.outils[1].techniqueEurAn * 100) / 100,
            vpo.outils.every(g => g.prodEurAn === null),
            Math.round(vpo.nonReparti * 100) / 100,
            Math.round((vpo.verdict - vpo.sommeTuiles - vpo.sommeSorties - vpo.sommeAjouts - vpo.nonReparti) * 100) / 100],
           [false, 166.67, 62.5, true, 0, 0]);
        ok("verdict par outil : l'indice de conditions (Vc·f) de T548 est le SIEN — jamais celui d'un voisin décalé",
           [Math.round(vpo.parLogement.get("gc3").indice),
            vpo.parLogement.get("gc3").pctCycle],
           [Math.round((220 * 0.3) / (260 * 0.3) * 100), Math.round(100 - (220 * 0.3) / (260 * 0.3) * 100)]);
        ok("verdict par outil : la ligne « dont sorties du scénario » nomme le poste supprimé (l'incident du 26/10 rendu visible)",
           [verdictSortiesHTML(vpo).indexOf("dont sorties du scénario") > -1,
            verdictSortiesHTML(vpo).indexOf("T543 · D1") > -1,
            verdictSortiesHTML(null) === ""],
           [true, true, true]);
        /* avec chrono complet : le levier productivité par groupe (max, jamais
           la somme) — et la réconciliation dit EN CLAIR ce qui sort du verdict */
        const baseT = mkV("sVBT", "Base chrono", true, [
          { tid: "tb1", numero: "T541", logements: [ { gid: "gb1", nom: "D1", prix: 40, aretes: 8, charn: 100, vc: 200, f: 0.3, tps: 60 } ] },
          { tid: "tb2", numero: "T543", logements: [ { gid: "gb2", nom: "D1", prix: 38, aretes: 4, charn: 700, vc: 180, f: 0.25, tps: 120 } ] },
          { tid: "tb3", numero: "T548", logements: [ { gid: "gb3", nom: "D1", prix: 30, aretes: 8, charn: 100, vc: 220, f: 0.3, tps: 60 } ] } ]);
        const candT = mkV("sVCT", "Candidat chrono", false, [
          { tid: "tc1", numero: "T541", logements: [ { gid: "gc1", nom: "D1", prix: 40, aretes: 8, charn: 150, vc: 240, f: 0.3, tps: 50 } ] },
          { tid: "tc3", numero: "T548", logements: [ { gid: "gc3", nom: "D1", prix: 30, aretes: 8, charn: 120, vc: 260, f: 0.3, tps: 50 } ] } ]);
        const vpoC = verdictParOutil(candT, Object.assign({}, cfgV), { coutHoraire: "45" }, refV, baseT);
        ok("verdict par outil : chrono complet — le levier productivité au centime (série : les temps se déduisent)",
           [vpoC.chronoComplet,
            Math.round(vpoC.outils[0].prodEurAn),
            Math.round(vpoC.outils[1].prodEurAn),
            Math.round(vpoC.nonReparti)],
           [true, 1250, 1250, -2500]);
        /* groupe simultané : max, jamais la somme — porté par le plus long */
        const candS = mkV("sVS", "Simultané VPO", false, [
          { tid: "ts1", numero: "T541", logements: [ { gid: "gs1", nom: "D1", prix: 40, aretes: 8, charn: 150, vc: 240, f: 0.3, tps: 50 } ] },
          { tid: "ts3", numero: "T548", sim: true, logements: [ { gid: "gs3", nom: "D1", prix: 30, aretes: 8, charn: 120, vc: 260, f: 0.3, tps: 40 } ] } ]);
        const vpoS = verdictParOutil(candS, Object.assign({}, cfgV), { coutHoraire: "45" }, refV, baseT);
        ok("verdict par outil : groupe simultané — le levier vaut le PLUS LONG (max, jamais la somme), porté par le pilote",
           [Math.round(vpoS.outils[0].prodEurAn), vpoS.outils[0].bottleneck,
            vpoS.outils[0].simultane, vpoS.outils[1].prodEurAn === null],
           [8750, true, true, true]);
        /* sans chrono : le HTML de la tuile n'invente AUCUNE seconde */
        const tuileHtml = apercuLogementHTML(candV, candV.outils[0], candV.outils[0].logements[0], "#3b82f6", 0, 10000, null, 0, vpo, null, null);
        ok("verdict par outil : sans chrono, la tuile n'invente AUCUNE seconde — tout en % et en €/an, dégradé posé",
           [new RegExp("[0-9](?:,[0-9]+)? s[^a-zà-ÿ]").test(tuileHtml),
            tuileHtml.indexOf("hors temps machine") > -1,
            tuileHtml.indexOf("data-gain") > -1,
            tuileHtml.indexOf("Levier technique") > -1],
           [false, true, true, true]);
      }""",
"7. tests runTests verdict par outil")

io.open(p, "w", encoding="utf-8").write(s)
print("patch 4.111.0 posé :", n0, "->", len(s))
