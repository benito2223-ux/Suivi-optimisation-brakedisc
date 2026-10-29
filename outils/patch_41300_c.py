# -*- coding: utf-8 -*-
# Tour 109 — 4.130.0 — patch C : la feuille de coque (spk-app.css) + la
# hauteur mesurée de l'en-tête (spk-shell.js).
# Un bloc final v4.130 qui surcharge : rangée 1 navy (mark + titre + actions),
# rangée 2 blanche (onglets soulignés, fil d'Ariane, + Scénario, bandeau
# projets compacté), liseré bas 3 px bleu, écrans plein écran repoussés sous
# l'en-tête, .hd et .toolbar du monolithe masqués, filigrane coin repoussé
# sous l'en-tête, media queries de resserrement.
import io

F = "spk-app.css"
src = io.open(F, encoding="utf-8").read()

BLOC = """

/* ════════════════════════════════════════════════════════════════════════════
   v4.130.0 — L'EN-TÊTE DU DESIGN SYSTEM (remplace le rail)
   Rangée 1 : navy --ink-navy, mark SPK + titre de la référence + actions.
   Rangée 2 : blanc, onglets soulignés (2 px bleu, 11 px/600/0,05 em
   majuscules) + fil d'Ariane 12 px + « + Scénario » + bandeau projets.
   Liseré bas 3 px bleu. Les écrans plein écran passent sous l'en-tête —
   la hauteur réelle est mesurée par la coque dans --spk-head-h.
   ════════════════════════════════════════════════════════════════════════════ */

:root { --spk-head-h: 98px; }

body.spk-has-head{ padding-top:0; }
body.spk-has-head .wrap{ margin-top:var(--spk-head-h); }

.spk-head{
  position:fixed; top:0; left:0; right:0; z-index:90;
  background:var(--ink-navy, #2F4159);
  border-bottom:3px solid #1B5EA6;
  box-shadow:0 2px 8px rgba(47,65,89,.18);
}
.spk-head-r1{
  display:flex; align-items:center; gap:16px;
  min-height:54px; padding:4px 18px;
}
.spk-head-mark{
  font-family:'Open Sans Condensed','Open Sans',Arial,sans-serif;
  font-size:26px; font-weight:700; letter-spacing:.04em; color:#fff;
  line-height:1; flex:0 0 auto;
}
.spk-head-mark span{
  display:block; font-family:'Open Sans',Arial,sans-serif;
  font-size:9px; font-weight:600; letter-spacing:.22em;
  text-transform:uppercase; color:rgba(255,255,255,.72);
}
.spk-head-titre{ flex:1 1 auto; min-width:0; }
.spk-head-titre h1{
  margin:0; color:#fff; font-size:20px; line-height:1.2;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.spk-head-actions{
  display:flex; align-items:center; gap:6px; flex:0 0 auto;
}
.spk-head-r1 button.ghost, .spk-head-r1 .toolbar-more-wrap > button{
  background:transparent; border:1px solid rgba(255,255,255,.28);
  color:#fff; border-radius:3px;
}
.spk-head-r1 button.ghost:hover, .spk-head-r1 .toolbar-more-wrap > button:hover{
  background:rgba(255,255,255,.12); border-color:rgba(255,255,255,.45);
}
.spk-head-r1 button.ghost .icon{ stroke:#fff; }
.spk-head-r1 .toolbar-more{
  background:#fff; color:var(--ink);
  border:1px solid var(--border, #e5e7eb); border-radius:3px;
  box-shadow:0 8px 24px rgba(0,0,0,.16);
}
.spk-head-r1 .save-status{ color:rgba(255,255,255,.72); font-size:11px; }

.spk-head-r2{
  display:flex; align-items:center; gap:16px;
  min-height:44px; padding:2px 18px;
  background:#fff; flex-wrap:wrap;
}
.spk-head-onglets{ display:flex; align-items:stretch; gap:18px; flex:0 1 auto; min-width:0; overflow-x:auto; }
.spk-head-links button{
  background:none; border:none; box-shadow:none;
  padding:12px 2px 10px; margin:0; border-radius:0;
  font-family:'Open Sans',Arial,sans-serif; font-size:11px; font-weight:600;
  letter-spacing:.05em; text-transform:uppercase;
  color:var(--ink, #1a1a1a); position:relative; white-space:nowrap;
  display:inline-flex; align-items:center; gap:6px;
}
.spk-head-links button .icon{ width:14px; height:14px; stroke:var(--blue, #1B5EA6); }
.spk-head-links button::after{
  content:""; position:absolute; left:0; right:0; bottom:-1px; height:2px;
  background:transparent;
}
.spk-head-links button:hover{ color:var(--blue, #1B5EA6); }
.spk-head-links button.is-active{ color:var(--blue, #1B5EA6); }
.spk-head-links button.is-active::after{ background:var(--blue, #1B5EA6); }

.spk-head-contexte{
  display:flex; align-items:center; gap:12px; flex:1 1 auto;
  min-width:0; flex-wrap:wrap; justify-content:flex-end;
}
.spk-head-contexte .fil-ariane{ font-size:12px; color:var(--label, #555); }
.spk-head-contexte .fil-ariane .fil-lib{ font-size:10px; }
.spk-head-contexte .fil-ariane .fil-val{ font-size:12px; }
.spk-head-contexte #addBtn{ flex:0 0 auto; }
.spk-head-contexte #projetsBandeau{ flex:0 1 auto; min-width:0; }
.spk-head-contexte #projetsBandeau .pj-entete{ margin:0; padding:0; background:none; border:none; }

/* le bandeau bleu de la fiche et la toolbar du monolithe : leurs éléments
   vivent dans l'en-tête maintenant — les cadres vides disparaissent. */
body.spk-has-head .hd{ display:none; }
body.spk-has-head .toolbar{ display:none; }
/* l'ancien rail : plus d'élément, plus de décalage */
body.spk-has-head .panel.panel-large,
body.spk-has-head #backlogWrap{
  left:0 !important; width:auto !important;
  top:var(--spk-head-h) !important;
}
body.spk-has-head #syntheseWrap{ margin-top:0; }
/* la poignée de repli du rail n'existe plus */
#spkRailToggle{ display:none !important; }
/* le filigrane au coin passe sous l'en-tête */
body[data-env="dev"][data-filigrane-code]:not([data-filigrane-code=""])::after{
  top:calc(var(--spk-head-h) + 8px);
}
/* le bouton Retour des espaces de travail suit */
#spkWorkspaceClose{ top:calc(var(--spk-head-h) + 12px); }

@media (max-width:760px){
  .spk-head-r1{ flex-wrap:wrap; padding:6px 12px; gap:8px; }
  .spk-head-mark{ font-size:20px; }
  .spk-head-titre{ flex:1 1 100%; order:3; }
  .spk-head-titre h1{ font-size:16px; white-space:normal; }
  .spk-head-actions{ margin-left:auto; }
  .spk-head-r1 .label-tb{ display:none; }
  .spk-head-r1 button.ghost{ min-width:44px; min-height:44px; justify-content:center; }
  .spk-head-r2{ gap:10px; padding:2px 12px; }
  .spk-head-onglets{ flex:1 1 100%; }
  .spk-head-contexte{ justify-content:flex-start; }
  body.spk-has-head .panel.panel-large,
  body.spk-has-head #backlogWrap{ top:var(--spk-head-h) !important; }
}

/* mode atelier : les actions de la barre restent des cibles de 56 px */
html[data-mode="atelier"] .spk-head-r1 button.ghost,
html[data-mode="atelier"] .spk-head-r1 .toolbar-more-wrap > button{
  min-width:56px; min-height:56px; justify-content:center;
}
html[data-mode="atelier"] .spk-head-links button{ min-height:56px; }
"""

src = src.rstrip() + "\n" + BLOC
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch C (spk-app.css) appliqué :", len(BLOC), "octets ajoutés")

# --- la hauteur mesurée dans spk-shell.js ------------------------------------
F2 = "spk-shell.js"
js = io.open(F2, encoding="utf-8").read()
ANCRE = """  /* l'ancien verrou d'animation du boot : retiré après deux frames
     (filet de secours par timeout, comme avant). */
  const finBoot = () => document.documentElement.classList.remove("spk-boot");
  requestAnimationFrame(() => requestAnimationFrame(finBoot));
  setTimeout(finBoot, 300);
"""
MESURE = ANCRE + """
  /* la hauteur réelle de l'en-tête nourrit --spk-head-h : les écrans plein
     écran et le filigrane du coin se posent sous la barre, quelle que soit
     la largeur (l'en-tête wrappe sur mobile). */
  if (window.ResizeObserver) {
    const poserHauteur = () => {
      document.documentElement.style.setProperty("--spk-head-h", head.offsetHeight + "px");
    };
    const obsHead = new ResizeObserver(poserHauteur);
    obsHead.observe(head);
    poserHauteur();
  }
"""
n = js.count(ANCRE)
assert n == 1, "ancre finBoot : %d occurrences (attendu 1)" % n
js = js.replace(ANCRE, MESURE)
io.open(F2, "w", encoding="utf-8", newline="\n").write(js)
print("patch C (spk-shell.js hauteur mesurée) appliqué")
