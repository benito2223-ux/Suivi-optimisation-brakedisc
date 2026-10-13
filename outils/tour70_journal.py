# -*- coding: utf-8 -*-
"""Tour 70 : CHANGELOG 4.87.0 + entree de journal (verrou deja libere a la main)."""

c = open('CHANGELOG.md', encoding='utf-8').read()
entree = """## [4.87.0] — 2026-10-14 · Tour 70

**Plein écran partout où ça compte.** Retour de Benjamin : « l'affichage de
l'accueil et du plan de conversion sont vraiment trop petits et illisibles ».

### Ajouté
- **plein écran GÉNÉRIQUE** : la règle CSS passe de `#simulPanel` à **tout
  `.panel`** — l'accueil, le Plan de conversion et le Simulateur passent en
  vraie pleine surface (plus de colonne de 1120 px), le mode natif est tenté
  par-dessus (projection) ;
- **polices majorées en mode maxi** : table 16,5 px, titres 22 px, champs 14 px
  — la lecture à distance de réunion ;
- **basculerMaxi()** générique : un bouton ⛶ sur l'accueil (pied) et sur le
  Plan ; le Simulateur délègue au même mécanisme ; Échap rend la main ;
- porte hors-suite étendue : **6 règles** lues dans le fichier réel.

"""
ancre = "## [4.86.0]"
assert ancre in c
c = c.replace(ancre, entree + ancre, 1)
open('CHANGELOG.md', 'w', encoding='utf-8').write(c)
print("changelog 4.87.0")

s = open('ECHANGES.md', encoding='utf-8').read()
tour = """### Tour 70 — 14/10/2026 — **Z Code** (v4.87.0 — plein écran partout où ça compte)

**La commande.** Benjamin : « l'affichage de l'accueil et du plan de
conversion sont vraiment trop petits et illisibles — comment modifier pour
avoir un quasi plein écran voire un écran plein ? »

**Le diagnostic.** Les deux écrans vivent dans des panneaux `panel-large`
bridés à 1120 px — et l'accueil lui-même EST un panneau depuis la décision
overview (4.62). Un seul remède valait la peine : un mode plein écran
GÉNÉRIQUE, pas trois rustines.

**Livré.** La règle CSS passe de `#simulPanel` à **tout `.panel`** ;
`basculerMaxi()` générique (CSS maxi + Fullscreen API native, Échap rend la
main) ; boutons ⛶ sur l'accueil (pied) et le Plan ; le Simulateur délègue ;
**les polices montent en maxi** (table 16,5 px, titres 22 px, champs 14 px).
Porte hors-suite étendue à 6 règles lues dans le fichier réel.

**Vérifié.** 542/542 verts, node --check propre. Déployé sur Projet, vérifié
curl. La prod attend la phrase de Benjamin.

**Écart déclaré.** Le verrou n'a pas été repris avant l'écriture du tour 70
(oubli, repéré à la libération) — aucune collision réelle (Hermes
n'écrivait pas), la règle est réaffirmée au VERROU.

**Prochain tour** : les suggestions à la saisie ; la revue d'Hermes ;
l'export de l'accueil ; le chantier UI.

"""
ancre = "## Questions ouvertes à Z Code"
assert ancre in s
s = s.replace(ancre, tour + ancre, 1)
open('ECHANGES.md', 'w', encoding='utf-8').write(s)
print("tour 70 écrit")
