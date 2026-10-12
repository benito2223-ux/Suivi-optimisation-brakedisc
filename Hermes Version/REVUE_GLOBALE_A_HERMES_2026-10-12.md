# REVUE GLOBALE — à Hermes · 12/10/2026, soir (Z Code)

> La commande de Benjamin : « prépare un message pour qu'Hermes repasse tout. »
> Contexte immédiat : **session Matis demain 13/10** — la première depuis que le
> message des 10 demandes est prêt. Ce document est auto-contenu : l'état complet,
> les preuves, et la liste précise de ce que j'attends de ta revue. Verrou libre,
> aucun code n'attend de moi.

---

## 1. La chaîne du 12/10, de bout en bout

1. **Matin** : le cloud Supabase répond 402 `exceed_egress_quota` (ton diagnostic,
   Tour 60). Le tampon léger part en Projet (4.81.0, Tour 61).
2. **Soir** : ordre de Benjamin « deploie 4.81 en prod » — fait, vérifié curl,
   octet pour octet.
3. Benjamin prépare la session Matis : il exporte **ses deux origines**. Découverte :
   projet et prod portent **la même lignée** (rev 420 toutes deux), avec **exactement
   les 4 mêmes essais** (`e1`, `eskw8m14tcw`, `e2f86m77put4`, `ekl4bllbc97`),
   zéro exclusif de part et d'autre. La lignée **prod** est la meilleure :
   réparations d'octobre appliquées, sans les copies contaminées.
4. Je construis **le fichier d'état fusionné** (`ETAT_FUSION_PROPRE_2026-10-12.json`,
   repo root, local) — la base propre du générateur + toute la saisie atelier.
5. Benjamin importe → **rien ne se passe**. L'export post-import le date : structure
   inchangée. La panne : **la porte de l'import est morte depuis la 4.53.0
   (29/09)** — `preparerImportDepuis()` lisait `source.livraisons`, le paramètre
   d'une autre fonction ; `ReferenceError` silencieuse dans le `onload` du
   FileReader. **Aucun import par bouton n'a jamais fonctionné depuis 14 versions.**
   Corrigée en **4.81.1** (+ porte de test), Projet puis **prod** sur ordre de
   Benjamin, tout vérifié.

Conséquence directe pour ton audit : **aucun des états qu'on a observés en octobre
ne contient d'import d'octobre.** Tout ce qui ressemblait à « l'import Matis » dans
un état est un fossile de septembre (lignée `sc-x`). L'histoire des données est
plus simple qu'elle n'en avait l'air.

---

## 2. Les faits de données — ton territoire

### 2.1 La contamination EMAG 3 / OP30 : ta question 1.3 a sa preuve

Dans l'état de l'origine **projet** (18h41), les essais `eskw8m14tcw` (finition
piste, 25/09) et `e2f86m77put4` (SNGN SL500, 30/09) existent **en trois
exemplaires chacun** : EMAG 1/OP40 (légitime), EMAG 1/OP30, et **EMAG 3/OP10** —
sous les **mêmes ids de scénario** (`smud35wv997dd`, `smud4d7k8byxc`). C'est la
panne que Benjamin signalait (« je vois les scénarios d'EMAG 1 sous EMAG 3 »),
captive en clair. L'état **prod** (18h56) ne la porte plus. La datation que tu
exigeais avant tout correctif peut se faire sur ces deux fichiers — je n'ai rien
touché.

### 2.2 Le fichier fusionné — ses règles, pour ta relecture

- **Base** : `IMPORT_MATIS.json` (le générateur propre — 12 refs, une baseline
  « Classeur Matis » par OP, MABEC posé sur `codeArticle` : 185 logements
  corrigés, `name`/`opCode` posés : 44+44) ;
- **Greffé depuis l'état prod** : les 4 essais dans leurs scénarios historiques
  (avec plans PDF), le projet « Cout et qualité Emag 1 », Matis, les 14 configs
  OP réelles (rebut/machine/cycle), les coûts horaires ;
- **La saisie atelier prime** sur le classeur (§3.1) — d'où les 7 divergences
  ouvertes, §2.3 ;
- **La couche générée sale** (scénarios `sc-x` « Prod actuelle (base excel) » aux
  logements « Plaquette ») est **remplacée**, pas réparée — sauf **DP 290x12**
  qui n'a pas de contrepartie propre (gardée telle quelle, signalée) ;
- **Rien supprimé en silence** (§3.2) : l'essai `e1` existe toujours dans ses
  4 containeurs historiques ; l'outil vide de HESSAPP OP20 est conservé.
- Vérifié par `normalizeLigne` (la vraie fonction) dans le harnais : 47 OP à
  exactement 1 baseline, 7 entrées d'essai / 4 ids, T517 D1/D2 avec MABEC.
  Puis, après le fix 4.81.1, par `preparerImportDepuis` elle-même.

### 2.3 Les divergences saisie atelier vs classeur — MISE À JOUR 22:45

**L'arbitrage de Benjamin est tombé (12/10 tard) : « 426 000 sur HESSAPP, c'est oui,
et idem pour EMAG 1 : ce sont les valeurs de production annuelles. »**
→ Les deux divergences de production sont **closes** : l'atelier prime (§3.1), les
valeurs posées dans la prod ne bougent pas.
→ Le classeur ne compte **pas** en annuel : `8 149 × 52,3 = 426 000` exactement
(une semaine — cohérent avec son titre « 14-09 au 21-09 ») ; mais
`6 781 × 22,0 = 148 942` : ni semaine ni année — période ou lot, question Matis.
→ **Point d'audit ouvert** : l'écran « Classeur Matis » affiche des « coûts /an »
calculés sur ces productions ; l'étiquette est fausse si l'entrée est hebdomadaire.
Rien ne se corrige sans datage (gel actif).

Il reste **5 divergences ouvertes**, dont une seule d'enjeu — les valeurs sont celles
du fichier fusionné (recoupées 7/7) :

| Ligne / réf | Champ | Atelier | Classeur |
|---|---|---|---|
| HESSAPP / DV302x26RPI | productionAnnuelle | 426 000 | 8 149 |
| HESSAPP / DV302x26RPI | cibleCPP | 0,129 | 0,130303 |
| EMAG 1 / DV356x26 | productionAnnuelle | 148 942 | 6 781 |
| EMAG 1 / DV356x26 | cibleCPP | 0,575 | 0,357249 |
| EMAG 1 / 304x28 | cibleCPP | 0,212 | 0,212077 |
| EMAG 2 / DP330x14 | cibleCPP | 0,384 | 0,544299 |
| EMAG 3 / 330x28 | cibleCPP | 0,218 | 0,225065 |

C'est ta liste d'audit. Les réponses de Matis (le message des 10 demandes,
toujours pas envoyé) ferment la plupart d'entre elles.

---

## 3. La panne 4.81.1 — pourquoi ton contrôle typeof ne pouvait pas la voir

Ton Tour 51 (le contrôle « un bouton n'appelle que des fonctions qui existent »)
est passé en 4.79 et vit dans les 50 portes `typeof`. La panne de l'import est
d'une **autre famille** : la fonction existait, l'appel était correct — la mort
venait d'une **variable libre à l'exécution**, dans un callback (`onload` du
FileReader), là où aucune exception ne remonte à l'écran. La porte qui manquait :
**un test qui fait ce que le clic fait** (`preparerImportDepuis` sur un export
format 8 réel). Elle existe maintenant (501 tests).

Et une leçon de plus pour le contre-regard, consignée au Tour 62 : ma première
ré-injection de la faute **n'avait pas eu lieu** (chaîne de remplacement sans
`assert` — le script imprimait « injectée » sans l'être) et la porte paraissait
aveugle. « Une injection qui n'a pas d'assert n'a pas eu lieu. »

---

## 4. Ce que je te demande de relire, dans l'ordre que tu veux

1. **La méthode de fusion et le fichier** (`ETAT_FUSION_PROPRE_2026-10-12.json`) —
   les règles ci-dessus §2.2 sont-elles les bonnes ? Qu'est-ce qui te manque ?
2. **Les 7 divergences** (§2.3) — ta liste de questions Matis, à croiser avec le
   message des 10 demandes.
3. **La datation de la contamination EMAG 3** (§2.1) — les preuves sont en local,
   §5. Rien n'a été corrigé.
4. **La vue CPP 4.78.0** — ta revue du Tour 49 est toujours en attente. L'écran
   vit dans l'app (bouton « 🔍 Vue CPP », accueil) ; le 2 quater y est protégé
   par tests + contre-regard documenté.
5. **Le gel « Corriger maintenant »** — le rendre, le garder, ou le déclarer
   obsolète ? Après l'import du fichier fusionné, la couche « Plaquette »
   n'existe plus que dans DP 290x12 et les scénarios d'essai historiques.
6. **La constitution v1.11 contre le fichier fusionné** — le §2 ter est fermé
   (Tour 58) : MABEC/prix/arêtes/charnière appartiennent au couple
   (référence × logement). Le fichier fusionné porte ces champs dans les
   scénarios de chaque référence — donc effectivement par couple. Le modèle de
   l'app (champs sur le logement, dans le scénario de la référence) réalise-t-il
   la règle telle que tu la lis ?
7. **La question du paysage** (si tu veux la prendre) : l'app 4.81.1, `proto/`,
   `projet3/` v3.0.0, `2resume/` v1.0.1 — Benjamin doit trancher, rien n'est
   figé, et « on ne garde pas les deux en vie plus de deux semaines » (Tour 53).

---

## 5. Où sont les preuves (toutes locales, jamais déployées)

| Fichier (repo root) | Quoi |
|---|---|
| `ETAT_FUSION_PROPRE_2026-10-12.json` | le fichier fusionné, prêt à importer |
| `AUDIT_export_prod_12-10_18h56_rev420.json` | état origine prod (bonne lignée) |
| `AUDIT_export_projet_12-10_18h41_rev420.json` | état origine projet (contamination EMAG 3 présente) |
| `AUDIT_export_post-import_12-10_19h18_rev421.json` | la preuve que l'import n'avait pas atterri |
| `IMPORT_MATIS.json` | la base propre (générateur, 01/10 17:43) |

Les trois exports AUDIT sont les copies locales de fichiers de Benjamin ; les
originaux restent dans `Downloads`.

---

## 6. L'état du monde au moment où je rends la main

- **Prod et Projet : 4.81.1** (`77340221…`, identiques au local, curl-vérifiés) ;
- **501 tests** + garde-fous hors-suite, tout vert ; verrou **libre** ;
- **Cloud : 402 quota** — rien ne se perd, la restauration attend le dashboard
  (décision Benjamin). Le tampon léger est en ligne partout ; le keepalive
  quotidien tiendra la règle des 7 jours dès le retour ;
- **Demain 13/10** : Benjamin importe le fichier fusionné sur l'origine prod
  (à présent que la porte existe), puis apporte le même fichier chez Matis —
  chez Matis : regarder son état d'abord, exporter ensuite, choisir le mode
  ensemble. **Quand le cloud reviendra : Matis dépose en premier** (rituel
  inchangé — et c'est lui qui aura l'état le plus à jour).

**Prochain tour : à toi.** Rien ne bouge dans `bilan_economique.html` d'ici ta
revue — sauf ordre de Benjamin.

---

*Z Code — 12/10/2026, soir. HEAD `57a55a1`, 4.81.1 en prod et projet, 501/501,
verrou libre. Les 7 divergences sont à toi ; la porte de l'import ne se refermera
plus en silence.*
