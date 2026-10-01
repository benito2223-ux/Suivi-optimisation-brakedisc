# CONSTITUTION DU SUIVI — les règles du jeu · v1

**Co-rédigée** : Hermes (finalité) × Z Code (technique) · **Arbitre** : Benjamin
**Adoptée le** : 29/09/2026 · **Socle** : 4.53.0
**Statut** : toute nouvelle version, toute nouvelle fonctionnalité, tout correctif se
**vérifie contre ce document avant d'être livré**. Si une évolution contredit une règle,
la règle ne change que par décision explicite de Benjamin.

---

## 1. Ce que cet outil EST — et pour qui

Un **suivi d'optimisation du coût de revient des disques frein** (usinage céramique,
Sept Fons). Il sert trois publics, dans cet ordre de priorité :

1. **L'atelier (Matis, opérateurs)** : capturer les essais, mesurer, décider — gants,
   tablette, gros chiffres, la raison d'un état toujours à côté de l'état ;
2. **Matis pilote** : piloter le plan par OP et par poste, voir les gains se réaliser ;
3. **La hiérarchie de Matis** : lire la rigueur de la démarche, les gains actés, le
   plan d'action, et le partenariat outillage qui l'épaule (SPK by CeramTec).

**La direction du projet (Benjamin, 01/10/2026 — recopiée telle quelle) :**

> « Le CPP, c'est le sujet qui va nous servir de référence **jusqu'à la fin des
> projets**. On doit améliorer ces valeurs là, qui sont les valeurs actuelles. Et
> c'est en travaillant **opération par opération, outil par outil, logement par
> logement** qu'on arrive à optimiser ce CPP. Réfléchissez dans ce sens-là pour
> optimiser l'outil au mieux. C'est vous les cerveaux, moi je ne suis que le
> maître d'orchestre. »

Toute évolution de l'outil se vérifie contre cette direction : à chaque niveau de
l'arbre (pièce → OP → outil → logement), le CPP obtenu, sa référence, et l'écart.

## 2. Les entités qui existent (et celles qui n'existent pas)

| Entité | Ce que c'est | Où elle vit |
|---|---|---|
| **Ligne** | une machine de production (EMAG 1, HESSAPP…), un taux horaire | données ; topologie déclarée dans `LIGNES_SEPT_FONS` |
| **Référence** | un disque (ex. DV 356x26 RPI), sa cible de coût (`cibleCPP`), son volume annuel | données |
| **OP** | une opération sur une référence, identifiée par son **`opCode`** (OP10, OP30…) — le nom libre n'est jamais une clé | données (opCode dérivé, 4.50) |
| **Outil** (porte-outil) | le corps qui porte les logements ; identifié par son **numéro** (`T543`). **Pas** d'outillage interchangeable : le même `T543` peut être monté sur EMAG 1 et sur EMAG 3 | données (`scenario.outils[].numero`) |
| **Logement** (correcteur) | **un emplacement physique sur l'outil**, garni d'une plaquette. D1, D2, D3 sont des logements — **jamais des outils différents** | données (`scenario.outils[].logements[]`) |
| **Scénario** | une configuration d'outils testée contre la prod | données ; **la prod = le scénario ★** |
| **Poste** | ligne × opCode — un groupe d'outils qui tournent ensemble | **dérivé** (`gainPoste`), jamais stocké |
| **Livraison** | l'instantané FIGÉ et DATÉ des gains, que la hiérarchie lit | données (`livraisons`, 4.53) |
| **Projet** | une étiquette de regroupement — jamais une livraison, jamais un propriétaire | données (4.1) |

**Interdit** : inventer une entité dans le code qui n'est pas dans cette table (leçon
Bol/Piste v4.39, leçon « tuiles fantômes » 4.51.2). Une nouvelle entité entre ici, par
décision de Benjamin, avec sa migration.

---

## 2 ter. LA LOI DU CORRECTEUR — le mot, et ce qu'il interdit

*(Benjamin, 30/09 et 01/10/2026. Écrit après huit jours de batailles sur le même mot.
C'est l'article le plus important de cette constitution, parce que tous les autres
en découlent.)*

> **« Un correcteur qui se trouve dans l'excel de Matis est un logement. La machine
> appelle un outil et y ajoute le correcteur correspondant au logement pour avoir le
> point de départ de l'usinage. »**

### Les mots

| mot | veut dire | ne veut **jamais** dire |
|---|---|---|
| **porte-outil** / **outil** | le corps, le numéro `T543` | un jeu d'outillage qu'on interchange |
| **correcteur** / **logement** | un emplacement : D1, D2, D3 | un outil, une référence, une position d'OP |
| **plaquette** | ce qui garnit le logement, identifiée par son **MABEC** | l'emplacement lui-même |
| **MABEC** | le code article d'une plaquette | un identifiant d'outil — **plusieurs MABEC sur un outil est NORMAL** (un par logement) |

### Ce que la loi interdit, explicitement

1. **Créer un outil par correcteur.** `T543 D1` et `T543 D2` sont **un** outil `T543` à
   **deux** logements. Un outil sans correcteur, c'est un outil à un logement provisoire.
2. **Rapprocher sur la chaîne brute.** `T 513 D1` et `T513 D1` sont le **même**
   porte-outil : la clé de rapprochement ignore espaces, tirets et points
   (`matisClePorteOutil`). L'**affichage** garde la forme de l'atelier.
3. **Recopier le MABEC d'une ligne à la suivante** quand la ligne n'en a pas. Une case
   vide vaut mieux qu'un article attribué au mauvais logement.
4. **Écrire un zéro là où il n'y a pas de mesure.** Une production à 0 est une
   *absence* de mesure — l'écran dit « jamais travaillée », il n'invente pas.
5. **Utiliser « DTV » ou « voile »** dans une interface ou dans une variable. Le
   vocabulaire du projet est **battement, Ra, épaisseur de piste**.
   ⚠️ **« face appui » reste ambigu** — une mesure ou deux ? **Rien n'est codé tant que
   Matis n'a pas répondu.**

### La question ouverte — et elle est grande

**Un même logement, monté sur deux références différentes, porte-t-il deux plaquettes
différentes ?**

Mesuré dans le classeur, 01/10 : **oui, apparemment.** `T1 D1` porte `Z000 546 266` sur
la 266x13 et `IM02 137 021` (ISO *KY3500*) sur la 302x26.

> **Conséquence sur le modèle :** aujourd'hui MABEC, prix et DDV sont portés par le
> **logement**. Si la réponse est « oui », ils doivent être portés par le couple
> **(référence × logement)**.

**Ce n'est pas un bug, c'est une question de modèle** — et elle touche tous les coûts.
Elle est **posée à Matis** (message à Matis, demande n° 9). **Tant qu'elle n'est pas
réponse, le modèle ne change pas** : on ne change pas la façon dont tout se calcule sur
une supposition.


### 2 bis. Trois réserves de Hermes sur la v1 (à trancher, non bloquantes)

La constitution est Adoptée et je la valide comme document de référence. Trois points
demandent une phrase de plus, parce qu'ils resteront vrais dans trois versions :

**R1 — « La prod = le scénario ★ » est une règle *actuelle*, pas un état final.**
C'est la décision 2 de mon avis structurel, et elle n'est pas encore prise. Tant que
la prod est un scénario comme les autres, chaque version re-paye le « ★ d'abord, excel
en repli ». La table le dit honnêtement ; il faut seulement qu'on sache que c'est un
**état transitoire documenté**, et non la forme finale.

**R2 — « Le poste est dérivé, jamais stocké » a un prix, et il est assumé.**
Le poste reste une valeur calculée : deux affichages qui ne passent pas par
`gainPoste` raconteront deux histoires (leçon `coutEnCours`, 4.51.1). La règle §3.1
(source unique) est donc **la** protection du poste, et elle n'est pas facultative.
Si un jour le poste devient stocké, cette règle §3.1 doit être réévaluée dans le même
bref.

**R3 — La constitution ne dit rien du « qui écrit quand ».** *(résolue le 29/09/2026 —
voir §6, désormais appliquée ; la formulation d'origine est conservée ci-dessus comme
trace de la réserve)*
Elle dit quoi, pas qui. L'incident du 29/09 (deux sessions sur `bilan_economique.html`
à 20 minutes d'intervalle) montre qu'il manque une règle de gouvernance : **un seul
auteur sur le fichier à la fois, et un commit par version**. C'est une règle de
processus, pas de produit — mais c'est elle qui protège tout le reste.

## 2 quater. LE CPP — deux axes, jamais un seul chiffre

*(Benjamin, 01/10/2026, après la démonstration des deux axes.)*

> « Le CPP, c'est le sujet qui va nous servir de référence **jusqu'à la fin des projets**.
> On doit améliorer ces valeurs là, qui sont les valeurs actuelles. Et c'est en travaillant
> **opération par opération, outil par outil, logement par logement** qu'on arrive à
> optimiser ce CPP. »

**La règle.** Un CPP affiché n'est jamais un chiffre, c'est **deux chiffres et leur
décomposition** :

| axe | ce qu'il mesure | d'où il vient | comparé à Matis ? |
|---|---|---|---|
| **OUTILLAGE** | `prix ÷ (arêtes × DDV)`, par plaquette | formule du classeur, colonne I | **oui — c'est sa mesure** |
| **TEMPS** | `(taux horaire ÷ 3600) × temps de cycle` | mesures atelier, `coutMachinePiece` | **non — le classeur ne l'a pas** |

**Vérifié le 01/10, sur cinq lignes réelles du classeur et sur `posCost()` :**
`prix ÷ (arêtes × DDV)` = `prix ÷ (arêtes × charnière)`. **La même formule, terme pour
terme.** Avec la machine désactivée — le défaut — **le CPP de l'outil EST le CPP de Matis.**

**Les trois règles qui en découlent.**

1. **L'outillage est l'indicateur principal**, parce que c'est le seul que Matis peut
   vérifier. Le temps s'affiche **à côté**, valorisé au taux horaire de la ligne, **uniquement
   quand les données de cycle sont remplies**.
2. **Sans donnée de temps, l'outillage reste la base 100.** Une base unique permet de comparer ;
   deux chiffres non comparables ne permettent rien.
3. **On ne compare jamais un total de l'outil à un CPP de classeur.** Le total inclut la
   machine, le classeur l'ignore. La comparaison se fait **axe par axe** — sinon l'écart
   affiché mélange une amélioration et une différence de périmètre.

**Et la décomposition va jusqu'en bas**, à chaque étage, sur les deux axes :
pièce → OP → outil → logement. C'est la phrase de Benjamin, littéralement.

**Deux axes, deux questions, deux leviers :**
- *outillage* — « quelle plaquette me coûte cher ? » → prix, DDV, nombre d'arêtes, réf ;
- *temps* — « qu'est-ce qui prend du temps ? » → Vc, f, profondeur, machine.

## 3. Les règles de calcul — d'où vient chaque chiffre

1. **Source unique** : un même chiffre (gain de poste, coût pièce, % de chemin) se
   calcule **par une seule fonction** et s'affiche partout avec la même valeur. Deux
   modules ne racontent jamais deux histoires (leçon `coutEnCours` 4.51.1) ;
2. **Périmètre commun** : un delta ne compare jamais des postes de coût différents
   (`perimetreCompare`, 4.45) — un poste non chiffrable se déclare, il ne devient pas 0 ;
3. **Coût machine = la ligne du poste** : `coutsDetail` exige la ligne explicite ;
   `pieceCPPComplet` ne s'appelle qu'en contexte référence ouverte (leçon 4.51.1-§4) ;
4. **Les gains actés et projetés ne se somment jamais** — ils vivent dans des blocs
   distincts, étiquetés (4.45) ;
5. **Un chiffre mensonger vaut pire qu'un trou** : pas de « 0 € » qui voudrait dire
   « rien à gagner », pas de barre invisible qui voudrait dire « pas d'écart » —
   l'absence s'explique (leçon 4.49.4).

## 4. Les règles de confidentialité

1. **Jamais de K ni P_req visibles** — ni écran, ni impression, ni rapport, ni carte ;
   « Hex » s'appelle épaisseur de copeau ; les nuances sont **SPK** (jamais Greenleaf) ;
2. Les données réelles ne quittent jamais le poste ; **jamais de push du jeu [Exemple]** ;
3. L'outil est présentable en réunion telle quelle (règle A4 du 4.51.x).

## 5. Les règles d'interface

1. **Les informations arrivent en douceur** : couche 0 lisible en un coup d'œil, la
   couche suivante se paye par un geste (tuile → fiche → poste → essai) ;
2. **La raison d'un état est à côté de l'état** — jamais un chiffre seul ;
3. **Deux thèmes, impression A4 propre, tactile** : toute nouvelle UI se vérifie dans
   les deux thèmes, à l'impression, et au doigt ;
4. **Le design system tient** — **un seul jeu de tokens**, couleurs et formes nommées, pas
   de couleurs hors tokens sans décision *(v1.5, 30/09 : les tokens sont ceux du Design
   System B — `--radius: 2px`, `--red: #E30045`, `--blue: #006AB3`, quatre gris, une seule
   famille sans-serif + le mono pour les chiffres)* ;
5. **aucune dépendance réseau** *(v1.5, 30/09)* — ni CSS distant, ni police distante, ni
   image distante. L'outil doit s'afficher **complet avec le réseau coupé**, parce qu'il
   tourne sur le poste de Matis, en atelier. **Test d'acceptation : ouvrir le fichier hors
   ligne.** Une dépendance distante n'est pas une dégradation, c'est un écran blanc ;
6. **un chiffre qu'on ne peut pas justifier n'est pas affiché** *(v1.5, 30/09, arbitrage de
   Benjamin après la proposition Google Stitch)*. Un chiffre écrit gros et propre n'est pas
   plus vrai qu'un autre. Concrètement : si on ne peut pas remonter à sa source, il n'a pas
   le droit d'apparaître — **ni dans une maquette, ni dans un écran, ni dans un rapport**.
   *Cette règle vaut pour nous deux autant que pour une proposition externe.* Un agrégat
   calculé sur un périmètre partiel porte la taille de ce périmètre avec lui (§4.60.1 :
   « hors 1 opération non chiffrée »), jamais un total silencieux.

## 6. Qui écrit, et quand — la gouvernance (ajouté le 29/09/2026)

La constitution disait quoi, pas qui (réserve R3). Elle le dit maintenant :

1. **`VERROU.md` (racine du dépôt) est le gardien** : un tableau dit qui travaille sur
   `bilan_economique.html`, depuis quand, sur quelle version et quel sujet. Vide = le
   fichier est libre. Rempli = **personne d'autre n'y touche** ;
2. **un tour = un commit** : chaque session prend le verrou, travaille, écrit son tour
   dans `ECHANGES.md`, libère le verrou, et commite les trois ;
3. **`ECHANGES.md` est le journal commun** : chacun lit le dernier tour, écrit le sien en
   haut, et y consigne les « décisions en attente de Benjamin ». **Benjamin n'est plus le
   transporteur** — il ne relaie plus les messages entre les deux assistants ;
4. **on ne tranche pas à la place de Benjamin** : ce qui est usage, ihm revient, et c'est
   écrit comme tel ;
5. si le verrou est pris et qu'il faut écrire malgré tout : on demande, ou on passe par
   Benjamin. **On ne contourne pas** — c'est le geste qui a coûté une session le 29/09 ;
6. **on lit les tours vraiment, pas en diagonale** (ajouté le 30/09, leçon du Tour 4).
   Ni le verrou ni l'empreinte automatique n'attrapent une insertion manuelle ratée : le verrou
   protège contre deux auteurs, l'automatique contre une modification non déclarée. Mais
   « j'ai écrit, et j'ai affirmé que c'était bon » — seule une **relecture** l'attrape. Un
   contre-regard n'est pas de la formalité, c'est la seule chose qui marche. Concrètement :
   le tour précédent est relu en entier avant d'écrire le sien ;
7. **un contre-regard se restaure par copie sauvegardée, jamais par `git checkout`**
   (ajouté le 30/09, incident du Tour 20). `git checkout` rétablit le **dernier commit**, pas
   l'état d'avant injection : si le travail n'est pas commité, il l'efface. Z Code a perdu une
   version entière de la 4.61.0 ainsi, et l'a reconstituée intégralement. La procédure qui
   marche : **copier le fichier avant d'injecter la panne** (`cp` ou lecture en mémoire),
   puis le rendre par copie. Le contre-regard reste juste ; c'est le geste de restauration
   qui était mauvais. Et cette règle vaut pour les deux ;
8. **une injection se prépare, elle ne s'improvise pas** : trois étapes, toujours les mêmes —
   sauvegarder, casser, regarder, restaurer, **vérifier que le fichier restauré est
   identique octet pour octet**. Un contre-regard qui laisse le fichier différent du départ
   n'a rien vérifié ;
9. **une suite de tests ne voit pas ce qu'elle ne mesure pas** *(v1.6, 30/09, mesuré sur
   L3→L7)*. Le harnais vérifie des **fonctions** et le **contraste**. Il ne voit pas une
   bordure qui disparaît, un rayon qui change, un aplat qui devient un filet. Constaté en
   mesurant : sur cinq pannes CSS injectées, **une seule** a été vue (celle qui touchait un
   contraste) ; les quatre autres sont passées sans bruit. *Les tests protègent ce qu'on a
   programmé, pas ce qu'on a dessiné.* Corollaire : **un chantier de charte (L1→L7) se vérifie
   à l'œil et à la capture, jamais par « les tests sont verts »** — le vert ne dit rien de la
   forme. Et : un jour, il faudra un contrôle qui **compte** les occurrences d'un motif dans
   la CSS (comme on compte les aplats de couleur), pas seulement qui compare une valeur.

*Pourquoi c'est une règle de produit et pas seulement de méthode* : tout le travail
d'octobre tient dans un fichier unique. Une collision ne « perd » pas un bout de code, elle
écrase silencieusement des heures de travail et ne laisse pas de trace. C'est le seul point
du projet où une erreur n'est pas récupérable.

## 7. Règles de version

1. La constitution est **lue avant de coder** ; toute évolution contradictoire passe
   par une décision explicite de Benjamin, consignée ici ;
2. Rituel de release : tests verts + deux thèmes + console propre + NOUVEAUTES +
   CHANGELOG + déploiement **Projet** ; la prod ne bouge que sur validation de Benjamin ;
3. Un **client périmé ne peut plus effacer une donnée** : ce que le serveur défend
   (trigger `preserve_cibles_cpp`), la constitution l'interdit aussi ;
4. Toute nouvelle entité de données passe par Benjamin avec sa migration documentée.

---

*v1 — 29/09/2026, co-rédigée Hermes × Z Code, arbitrage Benjamin. Toute modification de
cette constitution se fait dans ce fichier, datée et motivée.*

*v1.1 — 29/09/2026, Hermes : adoption de la v1 comme document de référence, et ajout
du §2 bis (trois réserves : R1 la prod-★ est un état transitoire, R2 le poste dérivé
impose la source unique, R3 la constitution ne dit pas qui écrit quand). Aucune règle
de fond n'est modifiée par ces réserves ; elles les rendent explicites.*

*v1.2 — 29/09/2026, Hermes : la réserve R3 est résolue. Nouvelle section §6 « Qui écrit,
et quand » : le verrou (`VERROU.md`) et le journal commun (`ECHANGES.md`) remplacent le
transport par copier-coller ; Benjamin n'est plus le relais entre les deux assistants. Aucune
règle de fond (entités, calcul, confidentialité, interface) n'est modifiée par cette v1.2.*

*v1.3 — 30/09/2026, Hermes : regle 6 ajoutee a la section §6 (« on lit les tours vraiment, pas
en diagonale »),nee du Tour 4 de Z Code qui a attrape une insertion manuelle ratee de mon Tour 3
que j avais pourtant affirmee « intacte ». Aucune regle de fond modifiee.*

*v1.4 — 30/09/2026, Hermes : règles 7 et 8 ajoutées au §6 (restauration d'un contre-regard par copie sauvegardée, jamais par `git checkout` — incident Z Code au Tour 20 ; et vérification octet pour octet de la restauration).*

*v1.6 — 30/09/2026, Hermes : règle 9 ajoutée au §6 — « une suite de tests ne voit pas ce qu'elle ne mesure pas ». Mesuré sur les chantiers de charte L3→L7 : une panne CSS vue sur cinq. Un chantier de charte se vérifie à l'œil, jamais par « les tests sont verts ».*

**v1.7 — 30/09/2026, règle 10 (ajoutée après le contre-regard de la 4.71.0).** Un
contre-regard ne compte pas seulement les **échecs** : il vérifie que la suite **va jusqu'au
bout**. Constaté en mesurant la 4.71.0 — une panne qui faisait **planter** le script de
test était comptée « 0 échec », donc invisible ; et la moitié des tests n'avait pas tourné.
**0 échec ≠ Vert.** Une suite qui n'a pas terminé n'a rien rapporté. On compte les tests
exécutés autant que les échecs.

**v1.8 — 01/10/2026, Hermes : ajout de l'article 2 ter, « la loi du correcteur ».**
Huit jours de batailles sur le même mot, et la constitution ne le définissait nulle part.
Les entités **Outil** et **Logement** manquaient même dans la table du §2. Elles y sont
maintenant, avec la loi : ce que chaque mot veut dire, ce qu'il ne veut jamais dire, et
les cinq interdits. La question ouverte (l'article dépend-il de la référence ?) est écrite
comme question, avec sa mesure, et **n'est pas tranchée** — elle est à Matis.

*Cette version ne change aucun calcul. Elle écrit ce qu'on savait déjà et qu'on n'avait
jamais mis noir sur blanc.*

**v1.9 — 01/10/2026, Z Code : la direction CPP de Benjamin (01/10) transcrite en tête du §1, telle quelle, avec attribution.** Toute évolution se vérifie désormais contre : le CPP obtenu, sa référence, et l'écart — à chaque niveau de l'arbre pièce → OP → outil → logement.

**v1.10 — 01/10/2026, Hermes : ajout de l'article 2 quater, « le CPP — deux axes ».**
Trouvé en discutant : la formule de Matis (colonne I) et celle de l'outil (`posCost`) sont
**la même, terme pour terme** — `prix ÷ (arêtes × DDV)`. Le CPP de l'outil est donc le CPP
de Matis, exactement, tant que la machine est désactivée. C'est ce qui permet de nommer un
indicateur principal, et d'afficher le temps à côté sans jamais mélanger les deux périmètres.

*Aucun calcul n'a changé. Cette version écrit une architecture, sur une formule déjà
vérifiée — elle ne l'invente pas.*
