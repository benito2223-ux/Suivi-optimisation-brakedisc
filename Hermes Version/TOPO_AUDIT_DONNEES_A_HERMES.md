# TOPO À HERMES — audit complet des données requis (01/10/2026, Z Code)

> **Demandé par Benjamin** : « prépare un topo pour que Hermes repasse tout ».
> Trois symptômes consécutifs remontés par Benjamin **en utilisant l'outil avec ses
> vraies données** (retours d'usage n°1 à n°5, tous réels, aucun rejeté).
> **Ce document est une passation d'audit : les faits sont mesurés, les causes
> possibles sont séparées des certitudes, et rien n'a été corrigé sans tracer.**

---

## 0. L'état de l'art, en une phrase

Le cadre est bon (navigation, design, migrations à la demande), **mais les données
du suivi et le classeur de Matis racontent des histoires différentes à trois
endroits**, et seule une passe d'audit ligne par ligne — avec Matis — peut dire
qui a raison.

---

## 1. Les faits mesurés ce jour (harnais + navigateur + openpyxl)

### 1.1 HESSAPP — « T1 avec 7 logements, aucun correcteur » (Benjamin)

**Mesuré dans les données réelles** (scénario « base excel », DV302x26RPI, OP10) :

| outil « numéro » | logements | noms |
|---|---|---|
| **T1 D1** | **4** | Plaquette ×4 |
| **T1 D2** | **2** | Plaquette ×2 |
| **T1 D3** | **1** | Plaquette |
| **T1** (OP15, scénario « Process actuel - ») | 1 | Logement 1 |

**Benjamin compte 7** (= 4+2+1) **et dit que T1 n'a que 3 logements.**
Diagnostic : l'import 4.72 a créé UN OUTIL PAR (position × feuille) — T1 D1 porte
4 logements parce que T1 D1 apparaît sur 4 feuilles du classeur (une « Plaquette »
par feuille, chacune avec son MABEC/prix/DDV). La règle atelier (Benjamin) : **T1
a 3 logements (D1, D2, D3), chaque logement a UNE plaquette et SON correcteur**.

**À faire** : regrouper T1 D1+D2+D3 en un outil T1 à 3 logements (D1, D2, D3) en
conservant le MABEC/prix/DDV de la feuille la plus récente par logement — et
auditer T2 (D1×2 + D2?), T5 (D1 seul), T6 (D1×2, D2×1, nu ×1) pareil. La fonction
`reparerOutilsD1D2()` groupe par clé de porte et nommerait les logements, MAIS le
cas « plusieurs logements par outil déjà » (4 « Plaquette ») dépasse son périmètre
actuel (elle fusionne des OUTILS, pas des logements en double À L'INTÉRIEUR d'un
outil). **Extension nécessaire avant de lancer quoi que ce soit.**

**Pourquoi ma migration 4.74.0 n'a pas regroupé T1** : hypothèse forte — elle a
tourné AVANT que les données de l'import 4.72 n'arrivent dans le suivi suivi de
Benjamin (ordre des sauvegardes/fusions cloud à dater via `etat_historique`).
À vérifier, pas à supposer.

### 1.2 EMAG 3 — « les éléments d'EMAG 1 dans EMAG 3 » (Benjamin)

**Mesuré** : le scénario « base excel » d'EMAG 3 (DV 330x28 RPE K0) contient
T517 D1/D2, T519A D1/D2, T511 D1/D2, T521 D1/D2, T529 D1, T5211 D1/D2, T525 D1
(OP10) et T546 D1, T548 D1, T549 D1, T543 D1/D2 (OP40) — **et le classeur de
Matis dit EXACTEMENT la même chose** : la feuille « Cout pièce E3 330x28 RPE K0 »
liste ces outils (vérifié openpyxl, lignes 4-140). L'import est fidèle.

**Les deux hypothèses — à trancher par Matis, pas par nous** :
- (a) ces porte-outils sont réellement partagés EMAG 1 ↔ EMAG 3 (cohérent avec la
  règle de réutilisation des plaquettes) ;
- (b) la feuille E3 du classeur est une copie de la feuille E1 mal mise à jour.

### 1.3 Le scénario KY3500 « dans EMAG 3 » (Benjamin)

**Mesuré dans les données actuelles** : le scénario « Process actuel - finition
piste DWG 1743941R01 KY3500 ★ » (en série, avec l'Essai 1 du 22/09 et ses 12
prélèvements) vit **UNIQUEMENT sur EMAG 1 · DV 356x26 · OP40**. Il n'existe
AUCUNE occurrence sur EMAG 3.

**La capture de Benjamin** le montre pourtant sélectionné sous la barre de
contexte « EMAG 3 · DV 330x28 RPE K0 · OP10 Ebauche piste ». **Non résolu.**
Deux suspects, aucun tranché :
- (a) onglet périmé (le cache/code d'avant la 4.73) — MAIS Benjamin affirme avoir
  rechargé, et la purge SW a été faite depuis ;
- (b) un bug de navigation réellement reproductible — **à reproduire avec les
  étapes exactes** (par quel bouton, depuis quel écran). Demander à Benjamin de
  refaire le chemin en notant chaque clic.

**Suspect technique à auditer** : le ménage de mes migrations (4.74.0/4.74.1) a
réassigné `sc.outils` scénario par scénario — vérifier dans `etat_historique`
(20 versions cloud) à quel moment le contexte EMAG 3 a pu pointer le scénario
KY3500, et si un `switchReference/switchOp` a un jour écrasé un `activeId` de
travers. **Ne rien corriger avant d'avoir daté.**

---

## 2. La loi de vocabulaire (Benjamin, à écrire dans la constitution)

> **« Un correcteur qui se trouve dans l'excel de Matis est un logement. La
> machine appelle un outil et y ajoute le correcteur correspondant au logement
> pour avoir le point de départ de l'usinage. »**

Conséquences :
- colonne A du classeur (« N° d'outil / N° correcteur ») = porte-outil + logement ;
- **le correcteur DOIT apparaître** : champ Correcteur de l'outil (4.74.2) et
  dans le nom des logements (D1, D2 — fait par `reparerOutilsD1D2`) ;
- **jamais « DTV » ni « voile »** dans une interface : battement, Ra, épaisseur
  piste (+ convexité, face, appui — ⚠️ « face appui » : une ou deux mesures ?
  ambiguity non tranchée, ne pas coder avant réponse) ;
- l'ISO (colonne C) = la référence plaquette → `logement.ref` (corrigé 4.74.2).

---

## 3. Les chantiers pour l'audit, dans l'ordre

1. **dater la contamination** (1.3) : `etat_historique` (20 versions cloud) —
   à quel moment le contexte EMAG 3 a-t-il montré le KY3500 ? Reproduire
   d'abord avec les étapes exactes de Benjamin ;
2. **l'extension de `reparerOutilsD1D2`** au cas HESSAPP (1.1) : fusionner les
   logements en double À L'INTÉRIEUR d'un outil (garder le MABEC/prix/DDV de la
   feuille la plus récente), puis regrouper les positions en un outil —
   contre-regard obligatoire, et **Benjamin ne clique plus « Corriger
   maintenant » avant** (gel prudent : les corrections existantes sont sûres
   et testées, mais chaque nouvelle passe sur des données non auditées
   accumule du risque) ;
3. **la reconciliation ligne par ligne avec Matis** : pour chaque couple, les
   outils du classeur vs les outils du suivi — le cas E3 (1.2) tranché par
   elle ;
4. **la constitution** : vocabulaire (§2 ci-dessus) + la règle du test d'usage
   (proposition Tour 36) + le contrôle de version au démarrage (deuxième
   incident d'onglet périmé — Benjamin ET le harnais) ;
5. **le message à Matis** : ajouter la question E3 (1.2) aux 7 demandes
   existantes.

---

## 4. Ce qui est VRAI et n'est pas en cause (pour ne pas ré-auditer en boucle)

- le lecteur du classeur est fidèle au fichier (vérifié openpyxl contre le
  rendu, Tour 34 + ce jour) ;
- la migration D1/D2 ne mélange pas les lignes : elle opère scénario par
  scénario, et ses 6 tests verrouillent la conservation des champs ;
- le contraste, les 430+ tests métier et le harnais sont verts ;
- l'écran Classeur Matis et son bouton de lecture sont fonctionnels (4.73.1/2).

---

## 5. Ce que Benjamin doit faire (rien de technique)

1. **envoyer le message à Matis** (7 demandes + la question E3) — c'est LE
   goulot, tout le reste tourne en rond sans les données ;
2. **ne plus cliquer « Corriger maintenant »** jusqu'à la fin de l'audit
   (gel prudent — les corrections déjà appliquées restent) ;
3. **refaire le chemin KY3500/EMAG 3 en notant chaque clic** (ou nous
   l'observer faire) pour reproduire 1.3 ;
4. regarder la nouvelle peau et l'accueil à froid — le test de réussite
   reste le sien.

---

*Z Code — 01/10/2026. Tout est commité sur `dev` (4.75.0), rien vers la prod.
Verrou libre. Le harnais est prêt pour l'audit (434 tests + contraste +
`__DIAG__` paramétrable).*
