# -*- coding: utf-8 -*-
"""v4.49.3 — pop-up de première ouverture (message base 2026/2027 + geste de mise à jour)."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# 1. message de première ouverture, affiché une fois par poste
avant = """// en dernier : l'ecran doit etre pret derriere la fenetre des nouveautes
verifierNouveautes();"""
apres = """// en dernier : l'ecran doit etre pret derriere la fenetre des nouveautes
verifierNouveautes();
/* v4.49.3 — message de première ouverture après la mise en place de la base 2026/2027.
   Une fois par poste (drapeau local). Dit le geste critique : une version ancienne de
   l'application efface les cibles de coût au partage — vérifier la version en bas. */
(async function messagePremiereOuverture(){
  const CLE = "spk_msg_base_2026";
  let dejaVu = false;
  try{ dejaVu = localStorage.getItem(CLE) === "1"; }catch(e){}
  if(dejaVu) return;
  const ok = await ouvrirDialogue({
    titre: "Bienvenue dans la base 2026/2027",
    html: dlgTexte(
      "La base de départ est en place : les 6 références de l'atelier, avec leurs outils de prod complets (OP par OP), les références plaquettes ISO, les codes article MABEC et les cibles de coût pièce du site." +
      "\\n\\nLes nouveaux écrans : le coût pièce complet et la feuille de route prod → cible (vue de synthèse), les scénarios d'essai complétés depuis la prod, les outils simultanés en ambre." +
      "\\n\\nGeste important : regarde la version en bas de page — elle doit indiquer v" + TOOL_VERSION + ". Si une version plus ancienne s'affiche, ferme complètement l'application et rouvre-la connectée à Internet (elle se met à jour toute seule). Une version ancienne peut effacer les cibles de coût au moment du partage."),
    sansAnnuler: true, okLabel: "Compris"
  });
  try{ localStorage.setItem(CLE, "1"); }catch(e){}
})();
"""
assert s.count(avant) == 1, "ancre init"
s = s.replace(avant, apres)

# 2. version + NOUVEAUTES (attention : points:[ SANS guillemet parasite)
s = s.replace('const TOOL_VERSION = "4.49.2";', 'const TOOL_VERSION = "4.49.3";')
avant = 'const NOUVEAUTES = [\n  { version:"4.49.2", date:"28/09/2026", points:['
apres = '''const NOUVEAUTES = [
  { version:"4.49.3", date:"29/09/2026", points:[
    "<b>Message de bienvenue à la première ouverture.</b> Un écran d'accueil présente la base 2026/2027 et le geste de mise à jour de l'application (une version ancienne efface les cibles de coût au partage). Affiché une fois par poste."
  ]},
  { version:"4.49.2", date:"28/09/2026", points:['''
assert s.count(avant) == 1, "ancre NOUVEAUTES"
s = s.replace(avant, apres)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("4.49.3 OK")
