# -*- coding: utf-8 -*-
"""Trace PROD 4.90.0 dans ECHANGES.md (par fichier — pas d'heredoc)."""

s = open('ECHANGES.md', encoding='utf-8', newline='').read()
q = chr(39)
ancre = "PROD 4.89.1"
i = s.find(ancre)
if i == -1:
    # chercher un autre point d'ancrage : la premiere ligne du tableau apres l'entete
    ancre = "PROJET 4.88.0"
    i = s.find(ancre)
if i == -1:
    ancre = "PROD 4.88.0"
    i = s.find(ancre)
assert i > -1, "aucun point d'ancrage trouve"
# remonter au debut de la ligne (le | de la ligne du tableau)
deb_ligne = s.rfind(chr(10), 0, i) + 1
ligne = ("| 14/10 ~soir | **PROD 4.90.0** \u2014 les trois lots de la revue Claude (P7 bugs visibles, "
    "P6 lisibilit\u00e9, P3 honn\u00eatet\u00e9 du Plan, P2 base unique, P4 dernier export, P5 atelier) "
    "+ P8 d\u00e9cision (monolithe canonique), ordre de Benjamin : \u00ab d\u00e9ploie en prod \u00bb. "
    "| suivi-optimisation-septfons.surge.sh | \u2705 552 tests | 0 \u00e9checs relanc\u00e9s avant l\u2019acte ; "
    "curl HTTP 200, **1 486 030 o**, TOOL_VERSION = 4.90.0, SW 200 ; empreinte **identique octet "
    "pour octet** au local (e2aa671c...) ; Projet re-v\u00e9rifi\u00e9 4.90.0 inchang\u00e9 (Z Code, Tour 73 bis) |\n")
s = s[:deb_ligne] + ligne + s[deb_ligne:]
open('ECHANGES.md', 'w', encoding='utf-8', newline='').write(s)
print("trace PROD 4.90.0 inseree avant :", s[deb_ligne+len(ligne)+10:deb_ligne+len(ligne)+60])
