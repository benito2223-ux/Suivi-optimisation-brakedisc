# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donnée à part).

## [2.5.0] — 2026-08-28

Refonte typographique — c'est la police condensée qui donnait à l'outil son côté
« documentation industrielle ».

### Changé
- **Titres : Open Sans Condensed → Archivo** (600/700/800). Le condensé compressait tout et
  évoquait la fiche technique ; Archivo a de la présence aux grandes tailles.
- **Chiffres : Courier New → IBM Plex Mono**, dessiné pour les contextes techniques. Dans un
  outil de mesure, les chiffres sont le sujet principal.
- **Corps de texte : Open Sans conservé** — c'est la police de la charte SPK, et les documents
  générés partent chez Stellantis sous cette identité.
- Tracking resserré aux grandes tailles, et chiffres tabulaires forcés partout où des nombres
  s'alignent en colonne (ils ne dansent plus d'une ligne à l'autre).

### Corrigé
- Nom de scénario tronqué dans l'en-tête (« Mixte T50013 — bol CBN + piste céramiq… ») :
  Archivo étant plus large, le champ occupe désormais sa propre ligne pleine largeur.

### Documentation
- Mode d'emploi PDF refait en 6 pages : adresse en ligne en couverture, nouvelle section
  « Lire un scénario » (ordre verdict → chiffres → graphique → essais → configuration),
  mode atelier, suivi Marposs, dossier local photos, suggestions avec image, installation
  en application sur Edge et sur iPad.

## [2.4.0] — 2026-08-28

Refonte de la hiérarchie de lecture et arrivée du mode atelier. L'outil ne se contente plus
d'afficher des données : il énonce sa conclusion.

### Ajouté
- **Bandeau verdict** en tête de chaque scénario : le gain formulé en une phrase
  (« −46,7 % de coût outil par pièce · 2× la durée de vie d'arête · validation en cours »),
  avec chips coût/pièce, durée de vie et taux hors tolérance. Le scénario de référence
  s'affiche comme « Référence de production — base 100 ».
- **Mode atelier** : saisie plein écran conçue pour être utilisée debout devant la machine,
  avec des gants. Champs de mesure à 78px, n° de pièce deviné à partir du pas réel de
  prélèvement, sélecteurs de logement et de point de mesure en gros boutons, barre de
  progression vers la charnière, retour immédiat conforme / hors tolérance après chaque
  validation, Entrée pour enregistrer. Écrit dans les mêmes données que la saisie tableau.
- Support tactile réel : `@media (pointer: coarse)` avec cibles à 44px minimum sur écrans
  tactiles uniquement, et breakpoint < 720px (KPI sur 2 colonnes, barre d'outils pleine
  largeur).

### Changé
- Nouvel ordre de lecture d'un scénario : verdict → chiffres clés → graphique → essais →
  configuration → rebut. La preuve visuelle passe avant les détails de configuration.
- Le tableau outils/logements se replie une fois la campagne lancée (déplié automatiquement
  tant qu'une référence plaquette manque, et toujours déplié à l'impression).
- Couleurs Marposs tokenisées (`--teal`, `--teal-strong`) et éclaircies en thème sombre.

### Corrigé
- **`<meta viewport>` absent** : sur iPhone/iPad la page se rendait en 980px puis rétrécissait,
  rendant l'outil inutilisable au doigt. C'était le blocage principal pour l'usage tablette.
- **`<meta charset>` absent** : risque d'accents cassés à l'ouverture du fichier en local.
- **Graphique vide à la première ouverture** sur les scénarios EMAG 1 : les données de départ
  ne passaient pas par `normalizeScenario`, donc la mesure restait dans `batt` sans être
  reportée sur Droite/Gauche.
- Contraste insuffisant du teal Marposs en thème sombre (3,03:1 → conforme).
- Flèches d'incrément désactivées en mode atelier (le piège qui rendait la saisie pénible).

## [2.3.0] — 2026-08-28

Simplification structurelle, pas seulement visuelle — "loin d'être radical" puis "sois plus
radical pour simplifier" ont motivé ce passage : réduire ce qui est visible en permanence,
pas seulement le restyler.

### Changé
- Barre d'outils réduite de 13 à 3 boutons visibles (Exporter, Importer, + Ajouter un
  scénario) ; tout le reste (CSV, Synthèse, Suggestions, Options, PDF, Rapport, Historique,
  Dossier local, Réinitialiser, Restaurer, nom de l'exportateur) déplacé dans un menu "•••".
- Tableau des outils/logements : colonnes Rayon de bec et ap (affinage Fr·Fa) masquées par
  défaut tant que ce module optionnel n'est pas activé — 13 colonnes au lieu de 15. κr reste
  toujours visible (utilisé aussi par le widget K, indépendant de Fr·Fa).

## [2.2.0] — 2026-08-28

Deuxième passage design, plus marqué que le 2.1.0 — "loin d'être radical" était le retour, donc
changements à effet visuel net cette fois plutôt qu'incrémental.

### Changé
- Onglets Ligne de production / Référence disque / OP transformés en **contrôle segmenté**
  (piste grise, segment actif élevé en pilule blanche avec ombre douce) — remplace les
  rectangles bordés bleu-sur-bleu.
- Chiffres clés (coût/pièce, coût/arête, temps de cycle) fortement agrandis (25px → 38px, plus
  gras) avec libellés réduits au-dessus, pour un vrai contraste "chiffre héros / légende".
- Cartes comparatives de scénarios (`tab-card`) : coins plus généreux, ombre portée douce,
  anneau bleu net sur la carte active (au lieu d'un bord rouge/bleu sans signification claire).

## [2.1.0] — 2026-08-28

Passage design "élégance dans la simplicité" — pas de nouvelle fonctionnalité, ni de rupture,
mais un changement visuel assez large pour mériter son propre numéro.

### Changé
- Nouveaux tokens de rayon (`--radius-lg/--radius/--radius-sm`) : coins plus doux sur les
  cartes, panneaux et contrôles (avant : 3px partout, très anguleux).
- Boutons repensés : fond neutre discret par défaut, couleur pleine réservée aux actions
  principales (Exporter, Ajouter un scénario), forme plus arrondie, léger effet de survol.
- Icônes de la barre d'outils et des sections Marposs/Photos remplacées par des icônes traits
  fins cohérentes (au lieu d'emojis).
- Titres de section : bleu appuyé remplacé par un gris neutre — la couleur ne reste que pour ce
  qui est interactif.

## [2.0.0] — 2026-08-28

Version de consolidation : marque le passage d'un usage exploratoire à un outil structuré,
partagé (dépôt GitHub, hébergement en ligne) et documenté au fil de l'eau via ce changelog.
Regroupe tout ce qui a été construit depuis la version initiale.

### Ajouté
- Hiérarchie complète **Ligne de production → Référence disque → OP → Scénario → Essai → Prélèvement**
  (avant : une seule référence, un seul niveau de scénarios).
- Modèle **Outil → Logement** par scénario (N outils, N logements chacun), avec code couleur par
  outil et charnière indépendante par logement (avant : bol/piste fixes).
- Mode EMAG 1 (mesure Droite/Gauche) avec bascule automatique selon la ligne de production.
- Widget **K** (indice thermique) par logement, et ratio **Fr/Fa** optionnel (activable par OP).
- Scénario **de référence (★)** interchangeable, base 100 pour les comparaisons de coût/cycle.
- Critère de validation dissociable par logement : charnière seule, ou charnière + tolérance.
- Suivi **Marposs** par essai : collage direct de l'extraction de production, fenêtre de l'essai
  surlignée sur le graphique, moyenne essai vs moyenne journée.
- **Photos par essai**, stockées comme de vrais fichiers dans un dossier local choisi par
  l'utilisateur (jamais dans le fichier d'échange JSON) — nécessite Edge/Chrome et la version en
  ligne de l'outil.
- Backup automatique dans ce même dossier local, en plus de la sauvegarde navigateur.
- **Historique local** (5 derniers points de reprise automatiques) et garde-fou au chargement si
  le fichier semble vide alors qu'une sauvegarde plus ancienne contient des données.
- Vue de synthèse comparative (tableau + graphique superposé multi-scénarios).
- Onglet **Suggestions** (remontées Matis/Arthur, avec pièce jointe image) et rapport de
  validation HTML autonome, incluant désormais le détail des prélèvements.
- Export CSV limité au scénario affiché, avec sélection des essais à inclure.
- Couleur fixe et cohérente par point de mesure (Inter/Exter...) sur le graphique de tendance.
- Export/import qui rouvrent sur l'onglet exact utilisé au moment de l'export.
- Installation possible comme application (Edge/Chrome), icône SPK dans l'onglet et à
  l'installation.

### Corrigé
- Perte de réactivité de la saisie clavier physique (un clic ne validait qu'un incrément).
- Précision des mesures (3 décimales, clavier numérique adapté).
- Double confirmation par saisie de texte avant "Réinitialiser" (au lieu d'un simple clic).

### Changé
- Hébergement de référence : `https://suivi-optimisation-septfons.surge.sh`, en plus du fichier
  local — mise à jour transparente pour Matis/Arthur (rechargement de page, plus d'envoi de
  fichier).
- Code versionné sur GitHub (dépôt privé), données et exports jamais versionnés (`.gitignore`).

## [1.0] — avant 2026-08-27 (rétroactif)

Première version en usage réel chez Stellantis Sept Fons : suivi mono-référence, scénarios
bol/piste fixes, export/import JSON manuel, tolérance unique par campagne.
