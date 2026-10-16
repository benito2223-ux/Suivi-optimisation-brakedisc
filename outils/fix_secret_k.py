# -*- coding: utf-8 -*-
"""Fix 4.89.1 : le secret K (formule + points de production) dans l'aide livree — retire.

Claude, revue P1 : « K et P_req sont peut-etre dans le source » — l'audit grep
confirme : la ligne 2041 expose la FORMULE K = Vc x f x sin(kr) AVEC les points
de production (174 et 448), et la 2042 expose la decomposition Fr/Fa avec les
angles reels valides (75 degres, 85 degres). Aide visible dans l'UI = violation
directe de la regle §2.6 (jamais K ni P_req dans toute sortie visible).
"""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

# le bloc aide entier (h4 + ul), de l'ancre de titre a la fermeture du ul
i = s.find('<h4 id="aideTitreK">Formules du widget K / Fr\u00b7Fa</h4>')
assert i > -1, "bloc aide K introuvable"
j = s.find('</ul>', i)
assert j > -1
j += len('</ul>')

bloc = s[i:j]
assert 'K = Vc' in bloc and '174 et 448' in bloc and 'Fr/Fa' in bloc, "contenu inattendu"

remplacement = (
    '<h4 id="aideTitreK">Widget K / Fr\u00b7Fa</h4>\n'
    '      <ul>\n'
    '        <li>Cet indice est un <b>indice comparatif interne SPK</b> : sa formule, ses points de r\u00e9f\u00e9rence'
    ' et ses conditions de validit\u00e9 restent <b>internes</b> et ne sont pas document\u00e9s dans l\u2019outil.'
    ' Il sert \u00e0 situer un sc\u00e9nario par rapport aux points d\u00e9j\u00e0 \u00e9prouv\u00e9s en production.</li>\n'
    '      </ul>'
)
s = s[:i] + remplacement + s[j:]

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)

# verification : plus de formule, plus de points, plus d'angles
s2 = open('bilan_economique.html', encoding='utf-8', newline='').read()
assert 'K = Vc' not in s2, "la formule K traine encore"
assert '174 et 448' not in s2, "les points de production trainent"
assert 'valid\u00e9 le 26/08' not in s2, "l'angle valid\u00e9 traine"
print("bloc aide K remplace : formule, points et angles retires — verifie")
