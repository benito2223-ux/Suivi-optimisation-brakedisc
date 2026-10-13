# -*- coding: utf-8 -*-
"""Fix : la ligne cell de planCSV est tronquee et doublée — remplacement propre."""

p = 'bilan_economique.html'
s = open(p, encoding='utf-8', newline='').read()
q = chr(39)   # apostrophe
bs = chr(92)  # backslash

# la ligne tronquee (termine au milieu de l'expression) et la ligne orpheline suivante
av = ("  const cell = v => /[\"" + bs + "r" + bs + "n]/.test(String(v)) ? " + q + chr(34) + q +
      " + String(v).replace(/" + chr(34) + "/g, " + q + chr(34)*2 + q + ") + " + q + chr(34) + q + " : String(v);\n" +
      "]/.test(String(v)) ? " + q + chr(34) + q +
      " + String(v).replace(/" + chr(34) + "/g, " + q + chr(34)*2 + q + ") + " + q + chr(34) + q + " : String(v);")
ap = ("  const cell = v => /[\"" + bs + "r" + bs + "n]/.test(String(v)) ? " + q + chr(34) + q +
      " + String(v).replace(/" + chr(34) + "/g, " + q + chr(34)*2 + q + ") + " + q + chr(34) + q + " : String(v);")

assert av in s, "les deux lignes cassees sont introuvables"
s = s.replace(av, ap, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print("planCSV : une seule ligne cell, correcte")
