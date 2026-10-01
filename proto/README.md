# PROTO — cinq écrans, CPP plaquettes en driver, et les essais déjà faits

Maquette à tester, **à côté** de l'app de production. Le proto ne remplace rien et
ne touche jamais `bilan_economique.html`.

- **en ligne** : https://suivi-optimisation-projet2.surge.sh
- **localement** : `python -m http.server 8124` puis `http://127.0.0.1:8124/index.html`

## Ce qu'on teste

Une seule question : **cinq écrans valent-ils mieux que vingt ?** Cinq écrans, dans
l'ordre où les questions se posent : où en est-on → essai → preuve → décision → emporter.

## Reprendre les essais déjà faits (v1.0)

Le bouton **Données**, en haut à droite, ouvre le panneau d'import. Vous choisissez un
export `.json` de l'ancienne version du suivi — **formats 5, 6, 7 et 8, c'est-à-dire
tout ce que l'app a jamais produit**. Les cinq écrans se remplissent avec.

Le fichier est lu **sur le poste**. Il n'est ni envoyé, ni téléversé, ni conservé
ailleurs : les essais du site ne quittent jamais la machine.

**Ce qui est conservé** — le trio `prix / arêtes / charnière` qui fait le CPP
plaquettes, la charnière **mesurée** de chaque essai, la cible site de chaque
référence, les prélèvements de conformité, et le statut « en série ».

**Ce qui est abandonné** — les plans de porte-outil, les photos, les relevés Marposs,
le journal de rebut. Sur l'export réel du site : **3,2 Mo réduits à 49 Ko**, soit 1,5 %.

> Ce n'est pas une ressaisie. Aucun chiffre de décision n'est perdu, et le rapport
> d'import dit ce qui entre, ce qui manque et ce qui a été jeté.

### Le CPP réellement obtenu

L'app de production montre ce que le **scénario prévoit**. Le proto montre en plus ce
que l'**essai a donné**, essai par essai, dans la même unité — donc comparable.

Sur l'export réel du site, `EMAG 1 · OP40 · SL500` : le scénario prévoyait
**0,1735 €/pce**, l'essai a donné **0,0478 €/pce**.

## Fichiers

| Fichier | Rôle |
|---|---|
| `CAHIER.md` | le cahier des charges, une page — le code doit le respecter |
| `coeur.js` | les fonctions PURES (CPP, gain, verdict). Aucun DOM. Testées d'abord. |
| `import.js` | la projection d'un export ancien vers le modèle du proto. Pure elle aussi. |
| `donnees.js` | le jeu de départ — **structurel, aucun chiffre réel** |
| `proto.html` | les cinq écrans + le panneau d'import (le rendu ne calcule rien) |
| `assembler.py` | couture les quatre en un `index.html` déployable |
| `test_coeur.js` | 64 tests du noyau |
| `test_import.js` | 78 tests de la projection, **sur les vrais exports du site** |
| `test_proto.js` | 105 tests des écrans, des portes et de l'import de bout en bout |

## Les tests

```bash
python assembler.py       # obligatoire après toute modif : le déployé est index.html
node test_coeur.js        # le noyau
node test_import.js       # la projection
node test_proto.js        # les écrans + l'import de bout en bout
```

Les trois doivent dire `TOUT EST VERT` et sortir en code 0.

`test_import.js` tourne sur les **quatre exports réels** présents dans le dépôt
(`cloud_courant.json`, `suivi_corrige_mabec.json`, `base_depart_2026_2027.json`,
`IMPORT_MATIS.json`). Un jeu synthétique ne prouverait rien sur ce que Matis
déposera réellement.

## Deux pièges que les données réelles ont posés

Ils sont documentés ici parce qu'ils reviendront.

1. **`batt` n'est rempli que sur 1 prélèvement sur 84.** En EMAG 1, l'app relève
   *droite* et *gauche* séparément (`battD` / `battG`). Sans pont, tous les essais
   réimportés afficheraient « aucun prélèvement », silencieusement.
   Le noyau prend `batt`, sinon **le pire** des deux côtés — jamais la moyenne : un
   état des lieux ne doit pas flatter une pièce qui déborde d'un côté.
2. **Un test qui cherche une chaîne ne prouve pas qu'un nombre est juste.** Le
   contre-regard l'a montré : une faute affichant le CPP *prévu* à la place du CPP
   *obtenu* passait tous les tests, parce que le prévu était imprimé deux lignes
   plus haut. Le test relit désormais la valeur du bloc qu'il vérifie.

## Règles du proto

- **Données locales seulement.** Aucun cloud, aucun compte, rien qui sorte.
- **Aucun chiffre estimé.** Une mesure absente est écrite « non mesurable ».
- **Les gains ne se fusionnent jamais** : « acté » et « projeté » sont deux chiffres.
- **Une cible sans chiffrage reste visible** — elle ne disparaît pas.
- **La source est toujours affichée** en haut de l'écran : un outil qui ne dit pas
  d'où viennent ses chiffres laisse croire qu'ils sont les siens.

## Décision attendue sous une semaine

Le proto gagne → il devient la base, on migre écran par écran.
Le proto perd → il reste un banc d'essai, l'app de production continue.

Dans les deux cas, **on ne garde pas les deux en vie plus de deux semaines.**
