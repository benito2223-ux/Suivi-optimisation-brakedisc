# -*- coding: utf-8 -*-
"""Patch v4.86.0 partie B : fonctions du Plan de conversion + panneau + porte + tests."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# ── 1. fonctions + panneau, poses avant renderSimul ─────────────────────────
rep("function renderSimul(){",
'''/* ═══ v4.86 — LE PLAN DE CONVERSION : la vitrine commerciale ════════════════
   La demande de Benjamin : montrer a Matis, article par article, ce que vaut
   le passage sur les plaquettes SPK — progressivement, ligne par ligne, au
   bon moment. Regles : la consommation est celle des scenarios EN PRODUCTION
   (le meme calcul que partout) ; la cible est EDITABLE (auto-suggeree pour
   les KY3500 : meme geometrie en LKT640 a 5 EUR, decision Benjamin) ; l'etat
   de chaque ligne appartient a Benjamin (a proposer / proposee / en essai /
   gagnee) ; le TOTAL de la promesse ne compte que les lignes ou l'etat est
   pose. Les DDV d'essai n'entrent qu'apres validation operateur (decisions
   du 13/10). Aucun K, aucun P dans cet ecran. */
const PLAN_ETATS = ["\u00e0 proposer", "propos\u00e9e", "en essai", "gagn\u00e9e"];

function planLignes(){
  const d = plaquettesCommunes();
  const parMabec = {};
  plan.forEach(p => { parMabec[p.mabec] = p; });
  return d.groupes.map(g => {
    const art = catalogue.find(a => a.mabec === g.mabec && a.prix !== "" && a.prix > 0);
    const prixA = art ? art.prix : (g.usages[0] ? g.usages[0].prix : 0);
    const piecesAn = prixA > 0 ? g.coutAnnuel / prixA : 0;
    const isoKY = g.usages.map(u => u.iso).find(i => /KY3500/i.test(i || ""));
    const sugg = isoKY ? { iso: String(isoKY).replace(/KY3500/gi, "LKT640"), prix: 5 } : null;
    const p = parMabec[g.mabec] || {};
    const ciblePrix = (p.prixCible !== "" && p.prixCible != null) ? Number(p.prixCible)
                      : (sugg ? sugg.prix : "");
    const cibleIso = p.isoCible || (sugg ? sugg.iso : "");
    const actif = !!p.etat;
    const gain = (actif && ciblePrix !== "" && ciblePrix !== null && prixA > 0)
      ? piecesAn * (prixA - Number(ciblePrix)) : null;
    return { mabec: g.mabec, isos: [...g.isos], prixA, coutAnnuel: g.coutAnnuel,
             piecesAn, cibleIso, ciblePrix, etat: p.etat || "", actif, gain, auto: !!sugg };
  });
}

function planHTML(){
  const lignes = planLignes();
  if(!lignes.length) return `<p class="panel-hint">Aucun article de production chiffr\u00e9 : le plan se nourrit des m\u00eames donn\u00e9es que le simulateur (sc\u00e9narios en production, prix + volume).</p>`;
  const total = lignes.reduce((a, l) => a + (l.actif && l.gain ? l.gain : 0), 0);
  const actives = lignes.filter(l => l.actif).length;
  return `
    <div class="simul-note">Le pas-\u00e0-pas commercial : chaque ligne est un article actuel, sa consommation en production, et la cible SPK \u2014 r\u00e9v\u00e9l\u00e9e quand TU d\u00e9cides de poser son \u00e9tat. Le total ne compte que les lignes \u00e9tat\u00e9es.</div>
    <table class="simul-table">
      <thead><tr><th>Article actuel</th><th>Libell\u00e9s ISO</th><th>Prix actuel</th><th>Consommation</th><th>Cible SPK</th><th>Prix cible</th><th>\u00c9tat</th><th>Gain / an</th></tr></thead>
      <tbody>
      ${lignes.map((l, i) => {
        const isoCible = l.cibleIso || l.isos[0] || "";
        return `<tr>
          <td class="mono">${escapeAttr(l.mabec)}</td>
          <td style="font-size:11.5px; color:#888;">${l.isos.map(x => escapeAttr(x)).join("<br>")}</td>
          <td class="mono">${fmt(l.prixA, 2)} \u20ac</td>
          <td class="mono">${fmtEuroCourt(Math.round(l.coutAnnuel))}/an<br><span style="color:#888;">${fmt(l.piecesAn, 0)} plq/an</span></td>
          <td><input class="cell" style="width:190px; font-size:12px;" data-plan="${l.mabec}" data-field="isoCible" value="${escapeAttr(l.cibleIso)}" placeholder="plaquette SPK${l.auto ? " (LKT640 sugg\u00e9r\u00e9e)" : ""}"></td>
          <td><input class="cell" style="width:74px; font-family:var(--font-mono);" type="number" step="0.01" data-plan="${l.mabec}" data-field="prixCible" value="${l.ciblePrix === "" ? "" : l.ciblePrix}" placeholder="5"></td>
          <td><select class="cell small" data-plan="${l.mabec}" data-field="etat">
            <option value="">—</option>
            ${PLAN_ETATS.map(e => `<option value="${e}" ${l.etat === e ? "selected" : ""}>${e}</option>`).join("")}
          </select></td>
          <td class="mono" style="${l.gain ? "color:#1a7a3f; font-weight:600;" : "color:#888;"}">${l.gain != null ? "\u2212 " + fmtEuroCourt(Math.round(l.gain)) : "potentiel"}</td>
        </tr>`;
      }).join("")}
      </tbody>
    </table>
    <div class="simul-resultat">${actives
      ? `Promesse pos\u00e9e : <b>${actives} article(s)</b> en conversion \u2014 \u00e9conomie simul\u00e9e <b>\u2212 ${fmtEuroCourt(Math.round(total))} / an</b>.`
      : `Pose un \u00e9tat sur une ligne (m\u00eame \u00ab \u00e0 proposer \u00bb) pour l\u2019ajouter \u00e0 la promesse \u2014 le pas-\u00e0-pas t\u2019appartient.`}</div>
    <div class="simul-actions" style="margin-top:12px;">
      <button class="ghost small" id="planExporter">\u2935 Exporter le plan (CSV)</button>
    </div>`;
}

function renderPlan(){
  const wrap = document.getElementById("planPanel");
  if(!wrap) return;
  wrap.innerHTML = `<h3>\u2694\ufe0f Plan de conversion \u2014 vers les plaquettes SPK</h3>` + planHTML();
  wrap.querySelectorAll("[data-plan]").forEach(inp => inp.addEventListener("change", () => {
    const mabec = inp.getAttribute("data-plan"), field = inp.getAttribute("data-field");
    let e = plan.find(x => x.mabec === mabec);
    if(!e){ e = normalizePlanEntry({ mabec }); plan.push(e); }
    e[field] = field === "prixCible" ? (inp.value === "" ? "" : Number(inp.value)) : inp.value;
    saveData(); renderPlan();
  }));
  const ex = document.getElementById("planExporter");
  if(ex) ex.addEventListener("click", planExporter);
}
function ouvrirPlan(){
  fermerPanneaux();
  ouvrirPanneau("planPanel");
  renderPlan();
}

function planCSV(){
  const num = v => String(v === "" || v == null ? "" : Math.round(v * 10000) / 10000).replace(".", ",");
  const cell = v => /[";\r\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v);
  const lignes = planLignes();
  const L = ["sep=;", "Plan de conversion SPK - " + new Date().toLocaleDateString("fr-FR"), "",
    "Article actuel (MABEC);Libelles ISO;Prix actuel (EUR);Consommation (EUR/an);Plaquettes/an;Cible SPK;Prix cible (EUR);Etat;Gain (EUR/an)"];
  lignes.forEach(l => L.push([l.mabec, l.isos.join(" | "), num(l.prixA), num(l.coutAnnuel),
    num(l.piecesAn), l.cibleIso, num(l.ciblePrix), l.etat, l.gain != null ? num(l.gain) : ""].map(cell).join(";")));
  const total = lignes.reduce((a, l) => a + (l.actif && l.gain ? l.gain : 0), 0);
  L.push(["TOTAL (etat pose)", "", "", "", "", "", "", "", num(total)].map(cell).join(";"));
  return "\uFEFF" + L.join("\r\n");
}
function planExporter(){
  const blob = new Blob([planCSV()], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "Plan_conversion_SPK.csv";
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

function renderSimul(){''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print('patch B applique : fonctions du plan inserees')
