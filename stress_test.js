/* =============================================================================
   Suivi_optimisation_SPK — jeu de stress
   Base : script fourni par Hermès (revue externe). Corrigé et étendu.

   UTILISATION
     1. ouvrir bilan_economique.html dans le navigateur ;
     2. coller ce fichier entier dans la console (F12) ;
     3. SPK_STRESS.run()            → évaluation SANS TOUCHER à vos données ;
        SPK_STRESS.run({injecter:true}) → injecte le jeu dans l'interface pour l'inspecter
                                          à l'écran (une sauvegarde de secours est faite) ;
        SPK_STRESS.restaurer()      → revient à vos données après une injection.

   CE QUI A CHANGÉ PAR RAPPORT AU SCRIPT D'ORIGINE
   -----------------------------------------------------------------------------
   1. NON DESTRUCTIF PAR DÉFAUT. Le script d'origine écrivait immédiatement dans le
      localStorage réel via saveData(), avec revision:99. Ici, run() évalue tout en
      mémoire et restaure les variables globales dans un finally : rien n'est écrit.
      L'injection reste possible, mais elle est explicite.

   2. LE CAS « VOLUME NÉGATIF » S'EXÉCUTE ENFIN. Le script d'origine faisait
      getActiveReference().ops[1] — or o_stress2 n'est pas le 2e OP de la référence
      active, c'est le seul OP d'une AUTRE référence (r_stress2). ops[1] valait
      undefined, l'accès à .scenarios levait une exception, et le try/catch la
      transformait en « a lancé ». Le test le plus intéressant du jeu n'a donc jamais
      produit de résultat. Il est ici ciblé par identifiant.

   3. RESTAURATION FIDÈLE. La sauvegarde d'origine stockait la clé « activeId », alors
      que loadAll() lit « activeScenarioId » : au retour, le scénario ouvert était perdu.
      Le format écrit ici est exactement celui de saveData().

   4. runTests() RENVOIE BIEN {total, echecs, details} — le script d'origine avait raison
      sur ce point, vérification faite.

   5. COUVERTURE ÉTENDUE aux mécaniques postérieures à la revue : prévision d'usure et
      fusion de fichiers (3.16), fiches de saisie (3.17), aperçu de composition et plans
      d'outil (3.18), protection du quota de stockage (3.19).

   DÉTAILS DU JEU DE DONNÉES QUI NE PIÈGENT RIEN (sans effet, à corriger si utile) :
   les champs « fin » et « programmeCNC » n'existent pas sous ces noms (dateFin/heureFin
   et programme), et usure « neuve »/« usagée » n'est pas une valeur reconnue
   (ok / limite / changer). Ils sont ignorés sans casse.
   ============================================================================= */
(function(){
  "use strict";

  const JEU = {"outil":"SPK Suivi optimisation","format":5,"toolVersion":"stress","revision":99,"exporteLe":"2026-09-03T15:00:00.000Z","exportePar":"stress-test","activeLigneId":"l_stress","activeReferenceId":"r_stress","activeOpId":"o_stress","activeScenarioId":"s_piege1","lignes":[{"id":"l_stress","nom":"STRESS — EMAG 1","coutHoraire":50,"observations":"Ligne de test, scénarios piégeux","references":[{"id":"r_stress","nom":"DV 356x26 RPI (stress)","productionAnnuelle":200000,"ops":[{"id":"o_stress","nom":"OP10","ordre":10,"config":{"limitLabel":"Battement (mm)","limitValue":0.12,"coutRebutActif":true,"coutDisque":14,"cycleSecActif":true,"cycleRefSec":42,"coutMachineActif":true,"partCoupante":50,"cycleDetailActif":true,"piecesActif":true,"volumeActif":true,"forceRatioActif":true},"scenarios":[{"id":"s_piege1","name":"Référence piège (cycle=87,3)","baseline":true,"cycle":87.3,"emag1":true,"limitOverride":false,"validationThreshold":5,"statut":"serie","statutDate":"2026-08-30","outils":[{"id":"t1","numero":"T513.1","correcteur":"G53","description":"Foret carbure monobloc à goujure droite","logements":[{"id":"g1","nom":"Bol","ref":"CNGX 120716 CBN387+TiN","prix":38,"aretes":8,"charniere":75,"vc":"","f":"","tempsCoupe":"","tempsDeplacement":"","suiviTolerance":true},{"id":"g2","nom":"Piste","ref":"CNGX 120716 CBN387+TiN","prix":38,"aretes":8,"charniere":75,"vc":900,"f":0.5,"tempsCoupe":28,"tempsDeplacement":14,"suiviTolerance":true}],"pieces":[{"id":"pd1","nom":"Cale support","ref":"CALE-A","prix":200,"charniere":10000}]}],"essais":[{"id":"e_piege1a","titre":"Essai conforme","date":"2026-08-26","equipe":"Matin","operateur":"Arthur","observations":"RAS","params":{"logements":[{"outilId":"t1","logementId":"g2","outilNumero":"T513.1","logementNom":"Piste","vc":900,"f":0.5,"charniere":75}]},"marposs":{"debut":"","fin":"","releves":[]},"photos":[],"prelevements":[{"id":"p1","piece":50,"batt":"","battD":0.08,"battG":0.09,"logementId":"g2","pointMesure":"Inter"},{"id":"p2","piece":75,"batt":"","battD":0.1,"battG":0.11,"logementId":"g2","pointMesure":"Inter"}]}],"scrapLog":[]},{"id":"s_piege2","name":"Mixte piège (bol=300 piste=700, cycle détaillé incomplet)","baseline":false,"cycle":"","emag1":true,"limitOverride":false,"statut":"essai","outils":[{"id":"t2","numero":"T50013","logements":[{"id":"g3","nom":"Bol","ref":"CNGX 120716 T02020 LKT640","prix":5,"aretes":8,"charniere":150,"vc":300,"f":0.5,"tempsCoupe":"","tempsDeplacement":"","suiviTolerance":true},{"id":"g4","nom":"Piste","ref":"SNGX 120716 T02020 LKT640","prix":5,"aretes":8,"charniere":150,"vc":700,"f":0.5,"tempsCoupe":22,"tempsDeplacement":11,"kappaR":85,"suiviTolerance":true}],"pieces":[]}],"essais":[{"id":"e_piege2a","titre":"Essai 1 — mixte","date":"2026-08-27","equipe":"Matin","operateur":"Matis","params":{"logements":[{"outilId":"t2","logementId":"g3","outilNumero":"T50013","logementNom":"Bol","vc":300,"f":0.5,"charniere":150},{"outilId":"t2","logementId":"g4","outilNumero":"T50013","logementNom":"Piste","vc":700,"f":0.5,"charniere":150}]},"marposs":{"debut":"","fin":"","releves":[]},"photos":[],"prelevements":[{"id":"p1","piece":50,"batt":"","battD":0.07,"battG":0.07,"logementId":"g4","pointMesure":"Inter"},{"id":"p2","piece":100,"batt":"","battD":0.08,"battG":0.08,"logementId":"g4","pointMesure":"Inter"},{"id":"p3","piece":150,"batt":"","battD":0.1,"battG":0.11,"logementId":"g4","pointMesure":"Inter"},{"id":"p4","piece":200,"batt":"","battD":0.15,"battG":0.13,"logementId":"g4","pointMesure":"Inter"}]}],"scrapLog":[{"id":"sc1","date":"2026-08-30","equipe":"Matin","produites":1000,"rebutees":50}]},{"id":"s_piege3","name":"Valeurs aberrantes (arêtes=0, prix=0)","baseline":false,"cycle":"","emag1":false,"limitOverride":false,"statut":"abandonne","statutDate":"2026-08-30","outils":[{"id":"t3","numero":"T00000","logements":[{"id":"g5","nom":"Piste","ref":"INCONNU","prix":0,"aretes":0,"charniere":100,"vc":1000,"f":0.3,"suiviTolerance":true}],"pieces":[]}],"essais":[],"scrapLog":[{"id":"sc2","date":"2026-08-30","equipe":"Matin","produites":100,"rebutees":0}]},{"id":"s_piege4","name":"EMAG1 mal migré (battD/battG vides)","baseline":false,"cycle":75,"emag1":true,"limitOverride":false,"statut":"essai","outils":[{"id":"t4","numero":"T513.1","logements":[{"id":"g6","nom":"Piste","ref":"CNGX 120716 CBN387+TiN","prix":38,"aretes":8,"charniere":75,"vc":900,"f":0.5,"suiviTolerance":true}],"pieces":[]}],"essais":[{"id":"e_piege4a","titre":"Ancien format, juste « batt »","date":"2026-07-15","params":{"logements":[{"outilId":"t4","logementId":"g6","outilNumero":"T513.1","logementNom":"Piste","vc":900,"f":0.5,"charniere":75}]},"marposs":{"debut":"","fin":"","releves":[]},"photos":[],"prelevements":[{"id":"p1","piece":50,"batt":0.08,"battD":"","battG":"","logementId":"g6","pointMesure":"Exter"}]}],"scrapLog":[]},{"id":"s_piege5","name":"Sortie tolérance au milieu (charnière réelle)","baseline":false,"cycle":120,"emag1":true,"limitOverride":false,"statut":"valide","statutDate":"2026-08-29","outils":[{"id":"t5","numero":"T00099","logements":[{"id":"g7","nom":"Piste","ref":"TEST","prix":30,"aretes":8,"charniere":100,"vc":700,"f":0.4,"suiviTolerance":true}],"pieces":[]}],"essais":[{"id":"e_piege5a","titre":"Conforme puis hors puis conforme","date":"2026-08-25","params":{"logements":[{"outilId":"t5","logementId":"g7","outilNumero":"T00099","logementNom":"Piste","vc":700,"f":0.4,"charniere":100}]},"marposs":{"debut":"","fin":"","releves":[]},"photos":[],"prelevements":[{"id":"p1","piece":50,"batt":"","battD":0.08,"battG":0.09,"logementId":"g7","pointMesure":"Inter"},{"id":"p2","piece":100,"batt":"","battD":0.18,"battG":0.2,"logementId":"g7","pointMesure":"Inter"},{"id":"p3","piece":150,"batt":"","battD":0.09,"battG":0.1,"logementId":"g7","pointMesure":"Inter"}]}],"scrapLog":[]},{"id":"s_piege6","name":"Rebut énorme (50 %)","baseline":false,"cycle":80,"emag1":true,"limitOverride":false,"statut":"essai","outils":[{"id":"t6","numero":"T00088","logements":[{"id":"g8","nom":"Piste","ref":"TEST","prix":5,"aretes":8,"charniere":200,"vc":500,"f":0.3,"suiviTolerance":true}],"pieces":[]}],"essais":[{"id":"e_piege6a","titre":"Beaucoup de rebut","date":"2026-08-20","equipe":"Nuit","params":{"logements":[{"outilId":"t6","logementId":"g8","outilNumero":"T00088","logementNom":"Piste","vc":500,"f":0.3,"charniere":200}]},"marposs":{"debut":"","fin":"","releves":[]},"photos":[],"prelevements":[{"id":"p1","piece":100,"batt":"","battD":0.08,"battG":0.08,"logementId":"g8","pointMesure":"Inter"},{"id":"p2","piece":200,"batt":"","battD":0.09,"battG":0.09,"logementId":"g8","pointMesure":"Inter"}]}],"scrapLog":[{"id":"sc3","date":"2026-08-25","equipe":"Matin","produites":100,"rebutees":50},{"id":"sc4","date":"2026-08-26","equipe":"Après-midi","produites":100,"rebutees":50}]}]}]},{"id":"r_stress2","nom":"DV ABERRANT (volume=-5000)","productionAnnuelle":-5000,"ops":[{"id":"o_stress2","nom":"OP10","ordre":10,"config":{"limitLabel":"Battement (mm)","limitValue":0.12,"volumeActif":true,"partCoupante":100},"scenarios":[{"id":"s_volneg","name":"Volume annuel négatif","baseline":true,"cycle":100,"emag1":false,"limitOverride":false,"statut":"etude","outils":[{"id":"t_volneg","numero":"T-VN","logements":[{"id":"g_volneg","nom":"Piste","ref":"X","prix":10,"aretes":8,"charniere":100,"vc":1000,"f":0.5,"suiviTolerance":true}],"pieces":[]}],"essais":[],"scrapLog":[]}]}]}]}],"backlog":[]};

  const CLE_SECOURS = "__stress_backup";

  function estEnvironnementOutil(){
    return typeof lignes !== "undefined" && typeof data !== "undefined" && typeof normalizeScenario === "function";
  }

  /* jeu normalisé, indépendant de l'original : chaque run() repart d'une copie propre */
  function jeuNormalise(){
    const copie = JSON.parse(JSON.stringify(JEU));
    copie.lignes.forEach(l => l.references.forEach(r => r.ops.forEach(o => {
      o.scenarios = (o.scenarios || []).map(normalizeScenario);
      o.config = Object.assign({}, defaultConfig, o.config || {});
    })));
    return copie;
  }

  function ligneDe(arbre, id){ return arbre.lignes.find(l => l.id === id); }
  function refDe(ligne, id){ return ligne.references.find(r => r.id === id); }

  function evaluer(){
    const R = [];
    // une colonne separee pour l'attendu : concatener un objet a une chaine donnait
    // "[object Object]" et effacait le resultat qu'on venait de mesurer
    const T = (label, val, attendu) => R.push({ test: label, résultat: val, attendu: attendu || "" });
    const arbre = jeuNormalise();
    const l = ligneDe(arbre, "l_stress");
    const opPrincipal = refDe(l, "r_stress").ops[0];
    const scenarios = opPrincipal.scenarios;
    const sc = id => scenarios.find(s => s.id === id);

    /* Les fonctions de calcul lisent la config globale : on la bascule le temps de
       l'évaluation, et on la remet dans le finally de run(). */
    config = opPrincipal.config;
    data = scenarios;
    activeId = "s_piege1";

    T("cycle de la baseline (87,3 injecté)", (() => { recomputeCycles(); return sc("s_piege1").cycle; })(),
      "100 — la référence vaut 100 par définition, le champ n'est pas éditable sur elle");
    T("logementCycle(baseline)", (logementCycle(sc("s_piege1")) || {}).nom || "null");
    T("cycleDetailStatus(s_piege2) — 1 logement renseigné sur 2", cycleDetailStatus(sc("s_piege2"), opPrincipal.config));
    T("coutsDetail(baseline)", coutsDetail(sc("s_piege1"), opPrincipal.config, l));
    T("coutsDetail(arêtes=0, prix=0)", coutsDetail(sc("s_piege3"), opPrincipal.config, l));
    T("coutsDetail(rebut 50 %)", coutsDetail(sc("s_piege6"), opPrincipal.config, l));
    T("seuilBascule(scénario perdant)", seuilBascule(sc("s_piege2")));
    T("charnièreReelle(sortie de tolérance au milieu)", charniereReelle(sc("s_piege5"), "g7"),
      "moyenne 50 — on ne peut pas revendiquer 150 quand la cote est sortie à 100");
    T("mesurePrincipale(ancien format EMAG 1, « batt » seul)",
      typeof mesurePrincipale === "function" ? mesurePrincipale(sc("s_piege4"), sc("s_piege4").essais[0].prelevements[0]) : "fonction absente (< v3.16)");

    /* ---- volume négatif : ciblé par identifiant, pas par ops[1] ---- */
    const refVN = refDe(l, "r_stress2");
    const opVN = refVN.ops[0];
    const memoRef = typeof activeReferenceId !== "undefined" ? activeReferenceId : null;
    activeReferenceId = "r_stress2";
    lignes = arbre.lignes; activeLigneId = "l_stress"; activeOpId = "o_stress2";
    config = opVN.config; data = opVN.scenarios;
    T("bilanAnnuel(volume = -5000)", bilanAnnuel(opVN.scenarios[0]));
    T("volumeAnnuel(volume = -5000)", volumeAnnuel());
    activeReferenceId = memoRef;

    /* ---- mécaniques postérieures à la revue ---- */
    config = opPrincipal.config; data = scenarios;
    if(typeof previsionUsure === "function"){
      const p2 = sc("s_piege2"), p5 = sc("s_piege5");
      T("prévision d'usure — dépassement déjà constaté (pièce 200)", previsionUsure(p2, p2.essais[0], "g4"));
      T("prévision d'usure — 3 points seulement", previsionUsure(p5, p5.essais[0], "g7") === null
        ? "null (garde-fou : 4 points minimum)" : previsionUsure(p5, p5.essais[0], "g7"));
    }
    if(typeof dispersionEquipeHTML === "function"){
      T("dispersion par équipe", dispersionEquipeHTML() ? "affichée" : "masquée (moins de 2 équipes renseignées)");
    }
    if(typeof fusionnerLignes === "function"){
      const sansHorodatage = scenarios.flatMap(s => s.essais || []).filter(e => !e.modifieLe).length;
      T("essais sans horodatage (partiraient en conflit à la fusion)", sansHorodatage);
    }
    if(typeof apercuLogementHTML === "function"){
      const s3 = sc("s_piege3"), o3 = s3.outils[0];
      const tuile = apercuLogementHTML(s3, o3, o3.logements[0], "#000", 0);
      T("aperçu — logement à 0 arête",
        /Coût non calculable/.test(tuile) ? "signalé « Coût non calculable »" : "AUCUNE EXPLICATION (régression)");
    }
    if(typeof inventairePoids === "function"){
      lignes = arbre.lignes;
      T("inventaire du poids (pièces jointes intégrées au fichier)",
        inventairePoids().length ? inventairePoids().map(i => i.quoi + " — " + Math.round(i.octets/1024) + " ko") : "aucune");
    }
    return R;
  }

  const SPK_STRESS = {
    run(options){
      options = options || {};
      if(!estEnvironnementOutil()){
        console.error("Pas l'environnement de l'outil — ouvrez bilan_economique.html d'abord.");
        return;
      }
      const memo = {
        lignes, backlog, revision, config, data,
        activeLigneId, activeReferenceId, activeOpId, activeId
      };
      let resultats;
      try {
        resultats = evaluer();
      } finally {
        if(!options.injecter){
          // rien n'a été écrit : on remet simplement les variables en place
          lignes = memo.lignes; backlog = memo.backlog; revision = memo.revision;
          config = memo.config; data = memo.data;
          activeLigneId = memo.activeLigneId; activeReferenceId = memo.activeReferenceId;
          activeOpId = memo.activeOpId; activeId = memo.activeId;
          if(typeof render === "function") render();
        }
      }

      console.log("%c=== JEU DE STRESS — RÉSULTATS ===", "font-weight:bold");
      const enTexte = v => v === null ? "null" : (typeof v === "object" ? JSON.stringify(v) : String(v));
      console.table(resultats.map(r => ({ test: r.test, résultat: enTexte(r.résultat), attendu: r.attendu })));

      if(typeof runTests === "function"){
        const t = runTests();
        console.log("Moteur de tests intégré : " + (t.total - t.echecs) + "/" + t.total + (t.echecs ? " — " + t.echecs + " ÉCHEC(S)" : " — tout est vert"));
        t.details.filter(x => !x.pass).forEach(x => console.warn("  ✗", x.nom, "— reçu :", x.recu, "· attendu :", x.attendu));
        const ov = document.getElementById("testResults"); if(ov) ov.remove();
      }

      if(options.injecter) this.injecter();
      else console.log("Vos données n'ont pas été touchées. SPK_STRESS.run({injecter:true}) pour voir le jeu à l'écran.");
      return resultats;
    },

    injecter(){
      if(!estEnvironnementOutil()) return;
      if(!confirm("Injecter le jeu de stress DANS l'interface ?\n\nVos données actuelles seront remplacées à l'écran et dans ce navigateur. Une sauvegarde de secours est créée : SPK_STRESS.restaurer() les remet en place.\n\nExportez d'abord votre suivi si vous tenez à cette précaution supplémentaire.")) return;
      try {
        // format identique à celui de saveData() — activeScenarioId, pas activeId :
        // c'est cette clé que loadAll() relit, sinon l'onglet ouvert est perdu au retour
        localStorage.setItem(CLE_SECOURS, JSON.stringify({
          lignes, backlog, revision, activeLigneId, activeReferenceId, activeOpId, activeScenarioId: activeId
        }));
      } catch(e){
        alert("Sauvegarde de secours impossible (" + e.message + ") — injection annulée.");
        return;
      }
      const arbre = jeuNormalise();
      lignes = arbre.lignes; backlog = arbre.backlog; revision = arbre.revision;
      activeLigneId = arbre.activeLigneId; activeReferenceId = arbre.activeReferenceId; activeOpId = arbre.activeOpId;
      const op = getActiveOp();
      data = op ? op.scenarios : [];
      config = op ? op.config : Object.assign({}, defaultConfig);
      activeId = arbre.activeScenarioId;
      if(!data.find(s => s.baseline) && data.length) data[0].baseline = true;
      recomputeCycles(); saveData(); render();
      console.log("%cJeu injecté. SPK_STRESS.restaurer() pour revenir à vos données.", "color:#b45309;font-weight:bold");
    },

    restaurer(){
      let brut = null;
      try { brut = localStorage.getItem(CLE_SECOURS); } catch(e){}
      if(!brut){ console.error("Aucune sauvegarde de secours trouvée."); return; }
      try {
        localStorage.setItem("spk_suivi_optimisation_v1", brut);
        localStorage.removeItem(CLE_SECOURS);
        console.log("Données restaurées — rechargement…");
        location.reload();
      } catch(e){ console.error("Restauration impossible :", e); }
    }
  };

  window.SPK_STRESS = SPK_STRESS;
  console.log("%cSPK_STRESS prêt.", "font-weight:bold",
    "\n  SPK_STRESS.run()                → évalue sans toucher à vos données" +
    "\n  SPK_STRESS.run({injecter:true}) → injecte le jeu dans l'interface" +
    "\n  SPK_STRESS.restaurer()          → revient à vos données");
})();
