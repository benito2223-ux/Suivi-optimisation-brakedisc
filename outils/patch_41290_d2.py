# -*- coding: utf-8 -*-
# Tour 107 — 4.129.0 — patch D2 : correction de la porte lot 5 (patch D).
# Le motif step="500" est un motif NÉGATIF (échec s'il est PRÉSENT) : il
# figurait dans le tableau des présences, la porte réclamait donc le retour
# du fautif. Il est sorti du tableau et testé séparément.
import io

F = "build_harness.py"
src = io.open(F, encoding="utf-8").read()

AVANT = """      [['data-field="charniere" type="number" step="any" inputmode="numeric"', 'la charniere n accepte pas tout nombre (step any attendu)'],
       ['step="500"', 'le step 500 fauteur d invalid est encore la'],
       ['sécurité import : AUCUN innerHTML ni rendu', 'le test de sécurité à l import est absent de la suite'],
       ['__xssPwned=1', 'le payload hostile du test de sécurité est absent']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });"""
APRES = """      [['data-field="charniere" type="number" step="any" inputmode="numeric"', 'la charniere n accepte pas tout nombre (step any attendu)'],
       ['sécurité import : AUCUN innerHTML ni rendu', 'le test de sécurité à l import est absent de la suite'],
       ['__xssPwned=1', 'le payload hostile du test de sécurité est absent']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });
      if (html.indexOf('step="500"') !== -1) echecs.push('le step 500 fauteur d invalid est encore la');"""
n = src.count(AVANT)
assert n == 1, "ancre porte lot 5 : %d occurrences (attendu 1)" % n
src = src.replace(AVANT, APRES)
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch D2 appliqué.")
