# Demande à Z Code — Deux briques : le bandeau « Coût pièce » dit vrai (validé Benjamin) + la fusion des outils en doublon Classeur Matis

**Pour :** Z Code
**De :** Hermes — chantiers validés par Benjamin le 26/10/2026 (soir)
**Base de décision :** `AVIS_HERMES_BANDEAU_CPP_2026-10-26.md` (avis rendu,
points 1 et 2 **validés par Benjamin**) + le problème de doublons remonté par
Benjamin le même soir.
**Versions visées :** brique A → **4.114.0**, brique B → **4.115.0** (une brique
par tour, jamais les deux dans le même déploiement). Prod : **toujours rien**,
elle attend la phrase de Benjamin (Q8-A) — dev seule.

---

# BRIQUE A (4.114.0) — Le bandeau « Coût pièce complet » dit vrai

## A.1 La règle de lecture (décision Benjamin, non négociable)

**Production du jour d'une OP = son scénario `statut === "serie"` s'il existe,
sinon la ★ (repli). L'étoile NE BOUGE JAMAIS toute seule.**

L'étoile reste l'archive de comparaison (base 100 du Plan et des verdicts). Le
bandeau lit la production dérivée. Trois phrases affichées, jamais mêlées :

> **Aujourd'hui : 0,577 €/pièce** · Base 12/10 : 0,712 € · **Réalisé : −0,135 €**
> (LKT640, SL500) · **Reste possible : −0,002 €** · Cible site : 0,575 € —
> 99 % du chemin

- « Réalisé » = base − aujourd'hui, sur les OP dont la série existe (noms des
  scénarios passés entre parenthèses).
- « Reste possible » = aujourd'hui − meilleur scénario **non en série et non
  abandonné** (voir A.4).
- Le % de chemin = réalisé ÷ (réalisé + reste possible) — plus jamais calculé
  sur l'avant seul.
- Garde-fou d'affichage : quand une OP a une série ≠ ★, le bandeau le dit
  (« aujourd'hui : SL500 — base de comparaison : Classeur Matis »). La pilule
  et le chiffre qu'elle accompagne racontent enfin la même temporalité.

## A.2 La ré-base reste un geste manuel lourd

Si un jour Benjamin veut que l'étoile rattrape la production : geste manuel
explicite, confirmation avec avertissement lisible (« le réalisé repart de
zéro — le Plan et les verdicts changent de base »). Jamais automatique, jamais
un effet de bord d'un changement de statut. (Le geste `promouvoirEnProduction`
existe ; ajouter seulement l'avertissement de conséquence avant confirmation.)

## A.3 Le vocabulaire — trois termes tués, cinq états restants

Tuent, partout où ils se rendent (bandeau, fiches, Plan, impression) :
« meilleur en cours » (→ « réalisé » ou « candidat » selon le statut),
« 0,712 € prod » (→ « base »), « passé en série » (→ « en série »).
« base excel » : cantonné à la marque d'import dans l'historique du scénario,
jamais dans le bandeau. Cinq états, cinq pilules : **Base ★ / En série /
Validé 5× / Essai / Abandonné** — une notion = un mot.

## A.4 Le bug latent à corriger dans le même bloc

`pieceCPPComplet` : la boucle `meilleur` itère tous les scénarios non-★
**y compris les abandonnés** — un abandonné peut nourrir « meilleur en cours »
et le % du chemin. Filtrer `statut !== "abandonne"`. Un abandonné reste listé
dans le détail (§3.5, une absence se dit) mais grisé, jamais compté.

## A.5 Le détail scénarios — au clic sur la puce OP du bandeau

Le clic sur une puce OP ouvre un `panel-large` : une ligne par scénario de
cette OP, ~15 lignes maximum, tout visible sans défilement.

Colonnes : `scénario (nom) · coût €/pc · état (UNE pilule : Base ★ / En série /
Validé 5× / Essai / Abandonné) · écart vs base · gain €/an`. Tri par coût
croissant. Abandonné listé, grisé, non compté. Second point d'entrée : la vue
Synthèse, à côté de la feuille de route.

Portes harnais brique A : (1) fixture « série ≠ ★ » → le bandeau affiche le coût
série comme « aujourd'hui » et nomme la base ; (2) la ligne « réalisé » ne change
jamais si `cycleRefSec`/star bougent sans geste (anti-ré-base) ; (3) un abandonné
n'entre jamais dans « reste possible » ; (4) anti-régression vocabulaire (« meilleur
en cours » absent du HTML rendu).

---

# BRIQUE B (4.115.0) — La fusion des outils en doublon Classeur Matis

## B.1 Le problème, tel que Benjamin l'a décrit

Un scénario créé **avant** l'implémentation du Classeur Matis contient des outils
saisis à la main (avec l'histoire : essais, prélèvements, plan PDF, prix, mesures).
L'import du Classeur Matis apporte ses propres outils — la même physique existe
alors **deux fois** : la version manuelle riche, la version Classeur officielle
(mabec, correcteurs, mise en page). Aucune option de fusion n'existe ; la v4.71 ne
regroupe que des clés de porte-outil strictement identiques et ne touche jamais un
outil déjà positionné.

## B.2 Les deux dangers, vérifiés dans les données réelles (rev433)

1. **Les prélèvements d'essai pointent les logements par id** (`prelevements[].logementId`,
   ex. `g1k30etqklds`). Une fusion qui supprime un logement apparié casse
   l'historique de mesure — les Ra disparaissent (l'incident déjà vécu au
   réattribut PCI5, v4.10x).
2. **Les documents sont embarqués sur l'outil** (`plan.dataUrl`, PDF en base64 ;
   `pieces[]`). Une fusion écrasante les détruit en silence — interdit (§3.2).

## B.3 La règle de fusion (décision Benjamin)

**L'identité vient du Classeur Matis, l'histoire vient de l'outil manuel.**

- Vient du Classeur : les **noms de position** (D1, D2…), les **mabec /
  codeArticle**, l'**ordre des outils et logements** (la mise en page), les
  **numéros de correcteur**.
- Vient du manuel : **l'id de l'outil et des logements appariés** (ancre
  d'historique — les prélèvements restent valides), le **plan PDF**, les
  **pièces**, les **mesures** (vc, f, temps), les **essais**.
- **Champ par champ** : si les deux côtés sont renseignés et diffèrent →
  **conflit, demandé** (radio : Classeur / manuel). Si un seul côté est
  renseigné → ce côté gagne, listé dans le bilan sans question.
- Le **prix** est un conflit comme les autres (le Classeur a le prix officiel,
  le manuel a parfois le prix négocié — Benjamin choisit).

## B.4 L'appariement

Clé de rapprochement : **numéro de porte-outil normalisé** (passer par
`matisPorteOutilPosition` — les formats « T546 » et « T2D1 » collés sont déjà
gérés v4.77), puis **position/correcteur** au sein de l'outil. Un numéro ambigu
(doublon des deux côtés) n'est PAS apparié : il remonte dans la liste « à
résoudre à la main », jamais fusionné au hasard.

## B.5 L'UX — prévoir, puis appliquer ; jamais direct

1. **Étape détection** (deux points d'entrée) :
   a. **À l'import** du Classeur Matis dans un scénario existant : si des numéros
   existent déjà, l'outil le dit et propose « fusionner » (le défaut reste
   « ajouter » — comportement actuel inchangé si Benjamin ne choisit pas la
   fusion) ;
   b. **À froid** sur une fiche scénario déjà en doublon : action « fusionner les
   doublons » (réparable, comme la v4.71 l'était).
2. **Étape prévision** : un écran de révision, fonction PURE (rend la structure
   fusionnée, ne mute rien — même pattern que la v4.71) : pour chaque paire, les
   champs pris du Classeur, ceux gardés du manuel, les conflits avec radio, les
   unilateral listés, les logements non appariés proposés en « ajout » ou
   « retrait demandé ». Le bilan est visible AVANT d'appliquer.
3. **Étape application** : sur acceptation seulement. Les valeurs perdues dans un
   conflit (ex. un plan PDF écrasé par l'autre) sont listées dans le bilan final
   avec téléchargement possible avant écrasement — rien ne disparaît sans avoir
   été montré (§3.2, §3.5).
4. **Le plan PDF en double** : le modèle n'a qu'un `plan` par outil — conflit
   demandé ; si « garder les deux » est choisi, le second est proposé en
   téléchargement dans le bilan (pas de changement de modèle de données dans cette
   brique).

## B.6 Portes harnais brique B

1. Fixture manuel (T546 riche : plan PDF, essai avec prélèvements, prix saisi) +
   Classeur (T546 officiel : mabec, correcteur D1/D2) → après fusion : **un seul**
   T546, mabec Classeur présent, plan manuel présent, **tout `logementId` de
   prélèvement résout vers un logement existant** (zéro dangling).
2. Deux outils même numéro des DEUX côtés → non fusionnés, listés « à résoudre à
   la main ».
3. Conflit de prix non tranché → la fusion est refusée (l'écran de révision ne
   peut pas appliquer tant qu'une radio pende).
4. Contre-regard double sur chaque porte, protocole habituel.

## B.7 Hors périmètre (cette brique)

Pas de changement du modèle de données (pas de `plan` en tableau, pas de nouveau
champ persisté). Pas de fusion automatique à l'import (le défaut reste « ajouter »,
la fusion est un choix explicite). Pas de fusion inter-scénarios (uniquement au
sein d'un scénario).

---

# Rappels de protocole

Verrou avant d'écrire, harnais vert + `node --check` avant chaque livraison,
CHANGELOG + NOUVEAUTES + version, déploiement dev seul (prod = phrase de
Benjamin). Capture avant/après du bandeau sur EMAG 1 (le rendu attendu en A.1)
et de l'écran de révision de fusion. Contre-regard Hermes attendu sur chaque
brique avant validation.

— Hermes, 26/10/2026, nuit.
