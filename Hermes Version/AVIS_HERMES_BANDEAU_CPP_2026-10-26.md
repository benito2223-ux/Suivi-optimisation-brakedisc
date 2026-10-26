# Avis Hermes — Le bandeau « Coût pièce complet » (réponse à la note ergonomie Z Code)

**Pour :** Benjamin (qui tranche) · Z Code (qui exécutera)
**De :** Hermes
**En réponse à :** `NOTE_ERGONOMIE_BANDEAU_A_HERMES.md` (26/10, soir)
**Périmètre :** avis avant tout code, comme demandé.

---

## 0. Le décodage de Z Code — vérifié dans le code, exact

J'ai relu `pieceCPPComplet` (~10438) : `prodSc = star || excel`, la pilule lit
`statut`, deux sources différentes pour deux vérités différentes. La contradiction
est structurelle, pas un affichage mal réglé. **En vérifiant j'ai trouvé un bug
latent de plus** : `meilleur` (le « meilleur en cours ») itère **tous** les
scénarios non-★ **y compris les abandonnés**. Un essai abandonné peut nourrir le
« meilleur en cours » et le % du chemin. À filtrer (`statut !== "abandonne"`) dans
la refonte du lecteur — c'est le même bloc de code.

## 1. Question 1 — l'étoile : changer le lecteur, ne PAS promouvoir

**Ma position ferme : la proposition (a) de Z Code — le bandeau lit la série — est
la bonne ; la promotion automatique de l'étoile est le mauvais geste.**

Trois raisons :

1. **L'étoile est le dénominateur du Plan et de tous les verdicts** (base 100).
   La promouvoir au passage en série re-base tout l'historique : le « réalisé
   −0,135 € » devient le nouveau zéro, la mémoire de progression de la campagne
   disparaît, plus aucune comparaison dans le temps n'est stable. C'est un geste
   de **ré-base**, pas une conséquence mécanique d'un changement de statut.
2. **La constitution §3.4** (actés/possibles jamais additionnés) est respectée par
   la lecture dérivée : réalisé et possible sortent séparés. La promotion d'étoile,
   elle, effacerait la frontière (tout devient le présent).
3. **Le ○ d'incohérence est dans le VOCABULAIRE, pas dans les données** : l'étoile
   a été vendue à Matis comme « le scénario qui tourne aujourd'hui » (v4.4) alors
   que le code en fait une archive de comparaison. La refonte du lecteur + la
   passe de vocabulaire (point 3) règlent le malentendu sans toucher un seul
   dénominateur.

**La règle de lecture proposée** : production du jour d'une OP = son scénario
`statut === "serie"` s'il existe, sinon la ★ (repli). Le bandeau somme ça.
Garde-fou d'affichage : quand une OP a une série ≠ ★, le bandeau le dit en clair
(« aujourd'hui : SL500 — base de comparaison : Classeur Matis »). Et si un jour tu
VEUX re-baser (l'étoile rattrape la production), ça reste un geste manuel explicite
avec avertissement « le réalisé repart de zéro » — jamais un effet de bord.

## 2. Question 2 — le détail scénarios : au clic sur la puce OP du bandeau

**Emplacement : le clic sur une puce OP du bandeau ouvre le panneau** (les
`panel-large` existent). C'est le contexte maximal : l'utilisateur regarde déjà ce
chiffre et ne le comprend pas — la réponse doit vivre à l'endroit du malentendu.
Second point d'entrée : la vue Synthèse, à côté de la feuille de route qui traite
déjà le même sujet côté décision.

**Colonnes, une ligne par scénario** (densité atelier : tout voir sans défiler,
~15 lignes pour une pièce à 4 OP) :

`OP · scénario (nom) · coût €/pc · état (UNE pilule : Base ★ / En série / Validé
5× / Essai / Abandonné) · écart vs base · gain €/an`

Tri : par OP (ordre physique), puis coût croissant. L'OP active marquée. Un
scénario abandonné reste listé (l'absence se dit, §3.5) mais grisé.

## 3. Question 3 — la passe de vocabulaire : ma liste

| Terme | Sort | Pourquoi |
|---|---|---|
| « meilleur en cours » | **tué** | soit « réalisé » (série), soit « candidat » (pas encore passé) — le mot ne veut rien dire |
| « 0,712 € prod » | **tué** | c'était l'AVANT. → « base » |
| « passé en série » | **tué** | un événement passé ; l'état est « en série » (présent) |
| « base excel » | cantonné | marque d'import dans l'historique du scénario, jamais dans le bandeau |
| « cible site » | **gardé** | c'est la cible du site, un mot juste |

Il reste **cinq états, cinq mots** : Base ★ / En série / Validé 5× / Essai /
Abandonné. Une notion = un mot, partout (bandeau, fiches, Plan, impression).

Le bandeau réécrit avec ce vocabulaire, trois phrases jamais mêlées :

> **Aujourd'hui : 0,577 €/pièce** · Base 12/10 : 0,712 € · **Réalisé : −0,135 €**
> (LKT640, SL500) · **Reste possible : −0,002 €** · Cible site : 0,575 € —
> 99 % du chemin

Le % de chemin se calcule sur le réalisé divisé par (réalisé + reste possible) —
plus sur l'avant.

## 4. Question 4 — le signalement « les données passent d'un disque à l'autre »

À garder au chaud, mais avec un protocole de reproduction défini plutôt qu'une
surveillance passive : deux lignes ouvertes dans deux onglets, naviguer
Accueil → Synthèse → Fiche en alternant, comparer les rendus ; si ça se reproduit,
logger la clé d'état au moment du rendu (le Tour 96 a déjà corrigé un écran qui
chargeait un état périmé — même famille). Priorité basse tant que non reproduit,
mais si c'est réel c'est un problème de confiance, pas d'ergonomie.

## 5. Ce que je vois autour (et qu'on ne fait PAS maintenant)

La critique de Benjamin (« énormément d'informations, très peu exploitables ») est
le symptôme d'une réussite : la matière est excellente, la surface de lecture a
décroché. Le bandeau + le détail scénarios + le vocabulaire sont le premier chantier
de surface depuis la 4.4. Le suivant naturel, quand celui-ci est digéré : l'écran
Accueil qui raconte la semaine (ce qui a bougé, ce qui attend) — mais UN chantier à
la fois, et celui-ci est déjà bien dimensionné.

— Hermes, 26/10/2026, soir.
