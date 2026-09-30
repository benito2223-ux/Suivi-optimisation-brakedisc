/* ════════════════════════════════════════════════════════════════════════════
   v4.54.0 — FICHE POSTE (couche 1) : la porte qui manquait entre la carte et le détail

   La carte (4.51.2) dit QUOI : l'état, le gain, ce qui reste. La couche 2 (4.52) dit
   COMMENT : le scénario, les essais, les preuves. Entre les deux, il n'y avait rien —
   on sautait de la tuile au scénario sans jamais répondre à la seule question qui
   compte en atelier : « qu'est-ce qu'il se passe sur CETTE machine ? »

   La fiche répond à cette question, et porte une porte EXPLICITE vers la couche 2
   (« Ouvrir le poste → »). C'est le geste double (R3) : le survol / le premier
   toucher montre la fiche, le bouton entre. Le geste devient découvrable au lieu
   d'être un pari, et l'utilisateur n'est jamais forcé de deviner qu'un second
   toucher entre dans le détail.

   Trois règles tenues ici (constitution v1.1) :
   · D3 — la fiche ne montre AUCUN chiffre que le bandeau du scénario ne montre pas :
     tout vient de gainPoste() (4.51.0), jamais d'un recalcul local ;
   · la raison d'un état est toujours à côté de l'état (règle d'interface §5.2) ;
   · jamais de K ni de P_req : la fiche est présentable telle quelle.
   ────────────────────────────────────────────────────────────────────────── */

/* la prochaine étape du plan, dite en atelier : c'est l'information qui manque le
   plus dans tout l'outil aujourd'hui. Elle se déduit de l'état, jamais d'un statut
   technique stockée — donc elle ne peut pas mentir. */
function prochaineEtapePoste(t){
  const p = t.poste;
  if(t.etat === "gagne"){
    /* un poste acté se maintient : on le revalide, on ne le réinvente pas */
    const r = (p.refs || []).find(x => x.serie);
    return "En production — maintenir et confirmer au prochain rééquilibrage";
  }
  if(t.etat === "encours"){
    const r = (p.refs || []).find(x => x.meilleur && !x.serie);
    if(r && r.meilleur){
      const seuil = r.meilleur.sc.validationThreshold || 5;
      const faits = ((r.meilleur.sc.essais || []).length);
      return faits < seuil
        ? `Terminer le protocole ${seuil}× — ${faits}/${seuil} essais relevés`
        : `Protocole ${seuil}× atteint — passer en production`;
    }
    return "Essai en cours — relevés à finir";
  }
  if(t.etat === "aChiffrer"){
    return "Cible du site posée, aucune mesure : chiffrer la production de ce poste";
  }
  return "Poste déclaré, jamais travaillé — premier essai à faire";
}

/* Les scénarios du poste, regroupés par référence. C'est la lecture « par qui on
   travaille » : sur EMAG 1, OP10 sert la 356x26 et la 304x28 — la fiche le dit. */
function fichePostesReferences(t){
  return (t.poste.refs || []).map(r => {
    const st = r.serie ? "serie" : (r.gain !== null && r.gain > 0 ? "essai" : "essai");
    return { ref: r.ref, serie: r.serie, gain: r.gain, volume: r.volume,
             tBase: r.tBase, gainAnnuel: r.gain, seuil: r.meilleur ? (r.meilleur.sc.validationThreshold || 5) : null,
             nbEssais: r.meilleur ? ((r.meilleur.sc.essais || []).length) : 0,
             scId: r.meilleur ? r.meilleur.sc.id : (r.prodSc ? r.prodSc.id : null),
             statut: st };
  }).filter(x => x.scId);
}

function fichePosteHTML(t){
  const p = t.poste;
  const e = CARTE_ETATS[t.etat] || CARTE_ETATS.opportunite;
  const dom = p.refDominante;
  const nomRef = (dom && ((dom.ref && dom.ref.nom) || dom.nom)) || "";
  const refs = fichePostesReferences(t);
  const etape = prochaineEtapePoste(t);

  /* le pouls, identique à la tuile (D3 : même fonction, même valeur) */
  let pouls = "";
  if(p.gainActe > 0) pouls += `<span class="fp-acte">${p.gainActe >= 0 ? "+" : "−"}${fmtEuroCourt(Math.abs(p.gainActe))}<small>/an acté</small></span>`;
  if(p.gainProjete > 0) pouls += `<span class="fp-projete">${p.gainProjete >= 0 ? "+" : "−"}${fmtEuroCourt(Math.abs(p.gainProjete))}<small>/an projeté</small></span>`;
  if(!pouls) pouls = t.etat === "aChiffrer"
    ? `<span class="fp-invite">cible ${fmt(p.cibleCPP, 3)} €<small>— à chiffrer</small></span>`
    : `<span class="fp-vide">aucun gain chiffré</span>`;

  /* les références du poste : le travail réel, pas le concept */
  const lignesRef = refs.length ? refs.map(x => `
    <div class="fp-ref">
      <span class="fp-ref-nom">${escapeAttr((x.ref && x.ref.nom) || "référence")}</span>
      <span class="statut-pill ${x.serie ? "serie" : "essai"}">${x.serie ? "en production" : statutLabel("essai")}</span>
      ${x.gainAnnuel ? `<span class="fp-ref-gain">${x.gainAnnuel >= 0 ? "+" : "−"}${fmtEuroCourt(Math.abs(x.gainAnnuel))}/an</span>` : ""}
      ${x.seuil ? `<span class="fp-ref-prog">${x.nbEssais}/${x.seuil} essais</span>` : ""}
    </div>`).join("") : `<p class="fp-note">Aucune référence travaille ce poste pour l'instant.</p>`;

  /* la porte vers la couche 2 — visible, explicite, découvrable (R3) */
  const porte = t.etat === "opportunite" ? "" : `
    <div class="fp-actions">
      <button class="primary fp-ouvrir" data-ligne="${escapeAttr(t.ligne.id)}" data-code="${escapeAttr(t.code)}"
        title="Ouvrir le scénario de production de ce poste : composition, essais, preuves">Ouvrir le poste →</button>
    </div>`;

  return `<div class="fp-fiche ${e.classe}" data-ligne="${escapeAttr(t.ligne.id)}" data-code="${escapeAttr(t.code)}" role="dialog" aria-label="Fiche poste ${escapeAttr(t.nomMachine || t.code)}">
    <div class="fp-tete">
      <div class="fp-titre-bloc">
        <p class="fp-eyebrow">${escapeAttr(t.ligne.nom || "")} · ${escapeAttr(t.code)}</p>
        <h4 class="fp-titre">${escapeAttr(t.nomMachine || t.code)}</h4>
      </div>
      <span class="ca-etat">${e.label}</span>
      <button class="ghost fp-fermer" title="Fermer la fiche" aria-label="Fermer la fiche">✕</button>
    </div>
    ${nomRef ? `<p class="fp-ref-dominante">Référence principale : <b>${escapeAttr(nomRef)}</b>${refs.length > 1 ? ` <span class="ca-refs">+${refs.length - 1} réf.</span>` : ""}</p>` : ""}
    <div class="ca-pouls fp-pouls">${pouls}</div>
    ${p.chemin === null ? "" : `
      <div class="fp-chemin">
        <span class="fp-chemin-l">Vers la cible du site</span>
        <div class="ca-track"><div class="ca-fill" style="width:${Math.round(p.chemin)}%"></div></div>
        <span class="ca-pct">${Math.round(p.chemin)} %</span>
      </div>`}
    <div class="fp-refs"><h5>Travail sur ce poste</h5>${lignesRef}</div>
    <p class="fp-etape"><b>Prochaine étape :</b> ${escapeAttr(etape)}</p>
    ${(p.nonChiffres || 0) > 0 ? `<p class="fp-avertir">${p.nonChiffres} opération${p.nonChiffres > 1 ? "s" : ""} non chiffrable${p.nonChiffres > 1 ? "s" : ""} — le gain affiché ne les compte pas.</p>` : ""}
    ${porte}
  </div>`;
}

/* l'état du panneau de fiche : null = fermé, sinon { ligneId, code } */
let fichePosteOuverte = null;

/* La fiche vit DANS la carte (superposée), pas dans un second panneau : c'est la
   couche 1 du même écran, pas une nouvelle fenêtre. Le survol desktop ouvre aussi,
   mais seulement si aucune fiche n'est déjà ouverte (sinon survoler une autre tuile
   pendant la lecture de la fiche sous le doigt). */
function renderFichePoste(tuiles, t){
  const zone = document.getElementById("carteFicheZone");
  if(!zone) return;
  if(!t){ zone.innerHTML = ""; zone.hidden = true; return; }
  zone.hidden = false;
  zone.innerHTML = fichePosteHTML(t);
  const fermer = zone.querySelector(".fp-fermer");
  if(fermer) fermer.addEventListener("click", () => { fichePosteOuverte = null; renderFichePoste(tuiles, null); });
  const ouvrir = zone.querySelector(".fp-ouvrir");
  if(ouvrir) ouvrir.addEventListener("click", () => ouvrirPosteDepuisFiche(t));
}

/* la porte de la fiche appelle exactement le même chemin que le bouton de la tuile
   (couche 2, v4.52) : une seule implémentation de « entrer dans ce poste ». */
function ouvrirPosteDepuisFiche(t){
  const ligne = lignes.find(x => x.id === t.ligne.id);
  const bloc = scenariosPostes(ligne, t.code)[0];
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
}
