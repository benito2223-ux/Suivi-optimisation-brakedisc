    /* ---- v4.51.2 — la carte atelier (couche 0) ---------------------------------------
       La carte est une FONCTION du calcul testé en 4.51.0 : gainPoste() et etatTuile().
       Ce qu'on vérifie ici, c'est la carte elle-même : ce qu'elle dessine, ce qu'elle
       filtre, et le seuil de recette A2 qui dira si elle est utile ou décorative.

       ⚠ la carte dessine la VRAIE topologie déclarée (LIGNES_SEPT_FONS) croisée avec les
       lignes présentes dans les données : on ne peut pas lui passer une topologie de
       test. Les comptes attendus ci-dessous sont donc dérivés de la déclaration
       (assertée explicitement, pour que la carte et la déclaration ne puissent pas
       diverger en silence). */
    {
      const opCfg2 = Object.assign({}, defaultConfig, { volumeActif: true });
      const scSerie = (id, nom) => ({ id, name: nom, statut: "serie", outils: [
        { id: id + "u", numero: "T", logements: [ { id: id + "l", nom: "Bol", prix: 5, aretes: 8, charniere: 100 } ] } ] });
      const scProd  = (id) => ({ id, name: "Prod", baseline: true, outils: [
        { id: id + "u", numero: "T", logements: [ { id: id + "l", nom: "Bol", prix: 30, aretes: 8, charniere: 100 } ] } ] });
      const opAvec  = (id, nom, scenarios) => ({ id, nom, config: opCfg2, scenarios });
      const refAvec = (id, nom, vol, cible, ops) => normalizeReference({ id, nom, productionAnnuelle: vol, cibleCPP: cible || "", ops });

      const lignesSauve = lignes, projSauve = projets;
      try {
        /* --- la carte dessine toute l'usine déclarée, pas seulement nos lignes --- */
        lignes = [];
        const carteVide = cartePostes();
        ok("carte : sans aucune ligne dans le suivi, la carte est vide (aucune tuile fantôme)",
           carteVide.length, 0);

        /* EMAG 1 : un poste gagné (356x26 passée en série), un poste à chiffrer
           (304x28, cible posée, aucune mesure), et un OP10 « en cours ». */
        lignes = [ normalizeLigne({ id: "LC1", nom: "EMAG 1", references: [
          refAvec("r1", "356x26", "100000", "", [ opAvec("o1", "OP10", [ scProd("p1"), scSerie("s1", "SL500") ]) ]),
          refAvec("r2", "304x28", "50000", "0.250", [ opAvec("o2", "OP40", []) ]),
          refAvec("r3", "290x12", "80000", "", [ opAvec("o3", "OP10", [ scProd("p3"),
            { id: "s3", name: "Essai", statut: "essai", outils: [ { id: "s3u", numero: "T", logements: [ { id: "s3l", nom: "Bol", prix: 20, aretes: 8, charniere: 100 } ] } ],
              essais: [ { id: "e3", titre: "Essai 1", date: "2026-09-29", prelevements: [ { id: "pr3", piece: "5", cotes: {} } ] } ] } ]) ])
        ]}) ];

        const emagDeclaree = LIGNES_SEPT_FONS.find(x => x.nom === "EMAG 1").machines.map(m => m.code);
        const tous = cartePostes();
        ok("carte : une tuile par machine DÉCLARÉE de la ligne (la topologie fait foi)",
           tous.map(t => t.code), emagDeclaree);
        ok("carte : la ligne déclarée mais jamais travaillée est absente des données = aucune tuile",
           tous.length, emagDeclaree.length);

        const parCode = {}; tous.forEach(t => { parCode[t.code] = t; });
        ok("carte : le poste dont l'outillage est passé en série est vert « gagné »",
           parCode.OP10.etat, "gagne");
        ok("carte : le poste dont la référence dominante porte une cible sans mesure est « à chiffrer »",
           parCode.OP40.etat, "aChiffrer");
        ok("carte : un poste déclaré, jamais travaillé, reste une « opportunité »",
           parCode.OP20.etat, "opportunite");
        ok("carte : la tuile porte le nom de la machine quand il est déclaré",
           parCode.OP10.nomMachine, "Ébauche piste");

        /* --- le filtre projet --- */
        projets = [];
        ok("carte : sans projet, la carte montre toute l'usine",
           carteVisiblePostes(tous, null).length, tous.length);
        const pj = normalizeProjet({ nom: "2026/2027", tags: [ { ligneId: "LC1", referenceId: "r1", opId: "o1", scenarioId: "s1" } ] });
        projets = [pj];
        const filtres = carteVisiblePostes(tous, pj.id);
        ok("carte : le filtre projet ne garde que les postes étiquetés dans ce projet",
           [filtres.length, filtres.every(t => t.code === "OP10")], [1, true]);
        ok("carte : un projet inconnu ne filtre pas tout (on ne caches jamais l'usine)",
           carteVisiblePostes(tous, "pj-inexistant").length, tous.length);

        /* --- la recette A2 (seuil : ≥ 1/3 de tuiles actionnables) --- */
        const r = carteRecetteA2(tous);
        ok("carte : la recette A2 se calcule sur le ratio actionnables / total",
           Math.abs(r.ratio - r.actionnables / r.total) < 1e-9, true);
        ok("carte : le seuil A2 est atteint sur ce jeu (1 poste gagné + 1 à chiffrer)",
           [r.actionnables, r.ratio >= 1/3], [2, true]);
        ok("carte : une carte vide ne plante pas", carteRecetteA2([]).ratio, 0);
        ok("carte : une carte d'opportunités seules ne atteint PAS le seuil (elle est creuse)",
           carteRecetteA2(cartePostes().filter(t => t.etat === "opportunite")).ratio < 1/3
             || carteRecetteA2(cartePostes().filter(t => t.etat === "opportunite")).total === 0, true);
      } finally {
        lignes = lignesSauve; projets = projSauve;
        carteFiltreProjetId = null; carteProjetChoisi = false;
      }
    }
