# -*- coding: utf-8 -*-
"""Tour 101 — v4.125.0 — le lot 4.125 du brief externe (navigation et
doublons), feu vert de Benjamin. Sept gestes :
  1. L'outil s'ouvre sur l'ÉCRAN DE TRAVAIL (Q11 révisé par le brief validé) —
     la Vue d'ensemble s'ouvre sur clic ou #accueil.
  2. La boussole « Je cherche… » quitte l'écran de travail (Ctrl+K reste).
  3. Transmitter → fin de barre, à côté de + Scénario.
  4. Importer rejoint le groupe « L'archive » du menu Transmettre ; le bouton
     de la barre et celui du pied de rail disparaissent.
  5. La tuile ouverte se réduit au nom (une ligne) — plus de grande carte vide.
  6. Le bandeau coût pièce vide (cible non renseignée, rien réalisé) devient
     une ligne grise — un état vide ne pèse plus comme une donnée.
  7. L'anneau de focus ne se pose plus sur « Postes » à l'ouverture de la
     Vue d'ensemble (accueillPanel ne vole pas le focus)."""
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


# ── 1. l'ouverture : l'écran de travail (Q11 révisé) ─────────────────────────
remplace(
"""if(!location.hash || location.hash === "#accueil") ouvrirAccueil();""",
"""/* v4.125 (brief externe validé par Benjamin le 28/10) : l'ouverture est l'ÉCRAN DE
   TRAVAIL — la Vue d'ensemble s'ouvre sur clic ou #accueil. La décision v4.62/Q11
   (« l'accueil EST l'ouverture ») est révisée ici : deux couches (bandeau + écran
   plein écran) avant tout travail pesaient plus que la vue d'ensemble. */
if(location.hash === "#accueil") ouvrirAccueil();""",
"1. l'ouverture = l'écran de travail")

# ── 2. la boussole quitte la fiche ───────────────────────────────────────────
remplace(
"""  el.innerHTML = boussoleHTML() + '<div class="zone-band">""",
"""  /* v4.125 : la boussole « Je cherche… » quitte la fiche (brief externe P1-1) —
     Ctrl+K reste, la fonction et ses styles restent (dormants, réactivables). */
  el.innerHTML = '<div class="zone-band">""",
"2. la boussole quitte la fiche")

# ── 3. Transmettre à la fin de la barre ──────────────────────────────────────
# déplacement par bornes EXACTES (indentation réelle du fichier : le wrap ouvre
# à 12 espaces, le menu interne ferme à 8, le wrap ferme à 6 — le premier
# "\n + 6 espaces + </div>" APRÈS le wrap est sa fermeture).
iDeb = s.find('            <div class="toolbar-more-wrap" id="transmettreWrap">')
assert iDeb > -1, "wrap transmettre introuvable"
fermeture = "\n      </div>\n"
iFin = s.find(fermeture, iDeb)
assert iFin > -1, "fermeture du wrap introuvable"
iFin += len(fermeture)
bloc = s[iDeb:iFin]
s = s[:iDeb] + s[iFin:]
ancre_add = '<button class="primary" id="addBtn">+ Scénario</button>\n'
assert s.count(ancre_add) == 1, s.count(ancre_add)
iAdd = s.find(ancre_add) + len(ancre_add)
s = s[:iAdd] + bloc + s[iAdd:]
print("ok : 3. Transmettre déplacé après + Scénario")

# ── 4. Importer rejoint le groupe L'archive ─────────────────────────────────
remplace(
"""          <button class="ghost" id="csvBtn" title="Tous les prélèvements en tableau, pour Excel ou le système qualité"><svg class="icon" viewBox="0 0 18 18"><rect x="2.5" y="2.5" width="13" height="13" rx="1.5"/><path d="M2.5 7h13M2.5 11.5h13M7 2.5v13"/></svg>Export CSV</button>
        </div>
      </div>""",
"""          <button class="ghost" id="csvBtn" title="Tous les prélèvements en tableau, pour Excel ou le système qualité"><svg class="icon" viewBox="0 0 18 18"><rect x="2.5" y="2.5" width="13" height="13" rx="1.5"/><path d="M2.5 7h13M2.5 11.5h13M7 2.5v13"/></svg>Export CSV</button>
          <button class="ghost" id="importMenuBtn" title="Recharge un fichier .json reçu ou archivé — remplacer ou fusionner"><svg class="icon" viewBox="0 0 18 18"><path d="M9 11.5V3M5.5 6.5 9 3l3.5 3.5M3 14.5h12" stroke-linecap="round" stroke-linejoin="round"/></svg>Importer un suivi</button>
        </div>
      </div>""",
"4a. l'item Importer dans le menu Transmettre")

remplace(
"""      <button class="ghost" id="importBtn" title="Recharge un fichier .json reçu ou archivé"><svg class="icon" viewBox="0 0 18 18"><path d="M2.5 5.5a1 1 0 0 1 1-1H7l1.5 1.8H14.5a1 1 0 0 1 1 1V13a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1V5.5Z" stroke-linejoin="round"/></svg><span class="label-tb">Importer</span></button>
      <input type="file" id="importInput" accept=".json,application/json" hidden>""",
"""      <input type="file" id="importInput" accept=".json,application/json" hidden>""",
"4b. le bouton Importer quitte la barre")

remplace(
"""document.getElementById("importBtn").addEventListener("click", () => {
  document.getElementById("importInput").click();
});""",
"""/* v4.125 : l'import vit dans le menu Transmettre (groupe « L'archive ») —
   l'item importMenuBtn et le bouton du pied de rail déclenchent le même file picker. */
["importMenuBtn"].forEach(function(id){
  const b = document.getElementById(id);
  if(b) b.addEventListener("click", () => { document.getElementById("importInput").click(); });
});""",
"4c. le câblage du nouvel item")

# ── 5. la tuile ouverte = une ligne ──────────────────────────────────────────
remplace(
"""    return `
      <button class="tab-card st-${sc.statut || "essai"} ${sc.id === activeId ? "active" : ""} ${sc.baseline ? "is-baseline" : ""}" data-tab="${sc.id}">
        <span class="tc-head">
          <span class="tc-num">${numero}</span>
          <span class="tc-name">${escapeAttr(sc.name)}${sc.baseline ? " ★" : ""}</span>
        </span>""",
"""    /* v4.125 (brief P1-3) : la tuile ouverte = UNE LIGNE (nom + ★) — le nom et
       le statut y sont déjà portés par la fiche en dessous, les chiffres par
       les autres tuiles. FAILED reste visible sur la fiche (verdict tampon). */
    if(sc.id === activeId) return `
      <button class="tab-card active ${sc.baseline ? "is-baseline" : ""}" data-tab="${sc.id}" title="Scénario affiché — sa fiche est en dessous">
        <span class="tc-head">
          <span class="tc-num">${numero}</span>
          <span class="tc-name">${escapeAttr(sc.name)}${sc.baseline ? " ★" : ""}</span>
        </span>
      </button>
    `;
    return `
      <button class="tab-card st-${sc.statut || "essai"}" data-tab="${sc.id}">
        <span class="tc-head">
          <span class="tc-num">${numero}</span>
          <span class="tc-name">${escapeAttr(sc.name)}${sc.baseline ? " ★" : ""}</span>
        </span>""",
"5. la tuile ouverte = une ligne")

# ── 6. le bandeau coût vide devient une ligne grise ─────────────────────────
remplace(
"""  pcbDernier = p;
  const nomBase = (p.ops.find(o => o.prodSc) || {prodSc:null}).prodSc;""",
"""  pcbDernier = p;
  /* v4.125 (brief P1-3) : un état vide ne pèse pas comme une donnée — cible non
     renseignée, rien réalisé, rien possible : une ligne grise, pas un bandeau bleu. */
  if(p.cible === null && p.realise <= 0.0005 && p.reste <= 0.0005)
    return `<div class="pcb-vide" title="Renseignez la cible de coût pièce du site (champ cible de la référence) et les essais porteront leur écart ici.">Cible de coût non renseignée — ${escapeAttr(p.ref.nom || "")} coûte ${fmt(p.aujourdhui,3)} €/pièce aujourd'hui. <b>La renseigner</b></div>`;
  const nomBase = (p.ops.find(o => o.prodSc) || {prodSc:null}).prodSc;""",
"6a. la ligne grise sur état vide")

remplace(
""".boussole{display:flex; gap:6px; flex-wrap:wrap; align-items:center; margin:0 0 12px;}""",
""".pcb-vide{display:block; margin:0 0 10px; padding:9px 12px; border:1px dashed var(--border); border-radius:var(--radius-sm);
  background:var(--gray-50); font-size:12.5px; color:var(--ink-soft);}
.pcb-vide b{color:var(--blue); cursor:pointer;}
.boussole{display:flex; gap:6px; flex-wrap:wrap; align-items:center; margin:0 0 12px;}""",
"6b. le style de la ligne grise")

# ── 7. l'anneau de focus : la Vue d'ensemble ne vole pas le focus ────────────
remplace(
"""  document.getElementById("panelBackdrop").hidden = false;
  // le focus entre dans le panneau ouvert : premier champ, sinon le panneau lui-meme —
  // sinon il reste derriere le voile et Tab ressort de la fenetre invisible.
  const cible = pan.querySelector(SELECTEUR_FOCUSABLE);
  if(cible && cible.getClientRects().length) cible.focus();
  else { pan.tabIndex = -1; pan.focus({ preventScroll:true }); }""",
"""  document.getElementById("panelBackdrop").hidden = false;
  // le focus entre dans le panneau ouvert : premier champ, sinon le panneau lui-meme —
  // sinon il reste derriere le voile et Tab ressort de la fenetre invisible.
  // v4.125 (brief P1, détail) : un panneau data-sans-focus (la Vue d'ensemble) ne vole
  // pas le focus — l'anneau ne se pose plus sur « Postes » (le premier focusable)
  // alors que l'onglet actif est « Lignes ».
  if(pan.getAttribute("data-sans-focus") === "1"){ pan.tabIndex = -1; pan.focus({ preventScroll:true }); return; }
  const cible = pan.querySelector(SELECTEUR_FOCUSABLE);
  if(cible && cible.getClientRects().length) cible.focus();
  else { pan.tabIndex = -1; pan.focus({ preventScroll:true }); }""",
"7a. ouvrirPanneau respecte data-sans-focus")

remplace(
"""  <div class="panel panel-large" id="accueilPanel" hidden></div>""",
"""  <div class="panel panel-large" id="accueilPanel" data-sans-focus="1" hidden></div>""",
"7b. la Vue d'ensemble ne vole pas le focus")

io.open(p, "w", encoding="utf-8").write(s)
print("patch A posé :", n0, "->", len(s))
