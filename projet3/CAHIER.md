# PROJET3 — cahier des charges, une page

> Ce fichier n'est pas de la documentation. C'est **l'aiguille** : le code doit le
> respecter, et s'il ne peut pas le respecter, c'est le cahier qui a tort.
> Écrit le 02/10/2026, avant la première ligne de code, sur carte blanche de
> Benjamin (« tu pars de 0 et tu crées l'outil parfait selon toi »).

---

## 1. La phrase

**Un poste d'usinage céramique/CBN doit être tranché en cinq minutes — quel insert,
quel gain, quelle preuve — et l'atelier doit pouvoir tout saisir, en gants, sur une
page qui ne plante jamais.** L'atelier d'abord, le pilotage ensuite, la hiérarchie
en dernier — dans cet ordre, toujours.

## 2. Ce que cet outil est

La **génération 3** du suivi d'optimisation du coût de revient des disques de frein
(Sept Fons). Il succède à l'app de production (4.80.0, 18 000 lignes) et au proto
(projet2, banc d'essai) : il reprend **les trois étages atelier-d'abord du proto**,
**la richesse de saisie de l'app**, et **l'identité visuelle restaurée du Tour 56**.
Il ne garde ni les vingt-deux panneaux de l'app, ni les angles morts du proto.

Trois publics, dans cet ordre (constitution §1) : l'atelier (Matis, opérateurs),
Matis pilote, la hiérarchie (la page A4 que Benjamin emmène à Detlef).

## 3. Le driver : le CPP en deux chiffres, jamais un

Le CPP outillage (`Σ prix / (arêtes × charnière)`) porte la décision — c'est le seul
chiffre comparable au classeur de Matis. Et chaque CPP affiché porte **deux axes** :
ce que le scénario **prévoit**, et ce que l'essai a **obtenu**. Le temps machine se
lit à côté, marqué « non comparable au classeur », seulement quand le cycle est saisi.
À chaque étage de l'arbre (pièce → OP → outil → logement) : le CPP obtenu, sa
référence, et l'écart (direction de Benjamin, 01/10/2026).

## 4. Les écrans — un fil, pas vingt panneaux

| # | Écran | La question | Porte d'entrée |
|---|---|---|---|
| 1 | **Accueil (tuiles)** | où en est-on, ligne par ligne | au chargement |
| 2 | **La ligne** | qu'est-ce qui tourne aujourd'hui | tuile → |
| 3 | **Le poste** | le scénario de production, décomposé jusqu'au logement | OP → |
| 4 | **L'optimisation** | ce qu'on teste, la preuve, la décision go/no-go | « optimiser » |
| 5 | **Emporter** | la page A4 pour Detlef | 1 clic |
| — | **Projets** (transverse) | qui pilote quoi, où en sont les projets | filtre + carte |
| — | **Données** | export, import, fusion, historique, zone rouge | bouton |

Les informations arrivent en douceur : le gros chiffre d'abord, la fiche derrière un
geste. Rien ne se répète dans un même écran. La raison d'un état est à côté de l'état.

## 5. Les invariants (constitution, forme de code)

1. **Source unique** : un même chiffre se calcule par une seule fonction (noyau pur),
   le rendu lit et ne calcule rien.
2. **Un absent ne se comble jamais** : « — volume annuel non saisi », jamais un 0 ni
   un « — » nu. Un poste non chiffrable est compté, pas dilué (« hors n opérations »).
3. **Les gains actés et projetés ne se somment jamais** — deux blocs étiquetés.
4. **Le battement prend le pire des deux côtés** (D/G), jamais la moyenne.
5. **Une cible sans chiffrage reste visible**, marquée « à chiffrer ».
6. **Le CPP outillage n'est jamais labellisé « CPP pièce »** ; le mot CPP seul
   désigne le coût outillage.
7. **Aucun chiffre qu'on ne peut pas remonter à sa source** — ni écran, ni A4.
8. **K et P_req jamais en sortie visible** ; « épaisseur de copeau » pour Hex ;
   nuances SPK ; « battement / Ra / épaisseur de piste » (jamais DTV ni voile) ;
   « Field Operations Suite » (jamais l'autre mot).
9. **La loi du correcteur** : un correcteur est un logement (D1, D2…), jamais un
   outil. Un outil porte ses logements ; plusieurs MABEC sur un outil est normal.
10. **Un correcteur qui se trouve dans l'excel de Matis est un logement.**

## 6. La technique — contraintes non négociables

- **Un seul fichier HTML déployé** (assemblé par `assembler.py`), vanilla JS/CSS,
  zéro framework, zéro build pour l'usage.
- **Zéro dépendance réseau** : polices embarquées (Manrope / Roboto / IBM Plex Mono,
  récupérées de l'identité du Tour 56), icônes locales. Test d'acceptation : ouvrir
  le fichier hors ligne.
- **Persistance locale** : localStorage (état courant) + historique de sécurité
  (5 instantanés avant toute importation ou réinitialisation). **Pas de cloud en
  v1** : les données ne quittent jamais le poste ; l'échange passe par l'export
  JSON et une **fusion** essai par essai (arbitrage `modifieLe`). Le cloud-ready
  reste dans le modèle (chaque entité porte sa date de modification).
- **Deux thèmes** (jour + nuit), impression A4 propre, tactile (cibles ≥ 44 px),
  lisible à 1–2 m, français uniquement. PWA (manifest + service worker versionné).
- **Migration sans perte** : import des formats 5, 6, 7 et 8 (tout ce que l'app a
  jamais produit) — y compris photos, plans, relevés Marposs et journal de rebut,
  que le proto jetait. Le rapport d'import compte et nomme ce qui entre.
- **Vocabulaire de Matis préservé** : MABEC, numéro d'outil, correcteur, CPP.

## 7. Ce que la v3 n'a pas (par choix, écrit ici)

- Le **classeur Matis** (delta théorie/réalité) : la question « le logement
  dépend-il de la référence ? » est posée à Matis et non tranchée — l'outil ne
  l'invente pas. La clé MABEC de raccordement est dans le modèle.
- L'**éditeur d'annotation photo** : les photos et leurs annotations existantes
  sont conservées à l'import et affichées ; le canevas d'édition reste dans l'app
  4.x jusqu'à ce que la v3 soit éprouvée.
- Le **cloud Supabase** : cf. §6. Une fois la v3 éprouvée, la synchro se greffe
  sur le même modèle sans réécriture.
- La **cadence** : pas de cadence mesurée par ligne — l'écran le dit, il n'estime pas.

## 8. L'ordre de construction (imposé)

Noyau pur testé → import testé sur les vrais exports → écrans. Jamais l'inverse.
Une suite de tests se juge sur **les tests exécutés**, pas seulement sur les échecs
(« 0 échec ≠ vert »). Un chantier de charte se vérifie à l'œil et à la capture,
jamais par « les tests sont verts ». Tout déploiement est vérifié par `curl`
(jamais par le « Success! » de surge) et reste en dehors de la prod — la prod ne
bouge que sur une phrase de Benjamin dans une session.
