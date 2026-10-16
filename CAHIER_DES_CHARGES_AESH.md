# Cahier des charges technique — Outil d'optimisation AESH

> Dérivé de [RECAP_BESOIN_AESH.md](RECAP_BESOIN_AESH.md). Ce document tranche les choix
> techniques pour lancer le développement du MVP.

---

## 1. Choix d'architecture

- **Frontend** : React (Vite) + TypeScript, hébergement Surge.sh (cohérent avec le reste
  du parc d'outils).
- **Backend** : Python (FastAPI), parce que le cœur du produit — le solveur de contraintes
  — a besoin d'un vrai moteur d'optimisation, pas de bricolage JS. Déployé séparément
  (Render/Railway ou conteneur Supabase Edge si suffisant — à trancher à l'implémentation
  selon la charge de calcul réelle).
- **Solveur d'optimisation** : **Google OR-Tools, CP-SAT**. C'est le bon outil pour un
  problème d'affectation sous contraintes dures (heures, chevauchements) avec un objectif
  de priorité souple (matières). Pas besoin d'un solveur maison.
- **Base de données** : Supabase (Postgres), cohérent avec l'existant. Tables : établissement,
  classes, créneaux EDT, AESH, élèves (AI/AM), scénarios générés, affectations.
- **Auth** : Supabase Auth, un compte par coordinateur/établissement.

---

## 2. Modèle de données (v1 — Collège)

```
Etablissement { id, nom, type }
Classe { id, etablissement_id, nom }
Creneau { id, classe_id, jour, heure_debut, heure_fin, matiere, semaine (paire/impaire/toutes) }
Aesh { id, etablissement_id, nom, heures_semaine }
ElèveAI { id, nom, classe_id, matieres_prioritaires[], soins[] (jour, heure_debut, heure_fin) }
ElèveAM { id, nom, classe_id, matieres_prioritaires[] }
Scenario { id, etablissement_id, score_couverture, cree_le }
Affectation { id, scenario_id, aesh_id, creneau_id, cible_type (AI/AM), cible_id }
```

Le **bloc demi-journée** d'un AI n'est pas stocké comme un créneau à part : c'est une
vue calculée qui regroupe tous les créneaux consécutifs d'une classe sur matin/après-midi.
L'optimiseur raisonne directement sur ces blocs pour les AI (règle 2), et sur les créneaux
horaires bruts pour les AM (règle 3).

---

## 3. Le moteur d'optimisation (CP-SAT)

**Variables** : `x[aesh, cible, creneau] ∈ {0,1}` — l'AESH couvre cette cible sur ce créneau.

**Contraintes dures** :
1. Une AESH ne peut couvrir qu'une cible par créneau (règle 1).
2. Un bloc AI est couvert entièrement ou pas du tout par la même AESH (règle 2) — modélisé
   en fusionnant les créneaux du bloc en une seule variable de décision.
3. Somme des heures affectées à une AESH ≤ son plafond hebdomadaire (règle 7).
4. Portefeuille stable (règle 4) : une AESH ne peut être affectée qu'à des AI/classes
   présents dans son portefeuille déclaré. **Décision** : le portefeuille est une donnée
   d'entrée (le coordinateur le déclare), pas une variable que l'optimiseur invente — ça
   correspond à la réalité terrain (référente stable) et ça réduit drastiquement l'espace
   de recherche.
5. Créneaux de soins exclus du besoin (règle 6) : simplement absents de la liste des
   créneaux à couvrir pour cet élève.

**Objectif** : maximiser une somme pondérée où le poids de chaque créneau couvert dépend
du rang de sa matière dans l'ordre de priorité (règle 5) — poids décroissant
Histoire-Géo > Français > Maths > SVT > Physique-Chimie > reste.

**Génération de 3 scénarios distincts** : on résout une première fois, puis on ajoute une
contrainte "no-good cut" qui interdit de reproduire exactement la même affectation, et on
relance deux fois de plus. Chaque scénario reste proche de l'optimum mais explore une
combinaison différente — c'est ce qui donne un vrai choix au coordinateur plutôt que 3
variantes cosmétiques.

**Cas sous-effectif (question ouverte n°3 du besoin)** : tranché — l'outil calcule
toujours le meilleur plan possible même incomplet ("dégradé"), et liste les trous
séparément. Refuser de calculer n'aiderait personne ; c'est la liste des manques qui sert
de justificatif pour demander plus de moyens.

---

## 4. Import des emplois du temps

Trois formats, fiabilité décroissante — **décision : un pipeline commun avec écran de
relecture obligatoire**, parce que le parsing PDF/Word est intrinsèquement imparfait et
qu'une erreur silencieuse ici casse tout l'optimiseur en aval.

1. **XLS** : parsing direct (pandas/openpyxl) vers la grille `Creneau`. Fiable, pas de
   relecture nécessaire si le format suit un gabarit fourni par l'outil.
2. **PDF** : extraction de tableau (pdfplumber/camelot) vers la même grille, **puis écran
   de relecture** où le coordinateur corrige les cases mal lues avant validation.
3. **Word** : parsing des tableaux (python-docx) vers la même grille, même écran de
   relecture.

Semaines paires/impaires : champ `semaine` sur chaque créneau, géré dès le modèle de
données, pas comme un cas spécial ajouté après coup.

---

## 5. Parcours utilisateur (MVP)

1. Créer établissement + classes
2. Importer les EDT (par classe) → relecture/correction si PDF/Word
3. Ajouter les AESH (nom, heures/semaine)
4. Ajouter les élèves AI/AM (portefeuille, matières prioritaires, soins)
5. Lancer l'optimisation → 3 scénarios
6. Comparer (planning par AESH, planning par classe, récap élève, manques, score)
7. Exporter (Excel, PDF, vue web)

---

## 6. Phasage du développement

- **Phase 0 — MVP cœur métier** : saisie manuelle des EDT (pas d'import fichier), modèle
  de données, solveur CP-SAT, 3 scénarios, exports Excel/PDF. Objectif : valider que
  l'algorithme produit des plans que l'AESH référente juge crédibles, avant d'investir
  dans le parsing de fichiers.
- **Phase 1** : import XLS (le format le plus fiable).
- **Phase 2** : import PDF puis Word, avec écran de relecture.
- **Phase 3** : vue web interactive pour explorer les scénarios (au-delà des exports statiques).
- **Phase 4** : adaptateur "Primaire" (granularité demi-journée/quart de journée, ateliers).

---

## 7. Points à valider avec l'AESH référente avant de coder le Phase 0

Repris tels quels du besoin — ce sont les seuls points où la réponse change réellement
l'implémentation :

- Arbitrage quand une AESH n'a pas assez d'heures pour couvrir 2 matières prioritaires
  d'un même élève (quelle règle de départage encoder dans l'objectif ?)
- Le format de sortie Excel + PDF + vue web suffit-il, ou faut-il aussi un format
  "poster" imprimable ?

Tout le reste (règles 1 à 7, scénario utilisateur, phasage) est actionnable tel quel.
