# -*- coding: utf-8 -*-
"""Tour 73 : CHANGELOG 4.90.0 + liberation du verrou + entree de journal."""

c = open('CHANGELOG.md', encoding='utf-8').read()
entree = """## [4.90.0] — 2026-10-14 · Tour 73

**Les retours de la revue extérieure, appliqués.** Claude Code (version
gratuite, par dossier extrait) a lu les écrans critiques et rendu 8
directives priorisées. Les trois lots sont appliqués, les décisions
déléguées sont prises.

### Lot 1 — P7 (bugs visibles) + P6 (plancher de lisibilité)
- `data-plan` **échappé** (un MABEC importé avec un guillemet ne casse plus la ligne) ;
- le gain affiche le **bon signe** (négatif = + en rouge, jamais « − −X ») ;
- les **styles inline du Plan passent en classes** (`.simul-iso`, token
  `--ink-soft` ≥ 4,5:1) — le plein écran les corrige désormais vraiment ;
- **plancher de tailles** : `.os-sim` 9,5 → 11 px, `.status-badge` 10,5 → 11,5 px,
  labels d'accueil 11 → 12 px ;
- **le bloc Cadence quitte l'accueil** (jamais mesuré — on ne projette pas un
  tiret) et les **boutons suivent l'ordre du récit** : Catalogue → Plan →
  Simulateur.

### Lot 2 — P3 (l'honnêteté du Plan) + P2 (une seule base)
- **l'hypothèse de durée de vie est affichée et réglable** (« Durée de vie SPK :
  X % de l'actuelle ») — le gain = plaquettes/an × écart de prix, avec la
  cible qui dure X % de l'actuelle, donc il en faut plus ;
- **le seuil de neutralité** sur chaque ligne : la durée de vie minimale de la
  cible pour ne pas perdre — la réponse directe à « moins cher mais ça s'use
  plus vite » ;
- **le prix suggéré (5 €) sort du code** : réglage « Prix SPK défaut » dans le
  panneau — changer le prix change toutes les suggestions d'un coup ;
- **la case « Confirmé »** : une ligne dont le prix n'est pas confirmé reste du
  potentiel (le gain n'apparaît pas) — le total ne compte que le confirmé ;
- **le Simulateur partage le basculeur du Plan** : une seule base de
  consommation (théorique / réelle extrapolée) sur tous les écrans ; le réel
  est alloué au prorata du théorique entre les usages d'un article, étiqueté ;
- **les semaines/an sont éditables** (52 par défaut, borné 1-52) — la
  constante était codée en dur dans le basculeur.

### Lot 3 — P4 (dernier export) + P5 (atelier)
- **l'accueil affiche la date du dernier export** (« jamais exporté » nommé) ;
- **l'usure plaquette passe en pastilles** (— / OK / Limite / À changer) — le
  select natif demandait deux taps avec des gants ;
- **la conformité s'affiche EN DIRECT à la frappe** (✓ / ⚠ sous le champ),
  avant même d'enregistrer ;
- **les champs battement sont bornés** (0 à 10× la tolérance) — un 12 tapé pour
  0,012 est bloqué à la saisie ;
- **le message de charnière tient en 8 mots** — la version précédente était
  une phrase de jargon à 17 px.

### P1 — l'audit du secret K (fait immédiatement)
Claude avait vu juste : l'aide de l'outil affichait la formule K, ses points
de production et les angles validés. Retiré (4.89.1, déployé prod sur ordre),
et la porte hors-suite du harnais l'interdit définitivement.

### P8 — la décision (déléguée par Benjamin)
**Le monolithe `bilan_economique.html` est l'outil canonique.** `proto/`,
`projet3/` et `2resume/` restent dans le dépôt comme archives de recherche,
hors périmètre de déploiement. Le découpage par assembleur (calcul pur, puis
CSS/documents, puis cloud — chaque étape avec sortie identique à l'octet) est
en file, pas engagé.

### Le tour des CRLF
Le fichier portait **19 719 fins CRLF** qui faisaient échouer la moitié des
ancres de patch. Normalisé LF une fois pour toutes ; `build_harness.py`
réparé (le même mal : `\r\r` cassait les continuations Python). Tous les
patchs futurs passent par des fichiers et une normalisation en tête.

### Vérification
- 521 → **552 tests** (5 suggestion + 1 non-confirmée + 6 CSS/portes) ;
- contre-regards : confirmation sautée → **vue** au centime près ; potentiel
  compté comme promesse → **vue** ; restauration par copie, empreinte
  identique à chaque fois.

"""
ancre = "## [4.89.0]"
assert ancre in c, "ancre changelog: " + ancre
c = c.replace(ancre, entree + ancre, 1)
open('CHANGELOG.md', 'w', encoding='utf-8').write(c)
print("changelog 4.90.0")

v = open('VERROU.md', encoding='utf-8').read()
i = v.find("| **Auteur** | Z Code |")
j = v.find("\U0001F512", i)
assert i > -1 and j > i, "bloc verrou pris introuvable"
v2 = ("""| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

""" + "✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 73, v4.90.0). Pendant le\n"
"tour, les trois lots de la revue Claude sont appliqués : P7 (data-plan\n"
"échappé, signe du gain, ordre des boutons, Cadence retiré, taux en état),\n"
"P6 (plancher de tailles, token secondaire ≥ 4,5:1, styles inline en\nclasses), P3 (hypothèse DDV affichée et réglable, seuil de neutralité, prix\n"
"SPK en réglage, confirmation case par case, Potentiel), P2 (le Simulateur\n"
"partage le basculeur, semaines/an éditable), P4 (dernier export affiché),\n"
"P5 (usure en pastilles, conformité en direct, bornes, charnière en 8 mots).\n"
"Le fichier est **normalisé LF** (19 719 CRLF) — fin des ancres capricieuses.\n"
"P8 : monolithe canonique, archives intactes (décision déléguée). 521 →\n"
"**552/552 verts**. Contre-regards vus. **Déployé sur Projet, vérifié curl ;\n"
"la PROD attend la phrase de Benjamin.** Écrits : `bilan_economique.html`,\n"
"`outils/patch_4900_v2.py`, `outils/tour73_journal.py`, `build_harness.py`,\n"
"`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`, `AUDIT_CLOUD_RLS.md`.\n\n"
+ v[j:])
open('VERROU.md', 'w', encoding='utf-8').write(v2)
print("verrou libéré")

s = open('ECHANGES.md', encoding='utf-8').read()
tour = """### Tour 73 — 14/10/2026 — **Z Code** (v4.90.0 — les trois lots de la revue Claude)

**La commande.** Benjamin : « envoie tous les lots et décide pour moi » —
les huit directives de la revue Claude Code, triées et appliquées.

**Les décisions déléguées, prises.** P8 : **le monolithe est canonique**,
les trois réécritures restent en archives (rien supprimé), l'assembleur est
en file avec la contrainte de sortie identique à l'octet. Le cloud reste
actif (les données sont déjà chez Stellantis, Matis et Benjamin s'en
servent) — la **fermeture des inscriptions** au dashboard Supabase est
recommandée à Benjamin (dashboard only). Le bloc **Cadence quitte
l'accueil** (jamais mesuré — on ne projette pas un tiret). Les boutons
suivent **l'ordre du récit commercial** : Catalogue → Plan → Simulateur.

**Lot 1 — la crédibilité visible.** `data-plan` échappé, le signe du gain
corrigé (jamais « − −X »), Cadence retiré, les styles inline du Plan passent
en classes (`.simul-iso`, token `--ink-soft` ≥ 4,5:1) — le plein écran les
corrige désormais réellement. Plancher de tailles : `.os-sim` 9,5 → 11 px,
`.status-badge` 10,5 → 11,5 px, labels 11 → 12 px.

**Lot 2 — l'honnêteté du Plan.** L'**hypothèse de durée de vie** affichée et
réglable (« Durée de vie SPK : X % de l'actuelle » — le gain en dépend et le
dit). Le **seuil de neutralité** sur chaque ligne : la durée minimale pour ne
pas perdre — la réponse à « moins cher mais ça s'use plus vite ». Le **prix
suggéré sort du code** (réglage « Prix SPK défaut »). La **case Confirmé** :
une ligne non confirmée reste du potentiel (gain null), le total ne compte
que le confirmé. « Promesse » renommé **« Potentiel engagé »**. Et **le
Simulateur partage le basculeur** — une seule base de consommation sur tous
les écrans, le réel alloué au prorata du théorique, étiqueté.

**Lot 3 — les garde-fous.** L'accueil affiche la **date du dernier export**
(« jamais exporté » nommé). L'usure plaquette passe en **grosses pastilles**
(— / OK / Limite / À changer). La **conformité s'affiche EN DIRECT à la
frappe** (✓ / ⚠ sous le champ). Les champs battement sont **bornés**
(0 à 10× la tolérance — un 12 tapé pour 0,012 est bloqué). Le message de
charnière tient en 8 mots.

**P1 — l'audit du secret K, fait immédiatement.** La formule, ses points de
production et les angles validés étaient dans l'aide affichée. Retirés
(4.89.1, déployé prod), et la **porte hors-suite** du harnais les interdit
définitivement (formule + points + angles + titre de section = absents).

**Le tour des CRLF.** Le fichier portait **19 719 fins CRLF** qui faisaient
échouer la moitié des ancres. Normalisé LF une fois pour toutes ;
`build_harness.py` réparé (le même mal : `\r\r` cassait les continuations
Python). Tous les patchs futurs passent par des fichiers, normalisation en
tête.

**Contre-regards vus.** Confirmation sautée → gain au centime près alors
qu'il doit être null → **vu**. Potentiel compté comme promesse → **vue**.
Restaurations par copie, empreintes identiques, 521 → **552/552 verts**.

**Déploiement.** Projet, vérifié curl. La prod attend la phrase de Benjamin.

**Prochain tour** : le test tablette avec gants (20 mesures chronométrées) ;
la revue d'Hermes ; l'export de l'accueil ; le chantier UI de fond.

"""
ancre = "## Questions ouvertes \u00e0 Z Code"
assert ancre in s
s = s.replace(ancre, tour + ancre, 1)
open('ECHANGES.md', 'w', encoding='utf-8').write(s)
print("tour 73 écrit")

# ── AUDIT_CLOUD_RLS.md — les 10 lignes demandées par la revue Claude P1 ──────
audit = """# AUDIT CLOUD / RLS — les 10 lignes (revue Claude P1)

- **Ce qui est poussé** : une table `etat`, une ligne = le suivi complet
  (~3,4 Mo : références, essais, prix, volumes, photos en base64), +
  `etat_historique` (20 versions, trim par trigger). Le catalogue et le Plan
  de conversion ne sont PAS encore dans le payload cloud (locale only).
- **Vers quelle table** : `etat` (une ligne), projet Supabase `suivi-septfons`
  (org « Sept Fons », région EU).
- **Quelle clé** : la clé `publishable` (anon) est dans le HTML public — par
  conception, elle ne donne aucun droit sans être authentifié.
- **RLS** : `authenticated` + GRANT sur les tables. **Quiconque crée un compte
  peut lire et écrire.** La porte est la page de login.
- **À décider par Benjamin** : fermer les inscriptions dans le dashboard
  Supabase (Authentication → Providers → Email : désactiver le signup) tant
  que l'accord client sur l'hébergement des données n'est pas écrit.
- **Le cloud est actuellement en 402** (quota egress épuisé) : aucun transfert
  ne passe tant que le quota n'est pas réinitialisé ou le plan pas upgradé.
- **Si le cloud est jugé incompatible** : il se désactive par défaut (le
  tooling tourne 100 % offline, la synchro est optionnelle et coupable par
  une constante).
- **Le calcul qui produit K et P_req n'est PAS dans ce fichier** — le secret
  thermique vit dans l'app conseiller (autre projet). L'aide qui l'exposait a
  été retirée en 4.89.1 et la porte hors-suite l'interdit.

*Z Code — 14/10/2026, Tour 73.*
"""
open('AUDIT_CLOUD_RLS.md', 'w', encoding='utf-8', newline='\n').write(audit)
print("AUDIT_CLOUD_RLS.md écrit")
