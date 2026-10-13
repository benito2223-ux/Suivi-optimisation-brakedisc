# -*- coding: utf-8 -*-
"""Patch v4.85.0 : LE CATALOGUE PLAQUETTES — socle de la demarche commerciale.

Decisions Benjamin (13/10, validees) :
 1. un MABEC = UN prix (Matis verifiera le fichier prix ; 209 560 = 38 EUR) ;
 2. les gains du tableau commercial : valeurs classeur en phase 1, DDV d'essai
    seulement APRES validation operateur (protocole 5x) ;
 3. le fichier catalogue : un CSV standalone, edite dans Excel, importe a la main.

Ce patch pose le SOCLE : persistance dans le suivi (payload/loadAll/migration/
import remplace+fusion), fonctions pures (seed, application avec rapport,
CSV aller-retour tolerant), panneau 📚 Catalogue avec les 4 gestes.
La vitrine (Plan de conversion) et les suggestions : tour suivant.
"""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()
cpt = []

def rep(av, ap, n=1):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:90]
    s = s.replace(av, ap, n)
    cpt.append(av[:40])

# ── 1. la globale, a cote de livraisons ─────────────────────────────────────
rep("let livraisons = [];",
"""let livraisons = [];
/* v4.85 — LE CATALOGUE PLAQUETTES. Une ligne = UN article : { mabec, iso, prix,
   aretes, ddv }. Decisions Benjamin (13/10) : un MABEC = UN prix (Matis verifie
   le fichier prix ; 209 560 = 38 EUR) ; le fichier est un CSV standalone edite
   dans Excel ; les DDV d'essai n'entrent dans le tableau commercial qu'apres
   validation operateur. Le catalogue voyage dans le suivi (payload, import) et
   se propage aux logements avec rapport — jamais en silence (§3.2). */
let catalogue = [];

function normalizeArticleCat(a){
  return Object.assign({ mabec: "", iso: "", prix: "", aretes: "", ddv: "" }, a,
    { mabec: String((a && a.mabec) || "").trim().toUpperCase(),
      iso: String((a && a.iso) || "").trim(),
      prix: (a && a.prix) !== "" && a && a.prix != null ? Number(a.prix) : "" });
}""")
cpt and None

# ── 2. payloadSuivi : le catalogue voyage ────────────────────────────────────
rep("activeScenarioId: activeId, livraisons });",
    "activeScenarioId: activeId, livraisons, catalogue });")

# ── 3. migrerArbre (format 8) : lire le catalogue ───────────────────────────
rep("return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables, livraisons: Array.isArray(source.livraisons) ? source.livraisons.map(normalizeLivraison) : [] };",
"""return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables,
           catalogue: Array.isArray(source.catalogue) ? source.catalogue.map(normalizeArticleCat) : [],
           livraisons: Array.isArray(source.livraisons) ? source.livraisons.map(normalizeLivraison) : [] };""")

# ── 4. loadAll : lire le catalogue ───────────────────────────────────────────
rep("""        specsUsine = normaliserSpecsUsine(parsed.specsUsine);
        synchroNote = parsed.synchroNote || null;""",
"""        specsUsine = normaliserSpecsUsine(parsed.specsUsine);
        synchroNote = parsed.synchroNote || null;
        catalogue = (parsed.catalogue || []).map(normalizeArticleCat);""")

# ── 5. preparerImportDepuis : exposer le catalogue entrant ──────────────────
rep('''  return { nouvellesLignes, nouveauxProjets, nouveauxResponsables, nouveauBacklog, revisionEntrante,
           livraisons: migreImport ? (migreImport.livraisons || []) : [] };''',
'''  return { nouvellesLignes, nouveauxProjets, nouveauxResponsables, nouveauBacklog, revisionEntrante,
           catalogue: migreImport ? (migreImport.catalogue || []) : [],
           livraisons: migreImport ? (migreImport.livraisons || []) : [] };''')

# ── 6. appliquerImport : remplace / fusion du catalogue ─────────────────────
rep('''    const nouvellesLivraisons = (importEnAttente && importEnAttente.livraisons) || [];
    livraisons = (livraisons || []).concat(nouvellesLivraisons.filter(nl => !(livraisons || []).some(x => x.id === nl.id)));''',
'''    const nouvellesLivraisons = (importEnAttente && importEnAttente.livraisons) || [];
    livraisons = (livraisons || []).concat(nouvellesLivraisons.filter(nl => !(livraisons || []).some(x => x.id === nl.id)));
    /* fusion du catalogue : un MABEC = une entree, l'entrant gagne sur conflit */
    if(Array.isArray(importEnAttente.catalogue)){
      const parMabec = {};
      catalogue.forEach(a => { parMabec[a.mabec] = a; });
      importEnAttente.catalogue.forEach(a => { parMabec[a.mabec] = a; });
      catalogue = Object.values(parMabec).map(normalizeArticleCat);
    }''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("persistance catalogue posee :", len(cpt), "ancres :", len(cpt))
