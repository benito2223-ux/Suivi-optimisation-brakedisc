# Demande à Z Code — Le verdict par outil : gains détaillés outil par outil, cycle estimé par les conditions de coupe

**Pour :** Z Code
**De :** Hermes, chantier validé avec Benjamin le 26/10/2026
**Version visée :** 4.109.0 (la suivante après la 4.108.0)
**Périmètre :** `bilan_economique.html` — écran scénario (tuiles outils `ap-tuile`), dépliant traçabilité, verdict du scénario. Aucun changement de modèle de données (aucune migration JSON).

---

## 1. Le problème, en deux phrases

Aujourd'hui l'outil chiffre le gain d'un scénario **globalement**, et le temps de cycle
n'est fiable que si on chronomètre chaque outil (`tempsCoupe` par logement) — trop
difficile à mettre en œuvre en atelier. Benjamin veut un **verdict par outil** : pour
chaque outil (ou couple d'outils simultanés), l'augmentation ou la diminution **en
pourcentage par rapport au scénario de référence**, calculée uniquement depuis les
conditions de coupe (Vc, f), plus le gain financier détaillé en deux leviers.

**L'événement déclencheur** (vécu le 26/10) : le verdict « +16,8 k€/an » du scénario
SL500 sur EMAG 1 incluait silencieusement la suppression du logement T543 D1
(SL506, 9,8 k€/an à lui seul). Benjamin croyait comparer ses deux postes piste
(7,0 k€/an). L'écart n'a été trouvé qu'à la main. Le chantier doit rendre ce genre
d'écart **impossible à rater**.

## 2. Ce qui existe déjà (réutiliser, ne pas réinventer)

| Brique | Où | État |
|---|---|---|
| Indice conditions vs base `Vc·f` | ~ligne 9821, `indiceCond = vB/vSc*100` dans le dépliant | Déjà calculé par logement, mais **apparié par position** (voir §3.1) et jamais sommé en verdict |
| Groupes d'outils simultanés | `simultaneAvecPrecedent` par outil (v4.41), `cycleDetailStatus` | Le groupe vaut le plus long ; les temps ne s'additionnent pas |
| Ancre chronométrée | `config.cycleRefSec` (temps de cycle du scénario réf, en secondes) | Déjà éditable dans Options ; alimente l'indice base 100 du verdict |
| Coût plaquette/pièce | `prix/(aretes*charniere)` (lignes 6762, 15852) | Le levier « technique » existe déjà par logement |
| Coût machine/pièce | `temps × taux horaire` (0,3468 €/pièce dans le verdict) | Existe au niveau scénario quand le cycle est chiffrable |
| Tuiles `ap-tuile` + dépliant | `apercuScenarioHTML` / dépliant traçabilité | Structure cible pour l'affichage ; `--outil-couleur` existe déjà par tuile |

## 3. Les décisions de Benjamin (validées le 26/10 — ne pas rouvrir)

1. **Ancre de temps : « si un chrono est rentré, sinon tout en % ».**
   - Si les mesures `tempsCoupe` du scénario sont complètes (règle actuelle de
     `cycleDetailStatus` : jamais un mélange) → secondes et € machine affichés.
   - Sinon → **tout en pourcentages et €/an plaquettes**, pas de secondes inventées.
     Le levier productivité reste un % (badge), jamais une estimation de secondes.
2. **Le dégradé rouge→vert des tuiles colore le gain €/an de l'outil** — le verdict
   financier. Le % de cycle reste un badge texte sur la tuile.
3. **Un outil présent d'un côté et absent de l'autre porte un badge explicite**
   « sorti du scénario : ±X €/an » **dans les deux tuiles** (celle du scénario ouvert
   et, dans la mesure où elle est visible, la référence). Jamais compté comme un
   gain silencieux de la nouvelle plaquette.

## 4. Spécification fonctionnelle

### 4.1 Appariement par numéro d'outil — PAS par position (le piège n°1)

Aujourd'hui `flatsSc.indexOf(l)` apparie les logements du scénario et de la référence
par **position dans la liste**. Supprimer un outil en milieu de liste décale toutes les
comparaisons. Le nouveau module apparie par **`numero` d'outil** (T548 ↔ T548), puis
par `nom` de logement au sein de l'outil. Un outil sans numéro ou en doublon de
numéro : comparer par position pour celui-là uniquement, avec un badge « apparié par
position » dans le dépliant (traçabilité du défaut).

### 4.2 Le % cycle par outil — toujours, sans chrono

Pour chaque outil apparié : `indice = (Vc_ref × f_ref) / (Vc_sc × f_sc) × 100`.
100 = identique, > 100 = le scénario va plus vite (temps réduit), < 100 = plus lent.
C'est le ratio des temps dès que la géométrie est la même (même opération, même
disque — le cas de tous nos scénarios). Affiché en badge sur la tuile :
« cycle −15 % » / « cycle +8 % » / « cycle = réf. ». Si Vc ou f manque d'un côté →
badge « — » et rien d'estimé. **Ne jamais dériver un temps en secondes de ce ratio
seul** (décision §3.1).

Outils simultanés : chaque outil garde son badge individuel, mais le **groupe**
affiche son propre ratio, calculé sur le membre le plus long (même règle que le
cycle mesuré) — c'est lui qui pilote le temps machine du groupe.

### 4.3 Le gain €/an par outil — deux leviers détaillés

Dans le dépliant de chaque tuile, deux lignes séparées, jamais fondues :

- **Technique (toujours affiché)** : Δ coût plaquettes =
  `volume × (prix_ref/(arêtes_ref×charnière_ref) − prix_sc/(arêtes_sc×charnière_sc))`.
  Libellé du levier quand il bouge : « charnière améliorée », « prix plaquette »,
  les deux, ou défavorable.
- **Productivité (si chrono complet seulement)** : Δ temps machine =
  `volume × taux horaire × (temps_outil_réf − temps_outil_sc)` en respectant les
  groupes simultanés (max, pas somme). Si pas de chrono : la ligne porte
  « hors temps machine — renseigne le cycle de référence » (reprendre la sémantique
  existante du verdict).

Le **gain total €/an de l'outil** = somme des leviers disponibles. C'est lui qui
colore la tuile.

### 4.4 Les outils « sortis du scénario » — le piège n°2, rendu visible

Outil présent dans la référence mais absent (ou sans prix/charnière chiffrables) dans
le scénario ouvert : badge rouge neutre sur la tuile du scénario qui le contient :
« sorti de l'autre scénario : X €/an ». Et une **ligne dédiée dans le verdict** du
scénario : « dont sorties du scénario : −9,8 k€/an » (exemple T543 D1). Réciproquement
pour un outil ajouté. Le badge doit être visible **sans ouvrir le dépliant**.

### 4.5 La réconciliation — la somme des tuiles = le verdict global

Le total des gains par outil (+ sorties + ajout) **doit tomber sur le verdict global
du scénario** (hors temps machine si la référence n'a pas de cycle chiffrable, comme
aujourd'hui). Si un écart subsiste (outils non appariés, données incomplètes), il est
affiché en clair : « non réparti : X €/an (N outils sans pendant) ». C'est la
contre-mesure structurelle de l'incident du 26/10 : plus jamais un verdict global
qu'on ne peut pas refaire en additionnant les tuiles.

### 4.6 Le dégradé rouge → vert

- Métrique : gain €/an de l'outil (§4.3). Continu, pas des seuils binaires :
  `color-mix(in srgb, var(--red-dark), var(--green) t)` piloté par une position
  relative (ex. gain normalisé par le plus fort écart du scénario, 0 = gris neutre
  `var(--ink-faint)`). Liseré gauche de la tuile + teinte légère du fond, dans les
  deux modes clair/sombre, **jamais imprimé** (même règle que les couleurs de ligne).
- Accessibilité : le badge texte reste porteur du sens (« +2 370 €/an »), la couleur
  ne porte jamais l'information seule.
- Le dépliant traçabilité du scénario ouvert reprend le détail des deux leviers par
  outil + la ligne de réconciliation (§4.5).

## 5. Garde-fous harnais (obligatoires, même protocole que les portes existantes)

1. **Appariement** : scénario de test où un outil du milieu est supprimé → les
   indices des autres outils ne se décalent pas (porte `verdictParOutil`).
2. **Réconciliation** : somme(par outil) + sorties + ajout + non-réparti = verdict
   global (porte dédiée ; contre-exemple T543 D1 en fixture).
3. **Pas de secondes sans chrono** : `cycleRefSec` vide ou mesures incomplètes →
   aucun temps en secondes rendu dans les tuiles (regex anti-« s » sur le HTML rendu).
4. **Badge sorti du scénario** présent dans le HTML rendu quand la fixture contient
   un outil unilatéral.
5. Contre-regard double sur chaque porte (casser A, casser B, restauration
   octet-pour-octet), comme `panneauxSysteme` en 4.96.0.

## 6. Hors périmètre (ne pas faire)

- Ne pas modifier le modèle de données (pas de nouveau champ persisté ; l'appariement
  par numéro est un calcul, pas un stockage).
- Ne pas toucher au moteur économique du verdict global (les 629 tests actuels
  doivent rester verts sans modification de leurs attentes).
- Ne pas afficher d'estimation de secondes dérivée des seuls Vc·f (§3.1).
- Ne pas exposer K ni P_req dans les libellés (Vc et f sont des valeurs visibles
  autorisées ; les libellés parlent « conditions de coupe », jamais de coefficients).

## 7. Protocole

Verrou `VERROU.md` obligatoire avant d'écrire, harnais vert + `node --check` avant
chaque livraison, CHANGELOG + NOUVEAUTES + version, déploiement dev seul (la prod
garde l'accord de Benjamin, Q8-A). Capture avant/après de la fiche SL500 EMAG 1 —
le rendu attendu : 3 tuiles outils, dont 2 vertes (pistes, +2,4 k€/an chacune
environ) et la traçabilité montrant la sortie du T543 D1 (−9,8 k€/an) en rouge.
