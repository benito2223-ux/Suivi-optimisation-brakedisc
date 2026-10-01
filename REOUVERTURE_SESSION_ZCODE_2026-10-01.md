# RÉOUVERTURE DE SESSION — Z Code · 01/10/2026 (nouvelle fenêtre)

> **À coller en tête de la nouvelle fenêtre Z Code.** Tout le contexte nécessaire pour
> reprendre au bon endroit, sans relire l'historique. La fenêtre précédente est pleine,
> rien n'y est perdu : ce document est l'état réel du chantier au moment de la coupure.

---

## 0. En une phrase

Le suivi d'optimisation SPK est **en 4.78.0, tout vert (443 tests), verrou libre** ;
le dernier tour livré par Z Code est la **vue CPP** (l'écran que Benjamin a demandé :
opération par opération, outil par outil, logement par logement). **La revue est à
Hermes.** En parallèle, Hermes a abandoned son contrôle statique et m'a laissé un
chantier : le contrôle `typeof` dans le harnais.

---

## 1. Le projet

`bilan_economique.html` — **un seul fichier HTML**, ~18 300 lignes, zéro build, zéro SDK,
offline-first, PWA, synchro cloud Supabase. Dépôts : `suivi-optimisation-septfons.surge.sh`
(**prod**, ne jamais déployer sans feu vert explicite de Benjamin) et
`suivi-optimisation-projet.surge.sh` (**projet**, libre). Version courante **4.78.0**
(`TOOL_VERSION` ligne 12 387). Branche `dev`, HEAD `7fe0741`.

**Règle de déploiement, non négociable** : « rien n'est déployé sans que Benjamin l'ait
vu. Projet d'abord, prod sur feu vert. » Toujours vérifier par `curl`, jamais par le
« Success! » de surge.

---

## 2. Le protocole de travail (à respecter avant toute ligne de code)

Trois fichiers font la loi :

| Fichier | Rôle |
|---|---|
| `VERROU.md` | **verrou** — un seul auteur sur `bilan_economique.html` à la fois. Il est **libre** en ce moment. Le prendre avant d'écrire, le libérer en fin de tour. |
| `ECHANGES.md` | **journal commun** — chacun écrit son tour **en haut**, signe, date. Un tour = un commit. Le transport se fait par le fichier, plus par Benjamin. |
| `CONSTITUTION_SUIVI_v1.md` | **les règles** — v1.10. À relire avant de livrer. Points chauds : §3.1 source unique, §3.2 déclarer le non chiffrable, §3.4 additionner des gains interdits, §3.5 aucun chiffre mensonger, §2 quater les deux axes CPP, §5.x la rigueur, §6 gouvernance, §7 versions. |

Contraintes de communication avec Benjamin : ne jamais deployed en prod sans ordre,
ne pas cliquer « Corriger maintenant » (gel d'audit sur les données), ne jamais
déployer de données réelles (`.surgeignore` = liste blanche stricte). Le classeur
Excel de Matis se lit **en local uniquement** (constitution §4.2) ; les copies de
diagnostic se suppriment après usage.

---

## 3. Ce que Z Code vient de livrer (dernier tour, déjà commité et poussé)

**Tour 50 — v4.78.0 — la vue CPP** (`fa79c71` + `9335af4`, verrou libéré).
Elle affiche, en lecture seule, pour chaque pièce : le **CPP outillage obtenu face à la
référence Matis** (colonne I du classeur, importée dans `cibleCPP`), l'écart écrit en
toutes lettres, la décomposition **OP → outil → logement** avec MABEC / prix / arêtes /
DDV, l'axe **temps séparé** (jamais mêlé à la comparaison CPP, règle 2 quater), et
l'état déclaré des OP's non chiffrables. Porte d'entrée : bouton « 🔍 Vue CPP » dans
le pied de l'Accueil. **443 tests, tout vert.** Le contre-regard a été fait en deux
actes (le test « 2 quater » était d'abord **aveugle** — ni machine ni rebut dans le
cas ; on l'a rendu vulnérable, la panne est réapparue, puis restaurée par copie
sauvegardée).

**Pourquoi c'est important** : c'est l'écran que Benjamin a demandé en toutes lettres
— « le CPP, c'est le sujet jusqu'à la fin des projets ; c'est en travaillant
opération par opération, outil par outil, logement par logement qu'on optimise ».

---

## 4. Ce qui est en attente, et de qui

**De Hermes (elle le doit, à elle de dire quand c'est fait) :**
- la **revue de la vue CPP 4.78.0**, avec contre-regard sur la règle 2 quater en
  priorité. Tour 49 : « Ordre proposé, et il n'est pas le mien : Z Code construit la
  vue CPP, je relis. »

**De Z Code (prochain chantier naturel, proposé par Hermes au Tour 50) :**
- le **contrôle `typeof` dans le harnais** : boucle sur les gestionnaires de clic,
  un `typeof` par fonction appelée, un `ok()` par résultat. Hermes a abandonné son
  contrôle statique (regex) parce qu'un littéral comme `/^\/?xl\//` contient `//` et
  que son nettoyeur détruisait le fichier — donc 106 faux positifs, pire que pas de
  contrôle. Sa règle : **« une question sur le code se pose au code, pas à une
  approximation du code »**. Le harnais exécute déjà le JS dans Node : la réponse
  exacte (`typeof renderCarte` → `"function"` ; `typeof missionA4HTML` → `"undefined"`)
  est disponible sans parseur.
- **écrire `missionA4HTML()`** : son Tour 50 a vérifié que **le bouton existe mais la
  fonction n'existe pas** — un clic mort. Ce n'est pas encore corrigé.
- **les trois clics morts** restent ouverts (déjà diagnostiqués au Tour 46) : l'import
  de livraison et l'upload des photos de machines n'ont jamais été construits.

**De Benjamin (le goulot, rien ne le débloque) :**
- **envoyer le message à Matis** (`Hermes Version/MESSAGE_A_MATIS_7_demandes.md` —
  10 demandes de données, 7 des 10 ne peuvent venir que de lui). Tant qu'il n'est pas
  parti, l'audit tourne en rond.

**Données à faire confirmer par Matis (modèle en jeu) :** un même logement porte-t-il
un article (MABEC) différent selon la pièce usinée ? Si oui, le MABEC/prix/DDV doivent
descendre au couple (logement × référence) — chantier séparé, à ne pas ouvrir avant sa
réponse.

---

## 5. Décision de Benjamin à tracer (si elle revient)

Le **« Point hiérarchie »** (Q1 approuvée par Hermes) : un seul nom qui remplace
« A4 Mission » + « Livraisons », accessible depuis l'Accueil, **généré seulement à la
demande de Benjamin**. Pas construit à ce jour.

---

## 6. Comment reprendre, concrètement

1. Lire dans cet ordre : `VERROU.md` → **les 2 derniers tours en tête de `ECHANGES.md`**
   → la constitution → `CHANGELOG.md` (dernière entrée).
2. Vérifier l'état : `python build_harness.py` puis
   `node "$TEMP/h451.js"` → doit afficher « 443 tests | 0 echecs » + « TOUT EST VERT ».
3. **Si le prochain travail est du code** : prendre le verrou (`VERROU.md`), écrire,
   commiter (un tour = un commit), libérer le verrou, **déployer Projet seulement**,
   vérifier par `curl`, puis annoncer.
4. **Si c'est de la revue** : ne rien écrire dans `bilan_economique.html`, rendre la
   revue à Hermes.
5. Avant de livrer : **contre-regard**. Casser volontairement la règle protégée,
   vérifier qu'un test la voit, restaurer **par copie sauvegardée** (jamais
   `git checkout`, qui écrase le travail non commité — leçon du Tour 20).

---

## 7. Ce qu'il ne faut surtout pas faire

- Ne pas déployer en prod sans la phrase de Benjamin dans la session.
- Ne pas cliquer « Corriger maintenant » (gel d'audit, sur des données non comprises).
- Ne pas étendre `reparerOutilsD1D2()` ni corriger les 4 « Plaquette » avant d'avoir
  **daté** d'où ils viennent (Hermes, Tour 49).
- Ne pas commiter un contrôle ou un script qui n'a pas été vérifié en exécution.
- Ne pas ajouter au journal sans avoir relu l'ancre d'insertion (le journal s'est
  désorganisé deux fois).

---

*Transmis par Z Code le 01/10/2026 — HEAD `7fe0741`, 4.78.0, 443/443, verrou libre.*
