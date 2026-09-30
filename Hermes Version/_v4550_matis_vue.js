
/* ═══ L'ÉCRAN — le rendu de la mesure, et son ouverture ═══════════════════ */

/* le résultat de la dernière lecture : en mémoire seulement, JAMAIS écrit dans
   les données du suivi. C'est une observation, pas un import (option C). */
let matisLecture = null;

/* le couple « ligne × référence » du classeur, rapproché de la ligne de l'outil
   quand elle existe. Le classeur dit « E1 », l'outil dit « EMAG 1 » : le
   rapprochement est explicite et visible, jamais deviné en silence. */
const MATIS_LIGNE_OUTIL = { E1: "EMAG 1", E2: "EMAG 2", E3: "EMAG 3", H: "HESSAPP" };

function matisRapproche(c){
  const nomLigne = MATIS_LIGNE_OUTIL[c.codeLigne] || c.codeLigne;
  const lg = lignes.find(l => (l.nom || "").toUpperCase() === nomLigne.toUpperCase());
  const ref = lg ? lg.references.find(r => (r.nom || "").toUpperCase().includes(String(c.ref).split(" ")[0].toUpperCase())) : null;
  return { nomLigne, ligneId: lg ? lg.id : null, referenceId: ref ? ref.id : null };
}

function matisVueHTML(){
  if(!matisLecture) return `<p class="panel-hint">Aucun classeur lu pour l'instant. Choisissez le fichier
    « SUIVI DES CONSOMMATIONS… » de Matis : il est lu <b>sur ce poste uniquement</b>, rien n'est envoyé
    nulle part, et rien n'est écrit dans le suivi.</p>`;

  const couples = matisLecture.couples || [];
  const produits = couples.filter(c => c.aProduction);
  const totalTheo = couples.reduce((a, c) => a + (c.coutAnnuelTheorique || 0), 0);
  const totalReel = couples.reduce((a, c) => a + (c.coutAnnuelReel || 0), 0);
  const ecart = totalReel - totalTheo;
  const ecartPct = totalTheo ? (ecart / totalTheo) * 100 : null;

  const tuiles = `
    <div class="mt-bilan">
      <div class="mt-tuile">
        <div class="mt-l">Budget-outillage / an</div>
        <div class="mt-v">${fmtEuroCourt(Math.round(totalTheo))}</div>
        <div class="mt-sub">théorique, d'après prix et durées de vie</div>
      </div>
      <div class="mt-tuile">
        <div class="mt-l">Consommé / an</div>
        <div class="mt-v">${fmtEuroCourt(Math.round(totalReel))}</div>
        <div class="mt-sub">réel, d'après le relevé de Matis</div>
      </div>
      <div class="mt-tuile ${ecart > 0 ? "alerte" : (ecart < 0 ? "ok" : "")}">
        <div class="mt-l">Écart</div>
        <div class="mt-v ${ecart > 0 ? "mt-ecart-pos" : (ecart < 0 ? "mt-ecart-neg" : "")}">${ecart >= 0 ? "+" : "−"}${fmtEuroCourt(Math.round(Math.abs(ecart)))}</div>
        <div class="mt-sub">${ecartPct === null ? "—" : (ecartPct >= 0 ? "+" : "−") + fmt(Math.abs(ecartPct), 0) + " % vs théorie"}</div>
      </div>
      <div class="mt-tuile">
        <div class="mt-l">Couples produits</div>
        <div class="mt-v">${produits.length}<small> / ${couples.length}</small></div>
        <div class="mt-sub">avec une production relevée</div>
      </div>
    </div>`;

  const lignes = couples.map(c => {
    const r = matisRapproche(c);
    const mesure = c.ecart === null;
    return `<tr>
      <td class="mt-lign">${escapeAttr(c.codeLigne)} · ${escapeAttr(c.ref)}</td>
      <td class="num">${c.aProduction ? fmt(c.production, 0) : "—"}</td>
      <td class="num">${c.cppTheorique ? fmt(c.cppTheorique, 4) : "—"}</td>
      <td class="num">${c.cppReel ? fmt(c.cppReel, 4) : "—"}</td>
      <td class="num ${c.ecart > 0 ? "mt-ecart-pos" : (c.ecart < 0 ? "mt-ecart-neg" : "")}">${mesure ? "—" : (c.ecart >= 0 ? "+" : "−") + fmt(Math.abs(c.ecart), 4)}</td>
      <td class="mt-raison">${escapeAttr(libelleEcartMatis(c))}${r.ligneId ? "" : ` <span class="mt-avert">(ligne hors suivi : ${escapeAttr(r.nomLigne)})</span>`}</td>
    </tr>`;
  }).join("");

  return `
    <p class="mt-raz"><b>Ce que cet écran mesure.</b> Le budget-outillage de l'outil dit ce que la
      plaquette <i>devrait</i> coûter (prix × arêtes ÷ durées de vie). Le classeur de Matis dit ce
      qu'elle <i>a réellement</i> coûté. L'écart entre les deux mesure la santé du plan outillage :
      un écart stable et connu se budgète, un écart qui grossit se traite. Rien ici n'est une
      erreur de saisie — c'est de l'écart entre un modèle et le terrain.</p>
    <div class="mt-recap">
      <label class="ghost" for="mtFichier" style="cursor:pointer;padding:8px 13px;">📂 Lire le classeur de Matis…</label>
      <input type="file" id="mtFichier" accept=".xlsm,.xlsx" hidden>
      <span class="mt-fichier">${escapeAttr(matisLecture.fichier)} — lu le ${escapeAttr(matisLecture.luLe)} · ${(matisLecture.feuilles || []).length} feuilles « Cout pièce »</span>
    </div>
    ${tuiles}
    <div class="tbl-wrap">
      <table class="mt-tbl">
        <thead><tr><th>Couple</th><th class="num">Prod.</th><th class="num">CPP théo.</th><th class="num">CPP réel</th><th class="num">Écart</th><th>Lecture</th></tr></thead>
        <tbody>${lignes}</tbody>
      </table>
    </div>
    <p class="panel-hint" style="margin-top:12px;">Les couples à production nulle sont des postes
      ouverts ou arrêtés sur la période : ils figurent pour mémoire, ils ne comptent pas dans le bilan.
      Cette lecture est un <b>constat</b> — elle n'écrit rien dans le suivi et n'y changera rien tant
      que la décision 2 version n'aura pas été prise.</p>
    <div class="panel-actions">
      <button class="ghost" id="mtTools">Détail par outil</button>
      <button class="primary" id="mtClose">Fermer</button>
    </div>`;
}

function matisDetailHTML(){
  if(!matisLecture) return "";
  const couples = (matisLecture.couples || []).filter(c => c.aProduction);
  const blocs = couples.map(c => `
    <div class="mt-detail" style="margin-bottom:14px;">
      <h4 style="font-family:var(--font-disp);font-size:15px;margin:0 0 6px;">${escapeAttr(c.codeLigne)} · ${escapeAttr(c.ref)}</h4>
      <div class="tbl-wrap">
        <table class="mt-tbl">
          <thead><tr><th>Outil</th><th>OP</th><th>Article</th><th>MABEC</th><th class="num">CPP théo.</th><th class="num">CPP réel</th><th class="num">Qté réelle</th></tr></thead>
          <tbody>${c.outils.map(o => `<tr>
            <td class="mt-lign">${escapeAttr(o.numero)}</td>
            <td class="mt-op">${escapeAttr(o.opCode)}</td>
            <td class="mt-op">${escapeAttr(o.article || "—")}</td>
            <td class="mt-op">${escapeAttr(o.mabec || "—")}</td>
            <td class="num">${o.cppTheorique ? fmt(o.cppTheorique, 5) : "—"}</td>
            <td class="num">${o.cppReel ? fmt(o.cppReel, 5) : "—"}</td>
            <td class="num">${o.qteReelle === null ? "—" : fmt(o.qteReelle, 0)}</td>
          </tr>`).join("")}</tbody>
        </table>
      </div>
    </div>`).join("");
  return `<h3>Classeur Matis — détail par outil</h3>
    <p class="panel-hint">Les numéros d'outil et les articles MABEC sont ceux que Matis utilise au
      quotidien. Les comparer à l'outillage saisi dans le suivi est le premier pas d'un éventuel
      enrichissement du modèle.</p>
    ${blocs || `<p class="panel-hint">Aucun couple avec production relevée.</p>`}
    <div class="panel-actions"><button class="primary" id="mtDetailClose">Fermer</button></div>`;
}

function renderMatis(){
  const wrap = document.getElementById("matisPanel");
  if(!wrap) return;
  wrap.innerHTML = matisVueHTML();
  const fermer = document.getElementById("mtClose");
  if(fermer) fermer.addEventListener("click", fermerPanneaux);
  const detail = document.getElementById("mtTools");
  if(detail) detail.addEventListener("click", () => {
    const w2 = document.getElementById("matisDetailPanel");
    if(w2){ w2.innerHTML = matisDetailHTML(); ouvrirPanneau("matisDetailPanel"); }
  });
  const fichier = document.getElementById("mtFichier");
  if(fichier) fichier.addEventListener("change", async () => {
    const f = fichier.files && fichier.files[0];
    if(!f) return;
    /* l'utilisateur a choisi SON fichier : rien n'est envoyé, rien n'est écrit */
    try {
      matisLecture = await matisLireClasseur(f);
    } catch(err){
      dialogueAlerte("Lecture impossible : " + err.message, "Classeur Matis");
      return;
    }
    renderMatis();
  });
}

function ouvrirMatis(){ renderMatis(); ouvrirPanneau("matisPanel"); }
