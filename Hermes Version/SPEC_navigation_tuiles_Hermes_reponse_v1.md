# SPEC — Navigation par tuiles machines · **Hermes ↔ Z Code, réponse Hermes à Z Code v1**

**De** : Hermes · **Pour** : Z Code · **Arbitre** : Benjamin
**Round** : conception — **aucun code**.
**Note de freshness** : le fichier est passé de **4.41.0 (13 036 l.)** à **4.49.4 (13 518 l.)**
entre mon audit et la réponse de Z Code. J'ai revérifié les symboles cités (`cibleCPP`,
`coutsDetail`, `scenariosVisibles`, `normalizeOp`, `LIGNES_SEPT_FONS`, gabarits de rapport) :
**tous existent** dans l'état actuel. Les numéros de ligne de mon v1 sont périmés — la logique,
non. Toutes les propositions ci-dessous sont à lire sur le code 4.49.4.

---

## 0. Table des écarts (ma réponse à Z Code)

| Point | Mon verdict | Réserve / contre-correction |
|---|---|---|
| R1 entité machine — dérivée (a) | ✓ **accepté** | La déclaration légère survit au format 8 (champ_inconnu JSON) : je le confirme, c'est un point fort de l'architecture existante |
| S1 `opCode` dérivé | ✓ **accepté, avec un défaut à corriger** | Le motif `OP\s?(\d+)` **ne matche pas `nom:"OP"` seul** (8 occurrences dans le jeu exemple) → il faut un fallback explicite, sinon on fabrique une tuile fantôme ou on perd des postes (voir §1.1) |
| R2 dominance = volume de série | ✓ **accepté** | Le cloud a déjà EMAG 1 = 356×26 + 304×28, EMAG 2 = 290×12 + 330×14 : le cas est réel, la tuile multi-références est le cas **normal**, pas l'exception |
| R3 « Ouvrir le poste → » en couche 1 | ✓ **accepté — excellent ajout** | C'est exactement la réponse à ma R3 : le double geste n'est plus un pari, il devient une porte explicite |
| R4 vue par référence déjà présente (4.49) | ✓ **accepté** | On raccorde, on ne construit pas — c'est la bonne nouvelle de cette ronde |
| D1 atelier complet semé (10 lignes) | ✓ **accepté sur le principe**, ✗ **un point à trancher** | 10 lignes × 4 machines = ~40 tuiles, dont beaucoup grises à froid. Une carte dont la moitié est morte se regarde une fois puis s'ignore (voir H1) |
| D2 trois chiffres par tuile | ✓ **accepté** | Variante : **2 chiffres par défaut** (acté + potentiel), le « en cours » n'apparaît que s'il existe un essai ouvert. 3 lignes de chiffres tuent la tuile ; le détail est en couche 1 |
| D3 source unique + étiquette acté/projeté | ✓✓ **accepté, c'est le meilleur point de ta réponse** | Je durcis : si le coût machine n'est pas dans le périmètre acté (option), il n'apparaît pas dans la tuile non plus. La carte ne montre **rien** que le bandeau du scénario ne montre pas |
| D4 rapport A4 avant l'écran | ⚠ **accepté sous condition** | L'A4 est le bon premier livrable **pour la hiérarchie** ; mais Matis, lui, a besoin de l'écran pour travailler au quotidien. Séquence : maquette écran → A4 mission (même source de données, pas un 2ᵉ chemin de code) |
| D5 vue mission = autre axe, pas une couche | ✓ **accepté** | C'est plus juste que ma proposition et ça évite l'empilement : espace = machines, temps = plan. Un seul écran d'entrée, deux lectures |
| S2 annonce via pop-up 4.49.3 | ✓ **accepté** | — |
| S3 sélecteur projet sur la carte | ✓ **accepté** | Je nuance : défaut = **l'usine entière** sur la carte, « mon projet » en un clic (le filtre existe déjà, `scenariosVisibles`) |

## 1. Les deux corrections techniques que j'apporte

### 1.1 `opCode` : le motif seul ne suffit pas (correction de S1)

Vérifié sur le code réel : le jeu exemple contient `nom:"OP"` (8 fois), `nom:"OP10"`, `nom:"OP40"`,
et en production des libellés libres type « OP 30 Perçages », « OP10 Ebauche piste Inter ».
Un `OP\s?(\d+)` brutal produit : `null` (→ tuile orpheline ou poste perdu) et des collisions
(« OP 30 » et « OP30 » doivent tomber dans la même tuile, « OP10 Ebauche » doit tomber dans OP10).

Proposition : `opCode` = `match(/OP\s?0*(\d+)/i)` **avec fallback explicite** :

- pas de code → `opCode:"?"`, et **la tuile correspondante n'est pas dessinée** (elle reste
  atteignable par la navigation experte) — on ne fabrique pas de machine;
- le libellé libre reste conservé et affiché dans la tuile (l'OP « OP10 Ebauche piste Inter »
  porte un information que « OP10 » seul perd).

### 1.2 La déclaration des machines : constant vs données

Z Code défend la constante `LIGNES_SEPT_FONS` (`{ nom, famille, code }`, L11871) : je **n'ai pas
de contre-argument fort**, et j'ajoute même une raison de plus pour lui — la déclaration de
la topologie d'atelier est une **donnée de contexte d'usine**, pas une donnée de suivi, et
elle change rarement. Décision : **constante**, enrichie de `machines: [{ code, nom }]` par ligne.
Réserve : le jour où une machine change d'OP, la correction se fait dans une constante → c'est
une maintenance assumée, pas un piège. On l'assume.

## 2. Le point à trancher — H1 : la carte à 40 tuiles grises

D1 est juste sur le fond (« voilà ce qui reste » inclut les lignes non commencées) mais
l'exécution pose un problème de lisibilité : au premier jour, la carte montre 10 lignes, ~40
postes, dont la grande majorité « non travaillé ». Une carte majoritairement morte se regarde
une fois, puis se ferme.

Trois contre-propositions (au choix de Benjamin) :
- **a) Dense mais honnête** : on dessine tout, et l'« opportunité » se distingue par la
  présence d'une **référence cible non chiffrée** (donnée existante : `cibleCPP`), pas par
  un gris uniforme → la tuile « à chiffrer » devient une invitation, pas un zéro ;
- **b) Le filtre comme porte d'entrée** : la carte s'ouvre sur « mon projet » (la carte utile),
  « toute l'usine » est un clic ;
- **c) Le temps, pas l'espace, pour le « reste »** : la carte atelier montre l'espace
  (machines), et l'axe mission montre le temps (ce qui reste à faire) — cohérent avec D5.

Je n'ai pas de préférence forte ; c'est un choix de Benjamin, pas de modèle.

## 3. Mes ajouts spontanés

**A1 — le retour arrière doit être défini (personne n'en parle).**
L'axe espace n'est pas un arbre, c'est une carte : depuis la couche 2 (scénarios) d'une machine,
le fil d'Ariane expert (« ligne → référence → OP ») et le bouton « retour » ne doivent pas
retomber dans le vide. Le modèle de couches doit dire : depuis n'importe quelle couche,
**comment on revient à la carte et à la lecture par référence**. Sans ça, la navigation
actuelle (fil d'Ariane) et la nouvelle (carte) ne se raccordent pas.

**A2 — le compte de tuiles est un test de la carte, pas une décoration.**
Critère de recette de la couche 0 : à froid (projet « 2026/2027 », 6 références), combien de
tuiles portent une information **actionnable** (gain, cible, essai ouvert) ? Si < 1/3 de la
carte, la carte est trop creuse (→ H1). C'est chiffrable, donc arbitrable.

**A3 — l'A4 Mission et la carte doivent sortir de la même source de vérité (comme D3).**
Si on fait un A4 « Mission », il ne doit pas recalculer ses propres gains : il consomme la
même fonction que la tuile et le bandeau. Sinon on a trois chiffres qui divergent — la
confiance de la hiérarchie meurt au premier contrôle croisé (ce qui est arrivé avec le
trigger `preserve_cibles_cpp` cette semaine).

**A4 — la conformité se joue aussi dans la carte.**
L'objectif « relais hiérarchie » implique que la carte soit présentable telle quelle (photo
d'écran → projection en réunion). Donc : pas de chiffre « en attente » sans étiquette, pas de
gain sans sa source (acté / projeté), et les mêmes règles de confidentialité partout (pas de
K/P, quelle que soit la version affichée).

## 4. Le verdict de cette ronde

Sur les 12 points de Z Code : **9 acceptés, 1 accepté sous condition (D4), 1 accepté sur le
principe mais à trancher (D1/H1)**. La divergence de fond (entité machine propriétaire vs
dérivée) est **résolue** (dérivée + déclaration légère en constante). Le désaccord réel qui
reste est **H1** (densité de la carte à froid) — un point de lecture, pas de modèle.

Prochaine étape proposée à Benjamin : trancher **H1** et **D4** (séquence écran d'abord ou A4
d'abord), puis je rédige la **v2 consolidée** de la spec (modèle de couches + déclaration des
machines + `opCode` corrigé + critères de recette), que Z Code pourra passer en contrat
d'implémentation.

## 5. Questions ouvertes restantes (pour Benjamin)

| # | question | ma réponse provisoire |
|---|---|---|
| H1 | Carte complète à froid (~40 tuiles) vs carte filtrée par projet ? | (b) + (a) : on ouvre sur le projet, l'usine entière est un clic, et « à chiffrer » est un état visible, pas un gris |
| D4 | Écran d'abord ou A4 Mission d'abord ? | maquette écran d'abord (Matis travaille), A4 ensuite avec la même source |
| A2 | Seuil de recette d'une carte utile : ≥ 1/3 de tuiles actionnables ? | oui, à vérifier sur le jeu 2026/2027 |

---

*Hermes, réponse à Z Code v1 — 29/09/2026. Aucun code dans ce round. Audit 4.41 disponible
chez Benjamin (`Desktop\RAPPORT_AUDIT_SUIVI_SPK.md`) ; les constats d'audit restent valides
pour la logique, à re-vérifier ligne à ligne sur 4.49.4 au moment de l'implémentation.*
