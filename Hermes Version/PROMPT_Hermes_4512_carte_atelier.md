# PROMPT POUR HERMES — 4.51.2 : la carte atelier (couche 0) + décision (a)

> **De** : Benjamin · **À** : Hermes · **Validé par** : Z Code (revue croisée 4.51.0 +
> avis sur `VERIF_revue_ZCode_4510_Hermes.md`)
> **Branche** : `dev` · **Déploiement** : `suivi-optimisation-projet.surge.sh` UNIQUEMENT
> (la prod ne bouge pas sans ma validation explicite)

---

## 1. Ce qui est acté — lance-toi

1. **Ta revue est validée** : le §4 (défaut `pieceCPPComplet` — repli silencieux sur la
   ligne active, écart mesuré ×19) est réel. **Décision : option (a)** — documente la
   règle dans les deux modules (« le coût machine exige la ligne du poste ;
   `pieceCPPComplet` ne s'appelle qu'en contexte référence ouverte — la carte et l'A4
   consomment `gainPoste` »), zéro changement de comportement dans cette version. Le
   §3.1 est clos : reporté au test d'affichage de la 4.51.2, comme tu l'as proposé.
2. **Décisions H1 et D4 arbitées** (mes choix, voir §3) : la carte est un **bouton
   toolbar « Carte atelier » à côté du tableau de bord** pour cette version (l'écran
   d'entrée par défaut se décide après la recette A2), et l'**A4 Mission suit** avec la
   même source de données.
3. **Étendue exacte de cette version** : la **4.51.2 — la carte (couche 0, lecture
   seule)** + la décision (a). Touche à rien d'autre ; le rituel complet s'applique.

## 2. Rappels des décisions déjà arbitrées (à ne pas renégocier)

- Topologie **dérivée par `opCode`** (posé en 4.50, `normalizeOp`) + machines déclarées
  dans `LIGNES_SEPT_FONS` (posé en 4.50 — Weisser/PCI vides = à compléter par
  l'atelier, ne pas inventer) ;
- **H1 = (b)+(a)** : la carte s'ouvre sur le **projet actif** (tuiles utiles), « toute
  l'usine » est un clic ; une référence avec `cibleCPP` mais sans mesures = tuile
  **« à chiffrer »** (invitation, pas un gris mort) ;
- **Pouls = acté / potentiel** (+ « en cours » seulement s'il existe un essai ouvert) —
  D2 tel qu'amendé entre nous ;
- **D3 durci** : la carte ne montre rien que le bandeau du scénario ne montre pas, et
  tous les gains passent par `gainPoste` (4.51.0) → `bilanAnnuel` → `perimetreCompare` ;
- **A2 — seuil de recette** : ≥ 1/3 des tuiles actionnables sur le jeu 2026/2027, à
  mesurer et consigner à la livraison ;
- **Ambre = simultanéité** (4.47) : si un poste porte des outils simultanés, la fiche
  couche 1 le dira avec le même code couleur (pas de nouvelle couleur) ;
- **Pas de K/P, jamais** — la carte est présentable en réunion (A4 d'Hermes).

## 3. Le contenu de la 4.51.2 (ta spec §4, Phases 1 et 2 de la trame)

### Décision (a) — deux commentaires + une règle écrite
Dans `gainPoste` (ton code, déjà juste) et dans `pieceCPPComplet` (4.49) : ajouter le
contrat « le coût machine exige la ligne du poste — `pieceCPPComplet` ne s'appelle qu'en
contexte référence ouverte ; la carte et l'A4 consomment `gainPoste` ».

### La carte (couche 0, lecture seule)
- **Panneau `cartePanel`** (mécanique `ouvrirPanneau`), bouton toolbar **« Carte
  atelier »** à côté du bouton Tableau de bord ;
- **Tuiles = (ligne déclarée × machine déclarée)** de `LIGNES_SEPT_FONS` — l'usine
  entière est dessinable ; l'état par tuile vient de **`etatTuile(gainPoste(ligne,
  opCode))`** (4.51.0) :
  - **vert « gagné »** : gain acté (scénario en série) — afficher le €/an acté ;
  - **bleu « en cours »** : essai ouvert ou gain projeté — afficher le €/an projeté ;
  - **ambre « à chiffrer »** : la référence dominante porte une `cibleCPP` mais rien
    n'est mesuré — invitation à compléter la prod ;
  - **gris « opportunité »** : rien de tout cela (poste déclaré, jamais travaillé) ;
- **Multi-références** : réf. dominante (volume de série) + compteur « +n réf. » ;
- **Filtre sur la carte** : « mon projet / toute l'usine » — défaut = le projet actif ;
- **Design system** : Manrope (nom du poste), Plex Mono (chiffres), Public Sans (état) ;
  ambre réservé à la simultanéité ET à l'appel « à chiffrer » est toléré mais
  documente-le si tu l'utilises — sinon prends la famille bleu/gris ;
- **Double geste (R3)** : la tuile de la carte ouvre directement la couche 2 (fiche) ;
  la fiche couche 1 porte le bouton « Ouvrir le poste → » — même contenu, deux gestes,
  et le bouton explicite rend le geste découvrable.

### La fiche poste (couche 1) — incluse, c'est la porte du couche 2
- **Fiche** : réf. présentes (dominante + « +n »), série vs essai, gain du poste
  (acté/projeté), prochaine étape du plan, **bouton « Ouvrir le poste → »** qui
  positionne `activeLigneId/activeReferenceId/activeOpId` et rend le scénario
  (navigation experte existante) ;
- **Retour carte** : bouton permanent depuis la fiche et la couche 2 (jamais de
  cul-de-sac — A1 d'Hermes).

## 4. Ce que Z Code fera en parallèle (ne pas traiter dans cette version)

- **Couche 2** : le raccord du rendu scénario existant + retour carte (A1) ;
- **A4 Mission** : consommera `gainPoste` (sûr par construction) — jamais
  `pieceCPPComplet` hors contexte ;
- **Revue croisée de ta 4.51.2** à la livraison (seuil A2, états `etatTuile`, filtre,
  deux thèmes, console).

## 5. Rituel (le nôtre, inchangé)

1. Branche `dev`, un commit par version livrée ;
2. **Tests verts** (246 aujourd'hui — ajoute les tests de la carte : comptage de
   tuiles par opCode, états `etatTuile` sur le jeu 2026/2027, filtre projet) ;
3. Deux thèmes vérifiés, console propre ;
4. NOUVEAUTES + CHANGELOG + TOOL_VERSION (**4.52.0** pour la carte, ou 4.51.2 si tu
   préfères garder la carte en 4.51.x — ton choix, annonce-le dans le commit) ;
5. **Déploiement Projet seul** + vérification curl ;
6. Je fais la revue croisée avant tout passage vers main.

---

*Préparé par Z Code sur la base de la spec croisée v1/v2, de la revue 4.51.0 et de la
vérification Hermes. Go pour la carte, bro.*
