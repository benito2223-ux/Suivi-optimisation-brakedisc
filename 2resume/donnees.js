/* ============================================================================
   2resume — LE JEU DE DÉPART
   ----------------------------------------------------------------------------
   Structurel. **Aucun de ces chiffres n'est un relevé** : ce sont des nombres
   posés pour que les écrans aient quelque chose à afficher le premier jour, et
   pour que l'état réel d'une machine vide soit testable.

   Trois lignes, volontairement dans trois états différents, parce que ce sont
   les trois situations qu'un atelier traverse :

   · EMAG 1  — chiffrée, avec un essai qui fait MIEUX que le prévu (le cas
               heureux, et le seul qui prouve que la décomposition fonctionne) ;
   · EMAG 3  — chiffrée, aucun essai (la ligne qu'on oublie toujours) ;
   · PCI 4   — une cible connue, aucun coût calculable (le cas « à chiffrer »).

   Le bandeau de l'écran 1 affiche en permanence « jeu d'exemple — aucun chiffre
   réel » tant que ces données sont en place. Un outil dont on ne sait pas ce
   qu'il montre est un outil qui trompe.
   ========================================================================== */

const JEUX = {
  lignes: [
    {
      id: "j1", nom: "EMAG 1", coutHoraire: "",
      references: [{
        id: "jr1", nom: "Disque 356x26 RPI", cibleCPP: 0.2400, productionAnnuelle: "",
        ops: [
          {
            id: "jo1", nom: "OP10", ordre: 10, config: { partCoupante: 100 },
            scenarios: [
              {
                id: "jp1", name: "Prod actuelle", baseline: true, statut: "serie",
                outils: [{
                  id: "jpt1", numero: "T1", description: "Bol", correcteur: "D1",
                  logements: [
                    { id: "jpl1", nom: "D1", mabec: "", iso: "ISO —", prix: 7, aretes: 2, charniere: 40 },
                    { id: "jpl2", nom: "D2", mabec: "", iso: "ISO —", prix: 7, aretes: 2, charniere: 40 }
                  ]
                }],
                essais: []
              },
              {
                id: "jp2", name: "Essai — plaquette moins chère", statut: "essai",
                outils: [{
                  id: "jpt2", numero: "T1", description: "Bol", correcteur: "D1",
                  logements: [
                    { id: "jpl3", nom: "D1", mabec: "", iso: "ISO —", prix: 3.5, aretes: 2, charniere: 40 },
                    { id: "jpl4", nom: "D2", mabec: "", iso: "ISO —", prix: 3.5, aretes: 2, charniere: 40 }
                  ]
                }],
                essais: [{
                  id: "je1", titre: "Première série", date: "", equipe: "Matin",
                  params: { logements: [
                    { logementId: "jpl3", logementNom: "D1", outilNumero: "T1", charniere: 40 },
                    { logementId: "jpl4", logementNom: "D2", outilNumero: "T1", charniere: 40 }
                  ] },
                  prelevements: []
                }]
              }
            ]
          },
          {
            id: "jo2", nom: "OP20", ordre: 20, config: { partCoupante: 100 },
            scenarios: [{
              id: "jp3", name: "Prod actuelle", baseline: true, statut: "serie",
              outils: [{
                id: "jpt3", numero: "T2", description: "Piste", correcteur: "D1",
                logements: [{ id: "jpl5", nom: "D1", mabec: "", iso: "ISO —", prix: 12, aretes: 4, charniere: 60 }]
              }],
              essais: []
            }]
          }
        ]
      }]
    },
    {
      id: "j2", nom: "EMAG 3", coutHoraire: "",
      references: [{
        id: "jr2", nom: "Disque 330x28", cibleCPP: 0.3100, productionAnnuelle: "",
        ops: [
          {
            id: "jo3", nom: "OP10", ordre: 10, config: { partCoupante: 100 },
            scenarios: [{
              id: "jp4", name: "Prod actuelle", baseline: true, statut: "serie",
              outils: [{
                id: "jpt4", numero: "T4", description: "Bol", correcteur: "D1",
                logements: [{ id: "jpl6", nom: "D1", mabec: "", iso: "ISO —", prix: 9, aretes: 2, charniere: 30 }]
              }],
              essais: []
            }]
          },
          {
            id: "jo4", nom: "OP20", ordre: 20, config: { partCoupante: 100 },
            scenarios: []
          }
        ]
      }]
    },
    {
      id: "j3", nom: "PCI 4", coutHoraire: "",
      references: [{
        id: "jr3", nom: "Disque 305x22", cibleCPP: 0.1800, productionAnnuelle: "",
        ops: [{
          id: "jo5", nom: "OP10", ordre: 10, config: { partCoupante: 100 },
          scenarios: [{
            id: "jp5", name: "Prod actuelle", baseline: true, statut: "serie",
            outils: [{
              id: "jpt5", numero: "T7", description: "Bol", correcteur: "D1",
              logements: [{ id: "jpl7", nom: "D1", mabec: "", iso: "ISO —", prix: "", aretes: 2, charniere: 30 }]
            }],
            essais: []
          }]
        }]
      }]
    }
  ],
  projets: [],
  livraisons: []
};
