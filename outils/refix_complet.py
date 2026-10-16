# -*- coding: utf-8 -*-
"""Comprehensive : refix secret K (perdu au checkout) + version 4.90.0 + NOUVEAUTES + thead."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

# ── 1. REFIX secret K (le checkout l'a perdu) ────────────────────────────────
i = s.find('<h4 id="aideTitreK">Formules du widget K / Fr·Fa</h4>')
if i > -1:
    j = s.find('</ul>', i)
    assert j > -1
    j += len('</ul>')
    bloc = s[i:j]
    assert 'K = Vc' in bloc and '174 et 448' in bloc
    remplacement = (
        '<h4 id="aideTitreK">Widget K / Fr·Fa</h4>\n'
        '      <ul>\n'
        '        <li>Cet indice est un <b>indice comparatif interne SPK</b> : sa formule, ses points de référence'
        ' et ses conditions de validité restent <b>internes</b> et ne sont pas documentés dans l\u2019outil.'
        ' Il sert à situer un scénario par rapport aux points déjà éprouvés en production.</li>\n'
        '      </ul>'
    )
    s = s[:i] + remplacement + s[j:]
    print("REFIX secret K : bloc aide remplacé")
else:
    print("REFIX secret K : déjà absent (ok)")

# ── 2. TOOL_VERSION 4.90.0 ────────────────────────────────────────────────────
av = 'const TOOL_VERSION = "4.89.0";'
assert av in s, "version"
s = s.replace(av, 'const TOOL_VERSION = "4.90.0";', 1)

# ── 3. thead Confirmé ──────────────────────────────────────────────────────────
av2 = '<th>Cible SPK</th><th>Prix cible</th><th>État</th><th>Gain / an</th>'
assert av2 in s, "thead"
s = s.replace(av2, '<th>Cible SPK</th><th>Prix cible</th><th>Confirmé</th><th>État</th><th>Gain / an</th>', 1)

# ── 4. NOUVEAUTES 4.89.1 + 4.90.0 ─────────────────────────────────────────────
av3 = '''const NOUVEAUTES = [
  { version:"4.89.0", date:"14/10/2026", points:['''
ap3 = '''const NOUVEAUTES = [
  { version:"4.90.0", date:"14/10/2026", points:[
    "<b>Les retours de la revue extérieure, appliqués.</b> <b>Plan de conversion</b> : le prix cible se confirme case par case (le total ne compte que le confirmé), l'<b>hypothèse de durée de vie</b> est affichée et réglable, chaque ligne montre son <b>seuil de neutralité</b>, le prix suggéré est un réglage — et « Promesse » s'appelle « Potentiel ». <b>Le Simulateur partage le basculeur</b> du Plan : une seule base de consommation sur tous les écrans. <b>Saisie atelier</b> : usure en grosses pastilles, conformité affichée <b>en direct</b> à la frappe, bornes sur les champs. <b>Lisibilité</b> : plancher de tailles et contrastes remontés. L'accueil affiche la date du dernier export, le bloc Cadence (jamais mesuré) quitte la projection, et les boutons suivent l'ordre du récit : Catalogue → Plan → Simulateur."
  ]},
  { version:"4.89.1", date:"14/10/2026", points:[
    "<b>Correction de confidentialité.</b> L'aide de l'outil affichait une formule thermique interne et ses points de référence production — ça n'avait rien à faire dans un fichier public. Retiré : l'indice reste affiché comme indice comparatif, sa méthode reste interne SPK."
  ]},
  { version:"4.89.0", date:"14/10/2026", points:['''
assert av3 in s, "nouveautes"
s = s.replace(av3, ap3, 1)

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)

s2 = open('bilan_economique.html', encoding='utf-8', newline='').read()
assert 'K = Vc' not in s2, "la formule est toujours là !"
assert 'TOOL_VERSION = "4.90.0"' in s2
assert '<th>Confirmé</th>' in s2
print("comprehensive OK : secret K retiré, 4.90.0, thead, nouveautés")
