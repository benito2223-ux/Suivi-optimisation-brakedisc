# Les petits détails — analyse au niveau du geste et du champ

Complément de `REFONTE_OUTIL_CIBLE_2026-11-09.md` (qui traite les écrans). Ici : ce qu'on tape, combien de fois, et où ça se contredit.
Mesuré dans Chrome sur PROD 4.150.0, session réelle (rev 436), en lecture seule. Rien saisi, rien modifié, aucun code touché.
Tous les chiffres ci-dessous sont comptés dans tes données ; ce qui n'a pas été contrôlé est listé à la fin.

## Le principe qui manque : une donnée se tape une fois, à l'endroit où elle est vraie

Presque toutes les frictions ci-dessous viennent de la même cause : une donnée appartient physiquement à un niveau
(la broche, l'article, la pièce, l'OP) et l'outil la fait saisir un niveau plus bas, donc plusieurs fois.

| La donnée | Appartient à | Est saisie aujourd'hui | Résultat mesuré |
|---|---|---|---|
| Vitesse de coupe / de broche | la broche, donc le groupe simultané | dans chaque logement | 9 groupes sur 9 : valeurs identiques retapées |
| Prix, arêtes, désignation | l'article | dans chaque logement | 377 logements pour 26 articles |
| Mesures d'une pièce | la pièce | une ligne par outil | n° de pièce tapé deux fois |
| Tolérance | la référence × OP | dans chaque scénario | 0,04 et 0,12 sur la même OP |
| Conditions de l'essai | l'essai | nom du scénario + logement + copie dans l'essai | les trois divergent |

---

## A. La fiche outil

### A1. Conditions de coupe retapées dans chaque outil simultané — ton exemple
- **Constat.** 10 groupes d'outils simultanés. Sur les 9 où Vc et f sont saisis sur plusieurs logements, **9 fois sur 9 les valeurs sont identiques** (ex. T548 650 / 0,25 et T549 650 / 0,25). Zéro cas différent. Même chose à l'intérieur d'un outil à plusieurs logements : 8 sur 8 identiques, et 3 à moitié remplis (un logement a la valeur, pas l'autre).
- **Pourquoi c'est anormal.** Deux outils qui coupent en même temps sont sur la même broche : la vitesse de rotation est une seule et même grandeur, elle ne peut pas différer. La case « ⇉ Tourne en simultané » ne sert qu'au calcul du cycle, elle ne met rien en commun.
- **Règle.** Les conditions se saisissent **une fois, sur le groupe**. La vitesse est commune et non modifiable par outil. L'avance, κr, rε, ap sont **héritées** du groupe, avec un petit « différent sur cet outil » pour le cas (réel mais rare) où une tourelle avance autrement. Dans un outil à plusieurs logements, même héritage.
- **Données.** Les 9 groupes identiques se fusionnent sans perte. Les 3 logements à moitié remplis reçoivent la valeur de leur voisin — à te montrer avant d'appliquer.

### A2. Pas de mode G96 / G97 : « S700 » rangé dans « Vc m/min »
- **Constat.** Aucun champ pour le mode. Des essais en G97 S700 (tr/min) sont saisis **700 dans le champ « Vc (m/min) »**. Le mode est tapé à la main dans le nom du scénario.
- **Pourquoi c'est grave.** La valeur enregistrée n'a plus de sens : 700 tr/min et 700 m/min ne sont pas la même coupe. Tout calcul de temps de coupe ou de comparaison entre essais devient faux sans que rien ne l'indique.
- **Règle.** Un sélecteur **G96 (Vc en m/min) / G97 (S en tr/min)** sur le groupe ; l'unité du champ suit. En G97 l'outil affiche la Vc résultante aux diamètres de la piste (elle se calcule, elle ne se devine pas).
- **Données.** Rien n'est converti automatiquement. Les scénarios dont le nom contient « G97 » ou « S… » te sont listés pour confirmer le mode ; la valeur tapée est conservée telle quelle.

### A3. L'article retapé dans chaque logement
- **Constat.** **377 logements pour 26 articles.** Z000 546 265 est saisi 47 fois, Z000 546 266 41 fois, Z000 513 527 40 fois, IM02 137 021 38 fois. Chaque fois : référence + MABEC + prix + nombre d'arêtes.
- **Ce que ça a produit.** Les prix sont restés cohérents (0 écart, grâce au Catalogue depuis la 4.148), mais **le nombre d'arêtes diverge sur 3 articles** : Z000 522 436 (2 ou 3), IM02 137 020 (8 ou 2), Z000 539 100 (4 ou 8). Un écart d'arêtes de 2 à 8 change le coût par pièce d'un facteur 4. 50 logements n'ont aucun code article. `codeArticle` et `mabec` sont deux champs pour la même chose et diffèrent sur 6 logements.
- **Règle.** Dans le logement on **choisit l'article** (liste des 26, recherche par code ou désignation). Prix, arêtes, désignation viennent de l'article et ne se retapent pas. Le logement ne garde que ce qui lui est propre : la charnière, et le nombre d'arêtes **réellement utilisables dans ce porte-outil** s'il est inférieur à celui de l'article (c'est peut-être l'explication légitime de 8/2 — à trancher avec Matis, pas par l'outil).
- **Données.** Rattachement automatique par code. Les 3 articles aux arêtes divergentes et les 50 logements sans code sortent dans une liste « à trancher », rien n'est écrasé.

### A4. Deux champs « Correcteur », et des noms de logement qui en font un troisième
- **Constat.** « Correcteur » existe sur l'outil **et** sur le logement. Les noms de logement sont libres : « D1 » 173 fois, « D2 » 79, « Logement 1 » 31 et « Logement 2 » 13 (nom par défaut jamais renommé), « Plaquette » 13, et des « T0101 », « T0707 ». Les numéros d'outil aussi : « T546 D1 », « T513.1 », « T535S », un outil sans numéro.
- **Règle.** Un outil = un **T** ; un logement = un **D**. Deux petits champs numériques, le libellé « T548 · D1 » est fabriqué par l'outil. Plus de nom libre, plus de second champ Correcteur.
- **Données.** 252 « D1/D2 » se convertissent seuls ; les autres sont proposés un par un.

### A5. 13 champs par logement, tous au même niveau
- **Constat.** Un logement = 13 champs (nom, référence, MABEC, suivi en tolérance, prix, arêtes, charnière, Vc, f, κr, rε, ap, temps de coupe), l'outil en ajoute 5. Un scénario à 5 outils = **174 champs, 3,2 hauteurs d'écran**, sur une demi-largeur. Sur 252 outils, les conditions de coupe ne sont remplies que dans 18 scénarios sur 86 : l'écran demande beaucoup et reçoit peu.
- **Règle.** Après A1 et A3, une ligne de logement ne montre plus que **3 choses : D, article, charnière**. Un outil tient sur une ligne, un scénario à 5 outils sur un écran. Le reste (plan joint, κr, rε) est derrière « détail ».
- **Détail de confort.** Les flèches ▲▼ sur les champs numériques n'ont pas de sens pour un prix à 10,97 € ou une avance à 0,25 : à retirer, et ouvrir le pavé numérique sur tablette.

---

## B. L'essai

### B1. Les conditions de l'essai existent en trois exemplaires qui divergent
- **Constat.** (1) Dans le **nom** de 6 scénarios (« ESSAI : SNGN090416T00520 SN60 G96 S800 F0,25 ») ; (2) dans les **logements** (Vc 800) ; (3) dans la **copie prise au lancement de l'essai**. D'où le bandeau « ⚠ modifié depuis : T548·D1 Vc 700→800 · T549·D1 Vc 700→800 — Aligner sur le scénario ».
- **Pourquoi c'est grave.** On ne sait plus à quelle vitesse l'essai a tourné, et le bouton « Aligner » propose de **réécrire après coup** les conditions d'un essai déjà fait.
- **Règle.** Un essai **fige** ses conditions au lancement, elles sont affichées en tête de l'essai et ne bougent plus. Changer la vitesse en cours de route = un nouvel essai (un clic « même essai, autres conditions »), pas une retouche du scénario. Le nom du scénario est **fabriqué** par l'outil à partir de l'article et des conditions ; on n'y tape plus de paramètres.

### B2. Deux noms par scénario
- **Constat.** Champs `nom` (66 sur 86) et `name` (86 sur 86). Sur 4 scénarios, `nom` vaut « Classeur Matis » alors que `name` dit « ESSAI PLAQUETTES S675 F0.32 » ou « SNGN 090416 F SL 500 ».
- **Rectification (vérifiée dans le code).** L'écran lit `name`, qui est le bon nom : la bannière « Reprendre » et les listes n'affichent **pas** « Classeur Matis » à tort, contrairement à ce que j'avais écrit. `nom` est un reliquat qui n'est affiché nulle part.
- **Règle.** Un seul nom dans les données : retirer `nom` (étape 3, avec export avant). « Classeur Matis » est une **provenance**, pas un nom.

### B3. Deux lignes de relevé par pièce
- **Constat.** Sur un essai à 2 outils, chaque pièce occupe **2 lignes** : 30 lignes pour 15 pièces, 12 pour 6, 21 pour 11, 16 pour 8, 22 pour 11, 20 pour 10, 14 pour 7. Le n° de pièce est tapé deux fois, les cases de l'autre face restent vides. Un champ texte « Point de mesure (Inter, Exter…) » est vide partout, alors que les colonnes s'appellent déjà Inter et Exter. Le n° de pièce est enregistré tantôt en texte, tantôt en nombre.
- **Règle.** **Une pièce = une ligne**, les deux faces côte à côte. Le n° de pièce s'incrémente seul (+1, ou +pas de prélèvement). Le champ « Point de mesure » disparaît.
- **Données.** Les paires de lignes d'une même pièce se regroupent ; les 192 prélèvements sont conservés (contrôle : même nombre de valeurs mesurées avant et après).

### B4. L'en-tête d'essai demande 15 champs avant la première mesure
- **Constat.** Titre, date, équipe, opérateur, maturité des bruts, but, observations, rédacteur, heure début, heure fin, date fin, programme CNC, conclusion, photos, Marposs. L'onglet Essais fait **81 champs et 5,6 hauteurs d'écran**. Ce qui est réellement rempli : équipe 8 sur 16, conclusion 1 sur 16. Opérateur en texte libre : « Matis », « Matis  » (avec espace), « Matis HERNU », « Murielle/Lucas ».
- **Règle.** Au lancement : **le but** (une phrase) et rien d'autre. Date et heure sont prises seules, le rédacteur est le compte connecté, l'opérateur se choisit dans une liste. Maturité des bruts et programme CNC restent, mais dans « détail ». La conclusion est demandée **à la clôture**, pas dans l'en-tête.

### B5. Des essais jamais clos
- **Constat.** **7 essais sur 16 encore ouverts**, dont EMAG 1 OP10 (30 lignes) depuis le 25/08. Sur les 9 clos, le motif est « autre » 5 fois ; un essai PCI 4 OP40 est clos « casse » avec 0 relevé.
- **Règle.** Clôture en trois choix (**validé / arrêté / à refaire**) + une phrase obligatoire. Un essai ouvert sans relevé depuis 14 jours remonte en tête du poste avec « clore ? ». « Autre » disparaît.

---

## C. Les critères de qualité

### C1. La tolérance se règle par scénario
- **Constat.** EMAG 2 356x26 RPI OP40 et PCI 4 268x12 OP40 ont **à la fois 0,04 et 0,12** selon le scénario. Sur un même écran, le critère principal dit « Battement ≤ 0,12 » et la spec usine affichée au-dessus dit « Battement ≤ 0,040 · VE ≤ 0,010 ».
- **Pourquoi c'est anormal.** La tolérance vient du plan de la pièce. Deux scénarios de la même OP ne peuvent pas être jugés sur deux tolérances : la comparaison n'a plus de valeur.
- **Règle.** Tolérances saisies **une fois par référence × OP**, héritées par tous les scénarios et tous les essais. Un scénario ne peut pas les changer.

### C2. Deux critères Ra contradictoires, un critère principal jamais mesuré
- **Constat.** Sur le même scénario : « Ra (µm) ≤ 0,8 » et « Ra (µm) maxi 12 », valeurs mesurées 8,3 à 10,7. Le critère principal (battement) a sa colonne **vide** sur toutes les lignes.
- **Conséquence visible.** Colonne CONF « — », « Taux hors tolérance : — », « 0/5 essais conformes », alors que l'essai est noté « Arrêté — Hors tolérance le 15/10/2026 ». Et le même écran affiche « +1,1 k€/an … est le moins cher » à côté de « 0/5 essais conformes ».
- **Règle.** Un critère = une grandeur, une limite, une seule fois. Un critère sans aucune mesure affiche « non mesuré » (pas « — », pas « non conforme »). Un scénario sans essai conforme n'a pas le droit d'être annoncé « le moins cher » : il est « moins cher sur le papier, non validé ».

### C3. L'unité fausse à l'écran
- **Constat.** La colonne s'affiche « RA (MM) INTER ». Le libellé est bien « Ra (µm) », mais les en-têtes de tableau sont passés en majuscules par le style (`bilan_economique.html`, ligne 656) et la majuscule de « µ » est « Μ », qui se lit « M ».
- **Règle.** Les unités ne passent jamais en majuscules. Correction d'une ligne.

---

## D. Le coût

### D1. La durée de vie mesurée n'entre pas dans le coût
- **Constat.** T549 affiche « Charnière 50 — **6 réel** » en rouge, et le coût reste calculé sur 50 : 10,97 ÷ (8 × 50) = 0,0274 €/pièce. Avec les 6 pièces mesurées : 10,97 ÷ (8 × 6) ≈ 0,229 €/pièce, soit plus de 8 fois plus. À l'inverse, le check-up a relevé HESSAPP OP30 à 90 pièces réelles pour 50 saisies, sans effet sur le verdict.
- **Règle.** Deux coûts côte à côte, toujours : **« prévu » (charnière saisie) et « mesuré » (essai)**, avec le nombre de pièces qui fonde le mesuré. Le verdict d'un essai se prononce sur le mesuré.

### D2. Petits libellés
- Badge « FAILED » en anglais → « Arrêté ».
- « GAIN/AN +0 € » → ne rien afficher quand il n'y a pas d'écart.
- Bloc « Ailleurs dans l'usine » : « volume à saisir » répété 4 fois et « + 13 autre(s) » → une ligne « volume manquant sur N postes », cliquable.

---

## Ce que ça change, compté

| | Aujourd'hui | Après |
|---|---|---|
| Champs pour un scénario à 5 outils | 174 | une ligne par outil + un bloc conditions par groupe |
| Saisies d'un article | 377 (pour 26 articles) | 26 |
| Lignes de relevé pour 15 pièces à 2 outils | 30 | 15 |
| Champs avant la première mesure d'un essai | 15 | 1 |
| Endroits où vivent les conditions d'un essai | 3 | 1 |
| Endroits où se règle une tolérance | chaque scénario | la référence × OP |

## Ordre que je retiens

Ces corrections passent **avant** la refonte des écrans : elles touchent la saisie, là où Matis perd son temps, et elles
rendent les chiffres fiables avant qu'on les mette en avant.

1. **Sans risque, tout de suite** : C3 (unité), D2 (libellés), flèches ▲▼. — **fait en 4.150.1** (B2 n'avait rien à corriger à l'écran).
2. **Conditions de coupe** : A1 + A2 + B1 ensemble (groupe, mode G96/G97, essai figé). C'est ton exemple et c'est le plus rentable.
3. **Article choisi, pas retapé** : A3 + A4 + A5.
4. **Relevé** : B3 + B4 + B5.
5. **Critères et coût mesuré** : C1 + C2 + D1.

Les étapes 2 à 5 réorganisent où la donnée est rangée. Chacune se fait avec un export complet avant, une liste « à trancher »
montrée avant d'appliquer, et un contrôle de comptage après. Rien n'est supprimé : une valeur qui ne rentre pas dans la
nouvelle case reste visible dans « à trancher ». L'export complet (lot 0 de la refonte) reste donc le préalable.

## Non contrôlé

- Le format téléphone (le redimensionnement de la fenêtre n'a pas pris) : la fiche outil et le relevé n'ont pas été vus sur iPhone.
- Le code de la fiche logement et du formulaire d'essai n'a pas été relu ligne à ligne : l'inventaire des champs vient de l'écran, pas du code. Seule la fiche outil (`outilCarteHTML`, lignes 11654-11689) a été lue.
- La raison des arêtes divergentes (A3) : erreur de saisie ou arêtes réellement utilisables différentes selon le porte-outil — c'est une question pour Matis.
- Le cas d'une avance réellement différente entre deux outils simultanés n'existe pas dans tes données (0 sur 9) ; la dérogation est prévue par prudence.
- Les relevés Marposs, l'import de classeur et le rapport imprimé n'ont pas été examinés à ce niveau de détail.
