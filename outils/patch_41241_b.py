# -*- coding: utf-8 -*-
"""Tour 100 — v4.124.1 — version + NOUVEAUTES (la correction tracée)."""
import io, re

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()

assert s.count('const TOOL_VERSION = "4.124.0";') == 1
s = s.replace('const TOOL_VERSION = "4.124.0";', 'const TOOL_VERSION = "4.124.1";', 1)
print("ok : TOOL_VERSION")

m = re.search(r'const NOUVEAUTES = \[\n  \{ version:"4\.[0-9.]+", date:"[0-9/]+", points:\[\n', s)
assert m, "ancre NOUVEAUTES introuvable"
entree = (
    'const NOUVEAUTES = [\n'
    '  { version:"4.124.1", date:"28/10/2026", points:[\n'
    '    "<b>Correction de mise en forme (revue du 28/10).</b> La version précédente avait perdu une partie de son habillage : une règle de style laissée ouverte pendant la refonte du bandeau de bienvenue faisait ignorer au navigateur tout ce qui suivait — sans aucune erreur visible. Réparé (la règle d\\u2019origine est restaurée), et le garde-fou de test qui vérifie désormais l\\u2019équilibre du style à chaque livraison est posé. Si vous aviez ouvert la version précédente, rouvrez-la : l\\u2019habillage revient seul."\n'
    '  ]},\n'
)
s = s[:m.start()] + entree + s[m.start():]
print("ok : entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch version posé")
