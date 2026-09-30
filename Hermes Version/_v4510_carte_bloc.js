/* ════════════════════════════════════════════════════════════════════════════
   v4.51.0 — Carte atelier, couche 0 : le calcul pur du poste (sans un pixel d'UI)

   Deux fonctions PURES, testées, placées juste avant renderDashboard() (L11547) parce
   que la carte atelier est une évolution du tableau de bord : même source, jamais un
   second agrégat de gains. gainPoste() alimente la tuile et, plus tard, l'A4 Mission ;
   etatTuile() donne l'état de la tuile (gagné / en cours / à chiffrer / opportunité)
   sans jamais qu'une cascade de « if » dans le HTML décide de la couleur.

   Rappel D3 : la tuile n'affiche JAMAIS un chiffre que le bandeau du scénario
   n'afficherait pas. D'où le choix de bilanAnnuel() : c'est lui qui applique déjà
   perimetreCompare() (v4.45) et qui signale perimetrePartiel. On ne recalcule rien.
   ────────────────────────────────────────────────────────────────────────── */

/* Un poste = un couple (ligne x opCode). On ne dessine que les couples DÉCLARÉS :
   les machines de la ligne viennent de LIGNES_SEPT_FONS (v4.50), et les OP sans
   code exploitable (opCode "?", v4.50) ne dessinent aucune tuile — elles restent
   atteignables par la navigation experte. */
function postesLigne(ligne, lignesSeptFons){
  const def = (lignesSeptFons || []).find(d => d.nom === (ligne && ligne.nom));
  const machines = (def && def.machines) || [];
  return machines.map(m => ({ code: m.code, nom: m.nom || "", ligne }));
}

/* Les scénarios d'une ligne qui portent l'OP demandée (par CODE, pas par nom :
   « OP 30 Perçages » et « OP30 » sont le même poste). */
function scenariosPostes(ligne, opCode){
  const out = [];
  (ligne && ligne.references ? ligne.references : []).forEach(ref => {
    (ref.ops || []).forEach(op => {
      if((op.opCode || "?") !== opCode) return;
      out.push({ ref, op, scs: op.scenarios || [] });
    });
  });
  return out;
}

/* ── Le cœur : le gain d'un poste, périmètre commun obligatoire ──────────────
   Un poste peut être servi par plusieurs références (EMAG 1 : 356x26 + 304x28) :
   on additionne référence par référence, chaque delta passant par bilanAnnuel() —
   donc par perimetreCompare() (v4.45). Jamais une soustraction de deux totaux bruts.
   Le cas asymétrique réel (une OP avec prod chiffrable, une sans) sort du calcul,
   il ne devient pas 0 : il est compté dans nonChiffres.

   Renvoie { ligne, opCode, nom, refs, gainActe, gainProjete, coutProd, coutEnCours,
             cibleCPP, chemin, essaiOuvert, nonChiffres, refDominante } */
function gainPoste(ligne, opCode, lignesSeptFons){
  const poste = (postesLigne(ligne, lignesSeptFons) || []).find(p => p.code === opCode)
              || { code: opCode, nom: "", ligne };
  const blocs = scenariosPostes(ligne, opCode);
  const refs = [];
  let gainActe = 0, gainProjete = 0, coutProd = 0, coutEnCours = 0;
  let essaiOuvert = false, nonChiffres = 0;

  blocs.forEach(b => {
    /* la prod d'une OP, c'est D'ABORD la prod réelle (★), l'excel en repli (v4.49.4) */
    const excel = (b.scs || []).find(x => /base excel/i.test(x.name || ""));
    const star  = (b.scs || []).find(x => x.baseline);
    const prodSc = star || excel || null;
    if(!prodSc){ nonChiffres++; return; }

    const tBase = coutsDetail(prodSc, b.op.config, ligne).total;
    if(tBase === null){ nonChiffres++; return; }

    /* le meilleur scénario non-prod chiffrable : le gain ne peut se comparer que si
       l'autre côté de la comparaison est chiffrable aussi (v4.45) */
    let meilleur = null;
    (b.scs || []).forEach(sc => {
      if(prodSc.id === sc.id) return;
      const t = coutsDetail(sc, b.op.config, ligne).total;
      if(t === null) return;
      if(!meilleur || t < meilleur.cout) meilleur = { sc, cout: t };
    });

    /* même formule, même périmètre que le bandeau : bilanAnnuel() applique déjà
       perimetreCompare() et signale les postes exclus. On ne recalcule rien. */
    const an = meilleur ? bilanAnnuel(meilleur.sc, b.op.config, ligne, b.ref, prodSc) : null;
    let gain = null;
    if(an && an.gainAnnuel !== undefined) gain = an.gainAnnuel;

    const serie = !!(meilleur && meilleur.sc.statut === "serie");
    if(gain !== null){
      if(serie) gainActe += gain;
      else      gainProjete += gain;
    }
    coutProd    += tBase;
    coutEnCours += gain !== null && !serie ? meilleur.cout : tBase;

    if((b.scs || []).some(x => (x.essais || []).length)) essaiOuvert = true;

    refs.push({ ref: b.ref, prodSc, meilleur, tBase, gain, serie,
                volume: volumeAnnuel(b.ref, b.op.config), essaiOuvert: (meilleur && (meilleur.sc.essais || []).length) || false });
  });

  /* la référence DOMINANTE = celle du plus gros volume de série : c'est elle qui
     décide du chemin prod → cible affiché sur la tuile. Une tuile multi-références
     n'affiche qu'une seule cible, sinon deux chiffres se contredisent. */
  const dominante = refs.slice().sort((a, b) => (b.volume || 0) - (a.volume || 0))[0];
  const refDominante = dominante ? dominante.ref : null;
  const cible = refDominante ? cibleCPPDe(refDominante) : null;

  let chemin = null;
  if(cible !== null && cible > 0 && coutProd > cible && coutProd > 0){
    chemin = Math.max(0, Math.min(100, ((coutProd - coutEnCours) / (coutProd - cible)) * 100));
  }

  return { ligne, opCode, nom: poste.nom, refs, gainActe, gainProjete, coutProd, coutEnCours,
           cibleCPP: cible, chemin, essaiOuvert, nonChiffres, refDominante };
}

/* la cible CPP d'une référence, normalisée (nombre > 0, sinon « pas de cible ») */
function cibleCPPDe(ref){
  if(!ref || ref.cibleCPP === "" || ref.cibleCPP == null) return null;
  const v = parseFloat(ref.cibleCPP);
  return isNaN(v) || v <= 0 ? null : v;
}

/* ── L'état de la tuile : UNE fonction, jamais une cascade de if dans le HTML ──
   a) gagne      : un gain déjà acté (scénario en série) ;
   b) encours    : un essai existe sur ce poste sans gain acté ;
   c) aChiffrer  : la référence dominante a une cible CPP, mais rien n'est chiffré ;
   d) opportunite: rien de tout cela — le poste est déclaré mais pas travaillé. */
function etatTuile(poste){
  if(!poste) return "opportunite";
  if(poste.gainActe > 0) return "gagne";
  if(poste.essaiOuvert) return "encours";
  if(poste.cibleCPP !== null && poste.cibleCPP > 0) return "aChiffrer";
  return "opportunite";
}
