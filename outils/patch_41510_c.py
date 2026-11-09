# -*- coding: utf-8 -*-
"""Tour 134 — correction du bloc de tests étape 2 (fixture : A+B simultanés, C seul)."""
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

edits = [
("""    const scT = mkSc([
      { id:"tA", numero:"T10", logs:[{id:"gA1", nom:"D1"}] },
      { id:"tB", numero:"T20", sim:true, logs:[{id:"gB1", nom:"D1"}, {id:"gB2", nom:"D2"}] },
      { id:"tC", numero:"T30", sim:true, logs:[{id:"gC1", nom:"D1"}] }
    ]);
    const g = groupesSimultanes(scT);
    ok("etape2 : groupes simultanes — 1 outil + 2 simultanes = 2 groupes", [g.length, g[0].length, g[1].length], [2, 1, 2]);
    scT.outils[1].simultaneAvecPrecedent = false;
    ok("etape2 : decocher « simultané » sépare le groupe, chacun garde ses valeurs", [groupesSimultanes(scT).length, groupesSimultanes(scT)[1].length], [2, 2]);
    scT.outils[1].simultaneAvecPrecedent = true;
    const membres = groupesSimultanes(scT)[1];
    const avant = JSON.stringify(membres);
    const uni = conditionsUniformes(membres);
    ok("etape2 : lire l'état du groupe n'écrit rien", [JSON.stringify(membres) === avant, uni.f.uniforme], [true, true]);
    ok("etape2 : UNE saisie remplit tous les logements du groupe (4 logements ici)", [ecrireConditionsGroupe(membres, "f", 0.25), membres.flatMap(o => o.logements).every(l => l.f === 0.25)], [4, true]);
    ecrireConditionsGroupe(groupesSimultanes(scT)[0], "vc", 800);
    ok("etape2 : l'outil hors groupe garde ses propres valeurs", [scT.outils[0].logements[0].vc, scT.outils[1].logements[0].vc], [800, ""]);""",
"""    const scT = mkSc([
      { id:"tA", numero:"T10", logs:[{id:"gA1", nom:"D1"}] },
      { id:"tB", numero:"T20", sim:true, logs:[{id:"gB1", nom:"D1"}, {id:"gB2", nom:"D2"}] },
      { id:"tC", numero:"T30", logs:[{id:"gC1", nom:"D1"}] }
    ]);
    const g = groupesSimultanes(scT);
    ok("etape2 : 2 outils simultanés + 1 outil seul = 2 groupes", [g.length, g[0].length, g[1].length], [2, 2, 1]);
    scT.outils[1].simultaneAvecPrecedent = false;
    ok("etape2 : decocher « simultané » sépare le groupe", [groupesSimultanes(scT).length, groupesSimultanes(scT)[0].length, groupesSimultanes(scT)[1].length, groupesSimultanes(scT)[2].length], [3, 1, 1, 1]);
    scT.outils[1].simultaneAvecPrecedent = true;
    const membres = groupesSimultanes(scT)[0];
    const avant = JSON.stringify(membres);
    const uni = conditionsUniformes(membres);
    ok("etape2 : lire l'état du groupe n'écrit rien", [JSON.stringify(membres) === avant, uni.f.uniforme], [true, true]);
    ok("etape2 : UNE saisie remplit tous les logements du groupe (3 logements ici)", [ecrireConditionsGroupe(membres, "f", 0.25), membres.flatMap(o => o.logements).every(l => l.f === 0.25)], [3, true]);
    ecrireConditionsGroupe(membres, "vc", 800);
    ok("etape2 : l'outil hors groupe garde ses propres valeurs", [scT.outils[0].logements[0].vc, scT.outils[1].logements[0].vc, scT.outils[2].logements[0].vc], [800, 800, ""]);"""),
("""    const bloc96 = conditionsGroupeHTML(scT, groupesSimultanes(scT)[0], false);
    const bloc97 = conditionsGroupeHTML(mkSc([{ id:"tZ", numero:"T60", sim:false, logs:[{id:"gZ1", nom:"D1", x:{modeVitesse:"G97", sBroche:"500"}}] }]), groupesSimultanes(scT)[1], false);""",
"""    const bloc96 = conditionsGroupeHTML(scT, groupesSimultanes(scT)[0], false);
    const scZ = mkSc([
      { id:"tZ1", numero:"T60", logs:[{id:"gZ1", nom:"D1", x:{modeVitesse:"G97", sBroche:"500"}}] },
      { id:"tZ2", numero:"T61", sim:true, logs:[{id:"gZ2", nom:"D1", x:{modeVitesse:"G97", sBroche:"500"}}] }
    ]);
    const bloc97 = conditionsGroupeHTML(scZ, groupesSimultanes(scZ)[0], false);"""),
]

applied = 0
for old, new in edits:
    if new[:60] in src and old[:60] not in src:
        applied += 1  # déjà appliqué (approximation par sonde)
        continue
    src = repl(src, old, new, old[:50])
    applied += 1

io.open(P, "w", encoding="utf-8", newline="").write(src)
print("correctif tests appliqué (%d éditions)" % applied)
