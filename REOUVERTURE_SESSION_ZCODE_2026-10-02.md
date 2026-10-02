# RÉOUVERTURE DE SESSION — Z Code · 02/10/2026 (nouvelle fenêtre)

> **À coller en tête de la nouvelle fenêtre Z Code.** Tout le contexte nécessaire pour
> reprendre au bon endroit, sans relire l'historique. La fenêtre précédente est pleine,
> rien n'y est perdu : ce document est l'état réel du chantier au moment de la coupure.
>
> Le document précédent (`REOUVERTURE_SESSION_ZCODE_2026-10-01.md`) est **obsolète sur
> un point** : il annonce que « le proto n'existe pas encore ». Le proto existe, il est
> déployé, et il attend une décision. C'est la seule chose à savoir de plus.

---

## 0. En une phrase

L'app de production est en **prod 4.58.0 / projet 4.79.0**, intacte et non écrite
depuis le Tour 53 ; à côté, un **proto de réécriture est terminé, testé (247 tests) et
en ligne** — il lit les essais déjà faits au lieu d'en redemander. **Il attend une
décision de Benjamin qui ne coûte qu'une minute**, et cette décision commande tout le
reste du chantier.

---

## 1. Le projet principal

`bilan_economique.html` — **un seul fichier HTML**, ~18 300 lignes, zéro build, zéro
SDK, offline-first, PWA, synchro cloud Supabase. Branche `dev`, HEAD `6010bb7`.

| Dépôt | Version | Règle |
|---|---|---|
| `suivi-optimisation-septfons.surge.sh` (**prod**) | 4.58.0 | **jamais sans feu vert explicite de Benjamin dans la session** |
| `suivi-optimisation-projet.surge.sh` (**projet**) | 4.79.0 | libre |
| `suivi-optimisation-projet2.surge.sh` (**proto**) | v1.0, 83 Ko | libre — ne contient que le proto |

**Règle de déploiement, non négociable** : « rien n'est déployé sans que Benjamin l'ait
vu. Projet d'abord, prod sur feu vert. » Toujours vérifier par `curl`, jamais par le
« Success! » de surge — et le `.surgeignore` doit exister : les dossiers contiennent des
données d'essais réelles qui ne quittent jamais la machine.

---

## 2. Le proto (Tour 54 — c'est ça le sujet du jour)

`proto/` — une **réécriture complète**, cinq écrans, 86 Ko. Assemblée par
`python proto/assembler.py` à partir de quatre sources lisibles. Déployée sur
**projet2**.

Ce qu'elle apporte, et que l'app de production n'a pas : le **CPP plaquettes** en
chiffre driver (`Σ prix / (arêtes × charnière)` — la seule colonne comparable au classeur
de Matis), et surtout **le CPP réellement obtenu par essai**, comparé au prévu.

**Le critère demandé au Tour 54 — reprendre les essais déjà faits — est tenu, et
largement.** Ce n'est pas une ressaisie, c'est une projection : les trois ingredients
du CPP (`prix`, `arêtes`, `charnière`) sont dans tous les exports, plus la charnière
*mesurée* par essai. Sur le vrai fichier : **3,27 Mo → 49 Ko** (1,5 %), 135 logements et
5 essais intacts. Le rapport d'import **compte et nomme** tout ce qui a été jeté
(plans de porte-outil, photos, relevés Marposs, journal de rebut).

Les trois finds du tour, à ne pas refaire :

1. **`batt` est vide sur 83 prélèvements sur 84** — EMAG 1 relève droite/gauche
   séparément. Un noyau qui ne lit que `batt` vide les écrans **sans une seule erreur
   console**. Le pont est fait : `batt`, sinon **le pire** des deux côtés, jamais la
   moyenne.
2. **Trois compteurs-annoncés comptaient l'inverse** (`manqueDe()` → `trioRempli()`).
   Le test l'a vu ; les données du site, non — elles ont le trio complet.
3. **Un test qui cherche une chaîne ne prouve pas qu'un nombre est juste.** Injecté
   exprès, l'écran affichait le CPP *prévu* au lieu de l'*obtenu* : 105 tests verts.
   Et même resserré, le test échouait encore parce qu'il visait un poste où prévu =
   obtenu. **Un test doit viser l'endroit où la distinction porte du sens.**

**Ce que le réimport a révélé que l'app ne montre pas :**

| Scénario | Prévu | Obtenu |
|---|---|---|
| EMAG 1 · OP40 · KY3500 Production | 0,2452 €/pce | **0,0797** |
| EMAG 1 · OP40 · SNGN 090416-F SL500 | 0,1735 €/pce | **0,0478** |

Gain de 3,6× sur l'outillage, invisible dans l'app de production.

---

## 3. Le protocole de travail (avant toute ligne de code)

| Fichier | Rôle |
|---|---|
| `VERROU.md` | **verrou** — un seul auteur sur `bilan_economique.html` à la fois. **Libre** en ce moment. |
| `ECHANGES.md` | **journal commun** — chacun écrit son tour **en haut**, signe, date. Un tour = un commit. |
| `CONSTITUTION_SUIVI_v1.md` | **les règles**. Points chauds : §3.1 source unique, §3.2 déclarer le non chiffrable, §3.4 additionner des gains interdits, §3.5 aucun chiffre mensonger, §2 quater les deux axes CPP, §6 gouvernance, §7 versions. |

Le Tour 54 a élargi le verrou à `proto/`. Empreinte de `bilan_economique.html` à
connaître avant d'y toucher : `bf2e81a3998d4d9721c728eaaf666d1f7137fe1a5e5ea651440a65ea4eaf97ca`.

Contraintes permanentes : ne jamais déployer en prod sans ordre ; ne pas cliquer
« Corriger maintenant » (gel d'audit) ; le classeur Excel de Matis se lit **en local
uniquement** (constitution §4.2) ; K et P_req **jamais** en sortie visible ; « Field
Operations Suite », jamais « CRM » ; ne jamais citer la vente de la division SPK.

---

## 4. Ce qui est en attente, et de qui

**De Benjamin — le goulot, rien ne le débloque :**

> **Sur le même fichier, les deux « où en est-on » : tu lis le proto en dix secondes,
> ou tu le refermes ?**

Le proto gagne → il devient la base, on migre écran par écran (le noyau est déjà propre
et testé). Le proto perd → il reste un banc d'essai, l'app de production continue.
**Dans les deux cas, on ne garde pas les deux en vie plus de deux semaines.**

*Si le proto gagne, première chose à examiner :* ce qu'il ne montre pas encore —
**temps machine, rebut, pièces détachées**. Délibéré (ce ne sont pas des chiffres
comparables au classeur), mais Detlef peut les attendre.

**De Hermes :** la revue de la vue CPP 4.78.0, toujours pas écrite.

**De Matis :** le dépôt de ses données réelles dans le cloud. Le cloud est **vide** —
le dépôt initial passe uniquement par le bouton « Déposer ce suivi ». Ne jamais pousser
le jeu [Exemple].

**Chantiers ouverts sur l'app de production :** les trois clics morts (import livraison,
upload photos machines, `missionA4HTML()` — le bouton existe, la fonction n'existe pas) ;
le contrôle `typeof` du harnais qu'Hermes a abandonné ; Q13 (sélecteurs barre d'accueil)
⏳ à trancher.

---

## 5. Comment reprendre, concrètement

1. Lire dans cet ordre : `VERROU.md` → les 2 derniers tours en tête de `ECHANGES.md` →
   la constitution → `proto/README.md`.
2. Vérifier l'état du proto : les trois tests doivent afficher **64 + 78 + 105 = 247,
   0 échec**. Pour l'app de production : `python build_harness.py` puis
   `node "$TEMP/h451.js"`.
3. **Si le prochain travail est du code** : prendre le verrou, écrire, commiter (un tour
   = un commit), libérer le verrou, **déployer Projet seulement**, vérifier par `curl`.
4. **Si c'est de la revue** : ne rien écrire dans `bilan_economique.html`, rendre la
   revue à Hermes.
5. Avant de livrer : **contre-regard** — casser volontairement la règle protégée,
   vérifier qu'**un** test la voit, restaurer **par copie sauvegardée** (jamais
   `git checkout`), revérifier par `sha256sum`.

---

## 6. Ce qu'il ne faut surtout pas faire

- Ne pas déployer en prod sans la phrase de Benjamin dans la session.
- Ne pas deployer le proto avec le dossier entier : `proto/.surgeignore` est une liste
  blanche stricte (`*` puis `!index.html`), comme celui de la racine.
- Ne pas réintroduire une vérification par **présence de chaîne** là où il faut lire la
  **valeur** — c'est la panne que le Tour 54 a laissée passer 105 fois.
- Ne pas considérer un harnais qui ne peut pas atteindre une porte comme une couverture :
  le Tour 54 a eu 105 tests verts sans qu'un seul n'ait fait tourner l'import.
- Ne pas commiter un contrôle qui n'a pas été vérifié en exécution ; ne pas ajouter au
  journal sans avoir relu l'ancre d'insertion.

---

*Transmis par Z Code le 02/10/2026 — HEAD `6010bb7`, prod 4.58.0 / projet 4.79.0,
proto v1.0 (247/247), `bilan_economique.html` intact, verrou libre.*