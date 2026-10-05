# 2resume — cahier des charges, une page

> Ce fichier n'est pas de la documentation. C'est **l'aiguille** : le code doit le
> respecter, et s'il ne peut pas le respecter, c'est le cahier qui a tort.
> Écrit le 02/10/2026, avant la première ligne de `coeur.js`.

---

## 1. La phrase

**Le coût d'outillage d'un poste d'usinage céramique/CBN doit être lu en trente
secondes sur une tablette d'atelier, comparé à la cible du site, décidé avec la
preuve à côté — et il doit sortir une page A4 que Benjamin emmène à Detlef.**

L'outil est **complet**, pas une maquette : on y saisit, on y corrige, on y
imprime, on y exporte, on y partage. Cinq écrans ne veulent pas dire cinq
écrans vides.

## 2. Le driver : le CPP outillage

`Σ prix / (arêtes × charnière)` sur les logements — c'est le **coût outillage de
la pièce**, et c'est le seul chiffre comparable à la colonne I du classeur de
Matis. Le temps machine sort **à côté**, valorisé au taux horaire, marqué
« non comparable au classeur », et **jamais mélangé** au total qu'on compare.

Trois règles, non négociables :

1. **`coutLogement()` est le seul endroit où un CPP est calculé.** Tout le reste
   agrège. Deux modules ne racontent jamais deux histoires.
2. **Pas de comparaison hors périmètre commun.** Un écart entre deux coûts n'est
   affiché que si les **mêmes postes de coût** sont chiffrables des deux côtés ;
   sinon l'écran dit « non comparable » et **pourquoi**.
3. **Aucun chiffre estimé.** Une mesure absente s'écrit « non mesurable ». Jamais
   un `0` qui voudrait dire « rien à gagner », jamais une barre invisible qui
   voudrait dire « pas d'écart ».

## 3. Le modèle — la loi du correcteur

| entité | ce que c'est | ce qu'elle n'est jamais |
|---|---|---|
| **ligne** | une machine de production, un taux horaire | |
| **référence** | un disque, sa cible CPP, son volume annuel | |
| **OP** | une opération, identifiée par un `opCode` **dérivé** du nom | le nom libre n'est jamais une clé |
| **outil** (porte-outil) | le corps qui porte les logements, identifié par son numéro `T543` | un jeu d'outillage interchangeable |
| **logement** (correcteur) | un **emplacement** sur l'outil : D1, D2, D3 | un outil, une référence |
| **plaquette** | ce qui garnit le logement, identifiée par son **MABEC** | l'emplacement |
| **scénario** | une configuration d'outils essayée contre la prod | |
| **poste** | ligne × opCode — **dérivé**, jamais stocké | |
| **projet** | une **étiquette** transversale | un conteneur, un propriétaire |

`T543 D1` et `T543 D2` sont **un** outil à **deux** logements. Jamais deux outils.
Un MABEC n'est pas une clé unique : plusieurs MABEC sur un outil est normal.

**Le vide est une valeur.** Une case vide s'affiche comme vide, avec ce qui
manque. On n'écrit jamais `0` là où il n'y a pas de mesure.

## 4. Les cinq écrans — l'atelier d'abord

Un agent qui arrive sur une ligne ne commence pas par une décision : il commence
par **sa ligne**.

| # | écran | la question | la réponse |
|---|---|---|---|
| 1 | **Les lignes** | où en est-on | une carte par ligne : CPP outillage, cible, écart, postes non chiffrables |
| 2 | **La ligne** | qu'est-ce qui tourne | les OP's, et sous chacun **le scénario de production décomposé jusqu'au logement** |
| 3 | **Scénarios et essais** | qu'est-ce qu'on teste | les scénarios **qui ne sont pas** en production : preuves, conformité, saisie d'un essai |
| 4 | **Décision** | le gain, go / no-go | un mot par poste — ESSAYER, DÉCIDER, SÉRIE, CHIFFRER, RIEN — et sa raison |
| 5 | **À emporter** | la page qu'on emmène | l'A4 daté, imprimable en un clic |

L'écran 2 ne montre **que** la production. Un poste sans scénario de production
reste visible, marqué « sans production » : s'il disparaît, la ligne paraît
complète à tort. Les essais portés par la production sont montrés là aussi.

## 5. Ce que l'app de production ne montre pas, et qu'on montre ici

1. **Le CPP obtenu par essai**, dans la même unité que le prévu, essai par
   essai. Le prévu dit ce qu'on croit ; l'obtenu dit ce qui s'est passé.
2. **La charnière atteinte par logement**, pas en bloc : « D1 12/30 p · D2 0/30 p ».
3. **La décomposition à quatre étages** — pièce → OP → outil → logement — sur les
   deux axes, comme la phrase de Benjamin le demande littéralement.
4. **Ce qui manque**, compté et nommé : un outil sans prix, un logement sans
   charnière, un prélèvement sans battement. L'écran 1 porte ce décompte.

## 6. Les invariants, écrits AVANT le code

1. Un CPP affiché n'est jamais un chiffre seul : c'est **le CPP, sa référence, et
   l'écart** — à chaque étage de l'arbre.
2. **« CPP » seul désigne toujours le coût outillage.** Le temps machine, le
   rebut et les pièces détachées sont nommés, jamais confondus avec lui.
3. **Gain acté et gain projeté ne s'additionnent jamais.** Deux blocs étiquetés.
4. Une cible sans chiffrage reste visible : « à chiffrer », jamais « opportunité ».
5. Une absence dit ce qui manque : « — volume annuel non saisi », jamais « — » nu.
6. **Aucune valeur inventée**, dans aucun écran, aucune maquette, aucun rapport.
7. La **source** des chiffres est toujours affichée : jeu d'exemple, export
   importé, ou poste de Matis.

## 7. Les règles non négociables du projet

- **Jamais de K ni P_req en sortie visible** — ni écran, ni impression, ni
  rapport. Hex s'appelle « épaisseur de copeau ».
- Les nuances sont **SPK**. Le classeur Excel de Matis se lit **en local
  uniquement** : on n'y saisit rien, on n'y calcule rien.
- **Aucune dépendance réseau** : ni CSS, ni police, ni image distante. L'outil
  doit s'afficher complet **réseau coupé** — il tourne sur le poste de Matis,
  en atelier. Test d'acceptation : ouvrir le fichier hors ligne.
- **Les données réelles ne quittent jamais le poste.** Le cloud est un partage
  volontaire, jamais une dépendance : hors ligne, tout fonctionne.
- **Deux thèmes**, **impression A4 propre**, **tactile** (44 px de cible, gros
  chiffres, lisible avec des gants).
- L'outil est **présentable en réunion tel quel**.

## 8. L'ordre de construction

`noyau testé → tests verts → écrans`. Jamais l'inverse. Et une suite de tests ne
compte que les tests **exécutés** : `0 échec` sans « X tests passés » ne veut rien
dire.

## 9. Le hors-périmètre, dit et non caché

La **production hebdomadaire**, la **cadence** et le **délai moyen entre deux
essais** ne sont pas dans cet outil : ils sont détaillés par lot de lignes et ne
disent rien d'un poste d'outillage. L'écran 1 **écrit pourquoi** — un écran muet
laisse croire que l'absence était prévue.
