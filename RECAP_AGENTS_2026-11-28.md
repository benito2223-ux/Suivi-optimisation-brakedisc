# RECAP POUR TOUS LES AGENTS — état réel au 28/11/2026 (audit Claude Code, demande Benjamin)

**À lire avant toute écriture / tout déploiement. En cas de doute entre ce fichier et un VERROU/ECHANGES plus ancien : ce fichier prévaut (il est vérifié par curl + git).**

## 1. Une seule base de code, pas de « vieille version »
- Le dépôt de référence est `C:\Users\Admin\Desktop\Stellantis_SeptFons`, **branche `ux-rail`**, HEAD = `0ace22c` (4.165.0), identique à `origin/ux-rail` sur GitHub.
- La 165 est **linéaire** sur la 163 : `844a492` (4.163.0) → `e5ccb92` (4.164.0) → `4022c01` (4.164.1) → `0ace22c` (4.165.0). Aucune branche parallèle, aucun retour en arrière.
- `C:\Users\Admin\Documents\CeramTec\Suivi-optimisation-brakedisc` = **ancien clone figé en 4.28.0 (septembre)**. Il n'a rien reçu depuis le 24/09 (reflog vérifié). **Ne jamais y écrire ni en déployer.** Idem `.worktrees/v2` (4.160.3, prototype abandonné) et `_prod_ref` (4.129.1).
- `main` et `dev` sur GitHub sont **périmés (4.146.0)** : tout le travail récent n'existe que sur `ux-rail`.

## 2. Ce que contient la 165 par rapport à la 163 (tout est additif)
- **4.164.0** : nouvelle section *Outils › Conditions de coupe* (moteur κr 45°–95° + plaquettes rondes, 4 couleurs de zone, épaisseur de copeau, sélecteur Ligne › Disque › OP › Logement). Une ligne ajoutée dans `spk-shell.js` (entrée de menu).
- **4.164.1** : correctif bloquant du lien Conditions de coupe (globale `allData` inexistante, helper `escapeHTML` inexistant).
- **4.165.0** : postes mixtes ébauche + chanfreins (T521, κr ≤ 50°) = vrai verdict de zone ; finition ≤ 50° garde le badge neutre.
- Seul code existant touché : `kappaEffectif` et le `max` du champ κr (90 → 100). **Comportement identique pour 0 < κr ≤ 90°** ; la section Checkup 4.163 est intacte. +623 / −5 lignes dans `bilan_economique.html`.
- **Verdict : la 165 est une 163 + Conditions de coupe, pas une régression.** Harnais annoncé 1037 | 0 échec (non rejoué par moi).

## 3. ✅ RÉSOLU le 28/11 (rollback 163 ordonné par Benjamin) — PROBLÈME constaté en ligne (curl, 28/11)
**État actuel PROD : 4.163.0 + checkup 2026-11-25.3, 16/16 fichiers vérifiés. La 165 n'est que sur DEV.** Ce qui suit décrit l'incident, pour mémoire :
`https://suivi-optimisation-septfons.surge.sh` (PROD) :
- `bilan_economique.html` = **4.165.0** (md5 `ea0c674f…`, identique à `dist/` et au DEV) — alors que VERROU/ECHANGES disent « PROD : rien (4.163.0) ». **Quelqu'un a publié la 165 sur la PROD** (non tracé dans ECHANGES).
- **404** sur `spk-shell.js`, `spk-app.css`, `checkup.html`, `checkup.webmanifest`, `checkup-version.json`, `icons/checkup-*`, `fonts/`. La procédure documentée (10 fichiers de `dist/` + 6 fichiers du checkup) n'a pas été respectée : un déploiement partiel a écrasé la PROD.
- Conséquences : **les QR codes des 10 lignes (`checkup.html?ligne=`) mènent à une 404** ; un nouvel utilisateur / une nouvelle installation PWA charge l'outil sans coque ni CSS. La PWA de Benjamin affiche encore la 163 grâce au cache du service worker — elle basculera sur le site cassé à la prochaine mise à jour.
- DEV (`suivi-optimisation-projet.surge.sh`) : 4.165.0, complet, rien à faire.

## 4. Règles jusqu'à nouvel ordre
1. **Aucun déploiement Surge sans « oui » explicite de Benjamin, à chaque fois.** Pas de déploiement sur `-septfons` sans lui.
2. Réparation PROD (à faire sur accord de Benjamin, par UN seul agent) : choisir 163 (rollback) **ou** 165, puis publier le **jeu complet** : 10 fichiers de `dist/` (`node outils/build-coque.mjs`) + 6 fichiers checkup tels qu'en ligne/commités (`checkup.html`, `checkup.webmanifest`, `checkup-version.json`, `icons/checkup-*`). Vérifier ensuite par curl chaque fichier (200 + md5).
3. Ne jamais déployer depuis la racine du dépôt (cf. VERROU). Ne jamais importer `IMPORT_EMAG1_304.json` en PROD.
4. Outil toujours **gelé** (`bilan_economique.html`) sauf demande explicite de Benjamin.
5. Toute publication doit être **écrite dans ECHANGES « Faits extérieurs » AVANT l'acte** (et corrige l'erreur du 26/11 : la PROD y est annoncée à 4.163.0).

## 5. Non sauvegardé sur GitHub (au 28/11)
Modifs non commitées : `ECHANGES.md`, `RESULTATS_ESSAIS.md`, `conditions_coupe_standalone.html`, `scripts/recap_emag1_304.py`. Fichiers non suivis : programmes CN (`Programmes/…`), recaps xlsx, emails Matis, briefing temps de coupe 304, `RECAP_ESSAIS_DISQUES_POUR_TIMON.md`, xlsm/xlsx de suivi. Les backups Supabase (`archives/`, 127 Mo) sont volontairement hors git (`.gitignore`).
