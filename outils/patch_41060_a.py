# -*- coding: utf-8 -*-
"""Tour 88 (4.106.0) — brique D : le dossier de visite + couche codification.
Insère le bloc de fonctions (pures + rendu) avant la section Plan v4.102."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
ancre_txt = "   v4.102.0 — LE PLAN DE CONVERSION COMME TABLEAU DE BORD LIVE"
assert ancre_txt in src, "ancre v4.102 introuvable"
_i = src.index(ancre_txt)
NL = chr(10)
_j = src.rfind(NL, 0, _i)            # fin de la ligne des barres
_k = src.rfind(NL, 0, _j)            # debut de la ligne des barres
ancre = src[_k+1:_j+1]               # la ligne des barres, avec son retour a la ligne final

bloc = '''/* ════════════════════════════════════════════════════════════════════════════
   v4.106.0 — LA BRIQUE D : LE DOSSIER DE VISITE
   ---------------------------------------------------------------------------
   Benjamin (22/10, avant chaque rencontre) : retrouver d'un coup d'œil ce qui
   a été fait depuis la dernière fois, ce qui est bloqué, et ce qu'il reste à
   faire ensemble. Conception validée à trois (Z Code + Hermes + ChatGPT) :
   - la référence est `derniereVisite`, posée par Benjamin, PRÉREMPLIE à la
     dernière livraison, jamais obligatoire (Hermes Q4) ;
   - les actions anciennes toujours ouvertes restent visibles HORS fenêtre
     (ChatGPT n°3) — un sujet ouvert à la livraison 12 reste listé à la 14 ;
   - la codification, sémantique tranchée par Benjamin (23/10) : DEUX dates
     par article (demandée / accordée), l'âge de l'attente est la métrique ;
     un gain acté sous BADP n'est pas un gain à l'échelle — il est qualifié ;
   - AUCUN K, AUCUN P_req dans ce dossier (sanitiseur du pattern Mission) ;
     les gains viennent de gainPoste (source unique), jamais recalculés ici.
   ════════════════════════════════════════════════════════════════════════════ */

function dateIsoMax(a, b){
  const va = String(a || ""), vb = String(b || "");
  if(!va) return vb || null;
  if(!vb) return va || null;
  return vb > va ? vb : va;   /* ISO se compare en texte */
}
function dateIsoAujourdhui(){
  return new Date().toISOString().slice(0, 10);
}
function joursDepuis(iso){
  const d = Date.parse(String(iso || "") + "T00:00:00Z");
  if(isNaN(d)) return null;
  return Math.max(0, Math.floor((Date.now() - d) / 86400000));
}
/* L'état de codification d'un article — la source de tous les dérivés. */
function etatCodification(art){
  if(!art || (!art.codifieLe && !art.codificationDemandeeLe)) return { etat: "nonDemandee" };
  if(art.codifieLe) return { etat: "codifie", le: art.codifieLe };
  return { etat: "demandee", le: art.codificationDemandeeLe, jours: joursDepuis(art.codificationDemandeeLe) };
}
/* Les articles distincts d'un scénario (par MABEC des logements). Rend
   [{ mabec, art, horsCatalogue }] — art null si l'article n'est pas au catalogue. */
function articlesScenario(sc){
  const vus = new Set(), out = [];
  (sc.outils || []).forEach(o => (o.logements || []).forEach(l => {
    const m = String(l.codeArticle || l.mabec || "").trim().toUpperCase().replace(/\\s+/g, " ");
    if(!m || vus.has(m)) return;
    vus.add(m);
    out.push({ mabec: m, art: catalogue.find(a => a.mabec === m) || null,
               horsCatalogue: !catalogue.some(a => a.mabec === m) });
  }));
  return out;
}
/* L'état de codification DÉRIVÉ d'un scénario : un scénario n'est « codifié »
   que si TOUS ses articles le sont — l'écran dit lequel manque (décision
   Hermes Q2 : posé sur l'ARTICLE, jamais sur le scénario). La couche générée
   « base excel » (logements « Plaquette », MABEC synthétiques) est hors
   exigence, sinon l'outil exigerait de coder des articles fantômes. */
function codificationScenario(sc){
  if(/base excel/i.test(sc.name || "")) return { etat: "sansExigence" };
  const arts = articlesScenario(sc);
  if(!arts.length) return { etat: "sansArticle" };
  let tousCodifies = true, ageMax = 0, joursDemande = 0;
  const manquants = [];
  arts.forEach(a => {
    const e = etatCodification(a.art);
    if(e.etat === "codifie") return;
    tousCodifies = false;
    const label = a.mabec + (a.horsCatalogue ? " (hors catalogue)" : "");
    manquants.push(label + (e.etat === "demandee" ? " — demandée depuis " + (e.jours ?? "?") + " j" : ""));
    if(e.etat === "demandee"){ ageMax = Math.max(ageMax, e.jours || 0); joursDemande++; }
  });
  if(tousCodifies) return { etat: "codifie" };
  return { etat: joursDemande ? "attente" : "nonDemandee", jours: ageMax, manquants };
}

/* L'agrégat du dossier : LECTURE SEULE — rien n'est écrit, rien n'est recalculé
   en dehors des fonctions canoniques (planChronologieEssais pour les essais,
   planRecapGains pour les gains). reference = date ISO ou "" (tout l'historique). */
function dossierVisite(reference){
  const ref = String(reference || "");
  const chrono = planChronologieEssais();
  const dansFenetre = e => !ref || (e.date && e.date >= ref) || (e.dateFin && e.dateFin >= ref);
  const essais = chrono.filter(dansFenetre)
    .sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));
  const essaisOk = essais.filter(e => e.etat === "ok");
  /* les scénarios actuellement en série ou validés, avec leur dernier essai */
  const seriesVus = new Map();
  chrono.forEach(e => {
    if(e.statutScenario !== "serie" && e.statutScenario !== "valide") return;
    const cur = seriesVus.get(e.scenarioId);
    if(!cur){ seriesVus.set(e.scenarioId, { scenarioId: e.scenarioId, scenario: e.scenario, ligne: e.ligne, opCode: e.opCode,
      statut: e.statutScenario, dernierEssai: e.date, auteur: e.auteur }); return; }
    if(String(e.date || "") > String(cur.dernierEssai || "")) cur.dernierEssai = e.date;
  });
  /* ce qui est bloqué, état COURANT : clôturés (depuis la référence), hors
     course (motifs), abandonnés — trois listes, jamais fusionnées */
  const clotures = essais.filter(e => e.motif);
  const echecs = [], vusEchec = new Set();
  chrono.forEach(e => {
    if(!e.horsCourse || vusEchec.has(e.scenarioId)) return;
    vusEchec.add(e.scenarioId);
    echecs.push({ scenario: e.scenario, scenarioId: e.scenarioId, ligne: e.ligne, opCode: e.opCode, motif: e.motif || e.raison || "" });
  });
  const abandons = [], vusAb = new Set();
  chrono.forEach(e => {
    if(e.statutScenario !== "abandonne" || vusAb.has(e.scenarioId)) return;
    vusAb.add(e.scenarioId);
    abandons.push({ scenario: e.scenario, ligne: e.ligne, opCode: e.opCode });
  });
  /* les projets ouverts, TOUS ÂGES (les anciens sont marqués — ChatGPT n°3) */
  const projetsOuverts = (projets || [])
    .filter(pj => pj.statut === "encours" || pj.statut === "pause")
    .map(pj => ({ nom: pj.nom, statut: pj.statut, dateCible: pj.dateCible || "",
                  responsable: (pj.responsableId && (responsables.find(r => r.id === pj.responsableId) || {}).nom) || "",
                  nbScenarios: scenariosResolusDuProjet(pj).length,
                  ancien: !!(ref && pj.creeLe && String(pj.creeLe).slice(0, 10) < ref) }));
  /* la codification en attente, article par article, la plus vieille d'abord */
  const codifAttente = catalogue
    .map(a => { const e = etatCodification(a); return e.etat === "demandee"
      ? { mabec: a.mabec, le: e.le, jours: e.jours || 0 } : null; })
    .filter(Boolean).sort((a, b) => b.jours - a.jours);
  /* les gains : source unique planRecapGains, qualifiés BADP / cycle standard
     (décision Benjamin 23/10 — un gain acté sous BADP n'est pas à l'échelle) */
  const recap = planRecapGains();
  const actes = [], possibles = [];
  (recap.postes || []).forEach(p => (p.refs || []).forEach(r => {
    if(r.gain === null || r.gain === undefined || !(r.gain > 0) || !r.meilleur) return;
    const cod = codificationScenario(r.meilleur.sc);
    const base = { ligne: p.ligne, opCode: p.opCode, ref: (r.ref && r.ref.nom) || "?",
                   scenario: r.meilleur.sc.name || "Sans nom", gain: r.gain };
    if(r.serie){
      base.qualif = cod.etat === "codifie" ? "standard"
                  : (cod.etat === "attente" || cod.etat === "nonDemandee") ? "BADP" : null;
      if(base.qualif === "BADP") base.codifJours = cod.jours || 0;
      actes.push(base);
    } else {
      if(cod.etat === "attente") base.codifJours = cod.jours || 0;
      possibles.push(base);
    }
  }));
  actes.sort((a, b) => b.gain - a.gain);
  possibles.sort((a, b) => b.gain - a.gain);
  const somme = arr => arr.reduce((a, l) => a + l.gain, 0);
  return { reference: ref,
    derniereLivraison: (livraisons || []).map(l => l.date).filter(Boolean).sort().slice(-1)[0] || "",
    essais, essaisOk,
    series: [...seriesVus.values()].sort((a, b) => String(b.dernierEssai || "").localeCompare(String(a.dernierEssai || ""))),
    bloques: { clotures, echecs, abandons },
    projetsOuverts,
    codifAttente,
    gains: { actes,
      totalActeStandard: somme(actes.filter(l => l.qualif === "standard")),
      totalActeBadp: somme(actes.filter(l => l.qualif === "BADP")),
      totalActeSansInfo: somme(actes.filter(l => !l.qualif)),
      possibles, totalPossible: somme(possibles),
      nbEssais: chrono.length } };
}

/* le rendu — lisible debout devant un écran de réunion : les chiffres d'abord,
   les listes ensuite, tout étiqueté, jamais mélangé (§3.4). */
function visiteSectionTitre(t, sous){
  return `<div class="pc-titre-section">${escapeAttr(t)}${sous ? ` <span style="font-weight:400; letter-spacing:0; text-transform:none; color:var(--ink-faint);">${escapeAttr(sous)}</span>` : ""}</div>`;
}
function renderVisite(){
  const wrap = document.getElementById("visitePanel");
  if(!wrap) return;
  const d = dossierVisite(derniereVisite);
  const fr = iso => { const p = String(iso || "").split("-"); return p.length === 3 ? p[2] + "/" + p[1] + "/" + p[0] : (iso || "—"); };
  const refTxt = derniereVisite ? fr(derniereVisite) : "tout l'historique (aucune date posée)";
  let h = `<h3>🧳 Dossier de visite</h3>
    <div class="simul-controles" style="flex-wrap:wrap;">
      <span style="font-weight:600;">Depuis :</span>
      <input type="date" id="visiteDate" min="2025-01-01" max="2035-12-31" value="${escapeAttr(derniereVisite || "")}" title="Le point de référence du dossier — prérempli à la dernière livraison ; à poser au retour de chaque visite.">
      <button class="ghost small" id="visiteFaite" title="Pose la date de référence à aujourd'hui — le geste du retour de visite">✓ Visite faite (aujourd'hui)</button>
      <span style="font-size:13px; color:#1b5ea6;">référence : ${escapeAttr(refTxt)}${d.derniereLivraison ? ` · dernière livraison : ${escapeAttr(fr(d.derniereLivraison))}` : ""}</span>
    </div>`;
  /* les gains d'abord — qualifiés, jamais additionnés entre familles */
  const g = d.gains;
  const ligneGain = (l, badge) => `<tr><td class="mono">${escapeAttr(l.ligne)} · ${escapeAttr(l.opCode)}</td><td>${escapeAttr(l.ref)}</td><td><b>${escapeAttr(l.scenario)}</b></td><td>${badge || ""}</td><td class="mono" style="font-weight:600; color:var(--green);">+ ${fmtEuroCourt(Math.round(l.gain))}<small style="color:var(--ink-faint);"> /an</small></td></tr>`;
  h += visiteSectionTitre("Gains en course — " + g.nbEssais + " essai(s) dans le suivi", "actés et possibles ne se somment jamais");
  h += `<table class="simul-table"><thead><tr><th>Poste</th><th>Référence</th><th>Scénario</th><th>État</th><th>Économie</th></tr></thead><tbody>`;
  const badpBadge = l => `<span class="pc-stat attente" title="Achat ponctuel (BADP) : montants et récurrence limités — pas un gain à l'échelle tant que la codification n'est pas accordée.">via BADP${l.codifJours ? " — codification attendue " + l.codifJours + " j" : ""}</span>`;
  if(g.actes.length){
    h += `<tr class="pc-grp"><td colspan="5">Actés — en production${g.totalActeSansInfo ? ` <span style="font-weight:400; font-size:11px; color:var(--ink-faint);">(dont qualification de cycle à renseigner)</span>` : ""}</td></tr>`;
    g.actes.forEach(l => {
      const badge = l.qualif === "standard" ? `<span class="pc-stat serie" title="Articles codifiés : le cycle de commande standard peut porter ce gain.">cycle standard</span>`
                  : l.qualif === "BADP" ? badpBadge(l)
                  : `<span class="pc-stat attente" title="Renseigner la codification des articles (Catalogue) pour qualifier ce gain.">cycle non qualifié</span>`;
      h += ligneGain(l, badge);
    });
  }
  if(g.possibles.length){
    h += `<tr class="pc-grp"><td colspan="5">Possibles — validés ou essai positif, pas encore en série (cumul ${fmtEuroCourt(Math.round(g.totalPossible))} /an)</td></tr>`;
    g.possibles.forEach(l => {
      const badge = l.codifJours ? badpBadge(l) : "";
      h += ligneGain(l, badge);
    });
  }
  if(!g.actes.length && !g.possibles.length)
    h += `<tr><td colspan="5" style="color:var(--ink-soft);">Aucun scénario chiffrable en course : les lignes apparaissent dès qu'un essai chiffrable court face à sa production.</td></tr>`;
  h += `</tbody></table>`;
  h += `<div class="simul-resultat" style="margin-top:10px;">
    Actés : <b>${fmtEuroCourt(Math.round(g.totalActeStandard))}</b> /an sous cycle standard
    ${g.totalActeBadp ? ` · <b>${fmtEuroCourt(Math.round(g.totalActeBadp))}</b> /an <b>via BADP</b> (plafonné — codification en attente)` : ""}
    ${g.totalActeSansInfo ? ` · ${fmtEuroCourt(Math.round(g.totalActeSansInfo))} /an à qualifier` : ""}
    <br>Possibles (validation en attente) : <b>${fmtEuroCourt(Math.round(g.totalPossible))}</b> /an — jamais additionnés aux actés.</div>`;
  /* la codification en attente — l'argument porté à la hiérarchie */
  if(d.codifAttente.length){
    h += visiteSectionTitre("Codification en attente chez Matis", "prérequis du cycle de commande standard — sans elle, BADP seulement");
    h += `<table class="simul-table"><thead><tr><th>Article</th><th>Demandée le</th><th>Attente</th></tr></thead><tbody>`;
    d.codifAttente.forEach(c => { h += `<tr><td class="mono">${escapeAttr(c.mabec)}</td><td>${escapeAttr(fr(c.le))}</td><td class="mono" style="color:var(--amber); font-weight:600;">${c.jours} jour${c.jours > 1 ? "s" : ""}</td></tr>`; });
    h += `</tbody></table>`;
  }
  /* les essais depuis la référence */
  h += visiteSectionTitre("Essais " + (derniereVisite ? "depuis le " + refTxt : "réalisés"), d.essais.length + " essai(s)");
  if(d.essais.length){
    h += `<table class="simul-table"><thead><tr><th>Date</th><th>Essai</th><th>Poste</th><th>Auteur</th><th>Résultat</th></tr></thead><tbody>`;
    d.essais.forEach(e => {
      const cls = e.etat === "ok" ? "val" : e.etat === "bad" ? "" : "attente";
      const lab = e.etat === "ok" ? "Conforme" : e.etat === "bad" ? "Non conforme" : e.etat === "arrete" ? "Arrêté" : "En cours";
      h += `<tr><td class="mono">${escapeAttr(fr(e.date))}</td><td>${escapeAttr(e.titre)}</td><td>${escapeAttr(e.ligne)} · ${escapeAttr(e.opCode)}</td><td>${escapeAttr(e.auteur || "—")}</td><td><span class="pc-stat ${cls}">${escapeAttr(lab)}${e.raison && e.etat !== "ok" ? " — " + escapeAttr(e.raison) : ""}</span></td></tr>`;
    });
    h += `</tbody></table>`;
    if(d.essaisOk.length) h += `<p class="panel-hint">Conforme(s) : ${d.essaisOk.length} — chaque essai conforme compte pour le protocole (répété 5×, validé 5× et viable éco → production).</p>`;
  } else h += `<p class="panel-hint">Aucun essai sur la fenêtre.</p>`;
  /* scénarios en série / validés — l'état actuel, sans date prétendue */
  if(d.series.length){
    h += visiteSectionTitre("Scénarios validés ou en série", "état actuel");
    h += `<table class="simul-table"><thead><tr><th>Poste</th><th>Scénario</th><th>Statut</th><th>Dernier essai</th></tr></thead><tbody>`;
    d.series.forEach(s => { h += `<tr><td class="mono">${escapeAttr(s.ligne)} · ${escapeAttr(s.opCode)}</td><td><b>${escapeAttr(s.scenario)}</b></td><td><span class="pc-stat ${s.statut === "serie" ? "serie" : "val"}">${s.statut === "serie" ? "En série" : "Validé"}</span></td><td class="mono">${escapeAttr(fr(s.dernierEssai))}</td></tr>`; });
    h += `</tbody></table>`;
  }
  /* ce qui est bloqué */
  const b = d.bloques;
  if(b.clotures.length || b.echecs.length || b.abandons.length){
    h += visiteSectionTitre("Sujets bloqués ou arrêtés", "motifs en toutes lettres");
    h += `<table class="simul-table"><thead><tr><th>Sujet</th><th>Poste</th><th>Motif / état</th></tr></thead><tbody>`;
    b.clotures.forEach(e => { h += `<tr><td>Essai « ${escapeAttr(e.titre)} » — arrêté</td><td class="mono">${escapeAttr(e.ligne)} · ${escapeAttr(e.opCode)}</td><td>${escapeAttr(e.motifLibelle || e.motif || "")}</td></tr>`; });
    b.echecs.forEach(e => { h += `<tr><td>Scénario « ${escapeAttr(e.scenario)} » — hors course</td><td class="mono">${escapeAttr(e.ligne)} · ${escapeAttr(e.opCode)}</td><td>${escapeAttr(e.motif || "essais arrêtés")}</td></tr>`; });
    b.abandons.forEach(e => { h += `<tr><td>Scénario « ${escapeAttr(e.scenario)} » — abandonné</td><td class="mono">${escapeAttr(e.ligne)} · ${escapeAttr(e.opCode)}</td><td>abandonné</td></tr>`; });
    h += `</tbody></table>`;
  }
  /* les projets ouverts — TOUS ÂGES, les anciens marqués */
  if(d.projetsOuverts.length){
    h += visiteSectionTitre("Actions ouvertes — projets en cours ou en pause", "tous âges : un sujet ouvert reste listé jusqu'à sa clôture");
    h += `<table class="simul-table"><thead><tr><th>Projet</th><th>Responsable</th><th>Échéance</th><th>Scénarios</th><th></th></tr></thead><tbody>`;
    d.projetsOuverts.forEach(pj => { h += `<tr><td><b>${escapeAttr(pj.nom)}</b></td><td>${escapeAttr(pj.responsable || "—")}</td><td class="mono">${escapeAttr(fr(pj.dateCible))}</td><td class="mono">${pj.nbScenarios}</td><td>${pj.ancien ? `<span class="pc-stat attente" title="Ouvert avant la date de référence : toujours en attente de décision.">ouvert avant le ${escapeAttr(refTxt)}</span>` : ""}</td></tr>`; });
    h += `</tbody></table>`;
  }
  wrap.innerHTML = h;
  const dateInp = document.getElementById("visiteDate");
  if(dateInp) dateInp.addEventListener("change", () => {
    derniereVisite = dateInp.value || null;
    saveData(); renderVisite();
  });
  const faite = document.getElementById("visiteFaite");
  if(faite) faite.addEventListener("click", () => {
    dialogueConfirmer("Poser la date de référence du dossier à aujourd'hui (" + dateIsoAujourdhui().split("-").reverse().join("/") + ") ?\\n\\nLe prochain dossier couvrira tout ce qui arrive après cette visite.", { titre: "Marquer la visite faite", okLabel: "Marquer" }).then(ok => {
      if(!ok) return;
      derniereVisite = dateIsoAujourdhui();
      saveData(); renderVisite();
    });
  });
}
function ouvrirVisite(){
  fermerPanneaux();
  ouvrirPanneau("visitePanel");
  renderVisite();
}

'''
src = src.replace(ancre, bloc + ancre, 1)
io.open(p, "w", encoding="utf-8").write(src)
print("bloc D insere, taille:", len(src))
