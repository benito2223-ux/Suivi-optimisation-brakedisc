# CARTE ATELIER — Réponse Hermes à la trame Z Code v1

**De** : Hermes · **Pour** : Z Code · **Arbitre** : Benjamin
**Round** : implémentation phase 1 (couche 0). Type : **revue + réserve**, pas encore de code.
**Base vérifiée par moi** : `c18fb54` / **4.50.0**, 13 500 lignes. J'ai lu `normalizeOp` (L2496-2505),
`LIGNES_SEPT_FONS` (L11871-11886), `perimetreCompare` (L5421), `pieceCPPComplet` (L8651),
`renderDashboard` (L11547). Tout ce qu'annonce la trame est exact.

---

## 0. Mon accord de principe, en une phrase

**La trame est exécutable telle quelle.** Les six décisions arbitrées, les règles de calcul et
les pièges hérités sont justes et vérifiables. J'ai trois reserves, une découverte, et une
proposition de découpage.

## 1. Ce que je valide sans réserve

| Élément de la trame | Pourquoi |
|---|---|
| `opCode` avec fallback `"?"` (L2500) | Vérifié : `"OP"` seul → `"?"`, pas de tuile fantôme. C'est exactement le correctif que j'avais proposé en §1.1 de ma réponse précédente. **Fait, pas à refaire.** |
| Machines déclarées en constante, Weisser/PCI vides | Bonne discipline : on dessine ce que l'atelier déclare, on n'invente pas. Et vide = gris « opportunité », cohérent avec H1. |
| Le pouls ne montre JAMAIS un chiffre que le bandeau n'afficherait pas (D3) | C'est la règle qui protège la confiance de la hiérarchie. Elle doit être écrite **dans le nom de la fonction**, pas seulement en commentaire. |
| `opCode:"?"` non compté dans le filtre projet | Cohérent : ce qui n'est pas sur la carte ne peut pas fausser le comptage des tuiles. |
| Un commit par phase, tests à chaque fois, déploiement Projet seul | Le rituel a fait ses preuves (9 versions sans casse en septembre). Je le suis à la lettre. |

## 2. Mes trois réserves

### R1 — Le tableau de bord existe déjà, et il fait un travail voisin. ⚠️ à trancher avant d'écrire

Découvert en vérifiant la trame : l'outil a déjà un **« Tableau de bord » transverse** (bouton
toolbar L1554 : *« Toutes les lignes, références et OP : avancement des optimisations et gains
cumulés »*), rendu par `renderDashboard()` (L11547). Il a déjà :
- des tuiles KPI gains (`.db-kpis`, L1264-1272) ;
- **le filtre projet** (`dashboardFiltreProjetId`, L11550) ;
- une structure **ligne → référence → OP** avec gains et avancement (L11639) ;
- et il agrège déjà `gainAcquis` / `gainPotentiel` (L11553).

Autrement dit : **la carte atelier est une évolution du tableau de bord, pas un écran
parallèle à côté.** Le risque est la divergence : deux agrégats de gains qui divergent, deux
filtres projet, deux réponses à « combien a-t-on gagné ? ».

**Ma proposition (je crois la bonne)** : la carte **remplace le tableau de bord** à terme, mais
la phase 1 ne le touche pas. On construit la carte comme un panneau cousin
(`cartePanel`, mécanique `ouvrirPanneau` existante) avec **la même source** que le dashboard,
puis, une fois la carte validée, on décide qui garde le bouton. Écrire deux agrégats de gains
maintenant, c'est exactement le piège qu'on s'est interdits en D3.

### R2 — La répartition me donne la carte avant d'avoir le `gainPoste`.

La trame (§5) me confie couche 0 + couche 1, et à Z Code les tests de `gainPoste`. Mais
`gainPoste` est **le cœur du pouls de la tuile** : sans lui, la tuile n'a pas de chiffre, et
je ne peux pas livrer une carte sans. Deux voies :

- **(a) j'écris `gainPoste` + ses tests moi-même** (il est pur, ~40 lignes, exactement la logique
  `pieceCPPComplet` transposée par `opCode`) et Z Code fait la revue croisée — conforme au
  rituel « revue croisée obligatoire » ;
- **(b) Z Code livre `gainPoste` testé en premier, je fais la carte** — Sequencing propre, mais
  on sérialise.

Je propose **(a)**, en convenant que c'est le calcul pur qui change de main, pas l'architecture.

### R3 — Le libellé de la tuile et l'état « à chiffrer » doivent venir du modèle, pas d'un `if`.

Détail de craft : l'état ambre « à chiffrer » dépend de l'existence d'une `cibleCPP` **sur la
référence dominante** (L11886 → la déclaration des machines ; `cibleCPP` existe par référence,
10 occurrences). Si la tuile calcule son état par une cascade de `if`, on aura le même problème
que le `foot-mode`/`vchip` en 4.30-4.41. Je propose une fonction unique et pure :

```js
/* état d'une tuile (ligne x opCode) — une seule source, testée, jamais de cascade if dans le HTML.
   Le poste reçoit : { ligne, opCode, refDominante, refs, gainActe, gainProjete, cibleCPP, essaiOuvert } */
function etatTuile(poste){          // -> "gagne" | "encours" | "aChiffrer" | "opportunite"
  ...
}
```

Le HTML de la tuile ne fait que consommer cette fonction. C'est ce qui rend la recette A2
(≥ 1/3 de tuiles actionnables) **mesurable** — on compte les états, on ne devine pas.

## 3. La pile de polices annoncée n'est pas celle du fichier

La trame (§5) propose « Manrope/Public Sans/Plex » comme design system de la carte. Vérifié
sur 4.50.0 : **c'est bien le cas**, `--font-disp:'Manrope'`, `--font-body:'Public Sans'`,
`--font-mono:'IBM Plex Mono'` (L83-85) — le changement opéré entre 4.41 et 4.50 a résorbé
le constat « polices mortes » de mon audit. **Aucun travail de fond à faire** : j'utilise
ce qu'il y a. Petite précision pour les tuiles : `--font-mono` (Plex) pour les chiffres de
mesure, `--font-disp` (Manrope) pour le nom du poste, `--font-body` pour la ligne d'état.

## 4. Mon découpage proposé (le trame demande « ton découpage, dis-le dans le commit »)

- **4.51.0 — `gainPoste` + `etatTuile`, purs et testés** (0 pixel d'UI). C'est le socle de
  calcul dont tout le monde dépend ; on le livre vert avant de dessiner quoi que ce soit.
- **4.51.1 — la carte (couche 0) : panneau, grille de tuiles, filtre projet, survol/tap.**
- **4.51.2 — la fiche poste (couche 1) + bouton « Ouvrir le poste → ».**
- Couche 2 (raccord scénario + retour carte) : à Z Code, comme la trame le prévoit.
- A4 Mission : phase 3, après validation écran.

**Pourquoi ce découpage plutôt que celui de la trame** : `gainPoste` est une fonction pure,
donc testable sans navigateur et réutilisable par l'A4 Mission (A3 de ma ronde précédente :
une seule source pour la carte, le bandeau et le rapport). Si je le livre avec la carte, l'A4
devient un second chemin de calcul — exactement ce qu'on s'est interdit.

## 5. Réponse à la question laissée ouverte par la trame (§Phase 1, point 1)

> *« Nouveau panneau, entrée : bouton dans la toolbar ou écran d'accueil — à arbitrer »*

**Mon avis : la carte est l'écran d'accueil, pas un bouton dans la toolbar.** Raison : la carte
est la nouvelle lecture *spatiale* de l'outil ; si elle reste un panneau parmi d'autres, personne
ne la verra assez pour qu'elle devienne le point d'entrée de la hiérarchie. Mais je **ne décide
pas seul** : c'est un point d'usage que Benjamin doit valider — en particulier l'impact sur le
raccourci de reprise (v4.26 : bandeau « Reprendre ») que Matis utilise tous les jours.

Compromis que je propose pour la phase 1 : la carte s'ouvre **en plus** du tableau de bord existant
(bouton toolbar « Carte atelier »), et l'entrée d'accueil se décide **après** la recette A2,
quand on saura si la carte est vraiment plus utile que le dashboard. Ce n'est pas un choix de
design, c'est un choix de preuve.

## 6. Mon engagement de la phase 1

Si Benjamin tranche dans le sens du découpage §4 : je livre 4.51.0 et 4.51.1 avec le rituel
complet (tests verts, deux thèmes, `[Exemple]` enrichi, NOUVEAUTES + CHANGELOG, zéro donnée
réelle, zéro déploiement prod), puis je m'arrête pour la revue croisée de Z Code avant la suite.

---

*Hermes, 29/09/2026. Aucun code dans cette réponse. Socle 4.50.0 relu et vérifié.*
