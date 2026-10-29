# -*- coding: utf-8 -*-
# Tour 107 — 4.129.0 — patch D3 : la porte lot 5 était FAUSSE AU VERT
# (attrapée par le contre-regard CR2) : le motif « Tests du moteur economique »
# survit dans le COMMENTAIRE de l étape 5 bis même quand le code est amputé.
# La porte vise désormais la DÉCLARATION complète du marqueur dans le build.
import io

F = "build_harness.py"
src = io.open(F, encoding="utf-8").read()

AVANT = """      [['Tests du moteur economique', 'le build ne repère plus le bloc des tests'],"""
APRES = """      [["const MARQUE_TESTS = 'Tests du moteur economique';", 'le build ne repère plus le bloc des tests (déclaration amputée)'],"""
n = src.count(AVANT)
assert n == 1, "ancre : %d occurrences (attendu 1)" % n
src = src.replace(AVANT, APRES)
io.open(F, "w", encoding="utf-8", newline="
").write(src)
print("patch D3 appliqué.")
