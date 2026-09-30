# LE CLASSEUR MATIS — lecture en profondeur · ce que l'outil ne sait pas encore

**Source** : `C:\Users\Admin\Downloads\SUIVI DES CONSOMMATIONS LIGNES EMAG - 14-09-26 au 21-09-26.xlsm`
(560 Ko, 42 feuilles, macros actives `.xlsm`) — **lecture seule, analyse seule, rien n'est écrit,
le fichier ne quitte pas le poste** (règle de confidentialité §4.2 de la constitution).
**Date** : 29/09/2026 · **Auteur de l'analyse** : Hermes

---

## 1. Ce que le classeur est

Un **suivi de consommations réelles semaine par semaine** (14/09 → 21/09), organisé
par couple **ligne × référence**. Ce n'est pas un tableur de calcul : c'est un
**instrument de mesure du terrain**, et il sait des choses que notre outil ignore.

## 2. Les trois choses que le classeur sait et que l'outil ne sait pas

### 2.1 La production RÉELLE, chiffreée, par couple ligne × référence

Chaque feuille « Cout pièce » porte sa production en **B1** :

| Feuille | Production | Référence |
|---|---|---|
| E1 356x26 RPI | **6 781** | DV 356x26 RPI |
| E2 290x12 | **2 234** | DP 290x12 |
| E2 330x14 | **2 490** | 330x14 |
| E3 330x28 RPE K0 | **4 180** | 330x28 RPE K0 |
| H 302x26 RPI | **8 149** | DV 302x26 RPI |
| *(les 11 autres)* | 0 ou vide | postes ouverts, pas produits |

**Pourquoi c'est décisif.** Dans l'outil, la production est un **scénario déguisé** : un
booléen `baseline` posé sur un scénario d'essai, et le module cherche « ★ d'abord, excel
en repli » à chaque calcul. Dans le classeur, la production est **une feuille qui existe
ou qui n'existe pas**, avec un volume réel à l'appui.

> 16 des 16 couples ligne × référence sont **déjà modélisés** dans l'outil, mais avec des
> `productionAnnuelle` soit vides, soit estimées. **Le classeur est la source de vérité
> de ce champ** — et de tous les autres.

### 2.2 Le CPP réel par outil et par opération — le « Réel / Théorique »

Chaque ligne de chaque feuille donne, par outil et par OP :

| Champ | Colonne | Formule lue dans le classeur |
|---|---|---|
| Nb d'arêtes | E | — |
| Prix UHT outil neuf | G | — |
| DDV actuelle (durée de vie) | H | — |
| **CPP actuel** (théorique) | I | `=(E×G)/(F×H)` |
| **Qté théorique** | J | `=ROUNDUP(E×$B$1/(F×H),0)` |
| **Coût réel consommé** | L | `=N×G` |
| **CPP réel consommé** | M | `=L/$B$1` |
| **Qté réelle** | N | `SUMIFS('Tableau plaquette complet'…)` |
| **Écart** | O | `=-(K−N)` |

**C'est exactement la comparaison que notre outil ne fait pas** : lui calcule un coût
*théorique* à partir des prix et des durées de vie saisies ; le classeur calcule le coût
*réellement consommé* sur la semaine, et affiche l'écart. Sur l'OP10 de la 356x26, la
plaquette `Z000 544 318` est budgétée 23, va costing 90 consommés, soit un écart de +67.

**C'est un gainstalgie :** nos tuiles de la carte montrent le gain *théorique* d'un
changement d'outillage. Le classeur montre ce que ce changement a **coûté en plus cette
semaine**. Les deux ensemble, c'est la preuve que le gain est réel — et c'est
précisément ce que la hiérarchie demande.

### 2.3 Le périmètre réel de l'atelier

- **3 lignes** (E1, E2, E3) + HESSAPP (H)
- **6 références** : 290x12 · 302x26 RPI · 304x28 RPE · 330x14 · 330x28 RPE K0 · 356x26 RPI
- **4 OP** : OP 10, OP 20, OP 30, OP 40
- **37 outils distincts**, avec **numéro MABEC** (la référence article, le repère de l'atelier)
- **Codes articles** : `CNGX/SNGX/CNGM/SNMX/SNGN/RCGX/TNGN/…` + nuance SPK
  (`SN60`, `SL500`, `SL506`, `SL507`, `T00520`) — le classeur **nomme déjà les nuances
  SPK**, la règle de nomenclature est donc tenable sans effort.

**L'outil ne connaît ni les numéros MABEC, ni les codes articles.** Ce sont les identifiants
que Matis utilise au quotidien : « le T533, c'est du KTFSS7041640FEG, article IM02… ».

## 3. Ce que l'outil a déjà, et ce que le classeur apporte en plus

| Ce que l'outil sait | Ce que le classeur apporte |
|---|---|
| prix, arêtes, DDV, CPP théorique | + CPP **réel**, écart consumption, volume **réel** |
| essais, tolérances, photos, Marposs | + **numéro MABEC**, codes articles, quantités semaine |
| le « pourquoi » (essais, preuves) | le « combien réellement » (le terrain) |
| la méthode (protocole 5×) | la **production réelle** par couple ligne × référence |

**Le classeur et l'outil sont complémentaires, pas concurrents.** L'outil dit *pourquoi on
change* et *avec quelle preuve* ; le classeur dit *ce que ça a réellement coûté*.
Réunir les deux, c'est passer d'un carnet d'essais à un **système de pilotage**.

## 4. Ce que ça change pour la décision 2 (la prod comme entité)

**La décision 2 change de nature.** Ce n'est plus « inventer un statut production » : c'est
**« la production est une donnée réelle, chiffrée, venue du terrain »**. Le scénario-★
devient une **référence de comparaison** (ce contre quoi on mesure), et la production
réelle devient une **donnée à part** — volume, CPP réel, écart.

C'est plus propre que ce que je proposais, et c'est vérifiable : chaque nombre du
classeur est **auditable jusqu'à sa formule**.

## 5. Ce que je propose — trois options, aucune décidée par moi

**(a) Import one-shot, sans changement de modèle.** Un bouton « importer le classeur
Matis » qui lit les feuilles « Cout pièce » et remplit la production réelle, le CPP réel
et les numéros MABEC. Modèle inchangé, données réelles enhance. **Le plus rapide, le
moins ambitieux.**

**(b) La production devient une entité, alimentée par le classeur.** `productionReelle` par
couple ligne × référence, avec volume et CPP réel ; le scénario-★ devient la référence
de comparaison. C'est la décision 2 Version, et elle a maintenant une source.

**(c) D'abord mesurer l'écart.** Import (a) + un écran « écart théorie / réel » sur la
carte, pour voir sur trois mois de données à quel point les deux divergent — et **ensuite**
décider si (b) est justifié. **C'est ma recommandation** : on ne refait pas le modèle avant
d'avoir vu les données.

## 6. Les limites de cette analyse

- Analyse **statique** : je n'ai pas exécuté les macros, ni recalculé le classeur ; les
  valeurs lues sont les **résultats en cache** (dernière sauvegarde de Matis).
- Un seul couple ligne × référence a été lu en détail (E1 356x26) ; les 15 autres ont été
  inventoriés mais pas décomposés ligne à ligne.
- Je n'ai pas vérifié si `Tableau plaquette complet` et `Tableau plaquette outil` (les
  sources des `SUMIFS`) sont **à jour** ou seulement le dernier relevé.
- Le classeur est **hebdomadaire** : il n'a pas d'historique long dans ce fichier, mais la
  feuille `Evolution coût pièce EMAG` montre un suivi **par semaine** (semaines 2 à 54).

---

*Hermes — 29/09/2026. Fichier lu en place, rien n'a été écrit ni déplacé. La décision
sur (a)/(b)/(c) revient à Benjamin : c'est un choix de méthode, pas une décision technique.*
