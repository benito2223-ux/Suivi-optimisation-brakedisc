# PROMPT — REVUE CRITIQUE CLAUDE CODE (version gratuite)

> **Mode d'emploi pour Benjamin** : ouvre Claude Code DANS le dossier du projet
> (`C:\Users\Admin\Desktop\Stellantis_SeptFons`) et colle simplement :
>
> `Lis PROMPT_CLAUDE_CODE_REVUE.md et suis-le à la lettre. Tu ne modifies AUCUN
> fichier : tu écris uniquement ta revue dans CLAUDE_CODE_REVUE.md.`
>
> Le prompt ci-dessous est ce que le fichier contient. Budget gratuit = lectures
> limitées : le chemin de lecture est calibré pour ne pas dépasser.

---

## TON RÔLE

Tu es un relecteur critique EXTÉRIEUR. L'outil a été construit par une IA (Z Code)
avec une autre IA en relecture croisée (Hermes) — ils sont fiers de leur travail et
risquent la complaisance. **Ton travail : ne pas l'être.** Cherche ce qui cloche,
ce qui va casser, ce qui va faire fuir l'utilisateur, ce qui est surdimensionné ou
sous-dimensionné. Tu proposes, tu ne codes pas.

## LE PROJET EN 10 LIGNES

Outil de suivi d'optimisation du coût de revient des disques de frein (usinage
céramique, site Stellantis Sept Fons). **Un seul fichier HTML** :
`bilan_economique.html` (~19 200 lignes, 1,5 Mo), zéro build, zéro SDK,
offline-first, PWA, synchro cloud optionnelle (Supabase, actuellement en quota).
Trois publics : l'atelier (Matis, opérateurs, gants + tablette, saisie rapide),
le pilote (Matis again), la hiérarchie (documents imprimables). L'outil est
AUSSI un outil commercial : il doit démontrer à Matis l'économie du passage sur
les plaquettes SPK (le catalogue, le Plan de conversion, le simulateur).

Version courante : **4.89.0** — 551 tests verts (harnais maison). Déployé sur
deux domaines surge.sh (prod + projet).

## LES RÈGLES DU JEU (résumé de CONSTITUTION_SUIVI_v1.md — lis-le, il est court)

- §3.5 : aucun chiffre mensonger — un absent se nomme, jamais un zéro qui prétend ;
- 2 quater : le coût plaquette et le temps machine sont DEUX AXES, jamais sommés ;
- §3.4 : ne pas additionner des gains de natures différentes ;
- §6 : rien n'est déployé sans phrase de Benjamin ; on propose, on ne tranche pas ;
- K (Vc×Hex) et P_req n'apparaissent JAMAIS dans les sorties visibles (secret
  interne SPK) — vérifie qu'aucun écran ne les expose ;
- les données réelles ne sortent jamais du poste (lecture classeur locale).

## CHEMIN DE LECTURE (dans cet ordre, sans dévier — ton budget est compté)

1. `CHANGELOG.md` — les 5 dernières versions seulement (tu sauras ce qui vient
   d'être fait et comment ils écrivent) ;
2. `ECHANGES.md` — les 3 tours en tête (le journal des deux IA) ;
3. `CONSTITUTION_SUIVI_v1.md` — en entier (il tient sur un écran et demi) ;
4. `bilan_economique.html` — JAMAIS en continu. Par sondes :
   - `grep -n "^function \|^async function " bilan_economique.html` (la carte du code) ;
   - le CSS : lignes 200-1600 (palette, .wrap, .panel, tuiles, tailles de police) ;
   - l'écran d'accueil : cherche `function accueilHTML` / `accueilBandeauHTML` / `renderAccueil` ;
   - la saisie atelier : `function atelierHTML` / `renderAtelier` ;
   - le socle commercial : `planHTML` / `simulHTML` / `catalogueRendu` ;
   - le harnais : `build_harness.py` (comment ils testent).
5. Optionnel (si ton environnement l permet) : `python -m http.server 8765` puis
   lis le HTML rendu — tu ne peux pas voir le rendu visuel, dis-le honnêtement
   dans ta revue et juge le DOM et le CSS, pas l'apparence.

## LES AXES D'ANALYSE (sois impitoyable, cite des numéros de lignes)

**A. Ergonomie de saisie atelier** — Matis saisit avec des gants sur une tablette
dans un atelier bruyant. Les formulaires sont-ils saisissables ainsi ? Les
champs sont-ils assez gros ? Le clavier numérique vient-il automatiquement ?
Combien de taps pour enregistrer une mesure ?

**B. Hiérarchie visuelle** — Benjamin dit lui-même : « tout est ton sur ton, trop
petit ». Fond gris #e8eaed, cartes blanches, intitulés gris : la palette se
suffit-elle ? Que changerais-tu EN PREMIER, avec le moins de risque ?

**C. Le monolithe** — 19 200 lignes dans un seul fichier : où est la limite ?
Quelles zones (calcul, UI, cloud, tests) mériteraient une séparation ? Sois
pragmatique : l'équipe est composée d'IA et d'un non-développeur.

**D. Le socle commercial** — catalogue (CSV), Plan de conversion (états
step-by-step), basculeur de consommation (théorique vs réel ×52), simulateur.
La chaîne est-elle cohérente ? Compréhensible par Matis ? Que manque-t-il pour
que la démonstration soit imparable ?

**E. Les angles morts** — ce que personne n'a vu : dépendances cachées, états
globaux fragiles, points de casse, sécurité, ce qui se passe hors ligne, ce qui
se passe quand deux postes éditent en même temps.

## FORMAT DE SORTIE — `CLAUDE_CODE_REVUE.md`

Écris EXACTEMENT cette structure :

```
# REVUE CLAUDE CODE — <date>

## Verdict en 5 lignes (sans complaisance)

## Directives priorisées (5 à 10 max)
### P1 — <titre>  (à faire avant tout)
- Problème : ... (ligne(s) citée(s))
- Pourquoi c'est important : ...
- Directive concrète : ... (ce que Z Code doit faire, pas comment coder)
- Effort estimé : S / M / L

### P2 ... P3 ... (même format)

## Ce qui est BIEN fait (court, honnête — pour que la critique soit crédible)

## Ce que tu n'as pas pu évaluer (et pourquoi)
```

## INTERDITS

- Ne modifie AUCUN fichier sauf CLAUDE_CODE_REVUE.md ;
- Ne propose rien qui viole les règles du jeu ci-dessus (surtout §3.5 et K/P) ;
- Pas de complaisance (« c'est très bien ») : Benjamin paie en temps de lecture ;
- Pas de refonte totale : les directives doivent être implémentables
  incrémentalement par Z Code ;
- Ne lis pas les 19 200 lignes en continu : tu épuiseras ton budget avant la
  fin. Sonde, cite, passe.

---

*Prompt préparé par Z Code le 14/10/2026 — v4.89.0, 551 tests verts, journal à
Tour 72.*
