# -*- coding: utf-8 -*-
"""Tour 89 (4.107.0) — brique A : l'UI de la décomposition dans « Scénarios en validation »."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
n0 = len(src)

def remplace(avant, apres, label):
    global src
    assert avant in src, "ANCRE INTROUVABLE : " + label
    src = src.replace(avant, apres, 1)
    print("ok :", label)

# ── les colonnes Levier vie / Levier prix + le badge condition 5 ──
remplace(
'''    const cumul = items.reduce((a, l) => a + l.gain, 0);
    corps += `<tr class="pc-grp"><td colspan="5">${escapeAttr(titre)} (${items.length}) <span class="pc-grp-tot">cumul ${grp === 2 ? "acté" : grp === 1 ? "possible" : "projeté"} : ${fmtEuroCourt(Math.round(cumul))} /an</span><br><span style="font-weight:400; font-size:11px; color:var(--ink-faint);">${escapeAttr(sous)}</span></td></tr>`;
    items.forEach(l => {
      corps += `<tr>
        <td class="mono">${escapeAttr(l.ligne)} · ${escapeAttr(l.opCode)}</td>
        <td>${escapeAttr(l.ref)}</td>
        <td><b>${escapeAttr(l.scenario)}</b></td>
        <td><span class="pc-stat ${l.cls}">${l.libelle}</span></td>
        <td class="mono" style="font-weight:600; color:${l.grp === 2 ? "var(--green)" : l.grp === 1 ? "var(--blue)" : "var(--ink-soft)"};">+ ${fmtEuroCourt(Math.round(l.gain))}<small style="color:var(--ink-faint);"> /an</small></td>
      </tr>`;
    });
  });
  return `<table class="simul-table">
    <thead><tr><th>Poste</th><th>Référence</th><th>Scénario en course</th><th>État</th><th>Économie</th></tr></thead>
    <tbody>${corps}</tbody>
  </table>`;''',

'''    const cumul = items.reduce((a, l) => a + l.gain, 0);
    corps += `<tr class="pc-grp"><td colspan="7">${escapeAttr(titre)} (${items.length}) <span class="pc-grp-tot">cumul ${grp === 2 ? "acté" : grp === 1 ? "possible" : "projeté"} : ${fmtEuroCourt(Math.round(cumul))} /an</span><br><span style="font-weight:400; font-size:11px; color:var(--ink-faint);">${escapeAttr(sous)}</span></td></tr>`;
    items.forEach(l => {
      /* v4.107 — la décomposition des leviers : ce qui vient de la VIE et ce qui
         vient du PRIX, en % et en €/an, sur le poste plaquettes. L'interaction
         (les deux leviers se renforcent ou se gênent) vit dans l'info-bulle. */
      const d = l.dec;
      const sgn = v => v >= 0 ? "+" : "−";
      const euro = v => sgn(v) + " " + fmtEuroCourt(Math.round(Math.abs(v)));
      let cellVie = "—", cellPrix = "—";
      if(d){
        const tipVie = `Durée de vie effective : ${fmt(d.vBarBase, 0)} → ${fmt(d.vBarCand, 0)} pièces par plaquette (moyenne pondérée par l\\'usage). Gain vie seule : ${euro(d.gainVieSeul)} €/an — le candidat aux PRIX de la base.`;
        const tipPrix = `Coût plaquette moyen consommée : ${fmt(d.pBarBase, 2)} → ${fmt(d.pBarCand, 2)} € (baisse de ${fmt(Math.max(0, d.prixBaissePct), 0)} %). Gain prix seul : ${euro(d.gainPrixSeul)} €/an — le candidat à la DURÉE DE VIE de la base. Interaction vie×prix : ${euro(d.interaction)} €/an (ce que les deux leviers font ensemble au-delà de la somme). Coût plaquette par pièce : ${fmt(d.PBase / l.gain > 0 ? d.PBase : 0, 3)}…`;
        cellVie = `<b style="font-size:13.5px;">${d.viePct >= 0 ? "+" : "−"}${fmt(Math.abs(d.viePct), 0)} %</b> de vie<br><span class="mono" style="color:${d.gainVieSeul >= 0 ? "var(--green)" : "var(--red)"};">${euro(d.gainVieSeul)}<small style="color:var(--ink-faint);"> /an</small></span>`;
        cellPrix = `<b style="font-size:13.5px;">${d.prixBaissePct >= 0 ? "−" : "+"}${fmt(Math.abs(d.prixBaissePct), 0)} %</b> de prix<br><span class="mono" style="color:${d.gainPrixSeul >= 0 ? "var(--green)" : "var(--red)"};">${euro(d.gainPrixSeul)}<small style="color:var(--ink-faint);"> /an</small></span>`;
      }
      const badgeCycle = l.machineExclue ? ` <span class="pc-stat attente" style="font-size:10.5px;" title="Le temps machine n\\'est pas chiffré sur ce poste : ce gain est un gain OUTILLAGE — un levier Vc/f qui rendrait du temps machine n\\'apparaît pas dedans (condition 5).">gain outillage — levier cycle non chiffré</span>` : "";
      corps += `<tr>
        <td class="mono">${escapeAttr(l.ligne)} · ${escapeAttr(l.opCode)}</td>
        <td>${escapeAttr(l.ref)}</td>
        <td><b>${escapeAttr(l.scenario)}</b></td>
        <td><span class="pc-stat ${l.cls}">${l.libelle}</span></td>
        <td title="${d ? `Durée de vie effective : ${fmt(d.vBarBase, 0)} → ${fmt(d.vBarCand, 0)} pièces/plaquette. Gain vie seule : ${euro(d.gainVieSeul)} €/an.` : "Décomposition non chiffrable : la base ou le candidat n\\'a pas de prix et de durée de vie exploitables (jamais un zéro, §3.5)."}">${cellVie}</td>
        <td title="${d ? `Prix plaquette moyen consommée : ${fmt(d.pBarBase, 2)} → ${fmt(d.pBarCand, 2)} €. Gain prix seul : ${euro(d.gainPrixSeul)} €/an. Interaction vie×prix : ${euro(d.interaction)} €/an.` : "Décomposition non chiffrable (§3.5)."}">${cellPrix}</td>
        <td class="mono" style="font-weight:600; color:${l.grp === 2 ? "var(--green)" : l.grp === 1 ? "var(--blue)" : "var(--ink-soft)"};">+ ${fmtEuroCourt(Math.round(l.gain))}<small style="color:var(--ink-faint);"> /an</small>${badgeCycle}</td>
      </tr>`;
    });
  });
  return `<table class="simul-table">
    <thead><tr><th>Poste</th><th>Référence</th><th>Scénario en course</th><th>État</th><th>Levier vie</th><th>Levier prix</th><th>Gain total /an</th></tr></thead>
    <tbody>${corps}</tbody>
  </table>
  <p class="panel-hint" style="margin-top:8px;"><b>Lire les leviers</b> : la décomposition porte sur le <b>poste plaquettes</b> seul. <b>Gain vie seul</b> = le scénario candidat aux <b>prix de la base</b> ; <b>gain prix seul</b> = le candidat à la <b>durée de vie de la base</b> ; la somme des deux dépasse le gain plaquettes de l'<b>interaction</b> (ce que les deux leviers font ensemble) — l'info-bulle de chaque colonne la donne, avec le coût plaquette par pièce de chaque côté. Le <b>gain total</b> peut différer : il couvre tous les postes communs (machine, rebut…) et reste sourcé de gainPoste, comme partout.</p>`;''',
"planScenariosHTML colonnes leviers")

io.open(p, "w", encoding="utf-8").write(src)
print("taille:", n0, "->", len(src))
