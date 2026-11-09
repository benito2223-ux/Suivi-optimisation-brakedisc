# Demande à Hermes (ou Z Code / GLM) — coder l'étape 2 : les conditions de coupe se tapent une fois

De : Claude, Tour 133, 09/11/2026. Document auto-contenu : il se lit sans la conversation.

## 1. Où on en est

- Branche `ux-rail`, HEAD = Tour 133, version **4.150.1**, **790 tests | 0 échec**. Verrou libre.
- DEV et PROD servent la 4.150.1 (curl, empreinte identique au `dist/`).
- Benjamin a demandé une analyse de l'outil « au niveau du petit détail d'usage ». Son exemple :
  « il faut taper les conditions de coupe dans chaque fiche outil quand les outils travaillent en
  simultané, pas normal ».
- Deux documents font référence, à lire avant de coder :
  - `DETAILS_SAISIE_2026-11-09.md` — 15 frictions de saisie, mesurées sur PROD rev 436 ;
  - `REFONTE_OUTIL_CIBLE_2026-11-09.md` — la cible des écrans (plus tard).
- L'étape 1 (affichage seul) est livrée en 4.150.1. **Cette demande porte sur l'étape 2 uniquement.**

## 2. Le problème, chiffré (PROD rev 436, lecture seule)

| Constat | Mesure |
|---|---|
| Groupes d'outils simultanés | 10 |
| Groupes où Vc et f sont saisis sur plusieurs logements | 9, et **9 fois sur 9 les valeurs sont identiques** |
| Outils à plusieurs logements avec Vc saisi | 8 sur 8 identiques, 3 à moitié remplis |
| Scénarios avec Vc/f renseignés | 18 sur 86 |
| Scénarios dont le **nom** porte les conditions (« … G96 S800 F0,25 ») | 6 |
| Champ pour le mode G96 / G97 | aucun : des « G97 S700 » sont saisis 700 dans « Vc m/min » |
| Essais dont la copie de conditions diverge du scénario | bandeau « ⚠ modifié depuis : T548·D1 Vc 700→800 — Aligner sur le scénario » |

Trois défauts, une seule cause : la vitesse appartient à la broche (donc au groupe simultané), et
l'outil la fait saisir par logement, sans dire dans quelle unité, et laisse la réécrire après l'essai.

## 3. Ce qu'il faut coder

### 3.1 Décision d'architecture (prise, ne pas la rouvrir)

**Le rangement des données ne change pas.** `vc`, `f`, `kappaR`, `rayonBec`, `apPiste`, `tempsCoupe`
restent sur chaque logement, format 8 inchangé. On change **l'endroit où on les tape** : une saisie
au niveau du groupe est **recopiée à l'écriture** dans tous les logements du groupe.

Pourquoi : aucun calcul existant n'est à réécrire (cycle, coût, copie d'essai lisent le logement),
aucune migration, aucun point de non-retour, et un export fait avant ou après reste lisible par
toutes les versions. C'est ce qui permet de livrer cette étape **sans attendre** l'export complet
(lot 0 de la refonte), qui reste le préalable des étapes 3 à 5.

### 3.2 Le bloc « Conditions de coupe » du groupe

- Un **groupe** = un outil et tous les suivants cochés « simultané avec le précédent »
  (`simultaneAvecPrecedent`, calcul déjà fait trois fois : vers les lignes 6998, 7500 et 11019 —
  en profiter pour n'en garder qu'une fonction, `groupesSimultanes(sc)`).
  Un outil seul est un groupe d'un outil : même bloc, même code.
- Le bloc s'affiche **une fois, en tête du groupe** dans la fiche (`outilCarteHTML`, ligne ~11660,
  et `logementBlocHTML`, ligne 10769). Champs : mode, vitesse, avance, κr, rε, ap.
- **Vitesse** : commune au groupe, non modifiable par outil (même broche).
- **Avance, κr, rε, ap** : héritées par chaque logement, avec un lien « différent sur cet outil »
  qui rouvre le champ sur le logement. Cas absent des données (0 sur 9) : le prévoir, sans plus.
- Dans les logements, les champs correspondants **disparaissent** tant qu'ils valent la valeur du
  groupe. `tempsCoupe` reste par logement (il dépend de la longueur usinée).
- **À l'ouverture d'un scénario existant** : si tous les logements du groupe ont la même valeur
  (ou vide), le bloc l'affiche. S'ils diffèrent, le bloc affiche « valeurs différentes selon
  l'outil » et les champs restent visibles sur les logements : **ne rien écraser en silence**.
  Les 3 logements à moitié remplis reçoivent la valeur du voisin seulement quand l'utilisateur
  retouche le bloc.

### 3.3 Le mode G96 / G97

- Nouveau champ **additif** `modeVitesse` : `"G96"` | `"G97"` | absent. Porté par le logement comme
  les autres conditions (recopié par le bloc). Absent = non renseigné, rien n'est deviné.
- Le libellé et l'unité du champ vitesse suivent : « Vc (m/min) » en G96, « S (tr/min) » en G97.
  En G97 la valeur reste rangée dans `vc` **avec** `modeVitesse:"G97"` — ou, mieux, dans un champ
  `sBroche` distinct : à trancher en lisant qui consomme `vc` (calcul du temps de coupe surtout).
  Règle : **aucun calcul ne doit lire des tr/min comme des m/min.** Si un calcul a besoin d'une
  Vc et que seul S est connu sans diamètre, il affiche « non calculable », pas un chiffre.
- **Aucune conversion automatique des données existantes.** Proposer à l'utilisateur, une fois, la
  liste des scénarios dont le nom contient `G97` ou `S\d{3,4}` pour confirmer le mode. Il valide
  ligne par ligne ; la valeur tapée n'est jamais modifiée.

### 3.4 L'essai fige ses conditions

- La copie existe déjà : `snapshotLogements(sc)` (ligne 4234) → `essai.params.logements`.
- Afficher les conditions figées **en tête de l'essai** (mode, vitesse, avance par groupe).
- Le bouton « Aligner sur le scénario » (lignes 10452 et ~13099) **ne s'affiche plus dès que
  l'essai a un relevé**. Sur un essai sans relevé il reste. À la place, sur un essai avec relevés :
  « Nouvel essai avec les conditions actuelles ».
- Le bandeau « modifié depuis » devient une information (« le scénario a changé depuis cet
  essai »), pas une invitation à réécrire.
- Y ajouter `modeVitesse` dans la copie.

### 3.5 Hors périmètre de cette étape

Ne pas toucher : le choix d'article dans une liste (étape 3), les champs Correcteur et les noms de
logement (étape 3), le relevé à une ligne par pièce (étape 4), les tolérances par OP et le coût
mesuré (étape 5), le nom automatique des scénarios (ne renommer aucun scénario existant).

## 4. Critères d'acceptation

1. Sur un groupe de 2 outils simultanés, taper la vitesse et l'avance **une fois** remplit les
   logements des deux outils ; un export montre les mêmes valeurs sur chaque logement.
2. Un scénario existant dont les logements divergent s'ouvre sans qu'aucune valeur ne change
   (test : export avant = export après, octet pour octet sur les logements).
3. Décocher « simultané » sépare le groupe : chaque outil garde ses valeurs.
4. En G97, aucun écran n'affiche la valeur avec l'unité « m/min ».
5. Un essai avec relevés ne propose plus « Aligner ».
6. Les 790 tests passent, plus des tests neufs pour 1 à 5. Contrôle de comptage sur un export
   réel : 86 scénarios, 16 essais, 192 relevés, avant comme après.
7. Vérifié **à l'écran**, pas seulement par les tests : fiche à 2 outils simultanés, fiche à un
   outil, essai avec et sans relevé.

## 5. Règles du dépôt à respecter

- `VERROU.md` avant d'écrire dans `bilan_economique.html`, libéré en fin de tour ; un tour = un
  commit ; le tour s'écrit en tête de `ECHANGES.md` ; `CHANGELOG.md` et `NOUVEAUTES` à jour.
- Tests : `python build_harness.py sortie.js` puis `node sortie.js`.
- Publication : `node outils/build-coque.mjs` puis `surge dist <domaine>` ; seul le curl fait foi.
  **Jamais de déploiement sans l'accord explicite de Benjamin, à chaque fois.**
- Constitution §5.6 : aucun chiffre non justifiable à l'écran.
- Rien de visible ne montre le coefficient thermique ni la puissance requise ; l'épaisseur de
  copeau s'appelle « épaisseur de copeau ». Nuances en nom SPK. L'outil ne s'appelle jamais
  « CRM ».
- PROD en lecture seule pendant les contrôles : ne rien saisir, ne pas ouvrir le Dossier de visite.
- Piège connu : `allerVers(...)` enregistre la position ; la restaurer après un contrôle.

## 6. Ce que je n'ai pas vérifié — à lire avant de s'y fier

- Je n'ai lu ligne à ligne que `outilCarteHTML`. `logementBlocHTML` et le formulaire d'essai sont
  connus par l'inventaire de l'écran, pas par le code : **les numéros de ligne ci-dessus sont des
  repères, à confirmer**.
- Je n'ai pas recensé tous les lecteurs de `vc` : c'est la première chose à faire avant 3.3.
- Le format téléphone n'a pas été contrôlé.
- Une erreur de mon analyse a été rectifiée : l'écran lit bien `name` ; le champ `nom` des
  scénarios est un reliquat non affiché (voir `DETAILS_SAISIE`, B2).

## 7. La suite, pour mémoire (ne pas coder maintenant)

| Étape | Contenu | Préalable |
|---|---|---|
| 3 | Article choisi dans la liste (26 articles pour 377 logements), T/D numériques, un seul Correcteur, retrait de `nom` | export complet + liste « à trancher » |
| 4 | Relevé : une ligne par pièce, en-tête réduit au but, clôture en 3 choix | idem |
| 5 | Tolérances par référence × OP, coût « prévu » et « mesuré » côte à côte | idem |

Questions ouvertes pour Matis (pas pour le code) : les arêtes divergentes sur Z000 522 436 (2/3),
IM02 137 020 (8/2), Z000 539 100 (4/8) — erreur de saisie ou arêtes réellement utilisables ?
