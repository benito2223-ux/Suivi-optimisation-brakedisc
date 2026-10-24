# -*- coding: utf-8 -*-
"""Tour 90 (4.108.0) — brique C : la matrice « Où investir — les priorités ».
Deux axes jamais mélangés (ChatGPT n°2) : le POTENTIEL (€) et la FACILITÉ DE
CONCRÉTISATION (la prochaine étape + les freins). Cinq paniers — le cinquième
est celui d'Hermes : « travaillé et arrêté — motif ». Le filtre de l'univers
plaquettes (Hermes Q3) sort les articles sans lien outillage sur une ligne
explicite, jamais en silence. Source unique : planRecapGains."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
n0 = len(src)

def remplace(avant, apres, label):
    global src
    assert avant in src, "ANCRE INTROUVABLE : " + label
    src = src.replace(avant, apres, 1)
    print("ok :", label)

# ── 1. l'agrégat pur ──
remplace("function planScenariosHTML(recap){",
'''/* --- 1quinquies. v4.108 — OÙ INVESTIR (brique C) -------------------------
   Benjamin (23/10) : « repérer rapidement les applications sur lesquelles
   concentrer nos prochains efforts techniques et commerciaux ». Deux AXES
   jamais fondus en un score (ChatGPT n°2) : le POTENTIEL (dépense et gain
   €/an) et la FACILITÉ DE CONCRÉTISATION (la prochaine étape + les freins,
   dont la codification en attente — décision Benjamin du 23/10).
   Cinq paniers : validés non déployés / essai positif à compléter /
   dépense forte jamais travaillée / données insuffisantes (ce qui manque,
   nommé) / travaillé et arrêté — motif (Hermes Q3 : le cas SN60 — « qu'avez-
   vous appris, où avez-vous stoppé ? »). Source unique : planRecapGains. */
function planPrioritesData(recap){
  const items = [];
  let nbSerie = 0, totalSerie = 0;
  (recap.postes || []).forEach(p => {
    const refs = p.refs || [];
    if(refs.some(r => r.serie && r.gain > 0)){ nbSerie++; totalSerie += p.gainActe || 0; return; }
    const l = lignes.find(x => x.id === p.ligneId);
    const blocs = l ? scenariosPostes(l, p.opCode) : [];
    let valide = null, positif = null, echec = null, abandon = null;
    let depense = 0; const manques = [];
    refs.forEach(r => {
      if(r.volume > 0 && r.tBase != null) depense += r.tBase * r.volume;
      else if(r.prodSc) manques.push(r.volume ? "coût de la production (prix ou DDV des logements)" : "volume annuel de production");
      if(r.meilleur){
        const sc = r.meilleur.sc, st = scenarioStats(sc);
        if(sc.statut === "valide" && !valide) valide = { sc, gain: r.gain };
        else if(st.validCount > 0 && !positif) positif = { sc, gain: r.gain };
        const ev = scenarioEchec(sc);
        if(ev && !echec) echec = { sc, motifs: ev };
        if(sc.statut === "abandonne" && !abandon) abandon = { sc, motif: sc.statutMotif || "" };
      } else if(r.prodSc && !r.nonChiffre && (r.gain === null || r.gain === undefined)){
        manques.push("chiffrage du scénario candidat");
      }
    });
    const candidatsVivants = blocs.reduce((a, b) => a + (b.scs || []).filter(s =>
      !s.baseline && !/base excel/i.test(s.name || "") && !scenarioEchec(s) && s.statut !== "abandonne").length, 0);
    const base = { ligne: p.ligne, opCode: p.opCode, nbRefs: refs.length,
                   depense: depense > 0 ? depense : null };
    if(valide){
      items.push(Object.assign(base, { cle: "valide", scenario: valide.sc.name || "Sans nom",
        potentiel: valide.gain, codif: codificationScenario(valide.sc),
        step: "Passer en série — le gain est prêt" }));
      return;
    }
    if(positif){
      const st = scenarioStats(positif.sc);
      const seuil = parseFloat(positif.sc.validationThreshold) || 5;
      items.push(Object.assign(base, { cle: "positifs", scenario: positif.sc.name || "Sans nom",
        potentiel: positif.gain, codif: codificationScenario(positif.sc),
        step: "Compléter la validation : " + st.validCount + " essai(s) conforme(s), protocole " + seuil + "×" }));
      return;
    }
    if(echec || abandon){
      items.push(Object.assign(base, { cle: "arrete", scenario: (echec || abandon).sc.name || "Sans nom",
        motifs: echec ? echec.motifs : [abandon.motif || "abandonné sans motif enregistré"],
        step: "Tirer les enseignements, ou relancer autrement" }));
      return;
    }
    if(!candidatsVivants && depense > 0){
      items.push(Object.assign(base, { cle: "jamais",
        step: "Premier essai à lancer — tout gain de durée de vie se multiplie par cette dépense" }));
      return;
    }
    if(!manques.length) manques.push("aucun scénario chiffrable face à la production");
    items.push(Object.assign(base, { cle: "insuffisant", manques }));
  });
  /* l'univers plaquettes (Hermes Q3) : un article de la base 2025 sans aucun
     lien outillage (ni dans un logement, ni au catalogue) sort du périmètre —
     sur une ligne explicite, jamais en silence. */
  const univers = new Set();
  lignes.forEach(l => (l.references || []).forEach(r => (r.ops || []).forEach(o => (o.scenarios || []).forEach(sc =>
    (sc.outils || []).forEach(ou => (ou.logements || []).forEach(g => {
      const m = String(g.codeArticle || g.mabec || "").trim().toUpperCase();
      if(m) univers.add(m);
    }))))));
  (catalogue || []).forEach(a => univers.add(a.mabec));
  let horsTotal = 0; const horsArticles = [];
  if(conso2025){
    Object.entries(conso2025.parMabec).forEach(([mabec, e]) => {
      if(univers.has(mabec)) return;
      const cout = conso2025Somme(e);
      if(cout > 0){ horsTotal += cout; horsArticles.push({ mabec, cout }); }
    });
    horsArticles.sort((a, b) => b.cout - a.cout);
  }
  return { dejaEnSerie: { nb: nbSerie, total: totalSerie }, items, horsTotal, horsArticles };
}

function planPrioritesHTML(recap){
  const d = planPrioritesData(recap);
  const euro = v => (v != null && v > 0) ? fmtEuroCourt(Math.round(v)) : "—";
  const badgeCodif = cod => {
    if(!cod || cod.etat === "codifie" || cod.etat === "sansExigence" || cod.etat === "sansArticle") return "";
    if(cod.etat === "attente") return ` <span class="pc-stat attente" style="font-size:10.5px;" title="Codification par le service administratif de Matis : prérequis du cycle de commande standard — sans elle, BADP seulement (montants et récurrence limités).">codification attendue ${cod.jours ?? 0} j</span>`;
    return ` <span class="pc-stat attente" style="font-size:10.5px;" title="Aucune codification demandée : le cycle de commande standard est inaccessible — BADP seulement.">codification non demandée</span>`;
  };
  const PANIERS = [
    ["valide", "Validés, pas encore en série", "le gain est prêt — un geste le sort de la file (axe facilité : le plus court)"],
    ["positifs", "Essai positif — validation à compléter", "le potentiel est démontré une fois : le protocole (répété 5×) fait le reste"],
    ["jamais", "Dépense forte, jamais travaillée", "aucun scénario concurrent : tout gain de durée de vie se multiplie par cette dépense (axe potentiel)"],
    ["insuffisant", "Données insuffisantes — ce qui manque, nommé", "l'opportunité existe, la conclusion non : chaque absence est listée, jamais chiffrée en silence"],
    ["arrete", "Travaillé et arrêté — motif", "ce qu'on a appris et où l'on a stoppé : une information, pas un échec à cacher (Hermes)"]
  ];
  let corps = "";
  PANIERS.forEach(([cle, titre, sous]) => {
    const items = d.items.filter(x => x.cle === cle)
      .sort((a, b) => (b.potentiel || b.depense || 0) - (a.potentiel || a.depense || 0));
    if(!items.length) return;
    corps += `<tr class="pc-grp"><td colspan="4">${escapeAttr(titre)} (${items.length})<br><span style="font-weight:400; font-size:11px; color:var(--ink-faint);">${escapeAttr(sous)}</span></td></tr>`;
    items.forEach(x => {
      const fac = escapeAttr(x.step || "") + badgeCodif(x.codif)
        + (x.manques ? ` <span style="color:var(--amber);">${escapeAttr("manque : " + x.manques.join(", "))}</span>` : "")
        + (x.motifs ? `<br><span style="color:var(--amber);">${escapeAttr("motif : " + x.motifs.join(" · "))}</span>` : "");
      corps += `<tr>
        <td class="mono">${escapeAttr(x.ligne)} · ${escapeAttr(x.opCode)}${x.scenario ? `<br><span style="font-size:11px; color:var(--ink-faint);">${escapeAttr(x.scenario)}</span>` : ""}</td>
        <td class="mono" title="Coût de production actuel : la base × le volume — l'axe potentiel quand aucun candidat n'existe.">${euro(x.depense)}<small style="color:var(--ink-faint);"> /an</small></td>
        <td class="mono" style="font-weight:600; color:var(--green);">${x.potentiel != null && x.potentiel > 0 ? "+ " + fmtEuroCourt(Math.round(x.potentiel)) + "<small style=\\'color:var(--ink-faint);\\'> /an</small>" : "—"}</td>
        <td style="font-size:12.5px;">${fac}</td>
      </tr>`;
    });
  });
  if(!corps && !d.horsTotal) return `<p class="panel-hint">Aucune priorité calculable : les lignes apparaissent dès qu'un poste porte de la dépense ou des essais.</p>`;
  return `<table class="simul-table">
    <thead><tr><th>Poste</th><th>Dépense /an <span title="Axe POTENTIEL : le coût de production actuel (base × volume).">ⓘ</span></th><th>Potentiel /an <span title="Axe POTENTIEL : le gain annuel du meilleur scénario en course, quand il est chiffrable.">ⓘ</span></th><th>Facilité de concrétisation <span title="Axe FACILITÉ : la prochaine étape et les freins (codification en attente, données manquantes, motif d'arrêt) — jamais fondus avec le potentiel en un score.">ⓘ</span></th></tr></thead>
    <tbody>${corps}</tbody>
  </table>
  ${d.dejaEnSerie.nb ? `<p class="panel-hint" style="margin-top:8px;">Hors course à courir : <b>${d.dejaEnSerie.nb} poste(s) déjà en série</b> — ${fmtEuroCourt(Math.round(d.dejaEnSerie.total))} /an actés (voir « Scénarios en validation »).</p>` : ""}
  ${d.horsTotal ? `<p class="panel-hint" style="margin-top:4px;">Hors périmètre plaquettes : <b>${fmtEuroCourt(Math.round(d.horsTotal))} /an</b> de la base 2025 non comptés ici (articles sans aucun lien outillage : embouts, rondelles…) — ${d.horsArticles.slice(0, 3).map(h => escapeAttr(h.mabec) + " " + fmtEuroCourt(Math.round(h.cout)) + " €").join(", ")}${d.horsArticles.length > 3 ? "…" : ""} (§3.5 : nommés, pas masqués).</p>` : ""}`;
}

function planScenariosHTML(recap){''', "planPrioritesData + planPrioritesHTML")

# ── 2. intégration dans le tableau de bord ──
remplace('''    <div class="pc-titre-section">Scénarios en validation — le gain par poste</div>
    ${planScenariosHTML(recap)}
    <div class="pc-titre-section">Consommations et scénarios de base</div>''',
'''    <div class="pc-titre-section">Scénarios en validation — le gain par poste</div>
    ${planScenariosHTML(recap)}
    <div class="pc-titre-section">Où investir — les priorités</div>
    ${planPrioritesHTML(recap)}
    <div class="pc-titre-section">Consommations et scénarios de base</div>''', "intégration matrice C")

# ── 3. version + nouveautés ──
remplace('const TOOL_VERSION = "4.107.0";', 'const TOOL_VERSION = "4.108.0";', "version 4.108.0")
entree = '''  { version:"4.108.0", date:"24/10/2026", points:[
    "<b>Où investir — les priorités.</b> Une nouvelle section du Plan qui répond à « sur quel poste concentrer les efforts ? » : <b>cinq paniers</b> — validés pas encore en série, essai positif à compléter (protocole 5×), <b>dépense forte jamais travaillée</b>, données insuffisantes (<b>ce qui manque est nommé</b>), et <b>travaillé et arrêté — motif</b> (le cas SN60 : une information, pas un échec à cacher). Deux axes jamais fondus en un score : le <b>potentiel</b> (dépense et gain €/an) et la <b>facilité de concrétisation</b> (prochaine étape, freins — dont la codification en attente avec son âge). Et les articles de la base 2025 sans aucun lien outillage sortent du périmètre <b>sur une ligne explicite</b>, pas en silence."
  ]},
'''
src = src.replace('const NOUVEAUTES = [\n', 'const NOUVEAUTES = [\n' + entree, 1)
print("ok : nouveautes 4.108.0")

io.open(p, "w", encoding="utf-8").write(src)
print("taille:", n0, "->", len(src))
