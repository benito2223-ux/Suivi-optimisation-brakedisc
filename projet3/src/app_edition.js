/* ============================================================================
   PROJET3 — LES PANNEAUX D'ÉDITION, LE RENDU ET LE DÉMARRAGE
   (la suite d'app.js — l'assembler concatène dans l'ordre)
   La saisie arrive en douceur : les champs essentiels d'abord, le contexte
   replié derrière un geste.
   ========================================================================== */

"use strict";

/* ---- la ligne ---- */
function ouvrirPanneauLigne(ligne) {
  const nom = champ("Nom de la ligne", "text", ligne.nom);
  const taux = champ("Taux horaire (€/h)", "number", ligne.coutHoraire,
    { step: "any", min: "0" }, "il valorise le temps machine — jamais affiché en comparaison du classeur");
  const obs = h("label", { class: "champ" },
    h("span", { class: "etiquette" }, "Observations"),
    h("textarea", { onchange: e => { ligne.observations = e.target.value; saveData(); } }, ligne.observations || ""));
  nom.querySelector("input").addEventListener("change", e => { ligne.nom = e.target.value; saveData(); });
  taux.querySelector("input").addEventListener("change", e => { ligne.coutHoraire = e.target.value === "" ? "" : parseFloat(e.target.value); saveData(); });
  ouvrirPanneau("Fiche ligne", ligne.nom, [
    nom, taux, obs,
    h("div", { class: "note" }, "Le taux horaire sert seulement à la zone « temps machine », qui se lit à côté du CPP outillage — les deux périmètres ne se comparent jamais.")
  ]);
}

/* ---- la référence ---- */
function ouvrirPanneauReference(ligne, ref) {
  const creation = !ref;
  const r = ref || { id: uid("re"), nom: "", cibleCPP: "", productionAnnuelle: "", volumeHistorique: [], ops: [] };
  const nom = champ("Nom de la référence disque", "text", r.nom);
  const cible = champ("Cible CPP du site (€/pièce)", "number", r.cibleCPP, { step: "any", min: "0" },
    "la valeur du classeur de Matis — l'écart à la cible ne s'affiche que si elle existe");
  const volume = champ("Volume annuel (pièces/an)", "number", r.productionAnnuelle, { step: "any", min: "0" },
    "il transforme le gain par pièce en gain annuel — sans lui, pas de €/an affiché");
  nom.querySelector("input").addEventListener("change", e => { r.nom = e.target.value; saveData(); });
  cible.querySelector("input").addEventListener("change", e => { r.cibleCPP = e.target.value === "" ? "" : parseFloat(e.target.value); saveData(); });
  volume.querySelector("input").addEventListener("change", e => { r.productionAnnuelle = e.target.value === "" ? "" : parseFloat(e.target.value); saveData(); });

  /* Les OPs connus de la ligne (topologie d'atelier) : on les pré-pose d'un
     coup si l'utilisateur le veut — des OPs sans scénario restent visibles,
     marquées « sans production », jamais confondues avec une ligne finie. */
  const connus = opsConnusDeLigne(ligne.nom);
  const prePose = [];
  let blocOps = null;
  if (creation && connus.length) {
    blocOps = h("div", { class: "groupe-champs" },
      h("span", { class: "titre-groupe" }, "Les opérations connues de " + ligne.nom));
    connus.forEach(op => {
      const cb = h("input", { type: "checkbox", checked: false, onchange: e => {
        if (e.target.checked) prePose.push(op); else {
          const i = prePose.indexOf(op); if (i >= 0) prePose.splice(i, 1);
        }
      } });
      blocOps.appendChild(h("label", { class: "champ", style: { display: "flex", gap: "10px", alignItems: "center" } }, cb,
        h("span", {}, op.nom)));
    });
  }

  ouvrirPanneau(creation ? "Nouvelle référence" : "Fiche référence", ligne.nom, [
    nom, cible, volume, blocOps,
    creation ? h("button", {
      class: "bouton primaire", onclick: () => {
        if (!r.nom) { toast("Donnez un nom à la référence."); return; }
        prePose.forEach(op => r.ops.push({
          id: uid("op"), nom: op.nom, ordre: op.ordre, opCode: "OP" + op.ordre,
          ficheOutil: null, config: {}, scenarios: []
        }));
        ligne.references.push(r);
        saveData(); fermerPanneau(); aller("ligne", { ligneId: ligne.id, refId: r.id });
        toast(prePose.length ? "Référence créée avec " + prePose.length + " opération(s) pré-posée(s)." : "Référence créée.");
      }
    }, "Créer la référence") : null
  ]);
}

/* ---- l'OP ---- */
function ouvrirPanneauOp(ligne, ref, op) {
  const creation = !op;
  const o = op || { id: uid("op"), nom: "", ordre: null, opCode: "", ficheOutil: null, config: {}, scenarios: [] };
  const nom = champ("Nom de l'opération", "text", o.nom, { placeholder: "OP40 Finition pistes" });
  const ordre = champ("Ordre (le numéro de l'OP)", "number", o.ordre, { step: "1" },
    "le code OP40 est dérivé du nom ou de l'ordre — jamais saisi en double");
  nom.querySelector("input").addEventListener("change", e => { o.nom = e.target.value; if (o.opCode !== undefined) o.opCode = ""; saveData(); });
  ordre.querySelector("input").addEventListener("change", e => { o.ordre = e.target.value === "" ? null : parseInt(e.target.value, 10); saveData(); });

  /* Les modules de calcul optionnels, par OP (comme l'app). */
  const cfg = o.config = o.config || {};
  const modules = h("div", { class: "groupe-champs" },
    h("span", { class: "titre-groupe" }, "Modules de calcul de ce poste"),
    ligneBool("Volume annuel (les gains passent en €/an)", "volumeActif"),
    ligneBool("Coût machine (temps × taux horaire, à côté du CPP outillage)", "coutMachineActif"),
    ligneBool("Coût du rebut", "coutRebutActif"),
    ligneBool("Pièces détachées", "piecesActif"));
  function ligneBool(libelle, cle) {
    const cb = h("input", { type: "checkbox", checked: cfg[cle] === true, onchange: e => { cfg[cle] = e.target.checked; saveData(); } });
    return h("label", { class: "champ", style: { display: "flex", gap: "10px", alignItems: "center" } }, cb, h("span", {}, libelle));
  }

  ouvrirPanneau(creation ? "Nouvelle opération" : "Fiche OP", ref.nom, [
    nom, ordre, modules,
    creation ? h("button", {
      class: "bouton primaire", onclick: () => {
        if (!o.nom) { toast("Donnez un nom à l'opération."); return; }
        ref.ops.push(o);
        saveData(); fermerPanneau(); render();
      }
    }, "Créer l'opération") : null
  ]);
}

/* ---- le scénario : la fiche et son outillage ---- */
function ouvrirPanneauScenario(ligne, ref, op, sc, enProd) {
  const creation = !sc;
  const s = sc || {
    id: uid("sc"), name: "", cycle: 100,
    baseline: enProd === true, statut: enProd === true ? "serie" : "etude",
    statutMotif: "", statutDate: "",
    emag1: false, battCotes: "DG",
    limitOverride: false, limitLabel: "Battement (mm)", limitValue: "",
    limitLabel2: "Ra (µm)", limitValue2: 0.8, critere2Actif: false,
    criteresSup: [], validationThreshold: 5, battActif: true,
    tauxRebutAnnuel: "", marpossRapport: "", tendanceRapport: "", notes: "",
    outils: [], essais: [], scrapLog: [], modifieLe: new Date().toISOString()
  };

  const nom = champ("Nom du scénario", "text", s.name, { placeholder: "Essai SL500" });
  nom.querySelector("input").addEventListener("change", e => { s.name = e.target.value; saveData(); });

  /* Le statut : verrouillé pour le scénario de production (v4.4 de l'app). */
  const statut = champSelect("Statut",
    Object.keys(STATUTS_SCENARIO).filter(k => k !== "serie" || s.baseline).map(k => ({ value: k, libelle: STATUTS_SCENARIO[k].mot })),
    s.statut, {},
    s.baseline ? "le scénario de production est en série, verrouillé — passez la main par ★ sur un autre scénario" : "");
  statut.querySelector("select").addEventListener("change", e => {
    if (s.baseline) { toast("Le scénario de production reste en série."); e.target.value = "serie"; return; }
    s.statut = e.target.value;
    if (e.target.value === "serie") {
      s.baseline = true;
      (op.scenarios || []).forEach(x => { if (x.id !== s.id && x.baseline) { x.baseline = false; if (x.statut === "serie") x.statut = "valide"; } });
    }
    saveData();
  });

  /* Les limites de conformité (battement / Ra). */
  function ligneBool(libelle, cle) {
    const cb = h("input", { type: "checkbox", checked: s[cle] === true, onchange: e => { s[cle] = e.target.checked; saveData(); } });
    return h("label", { class: "champ", style: { display: "flex", gap: "10px", alignItems: "center" } }, cb, h("span", {}, libelle));
  }
  function champNum(libelle, cle, aide) {
    const el = champ(libelle, "number", s[cle], { step: "any", min: "0" }, aide || "");
    el.querySelector("input").addEventListener("change", e => {
      s[cle] = e.target.value === "" ? "" : parseFloat(e.target.value);
      if (cle === "limitValue") s.limitOverride = e.target.value !== "";
      saveData();
    });
    return el;
  }
  const limites = h("div", { class: "groupe-champs" },
    h("span", { class: "titre-groupe" }, "Les critères de conformité"),
    ligneBool("Le battement juge la conformité", "battActif"),
    champNum("Limite de battement (mm)", "limitValue", "laisser vide : la limite de l'atelier (0,12 mm) s'applique"),
    ligneBool("Le Ra juge aussi (2ᵉ critère)", "critere2Actif"),
    champNum("Limite Ra (µm)", "limitValue2", ""),
    champNum("Essais conformes pour valider (protocole 5×)", "validationThreshold", ""));

  /* L'outillage : outils → logements, éditables en place. */
  const outillageBloc = h("div", {});
  function logementVide(nomDefaut) {
    return { id: uid("g"), nom: nomDefaut, ref: "", codeArticle: "", mabec: "", prix: "", aretes: "", charniere: "", vc: "", f: "", kappaR: "", rayonBec: "", apPiste: "", tempsCoupe: "", tempsDeplacement: "", suiviTolerance: false };
  }
  function rendreOutillage() {
    outillageBloc.innerHTML = "";
    s.outils.forEach((o, iO) => {
      const bloc = h("div", { class: "groupe-champs" },
        h("span", { class: "titre-groupe" }, "Porte-outil " + (iO + 1)));
      const num = champ("Numéro (T543)", "text", o.numero);
      num.querySelector("input").addEventListener("change", e => { o.numero = e.target.value; saveData(); });
      const desc = champ("Description", "text", o.description);
      desc.querySelector("input").addEventListener("change", e => { o.description = e.target.value; saveData(); });
      const corr = champ("Correcteur", "text", o.correcteur);
      corr.querySelector("input").addEventListener("change", e => { o.correcteur = e.target.value; saveData(); });
      bloc.appendChild(num); bloc.appendChild(desc); bloc.appendChild(corr);

      (o.logements || []).forEach((l, iL) => {
        const g = h("div", { class: "groupe-champs", style: { background: "var(--carte-2)" } },
          h("span", { class: "titre-groupe" }, "Logement " + (l.nom || (iL + 1))));
        g.appendChild(champMini(l, "nom", "Logement (D1, bol, piste…)", "text"));
        g.appendChild(champMini(l, "mabec", "MABEC (code article plaquette)", "text"));
        g.appendChild(champMini(l, "ref", "Plaquette / article", "text"));
        g.appendChild(champMini(l, "prix", "Prix de la plaquette (€)", "number"));
        g.appendChild(champMini(l, "aretes", "Arêtes", "number"));
        g.appendChild(champMini(l, "charniere", "Charnière (pièces)", "number"));
        const plus = h("details", {},
          h("summary", { style: { cursor: "pointer", color: "var(--blue)", fontSize: "13px", minHeight: "44px", lineHeight: "44px" } }, "Conditions de coupe et cycle (facultatif)"),
          champMini(l, "vc", "Vc (m/min)", "number"),
          champMini(l, "f", "f (mm/tr)", "number"),
          champMini(l, "kappaR", "κr (°)", "number"),
          champMini(l, "apPiste", "ap piste (mm)", "number"),
          champMini(l, "tempsCoupe", "Temps de coupe (s)", "number"),
          champMini(l, "tempsDeplacement", "Temps de déplacement (s)", "number"));
        g.appendChild(plus);
        g.appendChild(h("button", {
          class: "bouton petit danger", onclick: () => {
            confirmer("Retirer le logement « " + (l.nom || "?") + " » de cet outil ? Le CPP du scénario sera recalculé.",
              "Retirer", () => { o.logements.splice(iL, 1); saveData(); fermerPanneau(); ouvrirPanneauScenario(ligne, ref, op, s, false); render(); });
          }
        }, "Retirer ce logement"));
        bloc.appendChild(g);
      });

      bloc.appendChild(h("div", { class: "liste-actions" },
        h("button", { class: "bouton petit", onclick: () => {
          o.logements.push(logementVide("D" + ((o.logements || []).length + 1)));
          saveData(); fermerPanneau(); ouvrirPanneauScenario(ligne, ref, op, s, false);
        } }, "+ Logement"),
        h("button", { class: "bouton petit danger", onclick: () => {
          confirmer("Retirer le porte-outil " + o.numero + " et tous ses logements ?", "Retirer l'outil", () => {
            s.outils.splice(iO, 1); saveData(); fermerPanneau(); ouvrirPanneauScenario(ligne, ref, op, s, false); render();
          }, { danger: true });
        } }, "Retirer ce porte-outil")));
      outillageBloc.appendChild(bloc);
    });
    outillageBloc.appendChild(h("div", { class: "liste-actions" },
      h("button", { class: "bouton petit", onclick: () => {
        s.outils.push({ id: uid("t"), numero: "T" + (500 + s.outils.length + 1), correcteur: "", description: "", plan: null, pieces: [], logements: [logementVide("D1")] });
        saveData(); fermerPanneau(); ouvrirPanneauScenario(ligne, ref, op, s, false);
      } }, "+ Porte-outil")));
  }
  function champMini(obj, cle, libelle, type) {
    const el = champ(libelle, type, obj[cle], { step: "any" });
    el.querySelector("input").addEventListener("change", e => {
      obj[cle] = (type === "number" && e.target.value !== "") ? parseFloat(e.target.value) : e.target.value;
      saveData();
    });
    return el;
  }
  rendreOutillage();

  const notes = h("label", { class: "champ" },
    h("span", { class: "etiquette" }, "Notes"),
    h("textarea", { onchange: e => { s.notes = e.target.value; saveData(); } }, s.notes || ""));

  ouvrirPanneau(creation ? "Nouveau scénario" : "Fiche scénario",
    ligne.nom + " · " + ref.nom + " · " + opCodeDe(op), [
    nom, statut, limites,
    h("div", { class: "groupe-champs" }, h("span", { class: "titre-groupe" }, "L'outillage"), outillageBloc),
    notes,
    creation ? h("button", {
      class: "bouton primaire", onclick: () => {
        if (!s.name) { toast("Donnez un nom au scénario."); return; }
        op.scenarios.push(s);
        saveData(); fermerPanneau(); render();
      }
    }, "Créer le scénario") : null
  ], { large: true });
}

/* ---- l'essai : la saisie en 90 s, le reste replié ---- */
function ouvrirPanneauEssai(ligne, ref, op, sc, essai) {
  const creation = !essai;
  const e = essai || {
    id: uid("e"), titre: "", date: new Date().toISOString().slice(0, 10),
    dateFin: "", heureDebut: "", heureFin: "",
    equipe: "", operateur: "", redigePar: "",
    programme: "", programmeGauche: "", programmeDroit: "",
    maturiteBruts: "", observations: "", cloture: null,
    params: { logements: [] }, prelevements: [],
    photos: [], marpossListe: [], marposs: null, modifieLe: new Date().toISOString()
  };
  e.modifieLe = new Date().toISOString();

  /* Les logements suivis + la charnière mesurée : le cœur de la saisie. */
  const logementsBloc = h("div", { class: "groupe-champs" },
    h("span", { class: "titre-groupe" }, "Les logements suivis — la charnière mesurée fait le CPP obtenu"));
  const tousLogements = [];
  (sc.outils || []).forEach(o => (o.logements || []).forEach(l => tousLogements.push({ o: o, l: l })));
  if (!tousLogements.length) {
    logementsBloc.appendChild(h("div", { class: "note" }, "Ce scénario n'a aucun logement : posez l'outillage dans la fiche scénario avant de consigner un essai."));
  }
  tousLogements.forEach(({ o, l }) => {
    const suivi = (e.params.logements || []).find(p => p.logementId === l.id);
    if (!suivi) {
      const cb = h("input", { type: "checkbox", onchange: ev => {
        if (ev.target.checked) {
          e.params.logements.push({ logementId: l.id, logementNom: l.nom || "?", charniere: "", vc: "", f: "" });
        } else {
          e.params.logements = e.params.logements.filter(p => p.logementId !== l.id);
        }
        e.modifieLe = new Date().toISOString();
        saveData(); fermerPanneau(); ouvrirPanneauEssai(ligne, ref, op, sc, e);
      } });
      logementsBloc.appendChild(h("label", { class: "champ", style: { display: "flex", gap: "10px", alignItems: "center" } }, cb,
        h("span", {}, h("span", { class: "mono" }, o.numero + " " + (l.nom || "?")), " — " + (l.ref || "sans article"))));
      return;
    }
    const ch = champ("Charnière mesurée — " + o.numero + " " + (l.nom || "?") + " (pièces)", "number", suivi.charniere, { step: "any", min: "0" },
      "le scénario prévoyait " + (l.charniere !== "" && l.charniere != null ? fmt(l.charniere, 0) : "—"));
    ch.querySelector("input").addEventListener("change", ev => { suivi.charniere = ev.target.value === "" ? "" : parseFloat(ev.target.value); e.modifieLe = new Date().toISOString(); saveData(); });
    logementsBloc.appendChild(ch);
  });

  /* Les prélèvements : pièce, battement (D/G si la machine relève les deux côtés), Ra, usure. */
  const prelsBloc = h("div", { class: "groupe-champs" });
  function rendrePrels() {
    prelsBloc.innerHTML = "";
    prelsBloc.appendChild(h("span", { class: "titre-groupe" }, "Les prélèvements"));
    if (!(e.prelevements || []).length) {
      prelsBloc.appendChild(h("div", { class: "note" }, "Aucun prélèvement. Le battement se relève par pièce : le pire des deux côtés juge (jamais la moyenne)."));
    }
    (e.prelevements || []).forEach((p, i) => {
      const g = h("div", { class: "rangee", style: { borderBottom: "1px solid var(--filet)", paddingBottom: "8px" } });
      const mk = (libelle, cle) => {
        const el = champ(libelle, "number", p[cle], { step: "any" });
        el.querySelector("input").addEventListener("change", ev => {
          p[cle] = ev.target.value === "" ? "" : parseFloat(ev.target.value);
          e.modifieLe = new Date().toISOString();
          saveData();
        });
        return el;
      };
      g.appendChild(mk("Pièce n°", "piece"));
      if (sc.emag1) {
        g.appendChild(mk("Battement D (mm)", "battD"));
        g.appendChild(mk("Battement G (mm)", "battG"));
      } else {
        g.appendChild(mk("Battement (mm)", "batt"));
      }
      if (sc.critere2Actif) g.appendChild(mk("Ra (µm)", "valeur2"));
      const usure = champSelect("Usure plaquette", [
        { value: "", libelle: "—" }, { value: "ok", libelle: "OK" },
        { value: "limite", libelle: "limite" }, { value: "changer", libelle: "à changer" }
      ], p.usure || "");
      usure.querySelector("select").addEventListener("change", ev => { p.usure = ev.target.value; e.modifieLe = new Date().toISOString(); saveData(); });
      g.appendChild(usure);
      g.appendChild(h("button", {
        class: "bouton petit danger", onclick: () => {
          e.prelevements.splice(i, 1); e.modifieLe = new Date().toISOString();
          saveData(); fermerPanneau(); ouvrirPanneauEssai(ligne, ref, op, sc, e);
        }
      }, "×"));
      prelsBloc.appendChild(g);
    });
    prelsBloc.appendChild(h("div", { class: "liste-actions" },
      h("button", { class: "bouton petit primaire", onclick: () => {
        e.prelevements.push({ id: uid("p"), piece: "", batt: "", battD: "", battG: "", logementId: (e.params.logements[0] || {}).logementId || "", pointMesure: "Piste", usure: "", valeur2: "", valeurs: {} });
        e.modifieLe = new Date().toISOString();
        saveData(); fermerPanneau(); ouvrirPanneauEssai(ligne, ref, op, sc, e);
      } }, "+ Prélèvement")));
  }
  rendrePrels();

  /* Les photos : ajoutées sur le poste, jamais envoyées. */
  const photosBloc = h("div", { class: "groupe-champs" });
  function rendrePhotos() {
    photosBloc.innerHTML = "";
    photosBloc.appendChild(h("span", { class: "titre-groupe" }, "Les photos"));
    if (!(e.photos || []).length) photosBloc.appendChild(h("div", { class: "note" }, "Aucune photo. Elles restent sur ce poste, comme tout le reste."));
    let poids = 0;
    (e.photos || []).forEach((ph, i) => {
      const t = (ph.data || ph.src || ph.url || "");
      poids += t.length;
      const lignePh = h("div", { class: "rangee", style: { alignItems: "center", borderBottom: "1px solid var(--filet)", paddingBottom: "6px" } });
      const legende = champ("Légende", "text", ph.legende || "");
      legende.querySelector("input").addEventListener("change", ev => { ph.legende = ev.target.value; saveData(); });
      legende.style.flex = "1 1 220px";
      lignePh.appendChild(legende);
      if (t) lignePh.appendChild(h("a", { href: t, target: "_blank", style: { color: "var(--blue)", fontSize: "13px" } }, "voir"));
      lignePh.appendChild(h("button", {
        class: "bouton petit danger", onclick: () => {
          e.photos.splice(i, 1); saveData(); fermerPanneau(); ouvrirPanneauEssai(ligne, ref, op, sc, e);
        }
      }, "×"));
      photosBloc.appendChild(lignePh);
    });
    if (poids > 3 * 1024 * 1024) {
      photosBloc.appendChild(h("div", { class: "note" }, "Les photos de cet essai pèsent environ " + Math.round(poids / 1048576) + " Mo : pensez à exporter régulièrement, le stockage local n'est pas infini."));
    }
    const input = h("input", { type: "file", accept: "image/*", style: { marginTop: "8px" }, onchange: ev => {
      const fichier = ev.target.files && ev.target.files[0];
      if (!fichier) return;
      const rd = new FileReader();
      rd.onload = () => {
        e.photos.push({ id: uid("ph"), filename: fichier.name, addedAt: new Date().toISOString(), legende: "", data: rd.result });
        e.modifieLe = new Date().toISOString();
        saveData(); fermerPanneau(); ouvrirPanneauEssai(ligne, ref, op, sc, e);
      };
      rd.readAsDataURL(fichier);
    } });
    photosBloc.appendChild(h("label", { class: "champ" }, h("span", { class: "etiquette" }, "Ajouter une photo"), input));
  }
  rendrePhotos();

  /* Les champs de contexte, repliés. */
  const contexte = h("details", {},
    h("summary", { style: { cursor: "pointer", color: "var(--blue)", minHeight: "44px", lineHeight: "44px" } }, "Le contexte (équipe, programmes, fin d'essai…)"));
  const mkCtx = (libelle, cle, type) => {
    const el = champ(libelle, type || "text", e[cle]);
    el.querySelector("input").addEventListener("change", ev => { e[cle] = ev.target.value; e.modifieLe = new Date().toISOString(); saveData(); });
    contexte.appendChild(el);
  };
  mkCtx("Équipe", "equipe"); mkCtx("Opérateur", "operateur"); mkCtx("Rédigé par", "redigePar");
  mkCtx("Fin d'essai (date)", "dateFin", "date"); mkCtx("Heure début", "heureDebut", "time"); mkCtx("Heure fin", "heureFin", "time");
  mkCtx("Programme CNC", "programme");
  if (sc.emag1) { mkCtx("Programme côté gauche", "programmeGauche"); mkCtx("Programme côté droit", "programmeDroit"); }
  mkCtx("Maturité des bruts", "maturiteBruts");
  const obs = h("label", { class: "champ" },
    h("span", { class: "etiquette" }, "Observations"),
    h("textarea", { onchange: ev => { e.observations = ev.target.value; e.modifieLe = new Date().toISOString(); saveData(); } }, e.observations || ""));
  contexte.appendChild(obs);

  const titre = champ("Titre de l'essai", "text", e.titre, { placeholder: "SL500 sur T513 D1" });
  titre.querySelector("input").addEventListener("change", ev => { e.titre = ev.target.value; e.modifieLe = new Date().toISOString(); saveData(); });
  const date = champ("Date", "date", e.date);
  date.querySelector("input").addEventListener("change", ev => { e.date = ev.target.value; e.modifieLe = new Date().toISOString(); saveData(); });

  ouvrirPanneau(creation ? "Consigner un essai" : "L'essai",
    ligne.nom + " · " + opCodeDe(op) + " · " + sc.name, [
    titre, date, logementsBloc, prelsBloc, photosBloc, contexte,
    creation ? h("button", {
      class: "bouton primaire", onclick: () => {
        (sc.essais = sc.essais || []).push(e);
        saveData(); fermerPanneau(); render();
      }
    }, "Consigner l'essai") : h("button", {
      class: "bouton", onclick: () => {
        if (!(e.cloture || {}).motif) {
          confirmer("Arrêter cet essai ? Un essai arrêté est une décision — il sera affiché « arrêté » avec sa raison.",
            "Arrêter l'essai", () => {
              e.cloture = { motif: "arrêté manuellement le " + dateCourte(), date: new Date().toISOString() };
              e.modifieLe = new Date().toISOString();
              saveData(); fermerPanneau(); render();
            });
        } else {
          e.cloture = null; saveData(); toast("Essai réouvert."); fermerPanneau();
        }
      }
    }, (e.cloture || {}).motif ? "Réouvrir l'essai" : "Arrêter l'essai (avec la raison)")
  ], { large: true });
}
