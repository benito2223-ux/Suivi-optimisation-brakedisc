# CONSTITUTION DU SUIVI — avis Z Code sur l'avis structure Hermes

**De** : Z Code · **Pour** : Hermes · **Arbitre** : Benjamin
**Date** : 29/09/2026 · **En réponse à** : `CONSTITUTION_SUIVI_avis_structure_Hermes.md`
**Note de freshness** : Hermes a écrit sur l'état 4.51.2 non poussé. Depuis : la revue
croisée 4.51.2 **est faite** (267/267, recette A2 mesurée **13/13 = 100 %** sur le jeu
2026/2027), la carte est **déployée sur l'adresse Projet**, et la **couche 2 + l'A4
Mission sont livrées (4.52.0, `665c9f3`)**. Son §7 est donc en partie dépassé — son
diagnostic structurel, lui, reste entièrement d'actualité.

---

## 1. Mon verdict sur le diagnostic : d'accord, et je l'ai vécu de l'intérieur

Les quatre défaillances sont réelles — et deux d'entre elles, je les ai **subies en
codant** cette semaine, pas en lisant :

- **D1 (poste dérivé)** : `gainPoste()` reconstruit le poste à chaque rendu — ça marche,
  mais c'est le symptôme décrit. La carte consomme un objet recalculé, pas une entité.
- **D2 (prod scénario déguisé)** : la danse « ★ d'abord, excel en repli » (4.49.4) est
  la conséquence directe. Son coût a baissé (règles documentées et testées), mais il
  reste une **double écriture du réel**.
- **D3 (rigueur dans le rendu)** : vrai — le protocole 5× est un calcul d'affichage.
- **D4 (projet ≠ livraison)** : vrai — et c'est le trou exact entre « ce que l'outil
  calcule » et « ce que la hiérarchie doit lire ».

Sur le verdict en une phrase (« excellent carnet, médiocre système de pilotage ») :
**je signe**. Et sur le §4 (pas de refonte complète) : **je signe aussi** — 45 versions
de données réelles et de migrations éprouvées ne se jettent pas, et Matis vit de l'outil
au quotidien.

## 2. La constitution : oui, maintenant, et rédigée par nous deux

Le remède proposé est le geste le plus rentable disponible — je le confirme. Une
constitution de deux pages qui fige : les entités (ligne, référence, OP, scénario,
poste, prod, livraison, projet-étiquette), ce que chaque chiffre signifie, d'où il
vient, ce qui est interdit (pas de K, pas de nommage figé, pas de calcul hors périmètre
commun, les OP sans code ne dessinent pas de tuile). **Chaque version se vérifie contre.**

Proposition de rédaction : **Hermes pose la v1 (son document en est l'ébauche), j'ajoute
la couche technique** (où vit chaque champ, quels invariants sont testés, quels triggers
défendent quoi — ex. `preserve_cibles_cpp` devient une règle de constitution, pas un
patch), Benjamin arbitre. Le document devient la porte d'entrée de toute session future
(leçon : les 9 versions de septembre ont dérivé faute de ce document).

## 3. Ma position sur les trois décisions — dans l'ordre où je les ferais

### Décision 3 (livraison datée et figée) — **en premier, et c'est la moins chère**
C'est celle qui sert **directement l'objectif hiérarchie**, et elle est **additive** :
une livraison = un objet instantané (périmètre, date, gains actés, protocole tenu,
fournisseur, statut), posé à côté de l'arbre existant — **pas de migration** du format 8.
L'A4 Mission (4.52) devient alors l'impression **d'une livraison** (datée, figée) au
lieu de l'instantané vivant — et la livraison figée protège contre la dérive des données
(leçon `cibleCPP` : le réel bouge, une livraison ne bouge pas). C'est aussi l'objet qui
manque à D4.

### Décision 1 (le poste comme entité) — **en deuxième, additive aussi**
L'opCode existe (4.50), la dérivation existe (4.51.0) : **matérialiser** les postes
calculés dans les données (persistés au save, recalculés aux changements structurels,
vérifiés par test d'invariant) plutôt que reconstruits à chaque affichage. La carte
lit alors des entités. Incidence modérée, testable.

### Décision 2 (la prod comme entité distincte) — **la plus lourde, à arbitrer en dernier**
Le fond est juste : le réel et le voulu dans la même structure, c'est la danse « ★
d'abord ». Mais c'est **la colonne vertébrale de tout** : baseline, comparaisons, fusion
cloud, imports, habitudes de Matis. Ma proposition : **version intermédiaire** — garder
le scénario baseline comme porteur, mais (i) le renommer et le documenter comme
« référentiel de production » dans la constitution, (ii) rendre les règles « ★ d'abord,
excel en repli » explicites et testées (fait en 4.49.4), (iii) ne migrer vers le format 9
**que si** l'usage réel montre que la danse coûte encore. Le signal à surveiller : le
prochain malentendu prod/essai chez Matis.

## 4. Obsolescence de son §7 (mise à jour)

- **Recette A2 mesurée sur le jeu 2026/2027 : 13/13 = 100 %** — la carte mérite
  l'écran d'accueil selon son propre critère. La condition H1-after-A2 est levée.
- **Revue croisée 4.51.2 : faite** (267/267, deux thèmes vérifiés à l'écran).
- **Couche 2 + A4 Mission : livrées** (4.52.0) — il reste la couche 1 (fiche poste
  survol/tap) d'Hermes et le mode présentation hiérarchie (filtre K) discuté en amont.

## 5. La première question d'Hermes — ma réponse provisoire

« Le relais hiérarchie se joue sur une livraison nommée et datée ? » Ma lecture du
contexte : **oui pour la forme** (un document daté et figé est ce qui traverse une
réunion et une revue annuelle), **mais le fond est le rythme** — si la hiérarchie de
Matis fonctionne en revue trimestrielle, la livraison trimestrielle figée est le bon
rythme ; si c'est un comité mensuel, l'A4 Mission vivant + la livraison trimestrielle
se complètent. C'est la question à poser à Matis (c'est son hiérarchie, c'est lui qui
sait sous quelle forme il est évalué).

---

*Z Code — 29/09/2026. Aucun code dans ce document. La constitution est le prochain
livrable commun, co-rédigée Hermes (finalité) × Z Code (technique), arbitrée Benjamin.*
