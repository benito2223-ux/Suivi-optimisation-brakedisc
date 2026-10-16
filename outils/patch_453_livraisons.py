# -*- coding: utf-8 -*-
"""Patch v4.53 : entité LIVRAISON (décision 3) — figée, datée, imprimable, voyagée."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# ── 1. globale déclarée avant loadAll (rituel anti-TDZ) ──
avant = """let synchroNote = null;
loadAll();
recomputeCycles();"""
apres = """let synchroNote = null;
/* v4.53 — les LIVRAISONS : l'objet que la hiérarchie lit (décision 3 de la constitution).
   Une livraison = un instantané FIGÉ et DATÉ des gains du plan (actés, en cours, plan
   poste par poste, cibles). Elle ne bouge plus : les chiffres vivent dans l'objet, pas
   dans les scénarios. Déclarée AVANT loadAll() (rituel anti-TDZ). */
let livraisons = [];
loadAll();
recomputeCycles();"""
assert s.count(avant) == 1, "globale"
s = s.replace(avant, apres)

# ── 2. migrerArbre : les 3 retours portent livraisons ──
avant = """    return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables };"""
apres = """    return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables, livraisons: Array.isArray(source.livraisons) ? source.livraisons.map(normalizeLivraison) : [] };"""
assert s.count(avant) == 1, "return 1"
s = s.replace(avant, apres)
avant = """    return { lignes: lignesPlates, projets: fin.projets, responsables: fin.responsables };"""
apres = """    return { lignes: lignesPlates, projets: fin.projets, responsables: fin.responsables, livraisons: [] };"""
assert s.count(avant) == 1, "return 2"
s = s.replace(avant, apres)

# ── 3. normalizeLivraison (près de normalizeProjet) ──
avant = "function getActiveLigne(){ return lignes.find(l => l.id === activeLigneId) || lignes[0]; }"
apres = """/* v4.53 — une livraison est un INSTANTANÉ FIGÉ : ses chiffres ne se recalculent jamais.
   normalizeLivraison ne fait qu'assurer la forme (l'exactitude est figée à la création). */
function normalizeLivraison(l){
  return Object.assign({
    id: l.id || ("lv" + Math.random().toString(36).slice(2)),
    nom: l.nom || "Livraison",
    date: l.date || "",
    creePar: l.creePar || "",
    gainsActes: l.gainsActes ?? null,
    gainsEnCours: l.gainsEnCours ?? null,
    plan: Array.isArray(l.plan) ? l.plan : [],
    cibles: Array.isArray(l.cibles) ? l.cibles : [],
    essais: Array.isArray(l.essais) ? l.essais : [],
    protocole: l.protocole || "Tout essai concluant est répété 5× ; validé 5× et viable économiquement, il passe en production."
  }, l);
}
function getActiveLigne(){ return lignes.find(l => l.id === activeLigneId) || lignes[0]; }"""
assert s.count(avant) == 1, "normalizeLivraison"
s = s.replace(avant, apres)

# ── 4. payloadSuivi : les livraisons voyagent (cloud + export) ──
avant = """  return JSON.stringify({ format:8, lignes, projets, activeProjetId, responsables, backlog, revision, specsUsine, synchroNote, activeLigneId, activeReferenceId, activeOpId, activeScenarioId: activeId });"""
apres = """  return JSON.stringify({ format:8, lignes, projets, activeProjetId, responsables, backlog, revision, specsUsine, synchroNote, activeLigneId, activeReferenceId, activeOpId, activeScenarioId: activeId, livraisons });"""
assert s.count(avant) == 1, "payloadSuivi"
s = s.replace(avant, apres)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("livraisons : globales, migration, sérialisation OK")
