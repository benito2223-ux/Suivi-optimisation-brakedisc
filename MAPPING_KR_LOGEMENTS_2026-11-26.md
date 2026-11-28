# Mapping κr / rε des logements — validation avant injection Supabase

> Généré le 26/11/2026 à partir des plans d'outillage du Drive (`3027-Toollayout-Rev08.pdf`, `3027_08_ToolLayout_*_REV01.pdf`, `CeramTec_Layout_4065_REV04.pdf`, `3015_Tool layout_2011-02-15.pdf`, `200929_Layout HESSAP_OP20.pdf`).
> **Aucune écriture effectuée dans Supabase** : ce tableau est à valider (ou annoter) par Benjamin avant toute injection en base. Une future injection ne devra jamais écraser un `kappaR` ou `rayonBec` déjà saisi manuellement.

## 1. EMAG 1 / 2 / 3 (source : `3027-Toollayout-Rev08.pdf`, 30/03/2023)

| OP | Outil (suivi) | Logement | Plaquette | κr (°) | rε (mm) | Statut / remarque |
|---|---|---|---|---:|---:|---|
| OP10 | T511 / T515 / T515A | D1 | SNMX / SNGX 120716 | **45** | 1,6 | Chanfrein alésage |
| OP10 | T511 / T515 / T515A | D2 | SNMX (302) / CNMX (330, 356) | **85** (302) / **95** (330, 356) | 1,6 | Face / alésage bol |
| OP10 | T517 / T519 / T511A | D1 | SNMX / SNGX 120716 | **85** | 1,6 | Épaulement |
| OP10 | T517 / T519 / T511A | D2 | CNMX / CNGX 120716 | **95** | 1,6 | Intérieur bol (Z) |
| OP10 | T513 / T50013 | D1 | CNMX / CNGX 120716 | **95** | 1,6 | Dégagement bol *(93° si DNMX 330×28)* |
| OP10 | T513 / T50013 | D2 | CNMX (75°) / SNMX (85°) 120716 | **75** *(ou **85** si SNMX terrain)* | 1,6 | **Grande face piste** — vérifier si passé en 85° sur EMAG 1 |
| OP20 | T521 | D1 / D2 | CNMX / SNMX 120716 | **45** | 1,6 | Chanfrein / Ø ext |
| OP20 | T523 / T529 | D1 | CNMX 120716 | **95** | 1,6 | Épaulement |
| OP20 | T523 / T529 | D2 | CNMX 120716 | **75** | 1,6 | **Grande face piste OP20** |
| OP20 | T525 | D1 | RCGX 090700 SL500 | **90** | **4,76** | Plaquette ronde Ø 9,52 |
| OP20 | T527 / T5211 | D1 / D2 (CNMX) | CNMX 120716 | **95** | 1,6 | Bol |
| OP20 | T527 / T5211 | D1 / D2 (ronde) | RBGN 0804M0 / RCGX 090700 | **90** | **4,0** / **4,76** | Ronde Ø 8 (302) ou Ø 9,52 (330, 356) |
| OP30 | T532 / T533 / T535 | Logement 1 | Embouts perçage | — | — | **Hors tournage céramique** |
| OP40 | T543 | D1 | TNGN 160412 SL506 | **93** | 1,2 | Alésage / face moyeu |
| OP40 | T543 | D2 | SNGN 090416 SN60 | **85** | 1,6 | Alésage / face moyeu |
| OP40 | T546 | D1 | CNMA / CNMX 120416/120716 | **95** | 1,6 | Finition bol *(vérifier si chanfrein 45° sur EMAG 2)* |
| OP40 | T547 / T547A | D1 | TNGN 110416 | **95** | 1,6 | Intérieur bol (330×14) |
| OP40 | T548 / T549 | D1 | SNGN 090408 F-85Z050 | **85** | **0,8** *(1,6 essai -F)* | **Finition pistes ventilés** |
| OP40 | T541 / T542 | D1 | SCGN 090408 F-85Z025 | **85** | **0,8** | **Finition pistes pleins (330×14)** |

## 2. WEISSER 1 / 2 / 3 / 4 (sources : `CeramTec_Layout_4065_REV04.pdf` + `3015_Tool layout`)

| OP | Outil (layout) | Pos | Plaquette | κr (°) | rε (mm) | Remarque |
|---|---|---:|---|---:|---:|---|
| OP10 | T3011 / T1 | 1 / 2 | SNMX / CNMX 120716 | **45** / **95** (304) ou **85** (pleins) | 1,6 | Alésage + bol |
| OP10 | T4012 / T2 | 3 / 4 | CNMX / SNMX 120716 | **95** / **85** *(85/85 pleins)* | 1,6 | Bol + épaulement |
| OP10 | T13 / T3 | 5 / 6 | CNMX 120716 | **75** / **95** | 1,6 | Piste + dégagement |
| OP20 | T21 / T4 | 1 / 2 | CNMX / SNMX 120716 | **45** / **45** | 1,6 | Chanfrein / Ø ext |
| OP20 | T322 / T5a | 3-4 / 5-6 | CNMX 120716 | **95** / **75** | 1,6 | Épaulement + piste |
| OP20 | T4024 | 5 | LBMP12A0800 | **90** | **4,0** | Gorge R4 |
| OP20 | T4025 / T7 | 6-7 / 3-4 | RBGN 0804M0 + CNMX | **90** (rε 4,0) / **95** | 4,0 / 1,6 | Gorge + bol |
| OP30 | T35 / T8a | 1 / 2 | SNGN 090416 (ou 12) + TNGN | **85** *(45 pleins)* / **93** | 1,6 / 1,6 | Alésage / moyeu |
| OP30 | T08 | 3 | CNMX 120716 | **95** | 1,6 | Finition bol (304×28) |
| OP30 | T32 / T33 / T11 / T12 | 4 / 5 | SNGN / SCGN 090408 | **85** | **0,8** | **Finition pistes** |

## 3. HESSAPP (source : `200929_Layout HESSAP_OP20.pdf` + suivi)

| OP | Outil | Plaquette | κr (°) | rε (mm) | Statut |
|---|---|---|---:|---:|---|
| OP20 | T6 / T7 | SNGX 120716 | **85** | 1,6 | Lu sur plan OP20 |
| OP20 | T8-D1 / T8-D2 | SNGX 120716 / TNGN 160412 | **95** / **95** | 1,6 / 1,2 | Lu sur plan OP20 |
| OP10 / OP15 / OP30 | T1, T2, T5, T6 | SNMX / CNMX / RBGN / DWG 1743941 | *85 / 93 / 90(r4)* | *1,6 / 0,8 / 4,0* | **À confirmer** (plans OP10/15/30 absents de `Layout\`) |

## 4. PCI 4 & 5 — estimation uniquement (100 % Kennametal, hors périmètre direct)

| OP | Outil (suivi) | Logement | Opération (DP268) | κr est. (°) | rε est. (mm) |
|---|---|---|---|---:|---:|
| OP10 | T6101 | T0101 / T0111 | Ébauche Ø bol / fond bol (SNMX) | **85** / **95** | 1,6 |
| OP10 | T6103 | T0303 / T0313 | Ébauche piste int. / bol (CNMX) | **75** / **95** | 1,6 |
| OP10 | T6105 | T0515 / T0525 | Moyeu / appui jante (SNMX) | **85** | 1,6 |
| OP20 | T6201 | T0101 / T0111 | Chanfrein / Ø ext (SNMX) | **45** | 1,6 |
| OP20 | T6203 | T0303 / T0313 | Ébauche piste (CNMX) | **75** / **95** | 1,6 |
| OP20 | T6205 | D1 / T0505 | Gorge (A4R0800) | **90** | **4,0** |
| OP20 | T6207 | T0717 | Face appui jante (SNMX) | **85** | 1,6 |
| OP30 | T6304 / T6305 | Log. 1 & 2 | Perçage / fraisurage | — | — |
| OP40 | T6401 | T0101 / T0111 | Alésage / face avant (SNGN/TNGN) | **85** / **93** | 1,2 / 1,6 |
| OP40 | T6403 | D1 / T0303 | Bol (CNMX) | **95** | 1,6 |
| OP40 | T6407 / T6417 | D1 / T0707 | **Finition pistes** (1743941) | **85** | **0,8** *(ou 1,2 selon plaquette)* |
