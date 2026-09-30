# Le rattachement d'un scénario HESSAPP au projet « Coût et qualité EMAG 1 »

**Constaté par Benjamin** le 29/09/2026, sur l'outil en 4.55.0.
**Verdict** : bug réel, deux causes distinctes, une seule source qui les produit.
**Aucun code écrit à ce stade** — diagnostic et correction proposée.

---

## 1. Ce que l'outil fait aujourd'hui

Il y a une règle, écrite en commentaire à la ligne 6911 et implémentée à la ligne 6947 :

> un projet peut légitimement traverser plusieurs lignes, donc on **avertit sans
> bloquer** quand on rattache un scénario à un projet qui ne contient que des scénarios
> d'une autre ligne.

La règle est donc **volontairement permissive**. Ton cas n'est pas un oubli de cette
règle : c'est un **trou dans sa condition**.

## 2. La cause exacte de ton cas

L'avertissement ne se déclenche que si ces trois conditions sont réunies (L6950) :

```js
if(ses.length && ligneCourante && !ses.includes(ligneCourante.nom)){ … avertir … }
```

Il manque l'inverse du cas. Le problème n'est pas le **Ht** :

1. le projet est nommé « Coût et qualité EMAG 1 » — c'est un **nom**, pas une contrainte ;
2. `lignesDuProjet()` ne regarde que les scénarios **déjà étiquetés** dans le projet ;
3. **si le projet est vide** (ou si ses étiquettes ne se résolvent plus après une
   purge/import), `ses` est vide → `ses.length` vaut 0 → **le `if` est court-circuité et
   l'avertissement ne s'affiche pas** ;
4. le rattachement passe **en silence**, sans rien dire.

**Autrement dit : un projet vide se comporte comme un projet « toutes les lignes ».**
C'est l'inverse de ce que son nom annonce, et c'est exactement ton cas.

## 3. Deux causes, donc deux corrections

### Cause 1 — le projet vide (TON CAS)
Un projet sans scénario étiqueté ne déclenche aucun avertissement, quelle que soit la
ligne. **C'est le trou principal.**

### Cause 2 — les deux autres chemins de rattachement, sans aucun avertissement
Il existe **deux autres façons** d'étiqueter un scénario, et **aucune** ne passe par la
règle :

- **la copie d'un scénario** (L10438) : la copie hérite des projets de l'original ;
- **la création d'un scénario dans le projet actif** (L10868) : le nouveau scénario est
  étiqueté d'office dans le projet ouvert.

Ces deux chemins sont **silencieux par construction**. Si tu crées un scénario HESSAPP
alors que le projet « Coût et qualité EMAG 1 » est ouvert, il est rattaché sans
question. C'est un choix d'usage de Matis (« renseigner les données dans le projet que
j'ai sélectionné ») — donc on ne le supprime pas, mais **il doit être visible**.

## 4. La correction que je propose

**(a) Un projet vide n'est pas une cible universelle.**
Quand un projet n'a **aucun** scénario étiqueté, le rattachement affiche une
confirmation explicite :

> « Le projet "Coût et qualité EMAG 1" ne contient encore aucun scénario. Vous êtes sur
> HESSAPP. Attribuer ce scénario à ce projet ? »

→ on **demande**, on ne bloque pas (cohérent avec la philosophie v4.5).

**(b) La règle couvre aussi le cas « le projet ne contient rien de la ligne courante ».**
Si le projet a des scénarios, mais **aucun** sur la ligne courante, l'avertissement
existe déjà — c'est bon. Il manque juste le cas vide, traité en (a).

**(c) Rendre visibles les deux chemins silencieux.**
- **copie** : si la copie va hériter d'un projet d'une autre ligne, une ligne
  d'information dans la confirmation de copie (« ce scénario restera rattaché à
  « Coût et qualité EMAG 1 », projet d'une autre ligne ») ;
- **création dans le projet actif** : la ligne de commentaire existe déjà, mais rien ne
  le dit à l'écran. Ajouter une mention discrète après création.

**(d) Un test** : rattacher un scénario HESSAPP à un projet **vide** doit déclencher la
confirmation. Et de même pour un projet dont les lignes ne sont pas résolues.

## 5. Ce que je n'ai pas fait, et pourquoi

- je n'ai **pas bloqué** le rattachement : la règle « un projet peut traverser les
  lignes » est saine, et c'est le choix de Matis ;
- je n'ai **pas** ajouté de contrainte « le nom du projet doit correspondre à la
  ligne » : un nom est un nom, pas une règle ;
- je n'ai **pas** touché au calcul : aucun chiffre n'est faux, c'est un problème
  d'étiquetage et de lisibilité.

## 6. La question pour Benjamin

**Le projet « Coût et qualité EMAG 1 » doit-il pouvoir accueillir un scénario HESSAPP ?**

- **S oui** (il couvre en fait deux lignes) → il faut renommer le projet, et l'avertissement
  devient un simple rappel, pas un frein ;
- **S non** (c'est bien un projet EMAG 1) → alors on peut **bloquer** ce cas précis, et
  c'est plus simple que d'avertir.

La réponse décide si (a) est un dialogue ou un garde-fou. C'est une décision d'usage,
pas de technique — et c'est la seule chose que je ne peux pas décider à ta place.

---

*Hermes — 29/09/2026. Diagnostic par lecture du code (4.55.0). Aucun correctif écrit à ce stade.*
