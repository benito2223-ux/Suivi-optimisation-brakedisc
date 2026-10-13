# -*- coding: utf-8 -*-
"""Patch v4.87.0 : plein ecran generique pour les grands panneaux (accueil,
simulateur, plan, catalogue) + lisibilite majoree en mode maxi."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# ── 1. le CSS : la regle specifique devient generique + lisibilite maxi ─────
rep("#simulPanel.simul-maxi { position:fixed; inset:0; max-width:none; width:100vw; height:100vh; max-height:none; z-index:260; overflow:auto; border-radius:0; margin:0; }",
"""/* v4.87 — plein ecran GENERIQUE : tout .panel peut passer maxi (accueil,
   simulateur, plan, catalogue) — et les polices montent avec la surface. */
.panel.simul-maxi { position:fixed; inset:0; max-width:none; width:100vw; height:100vh; max-height:none; z-index:260; overflow:auto; border-radius:0; margin:0; padding:26px clamp(20px, 4vw, 64px); font-size:15.5px; }
.panel.simul-maxi .simul-table { font-size:16.5px; }
.panel.simul-maxi .simul-table th { font-size:13px; }
.panel.simul-maxi .panel-hint { font-size:14.5px; }
.panel.simul-maxi h3 { font-size:22px; }
.panel.simul-maxi .cell, .panel.simul-maxi select { font-size:14px; }""")

# ── 2. la fonction generique, a cote de simulMaxi ────────────────────────────
rep("function simulMaxi(){",
'''/* v4.87 — bascule plein ecran GENERIQUE : tout grand panneau peut passer
   maxi (CSS) et le mode natif est tente par-dessus (projection). ESC rend la
   main. Les panneaux restent fermables normalement une fois reduits. */
function basculerMaxi(idPanel, btn){
  const p = document.getElementById(idPanel);
  if(!p) return;
  const on = !p.classList.contains("simul-maxi");
  p.classList.toggle("simul-maxi", on);
  try{
    if(on && p.requestFullscreen) p.requestFullscreen().catch(() => {});
    else if(!on && document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(() => {});
  }catch(e){}
  if(btn) btn.textContent = on ? "\\u2922 Quitter le plein ecran" : "\\u26f6 Plein ecran";
}

function simulMaxi(){
  basculerMaxi("simulPanel", document.getElementById("simulMaxiBtn"));
}

function simulMaxi_legacy(){''')

# ── 3. bouton ⛶ dans le Plan ────────────────────────────────────────────────
rep('''    <div class="simul-actions" style="margin-top:12px;">
      <button class="ghost small" id="planExporter">\\u2935 Exporter le plan (CSV)</button>
    </div>''',
'''    <div class="simul-actions" style="margin-top:12px;">
      <button class="ghost small" id="planExporter">\\u2935 Exporter le plan (CSV)</button>
      <button class="ghost small" id="planMaxiBtn" title="Projection en r\\u00e9union">\\u26f6 Plein \\u00e9cran</button>
    </div>''')

# ── 4. wiring du bouton Plan dans renderPlan ────────────────────────────────
rep('''  const ex = document.getElementById("planExporter");
  if(ex) ex.addEventListener("click", planExporter);''',
'''  const ex = document.getElementById("planExporter");
  if(ex) ex.addEventListener("click", planExporter);
  const mx = document.getElementById("planMaxiBtn");
  if(mx) mx.addEventListener("click", () => basculerMaxi("planPanel", mx));''')

# ── 5. bouton ⛶ sur l'ACCUEIL (pied) + wiring ───────────────────────────────
rep('''      <button class="primary small" id="pfPlan" title="Le pas-\\u00e0-pas commercial : article par article, la cible SPK et le gain annuel \\u2014 r\\u00e9v\\u00e9l\\u00e9 ligne par ligne">\\u2694\\ufe0f Plan de conversion</button>''',
'''      <button class="primary small" id="pfPlan" title="Le pas-\\u00e0-pas commercial : article par article, la cible SPK et le gain annuel \\u2014 r\\u00e9v\\u00e9l\\u00e9 ligne par ligne">\\u2694\\ufe0f Plan de conversion</button>
      <button class="ghost small" id="pfAccueilMaxi" title="L'accueil en plein \\u00e9cran \u2014 pour projeter">\u26f6 Plein \u00e9cran</button>''')

rep('''  const cPlan = document.getElementById("pfPlan");
  if(cPlan) cPlan.addEventListener("click", ouvrirPlan);''',
'''  const cPlan = document.getElementById("pfPlan");
  if(cPlan) cPlan.addEventListener("click", ouvrirPlan);
  const cMaxi = document.getElementById("pfAccueilMaxi");
  if(cMaxi) cMaxi.addEventListener("click", () => basculerMaxi("accueilPanel", cMaxi));''')

# ── 6. version + nouveautes ──────────────────────────────────────────────────
s = s.replace('const TOOL_VERSION = "4.86.0";', 'const TOOL_VERSION = "4.87.0";', 1)
rep('''const NOUVEAUTES = [
  { version:"4.86.0", date:"14/10/2026", points:[''',
'''const NOUVEAUTES = [
  { version:"4.87.0", date:"14/10/2026", points:[
    "<b>\\u26f6 Plein \\u00e9cran partout o\\u00f9 \\u00e7a compte.</b> L'accueil, le Plan de conversion et le Simulateur passent en <b>vraie pleine surface</b> \\u2014 plus de colonne de 1120 px : tout l'\\u00e9cran, et les polices qui montent avec. Un bouton \\u26f6 sur chaque \\u00e9cran ; \\u00c9chap ou le m\\u00eame bouton rend la main."
  ]},
  { version:"4.86.0", date:"14/10/2026", points:[''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("patch v4.87.0 applique : plein ecran generique + lisibilite maxi")

# ── 7. harnais : la porte CSS lit les 3 marqueurs ────────────────────────────
h = open('build_harness.py', encoding='utf-8').read()
av_g = "const manquantes = ['.simul-note {', '.simul-table {', '.simul-resultat {', '#simulPanel.simul-maxi']"
ap_g = "const manquantes = ['.simul-note {', '.simul-table {', '.simul-resultat {', '.panel.simul-maxi', '.panel.simul-maxi .simul-table', 'function basculerMaxi']"
if av_g in h:
    h = h.replace(av_g, ap_g, 1)
    h = h.replace("console.log((manquantes.length ? '  ECHEC ' : '  ok  ') + 'simulateur : CSS pr\\u00e9sent dans le fichier r\\u00e9el (' + (4 - manquantes.length) + '/4 r\\u00e8gles)'",
                  "console.log((manquantes.length ? '  ECHEC ' : '  ok  ') + 'simulateur/plein ecran : CSS pr\\u00e9sent dans le fichier r\\u00e9el (' + (6 - manquantes.length) + '/6 r\\u00e8gles)'")
    open('build_harness.py', 'w', encoding='utf-8').write(h)
    print("porte harnais etendue a 6 regles")
else:
    print("!! porte harnais : ancre introuvable")
