# RÉCAP — Temps de coupe tirés des programmes CN (EMAG 1, EMAG 2, PCI 4) — pour TIMON

> Auto-contenu. Écrit le 26/11/2026 par Claude pour Benjamin, qui confie la suite à TIMON (et Hermes si besoin).
> Ordre de lecture : `VERROU.md` → ce récap → `NOTES_A_VERIFIER_2026-11-24.txt` → fin de `ECHANGES.md` (« Faits extérieurs » du 23-24/11).
> Langue : français. Benjamin attend une direction assumée. **Rien à déployer** dans ce chantier : c'est de la donnée (cloud) + des recaps Excel.

## 1. De quoi il s'agit

Remplir le champ **temps de coupe** (`tempsCoupe`, en secondes par disque) de chaque logement des références « Classeur Matis »
de l'outil Suivi d'optimisation (Stellantis Sept-Fons), à partir des **programmes CN des machines** — et non du cycle pupitre.

**Définition retenue (ne pas changer sans Benjamin)** : temps de coupe = mouvements en avance (G1/G2/G3) **dans la fenêtre de
surveillance Montronix** ; longueur / (avance × vitesse de broche). Hors : rapides, chargement, changements d'outil, indexations.
C'est donc **plus court que le cycle pupitre** (≈ 60 s affichés sur EMAG 2 pour ≈ 30 s de coupe par OP) ; l'écart = « hors coupe »,
qui fait l'objet du **lot 2** (voir §6).

## 2. Où sont les choses

| Quoi | Où |
|---|---|
| Programmes (propriété Stellantis) | `Programmes/EMAG1 356x26/` (L110_1/2, L120_11/22, L130_11_K_SUB1/2, L140_1/2), `Programmes/EMAG1 - 304x28/` (L120_1/2), `Programmes/Programme DV356x26 EMAG 2/` (L110_CBN, L120, L130_11_K_SUB1, L140), `Programmes/PCI 4 - DP268X12/` (O2681 OP10, O2682 OP20, O2681-OP30, O2687 OP40). **Non versionnés, ne jamais les publier.** |
| Parseur Siemens (EMAG) | `scripts/spf_temps.py` — `run(path, balises_commentees=False, ouvre_extra=())` |
| Parseur Fanuc (PCI) | `scripts/fanuc_temps.py` — `run(path, fraisage=False, sans_limite=False)` |
| Générateurs de recap Excel | `scripts/recap_emag1.py` (EMAG 1 356), `scripts/recap_pci4_268.py`, `scripts/recap_emag1_304.py` (`--json` imprime les valeurs à saisir) |
| Recaps Excel | `Programmes/RECAP_TEMPS_COUPE_DV356_EMAG1.xlsx`, `…_DV356_EMAG2.xlsx`, `…_DP268_PCI4.xlsx`, `…_DV304_EMAG1_OP20.xlsx` |
| Résultats EMAG 2 (rédigé) | `Programmes/TEMPS_COUPE_DV356_EMAG2.md` (+ `temps_coupe_DV356_EMAG2.json`) |
| Notes « à vérifier » de Benjamin | `NOTES_A_VERIFIER_2026-11-24.txt` |
| Spec du lot 2 (hors coupe) | `SPEC_TEMPS_DE_COUPE_LOT2_2026-11-23.md` |
| Journal (révisions cloud, hypothèses) | `ECHANGES.md`, fin du journal, entrées du 23 et 24/11 |
| La conversation d'origine | session Claude Code du dossier `Stellantis_SeptFons`, fichier `~/.claude/projects/C--Users-Admin-Desktop-Stellantis-SeptFons/9e3ce9b6-42d8-47a5-88bd-42d3d511da53.jsonl` (EMAG 1, PCI 4, 304) ; EMAG 2 : commit `b2a8a9f` du 24/11 |

Relancer un recap (depuis la racine du dépôt) :
```
python scripts/recap_emag1.py "Programmes/EMAG1 356x26" Programmes/RECAP_TEMPS_COUPE_DV356_EMAG1.xlsx
python scripts/recap_pci4_268.py "Programmes/PCI 4 - DP268X12" Programmes/RECAP_TEMPS_COUPE_DP268_PCI4.xlsx
python scripts/recap_emag1_304.py "Programmes/EMAG1 - 304x28" Programmes/RECAP_TEMPS_COUPE_DV304_EMAG1_OP20.xlsx --json
```

## 3. Méthode — ce qu'il faut savoir des programmes

- **Fenêtre Montronix** : Siemens (EMAG) `M870` → `M890` ; dans les programmes **EMAG 1 356 les balises sont commentées** (option
  `balises_commentees=True`) ; dans **EMAG 1 304**, `M870` est mal tapé `M700` / `M670` sur T521 (lus comme M870 via `ouvre_extra`).
  Fanuc (PCI) : `M2908` → `M2909` (même entre parenthèses), courbes `M30xx`.
- **Limite de broche** : `LIMS` (Siemens) / `G50 S` (Fanuc) appliquée en G96 ; effet faible (≤ 0,4 s), mais la Vc réelle baisse sur les petits Ø.
- **Temporisations** : `G4 S` = tours, `G4 F` / `G04 X` = secondes ; comptées si dans la fenêtre.
- **Perçages** : multipliés par le nombre de trous (EMAG : 5 et 3 ; PCI 4 OP30 : 2 × Ø8,5 et 4 × Ø13,2 — la fenêtre ne couvre qu'un trou).
- **Logement** : un seul couple Vc / f par logement dans l'outil → on saisit la **condition qui pèse le plus en temps** (approximation
  quand il y en a plusieurs). G97 : `modeVitesse` = « G97 », tr/min dans `sBroche`, `vc` vide.
- **Correspondance Fanuc** : outil programme `Txx` → logement de l'outil `T%02d%02d` (ex. T15 → T0515, T25 → T0525).
- **EMAG 1 : côté 1 = référence** (programmes `L1xx_1`) ; le côté 2 n'a pas de place dans l'outil (une seule ligne par projet, décision Q3) : il reste dans l'Excel.
- **Simultanéité** : deux outils qui coupent en même temps → `simultaneAvecPrecedent = true` sur le second ; l'OP compte le plus long.

## 4. Résultats saisis dans le cloud (Supabase `cxjfyaorkkxemjnollnj`, table `sync_shards`, références « Classeur Matis »)

Temps en secondes par disque (coupe pure). Révisions et numéros de séquence : `ECHANGES.md`.

| Ligne / référence | OP10 | OP20 | OP30 | OP40 | Total | Remarques |
|---|---|---|---|---|---|---|
| **EMAG 2 / 356x26 RPI** (23-24/11) | 29,5 | 33,1 | 14,8 | 36,5 | **≈ 114** | T549 simultané de T548 ; conditions Vc/f saisies aussi |
| **EMAG 1 / 356x26 RPI**, côté 1 (24/11) | 38,65 | 24,93 | 15,45 | 33,47 | **≈ 112,5** | côté 2 : 39,82 / 23,35 / 14,38 / 36,88 (Excel seulement) |
| **PCI 4 / DP268x12** (24/11) | 19,83 | 14,91 | 14,32 | 20,28 | **≈ 69,3** | T6417 simultané de T6407 (confirmé par Benjamin) |
| **EMAG 1 / 304x28 RPE**, OP20 seule, côté 1 (24/11) | — | 31,0 | — | — | — | côté 2 : 36,66 (seul T521 diffère : Vc 1500 / f 0,35 côté 1, Vc 800 / f 0,30 côté 2) |

Détail par logement : les recaps Excel (onglet « Coupe par logement ») et `ECHANGES.md`.

Écarts notables EMAG 1 (côté 1) vs EMAG 2 : T50013 D2 / T513 22,69 s vs 11,1 s (EMAG 1 à Vc 500 / f 0,35) ; T549 17,38 vs 21,8 ;
T529 7,64 vs 10,3 ; T546 9,77 vs 8,3. Côté 1 vs côté 2 EMAG 1 : T546 9,77 s (G96 Vc 400) contre 13,74 s (G97 650 tr/min) → **piste d'optimisation**.

## 5. Hypothèses prises — à faire confirmer par Matis

EMAG 1 / 356 :
1. **T548** existe dans le suivi mais pas dans les programmes EMAG 1 → mis à **0 s**. Autre programme ?
2. **T5211** : le suivi n'a que D2 (plaquette CNMX), le programme travaille en D1 → 4,46 s posés sur D2. Inversion D1 / D2 ?
3. **Côté 2 non saisi** (référence = côté 1).
4. **T50013 D2** : « 2 vitesses » = une approche de 0,5 mm à Vc 900 (0,08 s) puis la coupe à Vc 500 / f 0,35 → saisi Vc 500 / f 0,35.
5. En-tête de `L110_1` mentionne encore DV304X28 ; `L140_2` contient une coquille « M770 ».
6. **T521 D1 charnière = 2400** (les autres à 150) : coquille probable dans l'outil principal (concerne le checkup).

PCI 4 / 268 :
7. **T6203 / T0313** jamais appelé dans O2682 (OP20) → **0 s**.
8. OP40 : deux passes identiques de 14,54 s **l'une après l'autre** dans le programme, saisies **simultanées** (T6407 / T6417) sur
   confirmation de Benjamin → vérifier que c'est bien le programme de la machine.
9. OP30 : perçage = Logement 1, fraisurage = Logement 2 ; tous les trous comptés.

EMAG 1 / 304 OP20 :
10. Balises `M700` / `M670` au lieu de `M870` sur T521 → la surveillance Montronix ne démarre pas sur T521 (à signaler aux méthodes).
11. **T521 côté 1 (Vc 1500) ou côté 2 (Vc 800)** : lequel est la bonne référence ? Rattachement droite / gauche de L120_1 / L120_2 inconnu.
12. T525 : trois avances (0,15 / 0,1 / 0,3) → saisi f 0,15. Une copie « Classeur Matis » non-référence (`smwuttz8udag9`) laissée intacte.

Général : 13. Vc / f saisis = la condition dominante en temps. 14. G97 : un essai doit avoir ses propres tr/min pour que l'outil
recalcule le temps (sinon il le dit). 15. Ce sont des temps de **coupe pure**, pas le cycle pupitre.

## 6. Ce qui reste à faire (dans l'ordre)

1. **Faire trancher les hypothèses §5 par Matis** (questions 1, 2, 7, 8, 11 en priorité : elles changent des chiffres saisis).
2. **Lot 2 — le hors coupe** (`SPEC_TEMPS_DE_COUPE_LOT2_2026-11-23.md`) : champ « hors temps de coupe » par OP (remplit la partie
   hachurée des barres), gain calculé sur le goulot, règle du bandeau §9, une seule fonction de gain dans `MoteurLigne`.
   **Attend les réponses de Matis D1, D2, D4** (tableau « Décisions en attente » d'ECHANGES). **Touche `bilan_economique.html`,
   gelé** : lever le gel avec Benjamin, prendre le verrou, version + CHANGELOG + tests (protocole habituel).
3. **Lignes sans programmes ici** : PCI 5 / 268 (mêmes outils que PCI 4 / 268), PCI 4 / 283 et 302, EMAG 2 / 330x14 et DP 290,
   EMAG 3, WEISSER, HESSAPP — temps vides. Demander les programmes à Matis, puis même méthode.
4. EMAG 1 / 304 : OP10 et OP40 (seule l'OP20 a été demandée et faite).

## 7. Pièges déjà rencontrés

- Écrire dans le cloud : `rev = rev + 1`, `seq = nextval('public.sync_seq')`, `modifie_par`, `modifie_le = now()` ; reconstruire
  `body->'outils'` en gardant l'ordre (`with ordinality`) ; **ne jamais écraser** un `tempsCoupe` déjà rempli
  (`coalesce(l->>'tempsCoupe','') = ''`) ; **toujours `coalesce(…, '[]')`** autour des agrégations de listes (une agrégation vide
  rend NULL : le 24/11 un outil est passé de `logements: []` à `null`, réparé). Valeurs stockées en texte (« 900 », « 0.43 », « 3.9 »).
- Les scénarios d'essai ont leurs **propres copies** des outils (et un essai « figé ») : changer la référence peut faire afficher
  « le scénario a changé » ; vérifier les drapeaux `suivi` avant.
- Windows / git-bash : le `/tmp` de bash n'est pas celui de Python Windows ; chemins relatifs au dépôt. `PYTHONIOENCODING=utf-8` pour les accents.
- Excel généré : une apostrophe dans un titre de colonne a cassé un script (chaîne Python) ; la virgule décimale française est ajoutée en post-traitement.
- Données Stellantis : programmes et contenu métier = confidentiels ; aucune mention SPK / CeramTec dans l'outil.
