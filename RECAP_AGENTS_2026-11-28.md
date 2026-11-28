# RECAP POUR TOUS LES AGENTS — état réel au 28/11/2026 (soir)

**À lire AVANT toute écriture et tout déploiement. Ce fichier prévaut sur tout VERROU / ECHANGES / briefing antérieur en cas de contradiction (il est vérifié par curl + git). Rédigé par Claude Code sur demande de Benjamin.**

## 0. En une phrase
La **PROD et le DEV servent la même version : 4.163.1** (= la 4.163.0 que Benjamin avait validée + 3 évolutions + 6 finitions sur les tuiles logement). **La 165 est abandonnée** (Benjamin développe en parallèle un moteur dédié « Conditions de coupe » ; on verra plus tard s'il s'intègre).

## 1. Ce qui s'est passé (chronologie)
1. 26/11 : des agents ont construit 4.164.0 → 4.164.1 → 4.165.0 (module *Outils › Conditions de coupe*) **sur la 163**, sans l'annoncer comme un déploiement PROD (VERROU/ECHANGES disaient « PROD : rien (4.163.0) »).
2. 28/11 (audit) : en réalité la **PROD servait `bilan_economique.html` 4.165.0 SEUL** — `spk-shell.js`, `spk-app.css`, `checkup.html`, `checkup.webmanifest`, `checkup-version.json`, icônes checkup = **404**. Un déploiement partiel avait écrasé la PROD (les QR codes des 10 lignes menaient à une 404 ; la PWA de Benjamin affichait encore la 163 grâce au cache du service worker).
3. 28/11 : **rollback 163 ordonné par Benjamin** → jeu complet de 16 fichiers publié, vérifié 16/16 par curl.
4. 28/11 : Benjamin demande 3 évolutions + finitions **sur la 163** → 4.163.1, déployée DEV puis PROD (16/16 vérifiés, voir §3).
5. La 165 (et son correctif de mise en page 4.165.1) reste dans l'historique de `ux-rail` mais **n'est PAS la ligne de production**.

## 2. OÙ SONT LES VERSIONS (important)
| Quoi | Où | État |
|---|---|---|
| **Ligne de PRODUCTION (4.163.1)** | branche **`prod-163-hotfix`** (GitHub), commit `0bc8bbd` ; **dossier principal `C:\Users\Admin\Desktop\Stellantis_SeptFons` (branche courante)** | = ce qui est en ligne sur PROD et DEV |
| 4.163.0 d'origine (ancienne PROD) | commit `844a492` (branche `ux-rail`) | base de `prod-163-hotfix` |
| Moteur Conditions de coupe 4.164.0 → 4.165.1 | branche **`ux-rail`** (`961cbf1` sur GitHub) | **MIS DE CÔTÉ, ne pas déployer, ne pas fusionner dans la prod** |
| Données atelier non versionnées avant (programmes CN, xlsm, xlsx, planche QR, tolérances…) | branche **`sauvegarde-donnees-atelier`** (`798ced0`) | sauvegarde, **GitHub public** (voir §5) |
| `main` / `dev` sur GitHub | `42f903c` (4.146.0) | **périmés**, ne pas s'y fier |
| Anciens clones | `Documents\CeramTec\Suivi-optimisation-brakedisc` (4.28.0, figé 24/09), `.worktrees\v2` (4.160.3, abandonné), `_prod_ref` (4.129.1) | **ne jamais écrire ni déployer depuis ces dossiers** |
| Backups Supabase + archives (195 Mo) | `archives/` (hors git) **et copie Google Drive** : `Mon Drive/CERAMTEC/Suivi optimisation Sept Fons - Sauvegardes/archives_2026-11-28` (33 fichiers, tailles et md5 vérifiés) | à recopier à chaque nouveau backup |
| Sites | **PROD** `https://suivi-optimisation-septfons.surge.sh` · **DEV** `https://suivi-optimisation-projet.surge.sh` | 4.163.1 partout, checkup `2026-11-25.3` en PROD |

**Pour travailler sur la production : la branche `prod-163-hotfix` est désormais la branche COURANTE du dossier principal `C:\Users\Admin\Desktop\Stellantis_SeptFons` (plus de worktree à part). Elle contient le code 4.163.1, le checkup `2026-11-25.3` réellement en ligne, et TOUS les documents (ECHANGES, VERROU, briefings, scripts, données versionnées) repris de `ux-rail`. Ne PAS repartir de `ux-rail`** (elle contient la 165). `main`/`dev` GitHub restent périmés ; le réglage « branche par défaut » du dépôt sur GitHub est à changer par Benjamin (Settings › Branches).

## 3. Contenu de la 4.163.1 (par rapport à la 163 validée)
- Tuile logement : chiffre **« Cycle » (temps de coupe, s)** visible sans déplier, étiqueté « mesuré » / « calculé » (même règle que le calcul du cycle ; fonction `tempsCoupeEffectifLogement`, lecture seule).
- Dépliant de la tuile : rubrique **« Plaquette »** (code MABEC, « provisoire » si PLA…, désignation catalogue, ISO).
- Survol « Apple » (soulèvement, ombre, enfoncement au clic, fondu du détail) — CSS dans `spk-app.css`, pointeurs fins uniquement, coupé sous `prefers-reduced-motion`.
- 6 finitions : coins/filets, hiérarchie (coût mis en avant), chevron qui pivote + rubriques nettes, focus clavier (Entrée/Espace), fondus courts panneaux/onglets, chiffres tabulaires.
- Tests : **1015 | 0 échec (×2)**. Détail : `CHANGELOG.md` de la branche, entrée 4.163.1.

## 4. PRÉCAUTIONS (règles ferme)
1. **Aucun déploiement Surge sans « oui » explicite de Benjamin, à chaque fois.** Il garde le rythme des mises à jour vues par Matis et Arthur.
2. **Un seul agent à la fois** écrit dans `bilan_economique.html` / déploie. Prendre le verrou (`VERROU.md`) et le libérer. L'outil est **gelé** sauf demande explicite.
3. **`surge` REMPLACE TOUT le site.** Toujours publier le **jeu complet de 16 fichiers** : 10 de la coque (`bilan_economique.html`, `index.html`, `version.json`, `spk-app.css`, `spk-shell.js`, `manifest.webmanifest`, `service-worker.js`, `icons/icon-192.png`, `icon-512.png`, `icon-512-maskable.png`) + **6 du checkup** (`checkup.html`, `checkup.webmanifest`, `checkup-version.json`, `icons/checkup-192.png`, `checkup-512.png`, `checkup-512-maskable.png`, build `2026-11-25.3`, blobs du commit `0ab66a5`). Un déploiement partiel = site cassé (c'est l'incident du 26-28/11).
4. **Procédure** : build `node outils/build-coque.mjs` dans le worktree (créer un dossier `fonts/` vide avant) → dossier de préparation avec les 10 + 6 fichiers → `surge <dossier> <domaine>` → **vérifier par curl les 16 fichiers (200 + md5 identiques)**. « Success! » ne prouve rien. Vérifier aussi que `ECHANGES.md`, `VERROU.md`, `.git/config`, `IMPORT_*.json` restent en 404.
5. **Ne jamais déployer depuis la racine du dépôt**, ni depuis un ancien clone. Ne jamais importer `IMPORT_EMAG1_304.json` en PROD.
6. **Tests = barrière avant tout déploiement** : `python build_harness.py <sortie.js>` puis `node <sortie.js>` **depuis la racine du worktree** ; le VERDICT doit être « tout est vert », deux fois. **Ne jamais enchaîner build + déploiement sans condition sur le résultat des tests** (un déploiement DEV est parti à tort le 28/11 pour cette raison). Le harnais lit les fichiers frères dans le dépôt courant.
7. **Tracer la publication dans ECHANGES « Faits extérieurs » AVANT l'acte**, et dire la vérité sur la PROD (la note du 26/11 était fausse).
8. **K, P_req** : jamais en sortie visible (règle SPK). Nuances = noms SPK. Voir AGENTS.md §2.

## 5. Sécurité des données — le dépôt GitHub est PUBLIC
`benito2223-ux/Suivi-optimisation-brakedisc` est **lisible sans authentification**. Il contient déjà des xlsm/xlsx de consommation réelle (EMAG, PCI, Pareto) ; Benjamin a **choisi de pousser aussi** la branche `sauvegarde-donnees-atelier` (programmes CN, WEISSER xlsm, tolérances disques…). **Ne rien pousser de plus de sensible sans lui demander** ; envisager de passer le dépôt en privé (réglage GitHub, par Benjamin).

## 6. Comportement à connaître (pas un bug) — temps de cycle
- Un **temps de coupe saisi** sur un logement **prime toujours** : changer Vc/f ne change pas le cycle.
- **Référence** = ancre mesurée (comme le classeur de Matis) : son temps ne se recalcule jamais. **Scénario d'essai** : temps absent ou copié de la référence → recalculé depuis la référence (G96 : t×(f0·Vc0)/(f1·Vc1) ; G97 : avec les tr/min).
- Depuis le 26/11 des temps issus des programmes CN sont saisis en cloud (EMAG 1 304x28 OP10–40, etc.) : ces logements restent figés sur la mesure. Évolution possible (non faite) : mémoriser les Vc/f/tr/min au moment de la mesure et recalculer si ils changent.

## 7. État du travail en cours / ouvert
- Moteur « Conditions de coupe » : **développé en parallèle par Benjamin**, intégration éventuelle plus tard ; la 165 n'est qu'une base de réflexion (`ux-rail`).
- Notes de Gemini/Brad/SeptFons-Dev du 26/11 (CN, ordres OP30/OP40 corrigés en prod cloud, `bilan_economique.html` non touché) : toujours valables, sauf toute phrase qui suppose la 164/165 en ligne.
- Backups avant écriture cloud : `archives/backup_supabase_2026-11-26_1541.json` et `backup_tree_prod_*` (copiés sur le Drive).
