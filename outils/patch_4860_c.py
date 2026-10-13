# -*- coding: utf-8 -*-
"""Patch v4.86.0 partie C : conteneur + bouton + porte + tests + version."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# 1. conteneur
rep('<div class="panel panel-large" id="cataloguePanel" hidden></div>',
    '<div class="panel panel-large" id="cataloguePanel" hidden></div>\n  <div class="panel panel-large" id="planPanel" hidden></div>')

# 2. bouton pied d'accueil
rep('''      <button class="primary small" id="pfCatalogue" title="La v\u00e9rit\u00e9 prix/article : un MABEC = un prix. Export/import CSV, propagation aux logements avec rapport">📚 Catalogue</button>''',
'''      <button class="primary small" id="pfCatalogue" title="La v\u00e9rit\u00e9 prix/article : un MABEC = un prix. Export/import CSV, propagation aux logements avec rapport">📚 Catalogue</button>
      <button class="primary small" id="pfPlan" title="Le pas-\u00e0-pas commercial : article par article, la cible SPK et le gain annuel \u2014 r\u00e9v\u00e9l\u00e9 ligne par ligne">\u2694\ufe0f Plan de conversion</button>''')

# 3. wiring
rep('''  const cCat = document.getElementById("pfCatalogue");
  if(cCat) cCat.addEventListener("click", ouvrirCatalogue);''',
'''  const cCat = document.getElementById("pfCatalogue");
  if(cCat) cCat.addEventListener("click", ouvrirCatalogue);
  const cPlan = document.getElementById("pfPlan");
  if(cPlan) cPlan.addEventListener("click", ouvrirPlan);''')

# 4. porte
rep('''  { porte:"📚 Catalogue (accueil)", fns:["ouvrirCatalogue", "renderCatalogue", "catalogueSeed", "catalogueAppliquer", "catalogueCSV", "catalogueDepuisCSV"] },''',
'''  { porte:"📚 Catalogue (accueil)", fns:["ouvrirCatalogue", "renderCatalogue", "catalogueSeed", "catalogueAppliquer", "catalogueCSV", "catalogueDepuisCSV"] },
  { porte:"\u2694\ufe0f Plan de conversion (accueil)", fns:["ouvrirPlan", "renderPlan", "planLignes", "planHTML", "planCSV"] },''')

# 5. version
s = s.replace('const TOOL_VERSION = "4.85.0";', 'const TOOL_VERSION = "4.86.0";', 1)

# 6. nouveautes
rep('''const NOUVEAUTES = [
  { version:"4.85.0", date:"13/10/2026", points:[''',
'''const NOUVEAUTES = [
  { version:"4.86.0", date:"14/10/2026", points:[
    "<b>\u2694\ufe0f Le Plan de conversion : le pas-\u00e0-pas commercial.</b> Chaque article actuel avec sa consommation en production, la <b>cible SPK \u00e9ditable</b> \u2014 les KY3500 se voient sugg\u00e9rer la m\u00eame g\u00e9om\u00e9trie en LKT640 \u2014 et le <b>gain annuel</b> calcul\u00e9 en direct. Chaque ligne porte son \u00e9tat (\u00e0 proposer / propos\u00e9e / en essai / gagn\u00e9e) : tu r\u00e9v\u00e8les au rythme que tu d\u00e9cides, le total ne compte que ce que tu as pos\u00e9. Export CSV pour la r\u00e9union."
  ]},
  { version:"4.85.0", date:"13/10/2026", points:[''')

# 7. tests : le plan — suggestion auto, gain, etat qui gate le total
rep('''        ok("catalogue : un prix illisible est signal\u00e9, pas invent\u00e9 (\u00a73.5)",
           catalogueDepuisCSV("MABEC;Prix EUR\\nIM02 137 021;nsp").erreurs.length > 0, true);''',
'''        ok("catalogue : un prix illisible est signal\u00e9, pas invent\u00e9 (\u00a73.5)",
           catalogueDepuisCSV("MABEC;Prix EUR\\nIM02 137 021;nsp").erreurs.length > 0, true);
      } finally { lignes = lAvC; catalogue = []; }
    }
    {
      /* v4.86 — LE PLAN DE CONVERSION : suggestion KY3500->LKT640 a 5 EUR,
         gain = pieces/an x (prix actuel - prix cible), et l'etat gate le total. */
      const lP = normalizeLigne({ id: "lPl", nom: "EMAG 1", references: [ normalizeReference({ id: "rPl", nom: "356x26", productionAnnuelle: 10000, ops: [
        normalizeOp({ id: "oPl", nom: "OP20", scenarios: [ normalizeScenario({ id: "scPl", name: "Prod", baseline: true, outils: [
          { id: "tP1", numero: "T521", logements: [
            { id: "gP1", nom: "D1", ref: "SNMX120716T02020 KY3500", codeArticle: "IM02 137 021", prix: 7.96, aretes: 8, charniere: 150 } ] } ] }) ] }) ] }) ] });
      const lAvP = lignes; lignes = [ lP ]; plan = [];
      try {
        const lignesPlan = planLignes();
        const l0 = lignesPlan[0];
        ok("plan : la cible KY3500 est auto-sugg\u00e9r\u00e9e en LKT640 \u00e0 5 \u20ac (d\u00e9cision Benjamin)",
           [l0.auto, l0.cibleIso, Number(l0.ciblePrix)], [true, "SNMX120716T02020 LKT640", 5]);
        const piecesAn = (7.96 / (8 * 150)) * 10000;
        ok("plan : le gain d'une ligne activ\u00e9e = plaquettes/an \u00d7 (prix actuel \u2212 prix cible)",
           [planLignes()[0].actif, planLignes()[0].gain], [false, null]);
        plan = [ normalizePlanEntry({ mabec: "IM02 137 021", isoCible: "SNMX120716T02020 LKT640", prixCible: 5, etat: "propos\u00e9e" }) ];
        const g1 = planLignes()[0];
        ok("plan : l'\u00e9tat pos\u00e9 active la ligne et son gain au centime pr\u00e8s",
           [g1.actif, Math.abs(g1.gain - piecesAn * (7.96 - 5)) < 1e-9], [true, true]);
        const tout = planLignes().reduce((a, l) => a + (l.actif && l.gain ? l.gain : 0), 0);
        ok("plan : le total de la promesse ne compte que les lignes \u00e9tat\u00e9es (le reste est du potentiel)",
           Math.abs(tout - piecesAn * 2.96) < 1e-9, true);
      } finally { lignes = lAvP; plan = []; }
    }''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("patch C applique : conteneur + bouton + porte + tests + 4.86.0")
