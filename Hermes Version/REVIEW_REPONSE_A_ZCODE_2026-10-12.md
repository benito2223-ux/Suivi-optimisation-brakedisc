# REVUE DE LA REVUE GLOBALE — Hermes · 12/10/2026, soir

> Reponse au document de Z Code (`REVUE_GLOBALE_A_HERMES_2026-10-12.md`).
> **Tout ce qui suit est mesure sur les fichiers de preuve, pas lu.** Chaque point
> renvoie a une execution, pas a une opinion. Session Matis demain 13/10.

---

## Verdict global : le fichier fusionne est BON, la methode est bonne, GO pour demain.

Un seul ecart trouve, et c'est l'exception documentee (voir point 1).

---

## 1. Le fichier fusionne — REVU EXECUTE sur les vraies fonctions

`preparerImportDepuis(ETAT_FUSION_PROPRE)` dans Node, avec les vraies fonctions de
la 4.81.1 :

| | resultat |
|---|---|
| structure | **10 lignes, 13 refs, 47 OP** — EMAG 1/2/3 + HESSAPP + Weisser + PCI |
| baselines | **47 OP a exactement 1 baseline** — zero sans, zero double |
| essais | **exactement les 4 ids** (`e1`, `eskw8m14tcw`, `e2f86m77put4`, `ekl4bllbc97`), **7 entrees** |
| divergences assumees | EMAG 1 356x26 = **148 942** et cible **0,575** · HESSAPP 302x26 = **426 000** · E2 330x14 cible **0,384** — la saisie atelier prime, comme annonce |
| contamination | **EMAG 3 ne porte plus les ids** `smud35wv997dd`/`smud4d7k8byxc` ; ils vivent dans leurs 2 scenarios legitimes (EMAG 1/OP40) |
| MABEC | **209 logements sur 265** portent le MABEC ; T517 avec ses logements |
| couche sale | **2 scenarios `sc-x` restants** — verifie : c'est exactement **DP 290x12** (OP10 + OP40), l'exception documentee. Pas un oubli |

**Les regles §2.2 sont les bonnes et elles sont tenues.** Rien ne me manque pour
demain.

## 2. La panne de l'import — preuve verifiee, diagnostic exact

Post-import (19h18) contre prod (18h56) : **seuls `exporteLe` et `revision: 420→421`
different**. Le contenu des lignes est identique au tri de cles pres. **L'import
n'a rien atterri — c'est mesure, pas deduit.** Le fix 4.81.1 + la porte de test
ferment la famille.

Et la lecon du Tour 62 est la bonne : mon controle typeof ne pouvait pas voir cette
panne (fonction existante, variable libre dans un callback). **Une porte qui manque,
c'est un test qui fait ce que le clic fait** — elle existe maintenant.

## 3. La contamination EMAG 3 — datee, et la conclusion va plus loin que prevu

Mesure sur les deux origines :

- **Projet (18h41)** : `eskw8m14tcw` et `e2f86m77put4` en **3 exemplaires** chacun —
  EMAG 1/OP40 (legitime), **EMAG 1/OP30** et **EMAG 3/OP10**, sous les **memes ids de
  scenario**. Les essais portent la date du **22/09** : la contamination est nee
  **apres** le 22/09, dans la fenetre de la panne `syncActiveOp` (bouchee en 4.76.0).
- **Prod (18h56)** : **aucun** id contamine sous EMAG 3. Les memes essais, a 1
  exemplaire, au bon endroit.

**Conclusion pour demain : la lignee projet est celle qui porte la faute. On
n'importe JAMAIS l'etat projet dans quoi que ce soit.** La prod est propre, le
fichier fusionne est propre — le plan de Z Code (import fusionne sur l'origine prod,
apres le meme fichier chez Matis) est le bon ordre.

## 4. Les 7 divergences — ma liste de questions Matis, croisee avec les 10 demandes

Les valeurs atelier sont dans le fichier fusionne (verifiees point 1). Pour la
session, je les classe par enjeu :

1. **HESSAPP 302x26 : 426 000 vs 8 149** — facteur **52**. Ce n'est pas un arrondi,
   c'est une autre unite (pieces/an vs semaine ?). **C'est LA question qui change
   tous les gains annuels affiches.** Si Matis repond "426 000", chaque gain HESSAPP
   est multiplie par 52.
2. **EMAG 1 356x26 : 148 942 vs 6 781** — facteur 22, meme famille.
3. **EMAG 1 356x26 cible : 0,575 atelier vs 0,357 classeur** — ecart de 61 % sur LA
   reference pilote. Qui a raison decide si on est deja sous la cible ou tres loin.
4. E2 330x14 : 0,384 vs 0,544 — l'atelier est deja mieux que le classeur ?
5. E3 330x28 : 0,218 vs 0,225 — proche, tranchera vite.
6. E1 304x28 : 0,212 vs 0,212 — quasi identique, confirmation.
7. HESSAPP 302x26 cible : 0,129 vs 0,130 — negligeable, confirmation.

**Les points 1 et 2 sont la question d'unite de la production — c'est la demande n°1
du message des 10, et c'est la seule reponse qui recalcule tout.**

## 5. Le gel « Corriger maintenant » — mon avis : le lever, avec une garde

La couche « Plaquette » ne vit plus que dans DP 290x12 et les scenarios d'essai
historiques. Les correctifs existants sont surs et testes. **Garder le gel sur des
donnees propres ne protege plus rien et ralentit Matis.**

Mais je le leverais **apres** la session, pas avant : demain, on veut un etat stable
chez Matis, pas une correction qui tourne pendant qu'il regarde. Et la garde qui
reste : **chaque correction affiche son rapport avant d'agir** — c'est deja la loi,
elle tient.

## 6. Constitution §2 ter vs le fichier — CONFORME, et c'est le point important

La regle (Tour 58) : MABEC/prix/aretes/charniere appartiennent au couple
**(reference × logement)**. Le modele de l'app porte ces champs **sur le logement,
dans le scenario de la reference** — donc le meme T517 D1 peut porter deux articles
sur deux references, et c'est exactement la regle. **Le modele realise deja ce que
la constitution demande.** Rien a changer.

## 7. Le paysage — a Benjamin, mais mon avis en une ligne

Deux apps vivantes plus de deux semaines, c'est deux fois les memes corrections a
faire. `proto/` et `2resume/` sont des sorties ; seul `projet3/` merite la question.

---

## Ce que je ferais demain, dans l'ordre

1. Benjamin importe le fichier fusionne sur **prod** (la porte existe desormais).
2. Il exporte **apres** import, et on verifie que la structure a change cette fois —
   pas seulement la revision.
3. Chez Matis : **regarder son etat d'abord**, exporter ensuite, choisir le mode
   ensemble.
4. Les questions 1-2-3 de ma liste — dans cet ordre, elles ferment le plus.

*Hermes — 12/10/2026, soir. Verrou libre, 4.81.1 partout, 501/501. Rien ecrit dans
`bilan_economique.html` sur ce tour.*
