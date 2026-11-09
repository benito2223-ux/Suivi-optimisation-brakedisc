# Proposition — la version simple du Suivi d'optimisation

**Auteur** : Claude · **Date** : 09/11/2026 · **Base** : 4.150.0 (`ux-rail`, HEAD `87b288e`)
**Statut** : analyse et proposition. Aucun code modifié, PROD non touchée.
**Méthode** : lecture du code (`bilan_economique.html`, `spk-shell.js`) et mesure de l'export réel rev435 du 09/11. Les écrans n'ont pas été re-parcourus dans le navigateur aujourd'hui (voir §8) : le vécu utilisateur s'appuie sur les deux parcours d'hier (`CHECKUP_2026-11-10.md`, `ANALYSE_OUTIL_2026-11-10.md`), que le code confirme.

---

## 1. Verdict

L'outil a grossi cent fois plus vite que ses données.

| Ce que l'outil contient | Ce que les données contiennent (rev435) |
|---|---|
| 23 151 lignes livrées, 694 fonctions | 6 lignes actives, 18 références, 67 OP |
| 32 panneaux, environ 33 entrées de menu | 81 scénarios, dont 69 « en série » (la production) |
| 250 versions en 73 jours | 12 essais, 146 prélèvements, 15 séries Marposs, 3 photos |
| 8 modes d'affichage | 1 projet, 7 suggestions |

Le moteur de calcul est juste (les 787 tests le tiennent). Ce qui ne va pas, c'est qu'un même chiffre est recalculé par plusieurs écrans avec des règles différentes, et qu'il faut choisir entre dix écrans pour lire une seule chose : **ce poste coûte combien, combien a-t-on gagné, que fait-on ensuite**.

La version simple tient en **4 écrans et 1 bouton**, sur le même moteur et le même fichier de données. Rien n'est réécrit de zéro.

**Un point à traiter avant tout le reste** : le fichier « Exporter » ne contient pas tout (§6). Le catalogue des prix, le plan, les consommations, les livraisons et les spécifications usine n'y sont pas écrits. L'import sait les lire, l'export ne les écrit pas.

---

## 2. Ce que vit l'utilisateur aujourd'hui

**Pour répondre à « où en est-on ? »**, dix écrans se disputent la réponse : Vue d'ensemble, Atelier (carte), Tableau, Synthèse, Vue CPP, La campagne, Plan de conversion, Économies générales, Dossier de visite, Bilan client. Quatre d'entre eux donnent une valeur différente de l'économie actée (0 / 7 449 / 0 / −2 112 €/an, reproduit hier).

**Pour répondre à « et si je baisse le prix, ou si la plaquette dure plus ? »**, aucun écran ne répond là où la question se pose (le poste). Il faut aller dans le Plan, qui répond par article toutes lignes confondues.

**Pour saisir un essai à la machine**, le régleur n'a aucun chiffre d'argent sous les yeux.

**Pour naviguer**, il faut connaître : le rail (5 écrans), le menu Outils (10 entrées), Transmettre (6), « Plus » (12), le fil d'Ariane, Essentiel/Détails, le mode gants, le verrou, la présentation client, le mode maxi, la vue projets.

---

## 3. Les doublons, famille par famille

| Famille | Ce qui existe | Ce qu'on garde |
|---|---|---|
| **État des lieux** | Vue d'ensemble, Carte atelier, Tableau, Vue CPP, Campagne, Économies générales, Dossier de visite, priorités du Plan, « trois gains », « démultiplication », « mission A4 » | **Un tableau Usine** : une ligne par poste |
| **Économie actée** | 4 fonctions (`gainPoste`, `campagneCollecter`, `planRecapGains`, `accueilBandeauHTML`) | **Une fonction**, lue partout |
| **« Et si… »** | Plan de conversion, simulateur (`simulHTML`), seuil de bascule, décomposition des leviers, bloc économies atelier | **Leviers sur le poste** (prix, vie) + cible par article dans le catalogue |
| **Durée de vie** | charnière visée, charnière réelle, par logement (fonction définie **deux fois**, l. 7149 et 7163), durée de vie scénario, prévision d'usure, gain mesuré replié | **Visé et mesuré côte à côte**, tous deux dans le verdict |
| **Temps de cycle** | champ manuel (0,0 %) et calcul Vc×f (+33 %) sur la même fiche | **Le calcul**, le champ manuel devient une correction étiquetée |
| **Comparer** | Synthèse, panneau Comparaison, tendances multi-essais, « décliner » | **Les scénarios en colonnes** sur le poste |
| **Documents** | Rapport de validation, rapport d'essai, PDF, Bilan client, Livraison, Mission A4, Dossier de visite | **Un rapport**, trois périmètres : essai, poste, usine |
| **Filets de sécurité** | sauvegarde locale, instantané avant import, Historique, Actions récentes, export, dossier local, synchro, export de secours, mémoire des textes | **Synchro + un Historique + un export complet** |
| **Modes** | Essentiel/Détails, gants, atelier, verrou, présentation client, maxi, vue projets, mode rapide | **Bureau / Atelier**, plus la lecture seule |
| **Données de base** | Options (taux, volumes, coût rebut), Catalogue, classeur Matis, conso 2025, fiche ligne, fiche référence | **Un écran Prix & volumes** |
| **Réparations ponctuelles** | réparation D1/D2, inversion MABEC, fusion Matis, dédoublonnage, chacun avec son panneau | La migration silencieuse au chargement reste, **les panneaux partent** |
| **Code mort** | `pipelineHTML`, `boussoleHTML`, `ouvrirSimul`, `ouvrirMemoireEssais` (définis, plus appelés), `photoObjectURL` défini deux fois | Supprimé |

Peu utilisé au regard de sa place : les **Projets** (1 seul projet réel, environ 300 lignes de code, deux panneaux) et les **Suggestions** (7 entrées, dont deux portent 114 Ko de photos dans le fichier du suivi).

---

## 4. La version cible : 4 écrans, 1 bouton

### Écran 1 — Usine (l'accueil)

Un seul tableau, une ligne par poste (ligne × OP), trié par argent en jeu.

```
Poste              CPP outillage   Cible    Acté         À portée      Prochain geste
HESSAPP · OP30     0,0536 €        …        —            −9,1 k€/an    confirmer la vie mesurée (essai en cours)
EMAG 1 · OP40      …               …        +7,4 k€/an   …             valider le candidat
HESSAPP · OP15     …               …        −2,1 k€/an   —             en série, coûte plus cher : à revoir
EMAG 3 · OP20      —               —        —            —             manque : volume annuel
```

*(Maquette. Seuls les chiffres déjà reproduits hier y figurent ; « … » = valeur que l'outil calculera, non inventée ici — constitution §5.6.)*

En tête, une phrase : « Acté : X k€/an sur N postes · À portée : Y k€/an · Z postes sans données ». La courbe de la campagne reste, sous la phrase. Un clic sur une ligne ouvre le poste.

Remplace : Vue d'ensemble, Carte atelier, Tableau, Vue CPP, La campagne, Économies générales, Dossier de visite, priorités du Plan.

### Écran 2 — Poste (là où on travaille)

Trois blocs, dans cet ordre.

**Le verdict, sur les trois axes du sujet** :

```
COÛT          0,0536 €/pièce (outillage)   −9,1 k€/an au vu du mesuré (90 p/arête, à confirmer)
PRODUCTIVITÉ  cycle +33 % (Vc × f)         temps machine non chiffré : taux horaire manquant
QUALITÉ       battement … conformes sur … · Ra … · rebut —
```

**La composition, logement par logement**, avec le coût de chacun et ses leviers sur place (exemple HESSAPP OP30, T5 + T6 ensemble, chiffres du check-up) :

```
T5 + T6 · KY3500 · 9,56 € · 50 p/arête (mesuré 90)        20,4 k€/an
   prix −10 % → −2,0 k€/an     +10 p/arête → −3,4 k€/an     vie mesurée → −9,1 k€/an
```

**Les scénarios en colonnes** : la production, puis chaque candidat, avec son statut (essai → validé → en série). C'est la Synthèse, ramenée au poste.

Remplace : fiche scénario, Synthèse, Comparaison, simulateur, seuil de bascule, fiche poste, et la lecture « par article » du Plan pour ce poste.

### Écran 3 — Essai (la saisie à la machine)

Le mode atelier devient cet écran, pas un habillage de tous les autres. Gros chiffres, gants.

- en tête, la ligne d'argent : « KY3500 · T5 + T6 — chaque 10 pièces de plus par arête = −3,4 k€/an » ;
- objectif, prélèvements, usure, Marposs, photos, observations, conclusion ;
- la bannière « Reprendre » nomme la ligne et l'OP.

### Écran 4 — Prix & volumes (les données de base)

Tout ce dont les calculs dépendent, à un seul endroit : catalogue (MABEC, prix, prix cible, vie cible), volumes annuels par référence, taux horaires par ligne, coût du rebut, consommations (2025 et classeurs hebdo de Matis). L'écran affiche en tête ce qui manque et ce que ça bloque (« 8 postes non chiffrés faute de volume »).

Le Plan de conversion y devient deux colonnes du catalogue (prix cible, vie cible) et un total unique, libellé par son périmètre.

### Le bouton — Transmettre

Un rapport (essai, poste ou usine, même gabarit A4), l'export complet, l'import. La présentation client reste : c'est la lecture seule sans les prix.

---

## 5. Ce qui sort de l'écran

| Retiré de l'interface | Ses données |
|---|---|
| Projets (panneaux, vue projets) | conservées ; le projet devient une étiquette filtrable sur le tableau Usine |
| Suggestions | conservées dans le fichier ; exportées une fois en `.md`, saisie retirée |
| Livraisons | conservées et listées dans Transmettre ; une livraison = un rapport usine figé |
| Dossier de visite | `derniereVisite` conservée ; le rapport usine prend la période en paramètre |
| Nouveautés, « Démarrer un suivi », Signaler un problème | aucune donnée métier |
| Panneaux de réparation D1/D2, MABEC, fusion Matis | aucune ; les migrations au chargement restent |
| Actions récentes + Restaurer + instantané | fondus dans l'Historique |
| Essentiel/Détails, maxi, mode rapide | aucune ; l'écran est simple par construction |

---

## 6. La garantie : aucune donnée perdue

**Le principe** : la simplification touche les écrans et les fonctions d'agrégation. **Le format de données (format 8) ne change pas, aucune clé n'est supprimée.** Un écran retiré laisse ses données dans le fichier.

**Le trou à boucher d'abord** (constaté au code, 4.150.0) :

- `exportData` (l. 4974-4998) écrit : lignes, projets, responsables, backlog, et la position active ;
- `payloadSuivi` (l. 4668, la sauvegarde locale) écrit en plus : `specsUsine`, `livraisons`, `catalogue`, `plan`, `conso2025`, `consoReelle`, `planSource`, `consoSemaines`, `planReglages`, `derniereVisite`, `synchroNote` ;
- `appliquerImport` (l. 5852 et suivantes) sait relire catalogue, plan, conso, livraisons, specs.

Donc aujourd'hui le catalogue et le plan ne vivent que dans le navigateur et dans la synchro. Un export archivé ne permet pas de les reconstruire. L'export rev435 le confirme : ces clés n'y sont pas.

**La preuve exigée à chaque lot** : un test d'aller-retour sur l'export réel. Charger rev435, exporter, recharger, comparer clé par clé, et recompter : 81 scénarios, 365 logements, 12 essais, 146 prélèvements, 15 séries Marposs, 3 photos, 7 notes d'essai (objectif, observations, conclusion). Un lot qui change un de ces nombres ne part pas.

---

## 7. Le chemin, lot par lot

Choix d'architecture : **élaguer, pas réécrire**. Une réécriture perdrait les 787 tests et le moteur validé contre le classeur de Matis ; l'élagage garde les deux et chaque lot reste livrable seul. Les écrans sont d'abord **débranchés du menu** (réversible en une ligne), puis leur code est supprimé deux semaines plus tard si personne ne les a réclamés.

| Lot | Contenu | Effort | Risque |
|---|---|---|---|
| **0** | Export complet (une seule fonction pour l'export et la sauvegarde) + test d'aller-retour + étiquette git de l'état actuel | S | nul, additif |
| **1** | Une seule fonction d'économie actée (config de l'OP, curseur de volume, série non-meilleure comptée, négatif affiché). Le 7 449 €/an changera : avant/après montré avant mise en ligne | M | chiffre visible modifié |
| **2** | Leviers prix / vie / vie mesurée sur le poste et l'essai ; verdict sur trois axes ; mesuré dans le verdict | M | faible |
| **3** | Tableau Usine ; les dix écrans d'état des lieux débranchés du menu | M | habitudes de Matis |
| **4** | Prix & volumes : catalogue + options + consommations réunis ; Plan replié en colonnes | M | faible |
| **5** | Un seul rapport, trois périmètres | M | forme des documents déjà envoyés |
| **6** | Suppression du code débranché et du code mort. Estimation à confirmer au lot : 5 000 à 7 000 lignes sur 23 000 | S | nul si le lot 0 tient |

---

## 8. Décisions prises, et ce qui te revient

**Tranché dans cette proposition** (dis-le si tu n'es pas d'accord) :

- « acté » = tout scénario en série, y compris à gain négatif, affiché comme tel ;
- le verdict affiche le visé **et** le mesuré, le mesuré tamponné « à confirmer » ;
- l'outillage reste l'indicateur principal, le temps à côté (constitution §2 quater) ;
- la ligne d'argent est visible sur l'écran atelier.

**À toi** :

1. **Plan de conversion** : replié dans Prix & volumes (ma recommandation), ou gardé en écran à part parce que c'est ton outil de négociation ?
2. **Projets** : une simple étiquette (ma recommandation, vu 1 projet réel), ou tu comptes en ouvrir d'autres ?
3. **Matis** : il utilise la Carte atelier et le Tableau tous les jours ? Si oui, le lot 3 se fait avec lui devant l'écran.

**Non vérifié dans cette passe** : les écrans dans le navigateur (l'outil de prévisualisation était indisponible), l'usage réel écran par écran (aucune mesure de fréquentation n'existe dans l'outil), le contenu du catalogue et du plan de ta session (absents de rev435, pour la raison du §6), l'iPhone, les triggers serveur.
