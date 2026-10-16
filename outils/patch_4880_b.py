# -*- coding: utf-8 -*-
"""Patch v4.88.0 partie B (réécrit) : UI du basculeur + tests + version."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# ── 1. la barre du basculeur dans planHTML ───────────────────────────────────
rep('''  return `
    <div class="simul-note">Le pas-à-pas commercial : chaque ligne est un article actuel, sa consommation en production, et la cible SPK — révélée quand TU décides de poser son état. Le total ne compte que les lignes étatées.</div>''',
'''  const modeReel = planSource === "reel";
  const etatConso = !modeReel
    ? "théorique — production ÷ (arêtes × DDV classeur)"
    : (consoReelle
        ? "réelle extrapolée — lue le " + consoReelle.lueLe + " (" + consoReelle.fichiers.join(", ") + ")"
        : "réelle — mais aucun classeur lu : lis un fichier ci-dessous");
  return `
    <div class="simul-note">Le pas-à-pas commercial : chaque ligne est un article actuel, sa consommation en production, et la cible SPK — révélée quand TU décides de poser son état. Le total ne compte que les lignes étatées.</div>
    <div class="simul-controles" style="flex-wrap:wrap;">
      <span style="font-weight:600;">Consommation :</span>
      <label style="cursor:pointer;"><input type="radio" name="consoSource" value="theo" ${!modeReel ? "checked" : ""}> théorique</label>
      <label style="cursor:pointer;"><input type="radio" name="consoSource" value="reel" ${modeReel ? "checked" : ""}> réelle extrapolée</label>
      <label class="ghost small" for="consoFichier" style="cursor:pointer;">📂 Lire un classeur de consommation…</label>
      <input type="file" id="consoFichier" accept=".xlsm,.xlsx" multiple hidden>
      <span id="consoEtat" style="font-size:13px; color:#1b5ea6;">${etatConso}</span>
    </div>
    ${modeReel && consoReelle ? `<p class="panel-hint">⚠ Consommation réelle = une semaine de tes classeurs × 52 (régime supposé constant). Les articles sans consommation lue perdent leur gain — jamais complétés en silence (§3.5).</p>` : ""}''')

# ── 2. la cellule consommation de chaque ligne, selon la source ──────────────
rep('''          <td class="mono">${fmtEuroCourt(Math.round(l.coutAnnuel))}/an<br><span style="color:#888;">${fmt(l.piecesAn, 0)} plq/an</span></td>''',
'''          <td class="mono">${l.sourceConso === "reelle"
            ? `${fmt(l.piecesAn, 0)} plq/an <span style="color:#1b5ea6;">(réel)</span><br><span style="color:#888;">${fmtEuroCourt(Math.round(l.piecesAn * l.prixA))} estimé/an</span>`
            : (l.sourceConso === "sans"
                ? `<span style="color:#b45309;">pas de conso réelle lue</span>`
                : `${fmtEuroCourt(Math.round(l.coutAnnuel))}/an<br><span style="color:#888;">${fmt(l.piecesAn, 0)} plq/an</span>`)}</td>''')

# ── 3. le wiring dans renderPlan ─────────────────────────────────────────────
rep('''  const mx = document.getElementById("planMaxiBtn");
  if(mx) mx.addEventListener("click", () => basculerMaxi("planPanel", mx));''',
'''  const mx = document.getElementById("planMaxiBtn");
  if(mx) mx.addEventListener("click", () => basculerMaxi("planPanel", mx));
  wrap.querySelectorAll('input[name="consoSource"]').forEach(r => r.addEventListener("change", () => {
    planSource = r.value; renderPlan();
  }));
  const fich = document.getElementById("consoFichier");
  if(fich) fich.addEventListener("change", async () => {
    const fichiers = Array.from(fich.files || []);
    if(!fichiers.length) return;
    const parArticle = {}; const noms = [];
    for(const f of fichiers){
      try{
        const lu = await consoLireClasseur(f);
        noms.push(lu.fichier);
        for(const [art, v] of Object.entries(lu.parArticle)){
          const e = parArticle[art] = parArticle[art] || { qtySemaine: 0, lignes: new Set() };
          e.qtySemaine += v.qtySemaine;
          v.lignes.forEach(x => e.lignes.add(x));
        }
      }catch(err){ dialogueAlerte("Lecture impossible : " + err.message, "Classeur de consommation"); }
    }
    consoReelle = { lueLe: new Date().toLocaleDateString("fr-FR"), fichiers: noms, parArticle };
    planSource = "reel";
    renderPlan();
  });''')

# ── 4. l'export CSV porte le mode ────────────────────────────────────────────
rep('''  const L = ["sep=;", "Plan de conversion SPK - " + new Date().toLocaleDateString("fr-FR"), "",
    "Article actuel (MABEC);Libelles ISO;Prix actuel (EUR);Consommation (EUR/an);Plaquettes/an;Cible SPK;Prix cible (EUR);Etat;Gain (EUR/an)"];
  lignes.forEach(l => L.push([l.mabec, l.isos.join(" | "), num(l.prixA), num(l.coutAnnuel),
    num(l.piecesAn), l.cibleIso, num(l.ciblePrix), l.etat, l.gain != null ? num(l.gain) : ""].map(cell).join(";")));''',
'''  const L = ["sep=;", "Plan de conversion SPK - " + new Date().toLocaleDateString("fr-FR"), "",
    "Consommation;" + (planSource === "reel" ? "REELLE extrapolee (classeur x 52)" : "theorique (DDV classeur)"), "",
    "Article actuel (MABEC);Libelles ISO;Prix actuel (EUR);Consommation (EUR/an);Plaquettes/an;Cible SPK;Prix cible (EUR);Etat;Gain (EUR/an)"];
  lignes.forEach(l => L.push([l.mabec, l.isos.join(" | "), num(l.prixA),
    l.sourceConso === "reelle" ? num(l.piecesAn * l.prixA) : num(l.coutAnnuel),
    num(l.piecesAn), l.cibleIso, num(l.ciblePrix), l.etat, l.gain != null ? num(l.gain) : ""].map(cell).join(";")));''')

# ── 5. tests : le parseur + le basculeur ─────────────────────────────────────
rep('''        ok("plan : le total de la promesse ne compte que les lignes étatées (le reste est du potentiel)",
           Math.abs(tout - plqAn * 2.96) < 1e-9, true);''',
'''        ok("plan : le total de la promesse ne compte que les lignes étatées (le reste est du potentiel)",
           Math.abs(tout - plqAn * 2.96) < 1e-9, true);
      } finally { lignes = lAvP; plan = []; }
    }
    {
      /* v4.88 — LE BASCULEUR : le parseur lit les feuilles « Pareto conso »
         (sections EMAG/PCI/HESSAPP), refuse un pareto de COUT, et le gain en
         mode réel vient de la consommation réelle × 52 — un article sans
         donnée réelle perd son gain (jamais complété en silence). */
      const cells = {
        "A1": "Étiquettes de lignes", "B1": "Somme de Qté",
        "A2": "PCI 4", "B2": 249,
        "A3": "IM02 137 021", "B3": 45,
        "A4": "Z000 513 527", "B4": 65,
        "A5": "PCI 5", "B5": 198,
        "A6": "IM02 137 021", "B6": 40,
        "A7": "Total général", "B7": 447
      };
      const lu = consoDepuisFeuille("pareto conso plaquette", cells);
      ok("basculeur : le parseur lit les sections et cumule un article vu sur deux lignes",
         [lu["IM02 137 021"].qtySemaine, lu["IM02 137 021"].lignes.size, lu["Z000 513 527"].qtySemaine],
         [85, 2, 65]);
      ok("basculeur : un pareto de COUT n'est jamais pris pour des quantités",
         consoDepuisFeuille("Pareto coût plaquette", { "A1": "Étiquettes", "B1": "Somme de Cout", "A2": "IM02 137 021", "B2": 358 }), null);
      const lR = normalizeLigne({ id: "lB", nom: "EMAG 1", references: [ normalizeReference({ id: "rB", nom: "356x26", productionAnnuelle: 10000, ops: [
        normalizeOp({ id: "oB", nom: "OP20", scenarios: [ normalizeScenario({ id: "scB", name: "Prod", baseline: true, outils: [
          { id: "tB1", numero: "T521", logements: [
            { id: "gB1", nom: "D1", ref: "SNMX120716T02020 KY3500", codeArticle: "IM02 137 021", prix: 7.96, aretes: 8, charniere: 150 },
            { id: "gB2", nom: "D2", ref: "CNGX 120716 S02020 CBN387", codeArticle: "IM02 209 560", prix: 38, aretes: 4, charniere: 600 } ] } ] }) ] }) ] }) ] });
      const lAvB = lignes; lignes = [ lR ]; plan = [
        normalizePlanEntry({ mabec: "IM02 137 021", prixCible: 5, etat: "proposée" }),
        normalizePlanEntry({ mabec: "IM02 209 560", prixCible: 5, etat: "proposée" }) ];
      try {
        consoReelle = { lueLe: "13/10/2026", fichiers: ["test"], parArticle: {
          "IM02 137 021": { qtySemaine: 85, lignes: ["PCI 4", "PCI 5"] } } };
        planSource = "reel";
        const lR1 = planLignes()[0];
        const sansData = planLignes()[1];
        ok("basculeur : en mode RÉEL, la consommation de l'article lu = semaine × 52",
           [lR1.sourceConso, Math.abs(lR1.piecesAn - 85 * 52) < 1e-9,
            Math.abs(lR1.gain - 85 * 52 * (7.96 - 5)) < 1e-9], ["reelle", true, true]);
        ok("basculeur : un article SANS consommation lue perd son gain (déclaré, jamais complété)",
           [sansData.sourceConso, sansData.gain], ["sans", null]);
        planSource = "theo";
        ok("basculeur : retour au théorique — le calcul revient à prod ÷ (arêtes × DDV)",
           Math.abs(planLignes()[0].piecesAn - 10000 / (8 * 150)) < 1e-9, true);
      } finally { lignes = lAvB; plan = []; consoReelle = null; planSource = "theo"; }
    }''')

# ── 6. version ────────────────────────────────────────────────────────────────
s = s.replace('const TOOL_VERSION = "4.87.0";', 'const TOOL_VERSION = "4.88.0";', 1)

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("patch B réécrit et appliqué : UI basculeur + tests + 4.88.0")
