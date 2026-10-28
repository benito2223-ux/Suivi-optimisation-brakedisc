# -*- coding: utf-8 -*-
"""Tour 104 — v4.127.0 — LOT 2 du brief complémentaire : LE MODE ATELIER.

1. Tokens dans :root (bureau = valeurs actuelles) + --bord-atelier.
2. Un bloc CSS `html[data-mode="atelier"]` (posé en fin du PREMIER bloc
   style — celui de l'app, pas des templates print) : texte ≥ 16 px,
   libellés ≥ 14 px, valeurs ≥ 20 px, cibles ≥ 56 px, boutons pleins,
   bordures ≥ 3:1, pastilles remplies, pas de verre.
3. IBM Plex Mono retiré (3 @font-face) : --font-mono retargeté Open Sans +
   tabular-nums global.
4. Écran de boot léger (div statique retiré au premier rendu) à la place du
   visibility:hidden, et le commentaire d'en-tête mis à jour."""
import io, re

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. tokens bureau + mono retargeté ────────────────────────────────────────
remplace(
"  --font-mono:'IBM Plex Mono','Courier New',Consolas,monospace;",
"""  /* v4.127 (LOT 2) — les tokens de lecture, bureau par défaut. Le mode
     atelier (html[data-mode]) les surcharge en dessous. */
  --fs-label:10.5px;
  --fs-base:12.5px;
  --fs-val:19px;
  --fs-hero:38px;
  --hit:32px;
  --bord-ui:#e5e5e5;
  --bord-atelier:#8a9099;   /* 3,05:1 sur blanc */
  --font-mono:'Open Sans',Consolas,monospace;   /* v4.127 : Plex retiré — tabular-nums sur Open Sans tient les colonnes */""",
"1. tokens bureau + mono retargeté")

# ── 2. le bloc atelier, en fin du PREMIER bloc style (par index) ─────────────
BLOC = """
  /* ═══ v4.127 — LE MODE ATELIER (html[data-mode="atelier"]) ════════════
     Posé en FIN du bloc style principal : il gagne les empilements équivalents.
     Écran tactile, gants, lumière d'usine — le mode bureau/commercial reste
     la charte CeramTec actuelle, inchangée. */
  html[data-mode="atelier"] body{ font-size:16px; }
  html[data-mode="atelier"] .foot-cell .l, html[data-mode="atelier"] .fs-l,
  html[data-mode="atelier"] .ap-l, html[data-mode="atelier"] .pcb-l,
  html[data-mode="atelier"] .tc-label, html[data-mode="atelier"] .fr-op,
  html[data-mode="atelier"] .hd-eyebrow, html[data-mode="atelier"] .pcb-st,
  html[data-mode="atelier"] .foot-verdict .fv-eyebrow,
  html[data-mode="atelier"] .zone-band span{ font-size:14px !important; }
  html[data-mode="atelier"] .foot-cell .v{ font-size:24px !important; }
  html[data-mode="atelier"] .foot-cell input.cell-cycle{ font-size:24px !important; }
  html[data-mode="atelier"] .foot-second .fs-v{ font-size:20px !important; }
  html[data-mode="atelier"] .ap-v, html[data-mode="atelier"] .tc-name,
  html[data-mode="atelier"] .fr-prod, html[data-mode="atelier"] .fr-essai,
  html[data-mode="atelier"] .pcb-total, html[data-mode="atelier"] .pcb-encours,
  html[data-mode="atelier"] .pcb-realise, html[data-mode="atelier"] .pcb-op,
  html[data-mode="atelier"] .foot-sub, html[data-mode="atelier"] .fs-sub,
  html[data-mode="atelier"] .pcb-vide, html[data-mode="atelier"] .panel-hint,
  html[data-mode="atelier"] .ap-ref, html[data-mode="atelier"] .ap-cond,
  html[data-mode="atelier"] .reprise-bandeau, html[data-mode="atelier"] .bandeau-premiere{ font-size:16px !important; }
  html[data-mode="atelier"] .ap-v small, html[data-mode="atelier"] .fs-v small,
  html[data-mode="atelier"] .foot-cell .v small{ font-size:14px !important; }
  html[data-mode="atelier"] button{ min-height:56px; }
  html[data-mode="atelier"] .toolbar button{ min-height:56px; min-width:56px; }
  html[data-mode="atelier"] input.cell, html[data-mode="atelier"] input.cell-cycle{ min-height:56px; }
  html[data-mode="atelier"] .tab-card{ min-height:56px; padding:12px 14px; }
  html[data-mode="atelier"] .ap-tuile{ padding:14px 16px; }
  html[data-mode="atelier"] select.cell, html[data-mode="atelier"] select{ min-height:56px; }
  html[data-mode="atelier"] .toolbar button,
  html[data-mode="atelier"] .sc-actions button,
  html[data-mode="atelier"] .toolbar-more button{ background:var(--surface); border:1.5px solid var(--bord-atelier); }
  html[data-mode="atelier"] button.primary{ background:var(--fill); color:#fff; border:1.5px solid var(--fill); }
  html[data-mode="atelier"] .toolbar button.is-actif{ background:var(--fill); color:#fff; }
  html[data-mode="atelier"] .pcb-st.ok{ background:var(--green); color:#fff; }
  html[data-mode="atelier"] .pcb-st.pending{ background:var(--amber); color:#fff; }
  html[data-mode="atelier"] .pcb-st.arrete{ background:var(--gray-300); color:var(--ink); }
  html[data-mode="atelier"] .status-badge.ok, html[data-mode="atelier"] .statut-pill.serie{ background:var(--green); color:#fff; }
  html[data-mode="atelier"] .status-badge.pending, html[data-mode="atelier"] .statut-pill.essai{ background:var(--amber); color:#fff; }
  html[data-mode="atelier"] .toolbar{ backdrop-filter:none !important; -webkit-backdrop-filter:none !important; background:var(--surface) !important; }
  html[data-mode="atelier"] .ap-tuile, html[data-mode="atelier"] .pcb-banner,
  html[data-mode="atelier"] .foot-cell, html[data-mode="atelier"] .tab-card,
  html[data-mode="atelier"] .panel{ border-color:var(--bord-atelier); }
  html[data-mode="atelier"] input.cell, html[data-mode="atelier"] input.cell-cycle,
  html[data-mode="atelier"] select{ border-color:var(--bord-atelier); }
  html[data-mode="atelier"] input.cell-cycle:focus{ background:var(--surface); color:var(--fill); border-color:var(--bord-atelier); }
"""
marqueur = "</style></head><body>"
i = s.find(marqueur)
assert i > -1, "premier bloc style introuvable"
s = s[:i] + BLOC + s[i:]
print("ok : 2. le bloc atelier (fin du premier bloc style)")

# ── 3. Plex : les @font-face sortent ─────────────────────────────────────────
n_plex = len(re.findall(r"@font-face\{font-family:'IBM Plex Mono", s))
s = re.sub(r"@font-face\{font-family:'IBM Plex Mono';[^}]*\}\n?", "", s)
print("ok : 3. %d @font-face Plex retirés" % n_plex)

# ── 4. l'écran de boot ───────────────────────────────────────────────────────
remplace(
"""html:not([data-pret]) body{visibility:hidden;}</style>""",
"""/* v4.127 : l'écran de boot (div statique ci-dessous) remplace le masquage du
   body — on voit une page de chargement, pas une page à moitié peinte. */
#spkBoot{position:fixed; inset:0; z-index:300; background:var(--bg,#e8eaed); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px;}
#spkBoot .spk-boot-t{font-family:var(--font-disp,'Open Sans Condensed',Arial,sans-serif); font-weight:800; font-size:26px; color:#1B5EA6; letter-spacing:-.01em;}
#spkBoot .spk-boot-b{width:34px; height:34px; border:3px solid #c9cdd4; border-top-color:#1B5EA6; border-radius:50%; animation:spkboot .9s linear infinite;}
@keyframes spkboot{to{transform:rotate(360deg);}}
html[data-pret] #spkBoot{display:none;}
</style>""",
"4a. le style du boot (le visibility:hidden part)")

# 4b : insertion par INDEX (l'ancre `</head><body>` existe aussi dans un
# template print — la première occurrence est le vrai document)
iBody = s.find("</head><body>")
assert iBody > -1, "le vrai document introuvable"
bootDiv = '</head>\n<body>\n<div id="spkBoot" aria-hidden="true"><div class="spk-boot-t">Suivi d\'optimisation</div><div class="spk-boot-b"></div></div>'
s = s[:iBody] + bootDiv + s[iBody+len("</head><body>"):]
print("ok : 4b. le div de boot (première occurrence)")

# ── 5. le commentaire d'en-tête des polices, mis à jour ─────────────────────
remplace(
"""   IBM Plex Mono porte tous les chiffres, de la saisie aux gabarits de rapport.""",
"""   v4.127 : IBM Plex Mono est retiré — Open Sans porte aussi les chiffres,
   avec font-variant-numeric: tabular-nums pour l'alignement des colonnes.""",
"5. commentaire d'en-tête")

# ── 6. tabular-nums global + la bascule dans la barre ────────────────────────
remplace(
"""<body>
<div id="spkBoot" aria-hidden="true">""",
"""<body>
<div id="spkBoot" aria-hidden="true"><!-- v4.127 : écran de chargement — retiré au premier rendu -->""",
"6a. note du boot")

# la bascule : un bouton ⚒ près de lockBtn, câblé au script
remplace(
"""      <button class="ghost" id="lockBtn" title="Passe l'outil en lecture seule — pour l'écran partagé d'atelier">""",
"""      <button class="ghost" id="modeBtn" title="Mode atelier : gros chiffres, cibles tactiles, contraste renforcé — pour l'écran de la machine"><svg class="icon" viewBox="0 0 18 18"><path d="M9 2.5v13M3 6c1.5-2 3-3 6-3s4.5 1 6 3" stroke-linecap="round"/></svg><span class="label-tb" id="modeLabel">Atelier</span></button>
      <button class="ghost" id="lockBtn" title="Passe l'outil en lecture seule — pour l'écran partagé d'atelier">""",
"6b. le bouton de bascule")

# le câblage JS : posé juste avant semerLignesSeptFons(); (le premier rendu lit le mode)
remplace(
"""semerLignesSeptFons();
render();""",
"""/* v4.127 — le MODE ATELIER : bascule mémorisée, défaut = écran tactile.
   Posé AVANT le premier rendu : le mode est appliqué dès la première peinture. */
(function modeAtelier(){
  const CLE = "spk_mode";
  let mode = null;
  try{ mode = localStorage.getItem(CLE); }catch(e){}
  if(mode !== "atelier" && mode !== "bureau"){
    try{ mode = window.matchMedia && matchMedia("(pointer:coarse)").matches ? "atelier" : "bureau"; }catch(e){ mode = "bureau"; }
  }
  if(mode === "atelier") document.documentElement.setAttribute("data-mode", "atelier");
  window._spkSetMode = function(m){
    if(m !== "atelier" && m !== "bureau") return;
    if(m === "atelier") document.documentElement.setAttribute("data-mode", "atelier");
    else document.documentElement.removeAttribute("data-mode");
    try{ localStorage.setItem(CLE, m); }catch(e){}
    const lbl = document.getElementById("modeLabel");
    if(lbl) lbl.textContent = m === "atelier" ? "Bureau" : "Atelier";
    const btn = document.getElementById("modeBtn");
    if(btn) btn.title = m === "atelier" ? "Revenir au mode bureau (charte commerciale)" : "Mode atelier : gros chiffres, cibles tactiles, contraste renforcé";
  };
  const btn = document.getElementById("modeBtn");
  if(btn) btn.addEventListener("click", () => {
    const courant = document.documentElement.getAttribute("data-mode") === "atelier" ? "atelier" : "bureau";
    window._spkSetMode(courant === "atelier" ? "bureau" : "atelier");
  });
  window._spkSetMode(mode);
})();
semerLignesSeptFons();
render();""",
"6c. le câblage du mode (avant le premier rendu)")

# ── 7. version + NOUVEAUTES ──────────────────────────────────────────────────
assert s.count('const TOOL_VERSION = "4.126.0";') == 1
s = s.replace('const TOOL_VERSION = "4.126.0";', 'const TOOL_VERSION = "4.127.0";', 1)
print("ok : TOOL_VERSION")

ancre = 'const NOUVEAUTES = [\n'
assert s.count(ancre) == 1
entree = (
    '  { version:"4.127.0", date:"28/10/2026", points:[\n'
    '    "<b>Le mode atelier.</b> Un bouton <b>⚒ Atelier</b> de la barre bascule l\\u2019outil en mode machine : texte et libellés agrandis (plus rien en dessous de 14 px), <b>cibles tactiles de 56 px</b> (boutons, champs, lignes), boutons <b>pleins et bordés</b> (plus de ton sur ton), états en <b>pastilles remplies</b> (conforme, à faire — lisibles sans la couleur seule), bordures renforcées, plus de verre sur la barre. Mémorisé, et <b>automatique sur écran tactile</b>. Le mode bureau garde la charte CeramTec inchangée. Au passage : la police mono des chiffres passe en <b>Open Sans tabulaire</b> (Plex retiré — deux polices de moins embarquées), et l\\u2019ouverture affiche un écran de chargement au lieu d\\u2019une page à moitié peinte."\n'
    '  ]},\n'
)
s = s.replace(ancre, ancre + entree, 1)
print("ok : entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch LOT 2 posé :", n0, "->", len(s))
