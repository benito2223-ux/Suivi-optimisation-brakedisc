# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donnée à part).

## [3.3.0] — 2026-08-29

Toggle de comparaison graphique v2.5 / v3.2 — **temporaire**, le temps de recueillir l'avis
de Matis (Stellantis) sur la refonte avant de basculer `main` dessus.

### Ajouté
- Un bouton flottant en bas à droite ("🎨 Voir l'ancien design" / "🎨 Voir le nouveau design")
  bascule entre l'habillage v2.5.0 (en-tête classique, pas de rail) et la refonte v3.0+
  (rail sombre, en-tête en carte, verdict retravaillé). Le choix est mémorisé
  (`localStorage`) et survit à la fermeture du fichier.
- Techniquement additif comme la refonte elle-même : les deux blocs CSS `@media screen`
  de la refonte sont conditionnés à `html:not([data-layout="classic"])` (CSS nesting), et
  le script qui construit le rail s'arrête tôt si le mode classique est actif. Rien n'a été
  dupliqué ni retiré de l'ancien CSS.
- Les évolutions fonctionnelles apportées depuis (essais en tuiles, icônes aide/légende,
  menu ligne) restent actives dans les deux habillages — seul l'agencement visuel change.

### À faire une fois le choix arbitré
- Retirer le bouton, le script de bootstrap en tête de fichier, et les deux conditions
  `html:not([data-layout="classic"])` (en gardant leur contenu tel quel si v3.2 est retenu ;
  en supprimant les deux blocs `@media screen` de la refonte si l'ancien design est retenu).

## [3.2.0] — 2026-08-29

Essais en tuiles + informations de ligne — deux ajouts après retour terrain sur la v3.1 :
l'écran d'un scénario affichait tous ses essais entièrement dépliés (tableau, graphique
Marposs, photos) en permanence, ce qui devenait confus dès qu'une campagne comptait
plusieurs essais.

### Ajouté
- **Informations de ligne** : une icône ⚙ sur l'onglet de ligne actif (à côté de ✎ renommer)
  ouvre un panneau avec coût horaire (€/h), observations libres, et dernière maintenance
  (date + type d'intervention en texte libre). Champs préparatoires — pas encore intégrés
  au calcul du coût/pièce.
- Les deux paragraphes "Sauvegarde" et "Méthode de calcul", auparavant fixes en bas de page,
  sont maintenant deux sections du panneau "Comment ça marche" (même icône ⓘ).

### Changé
- **Essais en tuiles** : chaque essai est replié par défaut (titre, date, badge de statut
  coloré selon l'état — conforme / non conforme / en cours). Cliquer la tuile déplie les
  détails (conditions de coupe, tableau de prélèvements, photos, suivi Marposs). Un essai
  nouvellement créé s'ouvre automatiquement pour la saisie ; les autres restent repliés.
  L'état ouvert/fermé de chaque tuile survit à la ressaisie d'une mesure (qui redessine
  l'écran) grâce à un suivi séparé, scénario + essai.
- Le résumé (fermé) du tiroir "Conditions de coupe et plaquettes" affiche maintenant la
  référence plaquette et le coût/pièce de chaque logement, plutôt que le numéro d'outil
  seul — l'info reste lisible sans avoir à déplier le tableau à 13 colonnes.

### Corrigé
- La coloration rouge du filet gauche d'un essai non conforme ne s'appliquait jamais
  (la classe posée par le code, `risk`, ne correspondait pas à la classe attendue par le
  CSS, `bad`) — corrigé au passage.

## [3.1.0] — 2026-08-29

Décluttering de l'écran de travail — les informations d'attribution (site, interlocuteurs,
mention confidentielle) et les aides secondaires n'ont pas leur place en permanence sous les
yeux ; elles sont soit déplacées en pied de document, soit rangées derrière une icône.

### Changé
- **En-tête écran** : le bloc site / interlocuteurs Stellantis / interlocuteur CeramTec est
  retiré de l'écran. Cette information reste dans les documents imprimés et exportés, mais
  déplacée en pied de page plutôt qu'en haut.
- **Bandeau « Confidentiel »** : retiré de l'écran (redondant avec le fait que l'outil ne
  quitte jamais le poste local). Conservé uniquement en pied des documents imprimés et du
  rapport de validation exporté, à côté de la mention site/interlocuteurs.
- **« Comment ça marche »** : réduit à une icône (rond bleu au survol/ouverture) au lieu d'une
  carte pleine largeur avec son intitulé en toutes lettres. Le contenu ne change pas, seul son
  déclencheur devient discret.
- **Légende champ éditable / calculé automatiquement** : les deux lignes de texte permanentes
  sont remplacées par un bouton compact (les deux pastilles de couleur) avec l'explication en
  info-bulle, posé à côté de l'icône d'aide.
- **Statut de sauvegarde** (barre d'outils) : le texte descriptif devient une pastille colorée
  (gris neutre / ambre en cours / vert exporté / rouge bloqué), le détail complet passant en
  info-bulle. Les indicateurs de la même famille dans le menu `•••` (dossier photos, révision)
  ne sont pas concernés, ils sont déjà dans un menu secondaire.

### Non affecté
- Aucune donnée, logique de calcul ou de validation modifiée.
- Le rapport de validation exporté et l'impression conservent l'intégralité de l'information
  (site, interlocuteurs, confidentialité), simplement repositionnée en pied de document.

## [3.0.0] — 2026-08-29

Refonte visuelle + coquille applicative — le plan de travail gagne un rail de navigation
permanent, et l'en-tête, le verdict et les chiffres clés sont retravaillés dans la charte SPK.
Changement structurel (nouvelle disposition en grille), d'où le passage en version majeure.

### Changé
- **Nouvelle coquille applicative** : rail sombre collé à gauche (`#0f2740`), plan de travail à
  droite. Le rail contient le logo, la sélection Ligne › Référence › OP, la liste des scénarios
  (coût/pièce et delta visibles sans naviguer) et les actions (export/import, PDF, réinitialisation).
  Sous 1080px, le rail repasse en flux normal au-dessus du contenu.
- Sélecteurs Ligne / Référence / OP regroupés dans un conteneur commun (`.ctx-rail`), collé en
  haut de son conteneur ; se replie automatiquement si les trois listes sont vides.
- En-tête transformé en carte à filet bleu SPK, eyebrow précédé d'un tiret rouge, titre en
  Archivo 800.
- Bandeau verdict : fond teinté plat (au lieu du dégradé) + barre d'accent de 5px à gauche selon
  l'état (référence / conforme / hors tolérance / en attente).
- Chiffres clés de pied de scénario agrandis (jusqu'à 44px), deltas présentés en pastilles.
- Cartes de scénario, encarts (notes, aide, Marposs, photos, backlog) et boutons harmonisés :
  rayons plus généreux, ombres portées cohérentes, repères de section en tiret rouge.
- Menu `•••` de la barre d'outils : s'ouvre désormais vers le haut depuis le pied du rail.

### Non affecté
- Aucune donnée, clé de stockage ou logique métier modifiée : sélection, saisie, mode atelier,
  suivi Marposs, export/import JSON/CSV/PDF, historique local — tout est inchangé.
- Rendu impression / export PDF inchangé (le rail est masqué à l'impression).
- Thème sombre (`prefers-color-scheme: dark` / `[data-theme="dark"]`) préservé tel quel.

### À vérifier
- Rendu non testé visuellement avant intégration (contrainte de l'outil de conception utilisé).
  À valider dans un navigateur réel (Edge/Chrome desktop, puis tablette) avant diffusion large.

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
