# DOSSIER DE REVUE — suivi SPK Sept Fons (extrait auto-contenu)

Tu es un relecteur critique EXTERIEUR. Cet outil a ete construit par deux IA
(Z Code + Hermes) qui sont fieres de leur travail — ne le sois pas a leur place.
Ton travail : trouver ce qui cloche, ce qui va casser, ce qui fera fuir
l'utilisateur. Tu PROPOSES, tu ne codes pas.

LE PROJET : suivi d'optimisation du cout de revient des disques de frein
(usinage ceramique, Stellantis Sept Fons). UN SEUL fichier HTML (~19 200 lignes),
zero build, zero SDK, offline-first, PWA. Trois publics : l'atelier (Matis,
operateurs, GANTS + TABLETTE, saisie rapide et bruyante), le pilote, la
hierarchie (documents imprimables). L'outil est AUSSI un outil commercial : il
doit demontrer a Matis l'economie du passage sur les plaquettes SPK.

VERSION COURANTE : 4.89.0 — 551 tests verts (harnais maison dans build_harness.py).

REGLES DU JEU (extrait de la constitution, a respecter dans tes directives) :
- aucun chiffre mensonger : un absent se NOMME, jamais un zero qui pretend ;
- cout plaquette et temps machine = DEUX AXES, jamais sommes ;
- ne pas additionner des gains de natures differentes ;
- K (Vc x Hex) et P_req n'apparaissent JAMAIS dans les sorties visibles (secret
  interne SPK) — verifie qu'aucun extrait ne les expose ;
- les donnees reelles ne sortent jamais du poste.

Ce dossier contient des EXTRAITS choisis, pas tout le fichier : declare ce que
tu n'as pas pu evaluer. Format de ta reponse : verdict en 5 lignes (sans
complaisance), puis 5 a 10 directives PRIORISEES (P1/P2/P3) — chacune avec
probleme, pourquoi, directive concrete pour Z Code, effort S/M/L. Termine par
ce qui est bien fait (court) et ce qui t'a manque.

Axes imposes : (A) ergonomie de saisie atelier (gants, tablette, bruit),
(B) hierarchie visuelle (Benjamin dit : « tout est ton sur ton, trop petit »),
(C) le monolithe de 19 200 lignes (ou est la limite ?), (D) la coherence du
socle commercial (catalogue, plan de conversion, basculeur, simulateur),
(E) les angles morts (etats globaux, hors ligne, deux postes en parallelle).

=== EXTRAITS ===

--- 1. CSS (regles cles : tokens, conteneur, panneaux, tuiles, champs, tables) ---


:root{
:root{
:root{
.wrap{max-width:1180px; margin:0 auto; padding:36px 24px 90px;}
.wrap{padding:20px 14px 70px;}
.wrap{ max-width:none; padding:0; }
.hd h1{font-family:var(--font-disp); font-weight:800; font-size:clamp(24px,3.4vw,32px); margin:0; line-height:1.05; color:var(--head-ink); min-width:0; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
.hd img{height:44px; width:auto; flex-shrink:0;}
body{background:var(--bg); color:var(--ink); font-family:var(--font-body); font-size:15px; line-height:1.55; margin:0;}
body{ -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; }
body{ background:#fff; font-size:11.5px; }
body{ background-image:none !important; }
body{font-family:Arial,'IBM Plex Sans',sans-serif; color:#1c211e; max-width:900px; margin:32px auto; padding:0 20px; line-height:1.5;}
body{font-family:'Open Sans',Arial,sans-serif; color:var(--ink); max-width:860px; margin:36px auto; padding:0 24px 60px; line-height:1.5; font-size:14px;}
.panel.simul-maxi { position:fixed; inset:0; max-width:none; width:100vw; height:100vh; max-height:none; z-index:260; overflow:auto; border-radius:0; margin:0; padding:26px clamp(20px, 4vw, 64px); font-size:15.5px; }
.panel.simul-maxi .simul-table { font-size:16.5px; }
.panel.simul-maxi .simul-table th { font-size:13px; }
.panel.simul-maxi .panel-hint { font-size:14.5px; }
.panel.simul-maxi h3 { font-size:22px; }
.panel.simul-maxi .cell, .panel.simul-maxi select { font-size:14px; }
.panel-search{width:min(580px,94vw);}
.panel-search #searchInput{width:100%; font-size:16px; padding:10px 12px; margin-bottom:8px;}
.btn-essai, .outil-add, .outils-copier, .outils-completer, .scrap-add, .piece-add,
.oc-simultane{display:flex; align-items:center; gap:8px; margin:0 0 10px; padding:6px 10px;
.oc-simultane:hover{border-color:var(--blue); color:var(--ink);}
.oc-champ{display:flex; flex-direction:column; gap:3px; min-width:0;}
.oc-champ > label{font-family:var(--font-mono); font-size:11px; font-weight:500; letter-spacing:.02em;
.oc-champ > label span{font-weight:500; opacity:.75;}
.oc-champ input.cell{width:100%; font-size:14px; padding:7px 9px; border:1px solid var(--border);
.oc-champ input.cell:hover{border-color:var(--ink-faint);}
.oc-champ input.cell:focus{border-color:var(--blue); outline:2px solid color-mix(in srgb, var(--blue) 25%, transparent); outline-offset:0;}
.at-charniere{margin:12px 0 4px; padding:14px 18px; border-radius:var(--radius); background:var(--gray-50); border:2px solid var(--amber); color:var(--amber); font-weight:700; font-size:17px; line-height:1.45;}
.at-charniere.depassee{background:var(--gray-50); border-color:var(--green); color:var(--green);}
.at-head{display:flex; align-items:flex-start; justify-content:space-between; gap:16px;}
.at-titre{font-family:var(--font-body); font-weight:700; font-size:24px; letter-spacing:-.01em; color:var(--ink);}
.at-sous{margin-top:3px; font-size:13px; color:var(--ink-faint); font-family:var(--font-mono);}
.at-close{min-height:48px; padding:12px 20px; font-size:15px;}
.at-logements{display:flex; gap:10px; flex-wrap:wrap;}
.at-log{flex:1 1 130px; min-height:64px; border-radius:var(--radius); border:2px solid var(--border);
.lb-tete{display:flex; flex-wrap:wrap; gap:10px 14px; align-items:flex-end; margin-bottom:12px;}
.lb-tol{display:flex; align-items:center; gap:7px; font-size:12.5px; color:var(--ink-soft);
.lb-tol input{width:17px; height:17px; accent-color:var(--blue); flex:0 0 auto;}
.lb-tete .logement-del{margin-left:auto; margin-bottom:4px;}
.lb-groupes{display:flex; flex-wrap:wrap; gap:10px;}
.lb-groupe{flex:1 1 auto; min-width:0; background:var(--surface-alt); border:1px solid var(--border);
.lb-groupe.lb-resultats{flex:0 0 auto; margin-left:auto; background:var(--gray-50); border-color:color-mix(in srgb, var(--blue) 30%, transparent);}
.lb-groupe.lb-resultats .oc-calc{background:var(--surface); color:var(--blue-dark); font-weight:500;}
.simul-note { background:#eef4fb; border:1px solid #cfe0f3; border-radius:4px; padding:9px 13px; font-size:13px; color:#1b5ea6; margin-bottom:14px; }
.simul-controles { display:flex; align-items:center; gap:10px; margin-bottom:12px; font-size:14px; }
.simul-controles input { width:80px; font-family:var(--font-mono); }
.simul-table { width:100%; border-collapse:collapse; font-size:13.5px; }
.simul-table th, .simul-table td { padding:7px 9px; border-bottom:1px solid #e4e6ea; text-align:left; }
.simul-table th { font-size:12px; color:#666; font-weight:600; text-transform:uppercase; letter-spacing:.03em; }
.simul-table td.mono, .simul-table tfoot td { font-family:var(--font-mono); }
.simul-table tfoot td { font-weight:600; border-top:2px solid #d6d9de; }
.os-sim{font-family:var(--font-mono); font-size:9.5px; font-weight:500; letter-spacing:.04em;
.os-grip{cursor:grab; color:var(--ink-faint); font-size:12px; line-height:1; padding:0 1px; user-select:none;}
.os-grip:active{cursor:grabbing;}
.os-numero{font-family:var(--font-mono); font-size:14.5px; font-weight:500; color:var(--ink);}
.os-corr{font-family:var(--font-mono); font-size:11.5px; color:var(--ink-faint); border:1px solid var(--border);
.os-desc{font-size:13px; color:var(--ink-soft); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:34ch;}
.os-logements{font-family:var(--font-mono); font-size:12px; color:var(--ink-faint);}
.os-plan{font-family:var(--font-mono); font-size:11px; font-weight:500; color:var(--teal);
.foot-cell input.cell-cycle, .essai-titre, .aide-step b, .marposs-kpis .v, .panel h3,
.foot-cell .v, .foot-cell input.cell-cycle, .fv-titre{ letter-spacing:-.025em; }
.foot-cell-wide{grid-column:span 2;}
.foot-cell{padding:14px 16px; border-right:1px solid var(--fill-line);}
.foot-cell-annuel{cursor:pointer;}
.foot-cell-annuel:hover{background:var(--fill-line);}
.foot-cell:last-child{border-right:none; background:var(--fill-good);}
.foot-cell:last-child .l, .foot-cell:last-child .foot-sub{color:var(--fill-good-ink-soft);}
.status-badge.risk{background:var(--white); color:var(--red-dark); border:1px solid var(--red-dark);}
.status-badge.risk::before{content:"!";}
.status-badge{display:inline-flex; align-items:center; gap:4px; font-family:var(--font-mono); font-size:10.5px; font-weight:500; padding:3px 10px; border-radius:var(--radius); letter-spacing:.02em; white-space:nowrap;}
.status-badge.ok{background:var(--green); color:var(--on-accent);}
.status-badge.ok::before{content:"✓";}
.status-badge.pending{background:var(--amber); color:var(--on-accent);}
.status-badge.pending::before{content:"⏳";}
.status-badge.arrete{background:var(--ink-faint); color:#fff;}

--- 2. L'ECRAN D'ACCUEIL (rendu) ---

function renderAccueil(){
  const wrap = document.getElementById("accueilPanel");
  if(!wrap) return;
  const gls = lignes.map(l => gainLigne(l, LIGNES_SEPT_FONS));
  /* v4.61 — Q12 : les lignes hors périmètre quittent la grille au rang d'une
     ligne vivante : elles vivent ensemble dans UNE tuile groupée, à la fin.
     La grille ne dit plus « six choses à faire » — la tuile dit leur nombre. */
  const vivantes = gls.filter(gl => !ligneHorsPerimetre(gl));
  const hors = gls.filter(ligneHorsPerimetre);
  const tuiles = vivantes.map(accueilTuileHTML).join("")
    + (hors.length ? accueilHorsTuileHTML(hors) : "");

  /* la recette A2 : l'écran dit s'il sert — actionnable = la pastille n'est pas
     « ouvert ». Le périmètre compte les lignes VIVANTES ; les hors périmètre
     sont dites à part, elles ne diluent pas le ratio. Sous 1/3 : creux, dit. */
  const total = vivantes.length;
  const actionnables = vivantes.filter(gl => etatLigne(gl).etat !== "opportunite").length;
  const ratio = total ? actionnables / total : 0;
  const recette = (total || hors.length)
    ? `<div class="al-recette ${total && ratio < 1/3 ? "al-recette-creuse" : ""}">`
      + (total && ratio < 1/3 ? `Écran creux : ` : ``)
      + `${actionnables} ligne${actionnables > 1 ? "s" : ""} actionnable${actionnables > 1 ? "s" : ""} sur ${total || 0} dans le périmètre`
      + (total && ratio < 1/3 ? ` — moins d'un tiers : cet écran n'éclaire pas encore l'usine` : ``)
      + (hors.length ? ` · ${hors.length} ligne${hors.length > 1 ? "s" : ""} hors périmètre` : ``)
      + `</div>`
    : "";

  wrap.innerHTML = `
    <div class="bd-entete">
      <div class="bd-accent"></div> <div class="bd-ariane">parc usinage sept-fons · lignes haute cadence</div>
      <div class="bd-titre-ligne">
        <h3 class="bd-titre">Tableau de bord des lignes d'usinage</h3>
        <span class="bd-perimetre">${escapeAttr(accueilPerimetreHTML(vivantes) || "usine")}</span>
        <div class="bd-index ${total && ratio < 1/3 ? "bd-index-surveiller" : ""}" title="La recette de l'écran : les lignes qu'il éclaire vraiment">
          ${total && ratio < 1/3 ? "à surveiller" : "conforme"} · ${actionnables}/${total || 0} actives${hors.length ? ` · ${hors.length} hors périmètre` : ""}
        </div>
      </div>
      <p class="bd-sous">L'usine par lignes : gains actés et en cours dans deux blocs séparés, coût pièce
        étiqueté vers la cible du site, et la prochaine étape de chaque machine — chaque chiffre
        remonte à sa source, chaque absence dit ce qui manque.</p>
    </div>
    ${accueilBandeauHTML(gls)}
    <div class="ca-grille al-grille">${tuiles}</div>
    ${recette}
    ${accueilMatriceHTML(gls)}
    ${accueilPiedHTML()}
    <div class="panel-actions"><button class="primary" id="alClose">Fermer</button></div>`;

  const fermer = document.getElementById("alClose");
  if(fermer) fermer.addEventListener("click", fermerPanneaux);
  wrap.querySelectorAll(".al-ouvrir").forEach(btn =>
    btn.addEventListener("click", ev => { ev.stopPropagation(); ouvrirCarte(btn.getAttribute("data-ligne")); }));
  wrap.querySelectorAll(".al-tuile:not(.al-hors)").forEach(t => {
    t.addEventListener("click", () => ouvrirCarte(t.getAttribute("data-ligne")));
    t.addEventListener("keydown", ev => { if(ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); ouvrirCarte(t.getAttribute("data-ligne")); } });
  });
  /* v4.65.2 — la porte de la matrice : même mécanique que la carte (couche 2) */
  wrap.querySelectorAll(".mx-ouvrir").forEach(b => {
    b.addEventListener("click", ev => {
      ev.stopPropagation();
      const ligne = lignes.find(x => x.id === b.getAttribute("data-ligne"));
      const code = b.getAttribute("data-code");
      if(!ligne) return;
      const bloc = scenariosPostes(ligne, code)[0];
      if(!bloc) return;
      const prodSc = (bloc.scs || []).find(x => x.baseline)
                  || (bloc.scs || []).find(x => /base excel/i.test(x.name || ""))
                  || (bloc.scs || [])[0];
      if(!prodSc) return;
      activeLigneId = ligne.id; activeReferenceId = bloc.ref.id; activeOpId = bloc.op.id; activeId = prodSc.id;
      fermerPanneaux(); render();
    });
  });
  /* les trois actions du pied : les boutons EXISTANTS de la barre, exposés —
     on ne crée pas de seconde implémentation */
  const cCarte = document.getElementById("pfCarte");
  if(cCarte) cCarte.addEventListener("click", ouvrirCarte);
  const cExport = document.getElementById("pfExport");
  if(cExport) cExport.addEventListener("click", () => { const b = document.getElementById("exportBtn"); if(b) b.click(); });
  const cHisto = document.getElementById("pfHisto");
  if(cHisto) cHisto.addEventListener("click", () => { const b = document.getElementById("historyBtn"); if(b) b.click(); });
  /* v4.78 — la vue CPP : la porte depuis l'accueil, là où la hiérarchie regarde */
  const cSimul = document.getElementById("pfSimul");
  if(cSimul) cSimul.addEventListener("click", ouvrirSimul);
  const cCat = document.getElementById("pfCatalogue");
  if(cCat) cCat.addEventListener("click", ouvrirCatalogue);
  const cMaxi = document.getElementById("pfAccueilMaxi");
  if(cMaxi) cMaxi.addEventListener("click", () => basculerMaxi("accueilPanel", cMaxi));
  const cPlan = document.getElementById("pfPlan");
  if(cPlan) cPlan.addEventListener("click", ouvrirPlan);
  const cCpp = document.getElementById("pfVueCpp");
  if(cCpp) cCpp.addEventListener("click", ouvrirVueCpp);
  /* la tuile hors périmètre déplie sa liste — le geste de Q12, pas la porte carte */
  const thors = wrap.querySelector(".al-hors");
  if(thors){
    const toggle = () => { accueilHorsDeplie = !accueilHorsDeplie; renderAccueil(); };
    thors.addEventListener("click", toggle);
    thors.addEventListener("keydown", ev => { if(ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); toggle(); } });
  }
}


function accueilBandeauHTML(gls){
  const vivantes = gls.filter(gl => !ligneHorsPerimetre(gl));

  /* 1. Économie validée : Σ gainActe, périmètre ÉCRIT — jamais « 100 % audité » */
  const acte = vivantes.reduce((a, gl) => a + (gl.gainActe || 0), 0);
  const nbActe = vivantes.filter(gl => (gl.gainActe || 0) > 0).length;
  const bloc1 = nbActe
    ? { v: `+${fmtEuroCourt(Math.round(acte))}`, u: "/an",
        sub: `sur ${nbActe} ligne${nbActe > 1 ? "s" : ""} qualifiée${nbActe > 1 ? "s" : ""} série` }
    : { v: "—", u: "", sub: "aucun gain acté — premiers passages en série en attente" };

  /* 2. Ralliement cible CPP : le reste à capter, CALCULÉ par ligne chiffrable
     (coût prod de la dominante − sa cible) × son volume. Les lignes à cible
     sans volume se comptent à part : leur absence se dit, elle ne s'invente pas. */
  let reste = 0, nbCible = 0, nbCibleSansVol = 0;
  vivantes.forEach(gl => {
    const cp = gl.coutPiece;
    if(!cp || cp.cible === null) return;
    if(!gl.volumeDominante){ nbCibleSansVol++; return; }
    if(cp.prod > cp.cible){ reste += (cp.prod - cp.cible) * gl.volumeDominante; nbCible++; }
  });
  const bloc2 = nbCible
    ? { v: `${fmtEuroCourt(Math.round(reste))}`, u: "€/an restants",
        sub: `cible du site · ${nbCible} ligne${nbCible > 1 ? "s" : ""} chiffrée${nbCible > 1 ? "s" : ""}`
            + (nbCibleSansVol ? ` · ${nbCibleSansVol} cible sans volume` : "") }
    : nbCibleSansVol
      ? { v: "—", u: "", sub: `cible posée sur ${nbCibleSansVol} ligne${nbCibleSansVol > 1 ? "s" : ""} — volume annuel à saisir` }
      : { v: "—", u: "", sub: "aucune cible CPP posée" };

  /* 3. Cadence : on n'a PAS de cadence mesurée par ligne — on ne l'estime
     jamais (volume ÷ heures serait une invention). Le tiret dit ce qui manque. */
  const bloc3 = { v: "—", u: "", sub: "cadence non mesurée — à relever avec Matis" };

  /* 4. Lignes en engagement : un COMPTE de chez nous, avec les noms */
  const engagees = vivantes.filter(gl => etatLigne(gl).etat !== "opportunite");
  const noms = engagees.map(gl => gl.ligne.nom);
  const bloc4 = engagees.length
    ? { v: String(engagees.length), u: `/ ${vivantes.length} lignes`,
        sub: noms.slice(0, 3).join(" · ") + (noms.length > 3 ? ` +${noms.length - 3}` : "") }
    : { v: "0", u: `/ ${vivantes.length} lignes`, sub: "aucune ligne en travail" };

  const bloc = (num, lib, b) => `
    <div class="bd-bloc" role="listitem">
      <div class="bd-lib">${num} · ${lib}</div>
      <div class="bd-v">${b.v}<small>${b.u}</small></div>
      <div class="bd-sub">${escapeAttr(b.sub)}</div>
    </div>`;
  return `<div class="bd-bandeau" aria-label="Les quatre chiffres de l'atelier">
    ${bloc("01", "Économie validée", bloc1)}
    ${bloc("02", "Ralliement cible CPP", bloc2)}
    ${bloc("03", "Cadence", bloc3)}
    ${bloc("04", "Lignes en engagement", bloc4)}
  </div>`;
}

/* ═══ v4.61.0 — Q12 (Benjamin) : la tuile regroupée des lignes HORS PÉRIMÈTRE ════
   Décision tranchée le 30/09 : une seule tuile grise pour les lignes déclarées
   sans références NI machines — « 6 lignes hors périmètre : Weisser 1–4, PCI 4–5 » —
   et un clic ouvre la liste. Le fond (Tour 19 d'Hermes) : les afficher une par une,
   au même poids visuel qu'EMAG 1, dirait qu'il y a six choses à faire — il n'y en a
   pas ; le regroupement ne cache rien, il dit la vérité en une tuile qui porte leur
   nombre. La ligne de choix explicite : déclarer leurs machines, ou les sortir du
   périmètre — jamais une invitation à la saisie impossible. */

/* les noms des lignes hors périmètre, compactés par famille :
   « WEISSER 1 » ×4 + « PCI 4 » + « PCI 5 » → « WEISSER 1–4 · PCI 4–5 » */

function accueilPiedHTML(){
  const gens = (responsables || []).filter(r => r.nom);
  const gensTxt = gens.length
    ? `<div class="pf-gens"><span class="pf-lib">L'équipe du suivi</span>${gens.map(r =>
        `<span class="pf-nom" style="--c:${escapeAttr(r.couleur || "var(--blue)")}">${escapeAttr(r.nom)}</span>`).join("")}</div>`
    : `<div class="pf-gens"><span class="pf-lib">L'équipe du suivi</span><span class="mx-zero">aucun responsable déclaré — Options → Responsables</span></div>`;
  return `<div class="pf-pied">
    ${gensTxt}
    <div class="pf-actions">
      <button class="ghost small" id="pfCarte" title="La carte atelier : chaque machine, son état, sa fiche">Bilan atelier</button>
      <button class="ghost small" id="pfExport" title="Enregistre un fichier .json à archiver ou à envoyer">Exporter</button>
      <button class="ghost small" id="pfHisto" title="Les sauvegardes automatiques précédentes">Historique</button>
      <button class="primary small" id="pfVueCpp" title="Le CPP obtenu vs la référence Matis, décomposé OP par OP, outil par outil, logement par logement">🔍 Vue CPP</button>
      <button class="primary small" id="pfSimul" title="Que vaut une baisse de prix sur les plaquettes utilisées par plusieurs productions ? Économie annuelle € et % — SIMULATION, rien n'écrit">💰 Simulateur prix</button>
      <button class="primary small" id="pfCatalogue" title="La vérité prix/article : un MABEC = un prix. Export/import CSV, propagation aux logements avec rapport">📚 Catalogue</button>
      <button class="primary small" id="pfPlan" title="Le pas-à-pas commercial : article par article, la cible SPK et le gain annuel — révélé ligne par ligne">⚔️ Plan de conversion</button>
      <button class="ghost small" id="pfAccueilMaxi" title="L'accueil en plein écran — pour projeter">⛶ Plein écran</button>
    </div>
  </div>`;
}



--- 3. LA SAISIE ATELIER (gants + tablette) ---

function atelierHTML(){
  if(!atelierCtx) return "";
  const sc = data.find(s => s.id === atelierCtx.scId);
  const essai = sc && (sc.essais||[]).find(e => e.id === atelierCtx.essaiId);
  if(!sc || !essai) return "";
  const snap = logementsSuivis(essai);
  if(!atelierCtx.logementId && snap.length) atelierCtx.logementId = snap[0].logementId;
  const lp = snap.find(x => x.logementId === atelierCtx.logementId);
  const piece = atelierProchainePiece(essai, atelierCtx.logementId);
  const st = essaiStats(sc, essai);
  const prog = st.logementProgress.find(p => p.logementId === atelierCtx.logementId);
  const pct = prog && prog.target ? Math.min(100, ((prog.lastPiece||0)/prog.target)*100) : 0;
  // v4.14 : le signal au bon moment. La barre de progression montrait la distance parcourue,
  // rien ne disait QUAND décider : à la charnière visée, on resserre le pas de mesure ou on
  // tranche (prolonger / arrêter) ; au-delà, la durée de vie dépasse l'objectif, c'est une
  // bonne nouvelle à exploiter tant que la cote tient.
  const viseeAtteinte = !!(prog && prog.target !== null && piece >= prog.target);

  // points de mesure deja utilises dans cet essai : proposes en raccourci
  const points = [...new Set((essai.prelevements||[]).map(r => (r.pointMesure||"").trim()).filter(Boolean))];
  const pmActif = atelierCtx.pointMesure || "";

  const dernieres = (essai.prelevements||[])
    .filter(r => !atelierCtx.logementId || r.logementId === atelierCtx.logementId)
    .slice(-4).reverse().map(r => {
      const c = checkConform(sc, r);
      const val = sc.emag1 ? (fmtBatt(r.battD) + " / " + fmtBatt(r.battG)) : fmtBatt(r.batt);
      return `<div class="at-recent-row"><span class="p">n°${escapeAttr(r.piece)}</span>
        <span class="pm">${escapeAttr(r.pointMesure)||""}</span>
        <span class="v">${val}</span>
        <span class="${c===false?"bad":c===true?"ok":"na"}">${c===false?"HORS TOL.":c===true?"OK":"—"}</span></div>`;
    }).join("") || `<div class="at-recent-vide">Aucune mesure pour l'instant</div>`;

  // v4.9 : champs de saisie construits depuis les critères actifs du scénario —
  // battement (respecte les côtés choisis, peut être désactivé) puis critères
  // supplémentaires (Ra, VE, libres) avec une case par axe.
  // v4.82 — les axes se CHOISISSENT au moment de la saisie (retour de Benjamin :
  // « j'ai inter et exter et droite et gauche à rentrer pour la même référence,
  // ce qui n'est pas logique »). Les pastilles (même style que les points de
  // mesure) montrent ou cache un axe POUR CET ESSAI — état de session
  // (atelierCtx.axesOn), la configuration du scénario reste intacte. Un axe
  // caché ne rend pas de champ ; le contrôle de conformité filtrait déjà les
  // côtés vides, la donnée ne change pas de forme.
  const cotesAt = battCotesDe(sc);
  const on = atelierCtx.axesOn || {};
  const chipAxes = (groupe, axes) => `<div class="at-groupe"><span class="at-groupe-label">${groupe}</span><span class="at-points-row">${axes.map(ax =>
    `<button class="at-pm ${axesActifs(axes, on[groupe]).includes(ax) ? "actif" : ""}" data-at-axe="${groupe}" data-at-axeval="${ax}">${AXE_LABELS[ax] || ax}</button>`).join("")}</span></div>`;
  const champs = [];
  if(sc.battActif !== false){
    if(cotesAt === "mono") champs.push(`<div class="at-champ"><label>${escapeAttr(libelleDe(sc))}</label><input type="number" step="0.001" inputmode="decimal" id="atV" placeholder="0,000"></div>`);
    else {
      if(cotesAt === "DG") champs.push(chipAxes("Côtés mesurés", ["D","G"]));
      const axesB = axesActifs(["D","G"], on.batt).filter(ax => cotesAt === "DG" ? true : ax === cotesAt);
      if(axesB.includes("D")) champs.push(`<div class="at-champ"><label>Droite</label><input type="number" step="0.001" inputmode="decimal" id="atD" placeholder="0,000"></div>`);
      if(axesB.includes("G")) champs.push(`<div class="at-champ"><label>Gauche</label><input type="number" step="0.001" inputmode="decimal" id="atG" placeholder="0,000"></div>`);
    }
  }
  criteresSupActifs(sc).forEach(c => {
    const axes = axesDe(c);
    if(axes.length > 1) champs.push(chipAxes(`${escapeAttr(c.label || "critère")} — axes mesurés`, axes));
    axesActifs(axes, on["cs_" + c.id]).forEach(ax => {
      const suf = ax === "v" ? "" : " " + (AXE_LABELS[ax] || ax);
      champs.push(`<div class="at-champ"><label>${escapeAttr(c.label || "critère")}${suf}</label><input type="number" step="0.001" inputmode="decimal" id="atCs_${c.id}_${ax}" placeholder="0,000"></div>`);
    });
  });
  const champUsure = `<div class="at-champ"><label>Usure plaquette</label>
    <select id="atUsure"><option value="">—</option><option value="ok">OK</option><option value="limite">Usure limite</option><option value="changer">À changer</option></select>
  </div>`;

  return `
    <div class="at-head">
      <div>
        <div class="at-titre">${escapeAttr(essai.titre)}</div>
        <div class="at-sous">${escapeAttr(sc.name)} — tolérance ${fmt(parseFloat(limiteDe(sc)),3)}</div>
      </div>
      <button class="ghost at-close" id="atelierClose">Fermer</button>
    </div>

    ${snap.length > 1 ? `<div class="at-logements">${snap.map(l => {
      const nom = nomLogementActuel(sc, l); // v4.22 : nom actuel du scenario
      return `<button class="at-log ${l.logementId===atelierCtx.logementId?"actif":""}" data-at-log="${l.logementId}">
        ${escapeAttr(nom.outilNumero||"?")}<span>${escapeAttr(nom.logementNom||"—")}</span>
      </button>`; }).join("")}</div>` : ""}

    <div class="at-piece">
      <label>N° pièce</label>
      <div class="at-piece-row">
        <button class="at-step" data-at-piece="-">−</button>
        <input type="number" inputmode="numeric" id="atPiece" value="${piece}">
        <button class="at-step" data-at-piece="+">+</button>
      </div>
      ${prog && prog.target ? `<div class="at-prog"><div class="at-prog-bar"><i style="width:${pct}%"></i></div>
        <span>${prog.lastPiece ?? 0} / ${prog.target} p — ${escapeAttr(prog.logementNom||"")}</span></div>` : ""}
      ${viseeAtteinte ? `<div class="at-charniere${piece > prog.target ? " depassee" : ""}">${piece > prog.target
        ? `◎ Au-delà de la charnière visée (${prog.target} p) — la durée de vie dépasse l'objectif : prolongez tant que la cote tient, ou clôturez l'essai.`
        : `◎ Cette pièce atteint la charnière visée (${prog.target} p) — resserrez le pas de mesure vers la fin, ou décidez : prolonger / arrêter.`}</div>` : ""}
    </div>

    ${points.length ? `<div class="at-points">
      <label>Point de mesure</label>
      <div class="at-points-row">
        ${points.map(p => `<button class="at-pm ${p===pmActif?"actif":""}" data-at-pm="${escapeAttr(p)}">${escapeAttr(p)}</button>`).join("")}
        <button class="at-pm ${pmActif===""?"actif":""}" data-at-pm="">—</button>
      </div>
    </div>` : ""}

    <div class="at-champs">${champs.join("")}${champUsure}</div>

    <button class="primary at-valider" id="atelierValider">Enregistrer et pièce suivante</button>

    <div class="at-recent">
      <div class="at-recent-t">Dernières mesures</div>
      ${dernieres}
    </div>
  `;
}


--- 4. LE PLAN DE CONVERSION (vitrine commerciale) ---

function planHTML(){
  const lignes = planLignes();
  if(!lignes.length) return `<p class="panel-hint">Aucun article de production chiffré : le plan se nourrit des mêmes données que le simulateur (scénarios en production, prix + volume).</p>`;
  const total = lignes.reduce((a, l) => a + (l.actif && l.gain ? l.gain : 0), 0);
  const actives = lignes.filter(l => l.actif).length;
  const modeReel = planSource === "reel";
  const etatConso = !modeReel
    ? "théorique — production ÷ (arêtes × DDV classeur)"
    : (consoReelle
        ? "réelle extrapolée — lue le " + consoReelle.lueLe + " (" + consoReelle.fichiers.join(", ") + ")"
        : "réelle — mais aucun classeur lu : lis un fichier ci-dessous");
  return `
    <div class="simul-note">Le pas-à-pas commercial : chaque ligne est un article actuel, sa consommation en production, et la cible SPK — révélée quand TU décides de poser son état. Le total ne compte que les lignes étatées.</div>
    <div class="simul-controles" style="flex-wrap:wrap;">
      <span style="font-weight:600;">Consommation :</span>
      <label style="cursor:pointer;"><input type="radio" name="consoSource" value="theo" ${!modeReel ? "checked" : ""}> théorique</label>
      <label style="cursor:pointer;"><input type="radio" name="consoSource" value="reel" ${modeReel ? "checked" : ""}> réelle extrapolée</label>
      <label class="ghost small" for="consoFichier" style="cursor:pointer;">📂 Lire un classeur de consommation…</label>
      <input type="file" id="consoFichier" accept=".xlsm,.xlsx" multiple hidden>
      <span id="consoEtat" style="font-size:13px; color:#1b5ea6;">${etatConso}</span>
    </div>
    ${modeReel && consoReelle ? `<p class="panel-hint">⚠ Consommation réelle = une semaine de tes classeurs × 52 (régime supposé constant). Les articles sans consommation lue perdent leur gain — jamais complétés en silence (§3.5).</p>` : ""}
    <table class="simul-table">
      <thead><tr><th>Article actuel</th><th>Libellés ISO</th><th>Prix actuel</th><th>Consommation</th><th>Cible SPK</th><th>Prix cible</th><th>État</th><th>Gain / an</th></tr></thead>
      <tbody>
      ${lignes.map((l, i) => {
        const isoCible = l.cibleIso || l.isos[0] || "";
        return `<tr>
          <td class="mono">${escapeAttr(l.mabec)}</td>
          <td style="font-size:11.5px; color:#888;">${l.isos.map(x => escapeAttr(x)).join("<br>")}</td>
          <td class="mono">${fmt(l.prixA, 2)} €</td>
          <td class="mono">${l.sourceConso === "reelle"
            ? `${fmt(l.piecesAn, 0)} plq/an <span style="color:#1b5ea6;">(réel)</span><br><span style="color:#888;">${fmtEuroCourt(Math.round(l.piecesAn * l.prixA))} estimé/an</span>`
            : (l.sourceConso === "sans"
                ? `<span style="color:#b45309;">pas de conso réelle lue</span>`
                : `${fmtEuroCourt(Math.round(l.coutAnnuel))}/an<br><span style="color:#888;">${fmt(l.piecesAn, 0)} plq/an</span>`)}</td>
          <td><input class="cell" style="width:190px; font-size:12px;" data-plan="${l.mabec}" data-field="isoCible" value="${escapeAttr(l.cibleIso)}" placeholder="plaquette SPK${l.auto ? " (LKT640 suggérée)" : ""}"></td>
          <td><input class="cell" style="width:74px; font-family:var(--font-mono);" type="number" step="0.01" data-plan="${l.mabec}" data-field="prixCible" value="${l.ciblePrix === "" ? "" : l.ciblePrix}" placeholder="5"></td>
          <td><select class="cell small" data-plan="${l.mabec}" data-field="etat">
            <option value="">—</option>
            ${PLAN_ETATS.map(e => `<option value="${e}" ${l.etat === e ? "selected" : ""}>${e}</option>`).join("")}
          </select></td>
          <td class="mono" style="${l.gain ? "color:#1a7a3f; font-weight:600;" : "color:#888;"}">${l.gain != null ? "− " + fmtEuroCourt(Math.round(l.gain)) : "potentiel"}</td>
        </tr>`;
      }).join("")}
      </tbody>
    </table>
    <div class="simul-resultat">${actives
      ? `Promesse posée : <b>${actives} article(s)</b> en conversion — économie simulée <b>− ${fmtEuroCourt(Math.round(total))} / an</b>.`
      : `Pose un état sur une ligne (même « à proposer ») pour l’ajouter à la promesse — le pas-à-pas t’appartient.`}</div>
    <div class="simul-actions" style="margin-top:12px;">
      <button class="ghost small" id="planExporter">⤵ Exporter le plan (CSV)</button>
      <button class="ghost small" id="planMaxiBtn" title="Projection en réunion">⛶ Plein écran</button>
    </div>`;
}


function planLignes(){
  const d = plaquettesCommunes();
  const parMabec = {};
  plan.forEach(p => { parMabec[p.mabec] = p; });
  const reel = (planSource === "reel") && consoReelle && consoReelle.parArticle;
  return d.groupes.map(g => {
    const art = catalogue.find(a => a.mabec === g.mabec && a.prix !== "" && a.prix > 0);
    const prixA = art ? art.prix : (g.usages[0] ? g.usages[0].prix : 0);
    const piecesAnTheo = prixA > 0 ? g.coutAnnuel / prixA : 0;
    /* v4.88 — le basculeur : en mode REEL, la consommation vient des feuilles
       Pareto conso des classeurs (qty semaine x 52). Un article sans donnee
       reelle n'est pas complete en silence : il perd son gain (null). */
    const conso = reel ? consoReelle.parArticle[g.mabec] : null;
    const sourceConso = reel ? (conso ? "reelle" : "sans") : "theo";
    const piecesAn = reel ? (conso ? conso.qtySemaine * 52 : 0) : piecesAnTheo;
    const isoKY = g.usages.map(u => u.iso).find(i => /KY3500/i.test(i || ""));
    const sugg = isoKY ? { iso: String(isoKY).replace(/KY3500/gi, "LKT640"), prix: 5 } : null;
    const p = parMabec[g.mabec] || {};
    const ciblePrix = (p.prixCible !== "" && p.prixCible != null) ? Number(p.prixCible)
                      : (sugg ? sugg.prix : "");
    const cibleIso = p.isoCible || (sugg ? sugg.iso : "");
    const actif = !!p.etat;
    const gain = (actif && ciblePrix !== "" && ciblePrix !== null && prixA > 0 && sourceConso !== "sans")
      ? piecesAn * (prixA - Number(ciblePrix)) : null;
    return { mabec: g.mabec, isos: [...g.isos], prixA, coutAnnuel: g.coutAnnuel,
             piecesAn, piecesAnTheo, sourceConso, cibleIso, ciblePrix, etat: p.etat || "", actif, gain, auto: !!sugg };
  });
}



--- 5. LE SIMULATEUR ---

function simulHTML(){
  const d = plaquettesCommunes();
  if(!d.groupes.length) return `<p class="panel-hint">Aucun logement de production avec prix, arêtes et durée de vie chiffrés. Le simulateur se nourrit des scénarios en production (★) des références à volume annuel.</p>`;
  return `
    <div class="simul-actions">
      <button class="ghost small" id="simulExporterBtn" title="Télécharge les deux tableaux en CSV — s'ouvre dans Excel">⤵ Exporter Excel (CSV)</button>
      <button class="ghost small" id="simulMaxiBtn" title="Projection en réunion">⛶ Plein écran</button>
    </div>
    <div class="simul-note">SIMULATION — rien n'écrit dans le suivi. Source : les scénarios en production (★), axe outillage seul, prix ÷ (arêtes × durée de vie) × volume annuel.</div>
    <div class="simul-controles">
      <label>Baisse de prix générale <input type="number" id="simulTaux" min="0" max="90" step="0.5" value="10"> %</label>
      <span>sur les articles cochés</span>
    </div>
    <table class="simul-table">
      <thead><tr><th></th><th>Article (MABEC)</th><th>Usages</th><th>Prix constatés</th><th>Coût / an</th><th>Économie / an</th></tr></thead>
      <tbody>
      ${d.groupes.map(g => {
        const prixMin = Math.min(...g.usages.map(u => u.prix)), prixMax = Math.max(...g.usages.map(u => u.prix));
        const ec = g.coutAnnuel * (parseFloat(document.getElementById("simulTaux")?.value) || 0) / 100;
        return `<tr>
          <td><input type="checkbox" class="simul-inc" data-mabec="${escapeAttr(g.mabec)}" checked></td>
          <td class="mono">${escapeAttr(g.mabec)}${g.isos.size ? `<br><span style="font-size:11.5px; color:#888;">${[...g.isos].map(x => escapeAttr(x)).join("<br>")}</span>` : ""}</td>
          <td>${g.usages.length} · ${escapeAttr([...new Set(g.usages.map(u => u.ligne))].join(", "))}</td>
          <td class="mono">${fmt(prixMin, 2)}${prixMin !== prixMax ? " – " + fmt(prixMax, 2) : ""} €</td>
          <td class="mono">${fmtEuroCourt(Math.round(g.coutAnnuel))}</td>
          <td class="mono simul-ec" data-cout="${g.coutAnnuel}">—</td>
        </tr>`;
      }).join("")}
      </tbody>
      <tfoot><tr><td colspan="4">Total outillage annuel en production</td><td class="mono">${fmtEuroCourt(Math.round(d.totalAnnuel))}</td><td class="mono" id="simulTotal">—</td></tr></tfoot>
    </table>
    ${d.refsWithoutVolumeNote || ""}
    ${d.parReference.length ? `
    <h4 style="margin:22px 0 8px; font-size:14px;">Budget outillage annuel par référence</h4>
    <table class="simul-table">
      <thead><tr><th>Ligne</th><th>Référence</th><th>Volume annuel</th><th>Coût / an</th><th>% du budget</th></tr></thead>
      <tbody>${d.parReference.map(x => `<tr>
        <td>${escapeAttr(x.ligne)}</td>
        <td>${escapeAttr(x.ref)}</td>
        <td class="mono">${fmt(x.prod, 0)}</td>
        <td class="mono">${fmtEuroCourt(Math.round(x.coutAnnuel))}</td>
        <td class="mono">${d.totalAnnuel ? fmt(x.coutAnnuel / d.totalAnnuel * 100, 1) : "—"} %</td>
      </tr>`).join("")}</tbody>
    </table>` : ""}
    ${d.refsSansVolume ? `<p class="panel-hint">⚠ ${d.refsSansVolume} référence(s) sans volume annuel — hors calcul : ${d.sansVolume.map(x => escapeAttr(x)).join(" · ")}</p>` : ""}
    <div class="simul-resultat" id="simulResultat"></div>`;
}



--- 6. LE CATALOGUE ---

function catalogueRendu(){
  if(!catalogue.length) return `<p class="panel-hint">Le catalogue est vide. Trois façons de le remplir : le <b>générer depuis l'outil</b> (un MABEC = un prix, le plus fréquent, divergences signalées), l'<b>importer d'un CSV</b> édité dans Excel, ou les deux — générer, exporter, faire corriger par Matis, réimporter.</p>
    <div class="simul-actions">
      <button class="ghost small" id="catSeed">🌱 Générer depuis l'outil</button>
      <label class="ghost small" for="catFichier" style="cursor:pointer;">⤴ Importer un CSV…</label>
      <input type="file" id="catFichier" accept=".csv,.txt" hidden>
    </div>`;
  return `
    <div class="simul-actions">
      <button class="primary small" id="catAppliquer" title="Propage les prix du catalogue dans tous les logements correspondants — avec rapport">✅ Appliquer les prix aux logements</button>
      <button class="ghost small" id="catExporter">⤵ Exporter le CSV</button>
      <label class="ghost small" for="catFichier" style="cursor:pointer;">⤴ Importer un CSV…</label>
      <input type="file" id="catFichier" accept=".csv,.txt" hidden>
      <button class="ghost small" id="catSeed">🌱 Regénérer depuis l'outil</button>
    </div>
    <p class="panel-hint">${catalogue.length} article(s). Un MABEC = un prix — la propagation remplace les prix des logements correspondants, avec rapport. <b>SIMULATION jusqu'à « Appliquer ».</b></p>
    <table class="simul-table">
      <thead><tr><th>Article (MABEC)</th><th>Libellés ISO vus</th><th>Prix</th></tr></thead>
      <tbody>${catalogue.map(a => `<tr>
        <td class="mono">${escapeAttr(a.mabec)}</td>
        <td style="font-size:12px; color:#888;">${escapeAttr(a.iso || "—")}</td>
        <td class="mono">${a.prix !== "" ? fmt(a.prix, 2) + " €" : "—"}${a.divergent ? ' <span style="color:#b45309;">(prix divergents dans l\'outil — Matis vérifie)</span>' : ""}</td>
      </tr>`).join("")}</tbody>
    </table>`;
}



--- 7. L'ECRITURE DES CHAMPS (le chemin de la saisie) ---

function writeFieldValue(el){
  const id = el.getAttribute("data-id");
  if(el.getAttribute("data-csup")) return ecrireCsup(el);
  const field = el.getAttribute("data-field");
  const outilId = el.getAttribute("data-outil");
  const logementId = el.getAttribute("data-logement");
  const essaiId = el.getAttribute("data-essai");
  const prelId = el.getAttribute("data-prel");
  const scrapId = el.getAttribute("data-scrap");
  const pieceId = el.getAttribute("data-piece");
  const sc = data.find(s => s.id === id);
  if(!sc) return null;
  const val = el.type === "number" ? (el.value === "" ? "" : parseFloat(el.value)) : el.value;
  if(pieceId){
    const o = sc.outils.find(x => x.id === outilId);
    const p = o && (o.pieces||[]).find(x => x.id === pieceId);
    if(p) p[field] = val;
  } else if(scrapId){
    const row = (sc.scrapLog||[]).find(r => r.id === scrapId);
    if(row) row[field] = val;
  } else if(prelId){
    const es = sc.essais.find(e => e.id === essaiId);
    const row = es && es.prelevements.find(r => r.id === prelId);
    if(row){ row[field] = val; toucherEssai(es); }
  } else if(essaiId){
    const es = sc.essais.find(e => e.id === essaiId);
    if(es){ es[field] = val; toucherEssai(es); }
  } else if(outilId && logementId){
    const o = sc.outils.find(x => x.id === outilId);
    const l = o && o.logements.find(x => x.id === logementId);
    if(l){
      l[field] = val;
      /* v4.89 — LA SUGGESTION : MABEC ou ISO saisi → le catalogue remplit le
         prix (toujours), l'ISO, les arêtes et la DDV (si vides). Ce qui est
         saisi à la main n'est jamais écrasé. */
      const ent = (field === "codeArticle") ? catalogueSuggestion(String(val || "")) : null;
      const entIso = (field === "ref") ? catalogueParIso(String(val || "")) : null;
      const cible = ent || entIso;
      if(cible) appliquerSuggestionCatalogue(l, cible);
    }
  } else if(outilId){
    const o = sc.outils.find(x => x.id === outilId);
    if(o) o[field] = val;
  } else {
    sc[field] = val;
  }
  /* v4.66.0 — le garde-fou porte-outil/logement, AU MOMENT OÙ ON ÉCRIT.
     On n'empêche rien : la valeur est écrite telle quelle (l'utilisateur a
     toujours le droit de garder deux outils distincts). On propose ensuite,
     en une phrase, ce que son vocabulaire suggère. */
  let fusion = null;
  if(outilId && !logementId && field === "numero"){
    fusion = proposerFusionLogement(val, sc.outils, outilId);
  }
  return { sc, outilId, logementId, field, fusion };
}

/* au blur (ou Entree/Tab qui en decoule) : on ecrit la valeur finale, on recalcule ce qui
   en depend, on sauvegarde et on reconstruit l'affichage complet (badges, couts, graphique). */

/* ---- v4.17 — ne jamais reconstruire l'ecran AU MILIEU d'un clic ----
   Le blur qui declenche `change` se produit pendant le MOUSEDOWN du clic suivant (l'action
   par defaut du mousedown est de deplacer le focus). Un render() immediat remplace alors le
   noeud sous le pointeur entre mousedown et mouseup : le click final part sur l'ancetre
   commun au lieu du bouton, et le clic est avele. Symptome exact du « Joindre le plan de
   l'outil » qui n'ouvrait le sélecteur de fichier qu'au DEUXIEME clic des que l'on venait
   de saisir un champ. On retarde donc le render a la fin du clic en cours — sans le
   retarder du tout quand le change arrive hors clic (Tab, Entree), ou le comportement
   reste immediat comme avant. */
let clicSourisEnCours = false;
/* [...extrait coupe a 70 lignes] */


--- 8. HISTORIQUE RECENT (CHANGELOG, 3 dernieres versions) ---

# Changelog — Suivi_optimisation_SPK

Toutes les évolutions notables de l'outil, datées, avec le numéro de version affiché en bas de
page dans l'outil (`Suivi_optimisation_SPK vX.Y.Z`).

Format des versions : `MAJEUR.MINEUR.CORRECTIF` (voir explication du vocabulaire donné à part).

## [4.89.0] — 2026-10-14 · Tour 72

**L'autocomplete du catalogue à la saisie — le dernier morceau du socle
commercial.** Taper un MABEC ou un ISO dans un logement propose les articles
du catalogue et remplit d'un clic.

### Ajouté
- **datalists natifs** (`catMabec`, `catIso`) : zéro framework, la règle
  maison ; alimentés depuis le catalogue au démarrage, à l'ouverture du
  panneau 📚 et après chaque changement du catalogue ;
- **`appliquerSuggestionCatalogue()`** (pure) : un MABEC tapé (même en
  minuscule) remplit **codeArticle et prix TOUJOURS** (un MABEC = un prix —
  décision Benjamin), l'**ISO, les arêtes et la DDV seulement si vides** —
  ce qui est saisi à la main n'est jamais écrasé ;
- **`catalogueParIso()`** : recherche par désignation ISO, insensible à la
  casse et aux espaces, multi-ISO gérée (le séparateur « | » du seed) ;
- 5 tests.

### Le contre-regard qui a renforcé le test
La porte initiale comparait un logement DÉJÀ aux valeurs du catalogue —
aveugle par construction. Renforcée : un ISO saisi à la main DIFFÉRENT doit
rester intact. Faute injectée (garde « si vide » sautée) → **vue** (l'ISO
manuel écrasé) → restaurée par copie, empreinte identique. 521 → **551/551
verts** depuis la 4.86.

## [4.88.0] — 2026-10-14 · Tour 71

**Le basculeur de consommation — theorique vs REELLE.** Benjamin, en voyant
les quantites du Plan : « j'ai de tres gros doutes sur tes quantites de
plaquettes annuelles ». Il a raison : elles sont theoriques (production /
(aretes x DDV classeur)), et l'historique de ses propres classeurs dit un
reel ~7,5 fois plus gros (867 000 EUR/an contre 115 469). Le Plan peut
desormais basculer sur la consommation REELLE.

### Ajoute
- **basculeur dans le Plan de conversion** : « theorie » ou « REELLE
  extrapolée » — la reelle lit les feuilles « Pareto conso » de SES classeurs
  (lecture locale, constitution 4.2), une semaine de consommation reelle par
  article, x 52 ;
- **consoDepuisFeuille()** (pure) : parse les sections EMAG n / PCI n /
  HESSAPP, cumule un article vu sur plusieurs lignes, **refuse un pareto de
  COUT** (jamais pris pour des quantites) et cherche la ligne d'en-tetes ;
- **honnetete integree** : en mode reel, un article SANS consommation lue
  PERD son gain (affiche « pas de conso reelle lue ») — jamais complete en
  silence (§3.5) ; l'avertissement « une semaine x 52, regime suppose
  constant » est affiche ; l'export CSV porte le mode utilise ;
- **consoReelle est un etat de session** (comme la lecture Classeur Matis) :
  jamais ecrit dans le suivi, a relire par session ;
- 5 tests : parseur (sections, cumul multi-lignes), refus du pareto cout,
  gain reel = semaine x 52 x ecart de prix, article sans donnee = gain null,
  retour au theorique exact.

### Verifie
- 542 -> **547 tests** ; contre-regard a venir au prochain tour (la porte
  « le reel retombe sur le theorique » est deja couverte par le test de
  bascule retour) ;
- ecart declare : verrou pris retroactivement (apres l'ecriture), comme le
  tour 70 — la regle des patchs-fichiers est tenue, celle du verrou non.

## [4.87.0] — 2026-10-14 · Tour 70

**Plein écran partout où ça compte.** Retour de Benjamin : « l'affichage de
l'accueil et du plan de conversion sont vraiment trop petits et illisibles ».

### Ajouté
- **plein écran GÉNÉRIQUE** : la règle CSS passe de `#simulPanel` à **tout
  `.panel`** — l'accueil, le Plan de conversion et le Simulateur passent en
  vraie pleine surface (plus de colonne de 1120 px), le mode natif est tenté
  par-dessus (projection) ;
- **polices majorées en mode maxi** : table 16,5 px, titres 22 px, champs 14 px
  — la lecture à distance de réunion ;
- **basculerMaxi()** générique : un bouton ⛶ sur l'accueil (pied) et sur le
  Plan ; le Simulateur délègue au même mécanisme ; Échap rend la main ;
- porte hors-suite étendue : **6 règles** lues dans le fichier réel.

## [4.87.0] — 2026-10-14 · Tour 70

**Plein écran partout où ça compte.** Retour de Benjamin : « l'affichage de
l'accueil et du plan de conversion sont vraiment trop petits et illisibles ».

### Ajouté
- **plein écran GÉNÉRIQUE** : la règle CSS passe de `#simulPanel` à **tout
  `.panel`** — l'accueil, le Plan de conversion et le Simulateur passent en

--- 9. JOURNAL (2 derniers tours) ---

# ECHANGES — le journal commun Hermes ↔ Z Code

> **Ce fichier remplace le transport par Benjamin.** Chacun lit le dernier tour,
> écrit le sien en haut, et commite. Un tour = un commit. Plus de copier-coller.
>
> **Règles** (constitution v1.1, réserve R3 — désormais appliquée) :
> 1. **un seul auteur sur `bilan_economique.html` à la fois** — voir `VERROU.md` ;
> 2. **un tour = un commit**, daté, signé ;
> 3. on **propose, on ne tranche pas** : ce qui revient à Benjamin est écrit dans
>    « Décisions en attente », jamais décidé en silence ;
> 4. on lit le **verrou** avant d'écrire une ligne de code, et on le libère en
>    fin de tour.
>
> **Ordre de lecture** : `VERROU.md` → dernier tour ci-dessous → constitution →
> CHANGELOG.

---

## Décisions en attente de Benjamin

| # | Question | Proposée par | Statut |
|---|---|---|---|
| Q1 | Z Code peut-il écrire et commiter directement dans ce dépôt ? (voir question ci-dessous) | Hermes | ✅ tranché — oui (Tour 2, 30/09) |
| Q2 | Décision 2 version : la production réelle devient-elle une entité ? On a la première mesure (écart +57 %) mais **un seul point de mesure** — il faut 2-3 mois de classeur pour trancher | Hermes | ✅ tranché (30/09, Benjamin) — reste un **constat lu à la demande** (écran Réel / Théorique), pas une entité ; les relevés continuent d'accumuler la mesure |
| Q3 | Le projet « Coût et qualité EMAG 1 » : peut-il accueillir une 2ᵉ ligne, ou reste-t-il mono-ligne ? | Benjamin | ✅ tranché — mono-ligne, blocage (4.55.1) |
| Q4 | Le MABEC devient-il un champ sur le logement ? (nécessaire au rapprochement classeur Matis → outil) | Hermes | ✅ tranché (30/09, Benjamin) — **oui**, champ sur le logement. ⚠️ précision de Benjamin : un même MABEC se retrouve sur **plusieurs outils, OP ou lignes** — c'est normal (même plaquette réutilisée). **Le MABEC n'est PAS une clé unique** ; le rapprochement par article se fait par MABEC + contexte (outil/OP), jamais par MABEC seul |
| Q5 | L'OP30 (perçage) : comptée **et** pilotée, partout où elle existe. Aucune exception à maintenir dans le code. | Benjamin | ✅ tranché (30/09) |
| Q6 | L'écran d'accueil, tuile-ligne : le « Coût €/pce » de la maquette — **retiré de la tuile** (il vit déjà dans le bandeau et le panneau de clic), ou **gardé étiqueté** par référence dominante (« 356x26 : 0,63 €/pce ») ? Un coût multi-réfs sans étiquette serait un chiffre mensonger (§3.5) | Z Code (mesure, Tour 6) | ✅ tranché (30/09, Benjamin) — **option B : cinq infos, coût étiqueté par référence dominante** |
| Q7 | Si le coût est gardé : **étendre `pieceCPPComplet` aux (réf, ligne) explicites** (comportement sans argument inchangé) plutôt que re-dériver la formule — c'est la voie D3 ; la barre « vers la cible » suivrait la même référence dominante | Z Code (mesure, Tour 6) | ✅ tranché (30/09, Benjamin) — suit Q6-B : extension de `pieceCPPComplet`, voie D3 |
| Q9 | ~~glossaire~~ → **tranché (Benjamin) : PAS de glossaire. Le vocabulaire va dans le topo à Matis, une section. Z Code s'en passe.** | ✅ |
| Q10 | ~~tuile sans volume~~ → **tranché (Benjamin) : la tuile affiche « — » et « volume annuel à saisir ». Ni coût pièce, ni référence dominante, tant que le volume manque. Jamais « la première référence »** | ✅ |
| Q8 | Qu'est-ce qui déclenche un déploiement prod : une phrase de Benjamin dans une session (statut actuel), ou une décision écrite au tableau AVANT l'acte ? (posé par Hermes, Tour 8 — « une décision d'usage mérite la même trace qu'une décision technique ») | Hermes | ✅ tranché (30/09, Benjamin) — **option A** : la phrase de Benjamin dans la session reste le déclencheur ; la trace est portée par la rubrique « Faits extérieurs » (l'acte écrit au moment de l'acte, avec sa vérification). La cérémonie d'une décision écrite préalable (B) ne se justifie que si quelqu'un d'autre que Benjamin peut déployer — ce n'est pas le cas |
| Q11 | Le réglage « écran d'ouverture » (Options, défaut inchangé) : **classée derrière le remplissage Matis** | ✅ tranchée (30/09, Benjamin) — « j'aimerais que l'outil ouvre sur une page overview » : l'accueil EST l'ouverture (4.62.0), **pas de réglage** — la décision différée depuis 4.51.2 est prise, directement par Benjamin | Benjamin |
| Q15 | ~~l'accueil~~ → **tranché (Benjamin) : on adopte la STRUCTURE de la capture (bandeau de 4 chiffres alignés, tuiles de ligne enrichies, matrice des opérations, pied avec les personnes et 3 actions) — avec nos vraies données. Les photos : on les demande à Matis et on attend.** | ✅ | 
| Q14 | ~~l'écran de saisie~~ → **tranché (Benjamin) : sur l'écran de saisie, 3 blocs sur 4 : (a) barre de contexte 4 etapes, (b) conditions de coupe en cartes par poste, (c) historique des essais en tableau. La métrologie en cartes reste à trancher. VOCABULAIRE : la constitution dit « DTV, Ra, voile » — Benjamin : « battement, Ra, épaisseur piste » + ajouter convexité, face, appui** | ✅ | 
| Q13 | ~~la taille des chiffres sur tuile~~ → **tranché (Benjamin) : on garde les DEUX chiffres par tuile (règle §3.4), mais on les grossit — gain acté 28-32 pt, en cours 20-22 pt. C'est C4′.** | ✅ | 
| Q13 | Les sélecteurs de la barre de l'accueil (spec C5 §1.2) : le champ « campagne / période » n'existe pas dans le modèle. Options : (a) le champ disparaît, (b) remplacé par un filtre existant (projet ou statut). La spec §4 renvoie la décision à Benjamin — construire les sélecteurs sans elle eût été une porte morte | Z Code (4.65.0) | ⏳ à trancher |
| Q12 | ~~lignes hors périmètre~~ → **tranché (Benjamin) : UNE tuile regroupée grise, « 6 lignes hors périmètre : Weisser 1-4, PCI 4-5 », un clic ouvre la liste. La vérité visible en une tuile.** | ✅ |

---

## Faits extérieurs — les actes, écrits au moment de l'acte

> Rubrique proposée par Hermes (Tour 8) et installée par Z Code (Tour 9) : un
> déploiement concerne Matis, pas seulement la conversation. **Celui qui fait
> l'acte écrit la ligne** — modèle ou Benjamin. Vérification : `curl -s URL |
> grep TOOL_VERSION`.

| Date | Acte | Où | Vérifié |
|---|---|---|---|
| 12/10 ~20:15 | **Fichier d'état fusionné préparé pour Benjamin (aucun déploiement)** — `ETAT_FUSION_PROPRE_2026-10-12.json` au racine du repo. Contexte : Benjamin voit Matis le 13/10 ; ses deux origines (prod 18:56, projet 18:41) contiennent les **4 mêmes essais** (e1, eskw8m14tcw, e2f86m77put4, ekl4bllbc97), zéro exclusif de part et d'autre — la lignée prod est la meilleure (réparations d'octobre appliquées, sans les copies contaminées EMAG 3/OP30 encore présentes dans l'état projet, où la panne signalée par Benjamin vit en clair). Fusion : base = IMPORT_MATIS.json (outils propres, MABEC sur codeArticle — 185 logements corrigés, name/opCode posés — 44+44) ; greffe = tout ce qui vient de l'atelier dans l'état prod (7 entrées d'essai dans leurs scénarios historiques avec plans, projet « Cout et qualité Emag 1 », responsable Matis, 14 configs OP réelles, saisie atelier productionAnnuelle/cibleCPP qui PRIME — 7 divergences avec le classeur listées pour l'audit, aucune tranchée). La couche générée sale (sc-x « Prod actuelle (base excel) » aux logements « Plaquette ») est remplacée par la couche générée propre, sauf DP 290x12 sans contrepartie (gardée telle quelle, signalée). | local uniquement | ✅ harnais : 500 tests \| 0 échec + smoke par `normalizeLigne` (la vraie fonction) : 10 lignes acceptées, T517 EMAG1/356x26/OP10 baseline « Classeur Matis 6781.0 » = D2 IM02 209 560 38 €/4ar + D1 IM02 198 054 38 €/8ar, 47 OP à exactement 1 baseline, 7 entrées d'essai / 4 ids, 0 scénario sans nom. **L'import chez Benjamin reste son geste** (« Remplacer tout »), ses deux exports restent le filet (Z Code) |
| 14/10 ~soir | **PROD 4.88.0** — le basculeur de consommation en prod, ordre de Benjamin : « passe le 4.88 en prod ». Les gains du Plan de conversion peuvent désormais se calculer sur la consommation réelle extrapolée des classeurs (une semaine × 52) — le fondement de la démonstration commerciale. | suivi-optimisation-septfons.surge.sh | ✅ 547 tests \| 0 échecs relancés avant l’acte ; curl HTTP 200, **1 496 294 o**, 'TOOL_VERSION = "4.88.0"', SW 200 ; empreinte **identique octet pour octet** au local ; Projet re-déployé 4.88.0 (il avait été OUBLIÉ au tour 71 — omission vue et corrigée au même moment) (Z Code, Tour 71 bis) |
| 14/10 ~midi | **PROD 4.87.0** — plein écran générique (accueil + plan + simulateur) et polices majorées, ordre de Benjamin : « passe en prod ». Benjamin exprime en même temps de **gros doutes sur les quantités de plaquettes annuelles** du Plan — doute fondé (les quantités sont théoriques : production ÷ (arêtes × DDV classeur), et l'historique réel des classeurs dit ~7,5× plus) ; le passage sur consommation réelle est proposé, en attente du feu vert. | suivi-optimisation-septfons.surge.sh | ✅ 542 tests \| 0 échecs relancés avant l'acte ; curl HTTP 200, **1 466 173 o**, `TOOL_VERSION = "4.87.0"`, SW 200 ; empreinte **identique octet pour octet** au local (`d950e649…`) ; Projet re-vérifié 4.87.0 inchangé (Z Code, Tour 70) |
| 13/10 ~nuit | **PROD 4.83.1** — le simulateur parle le métier (libellés ISO + budget annuel par référence), ordre de Benjamin : « deploie bro ». | suivi-optimisation-septfons.surge.sh | ✅ 518 tests \| 0 échecs relancés avant l'acte ; curl HTTP 200, **1 449 034 o**, `TOOL_VERSION = "4.83.1"`, SW 200 ; empreinte **identique octet pour octet** au local (`d90a2d4a…`) ; Projet re-vérifié 4.83.1 inchangé (Z Code, Tour 66 bis) |
| 13/10 ~soir | **PROD 4.83.0** — réattribution d'essai + simulateur prix plaquettes en prod, ordre de Benjamin : « deploie en prod ». La prod saute 4.81.2 → 4.83.0 : le bouton ⇄ Réattribuer, les pastilles d'axes de saisie (4.82.0), les dates bornées, le bandeau muet sur état propre, le 💰 Simulateur prix. | suivi-optimisation-septfons.surge.sh | ✅ 515 tests \| 0 échecs relancés avant l'acte ; curl HTTP 200, **1 445 828 o**, `TOOL_VERSION = "4.83.0"`, SW 200 ; empreinte **identique octet pour octet** au local (`4e2362e6…`) ; Projet re-vérifié 4.83.0 inchangé (Z Code, Tour 66) |
| 13/10 ~15:00 | **PROD 4.81.2** — le bandeau apprend le modèle v3, ordre explicite de Benjamin : « déploie la 4.81.2 en prod » (demandé depuis la session Matis — la PWA de Matis vit sur l'origine prod). | suivi-optimisation-septfons.surge.sh | ✅ 499 tests \| 0 échecs relancés avant l'acte ; curl HTTP 200, **1 426 028 o**, `TOOL_VERSION = "4.81.2"`, SW 200 ; empreinte **identique octet pour octet** au local (`37e72ddb…`) ; Projet re-vérifié 4.81.2 inchangé (Z Code, Tour 64) |
| 12/10 ~22:00 | **PROD 4.81.1** — la porte de l'import en prod, ordre de Benjamin : « deploie en prod et prepare un message pour qu'hermes repasse tout ». Sans ce déploiement, l'import du fichier fusionné chez Matis (13/10) serait mort en silence comme celui de la veille. | suivi-optimisation-septfons.surge.sh | ✅ 501 tests \| 0 échecs relancés avant l'acte ; curl HTTP 200, **1 425 878 o**, `TOOL_VERSION = "4.81.1"`, SW 200 ; fichier publié **identique octet pour octet** au local (`77340221…`) ; Projet re-vérifié 4.81.1 inchangé (Z Code, Tour 62) |
| 12/10 ~soir | **PROD 4.81.0** — le patch egress passe en prod, ordre de Benjamin : « deploie 4.81 en prod ». Contexte : Benjamin voit Matis demain ; le laptop de Matis vit sur l'origine prod, et dès la restauration du quota Supabase une 4.80 encore ouverte y reprendrait le pull aveugle (~3,43 Mo/90 s) et recreuserait le quota. Avec la 4.81, la synchro de routine ne lit plus que le tampon horaire. | suivi-optimisation-septfons.surge.sh | ✅ 500 tests \| 0 échecs relancés **avant** déploiement ; curl HTTP 200, **1 404 978 o**, `TOOL_VERSION = "4.81.0"`, SW 200 ; fichier publié **identique octet pour octet** au local (`20212862…` md5 local = md5 prod) ; pas le « Success! » de surge (règle du Tour 12). Projet re-vérifié inchangé : 4.81.0 (Z Code) |
| 12/10 ~10:40 | **Projet 4.81.0** — le pull aveugle est remplacé par le tampon léger (Tour 61), ordre de Benjamin : « on attend la réinitialisation et remplace le pull aveugle ». La prod reste en 4.80.0 et ne bougera que sur sa phrase. | suivi-optimisation-projet.surge.sh | ✅ 500 tests \| 0 échecs (497 + 3 portes cloud), contre-regard protocole (règle cassée → 1 test la voit → restauration par copie, empreinte identique) **avant** déploiement ; curl HTTP 200, **1 404 978 o**, `TOOL_VERSION = "4.81.0"`, `cloudLireTampon` présente (9 occurrences), `select=modifie_le,modifie_par` en ligne, fichier publié **identique octet pour octet** au local (`c13417e9…`) ; **prod re-vérifiée : 4.80.0 inchangée** (Z Code, Tour 61) |
| 12/10 ~09:55 | **Cloud restreint : `exceed_egress_quota`** — le projet Supabase `suivi-septfons` répond **402** sur tous les endpoints (« The project owner must upgrade their plan or remove spend caps ») : le quota mensuel de bande sortante du plan gratuit est épuisé. La synchro de la prod ET du proto2 est muette jusqu'à restauration — aucune donnée perdue, la requête échoue proprement côté client. Cause quasi certaine : le pull complet de l'état (~3,43 Mo) toutes les 90 s par onglet ouvert (`bilan_economique.html:16154`) ≈ 132 Mo/h/onglet. **Fait sans ordre, réversible** : 2resume passe en v1.0.1 — la lecture « Rafraîchir » ne tire plus que le tampon horaire (`select=modifie_le,modifie_par`, sans `donnees`) ; et une tâche planifiée Windows quotidienne (`Supabase keepalive suivi-septfons`, 09:17, `outils/supabase_keepalive.cmd`) pingue l'API contre la pause-7-jours du mail de Supabase. **Revient à Benjamin** : restaurer le service dans le dashboard (attendre la réinitialisation du quota ou Pro), puis dire si le patch egress de la prod est souhaité. | cloud `cxjfyaorkkxemjnollnj` · suivi-optimisation-projet2.surge.sh | ✅ curl rest/auth : **402** avec le corps `exceed_egress_quota` ; 2resume v1.0.1 : **372 tests verts**, redéployé, empreinte distante = `3bc951680c5718fb` ; tâche planifiée : **dernier résultat 0, activée, quotidienne 09:17** ; prod `bilan_economique.html` non écrite (empreinte `6a082cda…` inchangée) (Z Code, Tour 60) |
| 05/10 ~10:45 | **2resume v1.0.0 sur projet2** — l'outil écrit de zéro (Tour 59) remplace le proto sur `suivi-optimisation-projet2.surge.sh`. Déploiement sur ordre de Benjamin dans la fenêtre (« fini ce nouvel outil jusqu'à la livraison finale », « livraison sur l'adresse projet 2 »). `.surgeignore` liste blanche stricte ; le JSON d'essai réel copié pour le test navigateur a été **supprimé avant le déploiement**. | suivi-optimisation-projet2.surge.sh | ✅ curl : HTTP 200, **287 730 o** (identique au local), `OUTIL_VERSION = "1.0.0"`, `EMPREINTE_ASSEMBLAGE = "4bb9982c60ab57f3"` ; **les 12 sources/tests/documents en 404** ; **prod re-vérifiée inchangée : `bilan_economique.html` 1 401 140 o, `TOOL_VERSION = "4.80.0"`** ; empreinte locale du fichier de prod inchangée (`6a082cda…`) ; **projet3 re-vérifié non écrit** (Z Code, Tour 59) |
| 02/10 ~21:40 | **projet3 v3.0.0** — la génération 3 créée de zéro sur carte blanche de Benjamin (« tu pars de 0 et tu crées l'outil parfait selon toi… livraison sur une adresse surge projet3 »). Nouveau dossier `projet3/`, 9 sources + assembleur + 4 suites de tests. `bilan_economique.html` et `proto/` **non écrits**, verrou non nécessaire. | suivi-optimisation-projet3.surge.sh | ✅ 347 tests \| 0 échecs (149 noyau, 76 migration sur les 4 exports réels, 122 application) **avant** déploiement ; contre-regard **5/5 pannes vues**, restauration par copie vérifiée SHA-256 ; curl `VERSION = "3.0.0"`, empreinte locale = distante (`253bf49af7ac9c82`), SW + manifest + icônes 200 ; **sources, tests, documents et tout JSON de données en 404** (liste blanche stricte) ; vérifié dans le navigateur **depuis l'URL publique** (accueil, ligne, poste prévu/obtenu, nuit, A4, import réel IMPORT_MATIS 192 logements). **Prod 4.80.0 et proto2 v2.0 re-vérifiés inchangés.** (Z Code, Tour 57) |
| 02/10 ~14:20 | **PROD 4.80.0** — « on va deployer en prod ». Saute **22 versions** (4.58.0 → 4.80.0) : c'est le plus grand écart jamais mis en prod d'un coup. Contenu inchangé depuis le déploiement projet (le même fichier, le même SHA). | suivi-optimisation-septfons.surge.sh | ✅ 497 tests \| 0 échecs, `VERDICT : tout est vert` **avant** déploiement ; curl SW 200, **1 401 140 o**, `TOOL_VERSION = "4.80.0"` ; fichier publié **identique octet pour octet** au local (`6a082cda…`) ; **18 chemins testés, seuls les 5 blancs du `.surgeignore` renvoient 200** — `CHANGELOG.md`, `ECHANGES.md`, `VERROU.md`, `build_harness.py`, `cloud_courant.json`, `proto/`, `outils/`, `.git/config` et 10 autres en **404**, et les quatre premiers vérifiés **présents en local** (le 404 est donc un vrai refus, pas un fichier fantôme). Projet 4.80.0 et proto2 v2.0 re-vérifiés inchangés. (Z Code, Tour 56) |
| 02/10 ~13:35 | **Projet 4.80.0** — retour à l'identité d'avant le Design System B : palette v3.15, fond gris, rayons 3/4 px, et surtout **trois formes** (Manrope / Roboto / IBM Plex Mono) au lieu d'une seule. Ordre de Benjamin : « on garde le design système avant le design système B, avec notre nouvelle infrastructure ». Premier tour qui écrit dans `bilan_economique.html` depuis 21 versions. | suivi-optimisation-projet.surge.sh | ✅ curl SW 200, **1 401 140 o**, `TOOL_VERSION = "4.80.0"`, `--blue:#1B5EA6`, `--bg:#e8eaed`, `--font-disp:'Manrope'`, Manrope embarquée, **0 occurrence de `--blue:#006AB3`** ; fichier publié **identique octet pour octet** au local (`6a082cda…`) ; **les 7 fichiers testés renvoient 404**, le JSON réel compris. **Prod re-vérifiée inchangée : 4.58.0.** Proto projet2 inchangé : v2.0. 497 tests + 6 contrastes + **11 portes d'identité** (Z Code, Tour 56) |
| 01/10 | Proto **v1.0** — import des exports de l'ancienne version, `.surgeignore` en place | suivi-optimisation-projet2.surge.sh | ✅ curl : SW 200, 86 635 o, `PROTO_VERSION = "1.0"`, **les 10 fichiers sources/tests/documents en 404** ; prod 4.58.0 et projet 4.79.0 re-vérifiés inchangés (Z Code) |
| 30/09 ~09:20 | Prod **4.56.0** + Projet **4.56.0** (merge `main` = `c32a0ee`), ordre de Benjamin dans la session (Tour 7) | suivi-optimisation-septfons.surge.sh · suivi-optimisation-projet.surge.sh | ✅ curl, SW 200 (Z Code, puis re-vérifié par Hermes au Tour 8) |
| 30/09 ~11:00 | Prod **4.57.0** + Projet **4.57.0** (merge `main` = `b8c7d87`), ordre de Benjamin : « une fois vérifié tu déploies » | idem | ✅ curl `TOOL_VERSION = "4.57.0"`, coquille absente (Z Code, Tour 9) |
| 30/09 ~12:30 | Prod **4.58.0** + Projet **4.58.0** (merge `main` = `935b210`, ff), ordre de Benjamin : « fonce code et déploie » (Q8-A) — MABEC raccordé au logement, rapprochement du classeur par article | idem | ✅ curl `TOOL_VERSION = "4.58.0"` sur les deux domaines, `matisRapprocheMabec` présent (Z Code, Tour 10) |
| 30/09 ~17:00 | **Projet 4.63.3** (4.63.0/1/2 = la peau DS B de Z Code, + le correctif de lisibilité d Hermes : `--label` 2,81:1 → 5,07:1, et la police morte en tête de pile retirée), feu vert de Benjamin : « déploie sur Projet maintenant » | suivi-optimisation-projet.surge.sh | ✅ curl `TOOL_VERSION = "4.63.3"`, `--label:#6E6E73` en ligne, pile système en tête, SW 200 — **pas le « Success! » de surge** (règle du Tour 12) |
| 30/09 ~22:40 | **Projet 4.66.0** — le garde-fou porte-outil/logement à la saisie + Roboto réellement embarquée, ordre de Benjamin : « deploie sur projet » | suivi-optimisation-projet.surge.sh | ✅ curl `TOOL_VERSION = "4.66.0"`, `font-family:'Roboto'` embarquée, Roboto en tête, `proposerFusionLogement` présent, SW 200 — **pas le « Success! » de surge** (règle du Tour 12). La **prod reste en 4.58.0** |
| 01/10 soir | **Projet 4.79.0** (Tour 52 : promesses UI + A4 Mission + CSS d'impression au bon endroit), déploiement Projet libre par protocole (la prod ne bouge que sur phrase de Benjamin) | suivi-optimisation-projet.surge.sh | ✅ curl `TOOL_VERSION = "4.79.0"`, `print-mission`/`PROMESSES_UI`/`missionA4HTML` présents (38 occurrences), SW 200 — pas le « Success! ». **Prod re-vérifiée inchangée : 4.58.0** (Z Code, Tour 52) |
| 01/10 nuit | **proto2 v0.1** — le proto 5 écrans déployé sur un **troisième domaine**, à la demande de Benjamin (« carte blanche, tu es le boss, fonce ») après l'analyse « et si tu reprenais de zéro ». `bilan_economique.html` **non écrit**. | suivi-optimisation-projet2.surge.sh | ✅ curl HTTP 200, 58 246 octets, `PROTO v0.1` présent ; **les 6 sources/tests/données en 404** (`coeur.js`, `donnees.js`, `test_coeur.js`, `test_proto.js`, `CAHIER.md`, `proto.html`) — le `.surgeignore` du proto est strict. Vérifié dans Chrome : 5 écrans, 4 KPI, 0 `undefined`/`NaN` **dans le rendu** (les occurrences trouvées sont les mots du code source). **Prod 4.58.0 et Projet 4.79.0 re-vérifiés inchangés** (Z Code, Tour 53) |
| 02/10 | Proto **v2.0** — l'accueil en tuiles (une par ligne de production) puis le détail de la ligne, scénario de production seul, puis les scénarios à optimiser. Production hebdomadaire **retirée du périmètre** (décision de Benjamin) et **déclarée à l'écran** plutôt que témoignée. `bilan_economique.html` **non écrit**. | suivi-optimisation-projet2.surge.sh | ✅ curl SW 200, 115 279 o, `PROTO_VERSION = "2.0"`, `EMPREINTE_ASSEMBLAGE = "a58277527ed0079c"` — **les 11 sources / tests / documents en 404**, le JSON réel aussi. Vérifié dans le navigateur sur `cloud_courant.json` : 10 lignes, 6 déclarées vides, EMAG 1 décomposée jusqu'au logement. **Prod 4.58.0 et Projet 4.79.0 inchangés** (Z Code, Tour 55) |

---


**Fait de données — 12/10 ~22:25, l'acte de Benjamin.** Premier import par bouton
réussi depuis le 29/09 : l'export post-import de l'origine prod (rev 422) porte
**exactement le fichier fusionné** — vérifié mécaniquement : 10 lignes / 13 refs /
47 OP / 47 baselines, 7 entrées d'essai / 4 ids, ids générateur (`l-EMAG1`…),
baseline « Classeur Matis 6781.0 » avec T517 D1/D2 MABEC/prix/arêtes, EMAG 3 sans
contamination (les seuls `smud*` restants sont la copie légitime EMAG 1/OP40),
HESSAPP 426 000 / 0,129 posés, DP 290x12 conservée, projet et responsable présents.
Les 59 scénarios de la fusion sont identiques un à un (id / baseline / outils /
essais). Preuve locale : `AUDIT_export_prod_apres-import_12-10_22h25_rev422.json`.
**La prod est prête pour la session Matis du 13/10** — et le rituel du premier
dépôt cloud prendra CET état-là, pas un fossile.


**Décision de Benjamin — 12/10 tard, l'arbitrage des productions.** « 426 000 sur
HESSAPP, c'est oui, et idem pour EMAG 1 : ce sont les valeurs de production
annuelles. » **Deux des sept divergences sont closes : l'atelier prime, les valeurs
déjà posées dans la prod (426 000 / 148 942) ne bougent pas.** Conséquence lue au
calcul : le classeur de Matis ne compte PAS en annuel — 8 149 × 52,3 = 426 000
exactement (une semaine, cohérent avec son titre « 14-09 au 21-09 »), mais
6 781 × 22,0 = 148 942 (ni semaine ni année : période ou lot, à faire dire par
Matis). Point d'attention ouvert pour l'audit : l'écran « Classeur Matis » affiche
des « coûts /an » calculés sur ces productions — l'étiquette est fausse si
l'entrée est hebdomadaire ; rien ne se corrige sans datage (gel actif). Les