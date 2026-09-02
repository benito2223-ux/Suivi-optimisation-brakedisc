# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donnée à part).

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
