Salut Hermès,

Audit nickel, merci. Réponses point par point.

## uid() — collision d'IDs

Confirmé, go. Centralise `uid(prefix)` sur le pattern déjà en place pour e/p/t/g
(`prefix + Date.now().toString(36) + Math.random().toString(36).slice(2,6)`) et applique-le à
s/l/r/o. `pj` est déjà random via `normalizeProjet`, ne le touche pas. 15 min comme tu dis,
fais-le en premier — c'est le seul point réellement bloquant de l'audit.

## Stash v4.1.0 « garde-fous homonymes »

Pas un merge brut. La base a trop divergé : ta stash part d'avant `ee27216`, donc du modèle où
le projet possédait la ligne — le modèle actuel (v4.1+) fait des projets des étiquettes posées
sur des scénarios qui vivent dans les lignes. Un merge Git littéral va recoudre des hypothèses
mortes dans du code vivant.

Ce qui est bon dans ta stash, c'est le **concept**, pas le diff : détection d'homonymes,
confirmation avant de passer un scénario homonyme en série, bandeau dashboard. Ça reste
pertinent, et même plus qu'avant — la v4.4 vient justement de trancher la séparation
affichage/stats pour le scénario en production (`scenariosVisibles()` vs `statsProjet()`), donc
le risque de double comptage qu'attaquait ta stash est un sujet vivant, pas clos.

Décision : tu réimplémentes le concept en v4.5, contre le code actuel, en t'appuyant sur ta
stash comme spec de référence (pas comme patch à appliquer). Pas bloquant, tu l'enchaînes après
le fix uid().

## Poids des photos

D'accord, ajoute un affichage permanent du poids (pas seulement au seuil d'alerte) — petit
ajout, à caser où tu veux dans le paquet v4.5.

## Mono-fichier

Pas de refactor. La structure lignes→projets→tags est déjà prête si un jour on bascule sur un
petit backend (Supabase) — inutile d'anticiper tant que la fusion JSON suffit à l'usage réel
(voir plus bas).

## UI — prompt() natif pour créer un projet

D'accord, ça détonne avec le reste. Remplace par un panneau (même famille que le panneau projet
existant, avec son textarea Description) plutôt qu'un ajustement du prompt().

## Récap auto-tag à la création de projet

D'accord aussi — après création, le panneau qui s'ouvre affiche « N scénarios rattachés
automatiquement ». Petit ajout, à grouper avec le point homonymes/dashboard ci-dessus plutôt
qu'en isolé.

## Tes 4 questions

1. **Stash** : réintégrer en v4.5, comme concept réécrit contre le code actuel — voir ci-dessus.
2. **Version en production** : v4.4.0, déployée aujourd'hui sur
   `suivi-optimisation-septfons.surge.sh`. La mention « écart volontaire dépôt/production » dans
   le CHANGELOG 3.19.2 concernait une fenêtre de retour arrière ponctuelle, refermée depuis par
   la suite du développement (4.0→4.4) — ignore-la, elle n'est plus d'actualité.
3. **Usage réel** : Matis et moi saisissons déjà chacun de notre côté (Julien aussi, ponctuellement),
   le fichier circule déjà par export/import JSON entre postes. La fusion est déjà un chemin
   critique en usage réel, pas hypothétique — continue à la tester en priorité à chaque version,
   t'as raison de la remonter.
4. **Surge vs file:// local** : l'outil n'a aucun mécanisme de mise à jour automatique (fichier
   HTML unique, pas de service worker). Seuls ceux qui rechargent l'URL Surge reçoivent la 4.4.0
   automatiquement. Tout poste qui a une copie locale du fichier reste sur l'ancienne version
   tant qu'on ne lui renvoie pas le nouveau fichier — à garder en tête si tu distribues des
   correctifs.

## Poste de travail

Utilise `Documents\CeramTec\Suivi-optimisation-brakedisc` comme clone de référence — il est déjà
à jour (426abc5) et contient ta stash. J'ai retiré le vieux clone qui traînait sur le Bureau
(bloqué en v3.5.0 sur `dev`, mort, aucun rapport avec ton travail) pour éviter toute confusion
sur quel dossier est le bon. Pull avant de commencer, push + un mot quand tu livres, comme
d'habitude.

Vas-y pour uid() en premier.

Benjamin
