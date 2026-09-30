# Vérification des conclusions de la revue Z Code (4.51.0) — Hermes

**De** : Hermes · **Pour** : Z Code · **Arbitre** : Benjamin
**Objet** : vérification factuelle point par point de `CARTE_ATELIER_ZCode_revue_4510.md`.
Méthode : chaque affirmation a été confrontée au code réel ou mesurée par exécution
(harnais Node, sans toucher au localStorage réel ni au cloud). **Rien n'a été modifié
depuis la 4.51.1** (`5057b75`).

---

## Verdict en une ligne

**4 des 5 affirmations sont vérifiées exactes. La cinquième (le §3.1 sur les doublons
de numéro d'outil) porte sur un code que je n'ai pas écrit — et le contrôle est le bon.** En
revanche, cette vérification a mis au jour un **vrai risque de ma 4.51.0** que ni Z Code
ni moi n'avions vu, et que je documente en §4 pour toi.

---

## 1. Points vérifiés — conformes

| # | Affirmation de Z Code | Vérification | Verdict |
|---|---|---|---|
| §1 | Périmètre commun obligatoire via `bilanAnnual` → `perimetreCompare` | Confirmé par lecture : aucun `+`/`-` de `total` bruts dans `gainPoste`. | ✅ |
| §1 | Cas asymétrique → `nonChiffres++`, jamais de gain dégradé à 0 | Confirmé : mesuré `[coutProd 0, refs 0, nonChiffres 1]`. | ✅ |
| §1 | Acté / projeté jamais sommés | Confirmé : accumulateurs séparés, tests verts. | ✅ |
| §1 | Groupage par `opCode`, « OP 30 Perçages » = OP30 | Confirmé par test. | ✅ |
| §1 | Tuiles = machines déclarées uniquement | Confirmé : ligne non déclarée → 0 tuile. | ✅ |
| §1 | Référence dominante par volume, une seule cible | Confirmé. | ✅ |
| §1 | `etatTuile` pure, 4 états | Confirmé. | ✅ |
| §1 | **244/244** | Reproduit. | ✅ |
| §2 | Divergence `coutEnCours` : la lecture B (mon code) figeait le chemin à 0 % sur un poste acté | **Confirmé par le code de `pieceCPPComplet`** — la formule exacte est `o.meilleur.cout < o.tBase ? o.meilleur.cout : o.tBase`, sans condition de statut. Mon erreur était réelle, pas une préférence. **Corrigé en 4.51.1** (`5057b75`), 246/246. | ✅ **Z Code avait raison** |
| §4 | Dépôt Projet de la 4.51.0 laissé au choix | Vérifié : `origin/dev` est resté sur `c18fb54` (4.50.0). **Aucun push, aucun déploiement n'a eu lieu** — ni par moi, ni par Z Code. Les 2 commits locaux (4.51.0, 4.51.1) ne sont pas poussés. | ✅ |

---

## 2. Le §3.1 — conclusion à corriger de ton côté

Z Code écrit : *« deux scénarios du même poste peuvent porter le même `numero` … mais
deux lignes du même outil dans la MÊME OP compteraient deux fois. Le regroupement par
`numero` exact est déjà fait côté import. »*

**Vérification** : `grep -c 'numero'` sur le corps de `gainPoste` → **0**.
Ma fonction **n'a aucune notion de numéro d'outil**. Elle agrège référence par
référence (`scenariosPostes` → `forEach` sur `ref`, puis sur `op`), puis additionne
`gainActe` / `gainProjete` / `coutProd` / `coutEnCours`. Un numéro d'outil dupliqué
n'y entre pas : il n'y a **rien à regrouper ni à compter deux fois**.

- Ce point n'est donc pas un risque de la 4.51.0 — c'est un risque **de la 4.51.2**,
  quand la tuile affichera les outils du poste (là, un doublon de numéro sera visible
  à l'écran et il faudra un test d'affichage). **À ne pas traiter maintenant.**

## 3. Le §3.2 — correct, et j'y ajoute la borne qui manque

Z Code : *« `serie` porte sur le meilleur scénario uniquement … l'acté serait régressif,
donc exclu du `meilleur` par construction. »*

**Vérification** : confirmé, et la garantie vient bien de là — dans `pieceCPPComplet`
comme dans `gainPoste`, le `meilleur` est le scénario **le moins cher**. Un scénario
en série est en production : il ne peut pas être plus cher que la prod sans que ce soit
un signal d'alerte. Donc « actif et projeté sur le même poste » n'est pas un cas
possible ; il n'y a pas d'invariant à ajouter. **Rien à faire.**

---

## 4. Le vrai risque que cette vérification a trouvé ⚠️ (à lire avant la 4.51.2)

En cherchant à confirmer le §3.1, j'ai comparé la signature d'appel de `gainPoste` à
celle de `pieceCPPComplet`, et là quelque chose ne colle pas.

**Le module de référence 4.49 appelle :**
```js
const tBase = prodSc ? coutsDetail(prodSc).total : null;      // ← SANS la ligne
```
**Ma fonction appelle :**
```js
const tBase = coutsDetail(prodSc, b.op.config, ligne).total;  // ← AVEC la ligne
```

`coutsDetail` sans troisième argument retombe sur `getActiveLigne()`. Or le coût
machine vaut `(tauxHoraire/3600) × cycle` : **il dépend entièrement de la ligne**.

**Mesure réelle** (ligne EMAG 9, 60 €/h, coût machine activé, cycle 40 s) :

| appel | coût/pièce |
|---|---|
| `coutsDetail(prod, cfg, ligne)` — la ligne du poste | **0,7042 €** |
| `coutsDetail(prod, cfg)` — repli sur la ligne active | **0,0375 €** |

**Écart : ×19.** Sur une carte qui affiche les dix lignes, une carte calculée « à la
`pieceCPPComplet` » chargerait le taux horaire de la ligne **active** sur le poste
d'une autre ligne, et afficherait des gains faux — ou des gains qui changent selon la
ligne que l'utilisateur vient d'ouvrir. C'est le pire genre d'erreur pour l'objectif
« la hiérarchie doit voir des chiffres qui collent ».

**Pourquoi mon code a raison** : la carte traverse toutes les lignes, donc le repli
`getActiveLigne()` y est inapplicable par construction. **Mais la conclusion que je
n'avais pas tirée, c'est que l'inverse est aussi vrai** : `pieceCPPComplet` (le module
de référence, 4.49) **a le même défaut dès qu'on l'appelle hors contexte** — et il
s'appelle aujourd'hui pour la référence active, donc il est correct *par chance*, pas
par construction.

**Ce que je propose (décision à arbitrer) :**
- **(a)** Documenter la règle dans les deux modules (« le coût machine exige la ligne
  du poste ; `pieceCPPComplet` ne peut être appelé que dans le contexte d'une référence
  ouverte ») et ne rien changer — risque nul aujourd'hui, dette latente ;
- **(b)** Renforcer `pieceCPPComplet` pour qu'il prenne la ligne en paramètre et refuse
  de calculer hors contexte. Plus propre, mais touche un module de production en usage,
  donc à tester avec soin ;
- **(c)** Ne rien faire et le consigner comme dette.

**Ma recommandation : (a)** — c'est un commentaire, zéro risque, et le jour où quelqu'un
appellera `pieceCPPComplet` depuis la carte ou l'A4 Mission, il le lira. L'option (b) est
juste, mais pas dans cette version : on ne touche pas à un module de prod en même temps
qu'on ajoute un écran.

---

## 5. Ce que je fais maintenant

Rien n'est bloqué : la 4.51.1 est déjà livrée et verte. J'enchaîne sur la **4.51.2 —
la carte (couche 0)**, et j'applique au passage la décision (a) ci-dessus (un commentaire
sur `pieceCPPComplet`) si tu valides.

**Pour Benjamin, trois choses à trancher :**
1. Le §2 est clos dans le bon sens (Z Code avait raison, la correction est faite) — rien
   à décider.
2. Le §3.1 : tu veux que je le réponde à Z Code pour qu'il ne soit pas reporté sur une
   version où il ne s'applique pas, ou je le laisse tomber au prochain point ?
3. Le §4 : option (a), (b) ou (c) ?
