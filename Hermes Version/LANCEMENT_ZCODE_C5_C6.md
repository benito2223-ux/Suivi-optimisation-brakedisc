# À Z Code — C5′ + C6′, on lance

> Deux commands, deux écrans. **Elles sont indépendantes** : tu peux commencer par l'une ou
> l'autre. Voici l'ordre que je recommande, et pourquoi.

---

## Ce que Benjamin a décidé aujourd'hui

On a regardé les 4 écrans de la proposition Google Stitch. **Deux sont retenus, et pas
parce qu'ils sont plus joli — parce qu'ils sont plus utiles.** Le reste de la suite Stitch
(chiffres inventés, photos génériques, SHA-256 de session) **ne rentre pas**, et c'est
assumé : constitution §5.6.

Les deux commandes :

1. **`DEMANDE_C5_ACCUEIL_TABLEAU_DE_BORD_A_ZCODE.md`** — l'accueil devient un tableau de
   bord (au lieu d'une grille de tuiles), avec nos données.
2. **`DEMANDE_C6_ECRAN_SAISIE_A_ZCODE.md`** — l'écran de saisie atelier : barre de contexte,
   conditions de coupe en cartes, historique en tableau.

---

## L'ordre que je recommande, et il n'est pas celui du journal

**Commence par C6′-a (la barre de contexte en 4 étapes).** C'est le plus petit des six
chantiers, c'est le plus visible, et c'est **la réponse directe au reproche de Benjamin de
septembre** : *« quand tu veux une information, tu dois réfléchir »*. Sur l'écran de saisie,
avant de saisir quoi que ce soit, on doit savoir **où l'on est**.

Puis **C5′ en entier** (c'est l'écran qu'il regarde le matin), puis C6′-b et C6′-c.

**Pourquoi pas l'accueil d'abord** : c'est le plus gros, il demande une matrice d'opérations
qui n'existe pas, et c'est celui où on a le moins de données réelles — donc celui où le
risque d'inventer est le plus élevé. Le bandeau de 4 chiffres va afficher « — » sur
plusieurs blocs tant que Matis n'a pas saisi ses volumes. **Mieux vaut le finir quand les
données sont là.**

---

## Trois choses que tu dois savoir avant de commencer

**1. Un vocabulaire vient d'être corrigé par Benjamin, et il n'est pas dans la constitution.**

La constitution écrit « prélèvement métrologique (DTV, rugosité Ra, voile) ». **Benjamin, ce
soir : « on garde les noms de notre outil : battement, Ra et épaisseur piste ; à limite on
ajoute convexité, face, appui ».**

C'est exactement la maladie de septembre (le T517 D1/D2) : **un mot de document qui n'est
pas le mot de l'atelier.** La constitution va être corrigée — **ne code pas « DTV » ni
« voile » dans du texte d'interface.** Attends ma correction avant C6′-b.

⚠️ **Ambiguïté non tranchée** : « face appui » est-il **une** mesure (la face d'appui) ou
**deux** (face + appui) ? Ne devine pas — si tu en as besoin, laisse l'emplacement et
demande.

**2. Le bandeau de l'accueil est l'endroit où on aura le plus de temptation d'inventer.**

Sur la capture Stitch, les 4 chiffres du bandeau (`84 250 €`, `88,4 %`, `92 pcs/h`,
`120 000 pcs/an`) sont **tous faux** — le classeur de Matis dit **6 781** pièces sur EMAG 1
356x26, soit un facteur 18.

Chaque bloc qui n'a pas de donnée affiche **« — » et ce qui manque**. Un bandeau avec deux
chiffres et deux tirets est **correct** ; un bandeau avec quatre chiffres dont deux
inventés est un accident. C'est écrit noir sur blanc dans C5′, et c'est la seule chose que je
voudrai recompter à la revue.

**3. Le projet Stitch propose 4 écrans, et on n'en prend que 2.**

Le « comparateur de scénarios » et le « bilan économique & livraisons » **ne sont pas dans
ce lot**. Si tu les vois dans la capture et que tu te demandes pourquoi, ils sont hors périmètre.

---

## La méthode, inchangée (§6)

- **un chantier par commit**, chacun réversible seul ;
- **contre-regard** à chaque bloc : casser la règle protégée, vérifier qu'un test la voit,
  restaurer **par copie sauvegardée** — *jamais* par `git checkout` (§6.7) — et **vérifier
  l'octet pour octet** (§6.8) ;
- **rendu mesuré** : pas de débordement à 100 % ni à 360 px ; en 2×2, les cartes de
  positions différentes ont **la même hauteur** ;
- **le test de contraste** du harnais reste vert : il lit le CSS réel du fichier ;
- **les 351 tests métier ne bougent pas.** C'est de la mise en forme. Si un chiffre change,
  c'est qu'on a touché au moteur ;
- **rien vers la prod.** Projet seulement, et le feu vert reste à Benjamin.

---

## Un mot sur ce qui a été fait aujourd'hui, parce que c'est rare

Benjamin a passé la journée à dire que l'outil « ne ressemble à rien » et il **avait
raison** : on avait posé une palette sur une grille de tuiles, et appelé ça un design
system. Les tokens étaient posés depuis la 4.63.0 et l'écran n'avait pas bougé d'un
placement.

Le vrai coup de grâce est venu du harnais : **remettre le gris des intitulés à 2,81:1 n'a
déclenché aucun échec sur 351 tests.** Une suite qui teste des fonctions pures ne voit pas
une couleur. Le harnais mesure maintenant le contraste sur le CSS réel, et il est vérifié
dans les deux sens.

**Ce que j'en retiens pour toi** : les tests protègent ce qu'on a écrit, pas ce qu'on
*croit* avoir écrit. Une valeur qui vient d'une proposition n'est pas une valeur validée
parce qu'elle est dans un fichier de spec — elle l'est quand quelqu'un l'a mesurée.

---

**Prochain tour** : à moi pour la revue croisée de ce que tu livres. Et à Benjamin pour les
deux captures manquantes (comparateur, bilan) — mais **ne les attends pas pour commencer**.

Vas-y.
