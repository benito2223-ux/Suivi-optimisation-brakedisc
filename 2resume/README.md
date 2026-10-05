# 2resume — le suivi CPP, écrit de zéro

L'outil complet de suivi du coût d'outillage des disques frein (Sept Fons) :
**un seul fichier HTML**, zéro build, zéro SDK, offline-first, deux thèmes,
impression A4, partage cloud volontaire.

- **en ligne** : https://suivi-optimisation-projet2.surge.sh (l'adresse « projet 2 »)
- **en local** : `python -m http.server 8125` puis http://127.0.0.1:8125/index.html
  (ou ouvrir `index.html` directement, réseau coupé — il doit s'afficher complet)

## La phrase

**Le coût d'outillage d'un poste doit être lu en trente secondes sur une
tablette d'atelier, comparé à la cible du site, décidé avec la preuve à côté —
et il doit sortir une page A4 que Benjamin emmène à Detlef.**

Le driver : le **CPP outillage** `Σ prix ÷ (arêtes × charnière)` — terme pour
terme la formule de la colonne I du classeur de Matis, donc comparable.
Le temps machine, le rebut et les pièces détachées sont valorisés à côté,
**jamais mélangés** à ce qui se compare.

## Les cinq écrans — l'atelier d'abord

1. **Lignes** — une carte par ligne : CPP, cible, écart, postes à chiffrer,
   et la liste de ce qui manque ;
2. **Ligne** — le scénario de production décomposé **jusqu'au logement**
   (MABEC, plaquette, prix, arêtes, charnière, coût) ;
3. **Scénarios et essais** — ce qui n'est pas en production, le CPP **prévu**
   contre le CPP **obtenu** par essai, la saisie d'un essai ;
4. **Décision** — un mot par poste (ESSAYER, DÉCIDER, SÉRIE, CHIFFRER, RIEN)
   et sa raison ;
5. **À emporter** — la page A4 datée.

## Ce que l'app de production ne montrait pas

Le **CPP obtenu par essai**, dans la même unité que le prévu. Sur l'export
réel du site : `EMAG 1 · OP40 · SL500` prévoyait **0,1735 €/pce**, l'essai a
donné **0,0478 €/pce**. `KY3500` : prévu **0,2452**, obtenu **0,0797**.
Ces deux scénarios ne sont pas en production — l'écran 3 existe pour eux.

## Fichiers

| Fichier | Rôle |
|---|---|
| `CAHIER.md` | la spécification, écrite avant la première ligne de code |
| `coeur.js` | le noyau de calcul — PUR, aucun DOM. Un CPP se calcule à un seul endroit |
| `import.js` | la projection des exports anciens (formats 1 à 8) et la relecture des siens |
| `donnees.js` | le jeu de départ, structurel, aucun chiffre réel |
| `app.html` | les cinq écrans, la saisie, l'export, le partage (le rendu ne calcule rien) |
| `polices.css` | Manrope / Roboto / IBM Plex Mono, embarquées — aucune requête réseau |
| `assembler.py` | coud le tout en `index.html` + empreinte SHA-256 des sources |
| `test_coeur.js` | 147 tests du noyau |
| `test_import.js` | 141 tests de la projection, sur les QUATRE exports réels du dépôt |
| `test_app.js` | 82 tests des écrans, de l'import bout en bout, et du contre-regard |

## Les tests

```bash
python assembler.py     # obligatoire après toute modification
node test_coeur.js      # 147
node test_import.js     # 141
node test_app.js        # 82
```

Les trois doivent dire `TOUT EST VERT` et sortir en code 0. **370 tests.**

`test_app.js` **refuse de tourner sur un assemblage périmé** : il recalcule
l'empreinte des quatre sources et la compare à celle posée dans `index.html`.
Et il contient le **contre-regard** : il casse la formule du CPP dans une copie
du noyau et vérifie que les tests la verraient — un filet dont on a prouvé
qu'il prend, pas un filet décoratif.

## Ce que les tests ont déjà attrapé

Écrit ici pour qu'on ne l'oublie pas :

1. **Le code d'opération** : en donnant priorité au champ `ordre` sur le nom,
   « OP40 Finition Pistes » sortait en OP30. L'atelier lit le nom — le nom gagne.
2. **Un battement non mesuré comptait « conforme »** quand le critère Ra était
   inactif. L'absence doit dominer, toujours.
3. **Le champ `code` du verdict était écrasé** par le code d'OP.
4. **Le contre-regard lui-même a été corrigé** : « la somme des parties égale
   le total » reste vraie avec une formule fausse. La règle protégée est la
   valeur absolue, pas l'égalité.

## Le partage

Le bouton **Partager** se connecte au cloud Supabase du projet — dans des
tables **dédiées** (`etat_2resume`), jamais dans celles de l'app de
production. Le dépôt initial passe uniquement par **Déposer ce suivi**.
Hors ligne, tout fonctionne : le cloud est un partage, pas une dépendance.

## La confidentialité

Aucune donnée réelle ne quitte le poste sans **Exporter** ou **Déposer**.
Le `.surgeignore` est une liste blanche stricte : seul `index.html` est
publié. Le classeur Excel de Matis se lit en local uniquement — cet outil
n'y calcule rien.
