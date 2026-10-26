# -*- coding: utf-8 -*-
"""Tour 94 — v4.111.0 — correctif : les groupes d'outils construits dans
`parCle` n'étaient jamais poussés dans `outils` (le tableau rendu restait
vide). Vu par le harnais avant toute livraison (test « technique au centime »
sur outils[0] undefined)."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()

avant = """    g.techniqueEurAn = (volume && g.logements.every(x => x.technique !== null))
      ? g.logements.reduce((a, x) => a + x.technique, 0) : null;
  });"""
apres = """    g.techniqueEurAn = (volume && g.logements.every(x => x.technique !== null))
      ? g.logements.reduce((a, x) => a + x.technique, 0) : null;
    outils.push(g);
  });"""

assert s.count(avant) == 1, "ancre : %d occurrences" % s.count(avant)
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("ok : outils.push(g) rétabli")
