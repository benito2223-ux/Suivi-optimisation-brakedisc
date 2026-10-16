# Cahier des charges — Refonte UX générale (inspiration Apple)

Document de cadrage, pas de code. Objectif : poser le diagnostic et les décisions de design
AVANT de recoder, dans une session dédiée (économie de tokens : la discussion de fond se fait
ici, l'implémentation ailleurs sur la base de ce document tranché).

## 0. Pourquoi maintenant

L'outil a grossi par ajouts successifs (statuts, plans outil, projets, responsables, scénario
en production...) sans jamais revoir l'ensemble. Chaque ajout était cohérent pris seul ; la
somme ne l'est plus. Verdict de Benjamin : « c'est fouilli ». Ce document ne rajoute pas une
fonctionnalité de plus — il réorganise l'existant.

## 1. Diagnostic — ce qui ne va pas concrètement

Observé en relisant le HTML actuel et en rechargeant l'outil (pas une impression vague) :

1. **Trois niveaux de navigation qui se ressemblent tous.** Ligne → Référence → OP s'affichent
   comme trois rangées de pastilles identiques (même forme, même couleur, même taille), empilées.
   Rien ne dit visuellement « ceci est le plus haut niveau, ceci le plus bas » — on lit trois
   fois la même chose avant de comprendre qu'il y a une hiérarchie.
2. **La barre d'outils mélange tout, sans priorité.** Rangée 1 : Exporter / Importer / Ajouter
   un scénario / Verrouiller / bouton « ⋯ ». Le bouton « ⋯ » ouvre une liste PLATE de 13 actions
   sans aucun regroupement : Export CSV, Vue de synthèse, Nouveautés, Tableau de bord,
   Suggestions, Options, Générer le PDF, Rapport de validation, Historique, Dossier local,
   Réinitialiser, Restaurer. Une action destructrice (Réinitialiser) est au même niveau visuel
   qu'une action fréquente (Tableau de bord) et qu'une action rarissime (Restaurer).
3. **Le titre de l'outil déborde à l'écran.** Sur une largeur d'écran atelier courante, le nom
   de la référence disque sort du cadre noir d'en-tête (`[Exemple] Référen...` tronqué net, pas
   même une ellipse propre). Le bandeau d'en-tête est traité comme un logo décoratif, pas comme
   un élément qui doit s'adapter au contenu réel.
4. **Le nom du scénario est répété deux fois d'affilée.** Le libellé de la carte de scénario
   actif (« [Exemple] Process actuel ★ ») est immédiatement suivi, dans le détail juste en
   dessous, du même nom en titre de section. Deux endroits disent la même chose à trois lignes
   d'écart.
5. **Une phrase d'explication en corps de texte flotte à côté d'un bouton d'action.** À côté de
   « + Créer un projet », une phrase complète en texte courant (« Un projet regroupe les
   scénarios qui répondent à une même problématique... ») s'affiche en permanence, comme si
   c'était un mode d'emploi imprimé sur l'écran plutôt qu'une info-bulle consultée au besoin.
6. **Trop de familles de pastilles colorées différentes**, sans langage visuel commun : statut
   du scénario (à l'étude/essai/validé/série/abandonné), badge ★ scénario en production,
   étiquettes de projet, indicateur de sauvegarde, indicateur multi-projets du tableau de bord.
   Chacune a sa propre forme, sa propre logique de couleur. L'œil doit réapprendre un code à
   chaque zone de l'écran au lieu d'un seul vocabulaire visuel appliqué partout.
7. **Tout est encadré.** Bordures sur les cartes, les pastilles de navigation, les champs, les
   panneaux, les boutons fantômes. La hiérarchie se fait par des traits plutôt que par de
   l'espace — visuellement chargé, fatiguant à lire longtemps sur un écran d'atelier.
8. **Les panneaux (Options, Import, Impression, Tableau de bord...) sont tous le même type de
   boîte modale**, quels que soient leur fréquence d'usage et leur taille de contenu réels —
   pas de distinction entre un réglage ponctuel et un tableau de bord qu'on garde ouvert.

## 2. Principes retenus (inspiration Apple, adaptée à l'atelier)

Apple HIG résumé en trois mots — clarté, déférence, profondeur — traduit ici :

- **Clarté** : une seule information par endroit. Si le nom du scénario est déjà visible dans
  l'onglet actif, il ne se répète pas juste en dessous. Le texte d'aide se consulte (icône ⓘ ou
  info-bulle), il ne reste pas affiché en permanence à côté d'un bouton.
- **Déférence à la donnée, pas au chrome.** Moins de bordures, plus d'espace blanc pour séparer
  les blocs. Une couleur pleine réservée aux informations qui comptent vraiment (le coût pièce,
  le statut de production), pas distribuée à chaque petit badge secondaire.
- **Profondeur = une seule hiérarchie visible à la fois.** Ligne / Référence / OP doivent se
  lire comme un fil d'Ariane à un seul niveau de lecture (texte, pas trois rangées de pastilles
  identiques), avec la possibilité de changer chaque maillon sans changer les trois d'un coup.
- **Contraintes atelier non négociables, à garder explicitement** (ce n'est PAS parce qu'Apple
  fait différemment qu'on les abandonne) : contraste fort (déjà posé en v3.15, à conserver),
  cibles tactiles larges pour un usage ganté, lisible à 1-2 mètres, aucune interaction qui
  dépend du survol (hover) seul, fonctionnement 100 % hors-ligne, français uniquement.

## 3. Nouvelle architecture de l'information

### 3.1 En-tête : un seul fil, pas trois rangées

Remplacer les trois rangées de pastilles (ligne / référence / OP) par **un fil de navigation à
une seule ligne**, dans l'esprit d'un fil d'Ariane :

```
EMAG 1  ›  [Exemple] Référence disque  ›  OP10
```

Chaque maillon reste cliquable pour ouvrir son propre sélecteur (liste déroulante des lignes,
des références de cette ligne, des OP de cette référence) plutôt que d'occuper une rangée
entière en permanence. Le niveau actif se distingue par un poids de texte plus fort, pas par
une pastille bleue identique aux deux autres niveaux.

Gain : trois rangées de largeur pleine → une seule ligne. Le regard descend directement vers le
contenu (scénarios) au lieu de traverser trois strates de navigation qui se ressemblent.

### 3.2 Barre d'action : trier par fréquence, pas tout mettre à plat

Trois niveaux d'accès, pas un bouton plat + un menu fourre-tout :

- **Toujours visible (2-3 actions max)** : l'action la plus fréquente du contexte courant
  (ex. « + Ajouter un scénario » sur la vue OP), l'export (sauvegarde du travail — trop
  important pour être caché), et l'indicateur d'état de sauvegarde.
- **Menu contextuel groupé** (remplace le « ⋯ » plat actuel) : les 13 actions actuelles
  regroupées en 3-4 familles avec un séparateur visuel et un intitulé de groupe, par exemple :
  - *Consulter* : Vue de synthèse, Tableau de bord, Export CSV
  - *Documenter* : Générer le PDF, Rapport de validation, Nouveautés
  - *Gérer* : Options, Suggestions, Dossier local, Historique
  - *Zone rouge, séparée visuellement et en dernier* : Réinitialiser, Restaurer
- **Réglages de la campagne (Options)** restent dans leur propre panneau, inchangé sur le fond,
  mais accessible depuis le menu *Gérer* plutôt que noyé au même niveau que « Générer le PDF ».

### 3.3 Cartes de scénario : l'info ne se répète pas

Le nom du scénario actif s'affiche UNE fois (dans sa carte, en tête de la zone de détail qui
s'ouvre juste en dessous — pas dans les deux). Le détail qui suit commence directement par les
chiffres clés (coût pièce, cycle, validation), pas par un rappel du titre déjà lu trois lignes
plus haut.

### 3.4 Un seul langage de pastille, réutilisé partout

Définir **une seule forme de badge** (même hauteur, même rayon d'angle, même famille de police)
utilisée pour : statut de scénario, badge ★ production, étiquette de projet, indicateur
multi-projets. Seule la couleur change selon le sens (déjà globalement le cas avec
`OUTIL_COLORS`), pas la forme ni la taille. Aujourd'hui chaque zone de l'écran a sa propre
variante — à unifier en un seul composant CSS réutilisé.

### 3.5 Aide : consultée, pas imposée

Le texte explicatif à côté de « + Créer un projet » (et tout texte similaire ailleurs) passe en
info-bulle ou dans le panneau « Comment ça marche » existant, pas affiché en permanence en
corps de texte flottant à côté d'un bouton d'action.

### 3.6 En-tête (bandeau noir) : robuste au contenu réel

Le titre affiché (nom de la référence) doit tronquer proprement avec une ellipse (`…`) ou
passer sur une seconde ligne selon la largeur disponible — jamais déborder hors du cadre. Un
`title=""` HTML (info-bulle native) reprend le texte complet si tronqué.

## 4. Système visuel

- **Espacement** : passer d'une logique « bordure pour séparer » à une échelle d'espacement
  cohérente (ex. 4/8/12/16/24/32 px) qui sépare les blocs par du vide plutôt que des traits.
  Garder des bordures uniquement là où deux zones cliquables adjacentes en ont réellement besoin
  (ex. cartes de scénario côte à côte).
- **Typographie** : les polices actuelles (Manrope / Public Sans) sont bonnes et restent. Le
  travail est sur le NOMBRE de tailles utilisées à l'écran en même temps — réduire à une échelle
  claire (ex. titre de section / corps / légende / chiffre clé) au lieu de tailles ad hoc
  ajoutées au fil des versions.
- **Couleur** : conserver la palette `OUTIL_COLORS` et les couleurs de statut existantes (déjà
  travaillées en v3.15 pour le contraste — ne pas tout refaire). Le changement porte sur leur
  RÉPARTITION : réserver la couleur pleine (fond coloré) aux 2-3 informations qui comptent le
  plus par écran (coût, statut de production), et garder les informations secondaires en
  contour ou en texte coloré sans fond plein, pour que la couleur pleine garde sa valeur
  d'alerte visuelle.

## 5. Ce qui NE change PAS (hors périmètre explicite)

- Le modèle de données (`lignes` → `references` → `ops` → `scenarios` → `essais` →
  `prelevements`, les projets par étiquettes) : refonte visuelle uniquement, aucune migration de
  données requise par ce chantier.
- Le fonctionnement 100 % hors-ligne, fichier unique, sans dépendance réseau.
- Le contraste fort et la lisibilité atelier posés en v3.15 — on les renforce, on ne les
  abandonne pas au nom du style.
- Les fonctionnalités elles-mêmes (calculs, essais, prélèvements, projets, scénario en
  production) : ce chantier réorganise leur présentation, n'en retire aucune et n'en ajoute pas.

## 6. Plan de mise en œuvre proposé (par étapes, pour une refonte progressive et non un big-bang)

1. **Fil de navigation unique** (remplace les 3 rangées de pastilles) — le changement le plus
   visible, le plus structurant, le moins risqué (pas de logique métier touchée).
2. **Barre d'action groupée** (remplace le menu « ⋯ » plat) — regroupement pur, aucune action
   supprimée ni ajoutée.
3. **Composant de badge unique** appliqué progressivement à chaque zone (statut → ★ production →
   étiquettes projet → tableau de bord).
4. **Nettoyage des répétitions** (nom de scénario, textes d'aide flottants) et passage aux
   info-bulles.
5. **Passe d'espacement/bordures** sur l'ensemble, une fois les trois points précédents en place
   (sinon on repeint une structure qu'on va encore bouger).

## 7. Comment on saura que c'est réussi

- Le fil de navigation tient sur une ligne à la largeur d'écran atelier habituelle, sans
  troncature sauvage.
- Le menu d'actions secondaires se lit en groupes nommés, la zone destructrice (Réinitialiser /
  Restaurer) est visuellement séparée du reste.
- Aucune information (nom de scénario, texte d'aide) ne s'affiche deux fois dans le même écran
  sans raison.
- Un même badge de statut, vu sur une carte de scénario, sur le tableau de bord et sur une
  étiquette de projet, a la même forme partout — seule la couleur/le texte changent.
- Testé par Benjamin sur un écran de largeur atelier réelle (pas seulement en plein écran
  bureau) avant validation finale.
