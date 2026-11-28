# BRIEFING pour SeptFons-Dev — Intégration des temps de coupe EMAG 1 / DV 304x28 RPE dans bilan_economique.html

> Rédigé le 26/11/2026 par Gemini (TIMON) sur demande directe de Benjamin Rouquette.
> Concerne : Mise à jour de `bilan_economique.html` avec les temps de coupe machine issus des programmes CN du DV 304x28 RPE sur EMAG 1.

---

## 1. Contexte & Fichiers livrés

Matis a transmis les 8 programmes CN de la gamme complète EMAG 1 pour le disque **DV 304x28 RPE**.
Ils ont tous été rangés dans `Programmes/EMAG1 - 304x28/` :
- OP10 : `L110_1_CBN.SPF` (canal 1 / gauche), `L110_2_CBN.SPF` (canal 2 / droite)
- OP20 : `L120_1.SPF` (canal 1 / gauche), `L120_2.SPF` (canal 2 / droite)
- OP30 : `L130_11_S.SPF` (canal 1 / gauche), `L130_12_S.SPF` (canal 2 / droite)
- OP40 : `L140_1.SPF` (canal 1 / gauche), `L150_1.SPF` (canal 2 / droite — nommé 50_1 sur machine, confirmé par Matis)

Les calculs de coupe ont été réalisés via `scripts/spf_temps.py` et le script dédié mis à jour [scripts/recap_emag1_304.py](file:///C:/Users/Admin/Desktop/Stellantis_SeptFons/scripts/recap_emag1_304.py).
Livrables générés :
- Classeur Excel complet : [Programmes/RECAP_TEMPS_COUPE_DV304_EMAG1.xlsx](file:///C:/Users/Admin/Desktop/Stellantis_SeptFons/Programmes/RECAP_TEMPS_COUPE_DV304_EMAG1.xlsx)
- Données JSON : [Programmes/temps_coupe_DV304_EMAG1.json](file:///C:/Users/Admin/Desktop/Stellantis_SeptFons/Programmes/temps_coupe_DV304_EMAG1.json)
- Format import fusion : [IMPORT_EMAG1_304.json](file:///C:/Users/Admin/Desktop/Stellantis_SeptFons/IMPORT_EMAG1_304.json) (mis à jour avec les 4 OP et les outils réels)
- Standalone : [conditions_coupe_standalone.html](file:///C:/Users/Admin/Desktop/Stellantis_SeptFons/conditions_coupe_standalone.html) (enrichi des presets OP10 et OP40)

---

## 2. Synthèse des valeurs de temps de coupe à intégrer dans le modèle

### Règle d'intégration (identique à EMAG 1 356 et EMAG 2)
- Référence de base : **Côté 1 (gauche)**, avec prise en compte du poste validé pour les essais.
- Pour l'OP30 : temps unitaire du foret multiplié par le nombre de trous (×5 pour T532S, ×3 pour T533S).
- Pour l'OP40 T549 : sur le côté 1, 7,99 s de surfaçage sont hors balise `M870` en raison d'un placement tardif du code M sur la machine. Le temps de coupe réel physique est de **13,89 s** (5,90 s surveillé + 7,99 s avant M870). Côté 2 est à **12,03 s** (entièrement sous M870).

### Détail par logement

#### OP10 (Total coupe : 25,44 s)
| Outil | Logement | Opération | Conditions dominantes | Temps de coupe (s) |
| :--- | :--- | :--- | :--- | :---: |
| **T511** | D1 | Chanfrein alésage / face (S-Platte R1.6) | G96 Vc 900 · f 0,55 | **2,21** |
| **T511** | D2 | Ébauche Ø intérieur (C-Platte R1.6) | G96 Vc 650 · f 0,45 | **3,33** |
| **T513** | D2 | Ébauche grande face et Ø int (C-Platte R1.6) | G96 Vc 750 · f 0,55 | **8,61** |
| **T513** | D1 | Dégagement bol / épaulement (C-Platte R1.6) | G96 Vc 600 · f 0,35 | **7,76** |
| **T515** | D2 | Ébauche intérieure (S-Platte R1.6) | G96 Vc 900 · f 0,45 | **0,93** |
| **T515** | D1 | Ébauche intérieure (S-Platte R1.6) | G96 Vc 900 · f 0,55 | **2,60** |
*(Note : les plans mentionnaient parfois T517, le programme tourne bien avec T515).*

#### OP20 (Total coupe : 30,98 s en C1 / 36,65 s en C2)
| Outil | Logement | Opération | Prod C2 (Vc 800) | Essai validé C1 (Vc 1500) |
| :--- | :--- | :--- | :---: | :---: |
| **T521** | D1 | Chanfreins haut et bas (SNMX SL506) | 2,35 s (Vc 800) | **1,17 s** (Vc 1500) |
| **T521** | D2 | Ébauche Ø extérieur (SNMX SL506) | 8,15 s (Vc 800) | **3,66 s** (Vc 1500) |
| **T523** | D1 | Ébauche face (C-Platte R1.6) | 5,39 s (Vc 850) | **5,39 s** (Vc 850) |
| **T523** | D2 | Ébauche face int. / congé (C-Platte R1.6) | 1,77 s (Vc 650) | **1,77 s** (Vc 650) |
| **T525** | D1 | Gorge isolation thermique (RCGX 09, R4,76) | 9,13 s (Vc 500) | **9,13 s** (Vc 500) |
| **T527** | D1 | Finition bol / face (C-Platte R1.6) | 5,90 s (Vc 750) | **5,90 s** (Vc 750) |
| **T527** | D2 | Finition fond de gorge (R-Platte R4) | 3,97 s (Vc 750) | **3,97 s** (Vc 750) |

#### OP30 (Total coupe : 9,07 s)
| Outil | Logement | Opération | Conditions dominantes | Nb trous | Temps total (s) |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **T532S** | D1 | Foret carbure monobloc D13,1 | G97 2500 tr/min · f 0,40 | 5 | **6,15** (5 × 1,23 s) |
| **T533S** | D1 | Foret D8,6 | G97 3700 tr/min · f 0,40 | 3 | **2,92** (3 × 0,97 s) |

#### OP40 (Total coupe réelle : 20,56 s en C1 / 18,94 s en C2)
| Outil | Logement | Opération | Conditions dominantes | Temps Côté 1 (s) | Temps Côté 2 (s) |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **T543** | D2 | Finition alésage D71,05 | G96 Vc 650 / 600 · f 0,45 | **0,92** | 0,97 |
| **T543** | D1 | Finition face / chanfrein | G96 Vc 650 / 600 · f 0,25 | **4,16** | 4,37 |
| **T546** | D1 | Finition rayon R8 | G96 Vc 800 · f 0,50 | **1,59** | 1,57 |
| **T549** | D1 | Finition pistes ventilés (straddle) | G96 Vc 650 (C1) / 750 (C2) · f 0,35 | **13,89\*** | **12,03** |
*\*dont 7,99 s de coupe réelle exécutée avant la balise M870 (à corriger sur la machine).*

---

## 3. Ce que SeptFons-Dev doit faire dans `bilan_economique.html`
1. Prendre le verrou (`VERROU.md`).
2. Mettre à jour les temps de coupe de référence de la référence `304x28 RPE` sur EMAG 1.
3. Si un incrément de version est prévu, respecter la règle du gel (demander validation Benjamin).
4. Passer le harnais (`python build_harness.py` puis `node ...`) pour vérifier que les 1 037 tests restent verts.
5. Libérer le verrou.

---

## 4. Email préparé pour Matis
Le projet de mail complet est rédigé dans [EMAIL_MATIS_2026-11-26_programmes_304.md](file:///C:/Users/Admin/Desktop/Stellantis_SeptFons/EMAIL_MATIS_2026-11-26_programmes_304.md).
