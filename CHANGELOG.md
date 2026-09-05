# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donnée à part).

## [3.18.0] — 2026-09-05

### Ajouté — vue d'ensemble de la composition
Le « premier coup d'œil » tenait dans `.config-resume` : une ligne en 11 px mono, `--ink-faint`,
qui concaténait toutes les plaquettes bout à bout. Cette ligne essayait d'être deux choses à la
fois — l'étiquette d'un volet repliable **et** la vue d'ensemble du scénario. Elle était
dimensionnée comme une note de bas de page et lue comme un tableau de bord.

`compositionApercuHTML()` lui donne son propre bloc, **hors du volet repliable** donc visible
que la composition soit ouverte ou fermée : une tuile par logement (référence, charnière avec la
durée de vie réellement observée, prix/arêtes, €/pièce en bleu), chiffres à 19 px, en-tête avec
le compte d'outils et le coût outillage total à 22 px. Les données manquantes sont listées sous
la tuile concernée (« Manque : référence, prix ») au lieu d'être découvertes plus tard dans un
calcul qui ne tombe pas. L'ancienne ligne de résumé devient ce qu'elle aurait dû rester : une
étiquette (« outils, plaquettes, conditions de coupe — 3 fiches »).

### Ajouté — fiches outil repliables
`.outil-carte` passe de `<section>` à `<details>`, **fermé par défaut**, avec un `<summary>`
lisible : n° d'outil, correcteur, type, logements, badge plan, coût de l'outil. L'état ouvert
est mémorisé dans `outilsOuverts` (même mécanique que `essaisOuverts`) et survit aux re-rendus.
Avec l'aperçu au-dessus, on ne déplie que ce qu'on veut modifier.

### Ajouté — plan par outil (PDF ou image)
Nouveau champ `outil.plan`, distinct de `op.ficheOutil` (qui couvre toute l'opération et reste
inchangé). Deux modes de stockage, choisis automatiquement :
- **dossier local connecté** → le fichier est écrit via `writePhotoBlob()` sous le nom
  `plan_<scénario>_<outil>_<horodatage>.<ext>`, seul le nom est stocké dans le JSON. Mode
  recommandé et sans limite gênante.
- **sans dossier** → base64 dans le fichier de suivi, mais **uniquement sous 500 ko**. Au-delà,
  l'outil refuse et explique : `localStorage` plafonne autour de 5 Mo pour l'intégralité du
  suivi, deux plans de 1,5 Mo suffiraient à le saturer et à bloquer l'enregistrement des
  mesures. Le message indique le chemin pour connecter le dossier.

Retirer un plan stocké en dossier ne supprime que le lien, pas le fichier — c'est dit dans la
confirmation.

### Tests
68/68 (3 ajoutés) : `normalizeOutil` pose `plan: null` par défaut et conserve un plan existant
à l'identique, y compris à travers `normalizeScenario` — un plan perdu au rechargement aurait
été une disparition silencieuse.

## [3.17.0] — 2026-09-05

### Modifié — composition du scénario : fiches au lieu d'un tableau
Le bloc de saisie des outils était un tableau de 15 colonnes rendu en 11 px, avec
`table-layout:fixed` et des largeurs en pourcentage. La colonne « N° outil » recevait 6 % de
920 px — environ 55 px — pour y empiler trois champs (numéro, correcteur, type d'outil), et la
référence plaquette 20 à 30 % pour une chaîne du genre `CNGX 120716 T02020 LKT640 (κr 85°)`.
Avec `overflow:hidden` sur les cellules et `text-overflow:ellipsis` sur les entrées, tout était
tronqué : on ne pouvait pas relire ce qu'on venait de saisir.

Le problème de fond n'est pas la largeur, c'est la nature de l'objet : 15 colonnes pour 2 à 4
lignes, ce n'est pas un tableau, c'est un formulaire déguisé. Il est donc rendu comme un
formulaire.

- **Une fiche par outil** (`outilCarteHTML`), **un bloc par logement** (`logementBlocHTML`),
  chaque champ avec son libellé au-dessus et une largeur dimensionnée sur son contenu :
  `--oc-court` 110 px (correcteur), `--oc-moyen` 170 px (logement, code article),
  `--oc-large` 300 px minimum extensible (référence plaquette, type d'outil), `--oc-num` 96 px
  (valeurs numériques). Mesuré : la référence plaquette dispose de 505 px à 1440 px de large,
  contre ~200 px tronqués auparavant.
- **Champs groupés par nature** : Plaquette (prix, arêtes, charnière + durée de vie réelle),
  Conditions de coupe (Vc, f, κr, et rε/ap si Fr·Fa est actif, temps coupe/déplacement si le
  cycle détaillé l'est), Coût (€/arête, €/pièce, calculés, sur fond bleu et calés à droite).
- **Taille de saisie 11 → 14 px**, libellés 10 → 11 px.
- **Plus de `text-transform:uppercase` sur les libellés de champ** : Vc, f, κr, rε, ap sont des
  notations sensibles à la casse, elles s'affichaient « VC », « KR », « RE ». Les intitulés de
  groupe (mots ordinaires) restent en capitales.
- **Le tableau compact est conservé pour l'impression et le rapport client** — rien n'y est
  saisissable et la compacité y a du sens. La branche interactive de `logementRowHTML` a été
  supprimée plutôt que laissée en double entretien ; `outilRowsHTML` perd son paramètre
  `interactive`.
- Vérifié sans troncature de 820 à 1440 px de large (contrôle `scrollWidth > clientWidth` sur
  tous les champs, avec des valeurs longues réalistes).

### Ajouté — volume annuel invalide signalé
Un volume annuel négatif ou nul faisait renvoyer `null` à `volumeAnnuel()`, donc disparaître
silencieusement le bandeau de production, les gains en €/an, les heures machine et la
consommation annuelle de plaquettes. Le champ porte bien `min="0"`, mais rien n'empêche la
valeur d'arriver par un import — c'est exactement ce que le jeu de données de la revue externe
contenait. `volumeInvalideHTML()` affiche désormais un bandeau rouge nommant la référence, la
valeur fautive et le chemin pour la corriger, et précise que les chiffres ne valent pas zéro :
ils ne sont pas calculés. Rien n'est affiché tant que le champ est simplement vide.

### Tests
65/65 au vert. Contrôles complémentaires en session : saisie toujours enregistrée après
refonte (les gestionnaires sont liés aux classes et aux `data-*`, conservées), voie impression
produisant bien le tableau et aucune fiche, bandeau volume affiché pour −5000 et 0, absent
pour un champ vide et pour 200 000.

## [3.16.1] — 2026-09-05

Réglage du dosage de la fonction précédente : la fusion est prête, elle ne doit pas pour
autant s'imposer alors qu'une seule personne tient les saisies aujourd'hui.

### Modifié
- **« Remplacer tout » redevient le choix par défaut** de la fenêtre d'import (bouton primaire,
  placé en premier). C'est le geste que l'équipe connaît et le comportement correct tant qu'une
  seule personne saisit. « Fusionner » passe en action secondaire, disponible sans être
  proposée d'office.
- La note de version 3.16.0 (jamais diffusée, l'outil n'ayant pas été déployé) est corrigée en
  conséquence : elle présentait la fusion comme le choix recommandé.

### Ajouté
- **Explication au premier import** : un bloc dans la fenêtre d'import détaille ce que fait
  chaque option, le cas d'usage de chacune, et ce qui se passe quand l'outil ne peut pas
  trancher. Case **« Ne plus afficher cette explication »** (clé `spk_fusion_explication_masquee`,
  locale au poste comme celle des nouveautés) ; une fois cochée, le bloc se replie derrière un
  lien « Comment choisir ? » qui le redéploie — l'explication n'est jamais perdue, seulement
  rangée. Le choix lui-même n'est jamais masqué.

## [3.16.0] — 2026-09-05

Cinq chantiers issus d'une revue des marges d'amélioration réelles. La performance n'en fait
pas partie : l'historique et la sauvegarde dossier sont déjà throttlés à 5 min, la synthèse et
le backlog ne se recalculent que s'ils sont affichés, la saisie écrit la valeur sans
reconstruire l'écran. Le vrai point faible était le modèle d'échange de fichiers.

### Ajouté — import fusionnant (le chantier structurant)
`importData()` remplaçait tout l'arbre. À trois sur le même suivi, ça impose de travailler en
série : deux personnes saisissant en parallèle sur deux OP différents, le fichier importé en
dernier écrasait le travail de l'autre. Le compteur de révision prévenait, il n'empêchait rien.

- Nouveau champ `modifieLe` (ISO) par essai, posé à chaque écriture de champ d'essai ou de
  prélèvement, à la création, et à l'ajout/suppression de prélèvements, photos ou relevés
  Marposs (`toucherEssai()`).
- `fusionnerLignes()` — règle annoncée à l'utilisateur avant validation :
  - **structure** (lignes, références, OP, scénarios, outils, logements, conditions de coupe,
    options) : ce qui existe localement est conservé, ce qui n'existe que dans le fichier reçu
    est ajouté. Une fusion n'écrase jamais un réglage local.
  - **essais** : niveau d'arbitrage. Un essai présent des deux côtés est remplacé **en bloc**
    par la version au `modifieLe` le plus récent. Jamais champ par champ — deux moitiés
    d'essais recollées produiraient une mesure qui n'a jamais existé.
  - **conflit** (dates identiques, ou absentes d'un côté) : la version locale est conservée et
    listée nommément. Les fichiers antérieurs à cette version n'ont pas d'horodatage : leurs
    essais divergents remontent donc en conflit tant que chacun n'a pas ré-exporté une fois.
    C'est volontaire — mieux vaut signaler que deviner.
- Panneau de choix `#importPanel` (Fusionner / Remplacer tout), chaque option accompagnée de
  sa conséquence écrite, puis rapport de fusion : ajoutés, mis à jour, conservés, conflits.
- Une fusion incrémente la révision (`max + 1`) et repasse le fichier en « non exporté » : le
  résultat n'existe encore sur aucun autre poste.

### Ajouté — prévision de sortie de tolérance
`previsionUsure()` : régression linéaire des prélèvements (n° de pièce → cote), extrapolée
jusqu'à la tolérance, affichée en pastille à côté de la progression du logement. Rouge si la
sortie est prévue avant la charnière visée. Garde-fous : ≥ 4 points et ≥ 3 n° de pièce
distincts, pente positive, R² ≥ 0,35, incertitude à ± 2 erreurs-types toujours affichée. En
dessous : « tendance stable », « tendance non lisible » ou « déjà hors tol. » — jamais un
chiffre non défendable.

### Ajouté — dispersion par équipe
Les champs `equipe` et `redigePar` ne servaient qu'à tracer. Croisés avec la conformité des
prélèvements, ils donnent un tableau équipe × scénario du taux hors tolérance dans la vue de
synthèse. Badge « écart » au-delà de 5 points au-dessus de la moyenne des autres équipes, à
partir de 10 prélèvements évalués ; en dessous, la taille d'échantillon est affichée (n=…).
Le bloc n'apparaît qu'à partir de 2 équipes renseignées.

### Ajouté — mode consultation
Bouton cadenas : `body.locked` neutralise la saisie (champs en lecture seule, boutons d'action
masqués) sans rien cacher de l'information. L'outil tourne sur un écran partagé en tactile où
tout était éditable en permanence. Le mode atelier reste saisissable — on y entre
volontairement, en plein écran. État local au poste (`localStorage`), jamais exporté,
ré-appliqué après chaque rendu.

### Modifié
- Logo ré-encodé de 1796 px à 600 px de large (affiché en 52 px, ~14 mm à 300 dpi en
  impression) : 118 ko → 37 ko en base64. Fichier total 750 → 669 ko.

### Tests
16 cas ajoutés à `runTests()` (prévision d'usure : extrapolation, seuil de points, cote
stable, déjà hors tolérance ; fusion : reçu plus récent, local plus récent, conflit sans date,
fichiers identiques, essai ajouté, structure ajoutée sans écrasement). **65/65 au vert.**

## [3.15.0] — 2026-09-04

Refonte visuelle « blocs pleins » : contraste et lisibilité. Aucun changement de structure de
données, de calcul ni de format de fichier — les `.json` existants se rechargent à l'identique.

### Constat de départ
Mesure des contrastes de l'interface existante, plutôt qu'un jugement à l'œil :

| élément | avant | après | seuil AA |
|---|---|---|---|
| libellés (`--ink-faint`, #888 → #5a6470) | **3,5:1** | **6,0:1** | 4,5:1 |
| texte secondaire (`--ink-soft`, #555 → #454e59) | 7,5:1 | 8,4:1 | 4,5:1 |
| texte principal (`--ink`, #1a1a1a → #12161b) | 17,4:1 | 18,2:1 | 4,5:1 |
| bordures (`--border`, #e5e5e5 → #ccd1d8) | **1,3:1** | 1,5:1, ombre floue supprimée | 3:1 (non-textuel) |
| bleu SPK (#1b5ea6 → #0d47a1) | 6,6:1 | 8,6:1 | 4,5:1 |
| rouge (#e2001a → #c50018) | 4,6:1 | 6,2:1 | 4,5:1 |

Sur les aplats : blanc sur bleu 8,6:1, blanc sur vert 7,1:1, gain/perte éclaircis 5,5 et 5,1:1.
La bordure reste sous 3:1 par choix — elle ne porte aucune information à elle seule, elle
délimite ; ce sont l'ombre floue et le manque d'écart de fond qui la rendaient inopérante.

Le point noir n'était pas la palette mais les libellés : l'outil est fait presque entièrement
de petits libellés mono en majuscules (9,5 à 12 px), tous sous le seuil AA. Les bordures
`#e5e5e5`, noyées dans une ombre floue large, ne séparaient rien non plus.

### Modifié
- **Palette recalibrée** — `--ink` #12161b, `--ink-soft` #454e59, `--ink-faint` #5a6470,
  `--border` #ccd1d8, bleu #0d47a1, vert #12653a, ambre #8a4300, rouge #c50018.
- **Hiérarchie par aplats** — la rangée de chiffres clés d'un scénario (`.scenario-foot`), les
  KPI du tableau de bord et le bandeau de production annuelle passent sur fond de couleur
  pleine, chiffres en blanc. La cellule de validation part en vert : c'est le seul indicateur
  d'avancement de campagne, il ne se confond plus avec les coûts.
- **Bandeau de tête** en aplat noir, logo SPK posé sur une plaque blanche (le PNG a une encre
  sombre, il disparaissait sur fond noir).
- **Ombres** — `--shadow-card` réduit à un filet de 1 px : sur fond clair, un halo large et pâle
  ne sépare rien, il brouille l'arête de la carte. La profondeur vient désormais de la bordure.
- **Typographie** — Manrope (titres, gros chiffres) et Public Sans (texte courant, UI)
  remplacent Archivo et Open Sans, embarquées en base64 comme les précédentes (+66 ko, aucun
  appel réseau, fonctionnement hors ligne préservé). Public Sans est dessinée pour les petites
  tailles à l'écran, là où Open Sans se brouillait sous 12 px. IBM Plex Mono reste sur les
  chiffres.
- **Mode sombre** refait avec la même logique au lieu d'une inversion approximative : fond
  #0f1317, surfaces #181d22, texte #f1f4f7, accents remontés en tons clairs. Nouveau token
  `--on-accent` (encre posée sur un badge plein) : blanc en clair, sombre en mode nuit — les
  badges vert/rouge/ambre y étaient auparavant en texte blanc sur fond clair.
- **PDF et rapport client** alignés sur la même palette.

### Impression
- Les aplats pleins restent à l'écran : en `@media print`, les tokens `--fill*` basculent sur
  fond blanc (chiffres en bleu, cellule de validation en blanc, filets de séparation gris).
  Un tirage papier de plusieurs scénarios aurait sinon consommé beaucoup de toner pour rien.
  Comme les couleurs posées en style inline par le JS (gain/perte annuels, avertissements de
  cycle) passent par ces mêmes tokens, elles suivent automatiquement.

## [3.14.1] — 2026-09-04

Derniers constats cosmétiques de la revue Hermes.

### Corrigé
- `migrationTolerance` était une variable globale mutable jamais réinitialisée ; rendue
  locale à `loadAll()`.
- Champs numériques d'Options : chaque frappe déclenchait une sauvegarde + un rendu
  complets — léger debounce (150 ms) ajouté sur la saisie continue, `change` (blur/Entrée)
  reste instantané.
- Aucun signal quand la permission du dossier photos est révoquée en cours de session
  (paramètres du navigateur) — détectée à la prochaine lecture de photo, le statut
  « dossier non connecté » s'affiche automatiquement.
- Badges gris (`—`, compteurs) trop peu contrastés en éclairage d'atelier variable —
  couleur de texte plus soutenue.
- Badge « Charnière seule » raccourci en « 🔓 Charnière » avec info-bulle, prenait trop de
  place dans le tableau des prélèvements.
- Lightbox d'image : ajout d'un rappel « Cliquer ou Échap pour fermer », visible 2,5 s puis
  estompé (respecte `prefers-reduced-motion`).
- Menu **•••** : Échap ne le fermait pas (seul un clic à l'extérieur le faisait).
- Messages du module « Détailler le temps de cycle par logement » : couleurs factorisées
  en classes CSS sémantiques (`.cycle-detail-ok` / `.cycle-detail-ko`) plutôt qu'en style
  inline.

### Non retenu
- Pagination de la vue de synthèse au-delà de N scénarios (3.9) — Hermes notait lui-même
  que c'est à vérifier « en charge réelle » ; pas de cas concret aujourd'hui pour
  dimensionner correctement un seuil, laissé de côté pour éviter d'ajouter de la
  complexité sans bénéfice mesuré.
- `prompt()` natif pour les saisies rapides (2.11) — Hermes concluait lui-même qu'aucun
  changement n'était nécessaire en l'état.

## [3.14.0] — 2026-09-03

Suite de la revue de code externe (Hermes) : constats de cohérence et d'UI/UX restants.

### Corrigé — confidentialité (le plus important de ce lot)
- **Les données de démarrage étaient des données réelles.** `defaultScenarios` /
  `defaultLignes` (utilisés au tout premier lancement et après « Réinitialiser ») reprenaient
  exactement les références plaquette, numéros d'outil et mesures d'un export réel — donc
  versionnées sur GitHub et déployées sur l'URL publique Surge à chaque mise à jour, en
  contradiction directe avec la politique de confidentialité du README (« les données
  d'essais réelles ne sont jamais versionnées ici »). Remplacées par un jeu de données
  entièrement fictif, préfixé « [Exemple] » pour qu'il ne puisse plus être confondu avec un
  vrai projet.

### Corrigé — cohérence
- **Marge de charnière (0,5 pièce) codée en dur** — exposée en réglage `Options` :
  « Marge avant d'afficher un écart de charnière (pièces) », toujours visible, par défaut
  0,5.
- **Facteur de charnière au seuil de bascule** — formulation clarifiée : « Multiplier vos
  charnières par ×X pour revenir à l'équilibre » au lieu d'une simple valeur.
- **Champs de traçabilité (v3.11) sans valeur par défaut** — `redigePar`, `dateFin`,
  `heureFin`, `programme`, `programmeGauche`, `programmeDroit` sur un essai, et `legende` /
  `crop` / `annotations` sur une photo, étaient `undefined` plutôt que vides sur un JSON
  antérieur à ces versions. Ajoutés à la normalisation des essais/photos.

### Corrigé — UI/UX
- **Vocabulaire « Référence » à trois sens** — le badge de scénario « ★ Référence »
  (comparaison) était visible juste à côté de l'onglet « Référence disque » (la pièce) :
  renommé « ★ Scénario réf. », avec info-bulle.
- **Formule du coût machine non explicitée** — la case « Intégrer le temps machine au coût
  pièce » affiche maintenant la formule littérale : coût machine/pièce = coût horaire (€/h) ×
  temps de cycle (s) / 3 600.
- **Placeholder « Nom(s) » trop vague sur « Rédigé par »** — précise maintenant qu'il s'agit
  du rédacteur du rapport (pas forcément l'opérateur machine), et suggère le nom d'auteur
  déjà enregistré dans l'outil.
- **Éditeur d'annotation photo, fermeture sans confirmation** — Échap ou un clic en dehors du
  panneau perdait silencieusement le rognage/les formes/la légende non enregistrés ;
  confirmation ajoutée, uniquement s'il y a réellement quelque chose de non enregistré à
  perdre.
- **Éditeur d'annotation photo, cibles tactiles trop petites** — palette de couleurs et
  boutons d'outils agrandis sur écran tactile (`pointer: coarse`), comme le reste de l'outil.
- **Statuts « Validé » et « En série » trop proches visuellement** — les deux étaient en
  vert ; « En série » passe au bleu (déjà utilisé ailleurs pour ce même statut), pour
  distinguer d'un coup d'œil « essai confirmé » et « tourne en production ».
- **Message harmonisé** entre le rappel permanent d'Options et le statut par scénario du
  module « Détailler le temps de cycle par logement », qui pouvaient légèrement diverger
  dans leur formulation.

## [3.13.0] — 2026-09-03

Suite à une revue de code externe (Hermes) du fichier dans son ensemble — cohérence,
robustesse, UI/UX. 2 constats bloquants et 7 gênants de robustesse corrigés ici ; les
constats de cohérence et d'UI/UX restants sont notés pour un prochain lot.

### Corrigé (bloquants)
- **Temps de cycle de la baseline non éditable en pratique** — `recomputeCycles()` force
  `cycle = 100` sur le scénario de référence à chaque chargement (par construction : c'est
  le point zéro de l'indice), mais le champ restait affiché comme un `<input>` éditable.
  Une valeur saisie par erreur (constaté sur un export réel : `54,4` au lieu de `100`)
  disparaissait silencieusement au rechargement suivant. Le champ est maintenant en
  lecture seule sur la baseline, avec une info-bulle expliquant pourquoi.
- **Éditeur d'annotation photo : sauvegarde silencieusement bloquée** — si le stockage
  navigateur est plein au moment d'enregistrer une annotation, l'annotation reste
  correcte en mémoire pour la session mais n'est plus persistée ; rien ne le signalait.
  Un message prévient désormais l'utilisateur et l'invite à exporter le suivi.

### Corrigé (robustesse)
- **Fuite mémoire sur les photos** — les URLs temporaires (`ObjectURL`) créées pour
  afficher une miniature, ouvrir l'éditeur d'annotation ou la lightbox n'étaient jamais
  libérées. Révoquées maintenant dès que l'image correspondante est décodée.
- **Compression d'image à l'ajout d'une photo** — passait par un data URL base64
  intermédiaire (pic mémoire ~1,3× la taille du fichier, sensible sur mobile/mauvais
  réseau) ; utilise directement un `ObjectURL`.
- **Migration d'un ancien fichier de suivi non persistée** — la conversion vers le format
  Ligne/Référence/OP n'était sauvegardée qu'à la première saisie ultérieure ; elle l'est
  désormais immédiatement, sans attendre une action de l'utilisateur.
- **Éditeur d'annotation, touche Suppr** — promise dans le message d'aide pour effacer la
  forme sélectionnée, mais jamais câblée. Fonctionne maintenant (Suppr ou Retour arrière).
- **Éditeur d'annotation, bouton « Valider le rognage »** — restait actif même sans zone
  tracée, sans retour visible. Grisé tant qu'aucune zone valide n'est en cours, avec une
  info-bulle explicative.
- **Avertissement manquant si les Vc/f de la référence sont vides** — dans ce cas,
  l'indice de cycle des autres scénarios n'est plus recalculé automatiquement lors d'un
  changement de conditions de coupe, sans que rien ne le signale. Un message ambré
  l'indique désormais sous le temps de cycle des scénarios concernés.

### Non retenu de la revue
- Le constat sur `writeBackupToFolder()` (2.4) supposait qu'un échec de sauvegarde du
  dossier local pouvait faire croire à un échec de `localStorage`. Vérifié : la fonction
  encapsule déjà sa propre gestion d'erreur silencieuse et ne peut pas remonter jusqu'au
  `catch` de `saveData()` — le scénario décrit n'est pas reproductible en l'état.

## [3.12.0] — 2026-09-03

### Ajouté
- **Éditeur d'annotation de photo** (bouton ✎ sur chaque miniature, bloc Photos d'un
  essai) : rognage, flèches droites, flèches courbes (avec poignée de courbure
  ajustable), rectangles et ellipses de sélection, texte flottant, palette de 7
  couleurs + sélecteur personnalisé. Sélection/déplacement/suppression des formes,
  annuler la dernière forme.
  - Rognage et formes sont stockés en coordonnées vectorielles (fractions de l'image
    d'origine), jamais appliqués aux pixels du fichier — non destructif, ré-éditable
    à volonté, JSON toujours léger.
  - Cliquer sur une miniature ouvre désormais un aperçu plein écran recomposé
    (rognage + annotations), au lieu de la photo brute.

## [3.11.0] — 2026-09-03

Champs manquants identifiés en comparant un rapport d'essai papier réel (Matis) au modèle
de données de l'outil : rédaction, fin d'essai, programme CNC, correcteur, type d'outil,
légende de photo.

### Ajouté
- **Champs par essai** : rédigé par, fin d'essai (date + heure — en plus de la date de
  début déjà présente), nom du programme CNC (deux champs Gauche/Droit sur EMAG 1, un
  champ unique sinon). Repris dans le rapport d'essai généré.
- **Champs par outil** : correcteur (n° de jauge/offset machine), type d'outil (description
  libre, ex. « Foret carbure monobloc à goujure droite »). Repris dans le rapport d'essai
  et le rapport de validation.
- **Légende par photo d'essai** (ex. « Usure du foret après 4212 pièces (cumul) »).

## [3.10.0] — 2026-09-02

### Ajouté
- **Module « Détailler le temps de cycle par logement »** (Options → module de calcul) :
  au lieu d'un indice base 100 unique pour tout le scénario, chaque logement (bol, piste...)
  peut recevoir un temps de coupe et un temps de déplacement mesurés machine. Corrige
  l'incohérence de l'indice global sur les scénarios mixtes (un seul logement change de
  plaquette) — voir la discussion du 2026-09-02 : un ratio unique appliqué à tout le cycle
  coupant mélange deux réalités différentes dès qu'un seul côté de l'outil change.
  - Deux colonnes ajoutées à « Composition du scénario » quand le module est actif :
    Temps coupe (s) / Temps déplacement (s), par logement.
  - Le calcul détaillé ne remplace l'indice base 100 que si **tous** les logements du
    scénario sont renseignés ; sinon retombée automatique et silencieuse sur l'indice,
    signalée par un statut explicite sous le tableau (✓ complet / ⚠ incomplet, X/Y).
  - Message permanent dans Options prévenant que ces temps sont un relevé terrain réel,
    pas une estimation, et invitant à en discuter avant d'activer le module sur une
    référence.
- **Fiche outil (PDF ou image) par OP**, dans Options : illustre les n° d'outils et
  trajectoires par logement, pour aider à la saisie des temps ci-dessus. Ouverture en
  plein écran (image) ou nouvel onglet (PDF), retrait possible. Stockée avec l'OP,
  voyage donc avec l'export/import JSON.

## [3.9.5] — 2026-09-02

### Corrigé
- **Régression critique introduite en 3.9.1** : la lightbox d'agrandissement d'image
  (`.img-lightbox`) déclarait `display:flex` dans sa règle CSS de base, ce qui court-circuite
  l'attribut HTML `hidden` — une règle d'auteur avec `display` prime toujours sur le style
  agent-utilisateur par défaut `[hidden]{display:none}`, quel que soit l'ordre dans la feuille
  de style. Résultat : le voile plein écran (fond sombre à 85 % d'opacité) restait affiché en
  permanence dès le chargement de la page, rendant l'outil quasi illisible. Ajout de la règle
  `.img-lightbox[hidden]{display:none;}`, sur le modèle déjà suivi ailleurs dans le fichier
  (`.toolbar-more[hidden]`, `.atelier[hidden]`).

## [3.9.4] — 2026-09-02

### Ajouté
- **Rappel permanent dans Options**, sous « Intégrer le temps machine au coût pièce » :
  explique que le temps de cycle ne pèse dans le gain annuel que si les quatre conditions
  sont réunies — « Afficher le temps de cycle en secondes » ET « Intégrer le temps machine
  au coût pièce » cochés, coût horaire de la ligne renseigné, temps de cycle réel de la
  référence renseigné. Complète l'avertissement conditionnel ajouté en 3.9.3 (celui-ci
  n'apparaît qu'une fois le cycle déjà modifié).

## [3.9.3] — 2026-09-02

### Changé
- **Étiquette du champ « Temps de cycle »** — précise désormais « indice base 100 » pour
  ne plus le confondre avec la ligne de temps réel en secondes affichée en dessous
  (module « Afficher le temps de cycle en secondes »).

### Ajouté
- **Avertissement sous « Gain annuel »** quand le temps de cycle d'un scénario diffère de
  la référence sans que le module « Intégrer le temps machine au coût pièce » soit activé :
  le gain affiché ignore alors volontairement cet écart. Sans ce message, modifier le cycle
  sans effet sur le gain pouvait passer pour un bug de calcul.

## [3.9.2] — 2026-09-02

### Ajouté
- **Agrandissement plein écran des captures jointes à une suggestion** (menu `•••` →
  **Suggestions**) — un clic sur la miniature l'affiche en grand sur fond sombre (clic ou
  Échap pour refermer). Les captures d'écran collées par Matis/Arthur étaient jusque-là
  cantonnées à 220×160 px et illisibles.
- **Rappel dans la fenêtre « Nouveautés »** : quand une évolution correspond à une
  suggestion notée par ailleurs, un message invite à repasser son statut sur **Traité**
  dans le backlog — sans ça, les suggestions déjà traitées restaient marquées « Nouveau ».

## [3.9.1] — 2026-09-02

### Corrigé
- **Tuile « Production annuelle » chevauchant le tableau de composition** — quand le volume
  annuel était renseigné pour une référence, la tuile flottante s'imposait à côté du tableau
  « Composition du scénario » au lieu de passer au-dessus, ce qui écrasait ses colonnes
  (référence plaquette notamment) et rendait le contenu illisible. Le tableau se place
  désormais toujours sous la tuile, quelle que soit la largeur d'écran.

## [3.9.0] — 2026-09-02

Trois critères de validation de la durée de vie, au lieu d'un seul.

### Ajouté
- **Usure visuelle de la plaquette** — statut par prélèvement (OK / usure limite / à changer),
  saisi dans le tableau de l'essai comme en mode atelier. « À changer » rend le prélèvement
  non conforme même si la cote mesurée est dans la tolérance : un outil visiblement usé n'est
  pas rattrapé par une mesure encore bonne.
- **2e critère de tolérance, optionnel par scénario** (bloc « Essais ») — typiquement un état
  de surface (Ra/Rz/Rt) en plus de la tolérance dimensionnelle déjà suivie (battement,
  parallélisme, diamètre...). Les deux doivent être respectés pour qu'un prélèvement soit
  conforme. Une case vide sur le 2e critère ne fait jamais échouer un prélèvement par ailleurs
  bon — pas de reclassement rétroactif des essais existants.
- Le motif « hors tolérance » affiché sur les essais est désormais précis (cote hors tolérance,
  2e critère hors tolérance, ou usure) au lieu d'un seul libellé générique.

### Changé
- Table de prélèvements, mode atelier, rapports de validation et d'essai (HTML autonomes),
  export CSV : tous reprennent les deux nouveaux critères.

## [3.8.0] — 2026-09-02

L'outil annonce lui-même ses évolutions, et le menu d'aide rattrape les fonctionnalités
ajoutées depuis la v3.4.

### Ajouté
- **Fenêtre « Nouveautés »**, ouverte automatiquement quand la version affichée diffère de
  la dernière vue sur ce poste. Objectif : ne plus avoir à envoyer un e-mail à chaque mise
  à jour. Fermer la fenêtre vaut « lu » — elle ne revient qu'à la version suivante.
  Reste consultable à tout moment via le menu `•••` → **Nouveautés**.
  Une case « ne plus afficher » est proposée en secours ; la cocher revient à ne plus être
  prévenu des évolutions suivantes, d'où le choix de ne pas en faire le fonctionnement
  normal. Aucune version enregistrée = la fenêtre s'affiche, ce qui garantit que le premier
  déploiement de la fonction atteint bien tout le monde.
- Le contenu est maintenu dans la constante `NOUVEAUTES`, en tête du bloc correspondant :
  **3 à 5 points par version, lisibles par quelqu'un qui n'a pas suivi le développement**.
  Le CHANGELOG reste trop technique pour cet usage, les deux ne se remplacent pas.

### Changé
- **Menu « Comment ça marche » complété.** Cinq sections nouvelles : coût complet et ses
  modules d'Options (dont la part réellement coupante du cycle), seuil de bascule, charnière
  visée face à la charnière atteinte, statuts de scénario, tableau de bord. La section
  « Méthode de calcul » précise désormais que le coût plaquette seul est le comportement par
  défaut, pas la vérité complète.
- « Bon à savoir » mentionne les essais repliés en tuiles, le scénario ouvert placé en tête
  de liste avec son numéro stable, et le rôle du graphique de tendance — montrer la
  répétabilité entre essais, pas détailler un essai isolé.

## [3.7.0] — 2026-09-02

Retour à l'habillage d'origine et réorganisation de l'écran de travail autour du scénario
ouvert. Les évolutions fonctionnelles des versions 3.1 à 3.6 sont toutes conservées.

### Retiré
- **La refonte visuelle v3.0/v4.0 et son toggle de comparaison.** Le rail sombre, l'en-tête
  en carte et le verdict retravaillé sont supprimés : retour au visuel v2.5. Avec eux
  partent le bouton de bascule, son script d'amorçage et les deux blocs CSS conditionnés —
  environ 16 Ko de code mort en moins.

### Changé
- **Tuiles de scénario réorganisées.** Le scénario ouvert passe en tête de liste, sur toute
  la largeur, légèrement teinté en bleu, avec ses chiffres étalés sur une rangée. Les autres
  restent en dessous, en format condensé (nom, statut, coût/pièce, gain annuel).
  La tuile ouverte est sortie de la grille : quand elle la traversait, celle-ci créait autant
  de colonnes qu'elle pouvait en tenir et écrasait les autres tuiles à 218 px de large.
- **Numéro et couleur de statut sur chaque tuile.** Le numéro est celui de la création : il
  ne bouge pas quand l'ordre d'affichage change, pour qu'on puisse dire « regarde le 3 ». Un
  filet vertical donne le statut sans avoir à lire — gris à l'étude, ambre en essai, vert
  validé, bleu en série, rouge abandonné.
- **La composition du scénario remonte** juste après les chiffres clés, et s'affiche
  **dépliée par défaut** : c'est la fiche d'identité du scénario (outils, logements,
  plaquettes, pièces détachées, conditions de coupe). Elle reste repliable une fois la
  campagne lancée, et ce choix survit aux re-rendus.
  Nouvel ordre : tuiles → verdict → chiffres clés → composition → graphique → essais → rebut.
- **Production annuelle en évidence**, en gros et en bleu, en haut à droite de la composition
  dès que le module Volume annuel est actif. C'est le multiplicateur de tous les autres
  chiffres, il ne devait pas se chercher.

### Corrigé
- **Séparateur de milliers invisible.** Le français sépare les milliers par U+202F (espace
  fine insécable), et Archivo ne dessine pas ce caractère : « 200 000 » s'affichait quasi
  collé, l'espace tombant à 1,6 px au lieu de 9,6. Tous les nombres à quatre chiffres et plus
  étaient concernés. Les espaces fines sont désormais ramenées à l'espace insécable ordinaire
  U+00A0, présente dans toutes les polices — largeur correcte, et les nombres ne se coupent
  toujours pas en fin de ligne.

## [3.6.0] — 2026-09-02

Fiabilisation : plus aucun appel réseau, et le moteur économique est désormais couvert par
des tests. Rien ne change à l'usage.

### Corrigé
- **Le rapport d'essai exporté n'appelle plus Google Fonts.** Son pied de page affirme
  « Document 100 % local, aucune donnée transmise » alors qu'il chargeait trois polices
  depuis Google à chaque ouverture — contradiction gênante pour un document envoyé à
  Stellantis, et requête susceptible d'être bloquée par le proxy du site. Les piles de
  polices du rapport retombent sur Arial / Consolas, présentes partout.

### Ajouté
- **49 tests du moteur économique**, embarqués dans le fichier et inertes par défaut : ils ne
  s'exécutent qu'en ouvrant l'outil avec `#tests` à la fin de l'adresse, ou en tapant
  `runTests()` dans la console. Ils travaillent sur des données fabriquées et restaurent
  l'état réel ensuite — aucune sauvegarde n'est déclenchée, les données de travail ne sont
  jamais touchées.
  Couverture : `posCost`, `pieceCost`, `scenarioCost`, `recomputeCycles`, `cycleSecondes`
  (formule part coupante, cas 0 / 50 / 100 %), `coutMachinePiece`, `coutRebutPiece`,
  `coutPiecesDetachees`, `coutsDetail` (propagation des `null`, drapeau `multiPoste`),
  `charniereReelle` (borne inférieure, sortie de tolérance, échec au premier prélèvement),
  `ecartsCharniere`, `seuilBascule`, `bilanAnnuel`, `fmtEuroCourt`.
  Vérifié en remettant l'ancienne formule de cycle fausse : 5 tests tombent, dont ceux de
  `coutMachinePiece`, `coutsDetail` et `bilanAnnuel` — la cascade est bien détectée.

### Changé
- **Polices embarquées en base64, plus aucune dépendance réseau.** L'outil s'ouvre à
  l'identique hors ligne, depuis une clé USB, ou derrière un proxy d'usine. Fin du blocage
  de rendu pendant le délai d'attente réseau quand le poste atelier n'a pas Internet.
  Coût : le fichier passe de 479 à 600 Ko.
  Deux optimisations pour en arriver là plutôt qu'aux 510 Ko d'un embarquement naïf :
  Archivo et Open Sans sont des **polices variables** — Google sert le même fichier pour
  chaque graisse, les embarquer une par graisse aurait dupliqué 200 Ko à l'identique ; une
  seule face couvre désormais toute la plage (`font-weight: 600 800` et `300 700`). Et
  chaque police est **sous-ensemblée** au latin complet plus les symboles de l'interface
  (≤ ★ ✓ → κ €). Un caractère hors de ce jeu retombe sur la pile système déclarée derrière,
  sans casser la mise en page.

## [3.5.0] — 2026-09-01

Coût complet et pilotage du portefeuille d'optimisations. L'outil ne comparait que le prix
des plaquettes : un scénario deux fois plus lent mais moins cher en outil ressortait gagnant
alors qu'il pouvait être largement perdant. Tous les modules ci-dessous sont **désactivés par
défaut** — rien ne change tant qu'on ne les active pas dans Options, et une fois activés ils
prennent leur place de façon permanente.

### Ajouté — chaîne économique
- **Temps machine dans le coût pièce.** Le coût horaire de la ligne (saisi via l'icône ⚙ de
  l'onglet de ligne, existant depuis la v3.2) est enfin utilisé : il convertit l'écart de temps
  de cycle en euros. Sur les données OP10 actuelles, la céramique intégrale passe de « −93,4 % »
  à **+25 % de coût réel**, soit une perte de l'ordre de 37 k€/an à 200 000 disques.
- **Part réellement coupante du cycle (%).** L'indice de cycle vaut `100 × (Vc·f réf)/(Vc·f)` :
  c'est un indice de *temps coupant*, pas de cycle complet. L'appliquer au cycle entier
  surestimait la pénalité, puisque chargement, approche et retrait ne bougent pas avec Vc/f.
  On ne fait donc varier que la part déclarée comme coupante.
- **Pièces détachées par porte-outil** — cales, vis, corps d'outil, brides, chacune amortie sur
  sa propre charnière de remplacement et ajoutée au coût pièce.
- **Volume annuel de production**, réglé par référence disque : convertit chaque écart en €/an
  et en heures machine/an, et affiche la **consommation annuelle de plaquettes** par logement.
- **Décomposition du coût** — barre empilée + légende sous le chiffre de tête (plaquettes /
  pièces détachées / temps machine / rebut). Un chiffre agrégé seul n'est pas défendable.
- **Seuil de bascule** — « X s de cycle maximum pour rester gagnant », et le facteur à appliquer
  aux charnières pour revenir à l'équilibre. Quand le temps machine dépasse à lui seul la
  référence entière, l'outil le dit explicitement : aucune durée de vie ne compensera.

### Ajouté — suivi et pilotage
- **Charnière réellement atteinte**, calculée à partir des essais : dernier prélèvement conforme
  avant sortie de tolérance, moyenné sur les essais. Affichée sous la charnière visée dans le
  tableau plaquettes. Tant qu'aucun essai n'est sorti de tolérance, la valeur est présentée
  comme une borne inférieure (`≥ 150`) — les essais s'arrêtent à la cible, on ne sait rien
  au-delà. Dès qu'un essai lâche avant la cible, un encart signale l'écart et recalcule le coût
  réel correspondant.
- **Statut de vie d'un scénario** : à l'étude / en essai / validé / en série / abandonné, avec
  motif obligatoire à l'abandon et date de décision automatique. « Validé » et « en série » ne
  se confondent plus, et une impasse documentée évite qu'on la reparcoure deux ans plus tard.
- **Tableau de bord multi-lignes** (menu `•••`) : toutes les lignes, références et OP du fichier
  dans une seule vue — avancement des essais, coût pièce, écart, gain annuel, et en tête le
  cumul du gain acquis (scénarios en série) vs à déployer (validés pas encore passés en série).

### Changé
- Dès que plusieurs postes de coût sont actifs, **le coût total devient le chiffre de tête**
  partout : verdict, pied de scénario, liste des scénarios dans le rail, vue de synthèse et
  rapport de validation. Le coût plaquette reste affiché, en sous-ligne. Objectif : que le rail
  n'annonce jamais −46 % pendant que la fiche ouverte affiche +33 %.
- Le **rapport de validation** envoyé au client reprend le coût complet, la répartition
  plaquettes / temps machine et le gain annuel — c'est le document qui engage, il ne pouvait pas
  continuer à ne chiffrer que l'outil.
- La vue de synthèse ajoute une ligne « statut du scénario » et une ligne « gain annuel ».
- Le pied de scénario passe en grille auto-adaptative : il accueille le nombre de cellules
  correspondant aux modules actifs, sans mise en page figée à 4 ou 5 colonnes.

## [3.4.0] — 2026-08-30

Rapport par essai + message de divergence explicite.

### Ajouté
- **Rapport de l'essai** : bouton dans chaque essai qui génère un rapport HTML autonome
  dédié à cet essai — interlocuteurs (site, contacts Stellantis et CeramTec), but de
  l'essai, plaquettes utilisées (référence, Vc, f, charnière), tableau des prélèvements
  avec statut, observations. Mise en page reprenant les tokens du design system SPK
  (Archivo/IBM Plex Mono, bleu/rouge de la charte, logo).
- **But de l'essai** : nouveau champ libre par essai (bandeau bleu, à côté des
  observations), repris dans le rapport ci-dessus.
- La référence plaquette est désormais figée dans l'instantané de l'essai à sa création
  (elle ne l'était pas avant, seuls Vc/f/charnière l'étaient) — nécessaire pour que le
  rapport reste exact même si la référence change plus tard dans le scénario. Pour les
  essais déjà existants qui n'ont pas cette valeur figée, le rapport retombe sur la
  référence actuelle du scénario (meilleur effort).

### Changé
- **Message « le scénario a été modifié depuis »** : disait qu'un écart existait sans dire
  lequel. Indique maintenant précisément quoi (ex. « T513.1 · Piste — Vc 900→950, f
  0.5→0.45 ») avant de proposer d'aligner l'essai sur le scénario.

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
