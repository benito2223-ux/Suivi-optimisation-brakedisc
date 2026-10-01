# PROTO — cahier des charges, une page

> Ce fichier n'est pas de la documentation. C'est **l'aiguille** : le code doit le
> respecter, et s'il ne peut pas le respecter, c'est le cahier qui a tort.
> Écrit le 01/10/2026, avant la première ligne du proto.
>
> **Le proto ne remplace pas l'app.** Il répond à une seule question : *est-ce que cinq
> écrans valent mieux que vingt ?* Il vit dans `proto/`, se déploie à part, ne touche
> jamais `bilan_economique.html`.

---

## 1. La phrase

**Un poste d'usinage céramique/CBN doit être tranché en cinq minutes — quel insert, quel
gain, quelle preuve — et il doit sortir une page que Benjamin emmène à Detlef.**

Tout ce qui n'y sert pas est en trop.

## 2. Le driver : CPP plaquettes

C'est le **coût outillage de la pièce** — `Σ prix / (arêtes × charnière)` sur les
logements — qui porte la décision. Trois raisons, et elles ne sont pas des préférences :

1. C'est **le seul chiffre comparable au classeur de Matis** (colonne I, CPP théorique).
   Le temps machine, le rebut et les pièces détachées n'y sont pas (§2 quater : on ne
   compare jamais un total avec machine à un classeur CPP).
2. C'est le levier **directement actionnable** : changer d'insert change la charnière,
   donc le coût. Le temps machine, on ne le touche pas.
3. C'est ce que **Detlef peut contester utilement** — donc c'est celui qu'il faut avoir
   présent, propre et traçable.

Conséquence d'architecture : **le CPP plaquettes est le premier citizen de l'écran 1, et
le temps machine ne sort qu'en zone secondaire, marqué « non comparable au classeur ».**

## 3. Les cinq écrans, dans l'ordre où les questions se posent

| # | Écran | La question | Temps visé |
|---|---|---|---|
| 1 | Où en est-on | quelles lignes, quels postes, quelle décision en attente | 10 s |
| 2 | Essai | j'insère un essai | 90 s |
| 3 | Preuve | les répétitions, la charnière atteinte, la conformité | 30 s |
| 4 | Décision | le gain CPP, go / no-go | 15 s |
| 5 | Emporter | la page A4 | 1 clic |

Pas de sixième écran. Pas de menu « Outils », pas de réglages, pas de panneaux
secondaires. Ce qui ne sert pas les cinq questions n'existe pas.

## 4. Les invariants, écrits AVANT le code

Ce sont les règles de la constitution, traduites en **forme de code**. Pas en commentaire,
pas en convention : en impossibilité.

1. **Le CPP de prod et le CPP classeur ne se comparent que périmètre à périmètre.** Un
   écart n'est affiché que si les deux côtés sont chiffrables ; sinon la ligne porte
   « non mesurable » et la raison.
2. **Les gains ne s'additionnent qu'entre eux de même statut.** `gainActe` et
   `gainProjete` sont deux valeurs distinctes, jamais fusionnées en un « total gain ».
3. **Une cible sans chiffrage reste visible.** Une référence qui porte une cible CPP mais
   aucun coût calculable s'affiche « à chiffrer » — jamais « opportunité », jamais vide.
4. **Une absence dit ce qui manque.** Pas de « — » nu : « — volume annuel non saisi ».
5. **Le CPP outillage n'est jamais labellisé « CPP pièce ».** Le mot CPP seul désigne le
   coût outillage ; tout autre poste est nommé.
6. **Aucune valeur inventée.** Une cadence non mesurée affiche « non mesurée », jamais
   une estimation.

## 5. Le noyau, avant l'écran

`coutPoste()`, `cheminCPP()`, `statutEssai()`, `verdictPoste()` sont des **fonctions
pures**, sans DOM, testées avant que la moindre tuile existe. Le rendu lit, il ne calcule
rien.

Ordre de construction imposé : noyau testé → tests verts → écran. Jamais l'inverse.

## 6. Ce que le proto n'a pas

Par choix, pas par oubli : cloud, photos, annotations, historique, CSV, recherche,
rapport PDF, PWA, multi-utilisateurs.

Le proto tient dans **un fichier**, sans dépendance. S'il dépasse 500 Ko, c'est qu'il
redevient l'app.

> **v1.0 — une exception, prise le 01/10.** L'import des exports de l'ancienne version
> n'était pas dans la liste, à tort : sans lui, le proto démarre vide et on juge une
> maquette sur des données fictives. C'est une **projection**, pas une ressaisie — le
> fichier est lu sur le poste, et tout ce qui ne nourrit pas une décision d'outillage
> est abandonné et **compté à l'écran**. Le classeur Matis, lui, reste hors de portée :
> on n'y saisit rien, on n'y calcule rien.

## 7. Comment on tranche

Benjamin teste sur données réelles (ou sur le jeu d'exemple s'il n'a pas encore les
siennes), sur `projet2`. Réponse attendue sous une semaine :

- **le proto gagne** → il devient la base ; on migre écran par écran, sans réécrire le
  noyau (il est déjà propre et testé) ;
- **le proto perd** → il reste un banc d'essai, on continue sur l'app actuelle.

**Dans les deux cas, on ne garde pas les deux en vie plus de deux semaines.** C'est
exactement ce qui a produit 109 versions et vingt-deux panneaux.

## 8. Ce que le proto va probablement casser

Écrit d'avance, pour qu'on ne soit pas surpris :

- l'écran 2 (saisie en 90 s) est le plus difficile — la saisie actuelle est riche, et
  90 s suppose d'en abandonner des champs ;
- le vocabulaire de Matis (MABEC, numéro d'outil, CPP théorique) doit survivre tel quel,
  sinon Matis ne s'y retrouvera pas ;
- l'écran 1 risque de manquer une information que la carte atelier montre bien — c'est
  le vrai test, et c'est le but ;
- **le proto n'affiche ni le temps machine, ni le rebut, ni les pièces détachées.**
  C'est délibéré, et c'est peut-être faux : l'app de production les porte, et Detlef
  peut les attendre. Ce sont les seuls manques à examiner en premier si le proto gagne.