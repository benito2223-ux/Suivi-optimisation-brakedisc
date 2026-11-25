# BRIEFING — « Contrôle de prise de poste » (checkup) — passation à TIMON AI / Hermes

> Auto-contenu : ce fichier suffit pour reprendre le travail. Écrit le 24/11/2026 par Claude, **mis à jour le 25/11/2026 (§0)**, sur demande de Benjamin
> (« confier la suite à TIMON AI et à Hermes »). Ordre de lecture : `VERROU.md` → ce briefing → dernier tour de `ECHANGES.md`.
> Langue de travail avec Benjamin : français. Il écrit en dictée vocale. Il attend une direction assumée, pas un catalogue d'options.

## 0. OÙ ON EN EST — 25/11/2026 (à lire d'abord : prime sur les §3 à §5, écrits avant)

**Utilisateurs.** Aujourd'hui **Matis seul** (son téléphone). **Demain peut-être d'autres** (moniteurs d'atelier, autres
téléphones) : tout ce qui suit doit rester vrai le jour où l'app sort du téléphone de Matis.

**En ligne (PROD, `suivi-optimisation-septfons.surge.sh`)**
- Outil principal **4.163.0** (DEV identique) : nouvelle entrée **Outils › Checkup** = lecture de `checkup_journal`, 3 cartes
  (écarts actifs, contrôles, récidives), filtres, vue classée / plate, **export .xlsx**. Outil principal **de nouveau gelé**.
- `checkup.html` **build `2026-11-24.5`** (TIMON : motifs rapides en 1 tap + `?ligne=` pour QR codes ; planche
  `checkup_qrcodes_lignes.html`).
- **Build `2026-11-25.1` DÉPLOYÉ en PROD le 25/11** (remplace le `.5`) (correctifs de robustesse, voir ci-dessous). Déployer seulement sur
  feu vert explicite de Benjamin, avec la procédure du §6 (dossier de préparation = fichiers en ligne + fichiers du checkup ;
  pour l'outil principal, `dist/` **sans** son `.surgeignore` ni son `CNAME`).

**Supabase (`cxjfyaorkkxemjnollnj`) — FAIT le 24/11** (le §5 décrit le schéma, il est appliqué)
- `checkup_journal` : append-only ; anon/authenticated = INSERT seulement ; lecture = membres (`suivi_est_membre()`) ;
  trigger `checkup_journal_doublon` (un `id_local` déjà reçu est ignoré). Migrations : `supabase_migrations/`.
- `checkup_reference` : créée, lisible par anon, **VIDE** (aucune publication encore) → le checkup lit donc l'outil principal
  via `sync_pull`, **ce qui exige une connexion avec un compte membre**.
- Le journal contient de vrais relevés (premiers tests de Matis, 24/11).

**Build 2026-11-25.1 (Claude) — ce qui a changé**
1. **Session** : le checkup ne renouvelle **plus jamais** la session de l'outil principal (même téléphone, clé partagée) —
   Supabase change le jeton de renouvellement à chaque usage et l'outil principal aurait été déconnecté. Session partagée
   expirée → demande d'une connexion propre au checkup (`cu_cloud_session`).
2. **✓ sur une rangée en écart = « remis conforme »** (statut `ok`, commentaire « Remis conforme (écart corrigé) ») ; avant,
   c'était une annulation et la section Checkup gardait l'écart actif. ✓ sur un ✓ = annulation (inchangé).
3. **Rangée sans charnière de référence** (HESSAPP ×40, EMAG 2 DP 290 ×15…) : plus de ✓ / ≠, cadre « Référence à
   renseigner », et elle ne compte plus dans l'avancement de l'OP.
4. **✓ et ≠ écartés** (gants) : ≠ plus étroit à gauche, 28 px d'écart, ✓ large à droite ; sur écran ≤ 420 px, tailles
   réduites — avant, le titre « Potentiomètre » passait sous le bouton ≠ sur un téléphone de 375 px.
5. **Purge** des ✓ locaux de plus de 3 jours d'équipe.

**Build 2026-11-25.2 (Nova / TIMON, 25/11) — lots 2 et 3, COMMITÉ, NON DÉPLOYÉ** (feu vert de Benjamin requis)
Décision de Benjamin le 25/11 : **Matis est le seul utilisateur** → lots 2 (fiabiliser) et 3 (confort) seulement ; pas de
« Publier pour l'atelier » ; horaires d'équipe **confirmés** (5 h / 13 h / 21 h). `bilan_economique.html` non touché.
- **Envoi du journal** : un relevé refusé par le serveur (400) ne bloque plus les autres — le lot est coupé en deux jusqu'à
  l'isoler ; il est marqué « refusé », sorti de la file, conservé sur l'appareil, et l'écran le dit. Réseau, 5xx, 429 : tout
  reste en file (temporisation 15 s). 404 et 403 : tout reste, message affiché, nouvel essai à 5 min. Bouton retour du réseau : renvoi immédiat.
- **Bouton retour d'Android** : chaque écran est une entrée d'historique (`pile`, `popstate`) ; une feuille ouverte se ferme
  par le retour sans quitter l'OP.
- **Glisser-déposer** : un glisser interrompu (`pointercancel`, `lostpointercapture`) est rattrapé.
- **Mode nuit** : ✓ / ≠ à l'encre `--on-accent` (contraste 9:1 au lieu de 2,1:1).
- **Premier plan** : l'app relit les références au retour au premier plan (au plus toutes les 30 s).
- **Valeur d'écart** : comparée comme un nombre (« 2400.0 » pour une référence à 2400 n'est plus un écart), refusée si négative.
- **Écran de fin d'OP** (✓ « OP10 contrôlée à 06:12, équipe Matin, 0 écart ») + « OP suivante » / « Revoir l'OP ».
- **Retour automatique** à l'écran de la ligne après 3 min sans toucher l'écran ; **ligne figée** quand l'app s'ouvre par un QR
  code (`?ligne=`), avec « Choisir une autre ligne » en pied. Vibration à chaque ✓ (Android ; iOS l'ignore).
- **Place à l'écran** (mesuré à 390 px) : les 10 lignes tiennent sans défiler (grille 2 colonnes, 6 avant) ; « Organiser » (↕)
  passe dans l'en-tête, plus de pied fixe : 5 rangées visibles sur l'écran de contrôle au lieu de 3 ; boutons d'en-tête et
  motifs rapides à 72 px de haut ; le titre de l'écran racine devient « Prise de poste » (il était coupé).
- **Tests** : `scripts/test_checkup.js` (23 vérifications : équipes, envoi du journal dans 5 scénarios, contrôles du fichier),
  branché dans `build_harness.py` → le verdict global les compte. Vérifié qu'ils échouent sur une copie volontairement cassée.
- **Hors lot, volontairement** : le service worker (double chargement) n'est PAS touché — gel de l'outil principal.
- **Pour tester en local sans toucher la production** : copier `checkup.html` en remplaçant `CLOUD_URL` / `CLOUD_KEY` par une
  adresse morte, le servir sur 127.0.0.1 (le navigateur intégré de Timon refuse le domaine Surge, pas localhost).

**Prochaines étapes (ordre recommandé par Claude, validé dans l'esprit par Benjamin)**
1. ~~Déployer 2026-11-25.1~~ — fait le 25/11. **2026-11-25.2 : prêt, à déployer sur « Déploie ».**
2. **« Publier pour l'atelier »** dans l'outil principal (nécessite de lever le gel) : écrit `checkup_reference` (une ligne par
   ligne/référence/OP, version incrémentée, `publie_par`) ; le checkup la lit déjà en priorité. **Obligatoire avant tout
   utilisateur autre que Matis** : sinon un moniteur d'atelier doit être connecté avec un compte membre, qui peut lire ET
   modifier tout le suivi (essais, coûts…). Une fois publié : l'atelier n'a plus besoin de compte.
3. **Mode kiosque** (retour à l'écran de la ligne après inactivité, ligne figée par le QR code) + **écran de fin d'OP**
   (« OP10 contrôlée à 06:12, équipe Matin, 0 écart ») + thème nuit par défaut la nuit.
4. **État partagé entre appareils** pour l'équipe en cours (aujourd'hui les ✓ vivent dans chaque appareil ; le journal
   serveur est complet) : fonction serveur qui renvoie les statuts du jour, sans les commentaires.
5. **Alerte immédiate à Matis** sur un écart (phase 2 ; canal à choisir par Benjamin).
6. **Données** : renseigner les charnières manquantes dans l'outil principal (HESSAPP 266x13 / 266x22 / 283x26,
   EMAG 2 DP 290x12). ~~Faire confirmer T521 D1 = 2400~~ — **confirmé par Benjamin le 25/11 : valeur correcte** (un chanfrein uniquement).

**Points de vigilance connus (non corrigés)** : un compte connecté non membre voit « Aucun relevé » dans Outils › Checkup
(la règle de lecture renvoie 0 ligne, pas une erreur) ; n'importe qui ayant l'adresse peut AJOUTER des lignes au journal
(pas les lire) ; l'équipe dépend de l'horloge du téléphone (`recu_le` serveur permet le contrôle) ; le service worker de
l'outil principal sert `checkup.html` en cache d'abord — la mise à jour passe par `checkup-version.json` (changer `BUILD`
dans `checkup.html` ET `checkup-version.json`), et **pour tester en local, désenregistrer le service worker** (sinon on
regarde l'ancienne version).

## 1. Le but (mots de Benjamin)

Un outil **indépendant**, utilisable sur PC mais **testé par Matis sur iPhone/Android**, pour « le check-up du matin ». Usage final :
les moniteurs de l'atelier, chaque début d'équipe (3×8). **Objectif : vérifier qu'aucune charnière n'a été modifiée** — cela arrive
souvent, augmente fortement la consommation de plaquettes, et Matis ne peut pas le surveiller. **Mot-clé : simplicité absolue.**

Parcours voulu : choix de la **ligne** → choix de l'**OP** → toutes les charnières, **par outil et par logement**. L'ordre doit se
**régler par glissement** pour coïncider avec l'affichage du pupitre de la machine. Au bout de chaque rangée, une **validation** (vert)
qui dit que la charnière est bonne. Si elle a été modifiée : **la notification est enregistrée** (date, heure, ligne, OP, outil…).
Le fichier de **journal est stocké dans une section dédiée de l'outil principal**, branché par **Supabase**.

## 2. Décisions de Benjamin (verrouillées, ne pas rouvrir)

| Sujet | Décision |
|---|---|
| **Charnière** | = **nombre de pièces avant changement d'arête** (durée de vie par arête). Champ `charniere` du logement dans l'outil principal. **Pas** Vc ni f. |
| **Tolérance** | **Aucune.** Toute valeur différente de la référence est un écart. |
| **Potentiomètre** | doit être à **100 %** (« charnières figées »). **Exception : lignes EMAG = 120 %** (= valeurs nominales). |
| **Écart** | une valeur **nouvelle charnière** ET un **commentaire** doivent exister sur la feuille d'écart. |
| **Ce que voit l'opérateur** | la **valeur de référence** + boutons **✓** (conforme) et **≠** (modifiée). Pas de saisie systématique. (Vision de Claude, validée par Benjamin.) |
| **Ergonomie** | gros caractères, **gants**, cibles ≥ 72 px, chiffres tabulaires lisibles, bascule clair/nuit mémorisée. |
| **Design** | **design system exact de `bilan_economique.html`** (thème clair par défaut `#e8eaed` / cartes `#FFFFFF` / en-tête navy `#2F4159` / bleu `#1B5EA6` / rouge `#E2001A` alerte seule + thème nuit `#0f1317` / `#181d22` / `#5ba4f5`, rayon 3/4 px, polices `Open Sans` + `Open Sans Condensed` embarquées en base64). |
| **Marque / IP** | **aucune mention CeramTec ni SPK dans l'application.** Uniquement le rappel : « Conception et développement : Benjamin Rouquette · © 2026 — tous droits réservés · contenu confidentiel ». Ne **jamais** écrire dans l'app « écrit hors temps de travail / moyens personnels » (c'est dans le commentaire de code de l'outil principal, pas à l'écran). |
| **Adresse** | `https://suivi-optimisation-septfons.surge.sh/checkup.html` (même domaine que la PROD de l'outil principal). Installable en PWA. |
| **Recommandations de Claude acceptées** | pas de bouton « tout valider » (un ✓ par rangée) ; référence **publiée explicitement** pour l'atelier (« Publier pour l'atelier »), pas lue en direct dans les scénarios ; ordre réglé en mode « Organiser » ; journal en **table à part**, append-only ; on journalise **aussi les ✓** (preuve que le contrôle a été fait) ; **équipe (Matin/Après-midi/Nuit), pas de nom de personne** (sensibilité CSE) ; écran atelier **sans identifiant** (lien/code), droits Supabase minimaux ; **hors ligne** (file d'attente) ; alerte immédiate à Matis = phase 2. |

## 3. État au 24/11/2026 (`BUILD 2026-11-24.2`, commit `361be2d`, branche `ux-rail`, **déployé sur `suivi-optimisation-septfons.surge.sh/checkup.html`**)

**Front branché sur Supabase (10 lignes) et aligné sur le design system de `bilan_economique.html`.** Fichiers (tous à la racine, sauf icônes) :

| Fichier | Rôle |
|---|---|
| `checkup.html` | l'application complète (HTML+CSS+JS + polices `Open Sans` / `Open Sans Condensed` embarquées en base64, ~132 Ko). **Zéro donnée confidentielle codée en dur** (`const DATA` supprimé). |
| `checkup.webmanifest` | manifeste PWA : `id` `checkup-septfons`, `scope` `./checkup.html`, `start_url` `./checkup.html`, `theme_color` `#2F4159`, `background_color` `#e8eaed`. |
| `checkup-version.json` | `{"build":"2026-11-24.2"}` — signal de mise à jour (voir §6). **Ignoré par `.gitignore` (`*version.json`) : `git add -f`.** |
| `icons/checkup-192.png`, `-512.png`, `-512-maskable.png` | icônes (anneau bleu + coche verte), générées par script Pillow (non versionné). |
| `.surgeignore` | liste blanche étendue aux 6 fichiers ci-dessus. |

Ce que fait `checkup.html` (`2026-11-24.2`) :
- **Parcours 4 niveaux** : **Ligne** (les 10 lignes canoniques : `EMAG 1..3`, `HESSAPP`, `WEISSER 1..4`, `PCI 4..5`) → **Référence** (saut direct si 1 seule réf ; état vide clair si 0 réf) → **OP** → **Potentiomètre + Charnières** par outil·logement.
- **Branchement Supabase (`cxjfyaorkkxemjnollnj.supabase.co`) en double voie** :
  1. **Voie V1 prioritaire (sans identifiant)** : lit `GET /rest/v1/checkup_reference` dès qu'Hermes aura créé la table et publié des snapshots.
  2. **Voie cloud directe (active dès aujourd'hui)** : si `checkup_reference` renvoie 404 ou est vide, réutilise la session Supabase partagée avec `bilan_economique.html` (même domaine) ou propose une feuille « Connexion Supabase » pour tirer `POST /rest/v1/rpc/sync_pull` (`p_espace: "prod"`) et assembler les 10 lignes en direct.
  3. **Cache hors-ligne** (`cu_snapshot_v1`) + **file d'attente journal** (`cu_queue`) qui flushe automatiquement vers `POST /rest/v1/checkup_journal` dès que la table existe et que le réseau est là.
- **Design system identique à `bilan_economique.html`** : thème clair par défaut (`#e8eaed` / `#FFFFFF` / en-tête navy `#2F4159` / bleu `#1B5EA6`), thème nuit identique (`#0f1317` / `#181d22` / `#5ba4f5`) avec bascule `☀/☾` en en-tête, polices embarquées hors ligne, cibles gants ≥ 72 px, zéro mention CeramTec/SPK, pied de page IP Benjamin Rouquette conservé.
- **Fonctions atelier** : `✓` / `≠` (valeur ≠ référence + commentaire), détail au tap (plaquette, MABEC, Vc ou G97 `sBroche`, f), mode « Organiser » (poignée `≡`, glisser), équipe 3×8 automatique, avancement par OP / référence / ligne, potentiomètre 120 % EMAG / 100 % autres lignes.

**Non testé** : glisser-déposer sur un vrai téléphone / avec gants ; installation PWA sur un vrai téléphone ; déploiement Surge (attend le feu vert explicite de Benjamin).

**Pour Hermes (prochaine étape immédiate)** : `checkup.html` est déjà prêt côté client pour `checkup_reference` (GET) et `checkup_journal` (POST). Il suffit d'appliquer la migration SQL du §5 sur une branche Supabase puis prod (avec RLS + GRANT) : dès que les tables existent, `checkup.html` y basculera automatiquement sans retoucher son code.

## 4. À faire — dans cet ordre

1. **Valider avec Matis sur son téléphone** (installation PWA, lisibilité, gants). Recueillir ses retours AVANT de brancher Supabase.
2. **Remplacer les données de démo par un instantané publié.** Dans l'outil principal : un bouton « Publier pour l'atelier » (par
   ligne/référence/OP) qui écrit un **snapshot figé et versionné** (`ligne, référence, op, ordre d'affichage, rangées[outil, logement,
   plaquette, MABEC, charnière, Vc, f, mode, tr/min], potentiomètre attendu`, `publie_le`, `publie_par`). `checkup.html` lit **ce
   snapshot uniquement**, jamais les scénarios. Une modif légitime de charnière = republier ; sinon elle ressort en écart.
3. **Journal Supabase** (table dédiée, voir §5). Écriture seule pour l'atelier ; `checkup.html` met les événements en file d'attente
   hors ligne et les envoie au retour du réseau.
4. **Section « Journal des charnières » dans l'outil principal** (lecture) : écarts par ligne/outil/équipe, récidives, contrôles
   manquants (équipe qui n'a pas fait son contrôle), lien avec la consommation de plaquettes. **C'est un changement de
   `bilan_economique.html` → prendre le verrou (VERROU.md), version + CHANGELOG, tests, et attendre le feu vert de Benjamin pour déployer.**
5. **Ordre pupitre partagé** : enregistrer l'ordre (poignée ≡) **par ligne+OP côté serveur**, pas par téléphone (aujourd'hui `localStorage`).
6. Phase 2 : alerte à Matis (mail/notification) sur un écart ; export du journal.

## 5. Schéma Supabase (APPLIQUÉ le 24/11/2026 — voir §0 et `supabase_migrations/`)

Projet **`cxjfyaorkkxemjnollnj`**. L'outil principal stocke ses données dans `public.sync_shards(espace, id, kind, body jsonb, rev, seq,
supprime, modifie_par, modifie_le)`. **Ne pas y mettre le journal** : table dédiée.

```sql
-- instantané publié pour l'atelier (une ligne par ligne/référence/OP, remplacée à chaque publication)
create table public.checkup_reference (
  id text primary key,               -- 'EMAG 1/356x26 RPI/OP10'
  ligne text not null, reference text not null, op text not null,
  contenu jsonb not null,            -- rangées + ordre + potentiometre_attendu
  version int not null default 1,
  publie_le timestamptz not null default now(), publie_par text
);
-- journal : append-only, jamais modifié
create table public.checkup_journal (
  id bigint generated always as identity primary key,
  ts timestamptz not null default now(),
  equipe text not null check (equipe in ('Matin','Après-midi','Nuit')),
  ligne text not null, reference text not null, op text not null,
  type text not null check (type in ('charniere','potentiometre')),
  element text not null,             -- 'T517·D2' ou 'pot'
  attendu text, releve text,
  statut text not null check (statut in ('ok','ecart','annule')),
  commentaire text default '',
  version_reference int
);
```

**Droits (leçon apprise sur Fellow — RLS = RLS + GRANT)** : RLS activée sur les deux tables ; rôle atelier (`anon`) = `GRANT select` sur
`checkup_reference` seulement et `GRANT insert` sur `checkup_journal` seulement (pas de select/update/delete sur le journal) ; policies
correspondantes. Lecture du journal réservée à l'outil principal (utilisateur authentifié). Vérifier avec `get_advisors` après migration.

## 6. Pièges déjà rencontrés — à ne pas refaire

- **DÉPLOIEMENT SURGE : `surge` REMPLACE TOUT le site.** Le `bilan_economique.html` local (branche `ux-rail`) **n'est pas identique à la
  PROD** (au 24/11 : local `b0818d2a…` ≠ en ligne `e0d087fa…`). **Ne jamais déployer depuis la racine.** Procédure suivie : créer un
  dossier de préparation (`.deploy_checkup/`), y **télécharger par curl les fichiers actuellement en ligne** (`bilan_economique.html`,
  `index.html`, `service-worker.js`, `manifest.webmanifest`, `spk-app.css`, `spk-shell.js`, `version.json`, `icons/icon-192.png`,
  `icon-512.png`, `icon-512-maskable.png`), y ajouter les fichiers du checkup, noter leurs md5, puis
  `surge .deploy_checkup suivi-optimisation-septfons.surge.sh`, et **re-vérifier par curl que chaque ancien fichier est identique octet
  pour octet** (le « Success! » ne prouve rien), puis supprimer le dossier. Fait le 24/11 : 10 anciens fichiers identiques, 6 nouveaux servis.
- **Règle de Benjamin : ne JAMAIS déployer sans feu vert explicite dans le tour** (« déploie », « pousse »). Il veut garder le lead sur le
  rythme des mises à jour vues par Matis et Arthur.
- **Service worker** : celui de l'outil principal (`service-worker.js`, scope `./`) sert `checkup.html` en **cache d'abord** (seuls
  `bilan_economique.html`/`index.html` sont en réseau d'abord). **Ne pas le modifier** (un octet change = rechargement forcé des pages
  ouvertes de Matis). **Ne pas enregistrer un second SW au même scope** (il remplacerait celui de l'outil principal). Contournement en
  place : `checkup.html` lit `checkup-version.json` (nom terminé par `version.json` = réseau seulement côté SW) et, si le numéro diffère
  de sa constante `BUILD`, se recharge sur `checkup.html?b=<build>` (adresse neuve, hors cache). **À chaque mise à jour du checkup : changer
  `BUILD` dans `checkup.html` ET `build` dans `checkup-version.json`.** Si un jour le SW principal est modifié de toute façon, y ajouter
  `checkup.html` au réseau-d'abord et supprimer ce contournement.
- `.surgeignore` est une **liste blanche stricte** : tout nouveau fichier du checkup doit y être ajouté, sinon il ne part pas.
- **Données réelles en ligne** : la démo embarquée expose les charnières, Vc, f, plaquettes et MABEC de EMAG 1 356 et PCI 4 268 à
  quiconque a l'adresse. Le reste de l'outil garde d'habitude les données réelles en local. Acceptable pour une maquette demandée par
  Benjamin, **à supprimer dès le branchement Supabase** (le snapshot sera protégé par les droits).
- **Règle K/P** (AGENTS.md §2.6) : ne jamais exposer K = Vc × Hex ni P_req dans une sortie visible. Le checkup n'affiche ni coûts, ni temps,
  ni gains, ni K/P : **garder cette séparation**.
- Vocabulaire : jamais « CRM » (dire « Field Operations Suite »). Nuances toujours SPK (RST330, LST350, LSM800, SH4, SL500, SL506), jamais
  les noms Greenleaf.
- iPhone : champs de saisie ≥ 16 px (sinon zoom automatique). Déjà respecté (34 px / 22 px).
- Fins de ligne : Git avertit LF→CRLF sur Windows ; sans conséquence.

## 7. Anomalie de données à faire vérifier avant la première publication

EMAG 1 / 356x26 / OP20 : **T521 D1 a une charnière de 2400** alors que T521 D2 est à 150 et les autres logements à 150 ou moins.
**CONFIRMÉ CORRECT par Benjamin le 25/11/2026** : T521 D1 ne fait qu'un chanfrein, donc une durée de vie très longue. Ne plus le signaler.
Autres valeurs inhabituelles à relire : OP30 EMAG 1 (T533 = 1500, T535 = 4000, perçages) et OP30 PCI 4 (1500 partout).

## 8. Décisions qui restent à Benjamin (ne pas trancher à sa place)

- Le **nom** exact affiché (« Contrôle de prise de poste » aujourd'hui) et l'intitulé de l'icône (« Contrôle »).
- **Qui publie** la référence (Matis seul ? Benjamin aussi ?) et comment une charnière **légitimement** changée est republiée.
- **Que faire d'un écart** côté atelier : l'opérateur continue-t-il, appelle-t-il quelqu'un ? (aujourd'hui : il enregistre et continue.)
- Données de démo réelles en ligne : les laisser le temps de l'essai avec Matis, ou passer en valeurs fictives dès maintenant.
- Alerte immédiate à Matis (canal : mail ? autre ?) — phase 2.
- La référence **« DV 356x26 RPI »** (r1) d'EMAG 1 est un **reste du prototype d'août** (OP10 + 3 scénarios + essais Montronix du 26/08, volume vide) : Benjamin a décidé de la **garder**. Elle apparaît donc en double (ligne vide) dans le fichier central des volumes. Option si elle gêne : la renommer ou la sortir du tableau des volumes **sans toucher à ses données**.

## 9. Autre chantier en cours (hors checkup) — temps de coupe depuis les programmes CN

Détail dans `ECHANGES.md` (fin du journal, « Faits extérieurs — 24/11/2026 ») et `NOTES_A_VERIFIER_2026-11-24.txt`. En résumé : temps de coupe pure
saisis dans le cloud (références « Classeur Matis ») pour EMAG 1 356x26 (côté 1), PCI 4 DP268x12 (4 OP, T6417 simultané de T6407), EMAG 1 304x28
OP20 (côté 1). Scripts versionnés : `scripts/spf_temps.py` (Siemens), `scripts/fanuc_temps.py`, `scripts/recap_*.py`. Les **dossiers de programmes
et les recaps Excel sont la propriété de Stellantis : jamais dans le dépôt GitHub**. Lot 2 (champ « hors temps de coupe », gain par goulot) **attend les
réponses de Matis D1, D2, D4** ; l'**outil principal reste gelé** (correctifs bloquants seulement, chacun avec son verrou).

## 10. Critères d'acceptation du checkup (V1 branché)

1. Sur iPhone et Android : installation sur l'écran d'accueil, ouverture plein écran, hors ligne après une première visite.
2. Une équipe peut contrôler une OP de 10 rangées en moins d'une minute, avec des gants (cibles ≥ 72 px, aucune saisie si tout est conforme).
3. Un écart enregistre : date/heure, équipe, ligne, référence, OP, outil·logement, valeur attendue, valeur relevée, commentaire, version de référence.
4. Le journal est **immuable** (aucune policy update/delete) et **lisible uniquement** depuis l'outil principal.
5. Republier une référence ne génère pas de faux écart ; ne pas republier après un changement réel en génère un.
6. Aucune mention CeramTec/SPK dans l'application ; rappel Benjamin Rouquette présent ; aucun coût/temps/K/P affiché.
7. Après tout déploiement : curl — anciens fichiers identiques octet pour octet, nouveaux fichiers 200.

## 11. Prompts types pour reprendre

- **TIMON AI (orchestrateur)** : « Lis `BRIEFING_CHECKUP_TIMON_HERMES.md`. Étape 1 : prépare le plan de §4 en lots indépendants (snapshot publié ·
  journal Supabase + droits · section Journal dans l'outil principal · ordre pupitre serveur). Ne déploie rien et ne touche pas
  `bilan_economique.html` sans verrou. Rends les questions de §8 à Benjamin. »
- **Hermes** : « Reprends le lot « journal Supabase + droits » du §5 : écris la migration, applique-la **sur une branche Supabase** d'abord, vérifie
  RLS + GRANT avec `get_advisors`, teste insert anon / select refusé, puis rends la main. »
