# Diagnostic design — ce qui fait « année 1990 » dans l'outil

> Mesure faite sur `bilan_economique.html` v4.62.0 (30/09/2026). Chiffres, pas impressions.

## Ce qui va déjà bien — et c'est vrai

| Point | Mesure | Verdict |
|---|---|---|
| **Contraste** | 5,0:1 à 7,6:1 sur tous les textes | ✅ conforme AA. **Ce n'est pas un problème de lisibilité.** |
| **Angles quasi droits** | `--radius: 3px`, 48 usages var | ✅ le bon registre atelier |
| **Mono pour les chiffres** | IBM Plex Mono sur les données | ✅ la bonne décision |
| **Thème sombre** | présent, cohérent | ✅ |

**Donc le reproche n'est pas un défaut d'accessibilité.** C'est autre chose, et il faut le
nommer autrement.

## Les 4 causes réelles du « 1990 »

### 1. Six polices pour deux usages

`Archivo`, `Manrope`, `Open Sans Condensed`, `Open Sans`, `IBM Plex Mono` — et aucune
chargée par `<link>`, tout est en `@font-face` local. **On ne sait même pas lesquelles sont
réellement disponibles** sur le poste de Matis, donc selon la machine l'écran change.

**Deux usages suffisent** : un sans-serif pour le texte, un mono pour les chiffres. Cinq
fontes de plus, c'est cinq rendus différents selon qui ouvre l'outil.

### 2. Neuf transitions pour tout un outil

Aucune transition sur les **cartes**, les **tuiles**, les **boutons de la barre**, les
**onglets**, les **champs de saisie**. Elles existent sur quelques éléments au survol.

Un outil de travail n'a pas besoin d'animation pour être moderne. Il a besoin que **ce qu'on
pointe du doigt change de couleur quand on le pointe** — et c'est instantané, c'est ce qui
donne l'impression deyness de réactivité. L'animation est le contraire : elle fait attendre.

### 3. Le gris `--border: #e5e5e5` sur `--bg: #e8eaed`

**Le fond et les bordures sont presque la même couleur.** Sur une tuile, le contour
disparaît, et la tuile n'est plus une tuile : c'est du texte posé sur un fond gris. C'est
le défaut qui fait le plus « vieux » : **une surface sans contour n'existe pas visuellement.**

### 4. Treize valeurs de rayon, aucune rationale

`999px`, `50%`, `20px`, `8px`, `6px`, `4px`, `2px`, `var(--radius)`, `var(--radius-sm)`,
`var(--radius-lg)`, `0 var(--radius) var(--...)`. **Dix familles de formes différentes dans
un seul fichier** — c'est l'accumulation de deux ans de décisions ponctuelles, et ça se voit
comme une falta de cohérence, pas comme un style.

## Ce que je ne changerai pas

- **les angles quasi droits** — c'est le bon registre pour un atelier ;
- **le mono sur les chiffres** — c'est ce qui rend un chiffre lisible d'un coup d'œil ;
- **les deux thèmes** — Matis travaille en atelier ;
- **le contraste** — il est bon, inutile de le casser.

## La cible que je propose

**Pas « moderne » au sens SaaS** (verre, lueur, angles arrondis) — sur un outil d'atelier,
ça fait repository et condescendant. **Moderne au sens atelier** : plat, net, rapide,
dense sans être brouillon, et **immédiatement réactif**.

Concrètement, cinq changements et rien d'autre :

1. **deux polices**, déclarées une fois, avec un repli sûr ;
2. **une échelle d'espacement** (4/8/12/16/24/32) au lieu de valeurs libres ;
3. **trois valeurs de rayon** seulement — et rien de rond au-delà ;
4. **des contours réels** : la bordure plus sombre que le fond, et une ombre d'un pixel pour
   décoller la surface du plan ;
5. **du retour immédiat** : chaque élément cliquable réagit en moins de 80 ms, et
   `prefers-reduced-motion` déjà respecté.

**Cinq changements, zéro nouvelle fonction.** Et c'est réversible ligne par ligne : si un
point ne te plaît pas, on ne le garde pas, sans dismantler le reste.
