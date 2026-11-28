# Résultats d'essais — Sept Fons (historique consolidé)

**Objet.** La mémoire unique des essais terrain Sept Fons, en un fichier.
Elle sert à trois choses :

1. **Historique personnel de Benjamin** — une fiche par essai, récent → ancien.
2. **Source des skills** (`usinage-fonte-ceramique` → `references/fonte/`,
   `ceramic-cutting-references` → `sept-fons-field-tests-log.md`,
   `sept-fons-salesforce-reports`) : toute conclusion actée ici finit dans la
   skill correspondante.
3. **Rattachement à l'outil** : chaque essai est identifié par les mêmes clés
   que le suivi — **ligne / référence disque / OP / date**. Depuis la v4.146
   (09/11/2026) les essais sont enregistrés dans l'outil avec conclusion
   d'essai et logement (v4.147 : les relevés suivent leur logement) ; cette
   fiche en est la lecture consolidée, pas un doublon.

**Périmètre.** Essais Sept Fons uniquement (lignes EMAG, PCI, WEISSER,
HESSAPP — disques de frein GJL). Les essais clients aéronautiques (Inconel,
TOS 2000…) et SMTG restent dans le log skill `ceramic-cutting-references`.

---

## Règles actées (protocole permanent)

- **Protocole 5×** (accord Matis Hernu & Arthur Alves, sept. 2026) : tout essai
  concluant est répété 5 fois ; validé 5× + économiquement rentable →
  production, sauf force majeure (ex. code MABEC) avec justification écrite.
- **Optimisation OP par OP** sur EMAG 1 (scope convenu avec Arthur).
- **Ra non contrôlé sur EMAG 1** (rugosimètre en panne) → mesures Ra sur la
  ligne PCI (étape 3) avec Matis ; référence = lot de 30 disques aux conditions
  courantes avant toute comparaison.
- **Battement** : tolérance de référence 0,12 mm.
- **Une variable à la fois par essai** ; lot dégradé ne juge jamais une
  géométrie ni une nuance.
- **Champ `brut` proposé dans l'outil** (Tour 68, non encore codé) :
  `brut: {statut: sain|degrade|inconnu, peauHB, lot}` — la qualité du brut est
  une propriété de la campagne d'essai, saisie à réception. Le grenaillage est
  une variable de premier ordre depuis le 14/10.

---

## Les essais (récent → ancien)

### 2026-11-26 — PCI · 268x12 · chaîne sur-épaisseurs + correction programme finition pistes (S=500)

- **Chaîne de passes** : brut **17 mm ±0,3** → OP10 **15 mm** → OP20 **13 mm** → OP40 **12 mm ±0,1** (5 mm enlèvement total).
- **⚠ Correction Julien (26/11)** : le programme transmis donnait S=400 sur la finition des pistes — la vraie valeur est **S = 500 tr/min** → à Ø 268, Vc ≈ 421 m/min (à recalculer au Ø piste réel). Toute analyse fondée sur S=400 est à refaire.
- **Status** : données de référence, pas un essai.

### 2026-11-16 — EMAG 2 · OP20 gorge plongée · DV356x26 RPI · RCGX 090700 T03030 SL500 — sujet ouvert : usure abrasive saine, écart charnière 300/150 jamais creusé

- **Contexte** : action « Follow the RCGX 090700 » du rapport de visite 9-10/11. Même article aux deux logements (Z000 544 318, 13,67 €, 2 arêtes) : **T5211 D1 charnière 300 vs T525 D1 charnière 150** — écart ×2 d'origine **historique, jamais creusé**. Vc/f **non relevés** (champs vides dans l'outil rev435) ; extraction du programme 356 déjà chez Matis.
- **Photo Carson 16/11** : bande de dépouille polie régulière, film fer/graphite adhéré, **zéro écaillage, zéro notch** → usure **abrasive+adhésive**, rien de mécanique. L'arête atteint sa charnière de façon régulière (fiabilité déjà là).
- **Enjeu** : ~**8,7 k€/an** si le 150 rattrape le 300 (127 244 p/an) — sous condition de géométrie des deux gorges.
- **Prochaine étape** : relevé conditions + géométrie des deux gorges (Matis) → saisie outil → calcul interne comparé des deux logements → essai une variable (candidat : dégraissage 2 plongées). Objectif posé « comprendre d'abord, objectif ensuite ». Status : **ouvert**.

### 2026-11-10 — EMAG 2 · OP40 finition piste · DV356x26 RPI · SL500 SNGN 090416F « Essai 2 » — brut frais : la maturité mange la marge Ra

- **Conditions** (vérifiées dans l'outil, rev437) : même scénario que l'essai 1 du
  14/10 (SL500, Vc 700 / f 0,25, G96, programme L_140). Lot différent : maturité
  coulée **6 j → 4 j** (`maturiteBruts = 4`) + grenaillage récent — **conclusion
  saisie dans l'outil : « Pièces chaude --> grenaillage récent »**. Durée 09:45 →
  11:15, opérateur Léandre, rédigé par Matis.
- **Résultat** (prélèvements outil, 15 points) : **p1 Ra int 10,4 / ext 8,4** ;
  ext quasi stable (8,4 → 6,9 → 6,0 → 5,8 → 6,9 → 8,8 à p60) ; **int dérive
  10,4 → 8,8 → 10,0 → 8,5 → 9,8 → 13,2 (p50) → 15,3 (p60)** → hinge Ra max 12
  franchi côté int entre p50 et p60, **arrêt à p60**. **Battement 0,010-0,029
  sur toute la série — jamais en cause**, sortie de vie purement Ra (piste int
  d'abord). Obs Matis : « usure en peigne VB importante, pas d'écaillage
  visible » — confirmé au microscope le 16/11 (peigne développé, zéro casse).
- **Conclusion** : le « brut non stabilisé/tiède » est une variable de 1er ordre
  **sur la finition** (sur OP10 ébauche, l'expérience T1/T2 n'en montrait pas
  d'effet — ne pas généraliser). Co-variables documentées dans l'outil des deux
  côtés de l'A/B (maturité 6 vs 4 + conclusion grenaillage récent). Cause
  profonde : structure non stabilisée ; demande fonderie = dénominateur commun
  (disques froids, grenaillage assez tôt pour reposer).
- **⚠ À corriger dans l'outil** : motif de clôture de l'essai 2 = « casse »
  (détail « usure en peigne ») — le microscope exclut toute casse ; motif
  correct = « hors tolérance Ra » (le motif oriente le diagnostic, « casse »
  polluerait les filtres futurs).
- **Suite** : témoin même setup sur brut ≥ 6 j couru jusqu'au hinge réel (la
  base de vie SL500 sur brut mûr n'est pas mesurée — l'essai 1 du 14/10 s'est
  arrêté à 50 p sans hinge) ; puis essai f 0,30 sur brut mûr, protocole 5× ;
  âge minimum avant OP40 chiffré par la fonderie.
- **Outil** : EMAG 2 / 356x26 RPI / OP40 / « Essai 2 » du scénario SNGN 090416
  F SL500 G96 S700 F0,25 (rev437).

### 2026-10-14 — EMAG 2 · OP40 finition piste · DV356x26 RPI · essais 1-4 SN60 puis SL500 F — chatter résonant, pas la nuance

- **⚠ Relecture par les données outil (16/11)** : 4 scénarios datés du 14/10,
  tous à `maturiteBruts = 6`. La **SN60 n'est jamais allée en fin de vie** —
  trois essais interrompus :
  - **SN60 G96 S800 F0,25** : « Vibration dès la 5ème pièce » → arrêt (~5 p).
  - **SN60 G96 S760 F0,25** : « Vitesse baissée pour casser la vibration →
    n'a pas fonctionnée, pièce toujours vibrée » → arrêt (3 p).
  - **SN60 G97 S700 F0,25** : « Pièces vibrées à partir de la 5ème » (moins
    fort) → arrêt (~5 p). G97 réduit un peu l'intensité, pas le phénomène.
  - **SL500 F G96 S700 F0,25** : « La plaquette se comporte bien, 50 pièces
    usinées → peut faire plus » — **hinge jamais atteint** (d1 Ra 4,78/5,13 ;
    d5 stable ~4,0/3,46).
- **Lecture corrigée** : à maturité égale (6 j), SN60 vibré aux **trois**
  régimes essayés (800 G96, 760 G96, 700 G97) vs SL500 sans vibration sur
  50 p → le suspect est le **couple SN60/T-land sur ce montage**, pas le
  réglage vitesse. L'écaillage au microscope sur l'arête SN60 (fragment
  détaché, germe de notch à l'ap) = dégât mécanique subi pendant ces bains
  vibratoires courts, **pas une mort à la charnière**.
- **Référence production EMAG 1 (outil, scénario « valide »)** : **KY3500
  Vc 650 / f 0,25, charnière 30**. L'essai 22/09 (maturité **1 j**) : Ra int
  5,78 → 12,32 @ p15 → ~12 à p30. Second essai Kenna Vc 700 / f 0,25
  (maturité **2 j**) : **50 p sous le hinge** (6,5 int / 9,3 ext à p50, ext
  en montée), obs Matis : « **Usure en peigne (fonte fraiche)** » — le
  peigne existait déjà en septembre.
- **Conséquence benchmark** : « SL500 ×2 Kenna sur brut frais » comparait
  des maturités différentes (1-2 j vs 5 j) — confondu. Seul l'A/B/C même
  bain même jour (plan PCI 5 du 13/10) tranche proprement. Ancres SL500
  proprement datées : EMAG 2 14/10 (maturité 6) 50 p sans hinge ; **PCI 4
  268x12, 02/11 (maturité 3) : charnière 150 menée à son terme**.
- **Suite** : témoin SL500 sur brut mûr couru **jusqu'au hinge réel** (base
  de vie manquante pour re-ancrer tout calcul de Vc max) ; puis f 0,30 une
  variable à la fois, protocole 5× ; SN60 à réessayer seulement avec
  stratégie anti-vibration dédiée (bille, portoir). Saisir l'essai du 10/11
  (SL500, maturité 5, grenaillé ≤ 24 h tiède) dans l'outil — le champ
  `maturiteBruts` existe et est rempli sur EMAG1/EMAG2/PCI4.
- **Outil** : EMAG 2 / 356x26 RPI / OP40.

### 2026-10-13/14 — OP10 ébauche pistes · brut non grenaillé · LKT640 CNMX 120716 T02020 — cause racine fermée

- **Fait** (13/10, EMAG 1 — disque de la campagne 304x28/356x26) :
  Vc 700 / f 0,4 / ap 4 → **3 pièces/arête**, usure abrasive uniforme, zéro
  casse, surface pailletée. Bruts très mauvaise qualité.
- **Diagnostic** (Tours 67-68, cf. Conseils) : usure abrasive par peau de brut,
  pas le régime ni la géométrie — aucun levier process ne fait ×25 ; la loi
  Vc²·³ tient sur bruts sains (150 p @ Vc 500, 75-77 p @ Vc 700 = ×2 pour
  +40 % Vc) donc le 3 p est HORS loi.
- **Cause racine confirmée le 14/10 par le responsable fonderie** : lot
  **non grenaillé** (sable + burn-on + chill de peau). Le CNMX T02020 LKT640
  est lavé : 75-77 p/arête à Vc 700 sur grenaillés ; **Vc 700 / f 0,4 n'a
  jamais été faux**, aucun déclassement dès que le grenaillage est garanti
  amont.
- **Conclusion durable** : grenaillage = variable de 1er ordre ; le contrôle
  utile est à la RÉCEPTION (peau, avant l'atelier). Essai archivé côté outil
  comme valeur du risque (×25 de conso d'arêtes sur un lot).
- **Outil** : essai « Brut qualité dégradée » à archiver avec brut.statut =
  « degrade » (champ proposé, voir Règles).

### 2026-10-13 — PCI 5 · OP40 finition piste simultanée ext/int · DV304x28 RPE — préparation de campagne

- **Contexte** : nouvelle ligne avec Matis (resp. ligne Julien Flucher).
  Outil 6407 piste ext simultané avec 6417 piste int, bille antivibreur.
  Hinge actuel : 25 p/arête (Ra max 12 + battement 0,04). Bruts TRÈS frais
  (1-2 j). Objectif : ↑ vie + plaquettes moins chères.
- **Référentiel actuel** : Kennametal KY3500 wiper 0,50 (SNGN 0904, **Si₃N₄ pur
  Kennametal, haute ténacité** — correction user 16/11 : PAS SiAlON, PAS céramique
  mixte), ap 0,9 / Vc 700 / f 0,45, sec.
- **Candidats** : SN60 (codifié Stellantis) + SL500 F (arête vive) — hypothèse :
  supprimer les efforts radiaux du wiper (précédent OP10 EMAG 1 : le ×2 de vie
  venait de κr 85→95°).
- **Premiers essais** : Ra départ 6-10 vs limite 12 ; κr portoir 85°, K ≈ 250
  @ Vc 700 (rε 1,6) — Ra mesuré > théorie géométrique (≈ 4 µm) = part
  vibration/arête.
- **Suite** : A/B/C même bain même jour (Kenna 10 → SN60 10 → SL500 10),
  Ra + battement tous les 2-3 disques, protocole 5× avant production.
- **Outil** : PCI 5 / 304x28 RPE / OP40 (c'est l'essai manqué dans l'affichage
  du 20/10 — Tour 80 — corrigé depuis).

### 2026-09-22 — EMAG 1 · finition piste · DV356X26 RPI · SL500 vs KY3500 — le déclic Ra

- **Résultat** : SL500 (SNGN 090416F) surpasse nettement le KY3500 Kennametal.
  ⚠ Attribution : **le Ra max 12 atteint à la pièce N°15 est le résultat
  KY3500 (catastrophique)**, pas le SPK.
- **Lecture** : l'objectif n°1 était le battement, mais la qualité de surface
  s'est révélée le sujet critique (3 mois sans contrôle Ra sur la ligne).
  Hypothèse mécanisme : arête vive -F → forces de coupe réduites ; rayon de
  nez au lieu du wiper → idem.
- **Suite de l'époque** : mesure du battement sur les disques du jour ;
  protocole 5× acté. Rapport Salesforce finalisé (structure canonique).
- **Outil** : EMAG 1 / 356x26 RPI / OP40.

### 2026-08-26 — OP10 ébauche pistes · LKT640 (κr 85°, SNGX) · Vc 500 / f 0,35 — l'essai fondateur validé

- **Résultat** : **150 p/arête**, battement < 0,10, sur bruts grenaillés sains.
  Point d'ancrage site n°1, validé en production (case study Opp_7851).
- **Ce qu'il a servi à prouver depuis** : avec 75-77 p @ Vc 700 (T1/T2, bruts
  sains), la loi Vc²·³ tient sur fonte saine — ce qui a permis de détecter le
  hors-loi du 13/10 et de blanchir le régime.

---

## Conseils & leçons essais (transféré d'ECHANGES.md, ex-« Questions ouvertes à Z Code »)

Les trois sessions de conseil technique du 14/10, conservées telles quelles
(les renvois de version/verrou concernent le journal, pas les essais) :

### Tour 67 — 14/10/2026 — Hermes (mécanique des plaquettes)

Le fait : usure très rapide sur LKT640 CNMX 120716 T02020 (Vc 700 / f 0,4 /
ap 4), 3 pièces, surface pailletée, pas de casse ni d'écaillage.
Diagnostic : signature d'usure abrasive par peau de brut (sable incrusté,
croûte brûlée, points durs, chill 400-500 HB local) — pas le grade ni la
charge mécanique. Actions immédiates : retour à Vc 500 (point validé du
26/08), dureté EN PEAU (> ~255 HB = lot à écarter), photos des zones
pailletées (sable adhérent vs métal dur brillant = deux diagnostics, deux
interlocuteurs). Remontée fonderie formelle : grenaillage avant usinage,
traçabilité poche/moulage, sable de moulage. Si Vc 700 doit rester : SNGX
κr 85° (150 p/arête du 26/08) + hone 15-20 µm (bord arrondi tient mieux sur
peau abrasive). Dans l'outil : archiver l'essai comme « non conforme/arrêté »,
le 3 p vs 150 p est l'argument chiffré fonderie — premier cas d'usage du
module coût rebut.

### Tour 68 — 14/10/2026 — Z Code (contre-regard : le brut oui, le ×50 non)

Où Z Code signe : la peau du brut est la cause dominante, et l'argument qui
verrouille est dans nos données de site — aucun levier process ne fait ×25
(géométrie C→S = ×2, avance = ×1,1-1,3, tout empilé = ×2,6 ; le résidu ×10-20
n'a qu'un porteur : le garnissant). Le CNMX T02020 est la prescription, pas un
suspect (té 0,2×20° = préparation pour lots suspects ; zéro écaillage = elle
tient la charge).
Où Z Code corrige : ne pas vendre « Vc 700 divise la vie par 50 » comme la loi
Vc — (700/500)³ = 2,7 ; nos deux points de site donnent ×2 pour +40 % Vc,
exposant ≈ 2. L'argument honnête à la fonderie : « vie effondrée à 3 p/arête,
dureté en peau > ~255 HB, photos, quel que soit le régime ». Le retour Vc 500
est un test à double lecture : sur CES bruts, 6-15 p/arête prédits — 150 p
signifierait brut sain. La photo qui tranche : dépouille râpée uniforme = sable
exogène ; notch en V à la profondeur de coupe = croûte localisée ; facettes
polies + micro-fractures = chill/trempe blanche. Réserve méthodo : jamais le
switch SNGX 85° sur un lot dégradé.
Champ `brut` proposé pour l'outil : `{statut: sain|degrade|inconnu, peauHB,
lot}` — énumération fermée, `inconnu` défaut implicite (zéro migration),
filtre « usure anormale × brut dégradé » au lieu de relire les observations.
Variantes rejetées : tags libres dans observations.

### Tour 69 — 14/10/2026 — Z Code (clôture : cause racine confirmée — bruts non grenaillés)

Le responsable fonderie confirme : bruts **non grenaillés** → branche
garnissant exogène, pas le chill. Ce que ça ferme : diagnostic confirmé sans
nouvel essai ; CNMX T02020 LKT640 lavé (75-77 p/arête à Vc 700 sur
grenaillés) ; Vc 700 / f 0,4 jamais faux, pas de déclassement dès que le
grenaillage est garanti amont. Ce que ça ouvre : grenaillage = variable de
premier ordre, contrôle à la réception ; l'essai 3 p/arête = la valeur du
risque (×25 de conso) à archiver avec `brut.statut = "degrade"` ; reprise des
essais sur grenaillés (référence 30 disques, protocole 5×), le switch SNGX 85°
redevient testable.

---

*Fichier créé le 16/11/2026 lors du rangement du dossier (Tours reclassés dans
ECHANGES.md). Les prochains essais s'ajoutent ici, récent en tête, avec les
clés ligne / disque / OP / date — et se déclinent dans les skills.*
