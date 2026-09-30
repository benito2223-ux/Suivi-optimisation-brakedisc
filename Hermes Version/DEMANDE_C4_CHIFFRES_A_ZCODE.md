# Demande à Z Code — C4′ · la taille des chiffres (décidé par Benjamin le 30/09/2026)

> **Sujet** : le dernier écart qui sépare nos tuiles des écrans Stitch.
> **Périmètre strict** : la taille des chiffres et l'espace qui va avec. Rien d'autre.

---

## 0. Ce que Benjamin a tranché

> *« On garde nos deux chiffres par tuile, mais on les grossit — gain acté en 28-32 pt,
> en cours en 20-22 pt. C'est le compromis : la règle §3.4 tient, la lecture devient
> immédiate. »*

**La règle §3.4 ne bouge pas** : les gains actés et projetés restent dans **deux blocs
distincts et étiquetés**, jamais sommés. On ne gagne pas de la place en cachant un chiffre,
on en gagne en cessation de le tasser.

---

## 1. Le constat, mesuré

Les écrans Stitch portent leurs chiffres à **34-38 px**. Nos tuiles sont à :

| Bloc | Stitch | Nous aujourd'hui | Cible (décision Benjamin) |
|---|---|---|---|
| gain **acté** | 34-38 px | **14-20 px** | **28-32 px** |
| gain **en cours** | (séparé) | **12-16 px** | **20-22 px** |
| libellé au-dessus | 11-12 px capitales | 10-11 px | **inchangé** |
| unité (« /pce », « €/an ») | 13-15 px, à côté | 11-12 px | **14 px, à côté du chiffre** |

Z Code avait déjà documenté cet écart au Tour 23 : *« l'écart au Stitch 34-38 px est fait
pour des cartes plus grandes »*. **C'est vrai, et c'est pourquoi le chantier ne consiste pas
à gonfler une police** — il faut de la place, donc de l'espace.

---

## 2. Ce qu'il faut faire

### 2.1 Les chiffres

- **gain acté : 28-32 px**, poids fort, mono, `tabular-nums` ;
- **gain en cours : 20-22 pt**, dans son propre bloc, avec son étiquette ;
- **l'unité à côté du chiffre** et à la bonne taille relative (14 pt pour `/pce`) — jamais
  collée au chiffre en petit, illisible ;
- l'alignement reste **stable** quand le chiffre change : mono + `tabular-nums`, c'est déjà
  le cas, ne pas le casser.

### 2.2 L'espace qui va avec

Un chiffre à 30 px dans une carte prévue pour 14 px **déborde ou écrase ses voisins**. Donc
simultanément :

- **la hauteur des deux blocs de gain augmente** proportionnellement, et l'écart entre le
  chiffre et son étiquette aussi** — pas juste la taille de la police ;
- **la marge de la tuile reste celle du DS B** (pas de gonflement générique) : c'est
  `--radius: 2px`, `--white` sur `--gray-100`, et ça ne change pas ;
- **si l'alignement casse à 360 px, on remonte la taille d'un cran** plutôt que de
  comprimer le texte. Le mobile passe avant le desktop pour la lisibilité.

### 2.3 Ce qui ne change pas

- **deux blocs, deux étiquettes** (§3.4) ;
- **l'état en toutes lettres** à côté de la pastille ;
- **« hors n opérations non chiffrées »** sous le coût (§3.2) ;
- **la tuile hors périmètre** telle quelle ;
- **le mono sur tous les chiffres**.

---

## 3. Le test d'acceptation, et il est mesurable

Ce chantier est visuel, donc il faut une **mesure**, pas une impression :

1. **capture de l'écran d'accueil** en clair et en sombre, à 100 % et à 360 px ;
2. **aucun débordement** : le contenu de la tuile ne doit pas dépasser la carte, ni à 100 %
   ni à 360 px (mesurable dans le harnais de rendu, pas seulement à l'œil) ;
3. **la hauteur de la tuile** doit rester comparable entre les quatre tuiles vivantes — sinon
   la grille se décale et on revient a un decalage de grille ;
4. **351/351 toujours** — aucun calcul n'est touché. Si un chiffre change, c'est qu'on a
   cassé le moteur : ce chantier est de la peau.

---

## 4. Méthode (inchangée, §6 de la constitution)

- **un commit**, réversible seul ;
- **contre-regard** : la règle protégée ici est « deux blocs, jamais sommés » et « pas de
  débordement ». Casser l'une, vérifier qu'un test la voit, **restaurer par copie
  sauvegardée** (règle 7), **vérifier octet pour octet** (règle 8) ;
- **rien vers la prod** : projet d'abord, prod sur feu vert de Benjamin.

---

## 5. La phrase à retenir

**On grossit le chiffre, on ne retire pas l'information.**
Un outil d'atelier qui cache un chiffre pour qu'il rentre, c'est un outil qui ment sur ce qu'il
sait. La place se gagne en réorganisant, pas en supprimant.
