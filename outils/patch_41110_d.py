# -*- coding: utf-8 -*-
"""Tour 94 — v4.111.0 — deux attentes de test recâlées (le code était juste).

1. Avec chrono complet, `non réparti` = +15 000 €/an : le temps machine de
   l'outil SORTI (T543, 120 s × taux × volume) ne peut pas entrer dans un
   levier d'outil apparié — la réconciliation le met en clair, exactement le
   rôle voulu (§4.5 : « si un écart subsiste, il est affiché en clair »).
2. Le groupe simultané ne porte que ses membres APPARIÉS : le max côté
   référence vaut 60 s (T541/T548), pas 120 s — T543 n'a plus de pendant
   côté candidat et sort déjà en « non réparti ». Le levier vaut donc
   (60 − 50) s = 1 250 €/an, pas 8 750."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


remplace(
"""        const vpoC = verdictParOutil(candT, Object.assign({}, cfgV), { coutHoraire: "45" }, refV, baseT);
        ok("verdict par outil : chrono complet — le levier productivité au centime (série : les temps se déduisent)",
           [vpoC.chronoComplet,
            Math.round(vpoC.outils[0].prodEurAn),
            Math.round(vpoC.outils[1].prodEurAn),
            Math.round(vpoC.nonReparti)],
           [true, 1250, 1250, -2500]);""",
"""        const vpoC = verdictParOutil(candT, Object.assign({}, cfgV), { coutHoraire: "45" }, refV, baseT);
        ok("verdict par outil : chrono complet — productivité au centime, et le temps machine de l'outil SORTI (T543 : 120 s) sort en clair dans « non réparti »",
           [vpoC.chronoComplet,
            Math.round(vpoC.outils[0].prodEurAn),
            Math.round(vpoC.outils[1].prodEurAn),
            Math.round(vpoC.nonReparti)],
           [true, 1250, 1250, 15000]);""",
"1. attente non réparti avec chrono (le temps machine de la sortie sort en clair)")

remplace(
"""        ok("verdict par outil : groupe simultané — le levier vaut le PLUS LONG (max, jamais la somme), porté par le pilote",
           [Math.round(vpoS.outils[0].prodEurAn), vpoS.outils[0].bottleneck,
            vpoS.outils[0].simultane, vpoS.outils[1].prodEurAn === null],
           [8750, true, true, true]);""",
"""        ok("verdict par outil : groupe simultané — le levier vaut le PLUS LONG des membres APPARIÉS (T543 sorti n'y entre plus), porté par le pilote",
           [Math.round(vpoS.outils[0].prodEurAn), vpoS.outils[0].bottleneck,
            vpoS.outils[0].simultane, vpoS.outils[1].prodEurAn === null],
           [1250, true, true, true]);""",
"2. attente groupe simultané (membres appariés seulement)")

io.open(p, "w", encoding="utf-8").write(s)
print("attentes recalées")
