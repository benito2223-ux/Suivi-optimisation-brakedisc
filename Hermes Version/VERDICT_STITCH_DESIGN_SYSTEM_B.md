# Verdict sur la proposition Google Stitch — Design System B

> Demandé par Benjamin le 30/09/2026. Analyse des 2 captures, du `Design_system_B.md` et du
> HTML généré. **Aucun code écrit dans l'outil. Décision à trancher par Benjamin.**

---

## 1. Le verdict en une phrase

**Le design est le meilleur qu'on ait eu sur ce projet — et le fichier contient des chiffres
qu'on ne peut pas justifier, plus quatre dépendances réseau qui cassent l'outil hors ligne.**

Donc : **on prend la peau, on refuse le reste.**

---

## 2. Ce qu'il faut garder — et c'est beaucoup

### 2.1 Les tokens (`Design_system_B.css`)

30 lignes qui remplacent 13 valeurs de rayon, 6 polices et 3 blocs `:root`. C'est exactement
le chantier C1 + C5 de notre demande, **fait et écrit**.

| Token | Valeur | Notre actuel | Verdict |
|---|---|---|---|
| `--radius` | **2px** | 13 valeurs (2 à 999px) | ✅ une seule |
| `--red` | `#E30045` | `#E2001A` | ✅ plus net |
| `--blue` | `#006AB3` | `#1B5EA6` | ✅ plus lisible sur blanc |
| `--gray-100/200/300` | 3 gris | non nommés | ✅ nommés |
| `--ink/--body/--label` | 3 niveaux de texte | `--ink/--ink-soft/--ink-faint` | ✅ même idée, mieux |
| `--font` | 1 famille | 6 déclarées | ⚠️ à garder **locale** |

**Les 4 gris + 1 rouge + 1 bleu, c'est exactement le budget qu'on s'était fixé.** Il a trouvé
la cible tout seul.

### 2.2 La grammaire visuelle

- **l'accent à gauche de 2-3 px sur les cartes** — c'est le détail qui fait « fait pour ça »
  plutôt que « maquette » ;
- **le chiffre en 36-38 pt avec son unité** — la valeur se lit sans effort ;
- **le bandeau de 2 px rouge + bleu sous l'en-tête** — signature CeramTec, sobre ;
- **les champs à soulignement seul** (pas d'encadré) — plus lisible qu'une boîte, et
  conforme à l'esprit atelier ;
- **les boutons cercle + chevron** — moins de masse, plus de cible tactile ;
- **les transitions courtes** (`duration-100`, `duration-150`) — exactement le 80-150 ms
  qu'on demandait en C4.

### 2.3 Il a compris nos règles — et c'est la vraie surprise

Sans qu'on les lui donne, la capture 2 applique :

- **§3.4 — gains actés et projetés jamais sommés** : `+84 250 €/an` et `+26 600 €/an` sont
  dans **deux blocs distincts**, jamais fusionnés ;
- **le projeté marqué en rouge** avec « non signé optimisation/outillage » — exactement notre
  exigence des Tours 11→14 ;
- **§3.5 — le poste neutre déclaré** : T04 porte `±0.000 €` au lieu de disparaître ;
- **l'absence dite, pas devinée** : « Oct 2026 — data-gap fort », « Aucun essai scellé ».

**Un générateur visuel qui respecte une constitution qu'il n'a pas lue, c'est la preuve que
la constitution est la bonne.**

---

## 3. Ce qu'il faut refuser — et pourquoi

### 3.1 Les chiffres — le vrai danger

Les chiffres de Stitch sont **très plausibles et faux**. Il les signale lui-même
(« data-gap fort »), mais il les affiche quand même en 36 pt en haut d'écran.

| Chiffre proposé | Ce qu'on sait |
|---|---|
| EMAG 1 356x26 : **120 000 pcs/an** | le classeur de Matis dit **6 781** — facteur 18 |
| **88,4 %** de ralliement cible | aucun calcul réel ne le produit aujourd'hui |
| **+84 250 €/an** consolidé | agrégat sur périmètre non vérifié |
| **+37 800 €** sur OP10 | dépend du volume ci-dessus |
| **1.200 €** cible CPP | valeur plausible, **non confirmée** |
| **91,3 %** de cible atteinte | calculé sur la cible ci-dessus |

**C'est précisément le défaut que nous avons passé un tour à corriger en 4.60.1** : un
agrégat partiel qui a l'air d'un total, juste parce qu'il est écrit gros et propre.

> **Règle à écrire dans la constitution :**
> **Si on ne peut pas remonter à la source du chiffre, il n'a pas le droit d'être affiché.**
> Un chiffre non justifié ne devient pas un chiffre parce qu'il est joli.

Et cette règle vaut **pour nous deux**, pas seulement pour Stitch.

### 3.2 Les dépendances réseau — l'outil casse hors ligne

Le HTML charge :

1. `cdn.tailwindcss.com` — **tout le style**
2. `fonts.googleapis.com` (Roboto Flex)
3. `fonts.googleapis.com` (Material Symbols)
4. une image `lh3.googleusercontent.com`

**Sur le poste de Matis, sans réseau : l'écran est blanc.** Ce n'est pas une dégradation,
c'est une panne totale. Et c'est contraire à la contrainte fondatrice : un fichier unique,
hors ligne, sans build.

### 3.3 La refonte du produit — le brief propose une autre application

Le `Design_system_B.md` ne parle pas d'habiller l'outil : il décrit **4 écrans, une matrice
d'entités, des formulaires de saisie, un comparateur**. C'est un produit différent du nôtre.

Utile comme **vision**. Dangereux comme **spec** : si Z Code suit ça ligne à ligne, il
réécrit l'outil au lieu de l'habiller — et on perd 4.62.0, les 351 tests, et le modèle qui
tourne.

Le brief dit « conformes Constitution §3.2 » — il a compris nos règles mieux que nous, et il
les applique mal : §3.4 dit « **ne jamais** sommer », et son bandeau les additionne.

---

## 4. Ce que je propose de faire

**C1' — Les tokens, Don B, tels quels.** 30 lignes. Ça règle la guerre des `:root`, les
13 rayons, les 6 polices et le bleu terne. Un commit, testable en 5 minutes, réversible seul.

**C2' — Supprimer les dépendances réseau.** Tout Tailwind → CSS local. Aucune police
distante. Aucune image distante. Test d'acceptation : **ouvrir le fichier avec le réseau
coupé.**

**C3' — L'accent à gauche et la typo des chiffres**, repris de la capture 1, sur nos tuiles
existantes. Sans toucher au contenu.

**Ce qu'on ne fait pas** : pas de comparateur, pas de formulaire, pas de matrice, pas de
4 écrans. On habille, on n'invente pas.

---

## 5. Les questions, avec des choix

### Q1 — Que fait-on de la proposition ?

### Q2 — Les chiffres de Stitch, on les traite comment ?

---

## 6. La phrase à retenir

**Stitch a dessiné un excellent outil avec des données qu'il n'a pas.**
Nous, on a un excellent outil avec des données qu'on n'a pas encore.
**La seule tâche qui compte, ce n'est ni l'un ni l'autre : c'est de remplir cet outil avec
les vraies données de Matis — et c'est pour ça que le message aux 7 demandes est en attente.**
