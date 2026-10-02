# PROJET3 — Suivi optimisation SPK · génération 3

La troisième génération du suivi d'optimisation du coût de revient des disques de
frein (site Sept Fons). Elle succède à l'app de production (`bilan_economique.html`,
4.80.0) et au proto (`proto/`, projet2) : les trois étages atelier-d'abord du proto,
la richesse de saisie de l'app, l'identité visuelle restaurée au Tour 56.

- **en ligne** : https://suivi-optimisation-projet3.surge.sh
- **localement** : `python -m http.server 8126` puis http://127.0.0.1:8126/index.html

## Ce qu'il est, en une phrase

Un poste d'usinage céramique/CBN tranché en cinq minutes — quel insert, quel gain,
quelle preuve — et une atelier qui peut tout saisir en gants. L'atelier d'abord,
le pilotage ensuite, la hiérarchie en dernier.

## Les règles que le code respecte

`CAHIER.md` est l'aiguille (une page, écrite avant le code). La `CONSTITUTION_SUIVI_v1.md`
de la racine du dépôt fait foi : source unique de chaque chiffre, un absent ne se
comble jamais, gains actés et projetés jamais sommés, battement jugé au pire des
deux côtés, K et P_req jamais visibles, loi du correcteur, aucune dépendance réseau.

## Fichiers

| Fichier | Rôle |
|---|---|
| `CAHIER.md` | le cahier des charges, une page — le code doit le respecter |
| `src/coeur.js` | les fonctions PURES (CPP, conformité, verdicts, gains, projets) |
| `src/import.js` | la migration formats 5-8 (sans perte) + la fusion arbitrage `modifieLe` |
| `src/donnees.js` | la topologie de l'atelier + le jeu d'exemple structurel |
| `src/ui.js` | les composants (badge unique, panneaux, toasts) |
| `src/app.js` | les cinq écrans (accueil, ligne, poste, emporter, projets) |
| `src/app_edition.js` | les panneaux de saisie (ligne, référence, OP, scénario, essai) |
| `src/app_panneaux.js` | projets, livraisons, options, données, rendu, démarrage |
| `src/fonts.css` | Manrope / Roboto / IBM Plex Mono embarquées (identité Tour 56) |
| `src/styles.css` | les tokens (jour + nuit), les composants, l'impression A4 |
| `src/shell.html` | la coquille |
| `assembler.py` | la couture en un `index.html` unique + empreinte SHA-256 des sources |
| `sw.js`, `manifest.webmanifest`, `icons/` | le service worker (réseau d'abord) et la PWA |

## Les tests (le rituel)

```bash
python assembler.py          # obligatoire après toute modification de source
node tests/test_coeur.js     # 149 tests du noyau
node tests/test_import.js    #  76 tests de migration, sur les 4 exports réels du dépôt
node tests/test_app.js       # 122 tests de l'assemblé (empreinte, portes, VALEURS rendues)
python tests/contre_regard.py  # 5 pannes injectées par couche — chacune doit être vue
```

Tout doit dire `TOUT EST VERT` / `CONTRE-REGARD VERT` et sortir en code 0.
Les suites comptent les tests EXÉCUTÉS, pas seulement les échecs (« 0 échec ≠ vert »,
constitution §6.10). `test_import.js` tourne sur les exports réels présents à la
racine du dépôt — ils ne quittent JAMAIS la machine (`.surgeignore` en liste blanche).

## Le déploiement

```bash
npx surge . suivi-optimisation-projet3.surge.sh
```

Le `.surgeignore` est une liste blanche stricte (index.html, manifest, sw, icônes) :
les sources, les tests et surtout les données d'essais réelles ne partent pas.
Vérifier ensuite PAR CURL, jamais par le « Success! » de surge :

```bash
curl -s https://suivi-optimisation-projet3.surge.sh/ | grep -o "Empreinte de l'assemblage : [0-9a-f]*"
```

La production (`suivi-optimisation-septfons.surge.sh`) ne bouge que sur une phrase
de Benjamin dans une session — règle non négociable.

## Les données

Rien ne sort du poste : pas de cloud, pas de compte. L'échange passe par
**Données → Exporter** (JSON complet, format 9) et **Importer**, qui propose
**Fusionner** (arbitrage `modifieLe` essai par essai) ou **Remplacer tout**
(double confirmation). Un instantané de secours est pris avant chaque import,
fusion ou réinitialisation (5 places, restaurables en zone rouge).

L'import lit les exports de l'app de production (formats 5 à 8) **sans perte** :
photos, plans de porte-outil, relevés Marposs et journal de rebut passent aussi —
le proto les jetait, la v3 est l'outil.

## Ce que la v3 n'a pas (par choix, cf. CAHIER.md §7)

Le classeur Matis (question de modèle posée à Matis, non tranchée), l'éditeur
d'annotation photo (les photos et annotations existantes sont conservées et
affichées), le cloud Supabase (le modèle est cloud-ready : chaque entité porte
`modifieLe`), la cadence (aucune cadence mesurée par ligne — l'écran le dit).
