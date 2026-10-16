# -*- coding: utf-8 -*-
"""Restaure les 3 handlers avalés par le remplacement par bornes (source : git HEAD)."""
import subprocess

head = subprocess.run(["git", "show", "HEAD:bilan_economique.html"], capture_output=True, text=True, encoding="utf-8").stdout

def extraire(source, debut_sel, fin_sel):
    """extrait le bloc handler complet du debut_sel jusqu'au '});' fermant le forEach."""
    i = source.find(debut_sel)
    assert i > 0, "introuvable : " + debut_sel
    j = source.find(fin_sel, i)
    assert j > i
    fin = source.find("});", j)
    assert fin > 0
    return source[i:fin+3]

h1 = extraire(head, 'root.querySelectorAll(".essai-cloture")', 'el.addEventListener')
h2 = extraire(head, 'root.querySelectorAll(".ap-tuile[data-cle-detail]")', 'tuile.addEventListener("click"')
h3 = extraire(head, 'root.querySelectorAll(".foot-cell-annuel")', 'cell.addEventListener("click"')

p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()
ancre = "  /* v4.48 — compléter depuis la prod (base excel) : ajout SEUL, jamais de remplacement */"
assert s.count(ancre) == 1
# insérer les 3 restaurés AVANT le handler v4.48 (leur ordre d'origine)
s = s.replace(ancre, "  " + h1 + "\n  " + h2 + "\n  " + h3 + "\n\n" + ancre)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("3 handlers restaurés")
