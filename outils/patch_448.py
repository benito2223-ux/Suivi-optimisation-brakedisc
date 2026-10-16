# -*- coding: utf-8 -*-
"""Patch v4.48 : Compléter depuis la prod + cascade toujours rendue."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# 1. fonctions près de copieDepuisPossible
avant = """function copieDepuisPossible(sc){
  const base = baselineScenario();
  return !!(base && base.id !== sc.id && (base.outils || []).length);
}"""
apres = avant + """
/* v4.48 — le scénario « Prod actuelle (base excel) » du même OP : la base économique
   figée, source du complément d'outils pour les scénarios d'essai incomplets. */
function scenarioBaseExcel(sc){
  return (data || []).find(x => x.id !== sc.id && /base excel/i.test(x.name || "")) || null;
}
/* v4.48 — outils de la base excel absents du scénario. Rapprochement par préfixe de
   numéro (T548 ↔ T548 D1 = le même outil : la convention de nommage diffère entre les
   scénarios de Matis et l'excel). Un outil déjà présent à l'essai n'est JAMAIS remplacé :
   ses conditions d'essai font foi ; seuls les manquants seront ajoutés. */
function outilsManquants(sc){
  const base = scenarioBaseExcel(sc);
  if(!base || sc.baseline) return [];
  const prefixe = n => String(n || "").trim().toLowerCase().split(/\\s+/)[0] || "?";
  const dispo = {};
  (sc.outils || []).forEach(t => { const p = prefixe(t.numero); dispo[p] = (dispo[p] || 0) + 1; });
  const manquants = [];
  const restants = Object.assign({}, dispo);
  (base.outils || []).forEach(t => {
    const p = prefixe(t.numero);
    if((restants[p] || 0) > 0){ restants[p]--; return; }
    manquants.push(t);
  });
  return manquants;
}"""
assert s.count(avant) == 1, "copieDepuisPossible"
s = s.replace(avant, apres)

# 2. bouton dans posFiches
avant = '    ${interactive && copieDepuisPossible(sc) ? `<button class="ghost outils-copier" data-id="${sc.id}" style="margin-top:10px;">'
assert s.count(avant) == 1, "ligne outils-copier"
i = s.find(avant)
fin_ligne = s.find("\n", i)   # fin de la ligne copier COMPLETE (après son } fermant)
assert fin_ligne > 0
bouton = ('\n    ${interactive && outilsManquants(sc).length ? `<button class="ghost outils-completer" data-id="${sc.id}"'
          ' style="margin-top:10px;" title="Ajouter à ce scénario les outils qui tournent en prod mais manquent ici (base excel) — '
          "les outils d'essai et les essais enregistrés ne sont pas touchés. Comparer un scénario incomplet à une prod complète fausse le coût pièce."
          '">⊞ Compléter depuis la prod (${outilsManquants(sc).length} outil${outilsManquants(sc).length>1?"s":""} manquant${outilsManquants(sc).length>1?"s":""})</button>` : ""}')
bouton = bouton + "}"
s = s[:fin_ligne] + bouton + s[fin_ligne:]

# 3. handler : insérer APRÈS le handler .essai-lp-add complet (borne fiable)
#    → on s'insère juste avant le commentaire v4.25 essai-cloture
ancre = '  /* v4.25 — clôture d\'essai (arrêt anticipé) */'
assert s.count(ancre) == 1, "ancre v4.25"
handler = '''  /* v4.48 — compléter depuis la prod (base excel) : ajout SEUL, jamais de remplacement */
  root.querySelectorAll(".outils-completer").forEach(el => {
    el.addEventListener("click", () => {
      const manquants = outilsManquants(sc);
      if(!manquants.length) return;
      const liste = manquants.map(t => "\\u00b7 " + (t.numero || "outil sans n\\u00b0") + ((t.logements||[]).length > 1 ? " (" + t.logements.length + " logements)" : "")).join("\\n");
      dialogueConfirmer("Compl\\u00e9ter ce sc\\u00e9nario avec " + manquants.length + " outil(s) de la prod (base excel) ?\\n\\n" + liste + "\\n\\nVos outils d'essai gardent leurs conditions — seuls les outils manquants sont ajoutés, tels qu'ils tournent en prod. Les essais, prélèvements et photos enregistrés ne sont pas touchés.",
        { titre: "Compléter depuis la prod ?", okLabel: "Compléter" }).then(ok => {
        if(!ok) return;
        manquants.forEach(src => {
          const copie = JSON.parse(JSON.stringify(src));
          copie.id = "t" + Math.random().toString(36).slice(2);
          copie.plan = null;
          copie.logements = (copie.logements || []).map(l => Object.assign(l, { id: "g" + Math.random().toString(36).slice(2) }));
          copie.pieces = (copie.pieces || []).map(pc => Object.assign(pc, { id: "pc" + Math.random().toString(36).slice(2) }));
          sc.outils.push(copie);
        });
        saveData(); render();
      });
    });
  });

'''
s = s.replace(ancre, handler + ancre)

# 4. cascade : toujours rendue
avant = """  const actif = data.find(sc => sc.id === activeId);
  if(!actif || actif.id === base.id) return "";
  const cb = coutsDetail(base), ca = coutsDetail(actif);
  if(cb.total === null || ca.total === null || !cb.multiPoste) return "";"""
apres = """  const actif = data.find(sc => sc.id === activeId);
  /* v4.48 — la cascade ne disparaît plus silencieusement : quand le scénario ouvert EST
     la base ou qu'aucun poste n'est chiffrable, le bloc reste visible et dit pourquoi —
     une barre absente se lit comme un bug, pas comme une absence d'écarts. */
  if(!actif || actif.id === base.id){
    return `<div class="synthese-block"><h3>Cascade du gain — d'où vient l'économie</h3>
      <p class="chart-empty">Le scénario ouvert est la base de comparaison — ouvrez un scénario d'essai pour voir d'où vient chaque euro économisé, poste par poste.</p></div>`;
  }
  const cb = coutsDetail(base), ca = coutsDetail(actif);
  if(cb.total === null || ca.total === null) return "";"""
assert s.count(avant) == 1, "cascade gate"
s = s.replace(avant, apres)

avant = """  if(!postes.length) return "";
  const gainPiece = cb.total - ca.total;"""
apres = """  if(!postes.length){
    return `<div class="synthese-block"><h3>Cascade du gain — d'où vient l'économie</h3>
      <p class="chart-empty">${escapeAttr(actif.name)} et la base ont des coûts identiques poste par poste — aucun écart à détailler.</p></div>`;
  }
  const gainPiece = cb.total - ca.total;"""
assert s.count(avant) == 1, "cascade postes vides"
s = s.replace(avant, apres)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("4.48 OK")
