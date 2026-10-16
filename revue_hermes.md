# Demande de revue — Suivi_optimisation_SPK

## Contexte

`bilan_economique.html` (joint à ce message) est un outil de suivi d'essais et de bilan
économique pour des plaquettes/outils céramiques en usinage (tournage de disques de frein,
site Stellantis Sept Fons). Développé par un ingénieur d'application terrain (pas
développeur de métier), avec l'assistance de Claude.

**Contraintes techniques volontaires, à respecter dans les suggestions :**
- Fichier HTML unique, vanilla JS/CSS, **aucune dépendance de build**. Toute suggestion
  doit rester compatible avec ce format (pas de framework, pas d'étape de compilation).
- Fonctionne 100 % hors-ligne, aucune donnée envoyée à un serveur. Persistance via
  `localStorage` (état courant) + `IndexedDB` (handle de dossier local) + export/import
  manuel au format `.json` pour l'échange entre collègues.
- Utilisateurs : ingénieurs/opérateurs d'atelier (usage tactile/écran partagé possible),
  interface entièrement en français, vocabulaire métier usinage/céramique.

**Hiérarchie des données :** Ligne de production → Référence disque → OP → Scénario →
Essai → Prélèvement. Un scénario porte des outils, chacun avec un ou plusieurs logements
(ex. bol/piste), chacun avec ses conditions de coupe (Vc, f, charnière, prix plaquette...).

## Ce qui a été ajouté récemment (contexte des dernières évolutions)

- Modules de calcul optionnels dans **Options** : coût du rebut, temps de cycle en
  secondes, coût machine, pièces détachées, volume annuel, effort Fr/Fa, détail du cycle
  par logement (temps coupe/déplacement mesurés machine vs indice base 100).
- Fiche outil (PDF/image) attachable par OP.
- Champs par essai : rédigé par, fin d'essai (date+heure), programme CNC.
- Champs par outil : correcteur, type d'outil.
- **Éditeur d'annotation de photo** (nouveau, canvas) : rognage non destructif, flèches
  droites/courbes, rectangles, ellipses, texte flottant, palette de couleurs — tout stocké
  en coordonnées vectorielles (fractions de l'image d'origine), recomposé à l'affichage.

## Ce qu'on te demande

Une revue de fond de l'outil dans son ensemble, sur trois axes :

### 1. Cohérence
- Le modèle de données est-il cohérent de bout en bout (normalisation, migrations
  d'anciens formats, valeurs par défaut) ? Des champs orphelins, redondants, ou qui se
  contredisent ?
- Les calculs économiques (coût/pièce, gain annuel, seuil de bascule, temps de cycle)
  sont-ils internement cohérents entre les différents modules quand plusieurs sont
  activés ensemble ? Cas limites où deux modules pourraient se contredire ?
- La logique de repli (ex. le calcul détaillé du cycle qui retombe sur l'indice base 100
  si incomplet) est-elle appliquée partout où elle devrait l'être, sans angle mort ?

### 2. Robustesse
- Gestion des erreurs / cas limites : valeurs vides, NaN, division par zéro, tableaux
  vides, `localStorage` plein (quota dépassé), `File System Access API` non supportée ou
  permission révoquée, import d'un JSON malformé ou d'une version antérieure.
- Compatibilité navigateur (l'app cible Edge/Chrome desktop pour les fonctions avancées) —
  y a-t-il des dépendances silencieusement cassées ailleurs (Firefox, Safari, mobile) ?
- Perte de données possible : y a-t-il des chemins où une action utilisateur pourrait
  effacer ou corrompre des données sans confirmation ni sauvegarde de secours ?
- Performance sur un fichier JSON qui grossit (beaucoup d'essais/prélèvements/photos
  annotées) — points de ralentissement prévisibles ?

### 3. UI/UX
- Clarté et découvrabilité des modules optionnels (Options) — un nouvel utilisateur
  comprend-il ce qu'il active et pourquoi, sans devoir demander ?
- Cohérence visuelle et de vocabulaire entre les écrans (mêmes libellés, mêmes unités,
  mêmes conventions de couleur pour statut/validation/alerte).
- Utilisabilité en contexte atelier (doigts gantés, écran parfois petit, lumière
  variable) : tailles de cible tactile, contraste, lisibilité des tableaux denses.
- Le nouvel éditeur d'annotation en particulier : la prise en main est-elle intuitive
  sans documentation (outils, couleurs, validation du rognage, poignée de courbe) ?
- Formulaires longs (composition du scénario, bloc essai) : sont-ils scannables, ou le
  nombre de colonnes/champs devient-il écrasant quand plusieurs modules sont actifs à la
  fois ?

## Livrable attendu

Une liste priorisée de constats, si possible avec :
- **Sévérité** (bloquant / gênant / cosmétique) et **catégorie** (cohérence / robustesse /
  UI-UX).
- **Où** (nom de fonction, section d'écran, ou description précise du parcours) —
  l'app fait ~6000 lignes en un seul fichier, une référence précise fait gagner du temps.
- **Le problème concret** et si possible **une piste de correction**, en gardant à
  l'esprit les contraintes techniques ci-dessus (pas de framework, pas de build).

Merci de ne pas te limiter aux évolutions récentes listées plus haut : une revue de
l'ensemble de l'outil est souhaitée, y compris les parties plus anciennes et stables.
