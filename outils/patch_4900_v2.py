# -*- coding: utf-8 -*-
"""Patch v4.90.0 (v2) : les trois lots de la revue Claude + décisions déléguées."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()
s = s.replace(chr(13) + chr(10), chr(10))   # normalisation LF : fin des ancres CRLF

def rep(av, ap, n=1):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, n)

NL = chr(10)
TAB = "  "

def multi(lignes):
    return NL.join(lignes)

# ═══ NORMALISATION DÉJÀ FAITE EN TÊTE ════════════════════════════════════════

# ═══ LOT 3 — P5 : ATELIER ════════════════════════════════════════════════════
rep('    <select id="atUsure"><option value="">—</option><option value="ok">OK</option><option value="limite">Usure limite</option><option value="changer">À changer</option></select>',
multi([
'    <div class="at-points-row">',
'      <button type="button" class="at-pm ${atelierCtx.usure === "" ? "actif" : ""}" data-at-usure="">—</button>',
'      <button type="button" class="at-pm ${atelierCtx.usure === "ok" ? "actif" : ""}" data-at-usure="ok">OK</button>',
'      <button type="button" class="at-pm ${atelierCtx.usure === "limite" ? "actif" : ""}" data-at-usure="limite">Limite</button>',
'      <button type="button" class="at-pm ${atelierCtx.usure === "changer" ? "actif" : ""}" data-at-usure="changer">À changer</button>',
'    </div>']))

rep('  const on = atelierCtx.axesOn || {};',
multi(['  const on = atelierCtx.axesOn || {};',
'  if(atelierCtx.usure === undefined) atelierCtx.usure = "";']))

rep('''  const champUsure = `<div class="at-champ"><label>Usure plaquette</label>
    <div class="at-points-row">
      <button type="button" class="at-pm ${atelierCtx.usure === "" ? "actif" : ""}" data-at-usure="">—</button>
      <button type="button" class="at-pm ${atelierCtx.usure === "ok" ? "actif" : ""}" data-at-usure="ok">OK</button>
      <button type="button" class="at-pm ${atelierCtx.usure === "limite" ? "actif" : ""}" data-at-usure="limite">Limite</button>
      <button type="button" class="at-pm ${atelierCtx.usure === "changer" ? "actif" : ""}" data-at-usure="changer">À changer</button>
    </div></div>`;''',
'''  const champUsure = `<div class="at-champ"><label>Usure plaquette</label>
    <div class="at-points-row">
      <button type="button" class="at-pm ${atelierCtx.usure === "" ? "actif" : ""}" data-at-usure="">—</button>
      <button type="button" class="at-pm ${atelierCtx.usure === "ok" ? "actif" : ""}" data-at-usure="ok">OK</button>
      <button type="button" class="at-pm ${atelierCtx.usure === "limite" ? "actif" : ""}" data-at-usure="limite">Limite</button>
      <button type="button" class="at-pm ${atelierCtx.usure === "changer" ? "actif" : ""}" data-at-usure="changer">À changer</button>
    </div></div>
    <div class="at-champ"><label>En direct</label><span id="atLive" style="font-weight:700;">—</span></div>`;''')

rep('''      if(cotesAt === "mono") champs.push(`<div class="at-champ"><label>${escapeAttr(libelleDe(sc))}</label><input type="number" step="0.001" inputmode="decimal" id="atV" placeholder="0,000"></div>`);
    else {
      if(cotesAt === "DG") champs.push(chipAxes("Côtés mesurés", ["D","G"]));
      const axesB = axesActifs(["D","G"], on.batt).filter(ax => cotesAt === "DG" ? true : ax === cotesAt);
      if(axesB.includes("D")) champs.push(`<div class="at-champ"><label>Droite</label><input type="number" step="0.001" inputmode="decimal" id="atD" placeholder="0,000"></div>`);
      if(axesB.includes("G")) champs.push(`<div class="at-champ"><label>Gauche</label><input type="number" step="0.001" inputmode="decimal" id="atG" placeholder="0,000"></div>`);
    }
  }''',
'''      const maxBatt = (Math.max(parseFloat(limiteDe(sc)) || 0.12, 0.12) * 10).toFixed(3);
      if(cotesAt === "mono") champs.push(`<div class="at-champ"><label>${escapeAttr(libelleDe(sc))}</label><input type="number" step="0.001" inputmode="decimal" min="0" max="${maxBatt}" id="atV" placeholder="0,000"></div>`);
    else {
      if(cotesAt === "DG") champs.push(chipAxes("Côtés mesurés", ["D","G"]));
      const axesB = axesActifs(["D","G"], on.batt).filter(ax => cotesAt === "DG" ? true : ax === cotesAt);
      if(axesB.includes("D")) champs.push(`<div class="at-champ"><label>Droite</label><input type="number" step="0.001" inputmode="decimal" min="0" max="${maxBatt}" id="atD" placeholder="0,000"></div>`);
      if(axesB.includes("G")) champs.push(`<div class="at-champ"><label>Gauche</label><input type="number" step="0.001" inputmode="decimal" min="0" max="${maxBatt}" id="atG" placeholder="0,000"></div>`);
    }
  }''')

rep('''  el.querySelectorAll("[data-at-pm]").forEach(b => b.addEventListener("click", () => {
    atelierCtx.pointMesure = b.getAttribute("data-at-pm"); renderAtelier();
  }));''',
'''  el.querySelectorAll("[data-at-pm]").forEach(b => b.addEventListener("click", () => {
    atelierCtx.pointMesure = b.getAttribute("data-at-pm"); renderAtelier();
  }));
  el.querySelectorAll("[data-at-usure]").forEach(b => b.addEventListener("click", () => {
    atelierCtx.usure = b.getAttribute("data-at-usure"); renderAtelier();
  }));
  /* v4.90 — la conformité se juge À LA FRAPPE : le badge en direct lit la
     valeur non encore enregistrée. Un 12 tapé pour 0,012 se voit tout de suite
     — la borne max bloque déjà la saisie absurde. */
  el.querySelectorAll("#atV, #atD, #atG").forEach(inp => inp.addEventListener("input", () => {
    const scL = data.find(x => x.id === atelierCtx.scId);
    const esL = scL && (scL.essais||[]).find(e => e.id === atelierCtx.essaiId);
    const live = document.getElementById("atLive");
    if(!live) return;
    if(!scL || !esL){ live.textContent = "—"; return; }
    const tentative = { batt:"", battD:"", battG:"" };
    const v = document.getElementById("atV"), d = document.getElementById("atD"), g = document.getElementById("atG");
    if(v) tentative.batt = v.value;
    if(d) tentative.battD = d.value;
    if(g) tentative.battG = g.value;
    const c2 = checkConformPrincipal(scL, tentative);
    live.textContent = c2 === true ? "✓ dans la tolérance" : c2 === false ? "⚠ hors tolérance" : "—";
    live.style.color = c2 === false ? "var(--red)" : c2 === true ? "var(--green)" : "var(--ink-soft)";
  }));''')

rep('''        ? `◎ Au-delà de la charnière visée (${prog.target} p) — la durée de vie dépasse l'objectif : prolongez tant que la cote tient, ou clôturez l'essai.`
        : `◎ Cette pièce atteint la charnière visée (${prog.target} p) — resserrez le pas de mesure vers la fin, ou décidez : prolonger / arrêter.`}''',
'''        ? `◎ Charnière dépassée (${prog.target} p) — prolonger ou clore ?`
        : `◎ Charnière atteinte (${prog.target} p) — mesurez plus serré.`}''')

rep('''    const usureSel = document.getElementById("atUsure");
    if(usureSel) row.usure = usureSel.value;''',
'''    row.usure = atelierCtx.usure || "";''')

# ═══ LOT 1 — P7 : BUGS VISIBLES ══════════════════════════════════════════════
rep('data-plan="${l.mabec}"', 'data-plan="${escapeAttr(l.mabec)}"', 3)

rep('''  const total = lignes.reduce((a, l) => a + (l.actif && l.gain ? l.gain : 0), 0);
  const actives = lignes.filter(l => l.actif).length;''',
'''  const total = lignes.reduce((a, l) => a + (l.actif && l.confirme && l.gain ? l.gain : 0), 0);
  const actives = lignes.filter(l => l.actif && l.confirme).length;''')

rep('''      ? `Promesse posée : <b>${actives} article(s)</b> en conversion — économie simulée <b>− ${fmtEuroCourt(Math.round(total))} / an</b>.`''',
'''      ? `Potentiel engagé : <b>${actives} article(s)</b> en conversion — économie simulée <b>− ${fmtEuroCourt(Math.round(total))} / an</b> (hypothèse : durée de vie SPK = ${Math.round(planReglages.relSpk)} % de l'actuelle).`''')

# ═══ LOT 2 — P3 : HONNÊTETÉ DU PLAN ══════════════════════════════════════════
rep('''let consoReelle = null;''',
'''let consoSemaines = 52;   /* v4.90 — l'extrapolation × 52 devient un réglage éditable */
let planReglages = { prixSpk: 5, relSpk: 100 };  /* v4.90 — le prix SUGGÉRÉ et l'hypothèse de durée de vie sortent du code (revue Claude P3) */
let consoReelle = null;''')

rep('''    const sugg = isoKY ? { iso: String(isoKY).replace(/KY3500/gi, "LKT640"), prix: 5 } : null;''',
'''    const sugg = isoKY ? { iso: String(isoKY).replace(/KY3500/gi, "LKT640"), prix: planReglages.prixSpk } : null;''')

rep('''    const piecesAn = reel ? (conso ? conso.qtySemaine * 52 : 0) : piecesAnTheo;''',
'''    const piecesAn = reel ? (conso ? conso.qtySemaine * consoSemaines : 0) : piecesAnTheo;
    const confirme = !!p.confirme;''')

rep('''    const gain = (actif && ciblePrix !== "" && ciblePrix !== null && prixA > 0 && sourceConso !== "sans")
      ? piecesAn * (prixA - Number(ciblePrix)) : null;
    return { mabec: g.mabec, isos: [...g.isos], prixA, coutAnnuel: g.coutAnnuel,
             piecesAn, piecesAnTheo, sourceConso, cibleIso, ciblePrix, etat: p.etat || "",
             actif, gain, auto: !!sugg };''',
'''    /* v4.90 — l'hypothèse de durée de vie est EXPLICITE : la cible SPK dure
       rel % de l'actuelle -> il en faut piecesAn × 100/rel. Et le seuil de
       neutralité dit la durée minimale pour ne pas perdre (revue Claude P3). */
    const rel = (Number(planReglages.relSpk) > 0) ? Number(planReglages.relSpk) : 100;
    const piecesCible = piecesAn * 100 / rel;
    const coutActuel = (sourceConso === "reelle" && conso) ? conso.qtySemaine * consoSemaines * prixA : g.coutAnnuel;
    const gain = (actif && confirme && ciblePrix !== "" && ciblePrix !== null && prixA > 0 && sourceConso !== "sans")
      ? coutActuel - piecesCible * Number(ciblePrix) : null;
    const seuil = (ciblePrix !== "" && ciblePrix !== null && prixA > 0) ? Number(ciblePrix) / prixA * 100 : null;
    return { mabec: g.mabec, isos: [...g.isos], prixA, coutAnnuel: g.coutAnnuel, coutActuel,
             piecesAn, piecesAnTheo, sourceConso, cibleIso, ciblePrix, etat: p.etat || "",
             actif, confirme, gain, seuil, auto: !!sugg };''')

rep('''      <span id="consoEtat" style="font-size:13px; color:#1b5ea6;">${etatConso}</span>
    </div>''',
'''      <span id="consoEtat" style="font-size:13px; color:#1b5ea6;">${etatConso}</span>
      <span style="font-weight:600;">Prix SPK défaut :</span> <input id="planPrixSpk" type="number" step="0.5" min="0.5" style="width:64px; font-family:var(--font-mono);" value="${planReglages.prixSpk}"> €
      <span style="font-weight:600;">Durée de vie SPK :</span> <input id="planRelSpk" type="number" step="5" min="1" style="width:64px; font-family:var(--font-mono);" value="${planReglages.relSpk}"> % de l'actuelle
      <span style="font-weight:600;">Semaines/an :</span> <input id="planSemaines" type="number" step="1" min="1" max="52" style="width:56px; font-family:var(--font-mono);" value="${consoSemaines}">
    </div>''')

rep('''          <td><input class="cell" style="width:74px; font-family:var(--font-mono);" type="number" step="0.01" data-plan="${escapeAttr(l.mabec)}" data-field="prixCible" value="${l.ciblePrix === "" ? "" : l.ciblePrix}" placeholder="5"></td>''',
'''          <td><input class="cell" style="width:74px; font-family:var(--font-mono);" type="number" step="0.01" data-plan="${escapeAttr(l.mabec)}" data-field="prixCible" value="${l.ciblePrix === "" ? "" : l.ciblePrix}" placeholder="5"><br><span class="simul-iso" title="Durée de vie minimale de la cible pour ne pas perdre : au-dessus de ce seuil, le passage gagne.">seuil ${l.seuil != null ? fmt(l.seuil, 0) : "—"} %</span></td>''')

rep('''          <td class="mono" style="${l.gain ? "color:#1a7a3f; font-weight:600;" : "color:#888;"}">${l.gain != null ? "− " + fmtEuroCourt(Math.round(l.gain)) : "potentiel"}</td>''',
'''          <td class="mono" style="${l.gain != null ? (l.gain > 0 ? "color:#1a7a3f; font-weight:600;" : "color:var(--red); font-weight:600;") : "color:#888;"}">${l.gain == null ? "potentiel" : (l.gain >= 0 ? "− " + fmtEuroCourt(Math.round(l.gain)) : "+ " + fmtEuroCourt(Math.round(-l.gain)))}</td>''')

rep('''          <td><select class="cell small" data-plan="${escapeAttr(l.mabec)}" data-field="etat">''',
'''          <td><input type="checkbox" data-planconf="${escapeAttr(l.mabec)}" ${l.confirme ? "checked" : ""} title="Prix cible confirmé — la ligne compte dans le potentiel tant que cette case est cochée"></td>
          <td><select class="cell small" data-plan="${escapeAttr(l.mabec)}" data-field="etat">''')

rep('''      <thead><tr><th>Article actuel</th><th>Libellés ISO</th><th>Prix actuel</th><th>Consommation</th><th>Cible SPK</th><th>Prix cible</th><th>État</th><th>Gain / an</th></tr></thead>''',
'''      <thead><tr><th>Article actuel</th><th>Libellés ISO</th><th>Prix actuel</th><th>Consommation</th><th>Cible SPK</th><th>Prix cible</th><th>Confirmé</th><th>État</th><th>Gain / an</th></tr></thead>''')

rep('''  wrap.querySelectorAll("[data-plan]").forEach(inp => inp.addEventListener("change", () => {
    const mabec = inp.getAttribute("data-plan"), field = inp.getAttribute("data-field");
    let e = plan.find(x => x.mabec === mabec);
    if(!e){ e = normalizePlanEntry({ mabec }); plan.push(e); }
    e[field] = field === "prixCible" ? (inp.value === "" ? "" : Number(inp.value)) : inp.value;
    saveData(); renderPlan();
  }));''',
'''  wrap.querySelectorAll("[data-plan]").forEach(inp => inp.addEventListener("change", () => {
    const mabec = inp.getAttribute("data-plan"), field = inp.getAttribute("data-field");
    let e = plan.find(x => x.mabec === mabec);
    if(!e){ e = normalizePlanEntry({ mabec }); plan.push(e); }
    e[field] = field === "prixCible" ? (inp.value === "" ? "" : Number(inp.value)) : inp.value;
    if(field === "prixCible" && inp.value !== "") e.confirme = true;  /* édité à la main = confirmé */
    saveData(); renderPlan();
  }));
  wrap.querySelectorAll("[data-planconf]").forEach(cb => cb.addEventListener("change", () => {
    const mabec = cb.getAttribute("data-planconf");
    let e = plan.find(x => x.mabec === mabec);
    if(!e){ e = normalizePlanEntry({ mabec }); plan.push(e); }
    e.confirme = cb.checked;
    saveData(); renderPlan();
  }));
  const ps = document.getElementById("planPrixSpk");
  if(ps) ps.addEventListener("change", () => { planReglages.prixSpk = parseFloat(ps.value) || 5; renderPlan(); });
  const rs = document.getElementById("planRelSpk");
  if(rs) rs.addEventListener("change", () => { planReglages.relSpk = Math.max(1, parseFloat(rs.value) || 100); renderPlan(); });
  const sm = document.getElementById("planSemaines");
  if(sm) sm.addEventListener("change", () => { consoSemaines = Math.max(1, Math.min(52, parseInt(sm.value) || 52)); renderPlan(); });''')

# ═══ LOT 2 — P2 : LE SIMULATEUR PARTAGE LA BASE ══════════════════════════════
rep('''function simulHTML(){
  const d = plaquettesCommunes();
  if(!d.groupes.length) return `<p class="panel-hint">Aucun logement de production avec prix, arêtes et durée de vie chiffrés. Le simulateur se nourrit des scénarios en production (star) des références à volume annuel.</p>`;''',
'''/* v4.90 — une seule base de consommation : le simulateur honore le même
   basculeur que le Plan (revue Claude P2 — deux écrans ne racontent pas deux
   histoires). Le réel est alloué au prorata du théorique entre les usages
   d'un même article, étiqueté, jamais muet en silence. */
function consoEffectifGroupe(g){
  const art = catalogue.find(a => a.mabec === g.mabec && a.prix !== "" && a.prix > 0);
  const prixA = art ? art.prix : (g.usages[0] ? g.usages[0].prix : 0);
  const theoPieces = prixA > 0 ? g.coutAnnuel / prixA : 0;
  const reel = (planSource === "reel") && consoReelle && consoReelle.parArticle;
  if(!reel) return { cout: g.coutAnnuel, pieces: theoPieces, source: "theo" };
  const c = consoReelle.parArticle[g.mabec];
  if(!c) return { cout: 0, pieces: 0, source: "sans" };
  const pieces = c.qtySemaine * consoSemaines;
  return { cout: pieces * prixA, pieces, source: "reelle" };
}

function simulHTML(){
  const d = plaquettesCommunes();
  if(!d.groupes.length) return `<p class="panel-hint">Aucun logement de production avec prix, arêtes et durée de vie chiffrés. Le simulateur se nourrit des scénarios en production (star) des références à volume annuel.</p>`;''')

rep('''        return `<tr>
          <td><input type="checkbox" class="simul-inc" data-mabec="${escapeAttr(g.mabec)}" checked></td>
          <td class="mono">${escapeAttr(g.mabec)}${g.isos.size ? `<br><span style="font-size:11.5px; color:#888;">${[...g.isos].map(x => escapeAttr(x)).join("<br>")}</span>` : ""}</td>
          <td>${g.usages.length} · ${escapeAttr([...new Set(g.usages.map(u => u.ligne))].join(", "))}</td>
          <td class="mono">${fmt(prixMin, 2)}${prixMin !== prixMax ? " – " + fmt(prixMax, 2) : ""} €</td>
          <td class="mono">${fmtEuroCourt(Math.round(g.coutAnnuel))}</td>
          <td class="mono simul-ec" data-cout="${g.coutAnnuel}">—</td>
        </tr>`;''',
'''        const eff = consoEffectifGroupe(g);
        return `<tr>
          <td><input type="checkbox" class="simul-inc" data-mabec="${escapeAttr(g.mabec)}" checked></td>
          <td class="mono">${escapeAttr(g.mabec)}${g.isos.size ? `<br><span class="simul-iso">${[...g.isos].map(x => escapeAttr(x)).join("<br>")}</span>` : ""}</td>
          <td>${g.usages.length} · ${escapeAttr([...new Set(g.usages.map(u => u.ligne))].join(", "))}</td>
          <td class="mono">${fmt(prixMin, 2)}${prixMin !== prixMax ? " – " + fmt(prixMax, 2) : ""} €</td>
          <td class="mono">${fmtEuroCourt(Math.round(eff.cout))}${eff.source === "reelle" ? ' <span class="simul-iso">(réel)</span>' : ""}</td>
          <td class="mono simul-ec" data-cout="${eff.cout}">—</td>
        </tr>`;''')

rep('''    <div class="simul-controles">
      <label>Baisse de prix générale <input type="number" id="simulTaux" min="0" max="90" step="0.5" value="10"> %</label>
      <span>sur les articles cochés</span>
    </div>''',
'''    <div class="simul-controles">
      <label>Baisse de prix générale <input type="number" id="simulTaux" min="0" max="90" step="0.5" value="${simulTauxCourant}"> %</label>
      <span>— base : ${planSource === "reel" && consoReelle ? "réelle extrapolée (le basculeur du Plan)" : "théorique"}</span>
    </div>''')

rep('''function simulRecalcul(){
  const taux = (parseFloat(document.getElementById("simulTaux")?.value) || 0) / 100;
  const d = plaquettesCommunes();
  let inclu = 0;
  const cbs = Array.from(document.querySelectorAll(".simul-inc"));
  const tds = Array.from(document.querySelectorAll(".simul-ec"));
  d.groupes.forEach((g, i) => {
    const actif = cbs[i] && cbs[i].checked;
    const ec = actif ? g.coutAnnuel * taux : 0;
    inclu += ec;
    if(tds[i]) tds[i].textContent = ec ? "− " + fmtEuroCourt(Math.round(ec)) : "—";
  });
  const total = document.getElementById("simulTotal");
  if(total) total.textContent = inclu ? "− " + fmtEuroCourt(Math.round(inclu)) : "—";
  const res = document.getElementById("simulResultat");
  if(res){
    const pct = d.totalAnnuel ? (inclu / d.totalAnnuel) * 100 : 0;
    res.innerHTML = inclu
      ? `Économie annuelle simulée : <b>${fmtEuroCourt(Math.round(inclu))} / an</b> — <b>${fmt(pct, 1)} %</b> du budget outillage en production (${fmtEuroCourt(Math.round(d.totalAnnuel))}).`
      : `Cochez des articles et choisissez un taux : l'économie se calcule sur le budget outillage des scénarios en production.`;
  }
}''',
'''let simulTauxCourant = 10;
function simulRecalcul(){
  const taux = (parseFloat(document.getElementById("simulTaux")?.value) || 0) / 100;
  simulTauxCourant = taux * 100;
  const d = plaquettesCommunes();
  let inclu = 0, totalEff = 0;
  const cbs = Array.from(document.querySelectorAll(".simul-inc"));
  const tds = Array.from(document.querySelectorAll(".simul-ec"));
  d.groupes.forEach((g, i) => {
    const eff = consoEffectifGroupe(g);
    totalEff += eff.cout;
    const actif = cbs[i] && cbs[i].checked;
    const ec = actif ? eff.cout * taux : 0;
    inclu += ec;
    if(tds[i]) tds[i].textContent = ec ? "− " + fmtEuroCourt(Math.round(ec)) : "—";
  });
  const total = document.getElementById("simulTotal");
  if(total) total.textContent = inclu ? "− " + fmtEuroCourt(Math.round(inclu)) : "—";
  const res = document.getElementById("simulResultat");
  if(res){
    const pct = totalEff ? (inclu / totalEff) * 100 : 0;
    res.innerHTML = inclu
      ? `Économie annuelle simulée : <b>${fmtEuroCourt(Math.round(inclu))} / an</b> — <b>${fmt(pct, 1)} %</b> du budget outillage en production (${fmtEuroCourt(Math.round(totalEff))}).`
      : `Cochez des articles et choisissez un taux : l'économie se calcule sur le budget outillage des scénarios en production.`;
  }
}''')

# ═══ LOT 3 — P4 : LE DERNIER EXPORT AFFICHÉ ══════════════════════════════════
rep('''let consoSemaines = 52;''',
'''let dernierExportLe = null;   /* v4.90 — l'accueil dit quand le suivi est sorti la dernière fois */
let consoSemaines = 52;''')

rep('''  const blob = new Blob([JSON.stringify(payload, null, 2)], {type:"application/json"});''',
'''  try{ localStorage.setItem(STORAGE_KEY + "_export", new Date().toISOString()); dernierExportLe = new Date().toISOString(); }catch(e){}
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type:"application/json"});''')

rep('''    ${accueilPiedHTML()}''',
'''    ${accueilPiedHTML()}
    <p class="panel-hint" style="text-align:center;">\U0001F4E4 Dernier export du suivi : ${dernierExportLe ? new Date(dernierExportLe).toLocaleString("fr-FR") : "jamais exporté — 💾 Exporter le suivi le fait en un clic"}</p>''')

rep('''try{ renderCatalogueDatlists(); }catch(e){}''',
'''try{ dernierExportLe = localStorage.getItem(STORAGE_KEY + "_export") || null; }catch(e){}
try{ renderCatalogueDatlists(); }catch(e){}''')

# ═══ LOT 1 — P6 : PLANCHER DE LISIBILITÉ ═════════════════════════════════════
rep(".os-sim{font-family:var(--font-mono); font-size:9.5px;",
    ".os-sim{font-family:var(--font-mono); font-size:11px;")
rep(".status-badge{display:inline-flex; align-items:center; gap:4px; font-family:var(--font-mono); font-size:10.5px;",
    ".status-badge{display:inline-flex; align-items:center; gap:4px; font-family:var(--font-mono); font-size:11.5px;")
rep(".oc-champ > label{font-family:var(--font-mono); font-size:11px;",
    ".oc-champ > label{font-family:var(--font-mono); font-size:12px;")
rep("--ink-soft:", "--ink-soft2:#6e7178; --ink-soft:", 1)
rep('''          <td class="mono">${escapeAttr(g.mabec)}${g.isos.size ? `<br><span style="font-size:11.5px; color:#888;">${[...g.isos].map(x => escapeAttr(x)).join("<br>")}</span>` : ""}</td>''',
'''          <td class="mono">${escapeAttr(g.mabec)}${g.isos.size ? `<br><span class="simul-iso">${[...g.isos].map(x => escapeAttr(x)).join("<br>")}</span>` : ""}</td>''')
rep('''        <td style="font-size:12px; color:#888;">${escapeAttr(a.iso || "—")}</td>''',
'''        <td style="font-size:12.5px; color:var(--ink-soft);">${escapeAttr(a.iso || "—")}</td>''')
rep(".simul-note { background:#eef4fb;",
'''.simul-iso { font-size:12.5px; color:var(--ink-soft); }
.panel.simul-maxi .simul-iso { font-size:14.5px; }
.simul-note { background:#eef4fb;''')

# ═══ LOT 1 — P7 : L'ORDRE DU RÉCIT COMMERCIAL ════════════════════════════════
rep('''      <button class="primary small" id="pfSimul" title="''',
'''      <button class="primary small" id="pfCatalogue" title="La vérité prix/article : un MABEC = un prix. Export/import CSV, propagation aux logements avec rapport">📚 Catalogue</button>
      <button class="primary small" id="pfPlan" title="Le pas-à-pas commercial : article par article, la cible SPK et le gain annuel — révélé ligne par ligne">⚔️ Plan de conversion</button>
      <button class="primary small" id="pfSimul" title="''', 1)

# ═══ P7 : LE CADENCE RETIRE (décision : pas mesuré, pas projeté) ═════════════
rep('''    ${bloc("03", "Cadence", bloc3)}
''', "")

# ═══ P8 : DÉCISION — MONOLITHE CANONIQUE, ARCHIVES INTACTES ══════════════════
rep("/* barre d'outils simplifiée :",
'''/* v4.90 — DÉCISION (Benjamin délègue, Tour 73) : le monolithe bilan_economique.html
   est l'outil CANONIQUE ; proto/, projet3/ et 2resume/ restent dans le dépôt
   comme archives de recherche, hors périmètre de déploiement. Le découpage par
   assembleur est en file (contrainte : sortie identique à l'octet).
/* barre d'outils simplifiée :''')

# ── version + nouveautés ──────────────────────────────────────────────────────
s = s.replace('const TOOL_VERSION = "4.89.1";', 'const TOOL_VERSION = "4.90.0";', 1)
rep('''const NOUVEAUTES = [
  { version:"4.89.1", date:"14/10/2026", points:[''',
'''const NOUVEAUTES = [
  { version:"4.90.0", date:"14/10/2026", points:[
    "<b>Les retours de la revue extérieure, appliqués.</b> <b>Plan de conversion</b> : le prix cible se confirme case par case (le total ne compte que le confirmé), l'<b>hypothèse de durée de vie</b> est affichée et réglable, chaque ligne montre son <b>seuil de neutralité</b>, le prix suggéré est un réglage — et « Promesse » s'appelle « Potentiel ». <b>Le Simulateur partage le basculeur</b> du Plan : une seule base de consommation sur tous les écrans. <b>Saisie atelier</b> : usure en grosses pastilles, conformité affichée <b>en direct</b> à la frappe, bornes sur les champs. <b>Lisibilité</b> : plancher de tailles et contrastes remontés. L'accueil affiche la date du dernier export, le bloc Cadence (jamais mesuré) quitte la projection, et les boutons suivent l'ordre du récit : Catalogue → Plan → Simulateur."
  ]},
  { version:"4.89.1", date:"14/10/2026", points:[''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='\n').write(s)
print("patch v4.90.0 (v2) appliqué : les trois lots + décisions")
