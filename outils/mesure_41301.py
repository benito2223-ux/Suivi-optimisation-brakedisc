# -*- coding: utf-8 -*-
"""Captures + mesures du rendu réel (1440 et 390) pour le lot 4.130.1.
Usage : python outils/mesure_41301.py [avant|apres]
Sortie : outils/captures_41301/{tag}_{vue}_{largeur}.png + mesures sur stdout.
"""
import sys, os, json
from playwright.sync_api import sync_playwright

TAG = sys.argv[1] if len(sys.argv) > 1 else "avant"
ICI = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(os.path.dirname(ICI), "dist", "bilan_economique.html")
SORTIE = os.path.join(ICI, "captures_41301")
os.makedirs(SORTIE, exist_ok=True)

MESURE_JS = """(() => {
  const res = {};
  res.scrollW = document.documentElement.scrollWidth;
  res.clientW = document.documentElement.clientWidth;
  res.deborde = res.scrollW > res.clientW + 1;
  /* les boutons .primary VISIBLES (rect intersectant le viewport + au centre) */
  const prim = [...document.querySelectorAll("button.primary, a.primary")].filter(b => {
    const r = b.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return false;
    if (r.bottom < 0 || r.top > innerHeight) return false;
    const c = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
    return !c || b.contains(c) || c.contains(b) || b === c;
  });
  res.primairesVisibles = prim.map(b => (b.textContent || "").trim().slice(0, 40));
  /* rangées du haut : rects des blocs d'en-tête connus */
  const ids = ["spk-head", "spk-tabs", "toolbar", "toolbarmore", "panelBackdrop"];
  res.blocs = ids.map(id => {
    const el = document.getElementById(id) || document.querySelector("." + id);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { id, top: Math.round(r.top), h: Math.round(r.height), w: Math.round(r.width) };
  }).filter(Boolean);
  res.head = document.querySelector(".spk-head") ? (() => {
    const r = document.querySelector(".spk-head").getBoundingClientRect();
    return { top: Math.round(r.top), h: Math.round(r.height) };
  })() : null;
  res.tabs = document.querySelector(".spk-tabs") ? (() => {
    const r = document.querySelector(".spk-tabs").getBoundingClientRect();
    return { top: Math.round(r.top), h: Math.round(r.height) };
  })() : null;
  /* la barre d'outils mobile : combien de rangées occupe-t-elle ? */
  const tb = document.getElementById("toolbar");
  if (tb) {
    const r = tb.getBoundingClientRect();
    res.toolbar = { top: Math.round(r.top), h: Math.round(r.height), w: Math.round(r.width),
      rangées: Math.round(r.height / 48) };
  }
  /* le premier contenu (h1 / première section) */
  const h1 = document.querySelector("h1, h2, h3");
  if (h1) res.premierContenu = Math.round(h1.getBoundingClientRect().top);
  /* débord INTERNE de l'en-tête : scrollW ne voit pas un flex fixed qui
     clippe ses enfants (le défaut « Verrouille…/Transmett… » coupés). */
  const r1el = document.querySelector(".spk-head-r1");
  if (r1el) {
    const rr = r1el.getBoundingClientRect();
    let somme = 0;
    [...r1el.children].forEach(c => { const s = getComputedStyle(c);
      somme += c.getBoundingClientRect().width + parseFloat(s.marginLeft||0) + parseFloat(s.marginRight||0); });
    res.r1 = { largeur: Math.round(rr.width), contenu: Math.round(somme), deborde: somme > rr.width + 1 };
  }
  return res;
})()"""

VUES = [("normal", None), ("atelier", None)]

with sync_playwright() as p:
    nav = p.chromium.launch()
    for w, h, nom in [(1440, 900, "1440"), (390, 844, "390")]:
        page = nav.new_page(viewport={"width": w, "height": h})
        page.goto("file:///" + DIST.replace("\\", "/"))
        page.wait_for_timeout(2500)
        # fermer la bannière nouveautés si elle bloque
        for sel in [".nv-fermer", "#nouveautesFermer", "button:has-text('Plus tard')"]:
            try:
                page.locator(sel).first.click(timeout=800)
                page.wait_for_timeout(400)
            except Exception:
                pass
        m = page.evaluate(MESURE_JS)
        png = os.path.join(SORTIE, f"{TAG}_normal_{nom}.png")
        page.screenshot(path=png, full_page=False)
        print(f"--- {nom}px [{TAG}] ---")
        print(json.dumps(m, ensure_ascii=False, indent=1))
        page.close()
    nav.close()
print("captures dans", SORTIE)
