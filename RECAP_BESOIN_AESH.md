# Récapitulatif du besoin — Outil d'optimisation AESH

> **Destinataires** : Claude (analyse technique) + une AESH référente (validation terrain)
> **Auteur** : Benjamin Rouquette
> **Date** : septembre 2026
> **Objectif du document** : présenter le besoin fonctionnel de l'outil sans le jargon technique, pour valider que l'outil répond bien au vécu du terrain.

---

## 🎯 À quoi sert cet outil ?

Dans un collège (et plus tard dans une école primaire), un **AESH** (Accompagnant d'Élève en Situation de Handicap) aide des élèves qui ont besoin d'un coup de pouce pour suivre les cours. Le problème, c'est que :

- Le **nombre d'AESH** est limité (on en a pas autant qu'on voudrait)
- Chaque AESH a un **nombre d'heures** à faire dans la semaine
- Les élèves ont des besoins très différents : certains ont besoin d'un suivi **individuel** (1 adulte rien que pour eux), d'autres sont en groupe **mutualisé** (1 adulte pour 2-3 élèves ensemble)
- Les **emplois du temps** des classes sont compliqués : cours de 1h, de 2h, parfois des demi-journées entières avec plusieurs matières

Aujourd'hui, l'attribution des AESH se fait **à la main**, au feeling, par les coordinateurs. C'est long, c'est stressant, et souvent on rate des opportunités (une AESH disponible qui pourrait couvrir un élève qu'on a oublié).

**L'outil doit faire ce travail automatiquement** : à partir des emplois du temps des classes et de la liste des élèves à accompagner, il propose **3 scénarios d'attribution** parmi les meilleurs possibles, avec un score qui explique pourquoi tel scénario est bon.

---

## 👥 Les personnes concernées

### L'AESH
- A un **nombre d'heures par semaine** à effectuer (souvent 24h, 30h, ou 35h)
- Est **référente** d'un petit groupe stable : 1 ou 2 élèves en suivi individuel, plus 1 à 3 classes où elle accompagne des élèves mutualisés
- Travaille sur plusieurs classes, pas une seule
- Ne peut pas être à 2 endroits en même temps

### L'élève en accompagnement individuel (AI)
- A besoin d'une AESH **sur des blocs de demi-journée** entiers (matin OU après-midi)
- L'AESH ne peut pas être coupée au milieu du bloc : si l'AESH est avec cet élève le matin, elle est avec lui tout le matin
- A des **matières prioritaires** où sa présence est cruciale : Histoire-Géo → Français → Maths → SVT → Physique-Chimie (dans cet ordre)
- A parfois des **soins paramédicaux** (orthophonie, kiné, CMP…) sur certains créneaux : ces créneaux sont **indisponibles**, pas besoin d'AESH à ce moment-là

### L'élève en accompagnement mutualisé (AM)
- Est avec d'autres élèves mutualisés dans la même classe
- Est couvert à l'**heure** (pas en bloc) : une AESH peut couvrir un cours de maths de 1h, puis un cours de français de 1h, etc.
- Mêmes **matières prioritaires** que les AI

### Le coordinateur (utilisateur de l'outil)
- Entre les données de l'établissement (classes, EDT, élèves, AESH)
- Lance l'optimisation
- Compare les 3 scénarios proposés
- Choisit celui qui lui convient (ou ajuste à la marge)

---

## 📋 Les données à fournir en entrée

L'utilisateur doit pouvoir tout configurer, pas de champs figés :

| Donnée | Exemple | Format |
|---|---|---|
| Nom de l'établissement | "Collège Victor Hugo" | Texte libre |
| Type | Collège (v1) / Primaire (v2) | Choix |
| Liste des classes | 6èmeA, 6èmeB, 5èmeA, 4èmeC | Texte libre |
| Emploi du temps de chaque classe | Voir ci-dessous | XLS, PDF ou Word |
| Liste des AESH | 8 AESH, avec heures/semaine | Tableau |
| Liste des élèves AI | Nom + nb blocs/semaine + matières prioritaires + soins | Tableau |
| Liste des élèves AM | Nom + classe + matières prioritaires | Tableau |

**Pour l'emploi du temps**, on accepte **3 formats** parce que les établissements utilisent des outils différents (Pronote, EduConnect, tableaux Excel maison…) :
- **XLS** (le plus simple, structuré en cases)
- **PDF** (souvent exporté depuis Pronote)
- **Word** (parfois fait à la main par les coordinateurs)

Les cours peuvent être :
- de **1 heure**
- de **2 heures**
- ou un **bloc de demi-journée** entière avec plusieurs matières

Et les emplois du temps peuvent être **différents sur les semaines paires et impaires** (certains cours alternent une semaine sur deux).

---

## ⚙️ Les règles du jeu (à respecter impérativement)

### Règle 1 — Une AESH ne peut pas être à deux endroits à la fois
Sur un créneau donné (une heure ou un bloc), une AESH est soit avec un élève individuel, soit avec un groupe mutualisé, soit **libre**. Pas de mélange.

### Règle 2 — Les blocs de demi-journée sont indivisibles pour les AI
Si un AI est couvert le matin, l'AESH est avec lui **tout le matin** (8h-12h par exemple). On ne peut pas couper le bloc.

### Règle 3 — Les mutualisés se gèrent à l'heure
Une AESH peut couvrir un cours de maths de 14h à 15h, puis un cours de français de 15h à 16h dans une autre classe. C'est fractionnable.

### Règle 4 — Une AESH a un portefeuille stable
Une AESH est référente de **1 ou 2 élèves individuels** ET de **jusqu'à 3 classes mutualisées**. C'est son périmètre, et c'est stable sur l'année (ou au moins sur le semestre).

### Règle 5 — Priorité aux matières clés
Quand l'outil arbitre entre plusieurs options possibles, il privilégie les matières dans cet ordre : **Histoire-Géo → Français → Maths → SVT → Physique-Chimie**.

### Règle 6 — Les soins sont des absences
Si un élève AI a un rendez-vous orthophonie le mardi matin, ce créneau est **sorti du besoin** : pas besoin d'AESH.

### Règle 7 — Les heures hebdomadaires sont le plafond
Une AESH qui fait 24h/semaine ne peut pas en faire 25. C'est la contrainte dure numéro 1.

---

## 🎬 Comment l'outil doit être utilisé (scénario utilisateur)

1. **Je crée mon établissement** (nom, type, classes)
2. **J'importe les emplois du temps** (un par classe, XLS/PDF/Word)
3. **J'ajoute mes AESH** (nom + heures/semaine)
4. **J'ajoute mes élèves accompagnés** (AI ou AM, avec leurs besoins)
5. **Je clique sur "Optimiser"**
6. **L'outil me propose 3 scénarios**, chacun avec :
   - Le détail des attributions (quelle AESH avec quel élève, quel jour, quel créneau)
   - Un score qui explique pourquoi ce scénario est bon (ex : "Couvre 95% des matières prioritaires")
   - Les trous restants (ex : "Pas d'AESH pour le cours de SVT du jeudi 14h-15h en 4èmeC")
7. **Je compare les 3 scénarios**, je choisis celui qui me plaît
8. **J'exporte** en Excel, PDF ou vue web pour le partager avec mon équipe / ma hiérarchie

---

## 📦 Ce que l'outil doit livrer en sortie

Pour chacun des 3 scénarios :

- **Le planning AESH par AESH** (tableau semaine)
- **Le planning AESH par classe** (qui est avec quelle classe à quel moment)
- **Le récap par élève** (combien d'heures couvertes, sur quelles matières)
- **La liste des manques** (créneaux non couverts, à arbitrer à la main)
- **Le score de couverture** (% de matières prioritaires couvertes)

Format de sortie : **Excel** (pour l'archivage et le partage), **PDF** (pour la lecture), et **vue web interactive** (pour explorer).

---

## 🏫 La suite : le module Primaire (v2)

Pour l'école primaire, la logique est **différente** :
- Pas de notion de matière (on est en demi-journée ou quart de journée)
- La granularité est **plus fine** : le matin, le début d'après-midi, la fin d'après-midi
- Les mutualisés peuvent correspondre à des **ateliers** (lecture, arts plastiques, sport…) ou à des **regroupements multi-niveaux**

On garde la même architecture, mais on branche un **adaptateur "Primaire"** à côté de l'adaptateur "Collège" actuel.

---

## ❓ Questions encore en suspens (à valider avec une AESH)

1. Si un AI n'est pas couvert sur une matière prioritaire, est-ce que l'AESH référente peut exceptionnellement couvrir une autre matière ? (ex : l'élève a maths ET histoire-géo prioritaires, mais l'AESH n'a que 2h dispo cette semaine → laquelle choisir ?)
2. Comment on réagit si l'EDT change en cours d'année (un prof est remplacé, un cours est déplacé) ? Est-ce qu'on relance juste l'optimisation ?
3. Si on manque d'AESH (genre il en faut 10 et on en a 8), l'outil doit-il proposer quand même un plan "dégradé" qui couvre le maximum, ou refuser de calculer ?
4. L'AESH référente doit-elle **rencontrer** ses élèves en début d'année, ou l'outil peut s'en charger ?

---

## 💬 Questions à poser à l'AESH qui lira ce document

- Est-ce que la règle "1 AESH = 1-2 AI + jusqu'à 3 classes mutualisées" correspond à ta réalité ?
- Est-ce que l'ordre des matières prioritaires te semble juste, ou tu changerais ?
- Est-ce que tu as déjà vécu un cas où l'attribution était vraiment injuste / absurde ? (ça nous donnera des exemples à tester dans l'outil)
- Est-ce que la sortie "Excel + vue web + PDF" te suffit, ou tu voudrais autre chose (genre impression poster pour affichage dans la salle des profs) ?
