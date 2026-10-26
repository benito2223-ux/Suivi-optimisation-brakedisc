# Contre-regard Hermes — 4.111.0 « Verdict par outil » (Z Code, Tour 94)

**Pour :** Z Code · copie Benjamin
**Par :** Hermes, 26/10/2026
**Vérifié sur :** l'arbre local, `dist/`, le DEV servi, et le harnais régénéré par
mes soins — pas sur la foi du rapport.

## 1. Ce que j'ai vérifié indépendamment — tout est confirmé

| Affirmation du rapport | Ma vérification | Verdict |
|---|---|---|
| Harnais 642/0 (+8 tests verdict par outil) | Régénéré et exécuté : 642/0, les 8 tests 439–446 visibles | ✅ |
| `appariementOutils` par numéro, `flatsSc.indexOf` banni de la tuile | 5 occurrences du module, **0** occurrence de l'appariement positionnel | ✅ |
| Badge « sorti du scénario » + ligne « dont sorties du scénario » | `fv-sortie` ×2, ligne ×5 | ✅ |
| Ancre de temps : jamais de secondes sans chrono | `chronoComplet` ×8 ; porte anti-secondes dans la suite | ✅ |
| Porte hors-suite `verdict par outil 4.111` | Présente dans `build_harness.py` (ligne ~1202) | ✅ |
| Dev == dist | md5 `d1957e5e…` identiques octet pour octet | ✅ |
| Aucun K/P_req dans les libellés | Les 3 occurrences du HTML sont des commentaires du sanitiseur lui-même | ✅ |
| Contre-regard double (casse A/B) | **Refait par Hermes, indépendamment** : marqueur positionnel réinjecté dans le bloc tuile → porte tombée proprement (`ECHEC … l'appariement positionnel est de retour dans la tuile`), restauration octet-pour-octet, 642/0 après | ✅ |

Un écart de rapport, sans gravité : l'empreinte citée (`e0001dd4…`) ne correspond
pas au md5 actuel de `dist/bilan_economique.html` (`d1957e5e…`, qui est bien celui
que sert le DEV). Probablement une empreinte prise avant un rebuild. Citer le md5
du fichier livré, pas d'un état intermédiaire.

## 2. Sur la « découverte assumée » (le groupe sans ses membres sortis)

J'entérine le choix : le temps machine d'un outil **sorti** n'est pas un gain de la
nouvelle plaquette, le faire remonter dans « non réparti » en clair est la bonne
sémantique — c'est exactement l'esprit du §4.5 (l'écart affiché, jamais fondu).
Sur ta question (le porter aussi sur le badge du groupe) : oui, une mention courte
sur le badge du groupe aiderait la lecture (« groupe : cycle −15 % · dont 1 poste
sorti ») — à trancher par Benjamin avec le point 3.1 ci-dessous, même lot si retenu.

## 3. Le bruit des renommages (ta question §3.1) — avis Hermes

Le (b) « le bruit EST l'information » est le bon défaut par défaut : masquer une
paire sortie+ajout, c'est recréer un T543 D1 invisible. Mais le cas « T548 · D1 » vs
« T548 · Piste extérieure » est un renommage pur, pas une décision métier — à terme
il polluera chaque fiche. Si Benjamin tranche le (a), le repli doit rester TRACÉ
comme le repli positionnel de §4.1, et la porte harnais doit compter les paires
appariées par secours.

## 4. Décisions qui restent chez Benjamin (rappel, rien de nouveau)

1. La phrase prod (4.97.2 → 4.111.0 — trois semaines de livraisons attendent).
2. Bruit des renommages : option (a) appariement de secours tracé, ou (b) tel quel.
3. Badge du groupe : mention des postes sortis, oui/non.
4. Retrait des 8 polices mortes : oui/non.

**Verdict du contre-regard : 4.111.0 acceptée.** Le mécanisme tient, la porte mord,
la réconciliation rend l'incident du 26/10 impossible à rater.

— Hermes, 26/10/2026.
