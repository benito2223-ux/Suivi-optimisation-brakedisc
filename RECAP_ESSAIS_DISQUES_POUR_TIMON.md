# RECAP — Essais sur disques de frein (Sept-Fons) — pour TIMON AI

> Écrit le 26/11/2026 par Claude, sur demande de Benjamin. **Lecture seule** : rien n'a été modifié dans l'outil ni dans le cloud.
> Source : base cloud PROD `suivi-septfons` (Supabase `cxjfyaorkkxemjnollnj`, table `sync_shards`, shards `sc:*`), lue le 26/11/2026.
> Auto-contenu. Langue de travail avec Benjamin : français (dictée vocale, il attend une direction assumée).
> Règles à garder : jamais K ni P_req en sortie visible ; nuances toujours en noms SPK (SL500, SL506…) ; l'outil = « Field Operations Suite » dans toute communication externe.

## 1. En une phrase

Depuis août, la plaquette **SNGN 090416 F SL500 (arête vive, rayon 1,6)** a été essayée sur 4 lignes contre les plaquettes en place
(KY3500 wiper DWG1743941R01, CBN, SN60). Résultat net : elle **tient 50 pièces sur EMAG 1 OP40 mieux que le process actuel**, mais
**perd contre le wiper sur HESSAPP OP30**, où la rugosité dérive à cause d'une usure en peigne + cratère.

## 2. Tableau des essais (par ligne / opération)

| Date | Ligne · réf · OP | Plaquette essayée | Conditions | Résultat | Statut / clôture |
|---|---|---|---|---|---|
| 25/08 | EMAG 1 · 356x26 RPI · OP10 | Céramique intégrale LKT640 | Vc 700 · f 0,35 · charnière 150 | Battement 0,03 à 0,09 mm sur 150 pièces, stable | **Validé** |
| 26/08 | EMAG 1 · 356x26 RPI · OP10 | Mixte T50013 (bol CBN + piste céramique) | Vc 700 · f 0,35 · 150 | 1 seul relevé (0,09 mm à 150) | En essai, incomplet |
| 26/08 | EMAG 1 · 356x26 RPI · OP10 | Process actuel CBN | Vc 900 · f 0,5 · charnière 75 | 1 seul relevé (0,10 mm à 75) | Validé (référence) |
| 22/09 | EMAG 1 · 356x26 RPI · OP40 | **Process actuel KY3500 wiper (référentiel)** | Vc 650 · f 0,25 · charnière 30 | Ra 5,8 à 12,5 µm, **hors tolérance avant 30 pièces**, « Ra très élevé dès les premières pièces » | Série, clôturé hors tolérance |
| 22/09 | EMAG 1 · 356x26 RPI · OP40 | **SNGN 090416 F SL500** | Vc 700 · f 0,25 · charnière 50 | T548 : 9,8 → 4,3 → 6,5 µm ; T549 : 2,7 → 7,7 → 9,3 µm sur 50 pièces ; « usure en peigne (fonte fraîche) » | Essai, fin de charnière |
| 13/10 | PCI 5 · DV 304x28 RPE · OP40 | Référence KY3500 1743941 | — | Battement 0,009 à 0,024 mm (6 relevés, 22 pièces) | Série, clôturé « casse » |
| 13/10 | EMAG 2 · 356x26 RPI · OP40 | Référentiel (SNGN090408F KY3500) | — | 16 relevés **sans valeur lisible** | Série, clôturé « casse » |
| 14/10 | EMAG 2 · 356x26 RPI · OP40 | **SNGN 090416 F SL500**, G96 S700 | f 0,25 · charnière 50 | Battement 0,02 à 0,04 mm sur 50 pièces, « se comporte bien, peut faire plus » | Essai, OK |
| 14/10 | EMAG 2 · 356x26 RPI · OP40 | SNGN 090416 **SN60**, G96 S800 | f 0,25 | **Vibration dès la pièce 5** | Clôturé hors tolérance |
| 14/10 | EMAG 2 · 356x26 RPI · OP40 | SNGN 090416 SN60, G96 S760 | f 0,25 | Vc baissée pour casser la vibration : **sans effet** | Clôturé, vibration |
| 14/10 | EMAG 2 · 356x26 RPI · OP40 | SNGN 090416 SN60, **G97** S700 | f 0,25 | Pièces vibrées à partir de la 5e | Clôturé, vibration |
| 02/11 | PCI 4 · 268x12 · OP40 | SNGN 090416 F SL500 | charnière 150 | Charnière menée à terme ; **la bavure sur le diamètre de centrage subsiste** ; pas de gain de qualité | Essai terminé |
| 09/11 | HESSAPP · 302x26 RPI · OP30 | **SNGN 090416 F SL500** (T5 et T6) | Vc 675 · f 0,32 · charnière 50 | Ra 2,4 → **14,1 µm à 50 pièces** (T5) ; 2,8 → 9,2 µm (T6) | **Abandonné, hors tolérance** |
| 10/11 | EMAG 2 · 356x26 RPI · OP40 | SNGN 090416 F SL500, G96 S700 (reprise) | f 0,25 · charnière 50 | Battement 0,010 → 0,029 mm à 60 pièces ; **Ra 13, usure en peigne, VB importante, pas d'écaillage** ; pièces chaudes (grenaillage récent) | Clôturé hors tolérance |

Référence historique HESSAPP OP30 (23/09, wiper KY3500, Vc 650 · f 0,25) : Ra 2,3 à 3,3 µm jusqu'à 40 pièces, puis 4 à 7 µm, 90 pièces tenues,
talon en début de piste intérieure à partir de la pièce 50.

## 3. Ce qu'on a appris

1. **Dépend de la ligne, pas seulement de la plaquette.** Le même wiper KY3500 à 650 / 0,25 donne Ra 6 à 12 µm sur EMAG 1 et 2 à 7 µm sur HESSAPP.
   Un résultat obtenu sur une ligne ne se transpose pas à une autre sans essai.
2. **Sur EMAG 1 OP40, la SNGN SL500 bat le process actuel** (Ra 3 à 9 µm sur 50 pièces contre 6 à 12,5 µm hors tolérance en 30 pièces).
3. **Sur HESSAPP OP30, la SNGN perd contre le wiper.** À Vc 675 / f 0,32, la SNGN part au niveau du wiper (2,4 à 2,8 µm) puis dérive d'environ 0,2 µm par pièce
   (≈ 45 pièces avant 12 µm sur T5), tandis que le wiper plafonne. Constat visuel de Benjamin : **usure pure, peigne + cratère**.
4. **Pourquoi (hypothèse de travail, à confirmer par VB)** : avec l'arête vive, la surface est générée par le seul rayon de bec, donc le peigne et le cratère
   s'impriment directement. Le wiper (méplat 0,5 mm pour f = 0,32, soit un rapport d'environ 1,6) re-lisse derrière lui et cache l'usure.
   L'usure de l'arête est peut-être comparable, c'est sa transmission au Ra qui diffère. Si c'est confirmé, aucun réglage de Vc ou f ne rattrape le wiper sur la durée de vie.
5. **Coût par pièce.** Wiper KY3500 : 9,56 €, 8 arêtes, charnière visée 150, soit environ 0,008 € la pièce. SNGN SL500 : 8,5 €, 8 arêtes, 45 à 60 pièces utiles, soit environ 0,02 € la pièce.
   Il faudrait à peu près tripler la durée de vie pour égaler le wiper.
6. **SN60 en arête vive : vibration systématique dès 5 pièces** à Vc 700 à 800, en G96 comme en G97. Baisser la vitesse ne règle rien. Piste fermée sur EMAG 2.
7. **Le wiper a une marge que la SNGN n'a pas** : méplat 0,5 mm, donc possibilité de monter l'avance vers 0,40-0,45 sans perdre le Ra, avec gain de temps de cycle.
8. **PCI 4** : la SNGN n'a pas supprimé la bavure du diamètre de centrage. Piste notée par l'opérateur : plaquette CeramTec triangulaire pour l'appui moyeu.
9. **Fonte et chaleur.** Peigne observé sur fonte fraîche (22/09, bruts de 2 jours) et sur pièces chaudes après grenaillage (10/11). Fonte de 5 jours au 09/11 : le chill n'est donc pas le suspect principal sur HESSAPP.

## 4. Questions encore ouvertes

- **Aucune mesure de VB** sur les essais. C'est le test qui tranche entre « la SNGN s'use autant que le wiper » et « elle s'use plus vite ». À faire après 60 pièces, SNGN et wiper côte à côte, mêmes conditions.
- **Pas d'essai wiper à 675 / 0,32 sur HESSAPP** : la baseline a été relevée à 650 / 0,25, donc la comparaison du 09/11 n'est pas strictement iso-condition.
- **Leviers non testés** : Vc vers 600, f vers 0,40-0,45 sur la SNGN, arrosage ou non (peigne possible par fatigue thermique), une plaquette par piste en inversant T5 et T6 (T5 et T6 divergent de 14 contre 9 µm à conditions identiques, l'effet piste est mélangé à l'effet plaquette).
- **Tolérance Ra configurée à 12 µm** dans l'outil sur ces OP : à faire confirmer par Benjamin ou Matis (elle semble élevée pour une piste de frottement).

## 5. Problèmes de saisie dans l'outil (à corriger avant tout rapport client)

1. **Références de plaquettes périmées dans les essais.** Les essais du 22/09 (EMAG 1 OP40, scénario « SNGN 090416-F SL500 ») et du 09/11 (HESSAPP, T5 et T6) affichent encore « DWG1743941R01 KY3500 » dans leurs paramètres, alors que les plaquettes réellement montées sont des SNGN SL500. Benjamin confirme : **T5 et T6 sont montés en SNGN SL500, arête vive, rayon 1,6**.
2. **f et Vc du 09/11** : l'outil dit Vc 675 · f 0,32 pour T5 et T6. Benjamin avait parlé de F 0,35 dans son premier message, puis a précisé que l'avance du wiper est 0,32 et que **0,5 mm est la longueur du méplat**. À confirmer pour la SNGN.
3. **Maturité des bruts vide** sur l'essai du 09/11 (fonte de 5 jours d'après Benjamin).
4. **Doublons EMAG 1 OP40** : « Classeur Matis » et « Process actuel finition piste » contiennent le même essai (mêmes valeurs).
5. **EMAG 2 OP40** : relevés présents mais valeurs absentes sur l'essai du 13/10 (16 relevés), sur T549 de l'essai du 14/10 et sur les trois essais SN60. L'essai 2 du 10/11 n'a de valeurs que pour T548 (le critère Ra n'y est pas saisi alors que la clôture parle de « Ra 13 »).
6. **Motifs de clôture incohérents** : « casse » est utilisé pour des fins de charnière normales (PCI 4, PCI 5) alors qu'il n'y a pas eu de casse documentée.
7. **Référentiel EMAG 2 OP40 du 13/10** : date de fin saisie « 0002-10-13 » (erreur d'année).

## 6. Ce que je ferais ensuite (direction proposée)

1. **Corriger la saisie** (point 5 ci-dessus), surtout les références SL500 et la maturité 5 jours. Sans ça, le rapport d'essai affiche des plaquettes fausses.
2. **Faire l'essai de mesure VB** sur HESSAPP OP30 : SNGN contre wiper, Vc 675 · f 0,32, même fonte, une plaquette par piste puis inversion, VB relevé aux pièces 20, 40, 60.
3. **Selon le VB** : si l'usure est comparable, arrêter de chercher à égaler le wiper sur HESSAPP et garder la SNGN pour les lignes où elle gagne (EMAG 1 OP40). Si la SNGN s'use nettement plus, tester Vc 600 puis f 0,40.
4. **Ne pas lancer de nouvel essai SN60** en arête vive sur EMAG 2 (vibration prouvée).

## 7. Où retrouver les données

- Cloud PROD : table `sync_shards`, espace `prod`, `kind = 'sc'`, id `sc:<id_op>:<id_scénario>`. Opérations concernées : `o-EMAG1-356X26RPI-OP10`, `o-EMAG1-356X26RPI-OP40`, `o-EMAG2-356X26RPI-OP40`, `o-HESSAPP-302X26RPI-OP30`, `o-PCI4-268X12-OP40`, `omv6f3fhyoltz` (PCI 5 OP40).
- Export local le plus récent : `SuiviOptimisation_rev435_20261109-1000.json` (antérieur à l'essai HESSAPP du 09/11 après-midi : ne pas s'y fier pour cet essai).
- Rapport d'essai EMAG 1 OP40 du 22/09 : `Downloads/Rapport_essai_SNGN_090416_F_SL500_Essai_1_20261109.html`.
