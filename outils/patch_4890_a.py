# -*- coding: utf-8 -*-
"""Patch v4.89.0 partie A (v2, ancres mono-ligne) : suggestions a la saisie."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# ── 1. fonctions pures, devant catalogueRendu ────────────────────────────────
rep("function catalogueRendu(){",
'''/* v4.89 — LES SUGGESTIONS À LA SAISIE : l'autocomplete du catalogue.
   Taper un MABEC ou un ISO dans un logement propose les articles connus
   (datalist natif — zéro framework) et remplit d'un changement : le MABEC,
   le prix (toujours — un MABEC = un prix), l'ISO, les arêtes et la durée de
   vie SI VIDES. Ce qui est saisi à la main n'est jamais écrasé. */
function catalogueSuggestion(mabec){
  const n = String(mabec || "").trim().toUpperCase().replace(/\\s+/g, " ");
  if(!n) return null;
  return catalogue.find(a => a.mabec === n) || null;
}

function catalogueParIso(iso){
  const n = String(iso || "").trim().toUpperCase().replace(/\\s+/g, " ");
  if(!n) return null;
  return catalogue.find(a => String(a.iso || "").toUpperCase().replace(/\\s+/g, " ").split(" | ").some(x => x === n)) || null;
}

function appliquerSuggestionCatalogue(l, entry){
  if(!l || !entry) return [];
  const mods = [];
  const vide = v => v === "" || v == null;
  const isoUnique = (entry.iso && entry.iso.indexOf(" | ") === -1) ? entry.iso : "";
  const poser = (champ, valeur, toujours) => {
    if(valeur === "" || valeur == null) return;
    if(!toujours && vide(l[champ]) === false) return;
    if(String(l[champ]) === String(valeur)) return;
    l[champ] = valeur;
    mods.push(champ);
  };
  poser("codeArticle", entry.mabec, true);
  poser("prix", entry.prix, true);
  poser("ref", isoUnique, false);
  poser("aretes", entry.aretes, false);
  poser("charniere", entry.ddv, false);
  return mods;
}

function renderCatalogueDatlists(){
  const mabec = document.getElementById("catMabec");
  const iso = document.getElementById("catIso");
  if(!mabec || !iso) return;
  mabec.innerHTML = catalogue.map(a => `<option value="${escapeAttr(a.mabec)}">${escapeAttr(a.iso || "")}</option>`).join("");
  const isos = new Set();
  catalogue.forEach(a => String(a.iso || "").split(" | ").forEach(x => { if(x.trim()) isos.add(x.trim()); }));
  iso.innerHTML = [...isos].map(x => `<option value="${escapeAttr(x)}">`).join("");
}

function catalogueRendu(){''')

# ── 2. les datalists dans le DOM ─────────────────────────────────────────────
rep('<div class="panel panel-large" id="planPanel" hidden></div>',
'''<div class="panel panel-large" id="planPanel" hidden></div>
  <datalist id="catMabec"></datalist>
  <datalist id="catIso"></datalist>''')

# ── 3. rendu au demarrage + a l'ouverture du catalogue ───────────────────────
rep("function renderCatalogue(){",
    "function renderCatalogue(){ renderCatalogueDatlists();")
rep('try{ renderPoidsFooter((localStorage.getItem(STORAGE_KEY) || "").length); installerClickPoids(); }catch(e){}',
'''try{ renderCatalogueDatlists(); }catch(e){}
try{ renderPoidsFooter((localStorage.getItem(STORAGE_KEY) || "").length); installerClickPoids(); }catch(e){}''')

# ── 4. les attributs list= sur les champs du logement ────────────────────────
rep('''${champHTML("Référence plaquette", `<input class="cell ref" ${base("ref")} value="${escapeAttr(l.ref)}" placeholder="CNGX 120716 T02020 LKT640">`, "oc-large")}''',
'''${champHTML("Référence plaquette", `<input class="cell ref" ${base("ref")} list="catIso" value="${escapeAttr(l.ref)}" placeholder="CNGX 120716 T02020 LKT640" title="La désignation ISO de la plaquette — l'autocomplete propose celles du catalogue.">`, "oc-large")}''')
rep('''${champHTML("MABEC <span>code article</span>", `<input class="cell ref" ${base("codeArticle")} value="${escapeAttr(l.codeArticle)}" placeholder="ex. IM02 209 560" title="Le numéro d'article du classeur de Matis (colonne MABEC). C'est lui qui relie le suivi au classeur : saisis-le tel quel.">`, "oc-moyen")}''',
'''${champHTML("MABEC <span>code article</span>", `<input class="cell ref" ${base("codeArticle")} list="catMabec" value="${escapeAttr(l.codeArticle)}" placeholder="ex. IM02 209 560" title="Le numéro d'article du classeur de Matis (colonne MABEC). L'autocomplete propose ceux du catalogue et remplit prix, arêtes, durée de vie.">`, "oc-moyen")}''')

# ── 5. le crochet dans writeFieldValue ────────────────────────────────────────
rep('''  } else if(outilId && logementId){
    const o = sc.outils.find(x => x.id === outilId);
    const l = o && o.logements.find(x => x.id === logementId);
    if(l) l[field] = val;
  } else if(outilId){''',
'''  } else if(outilId && logementId){
    const o = sc.outils.find(x => x.id === outilId);
    const l = o && o.logements.find(x => x.id === logementId);
    if(l){
      l[field] = val;
      /* v4.89 — LA SUGGESTION : MABEC ou ISO saisi → le catalogue remplit le
         prix (toujours), l'ISO, les arêtes et la DDV (si vides). Ce qui est
         saisi à la main n'est jamais écrasé. */
      const ent = (field === "codeArticle") ? catalogueSuggestion(String(val || "")) : null;
      const entIso = (field === "ref") ? catalogueParIso(String(val || "")) : null;
      const cible = ent || entIso;
      if(cible) appliquerSuggestionCatalogue(l, cible);
    }
  } else if(outilId){''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("patch A (v2) applique")
