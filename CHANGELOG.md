# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donnée à part).

## [4.55.0] — 2026-09-29

**Option C de l'analyse du classeur Matis : on mesure avant de décider.**
L'outil apprend à lire le classeur de consommations que Matis tient déjà, et
affiche l'écart entre ce qu'il budgète et ce que l'atelier consomme réellement.

### Ajouté — la lecture du classeur Matis
- **bouton « Classeur Matis »** (barre d'outils, à côté de « Carte atelier ») ;
- **lecteur `.xlsm` / `.xlsx` intégré, sans dépendance** : le fichier est une
  archive ZIP, son XML est lu directement et décompressé avec
  `DecompressionStream` (natif Chrome/Edge) — « un seul fichier, zéro appel
  réseau » reste vrai, rien à installer ;
- **`matisLecture` est un constat, jamais un import** : la lecture n'écrit rien
  dans les données du suivi. C'est délibéré — la décision « la production réelle
  devient-elle une entité » doit s'appuyer sur des mesures, pas sur un choix
  fait à l'avance ;
- chaque feuille « Cout pièce » est lue comme un couple **ligne × référence** :
  production (case B1), outils avec numéro, article, **MABEC**, CPP théorique,
  CPP réellement consommé, écart ; les 4 OP et 37 outils sont ainsi lisibles ;
- **écran « Réel / Théorique »** : budget-outillage annuel, consommation réelle
  annuelle, écart en € et en %, un tableau par couple, et un **détail par outil** ;
- chaque écart porte **sa raison en toutes lettres** (« surconsommation de
  0,1763 €/pièce », « non mesurable — pas de CPP réel relevé ») — jamais un
  chiffre nu (constitution §3.5) ;
- un couple **sans production** reste `null` et non `0` : « pas de mesure » ne
  doit jamais se lire « rien à consommer ».

### La première mesure, sur le classeur du 14–21/09/2026

| Couple | Production | Théorique | Réel | Écart |
|---|---|---|---|---|
| E1 356x26 RPI | 6 781 | 2 423 € | 3 618 € | **+1 196 €** |
| E2 330x14 | 2 490 | 1 355 € | 2 409 € | **+1 054 €** |
| E3 330x28 RPE K0 | 4 180 | 941 € | 1 471 € | **+530 €** |
| E2 290x12 | 2 234 | 499 € | 680 € | **+181 €** |
| **Total** | | **5 218 €/an** | **8 179 €/an** | **+2 961 €/an (+57 %)** |

**Lecture** : le budget-outillage sous-estime la consommation réelle d'environ
57 %. Ce n'est pas une erreur de saisie du classeur, c'est l'écart entre un modèle
et le terrain — l'outil budgète un CPP théorique à partir des prix et des durées
de vie, le terrain en consomme un CPP différent. C'est un **constat à traiter**,
pas une faute : il faudra décider s'il se corrige par des durées de vie plus
sûres, ou par un poste d'écart assumé.

### Tests
283 → **294** (11 nouveaux) : lecture d'un couple, production, CPP théorique/réel,
écart et écart annuel, couple non produit (null et non 0), libellés d'écart,
tri du récapitulatif, et le fait que la lecture n'écrit rien. Le lecteur a en
outre été validé **hors outil** sur le vrai classeur de Matis (les chiffres
obtenus concordent avec une lecture Python indépendante). Tout est vert.

## [4.54.0] — 2026-09-29

**La fiche poste (couche 1)** — la porte qui manquait entre la carte et le
détail. Décision **D1-SÛRE** (Benjamin) : le poste reste **dérivé** — aucun
changement de format, aucune migration — mais la couche 1 existe et devient un
point d'entrée réel.

### Ajouté — la fiche du poste
- **Survol (desktop) ou premier toucher (tablette)** sur une tuile → la fiche
  s'ouvre **dans la carte**, pas dans un second panneau : c'est la couche 1 du même
  écran, donc le retour n'est jamais une question ;
- elle répond à la seule question qui compte en atelier — *« qu'est-ce qui se
  passe sur CETTE machine ? »* : la référence principale, les références qui y
  travaillent, leur statut, leurs gains, le chemin vers la cible ;
- **la porte explicite « Ouvrir le poste → »** vers la couche 2 (v4.52) : le geste
  double (R3) devient découvrable — personne n'a à deviner qu'un second geste
  entre dans le détail. Un poste d'« opportunité » n'expose pas de porte morte ;
- **`prochaineEtapePoste()`** : l'information qui manquait le plus, en toutes
  lettres — « Terminer le protocole 5× — 2/5 essais relevés », « Cible du site
  posée, aucune mesure », « Jamais travaillé ». Elle se **déduit de l'état**
  (constitution §3), donc elle ne peut pas mentir ;
- survol, toucher **et** clavier (Entrée/Espace) ouvrent la fiche ; le survol n'écrase
  jamais une fiche déjà ouverte (on ne la substitue pas sous les yeux du lecteur) ;
- la fiche survit au changement de filtre si le poste reste visible, et se referme
  proprement sinon — pas de fiche orpheline.

### Corrigé — « 0/5 essais » sur un poste en production
La fiche affichait le compteur de protocole y compris pour une machine déjà en
série, ce qui laissait croire à une absence de travail — exactement le chiffre
mensonger que la constitution §3.5 interdit. L'avancement n'est affiché que pour
un protocole réellement en cours.

### Tests
270 → **283** (13 nouveaux) : prochaine étape selon l'état, rendu de la fiche
(machine, ligne, référence, porte, étape, état en toutes lettres), gain identique à
celui de la tuile (D3), pas de porte sur une opportunité, pas de « 0/5 » en série.
Tout est vert.

### Dette documentaire repayée dans le même commit
Le CHANGELOG avait perdu l'entrée **4.51.2** (la carte) et l'entrée **4.53.0**
(livraisons) n'avait jamais été écrite ; l'ordre était cassé (4.52/4.53 après
4.49.3). Les trois entrées sont restaurées, ordonnées et uniques.

## [4.53.0] — 2026-09-29

Décision 3 de la constitution : **la livraison**, l'objet que la hiérarchie lit.

### Ajouté — les livraisons (instantané figé et daté)
- Une **livraison** est un instantané FIGÉ des gains du plan (gains actés, gains
  en cours, plan par poste, cibles du site, nombre d'essais) : **elle ne se
  recalcule jamais**, c'est le document que Matis montre à sa hiérarchie
  (« livré en date du…, X €/an actés ») ;
- créée depuis la carte atelier, listée dans le dossier, imprimable en A4 ;
- **source unique** : `creerLivraison()` consomme `cartePostes()`, exactement
  comme l'affichage de la carte — aucune somme recalculée à la main ;
- elle **voyage avec la donnée** : cloud, export et fusion (cumul sans doublon),
  `normalizeLivraison()` n'assurant que la forme — l'exactitude est figée.

> Note de rédaction : cette entrée a été ajoutée par Hermes le 29/09, Z Code ayant
> livré la 4.53.0 sans écrire son entrée CHANGELOG.

## [4.52.0] — 2026-09-29

Phase 1 de la carte atelier (spec croisée Hermes × Z Code, arbitrages
Benjamin) — implémentée par Z Code après validation du socle 4.51.0/4.51.1
d'Hermes.

### Ajouté — couche 2 : « Ouvrir le poste → » et retour carte
Chaque tuile actionnable de la carte porte **« Ouvrir le poste → »** :
un clic positionne la navigation experte (ligne › référence › OP) sur la
prod du poste (★ puis excel) et referme la carte. Depuis la zone
Traçabilité, un bouton **« ⇠ Carte atelier »** permet de revenir — jamais
de cul-de-sac entre les deux lectures (A1).

### Ajouté — l'A4 Mission (livrable hiérarchie, imprimable)
Bouton « 🖨 A4 Mission » dans la carte : un imprimable qui raconte la
démarche de Matis — gains **ACTÉS** en production, gains **EN COURS**
(validés ou en essai), timeline des essais récents avec prélèvements,
plan poste par poste, le protocole 5× et le partenariat SPK by CeramTec.
**Une seule source de vérité** : l'A4 consomme `gainPoste()` — la carte,
le bandeau et l'A4 ne peuvent pas diverger (A3).

### Ajouté — défense serveur (rappel du round)
Trigger Postgres `preserve_cibles_cpp` : testé en production — un push
intégralement strippé atterrit avec les 6 cibles réinjectées.

## [4.51.2] — 2026-09-29

**La carte atelier (couche 0, lecture seule).** L'écran d'entrée spatial de
l'outil : une tuile par machine, lisible en un coup d'œil, avant toute saisie.

### Ajouté — la carte
- **Bouton « Carte atelier »** dans la barre d'outils, à côté du Tableau de bord
  (qui reste vivant : la décision d'entrée par défaut se prend après la recette A2) ;
- **`cartePanel`**, mécanique `ouvrirPanneau` existante, rempli par `renderCarte()` ;
- **Tuiles = (ligne déclarée × machine déclarée)** de `LIGNES_SEPT_FONS` (v4.50) :
  l'usine entière est dessinable, un poste déclaré mais jamais travaillé reste
  visible. Aucune tuile n'est inventée ;
- **Quatre états**, tous portés par la classe **et** par le mot — jamais la couleur
  seule (lisibilité daltonienne, mode nuit, impression) : `gagne` (vert, gain
  acté), `encours` (bleu, essai ouvert ou gain projeté), `aChiffrer` (ambre, cible
  posée sans mesure), `opportunite` (gris, poste déclaré non travaillé) ;
- **Pouls = 2 chiffres maximum** (D2) : €/an **acté** en gros, €/an **projeté** en
  dessous. Un poste sans gain n'affiche **jamais « 0 € »** : il affiche sa cible
  (« à chiffrer ») ou son silence (« jamais travaillé ») ;
- **Chemin prod → cible** affiché quand il existe, plafonné à 100 % ;
- **Multi-références** : référence dominante (plus gros volume) + compteur « +n réf. » ;
- **Filtre « mon projet / toute l'usine »**, défaut = le projet actif (H1-b), avec
  son propre état (indépendant du filtre du tableau de bord) ;
- **Recette A2 affichée** : la carte dit elle-même combien de ses tuiles portent
  une information actionnable, et signale le « carte creuse » sous 1/3.

### Corrigé — un poste à chiffrer était invisible
`gainPoste()` faisait sortir de `refs` toute opération sans prod chiffrable, donc
une référence qui porte une `cibleCPP` sans aucune mesure tombait en « opportunité »
— **l'invitation que l'atelier doit voir disparaissait**. La cible se lit désormais
avant tout calcul de coût, et l'opération reste visible (marquée `nonChiffre`) sans
contribuer à un gain. C'est le cas H1(a) : « à chiffrer » est une invitation, pas
une absence.

### Corrigé — la tuile affichait « aucune référence »
`refDominante` est l'entrée `{ ref, volume, … }` du tableau, pas l'objet référence :
le rendu faisait `ref.ref.nom` et affichait « aucune référence » alors que la
dominante existait. Six tests verrouillent désormais le **rendu** (nom de machine,
état, référence dominante, compteur, cible), pas seulement le calcul.

### Décision (a) — le contrat du coût machine est écrit
`pieceCPPComplet()` (4.49) appelle `coutsDetail()` **sans la ligne**, ce qui retombe
sur `getActiveLigne()` : correct **parce qu'il ne s'appelle qu'en contexte de
référence ouverte**, fragile autrement (écart mesuré ×19 sur une ligne à taux
horaire). Le contrat est désormais écrit dans les deux modules : le coût machine
exige la ligne du poste ; la carte et l'A4 Mission consomment `gainPoste()`.
Aucun changement de comportement.

### Tests
246 → **267** (21 nouveaux) : topologie déclarée, les quatre états, référence
dominante, filtre projet (dont le cas des étiquettes à quadruplet exact), recette
A2, et le rendu de la tuile. Tout est vert.

## [4.51.1] — 2026-09-29

Correctif issu de la **revue croisée Z Code** de la 4.51.0 (§2 : divergence
sémantique sur `coutEnCours`).

### Corrigé — un gain réalisé fait enfin bouger le chemin prod → cible
- **Le fait** : `pieceCPPComplet()` (v4.49) crédite le meilleur scénario
  *sans condition de statut* — `meilleur.cout < tBase ? meilleur.cout : tBase`.
  Ma 4.51.0 ne créditait que le **projeté**. Conséquence : sur un poste dont le
  nouveau outillage est passé en série, `coutEnCours` restait au coût de prod, le
  chemin affichait **0 %**, et le gain réalisé ne vivait que dans `gainActe` —
  donc **invisible dans le coût**, sur la barre que la hiérarchie regarde.
- **La correction** : `coutEnCours` suit désormais la formule du module de
  référence, mot pour mot. D3 (source unique) prime : deux modules ne doivent
  jamais raconter deux histoires différentes sur le même poste.
- **Décision d'usage** : « en cours » = ce que la pièce coûte **aujourd'hui**,
  gains réalisés compris. C'est la lecture qui sert l'objectif « mettre en avant
  les gains de Matis ».
- **Verrouillé par deux tests** : un poste entièrement acté fait avancer le
  chemin ; la formule est identique à celle de `pieceCPPComplet`. Le chemin se
  plafonne à 100 % quand le gain dépasse la cible (pas de « 175 % atteint »).
- 244 → **246** tests, tout vert. Aucun changement visible à l'écran (la carte
  n'est pas encore dessinée) — c'est la 4.51.2 qui la rendra lisible.

## [4.51.0] — 2026-09-29

Phase 1 de la carte atelier, **socle de calcul uniquement — aucun changement
visible à l'écran**. Ce que la carte consommera, et l'A4 Mission plus tard, est
donc écrit, testé et juste avant d'être dessiné.

### Ajouté — le calcul pur du poste (ligne x opCode)
- `postesLigne()` : les tuiles suivent les machines **déclarées** par ligne
  (`LIGNES_SEPT_FONS`, v4.50), jamais les scénarios rencontrés — une ligne non
  déclarée ne dessine aucune tuile ;
- `scenariosPostes()` : un poste se retrouve par **code** d'OP, pas par son nom
  libre (« OP 30 Perçages » et « OP30 » sont le même poste) ;
- `gainPoste()` : somme, référence par référence, des gains d'un poste servi par
  plusieurs références (cas réel EMAG 1 : 356x26 + 304x28) ;
- `etatTuile()` : les quatre états (gagné / en cours / à chiffrer / opportunité)
  dans une **fonction unique** — jamais une cascade de `if` dans le HTML.

### Décisions de calcul (à relire avant de dessiner)
- **Rappel D3** : le gain passe par `bilanAnnuel()`, donc par
  `perimetreCompare()` (v4.45) — jamais une soustraction de deux totaux bruts. La
  tuile ne pourra donc jamais afficher un chiffre que le bandeau d'un scénario
  n'afficherait pas ;
- la prod d'une OP reste **★ d'abord, excel en repli** (v4.49.4) ;
- une OP **non chiffrable sort du calcul** et est comptée dans `nonChiffres` :
  elle ne se dégrade jamais en « gain de 0 € » ;
- gain **acté** = scénario en série ; **projeté** = le reste. Les deux ne sont
  jamais sommés ensemble ;
- la cible et le chemin prod → cible viennent de la **référence dominante**
  (le plus gros volume de série) : une tuile multi-références n'affiche qu'une
  seule cible, sinon deux chiffres se contredisent ;
- un poste déjà sous sa cible n'affiche **aucun chemin** (il n'y en a pas).

### Tests
224 → **244** (20 nouveaux) : topologie déclarée, appariement par code, gain
acté calculé à l'euro près, multi-références, cas asymétrique réel (OP non
chiffrable), les quatre états, référence dominante, bornes 0-100 du chemin.
Tout est vert.

## [4.50.0] — 2026-09-29

Début de la phase « carte atelier » (vue en tuiles machines, spec croisée
Hermes × Z Code arbitrée par Benjamin — décisions : topologie dérivée par
opCode + déclaration des machines en constante, carte ouverte sur le
projet avec l'usine entière à un clic, écran d'abord puis A4 Mission).

### Ajouté — socle technique de la carte (aucun changement visible)
- **`opCode` dérivé** à la normalisation de chaque OP (motif OP+digits,
  insensible aux espaces et zéros de tête) : « OP 30 Perçages » et
  « OP10 Ebauche piste Inter » tombent respectivement dans OP30 et OP10 ;
  sans code exploitable, opCode vaut « ? » et la future carte ne dessine
  pas de tuile fantôme.
- **Topologie machines déclarée** dans `LIGNES_SEPT_FONS` (constante du
  semis v4.27) : EMAG 1 OP10/20/30/40, EMAG 2 OP10/30/40, EMAG 3
  OP10/40, HESSAPP OP10/15/20/40 — les lignes sans données connues
  (Weisser, PCI) restent à compléter par l'atelier.

## [4.49.4] — 2026-09-29

Retour Benjamin : sur EMAG 1 / DV 356x26, l'OP40 et l'OP20 manquaient au
coût pièce complet.

### Corrigé — toutes les OPs comptées, les absentes visibles
- **Le coût de prod d'une OP = d'abord la prod réelle (★), l'excel en
  repli.** Après le merge OP40 (DWG ★ remplaçant le scénario excel), le
  bandeau ne cherchait que les « base excel » : l'OP40 avait disparu du
  décompte. Vérifié : 356x26 = 0,763 € (OP10 0,174 + OP40 0,539 +
  OP30 0,050), le meilleur essai par OP suit (SL500 −0,058 € sur l'OP40).
- **Une OP sans scénario chiffrable s'affiche « non chiffrée — à
  compléter »** au lieu de disparaître (l'OP20 de la 356x26 attend ses
  valeurs : le « Process actuel » de Matis y a des outils sans
  prix/charnière).

### Sécurisé — défense serveur contre les clients périmés (3e strip à 05h42)
Le client périmé poussait en boucle : chaque restauration était re-strippée
en minutes. Un **trigger Postgres** (`preserve_cibles_cpp` sur la table
`etat`) réinjecte désormais les `cibleCPP` connus dans toute écriture qui
les efface, référence par référence (id, repli ligne+nom). Testé en
production : un push intégralement strippé atterrit avec les 6 cibles
intactes. La donnée est défendue côté serveur, quelle que soit la version
du client.

## [4.49.3] — 2026-09-29

### Ajouté — message de bienvenue à la première ouverture
Après la mise en place de la base 2026/2027, un écran d'accueil s'affiche
une fois par poste : ce que contient la base (6 références, outils de prod
par OP, ISO/MABEC, cibles), les nouveaux écrans (feuille de route, coût
pièce complet), et surtout le geste critique — vérifier la version en bas
de page et rouvrir l'application connectée si elle est ancienne : une
version d'avant la 4.46 efface les cibles de coût au partage (2e strip
constaté ce matin à 5h26, cibles restaurées). Vocabulaire « l'application »
(demande Benjamin, pour Matis).

## [4.49.2] — 2026-09-28

### Corrigé — le graphe de tendance redevient lisible après complétion
L'échelle horizontale était calée sur la plus grande charnière de TOUT
l'outillage du scénario. Depuis « Compléter depuis la prod », un scénario
d'essai porte aussi les outils longs de l'excel (jusqu'à 300-4000 pièces)
qui ne sont pas suivis par l'essai : leur max écrasait les prélèvements
réels sur une fine bande du graphe (retour Benjamin : « visibilité
impactée fortement »). L'échelle suit désormais les charnières des
**logements réellement suivis** par les essais tracés — vérifié sur le
SL500 OP40 : axe 0-54 au lieu de 0-324, les 50 pièces mesurées occupent
toute la largeur. Le rapport d'essai embarqué bénéficie du même correctif
(fonction partagée).

## [4.49.1] — 2026-09-28

### Corrigé — la fusion ne crie plus au conflit pour rien
La comparaison d'essais de `fusionnerLignes` utilisait `JSON.stringify`
brut, sensible à l'ordre des clés : un aller-retour JSON (export/import,
régénération de fichier) réordonne les clés sans toucher aux valeurs et
déclarait des « conflits à vérifier » sur des essais strictement
identiques — 5 faux positifs constatés au dépôt du correctif ISO/MABEC.
Comparaison désormais **canonique** (clés triées récursivement), testée.
Au passage, correction de données : dans les scénarios « base excel »,
**référence plaquette = ISO** de l'excel et **Art. Stellantis = code
MABEC/MM** (l'import initial avait croisé les deux — 102 logements
corrigés au cloud, vérifiés).

## [4.49.0] — 2026-09-28

Cadrage acté avec Benjamin : l'outil devient la feuille de route commune
des économies (tracker les progrès réalisés et en cours, globalement, par
OP, par outil).

### Ajouté — coût pièce complet et feuille de route
- **Bandeau « Coût pièce complet » (Zone 1)** : somme du CPP de prod
  (base excel) de toutes les OPs de la référence — la 356x26 affiche
  0,747 € (OP10 0,158 + OP40 0,539 + OP30 0,050) — avec par OP le
  meilleur essai en cours et son statut, et la barre prod → cible du
  site (cibleCPP).
- **Feuille de route en tête de la vue de synthèse** : barre prod →
  cible avec le % de chemin parcouru, une ligne par OP (CPP prod,
  meilleur essai, gain annualisé, statut « passé en série / validé 5× /
  essai en cours / prod seule »), et le gain disponible aujourd'hui.
- `pieceCPPComplet()` agrège par référence en respectant le contexte de
  config de chaque OP ; `statutOP()` dérive l'avancement des scénarios.

### Corrigé — la cascade du gain ne disparaît plus
Quand le scénario ouvert est la base, ou qu'aucun poste n'est chiffrable
(gate `multiPoste` retirée), ou que les coûts sont identiques : le bloc
reste affiché et EXPLIQUE pourquoi il est vide — une barre absente se
lisait comme un bug (retour Benjamin : « aucune barre ne s'affiche »).

## [4.48.0] — 2026-09-28

### Ajouté — « ⊞ Compléter depuis la prod »
Sur un scénario d'essai incomplet, un bouton ajoute les outils qui
tournent en prod (scénario base excel du même OP) mais manquent au
scénario — rapprochement par préfixe de numéro (T548 ↔ T548 D1 :
convention de nommage Matis ≠ excel), aperçu de la liste et
confirmation. Ajout PUR : les outils d'essai gardent leurs conditions,
les essais/prélèvements/photos ne sont pas touchés. Comparer un scénario
incomplet à une prod complète faussait le CPP — c'est le prérequis des
comparaisons OP40 (vérifié sur le DWG réel : propose exactement T546 D1,
T543 D2, T543 D1).

### Note exploitation — clients périmés
Incident du 28/09 18h59 : un client resté sur une version ≤ 4.46 a
rapatrié le cloud puis repoussé l'arbre normalisé par son ancien code —
qui ne connaissait pas `cibleCPP` — et a strippé les cibles du cloud.
Restaurées le soir même (les 6, vérifiées). Le risque disparaît quand
tous les postes tournent la même version (merge prod) ; en attendant,
fermer les onglets/PWA périmés de l'outil.

## [4.47.1] — 2026-09-28

### Corrigé — un scénario d'essai ne s'affichait pas au clic (retour Benjamin)
Sur EMAG 1 OP40, cliquer le scénario DWG laissait l'écran figé sur la
sélection précédente. Cause : `prelevementRowHTML` référençait
`mesureLabel`, variable qui n'existait que dans la portée d'
`essaiCardHTML` — bug latent depuis la v4.9, qui ne se déclenchait que
sur la branche « mono » du battement (scénarios **sans** `emag1`, cas
des scénarios OP40 de la nouvelle base). Le rendu levait une
ReferenceError et le DOM gardait l'ancien contenu. Le libellé est
désormais calculé dans la fonction elle-même. Vérifié : les 23 scénarios
de la base rendent sans erreur.

## [4.47.0] — 2026-09-28

Retour UI de Benjamin : « la simultanéité est visuellement pauvre ».

### Ajouté — les groupes d'outils simultanés deviennent visibles
Dans la vue d'ensemble de la composition, les tuiles des outils d'un même
groupe simultané sont enfermées dans un **bloc ambre à bordure pointillée**
avec l'en-tête « ⇉ Travail simultané — n outils usinent ensemble, seul le
plus long compte dans le cycle ». Le badge de la fiche repliée et la case
de la fiche ouverte passent à la même couleur ambre : un seul code visuel
pour le concept (ambre = simultanéité). La disposition reflète
exactement le calcul v4.41 (regroupement consécutif).

## [4.46.1] — 2026-09-28

### Ajouté — cible de coût pièce par référence
Les cibles du site (colonne « Cible » des onglets « Evolution coût pièce »
de l'excel de Matis) deviennent un champ de la référence (`cibleCPP`) :
persistées à l'import/export, affichées dans la cellule coût du scénario
de référence (« cible site : 0,212 €/pièce »). Positionnées sur les 6
références retenues : DV 356x26 RPI 0,575 · DV 304x28 RPE 0,212 ·
DP 290x12 0,232 · DP 330x14 0,384 · DV 330x28 RPE K0 0,218 ·
DV 302x26 RPI (HESSAPP) 0,129.

### Restreint — références implémentées
L'assemblage de base ne crée que les **6 références qui comptent**
(liste Matis) : les autres de l'excel (usinées très rarement) ne sont
pas créées — l'excel reste la source si une référence rare devait
être ajoutée un jour.

## [4.46.0] — 2026-09-28

Deux chantiers : la base de départ 2026/2027 (fichier de Matis) et le
retour au design system d'origine.

### Ajouté — base_depart_2026_2027.json (fichier à importer, hors outil)
Les 16 références disques de l'excel consommation de Matis (EMAG 1/2/3 +
HESSAPP) sont figées en scénarios « Prod actuelle » baseline : 210
outils/logements avec N° d'outil, ISO en description, référence plaquette
MABEC, prix UHT, arêtes et charnière (DDV) — la formule du fichier
(prix ÷ arêtes × DDV = CPP) coïncide avec le modèle de l'outil. Import
vérifié par la chaîne standard (4 lignes, 16 scénarios baseline, 210
outils). Notes pour Benjamin :
- les « Production » des onglets sont reprises en volume annuel — à
  confirmer/corriger (champ éditable dans Options) ;
- 4 références sans outil exploitable (prix/DDV absents dans l'excel) :
  E1 302x26 RPI, H 266x13, H 266x22 RPI, H 283x26 RPI ;
- quelques arêtes recalées sur le CPP du fichier (T533/T535 notamment).

### Modifié — design system v4.29 restauré
Manrope (titres, gros chiffres, en 800) et Public Sans (texte) reprennent
le design system posé à la v4.29, IBM Plex Mono garde les chiffres ;
l'identité couleur SPK by CeramTec (4.32) et toutes les évolutions
d'écran 4.30→4.45 restent inchangées. (Retour d'usage : Open Sans
Condensed, posé en 4.32, ne faisait pas l'unanimité.)

## [4.45.0] — 2026-09-28

Retour du terrain (Benjamin) : sur un scénario d'essai avec mesures de
cycle complètes, le coût pièce intégrait le temps machine pendant que la
référence (sans mesures, sans cycle de référence en secondes) restait en
plaquettes seules — le delta comparait deux périmètres différents.

### Corrigé — périmètre de comparaison synchronisé
- `perimetreCompare()` (testée) : un poste n'entre dans un delta que s'il
  est chiffrable **des deux côtés** ; les postes à un seul côté sont exclus
  et signalés.
- **% du coût par pièce** (tableau de bord + verdict) : calculés sur le
  périmètre commun ; titre qualifié « (hors temps machine) » et
  avertissement explicite avec l'invitation à renseigner le cycle de
  référence en secondes pour un « tout compris ».
- **Gain annuel** : même règle — poste commun seulement, drapeau
  `perimetrePartiel` remonté jusqu'à la cellule et au détail dépliable.
- Les heures machine annuelles exigeaient déjà les deux cycles : inchangé.
- Le coût total affiché de chaque scénario reste sa vérité propre (avec sa
  machine) ; seul le delta porte le périmètre commun.

### Tests
`perimetreCompare` (exclusion, totaux communs, périmètre complet) et
`bilanAnnuel` asymétrique (gain hors machine = 4 375 €/an sur le jeu rond).

## [4.44.0] — 2026-09-25

### Modifié — la feuille de style remise d'aplomb
- **Patchs consolidés** : les blocs `<style>` datés 4.32→4.41 (identité SPK,
  respiration 4.33, hiérarchie 4.34, repère de zone 4.35) fusionnent en un
  seul bloc documenté, toujours après la feuille principale (cascade
  conservée à l'identique). C'est la pile « dernier gagne » qui avait causé
  l'écrasement d'encre corrigé en 4.40 — un seul bloc, plus de surprise.
- **Classes mortes purgées** (recoupage des émissions dynamiques fait) :
  `.pos-label`, `.ref-stack`, `.badge.type-bug/.type-amelioration`,
  `.log-add`, `.limit-global`, `.mini-stat`, `.sc-r`, et retrait de
  `.ligne-strip`/`.reference-strip` du masquage d'impression.
- **Couleurs tokenisées** : hover du bouton de sauvegarde en `color-mix`
  sur `--green`, fond des badges photo en `--photo-overlay`.

## [4.43.0] — 2026-09-25

### Modifié — le système de polices assaini (héritage 4.32)
Le passage à l'identité SPK (4.32) avait changé les tokens sans nettoyer.
- **`--font-mono` redevient une vraie chasse fixe** : IBM Plex Mono, déjà
  embarquée pour les gabarits de rapport — saisie, cellules et libellés
  data retrouvent le rendu « outil de mesure ».
- **Manrope et Public Sans supprimées** (−67 Ko) : embarquées depuis la
  4.31, plus aucune utilisation. Archivo reste (canvas du logo), Plex Mono
  reste (gabarits).
- **Faux gras 800 éliminé** : Open Sans Condensed n'est embarquée qu'en
  700 — les 16 règles `--font-disp` en 800 synthétisaient un gras artificiel.
  La hiérarchie titres/chiffres vient désormais de la taille et de
  l'encre. Le 700 du gabarit de rapport passe à 600 (vraie graisse).
- **Commentaires et aide remis en phase** : en-têtes CSS (ils racontaient
  encore Manrope/Plex), commentaire de `fmt()` (Archivo), aide (plus de
  « plaquettes bol et piste » ni « ap piste »). L'annonce historique
  3.x restant inchangée : on ne réécrit pas l'histoire.

## [4.42.0] — 2026-09-25

### Modifié — le coefficient K devient une botte secrete
L'indice thermique du widget Fr·Fa (Vc × f × sin(κr), équivalent exact de
Vc × Hex en tournage) est désormais réservé à l'auteur du projet : il ne
s'affiche que sur son poste (nom d'auteur ou drapeau local) et ne part
JAMAIS dans les pages imprimées. La ligne « Formules du widget K » de
l'aide disparaît pour les autres accès. Le calcul (kvfDe) et la saisie du
κr restent inchangés ; Fr/Fa reste visible de tous.

### Tests
Sortie du widget avec et sans autorisation (aucun K sans, K présent avec,
Fr/Fa dans les deux cas).

## [4.41.1] — 2026-09-25

Correctifs issus de l'audit complet du 25/09 (rapports croisés ZCode +
Hermes). Aucun changement de calcul ni de donnée.

### Corrigé
- **Textes corrompus** : le résumé replié de la Tendance et deux annonces
  4.38 affichaient des séquences d'encodage corrompues (« Ã©volution ») ;
  balayage complet du fichier et réparation de toutes les occurrences.
- **Contraste de la cellule Validation** (thème clair) : l'encre passe à
  #dcf2e4 sur le vert — 4,58:1, au-dessus du seuil WCAG AA (était 3,96:1).
- **Secondes de cycle alignées** : les tuiles de scénarios affichent
  désormais les secondes/cadence comme le tableau de bord, sans condition
  d'option ; le libellé de l'option est reformulé (elle ne concerne plus
  que les tuiles).
- **Options remises en phase** : le module « Détailler le temps de cycle »
  ne mentionne plus le temps de déplacement (sorti du calcul en 4.39) et
  décrit la règle réelle (mesures complètes = comptées, l'option ne gère
  que la colonne d'impression).
- **Débogage** : un échec de lecture du suivi au chargement laisse
  désormais une trace en console au lieu d'un repli silencieux.

### Tests
`cadenceHeure` (jamais couverte), la migration du mode global 4.39/4.40
vers les cases par outil, et l'annonce du nombre de groupes dans le statut
de composition.

## [4.41.0] — 2026-09-25

Précision de Benjamin sur la 4.40 : le simultané ne concerne pas le
scénario entier mais **deux outils précis à la fois** — il faut pouvoir
cocher l'un puis l'autre. Modèle validé : groupes d'outils simultanés,
on additionne les groupes.

### Ajouté — le simultané se coche outil par outil
Chaque fiche outil (sauf la première, qui ouvre la marche) gagne une case
**« ⇉ Tourne en simultané avec l'outil précédent »** (`simultaneAvecPrecedent`,
avec le n° du voisin dans le libellé). Le regroupement est consécutif :
cochée, l'outil rejoint le groupe de son voisin. Le calcul
(`cycleDetailStatus`) forme les groupes, chaque groupe vaut le temps de son
outil le plus long (logements d'un même outil toujours additionnés), et le
cycle est la **somme des groupes**. Aucune case cochée = outils en série.
- Badge **« ⇉ simultané »** visible sur la fiche repliée.
- La cellule Temps de cycle du tableau de bord et le statut de composition
  annoncent le nombre de groupes et la règle.
- Migration : le mode global 4.39/4.40 (`outilsParalleles`) coche
  « simultané » sur tous les outils sauf le premier (un seul groupe =
  même résultat) ; le champ `logementsParalleles` de la 4.39 n'a jamais
  quitté l'adresse projet.
- Exemple testé : outil 2 logements (30+20 s) ; TC2 (20 s) simultané ;
  TC3 (25 s) à part → 30 + 25 = **55 s** au lieu de 95 s en série.

## [4.40.0] — 2026-09-25

Deux corrections de Benjamin sur la 4.39 (déployée entre-temps sur
l'adresse projet uniquement) : le simultané ne peut pas s'appliquer au
scénario entier, et le bandeau bleu est redevenu illisible.

### Corrigé — le simultané est un mode ENTRE OUTILS, pas entre logements
La physique d'une OP : **dans un outil, les logements enchaînent toujours
à la suite** (leurs temps de coupe s'additionnent, quel que soit le mode) ;
ce sont les **outils** qui tournent en simultané (ébauche ou finition piste
sur deux stations) — le cycle est alors **le temps de l'outil le plus
long**, pas celui du plus long logement. `logementsParalleles` devient
`outilsParalleles` (le champ 4.39 n'a jamais quitté l'adresse projet,
aucune donnée réelle à migrer). Sélecteur, statut de composition, dépliant
de tuile et tests alignés : outil à 2 logements 30+20 s + outil à 20 s →
70 s en série, 50 s en simultané.

### Corrigé — les libellés du bandeau bleu écrasés en gris/noir
Le bloc « deux niveaux de libellés » (4.34) forçait `.foot-cell .l` en
`--ink-faint` et `.foot-cell .v` en `--ink` — gris foncé et noir sur
l'aplat bleu du tableau de bord (et jusque sur le vert de la cellule
validation). Le bandeau est exclu du recul d'étiquettes : il garde sa
hiérarchie d'encre propre (`--fill-ink-soft` / `--fill-ink`), lisible sur
le bleu comme sur le vert.

## [4.39.0] — 2026-09-25

Cadrage discuté avec Benjamin (temps de cycle vs coût machine) : la
mécanique existait (mesures par logement, indice base 100, coût machine)
mais dispersée dans Options et muette sur sa propre logique. Décisions :
déplacement hors calcul, somme **ou** max par scénario, plus aucun nom
figé dans le code. ⚠ Note : les entrées 4.31 → 4.38 manquent à ce
CHANGELOG (itérations UI sur dev, annonces in-app présentes) — à
compléter avant tout passage en production.

### Ajouté — le cycle par logement lisible et pilotable
- **Section Cycle dans le dépliant de chaque tuile logement** : temps de
  coupe mesuré, part du cycle (selon le mode), indice conditions vs base
  (Vc·f, estimation distincte de la mesure) et rappel explicite quand les
  mesures sont ignorées (« 1/2 logements renseignés »).
- **Cellule Temps de cycle du tableau de bord** : secondes et cadence
  toujours affichées (l'option `cycleSecActif` ne gate plus l'écran),
  mention de la source (mesures machine n/n ou indice), et
  **€ machine/pièce affiché dès que le taux horaire de la ligne existe** —
  affiché même quand l'option « Intégrer le temps machine » est inactive
  (mention « affiché, non pondéré »). Un scénario appartient à une ligne :
  le taux horaire de la ligne suffit, confirmé.
- **Les mesures comptent sans interrupteur** : `cycleSecondes` retient le
  total mesuré dès qu'il est complet (tous les logements), l'option
  « détail du cycle par logement » ne décide plus que de l'affichage de la
  colonne à l'impression. Le champ Temps de coupe est visible en fiche
  outil en permanence.
- **Sélecteur série/simultané par scénario** (dans la cellule) :
  `logementsParalleles` — en série le cycle est la somme des temps de
  coupe ; en simultané (finition OP40, les deux outils tournent ensemble)
  c'est le temps du plus long. Le statut sous la composition nomme le
  mode appliqué.

### Modifié — déplacement hors calcul, noms défigés
- `tempsDeplacement` quitte la saisie (fiche outil), le tableau
  d'impression et le total du cycle ; les valeurs déjà stockées restent
  dans les données, ignorées. La complétude exige désormais les temps de
  **coupe** de tous les logements, rien qu'eux.
- `logementCycle()` ne cherche plus un logement nommé « Piste » (héritage
  de la toute première saisie) : **le premier logement du scénario** ancre
  l'indice — l'ordre des fiches fait foi. Libellé « €/arête (bol + piste) »
  → « €/arête (tous logements) ». Impact possible : si dans des données
  existantes « Piste » n'était pas le premier logement, l'indice recalculé
  peut varier légèrement au rechargement.

## [4.38.0] — 2026-09-24

### Modifié — la tendance passe en zone de lecture repliable
Le graphique d'évolution au fil des pièces est replié par défaut : il ne
concurrence plus la saisie des essais et s'ouvre au clic. (Rappel 4.37 :
zone de détail regroupée.)

## [4.37.0] — 2026-09-24

### Ajouté — zone de détail regroupée
Détail du calcul, consommation annuelle et pièces détachées ne font plus
qu'un seul bloc repliable : l'écran montre la décision (zones 1 et 2) et
tient le calcul à un clic. (Rappel 4.36 : écran en trois zones nommées.)

## [4.36.0] — 2026-09-24

### Ajouté — écran structuré en trois zones nommées
**1 · Réponse** (base de comparaison et meilleur coût), **2 · Scénarios**,
**3 · Traçabilité du scénario ouvert** : on sait toujours où l'on est dans
l'écran. (Rappel 4.35 : repère de zone, deux niveaux de libellés, blocs
périphériques repliés.)

## [4.35.0] — 2026-09-24

### Ajouté — repère de zone avant la traçabilité
Un bandeau marque l'entrée dans la traçabilité du scénario ouvert (outils,
cycle, essais, rebut), au lieu d'enchaîner les blocs à la suite.
(Rappel 4.34 : deux niveaux de libellés.)

## [4.34.0] — 2026-09-24

### Modifié — deux niveaux de libellés
Les étiquettes (petites, grises) reculent, les valeurs et les chiffres
avancent : l'écran se lit par niveaux au lieu d'un aplat uniforme.
(Note : le bandeau bleu du tableau de bord a été exclu de ce recul en
4.40 — voir [4.40.0].)

## [4.33.0] — 2026-09-24

### Modifié — densité de l'écran : l'écran respire
Les blocs périphériques (consommation annuelle, pièces détachées) sont
repliés par défaut : l'essentiel reste visible, le détail s'ouvre au clic.
Espacements revus entre les grands blocs. Correction : les styles ajoutés
(polices embarquées + bandeau de base) étaient partis dans le gabarit de
rapport au lieu de la feuille de l'app. L'impression reste complète.

## [4.32.0] — 2026-09-24

### Ajouté — base de comparaison explicite + identité SPK by CeramTec
Le ★ (scénario en production) est dissocié du **choix de base** : un
bandeau nomme la base, un sélecteur par OP permet d'en changer sans
toucher au statut ; si la base est la plus chère, l'outil l'annonce et
nomme le meilleur coût. Identité SPK by CeramTec : bleu #1B5EA6, rouge
#E2001A en accent, rayon 3 px, polices embarquées, hiérarchie des titres.
Aucun changement de logique de calcul.

## [4.31.0] — 2026-09-24

### Ajouté — vue de synthèse comparative regroupée
Les critères sont rangés en trois blocs — Économique, Process, Qualité &
essais — au lieu d'une liste plate. Pour chaque critère, la meilleure
valeur passe en vert et la plus défavorable en rouge ; chaque scénario
compte les critères qu'il remporte. Un bloc « cascade du gain » explique
l'économie poste par poste (plaquettes, pièces détachées, temps machine,
rebut) face à la référence. Aucun changement de calcul ni de donnée.

## [4.30.0] — 2026-09-24

Session dédiée UI (audit densité + typographie du détail scénario, captures
des deux thèmes à l'appui). Cadrage acté avec Benjamin : fusion verdict +
bande de chiffres, contexte d'essai repliable, refonte de la ligne critères,
normalisation typographique. Travaillé sur la branche `dev`.

### Modifié — verdict et chiffres fondus en un seul tableau de bord
La bande verdict (titre + sous-titre + chips) et la bande de chiffres
disparaissent au profit d'**une seule bande** (`.scenario-foot`) : la zone
verdict (`.foot-verdict`, état coloré sur l'aplat : vert/rouge/ambre, neutre
pour la référence) ouvre la marche, suivie des cellules coût/pièce,
gain annuel, **durée de vie visée** (nouvelle cellule — elle quittait les
chips ; la valeur de la référence s'affiche à côté pour un scénario d'essai),
€/arête, cycle, validation (qui gagne le **% de prélèvements hors tolérance**,
lui aussi ex-chip). Chaque nombre n'apparaît plus qu'une fois au lieu de
trois-quatre. Le détail du coût annuel (v4.29) se déplie désormais **en bas
de bande** sur toute la largeur au lieu de couper la rangée de cellules.
`verdictHTML` est réécrite (plus de chips), `dureeVieScenario` extraite
(testée) ; le CSS `.verdict`/`.vchip` de la feuille principale est supprimé
(les gabarits de rapport gardent le leur).

### Ajouté — le contexte de l'essai se replie
But, observations, rédacteur, début/fin d'essai et programme CNC regroupés
dans un bloc `details.essai-ctx` : **ouvert tant que l'essai est vierge**
(mode création), **replié dès qu'un champ est rempli**, avec un aperçu du
but dans le bandeau. L'état ouvert/replié posé par l'utilisateur survit aux
re-rendus (`essaiCtxOuverts`, même mécanique que les fiches outil).
L'impression reste inchangée (lignes à plat).

### Modifié — ligne critères d'essais resserrée
Les boutons + Ra / + VE / + Autre critère ne s'empilent plus en colonne :
leur phrase d'explication passe en info-bulle. La note « valeur OP — l'éditer
la rend spécifique » devient « valeur OP » nowrap (phrase en info-bulle).
La spéc usine s'aligne à droite de la meta-ligne (`.spec-usine`).

### Corrigé — typographie des chiffres
- **Faux gras mono éliminé** : IBM Plex Mono n'embarque que 400/500/600, tous
  les `font-weight:700` mono (badges, `.tc-val`, `.os-numero`, pastilles
  outil, valeurs atelier…) passent à la vraie graisse 600.
- **`tabular-nums` complet** sur les héros qui en manquaient
  (`.foot-cell .v`, `input.cell-cycle`, `.kvf-item .v`, `.vb-v`).
- **Échelle de héros fermée** dans la bande : 38 / `.mid` 24 / `.small` 19 —
  les `font-size:26px/18px` inline disparaissent.
- **Unités `<small>` normalisées** : Public Sans 600 / 10,5 px partout
  (le pied de bande était en 500/12 px, le total compo en 11,5).
- **Impression** : les valeurs saisies du tableau (`td.num`) passent en mono
  tabulaire — mêmes polices qu'à l'écran, plus de mélange dans une ligne.

## [4.29.0] — 2026-09-24

Deux points de Benjamin : le piège « rattacher un scénario d'une ligne à un
projet d'une autre ligne » (ex. un scénario HESSAPP dans le projet « coût
EMAG 1 »), et le coût annuel GÉNÉRAL du pied de scénario qui mérite le même
détail dépliable que les tuiles de logement.

### Modifié — les étiquettes de projet traversent les lignes, mais plus en silence
Le modèle v4.1 reste entier : un projet est une playlist qui peut légitimement
couvrir plusieurs lignes. Mais désormais `lignesDuProjet(pj)` (testée) liste
les lignes couvertes : **l'info-bulle de chaque étiquette** dit « contient :
EMAG 1 », et un clic qui rattache un scénario depuis une ligne absente du
projet ouvre une **confirmation** (« y rattacher quand même ? ») — on avertit,
on ne bloque pas (philosophie v4.5).

### Ajouté — le coût annuel général se déplie
La tuile « Coût annuel / Gain annuel » du pied de scénario est cliquable ;
un bandeau de détail se déploie sous la rangée, avec le même point de vérité
que le chiffre de tête (`coutsDetail` sans ligne explicite) : **Coût annuel** —
outillage × production, détail logement par logement (prix ÷ arêtes ×
charnière de chacun), puis pièces détachées / temps machine / rebut si leurs
modules sont actifs, et le total. **Gain annuel** — référence × production,
scénario × production, le gain et les heures machine. État déplié mémorisé
(`coutAnnuelDetailOuvert`), bandeau masqué à l'impression si replié.

## [4.28.0] — 2026-09-23

Deux points de Matis/Benjamin : « l'affichage Bol/Piste persiste » (copie
écran OP40 HESSAPP — non reçue, remplacée par un balayage exhaustif du code),
et l'ajout du **détail du calcul de coût annuel** au clic sur la tuile.

### Corrigé — les quatre derniers affichages à noms figés
Balayage complet des usages de `logementNom`/`outilNumero` : il restait quatre
sites qui lisaient l'instantané figé de l'essai — la **barre de progression du
mode atelier** (elle utilise maintenant `logementProgress`, déjà résolu), le
**sélecteur de logement** des lignes de prélèvements, son équivalent à
l'impression, et la **fenêtre de comparaison d'essais** (plaquettes et
conditions ; elle affiche aussi désormais le statut « ⏹ Arrêté »). Tous
relisent le nom actuel via `nomLogementActuel`.

### Ajouté — le détail du calcul au clic sur la tuile
Choix : **déploiement** plutôt qu'infobulle (lisible au doigt, copiable,
découvrable). Un clic sur une tuile de la vue d'ensemble déplie les opérations
avec les vrais chiffres : prix plaquette, durée de vie visée (arêtes ×
charnière), coût pièce, production annuelle, plaquettes/an, coût annuel. Tuile
non calculable : la raison exacte. L'état déplié survit aux re-rendus
(`apDetailsOuverts`, même mécanique que les fiches outil) ; l'impression
n'emporte le détail que s'il est déplié.

### [4.27.1 / 4.27.2] — 2026-09-23 (retouches)
Kaki HESSAPP renforcé (#556b2f, opacité 13 %), filigrane réduit (tuile
240×150, police 54) pour plus de répétitions, puis suppression du filigrane
sur HESSAPP (ligne unique : la teinte suffit — flag `sansFiligrane` par
famille).

## [4.27.0] — 2026-09-23

Info structurante de Benjamin/Matis : le plan machine de Sept Fons, du fond de
l'atelier vers l'entrée — Weisser 1-4, HESSAPP (double OP droite/gauche, comme
EMAG 1), EMAG 1 (double OP), EMAG 2-3, PCI 1-2. Deux usages : le semis des
lignes manquantes dans l'arbre, et l'orientation visuelle par famille.

### Ajouté — référentiel des lignes de Sept Fons
Au premier lancement de cette version (`localStorage: spk_lignes_septfons_
semees`, une seule fois), les lignes du référentiel absentes de l'arbre sont
créées **vides** et l'ensemble est remis dans l'**ordre physique de
l'atelier** (`rangLigneSeptFons`, lignes inconnues après le référentiel).
Une ligne supprimée volontairement ensuite ne revient pas. HESSAPP est notée
double OP dans la fenêtre des nouveautés — ses OP se créeront avec ses
premiers essais.

### Ajouté — teinte de fond par famille de machines
Quand une ligne est affichée, le fond de page prend une teinte légère selon sa
famille (préfixe du nom : Weisser → rouge, HESSAP* → kaki, EMAG* → gris,
PCI* → bleu) avec le **code ligne en filigrane répété** (W1…W4, HESSAPP, E1-E3,
P1-P2). Implémentation : un seul `background-image` SVG data-URL posé sur le
body (rect teinté + texte en filigrane dans la tuile répétée) — rien ne flotte
au-dessus du contenu. L'encre du filigrane s'adapte au thème (sombre sur fond
clair, blanche sur fond sombre) ; ni teinte ni filigrane à l'impression.
Ligne hors référentiel : pas de teinte.

## [4.26.0] — 2026-09-23

Deux retours d'usage (Matis/Benjamin) : le bandeau bleu « Reprendre » affichait
un vieil essai (et les noms de logements d'époque, « Bol/Piste ») sur les
nouvelles créations ; et la popup de démarrage listait TOUT l'historique des
versions.

### Modifié — le bandeau « Reprendre » est contextualisé
`dernierEssaiEnCours` propose **d'abord un essai en cours du scénario
affiché** (`activeId`) — là où l'on travaille ; à défaut seulement, l'essai en
cours le plus récent de l'outil (comportement précédent). Recentrer la vue sur
un autre scénario recalcule le bandeau.

### Modifié — la fenêtre des nouveautés ne garde que 10 jours
`nouveautesHTML` filtre les entrées à la dizaine écoulée (dates
jj/mm/aaaa ; entrée illisible conservée par prudence ; jamais de liste vide —
retombe sur la dernière version). L'entrée du jour est toujours là.

## [4.25.0] — 2026-09-23

Question de Benjamin : « comment clôturer un essai arrêté avant la charnière
cause fail ? » — et le constat : le cas du fail **mesuré** était déjà couvert
(un prélèvement hors tolérance → « Non conforme » automatique), mais pas
l'arrêt **net** (insert cassé, brut éclaté, incident machine) : le statut étant
calculé, l'essai restait « en cours — X pièces à saisir » pour toujours et
remplissait le bandeau de reprise. Nouveau champ `cloture` sur l'essai
(`{motif, detail, date}`), absent = non clôturé — aucune migration.

### Ajouté — clôturer un essai (arrêt anticipé)
Bouton **⏹ Clôturer** sur la carte d'essai → panneau motif/précision/date
(casse, hors tolérance, brut, incident machine, autre). L'essai passe
**⏹ Arrêté — motif · détail** :
- **statut `arrete`** calculé en tête de la chaîne de décision de `essaiStats`
  (la décision de record passe avant tout) ;
- sort du **bandeau de reprise** (déjà : seul `pending` y entre) et du
  **protocole 5×** (`scenarioStats.arreteCount` — ni conforme ni non conforme) ;
- **résumé du scénario** : les essais arrêtés s'affichent à part
  (« N arrêtés avant charnière ») ;
- **rapport d'essai** : verdict « Arrêté — motif · détail », pastille grise ;
- **réouvrable** (suppression du champ, retour « en cours ») — les
  prélèvements, courbes et photos ne bougent jamais.

## [4.24.0] — 2026-09-23

Demande de Matis : faire apparaître dans le rapport d'essai les images de
l'onglet Photos (avec leurs légendes) — rapport de métrologie photographié,
usures de plaquettes, constats — pour que les destinataires aient les preuves
en même temps que les chiffres. Le rapport reste **un seul fichier HTML
autonome** : chaque photo est aplatie (rognage + annotations appliqués) en JPEG
embarqué en data URL, jamais un lien ni un dossier à joindre.

### Ajouté — les photos voyagent avec le rapport
- `photosPourRapport(essai)` : pour chaque photo, `photoObjectURL` résout le
  stockage (dossier local ou cloud + cache), l'image est décodée puis
  **aplatie** — `aplatirPhoto` applique le crop (fractions de l'original) et
  redessine les annotations via `drawAnnotShapes`, qui accepte désormais un
  crop explicite (paramètre optionnel, comportement de l'éditeur inchangé).
  Plafond 1200 px de large, JPEG 0,85 — une photo pèse ~150-400 ko dans le
  rapport.
- Section **« Photos — constats, métrologie, usures »** dans le rapport
  (après Observations, avant Marposs), grille de figures avec légendes. Une
  photo indisponible à la génération (dossier déconnecté, cloud hors ligne)
  devient une case qui nomme la raison — les autres partent quand même, et un
  message dédié s'affiche si AUCUNE n'a pu partir.
- `telechargerRapportEssai` devient asynchrone (téléchargements cloud
  éventuels) avec filet : échec → dialogue explicite.

## [4.23.0] — 2026-09-23

Signalement de Benjamin : le volume annuel « n'est pas rattaché à une ligne et
une référence » — en éditant la valeur sur une nouvelle ligne, il a vu
l'ancienne valeur d'EMAG remplacée. Audit complet de toutes les écritures
(`appliquerOptions`, création de ligne/référence/OP, import par identifiants,
fusion cloud par identifiants) : **aucune écriture croisée n'existe dans le
code** — la valeur a toujours été stockée sur la référence. Le vrai problème
est l'ambiguïté de saisie : rien n'indiquait à QUELLE référence le champ
s'appliquait, et la tuile de composition n'emmène nulle part. Correctif UX +
traçabilité.

### Modifié — le champ volume dit à qui il s'applique
- Options : sous le champ, **« S'applique à : EMAG 1 › DV 356X26 RPI »**, plus
  la trace de la dernière modification.
- La tuile « Production annuelle » de la composition devient **cliquable** :
  elle ouvre Options pré-remplie pour LA référence affichée (curseur, survol,
  mention ✎ modifier). Un seul geste, zéro ambiguïté.

### Ajouté — historique du volume sur la référence
`enregistrerVolumeAnnuel(ref, nv)` (testée) trace chaque changement réel
(valeur, auteur, date — 10 dernières entrées, réécrire la même valeur ne trace
pas, vider le champ se trace). La dernière entrée s'affiche sous le champ
Options : si un doute réapparaît, on voit immédiatement qui a écrit quoi,
quand.

## [4.22.0] — 2026-09-23

Deux demandes liées de Benjamin : les renommages d'outils/logements n'étaient
pas pris en compte dans le graphe des prélèvements (« le nom initial reste en
mémoire »), et un nouveau scénario devait pouvoir **copier les outils de la
production par sélection** plutôt que tout retaper.

### Corrigé — les noms affichés suivent le scénario
L'instantané d'un essai (`params.logements`) gelait les conditions de coupe
*et les noms*. `nomLogementActuel(sc, lp)` relit désormais les noms dans le
scénario au moment de l'affichage (via `logementId`), avec repli sur le nom
figé si le logement a été retiré (trace historique). Appliqué partout où le
nom s'affiche : **graphe des prélèvements** (`seriesTendance`), puces
d'essai, rapport de validation (`prelevementsDetailHTML`, tableaux du rapport
d'essai), export CSV, message de divergence des conditions, bandeau de
reprise, onglets du mode atelier. Les conditions elles-mêmes restent figées —
c'est leur rôle. Décision actée pour la comparaison : les outils copiés
conservent les noms de la production (mêmes positions physiques) et chaque
courbe reste titrée par son essai — pas d'ambiguïté.

### Ajouté — copier les outils de la production
Bouton « ⧉ Copier les outils de « … » » dans la composition d'un scénario non
référence (`copieDepuisPossible`), panneau à cases à cocher, et
`copierOutilsDeProduction` (testée) : copie profonde des outils sélectionnés
avec **nouveaux identifiants** outils/logements/pièces (aucune collision avec
les instantanés d'essai de la production), plan non copié (fichier du
scénario d'origine), essais existants du scénario cible inchangés (les
logements copiés ne s'y suivent pas automatiquement — « + suivre un
logement »).

## [4.21.0] — 2026-09-23

Le panneau Suggestions devient le **carnet de sujets chauds partagé** décidé
avec Benjamin (bugs et améliorations outil, essais à planifier, sujets
techniques abordés avec Matis, anticipation des arrêts de ligne). Nouveau
champ `declencheur` sur les items, types et statuts étendus — les items
existants migrent sans rien faire.

### Modifié — Suggestions enrichies
- Types : Bug · Amélioration · **Essai à planifier** · **Sujet technique**.
- Champ **déclencheur** (repéré par une barre ambre) : la condition qui rend le
  sujet saisable — « à lancer dès un arrêt de ligne EMAG 1 ».
- Statuts étendus pour suivre une opportunité : Nouveau → En cours →
  **Prêt à lancer** → **Lancé** → Clos (l'ancien « Traité » garde sa valeur
  `traite`, seul le libellé change).
- Texte d'en-tête aligné sur le nouveau rôle (pense-bête d'équipe, synchronisé).

## [4.20.0] — 2026-09-23

Le taux de rebut annuel entre dans le bilan économique. Décision actée avec
Benjamin : le taux ne vit pas seulement sur la référence — réduire le rebut est
un résultat d'essai possible, donc le champ existe **par scénario**. Nouveau
champ `tauxRebutAnnuel` sur le scénario, aucun changement du reste du JSON.

### Ajouté — taux de rebut annuel, saisie Matis qui fait foi
Champ « Taux de rebut annuel (%) » en tête du suivi rebut de chaque scénario.
`tauxRebutDe(sc)` devient l'unique point de vérité du taux : **la saisie
annuelle fait foi** quand elle est remplie ; sinon le taux calculé du journal
d'équipe (`scrapLog`) s'applique, comme avant. `coutRebutPiece` passe par ce
point de vérité — le coût pièce, le coût total et donc **tout l'affichage
« gain annuel » existant** (rapport, chips, synthèse, tuiles) intègrent
automatiquement le rebut saisi, sans nouveau rendu. Un indicateur sous le champ
dit quelle source est retenue et rappelle le prérequis (module « Coût de
rebut » actif + prix du disque dans Options).

## [4.19.0] — 2026-09-23

Deux demandes de terrain sur la vue d'ensemble : **où part l'argent** (coût
annuel par logement, coloré) et **remettre les outils dans l'ordre voulu** sans
les retaper. Aucun changement du JSON — l'ordre des outils était déjà l'ordre
du tableau `sc.outils`.

### Ajouté — coût annuel par logement, coloré par part
Chaque tuile de la vue d'ensemble affiche `coût pièce × production annuelle`
(production de la référence courante, déjà connue) sous le coût pièce, et le
total annuel outillage rejoint l'en-tête. La couleur compare la **part** du
logement à sa part théorique (1/n logements) : `couleurPartCout` interpole le
teinte 145° (vert, ratio ≤ 0,33) → 0° (rouge, ratio ≥ 2) — un logement 1/3
sous sa part théorique est mineur, un logement 2× au-dessus est majeur.
Sans production annuelle saisie, la ligne ne s'affiche pas (pas de faux —).
`libelleAnnuel` bascule en k€/an au-delà de 10 000 €.

### Ajouté — réordonner les outils par glissement de tuile
Poignée ⠿ sur le bandeau de chaque fiche outil (draggable), lâcher sur une
autre fiche réordonne le tableau : `deplacerOutil` (fonction pure, testée)
splice `sc.outils`. Un seul geste met d'accord fiches, tuiles d'aperçu et
pastilles numérotées, et l'ordre part dans la synchro. Un clic simple ouvre
toujours la fiche — le drag ne déclenche pas de click. Repères visuels :
fiche en cours de drag estompée, cible en pointillés bleus.

## [4.18.0] — 2026-09-23

L'outil devient installable (PWA) avec mise à jour automatique. Le HTML
reste LA application : le manifeste et le service worker sont trois fichiers
publiés à côté (`manifest.webmanifest`, `service-worker.js`, `icons/`), la
`.surgeignore` est ouverte pour eux uniquement. Aucun changement du JSON ni de
la synchro.

### Ajouté — installation en application
Le manifeste existait depuis longtemps… mais en **URL `data:`** — que Chrome
refuse pour l'installation. Il devient un vrai fichier (`manifest.webmanifest`,
mêmes métadonnées : nom, standalone, thème #1b5ea6), avec `start_url`,
`scope` et `id` ajoutés, et les deux icônes PNG extraites du manifeste data:
vers `icons/icon-192.png` / `icon-512.png` + une variante **maskable** (fond
noir plein bord, logo réduit dans le cercle de sûreté). Le service worker
s'enregistre sur https et localhost uniquement (file:// : pas de sens, catch
silencieux).

### Ajouté — mise à jour poussée, sans désinstallation
Stratégie du service worker : **réseau d'abord pour le HTML** (la version à
jour est servie dès que le réseau l'a vue — à l'ouverture suivante, sans
aucune manipulation, et le numéro de version n'est pas dupliqué dans le SW),
**cache d'abord pour le shell statique** (icônes, manifeste). Nouveau SW :
`skipWaiting` + `clients.claim`, purge des vieux caches à l'activation. Le
cache ne sert que de repli hors ligne. **Toute requête non-GET et tout domaine
étranger (Supabase : auth, synchro, photos) sont non interceptés** — le cloud
et l'offline-first existants restent strictement identiques. Le nom de cache
ne bouge que si le SW lui-même change.

## [4.17.0] — 2026-09-23

Deux irritants remontés par Benjamin et Matis à l'usage quotidien : la
reconnexion à chaque ouverture, et le premier clic sur l'upload de plan qui ne
fait rien. Aucun changement de données.

### Corrigé — la session cloud survit aux ouvertures hors réseau
`cloudRafraichirSession()` détruisait la session sur **tout** échec du
rafraîchissement — y compris `Failed to fetch` et l'`AbortError` du délai
d'attente. Ouvrir l'outil avant que le réseau soit monté (ou derrière le proxy
d'usine qui hang) suffisait à se faire déconnecter, alors que le refresh token
restait valable : il fallait se reconnecter **à chaque ouverture**. Désormais la
session n'est détruite que sur un refus formel du serveur (HTTP 400/401/403 —
jeton révoqué, refresh déjà consommé, mauvais identifiants). Hors ligne, la
pastille affiche « cloud injoignable — session conservée » et le rafraîchissement
retente au prochain contact (focus, 90 s, saisie), comme le reste de la synchro.

### Corrigé — le premier clic sur « Joindre le plan de l'outil »
Le `blur` d'un champ déclenche son `change`, qui reconstruit tout l'écran —
**pendant le mousedown** du clic suivant. Le nœud sous le pointeur étant
remplacé entre mousedown et mouseup, le click final partait sur l'ancêtre
commun au lieu du bouton : le sélecteur de fichier ne s'ouvrait qu'au deuxième
clic, dès qu'on venait de saisir un champ. Un mini-mécanisme global
(`renderApresClic`, capture `mousedown`/`mouseup` sur `document`) retarde le
render à la fin du clic en cours — et seulement dans ce cas : un `change` hors
clic (Tab, Entrée) reste immédiat comme avant. Routé sur les deux seuls `render`
déclenchés par un blur : `onInputChange` et le tri des prélèvements.

## [4.16.0] — 2026-09-23

Le dernier trou de la synchro : le JSON voyageait entre postes, pas les photos.
Côté Supabase, le bucket privé `photos` (préparé depuis la v4.8, policy
`photos_membres` ALL pour `authenticated` sur `bucket_id = 'photos'`) est branché.
Aucun changement du JSON existant : une photo cloud ajoute seulement
`stockage:"cloud"` et un chemin de bucket sur son objet — les photos de dossier
local ne bougent pas.

### Ajouté — les photos d'essai peuvent vivre dans le cloud
Trois modes d'ajout, par priorité : **dossier local** connecté (inchangé, zéro
réseau) ; sinon, **cloud privé** quand on est connecté (bouton « Ajouter des
photos (cloud) ») — la photo est redimensionnée côté client (1600 px JPEG) puis
envoyée dans le bucket, et le suivi ne porte que sa référence légère
(`essaiId/horodatage.jpg`), qui voyage donc avec l'export, l'import ET la synchro ;
sinon, l'invitation à se brancher reste affichée. L'autre poste télécharge la
photo à la demande (auth par session, jamais d'URL signée publique) pour la
miniature, l'agrandissement et l'annotation — et la met en **cache IndexedDB**
(`spk_photos_cloud`) : une photo déjà vue se réaffiche hors ligne. Une photo
jamais téléchargée s'affiche estompée avec la raison exacte en info-bulle. La
suppression retire le fichier du bucket (best effort) et le cache local. Le
dossier local reste prioritaire quand il est connecté ; les deux modes coexistent
photo par photo (`stockage:"dossier"` / `"cloud"`).

### Sous le capot
- `photoObjectURL(p)` factorise la lecture quel que soit le mode ; elle existe en
  stub dans le script principal (dossier seul) et est RÉDÉFINIE par le bloc cloud
  (téléchargement + cache) — parce que le premier rendu de l'écran photos arrive
  avant le chargement du module cloud. Dans la foulée, `cloudSession` est déplacée
  dans les globales du script principal : la zone d'ajout la lit au premier rendu,
  et une globale lue trop tard dans l'orbite de `loadAll()` est le piège TDZ
  documenté depuis la v4.9.
- Endpoints storage en REST direct (`/storage/v1/object/photos/…`, Bearer session,
  rafraîchie par `cloudRafraichirSession`) — toujours sans SDK. Cache « 400
  Duplicate » traité comme succès de ré-envoi.
- Les rapports générés n'embarquent pas les photos (inchangé) : aucun impact.

### Tests
148/148 au vert. Vérifié en session au navigateur : zone d'ajout dans ses trois
états (dossier / cloud / invitation), vignette cloud indisponible → estompée avec
l'info-bulle exacte contre le vrai endpoint Supabase (échec d'auth simulé),
suppression cloud sans exception, cache IndexedDB (écriture, lecture, effacement),
migration de policies vérifiée en base, aucune erreur console. L'upload réel avec
compte authentifié reste à éprouver sur le poste de Matis au premier usage — le
chemin POST est symétrique du GET testé.

## [4.15.0] — 2026-09-23

Analyse : les deux vues qui manquaient pour lire un essai dans son contexte — face à
un autre essai, et face à sa propre tolérance. Aucun changement de format de données.

### Ajouté — comparer deux essais
Le bouton **Comparer…** sur chaque essai ouvre un panneau : deux menus (A vs B,
groupés par scénario), les conditions côte à côte (scénario, date/équipe,
opérateur, maturité des bruts, **plaquettes figées à l'essai**, Vc/f/charnière,
nombre de prélèvements, % hors tolérance, statut) et les **courbes superposées**
par grandeur — battement puis chaque critère supplémentaire retrouvé par libellé —
chacune avec sa ligne de tolérance (« tol. A » / « tol. B », fusionnées si
identiques). Essai A en bleu plein, essai B en ambre tireté ; les séries reprennent
exactement la lecture de la Tendance (max Droite/Gauche sur EMAG 1, points de
mesure, axes par critère). Deux essais du même scénario affichent d'emblée le sens
de la lecture : la **répétabilité** — le fond du protocole 5× ; deux scénarios
différents : la comparaison de dérive. B est pré-rempli avec le premier autre essai
mesuré, de préférence du même scénario.

### Ajouté — les tendances en % de tolérance consommée
Chaque graphique de Tendance porte un bouton **« Voir en % de tol. »** : la mesure
est exprimée en pourcentage de la tolérance consommée (100 % = la limite, 0 % = la
borne mini si le critère a une plage min–max, sinon zéro), avec la ligne de
tolérance tracée à 100 % et un axe calé sur des graduations rondes. Utile pour lire
d'un coup d'œil un critère dont on ne connaît pas les valeurs par cœur, et pour
comparer des critères de nature différente sans mélanger leurs échelles physiques.
Option d'affichage seulement — jamais le défaut : un pourcentage reste une
normalisation, pas une mesure. Le bouton redevient « Voir les valeurs ». Nouveau
helper pur `pourcentageTolerance()` (4 tests).

### Tests
148/148 au vert (4 nouveaux). Vérifié en session au navigateur : panneau de
comparaison (tableau complet à deux colonnes, sélection A/B par optgroup, courbes
superposées avec légendes A/B, tolérances fusionnées quand identiques), cas
répétabilité (deux essais du même scénario, sous-titre dédié), bascule % dans les
deux sens (axe « % de la tolérance consommée », ligne « tolérance (100 %) »,
graduations 0/30/60/90/120, retour aux valeurs), aucune erreur console.

## [4.14.0] — 2026-09-23

Ergonomie du quotidien : les trois gestes qui revenaient chaque jour (reprendre la
saisie, retrouver un essai, savoir où on en est du protocole) deviennent des
raccourcis. Aucun changement de format de données.

### Ajouté — la ligne de reprise : le mode atelier à un clic
Le geste n°1 de la journée, c'est de continuer l'essai commencé avant. Il fallait
rouvrir le bon scénario, déplier le bon essai, trouver le bouton Mode atelier —
trois ou quatre gestes avant de pouvoir taper une mesure, debout devant la machine.
Un bandeau sous la navigation propose maintenant directement le dernier essai
**en cours** touché (`modifieLe` le plus récent, tous scénarios et OP confondus) :
titre, date, scénario, dernier prélèvement saisi, et ce qui manque. Boutons :
**Mode atelier** (le chemin court), **Ouvrir** (bascule d'arbre, déplie la tuile et
fait défiler jusqu'à elle — via le nouveau `allerVers()`, qui saute aussi le filtre
de projet s'il cachait le scénario visé), et **✕** (masque la proposition pour cet
essai ; elle revient seule dès qu'un essai plus récent devient le candidat). Un
essai conforme ou non conforme est une campagne close : il n'est jamais reproposé.
Si l'essai proposé est déjà ouvert à l'écran, le bandeau s'efface de lui-même.

### Ajouté — recherche partout (Ctrl+K)
L'arbre a grandi : lignes, références, OP, scénarios, dizaines d'essais, projets.
Une palette de recherche (Ctrl+K, ou bouton **Rechercher** du menu •••) indexe tout
cela : casse et accents ignorés (« reference disque » trouve « Référence disque »),
navigation ↑↓ puis Entrée, ou clic. Entrer sur un résultat d'essai positionne
l'arbre, déplie la tuile et y amène l'écran. L'index est reconstruit à chaque
ouverture — négligeable à cette échelle.

### Ajouté — le protocole 5× affiché là où on en est
La règle actée au site (un essai concluant répété 5× ; validé 5× + viabilité
économique → production) vivait en convention orale. Elle est maintenant portée par
l'outil : sous la cellule « Validation scénario » (« Protocole site : essai
concluant répété 5× + viabilité éco », avec info-bulle), en info-bulle sur le badge
« N/5 essais conformes » des tuiles, et dans le rapport de validation (« Critère de
passage en série : 5 essais conformes — protocole du site… Acquis à ce jour : N »).
Un scénario avec un seuil différent reste explicite (« seuil propre à ce scénario »).

### Ajouté — le mode atelier dit quand décider
La barre de progression montrait la distance parcourue, rien ne disait QUAND
trancher. À la charnière visée (la prochaine pièce l'atteint), un bandeau ambre
propose de resserrer le pas de mesure ou de décider : prolonger / arrêter. Au-delà,
il passe au vert : la durée de vie dépasse l'objectif — à exploiter tant que la
cote tient. La charnière visée reste celle de l'instantané de l'essai (figée à sa
création, comme les conditions de coupe).

### Tests
144/144 au vert. Vérifié en session au navigateur : bandeau de reprise (apparition
sur essai en cours, texte exact, masquage ✕, retour après render, disparition si
l'essai est déjà ouvert), Mode atelier depuis le bandeau (bon essai, bon logement),
bannière charnière dans ses trois états (ambre à la visée, vert au-delà, absente
loin), Ouvrir (bascule de scénario + tuile dépliée + carte dans le DOM), palette
Ctrl+K (ouverture, recherche par titre d'essai, Entrée = navigation + tuile
dépliée + panneau fermé, recherche insensible aux accents, état vide), protocole
affiché sous la validation et en info-bulle de tuile, aucune erreur console.

## [4.13.0] — 2026-09-23

Première tranche de la refonte UX cadrée dans `CAHIER_DES_CHARGES_UX_REFONTE.md`
(8 septembre 2026) : les étapes 1, 2 et les passes 3.4/3.6 du plan. Aucun changement
de format de données, aucune logique de calcul touchée.

### Modifié — un fil d'Ariane à la place des trois rangées de pastilles (CDC §3.1)
Ligne, Référence et OP s'affichaient en trois rangées de pastilles visuellement
identiques : trois strates à traverser avant le contenu, sans rien qui dise la
hiérarchie. Un seul fil maintenant — « EMAG 1 › Référence › OP10 » — où le niveau
courant se lit au poids du texte. Chaque maillon est cliquable et ouvre son propre
sélecteur ; les créations (« + Nouvelle ligne… », etc.), renommages et suppressions
vivent DANS ce sélecteur, avec les mêmes dialogues et les mêmes confirmations qu'avant.
L'icône ⚙ (coût horaire, observations, maintenance de la ligne) reste visible à côté
du premier maillon — leçon v4.2 : une action invisible n'est pas une action. En mode
consultation, le sélecteur ne propose plus que la navigation. `renderLignes`,
`renderReferences` et `renderOps` sont remplacées par `renderFilAriane()` ; un seul
écouteur délégué au document pilote le tout et survit aux re-rendus.

### Modifié — le menu ••• se lit en groupes nommés (CDC §3.2)
Les quatorze actions du menu étaient une liste plate où Réinitialiser voisinait le
Tableau de bord. Le menu est désormais groupé par nature — **Consulter** (Vue de
synthèse, Tableau de bord, Export CSV), **Documenter** (Rapport de validation,
Générer le PDF, Nouveautés), **Gérer** (Options, Démarrer un suivi, Suggestions,
Dossier local, Historique, nom d'auteur, révision) — et la zone destructrice
(Réinitialiser / Restaurer) reste séparée par un filet, en dernier. Le paragraphe
d'explication qui occupait la tête du menu est supprimé (CDC §3.5 : l'aide se
consulte via ⓘ, elle ne s'impose pas à chaque ouverture). Aucune action supprimée,
aucun id de bouton changé.

### Modifié — badges de même forme partout (CDC §3.4)
`.statut-pill`, `.status-badge` et `.tag-pill` (étiquettes de projet) partageaient
trois tailles de police, deux paddings et un traitement de casse différents. Ils ont
désormais la même géométrie (mono 10,5 px, padding 3×10, rayon plein) — seule la
couleur change selon le sens. Les statuts ne passent plus en majuscules forcées.

### Corrigé — le titre de l'en-tête déborde du cadre noir (CDC §3.6)
Un nom de référence long sortait du bandeau d'en-tête sans troncature propre. Le
titre tronque maintenant avec une ellipse et porte l'info-bulle native avec le texte
complet (`updateHeader` pose `title`). `text-wrap:balance` cédé la place au
comportement de troncature.

### Tests
144/144 au vert. Vérifié en session au navigateur : fil rendu sur une ligne, menus
des trois maillons (contenu selon niveau, maillon courant marqué ●), navigation
réelle par le menu (re-render complet), fermeture au clic extérieur et par Échap,
menu groupé dans l'ordre avec filet avant la zone rouge, mode consultation limité
à la navigation, aucune erreur console.

## [4.12.0] — 2026-09-22

### Ajouté — extractions Marposs multiples par essai (suggestion de Matis)
Un essai mené sur plusieurs jours (ex. 50 pièces le jour 1, 100 le jour 2) peut
maintenant coller **une extraction Marposs par journée**, dans un seul essai :
le bouton « + Ajouter une extraction » crée la journée suivante, avec son jour,
ses heures début/fin, son collage, ses moyennes journée/essai et **son propre
graphe** (plage horaire surlignée). Chaque extraction se supprime indépendamment.
La case « inclure dans le rapport » devient un drapeau de l'essai : le rapport
présente une sous-section par journée. Les données existantes migrent
automatiquement (l'ancien marposs unique devient la première extraction) —
aucun changement de format, rien à refaire.

## [4.11.2] — 2026-09-22

### Ajouté — le graphe de Tendance peut partir dans les rapports d'essai
Une case « Inclure le graphe de Tendance dans les rapports d'essai » dans le
bloc Essais du scénario (désactivée par défaut) : quand elle est cochée, chaque
rapport d'essai généré embarque les graphiques de tendance des critères suivis
(battement, Ra Inter/Exter, VE...) avec leurs lignes de tolérance — rendus avec
la palette du rapport, qui reste un fichier 100 % autonome.

## [4.11.1] — 2026-09-22

### Modifié — la Tendance trace tout critère évalué
Le graphique de tendance ne se limitait au battement : un essai jugé sur le Ra
se retrouvait sans courbe. Désormais chaque critère suivi a son propre graphe
« Tendance — {critère} en fonction du n° de pièce », avec sa ligne de tolérance
et sa borne mini si activée. Quand un critère porte plusieurs mesures (Ra
Inter / Ra Exter), chaque axe a sa courbe de couleur distincte — les évolutions
se comparent d'un coup d'œil. Le battement garde son graphe quand il est actif ;
les échelles ne se mélangent jamais entre critères.

## [4.11.0] — 2026-09-22

### Ajouté — on ne suit que ce qu'on veut suivre (sélection par essai)
Jusqu'ici, créer un essai snappshotait TOUS les logements du scénario :
progressions, colonnes et rapports s'imposaient même pour les outils qui ont
déjà atteint leur charnière et qui n'importent plus. Désormais chaque puce
« Conditions de l'essai » porte une croix : **✕ = ne plus suivre ce logement
dans cet essai**. Le logement reste dans le scénario (et re-suivable à tout
moment via « + suivre un logement »), son instantané est conservé (re-cocher
restitue les conditions d'origine), et ses prélèvements éventuels restent dans
le tableau — ils ne comptent simplement plus dans sa progression. Le tableau,
l'atelier, le graphique de tendance, le CSV et les rapports ne montrent plus
que les logements suivis. Aucun changement de format : la marque d'exclusion
s'ajoute aux instantanés existants, les essais anciens restent « tout suivi ».

## [4.10.1] — 2026-09-22

### Modifié — plus de logements pré-nommés à la création d'un scénario
Créer un scénario sur une ligne EMAG 1 pré-créeait automatiquement deux
logements nommés « Bol » et « Piste » : le bandeau récapitulatif de l'outil
les affichait donc même sur des montages qui n'en ont pas, et l'utilisateur
croyait à un bug d'affichage. Désormais le scénario arrive avec un outil vide —
l'opérateur crée et nomme ses logements lui-même (le bouton « + Logement »
propose « Logement 1 », « Logement 2 »… neutres, à renommer). Les données
existantes ne bougent pas : seules les futures créations sont concernées.

## [4.10.0] — 2026-09-22

Le travail à deux passe en fusion automatique. Aucun changement de format.

### Modifié — les conflits de synchro fusionnent au lieu de s'arbitrer à la main
Avant : « le cloud et ce poste ont changé — prendre le cloud ou déposer ma
version ? » (choix binaire, tout l'un ou tout l'autre). Désormais : **fusion
automatique essai par essai**, avec les règles déjà éprouvées par l'import
« Fusionner » — un essai présent seulement chez l'un est ajouté ; un même essai
modifié des deux côtés voit la version la plus récente gagner ; les réglages du
scénario (tolérances, critères, outils, conditions de coupe) restent à la version
locale. Le rapport de fusion détaille le résultat et liste les rares conflits
vrais (modifiés à la même seconde) à vérifier. La version du cloud remplacée
part à l'archive (20 versions), le résultat fusionné repart au cloud au cycle
suivant — les deux postes convergent sans geste.

### Ajouté — le journal de synchro, annoncé à l'ouverture
Chaque fusion/dépôt embarque une note dans le suivi (« fusion après le dépôt de
Matis : 3 essais ajoutés, 1 mis à jour, 0 conflit »). À l'ouverture, si l'autre
poste a déposé depuis votre dernière visite, l'outil le dit avant tout : qui,
quand, et le détail. Vos données sont déjà à jour quand le message s'affiche.

### Ajouté — traçabilité « modifié par »
Chaque essai porte désormais, à côté de son horodatage de modification, le nom
(ou le compte) de qui l'a touché — c'est ce qui alimente les messages et rend
l'arbitrage des fusions lisible.

## [4.9.1] — 2026-09-22

### Ajouté — heure de début d'essai
L'essai connaissait sa fin (date + heure) mais pas son début. Le champ « Début
essai » complète « Fin d'essai » dans l'en-tête, apparaît dans le rapport d'essai
(« 22/09/2026 · 08:00 → 09:30 ») et dans l'export CSV (colonnes « Heure debut » /
« Heure fin »). Le choix Matin / Après-midi / Nuit n'est pas touché : c'est le
champ Équipe (poste), utilisé par la dispersion entre équipes.

Bonus : la saisie de ces heures pré-remplit la fenêtre horaire du suivi Marposs
si elle est encore vide — la fenêtre reste modifiable séparément (la machine
contrôle toute la journée, l'essai une plage). Une seule saisie en pratique.

## [4.9.0] — 2026-09-22

Les critères de validation d'essai, refondus autour du retour terrain (Matis) :
chacun ses côtés, ses bornes, son activation — et les specs usine verrouillées.
Aucun changement de format : les nouveaux champs s'ajoutent aux objets existants
et un ancien fichier reste lisible (et lisible PAR un ancien fichier).

### Modifié — critères d'essai (bloc « Essais » de chaque scénario)
- **Le battement se décoche.** Un essai peut ne porter que sur l'état de surface.
- **Côtés Droite/Gauche sélectionnables par scénario** (les deux, droite seul,
  gauche seul) — un test mené sur un seul côté n'est plus jugé sur l'autre.
- **Critères supplémentaires en liste** : Ra, VE, ou tout critère libre nommé par
  l'opérateur. Chacun : borne maxi, **mini optionnelle** (plage min–max), et axes
  **Inter/Exter** (pistes) ou **Droite/Gauche** (broches) — une colonne de saisie
  par critère × axe, dans le tableau, le mode atelier, le CSV et les deux rapports.
  L'ancien « 2ᵉ critère » migre automatiquement vers cette liste au chargement.
- **La tolérance s'édite dans le bloc Essais**, toujours visible — l'éditer la rend
  spécifique au scénario (fini la case à cocher préalable) ; la valeur OP reste
  affichée comme repère.

### Ajouté — specs usine verrouillées (Options)
Battement ≤ 0,04 et VE ≤ 0,01 mesurés Marposs sur disque fini (après OP40,
finition) : référence pour toute l'usine, affichée sous les critères d'essai et
dans les rapports. Portée « Tous », voyage dans le suivi (cloud compris). Les
modifier exige une double validation : confirmation explicite, champs déverrouillés,
réenregistrement au reverrouillage — le panneau reverrouille à chaque ouverture.

### Ajouté — le graphe Marposs peut partir dans le rapport d'essai
Le suivi Marposs d'un essai (fenêtre horaire début–fin, relevés du jour collés,
graphe avec plage de l'essai surlignée) existait déjà dans l'outil ; une case
« Inclure ce graphe dans le rapport de l'essai » (désactivée par défaut pour ne
pas surcharger) ajoute au rapport généré la courbe du jour, la bande horaire de
l'essai, les moyennes journée/essai et la ligne de tolérance.

### Corrigé — l'ouverture des pièces jointes intégrées
Les PDF intégrés au suivi (plans, fiches outil) ne s'ouvraient plus :
`window.open()` sur une URL `data:` est bloqué par les navigateurs modernes.
Les documents passent maintenant par un fichier temporaire ; les images par
l'agrandissement plein écran.

### Sous le capot — un piège désamorcé
`loadAll()` est protégé par un `try/catch` silencieux : une variable déclarée
après son appel (TDZ) faisait repliquer tout le chargement sur les données
d'exemple sans aucun message. Les nouvelles globales se déclarent désormais
avant l'appel, avec un commentaire qui explique le piège.

## [4.8.0] — 2026-09-22

La synchro multi-postes via Supabase : la fin de l'échange manuel de JSON entre
Benjamin et Matis. Format de données inchangé — le cloud porte exactement le
même JSON que l'export (format 8), les allers-retours avec un poste hors cloud
restent donc possibles dans les deux sens.

### Ajouté — Options → Cloud, et une pastille ☁ en pied de page
Connexion par email + mot de passe (comptes créées côté Supabase). Une fois
connecté, le poste synchronise : tirage au chargement, au retour sur l'onglet
et toutes les 90 s ; dépôt automatique 4 s après chaque sauvegarde. Client
écrit à la main en `fetch()` (auth + REST) : pas de SDK, le fichier unique et
l'usage hors ligne restent la règle — sans réseau, l'outil marche comme avant
et la pastille dit « hors ligne », la synchro repart au retour du réseau.

### Le premier contact ne mélange jamais rien
Un cloud vide ne reçoit rien sans geste volontaire (bouton « Déposer ce
suivi ») — le jeu d'exemple d'un poste ne peut pas partir au cloud par
accident. Un cloud déjà rempli face à un poste qui a des données : l'outil
affiche le CV des deux versions (essais, date, auteur, marqueur [Exemple]) et
demande qui fait autorité, avec export de secours téléchargé avant tout
remplacement. Un conflit en cours de route (l'autre a déposé pendant que ce
poste saisissait) suit le même rituel. Aucune fusion automatique au premier
contact : la fusion essai par essai reste l'affaire de l'import manuel.

### Sous le capot
- Table `etat` (une ligne, `modifie_le` tenu par un trigger Postgres — le
  tampon horaire d'arbitrage n'est jamais calculé côté client) + table
  `etat_historique` plafonnée à 20 versions par trigger (filet de sécurité,
  le plan Free n'ayant pas de backups). RLS `authenticated` + GRANT (leçons
  Fellow), bucket privé `photos` préparé pour une étape suivante.
- Le tirage réutilise la machine d'import (« remplacer tout », avec son
  ↺ Restaurer) via un nouveau `preparerImportDepuis()` partagé par l'import
  fichier et le cloud — mêmes migrations de format garanti des deux côtés.
- Un hook dans `saveData()` marque le poste « sale » ; neutralisé pendant
  l'application d'un tirage pour qu'un pull ne se re-pousse pas en boucle.

## [4.7.1] — 2026-09-22

Deux corrections de la couche de fenêtres modales introduites en v4.6, dont une
rendait invisibles toutes les confirmations ouvertes depuis un panneau. Aucun
changement de format de données.

### Corrigé — les confirmations invisibles derrière les panneaux
Le dialogue de confirmation partageait le `z-index` des autres panneaux et était
déclaré avant eux dans le DOM : ouvert par-dessus le panneau projet, dashboard ou
import, il s'affichait en réalité **derrière**. Symptôme vu sur le terrain :
« Supprimer ce projet » semble ne rien faire (le dialogue est là, mais caché, et
le clavier est piégé dedans). Toutes les confirmations du même type étaient
touchées (suppression de responsable, fermeture de l'éditeur d'annotation…).
Le dialogue passe désormais au-dessus de tout (`z-index:120`).

### Corrigé — le panneau de création de projet restait ouvert
`fermerPanneaux()` fermait une liste de panneaux codée en dur, dans laquelle
`projetCreatePanel` (ajouté en v4.5) avait été oublié : après « Créer le
projet », le panneau de création restait empilé sous celui d'info, et un second
clic sur « Créer le projet » créait un doublon. La fermeture est généralisée à
tous les `.panel` — un futur panneau sera couvert d'office.

## [4.7.0] — 2026-09-09

Réorganisation du panneau Options, dont l'intégration du coût machine dispersait ses
réglages entre Options et l'icône ⚙ de l'onglet de ligne, sans dire les portées.
Aucun changement de format de données.

### Modifié — Options découpé par nature, portées affichées
Le panneau mélangeait quatre natures de réglages (mesure, économie, affichage, équipe)
sans séparation, et la note du module machine renvoyait ailleurs (« renseignez le coût
horaire via l'icône ⚙ de l'onglet de ligne ») — un écran qui t'envoie ailleurs pour
finir une configuration commencée chez lui est un écran mal fichu.

- Trois sections titrées : **Mesure & essais** (tolérance, marge charnière, cycle
  détaillé + fiche outil, Fr/Fa), **Coûts** (rebut, cycle en secondes, temps machine,
  pièces détachées, volume annuel), **Équipe** (responsables).
- Badge de portée sur chaque réglage : `OP`, `Référence`, `Ligne`, `Tous`. La ligne de
  contexte en tête de panneau nomme l'OP/référence/ligne ouverts et explique les badges.
- Ancien intitulé « Modules de calcul » supprimé (il ne disait rien des portées).

### Ajouté — le coût horaire de la ligne se saisit dans Options
Nouveau champ `optCoutHoraire` dans la section Coûts, affiché quand le module temps
machine est coché. Il écrit dans `ligne.coutHoraire` — exactement la même donnée que
l'icône ⚙ de l'onglet de ligne, qui reste fonctionnelle : même champ, deux portes
d'entrée. Plus aucun renvoi croisé pour finir une configuration.

### Ajouté — état calculé du coût machine, à la place de la note statique
La note des « quatre choses nécessaires ensemble » était fausse sur un point : la case
« Afficher le temps de cycle en secondes » est une commodité d'affichage, pas une
condition du calcul (`cycleSecondes` ne la consulte pas ; seuls `coutMachineActif`,
`cycleRefSec` et `coutHoraire` comptent). Un texte statique dérive toujours du code —
le statut est désormais calculé par `etatCoutMachine(cfg, ligne)` :

- module coché et tout renseigné : statut vert « Coût machine actif — X €/h × temps de
  cycle. Les écarts de cycle pèsent maintenant dans le coût pièce et le gain annuel. » ;
- sinon : statut ambre listant exactement ce qui manque (temps de cycle de référence
  et/ou coût horaire) et la conséquence (« aucun écart de cycle ne pèse dans le gain
  annuel »).
- `runTests()` : 4 nouveaux tests sur `etatCoutMachine` (complet, coût horaire cité,
  cycle de référence cité, module éteint).

### Nettoyé
- `optCoutHoraireRappel` (rappel texte du coût horaire) supprimé, remplacé par le
  statut calculé et le champ en place.
- La section « Comment ça marche » renvoie désormais vers la section Coûts d'Options
  pour le coût horaire, en gardant la mention de l'icône ⚙.

## [4.6.0] — 2026-09-09

Trois chantiers issus de la revue UX externe (pertinence/architecture/UX) : la fin des
fenêtres système, l'encodage de la convention de démarrage, et une passe accessibilité
clavier. Aucun changement de format de données.

### Ajouté — dialogues in-app : les 27 `alert()`, 20 `confirm()` et 4 `prompt()` natifs remplacés
Derniers vestiges de fenêtres système grises : cassaient l'identité visuelle (et le mode
nuit), et ne supportaient aucune mise en forme — les messages les plus importants (panne de
stockage, garde-fou double comptage) étaient des murs de texte brut.

- Nouveau panneau `#dialogPanel` (même famille visuelle que les autres panneaux), piloté par
  trois helpers : `dialogueAlerte()` (alerte), `dialogueConfirmer()` (confirm, promesse de
  booléen), `dialogueDemander()` (prompt, promesse de texte ou null).
- Sémantique native conservée : Échap et clic hors panneau = Annuler (déjà câblés sur
  `fermerPanneaux`), Entrée dans le champ = valider, défaut de focus sur le geste
  réversible (« Annuler »).
- Nouveau style `danger` (bouton rouge) pour les suppressions et la réinitialisation —
  la validation par saisie exacte de « REINITIALISER » est conservée.
- `promouvoirEnProduction()` scindée en `questionsPromotion()` (les questions, testables
  hors DOM) + `appliquerPromotion()` (l'effet, synchrone) + le chemin interactif (promesse).
  Le chemin accepte un injecteur de réponse pour les tests ; les garde-fous v4.5
  (double comptage, annonce du remplacement) passent par les mêmes dialogues, avec
  « Passer en série quand même » comme libellé explicite sur le premier.
- Les appelants asynchrones sauvegardent après résolution de la promesse (statut-select,
  pastille ★), pour ne jamais persister un état muté après coup.
- `runTests()` : 5 nouveaux tests (échappement `dlgTexte`, valeurs absentes, contenu des
  questions de promotion, application synchrone, refus sans mutation) — 140/140.

### Ajouté — parcours de démarrage : la convention v4.4 devient un guide
« Poser le scénario en production d'abord, créer les projets ensuite » n'était qu'une
convention à transmettre oralement ; elle est maintenant dans l'outil.

- Menu **••• → Démarrer un suivi** : panneau checklist à trois étapes (ligne → scénario ★
  sur l'OP → premier projet), qui se coche tout seul selon l'état réel du suivi
  (`etatParcours()`), avec le « pourquoi » de chaque étape.
- Bandeau bleu sur un OP vierge (ni scénario en production, ni projet) : rappel court,
  « Voir le parcours » ouvre le panneau, « Masquer » le retire définitivement sur ce poste
  (`spk_parcours_masque`). Il disparaît seul dès qu'une étape 2 ou 3 est franchie.
- Les projets restent facultatifs : le panneau le dit explicitement.

### Ajouté — accessibilité clavier des panneaux
- `ouvrirPanneau()` pose `role="dialog"` + `aria-modal="true"`, entre le focus dans le
  premier champ du panneau (sinon le panneau lui-même) et retient l'élément déclencheur ;
  `fermerPanneaux()`/`fermerDialogue()` restaurent le focus d'origine.
- La touche Tab reste piégée dans le panneau du dessus (pile de panneaux) : plus de focus
  perdu derrière le voile. Échap et le clic hors panneau gardent leur comportement.
- Les icônes du menu ••• portaient déjà des libellés visibles ; le statut de sauvegarde
  avait déjà son `role="status"`.

### Corrigé — le dernier point de la tendance collait au bord droit
`chartHTML()` et `multiChartHTML()` bornaient l'axe X au max des données (ou de la
charnière) : le point le plus avancé tombait exactement sur le cadre, à moitié coupé.
Une marge de 8 % sépare désormais le dernier point du bord.

## [4.5.0] — 2026-09-09

Deux garde-fous ergonomiques issus de l'audit externe (revue Hermes) et de sa relecture,
plus deux ajustements de confort. Aucun changement de format de données.

### Ajouté — garde-fous contre le double comptage inter-projets (le concept de la v4.1
non poussée, réécrit pour le modèle v4.4 où le projet est une étiquette, pas un propriétaire)
Dans le modèle actuel, le piège se joue au niveau du **scénario** : deux projets peuvent
étiqueter chacun un scénario différent, du même nom, « en série », sur la même ligne — deux
descriptions du même changement physique, et le tableau de bord additionne leurs gains sans
le savoir.

- `scenariosSerieHomonymes()` : détecte les groupes (nom de scénario + nom de ligne,
  insensibles à la casse et aux espaces de bord) où des scénarios « en série » distincts
  sont étiquetés dans plusieurs projets. Le **même** scénario étiqueté dans deux projets
  n'est PAS un homonyme (c'est un seul objet, compté une seule fois par construction).
- `avertissementSerieHomonymes(sc)` : appelée par `promouvoirEnProduction()` avant le
  passage en série — cite les projets où un homonyme est déjà en série sur la même ligne.
  Confirmation demandée, refus possible (rien n'est modifié), jamais bloquant.
- Tableau de bord, vue tous projets (≥ 2 projets, sans filtre) : bandeau ambre
  `.db-alerte-homonymes` listant les homonymes et rappelant la règle.
- `runTests()` : 5 nouveaux tests (cas sains non signalés, casse/espaces détectés,
  chemins cités).

### Ajouté — pastille permanente du poids du suivi
Le quota ne se voyait qu'au moment de l'alerte (souvent trop tard pour agir sereinement).
Une pastille en pied de page affiche en continu le poids du suivi sur ~5 Mo : neutre sous
60 %, ambre de 60 à 85 %, rouge au-delà. Le clic donne le détail (même contenu que
l'alerte) et les conseils pour alléger. Rendue à l'ouverture et à chaque sauvegarde.

### Modifié — la création de projet passe par un panneau
Le `prompt()` natif détonnait avec le reste de l'outil. Nouveau panneau (même famille que
le panneau projet) : champ nom, annonce du rattachement automatique (« N scénario(s) de
l'OP ouvert seront rattachés »), Enter valide, Annuler ferme. La création passe ensuite
par le panneau projet habituel comme avant.

### Ajouté — récap du rattachement automatique dans le panneau projet
Un projet créé rattache d'office les scénarios de l'OP ouvert (comportement v4.3 conservé),
mais rien ne le disait : le panneau projet affiche désormais « N scénario(s) rattaché(s)
automatiquement à la création » le jour de la création, avec l'invitation à ajuster les
étiquettes.

## [4.4.1] — 2026-09-08

Correctif robustesse remonté par l'audit externe (revue Hermes) de la 4.4.0 : collision
d'identifiants à la création.

### Corrigé — deux objets créés dans la même milliseconde avaient le même id
Les scénarios, lignes, références et OP recevaient un id `"s"+Date.now()` (idem l/r/o).
Deux créations dans la même milliseconde — double-clic sur « Dupliquer » ou
« + Ajouter un scénario », gestes scriptés — produisaient le **même id** : `data.find(id)`
pointait alors au mauvais endroit, un scénario en écrasait un autre, un projet pouvait
taguer le mauvais scénario. Reproduit pendant l'audit (5 copies → 1 seul id) ; probabilité
faible en usage calme mais corruption silencieuse quand ça arrive.

- Nouveau helper `uid(prefix)` : `prefix + Date.now().toString(36) + aleatoire` — le
  pattern déjà utilisé pour essais/prélèvements/outils/logements, étendu à s/l/r/o.
  `pj` reste géré par `normalizeProjet` (déjà aléatoire).
- Les 15 sites de création concernés passent par `uid()` (migrations legacy, import ancien
  format, création ligne/référence/OP/scénario, duplication).
- `runTests()` : 2 nouveaux tests (200 ids générés d'affilée tous uniques, préfixe respecté).

Aucun changement de format de données : les id existants ne sont pas touchés, seule la
génération des nouveaux change.

## [4.4.0] — 2026-09-08

Repart de la discussion sur la logique d'atelier réelle : très peu de données saisies par
Matis à ce stade, et Benjamin veut clarifier AVANT que la saisie s'accélère la relation entre
« ce qui tourne en série sur la machine » et « les projets qui organisent le travail dessus ».
Décision : chaque OP a un seul scénario en production, immuable au sens où il s'affiche
toujours (pas au sens où il serait figé/non éditable) ; les projets s'organisent PAR-DESSUS,
une fois cette brique posée.

### Ajouté — le scénario en production, un seul concept
Jusqu'ici, le badge ★ (`baseline`, scénario de comparaison base 100) et le statut « En série »
étaient deux champs indépendants qui pouvaient diverger sans que rien ne le signale — un
scénario ★ qui ne serait pas réellement en série n'a pourtant aucun sens dans cet outil.
Unifiés : `normalizeScenario()` force `statut:"serie"` dès que `baseline:true` sur toute
donnée chargée (fichier ancien, import, édition manuelle du JSON). L'interface l'empêche
désormais de diverger à la source :
- `appliquerChangementStatut()` refuse de sortir un scénario ★ de « En série » directement
  (message expliquant qu'il faut d'abord désigner un autre scénario comme référence) ;
- `statutSelectHTML()` affiche un verrou 🔒 avec info-bulle sur le menu déroulant du scénario
  en production, sans pour autant le rendre inerte : un changement tenté déclenche le refus
  ci-dessus puis se réaffiche correctement au re-rendu.

### Ajouté — promotion et rétrogradation
`promouvoirEnProduction(sc)` : désigner un scénario comme nouvelle référence (bouton ★ ou
menu statut sur « En série ») retire le badge à l'ancien et le rétrograde en **« Validé »**
(jamais « Abandonné » — il n'a rien raté, il a juste été remplacé), avec une date de statut
posée si elle manquait. Un `confirm()` annonce l'échange avant qu'il n'ait lieu (« Faire de
« X » le scénario en production ? Il remplace « Y » … son statut passera à « Validé » ») ;
annuler ne change rien. Le clic sur la pastille ★ et le passage du menu statut à « En série »
partagent désormais ce même chemin (`onInputChange` route les changements de
`select.statut-select` vers `appliquerChangementStatut` plutôt que l'écriture générique de
champ).

### Ajouté — visibilité toujours acquise, indépendante des statistiques
`scenariosVisibles()` (filtre réel du bandeau, v4.3) exempte désormais le scénario en
production : il reste dans la liste même si le projet actif ne le contient pas, ou si aucun
projet ne le mentionne du tout — c'est la référence de l'OP, elle ne doit jamais disparaître
pendant qu'on travaille filtré sur un projet. Cette exemption est strictement une exemption
d'AFFICHAGE : `projetContientScenario()` et `statsProjet()` restent inchangées, un scénario en
production non étiqueté dans un projet ne compte donc jamais dans les statistiques de ce
projet malgré sa présence à l'écran. Décision pesée explicitement pour ne pas fausser les
chiffres qu'un projet remonte sur ce qu'il couvre réellement.

### Modifié — info-bulle du badge ★ (pas de renommage)
Le libellé « ★ Scénario réf. » n'est pas renommé (déjà changé une fois en 3.14.0, éviter la
valse d'intitulés dans les rapports et habitudes). Son info-bulle est en revanche étoffée pour
expliquer, sans ambiguïté, que le désigner en fait le scénario en production (statut verrouillé
sur « En série », visibilité garantie même filtré par un projet).

### Portée volontairement non étendue
Le point de départ conceptuel de cette version — poser d'abord toute l'arborescence
lignes/références/OP avec leur scénario en production, PUIS créer des projets par-dessus —
reste pour l'instant une convention d'usage à transmettre à Matis, pas une contrainte imposée
par le logiciel : rien n'empêche techniquement de créer un projet avant d'avoir posé de
scénario en production sur l'OP. Aucune UI de "workflow guidé" n'a été ajoutée ; un ajustement
pourra suivre si l'usage réel montre que la convention seule ne suffit pas.

### Tests
129/129 (6 ajoutés) : `normalizeScenario` verrouille le statut à `serie` quand `baseline` est
vrai ; `appliquerChangementStatut` refuse de sortir le scénario en production de « En série » ;
`promouvoirEnProduction` bascule la référence et rétrograde l'ancien en « Validé » lors d'une
confirmation acceptée, n'effectue aucun changement si elle est refusée ; `scenariosVisibles`
inclut le scénario en production même non étiqueté dans le projet actif tout en le laissant
absent du calcul de `projetContientScenario` pour ce même projet.

Vérifié en session, au-delà des tests automatisés : verrou visuel 🔒 affiché sur le menu statut
du scénario ★, tentative de changement direct refusée avec message et menu réaffiché sur sa
vraie valeur après re-rendu ; clic sur ★ d'un autre scénario déclenchant le `confirm()` exact
annoncé, ancien scénario repassé en « Validé », nouveau en « En série » ; round-trip complet
vers la 3.19.2 réussi (lignes, essais, prélèvements et le champ `baseline` intacts — aucun
changement de structure racine, seul le comportement applicatif évolue).

## [4.3.0] — 2026-09-08

Correctif de fond suite à un retour d'usage direct de Benjamin : le filtre de projet livré
en 4.1/4.2 ne faisait que du cosmétique — activer un projet changeait le bandeau de cartes
mais ne touchait jamais à la liste des scénarios sur laquelle on travaille au quotidien.
Deux mécanismes de filtrage qui ne se parlaient pas, d'où le symptôme remonté : « je clique
sur une ligne, ça m'affiche des projets qui n'ont rien à voir ».

### Corrigé — bug réel : projet sans étiquette visible sur toutes les lignes
`projetVisibleSurLigne()` traitait tout projet à 0 étiquette comme visible partout, sans
distinction. Nouveau champ `projet.ligneCreation` (posé à la création) : un projet sans
étiquette n'est désormais visible **que sur la ligne où il a été créé**. Comportement legacy
(visible partout) conservé uniquement pour un projet créé avant la 4.3, qui n'a pas ce champ
— pour ne pas le faire disparaître sans explication à la mise à jour.

### Ajouté — le filtre scope réellement le travail
Nouvelles fonctions `opOrganiseParProjets()` et `scenariosVisibles()` :
- si aucun scénario de l'OP courant n'est étiqueté dans un projet, rien n'est filtré —
  comportement identique à avant l'existence des projets, pour ne rien changer à qui ne s'en
  sert pas ;
- dès qu'au moins un scénario de cet OP appartient à un projet, et qu'un projet précis est
  actif, la liste se scope réellement : seuls les scénarios de ce projet s'affichent
  (`renderTabs()`). Les autres restent dans l'outil, simplement masqués.

`render()` reconduit `activeId` vers le premier scénario encore visible si le filtre masque
celui qui était ouvert — jamais un panneau de détail affichant un scénario que la liste dit
ne pas montrer. Un état vide dédié (« Aucun scénario de « X » sur cet OP », avec un bouton
« Voir tous les scénarios de cet OP ») couvre le cas où le projet actif ne touche rien ici,
plutôt qu'un écran vide sans explication ni échappatoire.

Le numéro de chaque tuile reste calculé sur la liste complète de l'OP, pas sur la liste
filtrée — sinon « le scénario 3 » changerait de sens selon le projet ouvert.

### Modifié — création d'un projet
« Créer un projet ici » rattache désormais **tous les scénarios de l'OP ouvert**, pas
seulement celui affiché au moment du clic (l'ancien mécanisme, fragile : un projet créé sans
scénario actif restait vide et devenait le « fantôme visible partout » du bug ci-dessus).
L'association à la ligne se fait donc directement par l'acte de création, sans dialogue
supplémentaire — on affine ensuite au cas par cas avec les étiquettes des cartes de scénario.

### Ajouté — documentation intégrée
La section « Comment ça marche » de l'outil (icône ⓘ) n'avait jamais été mise à jour depuis
l'arrivée des projets — corrigé, avec une explication du filtre réel ci-dessus.

### Portée volontairement non étendue
La synthèse comparative, l'export CSV et l'impression restent **non filtrés** par le projet
actif — ce sont des vues de comparaison où voir l'ensemble reste souvent le but recherché,
y compris en travaillant principalement dans un projet. Seul le bandeau de travail quotidien
(`renderTabs`) applique le filtre réel.

### Tests
123/123 (10 ajoutés) : projet neuf visible sur sa ligne de création et caché ailleurs,
compatibilité d'un projet legacy sans ce champ, `opOrganiseParProjets()` vrai/faux selon
qu'un scénario de l'OP est étiqueté ou non, `scenariosVisibles()` dans les trois états (aucun
filtre, OP non organisé, OP organisé avec projet actif ne contenant rien ici — liste vide et
non un repli silencieux sur tout).

Vérifié en session : projet créé avec 3 scénarios auto-rattachés, un retiré manuellement puis
absent de la liste filtrée sans être supprimé de l'outil ; bascule automatique du scénario
ouvert quand le filtre le masque ; état vide avec échappatoire fonctionnelle ; bug d'origine
reproduit puis confirmé corrigé (un nouveau projet sur EMAG 1 n'apparaît plus sur Step 3) ;
round-trip complet vers la 3.19.2 toujours réussi (lignes/scénarios/prélèvements intacts).

## [4.2.0] — 2026-09-08

Suite directe des retours d'usage sur la 4.1.x, tous traités dans cette version : ergonomie
du panneau projet, gestion des pilotes avec couleur, identité visuelle par projet, zone de
texte étendue. Décisions posées dans `CAHIER_DES_CHARGES_PROJETS_V2.md`, validées avant
codage.

### Corrigé — visibilité des actions existantes
- Le bouton d'édition d'un projet était une icône ⚙ 22×22 px transparente jusqu'au survol
  (`.pj-cfg`) — personne ne la trouvait. Remplacée par un bouton texte **« Modifier »**,
  visible en permanence, hors de la carte cliquable (`.pj-modifier`, sibling de `.pj-corps`
  plutôt que bouton imbriqué dans un bouton — l'ancien markup était `<button>` dans
  `<button>`, invalide en HTML, corrigé au passage).
- Le bouton qui enregistre le panneau projet s'appelait « Fermer » alors qu'il sauvegardait
  déjà (`enregistrerProjetInfo()` puis fermeture) — renommé **« Enregistrer »**. Aucun
  changement de comportement, seulement de l'étiquette.
- « + Créer un projet » / « + Nouveau projet » passent de `button.ghost.small` (11 px,
  transparent) à `button.primary` — aussi visibles que « + Ajouter un scénario ».
- Le tableau de bord signale maintenant qu'un OP porte des scénarios de plusieurs projets à
  la fois (pastilles colorées dans `.db-op-head`, calculées sur l'ensemble des scénarios de
  l'OP — pas seulement ceux visibles sous un filtre de projet actif, qui masquerait
  justement la cohabitation qu'il s'agit de signaler). Cette capacité existait déjà
  (modèle par étiquettes, v4.1) ; seule sa visibilité manquait.

### Ajouté — responsables gérés, avec couleur
Nouvelle liste racine `responsables: [{id, nom, couleur}]`, gérée dans Options (ajout avec
sélecteur `<input type="color">`, suppression avec confirmation). `projet.responsableId`
remplace le champ texte libre `projet.responsable` comme source de vérité en saisie — un
menu déroulant dans le panneau projet, avec une option **« + Nouveau responsable… »** qui
crée la personne à la volée sans quitter le panneau (couleur assignée automatiquement,
modifiable ensuite dans Options).

- Migration automatique : un projet issu d'un fichier antérieur (v4.0/4.1) avec un champ
  `responsable` texte libre voit ce texte devenir une entrée de la liste gérée
  (`finaliserProjetsEtResponsables`, appelée par `migrerArbre` pour les trois formats lus),
  couleur assignée par cycle sur `OUTIL_COLORS`. Aucune saisie perdue ni à ressaisir.
- Suppression d'un responsable : les projets qu'il pilotait repassent à « Aucun », jamais de
  suppression en cascade.
- Fusion : `fusionnerResponsables()` — correspondance par id ou par nom (deux « Julien »
  créés indépendamment sur deux postes ne se dupliquent pas), couleur locale jamais écrasée
  par le fichier reçu.
- La couleur du responsable habille la bordure gauche de ses cartes de projet — remplace
  l'ancien codage par statut sur cet axe. Le statut reste lisible via son badge texte,
  inchangé. Choix documenté : deux informations différentes (qui pilote / où en est le
  projet) ne doivent pas se disputer un seul axe couleur.

### Ajouté — identité visuelle par projet
Chaque projet reçoit une couleur à sa création (`OUTIL_COLORS[projets.length % ...]`,
stockée une fois pour toutes, jamais recalculée au rendu pour ne pas « sauter » d'une
session à l'autre). Appliquée à un petit point sur sa carte (`.pj-puce`) et à ses étiquettes
actives sur les cartes de scénario (`.tag-pill.on`, auparavant uniformément bleues quel que
soit le projet) — avec plusieurs projets sur un même scénario, chaque étiquette reste
identifiable sans lire son texte. Axe volontairement distinct de la couleur du responsable
(voir ci-dessus) : le confondre ferait porter deux informations différentes à une seule
couleur.

### Modifié — description du projet
Champ `problematique` (nom interne inchangé — aucune donnée à migrer) renommé
**« Description »** en interface et passé d'un `<input>` une ligne à un `<textarea>` de 5
lignes, redimensionnable : assez de place pour l'objectif et les moyens mis en œuvre, plus
seulement une phrase.

### Format de fichier : 8
`lignes` reste la racine, exactement comme les formats 5 et 7 — `responsables` et les
nouveaux champs de projet (`couleur`, `responsableId`) sont des ajouts, pas une
restructuration. Vérifié : un export produit par cette version, rechargé dans le code de la
3.19.2, restitue lignes/scénarios/prélèvements intacts ; seuls `projets` et `responsables`
lui restent invisibles.

### Hors périmètre (rappel)
Rattacher un projet à une référence disque entière reste écarté (décision v4.1.1) — deuxième
granularité d'étiquette, questions d'héritage non résolues pour un besoin quasi inexistant.

### Tests
115/115 (13 ajoutés) : défauts de `normalizeResponsable`, migration d'un `responsable` texte
libre vers la liste gérée avec couleur assignée et lien `responsableId` correct, assignation
de couleur aux projets migrés sans couleur, `prochaineCouleurLibre` (évite les doublons tant
qu'il reste une couleur libre, recycle sans exception au-delà), fusion de responsables par id
ou par nom sans duplication ni écrasement de couleur locale.

Vérifié en session, au-delà des tests automatisés : création d'un responsable à la volée
depuis le menu déroulant du panneau projet, couleur répercutée sur la bordure de carte,
suppression depuis Options sans toucher au projet, deux projets avec des couleurs
d'identité distinctes visibles sur leurs cartes et sur les étiquettes d'un scénario partagé,
repère multi-projets affiché au niveau d'un OP dans le tableau de bord, description
multi-lignes enregistrée et restituée, filtre des cartes par ligne (v4.1.1) toujours
opérationnel, fichier réel de production (format 5) chargé sans perte ni projet fantôme,
round-trip complet 4.2.0 → 3.19.2 réussi.

## [4.1.1] — 2026-09-08

Retour d'usage immédiat sur la 4.1.0 (déployée le jour même sur le domaine de test) : les
cartes de projet s'affichaient toutes, sur toutes les lignes, sans rapport avec la ligne
ouverte. Ce n'était pas voulu — juste une simplification prise en construisant la
fonctionnalité, sans peser le sens inverse du principe déjà appliqué à la navigation
(« la ligne/référence/OP ne se filtrent jamais par projet »).

### Corrigé — cartes de projet filtrées par ligne
`projetVisibleSurLigne(pj, ligneId)` décide de la visibilité d'une carte : visible si (a)
c'est le projet actif — on doit toujours pouvoir voir/désactiver ce qu'on a sélectionné, même
en étant sur une autre ligne, un projet pouvant volontairement couvrir plusieurs lignes —, ou
(b) il a déjà au moins une étiquette sur cette ligne, ou (c) il n'a **encore aucune étiquette
nulle part** (projet tout juste créé). Cette dernière règle est la plus importante : sans elle,
un projet neuf ne s'affiche nulle part et on ne peut jamais y rattacher un premier scénario.

`renderProjets()` gère trois états : la liste filtrée normale, l'absence de projet pertinent
sur la ligne courante (bandeau qui le dit explicitement plutôt que de paraître vide, avec un
lien pour voir les projets existant ailleurs), et une bascule « Voir tous les projets » /
« Filtrer sur cette ligne » — état volatil (`bandeauProjetsTousAffiches`, non persisté, comme
le filtre du tableau de bord), remis à zéro à chaque changement de ligne pour rester une
échappatoire ponctuelle plutôt qu'un réglage qui reste collé.

Les étiquettes cliquables sur les cartes de scénario restent volontairement **non filtrées** :
elles permettent de rattacher délibérément un scénario à un projet d'une autre ligne (c'est
tout l'intérêt du modèle par étiquettes face à l'ancien modèle par propriété), alors que le
bandeau du haut sert à ne montrer que ce qui est pertinent au premier coup d'œil.

Nettoyage au passage : `projetsBandeauOuvert`, un identifiant DOM vérifié dans une condition
mais ne correspondant à aucun élément (donc toujours `null`, condition sans effet réel),
retiré.

### Discuté et volontairement écarté
Rattacher un projet à une référence disque entière (plutôt qu'à des scénarios un par un) a été
envisagé puis abandonné : ça aurait introduit une deuxième granularité d'étiquette, avec les
questions d'héritage et de précédence que ça pose (une référence taguée inclut-elle les futurs
scénarios ? comment exclure une exception ?) — exactement le type d'ambiguïté que le passage de
la 4.0.0 à la 4.1.0 a cherché à éliminer. Le rattachement multi-lignes, en revanche, ne demande
aucun changement : le modèle par étiquettes le permettait déjà nativement (un projet est une
liste de scénarios, indépendamment de leur ligne).

### Tests
102/102 (5 ajoutés) : visibilité d'un projet mono-ligne sur sa ligne et sur une autre, d'un
projet cross-ligne des deux côtés, d'un projet neuf sans étiquette, et persistance de la
visibilité du projet actif hors de sa ligne.

Vérifié en session : 4 projets réels (mono-ligne EMAG 1, mono-ligne Step 3, cross-ligne, neuf)
répartis correctement entre deux lignes ; projet actif resté visible et marqué en changeant de
ligne ; bandeau « aucun projet ici » avec bouton d'échappatoire quand c'est le cas ; retour
automatique au filtre après un changement de ligne suivant un « voir tous ».

## [4.1.0] — 2026-09-08

Les projets reviennent, sur un modèle différent. Retour d'expérience et revue externe
(Hermès) sur la 4.0.0, retirée quatre jours plus tôt : elle avait mis la coupure de propriété
au-dessus de la machine (`Projet → Ligne → Référence → OP → Scénario`), forçant une ligne de
production à n'appartenir qu'à un seul projet. Une ligne physique — une machine, un coût
horaire, une référence disque — est un fait unique ; en faire la propriété exclusive d'un
projet confondait « le projet possède la machine » avec « le projet s'intéresse à certains
essais menés sur la machine ».

### Le modèle : des étiquettes, pas un propriétaire
L'arbre physique redevient racine, exactement comme avant la 4.0.0 : `lignes` n'est plus
réassigné selon le projet ouvert, toute la gymnastique `syncActiveProjet()` de la 4.0.0
disparaît. Un **projet** (`normalizeProjet`) est désormais une liste d'étiquettes
(`{ligneId, referenceId, opId, scenarioId}`) posées sur des scénarios existants, plus les
quatre informations que la 4.0.0 avait raison d'inventer : problématique, pilote, statut,
échéance.

Conséquences directes de ce choix :
- **Un scénario peut appartenir à plusieurs projets.** Le cas qu'un modèle en arbre ne peut
  pas exprimer (« cette plaquette est testée à la fois pour le coût sur EMAG 1 et pour l'état
  de surface pour Step 3 ») devient une simple étiquette de plus.
- **Pas de double comptage.** Un scénario « en série » a une seule adresse ; le tableau de
  bord additionne des scénarios uniques, jamais des copies.
- **Une étiquette peut pointer vers un scénario supprimé** entre-temps — `resoudreTag()` ne
  lève jamais d'exception dans ce cas, renvoie `null`, et `purgerTagsMorts()` nettoie
  silencieusement à chaque chargement. Ce n'est pas une perte de données : c'est une entrée de
  liste qui n'a plus de sens.
- **La navigation reste volontairement non filtrée** : le bandeau ligne/référence/OP montre
  toutes les lignes existantes, quel que soit le projet ouvert. Le cloisonnement porte sur la
  lecture (tableau de bord, cartes de projet), pas sur la vue d'ensemble de l'atelier — Matis
  n'a jamais demandé à ne plus voir Step 3 exister, il a demandé à ne pas mélanger les essais
  dans sa synthèse.

### Format de fichier : 7 (rétro-compatible en lecture)
`payloadSuivi()`, l'export manuel et la sauvegarde automatique dans le dossier local écrivent
`{ format:7, lignes, projets, activeProjetId, ... }` — **`lignes` reste à la racine, exactement
comme le format 5.** C'est la différence majeure avec le format 6 de la 4.0.0 : une version
antérieure à la v4 (3.19.x et avant) ouvre un fichier format 7 sans problème et affiche toutes
les lignes et mesures ; seul `projets` lui est invisible, puisqu'elle ne le lit pas. Vérifié en
session : un export produit par cette version, rechargé dans le code de la 3.19.2, restitue
les lignes, les 3 scénarios et l'intégralité des prélèvements.

`migrerArbre()` remplace `lireProjets()`/`lignesDepuisArbre()` des versions précédentes et unifie
la lecture des trois formats en un seul point d'entrée (chargement, historique, point de
reprise, import) :
- **format 5 ou 7** (`lignes` à la racine) → lu directement, `projets` reconstruit uniquement
  s'il a la forme d'étiquettes (`tags`) ;
- **format 6** (4.0.0, projets propriétaires) → les lignes de chaque ancien projet sont
  aplaties dans l'arbre commun, **et un projet-étiquettes est reconstruit avec la même
  métadonnée** (nom, problématique, pilote, statut, échéance) pointant vers les scénarios
  désormais dans l'arbre partagé. Une personne qui a ouvert la 4.0.0 avant son retrait ne perd
  ni ses mesures ni son regroupement — contrairement au garde-fou de la 3.19.2, qui préservait
  les mesures mais abandonnait le regroupement.

### Interface
- **Cartes de projet** (`renderProjets`, `projetCarteHTML`) au-dessus du bandeau
  ligne/référence/OP, qui reste entièrement visible et navigable — le projet est un filtre de
  lecture, pas un niveau de navigation physique de plus. Cliquer une carte l'active comme
  filtre (fil d'Ariane, tableau de bord) ; un second clic la désactive.
  Chaque carte affiche : nombre de scénarios étiquetés, lignes touchées, essais, scénarios en
  série, gain annuel acquis (calculé via `dansContexteOp` + `bilanAnnuel`, sans toucher aux
  globales de navigation), pilote, statut, échéance en J−n **sans notion de retard** — un essai
  qui glisse dans un atelier est subi, pas fautif.
- **Aucun bandeau si aucun projet n'existe** : un simple lien « + Créer un projet ». Les
  projets restent facultatifs, l'outil se comporte à l'identique sans eux.
- **Étiquettes cliquables sur chaque carte de scénario** (`.tag-pill`) : ajoute ou retire le
  scénario d'un projet en un clic, sans ouvrir de panneau. Répond littéralement à la demande de
  Matis (« sélectionner le projet qu'on veut pour renseigner les données ») par un mécanisme
  différent : **créer un scénario pendant qu'un projet est ouvert l'y étiquette
  automatiquement** ; dupliquer un scénario fait hériter la copie des mêmes projets que
  l'original, pour qu'un test de variante ne sorte pas silencieusement de sa campagne.
- **Panneau d'édition de projet** : nom, problématique, pilote, statut, échéance. La
  suppression d'un projet ne touche à **aucune donnée physique** — seules les étiquettes
  disparaissent, les scénarios et essais restent dans l'outil. Contraste volontaire avec la
  4.0.0, où supprimer un projet supprimait ses lignes.
- **Tableau de bord filtrable par projet** (`<select>`, un projet = potentiellement plusieurs
  lignes désormais), réglé sur *tous les projets* par défaut.

### Fusion
`fusionnerLignes()` retrouve sa forme d'avant la 4.0.0 (fusion par identifiant, sans paramètre
de préfixe de projet). `fusionnerProjetsTags()` la complète : un projet inconnu arrive en
entier, un projet connu reçoit les étiquettes qui lui manquent, **sans jamais toucher à son
nom, son pilote, son statut ou son échéance locaux** — même règle que pour les outils et les
conditions de coupe. Beaucoup plus simple que la fusion au niveau projet de la 4.0.0 : fusionner
des listes d'identifiants ne demande aucun arbitrage essai-par-essai.

### Tests
97/97 (24 ajoutés) : défauts de `normalizeProjet` ; résolution d'étiquette valide et morte sans
exception ; purge d'étiquettes mortes ; bascule d'appartenance ; migration depuis un format 6
synthétique avec vérification que la métadonnée et le regroupement survivent et qu'aucun
prélèvement n'est perdu ; lecture des formats 5 et 7 ; fusion de projets-étiquettes (projet
inconnu ajouté, étiquette manquante fusionnée, nom et pilote locaux jamais écrasés).

Vérifié en session, au-delà des tests automatisés : deux projets réels créés, un même scénario
étiqueté dans les deux simultanément (le cas que la 4.0.0 ne pouvait pas exprimer) ; navigation
ligne/référence/OP restée complètement visible avec un projet actif ; tableau de bord filtré
sur un seul projet puis remis à zéro ; export de cette version rechargé avec succès dans le
code de la 3.19.2 (lignes, scénarios et prélèvements intacts, projets invisibles comme prévu) ;
le fichier réel de production le plus récent (format 5, 3 scénarios, 32 prélèvements) chargé
sans perte et sans création de projet fantôme.

## [3.19.2] — 2026-09-08

Retour arrière : la 4.0.0 est retirée de la production le temps de trancher si une ligne doit
appartenir à un seul projet ou pouvoir être suivie dans plusieurs. Décision assumée de décider
avant que des campagnes entières soient rangées d'une façon qu'il faudrait défaire ensuite.

> **Superseded.** Cette version a été la production le temps de trancher la question ci-dessus.
> Elle est remplacée par la 4.1.0 (voir plus bas), qui répond à la question : le projet devient
> une étiquette posée sur des scénarios, pas un propriétaire de la ligne physique. Conservée
> sur la branche `rollback/3.19.2` comme filet de secours.

### Pourquoi un retour arrière brut aurait été dangereux
Vérifié, pas supposé : la 3.19.1 face à un `localStorage` en format 6 ne trouve pas
`parsed.lignes`, conclut qu'elle démarre à neuf et **affiche le jeu d'exemple**. Les vraies
mesures restent présentes dans le navigateur mais invisibles, et la première saisie les écrase.
C'est exactement l'incident du 27/08/2026 documenté plus bas dans ce fichier — une migration
produisant un arbre vide qui masque silencieusement les vraies données.

### Garde-fou ajouté
`lignesDepuisArbre()` lit indifféremment `lignes` (format 5) et `projets` (format 6, dont les
lignes sont aplaties dans l'arbre unique de cette version). Appliqué au chargement, aux **deux**
chemins de restauration (historique et point de reprise — la 4.0 y écrivait aussi des `projets`)
et à l'import de fichier. Aucune donnée n'est perdue ; seul le regroupement par projet
disparaît, et il revient si la 4.0 est redéployée.

Vérifié : deux projets en format 6 → deux lignes, 31/31 prélèvements, préservés après
sauvegarde ; format 5 inchangé ; import d'un `.json` format 6 accepté ; 73/73 tests.

### Note de version affichée aux utilisateurs
Explicite sur le fait que les projets sont *mis en attente* et que les données saisies
entre-temps sont reprises — quelqu'un qui a vu les projets ce matin doit comprendre pourquoi
ils ont disparu, sinon il conclura à une perte.

## [4.0.0] — 2026-09-08

Nouveau niveau racine : les **projets**. Demande de Matis — un nouveau technicien process
(Julien) mène désormais des essais sur Step 3 qui n'ont rien à voir avec EMAG 1, et les deux
campagnes se retrouvaient dans le même arbre, la même synthèse et le même tableau de bord.

Hiérarchie : `Projet → Ligne → Référence → OP → Scénario → Essai → Prélèvement`.

### Choix d'architecture
- **`lignes` reste la variable « lignes du projet actif »**, exactement comme `data` est déjà
  « scénarios de l'OP active ». Les ~90 points du code qui manipulent `lignes` n'ont pas été
  touchés. Contrepartie identique à celle de `data`/`config` : quand `lignes` est réassigné
  (filter, defaultLignes…), il faut le recopier dans le projet — rôle de `syncActiveProjet()`,
  appelé par `saveData()` à côté de `syncActiveOp()`.
- **Une ligne appartient à un seul projet** (arbre, pas graphe). Mettre EMAG 1 dans deux
  projets suppose de la dupliquer, et les scénarios divergeront ensuite. C'est le choix
  difficile à défaire ; il correspond à la demande telle qu'elle a été formulée, et un modèle
  en graphe coûtait trois fois le prix pour un besoin qui n'existe pas encore.
- `appliquerArbre()` factorise la remise en place d'un arbre complet (chargement, historique,
  point de reprise, import) — la logique était dupliquée quatre fois.

### Format de fichier 5 → 6
- `lireProjets()` accepte indifféremment les deux formats ; un arbre format 5 est migré à la
  volée dans un projet unique nommé d'après sa première ligne (« Optimisation EMAG 1 »), avec
  la problématique « Coût et qualité » pré-remplie.
- **Point de reprise automatique posé avant la migration** (`backupSnapshot`), en plus de
  l'historique glissant existant.
- Les points de reprise et l'historique antérieurs à la v4 n'ont que des `lignes` : ils restent
  restaurables via le même `lireProjets()`.
- **Sens unique** : un fichier exporté en format 6 ne s'ouvrira pas dans une version antérieure
  à la 4.0. Signalé dans les notes de version, à répercuter auprès de toute personne qui
  garderait une copie locale ancienne.

### Champs du projet
`nom`, `problematique`, `responsable` (le pilote de CE projet), `statut`
(encours/pause/termine/abandonne), `dateCible` facultative, `creePar`/`creeLe`.
Pas de gestion de rôles ni de permissions : l'outil n'a pas d'authentification et n'en aura pas
— `creePar` sert la traçabilité, la convention d'équipe fait le reste, et le mode consultation
verrouillé (v3.16) couvre déjà la protection contre les modifications involontaires.

### Interface
- Sélecteur en **cartes** (`renderProjets`), pas une quatrième barre grise : quatre barres
  empilées auraient transformé le haut de l'écran en pile de bandeaux, et le projet est un
  changement de contexte complet, pas une sélection de plus au même niveau que la ligne ou l'OP.
- Chaque carte porte de quoi piloter un portefeuille : lignes, OP, scénarios, essais, scénarios
  passés en série, gain annuel acquis, pilote, statut, échéance.
- Échéance affichée en J−n, **sans badge « en retard »** : dans un atelier, un essai glisse pour
  des raisons subies (dispo machine, dispo bruts, priorité client) et un voyant rouge
  n'apprendrait rien à personne.
- Panneau d'édition du projet, avec suppression protégée (impossible s'il ne reste qu'un projet,
  confirmation détaillant ce qui disparaît, point de reprise posé avant).
- Le projet ouvre le fil d'Ariane du bandeau dès qu'il y a plus d'un projet.

### Fusion
`fusionnerProjets()` ajoute le niveau projet : un projet inconnu arrive en entier, un projet
connu voit ses lignes fusionnées. Le paramétrage local du projet (nom, pilote, statut,
échéance) n'est jamais écrasé par le fichier reçu — même règle qu'aux niveaux inférieurs.
Ce niveau devient nécessaire maintenant que plusieurs personnes saisissent en parallèle : sans
lui, fusionner deux fichiers ferait disparaître le projet de l'autre.

### Tableau de bord
Bascule « projet ouvert / tous les projets », **tous par défaut** — c'est la vue que Matis avait
avant, et celle qu'il perdrait sans elle.

### Tests
83/83 (10 ajoutés) : migration 5→6 (projet unique, nom repris, aucun prélèvement perdu, migration
signalée), relecture format 6 sans migration, statut par défaut, et fusion au niveau projet
(projet inconnu ajouté, ligne reçue rattachée au projet connu, nom et pilote locaux préservés).

### Validation sur données réelles
La migration a été éprouvée sur le dernier export de production avant bascule
(`rev16`, 07/09/2026, format 5, produit par la 3.19.1 — 1 ligne, 1 référence, 1 OP,
3 scénarios, 32 prélèvements, 7 suggestions) :

| contrôle | résultat |
|---|---|
| prélèvements avant / après migration | 32 / 32 |
| scénarios, baseline, statuts | conservés à l'identique |
| backlog | 7 / 7 |
| onglet actif (ligne › référence › OP › scénario) | restitué |
| projet créé | « Optimisation EMAG 1 », problématique pré-remplie |

Aucune perte, aucune exception. Le test a été mené sur une copie servie en local ; le fichier
de production n'est pas versionné (voir README, § Confidentialité).

### Points ouverts — pour la revue externe
Décisions assumées de cette version, listées ici parce qu'elles sont les plus discutables et
les plus coûteuses à défaire :

1. **Arbre et non graphe.** Une ligne appartient à un seul projet. Suivre EMAG 1 dans deux
   projets distincts suppose de la dupliquer, et les scénarios divergeront ensuite. Choix fait
   pour coller à la demande telle que formulée ; un modèle en graphe (ligne partagée, scénarios
   référencés) coûtait environ trois fois le prix. **Question ouverte** : est-ce que le besoin
   « même machine, deux problématiques suivies séparément » va apparaître, et à quelle échéance ?
2. **`lignes` reste une variable globale pointant sur le projet actif**, sur le modèle de
   `data`/`config` pour l'OP active. Cela a évité de toucher ~90 points d'appel, au prix d'un
   invariant à tenir : toute réassignation de `lignes` doit être suivie d'un `syncActiveProjet()`.
   Aujourd'hui garanti par `saveData()`, plus un filet dans `syncActiveProjet()` qui recrée un
   projet si l'arbre se retrouve sans racine. **Question ouverte** : cet invariant tient-il face
   aux chemins d'erreur (import interrompu, quota atteint en cours de bascule de projet) ?
3. **Format 6 à sens unique.** Les fichiers antérieurs s'ouvrent, l'inverse est faux. Aucun
   garde-fou côté anciennes versions : elles afficheront « Aucune donnée reconnue ». **Question
   ouverte** : faut-il un message explicite côté nouvelle version quand elle détecte qu'un
   fichier a été produit par une version plus récente qu'elle ?
4. **Défaut d'import inchangé.** « Remplacer tout » reste le bouton primaire, décision prise en
   3.16.1 quand une seule personne saisissait. Avec l'arrivée d'un second technicien process,
   c'est devenu le bouton qui écrase le travail de l'autre. Non modifié dans cette version pour
   ne pas changer un défaut sans arbitrage explicite. **Question ouverte** : inverser ?
5. **Échéance sans notion de retard.** `dateCible` est affichée en J−n, sans badge ni statut
   automatique « en retard ». Motif : dans un atelier, un essai glisse pour des raisons subies
   (disponibilité machine, disponibilité bruts, priorité client) et un voyant rouge n'apporte
   pas d'information exploitable — voire nuit, sur un écran visible par le client.

### Anomalie découverte hors périmètre de cette version
Vérifié sur la 4.0.0 mais préexistant : dans le module Marposs, coller une seconde extraction
**écrase la première** (`es.marposs.releves = rows`). Un essai mené sur deux jours ne peut pas
être saisi sans perdre la moitié des relevés, et rien ne le signale. Remonté par l'utilisateur
sous la forme d'une demande d'évolution (« Essais en plusieurs parties ») ; c'est en réalité une
perte de données silencieuse. À traiter en priorité dans une version ultérieure.

## Non versionné — 2026-09-05

Mentions de paternité. **`TOOL_VERSION` volontairement inchangé** : le bandeau « Nouveautés »
s'ouvre dès que la version stockée diffère, et cette modification ne concerne ni les
utilisateurs de l'outil ni le client. Elle n'a donc pas d'entrée dans `NOUVEAUTES`.

- En-tête de commentaire en tête du fichier source : conception et développement, mention de
  droits, et précision que le logo SPK identifie le contexte d'utilisation sans valoir cession
  des droits sur le code. Précise aussi que la mention porte sur le logiciel, pas sur les
  données métier saisies dedans.
- Pied de page écran : « Conception et développement : Benjamin Rouquette — © 2026, tous droits
  réservés ».
- Pied de page imprimé (documents qui partent chez le client) : formulation volontairement plus
  sobre, « outil conçu et développé par Benjamin Rouquette », sans réserve de droits — une
  mention de copyright sur un livrable client appelle des questions qui n'ont pas à se poser
  dans ce contexte.

## [3.19.1] — 2026-09-05

Trouvé en rejouant le jeu de données de la revue externe sur la version courante.

### Corrigé
- Vue d'ensemble : un logement dont une valeur est **saisie mais inexploitable** (0 arête,
  charnière à 0, prix négatif) affichait « Coût — » sans explication, alors que la cause était
  lisible juste au-dessus dans la même tuile. `apercuLogementHTML()` distingue désormais deux
  situations qui n'appellent pas le même geste : « Manque : … » (case pas encore remplie, en
  ambre) et « Coût non calculable : … » (valeur présente qui bloque le calcul, en rouge).

### Tests
73/73 (3 ajoutés) : 0 arête signalé comme bloquant et non comme manquant, cases vides
listées comme manquantes.

### Relance du jeu de stress externe sur la 3.19.1
Aucune régression, aucune exception. Rappel des comportements confirmés : cycle de la baseline
ramené à 100 (par définition), repli sur l'indice quand le cycle détaillé est incomplet
(1 logement sur 2 renseigné), `plaquettes: null` sans division par zéro sur 0 arête, rebut 50 %
à 7 €/pièce, seuil de bascule déclaré impossible sur un scénario perdant, charnière réelle
arrêtée à 50 pièces quand la tolérance est franchie au milieu, mesure de l'ancien format EMAG 1
correctement relue. Le volume négatif — dont le test n'avait jamais tourné dans le script
d'origine, un mauvais chemin d'accès l'ayant fait échouer silencieusement — est bien neutralisé
et affiche le bandeau d'alerte ajouté en 3.17. Les trois niveaux de protection du quota se
comportent comme prévu sous échec d'écriture provoqué. 70 puis 73 tests internes au vert.

## [3.19.0] — 2026-09-05

Sécurisation du stockage. Le risque le plus sérieux de l'outil n'était pas un calcul faux :
c'était `saveData()` qui échouait sur quota dépassé en ne mettant à jour qu'une **pastille de
22 px avec une info-bulle**. Quelqu'un qui saisit des relevés devant une machine ne survole
jamais une pastille — il pouvait travailler une heure sur des données écrites nulle part et
tout perdre en fermant l'onglet.

### Ajouté — gestion du quota en trois niveaux
1. **Récupération automatique.** Sur échec d'écriture, `libererEspaceHistorique()` purge
   l'historique glissant (5 instantanés complets, soit plusieurs fois le poids du suivi) et
   réessaie. Silencieux et volontairement : un point de reprise vaut moins que les mesures en
   cours de saisie.
2. **Alerte franche** si le mur est réel : une modale unique (`quotaPanneSignalee` évite une
   fenêtre par frappe) listant les actions dans l'ordre — exporter d'abord, déplacer les pièces
   jointes ensuite — et un **bandeau rouge permanent** en haut de page tant que dure la panne,
   avec le bouton « Exporter le suivi maintenant » dedans. Le bandeau disparaît dès qu'une
   sauvegarde repasse.
3. **Prévention** dès 3,5 Mo (`QUOTA_ALERTE`) : avertissement unique accompagné de
   `detailPoidsTexte()`, qui nomme les pièces jointes les plus lourdes.

`inventairePoids()` recense les pièces jointes **intégrées au fichier** (fiche outil de l'OP,
plans d'outil, images de suggestions) en ignorant celles du dossier local, qui ne coûtent rien
au quota — les confondre enverrait l'utilisateur alléger le mauvais fichier.

### Modifié — fiche outil de l'OP alignée sur les plans
`op.ficheOutil` acceptait jusqu'à **6 Mo en base64**, assez à elle seule pour saturer les ~5 Mo
de `localStorage` et bloquer l'enregistrement des mesures. Elle passe par
`attacherPieceJointe()`, la règle unique désormais partagée avec les plans d'outil :
dossier local s'il est connecté, sinon base64 sous 500 ko, sinon refus expliqué. Les fiches
jointes avant cette version n'ont pas de champ `stockage` : elles sont traitées comme intégrées
au fichier, restent lisibles et ne sont pas migrées d'office.

`ouvrirPieceJointe()` factorise l'ouverture quel que soit le mode de stockage.

### Non modifié — vérifié
Les images de suggestions étaient déjà redimensionnées côté client (1000 px de large, JPEG
qualité 0,82, soit ~100 à 200 ko) : elles ne posent pas le même problème, rien à changer.

### Tests
70/70 (2 ajoutés) : `inventairePoids()` ne compte que les pièces intégrées au fichier et
ignore celles du dossier local, et trie du plus lourd au plus léger. Les trois niveaux ont été
éprouvés en session en interceptant `Storage.prototype.setItem` : récupération silencieuse
après purge de l'historique, modale + bandeau si le mur persiste, pas de seconde modale sur les
sauvegardes suivantes, retour à la normale une fois la place libérée.

## [3.18.0] — 2026-09-05

### Ajouté — vue d'ensemble de la composition
Le « premier coup d'œil » tenait dans `.config-resume` : une ligne en 11 px mono, `--ink-faint`,
qui concaténait toutes les plaquettes bout à bout. Cette ligne essayait d'être deux choses à la
fois — l'étiquette d'un volet repliable **et** la vue d'ensemble du scénario. Elle était
dimensionnée comme une note de bas de page et lue comme un tableau de bord.

`compositionApercuHTML()` lui donne son propre bloc, **hors du volet repliable** donc visible
que la composition soit ouverte ou fermée : une tuile par logement (référence, charnière avec la
durée de vie réellement observée, prix/arêtes, €/pièce en bleu), chiffres à 19 px, en-tête avec
le compte d'outils et le coût outillage total à 22 px. Les données manquantes sont listées sous
la tuile concernée (« Manque : référence, prix ») au lieu d'être découvertes plus tard dans un
calcul qui ne tombe pas. L'ancienne ligne de résumé devient ce qu'elle aurait dû rester : une
étiquette (« outils, plaquettes, conditions de coupe — 3 fiches »).

### Ajouté — fiches outil repliables
`.outil-carte` passe de `<section>` à `<details>`, **fermé par défaut**, avec un `<summary>`
lisible : n° d'outil, correcteur, type, logements, badge plan, coût de l'outil. L'état ouvert
est mémorisé dans `outilsOuverts` (même mécanique que `essaisOuverts`) et survit aux re-rendus.
Avec l'aperçu au-dessus, on ne déplie que ce qu'on veut modifier.

### Ajouté — plan par outil (PDF ou image)
Nouveau champ `outil.plan`, distinct de `op.ficheOutil` (qui couvre toute l'opération et reste
inchangé). Deux modes de stockage, choisis automatiquement :
- **dossier local connecté** → le fichier est écrit via `writePhotoBlob()` sous le nom
  `plan_<scénario>_<outil>_<horodatage>.<ext>`, seul le nom est stocké dans le JSON. Mode
  recommandé et sans limite gênante.
- **sans dossier** → base64 dans le fichier de suivi, mais **uniquement sous 500 ko**. Au-delà,
  l'outil refuse et explique : `localStorage` plafonne autour de 5 Mo pour l'intégralité du
  suivi, deux plans de 1,5 Mo suffiraient à le saturer et à bloquer l'enregistrement des
  mesures. Le message indique le chemin pour connecter le dossier.

Retirer un plan stocké en dossier ne supprime que le lien, pas le fichier — c'est dit dans la
confirmation.

### Tests
68/68 (3 ajoutés) : `normalizeOutil` pose `plan: null` par défaut et conserve un plan existant
à l'identique, y compris à travers `normalizeScenario` — un plan perdu au rechargement aurait
été une disparition silencieuse.

## [3.17.0] — 2026-09-05

### Modifié — composition du scénario : fiches au lieu d'un tableau
Le bloc de saisie des outils était un tableau de 15 colonnes rendu en 11 px, avec
`table-layout:fixed` et des largeurs en pourcentage. La colonne « N° outil » recevait 6 % de
920 px — environ 55 px — pour y empiler trois champs (numéro, correcteur, type d'outil), et la
référence plaquette 20 à 30 % pour une chaîne du genre `CNGX 120716 T02020 LKT640 (κr 85°)`.
Avec `overflow:hidden` sur les cellules et `text-overflow:ellipsis` sur les entrées, tout était
tronqué : on ne pouvait pas relire ce qu'on venait de saisir.

Le problème de fond n'est pas la largeur, c'est la nature de l'objet : 15 colonnes pour 2 à 4
lignes, ce n'est pas un tableau, c'est un formulaire déguisé. Il est donc rendu comme un
formulaire.

- **Une fiche par outil** (`outilCarteHTML`), **un bloc par logement** (`logementBlocHTML`),
  chaque champ avec son libellé au-dessus et une largeur dimensionnée sur son contenu :
  `--oc-court` 110 px (correcteur), `--oc-moyen` 170 px (logement, code article),
  `--oc-large` 300 px minimum extensible (référence plaquette, type d'outil), `--oc-num` 96 px
  (valeurs numériques). Mesuré : la référence plaquette dispose de 505 px à 1440 px de large,
  contre ~200 px tronqués auparavant.
- **Champs groupés par nature** : Plaquette (prix, arêtes, charnière + durée de vie réelle),
  Conditions de coupe (Vc, f, κr, et rε/ap si Fr·Fa est actif, temps coupe/déplacement si le
  cycle détaillé l'est), Coût (€/arête, €/pièce, calculés, sur fond bleu et calés à droite).
- **Taille de saisie 11 → 14 px**, libellés 10 → 11 px.
- **Plus de `text-transform:uppercase` sur les libellés de champ** : Vc, f, κr, rε, ap sont des
  notations sensibles à la casse, elles s'affichaient « VC », « KR », « RE ». Les intitulés de
  groupe (mots ordinaires) restent en capitales.
- **Le tableau compact est conservé pour l'impression et le rapport client** — rien n'y est
  saisissable et la compacité y a du sens. La branche interactive de `logementRowHTML` a été
  supprimée plutôt que laissée en double entretien ; `outilRowsHTML` perd son paramètre
  `interactive`.
- Vérifié sans troncature de 820 à 1440 px de large (contrôle `scrollWidth > clientWidth` sur
  tous les champs, avec des valeurs longues réalistes).

### Ajouté — volume annuel invalide signalé
Un volume annuel négatif ou nul faisait renvoyer `null` à `volumeAnnuel()`, donc disparaître
silencieusement le bandeau de production, les gains en €/an, les heures machine et la
consommation annuelle de plaquettes. Le champ porte bien `min="0"`, mais rien n'empêche la
valeur d'arriver par un import — c'est exactement ce que le jeu de données de la revue externe
contenait. `volumeInvalideHTML()` affiche désormais un bandeau rouge nommant la référence, la
valeur fautive et le chemin pour la corriger, et précise que les chiffres ne valent pas zéro :
ils ne sont pas calculés. Rien n'est affiché tant que le champ est simplement vide.

### Tests
65/65 au vert. Contrôles complémentaires en session : saisie toujours enregistrée après
refonte (les gestionnaires sont liés aux classes et aux `data-*`, conservées), voie impression
produisant bien le tableau et aucune fiche, bandeau volume affiché pour −5000 et 0, absent
pour un champ vide et pour 200 000.

## [3.16.1] — 2026-09-05

Réglage du dosage de la fonction précédente : la fusion est prête, elle ne doit pas pour
autant s'imposer alors qu'une seule personne tient les saisies aujourd'hui.

### Modifié
- **« Remplacer tout » redevient le choix par défaut** de la fenêtre d'import (bouton primaire,
  placé en premier). C'est le geste que l'équipe connaît et le comportement correct tant qu'une
  seule personne saisit. « Fusionner » passe en action secondaire, disponible sans être
  proposée d'office.
- La note de version 3.16.0 (jamais diffusée, l'outil n'ayant pas été déployé) est corrigée en
  conséquence : elle présentait la fusion comme le choix recommandé.

### Ajouté
- **Explication au premier import** : un bloc dans la fenêtre d'import détaille ce que fait
  chaque option, le cas d'usage de chacune, et ce qui se passe quand l'outil ne peut pas
  trancher. Case **« Ne plus afficher cette explication »** (clé `spk_fusion_explication_masquee`,
  locale au poste comme celle des nouveautés) ; une fois cochée, le bloc se replie derrière un
  lien « Comment choisir ? » qui le redéploie — l'explication n'est jamais perdue, seulement
  rangée. Le choix lui-même n'est jamais masqué.

## [3.16.0] — 2026-09-05

Cinq chantiers issus d'une revue des marges d'amélioration réelles. La performance n'en fait
pas partie : l'historique et la sauvegarde dossier sont déjà throttlés à 5 min, la synthèse et
le backlog ne se recalculent que s'ils sont affichés, la saisie écrit la valeur sans
reconstruire l'écran. Le vrai point faible était le modèle d'échange de fichiers.

### Ajouté — import fusionnant (le chantier structurant)
`importData()` remplaçait tout l'arbre. À trois sur le même suivi, ça impose de travailler en
série : deux personnes saisissant en parallèle sur deux OP différents, le fichier importé en
dernier écrasait le travail de l'autre. Le compteur de révision prévenait, il n'empêchait rien.

- Nouveau champ `modifieLe` (ISO) par essai, posé à chaque écriture de champ d'essai ou de
  prélèvement, à la création, et à l'ajout/suppression de prélèvements, photos ou relevés
  Marposs (`toucherEssai()`).
- `fusionnerLignes()` — règle annoncée à l'utilisateur avant validation :
  - **structure** (lignes, références, OP, scénarios, outils, logements, conditions de coupe,
    options) : ce qui existe localement est conservé, ce qui n'existe que dans le fichier reçu
    est ajouté. Une fusion n'écrase jamais un réglage local.
  - **essais** : niveau d'arbitrage. Un essai présent des deux côtés est remplacé **en bloc**
    par la version au `modifieLe` le plus récent. Jamais champ par champ — deux moitiés
    d'essais recollées produiraient une mesure qui n'a jamais existé.
  - **conflit** (dates identiques, ou absentes d'un côté) : la version locale est conservée et
    listée nommément. Les fichiers antérieurs à cette version n'ont pas d'horodatage : leurs
    essais divergents remontent donc en conflit tant que chacun n'a pas ré-exporté une fois.
    C'est volontaire — mieux vaut signaler que deviner.
- Panneau de choix `#importPanel` (Fusionner / Remplacer tout), chaque option accompagnée de
  sa conséquence écrite, puis rapport de fusion : ajoutés, mis à jour, conservés, conflits.
- Une fusion incrémente la révision (`max + 1`) et repasse le fichier en « non exporté » : le
  résultat n'existe encore sur aucun autre poste.

### Ajouté — prévision de sortie de tolérance
`previsionUsure()` : régression linéaire des prélèvements (n° de pièce → cote), extrapolée
jusqu'à la tolérance, affichée en pastille à côté de la progression du logement. Rouge si la
sortie est prévue avant la charnière visée. Garde-fous : ≥ 4 points et ≥ 3 n° de pièce
distincts, pente positive, R² ≥ 0,35, incertitude à ± 2 erreurs-types toujours affichée. En
dessous : « tendance stable », « tendance non lisible » ou « déjà hors tol. » — jamais un
chiffre non défendable.

### Ajouté — dispersion par équipe
Les champs `equipe` et `redigePar` ne servaient qu'à tracer. Croisés avec la conformité des
prélèvements, ils donnent un tableau équipe × scénario du taux hors tolérance dans la vue de
synthèse. Badge « écart » au-delà de 5 points au-dessus de la moyenne des autres équipes, à
partir de 10 prélèvements évalués ; en dessous, la taille d'échantillon est affichée (n=…).
Le bloc n'apparaît qu'à partir de 2 équipes renseignées.

### Ajouté — mode consultation
Bouton cadenas : `body.locked` neutralise la saisie (champs en lecture seule, boutons d'action
masqués) sans rien cacher de l'information. L'outil tourne sur un écran partagé en tactile où
tout était éditable en permanence. Le mode atelier reste saisissable — on y entre
volontairement, en plein écran. État local au poste (`localStorage`), jamais exporté,
ré-appliqué après chaque rendu.

### Modifié
- Logo ré-encodé de 1796 px à 600 px de large (affiché en 52 px, ~14 mm à 300 dpi en
  impression) : 118 ko → 37 ko en base64. Fichier total 750 → 669 ko.

### Tests
16 cas ajoutés à `runTests()` (prévision d'usure : extrapolation, seuil de points, cote
stable, déjà hors tolérance ; fusion : reçu plus récent, local plus récent, conflit sans date,
fichiers identiques, essai ajouté, structure ajoutée sans écrasement). **65/65 au vert.**

## [3.15.0] — 2026-09-04

Refonte visuelle « blocs pleins » : contraste et lisibilité. Aucun changement de structure de
données, de calcul ni de format de fichier — les `.json` existants se rechargent à l'identique.

### Constat de départ
Mesure des contrastes de l'interface existante, plutôt qu'un jugement à l'œil :

| élément | avant | après | seuil AA |
|---|---|---|---|
| libellés (`--ink-faint`, #888 → #5a6470) | **3,5:1** | **6,0:1** | 4,5:1 |
| texte secondaire (`--ink-soft`, #555 → #454e59) | 7,5:1 | 8,4:1 | 4,5:1 |
| texte principal (`--ink`, #1a1a1a → #12161b) | 17,4:1 | 18,2:1 | 4,5:1 |
| bordures (`--border`, #e5e5e5 → #ccd1d8) | **1,3:1** | 1,5:1, ombre floue supprimée | 3:1 (non-textuel) |
| bleu SPK (#1b5ea6 → #0d47a1) | 6,6:1 | 8,6:1 | 4,5:1 |
| rouge (#e2001a → #c50018) | 4,6:1 | 6,2:1 | 4,5:1 |

Sur les aplats : blanc sur bleu 8,6:1, blanc sur vert 7,1:1, gain/perte éclaircis 5,5 et 5,1:1.
La bordure reste sous 3:1 par choix — elle ne porte aucune information à elle seule, elle
délimite ; ce sont l'ombre floue et le manque d'écart de fond qui la rendaient inopérante.

Le point noir n'était pas la palette mais les libellés : l'outil est fait presque entièrement
de petits libellés mono en majuscules (9,5 à 12 px), tous sous le seuil AA. Les bordures
`#e5e5e5`, noyées dans une ombre floue large, ne séparaient rien non plus.

### Modifié
- **Palette recalibrée** — `--ink` #12161b, `--ink-soft` #454e59, `--ink-faint` #5a6470,
  `--border` #ccd1d8, bleu #0d47a1, vert #12653a, ambre #8a4300, rouge #c50018.
- **Hiérarchie par aplats** — la rangée de chiffres clés d'un scénario (`.scenario-foot`), les
  KPI du tableau de bord et le bandeau de production annuelle passent sur fond de couleur
  pleine, chiffres en blanc. La cellule de validation part en vert : c'est le seul indicateur
  d'avancement de campagne, il ne se confond plus avec les coûts.
- **Bandeau de tête** en aplat noir, logo SPK posé sur une plaque blanche (le PNG a une encre
  sombre, il disparaissait sur fond noir).
- **Ombres** — `--shadow-card` réduit à un filet de 1 px : sur fond clair, un halo large et pâle
  ne sépare rien, il brouille l'arête de la carte. La profondeur vient désormais de la bordure.
- **Typographie** — Manrope (titres, gros chiffres) et Public Sans (texte courant, UI)
  remplacent Archivo et Open Sans, embarquées en base64 comme les précédentes (+66 ko, aucun
  appel réseau, fonctionnement hors ligne préservé). Public Sans est dessinée pour les petites
  tailles à l'écran, là où Open Sans se brouillait sous 12 px. IBM Plex Mono reste sur les
  chiffres.
- **Mode sombre** refait avec la même logique au lieu d'une inversion approximative : fond
  #0f1317, surfaces #181d22, texte #f1f4f7, accents remontés en tons clairs. Nouveau token
  `--on-accent` (encre posée sur un badge plein) : blanc en clair, sombre en mode nuit — les
  badges vert/rouge/ambre y étaient auparavant en texte blanc sur fond clair.
- **PDF et rapport client** alignés sur la même palette.

### Impression
- Les aplats pleins restent à l'écran : en `@media print`, les tokens `--fill*` basculent sur
  fond blanc (chiffres en bleu, cellule de validation en blanc, filets de séparation gris).
  Un tirage papier de plusieurs scénarios aurait sinon consommé beaucoup de toner pour rien.
  Comme les couleurs posées en style inline par le JS (gain/perte annuels, avertissements de
  cycle) passent par ces mêmes tokens, elles suivent automatiquement.

## [3.14.1] — 2026-09-04

Derniers constats cosmétiques de la revue Hermes.

### Corrigé
- `migrationTolerance` était une variable globale mutable jamais réinitialisée ; rendue
  locale à `loadAll()`.
- Champs numériques d'Options : chaque frappe déclenchait une sauvegarde + un rendu
  complets — léger debounce (150 ms) ajouté sur la saisie continue, `change` (blur/Entrée)
  reste instantané.
- Aucun signal quand la permission du dossier photos est révoquée en cours de session
  (paramètres du navigateur) — détectée à la prochaine lecture de photo, le statut
  « dossier non connecté » s'affiche automatiquement.
- Badges gris (`—`, compteurs) trop peu contrastés en éclairage d'atelier variable —
  couleur de texte plus soutenue.
- Badge « Charnière seule » raccourci en « 🔓 Charnière » avec info-bulle, prenait trop de
  place dans le tableau des prélèvements.
- Lightbox d'image : ajout d'un rappel « Cliquer ou Échap pour fermer », visible 2,5 s puis
  estompé (respecte `prefers-reduced-motion`).
- Menu **•••** : Échap ne le fermait pas (seul un clic à l'extérieur le faisait).
- Messages du module « Détailler le temps de cycle par logement » : couleurs factorisées
  en classes CSS sémantiques (`.cycle-detail-ok` / `.cycle-detail-ko`) plutôt qu'en style
  inline.

### Non retenu
- Pagination de la vue de synthèse au-delà de N scénarios (3.9) — Hermes notait lui-même
  que c'est à vérifier « en charge réelle » ; pas de cas concret aujourd'hui pour
  dimensionner correctement un seuil, laissé de côté pour éviter d'ajouter de la
  complexité sans bénéfice mesuré.
- `prompt()` natif pour les saisies rapides (2.11) — Hermes concluait lui-même qu'aucun
  changement n'était nécessaire en l'état.

## [3.14.0] — 2026-09-03

Suite de la revue de code externe (Hermes) : constats de cohérence et d'UI/UX restants.

### Corrigé — confidentialité (le plus important de ce lot)
- **Les données de démarrage étaient des données réelles.** `defaultScenarios` /
  `defaultLignes` (utilisés au tout premier lancement et après « Réinitialiser ») reprenaient
  exactement les références plaquette, numéros d'outil et mesures d'un export réel — donc
  versionnées sur GitHub et déployées sur l'URL publique Surge à chaque mise à jour, en
  contradiction directe avec la politique de confidentialité du README (« les données
  d'essais réelles ne sont jamais versionnées ici »). Remplacées par un jeu de données
  entièrement fictif, préfixé « [Exemple] » pour qu'il ne puisse plus être confondu avec un
  vrai projet.

### Corrigé — cohérence
- **Marge de charnière (0,5 pièce) codée en dur** — exposée en réglage `Options` :
  « Marge avant d'afficher un écart de charnière (pièces) », toujours visible, par défaut
  0,5.
- **Facteur de charnière au seuil de bascule** — formulation clarifiée : « Multiplier vos
  charnières par ×X pour revenir à l'équilibre » au lieu d'une simple valeur.
- **Champs de traçabilité (v3.11) sans valeur par défaut** — `redigePar`, `dateFin`,
  `heureFin`, `programme`, `programmeGauche`, `programmeDroit` sur un essai, et `legende` /
  `crop` / `annotations` sur une photo, étaient `undefined` plutôt que vides sur un JSON
  antérieur à ces versions. Ajoutés à la normalisation des essais/photos.

### Corrigé — UI/UX
- **Vocabulaire « Référence » à trois sens** — le badge de scénario « ★ Référence »
  (comparaison) était visible juste à côté de l'onglet « Référence disque » (la pièce) :
  renommé « ★ Scénario réf. », avec info-bulle.
- **Formule du coût machine non explicitée** — la case « Intégrer le temps machine au coût
  pièce » affiche maintenant la formule littérale : coût machine/pièce = coût horaire (€/h) ×
  temps de cycle (s) / 3 600.
- **Placeholder « Nom(s) » trop vague sur « Rédigé par »** — précise maintenant qu'il s'agit
  du rédacteur du rapport (pas forcément l'opérateur machine), et suggère le nom d'auteur
  déjà enregistré dans l'outil.
- **Éditeur d'annotation photo, fermeture sans confirmation** — Échap ou un clic en dehors du
  panneau perdait silencieusement le rognage/les formes/la légende non enregistrés ;
  confirmation ajoutée, uniquement s'il y a réellement quelque chose de non enregistré à
  perdre.
- **Éditeur d'annotation photo, cibles tactiles trop petites** — palette de couleurs et
  boutons d'outils agrandis sur écran tactile (`pointer: coarse`), comme le reste de l'outil.
- **Statuts « Validé » et « En série » trop proches visuellement** — les deux étaient en
  vert ; « En série » passe au bleu (déjà utilisé ailleurs pour ce même statut), pour
  distinguer d'un coup d'œil « essai confirmé » et « tourne en production ».
- **Message harmonisé** entre le rappel permanent d'Options et le statut par scénario du
  module « Détailler le temps de cycle par logement », qui pouvaient légèrement diverger
  dans leur formulation.

## [3.13.0] — 2026-09-03

Suite à une revue de code externe (Hermes) du fichier dans son ensemble — cohérence,
robustesse, UI/UX. 2 constats bloquants et 7 gênants de robustesse corrigés ici ; les
constats de cohérence et d'UI/UX restants sont notés pour un prochain lot.

### Corrigé (bloquants)
- **Temps de cycle de la baseline non éditable en pratique** — `recomputeCycles()` force
  `cycle = 100` sur le scénario de référence à chaque chargement (par construction : c'est
  le point zéro de l'indice), mais le champ restait affiché comme un `<input>` éditable.
  Une valeur saisie par erreur (constaté sur un export réel : `54,4` au lieu de `100`)
  disparaissait silencieusement au rechargement suivant. Le champ est maintenant en
  lecture seule sur la baseline, avec une info-bulle expliquant pourquoi.
- **Éditeur d'annotation photo : sauvegarde silencieusement bloquée** — si le stockage
  navigateur est plein au moment d'enregistrer une annotation, l'annotation reste
  correcte en mémoire pour la session mais n'est plus persistée ; rien ne le signalait.
  Un message prévient désormais l'utilisateur et l'invite à exporter le suivi.

### Corrigé (robustesse)
- **Fuite mémoire sur les photos** — les URLs temporaires (`ObjectURL`) créées pour
  afficher une miniature, ouvrir l'éditeur d'annotation ou la lightbox n'étaient jamais
  libérées. Révoquées maintenant dès que l'image correspondante est décodée.
- **Compression d'image à l'ajout d'une photo** — passait par un data URL base64
  intermédiaire (pic mémoire ~1,3× la taille du fichier, sensible sur mobile/mauvais
  réseau) ; utilise directement un `ObjectURL`.
- **Migration d'un ancien fichier de suivi non persistée** — la conversion vers le format
  Ligne/Référence/OP n'était sauvegardée qu'à la première saisie ultérieure ; elle l'est
  désormais immédiatement, sans attendre une action de l'utilisateur.
- **Éditeur d'annotation, touche Suppr** — promise dans le message d'aide pour effacer la
  forme sélectionnée, mais jamais câblée. Fonctionne maintenant (Suppr ou Retour arrière).
- **Éditeur d'annotation, bouton « Valider le rognage »** — restait actif même sans zone
  tracée, sans retour visible. Grisé tant qu'aucune zone valide n'est en cours, avec une
  info-bulle explicative.
- **Avertissement manquant si les Vc/f de la référence sont vides** — dans ce cas,
  l'indice de cycle des autres scénarios n'est plus recalculé automatiquement lors d'un
  changement de conditions de coupe, sans que rien ne le signale. Un message ambré
  l'indique désormais sous le temps de cycle des scénarios concernés.

### Non retenu de la revue
- Le constat sur `writeBackupToFolder()` (2.4) supposait qu'un échec de sauvegarde du
  dossier local pouvait faire croire à un échec de `localStorage`. Vérifié : la fonction
  encapsule déjà sa propre gestion d'erreur silencieuse et ne peut pas remonter jusqu'au
  `catch` de `saveData()` — le scénario décrit n'est pas reproductible en l'état.

## [3.12.0] — 2026-09-03

### Ajouté
- **Éditeur d'annotation de photo** (bouton ✎ sur chaque miniature, bloc Photos d'un
  essai) : rognage, flèches droites, flèches courbes (avec poignée de courbure
  ajustable), rectangles et ellipses de sélection, texte flottant, palette de 7
  couleurs + sélecteur personnalisé. Sélection/déplacement/suppression des formes,
  annuler la dernière forme.
  - Rognage et formes sont stockés en coordonnées vectorielles (fractions de l'image
    d'origine), jamais appliqués aux pixels du fichier — non destructif, ré-éditable
    à volonté, JSON toujours léger.
  - Cliquer sur une miniature ouvre désormais un aperçu plein écran recomposé
    (rognage + annotations), au lieu de la photo brute.

## [3.11.0] — 2026-09-03

Champs manquants identifiés en comparant un rapport d'essai papier réel (Matis) au modèle
de données de l'outil : rédaction, fin d'essai, programme CNC, correcteur, type d'outil,
légende de photo.

### Ajouté
- **Champs par essai** : rédigé par, fin d'essai (date + heure — en plus de la date de
  début déjà présente), nom du programme CNC (deux champs Gauche/Droit sur EMAG 1, un
  champ unique sinon). Repris dans le rapport d'essai généré.
- **Champs par outil** : correcteur (n° de jauge/offset machine), type d'outil (description
  libre, ex. « Foret carbure monobloc à goujure droite »). Repris dans le rapport d'essai
  et le rapport de validation.
- **Légende par photo d'essai** (ex. « Usure du foret après 4212 pièces (cumul) »).

## [3.10.0] — 2026-09-02

### Ajouté
- **Module « Détailler le temps de cycle par logement »** (Options → module de calcul) :
  au lieu d'un indice base 100 unique pour tout le scénario, chaque logement (bol, piste...)
  peut recevoir un temps de coupe et un temps de déplacement mesurés machine. Corrige
  l'incohérence de l'indice global sur les scénarios mixtes (un seul logement change de
  plaquette) — voir la discussion du 2026-09-02 : un ratio unique appliqué à tout le cycle
  coupant mélange deux réalités différentes dès qu'un seul côté de l'outil change.
  - Deux colonnes ajoutées à « Composition du scénario » quand le module est actif :
    Temps coupe (s) / Temps déplacement (s), par logement.
  - Le calcul détaillé ne remplace l'indice base 100 que si **tous** les logements du
    scénario sont renseignés ; sinon retombée automatique et silencieuse sur l'indice,
    signalée par un statut explicite sous le tableau (✓ complet / ⚠ incomplet, X/Y).
  - Message permanent dans Options prévenant que ces temps sont un relevé terrain réel,
    pas une estimation, et invitant à en discuter avant d'activer le module sur une
    référence.
- **Fiche outil (PDF ou image) par OP**, dans Options : illustre les n° d'outils et
  trajectoires par logement, pour aider à la saisie des temps ci-dessus. Ouverture en
  plein écran (image) ou nouvel onglet (PDF), retrait possible. Stockée avec l'OP,
  voyage donc avec l'export/import JSON.

## [3.9.5] — 2026-09-02

### Corrigé
- **Régression critique introduite en 3.9.1** : la lightbox d'agrandissement d'image
  (`.img-lightbox`) déclarait `display:flex` dans sa règle CSS de base, ce qui court-circuite
  l'attribut HTML `hidden` — une règle d'auteur avec `display` prime toujours sur le style
  agent-utilisateur par défaut `[hidden]{display:none}`, quel que soit l'ordre dans la feuille
  de style. Résultat : le voile plein écran (fond sombre à 85 % d'opacité) restait affiché en
  permanence dès le chargement de la page, rendant l'outil quasi illisible. Ajout de la règle
  `.img-lightbox[hidden]{display:none;}`, sur le modèle déjà suivi ailleurs dans le fichier
  (`.toolbar-more[hidden]`, `.atelier[hidden]`).

## [3.9.4] — 2026-09-02

### Ajouté
- **Rappel permanent dans Options**, sous « Intégrer le temps machine au coût pièce » :
  explique que le temps de cycle ne pèse dans le gain annuel que si les quatre conditions
  sont réunies — « Afficher le temps de cycle en secondes » ET « Intégrer le temps machine
  au coût pièce » cochés, coût horaire de la ligne renseigné, temps de cycle réel de la
  référence renseigné. Complète l'avertissement conditionnel ajouté en 3.9.3 (celui-ci
  n'apparaît qu'une fois le cycle déjà modifié).

## [3.9.3] — 2026-09-02

### Changé
- **Étiquette du champ « Temps de cycle »** — précise désormais « indice base 100 » pour
  ne plus le confondre avec la ligne de temps réel en secondes affichée en dessous
  (module « Afficher le temps de cycle en secondes »).

### Ajouté
- **Avertissement sous « Gain annuel »** quand le temps de cycle d'un scénario diffère de
  la référence sans que le module « Intégrer le temps machine au coût pièce » soit activé :
  le gain affiché ignore alors volontairement cet écart. Sans ce message, modifier le cycle
  sans effet sur le gain pouvait passer pour un bug de calcul.

## [3.9.2] — 2026-09-02

### Ajouté
- **Agrandissement plein écran des captures jointes à une suggestion** (menu `•••` →
  **Suggestions**) — un clic sur la miniature l'affiche en grand sur fond sombre (clic ou
  Échap pour refermer). Les captures d'écran collées par Matis/Arthur étaient jusque-là
  cantonnées à 220×160 px et illisibles.
- **Rappel dans la fenêtre « Nouveautés »** : quand une évolution correspond à une
  suggestion notée par ailleurs, un message invite à repasser son statut sur **Traité**
  dans le backlog — sans ça, les suggestions déjà traitées restaient marquées « Nouveau ».

## [3.9.1] — 2026-09-02

### Corrigé
- **Tuile « Production annuelle » chevauchant le tableau de composition** — quand le volume
  annuel était renseigné pour une référence, la tuile flottante s'imposait à côté du tableau
  « Composition du scénario » au lieu de passer au-dessus, ce qui écrasait ses colonnes
  (référence plaquette notamment) et rendait le contenu illisible. Le tableau se place
  désormais toujours sous la tuile, quelle que soit la largeur d'écran.

## [3.9.0] — 2026-09-02

Trois critères de validation de la durée de vie, au lieu d'un seul.

### Ajouté
- **Usure visuelle de la plaquette** — statut par prélèvement (OK / usure limite / à changer),
  saisi dans le tableau de l'essai comme en mode atelier. « À changer » rend le prélèvement
  non conforme même si la cote mesurée est dans la tolérance : un outil visiblement usé n'est
  pas rattrapé par une mesure encore bonne.
- **2e critère de tolérance, optionnel par scénario** (bloc « Essais ») — typiquement un état
  de surface (Ra/Rz/Rt) en plus de la tolérance dimensionnelle déjà suivie (battement,
  parallélisme, diamètre...). Les deux doivent être respectés pour qu'un prélèvement soit
  conforme. Une case vide sur le 2e critère ne fait jamais échouer un prélèvement par ailleurs
  bon — pas de reclassement rétroactif des essais existants.
- Le motif « hors tolérance » affiché sur les essais est désormais précis (cote hors tolérance,
  2e critère hors tolérance, ou usure) au lieu d'un seul libellé générique.

### Changé
- Table de prélèvements, mode atelier, rapports de validation et d'essai (HTML autonomes),
  export CSV : tous reprennent les deux nouveaux critères.

## [3.8.0] — 2026-09-02

L'outil annonce lui-même ses évolutions, et le menu d'aide rattrape les fonctionnalités
ajoutées depuis la v3.4.

### Ajouté
- **Fenêtre « Nouveautés »**, ouverte automatiquement quand la version affichée diffère de
  la dernière vue sur ce poste. Objectif : ne plus avoir à envoyer un e-mail à chaque mise
  à jour. Fermer la fenêtre vaut « lu » — elle ne revient qu'à la version suivante.
  Reste consultable à tout moment via le menu `•••` → **Nouveautés**.
  Une case « ne plus afficher » est proposée en secours ; la cocher revient à ne plus être
  prévenu des évolutions suivantes, d'où le choix de ne pas en faire le fonctionnement
  normal. Aucune version enregistrée = la fenêtre s'affiche, ce qui garantit que le premier
  déploiement de la fonction atteint bien tout le monde.
- Le contenu est maintenu dans la constante `NOUVEAUTES`, en tête du bloc correspondant :
  **3 à 5 points par version, lisibles par quelqu'un qui n'a pas suivi le développement**.
  Le CHANGELOG reste trop technique pour cet usage, les deux ne se remplacent pas.

### Changé
- **Menu « Comment ça marche » complété.** Cinq sections nouvelles : coût complet et ses
  modules d'Options (dont la part réellement coupante du cycle), seuil de bascule, charnière
  visée face à la charnière atteinte, statuts de scénario, tableau de bord. La section
  « Méthode de calcul » précise désormais que le coût plaquette seul est le comportement par
  défaut, pas la vérité complète.
- « Bon à savoir » mentionne les essais repliés en tuiles, le scénario ouvert placé en tête
  de liste avec son numéro stable, et le rôle du graphique de tendance — montrer la
  répétabilité entre essais, pas détailler un essai isolé.

## [3.7.0] — 2026-09-02

Retour à l'habillage d'origine et réorganisation de l'écran de travail autour du scénario
ouvert. Les évolutions fonctionnelles des versions 3.1 à 3.6 sont toutes conservées.

### Retiré
- **La refonte visuelle v3.0/v4.0 et son toggle de comparaison.** Le rail sombre, l'en-tête
  en carte et le verdict retravaillé sont supprimés : retour au visuel v2.5. Avec eux
  partent le bouton de bascule, son script d'amorçage et les deux blocs CSS conditionnés —
  environ 16 Ko de code mort en moins.

### Changé
- **Tuiles de scénario réorganisées.** Le scénario ouvert passe en tête de liste, sur toute
  la largeur, légèrement teinté en bleu, avec ses chiffres étalés sur une rangée. Les autres
  restent en dessous, en format condensé (nom, statut, coût/pièce, gain annuel).
  La tuile ouverte est sortie de la grille : quand elle la traversait, celle-ci créait autant
  de colonnes qu'elle pouvait en tenir et écrasait les autres tuiles à 218 px de large.
- **Numéro et couleur de statut sur chaque tuile.** Le numéro est celui de la création : il
  ne bouge pas quand l'ordre d'affichage change, pour qu'on puisse dire « regarde le 3 ». Un
  filet vertical donne le statut sans avoir à lire — gris à l'étude, ambre en essai, vert
  validé, bleu en série, rouge abandonné.
- **La composition du scénario remonte** juste après les chiffres clés, et s'affiche
  **dépliée par défaut** : c'est la fiche d'identité du scénario (outils, logements,
  plaquettes, pièces détachées, conditions de coupe). Elle reste repliable une fois la
  campagne lancée, et ce choix survit aux re-rendus.
  Nouvel ordre : tuiles → verdict → chiffres clés → composition → graphique → essais → rebut.
- **Production annuelle en évidence**, en gros et en bleu, en haut à droite de la composition
  dès que le module Volume annuel est actif. C'est le multiplicateur de tous les autres
  chiffres, il ne devait pas se chercher.

### Corrigé
- **Séparateur de milliers invisible.** Le français sépare les milliers par U+202F (espace
  fine insécable), et Archivo ne dessine pas ce caractère : « 200 000 » s'affichait quasi
  collé, l'espace tombant à 1,6 px au lieu de 9,6. Tous les nombres à quatre chiffres et plus
  étaient concernés. Les espaces fines sont désormais ramenées à l'espace insécable ordinaire
  U+00A0, présente dans toutes les polices — largeur correcte, et les nombres ne se coupent
  toujours pas en fin de ligne.

## [3.6.0] — 2026-09-02

Fiabilisation : plus aucun appel réseau, et le moteur économique est désormais couvert par
des tests. Rien ne change à l'usage.

### Corrigé
- **Le rapport d'essai exporté n'appelle plus Google Fonts.** Son pied de page affirme
  « Document 100 % local, aucune donnée transmise » alors qu'il chargeait trois polices
  depuis Google à chaque ouverture — contradiction gênante pour un document envoyé à
  Stellantis, et requête susceptible d'être bloquée par le proxy du site. Les piles de
  polices du rapport retombent sur Arial / Consolas, présentes partout.

### Ajouté
- **49 tests du moteur économique**, embarqués dans le fichier et inertes par défaut : ils ne
  s'exécutent qu'en ouvrant l'outil avec `#tests` à la fin de l'adresse, ou en tapant
  `runTests()` dans la console. Ils travaillent sur des données fabriquées et restaurent
  l'état réel ensuite — aucune sauvegarde n'est déclenchée, les données de travail ne sont
  jamais touchées.
  Couverture : `posCost`, `pieceCost`, `scenarioCost`, `recomputeCycles`, `cycleSecondes`
  (formule part coupante, cas 0 / 50 / 100 %), `coutMachinePiece`, `coutRebutPiece`,
  `coutPiecesDetachees`, `coutsDetail` (propagation des `null`, drapeau `multiPoste`),
  `charniereReelle` (borne inférieure, sortie de tolérance, échec au premier prélèvement),
  `ecartsCharniere`, `seuilBascule`, `bilanAnnuel`, `fmtEuroCourt`.
  Vérifié en remettant l'ancienne formule de cycle fausse : 5 tests tombent, dont ceux de
  `coutMachinePiece`, `coutsDetail` et `bilanAnnuel` — la cascade est bien détectée.

### Changé
- **Polices embarquées en base64, plus aucune dépendance réseau.** L'outil s'ouvre à
  l'identique hors ligne, depuis une clé USB, ou derrière un proxy d'usine. Fin du blocage
  de rendu pendant le délai d'attente réseau quand le poste atelier n'a pas Internet.
  Coût : le fichier passe de 479 à 600 Ko.
  Deux optimisations pour en arriver là plutôt qu'aux 510 Ko d'un embarquement naïf :
  Archivo et Open Sans sont des **polices variables** — Google sert le même fichier pour
  chaque graisse, les embarquer une par graisse aurait dupliqué 200 Ko à l'identique ; une
  seule face couvre désormais toute la plage (`font-weight: 600 800` et `300 700`). Et
  chaque police est **sous-ensemblée** au latin complet plus les symboles de l'interface
  (≤ ★ ✓ → κ €). Un caractère hors de ce jeu retombe sur la pile système déclarée derrière,
  sans casser la mise en page.

## [3.5.0] — 2026-09-01

Coût complet et pilotage du portefeuille d'optimisations. L'outil ne comparait que le prix
des plaquettes : un scénario deux fois plus lent mais moins cher en outil ressortait gagnant
alors qu'il pouvait être largement perdant. Tous les modules ci-dessous sont **désactivés par
défaut** — rien ne change tant qu'on ne les active pas dans Options, et une fois activés ils
prennent leur place de façon permanente.

### Ajouté — chaîne économique
- **Temps machine dans le coût pièce.** Le coût horaire de la ligne (saisi via l'icône ⚙ de
  l'onglet de ligne, existant depuis la v3.2) est enfin utilisé : il convertit l'écart de temps
  de cycle en euros. Sur les données OP10 actuelles, la céramique intégrale passe de « −93,4 % »
  à **+25 % de coût réel**, soit une perte de l'ordre de 37 k€/an à 200 000 disques.
- **Part réellement coupante du cycle (%).** L'indice de cycle vaut `100 × (Vc·f réf)/(Vc·f)` :
  c'est un indice de *temps coupant*, pas de cycle complet. L'appliquer au cycle entier
  surestimait la pénalité, puisque chargement, approche et retrait ne bougent pas avec Vc/f.
  On ne fait donc varier que la part déclarée comme coupante.
- **Pièces détachées par porte-outil** — cales, vis, corps d'outil, brides, chacune amortie sur
  sa propre charnière de remplacement et ajoutée au coût pièce.
- **Volume annuel de production**, réglé par référence disque : convertit chaque écart en €/an
  et en heures machine/an, et affiche la **consommation annuelle de plaquettes** par logement.
- **Décomposition du coût** — barre empilée + légende sous le chiffre de tête (plaquettes /
  pièces détachées / temps machine / rebut). Un chiffre agrégé seul n'est pas défendable.
- **Seuil de bascule** — « X s de cycle maximum pour rester gagnant », et le facteur à appliquer
  aux charnières pour revenir à l'équilibre. Quand le temps machine dépasse à lui seul la
  référence entière, l'outil le dit explicitement : aucune durée de vie ne compensera.

### Ajouté — suivi et pilotage
- **Charnière réellement atteinte**, calculée à partir des essais : dernier prélèvement conforme
  avant sortie de tolérance, moyenné sur les essais. Affichée sous la charnière visée dans le
  tableau plaquettes. Tant qu'aucun essai n'est sorti de tolérance, la valeur est présentée
  comme une borne inférieure (`≥ 150`) — les essais s'arrêtent à la cible, on ne sait rien
  au-delà. Dès qu'un essai lâche avant la cible, un encart signale l'écart et recalcule le coût
  réel correspondant.
- **Statut de vie d'un scénario** : à l'étude / en essai / validé / en série / abandonné, avec
  motif obligatoire à l'abandon et date de décision automatique. « Validé » et « en série » ne
  se confondent plus, et une impasse documentée évite qu'on la reparcoure deux ans plus tard.
- **Tableau de bord multi-lignes** (menu `•••`) : toutes les lignes, références et OP du fichier
  dans une seule vue — avancement des essais, coût pièce, écart, gain annuel, et en tête le
  cumul du gain acquis (scénarios en série) vs à déployer (validés pas encore passés en série).

### Changé
- Dès que plusieurs postes de coût sont actifs, **le coût total devient le chiffre de tête**
  partout : verdict, pied de scénario, liste des scénarios dans le rail, vue de synthèse et
  rapport de validation. Le coût plaquette reste affiché, en sous-ligne. Objectif : que le rail
  n'annonce jamais −46 % pendant que la fiche ouverte affiche +33 %.
- Le **rapport de validation** envoyé au client reprend le coût complet, la répartition
  plaquettes / temps machine et le gain annuel — c'est le document qui engage, il ne pouvait pas
  continuer à ne chiffrer que l'outil.
- La vue de synthèse ajoute une ligne « statut du scénario » et une ligne « gain annuel ».
- Le pied de scénario passe en grille auto-adaptative : il accueille le nombre de cellules
  correspondant aux modules actifs, sans mise en page figée à 4 ou 5 colonnes.

## [3.4.0] — 2026-08-30

Rapport par essai + message de divergence explicite.

### Ajouté
- **Rapport de l'essai** : bouton dans chaque essai qui génère un rapport HTML autonome
  dédié à cet essai — interlocuteurs (site, contacts Stellantis et CeramTec), but de
  l'essai, plaquettes utilisées (référence, Vc, f, charnière), tableau des prélèvements
  avec statut, observations. Mise en page reprenant les tokens du design system SPK
  (Archivo/IBM Plex Mono, bleu/rouge de la charte, logo).
- **But de l'essai** : nouveau champ libre par essai (bandeau bleu, à côté des
  observations), repris dans le rapport ci-dessus.
- La référence plaquette est désormais figée dans l'instantané de l'essai à sa création
  (elle ne l'était pas avant, seuls Vc/f/charnière l'étaient) — nécessaire pour que le
  rapport reste exact même si la référence change plus tard dans le scénario. Pour les
  essais déjà existants qui n'ont pas cette valeur figée, le rapport retombe sur la
  référence actuelle du scénario (meilleur effort).

### Changé
- **Message « le scénario a été modifié depuis »** : disait qu'un écart existait sans dire
  lequel. Indique maintenant précisément quoi (ex. « T513.1 · Piste — Vc 900→950, f
  0.5→0.45 ») avant de proposer d'aligner l'essai sur le scénario.

## [3.3.0] — 2026-08-29

Toggle de comparaison graphique v2.5 / v3.2 — **temporaire**, le temps de recueillir l'avis
de Matis (Stellantis) sur la refonte avant de basculer `main` dessus.

### Ajouté
- Un bouton flottant en bas à droite ("🎨 Voir l'ancien design" / "🎨 Voir le nouveau design")
  bascule entre l'habillage v2.5.0 (en-tête classique, pas de rail) et la refonte v3.0+
  (rail sombre, en-tête en carte, verdict retravaillé). Le choix est mémorisé
  (`localStorage`) et survit à la fermeture du fichier.
- Techniquement additif comme la refonte elle-même : les deux blocs CSS `@media screen`
  de la refonte sont conditionnés à `html:not([data-layout="classic"])` (CSS nesting), et
  le script qui construit le rail s'arrête tôt si le mode classique est actif. Rien n'a été
  dupliqué ni retiré de l'ancien CSS.
- Les évolutions fonctionnelles apportées depuis (essais en tuiles, icônes aide/légende,
  menu ligne) restent actives dans les deux habillages — seul l'agencement visuel change.

### À faire une fois le choix arbitré
- Retirer le bouton, le script de bootstrap en tête de fichier, et les deux conditions
  `html:not([data-layout="classic"])` (en gardant leur contenu tel quel si v3.2 est retenu ;
  en supprimant les deux blocs `@media screen` de la refonte si l'ancien design est retenu).

## [3.2.0] — 2026-08-29

Essais en tuiles + informations de ligne — deux ajouts après retour terrain sur la v3.1 :
l'écran d'un scénario affichait tous ses essais entièrement dépliés (tableau, graphique
Marposs, photos) en permanence, ce qui devenait confus dès qu'une campagne comptait
plusieurs essais.

### Ajouté
- **Informations de ligne** : une icône ⚙ sur l'onglet de ligne actif (à côté de ✎ renommer)
  ouvre un panneau avec coût horaire (€/h), observations libres, et dernière maintenance
  (date + type d'intervention en texte libre). Champs préparatoires — pas encore intégrés
  au calcul du coût/pièce.
- Les deux paragraphes "Sauvegarde" et "Méthode de calcul", auparavant fixes en bas de page,
  sont maintenant deux sections du panneau "Comment ça marche" (même icône ⓘ).

### Changé
- **Essais en tuiles** : chaque essai est replié par défaut (titre, date, badge de statut
  coloré selon l'état — conforme / non conforme / en cours). Cliquer la tuile déplie les
  détails (conditions de coupe, tableau de prélèvements, photos, suivi Marposs). Un essai
  nouvellement créé s'ouvre automatiquement pour la saisie ; les autres restent repliés.
  L'état ouvert/fermé de chaque tuile survit à la ressaisie d'une mesure (qui redessine
  l'écran) grâce à un suivi séparé, scénario + essai.
- Le résumé (fermé) du tiroir "Conditions de coupe et plaquettes" affiche maintenant la
  référence plaquette et le coût/pièce de chaque logement, plutôt que le numéro d'outil
  seul — l'info reste lisible sans avoir à déplier le tableau à 13 colonnes.

### Corrigé
- La coloration rouge du filet gauche d'un essai non conforme ne s'appliquait jamais
  (la classe posée par le code, `risk`, ne correspondait pas à la classe attendue par le
  CSS, `bad`) — corrigé au passage.

## [3.1.0] — 2026-08-29

Décluttering de l'écran de travail — les informations d'attribution (site, interlocuteurs,
mention confidentielle) et les aides secondaires n'ont pas leur place en permanence sous les
yeux ; elles sont soit déplacées en pied de document, soit rangées derrière une icône.

### Changé
- **En-tête écran** : le bloc site / interlocuteurs Stellantis / interlocuteur CeramTec est
  retiré de l'écran. Cette information reste dans les documents imprimés et exportés, mais
  déplacée en pied de page plutôt qu'en haut.
- **Bandeau « Confidentiel »** : retiré de l'écran (redondant avec le fait que l'outil ne
  quitte jamais le poste local). Conservé uniquement en pied des documents imprimés et du
  rapport de validation exporté, à côté de la mention site/interlocuteurs.
- **« Comment ça marche »** : réduit à une icône (rond bleu au survol/ouverture) au lieu d'une
  carte pleine largeur avec son intitulé en toutes lettres. Le contenu ne change pas, seul son
  déclencheur devient discret.
- **Légende champ éditable / calculé automatiquement** : les deux lignes de texte permanentes
  sont remplacées par un bouton compact (les deux pastilles de couleur) avec l'explication en
  info-bulle, posé à côté de l'icône d'aide.
- **Statut de sauvegarde** (barre d'outils) : le texte descriptif devient une pastille colorée
  (gris neutre / ambre en cours / vert exporté / rouge bloqué), le détail complet passant en
  info-bulle. Les indicateurs de la même famille dans le menu `•••` (dossier photos, révision)
  ne sont pas concernés, ils sont déjà dans un menu secondaire.

### Non affecté
- Aucune donnée, logique de calcul ou de validation modifiée.
- Le rapport de validation exporté et l'impression conservent l'intégralité de l'information
  (site, interlocuteurs, confidentialité), simplement repositionnée en pied de document.

## [3.0.0] — 2026-08-29

Refonte visuelle + coquille applicative — le plan de travail gagne un rail de navigation
permanent, et l'en-tête, le verdict et les chiffres clés sont retravaillés dans la charte SPK.
Changement structurel (nouvelle disposition en grille), d'où le passage en version majeure.

### Changé
- **Nouvelle coquille applicative** : rail sombre collé à gauche (`#0f2740`), plan de travail à
  droite. Le rail contient le logo, la sélection Ligne › Référence › OP, la liste des scénarios
  (coût/pièce et delta visibles sans naviguer) et les actions (export/import, PDF, réinitialisation).
  Sous 1080px, le rail repasse en flux normal au-dessus du contenu.
- Sélecteurs Ligne / Référence / OP regroupés dans un conteneur commun (`.ctx-rail`), collé en
  haut de son conteneur ; se replie automatiquement si les trois listes sont vides.
- En-tête transformé en carte à filet bleu SPK, eyebrow précédé d'un tiret rouge, titre en
  Archivo 800.
- Bandeau verdict : fond teinté plat (au lieu du dégradé) + barre d'accent de 5px à gauche selon
  l'état (référence / conforme / hors tolérance / en attente).
- Chiffres clés de pied de scénario agrandis (jusqu'à 44px), deltas présentés en pastilles.
- Cartes de scénario, encarts (notes, aide, Marposs, photos, backlog) et boutons harmonisés :
  rayons plus généreux, ombres portées cohérentes, repères de section en tiret rouge.
- Menu `•••` de la barre d'outils : s'ouvre désormais vers le haut depuis le pied du rail.

### Non affecté
- Aucune donnée, clé de stockage ou logique métier modifiée : sélection, saisie, mode atelier,
  suivi Marposs, export/import JSON/CSV/PDF, historique local — tout est inchangé.
- Rendu impression / export PDF inchangé (le rail est masqué à l'impression).
- Thème sombre (`prefers-color-scheme: dark` / `[data-theme="dark"]`) préservé tel quel.

### À vérifier
- Rendu non testé visuellement avant intégration (contrainte de l'outil de conception utilisé).
  À valider dans un navigateur réel (Edge/Chrome desktop, puis tablette) avant diffusion large.

## [2.5.0] — 2026-08-28

Refonte typographique — c'est la police condensée qui donnait à l'outil son côté
« documentation industrielle ».

### Changé
- **Titres : Open Sans Condensed → Archivo** (600/700/800). Le condensé compressait tout et
  évoquait la fiche technique ; Archivo a de la présence aux grandes tailles.
- **Chiffres : Courier New → IBM Plex Mono**, dessiné pour les contextes techniques. Dans un
  outil de mesure, les chiffres sont le sujet principal.
- **Corps de texte : Open Sans conservé** — c'est la police de la charte SPK, et les documents
  générés partent chez Stellantis sous cette identité.
- Tracking resserré aux grandes tailles, et chiffres tabulaires forcés partout où des nombres
  s'alignent en colonne (ils ne dansent plus d'une ligne à l'autre).

### Corrigé
- Nom de scénario tronqué dans l'en-tête (« Mixte T50013 — bol CBN + piste céramiq… ») :
  Archivo étant plus large, le champ occupe désormais sa propre ligne pleine largeur.

### Documentation
- Mode d'emploi PDF refait en 6 pages : adresse en ligne en couverture, nouvelle section
  « Lire un scénario » (ordre verdict → chiffres → graphique → essais → configuration),
  mode atelier, suivi Marposs, dossier local photos, suggestions avec image, installation
  en application sur Edge et sur iPad.

## [2.4.0] — 2026-08-28

Refonte de la hiérarchie de lecture et arrivée du mode atelier. L'outil ne se contente plus
d'afficher des données : il énonce sa conclusion.

### Ajouté
- **Bandeau verdict** en tête de chaque scénario : le gain formulé en une phrase
  (« −46,7 % de coût outil par pièce · 2× la durée de vie d'arête · validation en cours »),
  avec chips coût/pièce, durée de vie et taux hors tolérance. Le scénario de référence
  s'affiche comme « Référence de production — base 100 ».
- **Mode atelier** : saisie plein écran conçue pour être utilisée debout devant la machine,
  avec des gants. Champs de mesure à 78px, n° de pièce deviné à partir du pas réel de
  prélèvement, sélecteurs de logement et de point de mesure en gros boutons, barre de
  progression vers la charnière, retour immédiat conforme / hors tolérance après chaque
  validation, Entrée pour enregistrer. Écrit dans les mêmes données que la saisie tableau.
- Support tactile réel : `@media (pointer: coarse)` avec cibles à 44px minimum sur écrans
  tactiles uniquement, et breakpoint < 720px (KPI sur 2 colonnes, barre d'outils pleine
  largeur).

### Changé
- Nouvel ordre de lecture d'un scénario : verdict → chiffres clés → graphique → essais →
  configuration → rebut. La preuve visuelle passe avant les détails de configuration.
- Le tableau outils/logements se replie une fois la campagne lancée (déplié automatiquement
  tant qu'une référence plaquette manque, et toujours déplié à l'impression).
- Couleurs Marposs tokenisées (`--teal`, `--teal-strong`) et éclaircies en thème sombre.

### Corrigé
- **`<meta viewport>` absent** : sur iPhone/iPad la page se rendait en 980px puis rétrécissait,
  rendant l'outil inutilisable au doigt. C'était le blocage principal pour l'usage tablette.
- **`<meta charset>` absent** : risque d'accents cassés à l'ouverture du fichier en local.
- **Graphique vide à la première ouverture** sur les scénarios EMAG 1 : les données de départ
  ne passaient pas par `normalizeScenario`, donc la mesure restait dans `batt` sans être
  reportée sur Droite/Gauche.
- Contraste insuffisant du teal Marposs en thème sombre (3,03:1 → conforme).
- Flèches d'incrément désactivées en mode atelier (le piège qui rendait la saisie pénible).

## [2.3.0] — 2026-08-28

Simplification structurelle, pas seulement visuelle — "loin d'être radical" puis "sois plus
radical pour simplifier" ont motivé ce passage : réduire ce qui est visible en permanence,
pas seulement le restyler.

### Changé
- Barre d'outils réduite de 13 à 3 boutons visibles (Exporter, Importer, + Ajouter un
  scénario) ; tout le reste (CSV, Synthèse, Suggestions, Options, PDF, Rapport, Historique,
  Dossier local, Réinitialiser, Restaurer, nom de l'exportateur) déplacé dans un menu "•••".
- Tableau des outils/logements : colonnes Rayon de bec et ap (affinage Fr·Fa) masquées par
  défaut tant que ce module optionnel n'est pas activé — 13 colonnes au lieu de 15. κr reste
  toujours visible (utilisé aussi par le widget K, indépendant de Fr·Fa).

## [2.2.0] — 2026-08-28

Deuxième passage design, plus marqué que le 2.1.0 — "loin d'être radical" était le retour, donc
changements à effet visuel net cette fois plutôt qu'incrémental.

### Changé
- Onglets Ligne de production / Référence disque / OP transformés en **contrôle segmenté**
  (piste grise, segment actif élevé en pilule blanche avec ombre douce) — remplace les
  rectangles bordés bleu-sur-bleu.
- Chiffres clés (coût/pièce, coût/arête, temps de cycle) fortement agrandis (25px → 38px, plus
  gras) avec libellés réduits au-dessus, pour un vrai contraste "chiffre héros / légende".
- Cartes comparatives de scénarios (`tab-card`) : coins plus généreux, ombre portée douce,
  anneau bleu net sur la carte active (au lieu d'un bord rouge/bleu sans signification claire).

## [2.1.0] — 2026-08-28

Passage design "élégance dans la simplicité" — pas de nouvelle fonctionnalité, ni de rupture,
mais un changement visuel assez large pour mériter son propre numéro.

### Changé
- Nouveaux tokens de rayon (`--radius-lg/--radius/--radius-sm`) : coins plus doux sur les
  cartes, panneaux et contrôles (avant : 3px partout, très anguleux).
- Boutons repensés : fond neutre discret par défaut, couleur pleine réservée aux actions
  principales (Exporter, Ajouter un scénario), forme plus arrondie, léger effet de survol.
- Icônes de la barre d'outils et des sections Marposs/Photos remplacées par des icônes traits
  fins cohérentes (au lieu d'emojis).
- Titres de section : bleu appuyé remplacé par un gris neutre — la couleur ne reste que pour ce
  qui est interactif.

## [2.0.0] — 2026-08-28

Version de consolidation : marque le passage d'un usage exploratoire à un outil structuré,
partagé (dépôt GitHub, hébergement en ligne) et documenté au fil de l'eau via ce changelog.
Regroupe tout ce qui a été construit depuis la version initiale.

### Ajouté
- Hiérarchie complète **Ligne de production → Référence disque → OP → Scénario → Essai → Prélèvement**
  (avant : une seule référence, un seul niveau de scénarios).
- Modèle **Outil → Logement** par scénario (N outils, N logements chacun), avec code couleur par
  outil et charnière indépendante par logement (avant : bol/piste fixes).
- Mode EMAG 1 (mesure Droite/Gauche) avec bascule automatique selon la ligne de production.
- Widget **K** (indice thermique) par logement, et ratio **Fr/Fa** optionnel (activable par OP).
- Scénario **de référence (★)** interchangeable, base 100 pour les comparaisons de coût/cycle.
- Critère de validation dissociable par logement : charnière seule, ou charnière + tolérance.
- Suivi **Marposs** par essai : collage direct de l'extraction de production, fenêtre de l'essai
  surlignée sur le graphique, moyenne essai vs moyenne journée.
- **Photos par essai**, stockées comme de vrais fichiers dans un dossier local choisi par
  l'utilisateur (jamais dans le fichier d'échange JSON) — nécessite Edge/Chrome et la version en
  ligne de l'outil.
- Backup automatique dans ce même dossier local, en plus de la sauvegarde navigateur.
- **Historique local** (5 derniers points de reprise automatiques) et garde-fou au chargement si
  le fichier semble vide alors qu'une sauvegarde plus ancienne contient des données.
- Vue de synthèse comparative (tableau + graphique superposé multi-scénarios).
- Onglet **Suggestions** (remontées Matis/Arthur, avec pièce jointe image) et rapport de
  validation HTML autonome, incluant désormais le détail des prélèvements.
- Export CSV limité au scénario affiché, avec sélection des essais à inclure.
- Couleur fixe et cohérente par point de mesure (Inter/Exter...) sur le graphique de tendance.
- Export/import qui rouvrent sur l'onglet exact utilisé au moment de l'export.
- Installation possible comme application (Edge/Chrome), icône SPK dans l'onglet et à
  l'installation.

### Corrigé
- Perte de réactivité de la saisie clavier physique (un clic ne validait qu'un incrément).
- Précision des mesures (3 décimales, clavier numérique adapté).
- Double confirmation par saisie de texte avant "Réinitialiser" (au lieu d'un simple clic).

### Changé
- Hébergement de référence : `https://suivi-optimisation-septfons.surge.sh`, en plus du fichier
  local — mise à jour transparente pour Matis/Arthur (rechargement de page, plus d'envoi de
  fichier).
- Code versionné sur GitHub (dépôt privé), données et exports jamais versionnés (`.gitignore`).

## [1.0] — avant 2026-08-27 (rétroactif)

Première version en usage réel chez Stellantis Sept Fons : suivi mono-référence, scénarios
bol/piste fixes, export/import JSON manuel, tolérance unique par campagne.
