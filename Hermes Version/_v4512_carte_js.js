/* ════════════════════════════════════════════════════════════════════════════
   v4.51.2 — CARTE ATELIER (couche 0, lecture seule)

   L'écran d'entrée spatial de l'outil : des tuiles = les postes (ligne x opCode)
   DÉCLARÉS dans LIGNES_SEPT_FONS. On lit la carte en un coup d'œil — où en est
   l'usine, qu'a-t-on gagné, qu'est-ce qui reste — puis on descend couche par couche.

   Trois règles non négociables, tenues ici :
   · D3 — la tuile ne montre AUCUN chiffre que le bandeau du scénario ne montre pas :
     tout passe par gainPoste() (4.51.0) → bilanAnnuel() → perimetreCompare() (v4.45) ;
   · le coût machine exige la ligne du poste — c'est pour ça que gainPoste() passe
     la ligne à coutsDetail(), alors que pieceCPPComplet() (v4.49) s'appuie sur le
     repli getActiveLigne() et n'a donc de sens qu'en contexte d'une référence
     ouverte. La carte et l'A4 Mission consomment gainPoste(), jamais pieceCPPComplet ;
   · jamais de K ni de P_req : la carte est présentable telle quelle en réunion.
   ────────────────────────────────────────────────────────────────────────── */

/* Le filtre de la carte : le projet actif par défaut (H1-b), « toute l'usine » à un clic.
   null = toute l'usine. Mémorisé comme le filtre du tableau de bord, mais indépendant :
   chaque écran a SON filtre, sinon les deux se marchent dessus. */
let carteFiltreProjetId = null;
let carteProjetChoisi = false;   // false = suit le projet actif tant qu'on n'a pas choisi

/* Les postes visibles sur la carte. Une tuile = (ligne déclarée x machine déclarée).
   La ligne doit exister dans les données (sinon on dessine une ligne sans suivi) ; la
   machine vient de la déclaration, jamais des scénarios rencontrés. */
function cartePostes(){
  const out = [];
  lignes.forEach(ligne => {
    postesLigne(ligne, LIGNES_SEPT_FONS).forEach(m => {
      const poste = gainPoste(ligne, m.code, LIGNES_SEPT_FONS);
      out.push({ ligne, code: m.code, nomMachine: m.nom, poste,
                 etat: etatTuile(poste), refs: poste.refs || [] });
    });
  });
  return out;
}

/* Le filtre projet : « mon projet » garde les postes qui portent au moins un scénario
   étiqueté dans le projet. On ne filtre pas sur le gain mais sur la présence — sinon un
   poste « à chiffrer » (encore vide) disparaît justement quand on cherche à le remplir. */
function carteVisiblePostes(tous, pjId){
  if(!pjId) return tous;
  const pj = projets.find(p => p.id === pjId);
  if(!pj) return tous;
  return tous.filter(t => t.refs.some(r => r.meilleur && projetContientScenario(pj, t.ligne.id, r.ref.id, null, r.meilleur.sc.id)));
}

/* Le décompte de recette A2 : quelle part des tuiles porte une information
   ACTIONNABLE (un gain, une cible, un essai ouvert) ? C'est le seuil qui dira si la
   carte est utile ou décorative — mesuré, pas ressenti. */
function carteRecetteA2(tuiles){
  if(!tuiles.length) return { total: 0, actionnables: 0, ratio: 0 };
  const actionnables = tuiles.filter(t => t.etat === "gagne" || t.etat === "encours" || t.etat === "aChiffrer").length;
  return { total: tuiles.length, actionnables, ratio: actionnables / tuiles.length };
}

/* ── Le rendu ─────────────────────────────────────────────────────────────── */
const CARTE_ETATS = {
  gagne:      { label: "Gagné",       classe: "gagne" },
  encours:    { label: "En cours",    classe: "encours" },
  aChiffrer:  { label: "À chiffrer",  classe: "achiffrer" },
  opportunite:{ label: "Opportunité", classe: "opportunite" }
};

function carteTuileHTML(t, pjId){
  const p = t.poste;
  const e = CARTE_ETATS[t.etat] || CARTE_ETATS.opportunite;
  const dom = p.refDominante;
  const autres = Math.max(0, (p.refs || []).length - 1);

  /* le pouls : deux chiffres, jamais plus (D2). Acté en gros s'il existe, projeté en
     dessous. Un poste sans gain n'affiche PAS de 0 € — il affiche son invitation
     (« à chiffrer ») ou son silence (opportunité). */
  let pouls = "";
  if(p.gainActe > 0){
    pouls = `<span class="ca-acte">${p.gainActe >= 0 ? "+" : "−"}${fmtEuroCourt(Math.abs(p.gainActe))}<small>/an acté</small></span>`;
  }
  if(p.gainProjete > 0){
    pouls += `<span class="ca-projete">${p.gainProjete >= 0 ? "+" : "−"}${fmtEuroCourt(Math.abs(p.gainProjete))}<small>/an projeté</small></span>`;
  }
  if(!pouls){
    pouls = t.etat === "aChiffrer"
      ? `<span class="ca-invite">cible ${fmt(p.cibleCPP, 3)} €<small>— à chiffrer</small></span>`
      : `<span class="ca-vide">—</span>`;
  }

  /* le chemin prod → cible : la barre que la hiérarchie regarde. */
  const chemin = p.chemin === null ? "" :
    `<div class="ca-chemin" title="Part du chemin vers la cible du site déjà parcourue sur ce poste">
       <div class="ca-track"><div class="ca-fill" style="width:${Math.round(p.chemin)}%"></div></div>
       <span class="ca-pct">${Math.round(p.chemin)} %</span>
     </div>`;

  /* le libellé du poste : le nom de la machine s'il est déclaré, le code d'OP sinon.
     Jamais l'inverse — « OP10 » ne dit rien, « Ébauche piste » si. */
  const titre = escapeAttr(t.nomMachine || t.code);
  const sousTitre = escapeAttr((dom && dom.ref && dom.ref.nom) || "aucune référence");
  const nbRef = autres > 0 ? `<span class="ca-refs" title="${autres} autre(s) référence(s) sur ce poste">+${autres} réf.</span>` : "";

  /* le multi-geste (R3) : la tuile elle-même EST la fiche couche 1 (survol = titre
     déjà visible, tap = la même fiche ouverte), et le bouton « Ouvrir le poste → »
     qu'elle porte est la porte explicite vers la couche 2. Un seul survol, pas
     deux couches de survol qui se marchent dessus. */
  return `<div class="ca-tuile ${e.classe}" data-ligne="${escapeAttr(t.ligne.id)}" data-code="${escapeAttr(t.code)}" tabindex="0" role="button">
    <div class="ca-tete">
      <span class="ca-titre">${titre}</span>
      <span class="ca-etat">${e.label}</span>
    </div>
    <div class="ca-ref-ligne">${sousTitre} ${nbRef}</div>
    <div class="ca-pouls">${pouls}</div>
    ${chemin}
    ${t.etat === "opportunite" ? `<div class="ca-tentant">déclaré, jamais travaillé</div>` : ""}
    ${(p.nonChiffres || 0) > 0 ? `<div class="ca-avertir" title="Une opération de ce poste n'est pas chiffrable : le gain affiché ne la compte pas.">${p.nonChiffres} opération${p.nonChiffres > 1 ? "s" : ""} à chiffrer</div>` : ""}
  </div>`;
}

function renderCarte(){
  const wrap = document.getElementById("cartePanel");
  if(!wrap) return;

  /* H1-b : la carte s'ouvre sur le projet actif tant que l'utilisateur n'a pas choisi
     explicitement un filtre sur la carte elle-même. */
  if(!carteProjetChoisi) carteFiltreProjetId = activeProjetId || null;
  const pj = carteFiltreProjetId ? projets.find(p => p.id === carteFiltreProjetId) : null;

  const tous = cartePostes();
  const visibles = carteVisiblePostes(tous, carteFiltreProjetId);
  const recette = carteRecetteA2(visibles);

  /* le décompte d/usine : la carte doit raconter l'usine entière même filtrée. */
  const parLigne = {};
  tous.forEach(t => { (parLigne[t.ligne.nom || "?"] = parLigne[t.ligne.nom || "?"] || []).push(t); });

  const sections = lignes.map(ligne => {
    const tuilesL = visibles.filter(t => t.ligne.id === ligne.id);
    if(!tuilesL.length) return "";
    const nom = ligne.nom || "Ligne sans nom";
    const gainL = tuilesL.reduce((a, t) => a + (t.poste.gainActe || 0), 0);
    const infos = [];
    if(ligne.coutHoraire !== "" && !isNaN(parseFloat(ligne.coutHoraire))) infos.push(fmt(parseFloat(ligne.coutHoraire), 2) + " €/h");
    infos.push(`${tuilesL.filter(t => t.etat === "gagne").length} gagné${tuilesL.filter(t => t.etat === "gagne").length > 1 ? "s" : ""}`);
    return `<section class="ca-ligne">
      <h3 class="ca-ligne-titre">${escapeAttr(nom)}
        <span class="ca-ligne-info">${escapeAttr(infos.join(" · "))}</span>
        ${gainL > 0 ? `<span class="ca-ligne-gain">+${fmtEuroCourt(gainL)}/an acté</span>` : ""}
      </h3>
      <div class="ca-grille">${tuilesL.map(t => carteTuileHTML(t, carteFiltreProjetId)).join("")}</div>
    </section>`;
  }).join("");

  const filtreHTML = projets.length ? `
    <div class="ca-filtre">
      <label for="caFiltreProjet">Vue</label>
      <select id="caFiltreProjet">
        <option value="">Toute l'usine</option>
        ${projets.map(x => `<option value="${x.id}" ${x.id === carteFiltreProjetId ? "selected" : ""}>Projet « ${escapeAttr(x.nom)} »</option>`).join("")}
      </select>
      <span class="ca-filtre-note">${pj
        ? `Postes étiquetés dans « ${escapeAttr(pj.nom)} ».`
        : "Toutes les machines déclarées de l'usine."}</span>
    </div>` : `<p class="panel-hint">Aucun projet défini : la carte montre toute l'usine. Créez un projet pour la filtrer.</p>`;

  wrap.innerHTML = `
    <h3>Carte atelier</h3>
    ${filtreHTML}
    <p class="panel-hint">Une tuile = une machine, lisible en un coup d'œil. Un poste marqué <b>À chiffrer</b> porte une cible du site mais n'a pas encore de mesure : c'est une invitation, pas un poste raté. Touchez une tuile pour sa fiche, puis « Ouvrir le poste » pour entrer dans le détail.</p>
    <div class="ca-recette" title="Part des tuiles portant une information actionnable (gain, cible ou essai ouvert)">
      <b>${recette.actionnables}</b> tuiles actionnables sur ${recette.total} — ${Math.round(recette.ratio * 100)} %
      ${recette.ratio >= 1/3 ? `<span class="ca-ok">carte utile</span>` : `<span class="ca-faible">carte creuse — filtrer par projet</span>`}
    </div>
    ${sections || `<p class="panel-hint">Aucun poste à afficher${pj ? " dans ce projet" : ""}. Les machines déclarées par l'atelier dessinent la carte ; un poste sans donnée reste visible en « Opportunité ».</p>`}
    <div class="panel-actions"><button class="primary" id="carteClose">Fermer</button></div>
  `;

  const btn = document.getElementById("carteClose");
  if(btn) btn.addEventListener("click", fermerPanneaux);
  const sel = document.getElementById("caFiltreProjet");
  if(sel) sel.addEventListener("change", () => { carteFiltreProjetId = sel.value || null; carteProjetChoisi = true; renderCarte(); });
}

/* l'entrée : le bouton de la barre d'outils ouvre la carte (v4.51.2) */
function ouvrirCarte(){ renderCarte(); ouvrirPanneau("cartePanel"); }
