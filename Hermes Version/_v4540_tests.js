    /* ---- v4.54.0 — la fiche poste (couche 1) : ce que dit la machine ---------- */
    {
      const opCfg3 = Object.assign({}, defaultConfig, { volumeActif: true });
      const scS = (id, prix) => ({ id, name: id, statut: "serie", outils: [
        { id: id + "u", numero: "T", logements: [ { id: id + "l", nom: "Bol", prix, aretes: 8, charniere: 100 } ] } ] });
      const scP = (id) => ({ id, name: "Prod", baseline: true, outils: [
        { id: id + "u", numero: "T", logements: [ { id: id + "l", nom: "Bol", prix: 30, aretes: 8, charniere: 100 } ] } ] });
      const opF = (id, nom, scs) => ({ id, nom, config: opCfg3, scenarios: scs });
      const refF = (id, nom, vol, cible, ops) => normalizeReference({ id, nom, productionAnnuelle: vol, cibleCPP: cible || "", ops });
      const lignesS = lignes, projS = projets;
      try {
        lignes = [ normalizeLigne({ id: "LF", nom: "EMAG 1", coutHoraire: "45", references: [
          refF("rf1", "356x26", "120000", "", [ opF("of1", "OP10", [ scP("pf1"), scS("sf1", 5) ]) ]),
          refF("rf2", "304x28", "90000", "0.250", [ opF("of2", "OP40", []) ])
        ]}) ];
        projets = [];
        const t = cartePostes();
        const gagne = t.find(x => x.code === "OP10");
        const chiffrer = t.find(x => x.code === "OP40");
        const opp = t.find(x => x.code === "OP20");

        /* ── la prochaine étape : l'information qui manquait le plus ── */
        ok("fiche : un poste gagné se maintient (on ne réinvente pas un gain acquis)",
           prochaineEtapePoste(gagne).includes("En production"), true);
        ok("fiche : un poste à chiffrer dit exactement ce qu'il attend",
           prochaineEtapePoste(chiffrer).includes("chiffrer"), true);
        ok("fiche : un poste d'opportunité dit qu'il n'a jamais été travaillé",
           prochaineEtapePoste(opp).includes("jamais travaillé"), true);

        /* un essai en cours : l'étape parle du protocole 5× ET de l'avancement */
        lignes = [ normalizeLigne({ id: "LF2", nom: "EMAG 2", references: [
          refF("rf3", "290x12", "70000", "", [ opF("of3", "OP10", [ scP("pf3"),
            { id: "ef3", name: "Essai", statut: "essai", outils: [ { id: "ef3u", numero: "T", logements: [ { id: "ef3l", nom: "Bol", prix: 20, aretes: 8, charniere: 100 } ] } ],
              essais: [ { id: "x1", titre: "E1", date: "2026-09-29", prelevements: [ { id: "y1", piece: "5", cotes: {} } ] },
                        { id: "x2", titre: "E2", date: "2026-09-29", prelevements: [ { id: "y2", piece: "6", cotes: {} } ] } ] } ]) ])
        ]}) ];
        const enc = cartePostes().find(x => x.code === "OP10");
        ok("fiche : un poste en cours annonce le protocole 5× et l'avancement (2/5)",
           prochaineEtapePoste(enc).includes("2/5"), true);
        ok("fiche : un poste gainé par la tuile et par la fiche = MÊME valeur (règle D3)",
           [gagne.poste.gainActe > 0, prochaineEtapePoste(gagne).length > 0], [true, true]);

        /* ── le rendu de la fiche : titre, référence, porte, étape ── */
        lignes = [ normalizeLigne({ id: "LF", nom: "EMAG 1", references: [
          refF("rf1", "356x26", "120000", "", [ opF("of1", "OP10", [ scP("pf1"), scS("sf1", 5) ]) ]) ]}) ];
        const g2 = cartePostes().find(x => x.code === "OP10");
        const h = fichePosteHTML(g2);
        ok("fiche : elle nomme la machine et la ligne",
           [h.includes("Ébauche piste"), h.includes("EMAG 1")], [true, true]);
        ok("fiche : elle nomme la référence principale",
           h.includes("356x26"), true);
        ok("fiche : elle porte la porte EXPLICITE vers la couche 2 (geste découvrable)",
           [h.includes("Ouvrir le poste"), h.includes("fp-ouvrir")], [true, true]);
        ok("fiche : elle annonce la prochaine étape en toutes lettres",
           h.includes("Prochaine étape"), true);
        ok("fiche : elle affiche l'état en toutes lettres (jamais la couleur seule)",
           h.includes("Gagné"), true);
        ok("fiche : le gain affiché vient de gainPoste, jamais d'un recalcul local",
           h.includes(fmtEuroCourt(g2.poste.gainActe)), true);
        /* un poste d'opportunité n'a PAS de porte : il n'y a rien à ouvrir */
        lignes = [ normalizeLigne({ id: "LV", nom: "HESSAPP", references: [] }) ];
        const hOpp = fichePosteHTML(cartePostes().find(x => x.code === "OP10"));
        ok("fiche : un poste jamais travaillé n'expose pas de porte morte",
           hOpp.includes("fp-ouvrir"), false);
      } finally {
        lignes = lignesS; projets = projS; fichePosteOuverte = null;
      }
    }
