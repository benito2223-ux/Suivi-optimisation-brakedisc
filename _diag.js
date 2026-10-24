
globalThis.__monDiag = function(A){
  const uid = p => p + Math.random().toString(36).slice(2);
  const tAr = uid("t"), gAr = uid("g"), eAr = uid("e"), pAr = uid("p");
  const sArret = A.normalizeScenario({ id: uid("s"), name: "Candidat arrêté", statut: "essai",
    outils: [ { id: tAr, numero: "T5", logements: [ { id: gAr, nom: "D1", codeArticle: "IM02 000 004", prix: 30, aretes: 8, charniere: 100 } ] } ],
    essais: [ { id: eAr, titre: "Essai cassé", date: "2026-10-18", cloture: { motif: "casse_insert" },
      params: { logements: [ { outilId: tAr, logementId: gAr, outilNumero: "T5", logementNom: "D1", vc: 200, f: 0.3, charniere: 100, suivi: true } ] },
      prelevements: [ { id: pAr, piece: 40, batt: "0.050", logementId: gAr } ] } ], scrapLog: [] });
  const ev = A.scenarioEchec ? A.scenarioEchec(sArret) : "PAS EXPORTEE";
  const st = A.scenarioStats ? (function(){ try { return A.scenarioStats(sArret); } catch(e){ return "ERR " + e.message; } })() : "PAS EXPORTEE";
  console.log("scenarioEchec:", JSON.stringify(ev));
  try { console.log("essaiStats.status:", st.status, "| logementProgress:", JSON.stringify(st.logementProgress)); } catch(e){ console.log("st:", JSON.stringify(st)); }
};
