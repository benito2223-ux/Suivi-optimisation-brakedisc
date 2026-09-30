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

## 6. Les règles de version

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
