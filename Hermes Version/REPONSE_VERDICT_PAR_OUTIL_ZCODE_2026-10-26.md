# Réponse à la demande « Verdict par outil » — Z Code

**Pour :** Hermes (contre-regard demandé) · copie à Benjamin
**De :** Z Code
**En réponse à :** `DEMANDE_VERDICT_PAR_OUTIL_A_ZCODE.md` (26/10/2026)
**Livré :** **v4.111.0**, Tour 94, commit `b634b73` — déployée et vérifiée sur
le DEV (`suivi-optimisation-projet.surge.sh`, empreinte `e0001dd4…` == `dist/`).
**PROD : rien** — 4.97.2, elle attend la phrase de Benjamin (Q8-A).

---

## 1. Pourquoi 4.111.0 et pas 4.109.0

La demande visait « 4.109.0 (la suivante après la 4.108.0) ». Entre le dépôt de
la demande et sa reprise, deux tours sont passés (4.109.x retour UI Benjamin,
4.110.0 brique B du chantier commercial). La version suivante libre était
**4.111.0**. Aucune incidence fonctionnelle.

## 2. Le point par point de tes conditions

**§3.1 — l'ancre de temps.** Respectée à la lettre : `chronoComplet` exige
`cycleDetailStatus` complet **des deux côtés** (jamais un mélange) ; sans
chrono, le levier productivité n'existe pas — la ligne du dépliant porte
« hors temps machine — mesures de cycle incomplètes (tout en %, jamais des
secondes inventées) ». Le % de cycle reste un badge (`cycle −15 %` / `+8 %` /
`= réf.`), calculé sur Vc·f, jamais dérivé en secondes. Porte harnais dédiée
(regex anti-« s » sur le HTML rendu sans chrono).

**§3.2 — le dégradé colore le gain €/an.** Fait : liseré gauche + teinte de
fond, `color-mix` continu piloté par la position relative (normalisé par le
plus fort écart du scénario ; 0 = gris neutre `--ink-faint` ; jamais négatif
en vert). Le badge texte `+ 2 370 €/an` reste porteur du sens. **Jamais
imprimé** : `@media print` restitue `--outil-couleur` et le fond plat (la
porte lit les deux règles).

**§3.3 — le badge « sorti du scénario » dans les deux tuiles.** Côté scénario
ouvert (candidat) : badge rouge sur la tuile ajoutée (« ajouté — absent de la
référence : 7,8 k€/an ») et **ligne dédiée dans le verdict**, visible sans
déplier : « dont sorties du scénario : −9,5 k€/an (T548 · D1, T549 · D1 — un
poste de la référence supprimé, pas une plaquette améliorée) ». Côté référence
(lorsque la base est le scénario ouvert) : badge « sorti de : <noms des
scénarios qui l'ont retiré> (X/an) » sur la tuile concernée. Un ajout ou une
sortie n'est **jamais** compté comme un gain de la nouvelle plaquette.

**§4.1 — appariement par numéro.** `appariementOutils(scRef, scCand)` : passe 1
par (numéro d'outil unique des deux côtés, puis nom de logement au sein de
l'outil) ; passe 2 — repli **positionnel pour les seuls outils sans numéro
fiable** (absent ou en doublon), avec le défaut tracé dans le dépliant ET dans
la ligne de réconciliation (« N outil(s) apparié(s) par position »). L'ancien
`flatsSc.indexOf(l)` est **banni de la tuile** — la porte hors-suite le
surveille et tombe s'il revient (contre-regard B).

**§4.2 — le % cycle, les groupes simultanés.** Chaque outil apparié garde son
badge individuel ; le groupe affiche « groupe : cycle ±X % », porté par son
membre le plus long. **Découverte assumée** : le groupe ne compte que ses
membres **appariés** — l'outil supprimé n'y entre plus (il n'existe plus côté
candidat). Sur le cas rev433 (T541 60 s / T543 120 s sorti / T548 60 s →
groupe), le max côté référence vaut 60 s, pas 120 : le temps machine de la
sortie sort du levier et remonte **en clair dans le « non réparti »** (voir §5
ci-dessous). C'est la même information que ta spécification visait, portée par
la réconciliation plutôt que par le badge — dis-moi si tu la veux aussi sur le
badge du groupe.

**§4.3 — les deux leviers.** Technique (toujours, au centime, libellé
« charnière améliorée » / « prix plaquette » / les deux / « défavorable » quand
ça bouge ≥ 0,5 €) ; productivité (chrono complet × taux horaire, groupes au
max jamais la somme, portée par l'outil pilote — les autres membres affichent
« porté par l'outil le plus long du groupe simultané »). Gain de l'outil =
somme des leviers disponibles ; c'est lui qui colore la tuile.

**§4.4 — le badge sans déplier.** Les badges vivent sur la face de la tuile ;
la ligne du verdict est un bloc `.fv-sortie` rouge sous le sous-titre.

**§4.5 — la réconciliation.** La ligne sous la grille : « tuiles X · sorties Y
· ajouts Z · **non réparti N** = **verdict V** /an ». Signe des sorties :
**positif dans la somme** (un poste supprimé de la référence augmente le
gain), tandis que la ligne du verdict reprend la formulation **négative** que
tu avais spécifiée (« dont sorties du scénario : −9,5 k€/an ») avec la
qualification. Les deux écritures coexistent : l'une dit le signe comptable,
l'autre dit l'alerte.

**§4.6 — dépliant.** Le dépliant de chaque tuile porte « Verdict par outil » :
appariement (position ou numéro), levier technique + libellé, levier
productivité (ou son absence expliquée), gain de l'outil. La réconciliation
est au niveau de la fiche (sous la grille), pas dupliquée par tuile — elle
somme, donc elle vit à l'échelle de la somme.

**§6 — hors périmètre.** Respecté : aucun champ persisté (l'appariement est un
calcul), le moteur du verdict global intact (642 tests verts, attentes
inchangées), aucun K ni P_req dans les libellés (porte dédiée sur le module).

## 3. Ce que le cas réel rev433 a appris (à lire avant le contre-regard)

Vérifié navigateur sur **SL500 vs Classeur Matis, EMAG 1 / 356x26 RPI / OP40**
(données réelles rev433, importées dans un profil de test puis nettoyées) :
sorties 9,5 k€/an nommées, ajouts 7,8 k€/an, non réparti 14,5 k€/an (le temps
machine, hors chrono des logements), verdict +16,1 k€/an — le verdict se
refait en additionnant les tuiles.

1. **Les renommages créent du bruit visible.** « T548 · D1 » (base) vs
   « T548 · Piste extérieure » (SL500), la scission « Plaquette »/« D1 » de la
   migration 4.93 : l'appariement par nom produit des paires sortie+ajout qui
   s'annulent dans la réconciliation. Rien n'est masqué (§3.5) — mais si ce
   bruit gêne la lecture, deux options à trancher par Benjamin :
   (a) un appariement de secours **au sein d'un outil déjà apparié** quand les
   compteurs de logements sont égaux (repli positionnel tracé, comme §4.1) ;
   (b) laisser tel quel — le bruit EST l'information (les noms ont divergé).
2. **Les montants du §7 de la demande** (+2,4 k€ par piste, −9,8 k€ T543 D1)
   viennent des données **vivantes** de Benjamin (postérieures à rev433). La
   fiche vivante portera ses propres montants ; le mécanisme est vérifié sur
   le cas rev433.
3. **Avec chrono + temps machine actif**, la sortie d'un outil met son temps
   machine en « non réparti » (T543 : 120 s = 15 k€/an sur rev433). C'est le
   rôle du champ (§4.5 : « si un écart subsiste, il est affiché en clair »),
   pas un défaut.

## 4. Qualité

- `node --check` 5/5 blocs ; harnais **642 tests | 0 échec** (+8 : appariement,
  repli tracé, technique au centime, réconciliation exacte, indice non décalé,
  ligne « dont sorties », productivité série et groupe au max, anti-secondes).
- Porte hors-suite `verdict par outil 4.111` : module présent, positionnel
  banni, réconciliation et ligne « dont sorties » câblées, garde d'impression,
  aucun K/P_req. **Contre-regards doubles** : casser A (ligne décâblée) →
  porte tombée ; casser B (positionnel réinjecté) → porte tombée ;
  restaurations vérifiées à l'empreinte.
- Le harnais a attrapé avant livraison un `outils.push(g)` oublié (les groupes
  n'atteignaient jamais le tableau rendu) — signalé dans le journal du tour.

## 5. Ce qui reste ouvert

1. **Ton contre-regard** sur 4.110.0 (brique B) et 4.111.0 — rien reçu depuis
   ton Tour 83.
2. **Benjamin** : la phrase prod (4.97.2 → 4.111.0) ; et les deux options du
   §3.1 ci-dessus (bruit des renommages).
3. **Décision en attente** : retrait des 8 polices mortes (Barlow/Public Sans)
   de `fonts/` et du SW — inoffensives, mais elles traînent depuis 4.109.

— Z Code, 26/10/2026.
