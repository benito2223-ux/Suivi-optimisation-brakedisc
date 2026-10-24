# -*- coding: utf-8 -*-
"""Tour 89 (4.107.0) — brique A : la décomposition des leviers (vie / prix).
Cinq conditions d'Hermes :
  1. décomposer le SEUL poste « plaquettes » (jamais machine/rebut/pièces) ;
  2. l'enveloppe est le périmètre déjà calculé par bilanAnnuel (source unique) ;
  3. les hors course sont exclus en amont par gainPoste (rien de nouveau) ;
  4. base sans prix ou sans DDV exploitable → « — », jamais 0 (§3.5) ;
  5. cycle non chiffré → badge « gain outillage — levier cycle non chiffré ».
Le piège d'appariement est évité par construction : on décompose sur les
TOTAUX plaquettes (prix moyen pondéré par l'usage × plaquettes par pièce),
jamais logement par logement."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
n0 = len(src)

def remplace(avant, apres, label):
    global src
    assert avant in src, "ANCRE INTROUVABLE : " + label
    src = src.replace(avant, apres, 1)
    print("ok :", label)

# ── 1. la fonction pure, dans la famille du Plan (avant planRecapGains) ──
remplace("function planRecapGains(){",
'''/* --- 1ter. v4.107 — LA DÉCOMPOSITION DES LEVIERS (brique A) --------------
   Benjamin (23/10) : « montrer qu'une amélioration de durée de vie de 30 %
   peut générer davantage d'économies qu'une simple baisse du prix ». Le
   poste plaquettes d'un scénario = prix moyen pondéré par l'usage (p̄) ×
   plaquettes consommées par pièce (q) : P = p̄ × q, sans appariement des
   logements (Hermes : jamais logement par logement — les outils peuvent
   différer). Décomposition exacte à trois termes :
     gain prix seul  = (p̄_base − p̄_cand) × q_base × volume   (usage de la base)
     gain vie seul   = p̄_base × (q_base − q_cand) × volume    (prix de la base)
     interaction     = (p̄_base − p̄_cand) × (q_base − q_cand) × volume
     et gainPrix + gainVie − interaction = gain plaquettes, EXACTEMENT.
   Condition 1 (Hermes) : le poste PLAQUETTES seul — machine, rebut et pièces
   détachées restent dans le gain total, jamais dans ces trois termes.
   Condition 4 : base ou candidat sans prix/DDV exploitable → null (« — »). */
function decompositionLeviers(prodSc, candSc, volume){
  if(!prodSc || !candSc || !(volume > 0)) return null;
  const cote = sc => {
    let sommePV = 0, sommeQ = 0, n = 0;
    (sc.outils || []).forEach(o => (o.logements || []).forEach(l => {
      const pr = parseFloat(l.prix), a = parseFloat(l.aretes), c = parseFloat(l.charniere);
      if(!pr || !a || !c || !(pr > 0) || !(a > 0) || !(c > 0)) return;   /* même filtre que posCost */
      sommePV += pr / (a * c);
      sommeQ += 1 / (a * c);
      n++;
    }));
    if(!n || !(sommeQ > 0)) return null;
    return { P: sommePV, q: sommeQ, pBar: sommePV / sommeQ, vBar: 1 / sommeQ };
  };
  const b = cote(prodSc), c = cote(candSc);
  if(!b || !c) return null;
  return {
    PBase: b.P * volume, PCand: c.P * volume,
    pBarBase: b.pBar, pBarCand: c.pBar, vBarBase: b.vBar, vBarCand: c.vBar,
    gainPrixSeul: (b.pBar - c.pBar) * b.q * volume,
    gainVieSeul: b.pBar * (b.q - c.q) * volume,
    interaction: (b.pBar - c.pBar) * (b.q - c.q) * volume,
    gainPlaquettes: (b.P - c.P) * volume,
    viePct: (c.vBar / b.vBar - 1) * 100,
    prixBaissePct: (b.pBar - c.pBar) / b.pBar * 100
  };
}

function planRecapGains(){''', "fonction decompositionLeviers")

# ── 2. gainPoste : porter le périmètre partiel dans refs (condition 5) ──
remplace('''    refs.push({ ref: b.ref, prodSc, meilleur, tBase, gain, serie,
                volume: volumeAnnuel(b.ref, b.op.config), essaiOuvert: (meilleur && (meilleur.sc.essais || []).length) || false });''',
'''    /* v4.107 — le périmètre partiel voyage avec la référence : la brique A doit
       savoir dire « gain outillage — levier cycle non chiffré » quand le temps
       machine est exclu de la comparaison (condition 5, Hermes). */
    refs.push({ ref: b.ref, prodSc, meilleur, tBase, gain, serie,
                volume: volumeAnnuel(b.ref, b.op.config), essaiOuvert: (meilleur && (meilleur.sc.essais || []).length) || false,
                perimetrePartiel: an ? (an.perimetrePartiel || []) : [] });''', "gainPoste refs + perimetrePartiel")

# ── 3. planScenariosHTML : la décomposition dans chaque ligne ──
remplace('''    lignesSc.push({ grp, cls, libelle,
      ligne: p.ligne, opCode: p.opCode, ref: (r.ref && r.ref.nom) || "?",
      scenario: sc.name || "Sans nom", gain: r.gain });''',
'''    lignesSc.push({ grp, cls, libelle,
      ligne: p.ligne, opCode: p.opCode, ref: (r.ref && r.ref.nom) || "?",
      scenario: sc.name || "Sans nom", gain: r.gain,
      dec: decompositionLeviers(r.prodSc, r.meilleur.sc, r.volume),
      machineExclue: (r.perimetrePartiel || []).indexOf("temps machine") > -1 });''', "planScenariosHTML + dec")

io.open(p, "w", encoding="utf-8").write(src)
print("taille:", n0, "->", len(src))
