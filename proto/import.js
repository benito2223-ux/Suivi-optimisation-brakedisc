/* ============================================================================
   PROTO — LA PROJECTION
   Reprend un export de l'ancienne version (format 5, 6, 7 ou 8) et le projette
   vers le modèle du proto. Ce n'est PAS une ressaisie : tout ce qui est lu est
   conservé tel quel, et ce qui est abandonné est compté et nommé.

   Fonction PURE : elle ne touche ni au DOM, ni au disque, ni au réseau. Elle
   prend un objet déjà désérialisé et renvoie un objet. C'est ce qui permet de la
   tester sur les vrais exports du site, en Node, sans navigateur.

   ── ce que la projection garde, et pourquoi ──────────────────────────────────
     prix, arêtes, charnière   → le CPP plaquettes, le driver (cahier §2)
     charnière d'un essai      → le CPP RÉELLEMENT obtenu (cppEssai)
     cibleCPP de la référence  → la cible du site, colonne I du classeur
     prelevements              → la preuve de conformité
     statut "serie"            → ce qui est réellement.acté en production
     plan, photos, marposs,
     scrapLog, backlog         → abandonnés : aucun ne nourrit une décision
                                 d'outillage

   ── pourquoi c'est raisonnable ───────────────────────────────────────────────
   Sur l'export réel du site, ces cinq champs abandonnés pèsent 3,2 Mo sur
   3,27 Mo. Après projection : 56 Ko. Les 135 logements et les 5 essais sont
   intacts. On ne perd pas un chiffre de décision en jetant l'image.
   ========================================================================== */

const IMPORT_VERSION = "1.0";

/* Les champs qu'on prend d'un objet, ou null si on ne prend rien.
   `garder` est plus sûr que lister ce qu'on jette : un champ ajouté par une
   version future de l'app ne peut pas se glisser dans la projection. */
function projeter(source) {
  const vide = {
    ok: false, lignes: [], rapport: null,
    erreur: "Ce fichier n'est pas un export du suivi d'optimisation."
  };
  if (!source || typeof source !== "object") return vide;

  const racines = racinesLignes(source);
  if (!racines) return vide;

  const r = {
    format: source.format != null ? source.format : null,
    toolVersion: source.toolVersion || source.version || null,
    exporteLe: source.exporteLe || null,
    exportePar: source.exportePar || null,
    lignes: 0, references: 0, ops: 0, scenarios: 0,
    essais: 0, prelevements: 0, logements: 0,
    scenariosChiffrables: 0,
    essaisChiffrables: 0,
    scenariosCibles: 0,
    sansPrix: 0, sansAretes: 0, sansCharniere: 0,
    prelevementsSansBatt: 0,
    abandons: ["plans de porte-outil", "photos", "relevés Marposs", "journal de rebut"],
    avertissements: []
  };

  const lignes = [];
  racines.forEach(lBrut => {
    const ligne = {
      id: lBrut.id || ("li" + (lignes.length + 1)),
      nom: lBrut.nom || "Ligne sans nom",
      refs: []
    };
    (lBrut.references || []).forEach(refBrut => {
      const ref = {
        id: refBrut.id || ("re" + (ligne.refs.length + 1)),
        nom: refBrut.nom || "Référence sans nom",
        cibleCPP: cibleOuVide(refBrut.cibleCPP),
        productionAnnuelle: refBrut.productionAnnuelle || "",
        ops: []
      };
      if (parseFloat(ref.cibleCPP) > 0) r.scenariosCibles++;
      r.references++;
      (refBrut.ops || []).forEach(opBrut => {
        const op = {
          id: opBrut.id || ("op" + (ref.ops.length + 1)),
          nom: opBrut.nom || "OP",
          ordre: opBrut.ordre != null ? opBrut.ordre : null,
          code: opBrut.code || codeDeOp(opBrut),
          scs: []
        };
        r.ops++;
        (opBrut.scenarios || []).forEach(scBrut => {
          const sc = {
            id: scBrut.id || ("sc" + (op.scs.length + 1)),
            name: scBrut.name || "Scénario",
            baseline: scBrut.baseline === true,
            statut: scBrut.statut || "",
            validationThreshold: scBrut.validationThreshold || 5,
            battActif: scBrut.battActif,
            limitOverride: scBrut.limitOverride,
            limitValue: scBrut.limitValue,
            emag1: scBrut.emag1,
            outils: [],
            essais: []
          };
          r.scenarios++;
          (scBrut.outils || []).forEach(oBrut => {
            sc.outils.push({
              id: oBrut.id || "",
              numero: oBrut.numero || "",
              description: oBrut.description || "",
              correcteur: oBrut.correcteur || "",
              /* `plan` est délibérément absent : c'est 320 à 370 Ko de géométrie
                 par outil, et pas un chiffre. */
              logements: (oBrut.logements || []).map(lBrut => {
                r.logements++;
                const rempli = trioRempli(lBrut);
                if (!rempli.prix) r.sansPrix++;
                if (!rempli.aretes) r.sansAretes++;
                if (!rempli.charniere) r.sansCharniere++;
                return {
                  id: lBrut.id || "",
                  nom: lBrut.nom || "Logement",
                  ref: lBrut.ref || "",
                  codeArticle: lBrut.codeArticle || "",
                  prix: lBrut.prix != null ? lBrut.prix : "",
                  aretes: lBrut.aretes != null ? lBrut.aretes : "",
                  charniere: lBrut.charniere != null ? lBrut.charniere : "",
                  vc: lBrut.vc != null ? lBrut.vc : "",
                  f: lBrut.f != null ? lBrut.f : ""
                };
              })
            });
          });
          (scBrut.essais || []).forEach(eBrut => {
            const essai = {
              id: eBrut.id || "",
              titre: eBrut.titre || "Essai",
              date: eBrut.date || "",
              operateur: eBrut.operateur || "",
              equipe: eBrut.equipe || "",
              but: eBrut.but || "",
              observations: eBrut.observations || "",
              cloture: eBrut.cloture || null,
              params: { logements: (eBrut.params && eBrut.params.logements) || [] },
              prelevements: []
            };
            r.essais++;
            (eBrut.prelevements || []).forEach(pBrut => {
              r.prelevements++;
              if (isNaN(parseFloat(pBrut.batt)) && isNaN(parseFloat(pBrut.battD))
                  && isNaN(parseFloat(pBrut.battG))) r.prelevementsSansBatt++;
              essai.prelevements.push({
                id: pBrut.id || "",
                piece: pBrut.piece != null ? pBrut.piece : "",
                batt: pBrut.batt != null ? pBrut.batt : "",
                battD: pBrut.battD != null ? pBrut.battD : "",
                battG: pBrut.battG != null ? pBrut.battG : "",
                logementId: pBrut.logementId || "",
                usure: pBrut.usure != null ? pBrut.usure : "",
                pointMesure: pBrut.pointMesure || ""
              });
            });
            sc.essais.push(essai);
          });
          op.scs.push(sc);
        });
        ref.ops.push(op);
      });
      ligne.refs.push(ref);
    });
    lignes.push(ligne);
  });

  r.lignes = lignes.length;
  if (!r.lignes) return vide;

  /* Les deux mesures de qualité d'un import, calculées par le NOYAU et pas
     ici : une projection ne se juge pas elle-même. Elles sont recalculées par
     l'appelant dès que les lignes sont en place. */
  if (!r.essais) {
    r.avertissements.push(
      "Aucun essai dans cet export : les écrans de preuve et de décision resteront vides.");
  }
  if (!r.scenariosCibles) {
    r.avertissements.push(
      "Aucune cible CPP de site : les distances vers la cible ne pourront pas s'afficher.");
  }
  if (r.sansPrix || r.sansAretes || r.sansCharniere) {
    r.avertissements.push(
      (r.sansPrix + r.sansAretes + r.sansCharniere)
      + " logement(s) incomplet(s) sur le trio prix / arêtes / charnière : "
      + "ils resteront non chiffrables, et c'est dit à l'écran.");
  }
  if (r.prelevementsSansBatt) {
    r.avertissements.push(
      r.prelevementsSansBatt + " prélèvement(s) sans battement ni côté D/G : "
      + "ils ne montreront aucune conformité.");
  }
  return { ok: true, lignes: lignes, rapport: r, erreur: null };
}

/* Les racines acceptées. Format 5/7/8 : `lignes` à la racine.
   Format 6 : les lignes sont portées par des projets — on les aplatit. */
function racinesLignes(source) {
  if (Array.isArray(source.lignes) && source.lignes.length) return source.lignes;
  if (Array.isArray(source.projets) && source.projets.length
      && Array.isArray(source.projets[0].lignes)) {
    const plat = [];
    source.projets.forEach(pj => (pj.lignes || []).forEach(l => plat.push(l)));
    return plat.length ? plat : null;
  }
  return null;
}

function cibleOuVide(v) {
  return (v === "" || v === null || v === undefined) ? "" : v;
}

/* Le libellé court d'une opération. L'export ne porte pas `code` : on le
   reconstruit depuis `ordre`, et on retombe sur le nom si `ordre` manque.
   Un `code` déjà présent dans le fichier n'est jamais écrasé — c'est une donnée
   saisie, pas une valeur dérivée. */
function codeDeOp(op) {
  if (op.code) return op.code;
  if (op.ordre != null && !isNaN(parseFloat(op.ordre))) return "OP" + parseFloat(op.ordre);
  const m = /OP\s*0*(\d+)/i.exec(op.nom || "");
  return m ? "OP" + parseInt(m[1], 10) : (op.nom || "OP");
}

/* Le trio prix / arêtes / charnière est-il saisi, membre par membre ?
   ATTENTION à ne pas inverser le sens : le premier jet de cette fonction
   s'appelait `manqueDe` et renvoyait en réalité « la valeur est là ». Les
   compteurs sansPrix / sansAretes / sansCharniere comptaient donc exactement
   l'inverse de ce qu'ils annoncent, et aucun test sur données réelles ne les
   avait remarkés — parce que les exports du site ont le trio complet. Une
   fonction qui compte le contraire de ce qu'elle dit est pire qu'une fonction
   absente : elle donne un faux sentiment de couverture. */
function trioRempli(l) {
  return {
    prix: parseFloat(l.prix) > 0,
    aretes: parseFloat(l.aretes) > 0,
    charniere: parseFloat(l.charniere) > 0
  };
}

/* Le poids de l'import, mesuré SANS dépendre d'un environnement : c'est la
   taille de ce que la projection produit, comparée à celle du fichier lu.
   Une régression ici (un `plan` qui se glisse) se voit immédiatement. */
function poids(jsonSource, projete) {
  let avant = 0, apres = 0;
  try { avant = JSON.stringify(jsonSource).length; } catch (e) { avant = 0; }
  try { apres = JSON.stringify(projete).length; } catch (e) { apres = 0; }
  return {
    avant: avant,
    apres: apres,
    ratio: avant ? Math.round((apres / avant) * 1000) / 1000 : null
  };
}
