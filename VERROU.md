| **Auteur** | **Hermes** |
| **Pris le** | 30/10/2026 |
| **Écrit dans** | `spk-app.css`, `spk-shell.js`, `bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md` |
| **Version visée** | 4.130.1 |
| **Sujet** | Reprise du lot 4.130 : hiérarchie réelle des boutons (un principal plein par écran), en-tête 2 rangées vérifié au rendu (1440 ET 390), onglets soulignés, débord mobile 390 réglé, captures livrées pour chaque point. |

---

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

---

✅ **Verrou libéré par Hermes le 30/10/2026** (Tour 110, v4.130.1 — reprise
du lot 4.130 : « + Scénario » principal bleu plein, en-tête mobile
343 px → 95 px, mesure du débord interne, porte coque 4.130.1, contre-regard
3 régressions vues, 673/0, DEV vérifiée curl). **PROD : rien — 4.129.1.**
Reste au brief : lot 4.131 (chiffre de gain, états vides), lot 4.132 ;
`outils/mesure_41301.py` fournit captures et mesures 1440/390 pour chaque
Attention au cache service worker pour tout test visuel :
purger les registrations avant de juger un rendu.

✅ **Verrou libéré par Z Code le 29/10/2026** (Tour 109, v4.130.0 — passe
design lot 4.130 : boutons et en-tête). **Charter v4.70 (disque noir +
chevron) remplacé** par trois niveaux (principal bleu plein unique,
secondaire contour, tertiaire texte ; rouge = accent/destructif) ; les
principaux foisonnants rétrogradés (13 → 1 réel par écran : Voir l'atelier,
pf*, alClose, Mode atelier, atelier-open, + Créer un projet → ghost) ;
**+ Scénario en tuile d'invitation pointillée** de la Vue d'ensemble
(4.131.B anticipé, annoncé), masqué quand un espace plein écran s'ouvre
(:has(), l'Accueil exclu car il EST un .panel-large) ; **en-tête 2 rangées
remplace le rail** : navy #2F4159 54 px (mark, titre déplacé — le h1 se
met à jour, actions : Rechercher câblé sur ouvrirRecherche, Transmettre,
verrou, mode, •••, aide) + blanc 48 px (onglets soulignés 2 px bleu — VE ·
Synthèse · Matis · Atelier ; fil d'Ariane compacté ; bandeau projets
tertiaire) ; **105 px total** (≤ 110), --spk-head-h mesurée par
ResizeObserver ; écrans plein écran sous l'en-tête ; Données locales +
version au pied de page ; **filigrane au coin en DEV seulement**
(body[data-env=dev] posé par appliquerFondLigne) ; **virgule orpheline de
la grille Composition** : tuileOutil sans join — le cast Array séparait
par « , » ; chips pointillées + bleu. **Pièges** : la règle filigrane
tombée DANS le @media print (piège du head rejoué, corrigé au rendu) ; le
SW local a servi l'ancien CSS trois mesures (purge systématique) ; la
porte coque 4.100 recalée en 4.130 (en-tête, plus de rail, z 90 > 80,
poignée neutralisée) et le bug **'z-index:' = 8 caractères** (j+9 mangeait
le chiffre sans espace : z-index:90 lu 0 — l'ancienne convention avec
espace le masquait) ; contre-regard z 50 → porte tombée. **Vérifié** :
673 tests | 0 échec, 0 erreur syntaxe, 16 blocs style équilibrés,
1 principal/écran (6 écrans, mesure rect+elementFromPoint), verrouillé :
0 action de saisie + bannière, 0 erreur console, 0 débord 1440. Captures
avant/après 6+6 — **une capture (verrouillé 1440) en retard à la
livraison** (surface IAB saturée en fin de salée ; l'état verrouillé est
prouvé programmatiquement). **Écarts annoncés** : + Scénario pointillé
dès 4.130, Atelier revient en onglet (le brief le liste), Rechercher =
câblage existant, portes historiques du rail vertes sur règles inertes.
**DEV** : 4.130.0 servie, SHA-256
`d72d4be5a318cc62eef38abe2389b6708fccce5e360d8e54f964ae4a6d1f19ab`
(dist == servi, intégral), version.json `{"v":"4.130.0"}`, sensibles 404.
**PROD : rien** — Benjamin regarde le rendu. Écrits :
`bilan_economique.html`, `spk-shell.js`, `spk-app.css`, `build_harness.py`,
`outils/patch_41300_a-e.py`, `outils/captures_4130/`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 29/10/2026** (Tour 108 ter — **PROD 4.129.1**

---

✅ **Verrou libéré par Z Code le 29/10/2026** (Tour 108 ter — **PROD 4.129.1**
passée sur la phrase de Benjamin). Rebuild de contrôle : le dist reconstruit
est **identique octet pour octet** au dist vérifié (SHA-256 `c280fdef…`,
intégral). **Publiée** sur suivi-optimisation-septfons.surge.sh et vérifiée :
HTML servi 1 538 256 octets SHA-256
`c280fdefee9b314d592972ec1b9107a9bdc8cba7ac87e7936a8fb4c25f81909b`
(dist == servi), `version.json` servi `{"v":"4.129.1"}`, SW/CSS/shell/manifest
200 identiques au dist, sensibles 404, **rendu public regardé** (TOOL_VERSION
4.129.1, pied « v4.129.1 », suite inerte, écran complet — capture regardée,
profil du navigateur de test purgé et fermé). **Retour arrière sous la
main** : `outils/retour_arriere/4.126.0_bilan_economique.html`
(SHA `ed95f499c7c414d5…`) — une publication remet la 4.126.0 ; à garder
pendant la première semaine (consigne Benjamin). **LOT 4 gelé** jusqu'à
stabilité. Écrits : `dist/` (rebuild), `ECHANGES.md`, `VERROU.md` —
**pas dans `bilan_economique.html`.**

---

✅ **Verrou libéré par Z Code le 29/10/2026** (Tour 108 bis — le contrôle
pré-prod demandé par Benjamin, fait). **rev433 injectée par le vrai chemin
d'import dans la prod 4.126.0 (téléchargée, SHA `ed95f499c7c414d5…`, l'empreinte
exacte du Tour 103 — archivée dans `outils/retour_arriere/` : le retour arrière
est sous la main) et dans le dist 4.129.1.** Scénario actif des deux côtés :
« Process actuel - OP40 » (le cas T543), révision 433, 11 essais chacun.
**Gain annuel 3 394 €/an et ≈ 6 788 €/an : identiques. Coût/pièce 0,0080 € :
identique.** Trois affichages bougent de leur composante machine exacte (base
0,457 → 0,146 €/pièce, OP40 0,327 → 0,016, OP15 0,411 → 0,037 — la tuile
« 0,3111 € machine/pièce » reste à part) : **c'est la redéfinition actée du
LOT 3, pas une régression — les coûts absolus baissent, les gains restent.**
Deux fausses alertes résolues : shadowing de `lignes` dans mon script
d'extraction (le produit n'est pas concerné, 11 essais recomptés) ; et
`CLOUD_ECRITURE_AUTORISEE` est vrai sur localhost — vérifié **deux gardes
indépendantes** (`cloudSync`, `cloudApresSauvegarde` : `if(!cloudSession)
return`) et le profil de test n'a jamais été connecté : **rien n'a pu partir
vers la prod**. Profils purgés, serveurs arrêtés. Écrits :
`outils/retour_arriere/4.126.0_bilan_economique.html`, `ECHANGES.md`,
`VERROU.md` — **pas dans `bilan_economique.html`.**

---

✅ **Verrou libéré par Z Code le 29/10/2026** (Tour 108, v4.129.1 — suite
navigable, atelier 56 px tout interactif). **#tests au navigateur** : la
faute était `global.localStorage` dans la porte TDZ (v4.112.1) — Node-only,
l'exception interrompait la suite au test n° 472 (constat Benjamin 471/472).
**globalThis + sonde** : l'accesseur window.localStorage n'a pas de setter,
la sonde vérifie la substitution et la porte l'annonce (« jouée pour de vrai
au harnais ») au lieu d'échouer — **première sonde fausse attrapée au test
réel** (elle interrogeait lsFaux, toujours vrai) ; corrigée, la sonde passe
par la globale. **663/663 tout est vert au navigateur** (673 au harnais :
dix tests vivent sous des branches d'environnement). **Atelier 56 px** :
inputs texte/nombre tous, textarea, summary, .pcb-op, cases à cocher 56 px
de boîte cliquable pour 28 px dessinés (border transparent +
background-clip:content-box) ; select déjà couvert. **Mesure v2** : cinq
écrans (saisie d'essai, vue d'ensemble, synthèse, Matis, Transmettre menu
ouvert), tout interactif — **653 interactifs, zéro sous 56 px ; 2 389
textes, zéro sous 12 px** ; attente 2 200 ms par écran (à 900 ms : 156
textes transitoires sur la Vue d'ensemble, la passe throttlée du plancher
était en cours — faux positif nommé au script). Playwright absent du poste :
mesure tournée à l'IAB avec le même JS. **Empreinte nommée** (SHA-256
intégral) : dist/bilan_economique.html **1 538 256 octets,
`c280fdefee9b314d592972ec1b9107a9bdc8cba7ac87e7936a8fb4c25f81909b`**, fichier
servi identique octet pour octet, annexes hachées au journal, version.json
servi `{"v":"4.129.1"}`, sensibles 404. **Vérifié** : 673/0 harnais,
syntaxe 0 erreur, CR4 (summary amputé → porte tombée, restauration SHA
identique), capture regardée (atelier : barre boutons pleins et hauts,
fil agrandi, aucun débord — un screenshot transitoire mesuré scrollW =
clientW = 1280). Profils embarqués purgés. **PROD** : 4.126.0 — tout
attend ta phrase. Écrits : `bilan_economique.html`, `build_harness.py`,
`outils/mesure_atelier.py`, `outils/patch_41291_a/b.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 29/10/2026** (Tour 107, v4.129.0 — LOT 5 :
l'hygiène). **Les tests ne partent plus dans le livré** : étape « 5 bis » du
build retire le bloc des tests (~3 550 lignes) du dist — **1 536 582 octets
servis contre 1 806 267 au source (~15 % de moins)** — le harnais garde sa
source dans le monolithe ; la **botte secrete (v4.42) est extraite et
reposée à la même place** (elle vivait dans le bloc : l'aide K reste masquée
pour tous) ; le contrôle « 7 bis » refuse de livrer une suite résiduelle ou
un style déséquilibré. **Test de sécurité à l'import** (6 tests in-suite) :
payload `<img src=x onerror=` dans chaque champ texte, vrai chemin d'import,
chaque innerHTML écrit capté — la forme crue interdite partout, le payload
échappé exigé au moins une fois (porte non aveugle) ; saveData neutralisé
pendant le test. **Charnière `step="any"` + inputmode** (table des pièces) —
résidu nommé : le champ charnière des logements garde step="1" (le brief ne
le nommait pas, à trancher). **Lint CSS étendu au dist** (porte + build).
**Porte fausse au vert attrapée** : le motif du build survivait dans le
commentaire de l'étape — recalée sur la déclaration complète, contre-regard
rejoué, porte tombée. **Vérifié** : 673 tests | 0 échec (+6), syntaxe 0
erreur, 3 contre-regards vus (21 rendus exposent le payload sans
l'échappement `<` ; porte tombée ; build en échec bruyant), rendu regardé au
navigateur (capture, écran complet), sécurité au navigateur réel (aucun
onerror exécuté, 0 img crue, payload en texte échappé), charnière 1250
valide, #tests inerte, profil embarqué purgé. **DEV** : 4.129.0 servie,
SHA-256 `90150065501a7760…` == dist, version.json cohérent. **PROD** :
4.126.0 — LOT 2, LOT 3 et LOT 5 attendent ta phrase (aucun chiffre affiché
ne change avec la 4.129). Écrits : `bilan_economique.html`,
`outils/build-coque.mjs`, `build_harness.py`, `outils/patch_41290_a/b/c/d/
d2/d3.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 106, v4.128.0 — LOT 3 :
le chiffre de tête est le gain d'outillage). **coutsDetail** ne somme plus
plaquettes + machine (total = plaquettes + pièces ; cumul sur demande) ;
**bilanAnnuel** : le gain = l'écart d'outillage, les écarts machine (h/an +
€/an) et rebut en champs séparés ; **la fourchette** visée/min/moyenne avec
étiquette (« objectif, non mesuré » / « mesuré (min, N essais) ») ;
**charniereReelle** expose min/N/fins réelles/moyenneFins(≥ 5) +
charniereReelleParLogement pour la substitution ; **polarité des heures**
(« plus rapide » / « plus lent ») ; **plaquettesParAn** (conditionnement +
casse, vides = inchangé) ; **le rebut nomme son N** ; **la fusion nomme le
conflit d'horloge < 10 min** (local conservé, signalé). **Recalages
documentés** : coutsDetail (outillage / cumul), seuilBascule (axe
outillage, « hors plaquettes » = pièces + rebut, le fixture contrôle sa
comparaison), le non-réparti du verdict par outil dit la productivité
machine non portée. **Vérifié** : 667 tests | 0 échec (+2), syntaxe 0
erreur. **DEV** : 4.128.0 servie, SHA-256 `0491ad8ebb49bdd3…` == dist,
version.json cohérent. **PROD** : 4.126.0 — le LOT 3 attend ta phrase.
Écrits : `bilan_economique.html`, `outils/patch_41280_a.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---
---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 105, v4.127.1 — l'étape 0
de la feuille de route). **Empreinte** : SHA-256 nommé, périmètre = dist +
fichier servi, recalculés identiques (`4a1d3bc919e775b20e5124bef2709aaadc16cfbf2b66d01babaa997fe6cf16f9`)
— le protocole nomme désormais algorithme et périmètre. **Plancher 12 px** :
MutationObserver throttlé (200 ms) + restauration en sortie de mode — mesure :
417 éléments de texte, **1 résidu = le 🔒 à 0 px masqué volontairement** (le
critère honnête : « aucun texte visible ») ; le script annexe livré
(`outils/mesure_atelier.py`). **Atelier** : disques ::before supprimés,
filigrane masqué, boutons icône étiquetés (data-etiquette + ::after), aide
projet sans chevauchement. **SPK_MAJ** : les mêmes gardes (saisie, flush,
anti-boucle par CACHE). **version.json network-only** dans le SW. **Cause
réelle du rejet CSS nommée** : le bloc atelier était DANS le @media print non
fermé qui termine le dernier bloc style du head ; **lint structurel** posé
(analyse d'accolades à pile, quote/backslash par String.fromCharCode — écart
assumé : pas de tinycss2, zéro SDK). **A4** : pile mono complète.
**Accroc attrapé par version.json** : le bump de version oublié du patch
(build générait 4.127.0 pour un code modifié) — la cohérence
version.json/TOOL_VERSION est un test de livraison de fait. **Vérifié** :
662 tests | 0 échec, syntaxe 0 erreur, audit navigateur (417 éléments,
cibles 56 px, profil nettoyé). **DEV** : 4.127.1 servie, SHA-256
`a3b7ed50c4146e8a…` == dist, version.json cohérent. **PROD** : 4.126.0 —
elle attend ta phrase (4.123.0 → 4.127.1 d'un coup). Écrits :
`bilan_economique.html`, `service-worker.js`, `outils/build-coque.mjs`,
`outils/patch_41271_a.py`, `outils/mesure_atelier.py`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---
---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 104, v4.127.0 — LOT 2 :
le mode atelier ; **PROD 4.126.0** passée sur ta phrase). **Accroc** :
version.json en 404 sur la prod (liste blanche du dist sans le fichier) —
corrigé dans le build, redéployé, servi sur les deux domaines. **Le mode
atelier** : tokens de lecture + surcharge data-mode (14/16/20/24 px, cibles
56 px, boutons pleins, pastilles remplies, bordures 3:1, plus de verre),
bascule ⚒ mémorisée (défaut pointer:coarse), **Plex retiré** (A4 à
Consolas), écran de boot. **Découvert** : le parseage des 30 blocs de style
a rejeté le bloc atelier silencieusement — le CSS du mode est **injecté par
JS** (feuille dédiée posée/vidée à chaque bascule). **Vérifié** : 662 tests
| 0 échec + portes LOT 1/2 étendues, contre-regards (boot, SW, masquage),
navigateur (cibles 56 px mesurées, capture regardée, bascule réversible,
profil nettoyé). **DEV** : 4.127.0, SHA `4a1d3bc9…` == dist. **PROD** :
4.126.0 (le LOT 2 attend ta phrase). Résidu assumé : quelques libellés
9-10 px hors familles couvertes. Écrits : `bilan_economique.html`,
`service-worker.js`, `spk-shell.js`, `spk-app.css`, `outils/build-coque.mjs`,
`outils/patch_41270_a.py`, `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`,
`VERROU.md`.

---
---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 103, v4.126.0 — LOT 1 du
brief complémentaire). La vérif de version fetch **version.json** (quelques
octets, publié par le build depuis le source) au lieu du HTML complet toutes
les 60 s ; fréquence **10 min + retour d'onglet** ; **reload gardé** (pas de
saisie au focus, saveData flushé, anti-boucle < 2 par version) sinon bandeau
« Recharger » non bloquant ; **version.json en réseau d'abord dans le SW**
(trouvé au test réel : le cache-first cacherait le signal). **Vérifié** :
662 tests | 0 échec + porte « lot 1 4.126 », contre-regard (fetch HTML
réinjecté → porte), navigateur (reload spontané constaté, bandeau à
l'anti-boucle). **DEV** : 4.126.0 servie, SHA `ed95f499…` == dist,
version.json servi. **PROD : rien** — 4.125.1 (son version.json est la page
404 de surge → repli silencieux correct). Écrits : `bilan_economique.html`,
`outils/build-coque.mjs`, `build_harness.py`, `outils/patch_41260_a.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 102, v4.125.1 — le mode
Consultation verrouille de nouveau l'import ; **PROD**). Le fix de la
régression vue par Benjamin (l'item du menu Transmettre restait actif
verrouillé) + orphelins retirés + tuile active compactée + porte étendue
(contre-regard : masquage retiré → porte tombée). **Test de recette au
rendu** (consigne du Tour 100) : verrouiller → item display:none, bannière
posée, capture regardée. **DEV + PROD : 4.125.1** (phrase de Benjamin) —
curl : empreinte `4f8086b9…` == dist sur les deux domaines, SW v7, sensibles
404, rendu public vérifié. La prod saute 4.123.0 → 4.125.1. Écrits :
`bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`,
`VERROU.md`.

---
---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 101, v4.125.0 — lot 2 du
brief : la navigation se resserre). **Ouverture sur l'écran de travail** (Q11
révisé comme demandé ; Vue d'ensemble au clic ou #accueil) + anneau de focus
retiré de son ouverture (data-sans-focus) ; **boussole retirée de la fiche**
(Ctrl+K reste) ; **Transmettre en fin de barre** avec **Importer dans son
groupe « L'archive »** (boutons de barre et de rail retirés ; la porte
« lot UX 4.120 » mise à jour) ; **tuile ouverte = une ligne** (doublons
nom/statut partent) ; **ligne grise d'état vide** au lieu du grand bandeau
(bug latent : la 4.114 calculait realise/reste sans les renvoyer — exposés).
**Vérifié** : 662 tests | 0 échec + porte « lot 4.125 » (7 points),
contre-regards tombés (dont le déplacement raté de Transmettre, vu en vrai),
navigateur (ouverture sans panel, ordre de barre mesuré, import au menu,
ligne grise prouvée, profil nettoyé), captures avant/après fournies.
**DEV** : 4.125.0 servie, SHA `db8bf532…` == dist. **PROD : rien** — 4.123.0.
Reste : mobile 467 px (4.127), couleurs/disques (4.126), aide, briques Hermes.
Écrits : `bilan_economique.html`, `spk-shell.js`, `spk-app.css`,
`build_harness.py`, `outils/patch_41250_a/b/c.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---
---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 100, v4.124.1 — la
réparation de Benjamin adoptée, le garde-fou structurel posé). La 4.124.0
était cassée par MON patch P0-2 (`.reprise-bandeau{` ouvert sans
déclarations — habillage avalé, zéro erreur console, vu au rendu par la
revue, pas par mes tests). Réparation adoptée telle quelle (diff = 1 ligne,
ma source == sa copie octet pour octet) ; porte « équilibre css » : chaque
bloc style doit avoir ses accolades fermées + la règle complète gardée par
son nom ; contre-regard = le bug exact rejoué → porte nomme « 1061 ouvrantes,
1060 fermantes ». **La consigne de Benjamin est au protocole** : ne rien
livrer sans la capture de l'écran principal + les 3 contrôles de rendu.
Vérifié au navigateur avec capture : Vue d'ensemble complète, + Scénario
stylé, tuile bordée 2,67px, bannière absente, innerText sans /*, profil
nettoyé. **DEV** : 4.124.1 servie, SHA `25dcfe81…` == dist. **PROD : rien**
— 4.123.0. Reste : trou de grille P0-3, mobile 467 px, lot P1 (4.125-4.127),
briques Hermes, Q11. Écrits : `bilan_economique.html`, `build_harness.py`,
`outils/patch_41241_a/b.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 99, v4.124.0 — les quatre
P0 du brief de revue externe). P0-1 commentaire rendu en texte sur les tuiles
→ retiré + **machine à états** du harnais qui garde la règle « jamais de
commentaire dans un template » (3 itérations : global faux → accolades naïves
fausses → pile d'états juste, contre-regard tombé) ; P0-2 Bienvenue →
**bandeau non bloquant fermable une fois** (l'ouverture auto Q11 de Benjamin
NON changée — à sa voix) ; P0-3 le vert devient **`.is-ok` explicite** (seuil
atteint) et les 3 précisions descendent en ligne secondaire grise ; P0-4
Atelier/Tableau masqués du rail (clics internes vérifiés au navigateur).
**Vérifié** : 662 tests | 0 échec, contre-regards A/B/C/D tombés, navigateur
(innerText sans /*, rail 3 écrans, bandeau non modal, profil nettoyé).
**DEV** : 4.124.0 servie, SHA `f63bbab7…` == dist. **PROD : rien** — 4.123.0.
Reste : P1/P2 du brief (4.125-4.127), briques Hermes en file, Q11 à trancher.
Écrits : `bilan_economique.html`, `build_harness.py`,
`outils/patch_41240_a/b/c.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Hermes le 28/10/2026, nuit** (acte II du débroussaillage,
v4.121.0 + 4.122.0). **Fiche scénario en niveaux** : trois chiffres clés ouvrent la
bande (verdict, coût/pièce, validation) ; la tuile ouverte redevient de la
navigation ; badges doublons (« En cours », « x/y essais conformes » du résumé)
supprimés ; config et rebut repliés par défaut. **Fusion Accueil/Atelier/Tableau**
en une entrée « Vue d'ensemble » (rail 3→1), bascule dans l'écran, exclusivité
préservée. Porte harnais rail 4.100.4 mise à niveau, **2 contre-regards, 2
détectés**. États vides CPP constatés déjà conformes. **Vérifié** : 662 tests | 0
échec sur le fichier de déploiement, VERDICT tout vert ; dev servie 4.122.0, md5
identique au dist ; prod 4.120.0 re-vérifiée inchangée. **PROD : rien** — phrase de
Benjamin attendue. Acte III (bouton « Transmettre » unique) reste en file.

✅ **Verrou libéré par Hermes le 28/10/2026, nuit (2)** (acte III du débroussaillage,
v4.123.0). **Un bouton « Transmettre »** en tête de barre (Rapport de validation,
Générer le PDF, Exporter .json, Export CSV — ids inchangés) ; le menu ••• se
recentre sur Consulter + Gérer. Trois défauts de rendu attrapés à l'écran (menu hors
écran, wrap 31 px, bloc vert sans libellé) et corrigés. **Vérifié** : 662 tests | 0
échec, VERDICT tout vert ; dev servie 4.123.0, md5 identique au dist ; prod
4.120.0 re-vérifiée inchangée. **PROD : rien** — phrase de Benjamin attendue. Le
débroussaillage acté par la revue Claude est terminé (actes I, II, III).

---

✅ **Verrou libéré par Z Code le 28/10/2026** (Tour 98, v4.120.0 — lot
confort). **⤓ Imprimer réparé** (mort depuis le dé-branding 4.104 : printGo
lisait le logo retiré de l'en-tête, TypeError avant window.print() — le logo
A4 embarqué est la source directe) ; **anti-flash au démarrage** (body caché
jusqu'au premier rendu, filet à 5 s — posé après loadAll, PAS en script de
head : la porte css impression découpe le head au premier script) ;
**⤒ Importer au pied du rail** (même file picker que la barre d'outils).
**Vérifié** : 662 tests | 0 échec, contre-regards A/B/C tombés, navigateur
sur dist (bouton rail visible, printGo rejoué sans exception, data-pret
posé), profil nettoyé. **DEV** : 4.120.0 servie. **PROD : rien** — phrase de
Benjamin attendue. Le raccourci Matis : expliqué (lecteur du classeur hebdo,
redondant avec le Plan), retrait proposé — décision Benjamin. Écrits :
`bilan_economique.html`, `spk-shell.js`, `spk-app.css`, `build_harness.py`,
`outils/patch_41200_a/b/c/d.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Hermes le 26/10/2026, nuit (7)** — Base Matis embarquée
4.119.0 (« go » de Benjamin). `const BASE_MATIS` : 16 articles du Pareto MAJ
vérifiés (total empilé = 1 004 671 €, la base actée), décomptes par ligne des
gros posts (Z000 546 265 = 159 040 €/an toutes lignes), volumes des suivis,
réel-vs-théorique. Colonne **Réel Matis** dans le tableau du simulateur avec
détail au survol + note « l'écart est l'argument ». Porte dernierLotGate
étendue (4 checks). 662/0 ×2, syntaxe 5/5. **DEV** md5 `fbf78838…` servi,
TOOL_VERSION 4.119.0. PROD : 4.118.0 — le push attend le mot de Benjamin.
Diagnostic acté (ne pas perdre) : écart Z000 546 265 = WEISSER hors périmètre
87 920 € (55 %) + volumes réels > saisis (356x26 : 6 781/sem vs 2 864/sem
implicites) + DDV non tenue (suivis Matis : +63 % EMAG, ×4,6 HESSAPP).
Écrits : `bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`,
`VERROU.md`.

✅ **Verrou libéré par Hermes le 26/10/2026, nuit (6)** — retours de terrain
4.118.0 (Benjamin) : champ « Logement » renommé **« Correcteur (D1, D2…) »**
(c'est le N° de correcteur que remplissent les excels Matis — libellé seul,
modèle intact), croix de suppression visible (26 px, bordée, rouge survol),
confirmation de suppression nominative (« logement « D1 » de l'outil T546 ? »),
**🗑 Supprimer l'outil** dans le bandeau de chaque outil (confirmation
nominative, prélèvements ancrés comptés, instantané filet 30 j avant
mutation). 662/0 ×2, syntaxe 5/5. **DEV** md5 `186f6743…`, TOOL_VERSION
4.118.0 servi. PROD : 4.117.0 — le push attend le mot de Benjamin.
Écrits : `bilan_economique.html`, `CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 26/10/2026, nuit (5)** — lot 4.117.0 livré et
**PROD déployée à la demande explicite de Benjamin** (« passe en prod »).
Livré : boussole « Première Lecture » en tête d'accueil (les cinq questions,
chacune saute vers sa réponse), Ctrl+K, « Ce qui attend » (âges dans La
campagne), « ⇄ Décliner ce gagnant » (copie à ids neufs, aucun historique
partagé), « ⤺ Actions récentes » (filet 30 j, instantané AVANT mutation,
restauration en un clic). Porte `dernierLotGate`. 662/0 ×2, syntaxe 5/5.

⚠️ **Incident du lot — la leçon la plus importante de la soirée.** Une ancre
de bouton a fait doublé un appel (`matisPairesDoublons(matisPairesDoublons(…))`)
— **invisible sur les données d'exemple** (la fonction renvoie vide sans
planter), **fatal sur les vraies données** (l'accueil aurait cassé dès qu'une
paire de doublons existerait). Attrapé par le node --check de protocole.
Leçons : (1) une vérification de syntaxe ne voit pas les erreurs sémantiques —
pour les insertions dans les templates, relire la ligne générée, pas seulement
compiler ; (2) une salve d'apostrophes a ensuite dû être réparée itérativement
contre node --check — ne JAMAIS faire de remplacement global d'échappements
(`\'` → `'`) sur ce fichier : chaque chaîne JS single-quote doit être
réparée individuellement, vérifiée par le compilateur.

**DEV** md5 `5065c65a…` ; **PROD** md5 `5065c65a…`, TOOL_VERSION 4.117.0 servi
sur les deux. Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 26/10/2026, nuit (4)** — brique B 4.116.0,
spec `DEMANDE_BANDEAU_CPP_ET_FUSION_OUTILS_A_ZCODE.md` intégralement tenue.
Détection par porte+position (bouton sur la fiche scénario), porteur
d'histoire (score : prélèvements ancrés > plan PDF > pièces) garde son id et
ceux de ses logements, prévision pure, conflits champ par champ en radio
(« manuel / Classeur »), application bloquée tant qu'une radio pende, PDF non
retenu téléchargeable dans le bilan, numéro ambigu et double porteur d'histoire
jamais fusionnés, contrôle des prélèvements AVANT mutation. `fusionGate` + 9
tests in-suite (B.6). Contre-regard : amputation réelle → porte tombée.
**Piège du contre-regard** : une casse par préfixe (renommer
`matisPairesDoublons` en `matisPairesDoublonsX`) ne peut PAS tomber une porte
à `indexOf` — amputer vraiment, pas renommer. **662/0 ×2, syntaxe 5/5.**
**DEV** : md5 `c893feff…` identique, TOOL_VERSION 4.116.0 servi. PROD : 4.113.0.
Reste du chantier : la navigation « Première Lecture » (5 questions), les
améliorations actées (âges généralisés, décliner un gagnant, Ctrl+K, filet
undo 30 j). Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 26/10/2026, nuit (3)** — fix 4.115.1, remonté
par Benjamin (copie d'écran : cascade sans barres). Cause : le CSS de la
cascade ET de la table comparative v4.30 ne vivait que dans le template JS du
rapport de validation — la page n'en a jamais eu de copie depuis la v4.31
(a11ae10). Diagnostic : 14 blocs `<style>` dans le fichier, 10 dans le DOM.
Fix : copie page des 33 règles entre le dernier vrai `</style>` et le premier
`<script>` + porte `cascadeGate` (chaque règle colorée doit exister 2× :
template + page ; contre-regard par amputation → porte tombée).

⚠️ **Deux leçons de structure, à ne pas oublier :**
1. **Le document n'a pas de `<head>`/`<body>` explicites.** Le navigateur les
   déduit ; le premier `</head><body>` du fichier est celui du TEMPLATE du
   rapport, dans une chaîne JS. Pour du CSS page : insérer entre le dernier
   vrai `</style>` (fin bloc 9, avant le premier `<script>`) — jamais sur une
   ancre `</head>`.
2. **Le harnais doit être régénéré APRÈS le dernier octet écrit et lancé au
   moins 2× avant tout déploiement** : un « 1 échec » transient a été vu une
   fois (course régénération/écriture), jamais revu en 3 relances.

Écrits : `bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`,
`VERROU.md`. **DEV** : md5 `c98baec7…` identique, TOOL_VERSION 4.115.1 servi.
PROD : 4.113.0 — reste à la main de Benjamin.

✅ **Verrou libéré par Hermes le 26/10/2026, nuit (2)** — brique C 4.115.0.
« La campagne » : panneau timeline (menu ••• + résumé en tête de Synthèse),
jalons datés (essais/validations/séries), gains €/an actés par passage en
série, courbe SVG cumulée (séries datées SEULEMENT, §3.4), jalons sans date
affichés comme tels et poussés en file « à compléter » avec les coûts
incomplets (prix/charnière/arêtes) et les OP non chiffrables. Porte
`campagneGate` — deux désaccords attrapés par la porte elle-même à
l'insertion, corrigés avant livraison. 652/0, syntaxe 5/5, rendu vérifié
headless. **DEV** : md5 `fbf5b53f…` identique, TOOL_VERSION 4.115.0 servi.
Pièges du tour : fins de ligne MIXTES dans bilan_economique.html (une zone
CRLF, une zone LF — les ancres multi-lignes doivent être vérifiées par octets,
pas supposées) et le harnais est un template python à `
` littéraux (l'ancre
d'insertion de porte se cherche en octets). Reste : brique B (fusion Classeur
Matis) — spec prête dans `DEMANDE_BANDEAU_CPP_ET_FUSION_OUTILS_A_ZCODE.md`.
Écrits : `bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`,
`VERROU.md`.

✅ **Verrou libéré par Hermes le 26/10/2026, nuit** (brique A 4.114.0, prise de
main actée par Benjamin). Le bandeau « Coût pièce » lit désormais la production
du jour (série si existe, sinon ★), trois phrases séparées (aujourd'hui /
réalisé / reste possible), l'étoile jamais re-basée automatiquement, abandonnés
filtrés du « meilleur » (bug latent), vocabulaire 5 mots, détail scénarios au
clic puce OP (panel + délégation). Porte `bandeauCPPGate` + contre-regard
casse/restaure par Hermes (652/0 avant et après). Piège du tour : label de porte
avec apostrophes/backslash → h451.js en SyntaxError, réparé en réécrivant le
libellé sans échappement ; et build coque invoqué par erreur avec python (le
vrai runner est `node outils/build-coque.mjs`). **DEV vérifiée** : md5
`adf497c4…` identique octet pour octet, TOOL_VERSION 4.114.0 servi. PROD :
4.113.0 (déploiement Benjamin du jour), reste à sa discrétion. Écrits :
`bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`, `VERROU.md`.
---

| **Auteur** | **Z Code** |
| **Pris le** | 25/10/2026, Tour 92 |
| **Écrit dans** | `spk-app.css` (palette coque → brand guide), `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md` |
| **Version visée** | 4.109.1 |
| **Sujet** | Retour Benjamin : « trop de noir » — la coque (graphite + orange de l'auto-designer) reprend la palette du brand guide SPK : fond clair, bleu #1B5EA6 en identité, rouge #E2001A en alerte, noir en texte seulement. |

---

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

---

✅ **Verrou libéré par Z Code le 26/10/2026, soir** (Tour 97, v4.113.0 — le
bug OP40 vu par Benjamin en prod). Les logements SANS données (Plaquette/D1/
D2 de la migration 4.93) étaient appariés par nom : paires mortes, faux
« ajouté », et la vraie sortie T543·D1 (9,8 k€/an — l'incident exact du
26/10) masquée. Fix : seuls les porteurs de coût s'apparient, secours par
données identiques tracé, porteurs restants nommés en sortie. **Vérifié** :
652 tests | 0 échec (+3, dont le cas OP40 réel en fixture), contre-regard
(filtre retiré → tests tombés), navigateur rev433 (ligne « dont sorties :
−9,8 k€/an (T543 · D1) » affichée, zéro faux ajout, profil nettoyé).
**DEV** : 4.113.0 servie, SHA `7e0a083f…` == dist. **PROD : rien** — 4.112.1,
la phrase de Benjamin attendue. Écrits : `bilan_economique.html`,
`outils/patch_41130_a/b.py`, `build_harness.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 26/10/2026, après-midi** (Tour 96, v4.112.1 —
le correctif TDZ trouvé par la répétition générale, puis la PROD). Quatre
états déclarés après l'appel `loadAll()` (posés 4.90/4.101.1) levaient une
ReferenceError avalée par le catch silencieux : **les données réelles
retombaient sur l'exemple, et la première saisie aurait écrasé le
localStorage**. Déclarations montées avant l'appel + test de charge + porte
structurelle « toute globale de loadAll se déclare avant son appel » (la
première porte était AVEUGLE — regex dynamique fondue par l'échappement
Python→JS, le piège des Tours 82/4.100 repris ; réécrite en TEXTE BRUT, la
règle « regex dynamique bannie du harnais » est au journal). **Répétition
générale** : profil 4.97.2 + état réel rev433 enrichi (PARETO, catalogue,
livraison) → swap → bascule observée, tout chargé, SW v1→v7, localStorage
intact. **Vérifié** : 649 tests | 0 échec, contre-regards vus tomber.
**DEV** : 4.112.1 servie. **PROD : 4.112.1** (ordre de Benjamin) — empreinte
`08a71a1f…` == dist, SW v7, coque 200, sensibles 404, rendu public vérifié.
Écrits : `bilan_economique.html`, `build_harness.py`,
`outils/patch_41121.py`, `outils/patch_41121_b.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 26/10/2026, soir** (Tour 95, v4.112.0 — le
complément du verdict par outil, décisions Benjamin du soir). **Secours
intra-outil tracé** (compteurs égaux, jamais entre outils ; compteurs
inégaux = déséquilibre visible) — sur rev433, zéro sortie fantôme, les
renommages s'apparient par secours. **Mention « dont N poste(s) sorti(s) »**
sur le badge du groupe (le chiffré reste en « non réparti », vérifié au
centime). **8 polices mortes retirées** (fichiers, SW, CACHE v6→v7, build —
avec purge de dist/fonts désormais intégrée au build : le premier
déploiement était reparti avec les anciennes, vu et corrigé dans la foulée).
**Vérifié** : 648 tests | 0 échec (+6), contre-regards A/B/C tombés (et une
porte fausse-au-vert resserrée sur les blocs de rendu), navigateur rev433
(profil nettoyé), curl : 404 polices, SW v7, empreinte `655b9cec…` == dist.
**PROD : rien** — 4.97.2. Écrits : `bilan_economique.html`,
`service-worker.js`, `fonts/` (retraits), `outils/build-coque.mjs`,
`outils/patch_41120_a/b/c.py`, `build_harness.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 26/10/2026** (Tour 94, v4.111.0 — le verdict
par outil, demande Hermes/Benjamin du 26/10). L'appariement va par NUMÉRO
d'outil (plus jamais par position), les tuiles portent cycle Vc·f en %,
les deux leviers séparés (technique toujours, productivité si chrono
complet, groupes au max), les sorties/ajouts nommés, le dégradé rouge→vert
sur le gain €/an, la ligne « dont sorties du scénario » dans le verdict et
la réconciliation tuiles + sorties − ajouts + non réparti = verdict.
**Vérifié** : 642 tests | 0 échec (+8), syntaxe 0 erreur, contre-regards
doubles (2 régressions, 2 portes tombées, restauration vérifiée), navigateur
sur le cas réel rev433 SL500/OP40 (sorties 9,5 k€/an nommées, réconciliation
exacte, profil embarqué nettoyé). **DEV** : 4.111.0 servie, SHA `e0001dd4…`
identique au `dist/`. **PROD : rien** — 4.97.2. Écrits :
`bilan_economique.html`, `build_harness.py`, `outils/patch_41110_a/b/c/d/e.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 26/10/2026** (Tour 93, v4.110.0 — brique B :
le badge de codification sur les fiches scénario). Le chantier D → A → C → B
est **complet**. `badgeCodifScenario(sc)` (pure) dérive le badge — codifié /
attente X j / non demandée — affiché dans « Scénarios en validation » à côté
de l'état ; base excel et scénario sans article : aucun badge (hors exigence).
**Accroc** : la porte « coque 4.100 » du harnais était périmée (cherchait
Barlow Condensed, retirée au Tour 91) — recalée sur le brand guide (Open Sans
Condensed présente, Barlow bannie). **Vérifié** : 634 tests | 0 échec (+5),
syntaxe 0 erreur, 2 régressions injectées → 2 portes tombées, restauration
vérifiée, navigateur (pilules 117 j et « codifié » vues, profil embarqué
nettoyé). **DEV** : 4.110.0 servie, SHA `c3cdc863…` identique au `dist/`.
**PROD : rien** — 4.97.2. Écrits : `bilan_economique.html`,
`build_harness.py`, `outils/patch_41100_a/b/c.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 25/10/2026** (Tour 92, v4.109.1 — « trop
de noir » : la palette de la coque passe au brand guide). Cause :
l'auto-designer avait remappé --blue sur du graphite — tous les accents
de l'app rendaient noirs. Re-mappage : --blue → #1B5EA6, signal orange →
bleu, head/fill → bleu à texte blanc, fond crème → gris neutre surfaces
blanches, rail graphite → dégradé bleu SPK, rouge → #E2001A, nuit à
accent bleu lisible. Le noir ne reste que dans le texte. **Vérifié** :
capture navigateur sur le DEV servi (rail bleu, bandeau bleu, filigrane
E1). **DEV** : 4.109.1, SHA `a1b583e0…` identique au `dist/`. **PROD :
rien** — 4.97.2.

---

✅ **Verrou libéré par Z Code le 25/10/2026** (Tour 91, v4.109.0 — retour
Benjamin : « remets le filigrane en fond… et reprends les couleurs et
polices du design system SPK »). **Le filigrane** : la coque le tuait
(`body { background-image: none !important }`) — règle passée en
`background-color`, la teinte et le code de ligne (E1…) traversent la
coque ; texte du filigrane en Open Sans Condensed. **Les polices** :
brand guide SPK — --font-disp → Open Sans Condensed (titres, chiffres),
--font-body → Open Sans (corps, UI), embarquées en base64 (police
variable, 2 faces ~85 Ko, zéro réseau) ; **et la coque elle-même** — ses
:root redéfinissaient les tokens en Barlow Condensed / Public Sans, les
tokens s'alignent et ses @font-face locaux sont retirés. **Les couleurs
étaient déjà celles du guide** (portes d'identité inchangées et vertes).
**Vérifié** : 629 tests | 0 échec (portes suivies), calculé sur le DEV
servi : filigrane E1 posé, corps « Open Sans », titres « Open Sans
Condensed ». **DEV** : 4.109.0, SHA `30c2d37b…` identique au `dist/`.
**PROD : rien** — 4.97.2.

---

✅ **Verrou libéré par Z Code le 24/10/2026** (Tour 90, v4.108.0 — brique C :
« Où investir — les priorités », posée dans le tableau de bord du Plan).
**Deux axes jamais fondus en un score** (potentiel : dépense + gain €/an ;
facilité : prochaine étape + freins) et **cinq paniers** : validés pas encore
en série, essai positif à compléter (protocole 5× compté), dépense forte
jamais travaillée, données insuffisantes (manques nommés), travaillé et
arrêté — motif (SN60, Hermes Q3). **Univers plaquettes** (Hermes Q3) :
les articles de la base 2025 sans lien outillage sortent sur une ligne
explicite. Codification en attente = frein affiché sur l'axe facilité avec
son âge (57 jours sur le cas LKT640, vérifié navigateur). **Accroc** : les
fautés sont invisibles dans recap.postes (gainPoste les exclut du meilleur
depuis 4.101) — détection déplacée sur la liste des candidats. Une machine
déclarée sans scénario n'est pas une priorité. **Vérifié** : 629 tests |
0 échec (+7), navigateur sur le DEV servi (données de test nettoyées).
**DEV** : 4.108.0, SHA `5c22ed63…` identique au `dist/`. **PROD : rien** —
4.97.2. Reste au chantier : l'UI B, puis le contre-regard croisé A/C.

---

✅ **Verrou libéré par Z Code le 24/10/2026** (Tour 89, v4.107.0 — brique A :
la décomposition des leviers). Deux colonnes nouvelles dans « Scénarios en
validation » : **Levier vie** (+X % de vie effective → gain €/an) et
**Levier prix** (−Y % de prix moyen → gain €/an), info-bulles avec
l'interaction vie×prix et le coût plaquette/pièce de chaque côté
(affinage ChatGPT), note de lecture. Méthode (les cinq conditions
d'Hermes) : poste plaquettes seul ; enveloppe = le périmètre commun de
bilanAnnuel (le gain total reste sourcé de gainPoste, asserté au centime) ;
hors course exclus en amont ; base sans prix/DDV = « — » ;
`gainPoste` porte désormais `perimetrePartiel` — badge « gain outillage —
levier cycle non chiffré » quand le temps machine est exclu. Décomposition
sur les TOTAUX (p̄ × q), jamais un appariement logement à logement —
l'identité vie + prix − interaction = plaquettes tient avec des outils
différents (asserts dédiés). **Vérifié** : 622 tests | 0 échec (+6),
syntaxe 0 erreur, navigateur sur le DEV servi (cas +30 % vie / −25 % prix :
+115 €, +125 €, total +212 € — données de test nettoyées du poste).
**DEV** : 4.107.0, SHA `a4b39e6d…` identique au `dist/`. **PROD : rien** —
4.97.2. Prochain : C (la matrice « où investir »), puis l'UI B.

---

✅ **Verrou libéré par Z Code le 23/10/2026** (Tour 88, v4.106.0 — le chantier
commercial validé à trois démarre, ordre D → A → C → B). **Livré : D (le
dossier de visite)** — panneau depuis l'accueil et le Plan : gains en course
**qualifiés** (« cycle standard » / « via BADP » + âge d'attente, source
unique planRecapGains), codification en attente chez Matis avec l'âge en
jours (l'argument LKT640), essais de la fenêtre (réutilise
planChronologieEssais), scénarios validés/en série, sujets bloqués avec
motifs, projets ouverts **tous âges** (anciens marqués). **Couche B posée** :
deux dates de codification par article du catalogue (demandée / accordée),
dérivation par scénario (tous les articles, sinon l'écran dit lequel manque ;
« base excel » hors exigence). `derniereVisite` persistée, préremplie à la
dernière livraison, geste « ✓ Visite faite » ; import : la plus récente des
deux. Aucun K ni P dans le dossier. **Vérifié** : 616 tests | 0 échec (+10),
syntaxe 0 erreur, navigateur sur le DEV servi (BADP, 114 jours d'attente,
projet ancien marqué — données de test nettoyées du poste après vérif).
**DEV** : 4.106.0, SHA `9ec545a4…` identique au `dist/`. **PROD : rien** —
4.97.2. Prochain tour : A (décomposition vie/prix), puis C, puis l'UI B.

---

✅ **Verrou libéré par Z Code le 22/10/2026** (Tour 87, v4.105.0 — nom SPK
retiré de l'en-tête (titre, eyebrow, pied — le monde A4 reste brandé) ;
graphique du Plan pleine largeur (la grille 2 colonnes le réduisait de
moitié) ; section « Scénarios en validation — le gain par poste » en tête
du tableau de bord, états réels + économies €/an, cumuls étiquetés jamais
mélangés). **Vérifié** : 606/0, navigateur sur le DEV servi (captures).
**DEV** : 4.105.0, SHA `21c396e8…` identique au `dist/`. **PROD : rien** —
4.97.2.

---

✅ **Verrou libéré par Z Code le 22/10/2026** (Tour 86, v4.104.0 — sept
retours du terrain : graphique lisible + simulation dans le graphique,
consommations persistantes à l'import, pictogramme légende morte retiré,
logo SPK sorti de l'outil (gardé pour les rapports A4 via `LOGO_SPK_SRC`),
contrôles de consommation en tête du Plan, onglet Tableau qui se rouvre
(coque : fermeture des panneaux dérivés). **Vérifié** : 606/0, navigateur
sur le DEV servi. **DEV** : 4.104.0, SHA `1dbe45a0…` identique au `dist/`.
**PROD : rien** — 4.97.2.

---

✅ **Verrou libéré par Z Code le 21/10/2026, soir** (Tour 85, v4.103.0 — la
mission du verrou est remplie). **Validé sans correction** : ordre de
résolution de l'auteur (`redigePar > operateur > equipe > session`, conforme),
porte hors-suite 4.102 (5 contrôles réels, « gains non mélangés » posé sans
regex), tableau de bord live rendu au navigateur. **Corrigé : la divergence
prixSpk** — la décision Benjamin du 20/10 vit désormais dans le SOURCE
(`planReglages`, suggestion KY3500 sans prix, repli `ciblePrix`, contrôle UI,
listener, placeholder, test 4.86) ; `build-coque.mjs` ne détourne plus rien,
son garde-fou devient une porte de principe (1 occurrence de `prixSpk` =
build en échec) et une porte harnais équivalente verrouille la source entre
deux builds. **Vérifié** : 606/0 (porte « prix SPK défaut » nouvelle),
syntaxe 0 erreur, build 5 transformations / garde vert, navigateur (plus de
contrôle ni libellé « Prix SPK défaut », `planReglages = {relSpk:100}`,
levier prix live prix ÷2 → −50 %). **DEV** : 4.103.0 servie, SHA
`6e80a8ce…` identique au `dist/`, zéro `prixSpk` dans le fichier servi.
**PROD : rien** — 4.97.2.

---

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

---

✅ **Verrou libéré par Hermes le 21/10/2026, soir** (4.102.0 — le Plan de
conversion devient un tableau de bord live). La case « PRIX CONFIRME » était
**morte** (aucun listener : le total ne changeait pas) — câblée et renommée
« Prix validé ». Ajouts : bandeau gains **actés** / **possibles** (essais
positifs) / **écart**, jamais additionnés (constitution §3.4) ; vues graphiques
SVG (Pareto conso, base face à cible) avec le tableau des données sous
chacune ; chronologie des essais depuis le premier (frise + tableau + « qui a
fait quoi »). Source unique : `gainLigne`/`gainPoste`. **606/0** (13 portes
nouvelles) ; **contre-regard en série : 3 régressions vues**, restauration
SHA-256 identique. La porte « les gains ne sont pas mélangés » a dû être
**réécrite sans regex** (le `[^\n]` de la chaîne Python non-raw devenait un
vrai saut de ligne — elle passait au vert sans rien voir). **DEV : 4.102.0
servie, empreinte identique au `dist/` local (1 641 678 o). PROD : rien** —
4.97.2.

---

✅ **Verrou libéré par Hermes le 21/10/2026, soir** (4.101.1 — la Synthèse
réapparaît ; les consommations restent en mémoire). Diagnostic : le voile modal
(`panelBackdrop`, z 40) laissé ouvert par `ouvrirPanneau` recouvrait la Synthèse
(bloc en flux, sans z-index) et le premier clic sur le voile refermait tout —
le tour 81 avait réglé l'empilement des écrans, pas ce voile. Handler corrigé
(fermer → rouvrir), transformation « scrollIntoView » retirée de
`outils/build-coque.mjs` (son ancre n'existait plus : le build échouait).
`consoReelle` / `planSource` / `consoSemaines` / `planReglages` voyagent
désormais dans le payload format 8 (loadAll + import : l'entrant gagne s'il les
porte) — plus de relecture de classeurs à chaque ouverture.
**Incident assumé** : un premier déploiement est parti avec le `dist/` PÉRIMÉ
(4.101.0) pendant que le build échouait — corrigé, reconstruit, redéployé,
vérifié curl : **4.101.1 servie, empreinte identique au `dist/` local**
(1 610 755 o). 593/0 (2 portes nouvelles). **PROD : rien** — 4.97.2.
Écrits : `bilan_economique.html`, `outils/build-coque.mjs`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 21/10/2026** (Tour 82, v4.101.0 — libération
à la demande de Benjamin, vérification du tour d'Hermes). Le bilan d'Hermes
a été **vérifié point par point, rien pris sur parole** : 591/0 rejoués sur
la source, syntaxe 0 erreur, `scenarioEchec` + portes FAILED présentes,
flèches numériques hors atelier présentes, Tour 82 dans `ECHANGES.md`,
`dist/` frais (construit après la dernière édition source). **Le curl non
rejoué a été rejoué** : DEV sert 4.101.0, fichier servi **identique octet
pour octet au `dist/` local** (SHA-256 `651a1a61…`). **PROD : rien** —
4.97.2. Écrits du tour : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`, `scratch_main.js` (supprimé).

---

✅ **Verrou libéré par Hermes le 21/10/2026, matin** (4.100.4 — les onglets du
rail se remplacent au lieu de s'empiler). Benjamin : « les onglets tableau et
synthese ne fonctionnent pas ». Reproduction avec captures : les écrans du rail
**s'empilaient** — la Synthèse, bloc en flux de l'app d'avant la coque (aucun
z-index), s'ouvrait **derrière** l'Accueil ou le Tableau de bord restés ouverts
(z 80). Le shell referme maintenant les surfaces voisines en phase de capture
(la logique de l'app n'est pas réécrite), marque l'onglet de la Synthèse, lui
donne un Retour fonctionnel et l'affichage depuis le haut. Matrice complète
vérifiée en navigateur (8 chemins, un seul écran à la fois, zéro erreur JS).
Porte `rail exclusif 4.100.4` (5 points), 3/3 contre-regards détectés.
**DEV** : 4.100.4 servie, md5 `288e57aa…` (HTML) et `22f76752…` (shell)
identiques au `dist/` local. **PROD : rien** — 4.97.2.| **Auteur** | **Hermes** |
| **Pris le** | 21/10/2026, matin |
| **Écrit dans** | `spk-shell.js` (exclusivité du rail), `bilan_economique.html` (version), `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md` |
| **Version visée** | 4.100.4 |
| **Sujet** | Les onglets du rail se remplacent au lieu de s'empiler. |

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

✅ **Verrou libéré par Hermes le 20/10/2026, nuit** (4.100.3 — l'import prévient
avant de retirer des essais). Diagnostic par reproduction avec les vrais
fichiers du 13/10 : le code d'import et la fusion sont **sains** (rev431
importe → 7 essais, PCI 5 / OP 40 compris). La perte vient du geste :
plusieurs JSON importés à la suite avec **« Remplacer tout »** (le bouton par
défaut) ne laissent que le dernier. Deux pièges aggravants : la **révision ne
dit pas quel fichier est le plus complet** (rev432 > rev431 en numéro, mais
moins d'essais), et **le transfert de l'essai PCI 5 / OP 40 vers
« Classeur Matis » était délibéré** (Benjamin, confirmé le 21/10 — pas une
perte ; `rev431` reste le fichier de
référence). Correctif : l'écran d'import compare le **nombre d'essais** reçu et
local et affiche l'écart avant les boutons. Porte `import 4.100.3` (3 points),
contre-regards détectés. **DEV** : 4.100.3 servie, md5 `7a7c8119…`. **PROD :
rien** — 4.97.2.| **Auteur** | **Hermes** |
| **Pris le** | 20/10/2026, soir (~23:55) |
| **Écrit dans** | `bilan_economique.html` (écran d'import, version), `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md` |
| **Version visée** | 4.100.3 |
| **Sujet** | L'écran d'import prévient quand le fichier reçu porte moins d'essais que les données locales. |

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

✅ **Verrou libéré par Hermes le 20/10/2026, soir (5)** (4.100.2 — la mise à
jour à chaud : un correctif ne peut plus rester invisible en cache).
`spk-shell.js` passe en **réseau d'abord** (comme le HTML et le CSS) ; le
service worker s'enregistre avec `updateViaCache: "none"`, met chaque entrée
en cache séparément (`addAll` est tout ou rien : une police manquante
empêchait le nouveau SW de prendre la main), signale sa prise de main aux
pages ouvertes, et la page compare la version qu'elle a chargée à celle qui
est servie : si elles diffèrent, les caches sont purgés et la page se
recharge. Porte `maj a chaud 4.100.2` (8 points), **8 contre-regards, 8
détectés**. **Vérifié sur un profil « déjà visité »** : le cache est passé de
`v5`/`v6` à la bonne version **seul**, sans rechargement manuel, et le bouton
**Retour** reste affiché avec un dialogue ouvert sur le Plan. **DEV** :
4.100.2 servie, md5 `3162a60a…`. **PROD : rien** — 4.97.2, md5 `fe652969…`.| **Auteur** | **Hermes** |
| **Pris le** | 20/10/2026, soir (~22:40) |
| **Écrit dans** | `service-worker.js`, `bilan_economique.html` (version + enregistrement SW), `CHANGELOG.md`, `ECHANGES.md` |
| **Version visée** | 4.100.2 |
| **Sujet** | Mise à jour à chaud : le shell est servi en réseau d'abord, le cache ne peut plus retenir un correctif, et la page se recharge seule si elle est en retard. |

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

✅ **Verrou libéré par Hermes le 20/10/2026, soir (4)** (4.100.1 — le bouton
Retour ne disparaît plus sous un dialogue). Correction dans `spk-shell.js` : un
dialogue, une recherche ou l'annotation d'une photo se posent **par-dessus** un
espace de travail, ils ne le remplacent pas ; seuls les vrais petits panneaux
(Options, Import, Nouveau projet…) le remplacent. Vérifié par la mesure :
Plan + dialogue → **retour visible** ; Plan + Options → retour masqué (comme
avant). Porte `bouton retour 4.100.1` (3 points), 3 contre-regards, 3
détectés. **DEV** : 4.100.1 servie, md5 `6fc1c769…`, comportement vérifié
depuis l'URL publique. **PROD : rien** — 4.97.2, md5 `fe652969…`.| **Auteur** | **Hermes** |
| **Pris le** | 20/10/2026, soir (~21:50) |
| **Écrit dans** | `spk-shell.js`, `bilan_economique.html` (version), `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md` |
| **Version visée** | 4.100.1 |
| **Sujet** | Le bouton Retour ne disparaît plus quand un dialogue se pose par-dessus un espace de travail. |

| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

✅ **Verrou libéré par Hermes le 20/10/2026, soir (3)** (4.100.0 — la coque
est dans le repo git ; **DEV déployé**, PAS de prod).
Option A (Benjamin) : la coque de navigation du jour est portée dans le repo
git. `spk-app.css` + `spk-shell.js` + les 8 polices locales, assemblés au
déploiement par `outils/build-coque.mjs` dans `dist/` — le monolithe versionné
reste le logiciel métier **seul** (un tour de Z Code ne doit pas hériter d'un
diff de 1,5 Mo). Le build est **idempotent** et **échoue bruyamment** si une
ancre manque. `spk-shell.js` est identique au bit près à celui de l'auto-designer.

**Le défaut trouvé au passage : le rail était invisible.** Les écrans plein
écran (`z-index: 80 !important`, `inset: 0`) passaient **au-dessus** du rail
(60) et le recouvraient entièrement : il était dans le DOM, mesuré à 248 px,
avec son fond graphite appliqué — et invisible à l'écran. Rail remonté en
z-index 90 ; les écrans s'arrêtent au bord du rail (`left: 248px` + `right: 0`
+ `width: auto` — le `width: auto` est indispensable, un `left` seul
débordait de 248 px). **Poignée de repli active en plein écran** (Benjamin,
sur remarque de la revue).

**Vérifié** : `node --check` 5/5 · harnais **583/0** sur le fichier de
déploiement · porte hors-suite `coque 4.100` (12 points, fichiers réels) ·
**10 contre-regards injectés, 10 détectés** (restauration vérifiée par md5) ·
mesures à 1440 / 1024 / 390 : **0 débord horizontal** · repli en plein écran
testé · **DEV** : 4.100.0 servie, md5 `6080137b…` identique au `dist/`,
coque + polices en 200, fichiers sensibles en 404, rendu vérifié depuis l'URL
publique. **PROD : rien** — 4.97.2, md5 `fe652969…`, inchangée, sans coque et
sans la coupure cloud.

**Le passage qu'il a fallu franchir** : la porte a été **fausse au vert** trois
fois avant d'être juste — regex cassée par l'échappement Python→JS, `Number()`
renvoyant **NaN** (donc jamais comparable, donc toujours « vert »), et un
`\n` devenu un vrai saut de ligne qui empêchait le harnais de compiler. La
règle qui en sort : **une porte qui n'a pas été contre-regardée ne protège
rien**, et une porte qui renvoie `NaN` ne protège plus rien du tout.

✅ **Verrou libéré par Hermes le 20/10/2026, soir (2)** (4.99.0 — cloud
débranché sur le dev — **ÉCRIT ET TESTÉ, NON DÉPLOYÉ**).
Benjamin : « si j'ai bien compris le cloud est branché sur la branche dev alors
oui on le débranche ». Le cloud n'est pas branché sur une branche : il est
branché sur le **projet Supabase** dont la clé anon est dans le fichier livré —
dev et prod servaient donc le MÊME projet (`xlpfwvipdmgslwpbbfxs`). La coupure
est posée dans le **code livré** (test d'hôte), pas dans une configuration de
poste : c'est la seule façon que la règle soit vraie pour tout le monde. Six
points d'écriture coupés (dépôt d'état, envoi de photo, archivage, retrait du
bucket, connexion, cycle de synchro — ce dernier parce que la boucle de 90 s
continuait de LIRE le cloud de la prod et pouvait y fusionner l'état de Matis
par surprise). Visible : pastille « ☁ débranché » + panneau Options.
**Vérifié** : `node --check` 5/5 · harnais **583/0** · porte hors-suite
`cloud 4.99` (11 points lus dans le fichier réel) · **3 contre-regards**
(suppression d'une coupure → ECHEC ; coupure inconditionnelle, prod bloquée
→ ECHEC ; mode muet → ECHEC) · le stub `location` du harnais porte désormais
`hostname` (avant : `undefined`, la branche « débranché » n'était jamais testée).
**NON DÉPLOYÉ** : le domaine dev sert la refonte UI du jour (rail graphite),
construite hors du repo git par l'auto-designer ; deploying ce fichier le
remettrait à plat et j'ai déjà fait l'erreur une fois ce soir (Tour 76). La
4.99.0 attend que la coque du jour soit dans le repo git. **PROD : rien** —
4.97.2, md5 `fe652969…`.
✅ **Verrou libéré par Hermes le 20/10/2026, soir** (UI 4.98.0 — PAS de prod).
Pendant le tour : deux défauts **visibles à l'écran**, que ni les 582 tests ni le
journal ne voyaient. (1) Le libellé « PHOTO MACHINE À FOURNIR » (majuscules
7,5 px) demandait 4 lignes dans un cadre de 56 × 42 px : il en sortait et
passait sur « aucune référence déclarée ». Cause = la longueur du texte, pas le
cadre. Correctif : libellé court « photo à fournir » (8 px) + `overflow:hidden`
sur le cadre (un texte qui déborde ne peut plus recouvrir son voisin) ; la
formulation complète reste dans le `title`. (2) §3.5 du cahier UX : l'aide
`.pj-aide` flottait en permanence à côté de « + Créer un projet » — elle se
consulte désormais derrière un bouton (ⓘ), masquée par défaut ; mesuré : aide
rendue à 0 px, bouton 26 × 26, bandeau 44 px de haut. Les deux occurrences de
la même phrase dans les panneaux modaux sont laissées (§3.5 vise l'affichage
permanent à côté d'une action).
**Vérifié** : `node --check` 5/5 blocs · harnais **583/0** · 2 portes hors-suite
nouvelles (`tuile 4.98`, `aide 4.98`) qui lisent le fichier réel, **contre-regard
fait** sur chacune (régression injectée → ECHEC ; restauration → vert) ·
captures 1440 px et 900 px : superposition corrigée, les deux textes lisibles
et séparés · bandeau projets vérifié par le DOM (`+ Créer un projet ⓘ`).
Écrits : `bilan_economique.html`, `build_harness.py`, `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`. **PROD : rien** — la prod reste en 4.97.2, elle ne
bouge que sur la phrase de Benjamin (Q8-A).

✅ **Verrou libéré par Hermes le 17/10/2026 (2)** (UI 4.97.2 + PROD).
Pendant le tour : fin du débord horizontal mobile — le fautif était
`.hd-left` (flex sans min-width:0 ni wrap, eyebrow insécable), PAS les
tables (déjà scrollables via .tbl-wrap). Correctif : flex-wrap, break-word
sur eyebrow/h1, logo max-width:40vw. Vérifié scrollW 495 ≤ 500 au viewport
étroit. 582/0, `node --check` 5/5. **PROD** : Success!, md5 `fe652969…`
identique octet pour octet, TOOL_VERSION 4.97.2 servi. Écrits :
`bilan_economique.html`, `CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 17/10/2026** (UI 4.97.1 + PROD). Pendant le
tour : la barre d'outils passe de 180 px/3 rangées à **62 px/une ligne** —
icônes 13 px trait 1.7, segmented control pour les 5 écrans, libellés
courts, Exporter/Importer/Verrouiller en icône seule (title au survol),
moreBtn largeur fixe. Piège : wrap fantôme de 77 px sur le parent inline-flex
du ••• (contraint à 31 px). Mobile : boutons 44 px intacts ; débord
horizontal 420 px préexistant (.hd + table, hors périmètre, vérifié stash).
582/0, `node --check` 5/5, capture validée. **PROD** : Success!, md5
`18e46ebe…` identique octet pour octet, TOOL_VERSION 4.97.1 servi.
Écrits : `bilan_economique.html`, `CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 16/10/2026 (soir 2)** (UI 4.97.0, lot 4
« signature Apple » + PROD). Pendant le tour : toolbar sticky translucide
(verre `blur(14px)` + fond 78 %, classe `.is-sticky` au scroll, fallback
`@supports`, print statique — verre sur CETTE barre uniquement), motion
120→180 ms `cubic-bezier(.4,0,.2,1)`, ombres repliées sur `--shadow-card` /
`--shadow-hover` (23 valeurs héritées → 2 étages ; focus/insets/accents
légitimes conservés). Diagnostic documenté : les polices n'étaient pas le
problème. Piège rencontré et contourné : Chrome headless virtual-time gèle
la transition `background` — contre-vérifié sans transition (computed style
`0.78` alpha + `backdrop-filter` actif). 582/0, `node --check` 5/5.
**PROD** : Success!, md5 `54b0bea2…` identique octet pour octet,
TOOL_VERSION 4.97.0 servi. Écrits : `bilan_economique.html`,
`CHANGELOG.md`, `VERROU.md`.

✅ **Verrou libéré par Hermes le 16/10/2026 (soir)** (UI 4.96.1, lots 2+3 +
PROD). Pendant le tour : 20 déclarations `.var(--motion)` invalides réparées
(les hovers conçus v4.70 ne se sont jamais animés — le parser CSS rejetait
la déclaration entière) ; socle de mouvement commun tuiles/scénarios/cartes
avec `prefers-reduced-motion` ; gain annuel acté en gras (chiffre phare
carte atelier) ; refus documenté du cosmetic inutile (999px = pastilles
légitimes, `.btn` n'aurait rien changé). `outils/verif_lot23.js` 5/5,
harnais 582/0, `node --check` 4/4. **PROD sur ordre de Benjamin** :
`suivi-optimisation-septfons.surge.sh` — Success!, HTTP 200, md5
`dc5fe0e2…` identique octet pour octet, TOOL_VERSION 4.96.1 servi,
SW + manifest 200. Écrits : `bilan_economique.html`,
`build_harness.py` (porte 4.96), `outils/verif_lot23.js`, `CHANGELOG.md`,
`VERROU.md`.

✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 73, v4.90.0). Pendant le
tour, les trois lots de la revue Claude sont appliqués : P7 (data-plan
échappé, signe du gain, ordre des boutons, Cadence retiré, taux en état),
P6 (plancher de tailles, token secondaire ≥ 4,5:1, styles inline en
classes), P3 (hypothèse DDV affichée et réglable, seuil de neutralité, prix
SPK en réglage, confirmation case par case, Potentiel), P2 (le Simulateur
partage le basculeur, semaines/an éditable), P4 (dernier export affiché),
P5 (usure en pastilles, conformité en direct, bornes, charnière en 8 mots).
Le fichier est **normalisé LF** (19 719 CRLF) — fin des ancres capricieuses.
P8 : monolithe canonique, archives intactes (décision déléguée). 521 →
**552/552 verts**. Contre-regards vus. **Déployé sur Projet, vérifié curl ;
la PROD attend la phrase de Benjamin.** Écrits : `bilan_economique.html`,
`outils/patch_4900_v2.py`, `outils/tour73_journal.py`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`, `AUDIT_CLOUD_RLS.md`.

🔒 **Verrou pris par Z Code le 14/10/2026 soir** (tour 73, v4.90.0 — les suggestions à la saisie).✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 72, v4.89.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte post-patch : les
suggestions à la saisie (`catalogueSuggestion()`, `catalogueParIso()`,
`appliquerSuggestionCatalogue()` — pures et exportées), datalists natifs
`catMabec`/`catIso` alimentés au démarrage et aux changements du catalogue,
attributs `list=` sur les champs MABEC/ISO du logement, crochet dans
`writeFieldValue` (la branche logement), `TOOL_VERSION = "4.89.0"`,
NOUVEAUTES + CHANGELOG. Contre-regard : la porte initiale était aveugle
(logement déjà aux valeurs du catalogue) — **renforcée** (ISO manuel
DIFFÉRENT doit rester), faute injectée → **vue** → restaurée par copie,
empreinte identique, 521 → **551/551 verts**. **Déployé sur Projet,
vérifié curl ; la PROD attend la phrase de Benjamin.** Écrits :
`bilan_economique.html`, `outils/patch_4890_a.py`, `outils/verrou_t72.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

🔒 **Verrou pris par Z Code le 14/10/2026 soir** (tour 73, v4.90.0 — les suggestions à la saisie).✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 71, v4.88.0 — verrou pris
RÉTROACTIVEMENT, écart déclaré : le code était écrit avant la prise, aucun
autre auteur n'est intervenu). Pendant le tour, `bilan_economique.html` est
passé à l'empreinte post-patch : le **basculeur de consommation** dans le
Plan de conversion (théorique / RÉELLE extrapolée — les feuilles « Pareto
conso » des classeurs, une semaine × 52, lecture locale session-only ;
`consoDepuisFeuille()` pure, pareto de COUT refusé, ligne d'en-têtes
cherchée), un article sans donnée réelle **perd son gain** (jamais complété),
l'export CSV porte le mode, `TOOL_VERSION = "4.88.0"`, NOUVEAUTES +
CHANGELOG. 521 → **547/547 verts**. **Déployé sur Projet, vérifié curl ; la
PROD (4.87.0) attend la phrase de Benjamin.** Écrits :
`bilan_economique.html`, `outils/patch_4880_a/b.py`, `outils/tour71_journal.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.
**Accroc du tour : le VERROU lui-même a été commité VIDE par le tour 70
(`open('w')` tronquait avant un NameError) — reconstruit ici depuis
43f1efb, avec les entrées 70 et 71.**

---

✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 70, v4.87.0). Pendant le
tour, le plein écran GÉNÉRIQUE (`.panel.simul-maxi` — accueil, plan,
simulateur, catalogue), `basculerMaxi()` (boutons ⛶ sur l'accueil et le
Plan ; le Simulateur délègue), polices majorées en maxi (table 16,5 px,
titres 22 px), porte hors-suite à **6 règles**, `TOOL_VERSION = "4.87.0"`.
542/542 verts, syntaxe vérifiée par node --check. **Déployé sur Projet, puis
en prod sur la phrase de Benjamin (« passe en prod »), vérifiés curl.**
Écart déclaré : verrou non repris avant l'écriture du tour 70.

---

**Verrou libere par Z Code le 14/10/2026** (Tour 69, v4.86.0). Pendant le
tour, `bilan_economique.html` est passe a l'empreinte `ac9563a1...` : le Plan
de conversion (cibles SPK editables, auto-suggestion KY3500 -> LKT640 a 5 EUR,
etats step-by-step de Benjamin, total = lignes etatees seulement, gain =
plaquettes/an x ecart de prix, persistant dans le suivi, export CSV), portes,
`TOOL_VERSION = "4.86.0"`, NOUVEAUTES + CHANGELOG. Contre-regard : potentiel
compte comme promesse -> **vu** -> restauration par copie, empreinte
identique, 521 -> **542/542 verts**. Le tour des echappements consigne :
patchs par fichiers, heredocs bannis. **Deploye sur Projet ET en prod
(phrase de Benjamin : « fonce pour le Plan de conversion et deploie en
prod »), verifies curl — empreinte ac9563a1 identique aux deux domaines.**
Ecrits : `bilan_economique.html`, `outils/patch_4860_a/b/c.py`,
`outils/fix_plancsv*.py`, `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`,
`VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 68, v4.85.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `90ae73b6…` : le
catalogue plaquettes (persistant dans le suivi, seed par MABEC avec prix
fréquent et divergences signalées, propagation avec rapport, CSV standalone
aller-retour tolérant), panneau 📚 + porte de clic, `TOOL_VERSION = "4.85.0"`,
NOUVEAUTES + CHANGELOG. Le tour des guillemets : trois défauts attrapés par
le harnais avant livraison (apostrophe JS, ligne d'en-têtes cherchée, champs
quotés découpés proprement). Contre-regard : propagation muette → **vue** →
restauration par copie, empreinte identique, 521 → **533/533 verts**. Sur la
v5 réelle : 25 articles, 9 divergences pour Matis, le 137 021 porte déjà
LKT640 ET KY3500. **Déployé sur Projet, vérifié curl ; la PROD attend la
phrase de Benjamin.** Écrits : `bilan_economique.html`,
`outils/patch_4850_a/b/c.py`, `outils/fix_apostrophe.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 67, v4.84.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `55f32d76…` :
`simulCSV()` (CSV-FR : BOM + sep=; + décimales à virgule, deux tableaux,
export par Blob/ObjectURL), bouton ⤵ Exporter, ⛶ plein écran (CSS maxi +
Fullscreen API), **le bloc CSS du simulateur enfin inséré** (il manquait
DEPUIS LA 4.83 — garde conditionnel trop malin, insertion sautée en silence ;
porte hors-suite : 4 règles lues dans le fichier réel), la porte honnête du
66 bis remise (la restauration par copie avait rejoué une copie périmée),
`TOOL_VERSION = "4.84.0"`, NOUVEAUTES + CHANGELOG. Contre-regard : `sep=;`
faux → **vue** → restauration par copie **fraîche**, empreinte identique,
518 → 521/521 verts. **Déployé sur Projet, vérifié curl ; la PROD attend la
phrase de Benjamin.** Écrits : `bilan_economique.html`, `outils/patch_4840.py`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 66 bis, v4.83.1). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `d90a2d4a…` : libellés ISO
par article dans le simulateur, budget outillage annuel par référence (volume,
€/an, % du budget), clé de regroupement par référence = l'ID (268x12 sur deux
machines), `TOOL_VERSION = "4.83.1"`, NOUVEAUTES + CHANGELOG. Contre-regard :
clé par nom ré-injectée → **vue** (attribution mentie vue par la porte) →
restaurée par copie, empreinte identique, 518/518 verts. Deux attentes de tests
corrigées avant le vert (usages sans volume = présents à coût nul).
**Déployé sur Projet, vérifié curl ; la PROD attend la phrase de Benjamin.**
Écrits : `bilan_economique.html`, `outils/patch_4831.py`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 66, v4.83.0). Pendant le
tour, `bilan_economique.html` est passé à l'empreinte `4e2362e6…` :
`reattribuerEssai()` (bouton ⇄, même OP, essai entier, origine tracée, backup)
et le simulateur `plaquettesCommunes()` (panneau 💰 Simulateur prix, MABEC
regroupés multi-lignes, baisse %, économie €/an et % global, SIMULATION,
réfs sans volume nommées), portes de clic, `TOOL_VERSION = "4.83.0"`,
NOUVEAUTES + CHANGELOG. Contre-regard **deux fautes, deux portes** (assert) :
vues toutes les deux, restauration par copie, empreinte identique, 515/515
verts. **Déployé sur Projet, vérifié curl ; la PROD attend la phrase de
Benjamin.** Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 65, v4.82.0). Pendant le tour,
`bilan_economique.html` est passé à l'empreinte `904c7196…` : les 8 champs date
bornés (min 2025 / max 2035), les pastilles d'axes PAR ESSAI dans le panneau
atelier (`axesActifs()` pure + état de session, config du scénario intacte),
`TOOL_VERSION = "4.82.0"`, NOUVEAUTES + CHANGELOG. Un accroc assumé : le
remplacement global des bornes avait corrompu le sélecteur CSS
(`input[type="date" min=…]`) — réparé, et la porte hors-suite lit désormais le
fichier réel pour l'empêcher de revenir. Contre-regard **deux fautes, deux
portes** (assert) : vues toutes les deux, restauration par copie, empreinte
identique, 502/502 verts. **Déployé sur Projet, vérifié curl ; la PROD attend
la phrase de Benjamin.** Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 13/10/2026** (Tour 63, v4.81.2). Pendant le tour,
`bilan_economique.html` est passé à l'empreinte `37e72ddb…` : la branche
« correcteur manquant » (4.74.3) retirée du déclencheur du bandeau
(`detecterOutilsD1D2` ne voit plus que de vrais regroupements),
`compterCorrecteursManquants` supprimé, test 4.74.3 inversé en porte v3
(« un outil propre ne déclenche AUCUNE proposition, la correction n'y change
strictement rien »), `TOOL_VERSION = "4.81.2"`, NOUVEAUTES + CHANGELOG.
Contre-regard : faute ré-injectée **avec assert** → les deux portes v3 tombent →
restaurée par copie, empreinte identique, 499/499 verts. Le fichier v3 réel
(56 scénarios) : 0 regroupement, 0 inversion → **bandeau muet**.
**Déployé sur Projet, vérifié curl ; la PROD attend la phrase de Benjamin**
(en attendant, consigne chez Matis : ne pas cliquer le bandeau — faux positif
sur 4.81.1). Écrits : `bilan_economique.html`, `build_harness.py`,
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 12/10/2026** (Tour 62, v4.81.1). Pendant le tour,
`bilan_economique.html` est passé de l'empreinte `c13417e9…` à `77340221…`
(1 404 978 → 1 425 878 octets) : la porte de l'import (`preparerImportDepuis`,
faute `source.livraisons` depuis la 4.53.0 — ReferenceError silencieuse, aucun
import possible par bouton depuis le 29/09), une porte de test, entrée
NOUVEAUTES 4.81.1, `TOOL_VERSION = "4.81.1"`, CHANGELOG. Contre-regard selon
protocole : faute ré-injectée → **vue** par la porte
(`["ReferenceError: source is not defined"]`) → restaurée par copie
sauvegardée, empreinte `77340221…` identique avant/après, 501/501 verts.
Le fichier d'état fusionné réel passe par `preparerImportDepuis` : 10 lignes,
révision 421, T517 D1/D2 avec MABEC. **Déployé sur Projet, vérifié curl ; la
PROD reste en 4.81.0 et attend la phrase de Benjamin — c'est elle qui bloque
l'import du fichier fusionné demain chez Matis.** Écrits pendant le tour :
`bilan_economique.html`, `build_harness.py` (API + `preparerImportDepuis`),
`CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.

---

✅ **Verrou libéré par Z Code le 12/10/2026** (Tour 61, v4.81.0). Pendant le tour,
`bilan_economique.html` est passé de l'empreinte `6a082cda…` à `c13417e9…`
(1 401 140 → 1 404 978 octets) : `cloudLireTampon()` (lecture légère
`select=modifie_le,modifie_par`), `cloudSync()` réécrit pour ne payer la lecture
lourde que sur décision, 3 portes de test cloud, test « nouveautés » ré-ancré à
`TOOL_VERSION` (il était codé en dur 4.25.0 et se serait périmé seul),
`TOOL_VERSION = "4.81.0"`, NOUVEAUTES + CHANGELOG. Contre-regard selon protocole
(règle cassée → 1 test la voit → restauration par copie, empreinte vérifiée).
**Déployé sur Projet (4.81.0, vérifié curl, identique au local) ; la PROD reste
en 4.80.0 — elle ne bougera que sur phrase de Benjamin.** Écrits pendant le tour :
`bilan_economique.html`, `build_harness.py` (regénéré), `CHANGELOG.md`,
`ECHANGES.md`, `VERROU.md`. 2resume, proto/ et projet3 non écrits.

✅ **Verrou libéré par Z Code le 02/10/2026** (Tour 56, v4.80.0). Pendant le tour,
`bilan_economique.html` est passé de l'empreinte `afb7aa5d…` à `6a082cda…`
(1 348 004 → 1 401 140 octets) : palette v3.15, angles 3/4 px, Manrope
ré-embarquée, `TOOL_VERSION = "4.80.0"`. Aucun calcul, aucune fonction, aucune
saisie modifiés. Écrits pendant le tour : `bilan_economique.html`,
`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`. Le proto2 et la
prod n'ont pas été touchés (4.58.0 et 2.0 re-vérifiés).

✅ **Verrou libéré par Z Code le 02/10/2026** (Tour 55, proto v2.0). Pendant le tour,
`bilan_economique.html` n'a pas été écrit : son empreinte
`bf2e81a3998d4d9721c728eaaf666d1f7137fe1a5e5ea651440a65ea4eaf97ca` est identique à celle
notée au début. Seuls `proto/`, `ECHANGES.md` et `VERROU.md` ont été écrits.

---

## Comment ça marche

**Avant d'écrire la première ligne de code :**

1. tu remplis le tableau ci-dessus (auteur, heure, fichier, version visée, sujet) ;
2. tu **commites** ce changement — le verrou est donc dans l'historique, visible par tous ;
3. tu n'écris plus dans `bilan_economique.html` tant que le verrou est à toi.

**En fin de tour :**

1. tu vides le tableau (auteur → *(libre)*) ;
2. tu commites ;
3. ton tour est écrit dans `ECHANGES.md`, dans le même commit.

**Si le verrou est pris et que tu dois absolument écrire** : demande à l'autre session
de libérer, ou passe par Benjamin. **Ne contourne pas** — c'est exactement le geste qui a
coûté une session le 29/09.

---

## Pourquoi un verrou et pas une conversation

Parce que « je te préviens que je travaille » repose sur quelqu'un pour le dire, et
quoique quelqu'un oublie — surtout un agent, qui ne « pense pas » à l'étaler. Un fichier
qu'on lit par habitude, ça tient : c'est la première chose qu'on fait au tour.

---

## Variante automatique (proposée, non encore faite)

Le verrou manuel peut être oublié. Une version automatique lèverait deux défauts :

- **empreinte du fichier** : au début d'un tour, on note le SHA-256 de
  `bilan_economique.html` ; en fin de tour, on vérifie qu'il n'a changé que par nous. S'il a
  changé autrement, quelqu'un a écrit hors verrou → on le signale.
- **garde-fou de commit** : un script refuse un commit de `bilan_economique.html` si le
  verrou appartient à quelqu'un d'autre.

À faire quand on aura un vrai besoin — deux sessions qui codent en parallèle sur des
sujets différents. Pas avant : un garde-fou inutilisé est un garde-fou qu'on contourne.

## DEMANDE EN ATTENTE — ACTE II du débroussaillage (Benjamin, 28/10/2026)

Décrire « acte II » : dédoublonner la fiche scénario (nom ×3, « x/y essais conformes » ×4, statuts orange répétés — une info, un endroit), états vides du bandeau CPP en une ligne grise, fusionner Accueil/Atelier/Tableau en une « Vue densemble » (la boussole 4.117 reste en tête), fiche en niveaux (3 chiffres clés en tête : coût/pièce, écart vs base, validation ; config et rebut en accordéons repliés), puis acte III : bouton « Transmettre » unique + administration au menu •••. Protocole complet (verrou, ancres assert==1, portes, node --check, 662/0, build node, vérif curl). Ancres connues : nouveautesBtn ligne ~2024, verifierNouveautes ~14144, bb-alert ~2519, Tendance <h3> ~7467, rebut ~8774. État de départ : 4.120.0 en dev ET prod, 662/0, tout commité. NE PAS toucher aux polices des modèles dimpression A4 (Public Sans/Manrope = documents, pas linterface).
