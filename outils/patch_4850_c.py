# -*- coding: utf-8 -*-
"""Patch v4.85.0 partie C : tests du catalogue + API harnais."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

av = '''        ok("export simulateur : les deux tableaux sont l\u00e0, avec TOTAL et \u00e9conomies",
           [lignesCsv.some(x => x.indexOf("Budget outillage annuel par reference") === 0),
            lignesCsv.some(x => x.indexOf("TOTAL;") === 0),
            lignesCsv.some(x => x.indexOf("Economie annuelle (EUR)") > -1)],
           [true, true, true]);'''
ap = av + '''

    /* ---- v4.85.0 — LE CATALOGUE PLAQUETTES : seed, propagation, CSV ---------- */
    {
      const lC = normalizeLigne({ id: "lCat", nom: "EMAG 1", references: [ normalizeReference({ id: "rCat", nom: "356x26", productionAnnuelle: 1000, ops: [
        normalizeOp({ id: "oCat", nom: "OP10", scenarios: [ normalizeScenario({ id: "scCat", name: "Prod", baseline: true, outils: [
          { id: "tC1", numero: "T517", logements: [
            { id: "gC1", nom: "D1", ref: "SNGX 120716 S02020 CBN387", codeArticle: "IM02 209 560", prix: 38, aretes: 4, charniere: 600 },
            { id: "gC2", nom: "D2", ref: "CNGX 120716 S02020 CBN387", codeArticle: "IM02 137 021", prix: 7.96, aretes: 8, charniere: 150 } ] } ] }) ] }) ] }) ] });
      const lAvC = lignes; lignes = [ lC ];
      try {
        const seed = catalogueSeed();
        const e209 = seed.find(a => a.mabec === "IM02 209 560");
        ok("catalogue : le seed regroupe par MABEC et retient le prix le plus fr\u00e9quent",
           [seed.length, e209.prix, e209.iso.indexOf("SNGX") === 0], [2, 38, true]);
        catalogue = [ normalizeArticleCat({ mabec: "IM02 209 560", iso: e209.iso, prix: 42 }),
                      normalizeArticleCat({ mabec: "IM02 137 021", prix: 7.96 }) ];
        const rapport = catalogueAppliquer();
        const g1 = lignes[0].references[0].ops[0].scenarios[0].outils[0].logements[0];
        ok("catalogue : la propagation change le prix du logement et rend le rapport avant/apr\u00e8s",
           [rapport.logementsTouches, g1.prix, rapport.mabecs[0].avant, rapport.mabecs[0].apres],
           [1, 42, 38, 42]);
        ok("catalogue : un logement d\u00e9j\u00e0 au bon prix n'est pas \u00ab touch\u00e9 \u00bb (le rapport ne ment pas)",
           catalogueAppliquer().logementsTouches, 0);
        catalogue = seed.map(a => normalizeArticleCat(a));
        const csv = catalogueCSV();
        const rere = catalogueDepuisCSV(csv);
        ok("catalogue : le CSV standalone fait l'aller-retour sans perte (BOM, sep=;)",
           [rere.erreurs.length, rere.cat.length, rere.cat.find(x => x.mabec === "IM02 137 021").prix],
           [0, 2, 7.96]);
        ok("catalogue : l'import tol\u00e8re virgule d\u00e9cimale et s\u00e9parateur virgule (Excel FR)",
           catalogueDepuisCSV("MABEC,Prix EUR\\nIM02 137 021,\\"7,96\\"").cat[0].prix, 7.96);
        ok("catalogue : un prix illisible est signal\u00e9, pas invent\u00e9 (\u00a73.5)",
           catalogueDepuisCSV("MABEC;Prix EUR\\nIM02 137 021;nsp").erreurs.length > 0, true);
      } finally { lignes = lAvC; catalogue = []; }
    }'''
assert av in s, "ancre tests"
s = s.replace(av, ap, 1)
open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("tests catalogue ajoutes")

h = open('build_harness.py', encoding='utf-8').read()
if "catalogueSeed" not in h:
    h = h.replace('"getActiveLigne, preparerImportDepuis, axesActifs, reattribuerEssai, plaquettesCommunes, simulCSV, get lignes(){return lignes}, set lignes(v){lignes=v}, "',
                  '"getActiveLigne, preparerImportDepuis, axesActifs, reattribuerEssai, plaquettesCommunes, simulCSV, catalogueSeed, catalogueAppliquer, catalogueCSV, catalogueDepuisCSV, get lignes(){return lignes}, set lignes(v){lignes=v}, "')
    open('build_harness.py', 'w', encoding='utf-8').write(h)
    print("API harnais + catalogue")
