# -*- coding: utf-8 -*-
"""Tour 105 — v4.127.1 — ÉTAPE 0 de la feuille de route.

1. Le plancher atelier par MutationObserver throttlé : en mode atelier,
   AUCUN texte visible ne descend sous 12 px (le brief mesure 141 éléments ;
   les 276 sélecteurs < 12 px rendent la couverture CSS irréaliste).
2. Disques ::before supprimés en atelier (le cadre plein suffit), filigrane
   masqué, étiquettes des boutons icône seule.
3. SPK_MAJ : mêmes gardes que _spkVerifierVersion.
4. version.json en network-only dans le SW.
5. Gabarits A4 : pile mono complète."""
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


# ── 1. le plancher atelier (dans le câblage du mode) ─────────────────────────
remplace(
"""  function poserCSS(){
    let st = document.getElementById("spkAtelierCSS");
    if(!st){
      st = document.createElement("style");
      st.id = "spkAtelierCSS";
      document.head.appendChild(st);
    }
    st.textContent = document.documentElement.getAttribute("data-mode") === "atelier" ? CSS : "";
  }""",
"""  function poserCSS(){
    let st = document.getElementById("spkAtelierCSS");
    if(!st){
      st = document.createElement("style");
      st.id = "spkAtelierCSS";
      document.head.appendChild(st);
    }
    st.textContent = document.documentElement.getAttribute("data-mode") === "atelier" ? CSS : "";
  }
  /* v4.127.1 (étape 0.2) — LE PLANCHER 12 px : en mode atelier, un
     MutationObserver throttlé remonte à 12 px tout texte visible rendu plus
     petit (les 276 sélecteurs < 12 px des CSS rendent la couverture CSS
     irréaliste — le brief le prescrit). Les éléments à font-size 0
     (volontairement masqués) sont exclus. En sortie de mode : restauration. */
  const PLANCHER = 12;
  let obsAtelier = null, passeEnCours = false;
  function passePlancher(){
    if(passeEnCours || document.documentElement.getAttribute("data-mode") !== "atelier") return;
    passeEnCours = true;
    try{
      const tous = document.querySelectorAll("body *");
      for(const el of tous){
        const r = el.getBoundingClientRect();
        if(r.width <= 0 || r.height <= 0) continue;
        if(el.children.length && ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
        const st = getComputedStyle(el);
        const fs = parseFloat(st.fontSize);
        if(isNaN(fs) || fs <= 1) continue;          /* masqués volontairement */
        if(fs >= PLANCHER) continue;
        if(el.dataset.spkPlancher === undefined) el.dataset.spkPlancher = el.style.fontSize || "";
        el.style.fontSize = PLANCHER + "px";
      }
    }catch(e){}
    passeEnCours = false;
  }
  function restaurerPlancher(){
    document.querySelectorAll("[data-spk-plancher]").forEach(el => {
      if(el.dataset.spkPlancher) el.style.fontSize = el.dataset.spkPlancher;
      else el.style.removeProperty("font-size");
      delete el.dataset.spkPlancher;
    });
  }
  function brancherPlancher(){
    if(obsAtelier || !window.MutationObserver) return;
    let timer = null;
    const programme = () => {
      if(timer) clearTimeout(timer);
      timer = setTimeout(() => { timer = null; passePlancher(); }, 200);
    };
    obsAtelier = new MutationObserver(programme);
    obsAtelier.observe(document.body, { childList: true, subtree: true, attributes: true, characterData: false });
  }
  function debrancherPlancher(){
    if(obsAtelier){ obsAtelier.disconnect(); obsAtelier = null; }
    restaurerPlancher();
  }""",
"1. le plancher 12px par MutationObserver")

remplace(
"""  if(mode === "atelier") document.documentElement.setAttribute("data-mode", "atelier");
  else document.documentElement.removeAttribute("data-mode");
  window._spkSetMode = function(m){""",
"""  if(mode === "atelier"){
    document.documentElement.setAttribute("data-mode", "atelier");
    brancherPlancher();
  } else {
    document.documentElement.removeAttribute("data-mode");
    debrancherPlancher();
  }
  window._spkSetMode = function(m){""",
"2. le branchement dans le set initial")

remplace(
"""    if(m === "atelier") document.documentElement.setAttribute("data-mode", "atelier");
    else document.documentElement.removeAttribute("data-mode");
    try{ localStorage.setItem(CLE, m); }catch(e){}
    poserCSS();""",
"""    if(m === "atelier"){
      document.documentElement.setAttribute("data-mode", "atelier");
      brancherPlancher();
    } else {
      document.documentElement.removeAttribute("data-mode");
      debrancherPlancher();
    }
    try{ localStorage.setItem(CLE, m); }catch(e){}
    poserCSS();""",
"3. le branchement dans _spkSetMode")

# ── 2. atelier : disques, filigrane, étiquettes, chevauchement ───────────────
remplace(
"""    + "html[data-mode=\\"atelier\\"] input.cell-cycle:focus{ background:var(--surface); color:var(--fill); border-color:var(--bord-atelier); }"
    + "html[data-mode=\\"atelier\\"] .spk-rail-mark span, html[data-mode=\\"atelier\\"] .spk-rail-version, html[data-mode=\\"atelier\\"] .spk-rail-live{ font-size:14px !important; }\"""",
"""    + "html[data-mode=\\"atelier\\"] input.cell-cycle:focus{ background:var(--surface); color:var(--fill); border-color:var(--bord-atelier); }"
    + "html[data-mode=\\"atelier\\"] .spk-rail-mark span, html[data-mode=\\"atelier\\"] .spk-rail-version, html[data-mode=\\"atelier\\"] .spk-rail-live{ font-size:14px !important; }"
    + "html[data-mode=\\"atelier\\"] button::before, html[data-mode=\\"atelier\\"] .btn-serie::before{ content:none !important; }"
    + "html[data-mode=\\"atelier\\"] body{ background-image:none !important; }"
    + "html[data-mode=\\"atelier\\"] .toolbar button[data-etiquette]::after{ content:attr(data-etiquette); font-size:13px; font-weight:600; margin-left:6px; }\"""",
"4. disques/filigrane/étiquettes en atelier")

# les étiquettes sur les boutons icône seule
remplace(
"""      <button class="ghost" id="lockBtn" title="Passe l'outil en lecture seule — pour l'écran partagé d'atelier">""",
"""      <button class="ghost" id="lockBtn" data-etiquette="Verrouiller" title="Passe l'outil en lecture seule — pour l'écran partagé d'atelier">""",
"5a. étiquette du verrou")

remplace(
"""      <button class="ghost" id="moreBtn" title="Plus d'actions">""",
"""      <button class="ghost" id="moreBtn" data-etiquette="Plus" title="Plus d'actions">""",
"5b. étiquette du menu plus")

# le chevauchement « + Créer un projet » : l'aide ⓘ repasse à la ligne en atelier
remplace(
'    + "html[data-mode=\\"atelier\\"] .pcb-st.arrete{ background:var(--gray-300); color:var(--ink); }"',
'    + "html[data-mode=\\"atelier\\"] .pcb-st.arrete{ background:var(--gray-300); color:var(--ink); }"\n    + "html[data-mode=\\"atelier\\"] .pj-aide{ display:none; }"',
"5c. l'aide projet repassée à la ligne (chevauchement)")

# ── 3. SPK_MAJ : les mêmes gardes ────────────────────────────────────────────
remplace(
"""  navigator.serviceWorker.addEventListener("message", (e) => {
    if(e.data && e.data.type === "SPK_MAJ"){
      if(window.caches && window.caches.keys){
        caches.keys().then((cles) => Promise.all(cles.map((c) => caches.delete(c))))
          .catch(() => {})
          .then(() => location.reload());
      } else { location.reload(); }
    }
  });""",
"""  navigator.serviceWorker.addEventListener("message", (e) => {
    if(e.data && e.data.type === "SPK_MAJ"){
      /* v4.127.1 (étape 0.4) — les MÊMES gardes que _spkVerifierVersion :
         pas de reload pendant une saisie, sauvegarde flushée, anti-boucle —
         sinon le bandeau non bloquant. */
      if(_spkSaisieAuFocus()){ _spkMajBandeau(); return; }
      try{ saveData(); }catch(e){}
      const cible = e.data.version || "nouvelle";
      const cle = "spk_maj_recharges_" + cible;
      let n = 0;
      try{ n = parseInt(sessionStorage.getItem(cle) || "0", 10) || 0; }catch(err){}
      if(n >= 2){ _spkMajBandeau(); return; }
      try{ sessionStorage.setItem(cle, String(n + 1)); }catch(err){}
      if(window.caches && window.caches.keys){
        caches.keys().then((cles) => Promise.all(cles.map((c) => caches.delete(c))))
          .catch(() => {})
          .then(() => location.reload());
      } else { location.reload(); }
    }
  });""",
"6. SPK_MAJ : les gardes")

io.open(p, "w", encoding="utf-8").write(s)
print("patch html posé :", n0, "->", len(s))
