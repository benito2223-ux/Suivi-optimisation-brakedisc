# -*- coding: utf-8 -*-
"""Patch v4.83.1 : libelle ISO + budget annuel par reference dans le simulateur."""
import json

s = open('bilan_economique.html', encoding='utf-8').read()

# 1. plaquettesCommunes : ISO par groupe + budget par reference (cle = l'ID)
av = '''function plaquettesCommunes(){
  const groupes = {};
  let totalAnnuel = 0, refsSansVolume = 0;
  const sansVolume = new Set();
  lignes.forEach(l => (l.references || []).forEach(r => {
    const prod = parseFloat(r.productionAnnuelle);
    const aVolume = !isNaN(prod) && prod > 0;
    if(!aVolume){ refsSansVolume++; sansVolume.add((l.nom || "?") + " · " + (r.nom || "?")); }
    (r.ops || []).forEach(o => (o.scenarios || []).forEach(sc => {
      if(!sc.baseline) return;
      (sc.outils || []).forEach(ou => (ou.logements || []).forEach(g => {
        const mabec = String(g.codeArticle || g.mabec || "").trim().toUpperCase();
        const prix = parseFloat(g.prix), aretes = parseFloat(g.aretes), ddv = parseFloat(g.charniere);
        if(!mabec || isNaN(prix) || prix <= 0 || !isFinite(aretes) || aretes <= 0 || !isFinite(ddv) || ddv <= 0) return;
        const coutPiece = prix / (aretes * ddv);
        const coutAnnuel = aVolume ? coutPiece * prod : 0;
        totalAnnuel += coutAnnuel;
        const G = groupes[mabec] = groupes[mabec] || { mabec, usages: [], coutAnnuel: 0 };
        G.usages.push({ ligne: l.nom, ref: r.nom, op: o.opCode || o.nom || "?", outil: ou.numero || "?",
                        prix, aretes, ddv, coutPiece, coutAnnuel, aVolume });
        G.coutAnnuel += coutAnnuel;
      }));
    }));
  }));
  return { groupes: Object.values(groupes).sort((a, b) => b.coutAnnuel - a.coutAnnuel),
           totalAnnuel, refsSansVolume, sansVolume: Array.from(sansVolume) };
}'''
ap = '''function plaquettesCommunes(){
  const groupes = {};
  const parRef = {};   /* v4.83.1 — cle = l'ID de la ref : « 268x12 » existe sur PCI 4 ET PCI 5, le nom ne suffit pas */
  let totalAnnuel = 0, refsSansVolume = 0;
  const sansVolume = new Set();
  lignes.forEach(l => (l.references || []).forEach(r => {
    const prod = parseFloat(r.productionAnnuelle);
    const aVolume = !isNaN(prod) && prod > 0;
    if(!aVolume){ refsSansVolume++; sansVolume.add((l.nom || "?") + " · " + (r.nom || "?")); }
    const PR = parRef[r.id] = parRef[r.id] || { ligne: l.nom, ref: r.nom, prod: aVolume ? prod : 0, coutAnnuel: 0 };
    (r.ops || []).forEach(o => (o.scenarios || []).forEach(sc => {
      if(!sc.baseline) return;
      (sc.outils || []).forEach(ou => (ou.logements || []).forEach(g => {
        const mabec = String(g.codeArticle || g.mabec || "").trim().toUpperCase();
        const prix = parseFloat(g.prix), aretes = parseFloat(g.aretes), ddv = parseFloat(g.charniere);
        if(!mabec || isNaN(prix) || prix <= 0 || !isFinite(aretes) || aretes <= 0 || !isFinite(ddv) || ddv <= 0) return;
        const coutPiece = prix / (aretes * ddv);
        const coutAnnuel = aVolume ? coutPiece * prod : 0;
        totalAnnuel += coutAnnuel;
        PR.coutAnnuel += coutAnnuel;
        const G = groupes[mabec] = groupes[mabec] || { mabec, usages: [], isos: new Set(), coutAnnuel: 0 };
        const iso = String(g.ref || "").trim();
        if(iso) G.isos.add(iso);
        G.usages.push({ ligne: l.nom, ref: r.nom, op: o.opCode || o.nom || "?", outil: ou.numero || "?",
                        iso, prix, aretes, ddv, coutPiece, coutAnnuel, aVolume });
        G.coutAnnuel += coutAnnuel;
      }));
    }));
  }));
  return { groupes: Object.values(groupes).sort((a, b) => b.coutAnnuel - a.coutAnnuel),
           parReference: Object.values(parRef).filter(x => x.coutAnnuel > 0).sort((a, b) => b.coutAnnuel - a.coutAnnuel),
           totalAnnuel, refsSansVolume, sansVolume: Array.from(sansVolume) };
}'''
assert av in s, "ancre 1"
s = s.replace(av, ap, 1)

# 2. le rendu : ISO sous le MABEC
av2 = '''          <td class="mono">${escapeAttr(g.mabec)}</td>
          <td>${g.usages.length} · ${escapeAttr([...new Set(g.usages.map(u => u.ligne))].join(", "))}</td>'''
ap2 = '''          <td class="mono">${escapeAttr(g.mabec)}${g.isos.size ? `<br><span style="font-size:11.5px; color:#888;">${[...g.isos].map(x => escapeAttr(x)).join("<br>")}</span>` : ""}</td>
          <td>${g.usages.length} · ${escapeAttr([...new Set(g.usages.map(u => u.ligne))].join(", "))}</td>'''
assert av2 in s, "ancre 2"
s = s.replace(av2, ap2, 1)

# 3. la table budget par reference
av3 = '''    ${d.refsSansVolume ? `<p class="panel-hint">\u26a0 ${d.refsSansVolume} r\u00e9f\u00e9rence(s) sans volume annuel \u2014 hors calcul : ${d.sansVolume.map(x => escapeAttr(x)).join(" \u00b7 ")}</p>` : ""}'''
ap3 = '''    ${d.parReference.length ? `
    <h4 style="margin:22px 0 8px; font-size:14px;">Budget outillage annuel par r\u00e9f\u00e9rence</h4>
    <table class="simul-table">
      <thead><tr><th>Ligne</th><th>R\u00e9f\u00e9rence</th><th>Volume annuel</th><th>Co\u00fbt / an</th><th>% du budget</th></tr></thead>
      <tbody>${d.parReference.map(x => `<tr>
        <td>${escapeAttr(x.ligne)}</td>
        <td>${escapeAttr(x.ref)}</td>
        <td class="mono">${fmt(x.prod, 0)}</td>
        <td class="mono">${fmtEuroCourt(Math.round(x.coutAnnuel))}</td>
        <td class="mono">${d.totalAnnuel ? fmt(x.coutAnnuel / d.totalAnnuel * 100, 1) : "\u2014"} %</td>
      </tr>`).join("")}</tbody>
    </table>` : ""}
    ${d.refsSansVolume ? `<p class="panel-hint">\u26a0 ${d.refsSansVolume} r\u00e9f\u00e9rence(s) sans volume annuel \u2014 hors calcul : ${d.sansVolume.map(x => escapeAttr(x)).join(" \u00b7 ")}</p>` : ""}'''
assert av3 in s, "ancre 3"
s = s.replace(av3, ap3, 1)

# 4. tests
av4 = '''        ok("simulateur : le deuxi\u00e8me MABEC p\u00e8se de son propre co\u00fbt (un seul usage, un seul volume)",
           Math.abs(d.groupes.find(x => x.mabec === "Z000 513 527").coutAnnuel - (9.56 / (8 * 50)) * 10000) < 1e-9, true);'''
ap4 = av4 + '''
        ok("simulateur : le groupe porte les libell\u00e9s ISO de la plaquette, pas le MABEC seul",
           [...g.isos].sort().join("|"), ["ISO gS1", "ISO gS3"].sort().join("|"));
        ok("simulateur : budget annuel par r\u00e9f\u00e9rence \u2014 chaque r\u00e9f\u00e9rence p\u00e8se le volume de SA production",
           [d.parReference.length,
            Math.abs(d.parReference[0].coutAnnuel - ((7.96 / (8 * 150)) * 10000 + (9.56 / (8 * 50)) * 10000)) < 1e-9,
            Math.abs(d.parReference[1].coutAnnuel - (7.96 / (8 * 150)) * 5000) < 1e-9],
           [2, true, true]);
        /* la cl\u00e9 de regroupement par r\u00e9f\u00e9rence est l'ID : \u00ab 268x12 \u00bb existe sur
           PCI 4 ET PCI 5 \u2014 regrouper par nom fusionnerait deux machines. */
        const lHom = normalizeLigne({ id: "lS4", nom: "PCI 4", references: [ normalizeReference({ id: "rS4", nom: "330x14", productionAnnuelle: 2000, ops: [
          normalizeOp({ id: "oS4", nom: "OP10", scenarios: [ normalizeScenario({ id: "scS4", name: "Prod", baseline: true, outils: [
            { id: "tS4", numero: "T529", logements: [ mkLog("gS5", "IM02 137 021", 7.96, 8, 150) ] } ] }) ] }) ] }) ] });
        lignes.push(lHom);
        const d2 = plaquettesCommunes();
        lignes.pop();
        ok("simulateur : deux r\u00e9f\u00e9rences de M\u00caME NOM (deux lignes) restent deux lignes du budget \u2014 la cl\u00e9 est l'ID",
           d2.parReference.length, 3);'''
assert av4 in s, "ancre 4"
s = s.replace(av4, ap4, 1)

s2 = s.replace('const TOOL_VERSION = "4.83.0";', 'const TOOL_VERSION = "4.83.1";', 1)
ancien = '''const NOUVEAUTES = [
  { version:"4.83.0", date:"13/10/2026", points:['''
nouveau = '''const NOUVEAUTES = [
  { version:"4.83.1", date:"13/10/2026", points:[
    "<b>Le simulateur parle le m\u00e9tier.</b> Chaque article affiche d\u00e9sormais le <b>libell\u00e9 de la plaquette</b> (la d\u00e9signation ISO) en plus du code MABEC \u2014 et sous le tableau, le <b>budget outillage annuel par r\u00e9f\u00e9rence</b> : combien co\u00fbte chaque disque en plaquettes par an, en \u20ac et en % du budget."
  ]},
  { version:"4.83.0", date:"13/10/2026", points:['''
assert ancien in s2, "ancre 5"
s2 = s2.replace(ancien, nouveau, 1)

open('bilan_economique.html', 'w', encoding='utf-8', newline='\n').write(s2)
print("patch v4.83.1 applique : ISO + budget par reference + tests + version")
