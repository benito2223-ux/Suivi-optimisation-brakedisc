# PROTO — cinq écrans, CPP plaquettes en driver

Maquette à tester, **à côté** de l'app de production. Le proto ne remplace rien et
ne touche jamais `bilan_economique.html`.

- **en ligne** : https://suivi-optimisation-projet2.surge.sh
- **localement** : `python -m http.server 8124` puis `http://127.0.0.1:8124/index.html`

## Ce qu'on teste

Une seule question : **cinq écrans valent-ils mieux que vingt ?** Cinq écrans, dans
l'ordre où les questions se posent : où en est-on → essai → preuve → décision → emporter.

## Fichiers

| Fichier | Rôle |
|---|---|
| `CAHIER.md` | le cahier des charges, une page — le code doit le respecter |
| `coeur.js` | les fonctions PURES (CPP, gain, verdict). Aucun DOM. Testées d'abord. |
| `donnees.js` | le jeu de départ — **structurel, aucun chiffre réel** |
| `proto.html` | les cinq écrans (le rendu ne calcule rien) |
| `assembler.py` | couture les trois en un `index.html` déployable |
| `test_coeur.js` | 64 tests du noyau |
| `test_proto.js` | 70 tests des écrans et des portes |

## Les tests

```bash
python assembler.py     # obligatoire après toute modif : le déployé est index.html
node test_coeur.js      # le noyau
node test_proto.js      # les écrans
```

Les deux doivent dire `TOUT EST VERT` et sortir en code 0.

## Règles du proto

- **Données locales seulement.** Aucun cloud, aucun compte, rien qui sorte.
- **Aucun chiffre estimé.** Une mesure absente est écrite « non mesurée ».
- **Les gains ne se fusionnent jamais** : « acté » et « projeté » sont deux chiffres.
- **Une cible sans chiffrage reste visible** — elle ne disparaît pas.

## Décision attendue sous une semaine

Le proto gagne → il devient la base, on migre écran par écran.
Le proto perd → il reste un banc d'essai, l'app de production continue.

Dans les deux cas, **on ne garde pas les deux en vie plus de deux semaines.**
