# -*- coding: utf-8 -*-
"""Tour 99 — v4.124.0 — les 4 P0 du brief externe (chantier_zcode, Benjamin).

P0-1 : le commentaire `/* v4.121 acte II ... */` vivait DANS le template de la
tuile scénario — un commentaire JS dans des backticks se rend en TEXTE sur les
3 tuiles. Il sort du template (le commentaire monte au-dessus de la fonction).
P0-3 : le vert positionnel `.foot-cell:last-child` frappait « Temps de cycle »
(la validation a été déplacée au milieu par l'acte II d'Hermes). Le vert
devient une classe EXPLICITE `.is-ok` posée sur la validation seulement quand
le seuil est atteint ; durée de vie / €/arête / temps de cycle descendent dans
une ligne secondaire grise — 3 grandes cellules restent : coût, validation, gain.
P0-4 : #carteBtn et #dashboardBtn sont masqués du rail (display:none — les
onglets de la Vue d'ensemble les cliquent en interne, .click() marche sur un
bouton masqué)."""
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


# ── P0-1 : le commentaire quitte le template ─────────────────────────────────
remplace(
"""        ${!actif && an && an.gainAnnuel !== undefined ? `<span class="tc-row"><span class="tc-label">${an.gainAnnuel>=0?"Gain/an":"Perte/an"}</span><span class="tc-val ${an.gainAnnuel>=0?"tc-gain":"tc-perte"}">${(an.gainAnnuel>=0?"+":"−")+fmtEuroCourt(Math.abs(an.gainAnnuel))}</span></span>` : ""}
        /* v4.121 acte II : la mini-fiche de la tuile ouverte (plaquettes, cycle, essais, rebut) est supprimee - la fiche en dessous dit tout, un seul endroit */
      </button>
    `;""",
"""        ${!actif && an && an.gainAnnuel !== undefined ? `<span class="tc-row"><span class="tc-label">${an.gainAnnuel>=0?"Gain/an":"Perte/an"}</span><span class="tc-val ${an.gainAnnuel>=0?"tc-gain":"tc-perte"}">${(an.gainAnnuel>=0?"+":"−")+fmtEuroCourt(Math.abs(an.gainAnnuel))}</span></span>` : ""}
      </button>
    `;""",
"P0-1. le commentaire quitte le template des tuiles")

# ── P0-3a : le vert devient explicite + styles de la ligne secondaire ────────
remplace(
""".foot-cell:last-child{border-right:none; background:var(--fill-good);}
.foot-cell:last-child .l, .foot-cell:last-child .foot-sub{color:var(--fill-good-ink-soft);}""",
"""/* v4.124 (P0-3 du brief externe) — le vert n'est plus une POSITION (last-child
   frappait « Temps de cycle » depuis que la validation est remontée au milieu) :
   c'est un ÉTAT. .is-ok est posée par le JS sur la validation seulement quand
   le seuil est atteint. */
.foot-cell:last-child{border-right:none;}
.foot-cell.is-ok{background:var(--fill-good);}
.foot-cell.is-ok .l, .foot-cell.is-ok .foot-sub{color:var(--fill-good-ink-soft);}
/* v4.124 — la ligne secondaire de la fiche : durée de vie, €/arête, temps de
   cycle — de la précision utile, pas des chiffres de tête (brief P0-3). */
.foot-second{grid-column:1/-1; display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); border-top:1px solid var(--fill-line);}
.foot-second .fs-item{padding:9px 16px 10px; border-right:1px solid var(--fill-line); min-width:0;}
.foot-second .fs-item:last-child{border-right:none;}
.foot-second .fs-l{font-size:9px; text-transform:uppercase; letter-spacing:.05em; color:var(--fill-ink-soft); margin-bottom:3px; font-weight:500;}
.foot-second .fs-v{font-family:var(--font-disp); font-weight:700; font-size:16px; color:var(--fill-ink); font-variant-numeric:tabular-nums; line-height:1.15;}
.foot-second .fs-v small{font-family:var(--font-body); font-weight:500; font-size:10px; color:var(--fill-ink-soft); margin-left:2px;}
.foot-second .fs-sub{font-size:10.5px; color:var(--fill-ink-soft); margin-top:2px; line-height:1.35;}
.foot-second input.cell-cycle{font-family:var(--font-disp); font-weight:700; font-size:16px; font-variant-numeric:tabular-nums; color:var(--fill-ink); width:70px; border:1px solid transparent; border-bottom:2px dashed rgba(255,255,255,.5); border-radius:var(--radius-sm); background:transparent; padding:0 4px;}
.foot-second input.cell-cycle:hover{border-color:rgba(255,255,255,.5); background:rgba(255,255,255,.08);}
.foot-second input.cell-cycle:focus{border-color:var(--surface); outline:none; background:var(--surface); color:var(--blue);}""",
"P0-3a. vert explicite + styles ligne secondaire")

# ── P0-3b : la validation porte is-ok quand validée ──────────────────────────
remplace(
"""  const validationCell = `
      <div class="foot-cell">
        <div class="l">Validation scénario</div>""",
"""  const validationCell = `
      <div class="foot-cell${stats.validated ? " is-ok" : ""}">
        <div class="l">Validation scénario${stats.validated ? " — seuil atteint" : ""}</div>""",
"P0-3b. is-ok sur la validation validée")

# ── P0-3c : durée de vie / €/arête / temps de cycle descendent ───────────────
remplace(
"""  const vieScCell = dureeVieScenario(sc), vieBaseCell = base ? dureeVieScenario(base) : null;
  const foot = `""",
"""  const vieScCell = dureeVieScenario(sc), vieBaseCell = base ? dureeVieScenario(base) : null;
  /* v4.124 (P0-3) : les trois précisions (durée de vie, €/arête, temps de cycle)
     descendent dans une ligne secondaire grise — trois grandes cellules restent
     en tête (coût, validation, gain). Le champ cycle garde sa classe
     cell-cycle : le re-rendu recâble ses listeners. Les lignes foot-sub du
     cycle sont converties en .fs-sub (les div englobantes retirées). */
  const fs = t => t.replace(/<\\/?div[^>]*>/g, "").replace('class="foot-sub"', 'class="fs-sub"');
  const foot = `""",
"P0-3c-pre. le helper fs avant le foot")

remplace(
"""      <div class="foot-cell">
        <div class="l">Durée de vie visée</div>
        <div class="v mid">${vieScCell === null ? "—" : fmt(vieScCell,0)}<small>p/arête</small></div>
        ${!sc.baseline && vieBaseCell !== null
          ? `<div class="foot-sub">réf. ${fmt(vieBaseCell,0)} p/arête</div>`
          : `<div class="foot-sub">charnière du logement de référence</div>`}
      </div>
      <div class="foot-cell">
        <div class="l">€ / arête (tous logements)</div>
        <div class="v">${fmt(scenarioCostPerEdge(sc), 3)}<small>€</small></div>
      </div>
      <div class="foot-cell">
        <div class="l">Temps de cycle — indice base 100 (éditable)</div>
        ${cycleCell}
        ${cycleDeltaHtml}
        ${cycleModeLine}
        ${cycleSecLine}
        ${cycleMachineLine}
        ${cycleVfWarnLine}
      </div>
      
    </div>""",
"""      <div class="foot-second">
        <div class="fs-item">
          <div class="fs-l">Durée de vie visée</div>
          <div class="fs-v">${vieScCell === null ? "—" : fmt(vieScCell,0)}<small>p/arête</small>${!sc.baseline && vieBaseCell !== null ? `<small>· réf. ${fmt(vieBaseCell,0)}</small>` : ""}</div>
        </div>
        <div class="fs-item">
          <div class="fs-l">€ / arête (tous logements)</div>
          <div class="fs-v">${fmt(scenarioCostPerEdge(sc), 3)}<small>€</small></div>
        </div>
        <div class="fs-item">
          <div class="fs-l">Temps de cycle — indice base 100 (éditable)</div>
          <div class="fs-v" style="display:flex; align-items:baseline; gap:8px;">${cycleCell}${cycleDeltaHtml}</div>
          ${cycleModeLine ? fs(cycleModeLine) : ""}
          ${cycleSecLine ? fs(cycleSecLine) : ""}
          ${cycleMachineLine ? fs(cycleMachineLine) : ""}
          ${cycleVfWarnLine ? fs(cycleVfWarnLine) : ""}
        </div>
      </div>
    </div>""",
"P0-3c. la ligne secondaire remplace les 3 cellules")

# ── P0-4 : Atelier / Tableau quittent le rail ────────────────────────────────
remplace(
""".toolbar-ecrans button{ position:relative; }""",
""".toolbar-ecrans button{ position:relative; }
/* v4.124 (P0-4 du brief externe) — la Vue d'ensemble porte ses propres onglets
   Lignes · Postes · Tableau (4.122) : les boutons Atelier / Tableau quittent le
   rail. display:none les garde dans le DOM — les onglets de la Vue d'ensemble
   les cliquent en interne (.click() fonctionne sur un bouton masqué). */
.toolbar-ecrans #carteBtn, .toolbar-ecrans #dashboardBtn{ display:none; }""",
"P0-4. Atelier/Tableau masqués du rail")

io.open(p, "w", encoding="utf-8").write(s)
print("patch A posé :", n0, "->", len(s))
