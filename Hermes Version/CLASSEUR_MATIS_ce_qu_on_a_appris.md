# CLASSEUR MATIS — ce qu'on a appris en le lisant (29/30/09/2026)

> Source : `SUIVI DES CONSOMMATIONS LIGNES EMAG - 14-09-26 au 21-09-26.xlsm` (42 feuilles).
> Lecture seule, le fichier ne quitte pas le poste. Ces quatre points sont **des faits mesurés**,
> pas des hypothèses : chacun se vérifie en ouvrant le classeur.

---

## 1. Un MABEC = un article = un logement

**Une ligne du classeur = un logement** de notre modèle (une plaquette, un prix, une DDV).

C'est confirmé par la structure elle-même : sur l'EMAG 1 / 356x26 / OP10,

| Ligne Excel | Outil | Article | MABEC |
|---|---|---|---|
| L4 | T517 **D2** | CNGX 120716 S02020 CBN387 | IM02 209 560 |
| L5 | T519 **D2** | CNGX 120716 S02020 CBN387 | IM02 209 560 |
| L8 | T517 **D1** | SNGX 120716 S02020 CBN387 | IM02 198 054 |
| L9 | T519 **D1** | *(vide)* | IM02 198 054 |

Le suffixe **D1 / D2 est le correcteur, c'est-à-dire le logement** — pas un second outil.
Et **un MABEC = un article = une plaquette** : il est normal qu'un outil porte plusieurs MABECs,
puisqu'il a plusieurs logements. **Il n'y a pas de doublon de saisie à corriger.**

> *Premier jet erroné de ma part : j'ai lu « T533 apparaissant quatre fois » comme un doublon.
> Faux. T533 = un outil à deux logements (KCK10A, KC7215), T535 = un autre outil à deux
> logements. Notre modèle « un logement = une plaquette = un prix » est confirmé correct.*

**Conséquence** : le rapprochement futur classeur → outil est direct, sans ambiguïté. Il se fera
par MABEC, et il faudra alors **ajouter le MABEC comme champ** dans notre modèle (il n'existe pas
aujourd'hui).

## 2. L'OP30 (perçage) reste partout — arbitrage Benjamin, 30/09

J'avais compris que les OP's de perçage avaient été supprimées des autres lignes : **c'est
faux, et c'est mieux ainsi.** Mesure sur le classeur :

| Couple | OP30 ? | Production | Poids du perçage |
|---|---|---|---|
| E1 356x26 RPI | oui | 6 781 | 0,051 € (8 %) |
| E2 330x14 | oui | 2 490 | 0,134 € (**28 %**) |
| E2 356x26 RPI | oui | 0 | — |
| E3 330x14 | oui | 0 | — |
| 302x26, 304x28, 290x12, 330x28 K0 | **non** | — | — |

**Décision : on garde les OP30 là où elles sont.** Raison : le **coût pièce doit rester cohérent
avec celui de Matis**. Si l'outil ignorait le perçage, son coût sur la 330x14 serait faux de 0,13 €
(28 %) par rapport au classeur — et les deux chiffres se contrediraient devant la hiérarchie.

**Aucun changement de code.** Le tour a été annulé proprement (verrou pris puis libéré).

## 3. Le rapprochement : le MABEC comme champ

Le rapprochement classeur → outil est possible **dès que le MABEC existe chez nous**. Ce n'est
pas un blocage : c'est une demande de cohérence. Deux voies :

- **import** : à l'import d'un classeur, rattacher chaque logement à son article par MABEC ;
- **saisie** : un champ `mabec` sur le logement, que Matis remplit (il connaît ses articles).

À décider quand la décision 2 version se posera (elle a besoin de 2-3 mois de mesures, pas
d'une décision aujourd'hui).

## 4. Rappel du format du classeur (pour le jour où on lira vraiment)

- 42 feuilles ; 16 feuilles « Cout pièce » = 16 couples ligne × référence ;
- 12 ont des OP10/20/40, 4 ont en plus OP30 ; 3 lignes EMAG + HESSAPP ;
- 37 outils distincts, 4 OP's (OP10, OP20, OP30, OP40) ;
- **production réelle en case B1** de chaque feuille « Cout pièce » (c'est la donnée que l'outil
  n'a pas) ;
- **CPP théorique** (colonne I) = `(arêtes × prix) / (utilisations × DDV)` ;
- **CPP réel** (colonne M) = `coût réellement consommé / production` ;
- les les nuances sont **déjà nommées SPK** dans le classeur (SN60, SL500, SL506, SL507, T00520) —
  la règle de nomenclature est tenable sans effort.

---

*Hermes — 30/09/2026. Aucune modification de l'outil dans ce tour. Les quatre points sont
vérifiables à l'ouverture du classeur.*
