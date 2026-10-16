# -*- coding: utf-8 -*-
"""Releases 4.48/4.49 + tests outilsManquants (fichier, pas de heredoc)."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

s = s.replace('const TOOL_VERSION = "4.47.1";', 'const TOOL_VERSION = "4.49.0";')

avant = """const NOUVEAUTES = [
  { version:"4.47.1", date:"28/09/2026", points:["""
apres = """const NOUVEAUTES = [
  { version:"4.49.0", date:"28/09/2026", points:[
    "<b>La feuille de route arrive.</b> Un bandeau « Coût pièce complet » en tête d'écran somme le CPP de prod de toutes les OPs de la référence, le confronte à la cible du site et montre le meilleur essai en cours par OP. La vue de synthèse ouvre sur la feuille de route : barre prod → cible avec le % de chemin parcouru, statut par OP (passé en série / validé 5× / essai en cours / prod seule), gain disponible annualisé. Et la cascade du gain ne disparaît plus silencieusement : elle explique pourquoi elle est vide quand c'est le cas."
  ]},
  { version:"4.48.0", date:"28/09/2026", points:[
    "<b>« ⊞ Compléter depuis la prod ».</b> Sur un scénario d'essai incomplet, un bouton ajoute les outils qui tournent en prod (base excel) mais manquent ici — avec aperçu et confirmation. Les outils d'essai gardent leurs conditions, les essais/prélèvements/photos ne sont pas touchés : un ajout pur, indispensable pour comparer un scénario d'essai à une prod complète sans fausser le coût pièce."
  ]},
  { version:"4.47.1", date:"28/09/2026", points:["""
assert s.count(avant) == 1
s = s.replace(avant, apres)

avant = """    /* ---- v4.46.1 : cibleCPP de référence persistée à la normalisation ---- */"""
apres = """    /* ---- v4.48 : compléter depuis la prod — rapprochement par préfixe ---- */
    {
      const dAvant = data;
      const mk = (nom, base, outils) => normalizeScenario({ id:"cc-"+nom, name:nom, baseline:base, cycle: base?100:"", outils, essais:[], scrapLog:[] });
      data = [
        mk("Prod actuelle (base excel 2026/2027)", true, [
          { id:"te1", numero:"T548 D1", logements:[{ id:"ge1", nom:"Plaquette", prix:9.56, aretes:8, charniere:50 }] },
          { id:"te2", numero:"T543 D1", logements:[{ id:"ge2", nom:"Plaquette", prix:11.87, aretes:6, charniere:30 }] },
          { id:"te3", numero:"T546 D1", logements:[{ id:"ge3", nom:"Plaquette", prix:3.68, aretes:4, charniere:60 }] }
        ]),
        mk("Essai SL500", false, [
          { id:"tt1", numero:"T548", logements:[{ id:"gt1", nom:"Piste ext.", prix:9.56, aretes:8, charniere:50 }] }
        ])
      ];
      ok("outilsManquants : T548 rapproché par préfixe -> non proposé ; T543/T546 manquants",
         outilsManquants(data[1]).map(t => t.numero), ["T543 D1", "T546 D1"]);
      ok("outilsManquants : sur la base elle-même -> rien (baseline)",
         outilsManquants(data[0]).length, 0);
      data = dAvant;
    }

    /* ---- v4.46.1 : cibleCPP de référence persistée à la normalisation ---- */"""
assert s.count(avant) == 1
s = s.replace(avant, apres)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("releases OK")
