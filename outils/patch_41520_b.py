# -*- coding: utf-8 -*-
"""Tour 135 (4.152.0) — tests d'acceptation vue plaquette globale."""
import io

P = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/bilan_economique.html"
src = io.open(P, "r", encoding="utf-8", newline="").read()
orig_len = len(src)

def repl(s, old, new, label):
    for attempt in (old, old.replace("\n", "\r\n")):
        n = s.count(attempt)
        if n == 1:
            return s.replace(attempt, new)
        if n != 0:
            raise SystemExit("ANCRE '%s' : %d occurrences" % (label, n))
    raise SystemExit("ANCRE INTROUVABLE : %s" % label)

if "plaquette : 2 usages par désignation ISO" in src:
    print("déjà appliqué")
else:
    TESTS = r"""    /* Tour 135 (4.152.0) — la vue plaquette globale : usages par ISO + extrapolation à trois leviers (spec SPEC_VUE_PLAQUETTE_GLOBALE_2026-11-10.md) */
    {
      const lAv = lignes;
      try {
        lignes = [
          { id:"l1", nom:"EMAG 1", coutHoraire:"36", references:[
            { id:"r1", nom:"356x26", productionAnnuelle:"100000", cibleCPP:"", ops:[
              { id:"o1", opCode:"OP10", nom:"OP10", config:{ volumeActif:true }, scenarios:[
                { id:"sb1", name:"Base EMAG", baseline:true, statut:"serie", outils:[
                  { numero:"T1", logements:[{ id:"gp1", nom:"D1", ref:"CNGX 120716 LKT640", codeArticle:"IM02 1", prix:"10", aretes:"4", charniere:"50", tempsCoupe:"100" }] }] }] }] }] },
          { id:"l2", nom:"HESSAPP", coutHoraire:"", references:[
            { id:"r2", nom:"302x26", productionAnnuelle:"50000", ops:[
              { id:"o2", opCode:"OP30", nom:"OP30", config:{ volumeActif:true }, scenarios:[
                { id:"sb2", name:"Base HESSAPP", baseline:true, statut:"serie", outils:[
                  { numero:"T2", logements:[{ id:"gp2", nom:"D1", ref:"cngx120716 lkt640", codeArticle:"IM02 2", prix:"12", aretes:"4", charniere:"50" }] }] }] }] }] }
        ];
        const uv = usagesPlaquette("CNGX 120716 LKT640");
        ok("plaquette : 2 usages par désignation ISO, MABEC confondus (casse et espaces normalisés)", [uv.usages.length, uv.usages[0].mabec, uv.usages[1].mabec], [2, "IM02 1", "IM02 2"]);
        ok("plaquette : plaquettes/an et coût annuel exacts", [Math.round(uv.usages[0].plaquettesAn), Math.round(uv.usages[0].coutAnnuel), Math.round(uv.totalActuel)], [500, 5000, 8000]);
        const ex1 = extrapoleGlobale(uv, { prix: "8" });
        ok("plaquette : extrapolation prix seul = la variable de départ", [Math.round(ex1.totalEcart), ex1.usages[0].leviers.join(",")], [2000, "prix 10,00 → 8,00 €"]);
        const ex2 = extrapoleGlobale(uv, { prix: "8", charniere: "90" });
        ok("plaquette : prix + charnière cumulés, au centime", [Math.round(ex2.totalActuel - ex2.totalSimule)], [4667]);
        const ex3 = extrapoleGlobale(uv, { tempsCoupe: "80" });
        ok("plaquette : cycle chiffré sur la ligne à taux, nommé « non chiffré » sinon", [Math.round(ex3.totalEcart), ex3.cyclesNonChiffres.length, ex3.cyclesNonChiffres[0].usage.ligne], [20000, 1, "HESSAPP"]);
        lignes[0].references[0].productionAnnuelle = "";
        const uv2 = usagesPlaquette("cngx120716lkt640");
        ok("plaquette : sans volume, l'usage est listé avec son manque et exclu du total", [uv2.usages.length, uv2.exclus.length, uv2.exclus[0].manques.join(",")], [1, 1, "volume annuel"]);
        lignes[0].references[0].productionAnnuelle = "100000";
        const pan = panneauUsagesHTML(["CNGX 120716 LKT640"], { charniere: "90" });
        ok("plaquette : le panneau porte MABEC, désignation et l'étiquette SIMULATION", [/IM02 1/.test(pan), /CNGX 120716 LKT640/i.test(pan), /SIMULATION/.test(pan), /volume annuel/.test(pan)], [true, true, true, false]);
        const ex0 = extrapoleGlobale(uv, {});
        ok("plaquette : aucun levier → invitation, jamais un total inventé", [/Renseigne au moins un levier/.test(extrapoleTotalHTML(ex0)), extrapoleTotalHTML(ex0).indexOf("SIMULATION — si") === -1], [true, true]);
      } finally { lignes = lAv; }
    }
"""
    ANCRE = r'''    ok("etape2 : un groupe en G97 affiche S (tr/min)", /S <span>tr\/min<\/span>/.test(bloc97), true);
  }'''
    src = repl(src, ANCRE, ANCRE + "\n" + TESTS, "tests-plaquette")
    io.open(P, "w", encoding="utf-8", newline="").write(src)
    print("TESTS OK : %d -> %d (+%d)" % (orig_len, len(src), len(src) - orig_len))
