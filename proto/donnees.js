/* ============================================================================
   PROTO — LE JEU D'ESSAI DE DÉPART
   Données STRUCTURELLES, pas réelles. Aucun de ces chiffres n'est un relevé :
   ils servent à faire tourner les écrans et à voir ce qu'ils affichent quand
   tout est incomplet — ce qui est l'état réel de l'outil aujourd'hui.

   Trois lignes, volontairement dans trois états différents :
     EMAG 1  — chiffrée, avec un essai prometteur et un validé 5× (le cas heureux)
     EMAG 3  — chiffrée, sans essai (la ligne qu'on oublie)
     PCI     — cible connue, rien de chiffré (le cas « à chiffrer »)
   ========================================================================== */

const JEUX = {
  lignes: [
    {
      id: "l1",
      nom: "EMAG 1",
      refs: [{
        id: "r1",
        nom: "Disque 356x26 RPI",
        cibleCPP: 0.0240,
        ops: [
          { id: "o10", nom: "OP10", code: "OP10", scs: [
            { id: "p1", name: "Process actuel", baseline: true, validationThreshold: 5,
              outils: [{ id: "t1", numero: "T-517", logements: [
                { id: "g1", nom: "Face",  ref: "SL500",  prix: 42, aretes: 2, charniere: 150 },
                { id: "g2", nom: "Piste", ref: "SL500",  prix: 42, aretes: 2, charniere: 220 }
              ] }],
              essais: [] },
            { id: "e1", name: "SL500 · charnière 300", validationThreshold: 5,
              outils: [{ id: "t1", numero: "T-517", logements: [
                { id: "g1", nom: "Face",  ref: "SL500",  prix: 42, aretes: 2, charniere: 210 },
                { id: "g2", nom: "Piste", ref: "SL500",  prix: 42, aretes: 2, charniere: 300 }
              ] }],
              essais: [
                { id: "es1", titre: "Essai 1", date: "2026-09-28", equipe: "M.",
                  params: { logements: [
                    { logementId: "g1", logementNom: "Face",  charniere: 210 },
                    { logementId: "g2", logementNom: "Piste", charniere: 300 } ] },
                  prelevements: [
                    { id: "p1", piece: 210, batt: 0.09 }, { id: "p2", piece: 300, batt: 0.10 } ] },
                { id: "es2", titre: "Essai 2", date: "2026-09-30", equipe: "M.",
                  params: { logements: [
                    { logementId: "g1", logementNom: "Face",  charniere: 210 },
                    { logementId: "g2", logementNom: "Piste", charniere: 300 } ] },
                  prelevements: [
                    { id: "p1", piece: 210, batt: 0.11 }, { id: "p2", piece: 260, batt: 0.10 } ] }
              ] },
            { id: "e2", name: "SL506 · piste marquée", validationThreshold: 5,
              outils: [{ id: "t2", numero: "T-518", logements: [
                { id: "g1", nom: "Face",  ref: "SL506",  prix: 38, aretes: 2, charniere: 150 },
                { id: "g2", nom: "Piste", ref: "SL506",  prix: 38, aretes: 2, charniere: 240 }
              ] }],
              essais: [1, 2, 3, 4, 5].map(k => ({
                id: "ev" + k, titre: "Essai " + k, date: "2026-09-0" + k, equipe: "A.",
                params: { logements: [
                  { logementId: "g1", logementNom: "Face",  charniere: 150 },
                  { logementId: "g2", logementNom: "Piste", charniere: 240 } ] },
                prelevements: [
                  { id: "p1", piece: 150, batt: 0.10 }, { id: "p2", piece: 240, batt: 0.11 } ]
              })) }
          ] },
          { id: "o20", nom: "OP20", code: "OP20", scs: [
            { id: "p2", name: "Process actuel", baseline: true, validationThreshold: 5,
              outils: [{ id: "t3", numero: "T-522", logements: [
                { id: "g3", nom: "Epaisseur piste", ref: "SL500", prix: 46, aretes: 2, charniere: 130 }
              ] }],
              essais: [] },
            { id: "e3", name: "SL500 · 2 arêtes", validationThreshold: 5,
              outils: [{ id: "t3", numero: "T-522", logements: [
                { id: "g3", nom: "Epaisseur piste", ref: "SL500", prix: 46, aretes: 2, charniere: 120 }
              ] }],
              essais: [
                { id: "es1", titre: "Essai 1", date: "2026-09-27", equipe: "A.",
                  params: { logements: [{ logementId: "g3", logementNom: "Epaisseur piste", charniere: 120 }] },
                  prelevements: [{ id: "p1", piece: 60, batt: 0.08 }] }
              ] }
          ] },
          { id: "o30", nom: "OP30", code: "OP30", scs: [
            { id: "p3", name: "Process actuel", baseline: true, validationThreshold: 5,
              outils: [{ id: "t4", numero: "T-530", logements: [
                { id: "g4", nom: "Perçage avant", ref: "SL500", prix: 30, aretes: 2, charniere: 180 }
              ] }],
              essais: [] }
          ] }
        ]
      }]
    },
    {
      id: "l2",
      nom: "EMAG 3",
      refs: [{
        id: "r2",
        nom: "Disque 330x28",
        cibleCPP: 0.0310,
        ops: [
          { id: "o10", nom: "OP10", code: "OP10", scs: [
            { id: "p1", name: "Process actuel", baseline: true, validationThreshold: 5,
              outils: [{ id: "t1", numero: "T-610", logements: [
                { id: "g1", nom: "Face",  ref: "SL500", prix: 40, aretes: 2, charniere: 160 },
                { id: "g2", nom: "Piste", ref: "SL500", prix: 40, aretes: 2, charniere: 190 }
              ] }],
              essais: [] }
          ] },
          { id: "o20", nom: "OP20", code: "OP20", scs: [
            { id: "p2", name: "Process actuel", baseline: true, validationThreshold: 5,
              outils: [{ id: "t2", numero: "T-615", logements: [
                { id: "g3", nom: "Epaisseur piste", ref: "SL500", prix: 44, aretes: 2, charniere: 140 }
              ] }],
              essais: [] }
          ] }
        ]
      }]
    },
    {
      /* la ligne « à chiffrer » : une cible est connue, aucun coût ne l'est.
         C'est le cas que l'app actuelle faisait disparaître (cahier §4.3). */
      id: "l3",
      nom: "PCI (ligne 4)",
      refs: [{
        id: "r3",
        nom: "Disque 305x22",
        cibleCPP: 0.0180,
        ops: [
          { id: "o10", nom: "OP10", code: "OP10", scs: [] },
          { id: "o20", nom: "OP20", code: "OP20", scs: [] }
        ]
      }]
    }
  ]
};