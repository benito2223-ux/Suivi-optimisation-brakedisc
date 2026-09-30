# Demande à Z Code — C1′ · C2′ · C3′ (décidé par Benjamin le 30/09/2026)

> **Sujet** : appliquer le design de la proposition Google Stitch à l'outil existant.
> **Périmètre strict** : trois chantiers, **un commit chacun**, et **rien d'autre**.
> **Ce document est une spec. Il ne décrit pas un produit à refaire — il décrit une peau à poser.**

---

## 0. La règle qui gouverne ces trois chantiers

> **Un chiffre qu'on ne peut pas justifier n'est pas affiché** (constitution §5.6, v1.5).

Et son corollaire pour nous : **aucune donnée de la proposition Stitch ne doit entrer dans
l'outil.** Ni `120 000 pcs/an`, ni `84 250 €`, ni `88,4 %`, ni `91,3 %`, ni `1,200 €`. Ces
valeurs sont inventées par Stitch (le classeur de Matis dit **6 781** pièces sur EMAG 1
356x26, soit un facteur 18). **On prend la forme, pas les chiffres.**

---

## C1′ — Les tokens du Design System B, tels quels

**La source** : `Hermes Version/Design_system_B.md`, section 2, bloc `DESIGN_SYSTEM_B.css`.

### Ce qu'il faut faire

1. **Un seul jeu de tokens.** Aujourd'hui il y a **trois blocs `:root`** dans 16 214 lignes :
   L48 (référence), L1446 (`@media print`), L4339 (**hors `@media`, à plat**) — et celui-là
   écrase 14 variables du thème de référence. **Le supprimer ou le faire devenir ce qu'il
   est censé être** ;
2. **Adopter les tokens** :

   ```css
   --ink: #000000;  --body: #5C5D62;  --label: #9A9A9A;  --line: #535357;
   --red: #E30045;   --red-dark: #B8003A;
   --blue: #006AB3;  --blue-light: #EAF4FB;
   --white: #FFFFFF; --gray-50: #FAFAFA; --gray-100: #F4F4F4;
   --gray-200: #E5E5E5; --gray-300: #CFCFCF;
   --green: #1A7A3F; --green-bg: #EDF7F1;
   --amber: #B45309; --amber-bg: #FFF8ED;
   --radius: 2px;
   ```

3. **Une seule famille sans-serif + le mono pour les chiffres.** Aujourd'hui **six polices
   sont déclarées** pour deux usages (`Archivo`, `Manrope`, `Open Sans`, `Open Sans
   Condensed`, `IBM Plex Mono`) — et aucune n'est chargée par `<link>`, donc **selon le poste
   de Matis l'écran n'a pas la même tête**. On garde la sans-serif du DS B
   (`Roboto, -apple-system, BlinkMacSystemFont, Arial`) **déclarée localement**, plus
   `IBM Plex Mono` pour tous les chiffres. **Les quatre autres déclarations partent.**
4. **`--radius: 2px` partout.** Aujourd'hui il y a **dix familles de formes** (2 à 999px,
   `50%`, `20px`, `8px`…). Une seule.
5. **Le `@media print` reste un cas à part** — le papier, c'est légitimement différent. Mais
   il doit venir des mêmes tokens.

### Test d'acceptation

- **une seule déclaration de `--blue` hors `@media print`** (une ligne de shell) ;
- `grep -c '@font-face'` → **2** maximum (la sans-serif si déclarée + le mono) ;
- aucun `border-radius` en dur hors token ;
- **les 351 tests métier ne bougent pas.** Si un chiffre change, c'est qu'on a touché au
  moteur — interdit dans ce chantier.

---

## C2′ — Aucune dépendance réseau

**Bonne nouvelle : l'outil est déjà autonome** (0 feuille distante, 0 police distante,
0 image distante, 0 Tailwind CDN — vérifié le 30/09). **Ce chantier est donc quasi vide, et
c'est le but** : il empêche que C1′ et C3′ introduisent une dépendance par inadvertance.

**La règle** (constitution §5.5) : ni CSS distant, ni police distante, ni image distante.
**Test d'acceptation : ouvrir `bilan_economique.html` avec le réseau coupé** et vérifier
que l'écran est complet. Si une police Google Fonts traîne encore dans une `@import`, elle
part.

---

## C3′ — La grammaire visuelle de la proposition, sur nos tuiles existantes

Trois choses, reprises des captures Stitch. **Sur nos tuiles, pas sur un écran nouveau.**

### 3.1 L'accent à gauche, 3 px

Chaque carte de l'accueil et de la carte atelier porte **un filet vertical de 3 px** à
gauche, à gauche de son contenu. C'est le détail qui fait « fait pour ça » plutôt que
« maquette ». *La couleur du filet suit l'état de la tuile, avec le mot toujours présent.*

### 3.2 La typographie des chiffres

- **le chiffre principal en gros** (34–38 px), son unité avec lui ;
- **le mono sur tous les chiffres**, aligné à droite dans les tableaux (`tabular-nums`) ;
- le libellé **au-dessus**, en petit, en capitales espacées — jamais à côté du chiffre en
 同等 poids.

### 3.3 Le mouvement, court et utile

- survol des cartes et des boutons : **80–150 ms**, `cubic-bezier` **unique** pour toute la
  grille ;
- **jamais de transition sur un chiffre** — un chiffre qui bouge ment sur sa valeur ;
- `prefers-reduced-motion` déjà présent (2 occurrences) : **le conserver** ;
- transitions sur les deux seuls éléments réversibles : **transform** et **opacity**
  (jamais `width` ni `height`).

---

## Ce qu'on NE fait pas — et c'est important

La proposition Stitch décrit **4 écrans, une matrice d'entités, un comparateur de scénarios,
des formulaires de saisie, des rapports A4**. **Rien de tout cela n'est dans le périmètre.**

- ❌ pas de comparateur de scénarios ;
- ❌ pas de matrice d'entités ;
- ❌ pas de formulaires à soulignement ;
- ❌ pas d'écran « Bilan Économique & Livraisons » ;
- ❌ pas de refonte du modèle de données.

**On habille, on n'invente pas.** Le modèle, les 351 tests et les 4.60.x sont la valeur de
cet outil ; le design est la midwife.

---

## Méthode (règles du §6 de la constitution, déjà en vigueur)

1. **un chantier par commit**, chacun réversible seul. Si C3′ ne plaît pas, on ne le garde
   pas, sans dismantler C1′ et C2′ ;
2. **contre-regard à chaque étape** : casser la règle, vérifier qu'un test la voit, restaurer
   par **copie sauvegardée** (§6 règle 7 — *jamais* par `git checkout`), et **vérifier
   l'octet pour octet** (règle 8) ;
3. **capture d'écran avant/après** pour chaque chantier, dans les deux thèmes, à 100 % et à
   360 px ;
4. **rien n'est déployé sans que Benjamin l'ait vu.** Projet d'abord, prod sur feu vert.

---

## Le test de réussite, en une phrase

**Un atelier dense et net, pas une vitrine : et chaque chiffre exactement aussi lisible
qu'avant — en mieux.**

Si la refonte rend l'écran « plus joli » mais qu'il faut le regarder de plus près pour lire
un chiffre, **c'est un échec, même si c'est beau.**
