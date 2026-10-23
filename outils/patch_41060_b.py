# -*- coding: utf-8 -*-
"""Tour 88 (4.106.0) — suite : binding visiteBtn + colonne codification du catalogue."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
n0 = len(src)

def remplace(avant, apres, label):
    global src
    assert avant in src, "ANCRE INTROUVABLE : " + label
    src = src.replace(avant, apres, 1)
    print("ok :", label)

# 1. binding du bouton du Plan
remplace('  const mx = document.getElementById("planMaxiBtn");',
         '  const visBtn = document.getElementById("visiteBtn");\n'
         '  if(visBtn) visBtn.addEventListener("click", ouvrirVisite);\n'
         '  const mx = document.getElementById("planMaxiBtn");',
         "binding visiteBtn (Plan)")

# 2. colonne codification du catalogue
remplace(
    '      <thead><tr><th>Article (MABEC)</th><th>Libellés ISO vus</th><th>Prix</th></tr></thead>\n'
    '      <tbody>${catalogue.map(a => `<tr>\n'
    '        <td class="mono">${escapeAttr(a.mabec)}</td>\n'
    '        <td style="font-size:12px; color:#888;">${escapeAttr(a.iso || "—")}</td>\n'
    '        <td class="mono">${a.prix !== "" ? fmt(a.prix, 2) + " €" : "—"}${a.divergent ? \' <span style="color:#b45309;">(prix divergents dans l\\\'outil — Matis vérifie)</span>\' : ""}</td>\n'
    '      </tr>`).join("")}</tbody>',

    '      <thead><tr><th>Article (MABEC)</th><th>Libellés ISO vus</th><th>Prix</th><th>Codification Matis</th></tr></thead>\n'
    '      <tbody>${catalogue.map((a, i) => `<tr>\n'
    '        <td class="mono">${escapeAttr(a.mabec)}</td>\n'
    '        <td style="font-size:12px; color:#888;">${escapeAttr(a.iso || "—")}</td>\n'
    '        <td class="mono">${a.prix !== "" ? fmt(a.prix, 2) + " €" : "—"}${a.divergent ? \' <span style="color:#b45309;">(prix divergents dans l\\\'outil — Matis vérifie)</span>\' : ""}</td>\n'
    '        <td><label style="display:flex; align-items:center; gap:5px; font-size:11.5px; color:var(--ink-soft);" title="Codification par le service administratif de Matis : prérequis du cycle de commande standard — sans elle, BADP seulement (montants et récurrence limités). L\\\'âge de l\\\'attente est la métrique.">dem.<input type="date" min="2025-01-01" max="2035-12-31" data-catdate="${i}" data-catfield="codificationDemandeeLe" value="${escapeAttr(a.codificationDemandeeLe || "")}"> cod.<input type="date" min="2025-01-01" max="2035-12-31" data-catdate="${i}" data-catfield="codifieLe" value="${escapeAttr(a.codifieLe || "")}">${(() => { const e = etatCodification(a); return e.etat === "codifie" ? ` <span class="pc-stat serie">codifié</span>` : e.etat === "demandee" ? ` <span class="pc-stat attente">${e.jours ?? 0} j</span>` : ""; })()}</label></td>\n'
    '      </tr>`).join("")}</tbody>',
    "catalogue colonne codification")

# 3. binding des dates
remplace('  const seed = document.getElementById("catSeed");',
         '  wrap.querySelectorAll(\'input[data-catdate]\').forEach(inp => inp.addEventListener("change", () => {\n'
         '    const art = catalogue[Number(inp.getAttribute("data-catdate"))];\n'
         '    if(!art) return;\n'
         '    art[inp.getAttribute("data-catfield")] = inp.value || "";\n'
         '    saveData(); renderCatalogue();\n'
         '  }));\n'
         '  const seed = document.getElementById("catSeed");',
         "binding dates catalogue")

io.open(p, "w", encoding="utf-8").write(src)
print("taille:", n0, "->", len(src))
