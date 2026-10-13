# -*- coding: utf-8 -*-
"""Verrou : pris AVANT l'ecriture (tour 72)."""

v = open('VERROU.md', encoding='utf-8').read()
table = ("| **Auteur** | Z Code |\n"
         "| **Pris le** | 14/10/2026 soir |\n"
         "| **\u00c9crit dans** | `bilan_economique.html` |\n"
         "| **Version vis\u00e9e** | 4.89.0 |\n"
         "| **Sujet** | LES SUGGESTIONS \u00c0 LA SAISIE : l'autocomplete du catalogue"
         " \u2014 taper un MABEC ou un ISO propose les articles connus et remplit"
         " prix/ar\u00eates/DDV d'un clic. Le dernier morceau du socle commercial."
         " Verrou pris AVANT l'\u00e9criture cette fois. |\n\n"
         "\U0001F512 **Verrou pris par Z Code le 14/10/2026 soir** (tour 72, v4.89.0"
         " \u2014 les suggestions \u00e0 la saisie).")

i = v.find("| **Auteur** | *(libre)* |")
assert i > -1, "table introuvable"
j = v.find("\n\n", i)
v = v[:i] + table + v[j+2:]
open('VERROU.md', 'w', encoding='utf-8', newline='').write(v)
print("verrou pris AVANT l'ecriture (par fichier)")
