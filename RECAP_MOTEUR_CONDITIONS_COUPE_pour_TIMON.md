# RÉCAP POUR TIMON — Moteur « Conditions de coupe » (outil de simulation)

> Document interne (pas affiché dans l'outil). Rédigé le 26/11/2026, session cloud Claude Code.
> Statut : **cadrage terminé à ~70 %, AUCUN code écrit, AUCUN commit, rien déployé.**
> Auteur du besoin : Benjamin Rouquette. Langue de l'UI : français.

## 1. Objectif
Un mini-moteur intégré à l'outil « Suivi d'optimisation » (`bilan_economique.html`, v4.146.0),
dans une **section à part « Conditions de coupe »**, pour guider **toute l'équipe technique** :
l'utilisateur saisit ébauche/finition, Vc, f, ap, (rε / κr) ; le moteur calcule l'épaisseur de
copeau réelle Hm et affiche **une couleur de zone** (bleu = conseillé, rose = chaud, gris = froid),
**une flèche texte** et **une phrase d'une ligne**. Calcul local, consultatif, pas de cloud en v1.

Règle absolue (CONSTITUTION / brief §1) : l'écran n'affiche JAMAIS K, formule, seuils, ni mention
SPK/CeramTec. Closing systématique : « pour la préconisation chiffrée, contacter Benjamin Rouquette ».

## 2. Source du brief
`DRAFT_CLAUDE_MOTEUR_CONDITIONS_SEPTFONS.md` (fourni par Benjamin, non versionné dans le dépôt).
Contenu clé : Hm = f·sin(κr_eff) ; κr_eff = acos(1 − ap/rε) si ap < rε, sinon κr nominal ;
K = Vc·Hm (interne). Zones dans un bloc CONFIG unique :
- ébauche : froid si K<150 ou Vc<315 ; chaud si K>450
- finition : froid si K<150 ; chaud si K>200
Pins de test du brief §6 : ébauche 850/0,50 (ap 4, κ 90) → conseillé bord chaud (K=425) ;
ébauche 900/0,60 → chaud (540) ; finition 700/0,25 (ap 1, rε 1,6) → conseillé (K≈162) ;
finition 400/0,15 (ap 1, rε 1,2) → froid (K≈59).

## 3. Constats sur le dépôt (vérifiés)
- Branche de travail cloud : `claude/wonderful-carson-zzp16u` ; le brief parle de `ux-rail` (absente ici, seulement `main`).
- `VERROU.md` : verrou **libre** à la dernière lecture. Protocole à respecter (verrou, version, CHANGELOG, tests, pas de déploiement sans feu vert de Benjamin).
- `AGENTS.md` (cité §2.6 du brief) **n'existe pas** dans le dépôt ; règle « K caché » à retrouver dans `CONSTITUTION_SUIVI_v1.md`.
- Existant à NE PAS dupliquer sans réfléchir : `kappaEffectif(logement)` (ligne ~6094), `forceRatioDe`, `dansEncadrement`. Il borne l'arc à `rε·(1−cos κr)` (≠ brief qui utilise `ap < rε`). Identique à 90°, différent à 85°.
- Le K existe déjà dans l'outil (« botte secrète » v4.42 : visible seulement pour l'auteur du projet).
- Tests : harness `build_harness.py` (non encore ouvert/analysé). Chaque bloc script : `node --check`.

## 4. Anomalies / points à trancher
1. **Erreur numérique du brief §2** : pour ap 0,34 / rε 1,2, `acos(1−0,34/1,2)` = **44,2°** (pas 44,8°) → Hm ≈ **0,279**, K(400) ≈ **112** (pas 0,282 / 113). Test à corriger après confirmation que ap = 0,34.
2. **Conflit chaud/froid en ébauche** (ex. Vc 300, f 1,6 : K=480 chaud ET Vc<315 froid) → proposition : **chaud l'emporte**.
3. **Finition & correction d'arc** : les points validés (700×0,25 ; 600×0,30 ; 500×0,35) donnent K≈174 avec sin(85°) **sans** arc. Avec arc (rε 0,8, ap 0,3 → κ_eff ≈ 51°) K tombe ≈ 135 → « froid », ce qui contredit les points validés. Proposition : **pas de correction d'arc en finition** (Hm = f·sin κr nominal), arc seulement en ébauche. **À confirmer avec l'ap réel de finition.**
4. Bornes exactes (150, 200, 450) : proposition = incluses dans « conseillé ».
5. Saisies vides/aberrantes : pas de lampe + message « complète les champs » (sans révéler de seuil).
6. Visibilité du menu (équipe entière vs mécanisme K caché) : à décider.
7. Maturité du brut : **hors v1**, juste un point d'extension dans le CONFIG.

## 5. Matière nouvelle apportée par Benjamin (cette session)
- **Finition, toutes plaquettes κr = 85°** : disques pleins (DP) → SCGN 0904 positives ; disques ventilés → SNGN 0904 négatives ; actuellement KY3500 (rε 0,8, wiper 0,5). **Essai en cours : plaquette arête vive (-F) en SL500, rε 1,6.** À considérer pour l'instant dans l'outil : KY3500 / SL500 (même famille Si3N4).
- Layouts sur le Drive de Benjamin (dossier « Layout », réf. 3027-08, machine Tong Tai, matière GG-25).
- Règle de lecture donnée par Benjamin : **un angle de 95° = travail en Z** (à confirmer pour tous les plans).

## 6. Décodage layout 3027-08 — OP10 ventilé 302x26 (seul plan décodé en détail)
Tous rε 1,6, nuance SL506. Numéro de position = numéro de chemin (N.x) sur la coupe du disque.

| Pos | Porte-outil | Plaquette | κr lu | Chemin(s) |
|---|---|---|---|---|
| 1 | T511 | SNMX 120716 | 45° (chanfrein) | 1.1, 1.2 (alésage Ø66) |
| 2 | T511 | SNMX 120716 | 85° | 2.1, 2.2 |
| 3 | T412 | CNMX 120716 | 95° | 3.1, 3.2 |
| 4 | T412 | SNMX 120716 | 85° | 4.1 |
| 5 | T413 | CNMX 120716 | 75° | 5.1 (grande face de friction) |
| 6 | T413 | CNMX 120716 | 95° | 6.1, 6.2 |

Autres plans vus, pas encore décodés position par position : OP20 (CNMX/SNMX « REST CORNER », RCGX/RBGN rondes T424/T525),
OP40 ventilé (SNGN 090408 S-85Z050 SL506 ; SNGN 090416 T00520 SN60 ; TNGN 160416),
OP40 plein (SCGN 090408 F 85Z025 SL500 en T5xx). Les recadrages de tableaux OP20/OP40 ont coupé les premières lignes.
Impact κr : sin 95° = sin 85° ≈ 0,996 ; sin 75° ≈ 0,966 ; sin 45° ≈ 0,707 (chanfrein : message à part).

## 7. Idée de design proposée (non validée)
Un **catalogue de plaquettes dans le CONFIG** (réf, rε, κr nominal, nuance) et un sélecteur par **chemin**
(« OP10, ventilé, 5.1 ») qui déduit plaquette, κr, rε. Les ronds (RCGX/RBGN) viendront plus tard.
Une seule fenêtre de zones pour KY3500 / SL500 / SL506 (hypothèse à confirmer).

## 8. Programme PCI « décodé récemment » — NON RETROUVÉ
Benjamin parle d'un programme décodé avec Claude précédemment : `Programmes\RECAP_TEMPS_COUPE_DP268_PCI4.xlsx`
(PC de Benjamin : `C:\Users\Admin\Desktop\Stellantis_SeptFons\Programmes\`).
Introuvable : ni dans le dépôt, ni sur le Drive (seulement le « Time Study … DP268x12.xlsx » et les plans DP Ø268x12 OP10/20/30),
ni en mémoire. Aucun dossier PC n'est partagé avec la session cloud.
**Action pour TIMON / Benjamin : fournir ce fichier (Drive, collé dans le chat, ou dossier partagé via Remote Control) pour
caler le moteur sur les vraies conditions DP268 PCI4 (Vc, f, ap, plaquette par opération).**

## 9. Limites de l'environnement cloud (cette session)
- Pas d'accès au PC de Benjamin ; pas d'`AGENTS.md` ; harness de tests non encore lu.
- Lecture des PDF layouts : texte non extractible, lecture par rendu image (OK à 300 dpi sur zoom, trop petit à 110 dpi).
- Mémoire Claude Code vide pour ce dépôt.

## 10. Prochaines étapes (ordre proposé)
1. Récupérer `RECAP_TEMPS_COUPE_DP268_PCI4.xlsx` (ou l'équivalent) et caler le périmètre v1 dessus.
2. Benjamin tranche §4 (surtout points 1, 3, 6) et confirme « 95° = Z » partout, la plaquette -F rε 1,6 exacte, et la fenêtre unique de nuances.
3. Décoder OP20/OP40 + disque plein (268x12) → tableau OP / disque / chemin / plaquette / κr / rε.
4. Lire `build_harness.py`, `VERROU.md` (protocole), puis prendre le verrou.
5. Coder : bloc `MOTEUR CONDITIONS DE COUPE` (CONFIG + fonctions pures + une fonction exportée), section UI (champs ≥ 16 px, lampe, flèche, phrase, pré-remplissage logement `vc`/`f` en texte, virgule FR tolérée), tests (§2 corrigé + 4 pins §6), version + CHANGELOG.
6. Commit local seulement ; **aucun déploiement ni service-worker** sans feu vert explicite de Benjamin.
