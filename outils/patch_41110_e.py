# -*- coding: utf-8 -*-
"""Tour 94 — v4.111.0 — cosmétique vu au navigateur : les badges « ajouté »
et « sorti de » collaient « € » après un fmtEuroCourt qui finit déjà par €
(« 3,6 k€ €/an »). On aligne sur la ligne du verdict : fmtEuroCourt + « /an »."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


remplace(
'ajouté — absent de la référence : ${ajoutCoutEur.complet ? fmtEuroCourt(Math.round(ajoutCoutEur.cout)) + " €/an" : "prix ou charnière incomplets"}',
'ajouté — absent de la référence : ${ajoutCoutEur.complet ? fmtEuroCourt(Math.round(ajoutCoutEur.cout)) + "/an" : "prix ou charnière incomplets"}',
"1. badge ajouté : unité simple")

remplace(
'sorti de : ${sortieInfos.map(s => escapeAttr(s.nom) + " (" + fmtEuroCourt(Math.round(s.cout)) + " €/an)").join(", ")}',
'sorti de : ${sortieInfos.map(s => escapeAttr(s.nom) + " (" + fmtEuroCourt(Math.round(s.cout)) + "/an)").join(", ")}',
"2. badge sorti de : unité simple")

io.open(p, "w", encoding="utf-8").write(s)
print("correctif posé")
