# -*- coding: utf-8 -*-
# Tour 107 — 4.129.0, LOT 5 (hygiène) — patch B : le test de sécurité à l'import
# Injecté à la fin de runTests (avant le recalcul v4.66.0 du return) :
# un payload hostile est posé dans CHAQUE champ texte d'un suivi complet,
# le suivi passe par le VRAI chemin d'import (preparerImportDepuis +
# appliquerImport « remplace »), puis les rendus tournent et CHAQUE innerHTML
# écrit (piégé par un accessor) et chaque string rendue est scannée :
# la forme crue « <img src=x onerror= » ne doit exister nulle part.
# Règle du tour (Tours 82/104/105) : écrit depuis un fichier python UTF-8
# (pas d'heredoc), aucun backslash littéral dans le JS ci-dessous.
import io

F = "bilan_economique.html"
src = io.open(F, encoding="utf-8").read()

ANCRE = "  /* v4.66.0 — on RECALCULE le nombre d'échecs au moment du retour."
n = src.count(ANCRE)
assert n == 1, "ancre v4.66.0 : %d occurrences (attendu 1)" % n

BLOC = """  /* v4.129.0 — LOT 5 : LA SÉCURITÉ À L'IMPORT.
     Environ 90 innerHTML de l'outil sont alimentés par des données importées.
     Le pari historique : le JSON reçu n'est jamais du HTML, parce que chaque
     interpolation passe par escapeAttr. Ce test ne croit rien : il pose le
     MÊME payload hostile (« <img src=x onerror= ») dans chaque champ texte
     d'un suivi complet, le fait passer par le vrai chemin d'un import
     (preparerImportDepuis, puis appliquerImport « remplace »), puis appelle
     les rendus et scanne CHAQUE innerHTML écrit (le stub getElementById est
     enveloppé pendant le test) et chaque string rendue : la forme crue ne
     doit exister nulle part — et le payload échappé doit être VU au moins
     une fois, sinon la porte serait aveugle (un rendu vide passe au vert).
     saveData est neutralisé pendant le test (la promesse du bloc : aucune
     sauvegarne n'est déclenchée) ; l'état est restauré en finally.
     Contre-regard du tour : amputer l'échappement de escapeAttr doit faire
     tomber CE test. */
  {
    const sauves = {
      lignes, projets, responsables, livraisons, backlog, data, config,
      activeLigneId, activeReferenceId, activeOpId, activeId, activeProjetId,
      revision, specsUsine, synchroNote, catalogue, conso2025, consoReelle,
      planSource, consoSemaines, planReglages, derniereVisite, importEnAttente,
      unexported: (typeof unexported !== "undefined" ? unexported : null)
    };
    const saveAvant = saveData;
    const gidAvant = document.getElementById;
    try {
      saveData = function(){}; /* promesse du bloc tests : aucune sauvegarde */

      /* --- le suivi fabrique : le plus complet possible (deux scénarios,
             un essai avec prélèvement, un projet, une livraison, le catalogue) --- */
      lignes = [ normalizeLigne({ id:"lSec", nom:"EMAG 1", references:[
        normalizeReference({ id:"rSec", nom:"DV 356x26 RPI", productionAnnuelle:"200000", cibleCPP:"0.30", ops:[
          { id:"oSec", nom:"OP10", ordre:10, config: Object.assign({}, defaultConfig), scenarios:[
            normalizeScenario({ id:"sSecBase", name:"Base KY3500", baseline:true, statut:"serie",
              outils:[ { id:"uSec", numero:"T543 D1", logements:[ { id:"lgSec", nom:"Plaquette", mabec:"Z000 519 285", prix:11.87, aretes:6, charniere:30 } ] } ],
              essais:[] }),
            normalizeScenario({ id:"sSecEssai", name:"Essai SL500", baseline:false, statut:"essai",
              outils:[ { id:"uSec2", numero:"T544 D2", logements:[ { id:"lgSec2", nom:"Bol", prix:9, aretes:8, charniere:100 } ] } ],
              essais:[ { id:"eSec1", titre:"Essai 1", date:"2026-10-20", equipe:"Matin", operateur:"Matis", redigePar:"Matis",
                observations:"tenue correcte", prelevements:[ { id:"pSec1", grandeur:"battement", valeur:0.05, conforme:true } ] } ] })
          ] } ] }) ] }) ];
      projets = [ normalizeProjet({ nom:"2026/2027", tags:[ { ligneId:"lSec", referenceId:"rSec", opId:"oSec", scenarioId:"sSecBase" } ] }) ];
      responsables = [];
      backlog = [];
      livraisons = [ { id:"lvSec", nom:"Livraison de test", date:"2026-10-29" } ];
      catalogue = [ normalizeArticleCat({ mabec:"Z000 519 285", article:"137 021", prix:11.87 }) ];
      specsUsine = normaliserSpecsUsine(null);
      synchroNote = null; derniereVisite = null; revision = 500;
      activeLigneId = lignes[0].id; activeReferenceId = lignes[0].references[0].id;
      activeOpId = lignes[0].references[0].ops[0].id;
      data = lignes[0].references[0].ops[0].scenarios;
      activeId = data[0].id; activeProjetId = projets[0].id;

      /* --- infecter : la liste des CLÉS TEXTE de saisie (jamais les ids,
             dates, nombres ou statuts — on infecte ce qu'un opérateur tape) --- */
      const PAYLOAD = '<img src=x onerror="window.__xssPwned=1">';
      const CLES = ["nom","ref","article","commentaire","note","notes","observations",
        "operateur","equipe","redigePar","logement","numero","libelle","mabec","iso",
        "source","machine","titre","synchroNote","fournisseur","designation","categorie",
        "grandeur","piece","name"];
      const infecter = (o) => {
        if(Array.isArray(o)) return o.map(infecter);
        if(o && typeof o === "object"){
          const c = {};
          for(const k of Object.keys(o)){
            c[k] = (typeof o[k] === "string" && CLES.indexOf(k) !== -1) ? PAYLOAD : infecter(o[k]);
          }
          return c;
        }
        return o;
      };
      const arbre = JSON.parse(payloadSuivi());
      const infecte = infecter(arbre);
      const nEssais = cloudCompterEssais(infecte.lignes || []);
      ok("sécurité import : l'infection a touché les champs texte du suivi (payload présent, structure intacte)",
         [JSON.stringify(infecte).indexOf("<img src=x onerror=") >= 0, nEssais > 0], [true, true]);

      /* --- le vrai chemin d'import --- */
      const prep = preparerImportDepuis(infecte);
      ok("sécurité import : preparerImportDepuis accepte le suivi infecté et garde tous les essais",
         [prep !== null, cloudCompterEssais(prep ? prep.nouvellesLignes : [])], [true, nEssais]);
      importEnAttente = Object.assign({ parsed: infecte }, prep);
      appliquerImport("remplace");

      /* --- le piège à innerHTML : tout ce que les rendus écrivent est capté --- */
      const captes = [];
      document.getElementById = function(id){
        const el = gidAvant.call(document, id);
        if(el && !el.__spkPiegeSecu){
          let val = el.innerHTML;
          try{
            Object.defineProperty(el, "innerHTML", { configurable:true,
              get(){ return val; },
              set(v){ val = String(v == null ? "" : v); captes.push(val); } });
            el.__spkPiegeSecu = true;
          }catch(e){}
        }
        return el;
      };

      /* --- la batterie de rendus : chaque exception est un échec du test --- */
      const plantes = [];
      const tenter = (nomFn, fn) => { try{ fn(); }catch(e){ plantes.push(nomFn + " : " + e.message); } };
      const pousser = (nomFn, fn) => { try{ const v = fn(); if(v) captes.push(String(v)); }catch(e){ plantes.push(nomFn + " : " + e.message); } };
      tenter("render", () => render());
      tenter("renderAccueil", () => renderAccueil());
      tenter("renderDashboard", () => renderDashboard());
      tenter("renderHistoryPanel", () => renderHistoryPanel());
      tenter("renderBacklog", () => renderBacklog());
      tenter("renderCatalogue", () => renderCatalogue());
      tenter("renderPlan", () => renderPlan());
      tenter("renderSimul", () => renderSimul());
      tenter("renderVueCpp", () => renderVueCpp());
      tenter("renderCarte", () => renderCarte());
      tenter("renderReprise", () => renderReprise());
      tenter("rendreRecherche", () => rendreRecherche("a"));
      pousser("planHTML", () => planHTML());
      pousser("simulHTML", () => simulHTML());
      pousser("missionA4HTML", () => missionA4HTML());
      pousser("boussoleHTML", () => boussoleHTML());
      pousser("campagneCeQuiAttendHTML", () => campagneCeQuiAttendHTML());
      /* planLignes, planRecapGains, planChronologieEssais, dossierVisite et matisRecap
         rendent des STRUCTURES, pas du HTML : on les exécute (aucune exception tolérée)
         sans pousser leur sérialisation — une string JSON de données infectées porte
         TOUJOURS le payload cru, et ce n'est pas du HTML rendu. */
      tenter("planLignes", () => planLignes());
      tenter("planRecapGains", () => planRecapGains());
      tenter("planChronologieEssais", () => planChronologieEssais());
      pousser("livraisonImpressionHTML", () => livraisonImpressionHTML(livraisons[0]));
      tenter("dossierVisite", () => dossierVisite(""));
      tenter("matisRecap", () => matisRecap([]));

      ok("sécurité import : tous les rendus tournent sur un suivi infecté (aucune exception)",
         plantes, []);
      const crus = captes.filter(h => h.indexOf("<img src=x onerror=") !== -1);
      const echappes = captes.filter(h => h.indexOf("&lt;img src=x onerror=") !== -1);
      ok("sécurité import : AUCUN innerHTML ni rendu n'expose le payload cru (escapeAttr tient partout)",
         [crus.length, crus.slice(0, 2)], [0, []]);
      ok("sécurité import : le payload a bien TRAVERSÉ les rendus (la porte n'est pas aveugle)",
         [captes.length >= 10, echappes.length >= 1], [true, true]);
      ok("sécurité import : la structure survit à l'import infecté (essais comptés inchangés)",
         cloudCompterEssais(lignes), nEssais);
    } finally {
      document.getElementById = gidAvant;
      saveData = saveAvant;
      lignes = sauves.lignes; projets = sauves.projets; responsables = sauves.responsables;
      livraisons = sauves.livraisons; backlog = sauves.backlog; data = sauves.data;
      config = sauves.config; activeLigneId = sauves.activeLigneId;
      activeReferenceId = sauves.activeReferenceId; activeOpId = sauves.activeOpId;
      activeId = sauves.activeId; activeProjetId = sauves.activeProjetId;
      revision = sauves.revision; specsUsine = sauves.specsUsine;
      synchroNote = sauves.synchroNote; catalogue = sauves.catalogue;
      conso2025 = sauves.conso2025; consoReelle = sauves.consoReelle;
      planSource = sauves.planSource; consoSemaines = sauves.consoSemaines;
      planReglages = sauves.planReglages; derniereVisite = sauves.derniereVisite;
      importEnAttente = sauves.importEnAttente;
      unexported = sauves.unexported;
    }
  }

"""

src = src.replace(ANCRE, BLOC + ANCRE)
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch B appliqué : test de sécurité à l'import inséré avant le recalcul v4.66.0.")
