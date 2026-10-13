# -*- coding: utf-8 -*-
"""Patch v4.86.0 : LE PLAN DE CONVERSION — la vitrine commerciale.

Benjamin : toute KY3500 1207 (SNMX/CNMX/SNGX/CNGX) = LKT640 a 5 EUR.
Step by step : chaque ligne a un etat (a proposer / proposee / en essai /
gagnee) — le total ne compte que les lignes ACTEES par Benjamin.
Persistant dans le suivi (payload, loadAll, migration, import).
"""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# ── 1. globale + normalizer, a cote du catalogue ────────────────────────────
rep('''function normalizeArticleCat(a){''',
'''/* v4.86 — LE PLAN DE CONVERSION : une ligne par article a basculer vers SPK.
   Etat tenu par Benjamin, pas par l'outil : a proposer / proposee / en essai /
   gagnee. Le total de la promesse ne compte que les lignes ou l'etat est pose. */
let plan = [];

function normalizePlanEntry(p){
  return Object.assign({ mabec: "", isoCible: "", prixCible: "", etat: "" }, p,
    { mabec: String((p && p.mabec) || "").trim().toUpperCase(),
      isoCible: String((p && p.isoCible) || "").trim(),
      prixCible: (p && p.prixCible) !== "" && p && p.prixCible != null ? Number(p.prixCible) : "",
      etat: String((p && p.etat) || "") });
}

function normalizeArticleCat(a){''')

# ── 2. payload ───────────────────────────────────────────────────────────────
rep("activeScenarioId: activeId, livraisons, catalogue });",
    "activeScenarioId: activeId, livraisons, catalogue, plan });")

# ── 3. migrerArbre ───────────────────────────────────────────────────────────
rep("catalogue: Array.isArray(source.catalogue) ? source.catalogue.map(normalizeArticleCat) : [],",
    """catalogue: Array.isArray(source.catalogue) ? source.catalogue.map(normalizeArticleCat) : [],
           plan: Array.isArray(source.plan) ? source.plan.map(normalizePlanEntry) : [],""")

# ── 4. loadAll ───────────────────────────────────────────────────────────────
rep("        catalogue = (parsed.catalogue || []).map(normalizeArticleCat);",
"""        catalogue = (parsed.catalogue || []).map(normalizeArticleCat);
        plan = (parsed.plan || []).map(normalizePlanEntry);""")

# ── 5. preparerImportDepuis ──────────────────────────────────────────────────
rep("catalogue: migreImport ? (migreImport.catalogue || []) : [],",
    """catalogue: migreImport ? (migreImport.catalogue || []) : [],
           plan: migreImport ? (migreImport.plan || []).map(normalizePlanEntry) : [],""")

# ── 6. appliquerImport : fusion (entrant gagne par mabec) ────────────────────
rep('''      importEnAttente.catalogue.forEach(a => { parMabec[a.mabec] = a; });
      catalogue = Object.values(parMabec).map(normalizeArticleCat);
    }''',
'''      importEnAttente.catalogue.forEach(a => { parMabec[a.mabec] = a; });
      catalogue = Object.values(parMabec).map(normalizeArticleCat);
    }
    if(Array.isArray(importEnAttente.plan)){
      const parMabecP = {};
      plan.forEach(p => { parMabecP[p.mabec] = p; });
      importEnAttente.plan.forEach(p => { parMabecP[p.mabec] = p; });
      plan = Object.values(parMabecP).map(normalizePlanEntry);
    }''')

# ── 7. appliquerImport : remplace ────────────────────────────────────────────
rep("    catalogue = (parsed.catalogue || []).map(normalizeArticleCat);",
"""    catalogue = (parsed.catalogue || []).map(normalizeArticleCat);
    plan = (parsed.plan || []).map(normalizePlanEntry);""")

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("persistance plan posee : 7 ancres")
