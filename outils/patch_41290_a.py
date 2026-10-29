# -*- coding: utf-8 -*-
# Tour 107 — 4.129.0, LOT 5 (hygiène) — patch A : le source
# 1. TOOL_VERSION 4.128.0 -> 4.129.0
# 2. La charnière passe en step="any" + inputmode="numeric" (un 1250 saisi
#    passait :invalid avec step="500" — le navigateur invalidait une valeur
#    légale, l'outil restait utilisable mais le champ restait marqué rouge
#    au test :invalid).
# 3. Entrée NOUVEAUTES en tête du tableau.
import io, sys

F = "bilan_economique.html"
src = io.open(F, encoding="utf-8").read()
orig = src

def remplacer(avant, apres, label):
    global src
    n = src.count(avant)
    assert n == 1, "ancre %s : %d occurrences (attendu 1)" % (label, n)
    src = src.replace(avant, apres)
    print("ok  " + label)

# --- 1. version -------------------------------------------------------------
remplacer('const TOOL_VERSION = "4.128.0";',
          'const TOOL_VERSION = "4.129.0";', "TOOL_VERSION")

# --- 2. la charnière : step="any" -------------------------------------------
remplacer('<input class="cell" ${attrs} data-field="charniere" type="number" step="500" min="0" value="${p.charniere ?? ""}"></td>',
          '<input class="cell" ${attrs} data-field="charniere" type="number" step="any" inputmode="numeric" min="0" value="${p.charniere ?? ""}"></td>',
          "charniere step=any")

# --- 3. NOUVEAUTES -----------------------------------------------------------
NOUV_ANCRE = 'const NOUVEAUTES = [\n'
NOUV_ENTREE = '''const NOUVEAUTES = [
  { version:"4.129.0", date:"29/10/2026", points:[
    "<b>L\u2019outil livré se met au régime — et l\u2019import se teste en hostilité.</b> Le fichier que votre navigateur télécharge perd ses <b>~3 500 lignes de tests internes</b> (elles vivent toujours avec le code, mais ne voyagent plus jusqu\u2019aux postes : ~14 % de moins à chaque mise à jour). À l\u2019import, un <b>test de sécurité rejoué à chaque livraison</b> injecte un script hostile dans chaque champ texte d\u2019un suivi et vérifie qu\u2019aucun n\u2019est exécuté. Et la durée de vie (charnière) n\u2019invalide plus une valeur libre comme 1 250 — le champ accepte tout nombre."
  ]},
'''
n = src.count(NOUV_ANCRE)
assert n == 1, "ancre NOUVEAUTES : %d occurrences (attendu 1)" % n
src = src.replace(NOUV_ANCRE, NOUV_ENTREE)
print("ok  NOUVEAUTES 4.129.0")

assert src != orig
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch A appliqué.")
