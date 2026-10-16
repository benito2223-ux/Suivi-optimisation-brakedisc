# -*- coding: utf-8 -*-
"""Tour 69 : CHANGELOG + liberation du verrou + entree de journal."""

# ── CHANGELOG ────────────────────────────────────────────────────────────────
c = open('CHANGELOG.md', encoding='utf-8').read()
entree = """## [4.86.0] — 2026-10-14 · Tour 69

**Le Plan de conversion — le pas-a-pas commercial.** La demande de Benjamin :
montrer a Matis, article par article et au bon moment, ce que vaut le passage
sur les plaquettes SPK — premiere correspondance actee : toute KY3500 1207
(SNMX/CNMX/SNGX/CNGX) = LKT640 a 5 EUR.

### Ajoute
- **Plan de conversion** (pied de l'accueil) : chaque article de production
  avec son prix (du catalogue), sa consommation (EUR/an et plaquettes/an), la
  **cible SPK editable** — auto-suggeree pour les ISO KY3500 (meme geometrie,
  LKT640, 5 EUR) — et le **gain/an = plaquettes/an x ecart de prix** ;
- **les etats step-by-step** : a proposer / proposee / en essai / gagnee —
  poses par Benjamin, ligne par ligne ; **le total de la promesse ne compte
  que les lignes etatees**, le reste reste du potentiel (null, pas un
  chiffre) ;
- **le plan persiste dans le suivi** (payload, loadAll, migration, import
  remplace/fusion) ; **export CSV** pour la reunion.

### Verifie
- 521 -> **542 tests** ; sur la v5 reelle, les lignes KY3500 activees a 5 EUR
  donnent **-21 932 EUR/an** de promesse (le 513 527, geometrie DWG, a un
  prix cible a ajuster a la main — le panneau est editable pour ca) ;
- contre-regard : le potentiel compte comme promesse -> **vu** -> restaure
  par copie, empreinte identique ;
- le tour des echappements (accros assumes, tous vus par le harnais ou
  node --check) : echappements deformes par les heredocs (regex, BOM/CRLF,
  apostrophe), patch sans ecriture, copie perimee. Regle nouvelle : **les
  patchs passent par des fichiers, jamais par des heredocs**.

"""
ancre = "## [4.85.0]"
assert ancre in c
c = c.replace(ancre, entree + ancre, 1)
open('CHANGELOG.md', 'w', encoding='utf-8').write(c)
print("changelog 4.86.0")

# ── VERROU : liberation ──────────────────────────────────────────────────────
v = open('VERROU.md', encoding='utf-8').read()
av = """| **Auteur** | Z Code |
| **Pris le** | 14/10/2026 matin |
| **Ecrit dans** | `bilan_economique.html` |
| **Version visee** | 4.86.0 |"""
# le fichier porte les accents ; on remplace par le bloc complet connu
av2 = None
i = v.find("| **Auteur** | Z Code |")
j = v.find("🔒", i)
assert i > -1 and j > i, "bloc verrou introuvable"
v2 = ("""| **Auteur** | *(libre)* |
| **Pris le** | — |
| **Ecrit dans** | — |
| **Version visee** | — |
| **Sujet** | *Personne n'ecrit dans `bilan_economique.html`.* |

""" + "OKVERROUPLACEHOLDER" + v[j:])
v2 = v2.replace("OKVERROUPLACEHOLDER",
"""**Verrou libere par Z Code le 14/10/2026** (Tour 69, v4.86.0). Pendant le
tour, `bilan_economique.html` est passe a l'empreinte `ac9563a1...` : le Plan
de conversion (cibles SPK editables, auto-suggestion KY3500 -> LKT640 a 5 EUR,
etats step-by-step de Benjamin, total = lignes etatees seulement, gain =
plaquettes/an x ecart de prix, persistant dans le suivi, export CSV), portes,
`TOOL_VERSION = "4.86.0"`, NOUVEAUTES + CHANGELOG. Contre-regard : potentiel
compte comme promesse -> **vu** -> restauration par copie, empreinte
identique, 521 -> **542/542 verts**. Le tour des echappements consigne :
patchs par fichiers, heredocs bannis. **Deploye sur Projet ET en prod
(phrase de Benjamin : « fonce pour le Plan de conversion et deploie en
prod »), verifies curl — empreinte ac9563a1 identique aux deux domaines.**
Ecrits : `bilan_economique.html`, `outils/patch_4860_a/b/c.py`,
`outils/fix_plancsv*.py`, `build_harness.py`, `CHANGELOG.md`, `ECHANGES.md`,
`VERROU.md`.""")
open('VERROU.md', 'w', encoding='utf-8').write(v2)
print("verrou libere")

# ── JOURNAL : tour 69 ────────────────────────────────────────────────────────
s = open('ECHANGES.md', encoding='utf-8').read()
tour = """### Tour 69 — 14/10/2026 — **Z Code** (v4.86.0 — le Plan de conversion, et la prod rattrapee)

**La commande.** Benjamin : « fonce pour le Plan de conversion et deploye en
prod » — la vitrine de sa demarche commerciale : montrer a Matis, ligne par
ligne et au bon moment, ce que vaut le passage sur les plaquettes SPK.
Premiere correspondance actee : toute KY3500 1207 = LKT640 a 5 EUR.

**Livre.** Le panneau Plan de conversion : chaque article de production avec
son prix (du catalogue), sa consommation (EUR/an + plaquettes/an), la **cible
editable** (auto-suggeree KY3500 -> LKT640 a 5 EUR), le **gain/an**
(plaquettes/an x ecart de prix), et **les etats de Benjamin** : a proposer /
proposee / en essai / gagnee. **Le total ne compte que les lignes etatees** —
le reste affiche « potentiel », jamais un chiffre. Le plan persiste dans le
suivi et s'exporte en CSV.

**Sur la v5 reelle** : les KY3500 activees a 5 EUR donnent **-21 932 EUR/an**
de promesse — avec la nuance assumee que le 513 527 (geometrie DWG, pas 1207)
a un prix cible a ajuster a la main : le panneau est editable pour ca.

**Le tour des echappements** — accros assumés, tous vus par le harnais ou
node --check avant livraison : echappements deformes par les heredocs (regex,
BOM/CRLF, apostrophe), un patch sans ecriture, une copie perimee. Regle
nouvelle consignee : **les patchs passent par des fichiers ecrits, jamais par
des heredocs echappes** — le shell deforme les sequences.

**Contre-regard.** Le potentiel compte comme promesse -> **vue**
(`recu= [false, 24.67]`, `attendu= [false, null]`) -> restauration par copie,
empreinte identique, 521 -> **542/542 verts**. Deux attentes de tests
corrigees avant le vert (66,33 etait le cout EUR/an, pas les plaquettes/an —
8,33 : prod / (aretes x charniere)).

**Deploiement.** Projet ET prod (phrase recue), verifies curl : empreinte
ac9563a1 identique aux deux domaines, 1 464 071 octets.

**Prochain tour** : les suggestions a la saisie ; la revue d'Hermes ; le
chantier UI ; l'export de l'accueil.

"""
ancre = "## Questions ouvertes a Z Code"
if ancre not in s:
    ancre = "## Questions ouvertes \u00e0 Z Code"
assert ancre in s, "ancre journal introuvable"
s = s.replace(ancre, tour + ancre, 1)
open('ECHANGES.md', 'w', encoding='utf-8').write(s)
print("tour 69 ecrit")
