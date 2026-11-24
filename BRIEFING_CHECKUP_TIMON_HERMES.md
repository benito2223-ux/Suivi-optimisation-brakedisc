# BRIEFING — « Contrôle de prise de poste » (checkup) — passation à TIMON AI / Hermes

> Auto-contenu : ce fichier suffit pour reprendre le travail. Écrit le 24/11/2026 par Claude, sur demande de Benjamin
> (« confier la suite à TIMON AI et à Hermes »). Ordre de lecture : `VERROU.md` → ce briefing → dernier tour de `ECHANGES.md`.
> Langue de travail avec Benjamin : français. Il écrit en dictée vocale. Il attend une direction assumée, pas un catalogue d'options.

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
| **Ergonomie** | gros caractères, **gants**, faible luminosité → thème nuit, cibles ≥ 72 px, texte ≥ 22 px. |
| **Design** | design system de l'outil principal (jetons thème nuit, rayon 3 px, rouge = accent seulement, Open Sans / Open Sans Condensed). |
| **Marque / IP** | **aucune mention CeramTec ni SPK dans l'application.** Uniquement le rappel : « Conception et développement : Benjamin Rouquette · © 2026 — tous droits réservés · contenu confidentiel ». Ne **jamais** écrire dans l'app « écrit hors temps de travail / moyens personnels » (c'est dans le commentaire de code de l'outil principal, pas à l'écran). |
| **Adresse** | `https://suivi-optimisation-septfons.surge.sh/checkup.html` (même domaine que la PROD de l'outil principal). Installable en PWA. |
| **Recommandations de Claude acceptées** | pas de bouton « tout valider » (un ✓ par rangée) ; référence **publiée explicitement** pour l'atelier (« Publier pour l'atelier »), pas lue en direct dans les scénarios ; ordre réglé en mode « Organiser » ; journal en **table à part**, append-only ; on journalise **aussi les ✓** (preuve que le contrôle a été fait) ; **équipe (Matin/Après-midi/Nuit), pas de nom de personne** (sensibilité CSE) ; écran atelier **sans identifiant** (lien/code), droits Supabase minimaux ; **hors ligne** (file d'attente) ; alerte immédiate à Matis = phase 2. |

## 3. État au 24/11/2026 (commit `e25e631`, branche `ux-rail`, rien poussé sur GitHub)

**C'est une MAQUETTE.** Fichiers (tous à la racine, sauf icônes) :

| Fichier | Rôle |
|---|---|
| `checkup.html` | l'application complète (HTML+CSS+JS, un seul fichier), ~315 lignes. Données de **démo embarquées** (`const DATA`). |
| `checkup.webmanifest` | manifeste PWA : `id` `checkup-septfons`, `scope` `./checkup.html` (volontairement étroit pour ne pas se mélanger à l'outil principal), `start_url` `./checkup.html`. |
| `checkup-version.json` | `{"build":"2026-11-24.1"}` — signal de mise à jour (voir §6). **Ignoré par `.gitignore` (`*version.json`) : `git add -f`.** |
| `icons/checkup-192.png`, `-512.png`, `-512-maskable.png` | icônes (anneau bleu + coche verte), générées par script Pillow (non versionné). |
| `.surgeignore` | liste blanche étendue aux 6 fichiers ci-dessus. |

Ce que fait la maquette : écrans Ligne → OP → liste (potentiomètre + rangées outil·logement), `✓` / `≠` (feuille avec valeur +
commentaire, refuse une valeur identique à la référence), détail au tap (plaquette, MABEC, Vc, f ou G97 tr/min), mode « Organiser »
(poignée ≡, glisser), équipe déduite de l'heure (5-13 Matin, 13-21 Après-midi, 21-5 Nuit — la nuit appartient au jour de son début),
avancement par OP (« 3/7 », « ⚠ »), « Journal des écarts (aperçu) ». **Tout est local** (`localStorage` : `cu_checks`, `cu_order`,
`cu_log`) ; **rien n'est envoyé nulle part**.

Données de démo = vraies charnières « Classeur Matis » de **EMAG 1 / 356x26 RPI** (OP10-OP40) et **PCI 4 / 268x12** (OP10-OP40),
lues dans le cloud le 24/11 (shards `sc:<op>:s-<…>`, `base=true`).

**Non testé** : glisser-déposer sur un vrai téléphone / avec gants ; installation PWA sur un vrai téléphone ; offline réel.

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

## 5. Schéma Supabase proposé (NON appliqué — à valider)

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

EMAG 1 / 356x26 / OP20 : **T521 D1 a une charnière de 2400** alors que T521 D2 est à 150 et les autres logements à 150 ou moins. Probable coquille
de saisie dans l'outil principal (ou plaquette à très longue durée de vie). **Ne pas publier à l'atelier sans que Matis confirme.**
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
