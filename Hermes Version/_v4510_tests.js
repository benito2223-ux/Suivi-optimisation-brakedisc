    /* ---- v4.51.0 — carte atelier : le calcul pur du poste (couche 0) ---------------
       gainPoste() / etatTuile(). Aucun pixel d'UI ici : ces fonctions alimenteront la
       tuile ET l'A4 Mission, et doivent donc être justes avant d'être dessinées.
       Rappel D3 : le gain passe par bilanAnnuel() donc par perimetreCompare() (v4.45) —
       jamais une soustraction de deux totaux bruts. */
    {
      /* ⚠ les modules de coût (dont volumeActif) se règlent PAR OP (op.config), pas dans
         le config global : un test qui allume le module au mauvais endroit verrait un gain
         nul sans que la fonction soit fausse. C'est ce que le harnais a révélé — on touche
         donc chaque op.config explicitement. */
      const opCfg = (extra) => Object.assign({}, defaultConfig, { volumeActif: true }, extra || {});
      const lgA  = (l, refs) => normalizeLigne({ id: l, nom: "EMAG 1", coutHoraire: "", references: refs });

      /* --- référence A : 356x26, OP10 chiffrable (prod ★ + essai passé en série),
             et une OP20 déclarée mais NON chiffrable (prix/charnière vides) --- */
      const refA = normalizeReference({ id: "rA", nom: "356x26", productionAnnuelle: "100000", cibleCPP: "0.300",
        ops: [
          { id: "oA10", nom: "OP10 Ebauche", config: opCfg(), scenarios: [
            { id: "pA10", name: "Prod", baseline: true, outils: [
              { id: "u1", numero: "T1", logements: [ { id: "l1", nom: "Bol", prix: 30, aretes: 8, charniere: 100 } ] } ] },
            { id: "eA10", name: "Essai SL500", statut: "serie", outils: [
              { id: "u2", numero: "T2", logements: [ { id: "l2", nom: "Bol", prix: 10, aretes: 8, charniere: 100 } ] } ] } ] },
          { id: "oA20", nom: "OP20 Perçages", config: opCfg(), scenarios: [
            { id: "pA20", name: "Prod", baseline: true, outils: [
              { id: "u3", numero: "T3", logements: [ { id: "l3", nom: "Bol", prix: "", aretes: 8, charniere: "" } ] } ] } ] }
        ] });
      /* --- référence B : 304x28 sur le MÊME poste OP10 (le cas réel EMAG 1) --- */
      const refB = normalizeReference({ id: "rB", nom: "304x28", productionAnnuelle: "50000", cibleCPP: "",
        ops: [
          { id: "oB10", nom: "OP10", config: opCfg(), scenarios: [
            { id: "pB10", name: "Prod", baseline: true, outils: [
              { id: "u4", numero: "T4", logements: [ { id: "l4", nom: "Bol", prix: 40, aretes: 8, charniere: 100 } ] } ] },
            { id: "eB10", name: "Essai", statut: "essai", outils: [
              { id: "u5", numero: "T5", logements: [ { id: "l5", nom: "Bol", prix: 40, aretes: 8, charniere: 100 } ] } ] } ] }
        ] });
      const lg = lgA("L1", [refA, refB]);
      const LS = [{ nom: "EMAG 1", machines: [ { code: "OP10", nom: "Ébauche piste" }, { code: "OP20", nom: "Ébauche ext." },
                                             { code: "OP30", nom: "Perçages" },       { code: "OP40", nom: "Finition" } ] }];

      /* --- la topologie vient de la déclaration, jamais des scénarios --- */
      ok("postesLigne : les tuiles suivent les machines déclarées, pas les scénarios",
         postesLigne(lg, LS).map(p => p.code), ["OP10", "OP20", "OP30", "OP40"]);
      ok("postesLigne : une ligne non déclarée ne dessine aucune tuile",
         postesLigne(normalizeLigne({ id: "L9", nom: "Weisser 1" }), LS).length, 0);

      /* --- un poste se retrouve par CODE, pas par le nom libre de l'OP --- */
      ok("scenariosPostes : « OP20 Perçages » rejoint bien le poste OP20",
         scenariosPostes(lg, "OP20").length, 1);
      ok("scenariosPostes : « OP 30 Perçages » et « OP30 » sont le même poste",
         scenariosPostes(normalizeLigne({ id: "LX", nom: "EMAG 1", references: [ normalizeReference({ id: "rZ", nom: "z", ops: [
            { id: "oZ", nom: "OP 30 Perçages", scenarios: [] } ] }) ] }), "OP30").length, 1);
      ok("scenariosPostes : un opCode inconnu ne trouve rien",
         scenariosPostes(lg, "OP99").length, 0);

      /* --- le cas de référence : gain acté sur le poste OP10 --- */
      const p10 = gainPoste(lg, "OP10", LS);
      /* refA : prod 30/(8x100) = 0,0375 €/pièce · essai 10/(8x100) = 0,0125
                 gain = 0,025 x 100 000 = 2 500 €/an (périmètre commun = plaquettes seules)
         refB : prod 0,05 · essai 0,05 -> gain 0 (aucun écart, donc rien à acter) */
      ok("gainPoste : un scénario en série donne un gain ACTÉ, rien de projeté",
         [p10.gainActe > 0, p10.gainProjete], [true, 0]);
      ok("gainPoste : le gain acté = (prod - essai) x volume, périmètre commun",
         p10.gainActe, 2500, 1e-6);
      ok("gainPoste : deux références au même poste sont additionnées",
         p10.refs.length, 2);
      ok("gainPoste : le coût de prod cumule les deux références",
         p10.coutProd, 0.0375 + 0.05, 1e-9);

      /* --- le cas asymétrique réel réclamé par Z Code : l'OP20 non chiffrable --- */
      const p20 = gainPoste(lg, "OP20", LS);
      ok("gainPoste : une OP sans coût chiffrable sort du calcul (elle ne vaut pas 0)",
         [p20.coutProd, p20.refs.length, p20.nonChiffres], [0, 0, 1]);
      ok("gainPoste : un poste jamais travaillé n'a aucun gain",
         [p20.gainActe, p20.gainProjete], [0, 0]);

      /* --- un poste déclaré mais sans données ne plante pas --- */
      const p30 = gainPoste(lg, "OP30", LS);
      ok("gainPoste : OP30 (déclarée, aucune donnée) reste à zéro, sans erreur",
         [p30.gainActe, p30.gainProjete, p30.coutProd], [0, 0, 0]);

      /* --- l'état de la tuile : une fonction, quatre issues --- */
      ok("etatTuile : un gain acté = tuile verte",
         etatTuile(p10), "gagne");
      /* « en cours » = le poste porte un ESSAI (un relevé réel), pas un statut de scénario.
         C'est ce que veut dire « essai ouvert » : quelqu'un a mesuré sur ce poste. */
      const refEnCours = normalizeReference({ id: "rE", nom: "304x28", productionAnnuelle: "50000", ops: [
        { id: "oE", nom: "OP10", config: opCfg(), scenarios: [
          { id: "pE", name: "Prod", baseline: true, outils: [ { id: "uE1", numero: "T", logements: [ { id: "lE1", nom: "Bol", prix: 40, aretes: 8, charniere: 100 } ] } ] },
          { id: "eE", name: "Essai", statut: "essai", outils: [ { id: "uE2", numero: "T", logements: [ { id: "lE2", nom: "Bol", prix: 30, aretes: 8, charniere: 100 } ] } ],
            essais: [ { id: "ess1", titre: "Essai 1", date: "2026-09-29", prelevements: [ { id: "p", piece: "10", cotes: {} } ] } ] } ] } ] });
      const pEnCours = gainPoste(normalizeLigne({ id: "LE", nom: "EMAG 1", references: [ refEnCours ] }), "OP10", LS);
      ok("etatTuile : un poste qui porte un essai = tuile bleue « en cours »",
         [pEnCours.essaiOuvert, etatTuile(pEnCours)], [true, "encours"]);
      ok("etatTuile : une cible CPP posée mais rien de chiffré = à chiffrer",
         etatTuile({ gainActe: 0, gainProjete: 0, essaiOuvert: false, cibleCPP: 0.3 }), "aChiffrer");
      ok("etatTuile : rien du tout = opportunité",
         [etatTuile(p30), etatTuile(null)], ["opportunite", "opportunite"]);

      /* --- la cible et le chemin viennent de la référence DOMINANTE (volume) --- */
      ok("gainPoste : la cible vient de la référence dominante (la plus grosse)",
         [p10.refDominante.nom, p10.cibleCPP], ["356x26", 0.3]);
      /* le chemin n'existe que si la prod est AU-DESSUS de la cible. Ici 0,0375 €/pièce < 0,3 € :
         le poste est déjà sous la cible, il n'y a donc aucun « chemin » à afficher — c'est
         un résultat correct, pas un absent. Test explicite du cas « il y a un chemin ». */
      ok("gainPoste : un poste déjà sous la cible n'affiche aucun chemin",
         [p10.chemin, p10.coutProd < p10.cibleCPP], [null, true]);
      const refGrosGain = normalizeReference({ id: "rG", nom: "gros gain", productionAnnuelle: "100000", cibleCPP: "0.010", ops: [
        { id: "oG", nom: "OP10", config: opCfg(), scenarios: [
          { id: "pG", name: "Prod", baseline: true, outils: [ { id: "uG1", numero: "T", logements: [ { id: "lG1", nom: "Bol", prix: 30, aretes: 8, charniere: 100 } ] } ] },
          { id: "eG", name: "Essai", statut: "essai", outils: [ { id: "uG2", numero: "T", logements: [ { id: "lG2", nom: "Bol", prix: 5, aretes: 8, charniere: 100 } ] } ] } ] } ] });
      const pG = gainPoste(normalizeLigne({ id: "LG", nom: "EMAG 1", references: [ refGrosGain ] }), "OP10", LS);
      ok("gainPoste : un poste au-dessus de sa cible expose un chemin borné 0-100",
         pG.chemin !== null && pG.chemin >= 0 && pG.chemin <= 100, true);
      /* et borné aussi quand le gain projeté tire le cours EN DEÇÀ de la cible (plafond 100) */
      ok("gainPoste : le chemin est plafonné à 100 % quand la cible est dépassée",
         pG.chemin !== null && pG.chemin <= 100, true);
    }
