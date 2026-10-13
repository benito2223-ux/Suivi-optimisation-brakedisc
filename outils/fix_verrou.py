# -*- coding: utf-8 -*-
"""Reconstruit VERROU.md : base 43f1efb + liberation tour 70 + tour 71 (pris retroactif)."""

base = open('verrou_base_tmp.txt', encoding='utf-8').read()
q = chr(39)

# retirer le marqueur collee "Verrou pris tour 69" (le tour 69 est libere juste au-dessus)
base = base.replace(
    "`VERROU.md`." + chr(128274) + " **Verrou pris par Z Code le 14/10/2026 matin** (tour 69, v4.86.0 — le Plan de conversion).",
    "`VERROU.md`.")
base = base.replace(
    "`VERROU.md`." + chr(128274) + " **Verrou pris par Z Code le 14/10/2026 matin** (tour 69, v4.86.0 - le Plan de conversion).",
    "`VERROU.md`.")

entetes = """| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 71, v4.88.0 — verrou pris
RÉTROACTIVEMENT, écart déclaré : le code était écrit avant la prise, aucun
autre auteur n'est intervenu). Pendant le tour, `bilan_economique.html` est
passé à l'empreinte post-patch : le **basculeur de consommation** dans le
Plan de conversion (théorique / RÉELLE extrapolée — les feuilles « Pareto
conso » des classeurs, une semaine × 52, lecture locale session-only ;
`consoDepuisFeuille()` pure, pareto de COUT refusé, ligne d'en-têtes
cherchée), un article sans donnée réelle **perd son gain** (jamais complété),
l'export CSV porte le mode, `TOOL_VERSION = "4.88.0"`, NOUVEAUTES +
CHANGELOG. 521 → **547/547 verts**. **Déployé sur Projet, vérifié curl ; la
PROD (4.87.0) attend la phrase de Benjamin.** Écrits :
`bilan_economique.html`, `outils/patch_4880_a/b.py`, `outils/tour71_journal.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.
**Accroc du tour : le VERROU lui-même a été commité VIDE par le tour 70
(`open('w')` tronquait avant un NameError) — reconstruit ici depuis
43f1efb, avec les entrées 70 et 71.**

---

✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 70, v4.87.0). Pendant le
tour, le plein écran GÉNÉRIQUE (`.panel.simul-maxi` — accueil, plan,
simulateur, catalogue), `basculerMaxi()` (boutons ⛶ sur l'accueil et le
Plan ; le Simulateur délègue), polices majorées en maxi (table 16,5 px,
titres 22 px), porte hors-suite à **6 règles**, `TOOL_VERSION = "4.87.0"`.
542/542 verts, syntaxe vérifiée par node --check. **Déployé sur Projet, puis
en prod sur la phrase de Benjamin (« passe en prod »), vérifiés curl.**
Écart déclaré : verrou non repris avant l'écriture du tour 70.

---

"""

# le corps de la base commence par sa table libre + tour 69 : on garde tout apres l'entete
i = base.find("**Verrou libere par Z Code le 14/10/2026**")
sortie = entetes + base[i:]
open('VERROU.md', 'w', encoding='utf-8', newline='\n').write(sortie)
print("VERROU reconstruit :", len(sortie), "octets")
