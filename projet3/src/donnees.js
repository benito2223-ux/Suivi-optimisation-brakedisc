/* ============================================================================
   PROJET3 — LES DONNÉES DE DÉPART
   1. La topologie de Sept Fons (les lignes qui existent, leurs OPs) — un fait
      d'atelier, porté depuis LIGNES_SEPT_FONS de l'app de production.
   2. Le jeu d'exemple — STRUCTUREL, aucun chiffre réel. Il porte le marqueur
      [Exemple] partout où il se voit, pour qu'aucun chiffre fictif ne puisse
      passer pour une mesure du site. Les vraies données arrivent par
      l'import d'un export de l'app, sur le poste, sans rien envoyer.

   Aucune fonction de calcul ici — le noyau calcule, ce fichier décrit.
   ========================================================================== */

"use strict";

/* La topologie réelle de l'atelier : l'ordre est celui du référentiel de
   l'app de production. Une machine qui manque se déclare là, elle ne
   s'invente pas à l'écran. */
const LIGNES_SEPT_FONS = [
  { nom: "Weisser 1", familles: "weisser", ops: [] },
  { nom: "Weisser 2", familles: "weisser", ops: [] },
  { nom: "Weisser 3", familles: "weisser", ops: [] },
  { nom: "Weisser 4", familles: "weisser", ops: [] },
  { nom: "HESSAPP", familles: "hessapp", ops: [
    { nom: "OP10 Ébauche", ordre: 10 },
    { nom: "OP15 Ébauche", ordre: 15 },
    { nom: "OP20 Ébauche", ordre: 20 },
    { nom: "OP40 Finition", ordre: 40 }
  ] },
  { nom: "EMAG 1", familles: "emag", ops: [
    { nom: "OP10 Ébauche piste", ordre: 10 },
    { nom: "OP20 Ébauche piste extérieure", ordre: 20 },
    { nom: "OP30 Perçages", ordre: 30 },
    { nom: "OP40 Finition pistes", ordre: 40 }
  ] },
  { nom: "EMAG 2", familles: "emag", ops: [
    { nom: "OP10 Ébauche", ordre: 10 },
    { nom: "OP30 Perçages", ordre: 30 },
    { nom: "OP40 Finition pistes", ordre: 40 }
  ] },
  { nom: "EMAG 3", familles: "emag", ops: [
    { nom: "OP10 Ébauche", ordre: 10 },
    { nom: "OP40 Finition pistes", ordre: 40 }
  ] },
  { nom: "PCI 1", familles: "pci", ops: [] },
  { nom: "PCI 2", familles: "pci", ops: [] }
];

/* Le taux horaire est une DONNÉE de ligne, saisie — jamais un chiffre en dur
   dans le code (l'app le porte pareil). Le jeu d'exemple en met un fictif. */

/* ============================================================================
   LE JEU D'EXEMPLE — structurel, aucun chiffre réel
   ========================================================================== */

function idAleatoire(prefix) {
  return (prefix || "x") + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

/* Un état complet vierge, avec les LIGNES de l'atelier semées — sans
   référence ni opération : la structure OP d'une ligne se pose quand une
   référence arrive (des postes fantômes sans scénario feraient croire à une
   ligne travaillée). La topologie connue est proposée à la création. */
function etatVierge() {
  return {
    outil: "SPK Suivi optimisation",
    format: 9,
    toolVersion: VERSION,
    revision: 1,
    lignes: LIGNES_SEPT_FONS.map(l => ({
      id: idAleatoire("li"),
      nom: l.nom,
      coutHoraire: "",
      observations: "",
      maintenanceDate: "",
      maintenanceType: "",
      references: []
    })),
    projets: [],
    responsables: [],
    livraisons: [],
    backlog: [],
    activeProjetId: "",
    activeLigneId: "",
    activeReferenceId: "",
    activeOpId: "",
    activeScenarioId: "",
    modifieLe: new Date().toISOString()
  };
}

/* Les OPs connus d'une ligne (topologie de l'atelier) — proposés à la
   création d'une référence, pour poser la structure d'un coup. */
function opsConnusDeLigne(nomLigne) {
  const l = LIGNES_SEPT_FONS.find(x => x.nom.toLowerCase() === String(nomLigne || "").trim().toLowerCase());
  return l ? l.ops.slice() : [];
}

/* Le jeu [Exemple] : une référence, deux OPs, un scénario de production, un
   scénario d'essai avec son essai et ses prélèvements. Les chiffres sont
   PLAUSIBLES ET FICTIFS — la structure, pas la réalité du site. */
function etatExemple() {
  const etat = etatVierge();
  const emag1 = etat.lignes.find(l => l.nom === "EMAG 1");
  const hessapp = etat.lignes.find(l => l.nom === "HESSAPP");

  function logement(nom, mabec, ref, prix, aretes, charniere, extra) {
    return Object.assign({
      id: idAleatoire("g"), nom: nom, ref: ref, codeArticle: "", mabec: mabec,
      prix: prix, aretes: aretes, charniere: charniere,
      vc: "", f: "", kappaR: "", rayonBec: "", apPiste: "",
      tempsCoupe: "", tempsDeplacement: "", suiviTolerance: false
    }, extra || {});
  }
  function outil(numero, logements, extra) {
    return Object.assign({
      id: idAleatoire("t"), numero: numero, correcteur: "", description: "",
      plan: null, pieces: [], logements: logements
    }, extra || {});
  }

  /* ── EMAG 1 · OP40 finition pistes : l'exemple qui montre tout le chemin ── */
  const refE1 = {
    id: idAleatoire("re"), nom: "[Exemple] DV 356x26 RPI",
    cibleCPP: 0.10, productionAnnuelle: 60000, volumeHistorique: [],
    ops: []
  };

  const prodOP40 = {
    id: idAleatoire("sc"), name: "Prod actuelle", cycle: 100,
    baseline: true, statut: "serie", statutMotif: "", statutDate: "",
    emag1: true, battCotes: "DG",
    limitOverride: false, limitLabel: "Battement (mm)", limitValue: "",
    limitLabel2: "Ra (µm)", limitValue2: 0.8, critere2Actif: true,
    criteresSup: [], validationThreshold: 5, battActif: true,
    tauxRebutAnnuel: "", marpossRapport: "", tendanceRapport: "", notes: "",
    outils: [
      outil("T511", [
        logement("D1", "IM02 198 054", "SNGX 120716 S02020 CBN", 38, 8, 800),
        logement("D2", "IM02 209 560", "CNGX 120716 S02020 CBN", 38, 8, 700)
      ]),
      outil("T513", [
        logement("D1", "IM02 209 560", "CNGX 120716 S02020 CBN", 19, 4, 800)
      ])
    ],
    essais: [],
    scrapLog: [],
    modifieLe: new Date().toISOString()
  };

  const essaiOP40 = {
    id: idAleatoire("e"), titre: "[Exemple] SL500 sur T513 D1", date: "2026-09-15",
    dateFin: "2026-09-15", heureDebut: "08:00", heureFin: "10:30",
    equipe: "Matin", operateur: "", redigePar: "",
    programme: "", programmeGauche: "", programmeDroit: "",
    maturiteBruts: "", observations: "Essai fictif de démonstration — la structure d'un essai, pas une mesure du site.",
    cloture: null,
    params: { logements: [] },
    prelevements: [],
    photos: [], marpossListe: [], marposs: null,
    modifieLe: new Date().toISOString()
  };

  const essaiOP40b = {
    id: idAleatoire("e"), titre: "[Exemple] SL500 — répétition 2", date: "2026-09-22",
    dateFin: "2026-09-22", heureDebut: "13:00", heureFin: "15:00",
    equipe: "Après-midi", operateur: "", redigePar: "",
    programme: "", programmeGauche: "", programmeDroit: "",
    maturiteBruts: "", observations: "",
    cloture: null,
    params: { logements: [] },
    prelevements: [],
    photos: [], marpossListe: [], marposs: null,
    modifieLe: new Date().toISOString()
  };

  const essaiOP40c = {
    id: idAleatoire("e"), titre: "[Exemple] SL500 — répétition 3", date: "2026-09-29",
    dateFin: "2026-09-29", heureDebut: "08:00", heureFin: "11:00",
    equipe: "Matin", operateur: "", redigePar: "",
    programme: "", programmeGauche: "", programmeDroit: "",
    maturiteBruts: "", observations: "",
    cloture: null,
    params: { logements: [] },
    prelevements: [],
    photos: [], marpossListe: [], marposs: null,
    modifieLe: new Date().toISOString()
  };

  const optiOP40 = {
    id: idAleatoire("sc"), name: "Essai SL500", cycle: 100,
    baseline: false, statut: "essai", statutMotif: "", statutDate: "",
    emag1: true, battCotes: "DG",
    limitOverride: false, limitLabel: "Battement (mm)", limitValue: "",
    limitLabel2: "Ra (µm)", limitValue2: 0.8, critere2Actif: true,
    criteresSup: [], validationThreshold: 5, battActif: true,
    tauxRebutAnnuel: "", marpossRapport: "", tendanceRapport: "", notes: "",
    outils: [
      outil("T511", [
        logement("D1", "IM02 198 054", "SNGX 120716 S02020 CBN", 38, 8, 800),
        logement("D2", "IM02 209 560", "CNGX 120716 S02020 CBN", 38, 8, 700)
      ]),
      outil("T513", [
        logement("D1", "IM02 190 311", "SNGN 090416-F SL500", 27, 4, 2400, { kappaR: 85, vc: 350, f: 0.25 })
      ])
    ],
    essais: [essaiOP40, essaiOP40b, essaiOP40c],
    scrapLog: [],
    modifieLe: new Date().toISOString()
  };

  /* La charnière mesurée de chaque essai : elle fait le CPP OBTENU. */
  essaiOP40.params.logements = [
    { logementId: optiOP40.outils[0].logements[0].id, logementNom: "D1", charniere: 800, vc: "", f: "" },
    { logementId: optiOP40.outils[0].logements[1].id, logementNom: "D2", charniere: 700, vc: "", f: "" },
    { logementId: optiOP40.outils[1].logements[0].id, logementNom: "D1", charniere: 2400, vc: "", f: "" }
  ];
  essaiOP40.prelevements = [
    { id: idAleatoire("p"), piece: 800, batt: "", battD: 0.09, battG: 0.07, logementId: optiOP40.outils[1].logements[0].id, pointMesure: "Piste", usure: "ok", valeur2: 0.62, valeurs: {} },
    { id: idAleatoire("p"), piece: 1600, batt: "", battD: 0.10, battG: 0.08, logementId: optiOP40.outils[1].logements[0].id, pointMesure: "Piste", usure: "ok", valeur2: 0.58, valeurs: {} },
    { id: idAleatoire("p"), piece: 2400, batt: "", battD: 0.11, battG: 0.06, logementId: optiOP40.outils[1].logements[0].id, pointMesure: "Piste", usure: "ok", valeur2: 0.66, valeurs: {} }
  ];
  essaiOP40b.params.logements = essaiOP40.params.logements;
  essaiOP40b.prelevements = [
    { id: idAleatoire("p"), piece: 800, batt: "", battD: 0.08, battG: 0.07, logementId: optiOP40.outils[1].logements[0].id, pointMesure: "Piste", usure: "ok", valeur2: 0.60, valeurs: {} },
    { id: idAleatoire("p"), piece: 2400, batt: "", battD: 0.09, battG: 0.07, logementId: optiOP40.outils[1].logements[0].id, pointMesure: "Piste", usure: "ok", valeur2: 0.63, valeurs: {} }
  ];
  essaiOP40c.params.logements = essaiOP40.params.logements.map(x => Object.assign({}, x, {
    /* la répétition 3 mesure une charnière différente du prévu : c'est
       l'endroit où « prévu » et « obtenu » se distinguent à l'écran */
    charniere: x.charniere === 2400 ? 3000 : x.charniere
  }));
  essaiOP40c.prelevements = [
    { id: idAleatoire("p"), piece: 2400, batt: "", battD: 0.10, battG: 0.05, logementId: optiOP40.outils[1].logements[0].id, pointMesure: "Piste", usure: "ok", valeur2: 0.61, valeurs: {} }
  ];

  const op40 = {
    id: idAleatoire("op"), nom: "OP40 Finition pistes", ordre: 40, opCode: "OP40",
    ficheOutil: null,
    config: { volumeActif: true, coutMachineActif: false },
    scenarios: [prodOP40, optiOP40]
  };
  refE1.ops.push(op40);

  /* ── EMAG 1 · OP10 : un poste à chiffrer (cible posée, rien de saisi) ── */
  const op10 = {
    id: idAleatoire("op"), nom: "OP10 Ébauche piste", ordre: 10, opCode: "OP10",
    ficheOutil: null, config: {},
    scenarios: [{
      id: idAleatoire("sc"), name: "Base Excel", cycle: 100,
      baseline: true, statut: "serie", statutMotif: "", statutDate: "",
      emag1: false, battCotes: "DG",
      limitOverride: false, limitLabel: "Battement (mm)", limitValue: "",
      limitLabel2: "Ra (µm)", limitValue2: "", critere2Actif: false,
      criteresSup: [], validationThreshold: 5, battActif: true,
      tauxRebutAnnuel: "", marpossRapport: "", tendanceRapport: "", notes: "",
      /* Le trio est volontairement incomplet : le poste doit rester
         « à chiffrer » et être compté, pas dilué (cahier §5.2). */
      outils: [outil("T543", [logement("D1", "", "", "", "", "")])],
      essais: [], scrapLog: [], modifieLe: new Date().toISOString()
    }]
  };
  refE1.ops.push(op10);

  emag1.references = [refE1].concat(emag1.references);
  emag1.coutHoraire = 60;   // fictif [Exemple]

  /* ── HESSAPP · OP40 : un poste gagné (l'essai est passé en série) ── */
  const refH = {
    id: idAleatoire("re"), nom: "[Exemple] DV 302x26 RPI",
    cibleCPP: 0.14, productionAnnuelle: 40000, volumeHistorique: [],
    ops: [{
      id: idAleatoire("op"), nom: "OP40 Finition", ordre: 40, opCode: "OP40",
      ficheOutil: null, config: { volumeActif: true },
      scenarios: [
        {
          id: idAleatoire("sc"), name: "Prod actuelle", cycle: 100,
          baseline: false, statut: "valide", statutMotif: "", statutDate: "",
          emag1: false, battCotes: "DG",
          limitOverride: false, limitLabel: "Battement (mm)", limitValue: "",
          limitLabel2: "Ra (µm)", limitValue2: "", critere2Actif: false,
          criteresSup: [], validationThreshold: 5, battActif: true,
          tauxRebutAnnuel: "", marpossRapport: "", tendanceRapport: "", notes: "",
          outils: [outil("T548", [logement("D1", "Z000 546 266", "SNGN 120716 KY3500", 45, 8, 600)])],
          essais: [], scrapLog: [], modifieLe: new Date().toISOString()
        },
        {
          id: idAleatoire("sc"), name: "SL500 adopté", cycle: 100,
          baseline: true, statut: "serie", statutMotif: "", statutDate: "2026-09-10",
          emag1: false, battCotes: "DG",
          limitOverride: false, limitLabel: "Battement (mm)", limitValue: "",
          limitLabel2: "Ra (µm)", limitValue2: "", critere2Actif: false,
          criteresSup: [], validationThreshold: 5, battActif: true,
          tauxRebutAnnuel: "", marpossRapport: "", tendanceRapport: "", notes: "",
          outils: [outil("T548", [logement("D1", "IM02 137 021", "SNGN 120716 SL500", 27, 8, 1200)])],
          essais: [], scrapLog: [], modifieLe: new Date().toISOString()
        }
      ]
    }]
  };
  hessapp.references = [refH].concat(hessapp.references);
  hessapp.coutHoraire = 55;   // fictif [Exemple]

  /* ── Un responsable et un projet d'exemple ── */
  etat.responsables = [{ id: idAleatoire("u"), nom: "[Exemple] Pilote ligne", couleur: "#3b82f6" }];
  etat.projets = [{
    id: idAleatoire("pj"), nom: "[Exemple] Économie OP40",
    description: "Projet fictif : réduire le CPP outillage de l'OP40 en testant la SL500 sur le logement D1 de T513.",
    statut: "encours", dateCible: "2026-11-15",
    responsableId: etat.responsables[0].id,
    couleur: "#3b82f6",
    creePar: "", creeLe: new Date().toISOString(),
    modifieLe: new Date().toISOString(),
    tags: [{
      ligneId: emag1.id, referenceId: refE1.id, opId: op40.id, scenarioId: optiOP40.id
    }]
  }];

  etat.activeLigneId = emag1.id;
  etat.activeReferenceId = refE1.id;
  etat.activeOpId = op40.id;
  etat.activeScenarioId = optiOP40.id;

  return etat;
}
