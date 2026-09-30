# Demande à Z Code — C6′ · l'écran de saisie atelier (décidé par Benjamin le 30/09/2026)

> **Sujet** : l'écran de saisie des essais. C'est **le seul des quatre qui est un outil de
> travail** — les trois autres sont des tableaux de bord. C'est aussi celui que Matis ouvre
> tous les jours.
> **Périmètre** : la saisie d'essais uniquement. Trois chantiers, trois commits.

---

## 0. Ce que Benjamin a retenu de l'écran

Sur les quatre blocs possibles, il en a retenu **trois** :

1. ✅ **la barre de contexte en 4 étapes** (ligne → référence → opération → scénario) ;
2. ✅ **les conditions de coupe en cartes par poste** (2×2), avec un verdict par poste ;
3. ✅ **l'historique des essais en tableau** ;
4. ❌ **la métrologie en 3 cartes** — *pas dans ce lot* (voir §5, c'est peut-être une erreur).

Et il a corrigé le vocabulaire, ce qui est plus important que la mise en forme.

---

## 1. Le vocabulaire — à écrire dans la constitution (le vrai écart)

La constitution écrit : *« Prélèvement métrologique (DTV, rugosité Ra, voile) »*.

**Benjamin, le 30/09 :**
> « on garde les noms de notre outil : **battement**, **Ra** et **épaisseur piste** ; à limite
> on ajoute **convexité**, **face**, **appui** »

Donc la métrologie d'atelier, c'est :

| mesure | unité usuelle | remarque |
|---|---|---|
| **battement** | mm ou µm | ce que la constitution appelle « DTV » — **à corriger** |
| **Ra** | µm | identique dans les deux vocabulaires |
| **épaisseur piste** | µm ou mm | ce que la constitution appelle « voile » — **à vérifier** |
| **convexité** | — | à ajouter |
| **face** | — | à ajouter |
| **appui** | — | à ajouter |

**⚠️ Une ambiguïté à trancher avant de coder** : « face appui » est-il **une** mesure
(la face d'appui) ou **deux** (face + appui) ? Ne pas deviner — demander à Benjamin ou à
Matis. Le code ne doit pas figer un vocabulaire qui n'est pas le sien.

**Pourquoi c'est le point le plus important de ce tour** : c'est exactement la maladie de
septembre — « EMAG 1 j'ai T517 D2… et les outils configurés ne correspondent pas ». Un mot
de document qui n'est pas le mot de l'atelier coûte une journée. **La constitution doit
parler comme l'atelier, pas comme un rapport.**

---

## 2. C6′-a — La barre de contexte en 4 étapes

**Le manque, et c'est le reproche de septembre** : *« quand tu veux une information, tu
dois réfléchir »*. Aujourd'hui, avant de saisir, on ne sait pas explicitement **où l'on est**.

En tête de la saisie, une barre en 4 segments, chacun avec son numéro, son libellé en petites
capitales, et sa valeur **avec l'icône de modification à côté** (pour signaler que c'est
choisisseable) :

```
01 / LIGNE MACHINE      → 02 / RÉFÉRENCE PIÈCE    → 03 / OPÉRATION GAMME   → 04 / SCÉNARIO NUANCES
    EMAG 1 · Bi-broche       DV 356x26 RPI            OP10 Ébauche & Finition   SPK v3 (SH20+WG300)
```

**Règles :**
- **ce sont des liens, pas du texte** : un clic mène à la liste des valeurs réelles de ce
  niveau. Jamais un champ libre — une saisie libre ici réintroduirait le désordre que la
  constitution §5.2 interdit ;
- **le nom du scénario en bleu** s'il existe, sinon « aucun scénario de comparaison » — dit,
  pas supposé ;
- **verrou visible** : si le scénario est verrouillé en production, un cadenas **et le mot**
  « verrouillé ». Jamais l'icône seule ;
- c'est **un repère, pas un formulaire** : la saisie réelle reste plus bas.

---

## 3. C6′-b — Les conditions de coupe en cartes par poste

**Ce qui existe déjà** : la composition du scénario, avec VC, f, ap par logement, et l'usure
(VB). **Ce qui manque** : la présentation en cartes **avec un verdict par poste**.

En 2×2, une carte par poste déclaré de l'OP :

```
POSTE T01              POSTE T02  [Simultané T01]
Face Cloche · Ébauche  Face Jante · Ébauche
Plaquette SPK SH20     Plaquette SPK SH20
VC 850  F 0,35  AP 2,2 VC 850  F 0,35  AP 2,0
────────────────────   ────────────────────
Usure dépouille VB :   État arrêté :
0,12 mm à 140 pcs      Régulière / Pas d'écaillage
```

**Règles :**
- **le bandeau du bas est un fait mesuré, pas une formule** : si la donnée n'existe pas, il
  dit **« usure non relevée »** — jamais rien (§5.6) ;
- **« Simultané T01 »** n'est affiché que si la simultanéité est **réellement déclarée** dans
  la composition, avec le libellé complet — c'est notre ambre réservé ;
- **un poste sans données chiffrées reste visible** avec « non saisi » (§3.5 : on ne cache
  pas un poste) ;
- les trois valeurs VC / f / ap sont **en mono, alignées**, parce qu'on les compare ;
- la carte est cliquable : elle ouvre la saisie de ce poste.

---

## 4. C6′-c — L'historique des essais en tableau

En pied de l'écran, un tableau des **3 derniers essais** de cette ligne :

`essai · date · nuances · temps de cycle · gain vs base · mesures · statut`

**Règles :**
- **tri stable** : du plus récent au plus ancien, une fois pour toutes ;
- **le gain en secondes est signé et coloré** (rouge = gain, noir = référence) — mais **le
  mot reste** : « −11,2 s vs base », pas juste « −11,2 s » ;
- **un statut est un mot** : « qualifié », « archivé », « étalonnage » — pas une pastille
  seule (§5.2) ;
- **une ligne sans mesure affiche « — »**, jamais 0 : une mesure non faite n'est pas nulle ;
- l'historique existe déjà dans le modèle — c'est **une mise en tableau**, pas une fonction
  nouvelle.

---

## 5. Ce qu'on ne fait pas dans ce lot — et il y en a un qui me gêne

**Le SHA-256 de session et le « lot réglé §3.4 ».** Sur la capture d'origine, l'enregistrement
affiche une empreinte de session et un badge de conformité. **C'est de la théâtre** : personne
ne vérifie un SHA dans une UI d'atelier, et ça décrédibilise tout ce qui est écrit à côté.
**3.2 reste : des mesures horodatées et datées, pas une empreinte affichée.**

⚠️ **La métrologie en cartes est refusée dans ce lot, mais je le signale** : Benjamin a
refuse la presentation (3 cartes DTV/Ra/voile) **et** donné le vrai vocabulaire dans la même
réponse. Ces deux gestes ne vont pas ensemble : si on nomme les mesures, il faudra bien un
endroit où elles se lisent. **Je le laisse à trancher plutôt que de le faire tout seul** — il
peut très bien vouloir la métrologie en tableau, ou dans la fiche d'essai qui existe déjà.

---

## 6. Méthode (inchangée, §6)

- **un commit par bloc** (a, b, c), chacun réversible seul ;
- **contre-regard** à chaque bloc : casser la règle protégée, vérifier qu'un test la voit,
  restaurer **par copie sauvegardée** (§6.7), **vérifier octet pour octet** (§6.8) ;
- **rendu mesuré** : pas de débordement à 100 % ni à 360 px ; en 2×2, les cartes de
  positions différentes ont **la même hauteur** ;
- **351 tests métier** : aucun calcul ne bouge. C'est de la mise en forme.

---

## 7. Le test de réussite

**En arrivant sur l'écran de saisie, on sait où l'on est sans rien réfléchir, et chaque poste
affirme quelque chose de vrai ou dit qu'il ne sait pas.**
