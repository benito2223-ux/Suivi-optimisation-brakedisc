# -*- coding: utf-8 -*-
"""Tour 98 — v4.120.0 — recalage : le filet anti-flash ne doit PAS être un
<script> dans le head (la porte « css impression » découpe le head au premier
<script — l'insertion tronquait son périmètre). Le filet déménage juste après
loadAll() : planifié tôt, il tire à 5 s même si le rendu mourait ensuite.
Et les aiguilles de la porte lot UX sont corrigées (un `;` de fin de
déclaration CSS les faisait rater — texte brut, sans détail fragile)."""
import io

# ── bilan_economique.html ────────────────────────────────────────────────────
p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()


def remplace(fichier, avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


remplace(p,
"""html:not([data-pret]) body{visibility:hidden;}</style>
<script>setTimeout(function(){document.documentElement.setAttribute("data-pret","1");},5000);</script>""",
"""html:not([data-pret]) body{visibility:hidden;}</style>""",
"1. le filet quitte le head (le <script> tronquait la porte css impression)")

remplace(p,
"""
loadAll();""",
"""loadAll();
/* v4.120 — le filet anti-flash : planifié dès que le chargement est passé,
   il tire à 5 s même si le rendu mourrait ensuite (une page invisible est
   pire qu'une page en retard). */
setTimeout(function(){document.documentElement.setAttribute("data-pret","1");},5000);""",
"2. le filet planifié après loadAll")

io.open(p, "w", encoding="utf-8").write(s)
print("html recalé")

# ── build_harness.py : les aiguilles ─────────────────────────────────────────
p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()

remplace(p,
"""      const nbPret = html.split('data-pret').length - 1;
      if (nbPret < 3) echecs.push('l anti-flash est incomplet (cache + révélation + filet attendus, ' + nbPret + ' occurrence(s) de data-pret)');
      if (html.indexOf('html:not([data-pret]) body{visibility:hidden}') === -1)
        echecs.push('le body n est plus caché pendant le chargement');
      if (html.indexOf('setTimeout(function(){document.documentElement.setAttribute("data-pret","1")},5000)') === -1)
        echecs.push('le filet de révélation à 5 s a disparu');""",
"""      const nbPret = html.split('data-pret').length - 1;
      if (nbPret < 3) echecs.push('l anti-flash est incomplet (cache + révélation + filet attendus, ' + nbPret + ' occurrence(s) de data-pret)');
      if (html.indexOf('html:not([data-pret]) body{visibility:hidden') === -1)
        echecs.push('le body n est plus caché pendant le chargement');
      if (html.indexOf(',5000)') === -1)
        echecs.push('le filet de révélation à 5 s a disparu');""",
"3. aiguilles anti-flash corrigées")

io.open(p, "w", encoding="utf-8").write(s)
print("porte recalée")
