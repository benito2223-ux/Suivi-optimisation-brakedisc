# -*- coding: utf-8 -*-
"""v4.49.4 — coût pièce complet : la prod (★) d'abord, excel en repli, OPs non chiffrables visibles."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# 1. pieceCPPComplet : prod = ★ puis excel ; les OPs sans coût restent listées
avant = """  const ops = [];
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
  if(!connues.length) return null;"""
apres = """  const ops = [];
  ref.ops.forEach(op => {
    ops.push(dansContexteOp(op, () => {
      /* v4.49.4 — le coût de prod d'une OP, c'est D'ABORD la prod réelle (★), l'excel en
         repli : après le merge OP40 (DWG ★ qui remplace l'excel), le bandean ne comptait
         plus l'OP40. Et une OP sans scénario chiffrable (OP20 de Matis, valeurs vides)
         reste listée comme « non chiffrée » au lieu de disparaître — l'écart doit se voir. */
      const excel = (op.scenarios||[]).find(x => /base excel/i.test(x.name||""));
      const star = (op.scenarios||[]).find(x => x.baseline);
      const prodSc = star || excel || null;
      const tBase = prodSc ? coutsDetail(prodSc).total : null;
      let meilleur = null;
      (op.scenarios||[]).forEach(sc => {
        if(prodSc && sc.id === prodSc.id) return;
        const t = coutsDetail(sc).total;
        if(t === null) return;
        if(!meilleur || t < meilleur.cout) meilleur = { sc, cout: t };
      });
      return { op, prodSc, tBase, meilleur };
    }));
  });
  const connues = ops.filter(o => o.tBase !== null && o.tBase !== undefined);
  if(!connues.length) return null;"""
assert s.count(avant) == 1, "pieceCPPComplet"
s = s.replace(avant, apres)

# 2. retour : garder aussi les non chiffrées pour l'affichage
avant = """  let chemin = null;
  if(cible !== null && prod > cible && prod > 0) chemin = Math.max(0, Math.min(100, ((prod - enCours) / (prod - cible)) * 100));
  return { ref, ops: connues, prod, enCours, cible, chemin };"""
apres = """  let chemin = null;
  if(cible !== null && prod > cible && prod > 0) chemin = Math.max(0, Math.min(100, ((prod - enCours) / (prod - cible)) * 100));
  return { ref, ops: connues, nonChiffrees: ops.filter(o => o.tBase === null || o.tBase === undefined), prod, enCours, cible, chemin };"""
assert s.count(avant) == 1, "retour"
s = s.replace(avant, apres)

# 3. bandeau : puce « non chiffrée » pour les OPs sans coût
avant = """  const chips = p.ops.map(o => {
    const st = statutOP(o);
    const delta = o.meilleur && o.meilleur.cout < o.tBase ? ` <em>· ${escapeAttr(String(o.meilleur.sc.name).slice(0,26))} −${fmt(o.tBase - o.meilleur.cout,3)} €</em>` : "";
    return `<span class="pcb-op">${escapeAttr(String(o.op.nom||"OP").trim())} <b>${fmt(o.tBase,3)} €</b>${delta} <i class="pcb-st ${st.cls}">${st.txt}</i></span>`;
  }).join("");"""
apres = """  const chips = p.ops.map(o => {
    const st = statutOP(o);
    const delta = o.meilleur && o.meilleur.cout < o.tBase ? ` <em>· ${escapeAttr(String(o.meilleur.sc.name).slice(0,26))} −${fmt(o.tBase - o.meilleur.cout,3)} €</em>` : "";
    return `<span class="pcb-op">${escapeAttr(String(o.op.nom||"OP").trim())} <b>${fmt(o.tBase,3)} €</b>${delta} <i class="pcb-st ${st.cls}">${st.txt}</i></span>`;
  }).join("");
  const chipsVides = (p.nonChiffrees || []).map(o =>
    `<span class="pcb-op" title="Aucun scénario de prod chiffrable sur cette OP (outils sans prix ou charnière) — complétez la prod pour qu'elle entre dans le coût pièce.">${escapeAttr(String(o.op.nom||"OP").trim())} <b>non chiffrée</b> <i class="pcb-st pending">à compléter</i></span>`).join("");"""
assert s.count(avant) == 1, "chips"
s = s.replace(avant, apres)

avant = """    <div class="pcb-ops">${chips}</div>"""
apres = """    <div class="pcb-ops">${chips}${chipsVides}</div>"""
assert s.count(avant) == 1, "pcb-ops"
s = s.replace(avant, apres)

# 4. feuille de route : lignes pour les non chiffrées
avant = """  const rows = p.ops.map(o => {
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
  }).join("");"""
apres = """  const rows = p.ops.map(o => {
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
  }).join("") + (p.nonChiffrees || []).map(o =>
    `<div class="fr-row">
      <span class="fr-op">${escapeAttr(String(o.op.nom||"OP").trim())}</span>
      <span class="fr-prod">prod — €</span>
      <span class="fr-essai">non chiffrée : aucun scénario de prod chiffrable (outils sans prix ou charnière) — complétez la prod</span>
      <span class="pcb-st pending">à compléter</span>
    </div>`).join("");"""
assert s.count(avant) == 1, "rows"
s = s.replace(avant, apres)

# 5. version + NOUVEAUTES (points:[ propre, sans guillemet parasite)
s = s.replace('const TOOL_VERSION = "4.49.3";', 'const TOOL_VERSION = "4.49.4";')
avant = 'const NOUVEAUTES = [\n  { version:"4.49.3", date:"29/09/2026", points:['
apres = '''const NOUVEAUTES = [
  { version:"4.49.4", date:"29/09/2026", points:[
    "<b>Corrigé : le coût pièce complet compte maintenant toutes les OPs qui ont une prod.</b> Le coût de prod d'une OP, c'est d'abord la prod réelle (★), l'excel en repli — après le merge OP40 (DWG ★ remplaçant l'excel), l'OP40 avait disparu du décompte. Et une OP sans scénario chiffrable s'affiche désormais « non chiffrée — à compléter » au lieu de disparaître silencieusement (l'OP20 de la 356x26 attend ses valeurs)."
  ]},
  { version:"4.49.3", date:"29/09/2026", points:['''
assert s.count(avant) == 1, "NOUVEAUTES"
s = s.replace(avant, apres)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("4.49.4 OK")
