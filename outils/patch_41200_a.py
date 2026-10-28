# -*- coding: utf-8 -*-
"""Tour 98 — v4.120.0 — lot UX de Benjamin (28/10).

1. « ⤓ Imprimer » (Générer le PDF) est MORT depuis le dé-branding 4.104 :
   printGo lisait le logo dans l'en-tête (.hd-left img — retiré) → querySelector
   null → TypeError AVANT window.print(). Le logo A4 embarqué (LOGO_SPK_SRC)
   devient la source directe.
2. Anti-flash au démarrage : le squelette statique se peint pendant que le
   script se charge (« on aperçoit l'ancienne page puis la nouvelle »). Le body
   est caché jusqu'au premier rendu (filet : révélation forcée à 5 s)."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. le fix du PDF ─────────────────────────────────────────────────────────
remplace(
"""  const src = document.querySelector(".hd-left img").getAttribute("src");
  document.getElementById("printLogo").setAttribute("src", src);""",
"""  /* v4.120 — le logo ne vit plus dans l'en-tête (dé-branding 4.104) : lire
     l'embed A4 directement. L'ancienne ligne jettait (querySelector null) et
     « ⤓ Imprimer » ne faisait plus rien depuis le 22/10. */
  document.getElementById("printLogo").setAttribute("src", (typeof LOGO_SPK_SRC === "string" && LOGO_SPK_SRC) ? LOGO_SPK_SRC : "");""",
"1. printGo : le logo vient de LOGO_SPK_SRC")

# ── 2. l'anti-flash ──────────────────────────────────────────────────────────
remplace(
"<title>Suivi d'optimisation</title>",
"""<title>Suivi d'optimisation</title>
<style>/* v4.120 — anti-flash : le squelette statique ne doit pas être peint pendant
   que le script se charge (Benjamin : « on aperçoit l'ancienne page puis la
   nouvelle s'affiche »). La révélation se pose à la fin du premier rendu ;
   un filet à 5 s garantit l'affichage même si le rendu mourait. */
html:not([data-pret]) body{visibility:hidden;}</style>
<script>setTimeout(function(){document.documentElement.setAttribute("data-pret","1");},5000);</script>""",
"2a. le body se cache jusqu'au premier rendu")

remplace(
"""semerLignesSeptFons();
render();""",
"""semerLignesSeptFons();
render();
/* v4.120 — la révélation : le premier rendu est posé, le squelette peut se montrer. */
document.documentElement.setAttribute("data-pret", "1");""",
"2b. la révélation après le premier rendu")

# ── 3. version + NOUVEAUTES ──────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.119.0";', 'const TOOL_VERSION = "4.120.0";', "3a. TOOL_VERSION")

import re
m = re.search(r'const NOUVEAUTES = \[\n  \{ version:"4\.[0-9.]+", date:"[0-9/]+", points:\[\n', s)
assert m, "ancre NOUVEAUTES introuvable"
entree = (
    'const NOUVEAUTES = [\n'
    '  { version:"4.120.0", date:"28/10/2026", points:[\n'
    '    "<b>Lot confort — trois retours de terrain.</b> <b>⤓ Imprimer (Générer le PDF) refonctionne</b> : le logo de l\\u2019en-tête avait été retiré au dé-branding et l\\u2019impression tombait sur une erreur avant d\\u2019ouvrir la boîte d\\u2019impression — le logo A4 embarqué est maintenant lu directement. <b>Plus de page fantôme au démarrage</b> : l\\u2019écran ne se montre plus avant que les données soient rendues. Et <b>l\\u2019import d\\u2019un fichier JSON est désormais au pied du rail de navigation</b>, à côté de l\\u2019état des données."\n'
    '  ]},\n'
)
s = s[:m.start()] + entree + s[m.start():]
print("ok : entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch 4.120.0 (html) posé :", n0, "->", len(s))
