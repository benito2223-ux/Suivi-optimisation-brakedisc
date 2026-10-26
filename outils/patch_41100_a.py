# -*- coding: utf-8 -*-
"""Tour 93 — v4.110.0 — brique B (UI) : le badge de codification sur les
fiches scénario.

Ce que le patch pose (ancres exactes, assert avant chaque remplacement) :
  1. `badgeCodifScenario(sc)` — pure, dérive le badge HTML depuis
     `codificationScenario` (4.106). Trois états du sémantique Benjamin
     (23/10) : codifié / attente X j / non demandée. Base excel et scénario
     sans article : PAS de badge (hors exigence, Hermes Q2).
  2. `planScenariosHTML` : la fiche porte `codifB` (dérivé à la construction)
     et l'affiche dans la cellule État, à côté du badge d'état.
  3. TOOL_VERSION = 4.110.0.
  4. Entrée NOUVEAUTES en tête.
  5. Tests runTests : les trois états + hors exigence + le rendu de la fiche.
"""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)


def remplace(ancien, nouveau, nom):
    global s
    n = s.count(ancien)
    assert n == 1, "ancre %s : %d occurrences (attendu 1)" % (nom, n)
    s = s.replace(ancien, nouveau)
    print("ok  %s" % nom)


# ── 1. la fonction pure, juste après codificationScenario ────────────────────
A1 = (
    '  if(tousCodifies) return { etat: "codifie" };\n'
    '  return { etat: joursDemande ? "attente" : "nonDemandee", jours: ageMax, manquants };\n'
    '}\n'
)
N1 = A1 + (
    '\n'
    '/* v4.110 — le badge de codification sur les fiches scénario (brique B, UI) :\n'
    '   l\'état dérivé (codificationScenario) rendu là où le scénario est jugé —\n'
    '   « codifié » = tous les articles le sont, cycle standard accessible ;\n'
    '   « attente X j » / « non demandée » = BADP seulement (sémantique Benjamin\n'
    '   23/10). La couche « base excel » et un scénario sans article ne portent\n'
    '   PAS de badge (hors exigence, Hermes Q2 — jamais d\'article fantôme). */\n'
    'function badgeCodifScenario(sc){\n'
    '  const cod = codificationScenario(sc);\n'
    '  if(cod.etat === "codifie")\n'
    '    return ` <span class="pc-stat serie" style="font-size:10.5px;" title="Tous les articles du scénario sont codifiés : le cycle de commande standard est accessible.">codifié</span>`;\n'
    '  if(cod.etat === "attente")\n'
    '    return ` <span class="pc-stat attente" style="font-size:10.5px;" title="Codification par le service administratif de Matis : prérequis du cycle de commande standard — sans elle, BADP seulement (montants et récurrence limités). En attente : ${escapeAttr((cod.manquants || []).join(" · "))}">codification attendue ${cod.jours ?? 0} j</span>`;\n'
    '  if(cod.etat === "nonDemandee")\n'
    '    return ` <span class="pc-stat attente" style="font-size:10.5px;" title="Aucune codification demandée : le cycle de commande standard est inaccessible — BADP seulement. Concerné : ${escapeAttr((cod.manquants || []).join(" · "))}">codification non demandée</span>`;\n'
    '  return "";\n'
    '}\n'
)
remplace(A1, N1, "1. fonction badgeCodifScenario")

# ── 2a. la fiche dérive son badge à la construction ──────────────────────────
A2 = (
    '    lignesSc.push({ grp, cls, libelle,\n'
    '      ligne: p.ligne, opCode: p.opCode, ref: (r.ref && r.ref.nom) || "?",\n'
    '      scenario: sc.name || "Sans nom", gain: r.gain,\n'
    '      dec: decompositionLeviers(r.prodSc, r.meilleur.sc, r.volume),\n'
)
N2 = (
    '    lignesSc.push({ grp, cls, libelle,\n'
    '      ligne: p.ligne, opCode: p.opCode, ref: (r.ref && r.ref.nom) || "?",\n'
    '      scenario: sc.name || "Sans nom", gain: r.gain,\n'
    '      codifB: badgeCodifScenario(sc),\n'
    '      dec: decompositionLeviers(r.prodSc, r.meilleur.sc, r.volume),\n'
)
remplace(A2, N2, "2a. la fiche porte codifB")

# ── 2b. le badge s'affiche à côté de l'état ──────────────────────────────────
A3 = '        <td><span class="pc-stat ${l.cls}">${l.libelle}</span></td>\n'
N3 = '        <td><span class="pc-stat ${l.cls}">${l.libelle}</span>${l.codifB}</td>\n'
remplace(A3, N3, "2b. cellule État + badge codification")

# ── 3. la version ─────────────────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.109.1";', 'const TOOL_VERSION = "4.110.0";', "3. TOOL_VERSION")

# ── 4. l'entrée NOUVEAUTES ────────────────────────────────────────────────────
A4 = 'const NOUVEAUTES = [\n  { version:"4.109.1", date:"25/10/2026", points:[\n'
N4 = (
    'const NOUVEAUTES = [\n'
    '  { version:"4.110.0", date:"26/10/2026", points:[\n'
    '    "<b>La codification se voit sur chaque scénario.</b> Dans « Scénarios en validation » du Plan, chaque fiche scénario porte désormais son <b>badge de codification</b> : <b>codifié</b> (tous les articles le sont — le cycle de commande standard est accessible), <b>codification attendue X j</b> (la demande est posée chez Matis — l\'âge de l\'attente est la métrique) ou <b>codification non demandée</b> (BADP seulement). Les articles manquants sont nommés dans l\'info-bulle. La base « excel » historique n\'est pas concernée."\n'
    '  ]},\n'
    '  { version:"4.109.1", date:"25/10/2026", points:[\n'
)
remplace(A4, N4, "4. entrée NOUVEAUTES")

# ── 5. les tests runTests, après le bloc codification 4.106 ──────────────────
A5 = (
    '      } finally { catalogue = catAvT; }\n'
    '      /* le dossier de visite sur un mini-arbre : un acté via BADP, un essai\n'
)
N5 = (
    '      } finally { catalogue = catAvT; }\n'
    '      /* v4.110 — le badge de codification sur les fiches scénario (brique B) :\n'
    '         les trois états du sémantique Benjamin, la base excel hors badge. */\n'
    '      {\n'
    '        const scB = { name: "Candidat B", outils: [ { logements: [ { codeArticle: "A1" }, { codeArticle: "A2" } ] } ] };\n'
    '        const scBx = { name: "Prod actuelle (base excel)", outils: [ { logements: [ { codeArticle: "IM02 000 001" } ] } ] };\n'
    '        const catAvB = catalogue;\n'
    '        catalogue = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "A2", codificationDemandeeLe: "2026-07-01" } ];\n'
    '        try {\n'
    '          ok("badge codification : état « attente » — l\'âge du plus vieux et l\'article manquant sont dans le badge",\n'
    '             [badgeCodifScenario(scB).indexOf("codification attendue") > -1,\n'
    '              badgeCodifScenario(scB).indexOf(String(joursDepuis("2026-07-01"))) > -1,\n'
    '              badgeCodifScenario(scB).indexOf("A2") > -1],\n'
    '             [true, true, true]);\n'
    '          catalogue = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "A2", codifieLe: "2026-02-01" } ];\n'
    '          ok("badge codification : tous les articles codifiés = badge « codifié » (même pilule verte que le catalogue)",\n'
    '             [badgeCodifScenario(scB).indexOf(">codifié<") > -1,\n'
    '              badgeCodifScenario(scB).indexOf("pc-stat serie") > -1],\n'
    '             [true, true]);\n'
    '          catalogue = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "INCONNU" } ];\n'
    '          ok("badge codification : rien demandé = le badge le dit (cycle standard inaccessible, BADP seulement)",\n'
    '             badgeCodifScenario(scB).indexOf("codification non demandée") > -1, true);\n'
    '          ok("badge codification : la couche « base excel » ne porte AUCUN badge (hors exigence, Hermes Q2)",\n'
    '             badgeCodifScenario(scBx), "");\n'
    '          /* la fiche du Plan affiche le badge à côté de l\'état du scénario */\n'
    '          const recapB = { postes: [ { ligne: "EMAG 1", opCode: "OP10", refs: [ {\n'
    '            ref: { nom: "356x26" }, gain: 1200, serie: true, volume: 10000,\n'
    '            prodSc: scBx, meilleur: { sc: scB }, perimetrePartiel: [] } ] } ] };\n'
    '          catalogue = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "A2", codificationDemandeeLe: "2026-07-01" } ];\n'
    '          ok("badge codification : la fiche « Scénarios en validation » porte le badge — état et codification visibles ensemble",\n'
    '             [planScenariosHTML(recapB).indexOf("codification attendue") > -1,\n'
    '              planScenariosHTML(recapB).indexOf("En série — gain acté") > -1],\n'
    '             [true, true]);\n'
    '        } finally { catalogue = catAvB; }\n'
    '      }\n'
    '      /* le dossier de visite sur un mini-arbre : un acté via BADP, un essai\n'
)
remplace(A5, N5, "5. tests runTests")

io.open(p, "w", encoding="utf-8").write(s)
print("patch 4.110.0 posé :", n0, "->", len(s))
