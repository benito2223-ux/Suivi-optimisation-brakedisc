# Demande à Z Code — C5′ · l'accueil en tableau de bord (décidé par Benjamin le 30/09/2026)

> **Sujet** : l'écran d'accueil n'est pas une « page plus jolie » que la grille de tuiles
> actuelle. C'est **un autre écran, avec une autre logique** — et l'écart n'est pas cosmétique.
> **Décision de Benjamin** : on adopte la structure de la page Stitch (capture
> `b9f1a8ba217f4a5aa2e4614224cdce31`), **avec nos vraies données**.
> **Périmètre** : l'accueil seulement. Le comparateur de scénarios, la saisie d'essais et le
> bilan économique ne sont pas dans ce chantier.

---

## 0. Ce qui a été vérifié avant d'écrire cette demande

La bonne nouvelle : **presque toutes les données existent déjà.**

| Besoin de la page | État dans l'outil |
|---|---|
| gain annuel par ligne | ✅ `gainLigne` |
| gain unitaire par poste | ✅ `gainPoste` |
| gain **en cours** (séparé du gain acté) | ✅ `gainProjete` — §3.4 tenu |
| coût pièce par référence | ✅ `pieceCPPComplet(ref, ligne)` |
| cible CPP + progression | ✅ cible déjà dans le modèle |
| taux horaire de ligne | ✅ `coutHoraire` sur la ligne |
| état de la ligne + prochaine étape | ✅ `etatLigne`, `prochaineEtapePoste` |
| **les personnes** (responsables) | ✅ `normalizeResponsable`, `fusionnerResponsables` |
| le bandeau d'en-tête, la barre, les actions | ✅ existants |
| **une matrice croisant toutes les OP** | ❌ **à construire** (`flatMap`, pas un modèle) |
| **les photos de machines** | ❌ **on attend Matis — emplacement prévu, pas de photo fictive** |

**Il n'y a pas de blocage de données.** C'est de la composition.

---

## 1. La structure à reproduire, bloc par bloc

### 1.1 L'en-tête de page

- **fil d'ariane** discret en haut : `parc usinage sept-fons · lignes haute cadence` ;
- **titre de page** en gros, avec le périmètre à côté en bleu : « Tableau de bord des
  lignes d'usinage » / `EMAG & HESSAPP` ;
- **sous-titre** en une ligne, en gris, qui dit ce que c'est ;
- **à droite, l'index de qualité** : la recette A2 de l'accueil, reformulée en « conforme /
  à surveiller » — **avec le mot en toutes lettres** (règle §5.2, jamais la couleur seule).

### 1.2 La barre de contexte (les 3 champs)

Sur la capture, trois sélecteurs + un bouton d'action :

| Champ | Source dans l'outil | Règle |
|---|---|---|
| statut de ligne | `etatLigne(ligne).label` | liste réelle, pas une liste libre |
| référence pièce | `ligne.references` | **les vraies références de la ligne** |
| campagne / période | **n'existe pas** | ⚠️ **ne pas inventer** — voir §4 |

Et le bouton noir à droite : l'action d'écriture la plus utile, alignée à droite.

### 1.3 Le bandeau de 4 chiffres — **le cœur du chantier**

Quatre blocs alignés sur une ligne, chacun : libellé en capitales, chiffre **28-32 px** en
mono, unité à côté, et **une ligne de contexte en dessous**.

**Les 4 blocs, et leur source — sans exception :**

1. **Économie validée** → `gainLigne.gainActe` sommé sur les lignes. *Sous-titre : le
   périmètre exact, écrit* (« sur les lignes qualifiées série »). Jamais « 100 % audité »
  sauf si on peut l'affirmer ;
2. **Ralliement cible CPP** → progression vers `cibleCPP` sur la référence dominante. *La
   barre et le reste à capter en euros, calculés — pas écrits en dur* ;
3. **Cadence** → ⚠️ **on n'a pas de cadence mesurée par ligne.** Deux options : l'afficher
   seulement si `volumeAnnuel` et `coutMachine` existent, sinon **« — cadence non mesurée »**.
   **Ne jamais l'estimer** ;
4. **Lignes en engagement** → **un compte, pas un chiffre inventé** : combien de lignes ont
   une opération active, et lesquelles. C'est une donnée de chez nous.

**Règle absolue sur ce bandeau** (constitution §5.6) : un bloc sans donnée affiche
**« — » et ce qui manque**, jamais une estimation. Le bandeau est l'endroit où l'écran
aurait le plus de temptation d'inventer.

### 1.4 Les tuiles de ligne enrichies

Garder nos tuiles (une par ligne) mais **les remplir** comme sur la capture :

| Bloc sur la capture | Notre source | État |
|---|---|---|
| badge ligne + état | `etatLigne` | ✅ |
| nom + taux horaire | `ligne.nom`, `coutHoraire` | ✅ |
| **photo de la machine** | — | ⏳ **emplacement prévu, vide** |
| pièce / matière / volume | `refDominante` | ⚠️ volume = `productionAnnuelle`, peut être `null` → « à saisir » |
| opération active | `prochaineEtapePoste` | ✅ |
| **gain unitaire + gain annuel côte à côte** | `gainPoste` / `gainLigne` | ✅ |
| barre de ralliement CPP cible | cible + `pieceCPPComplet` | ✅ |
| **le contexte, en italique** | le fait le plus important de la ligne | ⚠️ voir §4 |
| signature : qui a validé, et par où on entre | `responsables` | ✅ |

**Le bloc en italique** : sur la capture, c'est une phrase de contexte
(« Coupe simultanée T01 + T02 active… »). **Chez nous, ce doit être une information
vérifiable** — par exemple le protocole en cours, ou la référence dominante avec son écart.
**Jamais une phrase d'ambiance.**

### 1.5 La matrice récapitulative des opérations — le seul vrai nouveau

Un tableau croisant **toutes les lignes × toutes leurs opérations** :

`ligne · opération · référence · gain unitaire · gain annuel · statut · porte`

C'est un `flatMap` sur `postesLigne()` + `gainPoste()`. **Pas un nouveau modèle.** Et c'est
l'écran que la hiérarchie regarde : une seule table, toutes les lignes, tous les statuts.

**Règles du tableau :**
- **§3.5** : un poste non impacté reste affiché avec `±0,000 €` — il ne disparaît pas ;
- **§3.4** : le gain annuel est celui de l'OP, jamais un cumul de projetés ;
- les statuts sont **des mots**, pas des pastilles seules ;
- **tri stable** (par ligne, puis par OP) — un tableau qui se réordonne à chaque rendu
  est illisible.

### 1.6 Le pied : les personnes et les trois actions

- **les gens** : les responsables existants, avec leur rôle. C'est la demande de septembre
  (« il doit pouvoir servir de relais, montrer qu'il travaille avec une équipe ») — elle est
  déjà dans le modèle, elle n'est juste pas affichée ;
- **trois actions** alignées à droite : bilan / export / historique. Les trois existent
  déjà comme fonctions — il s'agit de les **exposer**, pas d'en créer.

---

## 2. Ce qui ne change pas — non négociable

- **deux blocs de gain, jamais sommés** (§3.4) ;
- **« hors n opérations non chiffrées »** sous tout coût partiel (§3.2) ;
- **l'état en toutes lettres**, jamais la couleur seule ;
- **la tuile hors périmètre** (6 lignes) telle quelle, à sa place dans la grille ;
- **le mono sur tous les chiffres**, `tabular-nums` ;
- **`--radius: 2px`**, la palette DS B, la pile système ;
- **zéro dépendance réseau** (§5.5) ;
- **les 351 tests métier** : aucun calcul ne bouge. C'est un chantier de mise en page.

---

## 3. La méthode, inchangée (§6)

- **trois commits, un par bloc** : (1) en-tête + barre de contexte + bandeau,
  (2) tuiles enrichies, (3) matrice + pied. Chacun réversible seul, donc si le bandeau
  n'est pas bon, on ne le garde pas sans défaire les deux autres ;
- **contre-regard à chaque bloc** : casser la règle protégée, vérifier qu'un test la voit,
  restaurer **par copie sauvegardée** (§6 règle 7), **vérifier octet pour octet** (règle 8) ;
- **rendu mesuré** : pas de débordement à 100 % ni à 360 px, bandeau aligné sur une ligne
  (ou **explicitement** sur deux, mais alors les 4 blocs de même hauteur) ;
- **rien vers la prod** : projet d'abord.

---

## 4. Les deux pièges, dits franchement

**Le bandeau est l'endroit où l'écran aura le plus de temptation d'inventer.** Les quatre
blocs de la capture sont tous des nombres non justifiés : `84 250 €`, `88,4 %`, `92 pcs/h`,
`120 000 pcs/an` (le classeur de Matis dit **6 781**). **Chaque bloc qui n'a pas de donnée
affiche « — » et ce qui manque.** Un bandeau avec deux chiffres et deux tirets est correct ;
un bandeau avec quatre chiffres dont deux inventés est un accident.

**La campagne / période n'existe pas chez nous.** Il n'y a pas de notion de campagne dans le
modèle. **On ne l'invente pas** : soit le champ disparaît, soit il est remplacé par un filtre
qui existe (projet, ou statut). C'est une décision de Benjamin, signalée ici.

---

## 5. Le test de réussite

**On doit pouvoir ouvrir l'accueil et répondre en dix secondes à : « où en est l'atelier,
et qu'est-ce qui reste à faire ? »** — avec des chiffres qu'on peut remonter à leur source,
et des mots partout où une couleur suffirait.

Si l'écran devient plus handsome mais qu'il faut le regarder de plus près pour comprendre
où on en est, **c'est un échec.**
