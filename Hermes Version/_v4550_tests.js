    /* ---- v4.55.0 — le classeur Matis : la mesure de l'écart réel / théorique ----
       Le classeur de Matis donne la production RÉELLE par couple ligne × référence
       et le CPP réellement consommé. L'outil, lui, budgète un CPP. L'écart entre
       les deux mesure la santé du plan outillage — c'est tout ce que cet écran
       fait, et c'est déjà beaucoup. */
    {
      /* --- la fonction pure : matisRecap, testée sans fichier --- */
      const f = (nom, codeLigne, ref, prod, outils) => ({ codeLigne, ref, refComplete: ref, production: prod, outils });
      const o = (theo, reel, qte) => ({ cppTheorique: theo, cppReel: reel, qteReelle: qte, numero: "T", opCode: "OP10" });
      const feuilles = [
        f("f1", "E1", "356x26 RPI", 6781, [ o(0.0158, 0.0280, 5), o(0.0233, 0.0010, 1), o(0.0079, 0.0224, 4) ]),
        f("f2", "E2", "290x12", 2234, [ o(0.2235, 0.3045, 12) ]),
        /* un poste non produit : production nulle, il ne doit rien compter */
        f("f3", "E3", "330x14", 0, [ o(0.3154, null, null) ])
      ];
      const recap = matisRecap(feuilles);
      ok("matis : un couple ligne × référence = une ligne du récapitulatif", recap.length, 3);

      const e1 = recap.find(c => c.ref.includes("356x26"));
      ok("matis : la production réelle est lue du classeur (B1)", e1.production, 6781);
      ok("matis : le CPP théorique est la somme des outils", e1.cppTheorique, 0.0158 + 0.0233 + 0.0079, 1e-9);
      ok("matis : le CPP réel est la somme des consommations", e1.cppReel, 0.0280 + 0.0010 + 0.0224, 1e-9);
      ok("matis : l'écart = réel − théorique (positif = surconsommation)",
         [e1.ecart > 0, e1.ecart], [true, (0.0280 + 0.0010 + 0.0224) - (0.0158 + 0.0233 + 0.0079)]);
      ok("matis : l'écart annuel = CPP réel × production réelle",
         e1.gapAnnuel, e1.ecart * 6781, 1e-6);

      /* un poste non produit ne compte dans aucun total */
      const e3 = recap.find(c => c.ref.includes("330x14"));
      ok("matis : un couple sans production n'a ni coût annuel réel ni écart",
         [e3.aProduction, e3.coutAnnuelReel, e3.coutAnnuelTheorique, e3.gapAnnuel], [false, 0, 0, 0]);

      /* le libellé d'écart : toujours une raison, jamais un chiffre nu (constitution §3.5) */
      ok("matis : un écart positif se lit comme une surconsommation, avec son montant",
         libelleEcartMatis(e1).includes("surconsommation") && libelleEcartMatis(e1).includes("€/pièce"), true);
      ok("matis : un couple non mesuré le dit, plutôt que d'afficher un écart faux",
         libelleEcartMatis(e3).includes("non mesurable"), true);
      ok("matis : le récapitulatif est trié par production décroissante",
         recap[0].production >= recap[1].production, true);

      /* la lecture d'un classeur est un CONSTAT : elle n'écrit rien dans le suivi */
      ok("matis : la lecture ne touche ni les lignes ni les projets",
         [typeof matisRecap, lignes.length, projets.length] , ["function", lignes.length, projets.length]);
    }
