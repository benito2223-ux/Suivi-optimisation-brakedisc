# Spec — la vue plaquette globale : « où elle sert, et combien rapporte sa généralisation »

**De** : Benjamin Rouquette, 10/11/2026 · **Pour** : Hermes (conception, puis code après validation)
**Statut** : SPEC — rien de codé. Benjamin a tranché les trois décisions de structure le 10/11 (voir §2).

## 1. Le besoin en une phrase

Pour une plaquette donnée (vue **MABEC + désignation ISO**), voir **où elle sert dans l'usine** —
ligne, référence, OP, quantité — et **extrapoler** : quand un essai valide cette plaquette, combien
rapporterait son déploiement **global**, pas seulement sur le poste de l'essai.

## 2. Décisions Benjamin (10/11/2026, verrouillées)

1. **Clé de regroupement = la désignation ISO** (la plaquette physique), tous MABEC confondus.
   Un même ISO porté par plusieurs MABEC est normal : chaque usage montre son MABEC.
2. **L'extrapolation est prospective à trois leviers activables**, le prix étant la variable de
   départ : (a) **prix seul**, (b) **prix + charnière**, (c) **+ temps de cycle** si besoin.
   Chaque levier ne chiffre que si la donnée existe ; un usage non chiffrable est nommé, jamais
   complété (constitution §5.6, « jamais d'invention »).
3. **Les trois écrans d'un coup** : Catalogue, Plan de conversion, « Ailleurs dans l'usine » de la
   fiche scénario.

## 3. Le calcul — une source unique

**`usagesPlaquette(iso)`** (fonction pure, testée) : balaye `lignes → références → OP → scénario
de production de l'OP` (règle du bandeau 4.114 : la prod du jour — scénario en série s'il existe,
sinon ★) et retourne chaque logement portant cette ISO :

```
{ ligne, reference, opCode, scénario, mabec, designation, prix,
  aretes, charniereVisee, charniereMesuree?, volume?,
  plaquettesParAn (= plaquettesParAn()), coutAnnuel (= prix × plaquettesParAn) }
```

- Normalisation de l'ISO pour le rapprochement : trim, casse, espaces multiples — la clé
  d'affichage reste la forme saisie (`matisClePorteOutil` comme modèle).
- Volume manquant → l'usage apparaît, marqué « volume annuel à saisir », **exclu du total**
  (jamais un 0 qui voudrait dire rien).

**`extrapoleGlobale(iso, leviers)`** (fonction pure) — les trois leviers, cumulables, appliqués
à chaque usage sur son périmètre propre :

| Levier | Ce qu'il change | Condition d'application |
|---|---|---|
| **prix** | le prix de la plaquette de l'usage (variable de départ) | toujours chiffrable si l'usage a un prix |
| **charnière** | la charnière visée remplacée par la charnière cible (ex. le mesuré de l'essai) | la charnière cible > 0 |
| **temps de cycle** | l'écart de cycle × taux horaire de la ligne | `tempsCoupe` renseigné des deux côtés ; sinon l'usage sort « cycle non chiffré » nommé |

Sortie par usage : coût actuel/an → coût simulé/an → écart ; **total global** = Σ des usages
chiffrables, avec le compte des exclus et leurs noms. **Étiquette obligatoire** :
« SIMULATION — si cette plaquette était déployée au global, à conditions égales » — jamais
additionnée aux gains actés ou projetés (constitution §3.4), jamais présentée comme actée.

## 4. Les trois écrans

1. **Catalogue** : chaque article (MABEC + désignation) porte un accès « Où elle sert ? » —
   panneau : la liste des usages (ligne · réf · OP · MABEC · plaquettes/an · coût/an) + le bloc
   à trois leviers simulables en direct (prix cible, charnière cible, cycle) avec le total global
   qui suit à la frappe (même logique live que le Plan).
2. **Plan de conversion** : la même carte par ligne d'article — le Plan simule déjà prix et vie
   par article ; y ajouter le détail des usages et le total « toutes lignes confondues, ligne par
   ligne » qu'il calcule déjà mais n'expose pas usage par usage.
3. **Fiche scénario, rubrique « Ailleurs dans l'usine »** : chaque plaquette du scénario montre
   ses AUTRES usages dans l'usine (l'usage courant marqué comme tel) + le bouton « Extrapoler »
   qui pré-remplit la charnière cible avec **le mesuré de l'essai** quand il existe
   (`charniereReelle`), le prix cible avec le prix du scénario, et affiche la simulation.

## 5. Règles constitutionnelles à respecter

- §3.4 : acté / projeté / **simulé** vivent dans des blocs distincts, jamais sommés ;
- §5.6 : un usage sans volume ou sans prix est nommé avec ce qui manque, jamais chiffré en silence ;
- loi du correcteur : la plaquette appartient au **couple (référence × logement)** — deux logements
  du même ISO sur des disques différents peuvent avoir prix et charnière différents, c'est normal ;
- pas de K ni P dans la moindre sortie ; « CRM » interdit ;
- PROD en lecture seule pour la recette.

## 6. Effort et tests d'acceptation (pour le tour de code)

Effort **M** (une fonction pure + deux rendus + un branchement sur « Ailleurs », ~1 tour).

1. `usagesPlaquette` sur une fixture à 2 lignes / 3 usages du même ISO (MABEC différents) → 3
   usages, clés et montants exacts ; un usage sans volume → exclu du total mais listé.
2. `extrapoleGlobale` : prix seul / prix+charnière / +cycle → les trois totaux, au centime ; cycle
   manquant → usage nommé « cycle non chiffré », jamais dans le total.
3. Catalogue et Plan : la même carte rend les mêmes montants (source unique).
4. « Ailleurs dans l'usine » : l'usage courant marqué, le bouton « Extrapoler » pré-rempli avec le
   mesuré de l'essai.
5. Étiquette « SIMULATION » présente partout où un total extrapolé s'affiche.
6. Les 803 tests passent ; comptage rev435 inchangé avant/après ouverture des écrans.
