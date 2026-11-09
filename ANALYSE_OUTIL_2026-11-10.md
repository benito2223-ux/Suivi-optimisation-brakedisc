# Analyse indépendante — la logique et l'évidence de l'outil « Suivi d'optimisation »

**Auteur** : Hermes (second analyste) · **Date** : 10/11/2026 · **Base** : 4.150.0 (branche `ux-rail`, HEAD `df1b1ee`)
**Méthode** : lecture du code (`bilan_economique.html`, fonctions citées ligne à ligne) + reproduction **sur données réelles** : l'export rev435 du 09/11 (`SuiviOptimisation_rev435_20261109-1000.json`, exporté par Matis) injecté dans une instance locale du `dist/` 4.150.0, profil de test isolé, **aucune écriture** — ni dans la prod, ni dans le cloud. Chaque chiffre ci-dessous a été recalculé en appelant les fonctions de l'outil elle-même (`cartePostes`, `campagneCollecter`, `planRecapGains`, `bilanAnnuel`…), pas estimé.

---

## 1. Verdict en 5 lignes

1. **Le moteur de calcul est solide** : `coutsDetail`/`bilanAnnuel`/`perimetreCompare`/`charniereReelle` font ce que la constitution dit, les périmètres sont portés avec les chiffres, les abandons et hors course sont exclus — les 787 tests s'expliquent.
2. **Le chiffre le plus important de l'outil, « l'économie acquise », a quatre définitions concurrentes dans quatre écrans** — et les quatre valeurs ont été reproduites sur données réelles : 0 (Vue d'ensemble), 7 449 €/an (Campagne), 0 (Plan bandeau), −2 112 €/an (Plan tableau). Ce n'est pas un bug d'affichage : quatre fonctions lisent le même état avec des règles différentes.
3. **Le pire cas n'est pas une divergence abstraite** : un scénario réellement **en série** (EMAG 1 OP40, daté 22/09) délivre 7 449 €/an acté — et comme il n'est pas le « meilleur » de son poste, `gainPoste` l'ignore et l'écran affiche à la place **+12 195 €/an « projeté »** : le gain acquis est invisible et remplacé par une promesse. Aucun écran hors la Campagne ne le montre.
4. **Les trois questions de Benjamin n'ont pas de réponse en un coup d'œil** : le levier prix/vie n'existe que dans le Plan (par **article**, toutes lignes confondues, 2 clics + recherche + frappe pour lire un total au bas d'un tableau), l'écran atelier n'affiche **aucun** chiffre d'argent, et la durée de vie mesurée (90 réel vs 50 visé) est calculée (`gainMesure`) mais reléguée dans un pied replié — le verdict reste à la visée sans le dire.
5. **En dessous, l'outil se sabote sur des détails** : coquilles (« k€€/an », « −-0,005 », « /an/an », « + -4,1 k€ », « k€ € »), « manque : … » répété **18 fois** sur le Plan, bannière « Reprendre » qui emmène ailleurs sans nommer la ligne. Chacun est localisé à la ligne près et se corrige en une heure.

---

## 2. Contradictions de chiffres — même grandeur, deux valeurs

Toutes reproduites le 10/11 sur rev435. Rangs par gravité.

| # | Grandeur | Écran A (valeur · source) | Écran B (valeur · source) | Cause prouvée | Correction |
|---|---|---|---|---|---|
| C1 | Économie actée | Vue d'ensemble, bloc 01 : **« aucun gain acté — premiers passages en série en attente »** (`accueilBandeauHTML`, l. 20630 : ne compte que les lignes `gainActe > 0`) | Synthèse/Campagne : **7 449 €/an actés** (`campagneCollecter`, l. 11477 : **tout** scénario `serie` moins cher que la base, config **globale**, volume **brut**) | Trois définitions : (a) `gainPoste` l. 15903 ne compte que le scénario **« meilleur »** de chaque référence ; (b) campagne les compte tous ; (c) `planRecapGains` l. 19765 ne somme que `gainActe > 0` | **UNE fonction** `gainsActes()` consommée par les 4 écrans (détail §4, P0-1) |
| C2 | Économie actée (même écran Plan !) | Plan, bandeau : **« GAINS ACTÉS — aucun scénario passé en série pour l'instant »** (`planBandeauHTML`, `recap.totalActe = 0`) | Plan, section « Scénarios en validation » : **« En série — gains actés (1) · cumul acté : −2,1 k€/an »** (HESSAPP OP15, `gainPoste`) | Un gain acté **négatif** existe ; le bandeau le jette (`actes = postes.filter(p => p.gainActe > 0)`), le tableau l'affiche. Un « gain » négatif n'est pas un gain : mais un passage en série **existe** — le bandeau ment en disant le contraire | Le bandeau compte les séries (pas seulement les positives) : « 1 poste en série : −2,1 k€/an (coûte plus cher — à revoir) ». Vu à l'écran le 10/11 |
| C3 | Gain du poste EMAG 1 OP40 (356x26) | Campagne : **+7 449 €/an acté** (scénario « Process actuel — finition piste DWG… KY3500 », en série daté 22/09) | Vue d'ensemble / Plan / pipeline : **+12 195 €/an « projeté »**, acté invisible (`gainPoste` : le scénario en série n'est pas le « meilleur » → `serie=false`, son gain n'entre nulle part) | `gainPoste` ne lit qu'UN scénario par référence (le meilleur non échec) ; la campagne les lit tous. Résultat : le réel est remplacé par une promesse plus grosse | `gainPoste` : si un scénario en série existe, il est le **candidat acté** ; le « meilleur » non-série reste le potentiel. Les deux s'affichent côte à côte |
| C4 | Coût de HESSAPP OP15 (302x26), scénario en série | Campagne : gain **0 €** (`coutsDetail(sc, undefined, lg)` — config **globale**, l. 11474) | Plan tableau : **−2 112 €/an** (`coutsDetail(sc, op.config, lg)` — config **de l'OP**, via `bilanAnnuel`) | La campagne passe `undefined` à `coutsDetail` → les pièces détachées/coûts dépendants de la config de l'OP sont calculés avec la config par défaut. Deux configs, deux vérités | La campagne reçoit la config de l'OP (`dansContexteOp` la pose : lui passer `op.config`) |
| C5 | Volume annuel HESSAPP OP20 (426 000) | Campagne : `parseFloat(rf.productionAnnuelle)` **brut** — le volume compte | `gainPoste`/`bilanAnnuel` : `volumeAnnuel()` l. 20842-ish retourne **null** si `cfg.volumeActif` est désactivé — le volume ne compte pas | Deux lectures du même champ : le curseur « volume actif » de l'OP lie un écran, pas l'autre. Aujourd'hui le hasard fait que le scénario n'est pas moins cher (sinon : acté fantôme) | La campagne passe par `volumeAnnuel(rf, op.config)` comme tout le monde |
| C6 | Économie simulée du Plan | Bas du tableau : **« 3 article(s) en conversion — économie simulée : −72,8 k€/an »** (l. 20188 : articles **cochés** `etat`) | En-tête du visuel : **« −122 k€/an (−12 %) · 23 article(s) simulé(s) »** (l. 20272 : articles avec **prix et/ou vie cibles posés**) | Deux périmètres (`actif` vs `travail`), deux totaux, aucun mot ne les relie | Un seul total affiché + répartition : « dont 72,8 k€/an sur les 3 articles engagés » ; libeller chaque total par son périmètre |
| C7 | Temps de cycle (même scénario) | Tête de fiche : **« 0,0 % »** (l. 8950 : delta du champ **manuel** `sc.cycle`, vide → 0/réf.) | Tuiles par outil : **« cycle +33 % »** (l. 7477 : dérivé de **Vc×f**, `pctCycle = 100 − vB/vS×100`) | Deux définitions du « temps de cycle » : l'indice saisi à la main et le calcul Vc·f. Quand le champ est vide, l'écran haut ment (0,0 %) pendant que les tuiles disent +33 % | UNE définition affichée (Vc·f dérivé), le champ manuel garde son rôle de **correction** et porte son étiquette « relevé » |
| C8 | « Meilleur coût » (Synthèse) | **« Meilleur coût : … −0,0 % vs base »** (l. 8376 : `ecart == 0` → signe « − » + 0,0 %) | Le même écran dit ailleurs « aucun scénario ne bat la base » | L'ex æquo est affiché comme un meilleur | `ecart === 0` → « égal à la base » (mot + couleur neutre) |

---

## 3. Les trois questions — chemin actuel, ce qui manque, évidence cible

### Q1 — « Combien j'économise si je baisse le prix d'une plaquette sur une ligne ? »

**Chemin actuel (compté)** : « Outils » (1 clic) → « Plan de conversion » (2) → retrouver l'article parmi ~23 lignes (recherche visuelle, sans filtre par ligne) → taper le prix cible (frappe) → lire le total **en bas** du tableau. Total : 2 clics + recherche + frappe. Et la réponse obtenue est **fausse pour la question posée** : le Plan chiffre par **article, toutes lignes confondues** (`planLignes`, l. 19899 — la variable `vieLigne` y signifie « ligne du tableau », pas ligne de production). **Aucun écran de l'outil ne sait dire « −10 % de prix sur CETTE ligne = −X €/an »** — vérifié : aucun appel de levier prix par `ligneId` n'existe.

**Ce qui manque** : le levier au niveau où Benjamin raisonne (la ligne), et la réponse au point d'où il part (la carte du poste ou le Catalogue).

**Maquette textuelle de l'évidence cible** — sur la carte du poste (et dans la fiche scénario) :

> **Leviers — KY3500 sur HESSAPP OP30 (T5+T6, 20,4 k€/an)**
> prix −10 % (9,56 → 8,60 €) → **−2,0 k€/an**
> +10 pièces/arête (50 → 60) → **−3,4 k€/an**
> vie mesurée 90 au lieu de 50 → **−9,1 k€/an** (essai arrêté avant charnière — à confirmer)
> *(source : `bilanAnnuel` avec substitution prix/charnière — fonctions pures `levierPrix(sc, pct)`, `levierVie(sc, delta)` ; chaque ligne porte son « à confirmer » quand la donnée n'est pas actée)*

Un clic sur un levier = l'ouvrir dans le Plan pré-rempli (article + ligne), pas un chiffre mort.

### Q2 — « … et sur l'atelier (l'écran de saisie à la machine) ? »

**Chemin actuel** : aucun. Mesuré en mode atelier sur rev435 : **zéro mention** de coût, d'économie ou de charnière chiffrée à l'écran (le mot « charnière » n'apparaît que dans un label de saisie). Le bloc économies existe hors atelier (`atelierEconomieHTML`, l. 19036) mais affiche « Scénario de référence — pas d'économie à comparer » sur les scénarios de production (comportement testé, donc voulu) et l'option est **éteinte par défaut** depuis la 4.149.

**Ce qui manque** : la seule phrase utile debout devant la machine : « cette arête coûte X €/pièce · chaque pièce de plus = −Y €/an ». Le régleur n'a pas besoin du levier prix ; il a besoin de savoir si ce qu'il est en train de mesurer est de l'or.

**Maquette** — une ligne en tête de l'écran de saisie d'essai :

> **KY3500 · T5 D1 — 0,00095 €/pièce · +10 pièces/arête = −3,4 k€/an** *(à confirmer par l'essai en cours)*

Effort S/M (réutilise `posCost` et le levier vie). Condition constitutionnelle : le bloc reste une information, jamais une invite à la saisie impossible.

### Q3 — « … si j'améliore sa durée de vie (la charnière, en pièces par arête) ? »

**Chemin actuel** : la fiche montre « Charnière 50 · 90 réel » côte à côte, sans lien entre eux. Le calcul du gain mesuré **existe** — `bilanAnnuel` l. 7250-7253 (`gainMesure`, `gainMesureMoyen`, `gainMesureN`, `gainMesureBorneInf`) — et il est affiché… dans le pied de scénario replié (l. 9050, « mesuré (min, N essais) »). Le **verdict** (l. 6622 : `dCost` sur `coutsDetail` à la charnière **visée**) l'ignore, et l'avertissement l. 7688 le dit dans une infobulle que personne n'ouvre. C'est cohérent avec « jamais d'invention » (le visé est l'objectif) — mais l'exposition actuelle **trompe** : « 90 réel » affiché en gros, verdict 0 % en gros, la réconciliation en tout petit.

**Ce qui manque** : faire entrer le mesuré dans la réponse principale, **tamponné** pour ce qu'il est.

**Maquette** — sous le verdict, quand `gainMesure` existe :

> **Au vu du mesuré (90 p/arête, min sur N essais) : −9,1 k€/an** — au-dessus de la cible de 50 · horizon à confirmer (essai arrêté avant la charnière)

Et dans l'autre sens (mesuré < visé), le même bloc dit le surcoût réel : la charnière mesurée courte devient un coût affiché, pas une note de bas de page.

---

## 4. Autres constats

Chaque constat : où · preuve · correction · effort · test d'acceptation.

### P0 — faux ou trompeur (avant toute présentation)

**P0-1 — Une seule définition d'« acté ».** Où : `gainPoste` (l. 15903), `campagneCollecter` (l. 11461), `planRecapGains` (l. 19746), `accueilBandeauHTML` (l. 20630). Preuve : §2 C1-C5. Correction : une fonction pure unique, p. ex.

```
gainsActes(lignes) → { total, parPoste: [{ligne, opCode, gain, date, scenarios}], nbPostes }
```
règle proposée : *acté = tout scénario `statut:"serie"` non-baseline non-échec, gain = `bilanAnnuel(sc, op.config, ligne, ref, prodSc).gainAnnuel` (périmètre outillage, config de l'OP, `volumeAnnuel` fait foi), un poste = la somme de ses scénarios en série.* Consommateurs : bloc 01 de la Vue d'ensemble, bandeau du Plan, intro de la Campagne (qui garde sa timeline et ses jalons), kpi « Suivi d'essais — acté » de la vue générale. Un gain acté négatif s'affiche **comme tel** (« en série : −2,1 k€/an — coûte plus cher qu'avant »), il ne disparaît pas. Effort **M**. Test : fixture à trois cas (série-non-meilleur, série négatif, volume inactif) → les quatre écrans rendent **le même** total ; contre-regard : la campagne redivergente → porte tombe.

**P0-2 — Le gain acté remplacé par une promesse (C3).** Où : `gainPoste` l. 15903-15912. Preuve : EMAG 1 OP40 : campagne +7 449 acté, écrans +12 195 projeté. Correction : dans `gainPoste`, le meilleur scénario **en série** devient le porteur d'acté ; le meilleur absolu reste le projeté ; si le meilleur EST en série, acté = projeté (pas de double compte). Effort **S/M** (dans P0-1). Test : le cas EMAG 1 OP40 en fixture → `gainActe ≥ 7 449` et le projeté n'inclut plus le scénario en série.

**P0-3 — La campagne ignore la config de l'OP et le curseur de volume (C4-C5).** Où : `campagneCollecter` l. 11474 (`coutsDetail(sc, undefined, lg)`) et l. 11468 (`parseFloat(rf.productionAnnuelle)` brut). Preuve : HESSAPP OP15 → 0 vs −2 112 ; OP20 volume 426 000 compté alors que `volumeActif` est désactivé sur l'OP. Correction : utiliser `op.config` et `volumeAnnuel(rf, op.config)`. Effort **S**. Test : fixture avec deux configs divergentes → campagne et gainPoste égaux au centime. ⚠️ Attention au sens : corriger la campagne **change le 7 449 €/an affiché** — le nouveau total doit être annoncé à Benjamin avant déploiement.

**P0-4 — Le verdict ignore le mesuré sans le dire (Q3).** Où : `verdictHTML` l. 6622 ; `gainMesure` l. 7250, affiché l. 9050 seulement. Preuve : checkup Claude §P0-3 (S650 F0,25 : 50 visé / 90 réel / verdict 0 %) — mécanisme confirmé au code (le scénario lui-même n'existe pas dans rev435, voir §7). Correction : ligne « Au vu du mesuré : ±X k€/an (≥ si borne inférieure) » dans le verdict dès que `gainMesure !== null`, même libellé que la fourchette existante. Effort **S**. Test : scénario avec fins réelles → le verdict porte la ligne et son tampon ; sans fins réelles → pas de ligne.

**P0-5 — Deux totaux sur l'écran Plan (C6).** Où : l. 20188 vs l. 20272. Correction : un total principal (articles **engagés**), le second relégué en sous-texte nommé (« 23 articles ont une cible posée : −122 k€/an au total »). Effort **S**. Test : 3 cochés + 23 cibles → l'écran porte les DEUX nombres chacun avec son périmètre écrit.

### P1 — confus

**P1-1 — « manque : … » répété.** Où : l. 19521-19530 (`manques.push` **par référence** dans la boucle des refs d'un poste, sans dédup) rendu l. 19616. Preuve mesurée à l'écran : « volume annuel de production » ×**18**, « chiffrage du scénario candidat » ×**17** sur le seul écran Plan. Correction : `manques = [...new Set(manques)]` + préfixer par le nombre (« volume annuel (3 réf.) »). Effort **S**. Test : poste 3 réf. sans volume → une seule occurrence.

**P1-2 — Coquilles typographiques (toutes localisées).**

| Texte vu | Site | Cause | Fix |
|---|---|---|---|
| « 5,6 k€€/an restants » | l. 20647-20648 (`bloc2`) | `fmtEuroCourt` rend déjà « k€ » + unité « €/an restants » | `u: "/an restants"` |
| « 86,3 k€ € », « 12,1 k€ € » | l. 20138, l. 20160, l. 19632 | `fmtEuroCourt(x) + " €"` | retirer le « € » |
| « −-0,005 €/pièce · 2 112 €/an/an » | l. 11607 | `(tBase − t)` déjà signé inséré après « − » littéral ; `libelleAnnuel` finit par « /an » + « /an » | formater la valeur en valeur absolue ; retirer le « /an » |
| « + -4,1 k€(/an) » | l. 20074 et l. 20824 | `"+" + fmtEuroCourt(négatif)` sans garde de signe | `(v>0?"+":"")` comme le fait déjà `pipelineHTML` l. 20870 |

Effort **S** (une heure). Test : porte harnais qui balaye les rendus et interdit les motifs `k€€`, `€ €`, `/an/an`, `+ -` dans tout texte rendu (contre-regard : réinjecter une coquille → porte tombe).

**P1-3 — La bannière « Reprendre » emmène ailleurs sans nommer la ligne.** Où : l. 12294 — la bannière porte essai, date, scénario, dernier prélèvement, **pas la ligne ni l'OP**. Preuve : vue à l'écran le 10/11 (poste SNGN 090416 · PCI 4 OP40, bannière « Essai 1 · Classeur Matis · T6407 T0707 22/50 » — trois clics pour découvrir qu'on change de poste). Correction : préfixer « HESSAPP · OP30 — Reprendre… » (les données existent dans `rep`). Effort **S**. Test : la bannière d'un essai hors poste affiche ligne + OP ; un essai du poste courant ne les répète pas.

**P1-4 — Bloc 01 mensonger par wording.** Où : l. 20633 : « aucun gain acté — **premiers passages en série en attente** ». Preuve : un passage en série a EU lieu (HESSAPP OP15, et EMAG 1 OP40 acté invisible). Le texte dit « en attente » pour un fait accompli. Correction : résolu par P0-1 ; en attendant, le libellé du vide doit dire « aucun gain acté positif — 1 poste en série coûte plus cher qu'avant » (c'est une information, pas un vide). Effort **S**.

**P1-5 — Deux « Retour » qui ne font pas la même chose.** Où : « Détails/Essentiel » (spk-shell.js l. 434-435, replie le niveau de détail) et « ← Retour » (l. 795, referme l'espace de travail). Preuve : depuis le Plan, « Revenir à l'essentiel » ne referme pas le Plan → le clic paraît mort. Correction : renommer le toggle (« Essentiel ⇄ Détails » suffit) ou le faire refermer l'espace ouvert quand il est déjà en essentiel. Effort **S**. Test : interaction — Plan ouvert, clic Essentiel → soit le Plan se referme, soit le libellé ne promet plus un retour.

**P1-6 — Le Plan mélange trois consommations sans dire laquelle alimente quoi.** Où : `planLignes` l. 19899 (`sourceConso` : « 2025 » / « reelle » / « theo »), basculeur v4.88. Preuve : le tableau porte bien `sourceConso` par ligne, mais ni le total du bas ni le graphique n'écrivent « calculé sur : consommation 2025 ». Correction : porter la source active dans le libellé de chaque total (« économie simulée sur la conso 2025 : … »). Effort **S**. Test : changer `planSource` → les libellés suivent.

### P2 — confort

- **Cible posée sans volume = parcours sans issue** : Vue d'ensemble bloc 02 dit « cible posée sur 4 lignes — volume annuel à saisir » sans le geste qui y mène (vérifié à l'écran). Ajouter le lien « saisir les volumes » (ouvre la référence du premier trou). Effort S.
- **Écran « Réel vs budget » vide tant que le classeur n'est pas relu** : c'est documenté, mais l'écran pourrait porter la date de dernière lecture en tête (elle existe : `consoReelle.luLe`). Effort S.
- **Textes d'essai sans lieu de lecture d'un coup d'œil** : la mémoire 4.150 les journalise (serveur) ; il manque une vue « objectifs & conclusions des essais en cours » en tête de Synthèse (une liste : essai · objectif · conclusion · état). Effort M — à ranger derrière le besoin réel de Matis.

### Cohérence atelier / mobile

Rien à signaler sur cette passe : le mode atelier est cohérent (gants, 56 px acquis des versions précédentes) ; le problème de l'atelier est de **contenu** (Q2), pas de forme. Non testé sur iPhone (voir §7).

### Intégrité des données (synchro)

Lu au code : `syGardeEnvoi` (l. 22267) borne les envois ; les garde-fous 4.145 (suppression en masse) et le journal serveur des textes 4.150 (`sync_shards_textes`) sont en place côté code et CHANGELOG. **Non testé** : les triggers SQL réels et un cycle complet deux appareils (hors de ma portée ici — pas d'accès direct à la base, et la règle interdit d'écrire dans le cloud). Je n'ai **pas** trouvé de chemin qui supprime un texte ou un relevé sans trace dans le code client actuel ; la question serveur reste ouverte.

### Le langage commercial (ce que Benjamin peut dire sans la justifier)

Par écran, la phrase qui doit s'afficher **et** se dire, une fois P0-1 posé :

- **Vue d'ensemble, bloc 01** : « Nos essais ont déjà signé **+7,4 k€/an** d'économie d'outillage, sur deux postes. »
- **Plan, bandeau** : « **Signé : 7,4 k€/an. Prêt à signer : 7,7 k€/an** (validation en cours). En tout, le plan vise −122 k€/an sur 23 articles. »
- **Campagne** : inchangée — c'est déjà le bon écran pour la courbe à montrer en réunion (à condition que son total redevienne celui des autres).
- **Fiche scénario** : « avec la vie mesurée : −9,1 k€/an » plutôt que « 0 % ».

---

## 5. Plan d'action ordonné (une journée de Claude)

| Ordre | Lot | Contenu | Effort | Pourquoi cet ordre |
|---|---|---|---|---|
| 1 | **P0-1 + P0-2** | `gainsActes()` unique ; `gainPoste` crédite l'acté même non-meilleur ; brancher les 4 écrans ; un acté négatif s'affiche | M | Tout le reste en dépend : c'est LE chiffre que la hiérarchie lit |
| 2 | **P0-3** | Campagne : config de l'OP + `volumeAnnuel`. ⚠️ change le 7 449 affiché → prévenir Benjamin avec avant/après | S | Finit la cohérence du chiffre n°1 |
| 3 | **P0-4** | Le mesuré entre dans le verdict (tamponné) | S | Répond à la question « charnière » de Benjamin |
| 4 | **Bloc leviers** (Q1/Q2/Q3) | `levierPrix`/`levierVie` purs + affichage sur la carte poste, la fiche scénario et l'atelier (défaut : replié sur l'atelier) | M | La réponse « en un coup d'œil » aux trois questions |
| 5 | **P0-5 + P1-1 → P1-6 + P2** | Deux totaux nommés, dédup « manque », coquilles (P1-2), bannière, libellé bloc 01, Retour, sources de conso | S au total | Une passe de finissage, testable d'un coup par la porte anti-coquille |
| 6 | **Remplissage de données** (pas du code) | Volumes des 8 postes « insuffisants », 3 prix catalogue manquants, Vc/f, taux PCI 5, taux rebut — l'outil les liste déjà | — | À Matis/Benjamin ; la liste P2 du checkup tient |

Ordre de présentation à Benjamin : les totaux AVANT (l'ancien 7 449 changera au lot 2), le reste après.

---

## 6. Questions pour Benjamin (décisions qui lui reviennent)

1. **Définition d'« acté »** — ma proposition (P0-1) : tout scénario en série compte, y compris à gain négatif (affiché comme tel). Alternative : ne compter que les actés positifs et exposer les négatifs à part (« 1 poste en série en perte : −2,1 k€/an »). Laquelle devient la définition de la maison ?
2. **Le 7 449 €/an va bouger** (lot P0-3 : la campagne passera à la config de l'OP et au curseur de volume). Accepté que le chiffre « historique » affiché change, avec avant/après à l'écran ?
3. **Le levier au niveau ligne** (Q1) : veux-tu « −10 % prix **sur cette ligne** » (il faut ventiler la conso de l'article par ligne — la donnée existe dans les suivis hebdo Matis) ou le levier par article du Plan suffit-il, rapproché de la carte poste ?
4. **Le verdict peut-il être « mesuré »** quand la vie mesurée existe (P0-4), ou le verdict doit-il rester strictement « objectif visé » avec le mesuré dessous ?
5. **Atelier** (Q2) : la ligne d'argent en tête de saisie (P2, maquette Q2) est une info visible par les opérateurs — ok pour en faire un écran d'atelier, ou à réserver au pilote ?

---

## 7. Ce que je n'ai pas pu vérifier

- **Les données de Benjamin ne sont pas rev435** : la PROD sert la 4.150.0 mais mes écrans ont tourné sur l'export rev435 du 09/11 (exporté par Matis, 4.145.3). Les valeurs reproduites (7 449 / −2 112 / 0 / 0, les 18 « manque », le bloc 01) **coïncident avec celles du checkup de Claude fait sur la session réelle** — la convergence est une double validation. Mais : le **catalogue et `conso2025` sont vides dans rev435** (ils vivent dans la session de Benjamin) → les totaux du Plan −72,8 k€/an / −122 k€/an et les coquilles « k€ € » du Plan sont prouvés **au code** (lignes citées), pas reproduits à l'écran. Idem pour l'écran Catalogue et la vue générale 4.149.
- **Le scénario S650 F0,25 (HESSAPP OP30)** n'existe pas dans rev435 (créé dans la session locale de Benjamin après l'export) : le cas 50 visé / 90 réel est repris du checkup et prouvé au code (`verdictHTML` visé ; `gainMesure` l. 7250 ; rendu l. 9050), pas rejoué.
- **iPhone, relevés Marposs, import/export, impression A4, deux thèmes** : non testés (hors périmètre de cette passe « logique & évidence »).
- **Les triggers serveur** (`sync_shards_hist`, `sync_shards_textes`, garde-fous 4.145) : lus au CHANGELOG et au code client, non exécutés — pas d'accès base (et ne doit pas en avoir).
- **Le build** : `dist/` reconstruit localement pour l'analyse (idempotent, 4.150.0, 5 transformations) ; aucun fichier source du dépôt n'a été modifié, la PROD n'a pas été touchée (un seul chargement en lecture, sans session cloud).

---

*Analysé, proposé — rien tranché. Les lots 1 à 5 sont prêts pour un tour Claude avec tests d'acceptation ; les questions §6 attendent l'arbitrage.*
