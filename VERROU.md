| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

✅ **Verrou libéré par Hermes le 17/10/2026** (UI 4.97.1 + PROD). Pendant le
tour : la barre d'outils passe de 180 px/3 rangées à **62 px/une ligne** —
icônes 13 px trait 1.7, segmented control pour les 5 écrans, libellés
courts, Exporter/Importer/Verrouiller en icône seule (title au survol),
moreBtn largeur fixe. Piège : wrap fantôme de 77 px sur le parent inline-flex
du ••• (contraint à 31 px). Mobile : boutons 44 px intacts ; débord
horizontal 420 px préexistant (.hd + table, hors périmètre, vérifié stash).
582/0, `node --check` 5/5, capture validée. **PROD** : Success!, md5
`18e46ebe…` identique octet pour octet, TOOL_VERSION 4.97.1 servi.
Écrits : `bilan_economique.html`, `CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 16/10/2026 (soir 2)** (UI 4.97.0, lot 4
« signature Apple » + PROD). Pendant le tour : toolbar sticky translucide
(verre `blur(14px)` + fond 78 %, classe `.is-sticky` au scroll, fallback
`@supports`, print statique — verre sur CETTE barre uniquement), motion
120→180 ms `cubic-bezier(.4,0,.2,1)`, ombres repliées sur `--shadow-card` /
`--shadow-hover` (23 valeurs héritées → 2 étages ; focus/insets/accents
légitimes conservés). Diagnostic documenté : les polices n'étaient pas le
problème. Piège rencontré et contourné : Chrome headless virtual-time gèle
la transition `background` — contre-vérifié sans transition (computed style
`0.78` alpha + `backdrop-filter` actif). 582/0, `node --check` 5/5.
**PROD** : Success!, md5 `54b0bea2…` identique octet pour octet,
TOOL_VERSION 4.97.0 servi. Écrits : `bilan_economique.html`,
`CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 16/10/2026 (soir)** (UI 4.96.1, lots 2+3 +
PROD). Pendant le tour : 20 déclarations `.var(--motion)` invalides réparées
(les hovers conçus v4.70 ne se sont jamais animés — le parser CSS rejetait
la déclaration entière) ; socle de mouvement commun tuiles/scénarios/cartes
avec `prefers-reduced-motion` ; gain annuel acté en gras (chiffre phare
carte atelier) ; refus documenté du cosmetic inutile (999px = pastilles
légitimes, `.btn` n'aurait rien changé). `outils/verif_lot23.js` 5/5,
harnais 582/0, `node --check` 4/4. **PROD sur ordre de Benjamin** :
`suivi-optimisation-septfons.surge.sh` — Success!, HTTP 200, md5
`dc5fe0e2…` identique octet pour octet, TOOL_VERSION 4.96.1 servi,
SW + manifest 200. Écrits : `bilan_economique.html`,
`build_harness.py` (porte 4.96), `outils/verif_lot23.js`, `CHANGELOG.md`,
`VERROU.md`.

✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 73, v4.90.0). Pendant le
tour, les trois lots de la revue Claude sont appliqués : P7 (data-plan
échappé, signe du gain, ordre des boutons, Cadence retiré, taux en état),
P6 (plancher de tailles, token secondaire ≥ 4,5:1, styles inline en
classes), P3 (hypothèse DDV affichée et réglable, seuil de neutralité, prix
SPK en réglage, confirmation case par case, Potentiel), P2 (le Simulateur
partage le basculeur, semaines/an éditable), P4 (dernier export affiché),
P5 (usure en pastilles, conformité en direct, bornes, charnière en 8 mots).
Le fichier est **normalisé LF** (19 719 CRLF) — fin des ancres capricieuses.
P8 : monolithe canonique, archives intactes (décision déléguée). 521 →
**552/552 verts**. Contre-regards vus. **Déployé sur Projet, vérifié curl ;
la PROD attend la phrase de Benjamin.** Écrits : `bilan_economique.html`,
`outils/patch_4900_v2.py`, `outils/tour73_journal.py`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`, `AUDIT_CLOUD_RLS.md`.

🔒 **Verrou pris par Z Code le 14/10/2026 soir** (tour 73, v4.90.0 — les suggestions à la saisie).✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 72, v4.89.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte post-patch : les
suggestions à la saisie (`catalogueSuggestion()`, `catalogueParIso()`,
`appliquerSuggestionCatalogue()` — pures et exportées), datalists natifs
`catMabec`/`catIso` alimentés au démarrage et aux changements du catalogue,
attributs `list=` sur les champs MABEC/ISO du logement, crochet dans
`writeFieldValue` (la branche logement), `TOOL_VERSION = "4.89.0"`,
NOUVEAUTES + CHANGELOG. Contre-regard : la porte initiale était aveugle
(logement déjà aux valeurs du catalogue) — **renforcée** (ISO manuel
DIFFÉRENT doit rester), faute injectée → **vue** → restaurée par copie,
empreinte identique, 521 → **551/551 verts**. **Déployé sur Projet,
vérifié curl ; la PROD attend la phrase de Benjamin.** Écrits :
`bilan_economique.html`, `outils/patch_4890_a.py`, `outils/verrou_t72.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

🔒 **Verrou pris par Z Code le 14/10/2026 soir** (tour 73, v4.90.0 — les suggestions à la saisie).✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 71, v4.88.0 — verrou pris
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

**Verrou libere par Z Code le 14/10/2026** (Tour 69, v4.86.0). Pendant le
tour, `bilan_economique.html` est passe a l'empreinte `ac9563a1...` : le Plan
de conversion (cibles SPK editables, auto-suggestion KY3500 -> LKT640 a 5 EUR,
etats step-by-step de Benjamin, total = lignes etatees seulement, gain =
plaquettes/an x ecart de prix, persistant dans le suivi, export CSV), portes,
`TOOL_VERSION = "4.86.0"`, NOUVEAUTES + CHANGELOG. Contre-regard : potentiel
compte comme promesse -> **vu** -> restauration par copie, empreinte
identique, 521 -> **542/542 verts**. Le tour des echappements consigne :
patchs par fichiers, heredocs bannis. **Deploye sur Projet ET en prod
(phrase de Benjamin : « fonce pour le Plan de conversion et deploie en
prod »), verifies curl — empreinte ac9563a1 identique aux deux domaines.**
Ecrits : `bilan_economique.html`, `outils/patch_4860_a/b/c.py`,
`outils/fix_plancsv*.py`, `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`,
`VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 68, v4.85.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `90ae73b6…` : le
catalogue plaquettes (persistant dans le suivi, seed par MABEC avec prix
fréquent et divergences signalées, propagation avec rapport, CSV standalone
aller-retour tolérant), panneau 📚 + porte de clic, `TOOL_VERSION = "4.85.0"`,
NOUVEAUTES + CHANGELOG. Le tour des guillemets : trois défauts attrapés par
le harnais avant livraison (apostrophe JS, ligne d'en-têtes cherchée, champs
quotés découpés proprement). Contre-regard : propagation muette → **vue** →
restauration par copie, empreinte identique, 521 → **533/533 verts**. Sur la
v5 réelle : 25 articles, 9 divergences pour Matis, le 137 021 porte déjà
LKT640 ET KY3500. **Déployé sur Projet, vérifié curl ; la PROD attend la
phrase de Benjamin.** Écrits : `bilan_economique.html`,
`outils/patch_4850_a/b/c.py`, `outils/fix_apostrophe.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 67, v4.84.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `55f32d76…` :
`simulCSV()` (CSV-FR : BOM + sep=; + décimales à virgule, deux tableaux,
export par Blob/ObjectURL), bouton ⤵ Exporter, ⛶ plein écran (CSS maxi +
Fullscreen API), **le bloc CSS du simulateur enfin inséré** (il manquait
DEPUIS LA 4.83 — garde conditionnel trop malin, insertion sautée en silence ;
porte hors-suite : 4 règles lues dans le fichier réel), la porte honnête du
66 bis remise (la restauration par copie avait rejoué une copie périmée),
`TOOL_VERSION = "4.84.0"`, NOUVEAUTES + CHANGELOG. Contre-regard : `sep=;`
faux → **vue** → restauration par copie **fraîche**, empreinte identique,
518 → 521/521 verts. **Déployé sur Projet, vérifié curl ; la PROD attend la
phrase de Benjamin.** Écrits : `bilan_economique.html`, `outils/patch_4840.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

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
