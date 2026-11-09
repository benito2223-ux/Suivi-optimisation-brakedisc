# Refonte — l'outil cible, d'après son usage réel

Préparé le 09/11/2026. Remplace `PROPOSITION_SIMPLIFICATION_2026-11-09.md` (même direction, poussée plus loin).
Parcours fait dans Chrome sur PROD 4.150.0, sur ta session réelle (rev 436), en lecture seule :
rev 436 avant, rev 436 après, 16 essais et 192 prélèvements avant comme après. Aucun code touché, rien déployé.

Tous les chiffres de ce document sont lus dans l'outil ou comptés dans tes données. Là où je n'ai pas de chiffre, j'écris « … ».

---

## 1. Ce que l'usage dit (et que les écrans ne disent pas)

J'ai compté ce qui est réellement rempli dans tes données. C'est la meilleure mesure de ce qui sert.

### 1.1 Ce qui est rempli = ce qui sert

| Donnée | Rempli | Lecture |
|---|---|---|
| Prix d'un logement | 353 / 377 | **le socle** |
| Arêtes | 377 / 377 | le socle |
| Charnière (pièces par arête) | 310 / 377 | le socle |
| Volume annuel de la référence | 12 / 19 | le multiplicateur, incomplet |
| N° de pièce d'un prélèvement | 192 / 192 | l'atelier fonctionne |
| Battement (droite, gauche ou simple) | 73 / 63 / 20 sur 192 | la mesure qualité réelle |

### 1.2 Ce qui n'est presque jamais rempli = ce que l'outil demande pour rien

| Donnée | Rempli | Conséquence aujourd'hui |
|---|---|---|
| **Conclusion d'un essai** | **1 / 16** | aucun essai ne se termine par une décision écrite |
| But de l'essai | 7 / 16 | |
| Observations | 8 / 16 | |
| Usure plaquette sur un prélèvement | 21 / 192 | |
| Photos d'essai | 2 / 16 | « PHOTO À FOURNIR » affiché partout |
| Vc et f par logement | 38 / 377 | le temps de cycle n'est jamais calculé |
| Temps de cycle du scénario | 25 / 86 | l'axe productivité est vide |
| Taux horaire de la ligne | 4 / 11 lignes | le temps machine n'est pas chiffrable |
| Consommation réelle | absente | |
| Livraisons | 0 | écran jamais utilisé |
| Dossier de visite (dernière visite) | jamais ouvert | écran jamais utilisé |
| Projets | 1 seul | confirmé : inutile |
| Classeur Matis (Réel vs budget) | à relire à chaque session | écran vide à l'ouverture |

### 1.3 Le rythme réel

16 essais en 11 semaines, en cinq grappes : 25-26/08 (5), 22-23/09 (3), 13-14/10 (6), 02/11 (1), 09/11 (1).
L'outil vit **par campagnes de quelques jours, espacées de trois à quatre semaines**. Entre deux, personne ne l'ouvre.
Donc la première question à l'ouverture est toujours la même : **« où en était-on, et qu'est-ce qu'on fait maintenant ? »**
Aucun écran n'y répond aujourd'hui.

### 1.4 Le poids des écrans (mesuré, portable 1280 px)

| Écran | Hauteurs d'écran | Mots | Champs de saisie |
|---|---|---|---|
| Scénarios (écran de travail) | 3 | — | 81 (150 contrôles) |
| Vue d'ensemble | 4,8 | 846 | — |
| Carte atelier | 2,8 | 397 | — |
| Tableau de bord | 17,8 | 1 571 | 1 |
| Synthèse | 1,5 | 169 | 0 |
| Vue CPP | 7,5 | 1 104 | 0 |
| La campagne | 5,2 | 1 513 | 0 |
| Catalogue | 3,5 | 312 | 108 |
| **Plan de conversion** | **34,2** | **2 813** | **161** |
| Réglages | 6,9 | 970 | 20 |
| Mode atelier | 1,9 | 91 | 3 (18 contrôles) |

Le seul écran à la bonne taille est **le mode atelier**. C'est aussi le seul dont les données sont remplies à 100 %. Ce n'est pas un hasard : c'est le modèle à suivre.

### 1.5 Cinq écrans montrent la même matrice

Vue d'ensemble, Carte atelier, Tableau de bord, Vue CPP et la « feuille de route » de la Synthèse affichent tous **ligne × référence × OP → coût pièce**, avec cinq mises en page et cinq totaux. C'est le doublon central de l'outil.

### 1.6 Les contradictions vues à l'écran aujourd'hui

1. **« Économie acquise » a maintenant six valeurs** : « aucun gain acté » (Vue d'ensemble), 7 449 €/an (Synthèse et Campagne), « aucun scénario passé en série » puis −2,1 k€/an (Plan), et **+5,3 k€ « gain annuel acquis »** avec **−8,3 k€ « à déployer »** (Tableau de bord).
2. **EMAG 1 · 356x26 RPI · OP10, même écran** : en haut « 0 % — aucun scénario ne bat encore la base » ; 400 pixels plus bas, sur le scénario LKT640 : « −36,0 % de coût par pièce outil, +4,7 k€ ». Les deux sont « vrais » (bases différentes), l'utilisateur lit une contradiction.
3. **Même scénario** : statut « Validé », jauge « 1 / 5 essais conformes », et la Campagne écrit « Validé 5× depuis 45 jours ».
4. **Atelier, même essai** : « Charnière dépassée (150 p) — prolonger ou clore » sur un essai du 25/08 jamais clos.
5. **Deux lignes s'appellent « EMAG 1 »** (une avec 2 références, une avec 1). Tout total par ligne est faux tant qu'elles ne sont pas fusionnées.
6. Sur la référence de production : « Ajoutez un deuxième scénario pour comparer », « Validation scénario 0 / 5 essais conformes » — des cadres vides sur 70 scénarios de série sur 86.

### 1.7 Deux risques sur les données, à traiter avant tout le reste

- **Stockage local presque plein.** Suivi 958 Ko + copie 949 Ko + historique 2,96 Mo, pour un plafond d'environ 5 Mo. Le pied de page affiche « suivi 0,91 Mo / ~5 Mo » : il ne compte ni la copie ni l'historique. Quand le plafond est atteint, l'enregistrement échoue.
- **Export incomplet** (déjà signalé) : le fichier exporté ne contient ni le catalogue, ni le plan, ni les consommations, ni les réglages d'usine. La sauvegarde de secours, elle, est complète.

---

## 2. Le diagnostic en une phrase

L'outil a été construit **par ajout de vues** (250 versions en 73 jours), alors que le métier tient en **une équation et un cycle** :

> **Coût outillage par pièce = prix ÷ (arêtes × pièces par arête)**, multiplié par le volume annuel.
> Trois leviers et pas un de plus : **le prix, le nombre d'arêtes, la durée de vie**.
> À côté : **le temps** (cycle × taux horaire). Au-dessus : **la qualité**, qui n'est pas de l'argent mais une porte — conforme ou pas.

> **Cycle d'un poste** : situation actuelle → piste → essai → validé → en série.
> L'argent ne change de colonne **que** quand le statut change.

L'outil parfait montre cette équation et ce cycle partout, avec les mêmes mots, et rien d'autre.

---

## 3. L'outil cible : 3 écrans de travail, 1 référentiel, 1 document

Navigation : **Usine · Poste · Référentiel**. Un bouton : **Bilan**. L'atelier s'ouvre depuis un essai, comme aujourd'hui.

### 3.1 USINE — « où est l'argent, où en est-on, quoi faire »

Remplace : Vue d'ensemble, Carte atelier, Tableau de bord, Vue CPP, La campagne, la feuille de route de la Synthèse.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ACTÉ (en série, mesuré)     À PASSER EN SÉRIE (validé)     EN ESSAI      │
│  … €/an                      … €/an                         … €/an        │
├──────────────────────────────────────────────────────────────────────────┤
│  À FAIRE                                                                  │
│  • EMAG 1 · 356x26 RPI · OP10 — LKT640 validé depuis 45 jours,            │
│    pas en série                                          [Passer en série]│
│  • PCI 4 · 268x12 · OP40 — essai lancé il y a 7 jours, aucune mesure      │
│                                                          [Ouvrir l'essai] │
│  • EMAG 3, PCI 4 — taux horaire manquant                 [Renseigner]     │
├──────────────────────────────────────────────────────────────────────────┤
│  POSTE                      €/pièce   réf. Matis   €/an    ÉTAT           │
│  EMAG 1 · 356x26 RPI · OP10  0,0873      …          …      validé −36 %   │
│  EMAG 1 · 304x28 RPE · OP20  0,1107      …          …      rien en cours  │
│  …  (une ligne par poste, triée par €/an décroissant)                     │
└──────────────────────────────────────────────────────────────────────────┘
```

Règles :
- **Trois chiffres en tête, une seule fonction pour les calculer**, réutilisée par le Bilan. « Acté » = scénario en série **et** gain mesuré. Un acté négatif s'appelle « surcoût », en rouge, jamais « gain ».
- **« À faire » est calculé, pas saisi**, trois lignes maximum : validé qui attend, essai ouvert sans mesure, essai à charnière dépassée non clos, donnée manquante qui bloque un chiffrage. C'est la réponse à « où en était-on ».
- **Un seul tableau, trié par argent**. Un filtre par ligne. Pas de tuiles, pas de sous-vues, pas de paragraphe d'explication.
- Une donnée manquante s'affiche **dans la case** (« volume ? ») et se saisit là, d'un clic.

### 3.2 POSTE — « que coûte ce poste, quels leviers, quelles pistes »

Remplace : l'écran Scénarios (150 contrôles), la Synthèse, la comparaison, la simulation, le mode Essentiel/Détails.

```
EMAG 1 · 356x26 RPI · OP10                              148 942 disques/an

EN SÉRIE AUJOURD'HUI — Classeur Matis                       0,0873 €/pièce
  Plaquette          prix    arêtes   vie visée   vie mesurée    €/an
  …                  …       …        …           …              …
     si prix −10 % → … €/an    si +10 pièces/arête → … €/an

PISTES
  ● Céramique intégrale — LKT640    VALIDÉ   0,0558 €/pièce   −36,0 %
      1 essai (25/08) · conforme · gain « objectif, non mesuré »
      [Passer en série]   [Nouvel essai]
  ○ Mixte T50013 — bol CBN + piste céramique   …   0,0358 €/pièce
  ○ …
  [+ Nouvelle piste]

QUALITÉ    Battement ≤ 0,12 mm    … % hors tolérance sur … pièces mesurées
TEMPS      cycle … s → … s        taux horaire 32,00 €/h
```

Règles :
- **Lecture d'abord, saisie ensuite.** Les 81 champs toujours ouverts disparaissent : on lit un tableau, on touche une ligne pour la modifier.
- **La comparaison se fait toujours contre ce qui tourne en série.** Fin du « comparé à » réglable qui produit le « 0 % » au-dessus du « −36 % ».
- **Les leviers sont écrits sous chaque plaquette** : prix −10 %, +10 pièces par arête, et — quand elle existe — « avec la vie mesurée ». Ce sont tes trois questions du check-up, sans ouvrir un autre écran.
- **La vie mesurée entre dans le chiffre**, avec sa réserve en clair (« mesuré sur 1 essai »).
- Un scénario de série n'affiche **aucun** cadre d'essai vide.
- **Qualité = une porte.** Une ligne : la tolérance, le pourcentage hors tolérance, le nombre de pièces mesurées. Le détail (courbes, Marposs) s'ouvre à la demande.
- **Temps = deux nombres** : le cycle mesuré avant et après, en secondes. On arrête de demander Vc et f sur chaque logement (38 remplis sur 377) pour reconstituer un temps que l'opérateur lit sur la machine.

### 3.3 ESSAI et ATELIER — « mesurer vite, conclure toujours »

L'atelier reste tel quel : c'est le meilleur écran. Deux changements seulement.

- **Clore un essai devient un geste en trois choix**, obligatoire, à la place du champ « conclusion » (rempli 1 fois sur 16) :
  1. Résultat : **concluant / non concluant / à refaire** ;
  2. **Pièces par arête atteintes** (pré-rempli avec le dernier n° de pièce) ;
  3. Une phrase libre, facultative.
  C'est ce geste qui fait passer la vie « visée » en vie « mesurée », donc qui fabrique le chiffre d'économie. Aujourd'hui rien ne le déclenche.
- Les champs que personne ne remplit (programme gauche/droit, heures, maturité des bruts…) passent **sous un pli « détails »**. Ils restent dans le fichier.

Proposition nouvelle, à partir de données que tu as déjà : sur les essais où le battement est relevé pièce après pièce, **tracer le battement en fonction du n° de pièce** et afficher la pièce où il croise la tolérance. C'est le pont direct entre la qualité et le coût : « la tolérance tient jusqu'à la pièce N, donc la vie atteignable est N ». À valider avec toi avant de l'écrire : c'est un indicateur, pas un verdict.

### 3.4 RÉFÉRENTIEL — « les chiffres d'entrée, à un seul endroit »

Remplace : Réglages (6,9 hauteurs d'écran, 970 mots), Catalogue, Volume annuel, Réel vs budget, les imports de consommation du Plan.

Quatre tableaux, sans texte :
1. **Articles** : MABEC, libellé, prix. Un prix changé se propage partout (déjà fait depuis la 4.148).
2. **Références** : volume annuel, cible site, **référence Matis** — lue une fois dans son classeur et **conservée**, au lieu d'être relue à chaque session.
3. **Lignes** : taux horaire.
4. **Tolérances par OP** : grandeur, limite, nombre d'essais conformes exigés.

En tête : « il manque N valeurs » avec la liste cliquable. Aujourd'hui les manques sont dispersés dans six écrans.

### 3.5 BILAN — « la preuve, en une page »

Remplace : Bilan client PDF, Dossier de visite, Livraisons, Rapport, mode présentation, timeline de la Campagne, menu Transmettre.

Un seul document daté, deux portées (un poste, ou l'usine) : situation de départ, ce qui a été essayé, ce qui est acté, ce qui attend, ce qui manque. Mêmes trois chiffres que l'écran Usine, **par la même fonction**. Imprimable et envoyable.

### 3.6 Le Plan de conversion : il change de place

34 hauteurs d'écran, 161 champs : c'est ton outil de fournisseur, pas celui de l'usine, et il est dans le menu de tout le monde.
Décision : **il sort du menu commun**. Ce qu'il apporte à l'usine (« −X % de prix = −Y €/an ») devient la ligne de leviers de l'écran Poste. La vue article par article reste, réduite à un tableau, **visible sur ton compte seulement**.

---

## 4. Ce qui sort de l'écran

| Sort | Raison mesurée |
|---|---|
| Projets (bloc d'en-tête, filtre, création) | 1 projet, décision prise |
| Mode Essentiel / Détails | deux versions du même écran |
| Vue d'ensemble, Carte atelier, Tableau de bord, Vue CPP | fusionnés dans Usine |
| Synthèse, comparaison, simulation | fusionnés dans Poste |
| La campagne | ses 3 alertes vont dans « À faire », sa timeline dans le Bilan |
| Livraisons | 0 livraison |
| Dossier de visite | jamais ouvert |
| Réel vs budget (écran) | devient une colonne conservée |
| Réglages, Catalogue (écrans séparés) | fusionnés dans Référentiel |
| Mémoire, Parcours, Nouveautés | déjà retirés ou sans usage |

**Rien ne sort du fichier.** Un champ caché garde sa valeur, s'exporte et se réimporte. Le format de données (format 8) ne change pas : pas de migration, donc pas de risque de conversion.

Résultat attendu : de 32 panneaux à 5, de 12 entrées de menu à 3 plus un bouton.

---

## 5. Les dix règles de conception (à tenir à chaque tour)

1. **Un chiffre, une fonction.** Tout écran qui affiche un gain appelle la même.
2. **La réponse tient dans une hauteur d'écran.** Le détail est dessous, replié.
3. **Pas de mode d'emploi à l'écran.** Si un écran a besoin d'un paragraphe, c'est l'écran qui est faux.
4. **Une donnée manquante se demande là où elle manque**, une fois, avec ce qu'elle débloque.
5. **Un champ que personne ne remplit quitte le formulaire** (pas le fichier).
6. **Toujours comparé à ce qui tourne en série.**
7. **L'argent ne bouge qu'avec un statut.** Pas de gain sans passage en série ; pas de « validé » sans essai clos.
8. **Mesuré et visé ne se mélangent jamais** : deux colonnes, la réserve écrite.
9. **Un essai ouvert finit clos.** L'outil le rappelle tant que ce n'est pas fait.
10. **Aucun chiffre non justifiable** (constitution §5.6) : chaque montant est cliquable jusqu'à son prix, ses arêtes, sa vie, son volume.

---

## 6. Comment on y va : élaguer, pas réécrire

**Arbitrage.** Réécrire de zéro donnerait un code plus propre, mais ce sont des semaines sans livrer, 787 tests à refaire et un risque réel sur tes données. Les calculs sont justes ; c'est l'affichage qui déborde. Donc : on **garde le moteur et le format de données**, on écrit **deux écrans neufs** (Usine, Poste) par-dessus une seule fonction de vérité, on **débranche** les anciens du menu, et on ne **supprime** leur code que deux semaines après, quand personne ne les a réclamés. Chaque lot est livrable seul et réversible.

| Lot | Contenu | Visible ? | Réversible ? |
|---|---|---|---|
| **0** | Export complet + test d'aller-retour ; historique local plafonné ; jauge de stockage honnête | non | oui |
| **1** | Une seule fonction « acté / à passer en série / en essai » ; vie mesurée dans le chiffre ; coquilles (k€€, −-, /an/an) ; fusion des deux « EMAG 1 » | chiffres cohérents | oui |
| **2** | Écran **Usine** ; les cinq vues débranchées ; Projets retirés de l'affichage | oui | oui |
| **3** | Écran **Poste** avec leviers ; Synthèse et mode Essentiel/Détails débranchés | oui | oui |
| **4** | Clôture d'essai en trois choix ; plis « détails » | oui | oui |
| **5** | **Référentiel** ; référence Matis conservée | oui | oui |
| **6** | **Bilan** unique ; Plan sur ton compte seul ; suppression du code débranché | oui | **non** — point de non-retour, après accord |

Points d'attention :
- **Lot 0 d'abord, sans discussion** : c'est lui qui garantit « toutes les données gardées ».
- **Fusion des deux « EMAG 1 »** : je te montre le contenu des deux avant de fusionner, avec une copie de secours.
- **Lot 6** : seul geste irréversible côté code. Les données, elles, ne sont jamais touchées.
- **Matis** : les lots 2 et 3 changent son écran du jour au lendemain. À lui montrer avant de déployer.

---

## 7. Ce que je n'ai pas pu contrôler

- **Le format téléphone** : la fenêtre Chrome n'a pas accepté le redimensionnement (restée à 1280 px).
- **Le menu Transmettre** : le clic n'a rien ouvert de visible par mon mode de pilotage ; à revoir à la main.
- **Bilan client PDF, Dossier de visite, imports** : non ouverts, pour ne rien écrire dans tes données (le Dossier de visite enregistre une date de visite).
- Le texte du Catalogue et du Plan a été lu partiellement (une protection du navigateur a bloqué deux lectures) ; les mesures de taille, elles, sont complètes.
