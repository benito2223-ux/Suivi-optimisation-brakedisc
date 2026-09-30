# TRAME D'IMPLÉMENTATION — Carte atelier (tuiles machines) — pour Hermes

**De** : Z Code · **Pour** : Hermes · **Arbitre** : Benjamin
**Base** : spec croisée v1/v1 (`SPEC_navigation_tuiles_*.md`, 2 rounds, convergée)
**Branche** : `dev` · **Déploiement** : `suivi-optimisation-projet.surge.sh` UNIQUEMENT
**État du socle** : **4.50.0 livré** (commit `c18fb54`) — les prérequis sont en place, tu peux commencer.

---

## 0. Ce que Z Code a déjà fait (ne pas refaire)

- **`opCode` dérivé** dans `normalizeOp` (L2496) : motif `OP\s?0*(\d+)` sur le nom,
  fallback `"?"` (pas de tuile fantôme). Vérifié sur les vrais noms : « OP 30 Perçages »
  → OP30, « OP10 Ebauche piste Inter » → OP10, « OP » seul → « ? » ;
- **`machines` déclarées** dans `LIGNES_SEPT_FONS` (L11871) : EMAG 1 OP10/20/30/40 ·
  EMAG 2 OP10/30/40 · EMAG 3 OP10/40 · HESSAPP OP10/15/20/40 · Weisser et PCI : vides
  (à compléter par l'atelier — ne pas inventer) ;
- Tests : 224/224 verts, syntaxe vérifiée, déployé sur l'adresse Projet (4.50.0).

---

## 1. Les décisions arbitrées par Benjamin (non renégociables)

1. **Topologie dérivée + déclaration en constante** : jamais d'entité machine
   propriétaire, jamais gravée en dur ailleurs que dans `LIGNES_SEPT_FONS` ;
2. **H1 = (b)+(a)** : la carte s'ouvre sur **le projet actif** (tuiles utiles),
   « toute l'usine » est un clic ; les tuiles « à chiffrer » (référence avec
   `cibleCPP` mais sans mesures) sont un état visible **invitant**, pas un gris mort ;
3. **D4 = écran d'abord, A4 Mission juste derrière** — même source de données pour
   les deux (jamais de recalcul local dans l'A4) ;
4. **A2 — seuil de recette** : ≥ 1/3 des tuiles actionnables (gain, cible ou essai
   ouvert) sur le jeu 2026/2027, à vérifier à la livraison de la couche 0 ;
5. **Filtre projet sur la carte** : défaut = le projet actif, bascule « toute
   l'usine » sur la carte même ;
6. **Confidentialité** : la carte est présentable en réunion — pas de K/P (la botte
   secrete reste hors UI), chaque € étiqueté **acté** (série) ou **projeté** (essai),
   jamais sommés ensemble.

## 2. Les règles de calcul (source unique — réutilise, n'invente jamais)

- **Gain d'une tuile (ligne × opCode)** : somme, sur les références de la ligne
  présentes à cet opCode, des gains **périmètre commun** (`perimetreCompare`, 4.45)
  entre la prod de l'OP (★, repli excel) et le meilleur scénario non-prod —
  la même logique que `pieceCPPComplet` (4.49, L~8570) mais par opCode au lieu de
  référence. Étiquette : **acté** (statut série) / **projeté** (le reste), jamais
  sommés ensemble ;
- **Le pouls D2 = 2 chiffres + chemin** : acté (si > 0) · potentiel (si cible et
  périmètre le permettent) ; « en cours » seulement s'il existe un essai ouvert.
  La tuile ne montre JAMAIS un chiffre que le bandeau du scénario n'afficherait pas ;
- **Les OPs sans scénario chiffrable** : tuile grise « opportunité » — et si la
  référence a une `cibleCPP`, la tuile devient « à chiffrer » (invitation, décision H1-a) ;
- **OP sans code (`opCode:"?"`)** : pas de tuile — atteignable en navigation experte
  uniquement, et le filtre projet ne la compte pas dans les tuiles.

## 3. Phasage proposé (un commit par phase, rituel complet à chaque fois)

### Phase 1 — Couche 0 : la carte (lecture seule)
- Nouveau panneau (même mécanique que `ouvrirPanneau`), entrée : bouton dans la
  toolbar ou écran d'accueil — **à arbitrer avec Benjamin** (tranche à la revue de
  la maquette) ;
- Tuiles = (ligne déclarée × machine déclarée) ; état : vert (gagné, en série) /
  bleu (essai en cours) / ambre (à chiffrer, cible posée) / gris (opportunité) ;
- Pouls D2 : acté / potentiel / (% chemin si `cibleCPP` sur la ref dominante) ;
- Multi-réf. : réf. dominante (volume de série) + compteur « +n réf. » ;
- Filtre « mon projet / toute l'usine » sur la carte ;
- Navigation : clic tuile → couche 2. Retour carte = bouton permanent (A1 d'Hermes).

### Phase 2 — Couches 1-2 : fiche poste puis détail
- **Couche 1 (fiche)** : survol desktop / 1er tap tablette — réf. présentes, série
  vs essai, gain du poste, prochaine étape, **bouton « Ouvrir le poste → »** ;
- **Couche 2** : réutilise le rendu scénario EXISTANT (`scenarioBlockHTML`) — pas de
  nouvelle UI d'essai. Le fil d'Ariane expert reste le chemin par référence (R4) ;
- Retour carte défini depuis chaque couche (A1) — jamais de cul-de-sac.

### Phase 3 — A4 Mission (après validation de l'écran)
- Imprimable « Mission 2026/2027 » : timeline essais, protocole 5×, gains actés,
  plan des 6 références, SPK partenaire — **consomme `gainPoste`/`pieceCPPComplet`,
  zéro recalcul** ;
- Impression : réutiliser les patterns `@media print` existants.

## 4. Rituels (identiques à nos sessions précédentes)

1. **Branche `dev`** — jamais main ; **déploiement Projet uniquement** — la prod ne
   bouge pas sans validation Benjamin explicite ;
2. Version : prochaine **4.51.x** par phase livrée (4.51.0 carte, 4.51.1 fiche+couche 2,
   4.52.0 A4 — ou ton découpage, dis-le dans le commit) ;
3. Tests `runTests()` verts (224 aujourd'hui) + **nouveaux tests** pour `gainPoste`
   et le groupage par `opCode` (multi-réf., OP sans code, agrégation acté/projeté) ;
4. Deux thèmes, console propre, jeu [Exemple] enrichi pour prototyper (Q5) — le jeu
   réel reste dans le cloud, jamais en fichier ;
5. NOUVEAUTES + CHANGELOG à chaque version livrée ;
6. La donnée réelle ne quitte jamais le poste ; prototypage sur [Exemple].

## 5. Répartition d'équipe proposée (à ajuster entre nous)

- **Hermes** : couche 0 (carte + états + filtre) puis couche 1 (fiche) — ton choix
  visuel, dans le design system (Manrope/Public Sans/Plex, ambre = simultané,
  vert/bleu/gris = états de tuile) ;
- **Z Code** : couche 2 (raccord au rendu scénario existant + retour carte), les
  tests de calcul (`gainPoste`), l'A4 Mission, et la revue croisée de chaque phase ;
- **Revue croisée obligatoire** avant chaque déploiement Projet — le même pattern
  que la spec (tes réserves + mes ajouts se sont recoupés sans faille, on garde).

## 6. Points de vigilance hérités (les pièges qu'on a déjà rencontrés)

- Le nommage figé (leçon « Bol/Piste » 4.39) : la carte lit `opCode` + `LIGNES_SEPT_FONS`,
  jamais un nom de logement ;
- Les champs inconnus **survivent** aux allers-retours (Object.assign) — mais un client
  ≤ 4.46 strippera `cibleCPP` au partage : le trigger serveur
  `preserve_cibles_cpp` défend désormais (posé le 29/09, testé) ;
- `renderApresClic` pour les clics en zone de saisie (piège 4.17) ;
- Deux thèmes + impression à chaque phase ;
- Les tuiles ambre (simultané, 4.47) et le bloc groupe restent la référence visuelle
  de « ces outils tournent ensemble » — la carte doit rester cohérente avec ce code couleur.

---

*Trame Z Code v1 — 29/09/2026, sur l'état 4.50.0 (`c18fb54`). Le socle est posé, les
décisions arbitrées, les pièges cartographiés. Bon vol Hermes — revue croisée à chaque phase.*
