# -*- coding: utf-8 -*-
"""Réécrit proprement le bloc handler outils-completer (bornes, pas de matching interne)."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

debut = s.find('  /* v4.48 — compléter depuis la prod (base excel) : ajout SEUL, jamais de remplacement */')
assert debut > 0, "borne debut introuvable"
fin = s.find('  /* v4.23 — la tuile du volume annuel', debut)
if fin < 0:
    fin = s.find("root.querySelectorAll('.foot-cell-annuel')", debut)
assert fin > debut, "borne fin introuvable"

bloc = '''  /* v4.48 — compléter depuis la prod (base excel) : ajout SEUL, jamais de remplacement */
  root.querySelectorAll(".outils-completer").forEach(el => {
    el.addEventListener("click", () => {
      const manquants = outilsManquants(sc);
      if(!manquants.length) return;
      const liste = manquants.map(t => "\\u00b7 " + (t.numero || "outil sans n\\u00b0") + ((t.logements||[]).length > 1 ? " (" + t.logements.length + " logements)" : "")).join("\\n");
      dialogueConfirmer("Compl\\u00e9ter ce sc\\u00e9nario avec " + manquants.length + " outil(s) de la prod (base excel) ?\\n\\n" + liste + "\\n\\nVos outils d'essai gardent leurs conditions \\u2014 seuls les outils manquants sont ajout\\u00e9s, tels qu'ils tournent en prod. Les essais, pr\\u00e9l\\u00e8vements et photos enregistr\\u00e9s ne sont pas touch\\u00e9s.",
        { titre: "Compl\\u00e9ter depuis la prod ?", okLabel: "Compl\\u00e9ter" }).then(ok => {
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
s = s[:debut] + bloc + s[fin:]
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("handler réécrit proprement")
