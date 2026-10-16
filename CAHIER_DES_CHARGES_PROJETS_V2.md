# Cahier des charges — Projets v2 (Suivi_optimisation_SPK)

Base : v4.1.1 (modèle par étiquettes — voir CHANGELOG.md, entrées 4.1.0 et 4.1.1).
Ce document decrit les évolutions demandées suite à l'usage de la v4.1.1, à destination
d'une implémentation externe (Hermès + GLM 5.3 Flash). Aucune ligne de code n'a été écrite
pour ce document — c'est une spec à valider avant codage.

Convention : chaque section a une **Décision par défaut**, proposée par Claude. Si rien
n'est dit avant le passage en codage, l'implémentation suit cette décision par défaut.

---

## 0. Ce qui existe déjà et ne doit PAS être reconstruit

À vérifier par l'implémenteur avant de coder quoi que ce soit, pour ne pas dupliquer :

- **Un scénario peut déjà appartenir à plusieurs projets simultanément.** Le modèle de
  données (`projet.tags: [{ligneId, referenceId, opId, scenarioId}]`) n'a aucune contrainte
  d'unicité. Testé et vérifié en v4.1.0/4.1.1 avec deux projets tageant le même scénario.
- **Un projet peut déjà couvrir plusieurs lignes de production**, pour la même raison —
  chaque étiquette est indépendante des autres.
- **Palette de couleurs cyclique déjà présente** : `const OUTIL_COLORS = [...]` (8 couleurs),
  utilisée aujourd'hui pour distinguer les outils d'un scénario par une bordure de couleur.
  Le même mécanisme (index dans le tableau, cycle modulo) doit être réutilisé pour les
  couleurs de projet (§3) plutôt que d'inventer un second système.
- **Filtrage des cartes de projet par ligne active** (`projetVisibleSurLigne`), ajouté en
  v4.1.1 — ne pas retoucher sans raison, c'est un correctif récent et testé.

---

## 1. Rendre visibles les actions déjà existantes (correctif d'ergonomie)

### 1.1 Entrer dans un projet / le modifier

**Constat.** Cliquer une carte de projet l'active comme filtre (et comme cible d'étiquetage
automatique à la création d'un scénario). La modifier passe par une icône ⚙ 22×22 px,
transparente jusqu'au survol, en coin de carte — trouvée par personne en usage réel.

**Décision par défaut.** Deux actions distinctes et visibles sur chaque carte, sans attendre
un survol :
- cliquer le **corps de la carte** = filtrer/désactiver (comportement actuel, inchangé) ;
- un bouton texte **« Modifier »**, visible en permanence (pas seulement au survol), dans un
  coin de la carte — remplace l'icône ⚙ actuelle. Le texte plutôt qu'un pictogramme : ce
  public n'a pas à deviner qu'un engrenage veut dire « paramètres ».

### 1.2 Bouton d'enregistrement du panneau projet

**Constat.** Les champs s'enregistrent en réalité tout seuls (évènement `change` sur chaque
champ), et le bouton « Fermer » sauvegarde avant de fermer. Rien n'est perdu, mais rien ne le
dit non plus.

**Décision par défaut.** Renommer le bouton actuel « Fermer » en **« Enregistrer »** (il fait
déjà exactement ça). Ne pas ajouter de second bouton « Enregistrer » distinct de la fermeture
— un bouton qui fait une seule chose clairement nommée vaut mieux que deux boutons dont un ne
sert à rien de plus que l'autre.

### 1.3 Bouton de création de projet trop discret

**Constat.** `button.ghost.small` — 11 px, fond transparent, à côté d'un bouton primaire bleu
plein (« + Ajouter un scénario ») qui capte l'œil en premier.

**Décision par défaut.** Retirer `.small`, passer en style `.primary` ou au moins en style
`.ghost` de taille standard avec une bordure visible en permanence (pas seulement au survol).
Le bouton « + Créer un projet » doit être trouvable au même titre que « + Ajouter un
scénario », pas être un lien discret à côté.

### 1.4 Visibilité des projets multiples sur un même OP

**Constat.** La capacité existe (voir §0) mais rien ne la rend visible à l'échelle d'un OP ou
d'une référence — il faut inspecter chaque carte de scénario une par une pour voir ses
étiquettes.

**Décision par défaut.** Pas de nouvelle capacité de données. Ajouter un repère de lecture :
sous l'en-tête de la référence/OP (zone `db-op-head` du tableau de bord, et zone équivalente
dans la vue scénarios), afficher un petit résumé du type « 2 projets sur cet OP » avec les
pastilles de couleur des projets concernés (voir §3), cliquable pour filtrer. Reste un
affichage, aucun changement du modèle de données.

---

## 2. Responsable de projet : liste gérée + couleur

### 2.1 Modèle de données

Nouvelle liste globale, gérée dans Options (comme le sont déjà les autres réglages de
l'outil — modules, tolérances) :

```
responsables: [
  { id, nom, couleur }   // couleur : une valeur hex, choisie via un input type="color"
]
```

**Décision par défaut.** `projet.responsable` cesse d'être un champ texte libre et devient une
référence (`responsableId`) vers cette liste — avec une liste déroulante dans le panneau
projet, plus une option « + Ajouter un nouveau responsable » directement dans le menu
déroulant (pas besoin d'aller dans Options pour créer la toute première fois). Les projets
existants dont `responsable` est encore une chaîne libre (créés en v4.1.x) sont migrés
automatiquement : à la première ouverture après mise à jour, chaque valeur texte distincte
devient un responsable de la liste, avec une couleur assignée automatiquement dans l'ordre de
la palette (§3) — aucune saisie perdue, aucune ressaisie demandée.

**Alternative écartée** : garder du texte libre et faire correspondre une couleur au nom
saisi. Rejetée — une faute de frappe (« Julien » vs « Julien » avec espace en trop) casserait
silencieusement l'association couleur, sans qu'on comprenne pourquoi la couleur a disparu.

### 2.2 Gestion dans Options

Nouveau bloc dans le panneau Options : liste des responsables existants (nom + pastille de
couleur + bouton supprimer), plus une ligne d'ajout (nom + sélecteur de couleur `<input
type="color">`). Suppression d'un responsable : les projets qui le référencent repassent en
« aucun responsable » (jamais de suppression en cascade d'un projet à cause de ça).

### 2.3 Application visuelle

**Décision par défaut.** La couleur du responsable s'applique à la **bordure gauche** de la
carte de projet (`.pj-carte`), qui aujourd'hui code le statut. Le statut reste lisible via son
badge texte existant (`.pj-statut`, déjà présent, déjà coloré indépendamment) — rien n'est
perdu, l'axe couleur de la bordure change juste de signification, du statut vers la personne.

**Point à trancher avant codage** si ce choix ne convient pas : l'alternative est de garder la
bordure sur le statut et d'ajouter un petit repère séparé (pastille ronde à côté du nom du
pilote) pour la couleur du responsable — plus fidèle à l'existant, un peu plus chargé
visuellement. Dites lequel des deux avant que l'implémenteur commence.

---

## 3. Identité visuelle par projet (indépendante du responsable)

**Constat.** Aujourd'hui, l'étiquette « active » d'un scénario est bleue pour n'importe quel
projet — si un scénario appartient à 3 projets, ses 3 pastilles sont visuellement identiques,
seul le texte les distingue.

**Décision par défaut.** Chaque projet reçoit une couleur d'identité à sa création, assignée
automatiquement par cycle sur `OUTIL_COLORS` (même mécanisme que les outils, §0) — pas de
sélecteur de couleur manuel pour le projet lui-même (ça, c'est réservé au responsable, §2, où
la couleur porte une vraie signification durable — la personne). Cette couleur de projet
s'applique :
- au fond de l'étiquette (`.tag-pill.on`) quand elle est active pour CE projet précis, au lieu
  du bleu unique actuel ;
- au repère ajouté en §1.4 (pastilles par OP/référence) ;
- optionnellement, à un liseré fin sur la carte de scénario elle-même quand un seul projet est
  actif comme filtre (à évaluer selon la charge visuelle réelle une fois codé — ne pas sur-
  spécifier avant d'avoir vu le rendu).

**Ne pas fusionner avec la couleur du responsable (§2).** Ce sont deux informations
différentes — « quel projet » contre « qui le pilote » — same couleur pour les deux
créerait de la confusion (une carte pourrait sembler porter deux couleurs contradictoires
selon l'endroit où on la regarde). Les garder sur deux axes visuels distincts : bordure de
carte = responsable (une personne, une couleur stable dans le temps), étiquette/pastille =
projet (assignée à la création, cycle automatique).

---

## 4. Description du projet : zone de texte étendue

**Constat.** Le champ `problematique` est un `<input type="text">` une ligne — impossible d'y
décrire un objectif et les moyens mis en œuvre.

**Décision par défaut.** Remplacer par un `<textarea>` (4-6 lignes visibles, redimensionnable
verticalement), renommé **« Description »** plutôt que « Problématique ». Un seul champ libre,
pas deux champs séparés « objectif » / « moyens » — personne ne maintient proprement deux
champs de prose libre distincts dans la durée, ça ajoute de la friction sans bénéfice réel.
Le champ existant `problematique` est renommé en conservant son contenu (aucune perte de
données à la migration, simple changement d'étiquette et de type de saisie).

---

## 5. Points à trancher avant transmission à l'implémentation

Liste courte, à valider ou corriger avant de lancer Hermès + GLM 5.3 Flash :

1. Couleur du responsable sur la bordure de carte (§2.3) — remplace le statut comme axe
   couleur, statut gardé en texte. **Confirmer ou choisir l'alternative** (bordure = statut,
   pastille séparée = responsable).
2. Un seul champ « Description » en zone de texte (§4), pas deux champs séparés. **Confirmer.**
3. Couleur de projet assignée automatiquement (cycle sur palette), pas de sélecteur manuel
   pour le projet lui-même — seul le responsable a un vrai sélecteur de couleur. **Confirmer.**
4. Le repère « plusieurs projets sur cet OP » (§1.4) : uniquement dans le tableau de bord, ou
   aussi dans la vue scénarios au quotidien ? Impact sur la charge visuelle de l'écran
   principal à mesurer une fois un premier jet codé.

## 6. Hors périmètre (rappel, décision déjà actée)

Rattacher un projet à une référence disque entière (plutôt qu'à des scénarios un par un) —
écarté lors de la discussion précédente : deuxième granularité d'étiquette, questions
d'héritage/exception non résolues, complexité pour un besoin quasi inexistant. Ne pas le
réintroduire dans cette itération.

## 7. Tests attendus (pour l'implémentation)

- Migration d'un `responsable` texte libre existant vers la liste gérée : aucune perte, une
  entrée par valeur distincte, couleur assignée automatiquement.
- Suppression d'un responsable référencé par des projets : les projets repassent à « aucun »,
  aucune suppression en cascade.
- Couleur de projet stable dans le temps pour un même projet (pas de recalcul à chaque rendu
  qui ferait « sauter » les couleurs d'une session à l'autre) — assignée une fois à la
  création, stockée avec le projet.
- Le champ Description accepte et restitue un texte multi-paragraphes (retours à la ligne
  conservés à l'export/import).
- Non-régression : les 102 tests existants (v4.1.1) restent au vert.
