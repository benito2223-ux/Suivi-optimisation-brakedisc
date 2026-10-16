# -*- coding: utf-8 -*-
"""Patch v4.49 : CPP pièce complet (Zone 1) + feuille de route (Synthèse)."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# ---- 1. helpers v4.49 (après outilsManquants) ----
avant = """  const manquants = [];
  const restants = Object.assign({}, dispo);
  (base.outils || []).forEach(t => {
    const p = prefixe(t.numero);
    if((restants[p] || 0) > 0){ restants[p]--; return; }
    manquants.push(t);
  });
  return manquants;
}"""
apres = avant + """

/* ---- v4.49 — le coût pièce COMPLET : la pièce n'est pas une OP ------------------------
   L'outil pense par OP ; l'atelier pense par pièce. Cette agrégation somme, pour la
   référence affichée, le CPP de prod (scénario « base excel ») de chaque OP, le meilleur
   scénario d'essai disponible par OP, et le confronte à la cible du site (cibleCPP).
   % de chemin = ce que le meilleur en cours a déjà parcouru de prod vers la cible. */
function pieceCPPComplet(){
  const ref = getActiveReference();
  if(!ref) return null;
  const ops = [];
  ref.ops.forEach(op => {
    ops.push(dansContexteOp(op, () => {
      const base = (op.scenarios||[]).find(x => /base excel/i.test(x.name||""));
      const tBase = base ? coutsDetail(base).total : null;
      let meilleur = null;
      (op.scenarios||[]).forEach(sc => {
        if(/base excel/i.test(sc.name||"")) return;
        const t = coutsDetail(sc).total;
        if(t === null) return;
        if(!meilleur || t < meilleur.cout) meilleur = { sc, cout: t };
      });
      return { op, base, tBase, meilleur };
    }));
  });
  const connues = ops.filter(o => o.tBase !== null && o.tBase !== undefined);
  if(!connues.length) return null;
  const prod = connues.reduce((a,o) => a + o.tBase, 0);
  const enCours = connues.reduce((a,o) => a + (o.meilleur && o.meilleur.cout < o.tBase ? o.meilleur.cout : o.tBase), 0);
  const cible = (ref.cibleCPP !== "" && ref.cibleCPP != null && !isNaN(parseFloat(ref.cibleCPP))) ? parseFloat(ref.cibleCPP) : null;
  let chemin = null;
  if(cible !== null && prod > cible && prod > 0) chemin = Math.max(0, Math.min(100, ((prod - enCours) / (prod - cible)) * 100));
  return { ref, ops: connues, prod, enCours, cible, chemin };
}
/* statut de progression d'une OP : ce que l'atelier demande — réalisé / en cours / rien */
function statutOP(o){
  const scs = (o.op.scenarios||[]).filter(sc => !/base excel/i.test(sc.name||""));
  if(scs.some(sc => sc.statut === "serie")) return { cls:"ok", txt:"passé en série" };
  if(scs.some(sc => sc.statut === "valide")) return { cls:"ok", txt:"validé 5× — à passer en série" };
  if(scs.some(sc => (sc.essais||[]).length)) return { cls:"pending", txt:"essai en cours" };
  return { cls:"arrete", txt:"prod seule" };
}
/* la barre prod → cible, partagée par le bandeau pièce (Zone 1) et la feuille de route */
function barreRouteHTML(p){
  if(!p) return "";
  const pct = p.chemin === null ? 0 : Math.round(p.chemin);
  const cibleTxt = p.cible === null ? "cible non renseignée" : "cible site : " + fmt(p.cible,3) + " €";
  return `<div class="route-wrap">
    <div class="route-track"><div class="route-fill" style="width:${pct}%;"></div>
      <span class="route-mono">${fmt(p.prod,3)} € prod</span>
      ${p.chemin !== null ? `<span class="route-pct">${pct} % du chemin</span>` : ""}
      <span class="route-cible">${cibleTxt}</span>
    </div>
  </div>`;
}
/* bandeau Zone 1 : la pièce complète d'un coup d'œil */
function pieceCPPBannerHTML(){
  const p = pieceCPPComplet();
  if(!p) return "";
  const chips = p.ops.map(o => {
    const st = statutOP(o);
    const delta = o.meilleur && o.meilleur.cout < o.tBase ? ` <em>· ${escapeAttr(String(o.meilleur.sc.name).slice(0,26))} −${fmt(o.tBase - o.meilleur.cout,3)} €</em>` : "";
    return `<span class="pcb-op">${escapeAttr(String(o.op.nom||"OP").trim())} <b>${fmt(o.tBase,3)} €</b>${delta} <i class="pcb-st ${st.cls}">${st.txt}</i></span>`;
  }).join("");
  return `<div class="pcb-banner">
    <span class="pcb-l">Coût pièce complet — ${escapeAttr(p.ref.nom || "")}</span>
    <div class="pcb-ops">${chips}</div>
    <span class="pcb-total">${fmt(p.prod,3)} €<small>/pièce toutes OP</small></span>
    ${p.enCours < p.prod ? `<span class="pcb-encours">meilleur en cours : ${fmt(p.enCours,3)} € (−${fmt(p.prod - p.enCours,3)} €)</span>` : ""}
    ${barreRouteHTML(p)}
  </div>`;
}
/* feuille de route dans la vue de synthèse : global, par OP, statuts */
function feuilleRouteHTML(){
  const p = pieceCPPComplet();
  if(!p) return `<div class="synthese-block"><h3>Feuille de route — coût pièce complet</h3><p class="chart-empty">Aucune OP de cette référence n'a de scénario « base excel » chiffrable.</p></div>`;
  const vol = parseFloat(p.ref.productionAnnuelle);
  const rows = p.ops.map(o => {
    const st = statutOP(o);
    const essaiTxt = o.meilleur
      ? `${escapeAttr(o.meilleur.sc.name)} — <b>${fmt(o.meilleur.cout,3)} €</b> (−${fmt(o.tBase - o.meilleur.cout,3)} €/pièce${!isNaN(vol) && vol > 0 ? " · " + escapeAttr(libelleAnnuel((o.tBase - o.meilleur.cout) * vol)) + "/an" : ""})`
      : "aucun essai — prod seule";
    return `<div class="fr-row">
      <span class="fr-op">${escapeAttr(String(o.op.nom||"OP").trim())}</span>
      <span class="fr-prod">prod ${fmt(o.tBase,3)} €</span>
      <span class="fr-essai">${essaiTxt}</span>
      <span class="pcb-st ${st.cls}">${st.txt}</span>
    </div>`;
  }).join("");
  return `<div class="synthese-block">
    <h3>Feuille de route — coût pièce complet vs cible</h3>
    <div class="fr-global">
      <div class="fr-chiffres">
        <span><b>${fmt(p.prod,3)} €</b> prod (somme des OP)</span>
        ${p.enCours < p.prod ? `<span><b>${fmt(p.enCours,3)} €</b> meilleur en cours</span>` : ""}
        ${p.cible !== null ? `<span><b>${fmt(p.cible,3)} €</b> cible site</span>` : `<span>cible non renseignée</span>`}
        ${p.chemin !== null && !isNaN(vol) && vol > 0 ? `<span class="fr-gain">gain disponible aujourd'hui : ${escapeAttr(libelleAnnuel((p.prod - p.enCours) * vol))}/an</span>` : ""}
      </div>
      ${barreRouteHTML(p)}
    </div>
    <div class="fr-rows">${rows}</div>
  </div>`;
}"""
assert s.count(avant) == 1, "helpers v4.49"
s = s.replace(avant, apres)

# ---- 2. bandeau dans Zone 1 ----
avant = "      ${baseBannerHTML()}"
apres = "      ${baseBannerHTML()}\n      ${pieceCPPBannerHTML()}"
assert s.count(avant) == 1, "zone 1"
s = s.replace(avant, apres)

# ---- 3. feuille de route en tête de la synthèse ----
avant = """function syntheseHTML(){
  return syntheseTableHTML() + cascadeGainHTML() + dispersionEquipeHTML() + multiChartHTML();
}"""
apres = """function syntheseHTML(){
  return feuilleRouteHTML() + syntheseTableHTML() + cascadeGainHTML() + dispersionEquipeHTML() + multiChartHTML();
}"""
assert s.count(avant) == 1, "syntheseHTML"
s = s.replace(avant, apres)

# ---- 4. CSS ----
avant = "/* v4.47 — groupe d'outils simultanés : bloc ambre visible dans la vue d'ensemble."
apres = """/* v4.49 — bandeau coût pièce complet (Zone 1) + feuille de route (Synthèse) */
.pcb-banner{display:flex; align-items:center; gap:12px 16px; flex-wrap:wrap; background:var(--surface);
  border:1px solid var(--border); border-left:4px solid var(--green); border-radius:var(--radius);
  padding:10px 14px; margin-bottom:14px;}
.pcb-l{font-size:10px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-faint);}
.pcb-ops{display:flex; gap:8px; flex-wrap:wrap;}
.pcb-op{font-family:var(--font-mono); font-size:11px; color:var(--ink-soft); background:var(--surface-alt);
  border-radius:var(--radius-sm); padding:4px 9px; white-space:nowrap;}
.pcb-op b{color:var(--ink);}
.pcb-op em{font-style:normal; color:var(--green);}
.pcb-total{margin-left:auto; font-family:var(--font-disp); font-weight:700; font-size:19px; color:var(--ink);}
.pcb-total small{font-family:var(--font-body); font-weight:600; font-size:10.5px; color:var(--ink-faint); margin-left:4px;}
.pcb-encours{font-family:var(--font-mono); font-size:11px; color:var(--green);}
.pcb-st{font-family:var(--font-mono); font-size:9.5px; font-weight:600; letter-spacing:.03em; font-style:normal;
  border-radius:999px; padding:2px 8px; margin-left:6px; white-space:nowrap;}
.pcb-st.ok{background:var(--green-bg); color:var(--green);}
.pcb-st.pending{background:var(--amber-bg); color:var(--amber);}
.pcb-st.arrete{background:var(--surface-alt); color:var(--ink-faint);}
.route-wrap{flex:1 1 320px; min-width:260px;}
.route-track{position:relative; height:26px; background:var(--surface-alt); border:1px solid var(--border);
  border-radius:999px; overflow:hidden; display:flex; align-items:center;}
.route-fill{position:absolute; top:0; bottom:0; left:0; background:linear-gradient(90deg, var(--green-bg), var(--green)); opacity:.55;}
.route-mono,.route-pct,.route-cible{position:relative; font-family:var(--font-mono); font-size:10px; font-weight:600; padding:0 9px; white-space:nowrap;}
.route-mono{color:var(--ink-soft);}
.route-pct{color:var(--green); font-weight:700;}
.route-cible{margin-left:auto; color:var(--ink-faint);}
.fr-global{margin-bottom:14px;}
.fr-chiffres{display:flex; gap:8px 22px; flex-wrap:wrap; font-size:12.5px; color:var(--ink-soft); margin-bottom:9px;}
.fr-chiffres b{color:var(--ink);}
.fr-gain{color:var(--green); font-weight:600;}
.fr-row{display:flex; align-items:center; gap:12px; flex-wrap:wrap; padding:8px 2px; border-top:1px solid var(--border); font-size:12.5px;}
.fr-op{font-family:var(--font-mono); font-size:11px; font-weight:600; color:var(--blue-dark); flex:0 0 170px;}
.fr-prod{font-family:var(--font-mono); font-size:11px; color:var(--ink-faint); flex:0 0 110px;}
.fr-essai{flex:1 1 300px; color:var(--ink-soft);}
.fr-essai b{color:var(--ink);}
/* v4.47 — groupe d'outils simultanés : bloc ambre visible dans la vue d'ensemble."""
assert s.count(avant) == 1, "css"
s = s.replace(avant, apres, 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("4.49 code OK")
