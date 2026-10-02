/* ============================================================================
   PROJET3 — LE HARNAIS DE TEST, partagé par les trois suites.
   Règle constitutionnelle §6.10 : 0 échec ≠ vert. On compte les tests
   EXÉCUTÉS, et la suite doit aller jusqu'au bout — un plantage en cours de
   route est une suite rouge, pas une suite muette.
   ========================================================================== */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

/* Charge un fichier source tel quel — pas de copie, pas de re-définition —
   et renvoie les symboles demandés. */
function charger(chemin, noms) {
  const src = fs.readFileSync(path.resolve(__dirname, "..", chemin), "utf8");
  return (new Function(src + "\nreturn {" + noms.join(",") + "};")).call(globalThis);
}

function empreinte(chemin) {
  return crypto.createHash("sha256").update(fs.readFileSync(path.resolve(__dirname, "..", chemin))).digest("hex");
}

/* L'assertion : compte TOUJOURS le test, même en cas de plantage — un test
   qui crève avant son `ok` est un test exécuté et rouge, jamais un silence. */
function creerJuge(titre) {
  let total = 0, echecs = 0, plantages = 0;
  const details = [];
  function fail(nom, obtenu, attendu) {
    echecs++;
    details.push(nom);
    console.log("  ECHEC " + nom + " — obtenu " + JSON.stringify(obtenu) +
                ", attendu " + JSON.stringify(attendu));
  }
  function ok(nom, obtenu, attendu, tol) {
    total++;
    let bon;
    if (typeof attendu === "number" && typeof obtenu === "number" && tol !== undefined) {
      bon = Math.abs(obtenu - attendu) <= tol;
    } else {
      bon = JSON.stringify(obtenu) === JSON.stringify(attendu);
    }
    if (!bon) fail(nom, obtenu, attendu);
  }
  /* Un test qui doit lever : s'il ne lève pas, il échoue. */
  function leve(nom, fn) {
    total++;
    try { fn(); fail(nom, "aucune exception", "une exception"); }
    catch (e) { /* attendu */ }
  }
  /* Un bloc de test protégé : une exception y est comptée plantage et rouge. */
  function bloc(nom, fn) {
    total++;
    try { fn(); }
    catch (e) {
      plantages++;
      echecs++;
      details.push(nom + " (plantage : " + e.message + ")");
      console.log("  PLANTAGE " + nom + " — " + e.message);
    }
  }
  function finaliser() {
    console.log("\n" + "=".repeat(64));
    console.log(titre + " : " + total + " tests exécutés | " + echecs + " échecs (" + plantages + " plantage(s))");
    const vert = total > 0 && echecs === 0 && plantages === 0;
    console.log(vert ? "TOUT EST VERT" : "*** LA SUITE EST ROUGE ***");
    return vert;
  }
  return { ok, leve, bloc, fail, finaliser, total: () => total, echecs: () => echecs };
}

module.exports = { charger, empreinte, creerJuge };
