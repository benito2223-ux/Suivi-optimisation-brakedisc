# CONSTITUTION DU SUIVI — avis franc, structure à trancher

**De** : Hermes · **Pour** : Z Code · **Arbitre** : Benjamin
**Date** : 29/09/2026 · **État du socle** : `dev` = 4.51.2 (`a781dfd`), non poussé, non déployé
**Objet** : pause avant la suite. Un avis critique sur la structuration de l'outil au
regard de ses objectifs initiaux, et trois décisions de structure à trancher.

> Ce document ne remet pas en cause le travail fait : les 4.50 → 4.51.2 sont solides
> (267 tests verts). Il interroge la **projection** du modèle, pas sa qualité.

---

## 1. Le verdict en une phrase

**L'outil est un excellent carnet d'essais chiffré, et un médiocre système de
pilotage d'un plan d'optimisation.**

Le carnet d'essais mérite d'être gardé tel quel : le modèle données/mesures/
prélèvements tient, la comparaison par périmètre commun (v4.45) est une vraie
trouvaille, la migration 5×→série est propre, la synchro qui fusionne sans
écraser est du travail d'adulte, et 267 tests tiennent. **La critique porte sur
un seul point : ce que Benjamin veut montrer à la hiérarchie n'a pas de forme
dans le modèle.**

## 2. Les objectifs initiaux, énoncés pour mémoire

1. **Les informations arrivent en douceur**, couche par couche — le design viendra après ;
2. **Mettre en avant les gains réalisés par Matis** — travail d'équipe Matis + Benjamin ;
3. **Servir de relais vers la hiérarchie** : montrer une démarche rigoureuse, un plan
   d'action, des gains actés, avec un fournisseur qui épaule.

## 3. Quatre défaillances structurelles

### D1 — Le modèle encode la bibliothèque, pas l'atelier
La hiérarchie réelle des données est *ligne → référence → OP → scénario*. La réalité
de Sept Fons est *machine → poste → outillage → essai*. **L'entité « poste » — celle
que la carte atelier veut montrer en tuile — n'existe pas dans le modèle.** Nous l'avons
reconstruit par dérivation (`opCode`, 4.50) puis par calcul (`gainPoste`, 4.51.0) :
c'est le symptôme. Quand l'écran principal est un poste, le poste doit être une
entité de premier niveau, pas un calcul reconstruit à chaque affichage.

### D2 — La production réelle est un scénario déguisé
La prod est le scénario `baseline: true`. Mais une prod n'est pas une hypothèse : c'est
ce qui tourne, c'est le référentiel. Mélanger le réel et le voulu dans la même structure
explique pourquoi il faut sans cesse « ★ d'abord, excel en repli » (v4.49.4) — une
déception de base, payée à chaque version.

### D3 — Le temps n'est pas une dimension de premier ordre
La rigueur — l'objectif principal — est **reconstruite par le code de rendu** : compter
les essais, comparer au seuil 5, afficher une barre. Les dates existent, mais le concept
de *run* (une série d'essais, un protocole, un verdict daté) n'est pas dans les données.
**La rigueur est donc dans le code, pas dans le modèle** : elle s'affiche tant que le
code tient, et disparaît le jour où on refactore le rendu.

### D4 — Un projet n'est pas une livraison
Un projet est un jeu d'étiquettes posé sur des scénarios. Or l'objectif hiérarchie, c'est :
« voici ce que nous avons fait en 2026/2027, livré le 12/06, 8 400 € actés ». Cet objet
n'existe pas. Le client qui a payé le service veut **une livraison figée**, pas un filtre
dynamique sur un ensemble qui bouge en permanence.

## 4. Pourquoi je ne dis pas « refonte complète »

Une refonte complète serait une erreur, et je le dis franchement :

- elle jetterait des années de données réelles et des migrations éprouvées ;
- elle casserait la confiance de Matis, qui utilise l'outil tous les jours ;
- le modèle n'est pas **faux**, il est **mal projeté** : les entités existent, c'est
  leur **niveau** qui est faux.

On répare, on ne repart pas de zéro. Mais **les trois décisions se prennent ensemble** :
faire la 3 sans la 2 aggrave le modèle.

## 5. Les trois décisions à trancher (Benjamin arbitre)

### Décision 1 — Le poste devient l'ancrage
Le poste (ligne × code d'OP) devient une **entité de premier niveau**. Les tuiles sont
la structure, pas une vue. La navigation par référence (fil d'Ariane expert) devient un
**filtre transverse**, pas le squelette.
*Incidence* : la carte (4.51.2) cesse d'être un panneau parmi d'autres et peut devenir
l'écran d'accueil — ce qui était la condition H1-after-A2.

### Décision 2 — La production devient une entité distincte
Un statut « production », pas un scénario avec une étoile. La comparaison
scénario-de-produit devient explicite, et le « ★ d'abord, excel en repli » disparaît.
*Incidence* : migration du format 8 à format 9, **une seule fois**, avec réversibilité.

### Décision 3 — Le projet devient une livraison datée et figée
Un objet *livraison* : périmètre (les postes et références), date, gains actés, protocole
tenu, fournisseur associé, statut (en cours / livrée). C'est **l'objet que la hiérarchie
lit** — et l'A4 Mission (prévue en phase 3) en est la forme imprimée.

## 6. Le risque qui menace maintenant

**L'emballement des couches.** 45 versions en un mois, dont neuf en deux jours ; 22
versions d'écart entre la prod (4.29) et `dev` (4.51.2). Chaque couche a été posée *sur*
la précédente, jamais *dans*. Les preuves sont dans mon audit :

- classes CSS mortes héritées des refontes ;
- 46 `catch` vides (dont `loadAll()`, qui avale tout exception et retombe sur [Exemple]) ;
- 67,6 Ko de polices embarquées sans usage (résorbés depuis) ;
- deux modules racontant des histoires différentes sur le même poste (divergence
  `coutEnCours`, corrigée en 4.51.1 par la revue croisée) ;
- des modèles entiers qui se chevauchent (`logementsParalleles` → `outilsParalleles` →
  cases par outil : trois modèles successifs pour une seule idée).

Le remède n'est pas un gel : c'est **une constitution**. Deux pages qui disent quelles
entités existent, ce qu'elles signifient, ce qui est interdit, et où vit chaque chiffre.
Chaque version se vérifie contre. Sinon nous livrerons la carte, puis l'A4, puis la vue
mission, et dans trois versions plus personne ne saura quel chiffre est vrai.

**Je propose de rédiger cette constitution maintenant**, avant la suite. C'est le geste
le plus rentable disponible, et c'est court.

## 7. Ce que je propose comme suite immédiate

1. **Rédaction de la constitution** (2 pages, ce document en est l'ébauche) ;
2. **Mesure de la recette A2 sur le jeu 2026/2027** — le chiffre qui dira si la carte
   mérite d'être l'écran d'accueil (non fait à ce jour : la recette n'a été mesurée que
   sur mon jeu de test) ;
3. **Revue croisée Z Code de la 4.51.2** (`a781dfd`, non poussé) — notamment la
   vérification visuelle des deux thèmes et du mode tactile, que je n'ai pas pu faire
   (le harnais navigateur a expiré deux fois) ;
4. **Ensuite seulement**, la couche 2 et l'A4 Mission — ou les trois décisions de
   structure ci-dessus, selon ce que Benjamin juge prioritaire.

## 8. Ce que je n'ai pas vérifié (limites de cet avis)

Cet avis repose sur la **lecture du code** et sur les mesures d'exécution, pas sur une
observation de l'usage réel par Matis ni sur une entretien avec la hiérarchie. Le point
le plus fragile est D4 : je suppose que le relais hiérarchie se joue sur une *livraison*
nommée et datée. Si la hiérarchie attend autre chose — un tableau de bord permanent, une
réunion trimestrielle sans document — alors la décision 3 prend une autre forme. **C'est
la question à poser à Benjamin en premier.**

---

*Hermes — 29/09/2026. Aucun code dans ce document. Socle 4.51.2 relu et testé (267/267).*
