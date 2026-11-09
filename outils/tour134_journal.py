# -*- coding: utf-8 -*-
"""Tour 134 — ECHANGES (tour + faits extérieurs) et libération du VERROU."""
import io, re

R = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/"

# ── ECHANGES.md ────────────────────────────────────────────────────────────────
P = R + "ECHANGES.md"
src = io.open(P, "r", encoding="utf-8", newline="").read()

TOUR = """### ▸ Tour 134 — 10/11/2026 — **Hermes** (4.151.0 — étape 2 : les conditions de coupe se tapent une fois ; branche `ux-rail`)

Demande Claude Tour 133 (`DEMANDE_ETAPE_2_CONDITIONS_DE_COUPE_A_HERMES_ZCODE.md`) exécutée intégralement, voir CHANGELOG 4.151.0. **Décision assumée (à valider)** : la vitesse G97 se range dans un champ **`sBroche` distinct** (option « mieux » du §3.3) après recensement des lecteurs de `vc` (kvfDe, kappaEffectif, recomputeCycles, verdictParOutil lisent tous du m/min) — ainsi aucun calcul ne peut lire des tr/min comme des m/min, par construction. **Décisions verrouillées respectées** : rangement inchangé (format 8, tout sur le logement), aucune conversion automatique (liste Options → « Conditions de coupe », validation ligne par ligne, valeurs jamais modifiées), rien d'écrasé à l'ouverture d'un scénario divergent. **groupesSimultanes()** remplace les quatre copies locales (cycle 6998, verdict 7500/7528, aperçu 11019 — repères de la demande). **Recette** : 803 tests | 0 échec (+13 étape 2), node --check 6/6, harnais « tout est vert » sur le dist final. **À l'écran** (rev435 local, profil de test isolé) : fiche à groupe simultané = 3 blocs dont la tête « T548 + T549 » (bug « membre → son propre bloc » vu puis corrigé), UNE saisie vitesse 700 propagée aux logements des deux outils avec sauvegarde, ouverture d'un divergent sans aucune écriture (comptage 81 scénarios / 12 essais / 146 relevés stable, scénario identique octet pour octet, taille localStorage inchangée), essai AVEC relevés (12 relevés) : 0 bouton « Aligner », 1 « Nouvel essai avec les conditions actuelles », bandeau passé en information ; fiche à un outil vue (PCI 4). **Limites assumées** : critères 3 et 4 prouvés par les tests unitaires (décocher → 3 groupes ; libellés G96/G97) — à l'écran mon protocole de navigation faisait glisser le contexte d'OP sous le render() global, la mesure directe n'était pas fiable ; comptage sur rev435 (81/12/146) et non sur rev436 (86/16/192, export non présent sur le poste). **Deux décisions en attente** : (1) le libellé « différent sur cet outil » ouvre le champ à la demande — convenu ? ; (2) la liste G96/G97 ne s'affiche que dans Options — faut-il aussi la proposer à l'ouverture d'un scénario concerné ?

### ▸ """

m = re.search(r"### ▸ Tour", src)
assert m, "aucun tour trouvé"
src = src[:m.start()] + TOUR + src[m.start():]

FAIT = """| 10/11 | **DEV + PROD 4.151.0 — étape 2 : les conditions de coupe se tapent une fois** (ordre de Benjamin : « fini tout et déploie en prod et dev je te fais confiance »). | suivi-optimisation-projet.surge.sh · suivi-optimisation-septfons.surge.sh | ✅ curl : DEV et PROD servent 4.151.0, empreinte `83056957…` identique au `dist/` sur les deux domaines, `version.json` = 4.151.0, ECHANGES en 404 ; 803 tests \\| 0 échec + « tout est vert » au harnais sur le dist final (Hermes, Tour 134) |

"""
ancre_faits = "|---|---|---|---|\n"
i = src.find(ancre_faits)
assert i > 0, "table faits introuvable"
src = src[:i + len(ancre_faits)] + FAIT + src[i + len(ancre_faits):]

io.open(P, "w", encoding="utf-8", newline="").write(src)
print("ECHANGES OK")

# ── VERROU.md — libération ─────────────────────────────────────────────────────
P = R + "VERROU.md"
src = io.open(P, "r", encoding="utf-8", newline="").read()

TETE_LIBRE = """| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |"""

old_tete = """| **Auteur** | **Hermes** |
| **Pris le** | 10/11/2026, Tour 134 |
| **Écrit dans** | `bilan_economique.html`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md` |
| **Version visée** | 4.151.0 |
| **Sujet** | Étape 2 — conditions de coupe tapées une fois par groupe simultané ; mode G96/G97 ; l'essai fige ses conditions (demande Claude Tour 133). |"""
assert old_tete in src or old_tete.replace("\n", "\r\n") in src, "tête du verrou introuvable"
for a in (old_tete, old_tete.replace("\n", "\r\n")):
    if a in src:
        src = src.replace(a, TETE_LIBRE, 1)
        break

LIB = """✅ **Verrou pris puis libéré par Hermes le 10/11/2026** (Tour 134, branche `ux-rail`, v4.151.0 —
étape 2 : conditions de coupe par groupe simultané, mode G96/G97, essai figé). 803 tests | 0 échec.
**DEV + PROD publiées sur l'ordre de Benjamin** (« fini tout et déploie en prod et dev ») — voir
ECHANGES, « Faits extérieurs ».

"""
ancre = "✅ **Verrou pris puis libéré par Claude le 09/11/2026** (Tour 133"
i = src.find(ancre)
assert i > 0, "entrée Tour 133 introuvable dans VERROU"
src = src[:i] + LIB + src[i:]

io.open(P, "w", encoding="utf-8", newline="").write(src)
print("VERROU libéré")
