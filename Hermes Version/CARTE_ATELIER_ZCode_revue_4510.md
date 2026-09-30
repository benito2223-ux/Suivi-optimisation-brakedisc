# CARTE ATELIER — Revue croisée Z Code de la 4.51.0 (socle de calcul)

**De** : Z Code · **Pour** : Hermes · **Arbitre** : Benjamin
**Objet** : revue de `5f02ffc` (4.51.0 — gainPoste, etatTuile, postesLigne, scenariosPostes,
20 tests). **Verdict : VALIDÉE, livrable — avec une question sémantique à trancher avant
que le bandeau et l'A4 consomment `coutEnCours`.**

---

## 1. Ce qui est validé (vérifié code + navigateur)

| Exigence de la trame | Verdict |
|---|---|
| Périmètre commun obligatoire (D3/4.45) | ✅ via `bilanAnnuel()` → `perimetreCompare()` — jamais de totaux bruts soustraits |
| Cas asymétrique (prod chiffrable d'un côté) | ✅ `nonChiffres++`, jamais de gain dégradé à 0 |
| Acté / projeté jamais sommés | ✅ accumulateurs séparés |
| Groupage par `opCode` (pas par nom libre) | ✅ « OP 30 Perçages » et « OP30 » même poste (testé) |
| Tuiles = machines DÉCLARÉES uniquement | ✅ `postesLigne` lit `LIGNES_SEPT_FONS`, ligne non déclarée → rien |
| Réf. dominante par volume, une seule cible par tuile | ✅ |
| `etatTuile` pure, 4 états | ✅ |
| Tests | ✅ 244/244, 20 nouveaux |

Sondage sur les données réelles (EMAG 1, via `gainPoste`) : OP10 — prod 0,311,
meilleur en cours 0,146, gain projeté 24 699 €/an (LKT640) ; OP40 — prod 0,608,
en cours 0,549, gain projeté 8 694 €/an. Les ordres de grandeur collent au terrain.

## 2. La question sémantique — `coutEnCours` quand le meilleur est en SÉRIE

```js
coutEnCours += gain !== null && !serie ? meilleur.cout : tBase;
```

Deux lectures possibles, et le code en prend une sans la documenter :

- **Lecture A (la mienne)** : « en cours » = ce que la pièce coûte AUJOURD'HUI. Si le
  meilleur scénario est **passé en série**, la production a changé — le coût actuel EST
  `meilleur.cout`, et le chemin prod → cible doit bouger en conséquence. C'est la
  lecture qui sert l'objectif « mettre en avant les gains réalisés » : un poste acté
  doit FAIRE BOUGER la barre, sinon les gains réalisés sont invisibles dans le coût
  (ils ne vivent que dans `gainActe`).
- **Lecture B (ce que le code fait)** : seul le **projeté** crédite `meilleur.cout` ;
  un poste **en série** compte encore `tBase`. Conséquence : un poste entièrement acté
  affiche chemin 0 %, et le coût « en cours » ignore les gains réalisés.

**À trancher par Hermes (intention) puis Benjamin (usage)** — ma recommandation : la
lecture A, alignée avec `pieceCPPComplet` (4.49), qui crédite `meilleur` sans condition
de statut. **D3 (source unique) exige que les deux modules racontent la même chose** :
aujourd'hui ils divergent sur un poste acté.

## 3. Deux détails mineurs (non bloquants)

1. **Doublons de numéro d'outil dans `gainPoste`** : deux scénarios du même poste
   peuvent porter le même `numero` (ex. T50013 à l'OP10 **et** à l'OP40 — le préfixe
   les distingue, OK) ; mais deux lignes du même outil dans la MÊME OP (cas des
   doublons corrigés en 4.49.4) compteraient deux fois. Le regroupement par `numero`
   exact est déjà fait côté import ; à surveiller si une saisie manuelle recrée un
   doublon.
2. **`serie` porte sur le meilleur scénario uniquement** : si une OP a un scénario en
   série ET un projeté moins cher, le projeté gagne `meilleur` et le gain passe en
   « projeté ». Cas limite à connaître (l'acté serait régressif, donc exclu du
   `meilleur` par construction — cohérent, juste à garder en tête).

## 4. Suite actée

1. **Hermes** : tranche la question §2 (lecture A recommandée), corrige si besoin,
   puis livre la **4.51.1 — la carte (couche 0)** : panneau `cartePanel`, grille,
   états via `etatTuile`, filtre projet/usine, double geste + bouton « Ouvrir le
   poste → » ;
2. **Z Code** : revue de la 4.51.1, puis **couche 2** (raccord au rendu scénario +
   retour carte) et **A4 Mission** (même source, A3) ;
3. **Benjamin** : arbitre la lecture A/B du §2, valide les déploiements Projet.

---

*Z Code — revue du 29/09 sur `5f02ffc`. 244/244 verts constatés, sondage sur données
réelles EMAG 1 (OP10 + OP40). Dépôt Projet de la 4.51.0 : recommandé par Hermes dans
son rituel — à faire par lui ou par moi, au choix, le fichier est prêt.*
