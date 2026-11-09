# -*- coding: utf-8 -*-
"""Tour 134 — correctif 2 des tests étape 2 (états résiduels du fixture)."""
import io

P = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/bilan_economique.html"
src = io.open(P, "r", encoding="utf-8", newline="").read()

def repl(s, old, new, label):
    for attempt in (old, old.replace("\n", "\r\n")):
        n = s.count(attempt)
        if n == 1:
            return s.replace(attempt, new)
        if n != 0:
            raise SystemExit("ANCRE '%s' : %d occurrences" % (label, n))
    raise SystemExit("ANCRE INTROUVABLE : %s" % label)

src = repl(src,
"""    ecrireConditionsGroupe(membres, "modeVitesse", "G97");
    ecrireConditionsGroupe(membres, condChampVitesse("G97"), 700);
    ok("etape2 : G97 — S rangée dans sBroche, vc jamais touché, libellé tr/min", [membres[0].logements[0].sBroche, membres[0].logements[0].vc, membres[1].logements[0].sBroche, condLabelVitesse("G97")], [700, "", 700, "S <span>tr/min</span>"]);""",
"""    const vcAvant = membres[0].logements[0].vc;
    ecrireConditionsGroupe(membres, "modeVitesse", "G97");
    ecrireConditionsGroupe(membres, condChampVitesse("G97"), 700);
    ok("etape2 : G97 — S rangée dans sBroche, la Vc existante jamais touchée, l'outil hors groupe intact", [membres[0].logements[0].sBroche, membres[0].logements[0].vc === vcAvant, membres[1].logements[0].sBroche, scT.outils[2].logements[0].sBroche, condLabelVitesse("G97")], [700, true, 700, "", "S <span>tr/min</span>"]);""", "fix-g97")

src = repl(src,
"""    const bloc96 = conditionsGroupeHTML(scT, groupesSimultanes(scT)[0], false);""",
"""    ecrireConditionsGroupe(membres, "modeVitesse", "");  /* retour à « non renseigné » pour lire le libellé par défaut */
    const bloc96 = conditionsGroupeHTML(scT, membres, false);""", "fix-bloc96")

io.open(P, "w", encoding="utf-8", newline="").write(src)
print("correctif 2 appliqué")
