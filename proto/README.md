# PROTO — l'atelier d'abord : une tuile par ligne, puis la ligne, puis l'optimisation

Maquette à tester, **à côté** de l'app de production. Le proto ne remplace rien et
ne touche jamais `bilan_economique.html`.

- **en ligne** : https://suivi-optimisation-projet2.surge.sh
- **localement** : `python -m http.server 8124` puis `http://127.0.0.1:8124/index.html`

## Ce qu'on teste

Une seule question : **cinq écrans valent-ils mieux que vingt ?** — et depuis le
02/10, **dans quel ordre**. La réponse retenue : l'atelier d'abord.

1. **Les tuiles** — une par ligne de production (Weisser, Hessapp, EMAG, PCI).
2. **La ligne** — ses opérations, et sous chacune le **scénario de production**
   décomposé **jusqu'au logement**. Rien d'autre.
3. **Scénario et optimisation** — les scénarios **qui ne sont pas** en production,
   où ils en sont, et le formulaire d'essai.
4. Décision · 5. Emporter (inchangés).

**La production hebdomadaire n'y est plus** : elle est détaillée par lot de lignes et
ne dit rien d'un poste d'outillage. L'écran 1 **écrit pourquoi elle est absente**.

Le CPP plaquettes reste le driver : c'est le coût outillage de la pièce, et c'est le
seul chiffre comparable au classeur de Matis.

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
**0,1735 €/pce**, l'essai a donné **0,0478 €/pce**. `KY3500` : prévu **0,2452**,
obtenu **0,0797**.

> Ces deux scénarios-là **ne sont pas** en production — ils vivent à l'étage 3. Un seul
> scénario de production sur les dix lignes porte un essai (`HESSAPP · OP40`). Sans
> l'étage 3, la meilleure preuve du site serait invisible. Ce n'est pas un choix
> d'affichage : c'est ce que les données dictent.

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
| `test_tuiles.js` | 62 tests des deux premiers étages, **sur les vrais exports** |
| `test_proto.js` | 118 tests des écrans, des portes et de l'import de bout en bout |

## Les tests

```bash
python assembler.py       # obligatoire après toute modif : le déployé est index.html
node test_coeur.js        # le noyau
node test_import.js       # la projection
node test_tuiles.js       # les étages 1 et 2
node test_proto.js        # les écrans + l'import de bout en bout
```

Les quatre doivent dire `TOUT EST VERT` et sortir en code 0.

> **`test_proto.js` refuse de tourner sur un assemblage périmé.** Il teste `index.html`,
> donc l'état du code au moment de la dernière couture : modifier `coeur.js` et oublier
> `assembler.py` le ferait valider du code qui n'est plus dans le fichier — ce que le
> contre-regard du Tour 55 a constaté (118 tests verts sur une faute injectée dans le
> noyau). `assembler.py` pose donc une empreinte SHA-256 des quatre sources dans le
> fichier produit, et le harnais la recalcule : à la différence, il sort en erreur.

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
