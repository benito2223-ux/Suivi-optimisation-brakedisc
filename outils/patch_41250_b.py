# -*- coding: utf-8 -*-
"""Tour 101 — v4.125.0 — le bouton ⤒ Importer du pied de rail est retiré :
l'import vit dans le menu Transmettre (groupe « L'archive »). La coque ne
touchait jamais aux données : son câblage disparaît avec lui."""
import io

# ── spk-shell.js ─────────────────────────────────────────────────────────────
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
    /* v4.120 — l'import au pied du rail (demande Benjamin) : le même geste
       que l'Importer de la barre d'outils, à l'endroit où l'œil est. */
    '<div class="spk-rail-actions">',
    '  <button type="button" class="spk-rail-action" id="spkRailImport" title="Importer un fichier .json de suivi (remplacer ou fusionner)">⤒<span>Importer</span></button>',
    '</div>',
    '<div class="spk-rail-foot">',""",
"""    '<div class="spk-rail-nav" id="spkRailNav"></div>',
    /* v4.125 — le bouton Importer du pied de rail est retiré : l'import vit
       dans le menu Transmettre (groupe « L'archive »), comme l'export. */""",
"1. le bouton rail retiré du markup")

remplace(p,
"""  /* v4.120 — le câblage : le même file picker que l'Importer de la barre
     d'outils (la coque ne touche pas aux données, elle déclenche). */
  const railImport = rail.querySelector("#spkRailImport");
  if (railImport) railImport.addEventListener("click", () => {
    const inp = document.getElementById("importInput");
    if (inp) inp.click();
  });""",
"""  /* v4.125 — le câblage rail→import a disparu avec le bouton : l'import vit
     dans le menu Transmettre (bilan_economique.html, importMenuBtn). */""",
"2. le câblage retiré")

io.open(p, "w", encoding="utf-8").write(s)
print("patch shell posé")

# ── spk-app.css : les styles orphelins partent avec le bouton ────────────────
p = "spk-app.css"
s = io.open(p, encoding="utf-8").read()
avant = """/* v4.120 — l'import au pied du rail */
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
"""
assert s.count(avant) == 1
s = s.replace(avant, "/* v4.125 — les styles du bouton Importer du pied de rail sont retirés avec lui. */\n", 1)
io.open(p, "w", encoding="utf-8").write(s)
print("ok : styles retirés")
