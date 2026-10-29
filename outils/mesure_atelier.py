# Mesure du mode atelier — le critère de la feuille de route (annexe)
# Usage : python mesure_atelier.py <URL du bilan_economique.html>
# Critère : code de sortie 0 (aucun texte < 12 px, AUCUN élément interactif
# < 56 px de haut sur les cinq écrans, aucune erreur JS).
# v4.129.1 (Tour 108, brief Benjamin) : la mesure des interactifs s'étend à
#   a, button, input, select, textarea, summary, [onclick], [role=button] —
#   et elle parcourt la saisie d'essai, la vue d'ensemble, la synthèse,
#   Matis et Transmettre (menu ouvert).
# Exclusions assumées : les éléments à font-size 0 (volontairement masqués —
# ex. le 🔒 du bandeau verrouillé) et les interactifs invisibles (rect nul,
# display:none — les écrans non affichés).
# pip install playwright && playwright install chromium
import asyncio, json, sys
from playwright.async_api import async_playwright
URL = sys.argv[1]

ECRANS = [
    ("saisie d'essai", "ouvrirAtelier()"),
    ("vue d'ensemble", "ouvrirAccueil()"),
    ("synthese", "document.getElementById('syntheseBtn').click()"),
    ("matis", "ouvrirMatis()"),
    ("transmettre", "document.getElementById('transmettreBtn').click()"),
]

JS_MESURE = """()=>{
  const out={tiny:0,nText:0,tinyList:[],interactifs:0,petits:[]};
  const vis=e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);
    return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
  const SEL='a, button, input, select, textarea, summary, [onclick], [role=button]';
  for(const e of document.body.querySelectorAll('*')){
    if(!vis(e)) continue;
    const fs=parseFloat(getComputedStyle(e).fontSize);
    if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())){
      out.nText++;
      if(fs<12&&fs>1){ out.tiny++;
        out.tinyList.push(fs+'px '+e.tagName+'.'+String(e.className).split(' ')[0]); }
    }
  }
  for(const e of document.body.querySelectorAll(SEL)){
    if(!vis(e)) continue;
    out.interactifs++;
    const h=e.getBoundingClientRect().height;
    if(h<56){ const et=(e.textContent||e.value||'').trim().slice(0,24);
      out.petits.push(Math.round(h)+'px '+e.tagName+(e.type?('['+e.type+']'):'')
        +'.'+String(e.className).split(' ')[0]+' «'+et+'»'); }
  }
  return out;}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context(viewport={'width':1180,'height':820},
                                         has_touch=True)).new_page()
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(URL); await pg.wait_for_timeout(2500)
        await pg.evaluate("window._spkSetMode('atelier')")
        await pg.wait_for_timeout(800)
        r = await pg.evaluate("()=>({tiny:0,nText:0,interactifs:0,petits:[],mode:document.documentElement.getAttribute('data-mode')})")
        r['mode'] = await pg.evaluate("document.documentElement.getAttribute('data-mode')")
        r['ecrans'] = {}
        for nom, action in ECRANS:
            await pg.evaluate("()=>{ try{ fermerPanneaux(); }catch(e){} try{ document.body.click(); }catch(e){} }")
            await pg.wait_for_timeout(300)
            await pg.evaluate("()=>" + action)
            # 2200 ms et non 900 : la passe du plancher 12 px est throttlée
            # (200 ms) mais peut durer plus sur un gros écran — mesurer trop
            # tôt compte des textes transitoires en cours de remontée
            # (constaté sur la Vue d'ensemble : 156 textes à 900 ms, 0 à 2200).
            await pg.wait_for_timeout(2200)
            m = await pg.evaluate(JS_MESURE)
            m['petits'].sort()
            r['ecrans'][nom] = m
            r['tiny'] += m['tiny']; r['nText'] += m['nText']
            r['interactifs'] += m['interactifs']; r['petits'] += [nom+' :: '+x for x in m['petits']]
        r['errors']=errs
        print(json.dumps(r, indent=1, ensure_ascii=False))
        ok = r['tiny']==0 and not r['petits'] and not errs and r['mode']=='atelier'
        await b.close(); sys.exit(0 if ok else 1)
asyncio.run(main())
