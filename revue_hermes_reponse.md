# Réponse à la revue — jeu de stress

Merci pour le jeu de données : il est bien construit et il a trouvé quelque chose. Le script
qui l'accompagne avait en revanche trois défauts, dont un qui a empêché son test le plus
intéressant de produire un résultat. Le script corrigé est joint (`stress_test.js`).

Version de l'outil au moment de cette réponse : **3.19.1**.

---

## 1. Les trois corrections apportées au harnais

### Le cas « volume négatif » n'a jamais tourné

```js
const opVN = getActiveReference().ops[1]; // r_stress2 / o_stress2
```

`o_stress2` n'est pas le 2ᵉ OP de la référence active : c'est le seul OP d'une **autre
référence**, `r_stress2`. `ops[1]` vaut donc `undefined`, l'accès à `.scenarios` lève une
exception, et le `try/catch` la transforme en `"BILAN — bilanAnnuel(vol=-5000) a lancé"`. Le
message ressemble à un résultat de test alors que le test ne s'est pas exécuté.

C'est d'autant plus dommage que ce cas était le meilleur du jeu. Ciblé correctement, il donne :
`bilanAnnuel()` et `volumeAnnuel()` renvoient tous deux `null` — l'outil refuse un volume ≤ 0
au lieu de produire un gain annuel négatif absurde.

Il a aussi mis en évidence un défaut réel, corrigé depuis (voir §3).

### Le script écrit dans les données de production

`saveData()` est appelé avec `revision: 99` sur le `localStorage` réel. Combiné au point
suivant, une exécution sur le poste où Matis saisit ses relevés aurait été coûteuse.

Le script corrigé est **non destructif par défaut** : `SPK_STRESS.run()` évalue tout en mémoire
et restaure les variables globales dans un `finally`. Rien n'est écrit. L'injection dans
l'interface reste disponible, mais explicite : `SPK_STRESS.run({injecter:true})`.

### La restauration perd l'onglet ouvert

La sauvegarde de secours stocke la clé `activeId` :

```js
const cur = { lignes, backlog, revision, activeLigneId, activeReferenceId, activeOpId, activeId };
```

alors que `loadAll()` lit `activeScenarioId`. Au retour, le scénario ouvert retombe sur le
premier de la liste. Le script corrigé écrit exactement le format de `saveData()`.

Pour mémoire : `runTests()` renvoie bien `{total, echecs, details}`, le script d'origine avait
raison sur ce point.

### Détails sans conséquence

`fin` et `programmeCNC` n'existent pas sous ces noms (`dateFin` / `heureFin` et `programme`), et
`usure: "neuve"` / `"usagée"` ne sont pas des valeurs reconnues (`ok` / `limite` / `changer`).
Ils sont ignorés sans casse — mais ces pièges-là ne piègent rien.

---

## 2. Comportement de l'outil sur les pièges, version 3.19.1

| piège | résultat | lecture |
|---|---|---|
| cycle baseline 87,3 injecté | ramené à **100** | par définition ; le champ n'est pas éditable sur la référence |
| cycle détaillé incomplet (1 logement / 2) | `complete: false` | repli sur l'indice base 100, avec une ligne de statut qui dit lequel des deux calculs sert |
| arêtes = 0, prix = 0 | `plaquettes: null` | pas de division par zéro, pas d'`Infinity` ; le total reste calculé sur les postes valides |
| rebut 50 % | 7 €/pièce de rebut, total 8,17 €/pièce | contre 0,73 pour la référence |
| seuil de bascule, scénario perdant | `charniereImpossible: true` | le cycle nécessaire pour rentrer dans les coûts est absurde, et c'est dit |
| tolérance franchie **au milieu** | charnière réelle = **50 pièces** | on ne revendique pas 150 quand la cote est sortie à 100 |
| EMAG 1 ancien format (`batt` seul) | 0,08 relu correctement | la migration D/G n'écrase pas l'ancienne mesure |
| volume annuel = −5000 | `null` + bandeau d'alerte | voir §3 |

Aucun crash, aucun `NaN` affiché, 73/73 tests internes au vert sur ce jeu.

---

## 3. Ce que la revue a fait corriger

**Volume annuel invalide silencieux.** Un volume négatif ou nul faisait disparaître le bandeau
de production, les gains en €/an, les heures machine et la consommation de plaquettes — sans un
mot. Pour qui s'est trompé de signe, « le gain a disparu » est incompréhensible. Un bandeau
nomme désormais la référence, la valeur fautive et le chemin pour la corriger, et précise que
les chiffres **ne valent pas zéro : ils ne sont pas calculés**. *(v3.17.0)*

**Coût non calculable non expliqué.** En rejouant le jeu sur la version courante, le scénario
« valeurs aberrantes » a montré qu'un logement à 0 arête affichait « Coût — » dans la vue
d'ensemble alors que la cause était lisible trois lignes au-dessus, dans la même tuile. Le
contrôle ne détectait que les cases **vides** ; or 0 n'est pas vide, c'est une valeur saisie et
inexploitable. Deux problèmes distincts qui n'appellent pas le même geste, désormais distingués :
« Manque : … » (à remplir) et « Coût non calculable : nombre d'arêtes à 0 » (à corriger).
*(v3.19.1)*

---

## 4. Ce que le jeu ne couvre pas encore

Les mécaniques suivantes sont postérieures à la revue et sont maintenant évaluées par le script
corrigé — mais elles mériteraient leurs propres pièges, si tu veux pousser :

- **fusion de deux fichiers** (3.16) : l'arbitrage se fait par essai sur un horodatage
  `modifieLe`. Les 5 essais du jeu n'en ont pas et partiraient donc en conflit avec conservation
  de la version locale. Un jeu à deux fichiers divergents serait le vrai test ;
- **prévision d'usure** (3.16) : régression sur les prélèvements, avec garde-fous (≥ 4 points,
  ≥ 3 n° de pièce distincts, pente positive, R² ≥ 0,35). Le jeu la déclenche sur `s_piege2` —
  qui répond « déjà hors tolérance », la bonne priorité — et pas sur `s_piege5`, 3 points ;
- **protection du quota** (3.19) : trois niveaux (purge de l'historique et nouvelle tentative,
  puis alerte franche + bandeau permanent, plus un avertissement préventif dès 3,5 Mo qui nomme
  les pièces jointes lourdes). Se teste en interceptant `Storage.prototype.setItem` ;
- **pièces jointes** : plans d'outil et fiche outil d'OP passent par une règle unique — dossier
  local s'il est connecté, sinon base64 sous 500 ko, sinon refus expliqué. Motif : `localStorage`
  plafonne autour de 5 Mo pour l'intégralité du suivi, et une sauvegarde qui échoue bloque
  l'enregistrement des **mesures**. On ne perd pas des relevés à cause d'un plan.
