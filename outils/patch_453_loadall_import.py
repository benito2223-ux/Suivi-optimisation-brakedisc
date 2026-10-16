# -*- coding: utf-8 -*-
"""Patch v4.53 (2) : loadAll + appliquerArbre + import + export + tests livraisons."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# ── 1. loadAll : assigner livraisons ──
# loadAll assigne les champs depuis migre — chercher le motif d'assignation générique
import re
# motif : "lignes = migre.lignes;" (loadAll) et l'assignation projet/responsables
m = re.search(r"lignes = migre\.lignes;[^\n]*\n", s)
assert m, "assignation loadAll introuvable"
i = m.start()
# insérer l'assignation livraisons juste après la ligne "lignes = migre.lignes;"
fin = s.find("\n", i) + 1
ins = "  livraisons = (migre.livraisons || []).map(normalizeLivraison);\n"
s = s[:fin] + ins + s[fin:]
print("loadAll : livraisons assignées")

# ── 2. appliquerArbre : idem (restauration historique/reprise) ──
avant = """function appliquerArbre(source){
  const migre = migrerArbre(source);
  lignes = migre ? migre.lignes : [];
  projets = migre ? migre.projets : [];
  responsables = migre ? migre.responsables : [];"""
apres = """function appliquerArbre(source){
  const migre = migrerArbre(source);
  lignes = migre ? migre.lignes : [];
  projets = migre ? migre.projets : [];
  responsables = migre ? migre.responsables : [];
  livraisons = (migre && migre.livraisons) ? migre.livraisons.map(normalizeLivraison) : [];"""
assert s.count(avant) == 1, "appliquerArbre"
s = s.replace(avant, apres)

# ── 3. export payload (2298) : les livraisons partent dans l'export ──
avant = 'const payload = { outil:"SPK Suivi optimisation", format:8, toolVersion:TOOL_VERSION, revision, exporteLe:new Date().toISOString(), exportePar:auteurNom, lignes, projets, activeProjetId, responsables, backlog };'
apres = 'const payload = { outil:"SPK Suivi optimisation", format:8, toolVersion:TOOL_VERSION, revision, exporteLe:new Date().toISOString(), exportePar:auteurNom, lignes, projets, activeProjetId, responsables, backlog, livraisons };'
assert s.count(avant) == 1, "export payload"
s = s.replace(avant, apres)
print("export : livraisons incluses")

# ── 4. import : preparerImportDepuis porte les livraisons ──
avant = """    const fin = finaliserProjetsEtResponsables(projetsLus, source.responsables);
    return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables };"""
if s.count(avant) == 1:
    s = s.replace(avant, """    const fin = finaliserProjetsEtResponsables(projetsLus, source.responsables);
    return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables, livraisons: (source.livraisons || []).map(normalizeLivraison) };""")
    print("import : livraisons portées")
else:
    # variante : chercher le return de la branche format 8 de preparerImportDepuis
    m2 = re.search(r"(function preparerImportDepuis[\s\S]{0,2000}?)return \{ lignes: lignesLues, projets: fin\.projets, responsables: fin\.responsables \};", s)
    assert m2, "return preparerImportDepuis introuvable"
    s = s[:m2.start(1)] + s[m2.start(1):m2.end(1)].replace(
        "return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables };",
        "return { lignes: lignesLues, projets: fin.projets, responsables: fin.responsables, livraisons: (source.livraisons || []).map(normalizeLivraison) };"
    ) + s[m2.end(1):]
    print("import (variante) : livraisons portées")

# ── 5. appliquerImport : assigner ──
# appliquerImport(mode) applique nouvellesLignes etc. — livraisons suivent nouvellesLignes
avant = "      lignes = importEnAttente.nouvellesLignes;"
if s.count(avant) == 1:
    s = s.replace(avant, avant + "\n      livraisons = (importEnAttente.livraisons || []).map(normalizeLivraison);")
    print("appliquerImport : livraisons suivent")
else:
    print("!! appliquerImport : motif unique non trouvé, vérifier manuellement")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patch 2 OK")
