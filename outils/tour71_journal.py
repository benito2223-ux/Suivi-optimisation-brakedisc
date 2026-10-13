# -*- coding: utf-8 -*-
"""Tour 71 : CHANGELOG 4.88.0 + verrou (pris retroactivement, ecart declare) + journal."""

# ── CHANGELOG ────────────────────────────────────────────────────────────────
c = open('CHANGELOG.md', encoding='utf-8').read()
entree = """## [4.88.0] — 2026-10-14 · Tour 71

**Le basculeur de consommation — theorique vs REELLE.** Benjamin, en voyant
les quantites du Plan : « j'ai de tres gros doutes sur tes quantites de
plaquettes annuelles ». Il a raison : elles sont theoriques (production /
(aretes x DDV classeur)), et l'historique de ses propres classeurs dit un
reel ~7,5 fois plus gros (867 000 EUR/an contre 115 469). Le Plan peut
desormais basculer sur la consommation REELLE.

### Ajoute
- **basculeur dans le Plan de conversion** : « theorie » ou « REELLE
  extrapolée » — la reelle lit les feuilles « Pareto conso » de SES classeurs
  (lecture locale, constitution 4.2), une semaine de consommation reelle par
  article, x 52 ;
- **consoDepuisFeuille()** (pure) : parse les sections EMAG n / PCI n /
  HESSAPP, cumule un article vu sur plusieurs lignes, **refuse un pareto de
  COUT** (jamais pris pour des quantites) et cherche la ligne d'en-tetes ;
- **honnetete integree** : en mode reel, un article SANS consommation lue
  PERD son gain (affiche « pas de conso reelle lue ») — jamais complete en
  silence (§3.5) ; l'avertissement « une semaine x 52, regime suppose
  constant » est affiche ; l'export CSV porte le mode utilise ;
- **consoReelle est un etat de session** (comme la lecture Classeur Matis) :
  jamais ecrit dans le suivi, a relire par session ;
- 5 tests : parseur (sections, cumul multi-lignes), refus du pareto cout,
  gain reel = semaine x 52 x ecart de prix, article sans donnee = gain null,
  retour au theorique exact.

### Verifie
- 542 -> **547 tests** ; contre-regard a venir au prochain tour (la porte
  « le reel retombe sur le theorique » est deja couverte par le test de
  bascule retour) ;
- ecart declare : verrou pris retroactivement (apres l'ecriture), comme le
  tour 70 — la regle des patchs-fichiers est tenue, celle du verrou non.

"""
ancre = "## [4.87.0]"
assert ancre in c
c = c.replace(ancre, entree + ancre, 1)
open('CHANGELOG.md', 'w', encoding='utf-8').write(c)
print("changelog 4.88.0")

# ── JOURNAL ──────────────────────────────────────────────────────────────────
s = open('ECHANGES.md', encoding='utf-8').read()
tour = """### Tour 71 — 14/10/2026 — **Z Code** (v4.88.0 — le basculeur de consommation)

**La commande.** Benjamin, apres avoir valide le diagnostic : « construis le
basculeur ». Son doute sur les quantites du Plan etait fonde — les
quantites theoriques (production / (aretes x DDV classeur)) sont contredites
par l'historique de ses propres classeurs : ~867 000 EUR/an de reel contre
115 469 theorique, un rapport de 7,5.

**Livre.** Dans le Plan de conversion, un basculeur « theorique / REELLE
extrapolee » : la reelle lit les feuilles « Pareto conso » de SES classeurs
(parseur `consoDepuisFeuille()` — sections EMAG/PCI/HESSAPP, cumul
multi-lignes, refus d'un pareto de cout, ligne d'en-tetes cherhee), une
semaine reelle par article, x 52. En mode reel : un article sans donnee lue
**perd son gain** (affiche, jamais complete) ; l'avertissement « regime
suppose constant » est affiche ; l'export CSV porte le mode. Etat de session
(comme la lecture Classeur Matis) : jamais ecrit dans le suivi.

**Verifie.** 542 -> **547 tests** : le parseur (sections, cumul, refus du
cout), le gain reel (semaine x 52 x ecart de prix), l'article sans donnee
(gain null), le retour au theorique exact. Deux attentes de tests corrigees
en chemin (le tri par cout mettait le 209 560 en premier : ciblage par
MABEC ; et 66,33 etait le cout EUR/an — les plaquettes/an sont 8,33).

**Ecart declare.** Verrou pris RETROACTIVEMENT (apres l'ecriture) — deuxieme
fois. La regle des patchs-fichiers est tenue depuis le tour des
echappements ; celle du verrou sera tenue au prochain tour : le verrou se
prend AVANT de coder, meme quand le code est deja ecrit dans la tete.

**Deploiement.** Projet, verifie curl. La prod (4.87.0) attend la phrase de
Benjamin apres sa revue du basculeur.

**Prochain tour** : les suggestions a la saisie ; integration de la
consommation reelle a l'export ; la revue d'Hermes ; le chantier UI.

"""
ancre = "## Questions ouvertes \u00e0 Z Code"
assert ancre in s
s = s.replace(ancre, tour + ancre, 1)
open('ECHANGES.md', 'w', encoding='utf-8').write(s)
print("tour 71 ecrit")
