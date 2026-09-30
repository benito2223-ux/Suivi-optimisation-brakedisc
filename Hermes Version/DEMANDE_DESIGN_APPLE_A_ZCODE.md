# Demande à Z Code — refonte « look Apple », police du design system

> Émise par Hermes le 30/09/2026, après la demande de Benjamin : *« je veux un outil avec
> des polices agréables, des transitions douces et un look moderne apple »*.
> **Rien n'est codé dans l'outil. Cette demande décrit un travail à faire, pas un travail fait.**

---

## 1. Le problème, mesuré — pas « c'est moche »

J'ai audité `bilan_economique.html` v4.62.0 avant de parler. Voici les faits, pas des impressions.

### 1.1 Il y a TROIS blocs `:root` dans 16 214 lignes

| Ligne | Contexte | Ce qu'il fait |
|---|---|---|
| **L48** | `<style>` principal | le thème de référence (46 variables) |
| **L1446** | dans `@media print` | version papier, 14 variables |
| **L4339** | `<style>` **à plat, sans condition** | **redéfinit 14 variables par-dessus le thème** |

**Le L4339 est le coupable.** Il est hors de tout `@media`, donc il s'applique toujours, et il
écrase le thème de référence pour le bleu, le vert, l'ambre, le rouge et leurs fonds. **Les
couleurs que je croyais mesurées au L48 ne sont pas celles que l'écran affiche.**

C'est une **guerre de tokens**, pas un design system. Et ça explique une partie du « moche » :
personne — pas nous deux, pas le générateur qui a écrit ce bloc — ne sait aujourd'hui quelles
couleurs sont réellement en vigueur.

### 1.2 Six polices déclarées pour deux usages

`Archivo`, `Manrope`, `Open Sans`, `Open Sans Condensed`, `IBM Plex Mono` — **aucune
chargée par `<link>`**, tout est en `@font-face` local. Donc **selon la machine de Matis,
l'écran n'a pas la même tête**, et nous ne le savons pas.

### 1.3 Le fond et les bordures sont presque la même couleur

`--bg: #e8eaed` / `--border: #e5e5e5`. Sur une tuile, le contour disparaît : **une surface
sans contour n'existe pas visuellement.** C'est le défaut qui fait le plus « vieux ».

### 1.4 Neuf transitions, et **aucune** là où ça compte

Aucune transition sur les cartes, les tuiles, les onglets, les champs de saisie, les
boutons de la barre. Elles existent sur quelques éléments au survol. **Un outil de travail
n'a pas besoin d'animation pour être moderne** — il a besoin que ce qu'on pointe du doigt
réagisse. L'animation, c'est l'inverse : ça fait attendre.

### 1.5 Treize valeurs de rayon, aucune rationale

`999px`, `50%`, `20px`, `8px`, `6px`, `4px`, `2px`, `var(--radius)`, `var(--radius-sm)`,
`var(--radius-lg)`… **Dix familles de formes dans un fichier** — l'accumulation de deux ans
de décisions ponctuelles, et ça se lit comme un empilement.

### 1.6 Ce qui est bon, et qu'il ne faut pas casser

- **Contraste : 5,0:1 à 7,6:1** partout. Conforme AA. Ce n'est **pas** un problème de
  lisibilité, et il ne faut pas le « corriger » ;
- les angles quasi droits, le mono sur les chiffres, le thème sombre, la barre de tuiles
  fonctionnelle — tout ça marche.

---

## 2. La cible : « Apple », mais **atelier**

Benjamin a demandé un look moderne Apple. Il faut nommer la tension, parce qu'elle est
réelle : **le look Apple suppose des cartes à 14 px, beaucoup d'air, et de la légèreté.** Sur
un outil d'atelier, lu à 3 mètres, en fin de poste, avec des chiffres qu'on compare — 14 px
partout finit par lire « showcase », pas « outil de production ».

**La proposition : garder la grammaire Apple (typographie, espace, profondeur, mouvement
doux) et réduire le rayon.** C'est la direction qui satisfait les deux.

Et **une règle non négociable, déjà écrite dans la constitution** : une refonte ne doit
jamais diluer ce qui protège la lecture. Donc, dans les trois directions proposées, on garde
**le mono sur tous les chiffres**, **l'état nommé en toutes lettres** (jamais la couleur
seule), **l'invitation « hors n opérations non chiffrées »**, et **le regroupement des
lignes hors périmètre**.

---

## 3. Les cinq chantiers, par ordre de visible

### C1 — Un seul `:root`, et le rester

- Regrouper les 3 blocs en **un jeu de tokens unique** (racine) + un bloc strictement
  `@media print` (le papier, c'est legitimately différent) ;
- **supprimer** le bloc à plat L4339, ou le faire devenir ce qu'il est censé être ;
- **test d'acceptation** : une seule déclaration de `--blue` hors impression. C'est
  vérifiable en une ligne de shell, et ça interdit la régression.

### C2 — Deux polices, déclarées une fois

- **une sans-serif** (système : `-apple-system` / `Segoe UI` / `Inter`, avec repli sûr) ;
- **un mono** pour tous les chiffres ;
- **supprimer** les 4 autres déclarations de `@font-face` ;
- **règle** : **pas de police distante** — l'outil est hors ligne, il doit marcher sur le poste
  de Matis sans réseau. C'est une contrainte de terrain, pas un goût.

### C3 — Des contours réels, et un seul plan

- `--border` **nettement plus sombre que `--bg`** (au moins 2 tons d'écart) ;
- les cartes ont **une bordure visible + une ombre d'un pixel** (pas de carte qui n'existe
  que par son fond) ;
- **test d'acceptation** : une capture de l'écran d'accueil, en clair, à 100 % — on doit voir
  les tuiles comme des surfaces, pas comme du texte posé sur un fond.

### C4 — Le mouvement, là où il sert

- transitions **courtes (80–200 ms)** sur : survol des cartes, hover des boutons, focus ;
- **jamais** de transition sur un chiffre (un chiffre qui bouge ment sur sa valeur) ;
- `cubic-bezier` **uniforme** partout (pas 3 courbes différentes) ;
- `prefers-reduced-motion` **déjà présent** (2 occurrences) — le conserver.

### C5 — Une échelle, pas des valeurs libres

- espacement sur une base de 4 (4/8/12/16/24/32) ;
- **trois rayons** maximum (petit / normal / tuile), et **rien de rond au-delà** ;
- le mono sur les chiffres ne change pas.

---

## 4. Comment travailler — la méthode qu'on a déjà validée

1. **un chantier par commit**, chacun réversible seul (si C3 ne plaît pas, on ne le garde
   pas, sans dismantler C1 et C2) ;
2. **contre-regard à chaque étape** (la règle du §6 de la constitution) : casser la règle,
   vérifier qu'un test la voit, restaurer, **vérifier octet pour octet** ;
3. **aucune fonction nouvelle** dans ces chantiers — c'est de la peau, pas du métier. Les
   tests métier (actuellement **351**) ne doivent **pas bouger** : s'ils bougent, c'est
   qu'on a touché au moteur, et c'est interdit dans ce chantier ;
4. **capture d'écran avant/après** pour chaque chantier, dans les deux thèmes, à 100 % et à
   360 px.

---

## 5. La demande à Benjamin, et ce qui n'est pas tranché

Je n'ai pas de maquette à faire valider : **les trois maquettes que j'ai produites
étaient jugées « moches »**, et la raison est simple — c'était de l'HTML statique écrit à la
main, sans vrai survol, sans vrai mouvement, sans vraie police système. **On ne juge pas un
look Apple sur une maquette ; on le juge dans l'outil, au navigateur.** C'est toi qui as le
navigateur, c'est toi qui fais les captures.

**Ce que je propose, donc, n'est pas une maquette mais un chantier** : C1 (les tokens) est
le premier parce que **tant qu'il y a trois `:root`, on ne sait pas ce qu'on est en train de
redessiner**. On ne peut pas comparer « avant/après » si on ignore l'« avant ».

**Si tu veux une capture avant de commencer** : fais une de l'écran d'accueil en clair, en
100 %, et une en 360 px. Cela fixe la référence, et on verra tout de suite si C1 et C3 font
vivre l'écran.

---

## 6. Le test de réussite, en une phrase

**Un outil d'atelier, pas une vitrine : dense sans être brouillon, net sans être froid, et
chaque chiffre aussi lisible qu'avant, en mieux.**

Si la refonte rend l'écran « plus joli » mais qu'il faut le regarder de plus près pour lire
un chiffre, c'est un échec, même si c'est belle.
