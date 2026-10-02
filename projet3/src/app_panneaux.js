/* ============================================================================
   PROJET3 — LES PROJETS, LES LIVRAISONS, LES OPTIONS, LES DONNÉES, LE RENDU
   (la fin d'app.js — l'assembler concatène dans l'ordre)
   ========================================================================== */

"use strict";

/* ---- le projet ---- */
function ouvrirPanneauProjet(pj) {
  const creation = !pj;
  const p = pj || {
    id: uid("pj"), nom: "", description: "", statut: "encours", dateCible: "",
    responsableId: "", couleur: couleurProjetLibre(ETAT),
    creePar: "", creeLe: new Date().toISOString(), modifieLe: new Date().toISOString(), tags: []
  };

  const nom = champ("Nom du projet", "text", p.nom);
  nom.querySelector("input").addEventListener("change", e => { p.nom = e.target.value; saveData(); });
  const desc = h("label", { class: "champ" },
    h("span", { class: "etiquette" }, "Description (l'objectif, les moyens)"),
    h("textarea", { onchange: e => { p.description = e.target.value; p.modifieLe = new Date().toISOString(); saveData(); } }, p.description || ""));
  const statut = champSelect("Statut",
    Object.keys(PROJET_STATUTS).map(k => ({ value: k, libelle: PROJET_STATUTS[k] })), p.statut);
  statut.querySelector("select").addEventListener("change", e => { p.statut = e.target.value; p.modifieLe = new Date().toISOString(); saveData(); });
  const cible = champ("Date cible", "date", p.dateCible);
  cible.querySelector("input").addEventListener("change", e => { p.dateCible = e.target.value; saveData(); });

  /* Le responsable : la liste gérée, plus l'ajout direct (CDC Projets v2 §2.1). */
  const respSel = champSelect("Responsable",
    [{ value: "", libelle: "— aucun responsable" }].concat((ETAT.responsables || []).map(u => ({ value: u.id, libelle: u.nom }))),
    p.responsableId);
  respSel.querySelector("select").addEventListener("change", e => {
    p.responsableId = e.target.value; p.modifieLe = new Date().toISOString(); saveData();
  });
  const nouveauResp = h("details", {},
    h("summary", { style: { cursor: "pointer", color: "var(--blue)", minHeight: "44px", lineHeight: "44px" } }, "+ Ajouter un nouveau responsable"));
  const nomResp = champ("Nom", "text", "");
  const couleurResp = champ("Couleur (elle porte la bordure de ses cartes)", "color", "#3b82f6");
  nouveauResp.appendChild(nomResp); nouveauResp.appendChild(couleurResp);
  nouveauResp.appendChild(h("button", {
    class: "bouton petit", onclick: () => {
      const nomPropre = nomResp.querySelector("input").value.trim();
      if (!nomPropre) { toast("Donnez un nom."); return; }
      const u = { id: uid("u"), nom: nomPropre, couleur: couleurResp.querySelector("input").value };
      (ETAT.responsables = ETAT.responsables || []).push(u);
      p.responsableId = u.id;
      saveData(); fermerPanneau(); ouvrirPanneauProjet(p);
    }
  }, "Créer le responsable"));

  /* La couleur du projet : assignée à la création, stable dans le temps. */
  const couleur = h("div", { class: "note" },
    h("span", { class: "note-titre" }, "Couleur du projet : "),
    h("span", { class: "badge pastille", style: { background: p.couleur || "#545e68", color: "#fff" } }, "la pastille du projet"),
    " — assignée automatiquement à la création et stable : seule la couleur du responsable se choisit, c'est elle qui porte une signification durable.");

  /* Les scénarios rattachés. */
  const rattachement = h("div", { class: "groupe-champs" });
  function rendreTags() {
    rattachement.innerHTML = "";
    rattachement.appendChild(h("span", { class: "titre-groupe" }, "Les scénarios rattachés"));
    const lie = scenariosDeProjet(ETAT, p);
    if (lie.lies.length) {
      lie.lies.forEach((x, i) => {
        rattachement.appendChild(h("div", { class: "rangee", style: { alignItems: "center", borderBottom: "1px solid var(--filet)", paddingBottom: "6px" } },
          h("span", { style: { flex: "1" } },
            h("span", { class: "mono" }, (x.ligne ? codeLigneDe(x.ligne.nom) || x.ligne.nom : "?") + " · " + opCodeDe(x.op)),
            " · " + (x.ref ? x.ref.nom : "—") + " · " + x.sc.name),
          h("button", { class: "bouton petit danger", onclick: () => {
            p.tags.splice(i, 1); p.modifieLe = new Date().toISOString();
            saveData(); fermerPanneau(); ouvrirPanneauProjet(p);
          } }, "Détacher")));
      });
    } else {
      rattachement.appendChild(h("div", { class: "note" }, "Aucun scénario rattaché. On rattache depuis un poste : ouvrez un poste, puis « Étiqueter » sur le scénario."));
    }
    if (lie.orphelins.length) {
      rattachement.appendChild(h("div", { class: "note" }, lie.orphelins.length + " étiquette(s) pointe(nt) un scénario supprimé — elles restent comptées, elles ne polluent rien."));
    }
  }
  rendreTags();

  ouvrirPanneau(creation ? "Créer un projet" : "Le projet", "", [
    nom, desc, statut, cible, respSel, nouveauResp, couleur, rattachement,
    creation ? h("button", {
      class: "bouton primaire", onclick: () => {
        if (!p.nom) { toast("Donnez un nom au projet."); return; }
        (ETAT.projets = ETAT.projets || []).push(p);
        saveData(); fermerPanneau(); aller("projets");
      }
    }, "Créer le projet") : h("button", {
      class: "bouton danger", onclick: () => {
        confirmer("Supprimer le projet « " + p.nom + " » ? Les scénarios rattachés ne sont PAS supprimés — seules les étiquettes partent.",
          "Supprimer le projet", () => {
            ETAT.projets = ETAT.projets.filter(x => x.id !== p.id);
            if (VUE.filtreProjetId === p.id) VUE.filtreProjetId = "";
            saveData(); fermerPanneau(); aller("projets");
          }, { danger: true });
      }
    }, "Supprimer ce projet")
  ], { large: true });
}

/* Étiqueter un scénario dans des projets, depuis le poste. */
function ouvrirEtiquetage(ligne, ref, op, sc) {
  const projets = ETAT.projets || [];
  const contenu = h("div", {});
  if (!projets.length) {
    contenu.appendChild(h("div", { class: "aucun" }, "Aucun projet — créez-en un d'abord."));
  }
  projets.forEach(pj => {
    const deja = projetsDeScenario(ETAT, ligne.id, ref.id, op.id, sc.id).some(x => x.id === pj.id);
    const cb = h("input", { type: "checkbox", checked: deja, onchange: ev => {
      if (ev.target.checked) {
        pj.tags.push({ ligneId: ligne.id, referenceId: ref.id, opId: op.id, scenarioId: sc.id });
        toast("Rattaché à « " + pj.nom + " »");
      } else {
        pj.tags = pj.tags.filter(t => !(t.ligneId === ligne.id && t.referenceId === ref.id && t.opId === op.id && t.scenarioId === sc.id));
      }
      pj.modifieLe = new Date().toISOString();
      saveData();
    } });
    const resp = responsableDe(ETAT, pj);
    contenu.appendChild(h("label", { class: "champ", style: { display: "flex", gap: "10px", alignItems: "center" } }, cb,
      h("span", { class: "badge pastille", style: { background: pj.couleur || "#545e68", color: "#fff" } }, pj.nom),
      h("span", { style: { color: "var(--label)", fontSize: "12px" } }, resp ? resp.nom : "")));
  });
  contenu.appendChild(h("button", { class: "bouton", onclick: () => ouvrirPanneauProjet(null) }, "+ Créer un nouveau projet"));

  ouvrirPanneau("Étiqueter « " + sc.name + " »",
    "Un scénario peut appartenir à plusieurs projets à la fois — les étiquettes ne déplacent rien.", [contenu]);
}

/* ---- les livraisons ---- */
function ouvrirLivraisons() {
  const contenu = h("div", {});
  contenu.appendChild(h("button", {
    class: "bouton primaire", onclick: () => {
      const lv = capturerLivraison(ETAT, "Livraison du " + dateCourte(), "");
      (ETAT.livraisons = ETAT.livraisons || []).unshift(lv);
      saveData(); fermerPanneau(); ouvrirLivraisons();
      toast("Instantané figé — il ne bougera plus.");
    }
  }, "Figer un instantané des gains du jour"));
  contenu.appendChild(h("div", { class: "note" }, "Une livraison est un document figé et daté : elle ne se recalcule jamais après coup. C'est elle qu'on met dans le dossier."));

  const livraisons = ETAT.livraisons || [];
  if (!livraisons.length) {
    contenu.appendChild(h("div", { class: "aucun" }, h("span", { class: "grand" }, "Aucune livraison"), "Figez la première quand les chiffres du jour valent d'être gardés."));
  }
  livraisons.forEach(lv => {
    contenu.appendChild(h("div", { class: "carte", style: { boxShadow: "none", border: "1px solid var(--filet)" } },
      h("div", { class: "c-entete" },
        h("span", { class: "c-titre" }, lv.nom),
        h("span", { class: "mono", style: { color: "var(--label)", fontSize: "12px" } }, dateHeure(lv.date)),
        h("span", { class: "droite" },
          h("button", { class: "bouton petit", onclick: () => afficherLivraison(lv) }, "Voir"))),
      h("div", { class: "c-chiffres" },
        chiffre(lv.gainsActes != null ? fmt(lv.gainsActes, 4) : "—", " €/pièce", { etiquette: "Gain acté à la date" }),
        chiffre(lv.gainsEnCours != null ? fmt(lv.gainsEnCours, 4) : "—", " €/pièce", { etiquette: "Gain en cours à la date" }))));
  });
  ouvrirPanneau("Livraisons", "Les instantanés que la hiérarchie lit", [contenu]);
}

function afficherLivraison(lv) {
  const contenu = h("div", {});
  contenu.appendChild(h("div", { class: "bandeau" },
    h("div", { class: "bloc acte" },
      h("div", { class: "etiquette" }, "Gain acté (figé)"),
      h("div", { class: "valeur" }, lv.gainsActes != null ? fmt(lv.gainsActes, 4) : "—", h("span", { class: "unite" }, "€/pièce")),
      h("div", { class: "contexte" }, "à la date du document")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Gain en cours (figé)"),
      h("div", { class: "valeur" }, lv.gainsEnCours != null ? fmt(lv.gainsEnCours, 4) : "—", h("span", { class: "unite" }, "€/pièce")),
      h("div", { class: "contexte" }, "à la date du document"))));
  const table = h("table", { class: "tableau" });
  table.appendChild(h("thead", {}, h("tr", {},
    h("th", {}, "Ligne"), h("th", {}, "Dominante"), h("th", { class: "mono" }, "CPP"), h("th", { class: "mono" }, "Décisions"))));
  const corps = h("tbody", {});
  (lv.plan || []).forEach(t => {
    corps.appendChild(h("tr", {}, h("td", {}, t.ligne), h("td", {}, t.dominante || "—"),
      h("td", { class: "mono" }, t.cpp != null ? fmt(t.cpp, 4) : "—"), h("td", { class: "mono" }, String(t.decisions || 0))));
  });
  table.appendChild(corps);
  contenu.appendChild(h("div", { class: "tableau-enveloppe" }, table));
  ouvrirPanneau(lv.nom, dateHeure(lv.date) + " — cet instantané ne se recalcule jamais", [contenu], { large: true });
}

/* ---- les options ---- */
function ouvrirOptions() {
  const contenu = h("div", {});

  const respBloc = h("div", { class: "groupe-champs" });
  function rendreResp() {
    respBloc.innerHTML = "";
    respBloc.appendChild(h("span", { class: "titre-groupe" }, "Les responsables"));
    if (!(ETAT.responsables || []).length) {
      respBloc.appendChild(h("div", { class: "note" }, "Aucun responsable. Ils se créent aussi directement dans un projet."));
    }
    (ETAT.responsables || []).forEach((u, i) => {
      const r = h("div", { class: "rangee", style: { alignItems: "center", borderBottom: "1px solid var(--filet)", paddingBottom: "6px" } });
      r.appendChild(h("input", { type: "color", value: u.couleur || "#3b82f6", onchange: ev => { u.couleur = ev.target.value; saveData(); } }));
      const nom = champ("Nom", "text", u.nom);
      nom.querySelector("input").addEventListener("change", ev => { u.nom = ev.target.value; saveData(); });
      nom.style.flex = "1 1 160px";
      r.appendChild(nom);
      r.appendChild(h("button", {
        class: "bouton petit danger", onclick: () => {
          confirmer("Retirer « " + u.nom + " » de la liste ? Les projets qui le référencent repassent « aucun responsable » — aucun projet n'est supprimé.",
            "Retirer", () => {
              ETAT.responsables.splice(i, 1);
              (ETAT.projets || []).forEach(pj => { if (pj.responsableId === u.id) pj.responsableId = ""; });
              saveData(); fermerPanneau(); ouvrirOptions();
            }, { danger: true });
        }
      }, "×"));
      respBloc.appendChild(r);
    });
    respBloc.appendChild(h("div", { class: "liste-actions" },
      h("button", { class: "bouton petit", onclick: () => {
        (ETAT.responsables = ETAT.responsables || []).push({ id: uid("u"), nom: "Nouveau responsable", couleur: "#3b82f6" });
        saveData(); ouvrirOptions();
      } }, "+ Responsable")));
  }
  rendreResp();
  contenu.appendChild(respBloc);
  contenu.appendChild(h("div", { class: "note" },
    "La bordure gauche d'une carte de projet porte la personne ; la pastille porte le projet. Deux informations différentes, deux axes visuels distincts.",
    h("br"), "Les modules de calcul (volume, coût machine, rebut, pièces détachées) se règlent poste par poste : fiche OP dans le poste."));

  ouvrirPanneau("Options", "Le réglage ponctuel", [contenu]);
}

/* ---- les données ---- */
function ouvrirPanneauDonnees() {
  const contenu = h("div", {});

  contenu.appendChild(h("div", { class: "groupe-champs" },
    h("span", { class: "titre-groupe" }, "Exporter"),
    h("p", { style: { fontSize: "13.5px", color: "var(--body)", marginTop: "0" } },
      "Un fichier JSON complet : tout ce qui est ici, photos comprises. Il ne part nulle part — il se passe de main en main."),
    h("button", { class: "bouton primaire", onclick: exporterEtat }, "Exporter le suivi")));

  const importBloc = h("div", { class: "groupe-champs" },
    h("span", { class: "titre-groupe" }, "Importer"));
  const input = h("input", { type: "file", accept: ".json,application/json", style: { marginTop: "8px" } });
  input.addEventListener("change", ev => {
    const fichier = ev.target.files && ev.target.files[0];
    if (!fichier) return;
    const rd = new FileReader();
    rd.onload = () => {
      let source;
      try { source = JSON.parse(rd.result); }
      catch (e) { toast("Ce fichier n'est pas un JSON lisible."); return; }
      proposerImport(source, fichier.name);
    };
    rd.readAsText(fichier);
  });
  importBloc.appendChild(h("p", { style: { fontSize: "13.5px", color: "var(--body)", marginTop: "0" } },
    "Lit un export de cet outil (format 9) ou de l'app de production (formats 5 à 8 — tout ce qu'elle a jamais produit). "
    + "La migration est sans perte : photos, plans, relevés Marposs et journal de rebut passent aussi. Le fichier est lu sur ce poste, rien n'est envoyé."));
  importBloc.appendChild(input);
  contenu.appendChild(importBloc);

  ouvrirPanneau("Données", "Tout reste sur ce poste", [contenu]);
}

function exporterEtat() {
  ETAT.exporteLe = new Date().toISOString();
  ETAT.exportePar = "";
  const blob = new Blob([JSON.stringify(ETAT, null, 1)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "SuiviOptimisation_v3_" + new Date().toISOString().slice(0, 10).replace(/-/g, "") + ".json";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
  toast("Export téléchargé — passez-le à qui doit fusionner.");
}

/* Le choix d'import, avec le rapport qui compte et nomme. */
function proposerImport(source, nomFichier) {
  pousserSecours();
  const mig = normaliserEtat(source);
  if (!mig.ok) {
    ouvrirPanneau("Import impossible", nomFichier, [
      h("div", { class: "note" }, mig.erreur),
      h("p", { style: { fontSize: "13.5px", color: "var(--body)" } },
        "Ce fichier n'a pas la forme d'un export du suivi. Aucune donnée n'a été touchée ; un instantané de secours a été pris avant la tentative.")
    ]);
    return;
  }
  const r = mig.rapport;
  const rapport = h("div", { class: "note" },
    h("span", { class: "note-titre" }, "Ce qui entre :"),
    h("ul", { style: { margin: "6px 0 0 18px", padding: 0 } },
      h("li", {}, r.lignes + " ligne(s), " + r.references + " référence(s), " + r.ops + " opération(s)"),
      h("li", {}, r.scenarios + " scénario(s), " + r.outils + " porte-outil(s), " + r.logements + " logement(s)"),
      h("li", {}, r.essais + " essai(s), " + r.prelevements + " prélèvement(s)"),
      h("li", {}, r.photos + " photo(s), " + r.plans + " plan(s) de porte-outil, " + r.marposs + " relevé(s) Marposs, " + r.scrapLog + " entrée(s) de rebut"),
      h("li", {}, r.projets + " projet(s) (" + r.etiquettes + " étiquettes), " + r.responsables + " responsable(s)"),
      h("li", {}, r.livraisons + " livraison(s) figée(s), " + r.backlog + " entrée(s) de journal"),
      r.formatSource !== null ? h("li", {}, "format d'origine : " + r.formatSource + (r.toolVersion ? " (app " + r.toolVersion + ")" : "")) : null));
  const avert = (r.avertissements || []).map(a => h("div", { class: "note", style: { borderLeft: "3px solid var(--ambre)" } }, a));

  const contenu = [
    h("p", { style: { fontSize: "14px" } }, h("span", { class: "surbrillance" }, nomFichier)),
    rapport,
    avert,
    h("div", { class: "liste-actions" },
      h("button", {
        class: "bouton primaire", onclick: () => {
          const f = fusionnerEtat(ETAT, mig.etat);
          ETAT = f.etat;
          SOURCE_IMPORT = "fusion avec " + nomFichier + " (" + dateCourte() + ")";
          saveData(); fermerPanneau(); render();
          toast("Fusion : " + f.rapport.essaisAjoutes + " essai(s) ajouté(s), "
            + f.rapport.essaisGagnesArrivee + " mis à jour, " + f.rapport.essaisGardesLocaux + " gardé(s) du local.");
        }
      }, "Fusionner (recommandé)"),
      h("button", {
        class: "bouton danger", onclick: () => {
          confirmer("Remplacer TOUT l'état courant par ce fichier ? Les données locales actuelles ne restent que dans l'instantané de secours.",
            "Tout remplacer", () => {
              ETAT = mig.etat;
              SOURCE_IMPORT = "import complet de " + nomFichier + " (" + dateCourte() + ")";
              saveData(); fermerPanneau(); aller("accueil");
            }, { danger: true });
        }
      }, "Remplacer tout"))
  ];
  ouvrirPanneau("Importer", "Un instantané de secours a été pris avant ce choix", contenu, { large: true });
}

/* ---- la zone rouge : les instantanés ---- */
function ouvrirSecours() {
  const pile = lireSecours();
  const contenu = h("div", {});
  if (!pile.length) {
    contenu.appendChild(h("div", { class: "aucun" }, "Aucun instantané. Les secours se prennent avant chaque import, fusion ou réinitialisation."));
  }
  pile.forEach(s => {
    const mig = normaliserEtat(s.etat);
    const r = mig.ok ? mig.rapport : null;
    contenu.appendChild(h("div", { class: "carte", style: { boxShadow: "none", border: "1px solid var(--filet)" } },
      h("div", { class: "c-entete" },
        h("span", { class: "c-titre" }, "Instantané du " + dateHeure(s.date)),
        h("span", { class: "droite liste-actions", style: { margin: 0 } },
          h("button", {
            class: "bouton petit", onclick: () => {
              confirmer("Restaurer cet instantané ? L'état courant sera d'abord poussé au fond du tiroir des secours.",
                "Restaurer", () => {
                  pousserSecours();
                  ETAT = s.etat;
                  SOURCE_IMPORT = "instantané restauré du " + dateCourte();
                  saveData(); fermerPanneau(); aller("accueil");
                });
            }
          }, "Restaurer"))),
      r ? h("div", { style: { color: "var(--label)", fontSize: "12.5px" } },
        r.lignes + " ligne(s) · " + r.scenarios + " scénario(s) · " + r.essais + " essai(s) · " + r.projets + " projet(s)") : null));
  });
  ouvrirPanneau("Restaurer un instantané", "Zone rouge — chaque restauration est réfléchie", [contenu]);
}

/* ============================================================================
   LE RENDU ET LE DÉMARRAGE
   ========================================================================== */

function render() {
  const racine = document.getElementById("app");
  if (!racine) return;
  racine.innerHTML = "";

  let page;
  if (VUE.ecran === "accueil") page = renderAccueil();
  else if (VUE.ecran === "ligne") page = renderLigne();
  else if (VUE.ecran === "poste") page = renderPoste();
  else if (VUE.ecran === "emporter") page = renderEmporter();
  else if (VUE.ecran === "projets") page = renderProjets();
  else page = renderAccueil();

  racine.appendChild(topbarDOM());
  racine.appendChild(page);
  racine.appendChild(piedDOM());
}

/* Le démarrage : le thème d'abord (pas de flash), l'état ensuite, l'écran enfin.
   Toute globale est déclarée avant usage — le piège TDZ de l'ancienne app
   (repli silencieux sur l'exemple, zéro message) ne doit pas se reproduire. */
function demarrer() {
  try {
    const t = localStorage.getItem(THEME_KEY);
    document.documentElement.setAttribute("data-theme", t === "nuit" ? "nuit" : "jour");
  } catch (e) { document.documentElement.setAttribute("data-theme", "jour"); }
  chargerEtatInitial();
  render();
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", demarrer);
  else demarrer();
}
