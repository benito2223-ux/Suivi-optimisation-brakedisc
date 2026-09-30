# Audit de nos propres chiffres — la règle §5.6 appliquée à nous d'abord

> 30/09/2026, après l'arbitrage de Benjamin : la règle « un chiffre qu'on ne peut pas
> justifier n'est pas affiché » est écrite dans la constitution. **On commence par
> s'auditater soi-même**, sinon la règle ne vaut rien.

---

## Ce qui a été vérifié

### 1. Aucun chiffre inventé dans le moteur

Recherche de tous les montants et pourcentages littéraux dans `bilan_economique.html`
v4.62.0 (16 214 lignes) : **14 valeurs distinctes**, toutes vérifiées une à une.

| Valeur | Où elle est | Verdict |
|---|---|---|
| `127 340,88 €` | commentaire de carte (L4801) | ✅ pas de code |
| `5 218 €` / `8 179 €` | texte du panneau Matis | ✅ comparatif classeur réel |
| `0,212 €` / `0,129 €` | texte NOUVEAUTES (cible site) | ✅ chiffre de Matis cité |
| `0,763 €` / `0,038 €` / `0,63 €` | **commentaires** de la carte d'accueil | ✅ documentation |
| `0,7042 €` / `0,0375 €` | commentaire du test ×19 | ✅ mesure historique |
| `2 500 €` / `0,3 €` | **fixtures de test** | ✅ hors production |

**Zéro montant en dur dans une fonction de calcul.** L'outil calcule tout à partir des
saisies ; il ne 'invente' pas de résultat. C'est exactement ce que la constitution exige.

### 2. Les agrégats portent leur périmètre

- `gainActe` et `gainProjete` sont **deux blocs distincts** partout ;
- **0 occurrence** d'une somme `gainActe + gainProjete` en un seul chiffre (règle §3.4) ;
- la mention « hors n opération non chiffrée » est bien présente (règle §3.2, le correctif
  de la 4.60.1).

### 3. Les chiffres de Stitch — vérifiés, et écartés

| Chiffre Stitch | Dans notre outil ? | Source réelle |
|---|---|---|
| 120 000 pcs/an (EMAG 1 356x26) | **seulement dans les fixtures de test** | classeur Matis : **6 781** |
| 84 250 €/an | absent | non justifié |
| 37 800 € | absent | non justifié |
| 88,4 % | absent | non justifié |

**Fausse alerte de notre part, corrigée** : une recherche naïve concluait que « 120 000 »
était présent dans l'outil. Il l'est — mais **dans les jeux d'essai du harnais**, jamais dans
les données affichées. Le vérifié ici, c'est la distinction : c'est exactement le piège que la
règle veut nous faire éviter.

### 4. Aucune dépendance réseau

| Type | Nombre |
|---|---|
| feuille de style distante | **0** |
| police distante | **0** |
| image ou script distant | **0** |
| Tailwind CDN | **0** |

**L'outil est déjà 100 % autonome.** Il n'y a rien à supprimer de ce côté (chantier C2′ vide) :
c'était un risque pour l'**implémentation** de la proposition Stitch, pas un défaut de l'outil.

---

## Ce que l'audit révèle quand même

**Les productions réelles de Matis (6 781, 2 490, 8 149) sont absentes de l'outil.**

Ce n'est pas un défaut : elles vivent dans son classeur, et Matis ne les a pas encore saisies
dans le suivi. **C'est le remplissage — celui que le message aux 7 demandes demande.**

Et c'est pour ça que l'écran d'accueil affiche « volume annuel à saisir » plutôt qu'un
chiffre : **notre outil préfère ne rien montrer plutôt que montrer un chiffre sans source.**
C'est la règle §5.6 déjà appliquée, sans qu'on l'ait écrite.

---

## La conclusion, en une ligne

**Notre outil ne fabrique rien ; il affiche ce qui est saisi, et dit ce qui manque.**
C'est ce qui le sépare de la proposition Stitch — et c'est pour ça qu'il est plus proche
d'être défendable devant une hiérarchie, même incomplet, qu'un écran parfait et faux.
