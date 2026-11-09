# -*- coding: utf-8 -*-
"""Tour 135 — ECHANGES (tour + faits extérieurs) et libération du VERROU."""
import io, re

R = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/"

P = R + "ECHANGES.md"
src = io.open(P, "r", encoding="utf-8", newline="").read()

TOUR = """### ▸ Tour 135 — 10/11/2026 — **Hermes** (4.152.0 — la vue plaquette globale : où elle sert, ce qu'elle rapporte déployée au global ; branche `ux-rail`)

Spec `SPEC_VUE_PLAQUETTE_GLOBALE_2026-11-10.md` (décisions Benjamin prises dans la session) codée intégralement, voir CHANGELOG 4.152.0. **Choix d'implémentation à noter** : (1) la clé ISO ignore **tout séparateur** (« CNGX 120716 » = « cngx120716 » — vu réel : les désignations s'écrivent avec ou sans espaces) ; (2) le levier **temps de coupe est un axe MACHINE séparé, jamais sommé à l'outillage** (constitution §2 quater) — le total SIMULATION reste outillage, l'équivalent machine s'affiche en ligne propre « ±X €/an (±Y h/an) », chiffré seulement où temps de coupe ET taux horaire existent ; (3) les boutons passent toujours l'ISO **complet** venant de l'outil (catalogue, Plan, scénario) — le grade seul (« KY3500 ») ne matche pas et c'est voulu : l'appariement reste exact. **Recette** : 811 tests | 0 échec (+8), node --check 6/6, « tout est vert » au harnais sur le dist final. **À l'écran sur rev435** : ISO réel « SNGN090408F85Z050 KY3500 » → 2 usages chiffrés (EMAG 2 OP40 T548/T549, MABEC Z000 513 527, 454 pl/an, 4,3 k€/an chacun) + 8 exclusions nommées (« manque : volume annuel » — EMAG 1/EMAG 3 OP40) ; simulation prix 5 € + charnière 90 → **−6,9 k€/an**, recalculée à la frappe (prix 3 → −7,6 k€/an) ; étiquette SIMULATION et mention « jamais additionnée aux gains actés » présentes. Capture regardée. **PROD : rien — DEV seule déployée** (règle permanente) ; la PROD attend ta phrase.

### ▸ """

m = re.search(r"### ▸ Tour", src)
assert m, "aucun tour trouvé"
src = src[:m.start()] + TOUR + src[m.start():]

FAIT = """| 10/11 | **DEV 4.152.0 — la vue plaquette globale** (usages par désignation ISO + extrapolation prospective à trois leviers ; Catalogue, Plan, « Ailleurs dans l'usine »). | suivi-optimisation-projet.surge.sh | ✅ curl : DEV sert 4.151.0→4.152.0, empreinte identique au `dist/`, `version.json` = 4.152.0 ; 811 tests \\| 0 échec + « tout est vert » (Hermes, Tour 135). **PROD : rien — attend la phrase de Benjamin** |

"""
ancre_faits = "|---|---|---|---|\n"
i = src.find(ancre_faits)
assert i > 0, "table faits introuvable"
src = src[:i + len(ancre_faits)] + FAIT + src[i + len(ancre_faits):]

io.open(P, "w", encoding="utf-8", newline="").write(src)
print("ECHANGES OK")

P = R + "VERROU.md"
src = io.open(P, "r", encoding="utf-8", newline="").read()

TETE_LIBRE = """| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |"""

old_tete = """| **Auteur** | **Hermes** |
| **Pris le** | 10/11/2026, Tour 135 |
| **Écrit dans** | `bilan_economique.html`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md` |
| **Version visée** | 4.152.0 |
| **Sujet** | Vue plaquette globale (spec `SPEC_VUE_PLAQUETTE_GLOBALE_2026-11-10.md`) : usages par ISO + extrapolation prospective à trois leviers, dans le Catalogue, le Plan et « Ailleurs dans l'usine ». |"""
for a in (old_tete, old_tete.replace("\n", "\r\n")):
    if a in src:
        src = src.replace(a, TETE_LIBRE, 1)
        break
else:
    raise SystemExit("tête du verrou introuvable")

LIB = """✅ **Verrou pris puis libéré par Hermes le 10/11/2026** (Tour 135, branche `ux-rail`, v4.152.0 —
vue plaquette globale : usages par ISO, extrapolation à trois leviers, trois écrans). 811 tests | 0 échec.
**DEV déployée et vérifiée curl ; PROD : rien — attend la phrase de Benjamin.**

"""
ancre = "✅ **Verrou pris puis libéré par Hermes le 10/11/2026** (Tour 134"
i = src.find(ancre)
assert i > 0, "entrée Tour 134 introuvable dans VERROU"
src = src[:i] + LIB + src[i:]

io.open(P, "w", encoding="utf-8", newline="").write(src)
print("VERROU libéré")
