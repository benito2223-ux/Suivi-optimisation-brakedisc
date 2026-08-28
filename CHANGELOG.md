# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donnée à part).

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
