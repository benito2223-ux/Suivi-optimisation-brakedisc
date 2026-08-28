STELLANTIS SEPT FONS — OP10 EBAUCHE DISQUE DE FREIN EN-GJL-250
DV 356x26 RPI — EMAG 1 — Amelioration Process
Dossier de suivi — mis a jour le 27/08/2026

Interlocuteurs Stellantis : Matis Hernu, Arthur Alves
Interlocuteur CeramTec    : Benjamin Rouquette

===============================================================
DERNIER ETAT
===============================================================

Essai du jour (26/08/2026) VALIDE sur T513.1 :
  Vc = 500 m/min, f = 0,35 mm/rev, G96
  -> battement < 0,10 mm (tol 0,12), 150 pieces/arete (x2 vs CBN a 75 p),
     usure reguliere, pas d'entaille.

Compte-rendu complet publie : compte_rendu_OP10.html
  (analyse thermique K, analyse vibratoire/lobes, duree de vie,
   economie CBN vs ceramique LKT640, plan d'essai)

===============================================================
DECISIONS PRISES
===============================================================

1. K = Vc x f x sin(kappa_r) confirme comme indice thermique commun :
   174 (1/3 piste actuel) = 174 (essai du jour) ; 448 (2/3 piste, nominal).
   L'essai de demain (Vc700/f0,35 -> K=244) tombe dans cet intervalle
   deja valide en production -> feu vert thermique.

2. Hypothese lobe de vibration retenue comme co-cause probable du gain
   de battement (G96 500 m/min balaie 447-538 tr/min, tres different du
   684-880 tr/min du process actuel) -> a trancher par essai G97
   dedie (878 tr/min +/- 8%), pas seulement par l'effet ceramique.

3. Economie : ceramique integrale (LKT640 aux 2 positions) ramene le
   cout outil/piece de 0,127 EUR a 0,008 EUR (-93%). Scenario mixte
   T50013 (bol CBN + piste ceramique) : 0,067 EUR (-47%).

4. OUTIL DE SUIVI "bilan_economique.html" — choix du 26/08 :
   fonctionnement 100% LOCAL, aucune donnee envoyee sur internet.
   Sauvegarde auto dans le navigateur + bouton "Exporter le suivi"
   (fichier .json horodate) pour archivage et echange par e-mail.
   Bouton "Importer" pour recharger un fichier recu.
   Raison : confidentialite des donnees Stellantis (prix plaquettes,
   parametres process) — pas d'hebergement tiers.
   REGLE D'USAGE : un seul detenteur du fichier maitre a la fois,
   sinon deux copies divergent sans fusion possible.

   Structure de saisie : SCENARIO > ESSAI > PRELEVEMENT.
   Un essai = plusieurs prelevements sur la longueur de la charniere.
   Essai conforme = charniere atteinte ET aucun prelevement hors tol.
   Scenario valide = N essais conformes (N editable, 3 a 5).

5. OUTIL — PRINCIPE DE CONCEPTION retenu : MODULAIRE.
   Simple par defaut, exhaustif seulement si le besoin s'en fait sentir.
   Les calculs avances sont derriere le bouton "Options", desactives
   par defaut, et disparaissent proprement si on les recoupe.

===============================================================
OUTIL DE SUIVI — FONCTIONS DISPONIBLES (au 27/08/2026)
===============================================================

SAISIE
  - Scenarios : 2 positions (Bol / Piste), N° outil, ref plaquette,
    prix, nb aretes, charniere, Vc, f.
  - Essais datés avec equipe (Matin/Apres-midi/Nuit) et operateur.
  - Champ OBSERVATIONS par essai (mode d'usure, entaille, incident,
    lot de fonte).
  - Prelevements : n° piece + valeur mesuree. Tri automatique par
    n° de piece croissant en quittant le champ. Touche ENTREE dans
    la derniere ligne = nouvelle ligne de prelevement, focus pose
    directement dessus.
  - Mode EMAG 1 : deux mesures Droite / Gauche (conformite = le max).
  - Grandeur mesuree RENOMMABLE (battement, Ra, ...) : le libelle se
    propage a la colonne, au graphique et a l'axe Y.
  - Limite de tolerance editable (valeur + libelle).
  - Suivi rebut equipe : pieces produites / rebutees -> taux ligne.

LECTURE
  - GRAPHIQUE DE TENDANCE : une courbe par essai, ligne de tolerance
    en pointilles, points hors tolerance grossis en rouge. Chaque
    essai a aussi son propre style de trait (plein/tirets/pointilles)
    en plus de sa couleur, pour rester lisible en impression N&B.
  - Onglets comparatifs : cout/piece, ecart %, cycle, essais, rebut.
  - VUE DE SYNTHESE (bouton "📋 Vue de synthese") : tableau comparatif
    tous scenarios en colonnes / criteres en lignes (statut, couts,
    Vc/f, charniere, cycle, essais non conformes, rebut), plus un
    graphique superposant la courbe de l'essai le plus complet de
    chaque scenario, pour repondre a "lequel derive le plus vite ?".
  - Statut automatique par essai (Conforme / Non conforme / En cours)
    et par scenario (N essais conformes / seuil).

MODULES OPTIONNELS (bouton "Options", desactives par defaut)
  - Cout du rebut : champ "cout d'un disque rebute" -> affiche un
    cout total/piece = outil + rebut.
    ORDRE DE GRANDEUR MESURE : a 1,9% de rebut et 14 EUR/disque, le
    rebut pese 0,26 EUR/piece contre 0,13 EUR d'outil, soit le DOUBLE.
    -> a activer avant toute conclusion economique ferme.
  - Temps de cycle en secondes : champ "cycle du scenario de reference
    (s)" -> convertit l'indice base 100 en secondes et en pieces/heure.

SORTIE
  - Export / Import .json horodate (archivage + echange par e-mail).
  - Bouton "↺ Restaurer" : filet de securite d'un cran, active
    automatiquement avant tout "Reinitialiser" ou "Importer" — permet
    d'annuler si le geste etait involontaire. Disparait une fois utilise.
  - Export CSV (separateur ";", virgule decimale Excel FR).
  - PDF PARAMETRABLE : cases a cocher pour choisir le contenu
    (plaquettes/couts, essais, graphique, rebut, vue de synthese)
    et option "uniquement le scenario affiche".

===============================================================
A FAIRE / PROCHAINE ETAPE (27/08/2026)
===============================================================

[ ] Essai Vc700 / f0,35 en G96 (K=244) -> mesurer battement,
    pieces/arete, usure. Attendu : gain de cycle ~30% vs essai du jour.
[ ] Essai G97 a 878 tr/min (N_opt), puis 808 et 950 tr/min (+/-8%)
    -> identifier le lobe le plus silencieux, viser le retour au
    cycle nominal Vc900/f0,50 en G97 fixe.
[ ] Prix confirme de la plaquette SNGX 120716 LKT640 : 5 EUR (egalement que la CNGX).
[ ] Renseigner le cout reel d'un disque rebute (matiere + VA perdue)
    pour activer le module cout rebut avec un chiffre juste.
[ ] Relever le temps de cycle machine reel du scenario de reference
    pour activer l'affichage en secondes.
[ ] Lancer un essai bol dedie en ceramique avant toute decision de
    standardisation geometrique (SNGX 85 partout) — objectif >= 75 p/arete
    sur le bol, non teste a ce jour.

===============================================================
OUTIL — CORRECTIONS ET AJOUTS DU 27/08
===============================================================

[ ] VUE DE SYNTHESE COMPARATIVE A L'ECRAN (bouton "📋 Vue de
    synthese") : tableau tous scénarios en colonnes / critères en
    lignes (statut, coût outil et coût total si module rebut actif,
    €/arête, Vc/f, charnière, cycle, essais non conformes, taux de
    rebut). N'existait auparavant qu'implicitement, sous forme de
    cartes, dans les onglets.
[ ] GRAPHIQUE MULTI-SCENARIOS SUPERPOSE, dans la même vue de
    synthese : une courbe par scénario (l'essai le plus complet de
    chacun), pour comparer directement qui derive le plus vite.
    Les deux éléments (tableau + graphique) sont aussi inclus dans
    le PDF via une case à cocher dédiée, sauf si "uniquement le
    scénario affiché" est coché.
[ ] FILET DE SECURITE : un "↺ Restaurer" apparaît automatiquement
    dès qu'un "Réinitialiser" ou un "Importer" a été effectué, et
    permet de revenir en un clic à l'état juste avant. Il disparaît
    une fois utilisé (un seul niveau d'annulation, pas une pile).
[ ] LISIBILITE DU PDF EN NOIR ET BLANC : chaque courbe (essai ou
    scénario) a maintenant un style de trait distinct (plein, tirets,
    pointillés...) en plus de sa couleur, dans les deux graphiques.
[ ] SAISIE RAPIDE : touche Entrée dans le dernier prélèvement d'un
    essai crée la ligne suivante et y place directement le focus,
    sans passer par la souris.

===============================================================
OUTIL — CORRECTIONS ET AJOUTS DU 26/08 (soir)
===============================================================

[ ] BUG CORRIGÉ — un essai était déclaré "CONFORME" alors qu'AUCUNE
    mesure n'avait été saisie : il suffisait de créer les lignes de
    prélèvement à l'avance (n° pièces jusqu'à la charnière) pour que
    l'essai passe au vert, et le scénario pouvait être "Valide" sans
    une seule mesure. Désormais : conforme = toutes les lignes
    mesurées + aucune hors tolérance + charnière atteinte.
    Le badge indique toujours ce qui manque ("2 mesures à saisir",
    "charnière piste non renseignée", "40/75 p").
[ ] Paramètres de coupe FIGÉS dans l'essai (Vc / f / charnière
    enregistrés à sa création). Si le scénario est modifié ensuite,
    l'essai garde ses conditions réelles et affiche une alerte orange
    + bouton "Aligner sur le scénario" (à n'utiliser que si l'essai a
    réellement été mené avec les nouveaux paramètres).
[ ] Tolérance et grandeur mesuree définies GLOBALEMENT (Options),
    communes à tous les scénarios. Un scénario peut déclarer une
    exception via la case "Tolérance spécifique à ce scénario".
    Reprise automatique des anciens fichiers.
[ ] EXPORT CSV (bouton "Export CSV") : une ligne par prélèvement,
    séparateur ";" et virgule décimale (Excel FR), colonnes incluant
    les conditions de coupe de l'essai, la tolérance et OUI/NON.
[ ] AIDE INTÉGRÉE "Comment ça marche" dépliable en haut de page :
    scénario > essai > prélèvement, règles de validation,
    rappel sauvegarde. L'outil s'explique seul.

===============================================================
OUTIL — ÉVOLUTIONS RESTANTES
===============================================================

(neant pour l'instant — toutes les évolutions demandées au 26/08
ont été traitées le 27/08. À compléter au fil des besoins.)

===============================================================
POINTS DE VIGILANCE (signés par Claude, prompt généré par Hermes)
===============================================================

- Pas de base de seuils thermiques CBN/LKT640 validée disponible ici :
  le raisonnement thermique s'appuie sur l'encadrement par les points
  déjà prouvés en production (K=174 et K=448), pas sur un modèle
  physique absolu de ce couple nuance/fonte.
- "Vf = Vc x f" utilisé dans le prompt/rapport est un indice de
  productivité relatif, pas une vitesse d'avance machine réelle en
  mm/min.
- Durée de vie prédite pour l'essai de demain (~150 p/arête) est une
  hypothèse basée sur f inchangé, pas un chiffre garanti — un seul
  essai jour ne suffit pas à établir une loi d'usure fiable.
- OUTIL : le coût/piece par défaut ne couvre QUE la plaquette. Tant que
  le module "cout du rebut" n'est pas activé avec un coût disque réel,
  l'écart affiché (-93%) surestime le gain réel.
- OUTIL : la formule du coût rebut est volontairement simple et lisible
  (cout = outil + taux_rebut x cout_disque, par pièce produite). Elle
  suffit à comparer des scénarios entre eux, pas à un chiffrage
  comptable au centime.
- OUTIL : les modifications faites sur l'artefact en ligne (claude.ai)
  ne sont qu'un aperçu — les boutons Exporter/Importer n'y fonctionnent
  pas. Seul le fichier HTML local fait foi.
- OUTIL : le "↺ Restaurer" est un cran d'annulation unique (pas une
  pile d'historique) : il protège contre un Réinitialiser/Importer
  fait par erreur, pas contre des saisies erronées ultérieures.
- OUTIL : le graphique multi-scenarios trace l'essai le plus complet
  (le plus de mesures) de chaque scénario, pas une moyenne — à lire
  comme une comparaison indicative, pas un cumul statistique.

===============================================================
UTILISATION DU DOSSIER
===============================================================

Déposer ici : comptes-rendus d'essai, relevés de paramètres, photos
d'usure. Chaque nouveau fichier ajouté pourra être lu et analysé pour
maintenir un suivi continu du sujet OP10.

LU PAR HERMES LE 26/08/2026 : lecture du README, continuation OP10.
Prochaines étapes : préparation des essais Vc700/f0,35 (G96) puis G97
(N_opt +/- 8%) pour validation thermique et vibratoire. Mise à jour
de l'outil de suivi avec les nouveaux essais et amélioration éventuelle
du suivi K et Vf en temps réel.

MIS À JOUR PAR CLAUDE LE 27/08/2026 : les 5 évolutions listées dans
"OUTIL — ÉVOLUTIONS RESTANTES" du 26/08 ont été implémentées dans
bilan_economique.html (vue de synthèse comparative, graphique
multi-scenarios, filet de sécurité Restaurer, styles de trait N&B,
saisie rapide Entrée). Voir "OUTIL — CORRECTIONS ET AJOUTS DU 27/08"
ci-dessus. Au passage : le README portait une corruption mécanique
(séquences \n et \" littérales au lieu de retours à la ligne et
guillemets réels, de "BUG CORRIGÉ" jusqu'à la note Hermes) —
probablement un artefact d'écriture d'une session précédente ; corrigé
dans cette même passe.

NOTE IMPORTANTE CONCERNANT L'ESSAI DU 26/08 :
L'essai réalisé hier (26/08) a été effectué avec l'outil T50013
équipé d'une plaquette piste SNGX 120716 ayant un angle de rayon de
coupe (κr) de 85° (au lieu des 75° habituels). Cette géométrie
particulière permet de réduire significativement les forces radiales
lors de la coupe, ce qui est particulièrement pertinent étant donnée
la fraicheur (manque de maturité) des bruts de fonderie à Sept Fons.
La durée de vie de l'outil, exprimée en nombre de pièces par arête,
est directement liée à la tolérance de battement mesurée ; maintenir
le battement dans la tolérance permet de prolonger la vie de l'arête
malgré les conditions de matériau moins stables.

MIS À JOUR PAR CLAUDE LE 27/08/2026 (suite) — retours terrain de Benjamin :
- Prix plaquette SNGX 120716 LKT640 reconfirmé à 5 EUR (identique CNGX).
- Essai bol dédié réalisé en configuration d'origine : 150 p/arête sans
  problème (objectif >= 75 p/arête largement dépassé). Item "Lancer un
  essai bol dédié" de la liste A FAIRE : traité.
- Préférence opérateurs confirmée : synchroniser la charnière bol+piste
  simplifie le changement d'arêtes (un seul geste pour les 2 positions).
  Cela favorise le scénario "Céramique intégrale — LKT640" (150p/150p,
  déjà modélisé ainsi dans l'outil) par rapport au "Mixte T50013"
  (75p/150p, changements désynchronisés).
- Nouveau paramètre à suivre par essai, demandé par Benjamin : maturité
  des bruts (en jours), pour croiser avec le taux de rebut battement —
  cohérent avec la note ci-dessus sur la fraîcheur des bruts à Sept Fons.

OUTIL — 3 AJOUTS DU 27/08 (suite à la demande de Benjamin) :
- Champ "Maturité des bruts (jours)" par essai, affiché à côté du taux
  de prélèvements hors tolérance de cet essai (comparaison directe),
  et exporté dans le CSV.
- Widget K/Vf en temps réel dans chaque scénario : Vf = Vc x f et
  K = Vf x sin(κr piste), comparés en direct aux points déjà validés
  (Vf 175-450, K 174-448). Nécessite de renseigner un nouveau champ
  κr piste (°) dans le tableau plaquettes ; sans lui, K reste "—"
  (Vf seul reste calculable).
- Bouton "📩 Rapport de validation" : génère en un clic un fichier
  HTML autonome pour le scénario affiché (conditions de coupe, essais,
  résumé économique, verdict Validé/Non validé/À affiner) — prêt à
  envoyer par e-mail à Arthur/Matis sans passer par le PDF complet.

À noter : le README a de nouveau été réécrit entre-temps (accents
harmonisés, mais TOUTES les cases "[X]" — y compris celles du 26/08,
déjà vérifiées — sont repassées à "[ ]" de façon uniforme). Cela
ressemble à un effet de bord d'un script de reformatage plutôt qu'à
une remise en cause volontaire de ces items. Signalé ici sans le
corriger unilatéralement — à trancher avec Benjamin si besoin.