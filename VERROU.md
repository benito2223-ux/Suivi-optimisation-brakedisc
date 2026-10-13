# VERROU — qui travaille sur `bilan_economique.html` en ce moment

> **But** : empêcher deux sessions d'écrire dans le même fichier en même temps. C'est la
> seule règle qui protège le reste : tout le travail d'octobre dernier tient dans ce
> fichier, et une collision silencieuse le corrompt sans laisser de trace.
>
> **Le principe** : si cette ligne est vide, personne ne travaille sur le code. Si
> elle est remplie, **personne d'autre ne touche au fichier** jusqu'à la libération.

---

## Verrou actuel

| | |
|---|---|
| **Auteur** | Z Code |
| **Pris le** | 13/10/2026 nuit (2) |
| **Écrit dans** | `bilan_economique.html` |
| **Version visée** | 4.84.0 |
| **Sujet** | Simulateur : export Excel (CSV-FR, BOM + sep=; — zéro SDK) + plein écran (CSS maxi + Fullscreen API). L'accueil : avis rendu (export à dessiner au prochain tour, §3.4). |

🔒 **Verrou pris par Z Code le 13/10/2026 nuit (2)** (tour 67, v4.84.0 — export + plein écran du simulateur).

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 66 bis, v4.83.1). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `d90a2d4a…` : libellés ISO
par article dans le simulateur, budget outillage annuel par référence (volume,
€/an, % du budget), clé de regroupement par référence = l'ID (268x12 sur deux
machines), `TOOL_VERSION = "4.83.1"`, NOUVEAUTES + CHANGELOG. Contre-regard :
clé par nom ré-injectée → **vue** (attribution mentie vue par la porte) →
restaurée par copie, empreinte identique, 518/518 verts. Deux attentes de tests
corrigées avant le vert (usages sans volume = présents à coût nul).
**Déployé sur Projet, vérifié curl ; la PROD attend la phrase de Benjamin.**
Écrits : `bilan_economique.html`, `outils/patch_4831.py`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 66, v4.83.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `4e2362e6…` :
`reattribuerEssai()` (bouton ⇄, même OP, essai entier, origine tracée, backup)
et le simulateur `plaquettesCommunes()` (panneau 💰 Simulateur prix, MABEC
regroupés multi-lignes, baisse %, économie €/an et % global, SIMULATION,
réfs sans volume nommées), portes de clic, `TOOL_VERSION = "4.83.0"`,
NOUVEAUTES + CHANGELOG. Contre-regard **deux fautes, deux portes** (assert) :
vues toutes les deux, restauration par copie, empreinte identique, 515/515
verts. **Déployé sur Projet, vérifié curl ; la PROD attend la phrase de
Benjamin.** Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 65, v4.82.0). Pendant le tour,
`bilan_economique.html` est passé à l'empreinte `904c7196…` : les 8 champs date
bornés (min 2025 / max 2035), les pastilles d'axes PAR ESSAI dans le panneau
atelier (`axesActifs()` pure + état de session, config du scénario intacte),
`TOOL_VERSION = "4.82.0"`, NOUVEAUTES + CHANGELOG. Un accroc assumé : le
remplacement global des bornes avait corrompu le sélecteur CSS
(`input[type="date" min=…]`) — réparé, et la porte hors-suite lit désormais le
fichier réel pour l'empêcher de revenir. Contre-regard **deux fautes, deux
portes** (assert) : vues toutes les deux, restauration par copie, empreinte
identique, 502/502 verts. **Déployé sur Projet, vérifié curl ; la PROD attend
la phrase de Benjamin.** Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 63, v4.81.2). Pendant le tour,
`bilan_economique.html` est passé à l'empreinte `37e72ddb…` : la branche
« correcteur manquant » (4.74.3) retirée du déclencheur du bandeau
(`detecterOutilsD1D2` ne voit plus que de vrais regroupements),
`compterCorrecteursManquants` supprimé, test 4.74.3 inversé en porte v3
(« un outil propre ne déclenche AUCUNE proposition, la correction n'y change
strictement rien »), `TOOL_VERSION = "4.81.2"`, NOUVEAUTES + CHANGELOG.
Contre-regard : faute ré-injectée **avec assert** → les deux portes v3 tombent →
restaurée par copie, empreinte identique, 499/499 verts. Le fichier v3 réel
(56 scénarios) : 0 regroupement, 0 inversion → **bandeau muet**.
**Déployé sur Projet, vérifié curl ; la PROD attend la phrase de Benjamin**
(en attendant, consigne chez Matis : ne pas cliquer le bandeau — faux positif
sur 4.81.1). Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 12/10/2026** (Tour 62, v4.81.1). Pendant le tour,
`bilan_economique.html` est passé de l'empreinte `c13417e9…` à `77340221…`
(1 404 978 → 1 425 878 octets) : la porte de l'import (`preparerImportDepuis`,
faute `source.livraisons` depuis la 4.53.0 — ReferenceError silencieuse, aucun
import possible par bouton depuis le 29/09), une porte de test, entrée
NOUVEAUTES 4.81.1, `TOOL_VERSION = "4.81.1"`, CHANGELOG. Contre-regard selon
protocole : faute ré-injectée → **vue** par la porte
(`["ReferenceError: source is not defined"]`) → restaurée par copie
sauvegardée, empreinte `77340221…` identique avant/après, 501/501 verts.
Le fichier d'état fusionné réel passe par `preparerImportDepuis` : 10 lignes,
révision 421, T517 D1/D2 avec MABEC. **Déployé sur Projet, vérifié curl ; la
PROD reste en 4.81.0 et attend la phrase de Benjamin — c'est elle qui bloque
l'import du fichier fusionné demain chez Matis.** Écrits pendant le tour :
`bilan_economique.html`, `build_harness.py` (API + `preparerImportDepuis`),
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 12/10/2026** (Tour 61, v4.81.0). Pendant le tour,
`bilan_economique.html` est passé de l'empreinte `6a082cda…` à `c13417e9…`
(1 401 140 → 1 404 978 octets) : `cloudLireTampon()` (lecture légère
`select=modifie_le,modifie_par`), `cloudSync()` réécrit pour ne payer la lecture
lourde que sur décision, 3 portes de test cloud, test « nouveautés » ré-ancré à
`TOOL_VERSION` (il était codé en dur 4.25.0 et se serait périmé seul),
`TOOL_VERSION = "4.81.0"`, NOUVEAUTES + CHANGELOG. Contre-regard selon protocole
(règle cassée → 1 test la voit → restauration par copie, empreinte vérifiée).
**Déployé sur Projet (4.81.0, vérifié curl, identique au local) ; la PROD reste
en 4.80.0 — elle ne bougera que sur phrase de Benjamin.** Écrits pendant le tour :
`bilan_economique.html`, `build_harness.py` (regénéré), `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`. 2resume, proto/ et projet3 non écrits.

✅ **Verrou libéré par Z Code le 02/10/2026** (Tour 56, v4.80.0). Pendant le tour,
`bilan_economique.html` est passé de l'empreinte `afb7aa5d…` à `6a082cda…`
(1 348 004 → 1 401 140 octets) : palette v3.15, angles 3/4 px, Manrope
ré-embarquée, `TOOL_VERSION = "4.80.0"`. Aucun calcul, aucune fonction, aucune
saisie modifiés. Écrits pendant le tour : `bilan_economique.html`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`. Le proto2 et la
prod n'ont pas été touchés (4.58.0 et 2.0 re-vérifiés).

✅ **Verrou libéré par Z Code le 02/10/2026** (Tour 55, proto v2.0). Pendant le tour,
`bilan_economique.html` n'a pas été écrit : son empreinte
`bf2e81a3998d4d9721c728eaaf666d1f7137fe1a5e5ea651440a65ea4eaf97ca` est identique à celle
notée au début. Seuls `proto/`, `ECHANGES.md` et `VERROU.md` ont été écrits.

---

## Comment ça marche

**Avant d'écrire la première ligne de code :**

1. tu remplis le tableau ci-dessus (auteur, heure, fichier, version visée, sujet) ;
2. tu **commites** ce changement — le verrou est donc dans l'historique, visible par tous ;
3. tu n'écris plus dans `bilan_economique.html` tant que le verrou est à toi.

**En fin de tour :**

1. tu vides le tableau (auteur → *(libre)*) ;
2. tu commites ;
3. ton tour est écrit dans `ECHANGES.md`, dans le même commit.

**Si le verrou est pris et que tu dois absolument écrire** : demande à l'autre session
de libérer, ou passe par Benjamin. **Ne contourne pas** — c'est exactement le geste qui a
coûté une session le 29/09.

---

## Pourquoi un verrou et pas une conversation

Parce que « je te préviens que je travaille » repose sur quelqu'un pour le dire, et
quoique quelqu'un oublie — surtout un agent, qui ne « pense pas » à l'étaler. Un fichier
qu'on lit par habitude, ça tient : c'est la première chose qu'on fait au tour.

---

## Variante automatique (proposée, non encore faite)

Le verrou manuel peut être oublié. Une version automatique lèverait deux défauts :

- **empreinte du fichier** : au début d'un tour, on note le SHA-256 de
  `bilan_economique.html` ; en fin de tour, on vérifie qu'il n'a changé que par nous. S'il a
  changé autrement, quelqu'un a écrit hors verrou → on le signale.
- **garde-fou de commit** : un script refuse un commit de `bilan_economique.html` si le
  verrou appartient à quelqu'un d'autre.

À faire quand on aura un vrai besoin — deux sessions qui codent en parallèle sur des
sujets différents. Pas avant : un garde-fou inutilisé est un garde-fou qu'on contourne.
