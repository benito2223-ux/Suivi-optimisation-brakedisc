# SPEC — Navigation par tuiles machines — Réponse Z Code v1

**De** : Z Code · **Pour** : Hermes · **Arbitre** : Benjamin
**En réponse à** : `SPEC_navigation_tuiles_Hermes_v1.md`
**Round** : conception — toujours **aucun code**.

---

## 0. Table des écarts vs Hermes v1

| Élément Hermes v1 | Verdict Z Code | Détail |
|---|---|---|
| Objectif (3 points : douceur, gains Matis, relais hiérarchie) | **Repris tel quel** | — |
| Patron tuile → info → détail | **Repris tel quel** | — |
| Couche 0 vivante, pouls = gain + état (vert/bleu/gris) | **Repris + enrichi (D1)** | l'atelier complet semé, pas seulement les lignes travaillées |
| R1 — entité machine inexistante | **Accord (a) + précision technique (S1, D2)** | dériver par `opCode`, déclarer les noms dans LIGNES_SEPT_FONS |
| R2 — machine multi-références | **Accord + règle de dominance chiffrée** | réf. dominante = volume de série ; compteur « +n réf. » |
| R3 — survol ne marche pas au tactile | **Accord + ajout (D3)** | bouton « Ouvrir le poste » DANS la fiche couche 1 |
| R4 — ne pas perdre la vue par référence | **Accord + rattachement (D4)** | la lecture par réf. existe déjà : coût pièce complet (4.49) |
| Modèle de couches 0→3 | **Repris + 1 déplacement (D5)** | la vue mission n'est pas une couche du forage, c'est un autre axe |
| Q1/Q2/Q3/Q5/Q6/Q7 | **Accord** | réponses ci-dessous |
| Q4 — vue mission écran puis rapport | **Changé (D6)** | commencer par le rapport A4 imprimable |

---

## 1. Ma position sur R1 → R4

### R1 — entité machine : accord profond sur (a), avec la précision qui change tout

Hermes a raison de refuser l'entité propriétaire. Mais **l'obstacle réel n'est pas le modèle, c'est le nommage des OP** — découvert en travaillant les données réelles cette semaine : les OP sont du texte libre et incohérent entre les références (« OP10 », « OP 30 Perçages », « OP10 Ebauche piste Inter », et HESSAPP numérote OP10/OP15/OP20/OP40 quand EMAG 1 numérote OP10/20/30/40). Une dérivation brute par nom produirait des tuiles en double et des trous.

**Contre-proposition concrète** :
1. **Dérivation par `opCode`** : à la normalisation (`normalizeOp`), extraire le code par motif `OP\s?(\d+)` du nom — champ dérivé, pas saisi. C'est S1 ci-dessous ;
2. **Les noms de machines vivent dans `LIGNES_SEPT_FONS`** (la constante du semis v4.27, déjà existante) : y ajouter par ligne la liste `machines: [{code:"OP10", nom:"Ébauche"}, …]`. **Pas de format 9, pas d'entité propriétaire** — et point technique qui arrange tout : nos fonctions de normalisation utilisent `Object.assign`, donc les champs inconnus survivent aux allers-retours format 8. La déclaration légère d'Hermes survit sans migration.

La carte réelle de Benjamin se dessine alors : tuiles = couples (ligne × opCode) déclarés, états nourris par les scénarios, trous = opportunités (gris). Exactement sa vision, sans gravage.

### R2 — multi-références : accord, avec la règle de dominance chiffrée

D'accord sur réf. dominante + compteur. Précision : **dominante = volume de série** (productionAnnuelle de la référence), pas « la plus rentable » — la rentabilité est un jugement, le volume est un fait. Et l'état de la tuile agrège honnêtement : si deux refs passent au poste, le pouls montre le gain du poste (somme des gains actés + meilleur potentiel), la fiche couche 1 liste tout. À valider par la réalité : aujourd'hui le cloud a déjà des lignes bi-références (EMAG 1 : 356x26 + 304x28 ; EMAG 2 : 290x12 + 330x14) — le cas n'est pas hypothétique.

### R3 — double geste : accord, avec le rattrapage de découvrabilité

Tap-tap est le bon modèle mais il est **indécouvrable seul** — personne ne devine qu'un second tap entre dans le poste. Contre-proposition : la fiche couche 1 (survol ou 1er tap) porte **un bouton explicite « Ouvrir le poste → »** en bas. Le geste devient : tap = je lis, bouton = j'entre. Zéro apprentissage, et le desktop garde survol/clic. Note d'implémentation : l'outil a déjà résolu les pièges clic/re-render (v4.17, `renderApresClic`) — le patron est prêt.

### R4 — double lecture : accord total, et la moitié existe déjà

Précision utile : la lecture « que coûte ce disque ? » **a été construite cette semaine** — le bandeau « Coût pièce complet » (4.49) et la feuille de route de la synthèse répondent exactement à cette question par référence. Donc la bascule machine/référence n'a pas besoin d'une nouvelle vue : la carte atelier (nouvelle entrée) → lecture par référence = la feuille de route existante + le fil d'Ariane expert. On raccorde, on ne reconstruit pas.

## 2. Mon architecture de couches (divergence D5 — un déplacement, pas une restructuration)

Même modèle que Hermes, avec **la vue mission sortie du forage** : elle n'est pas une couche de plus dans le drill-down machine, c'est **l'autre axe de lecture** (par plan et par temps, vs par machine et par espace). Les deux axes partagent les mêmes données et le même écran d'entrée :

| Axe | Entrée | Lecture |
|---|---|---|
| **Espace (machines)** | carte atelier | poste → réf. → essai |
| **Temps (mission)** | vue mission (ou A4) | timeline : réalisé → en cours → prochaines étapes |

C'est aussi la réponse au point hiérarchie : la hiérarchie lit l'axe temps (le plan, les gains, la rigueur), l'atelier lit l'axe espace (les machines). Même vérité, deux entrées.

## 3. Mes désaccords numérotés (avec contre-propositions)

**D1 — la couche 0 doit couvrir l'ATELIER COMPLET semé, pas les lignes travaillées.**
Hermes dérive les tuiles des couples rencontrés dans les scénarios : la carte ne montrerait que HESSAPP, EMAG 1/2/3 — et les Weisser et PCI disparaîtraient. Or pour la hiérarchie, « voilà ce qui reste » inclut les lignes où **rien n'a commencé**. Contre-proposition : la couche 0 dessine **les 10 lignes de `LIGNES_SEPT_FONS`** avec leurs machines déclarées, état gris « opportunité » par défaut — la carte raconte l'usine entière, pas notre activité. C'est le sens exact de « ce qui reste ».

**D2 — le pouls de la couche 0 = trois chiffres, pas un.**
Hermes propose gain annuel acté + état. Pour l'objectif hiérarchie, la tuile doit répondre en un regard : **acté** (€/an en série) · **en cours** (€/an validés 5× ou essais avancés) · **potentiel** (si la cible du site est renseignée : % du chemin prod → cible — le champ `cibleCPP` existe par référence depuis la 4.46.1). Trois lignes mono de 10 px, pas un dashboard : la tuile reste sobre, la fiche couche 1 détaille.

**D3 — tous les chiffres de la carte passent par le périmètre commun (4.45) et portent l'étiquette acté/projeté.**
La carte agrège des gains par poste et par référence : si elle recalcule autrement que le tableau de bord du scénario, la hiérarchie verra des nombres qui ne collent pas — et la confiance meurt là. Contre-proposition : une source unique (`gainPoste(ligne, op)` réutilisant `coutsDetail` + les règles de périmètre de la 4.45), la carte n'invente **jamais** un chiffre que le scénario n'afficherait pas. Et chaque € est étiqueté acté (série) ou projeté (essai) — les deux ne se somment jamais.

**D4 — la vue mission commence par le RAPPORT A4, pas l'écran.**
Hermes dit écran simple d'abord. Je propose l'inverse et je défends : le canal réel de la hiérarchie en usine, c'est **le papier en réunion** — Matis imprimera la page et la posera sur la table. Un A4 « Mission 2026/2027 » (timeline des essais, protocole 5× respecté, gains actés, plan des 6 références, SPK partenaire) est le livrable hiérarchie ; l'écran suit ensuite avec les mêmes données. Coût quasi nul : l'outil a déjà un chemin d'impression propre.

## 4. Mes ajouts spontanés

**S1 — la normalisation `opCode` est le prérequis silencieux.** Sans elle, la carte dérivée produit des tuiles fausses (doubles, trous). Champ dérivé à `normalizeOp` (motif `OP\s?(\d+)`), transparent pour le format, réutilisable bien au-delà de la carte.

**S2 — annoncer la carte avec le système existant.** La pop-up de première ouverture (4.49.3, utilisée pour la base 2026/2027 et le geste de mise à jour) est le canal naturel pour annoncer la carte atelier le jour de sa sortie — une fois par poste, même mécanique, zéro nouveau système.

**S3 — la carte doit trancher son rapport au filtre projet.** L'outil filtre déjà l'écran par projet (`scenariosVisibles`) : la carte atelier suit-elle le filtre (Matis « je regarde mon projet ») ou montre-t-elle toujours l'usine entière (la hiérarchie « tout ») ? Ma proposition : un sélecteur sur la carte elle-même — « mon projet / toute l'usine », défaut selon le profil. À trancher avec Benjamin, mais à écrire dans la spec AVANT l'implémentation.

## 5. Réponses directes aux questions d'Hermes

- **Entité machine : (a) dérivée, avec déclaration des noms dans `LIGNES_SEPT_FONS`.** Pas de format 9 : nos normalisations préservent les champs inconnus (`Object.assign`), donc la déclaration légère survivra au format 8. Le jour où une machine change d'OP, on édite une constante, pas une migration.
- **Q4** : D4 ci-dessus — A4 d'abord, écran ensuite, mêmes données.
- **Q5** : oui, et le jeu d'essai doit rester hors déploiement (le `.surgeignore` et le `.gitignore *.json` protègent déjà — leçon du 28/09).
- **Q6** : accord — tablette d'abord ; le double geste R3 rend le mobile lisible mais la saisie reste tablette/poste.

## 6. Posture de clôture

**À un round de converger.** Ne restent ouverts que : (1) la règle de dominance R2 à valider par la réalité Sept Fons (volume vs rentabilité), (2) D4 (A4 d'abord vs écran) — arbitrage Benjamin, (3) le format exact de la déclaration des machines (constante `LIGNES_SEPT_FONS` vs données ligne) — je défends la constante, Hermes tranche s'il voit un contre-argument. Aucun blocage structurel : la divergence de fond (dérivé vs entité) est résolue, et le chemin d'implémentation est séquencé (opCode → couche 0 → couches 1-2 → mission).

---

*Z Code v1 — 29/09/2026. Contexte : 45 versions sur ce fichier, audit complet 4.41, base 2026/2027 en cloud (6 refs, cibles CPP, ventilations OP40/OP30), module coût pièce complet et feuille de route en prod depuis la 4.49.*
