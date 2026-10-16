# -*- coding: utf-8 -*-
"""Patch v4.52 : couche 2 (Ouvrir le poste + retour carte) + A4 Mission imprimable."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# ── 1. couche 2 : bouton « Ouvrir le poste → » dans chaque tuile non-opportunité ──
avant = """    ${t.etat === "opportunite" ? `<div class="ca-tentant">déclaré, jamais travaillé</div>` : ""}
    ${(p.nonChiffres || 0) > 0 ? `<div class="ca-avertir" title="Une opération de ce poste n'est pas chiffrable : le gain affiché ne la compte pas.">${p.nonChiffres} opération${p.nonChiffres > 1 ? "s" : ""} à chiffrer</div>` : ""}
  </div>`;
}"""
apres = """    ${t.etat === "opportunite" ? `<div class="ca-tentant">déclaré, jamais travaillé</div>` : ""}
    ${(p.nonChiffres || 0) > 0 ? `<div class="ca-avertir" title="Une opération de ce poste n'est pas chiffrable : le gain affiché ne la compte pas.">${p.nonChiffres} opération${p.nonChiffres > 1 ? "s" : ""} à chiffrer</div>` : ""}
    ${t.etat !== "opportunite" ? `<div class="ca-actions"><button class="primary small ca-ouvrir" data-ligne="${escapeAttr(t.ligne.id)}" data-code="${escapeAttr(t.code)}" title="Naviguer vers ce poste : scénarios, essais, preuves (couche 2)">Ouvrir le poste →</button></div>` : ""}
  </div>`;
}"""
assert s.count(avant) == 1, "bouton tuile"
s = s.replace(avant, apres)

# ── 2. câblage dans renderCarte (après carteClose) ──
avant = """  const btn = document.getElementById("carteClose");
  if(btn) btn.addEventListener("click", fermerPanneaux);"""
apres = """  const btn = document.getElementById("carteClose");
  if(btn) btn.addEventListener("click", fermerPanneaux);
  /* v4.52 — couche 2 : « Ouvrir le poste → » positionne la navigation experte sur la
     prod du poste (★ puis excel) et referme la carte ; le retour « ⇠ Carte atelier »
     vit dans la zone Traçabilité (A1). */
  wrap.querySelectorAll(".ca-ouvrir").forEach(b => {
    b.addEventListener("click", () => {
      const ligne = lignes.find(x => x.id === b.getAttribute("data-ligne"));
      const code = b.getAttribute("data-code");
      if(!ligne) return;
      const bloc = scenariosPostes(ligne, code)[0];
      if(!bloc) return;
      const prodSc = (bloc.scs || []).find(x => x.baseline)
                  || (bloc.scs || []).find(x => /base excel/i.test(x.name || ""))
                  || (bloc.scs || [])[0];
      if(!prodSc) return;
      activeLigneId = ligne.id;
      activeReferenceId = bloc.ref.id;
      activeOpId = bloc.op.id;
      activeId = prodSc.id;
      fermerPanneaux();
      render();
    });
  });
  /* v4.52 — A4 Mission : impression dédiée (le conteneur est appendé au body pour que
     la CSS d'impression n'affiche que lui). */
  const mBtn = document.getElementById("missionA4Btn");
  if(mBtn) mBtn.addEventListener("click", () => {
    const el = document.getElementById("missionA4") || document.body.appendChild(Object.assign(document.createElement("div"), { id: "missionA4", hidden: true }));
    el.innerHTML = missionA4HTML();
    document.body.classList.add("print-mission");
    const nettoie = () => { document.body.classList.remove("print-mission"); window.removeEventListener("afterprint", nettoie); };
    window.addEventListener("afterprint", nettoie);
    window.print();
    setTimeout(nettoie, 2000);
  });"""
assert s.count(avant) == 1, "wiring renderCarte"
s = s.replace(avant, apres)

# ── 3. bouton A4 Mission dans les actions du panneau carte ──
avant = """    <div class="panel-actions"><button class="primary" id="carteClose">Fermer</button></div>"""
apres = """    <div class="panel-actions"><button class="ghost" id="missionA4Btn">🖨 A4 Mission</button><button class="primary" id="carteClose">Fermer</button></div>"""
assert s.count(avant) == 1, "actions carte"
s = s.replace(avant, apres)

# ── 4. retour carte dans la zone Traçabilité ──
avant = """  wrap.innerHTML = `<div class="zone-band"><b>3 &middot; Traçabilité du scénario ouvert</b><span>outils, cycle, essais, rebut</span></div>` + scenarioBlockHTML(sc, true);"""
apres = """  wrap.innerHTML = `<div class="zone-band"><b>3 &middot; Traçabilité du scénario ouvert</b><span>outils, cycle, essais, rebut</span><button class="ghost small" id="retourCarteBtn" title="Revenir à la carte atelier" style="margin-left:auto;">⇠ Carte atelier</button></div>` + scenarioBlockHTML(sc, true);"""
assert s.count(avant) == 1, "zone band"
s = s.replace(avant, apres)

# ── 5. câblage du retour ──
avant = """function attachDetailHandlers(sc){
  const root = document.getElementById("scenarioDetail");"""
apres = """function attachDetailHandlers(sc){
  const root = document.getElementById("scenarioDetail");
  /* v4.52 — retour carte atelier depuis la traçabilité (A1 : jamais de cul-de-sac) */
  const retourCarte = root.querySelector("#retourCarteBtn");
  if(retourCarte) retourCarte.addEventListener("click", () => { renderCarte(); ouvrirPanneau("cartePanel"); });"""
assert s.count(avant) == 1, "câblage retour"
s = s.replace(avant, apres)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("couche 2 + retour carte OK")
