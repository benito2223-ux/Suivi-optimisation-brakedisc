# SPEC — Temps de coupe par logement et intérêt d'un gain de temps (lot 2)

23/11/2026 — Claude, à la demande de Benjamin. **Spécification seulement : aucun code, outil gelé en 4.162.0, rien saisi dans le cloud.**
Sources : programmes `Programmes/Programme DV356x26 EMAG 2/`, calcul `Programmes/TEMPS_COUPE_DV356_EMAG2.md`, lecture du code de `bilan_economique.html` et du cloud `suivi-septfons` (espace `prod`, en lecture).

## 1. But

Partir du temps de coupe pur de chaque logement (calculé depuis le programme), changer les conditions de coupe (Vc, f), et lire :
1. combien de secondes ça change, par logement et par OP ;
2. si ces secondes comptent pour la ligne ou non (goulot).

## 2. Ce que l'outil sait déjà faire (vérifié dans le code)

- Chaque logement porte déjà `vc`, `f`, `tempsCoupe` (s) et `tempsDeplacement` (s, ignoré dans le calcul). Champ « Temps de coupe » dans le bloc du logement.
- Quand **tous** les logements d'une OP ont un temps de coupe, l'outil en tire le cycle de l'OP (somme, groupes simultanés = outil le plus long) et affiche des secondes et une cadence en pièces/heure (`cycleDetailStatus`, `cycleDepuisTempsCoupe`). Sinon il retombe sur l'indice base 100.
- La vue plaquette globale a un levier « temps de coupe cible » (une seule valeur pour tous les usages) et ne chiffre que si le taux horaire de la ligne existe.
- Ligne EMAG 2 : coût horaire **32 €/h** (question D4 : coût complet ou main-d'œuvre seule, pas tranchée).
- Les temps de coupe de EMAG 2 / 356x26 RPI sont **tous vides** aujourd'hui (OP10 à OP40, scénario « Classeur Matis »).

Les outils et logements du scénario « Classeur Matis » collent aux programmes, sauf deux écarts : T548 (voir §4) et les noms OP30 (« Logement 1 » dans l'outil, T533S / T535S dans le programme).

> **Mise à jour du 24/11 :** Benjamin a demandé la saisie sans attendre le lot 2. Les 18 temps du §3 sont dans le cloud de prod (T548 = 21,8 s, simultané avec T549 ; hors-balises dans `tempsDeplacement`), voir `ECHANGES.md`. Le piège du §4.1 s'applique donc : l'écran affiche des cycles de coupe seule tant que le « hors coupe » du §5 n'existe pas. Les moyennes de cycle d'EMAG 2 (59-60 s) portent sur le 356 seul ; T548 travaille en simultané avec T549 (le programme porte `E_STRADDLE` et `CR_BD_THICKNESS`, finition des deux faces ; le nom d'outil est construit avec le numéro de canal) : à faire confirmer par Matis.

## 3. Données de base à saisir (calculées, pas mesurées)

| OP | Outil (outil) | Logement | Programme : Vc (m/min) / f (mm/tr) | Temps de coupe (s) |
|---|---|---|---|---|
| 10 | T517 | D1 | 900 / 0,48 puis 0,25 | 5,2 |
| 10 | T517 | D2 | 900 / 0,43, 0,40, 0,50 | 3,9 |
| 10 | T513 | D2 | 900 / 0,40 | 11,1 |
| 10 | T513 | D1 | 900 / 0,40, 0,50, 0,45 | 4,0 |
| 10 | T519 | D2 | 2200 tr/min fixe / 0,50 | 0,6 |
| 10 | T519 | D1 | 750 / 0,50, 0,40, 0,25 | 4,7 |
| 20 | T521 | D2 | 650 / 0,45, 0,50 (+ temporisations) | 5,5 |
| 20 | T521 | D1 | 800 / 0,45 (+ temporisations) | 2,4 |
| 20 | T529 | D1 | 850 / 0,60 puis 0,40 | 10,3 |
| 20 | T525 | D1 | 600 / 0,25 | 7,9 |
| 20 | T5211 | D1 | 800 / 0,40 | 4,5 |
| 20 | T5211 | D2 | 1498 tr/min fixe / 0,35 | 2,5 |
| 30 | T535 (foret Ø15,3) | Logement 1 | 2400 tr/min / 0,40 — 5 trous | 8,0 |
| 30 | T533 (foret Ø8,6) | Logement 1 | 3700 tr/min / 0,20 — 3 trous | 6,8 |
| 40 | T543 | D1 | 600 puis 700 / 0,30 puis 0,25 | 5,8 |
| 40 | T543 | D2 | 600 / 0,40 | 0,7 |
| 40 | T546 | D1 | 650 / 0,25 | 8,3 |
| 40 | **T549** | D1 | **600 / 0,30** (finition piste, SNGN 090408 R0.8) | **21,8** |

Cohérence vérifiée : l'outil porte déjà Vc 600 et f 0,3 sur la finition piste, comme le programme.

## 4. Pièges à traiter avant de saisir

1. **Le cycle affiché serait faux.** Avec les 18 temps saisis, l'outil afficherait un cycle de 29,5 s (OP10, 122 p/h), 33,1 s (OP20, 109 p/h), 14,8 s (OP30, 243 p/h) et 36,5 s (OP40, 99 p/h), alors que le pupitre affiche 59-60 s. L'outil prend la coupe pour le cycle et ignore tout le reste (rapides, changements d'outil, chargement, attente). Il manque un « hors coupe » par OP.
2. **T548 n'est pas dans le programme de l'OP40** (L140 : T543, T546, T549). Dans l'outil il porte la même plaquette que T549 (Z000 513 527, 8 arêtes, charnière 50). À faire confirmer par Matis : doublon du classeur ou vrai second outil. Tant qu'il est vide, l'outil refuse de calculer le cycle de l'OP40 (règle « tout ou rien »).
3. **Volumes** : EMAG 2 / 356x26 RPI = 127 244 disques en 2025 (48 645 en 2026). Les 223 709 disques utilisés plus haut pour les coûts par disque sont ceux de toute la ligne (330x14, 356x26, DP 290x12).
4. **Les copies d'essai** (ESSAI SL500 G96 S700 F0,25, ESSAI SN60 …) portent leurs propres outils et logements, vides eux aussi : le temps d'un essai doit se déduire de la base, pas se ressaisir.
5. **Plafond de broche (LIMS)** : sur les petits diamètres la vitesse réelle est plafonnée (OP10 : 2300 tr/min, OP20 : 2800, OP40 : 3000). Un Vc programmé plus haut n'y change rien.

## 5. Modèle proposé (lot 2, dans `MoteurLigne`, pas dans la fiche)

- **Temps de coupe** : valeur de base par logement, avec sa source (programme, mesure Montronix). Conditions de base = `vc` et `f` déjà portés par le logement.
- **Hors coupe par OP** (champ nouveau) : cycle propre de l'OP moins la somme des temps de coupe. Le cycle = coupe + hors coupe. Deux nombres distincts par OP : cycle propre (sans attente) et cadence imposée de la ligne.
- **Temps recalculé** pour un essai ou un scénario, sans saisie :
  - passe de face en G96 : t' = t x (f0 x Vc0) / (f1 x Vc1) (exact tant que la broche n'atteint pas LIMS) ;
  - broche fixe (G97) ou perçage : t' = t x (f0 x N0) / (f1 x N1).
- **Intérêt d'un gain**, par OP puis pour la ligne :
  - ligne synchrone (OP en série) : gain utile = le plus petit de (gain de l'OP, écart entre cette OP et la suivante la plus lente). Si l'OP n'est pas la plus lente, le gain utile est nul ;
  - converti en heures par an (volume) puis en € (taux horaire) **seulement si D1 est tranchée** (ligne saturée). Sinon on affiche la capacité libérée, sans euros.
- Une seule fonction de gain (règle du Tour 136) ; `AXES_LIGNE_DANS_FICHE` reste à `false`.

## 6. Exemples calculés sur la finition piste (T549, base 21,8 s)

| Condition | Temps de coupe | Écart |
|---|---|---|
| Base DWG : G96 S600, f 0,30 | 21,8 s | — |
| ESSAI SL500 : G96 S700, f 0,25 | 22,4 s | +0,6 s |
| ESSAI SN60 : G96 S760, f 0,25 | 20,6 s | −1,2 s |
| ESSAI SN60 : G96 S800, f 0,25 | 19,6 s | −2,2 s |
| ESSAI SN60 : G97 S700, f 0,25 | 24,5 s | +2,7 s |

L'essai SL500 à f 0,25 et Vc 700 ne change pas le temps de coupe : l'argument SL500 reste côté outillage. À 32 €/h, 1 s par disque vaut 0,89 ct, soit 35 h et environ 1 130 € par an sur 127 244 disques, mais seulement si l'OP est le goulot.

## 7. Questions ouvertes

- D1, D2, D4 (déjà posées, le lot 2 les attend).
- Note de Benjamin du 23/11 (Dossier de visite) : moyennes de **temps de cycle complet** relevées sur les pupitres : « OP20 70,6 s, OP10 90 s, OP30 82 s, OP40 46 s », puis « EMAG 2 pour comparaison OP40 59 s, OP10 60 s, OP20 60 s ». Précisé le 24/11 : le premier groupe est **EMAG 1, disque 304** (pas le 356). À préciser encore : si les moyennes d'EMAG 2 portent sur le 356x26 seul ou sur toutes les références de la ligne (330x14, 356x26, DP 290x12) ; l'OP30 d'EMAG 2 n'est pas relevée. Sur EMAG 1 / 304 les OP diffèrent beaucoup (90 s contre 46 s) : le pupitre y affiche donc bien des cycles propres, ce qui affaiblit l'hypothèse « cadence imposée » pour EMAG 2 (elle peut aussi être équilibrée par construction). Les deux jeux ne se comparent pas OP par OP : lignes et disques différents.
- T548 : doublon ou second outil ? (Benjamin le demande à Matis.)
- Cycle propre de chaque OP d'EMAG 2 sans attente (Fred, pupitre ou Montronix), pour fixer le hors coupe.

## 8. Conso théorique du DWG sur le 356x26 seul (calculée depuis les données de Matis dans l'outil)

Données du scénario « Classeur Matis » de l'OP40 : plaquette Z000 513 527, 9,56 €, 8 arêtes, charnière 50 pièces par arête, volume 2025 = 127 244 disques.

| Hypothèse | Plaquettes / an | Coût / an | Part du réel EMAG 2 (8 652 €) |
|---|---|---|---|
| T549 seul | 318 | 3 041 € | 35 % |
| T548 et T549 (comme dans l'outil) | 636 | 6 082 € | 70 % |

Le Pareto réel (8 652 €, 905 plaquettes) couvre toute la ligne EMAG 2 ; l'outil ne porte la plaquette DWG que sur le 356x26 (aucune sur 330x14 ni DP 290x12). Selon que T548 est réel, il reste 5 600 € ou 2 570 € à expliquer sur les autres références ou par une charnière réelle sous 50.
En temps de coupe : 50 disques par arête x 21,8 s = 18,1 min de coupe par arête (charnière théorique, pas la durée de vie constatée).

## 9. Correction demandée par Benjamin (24/11) : le bandeau « le scénario a changé »

**Règle voulue** : le bandeau (`paramsDivergences`, sous « Conditions de l'essai ») ne s'affiche que si une valeur **déjà renseignée** a réellement changé ou a été effacée. Passer de vide à renseigné (compléter une donnée) n'est pas un changement et ne déclenche rien.

- Où : la comparaison de la photo de l'essai avec les conditions actuelles (vc, f, charnière, mode, S). Aujourd'hui une valeur vide dans la photo et une valeur dans le scénario donnent « modifié ». À corriger pour que « vide dans la photo » soit toujours ignoré ; valeur dans la photo, vide ensuite = changement (effacement) ; valeur différente = changement.
- Même famille : la tuile d'un essai compare chaque logement à la référence (`ecartsOutilVsReference`) ; un essai à vide face à une référence renseignée y est montré comme écart. À traiter avec la même règle (ou à afficher « non renseigné » plutôt que « modifié »).
- Pourquoi : on complétera les conditions de coupe des postes au fil de l'eau (programmes, relevés) ; chaque complément ne doit pas faire douter de la validité d'un essai figé.
- Taille : une règle de comparaison dans deux fonctions, mais les 951 tests et la porte du lot devront être revus ; pas bloquant, donc **lot 2** (outil gelé en 4.162.0).
