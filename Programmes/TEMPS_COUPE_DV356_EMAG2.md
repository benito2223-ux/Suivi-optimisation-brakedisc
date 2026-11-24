# Temps de coupe par disque — DV356x26, ligne EMAG 2

Calculé le 23/11/2026 depuis les programmes `Programme DV356x26 EMAG 2/` (L110 = OP10, L120 = OP20, L130 = OP30, L140 = OP40).
Script : `scripts/spf_temps.py` ; détail par mouvement : `Programmes/temps_coupe_DV356_EMAG2.json`.

## Méthode et limites

- Temps de coupe = mouvements en avance (G1/G2/G3) entre M870 et M890 (fenêtres Montronix), longueur / (avance x vitesse de broche).
- G96 : vitesse de broche recalculée à chaque diamètre, plafonnée par LIMS (2300 OP10, 2800 OP20, 3000 OP40).
- Temporisations G4 S (tours) dans la fenêtre incluses. Perçages : multipliés par le nombre de trous (5 puis 3).
- **Pas du temps de cycle** : rapides, changements d'outil, chargement, soufflage, indexation C des perçages exclus.
- Logement = D1 / D2 de l'outil dans le programme.
- Non vérifié contre Montronix ni contre un chronomètre.

## Résultats (secondes par disque)

| OP | Outil / logement | Plaquette (programme) | Opération | Coupe (s) |
|---|---|---|---|---|
| 10 | T517 D1 | S R1.6 | ébauche intérieure | 5,2 |
| 10 | T517 D2 | C R1.6 | ébauche intérieure | 3,9 |
| 10 | T513 D2 | C R1.6 | ébauche piste | 11,1 |
| 10 | T513 D1 | C R1.6 | finition appui moyeu | 4,0 |
| 10 | T519 D2 | C R1.6 | alésage moyeu ébauche | 0,6 |
| 10 | T519 D1 | S R1.6 | face arrière moyeu | 4,7 |
| 20 | T521 D2 | S R1.6 | ébauche chanfrein piste, finition D356 | 5,5 |
| 20 | T521 D1 | S R1.6 | finition chanfreins entrée piste | 2,4 |
| 20 | T529 D1 | C R1.6 | ébauche piste (dont 1,8 s de retour à F0.4) | 10,3 |
| 20 | T525 D1 | R R4.76 | Ø ext. moyeu, fond gorge ébauche | 7,9 |
| 20 | T5211 D1 | R1.6 | Ø ext. moyeu finition | 4,5 |
| 20 | T5211 D2 | R R4.76 | fond gorge finition | 2,5 |
| 30 | T535S D1 | foret Ø15,3 | 5 trous (1,6 s/trou) | 8,0 |
| 30 | T533S D1 | foret Ø8,6 | 3 trous (2,3 s/trou) | 6,8 |
| 40 | T543 D1 | T R1.2 | finition chanfrein, face avant | 5,8 |
| 40 | T543 D2 | S R1.6 | alésage moyeu Ø71,095 | 0,7 |
| 40 | T546 D1 | C R1.6 | finition R114 | 8,3 |
| 40 | **T549 D1** | **S R0.8** | **finition piste, 1 passe** | **21,8** |

Totaux : OP10 29,5 s ; OP20 33,1 s ; OP30 14,8 s ; OP40 36,5 s ; **ligne 114,0 s**.
Avances hors fenêtre de surveillance (non comptées) : 2,4 s sur OP10, soit une OP10 entre 29,5 s et 31,9 s selon leur nature :
- T517 D2, `N285 G1 X-79.598 F0.5` : 2,08 s, à Z-13,685, soit 0,2 mm au-dessus de la face usinée à Z-13,9 juste avant. Approche ou petite passe : non tranché.
- T519 D1, `N970` : 0,31 s, retour de 6 mm à F0,5 après l'alésage : très probablement de l'approche.

Vérification croisée (23/11) : un second calcul indépendant du même type (Gemini) retrouve 14,8 s (OP30) et 36,5 s (OP40), 33,1 s (OP20) en comptant G4 S en tours de broche (1,04 s), et 31,9 s pour l'OP10 en comptant les deux avances ci-dessus. Il valide l'arithmétique et la lecture des programmes, pas le temps réel de la machine.

## Temps de cycle relevés sur les pupitres (23/11/2026, Benjamin)

| OP | Cycle pupitre (s) | Coupe calculée (s) | Hors coupe (s) |
|---|---|---|---|
| 10 | 60 | 29,5 | 30,5 |
| 20 | 60 | 33,1 | 26,9 |
| 30 | non relevé (un second « 59 s » reçu sous l'étiquette OP10, lu comme OP30 : à confirmer) | 14,8 | — |
| 40 | 59 | 36,5 | 22,5 |

Trois OP sur quatre affichent 59-60 s alors que leur coupe va de 29 à 37 s : hypothèse (non prouvée) que le pupitre affiche la cadence imposée, attente comprise, et pas le cycle propre de chaque machine. À confirmer : cycle propre sans attente, par OP.

Précisé le 24/11 : les moyennes d'EMAG 2 portent sur le 356 seul, le hors coupe ci-dessus est donc valable pour ce disque (OP10 : 28 à 30 s selon la nature des 2,4 s hors balises ; OP20 : 27 s ; OP40 : 22,5 s ; OP30 non relevée).

**Saisi dans l'outil le 24/11** (cloud de prod, scénario « Classeur Matis », voir `ECHANGES.md`) : les temps de coupe ci-dessus, T548 = 21,8 s comme T549 (simultané, T549 coché « simultané avec le précédent »), et le hors-balises dans « temps de déplacement » (T517 D2 2,1 s ; T519 D1 0,3 s ; T5211 D2 1,8 s ; T549 D1 0,6 s).

## Points à vérifier

- T549 : le programme annonce R0.8 ; l'essai SL500 était en R1.6 (SNGN 090416). Quelle avance a tourné pendant l'essai ?
- Vitesse plafonnée par LIMS sur T517 D2, T513 D1, T519 D1, T5211 D1 : la vitesse de coupe réelle est inférieure à celle programmée.
- T529 : retour de 16,45 mm à F0.4 dans la fenêtre, avec 16 mm d'aller en plus : environ 3,4 s, à confirmer avec un opérateur.
- Durée de vie en minutes : le Pareto donne la conso DWG de toute la ligne EMAG 2 (223 709 disques), alors que ce programme ne concerne que le 356x26 RPI (127 244 disques en 2025). La conso théorique du 356 seul se calcule avec les données de Matis de l'outil : 3 041 €/an avec T549 seul, 6 082 € avec T548 et T549 (voir §8 de `SPEC_TEMPS_DE_COUPE_LOT2_2026-11-23.md`). Avec la charnière théorique de 50 : 18,1 min de coupe par arête.
- Note de Benjamin du 23/11 dans l'outil (Dossier de visite) : moyennes de temps de cycle complet relevées aux pupitres, « OP20 70,6 s, OP10 90 s, OP30 82 s, OP40 46 s », puis EMAG 2 « pour comparaison » OP40 59 s, OP10 60 s, OP20 60 s. Le premier groupe est EMAG 1, disque 304 (précisé le 24/11), pas le 356. Reste à préciser si les moyennes d'EMAG 2 portent sur le 356x26 seul.

## À obtenir pour passer au temps de cycle

- Temps de cycle réels par OP (Fred) et, si possible, l'export Montronix des durées par étape.
- Taux horaire machine.
- Confirmation que la ligne est une chaîne OP10 → OP40, une machine par OP.
