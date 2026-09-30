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

## 2. Les entités qui existent (et celles qui n'existent pas)

| Entité | Ce que c'est | Où elle vit |
|---|---|---|
| **Ligne** | une machine de production (EMAG 1, HESSAPP…), un taux horaire | données ; topologie déclarée dans `LIGNES_SEPT_FONS` |
| **Référence** | un disque (ex. DV 356x26 RPI), sa cible de coût (`cibleCPP`), son volume annuel | données |
| **OP** | une opération sur une référence, identifiée par son **`opCode`** (OP10, OP30…) — le nom libre n'est jamais une clé | données (opCode dérivé, 4.50) |
| **Scénario** | une configuration d'outils testée contre la prod | données ; **la prod = le scénario ★** |
| **Poste** | ligne × opCode — un groupe d'outils qui tournent ensemble | **dérivé** (`gainPoste`), jamais stocké |
| **Livraison** | l'instantané FIGÉ et DATÉ des gains, que la hiérarchie lit | données (`livraisons`, 4.53) |
| **Projet** | une étiquette de regroupement — jamais une livraison, jamais un propriétaire | données (4.1) |

**Interdit** : inventer une entité dans le code qui n'est pas dans cette table (leçon
Bol/Piste v4.39, leçon « tuiles fantômes » 4.51.2). Une nouvelle entité entre ici, par
décision de Benjamin, avec sa migration.

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
4. **Le design system tient** : Manrope/Public Sans/Plex, couleurs SPK, ambre =
   simultanéité, pas de couleurs hors tokens sans décision.

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
   n'a rien vérifié.

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
