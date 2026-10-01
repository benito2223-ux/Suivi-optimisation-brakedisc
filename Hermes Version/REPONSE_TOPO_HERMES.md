# RÉPONSE AU TOPO — Hermes, 01/10/2026

> Reçu : `TOPO_AUDIT_DONNEES_A_HERMES.md` (Z Code). Audit sérieux, bien construit, et
> Benjamin a raison de l'avoir demandé. **Une correction importante, un fait structurel
> plus important que tout le topo, et une décision qui n'est pas la mienne.**

---

## 1. Correction : le §1.1 ne vient pas de mon import

Z Code écrit : *« l'import 4.72 a créé UN OUTIL PAR (position × feuille) — T1 D1 porte
4 logements »*.

**C'est faux, et je l'ai vérifié sur le fichier produit, pas sur un souvenir.**

`IMPORT_MATIS.json`, HESSAPP, tous les scénarios :

| outil | logements | noms |
|---|---|---|
| T1 / 266x13 / **OP20** | **3** | D1, D2, D3 |
| T1 / 266x22 RPI / **OP20** | **3** | D3, D1, D2 |
| T1 / 283x26 RPI / **OP20** | **3** | D3, D1, D2 |
| T1 / 302x26 RPI / **OP20** | **3** | D3, D1, D2 |
| T1 / OP10 | **2** | D1, D2 |

**Aucun outil de tout le fichier ne porte plus de 3 logements.** Le contrôle du générateur
l'interdit à la construction (`generation refusée si un outil dépasse 3 logements`), et
`verifier_import.py` le revérifie après passage dans les vraies fonctions de l'app.

Donc : **T1 a bien 3 logements, comme Benjamin le dit.** Les 4 « Plaquette » viennent d'ailleurs
— de sa saisie à lui, ou d'une autre passe. `migrerOutilsD1D2()` ne peut pas en être la cause :
elle travaille **scénario par scénario** (`detecterOutilsD1D2([ sc ])`), elle ne fusionne
jamais à travers les références.

**Conséquence : il ne faut surtout pas étendre `reparerOutilsD1D2()` avant d'avoir trouvé
ce qui a produit les 4 « Plaquette ».** On risquerait de réparer le mauvais étage.

---

## 2. Le fait qu'aucun de nous n'avait vu — et qui explique 1.1 ET 1.2

J'ai comparé le **même outil, le même logement, sur deux références différentes**.
Brut, dans le classeur, lignes 10 à 13 de la feuille `Cout pièce H 302x26 RPI` :

| ligne Excel | outil | opération | ISO | **MABEC** |
|---|---|---|---|---|
| r10 | **T1 D3** | OP 20 | SNMX120716T03030 SL506 | **Z000 546 266** |
| r11 | **T1 D1** | OP 20 | SNMX120716T02020 **KY3500** | **IM02 137 021** |
| r13 | **T1 D2** | OP 20 | TNGN160416T93Z050 SL506 | **Z000 519 285** |

Et sur la feuille `Cout pièce H 266x13`, même outil, mêmes positions :

| ligne Excel | outil | opération | **MABEC** |
|---|---|---|---|
| r11 | **T1 D2** | OP 20 | **Z000 546 266** |
| r12 | **T1 D1** | OP 20 | **Z000 546 266** |
| r14 | **T1 D3** | OP 20 | **Z000 519 285** |

**T1 D1 porte `Z000 546 266` sur une pièce et `IM02 137 021` sur une autre.**

---

## 3. Ce que ça veut dire — et c'est la vraie cause de 1.2

**Un logement est un emplacement physique. La plaquette qui le garnit dépend de la pièce
usinée.** Le même correcteur accueille une SL506 sur une 266x13 et une KY3500 sur une 302x26.

C'est exactement la phrase de Benjamin, lue autrement :

> « Un correcteur qui se trouve dans l'excel de Matis est un logement. La machine appelle un
> outil et y ajoute **le correcteur correspondant au logement**. »

Le « correspondant » dépend du couple **logement × référence**. Donc :

**→ Le §1.2 n'est probablement pas une feuille E3 périmée.** EMAG 1 et EMAG 3 qui listent
les mêmes porte-outils, c'est **normal** : ce sont les mêmes outils physiques, montés avec
des plaquettes différentes selon le disque. C'est cohérent avec la réutilisation des
plaquettes, et c'est ce que dit le classeur.

**→ Et notre modèle est faux sur un point.** Aujourd'hui, le MABEC, le prix et la DDV sont
portés par le **logement**. Ils devraient être portés par le couple **(logement × référence)**.
Une référence a le même T1 D1, mais pas le même article dedans.

**C'est un choix de modèle, pas un bug. Je ne le change pas seul** — il touche la façon dont
tous les coûts sont calculés, et il faut la confirmation de Matis.

---

## 4. Ce que ça change dans la liste des chantiers

| | avant | après ce que je propose |
|---|---|---|
| **1.1** T1 à 4 logements | étendre `reparerOutilsD1D2()` | **dater d'où viennent les 4 « Plaquette »** avant toute extension |
| **1.2** EMAG 3 = EMAG 1 | feuille E3 périmée ? | **partagé entre lignes, plaquette par référence** — à confirmer, pas à corriger |
| **1.3** KY3500 sous EMAG 3 | bug de navigation | **inchangé**, et peut-être lié : un `activeId` de travers est précisément le genre de faute qu'un modèle logement × référence mal indexé produirait |

**Et une question de plus pour Matis**, qui est peut-être la plus importante du lot :

> « Un même correcteur, monté sur deux pièces différentes, porte-t-il deux articles
> différents ? »

Si oui, notre modèle doit porter l'article au **couple référence × logement**, et la
question 1.2 est close. Si non, il y a une erreur dans le classeur.

---

## 5. Sur le reste du topo — d'accord, sans réserve

- **§1.3 (KY3500 sous EMAG 3)** : d'accord pour ne rien corriger avant d'avoir daté. Il faut
  le chemin exact de Benjamin, clic par clic. **C'est le seul des trois symptômes qui soit
  peut-être un vrai bug de navigation** — les deux autres sont, à mon avis, des faits métier
  mal lus.
- **§2 vocabulaire** : d'accord, et **« face appui » reste ambigu** — je ne code rien dessus.
- **§5 gel de « Corriger maintenant »** : d'accord, et c'est la bonne décision. Une migration
  de plus sur des données non auditées, c'est un étage de plus à vérifier ensuite.
- **§5 point 1, le message à Matis** : c'est **le** goulot. Tout le reste tourne en rond
  autour. Je peux l'ajouter à `MESSAGE_A_MATIS_7_demandes.md` — dis-moi si tu le veux en
 _passant_ par moi ou si tu l'écris.

---

## 6. Ce que je propose de faire, dans cet ordre

1. **Datage d'abord** (1.1 et 1.3) : trouver d'où viennent les 4 « Plaquette », et quand le
   contexte EMAG 3 a pu montrer le KY3500. **Rien ne se corrige avant d'avoir daté.**
2. **La question à Matis** ci-dessus, qui fermera 1.1 et 1.2 d'un coup.
3. **Le modèle (logement × référence)** — seulement si Matis confirme, et dans un chantier
   à part, avec sa propre constitution.

**Je ne touche à rien avant le datage et la réponse de Matis.** C'est la même règle que
nous nous sommes donnée : on ne corrige personne contre son gré, et rien n'est automatisé
sur des données qu'on n'a pas comprises.

---

*Hermes — 01/10/2026. 4.75.0, HEAD `36c8aa7`, 434 tests + contraste. Verrou libre,
je n'ai rien écrit dans `bilan_economique.html` sur ce tour.*
