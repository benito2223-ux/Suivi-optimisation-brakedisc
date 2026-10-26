# -*- coding: utf-8 -*-
"""Tour 93 — v4.110.0 — recalage après premier passage harnais.

1. `badgeCodifScenario` : le hors-exigence (base excel / sans article) est
   géré par une branche EXPLICITE — la porte 4.110 le lit dans le corps de
   la fonction, et c'est plus lisible que le repli muet.
2. Porte « coque 4.100 » recalée sur la réalité 4.109 : elle cherchait
   « Barlow Condensed » dans spk-app.css — périmée depuis que les polices
   de la coque sont passées au brand guide (Tour 91). Désormais : la coque
   déclare Open Sans Condensed, et Barlow Condensed y est bannie."""
import io

def remplace(p, avant, apres, label):
    s = io.open(p, encoding="utf-8").read()
    n = s.count(avant)
    assert n == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, n)
    s = s.replace(avant, apres, 1)
    io.open(p, "w", encoding="utf-8").write(s)
    print("ok :", label)

# ── 1. la branche explicite du hors-exigence ─────────────────────────────────
remplace(
    "bilan_economique.html",
    "function badgeCodifScenario(sc){\n"
    "  const cod = codificationScenario(sc);\n"
    "  if(cod.etat === \"codifie\")",
    "function badgeCodifScenario(sc){\n"
    "  const cod = codificationScenario(sc);\n"
    "  if(cod.etat === \"sansExigence\" || cod.etat === \"sansArticle\") return \"\";\n"
    "  if(cod.etat === \"codifie\")",
    "1. hors-exigence explicite dans badgeCodifScenario",
)

# ── 2. la porte coque suit le brand guide ────────────────────────────────────
remplace(
    "build_harness.py",
    "    if (css.indexOf('Barlow Condensed') === -1) echecs.push('les polices de la coque ne sont pas declarees');",
    "    /* v4.109 (brand guide SPK, Tour 91) : les polices de la coque sont\n"
    "       Open Sans Condensed / Open Sans — Barlow/Public Sans de\n"
    "       l'auto-designer sont retirées. La porte suit : la déclaration\n"
    "       doit être là, et la police retirée ne doit pas revenir. */\n"
    "    if (css.indexOf(\"'Open Sans Condensed'\") === -1) echecs.push('les polices de la coque ne sont pas au brand guide (Open Sans Condensed absente)');\n"
    "    if (css.indexOf('Barlow Condensed') !== -1) echecs.push('la police retirée Barlow Condensed est de retour dans la coque');",
    "2. porte coque recalée brand guide",
)

print("recalage posé")
