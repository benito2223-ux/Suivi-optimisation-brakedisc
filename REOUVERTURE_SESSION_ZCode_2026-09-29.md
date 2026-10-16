# RÉOUVERTURE DE SESSION — Z Code · 29/09/2026 (fin de journée)

> À coller en tête de la nouvelle session Z Code. Ce document contient tout le contexte
> nécessaire pour reprendre le travail exactement où on en est, sans relire l'historique.

---

## 1. Le projet en 30 secondes

Outil de suivi d'optimisation du coût de revient des disques frein (usinage céramique,
Stellantis Sept Fons). **UN SEUL fichier HTML** : `bilan_economique.html` (~13 500 lignes,
1,1 Mo), zéro build, zéro SDK, offline-first, synchro cloud Supabase (projet
`suivi-septfons`, org « Sept Fons », URL `https://cxjfyaorkkxemjnollnj.supabase.co`),
PWA installée chez les utilisateurs (service worker réseau-d'abord).

Contexte métier complet : `C:\Users\Admin\.zcode\AGENTS.md` §3.
Brief UI : `C:\Users\Admin\Desktop\BRIEF_UI_SUIVI_SPK.md` (partiellement obsolète —
polices et version changées depuis).
Constitution : `CONSTITUTION_SUIVI_v1.md` à la racine du repo (règles du jeu, à lire).

## 2. État des branches et déploiements (au 29/09 soir)

| Quoi | Où | Version |
|---|---|---|
| **`dev`** (travail) | GitHub `origin/dev` = `a28729c` | **4.54.0** |
| **`main`** (référence) | GitHub `origin/main` = `665c9f3` | **4.52.0** |
| **Prod** (PWA Matis/Benoît) | https://suivi-optimisation-septfons.surge.sh | **4.49.4** |
| **Projet** (test/validation) | https://suivi-optimisation-projet.surge.sh | **4.54.0** |

**À faire quand Benjamin valide** : merge `dev` → `main` + déploiement prod
(`npx surge . suivi-optimisation-septfons.surge.sh`) → tout le monde passe en 4.54.0.

## 3. Les 25 versions livrées (4.30 → 4.54.0) — résumé

Session dédiée UI (24-29/09), travail en équipe croisée Hermes × Z Code, arbitrage
Benjamin. CHANGELOG complet à partir de la 4.49.4 ; les entrées 4.31→4.38 ont été
rétro-écrites (rondes Hermes).

**4.30-4.38 (Hermes)** : tableau de bord fusionné, synthèse comparative, identité SPK
(bleu #1B5EA6), zones nommées (Réponse/Scénarios/Traçabilité), densité, libellés à deux
niveaux, tendance repliable.

**4.39-4.41 (Z Code)** : cycle par logement (somme ou max par opCode, mesures complètes
sans interrupteur), coût machine affiché/pondéré, périmètre de comparaison synchronisé
(`perimetreCompare`), cibles CPP par référence, pop-up bienvenue, A4 Mission, couche 2.

**4.42-4.44 (Hermes)** : fiche poste (couche 1), groupes d'outils simultanés en bloc
ambre, simultané par outil (pas par scénario), prod entité distincte (décision 2
arbitrée), constitution v1 co-rédigée.

**4.45-4.47 (Z Code)** : périmètre de comparaison synchronisé, cibles CPP, design system
v4.29 restauré, livraisons figées datées.

**4.48-4.54 (Hermes)** : compléter depuis la prod, coût pièce complet, feuille de route,
fiche poste (couche 1), pop-up bienvenue, A4 Mission, fix scénario figé, fix divergence
`coutEnCours`.

## 4. Les règles non négociables (constitution v1, résumé)

1. **Un seul fichier HTML**, zéro build, zéro réseau, polices embarquées ;
2. **Offline-first** : le cloud n'ajoute jamais une dépendance ;
3. **Jamais de K ni P_req visibles** — ni écran, ni impression, ni carte ;
4. Nommage nuances **SPK** (jamais Greenleaf), français atelier ;
5. **Deux thèmes** (sombre/clair) + **impression A4** + **tactile** vérifiés à chaque UI ;
6. **Déploiement Projet seul** — la prod ne bouge que sur validation de Benjamin ;
7. **Données réelles jamais déployées** ; prototypage sur jeu [Exemple] en profil isolé ;
8. **Source unique par chiffre** : périmètre commun obligatoire (`perimetreCompare`),
   la carte ne montre rien que le bandeau du scénario ne montre pas ;
9. **Pas de nommage figé dans le code** (leçon Bol/Piste) : `opCode` dérivé, machines
   déclarées dans `LIGNES_SEPT_FONS` ;
10. **Constitution** (`CONSTITUTION_SUIVI_v1.md`) : lue avant de coder, toute évolution
    contradictoire passe par une décision explicite de Benjamin.

## 5. Le serveur Postgres — défense serveur active

Trigger `preserve_cibles_cpp` sur la table `etat` (Supabase `cxjfyaorkkxemjnollnj`) :
réinjecte les `cibleCPP` dans toute écriture qui les efface. Testé en production —
un push intégralement strippé atterrit avec les 6 cibles intactes. **La donnée est
défendue côté serveur, quelle que soit la version du client.**

## 6. Où on en est — les phases de la carte atelier

- ✅ **Couche 0** (4.51.2) : carte en tuiles machines, lecture seule, filtre projet/usine
- ✅ **Couche 1** (4.54.0) : fiche poste au survol/tap (réfs, statuts, gains, prochaine
  étape en toutes lettres)
- ✅ **Couche 2** (4.52) : « Ouvrir le poste → » navigue vers le rendu scénario
- ✅ **A4 Mission** (4.52) : imprimable hiérarchie (gains actés, en cours, plan)
- ⏳ **Découpage restant** : fiche poste enrichie (couche 1 Hermes : gains par outil,
  chemin vers cible par poste), **décision 2** (prod entité distincte — différée),
  **décision 3** (livraison — le code est en 4.53, l'usage reste à activer par Matis)

## 7. Les points ouverts (rien d'urgent)

1. **Matis** : validation de la base 2026/2027 + mise à jour de son application (fermer
   les onglets périmés — version ancienne efface les cibles au partage) ;
2. **Volumes annuels** : les « Production » de l'excel semblent être des cumuls de
   période — à confirmer/corriger dans Options ;
3. **Charnières OP20** (ébauche piste ext., 3 outils) et **HESSAPP OP20** (1 outil vide) :
   à faire remplir par Matis — c'est ce qui bloque le coût pièce complet sur ces postes ;
4. **DDV T548** : signaler à Matis que son excel dit 50 alors que le terrain = 30 ;
5. **Weisser 1-4, PCI 4/5** : lignes vides — à créer quand ces lignes entrent dans le
   périmètre ;
6. **Merge dev → main + prod** : prêt, attend la validation de Benjamin ;
7. **Décision 2** (prod entité distincte) : différée — le format 9 n'est pas nécessaire
   tant que la danse ★/excel est documentée et testée.

## 8. Le serveur local

`python -m http.server 8017` à la racine du repo. Les tests : ouvrir
`http://localhost:8017/bilan_economique.html#tests` ou `runTests()` en console.
**Attendu : 283/283 verts** (4.54.0).

## 9. Rituel de release (inchangé)

1. Branche `dev`, un commit par version livrée ;
2. Tests verts + deux thèmes + console propre ;
3. NOUVEAUTES + CHANGELOG + TOOL_VERSION ;
4. Push `dev` + déploiement **Projet** ;
5. Revue croisée Hermes × Z Code avant tout passage vers main ;
6. Merge `dev` → `main` + déploiement **prod** uniquement sur validation de Benjamin.

---

*Z Code — 29/09/2026. Ce document remplace toute lecture de l'historique de session.*
