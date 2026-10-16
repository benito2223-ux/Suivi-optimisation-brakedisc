# Réponse au cadrage — revue v7

Ton résumé du spec est juste, on est alignés. Les deux réponses, puis un point à corriger.

## 1. Oui, va voir le code

Franchement oui, et pas seulement pour valider des hypothèses : le §4 du spec est une
description, le code est la source. Là où les deux divergent, **c'est le code qui a raison** —
signale-le moi, ça voudra dire que ma description a décroché.

Ordre suggéré, du plus rentable au moins :

1. **`lib/db/`** en premier — `cout.ts` (prix de revient et coût série), `gain.ts` (gain
   annualisé), `essai.ts` (verdict de conformité). C'est le cœur, c'est petit (~500 lignes au
   total), et c'est là qu'un bug est invisible. Si tu ne lis qu'une chose, lis ça.
2. **`app/(app)/pieces/[id]/PieceDetail.tsx`** — 957 lignes, le plus gros fichier du projet,
   et celui qui a le plus grossi par ajouts successifs. Ton avis sur sa structure m'intéresse
   autant que ton avis sur son UI.
3. **`app/(app)/radar/RadarBoard.tsx`** — 721 lignes, l'écran principal.
4. **`supabase/migrations/`** — 14 fichiers, et un `README.md` qui documente l'ordre de rejeu
   et les pièges. Les RLS multi-tenant sont dans `fellow_multi_tenant_isolation`.

Un test que tu peux faire sans rien exécuter : sur la pièce AXE-42C, le moteur affiche
0,207 € de consommable/pièce, 1,427 € de temps machine, 1,633 € de prix de revient, et pour
une série de 200 : 6 consommables, 58,20 €, soit 1,718 €/pièce. Les données d'entrée sont dans
`fellow_schema_v1` (outils T01/T02/T03, opérations OP10/20/30, 48 €/h). Si tu refais le calcul
à la main et que tu tombes ailleurs, dis-le tout de suite — ça passerait avant tout le reste.

## 2. Navigation : oui

Tu as raison, ça change la qualité du §UI/UX, et l'UI est justement le point sur lequel je
suis insatisfait depuis le début. Je t'envoie des identifiants par un canal séparé.

Deux consignes en contrepartie :

- **Crée tout ce que tu veux, ne supprime rien de ce qui existe.** Les 4 pièces, 3 machines et
  7 outils du jeu de démo me servent à montrer l'outil ; ils sont reconstructibles par la
  migration, mais je préfère ne pas avoir à le faire.
- Ce compte est le seul en service : ce que tu saisis est visible pour moi et pour n'importe
  quelle démo. Nomme ce que tu crées de façon reconnaissable (préfixe `ZZ-` par exemple).

Fais quand même le §1 : la navigation te dira ce que l'écran donne à voir, le code te dira
pourquoi. Les deux ensemble valent bien plus que l'un des deux.

## 3. Ton message annonce deux choix de cadrage, je n'en vois qu'un

Tu écris « deux choix de cadrage à trancher », puis une seule question — « comment veux-tu que
je fasse cette revue ». Le second manque. Reformule-le si tu l'avais en tête, je te réponds
avant que tu te lances.

Sur celui que je lis, voici comment je veux la revue :

- **Par ordre de conséquence, pas par ordre d'écran.** Commence par ce qui empêche de livrer,
  pas par un tour du propriétaire. Si trois choses seulement comptent, dis-moi trois choses.
- **Nommée et située.** « Le bandeau de prix de revient dans `PieceDetail` devrait X parce que
  Y » est exploitable ; « améliorer la hiérarchie visuelle » ne l'est pas.
- **Coûts en ordre de grandeur suffisent** — heure, journée, semaine. Pas besoin de plus
  précis, et une fausse précision me ferait plus de mal que de bien.
- **Ta définition du « prêt à livrer » d'abord.** C'est le livrable qui m'intéresse le plus,
  parce que c'est celui que je n'ai pas su écrire. Ne la déduis pas de ce qui est déjà
  construit : pars de ce qu'un patron de PME doit pouvoir faire seul pendant un mois, et
  regarde ensuite ce qui manque.
- **Trois pages utiles valent mieux que dix.** Tu peux couper court sur ce qui va bien.

Et le point du spec que je maintiens : contredis-moi. Le modèle Gamme et l'exclusion du
porte-outil et du rebut du prix de revient sont mes décisions les plus discutables, prises
seul, sans utilisateur réel pour l'instant.
