# -*- coding: utf-8 -*-
"""Tour 98 — v4.120.0 — le bouton Importer au pied du rail (coque).
Le même geste que l'Importer de la barre d'outils (file picker → importData),
à l'endroit où Benjamin le cherche : le pied du rail, à côté de l'état des
données. Le raccourci Matis reste en place (explication demandée, décision
Benjamin attendue avant tout retrait)."""
import io

# ── spk-shell.js : l'action + son câblage ────────────────────────────────────
p = "spk-shell.js"
s = io.open(p, encoding="utf-8").read()


def remplace(fichier, avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


remplace(p,
"""    '<div class="spk-rail-nav" id="spkRailNav"></div>',
    '<div class="spk-rail-foot">',""",
"""    '<div class="spk-rail-nav" id="spkRailNav"></div>',
    /* v4.120 — l'import au pied du rail (demande Benjamin) : le même geste
       que l'Importer de la barre d'outils, à l'endroit où l'œil est. */
    '<div class="spk-rail-actions">',
    '  <button type="button" class="spk-rail-action" id="spkRailImport" title="Importer un fichier .json de suivi (remplacer ou fusionner)">⤒<span>Importer</span></button>',
    '</div>',
    '<div class="spk-rail-foot">',""",
"1. l'action dans le rail")

remplace(p,
"""  document.body.prepend(rail);
  document.body.classList.add("spk-has-rail");""",
"""  document.body.prepend(rail);
  document.body.classList.add("spk-has-rail");

  /* v4.120 — le câblage : le même file picker que l'Importer de la barre
     d'outils (la coque ne touche pas aux données, elle déclenche). */
  const railImport = rail.querySelector("#spkRailImport");
  if (railImport) railImport.addEventListener("click", () => {
    const inp = document.getElementById("importInput");
    if (inp) inp.click();
  });""",
"2. le câblage du file picker")

io.open(p, "w", encoding="utf-8").write(s)
print("patch shell posé")

# ── spk-app.css : le style ───────────────────────────────────────────────────
p = "spk-app.css"
s = io.open(p, encoding="utf-8").read()

avant = ".spk-rail-foot {"
apres = """/* v4.120 — l'import au pied du rail */
.spk-rail-actions { padding: 10px 10px 0; }
.spk-rail-action {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 10px; border-radius: 4px;
  background: rgba(255, 255, 255, .12); color: #fff;
  border: 1px solid rgba(255, 255, 255, .28);
  font-family: var(--font-mono, monospace); font-size: 10.5px; letter-spacing: .04em;
  cursor: pointer;
}
.spk-rail-action:hover { background: rgba(255, 255, 255, .22); }
.spk-rail-off .spk-rail-action span { display: none; }
.spk-rail-foot {"""
assert s.count(avant) >= 1
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("ok : style du bouton rail")
