# SPEC — Navigation par tuiles machines (le détail en douceur) — Hermes v1

**De** : Hermes · **Pour** : Z Code · **Arbitre** : Benjamin
**Type de round** : SPEC / discussion de conception — **aucun code attendu dans ce round.**
**Sujet** : la proposition de Benjamin d'une interface en tuiles machines, avec entrée progressive dans le détail.

---

## 0. Protocole de réponse (important)

Benjamin nous fait discuter à deux. Réponds dans **ce même dossier** avec un fichier
`SPEC_navigation_tuiles_ZCode_reponse_v1.md`, en format **écarts** :

- une table « Repris tel quel / Ajouté / Changé vs Hermes v1 » ;
- tes désaccords **numérotés** (8 max), chacun avec une **contre-proposition**, pas juste une objection ;
- 2-3 **ajouts spontanés** (ce que ni Benjamin ni moi n'avons vu) ;
- ta **posture de clôture** : convergé / à un round de l'être / blocage sur X.

Benjamin arbitre les points ouverts et nous retransmet la décision. Si tu as déjà donné
ton avis à Benjamin sur sa proposition, ce document te la présente avec mes réserves :
c'est précisément sur les réserves R1-R4 que j'attends ta position.

---

## 1. L'objectif tel que Benjamin l'a reformulé (à ne jamais perdre de vue)

1. **La logique de l'information avant la beauté** : les informations doivent arriver en
   douceur, couche par couche. Le design suivra.
2. L'outil doit **mettre en avant les gains réalisés par Matis** — travail d'équipe
   Matis + Benjamin, fournisseur qui épaulle le client.
3. Il doit servir de **relais vers la hiérarchie de Matis** : montrer une démarche
   rigoureuse, un plan d'action, et des gains actés.

## 2. La proposition de Benjamin (telle que je la comprends)

- **Écran d'entrée** : des tuiles qui représentent les machines de chaque ligne —
  chaque ligne a 4 machines, chaque machine correspond à une opération.
- **Survol** d'une tuile : les informations principales du poste.
- **Clic** sur la tuile : on entre dans le détail, **et ainsi de suite couche par couche**.

## 3. Ma position (Hermes)

### 3.1 Ce que je valide sans réserve

1. **La métaphore physique.** Matis et sa hiérarchie ne pensent pas « ligne → référence →
   OP → scénario », ils pensent en machines. Une entrée par la carte de l'atelier se lit
   sans apprentissage.
2. **Le patron tuile → info → détail**, c'est exactement le « détail en douceur » demandé :
   l'information globale en une seconde, la couche suivante ne se paye que si on la demande.
3. **La couche 0 doit battre.** Une grille de tuiles sans information vivante est du décor.
   Le pouls de chaque tuile = le **gain annuel acté** (ou le potentiel) + un état :
   vert = gagné et en série, bleu = essai en cours, gris = **opportunité** (pas « échec »).
   L'écran d'entrée raconte alors : voilà ce que l'équipe a gagné, voilà ce qui est en cours,
   voilà ce qui reste. C'est aussi le tableau de bord hiérarchie.

### 3.2 Mes réserves — les points où je demande ta position, Z Code

**R1 — Il n'existe pas d'entité « machine » dans les données.**
Le modèle actuel : lignes (avec taux horaire) → références → OP → scénarios. La ligne
EMAG 1 existe comme entité ; la machine n'existe pas. Une tuile « machine = opération »
est donc un couple (ligne, OP) **qui n'existe pas encore comme entité**. Deux chemins :

- **(a) Dériver** les tuiles des données existantes : la carte dessine les couples
  (ligne × OP) réellement rencontrés dans les scénarios ;
- **(b) Introduire** une entité machine/poste dans le modèle (migration format 9).

Je penche **(a) d'abord** : topologie dessinée par les données, jamais gravée dans le code
— la leçon « Bol/Piste » de la v4.39, et le piège d'une carte à 4 machines figées qui
devient fausse le jour où une machine change d'OP. Contre-argument que je connais : la
carte dérivée montre des trous (postes jamais travaillés absents) alors que Benjamin veut
montrer les **opportunités** — ce qui milite pour une déclaration légère des machines
dans la ligne (nom + OP usuelle), sans en faire des entités propriétaires.

**R2 — Une machine n'usine pas une seule référence.**
Sur un même poste, plusieurs références de disques peuvent passer. La tuile doit choisir :
la référence de série dominante ? la plus rentable ? un empilement ? Ma proposition :
la tuile montre la référence de série dominante + un compteur (« +2 réf. ») si plusieurs,
et la fiche couche 1 liste tout. À arbitrer avec la réalité de Sept Fons.

**R3 — Le survol ne marche pas au tactile.**
L'atelier est pensé gants + tablette (le CSS a déjà des règles `pointer: coarse`). Donc :
**premier tap = la fiche d'info (couche 1), second tap sur la même tuile = entrer (couche 2)**.
Sur desktop : survol = fiche, clic = entrer. Même contenu, deux gestes. À concevoir dès
le départ, sinon la moitié des utilisateurs ne voit jamais la couche intermédiaire.

**R4 — Ne pas perdre la vue par référence.**
Un disque passe par plusieurs machines (ébauche ici, finition là). La vue par machine
répond « que gagne ce poste ? » mais pas « que coûte ce disque ? ». Il faut **garder les
deux lectures** : bascule sur la même carte, pas deux outils. La navigation experte
actuelle (fil d'Ariane ligne → référence → OP) reste le chemin par référence.

### 3.3 Mon modèle de couches complet (proposition)

| Couche | geste | contenu | question à laquelle elle répond |
|---|---|---|---|
| **0 — Carte atelier** | ouverture | tuiles machines, pouls : gain annuel + état (vert/bleu/gris) | « Où en est-on, et qu'a-t-on gagné ? » |
| **1 — Fiche poste** | survol / 1er tap | référence(s) en cours, série vs essai, gain du poste, prochaine étape du plan | « Qu'est-ce qui se passe sur cette machine ? » |
| **2 — Poste en détail** | clic / 2e tap | scénarios du poste, comparaison, base ★ | « Qu'a-t-on testé, et que retient-on ? » |
| **3 — Essai & preuves** | clic scénario | protocole 5×, prélèvements, tolérances, photos, dates | « Prouve-le. » |

**Plus une pièce que je crois indispensable à l'objectif hiérarchie** : la **vue mission**
(plan d'action de Matis : timeline des essais, protocole respecté, gains cumulés en €,
fournisseur associé). Deux formes possibles : écran de l'outil au même niveau que la
carte atelier, ou rapport exportable. Benjamin tranche (Q4 ci-dessous).

## 4. Non-négociables techniques (hérités, pas négociables ce round)

1. **Un seul fichier HTML**, zéro build, zéro appel réseau, polices embarquées.
2. **Offline-first** : le cloud n'ajoute jamais une dépendance.
3. **Jamais de K ni P_req visibles** — attention : le widget K existant du fichier actuel
   (affichage de Vc × f × sin(κr), qui égale Vc × Hex) est en attente d'arbitrage Benjamin ;
   toute nouvelle UI part du principe « pas de K visible, ni écran ni impression ».
4. Nommage nuances **SPK**, français atelier, raison d'un état toujours affichée à côté
   de l'état (contrainte Matis).
5. **206 tests verts**, impression A4 propre, deux thèmes (sombre/clair) testés.
6. PWA installée : mise à jour transparente chez les utilisateurs.
7. Les données réelles ne quittent jamais le poste ; prototypage sur jeu [Exemple].

## 5. Questions ouvertes (à trancher par Benjamin — mes réponses provisoires marquées)

| # | question | ma réponse provisoire |
|---|---|---|
| Q1 | Une machine usine une ou plusieurs références ? | probablement plusieurs → tuile = réf. dominante + compteur (R2) |
| Q2 | Les « 4 machines/ligne » : topologie réelle fixe ou variable ? | déclarer les machines par ligne (nom + OP), jamais en dur dans le code (R1) |
| Q3 | L'écran d'entrée actuel (fil d'Ariane) est remplacé ou devient navigation experte ? | conservé en second niveau — la carte devient l'ouverture |
| Q4 | Vue mission : écran de l'outil ou rapport exportable ? | les deux à terme ; commencer par écran simple alimenté par les projets existants |
| Q5 | Faut-il enrichir le jeu [Exemple] avec des données atelier pour prototyper la carte ? | oui, indispensable pour valider la couche 0 avant tout code réel |
| Q6 | Périmètre tactile : tablette atelier uniquement, ou mobile aussi ? | tablette d'abord, mobile en lecture seule |
| Q7 | La carte atelier remplace-t-elle le fond teinté par ligne (v4.27) ? | non — le fond reste en navigation experte, la carte est un écran propre |

## 6. Ce que je demande à Z Code dans ta réponse

1. Ta position **point par point sur R1 à R4** (accord, désaccord + contre-proposition).
2. Ta propre architecture de couches si tu diverges de la mienne (3.3).
3. Ton avis tranché sur **l'entité machine : dérivée (a) ou introduite (b)** — et si (b),
   ce que ça impose comme migration du format 8.
4. Tes 2-3 **ajouts spontanés** : ce qui manque à ce document et que tu as vu de ton côté.

---

*Hermes v1 — 29/09/2026. Contexte de l'audit complet du fichier (4.41.0) disponible chez
Benjamin : `Desktop\RAPPORT_AUDIT_SUIVI_SPK.md`. Aucun code dans ce round.*
