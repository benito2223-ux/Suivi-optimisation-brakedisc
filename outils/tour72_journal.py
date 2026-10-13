# -*- coding: utf-8 -*-
"""Tour 72 : CHANGELOG 4.89.0 + liberation du verrou + entree de journal."""

c = open('CHANGELOG.md', encoding='utf-8').read()
entree = """## [4.89.0] — 2026-10-14 · Tour 72

**L'autocomplete du catalogue à la saisie — le dernier morceau du socle
commercial.** Taper un MABEC ou un ISO dans un logement propose les articles
du catalogue et remplit d'un clic.

### Ajouté
- **datalists natifs** (`catMabec`, `catIso`) : zéro framework, la règle
  maison ; alimentés depuis le catalogue au démarrage, à l'ouverture du
  panneau 📚 et après chaque changement du catalogue ;
- **`appliquerSuggestionCatalogue()`** (pure) : un MABEC tapé (même en
  minuscule) remplit **codeArticle et prix TOUJOURS** (un MABEC = un prix —
  décision Benjamin), l'**ISO, les arêtes et la DDV seulement si vides** —
  ce qui est saisi à la main n'est jamais écrasé ;
- **`catalogueParIso()`** : recherche par désignation ISO, insensible à la
  casse et aux espaces, multi-ISO gérée (le séparateur « | » du seed) ;
- 5 tests.

### Le contre-regard qui a renforcé le test
La porte initiale comparait un logement DÉJÀ aux valeurs du catalogue —
aveugle par construction. Renforcée : un ISO saisi à la main DIFFÉRENT doit
rester intact. Faute injectée (garde « si vide » sautée) → **vue** (l'ISO
manuel écrasé) → restaurée par copie, empreinte identique. 521 → **551/551
verts** depuis la 4.86.

"""
ancre = "## [4.88.0]"
assert ancre in c
c = c.replace(ancre, entree + ancre, 1)
open('CHANGELOG.md', 'w', encoding='utf-8').write(c)
print("changelog 4.89.0")

v = open('VERROU.md', encoding='utf-8').read()
i = v.find("| **Auteur** | Z Code |")
j = v.find("\U0001F512", i)
assert i > -1 and j > i, "bloc verrou pris introuvable"
v2 = ("""| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Écrit dans** | — |
| **Version visée** | — |
| **Sujet** | *Personne n'écrit dans `bilan_economique.html`.* |

""" + "✅ **Verrou libéré par Z Code le 14/10/2026** (Tour 72, v4.89.0). Pendant le\n"
"tour, `bilan_economique.html` est passé à l'empreinte post-patch : les\n"
"suggestions à la saisie (`catalogueSuggestion()`, `catalogueParIso()`,\n"
"`appliquerSuggestionCatalogue()` — pures et exportées), datalists natifs\n"
"`catMabec`/`catIso` alimentés au démarrage et aux changements du catalogue,\n"
"attributs `list=` sur les champs MABEC/ISO du logement, crochet dans\n"
"`writeFieldValue` (la branche logement), `TOOL_VERSION = \"4.89.0\"`,\n"
"NOUVEAUTES + CHANGELOG. Contre-regard : la porte initiale était aveugle\n"
"(logement déjà aux valeurs du catalogue) — **renforcée** (ISO manuel\n"
"DIFFÉRENT doit rester), faute injectée → **vue** → restaurée par copie,\n"
"empreinte identique, 521 → **551/551 verts**. **Déployé sur Projet,\n"
"vérifié curl ; la PROD attend la phrase de Benjamin.** Écrits :\n"
"`bilan_economique.html`, `outils/patch_4890_a.py`, `outils/verrou_t72.py`,\n"
"`build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`.\n\n"
+ v[j:])
open('VERROU.md', 'w', encoding='utf-8').write(v2)
print("verrou libere")

s = open('ECHANGES.md', encoding='utf-8').read()
tour = """### Tour 72 — 14/10/2026 soir — **Z Code** (v4.89.0 — l'autocomplete du catalogue à la saisie)

**La commande.** Benjamin : « envoie les suggestions à la saisie
(l'autocomplete du catalogue) — le dernier morceau du socle commercial ».
Verrou pris AVANT l'écriture cette fois (par fichier — la règle tient).

**Livre.** Dans la fiche logement, les champs **MABEC** et **Référence
plaquette (ISO)** ont leurs datalists natifs : taper propose les articles du
catalogue, et `appliquerSuggestionCatalogue()` remplit d'un changement —
**MABEC et prix TOUJOURS** (un MABEC = un prix, décision Benjamin),
**ISO/arêtes/DDV si vides**. Ce qui est saisi à la main n'est jamais écrasé.
`catalogueParIso()` cherche par ISO insensible casse/espaces, multi-ISO géré.
Zéro framework : datalists HTML alimentés au boot et aux changements du
catalogue.

**Le contre-regard qui a renforcé le test.** La porte initiale comparait un
logement déjà aux valeurs du catalogue : aveugle par construction (la leçon
4.74.1, encore). Renforcée — un ISO manuel DIFFÉRENT doit rester — faute
injectée (garde sautée) → **vue** (l'ISO manuel écrasé par le catalogue) →
restauration par copie, empreinte identique, 521 → **551/551 verts** depuis
la 4.86.

**Déploiement.** Projet, vérifié curl. La prod attend la phrase de Benjamin.

**Prochain tour** : la revue d'Hermes ; l'export de l'accueil ; le chantier
UI de fond (les maquettes « ton sur ton »).

"""
ancre = "## Questions ouvertes \u00e0 Z Code"
assert ancre in s
s = s.replace(ancre, tour + ancre, 1)
open('ECHANGES.md', 'w', encoding='utf-8').write(s)
print("tour 72 ecrit")
